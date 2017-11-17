"""
# OVERVIEW

This algorithm tries to allocate multiple copies of a set of assays into
chambers combinatorially in such a way that each assay type gets a *reserved*
set of chambers, which, when they all *fire* guarantees the detection of that
assay's target. Regardless, that is, of which other assay targets might also be
present.  In other words, it guarantees to prevent false positive calls.

- Presents an algorithm for allocation that balances chamber utilization while
  keeping the chamber sets for each assay maximally different from each other
  for as long as possible.
- Requires no set operations - all based on simple loops with modulo 
  arithmetic.
- Represent the allocation of assays to chambers as boolean flags
  in a binary word where each bit position corresponds to a chamber.
- Then describes what I have called the size of the intersection set, as either
  crosstalk or correlation. These are conceptually identical.
- The algorithm deals with each level of multiplicity in successive passes.
- The algorithm sacrifices correlation progressively.

Exploiting Patterns

- The allocation forms a repeating pattern
- The first row is the allocation of the first assay, and can be thought of
  as a bit field.
- Subsequent rows turn out to be the row above right shifted (wrapping round at
  the ends) by one bit.
- The pattern means we can put to one side what has been said before and
  explore an arithmetic way to generate just the first row, based on the
  experiment parameters.
"""

from model.allocation import Allocation
from model.assay import Assay

class DiagonalsAllocator:
    """
    Provides an allocation algorithm based on avoiding all possible false 
    positives, no matter which targets are present. Uses a diagonal pattern
    heuristic for allocation.
    """


    def __init__(self, experiment_design):
        """
        Provide an ExperimentDesign object when initialising the allocator..
        """
        self._design = experiment_design
        # Prepare an Allocation object with which to register allocation
        # decisions as they progress.
        self.alloc = Allocation()
        # The N+3 relation below is a logical necessisity. See external
        # reasoning.
        self._replicas = experiment_design.sim_targets + 3


    def allocate(self):
        """
        Entry point to the allocation algorithm.
        """
        first_row_template = self._compute_chambers_for_first_assay()
        self._allocate_all_assays(first_row_template)

        return self.alloc


    #------------------------------------------------------------------------
    # Private / implementation methods below.
    #------------------------------------------------------------------------

    def _compute_chambers_for_first_assay(self):
        chambers = []
        num_assays = len(self._design.assay_types)
        num_chambers = self._design.num_chambers
        # We do these calcs with zero-based chamber indices to match
        # Arthur's doc.
        for replica in range(self._replicas):
            chamber = (num_assays * replica) % num_chambers
            # If this is a diagonal we already used, move to the next
            # unused diagonal.
            if chamber in chambers:
                chamber = self._next_unused(chamber, chambers)
            chambers.append(chamber)
        return chambers


    def _next_unused(self, chamber, chambers):
        # We get (num_chambers -1) bites at this cherry.
        num_chambers = self._design.num_chambers
        for count in range(num_chambers - 1):
            new_chamber = (chamber + 1 + count) % num_chambers
            if new_chamber not in chambers: # Diagonal not yet used.
                return new_chamber
        raise RuntimeError('No unused diagonals left')


    def _allocate_all_assays(self, first_row_template):
        # Incoming first row template is zero-based chamber numbers.
        for count, assay in enumerate(
                self._design.assay_types_in_priority_order()):
            shift_amount = count
            self._allocate_assay(assay, shift_amount, first_row_template)

    def _allocate_assay(self, assay, shift_amount, first_row_template):
        # Incoming first row template is zero-based chamber numbers.

        # Continue in zero-based chamber numbers.
        chambers = [(c + shift_amount) % self._design.num_chambers for 
                c in first_row_template]

        # Flip to one-based chamber numbers at last minute.
        chamber_set = [c + 1 for c in chambers]
        chamber_set = frozenset(chamber_set)
        self._assert_sufficiently_different_from_previous_sets(
                assay, chamber_set)
        self.alloc.allocate(assay, chamber_set)

        # nd frozenset([1, 5, 9, 13, 17, 21]))

    def _assert_sufficiently_different_from_previous_sets(
                self, assay, incoming_chamber_set):
        max_overlap = self._design.sim_targets - 1
        for prev_assay in self.alloc.all_assays():
            prev_chambers = self.alloc.chambers_for(prev_assay)
            intersection = incoming_chamber_set.intersection(prev_chambers)
            overlap = len(intersection)
            if overlap > max_overlap:
                msg = _EXCESS_OVERLAP % (assay, incoming_chamber_set,
                    prev_chambers, prev_assay, overlap, max_overlap)
                raise RuntimeError(msg)


_EXCESS_OVERLAP = \
"""
The allocation for <%s>, which is %s,
is too similar to %s, which was used
for <%s>. They have %d chambers in common, which is > the %d permitted.


"""
