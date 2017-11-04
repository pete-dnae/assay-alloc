"""
ALGORITHM EXPLANATION

OVERVIEW


This algorithm tries to allocate multiple copies of a set of assays into
chambers combinatorially in such a way that each assay type gets a *reserved*
set of chambers, which, when they all *fire* guarantees the detection of that
assay's target, regardless of which other assay targets might also be present.
In other words, it guarantees to prevent false positive calls.

The algorithm is set-theoretic. Operating by modelling the interaction between 
sets of chambers, that contain assays with sets of assay targets.

It works by making irreversible decisions about where to allocate the first
assay, and then moving on to consider the next, using the previous decisions
(cumulatively) as constraints.


MULTIPLE TARGETS PRESENT

Our allocation scheme must avoid false positives even when multiple targets are
present. Say we choose to allocate assay P to the chamber set {1,2,9}. We say
that P has *reserved* this chamber set.  It is reserved in the sense that we
want to be able to rely on the fact that when all of {1,2,9} fire, that is an
unequivocal indicator that P's target is present.

It follows that we must make sure there can be no other reason for all of
{1,2,9} to fire when P's target is not present.  Regardless, that is, of what
other targets might be present. This is to guarantee there can be no false
positives.

In this example case, we have chosen 3 chambers. But this allocation cannot
prevent the possibility of false positives if we accept that 3 targets might be
present simultaneously. We can easily hypothesise a set of 3 targets that
excludes P, but which, when present, would cause all of {1,2,9} to fire despite
P not being present. We can conjure such a set simply by sampling a different 
existing assay from each of {1,2,9} and combining their targets into a set of
3.

It follows that we must set ourselves a reasonable upper limit for how many
targets might be present simultaneously (max_targets), and then allocate at
least one more than this number of each assay to avoid inevitable false 
positives scenarios.

This produces a mathematical relationship between how many chambers are 
required for a given number of assays, in the light of our compromise choice of
(max_targets). As follows...

<todo>


METHOD

We begin by noting how many replicas of each assay we must allocate. I.e.
max_targets + 1.

Then we hypothesis all the possible chamber sets that are available to us at
the beginning of the process to allocate each assay's replicas. I.e. all the
sets of size(replicas) that can be drawn from {all chambers}. We refer to this
as our *pool* of available chamber sets.

We allocate the replicas of the first assay, arbitrarily to the first chamber
set in the pool.

But that allocation step allows us to deduce that some of the chamber sets that
remain in the pool must no longer be consdidered candidates for subsequent
assay allocations; so we remove these from the pool before continuing to
allocating the next assay. And so on.

For the second and subsequent assays, we must also make sure we adhere to its
don't-mix rules. So instead of using simply the first chamber set from the
remaining pool, we use the first that we find in the pool that does not
contravene the mixing rules.


WHICH CHAMBER SETS MUST BE REMOVED

Here is an example of what we must avoid. We show the problem first to make it
easier to explain the remedy. Let max_targets = 3, and consequently replicas =
4.  We reserve {1,2,9,14} for P, and then reserve {1,9,11,22} for Q.  The
problem here is that {1,9,11,22} has two chambers in common with {1,2,9,14}.
Now consider a potential targets-present set of {P,M,S}. We know that the
presence of P will cause both {1,9} to fire. Hence we will generate a false
positive for Q, if {M,S} causes both {11,22} to fire. Which is inevitable if we
consider all the possibilities for {M,S}.

The generalisation of the situation that must be avoided, is that no chamber
set can be reserved to call an assay, if that chamber set has more than one
chamber in common, with any of the other reserved chamber sets.

So this defines the chamber sets we must remove from the pool after each assay
allocation (P). I.e. any chamber that has more than one chamber in common with
the chamber set used for P.

"""

from itertools import combinations

from model.allocation import Allocation
from model.possibletargets import PossibleTargets
from model.assay import Assay

class DeductionAllocator:
    """
    Provides an allocation algorithm based on avoiding all possible false 
    positives, no matter which targets are present.
    """


    def __init__(self, experiment_design):
        """
        Provide an ExperimentDesign object when initialising the allocator..
        """
        self._design = experiment_design
        # This is a diagnostics channel to support unit testing.
        # A few parts of the code send it messages to provide evidence that
        # something happened (if it is none none).
        self.tracer = None
        # Prepare an Allocation object with which to register allocation
        # decisions as they progress.
        self.alloc = Allocation()
        # Prepare the set of all possible (hypothetical) target sets to 
        # consider during the allocation process.
        # NB, there are circa tens-of-thousands of these if we draw from a 
        # 20-member superset, and constrain the subsets to 5 or fewer members.
        self._possible_target_sets = PossibleTargets.create(
            experiment_design, experiment_design.sim_targets)
        # This algorithm requires that the number of replicas that get
        # placed for each assay, be at least one greater than the largest
        # number of simultaneous targets being considered.
        self._replicas = experiment_design.sim_targets + 1
        # Prepare the pool of chamber sets, that we can consider when searching
        # for a home of each assay's replicas. We deplete this as we go.
        self._pool_of_chamber_sets = \
                self._initial_set_of_available_chamber_sets(self._replicas)


    def allocate(self):
        """
        Entry point to the allocation algorithm.
        """

        # Work through the assay types in the priority order specified by
        # the experiment design, and for each, allocate all the replicas
        # in one go.
        for assay_P in self._design.assay_types_in_priority_order():
            chamber_set_used = self._allocate_all_replicas_of_this_assay_type(
                    assay_P)
            self._curate_pool(chamber_set_used)

        return self.alloc


    #------------------------------------------------------------------------
    # Private / implementation methods below.
    #------------------------------------------------------------------------

    def _initial_set_of_available_chamber_sets(self, replicas):
        """
        Builds the initial set of chamber sets. (A set of sets), which can be 
        consdidered to house the replicas of each assay.
        """
        chambers = self._design.set_of_all_chambers()
        chamber_sets = self._draw_possible_chamber_sets_of_size(
                chambers, replicas)
        return chamber_sets


    def _draw_possible_chamber_sets_of_size(self, chambers, size):
        """
        Provide all the chamber subsets of size <size> that are available 
        from the set given. Returns the collection of subsets as a sorted 
        sequence for two reasons. Firstly to place desirable choices nearer
        the beginning, and secondly to make the algorithm deterministic to help
        with automated testing.
        """
        subsets = set()
        [subsets.add(frozenset(c)) for c in combinations(chambers, size)]
        return subsets

    def _allocate_all_replicas_of_this_assay_type(self, assay):
        """
        Find homes for all the replicas of assay(P). In the context of
        having previously allocated the replicas that precede assay(P) in
        allocation priority order.
        """
        print('XXX allocate all of %s' % assay)

        # Use the first chamber set we encounter (in desirability order),
        # that does not contravene the assay's mixing rules.
        chamber_set = self._most_desirable_legal_available_chamber_set(assay)
        if chamber_set is None:
            raise RuntimeError('Cannot allocate: %s' % assay)
        self.alloc.allocate(assay, chamber_set)
        return chamber_set

    def _most_desirable_legal_available_chamber_set(self, assay):
        """
        Down-select from the global available chamber sets, those that
        don't contravene the dont-mix rules for this assay. Then provide the
        most desirable thereof.
        """
        sets = [cs for cs in self._pool_of_chamber_sets if
                self._compatible(cs, assay)]
        if len(sets) == 0:
            return None

        def _how_crowded(chamber_set):
            return sum([len(self.alloc.assay_types_present_in(c)) 
                    for c in chamber_set])

        def _alphabetical(chamber_set):
            frags = ['%02d' % c for c in chamber_set]
            frags = ''.join(frags)
            return frags

        sets = sorted(sets, key=_alphabetical)
        sets = sorted(sets, key=_how_crowded)
        return sets[0]

    def _compatible(self, chamber_set, assay):
        """
        Is the given chamber set compatible with assay(P) being added, to all
        of its members - on the basis of assay(P)'s don't mix rules?
        """
        for chamber in chamber_set:
            occupants = self.alloc.assay_types_present_in(chamber)
            legal = self._design.can_this_assay_go_into_this_mixture(
                assay, occupants)
            if not legal:
                return False
        return True

    def _curate_pool(self, newly_reserved_chamber_set):
        """
        Remove from our pool of available chamber sets, any that has
        more than one member in common with the given set.
        """
        to_remove = [cs for cs in self._pool_of_chamber_sets if 
                len(cs.intersection(newly_reserved_chamber_set)) > 1]
        self._pool_of_chamber_sets = \
                self._pool_of_chamber_sets - set(to_remove)
