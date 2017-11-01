"""
ALGORITHM EXPLANATION

We use the terms assays and targets almost interchangeably. 

We iterate over assay types in some priority order. E.g. (A,B,C...Q) etc.  In
each iteration we allocate all of the replicas of that assay (P) to a chamber
set. For example if 3 replicas are needed for (P), we might decide to use
{1,2,9}.  We refer to that chamber set as the chamber set that has been
*reserved* by assay (P).  It is reserved in the sense that we want to be able
to rely on the fact that when all of {1,2,9} fire, that is an unequivocal
indicator that (P) is present.  It follows that we must make sure there can be
no reason for all of {1,2,9} to fire when (P) is not present.  Regardless, that
is, of what other targets might be present. This is to guarantee there can be
no false positives.

We describe the allocation as a whole as *vulnerable* (to false positive
calls), when there is some particular combinations of targets that could be
present, which would cause all of the chambers in one of the reserved chamber
sets to fire, when its intended target is not present.

Our approach as we incrementally consider each assay type (P) in turn, is to
hypothesise chamber sets that we might use to house P's replicas. We consider
all legal chamber set possibilities (of the right size) in fact. For example:
{1,2,3}, {1,2,4}, {1,2,5}... {17,12,24} ... etc. Legal being defined as 
allocations that do not break the don't-mix rules.

To measure the *vulnerability* we must consider target sets that might be
present. For example {A} on its own, or {A,B}, or {A,N,F} and so on. In fact we
look at all the possible target sets that could be present. (See Note 001 
below).

If we can find, for any of our reserved chamber sets e.g. {1,2,9}, a potential
targets-present set (e.g. {A,B,C,D} that would cause all of {1,2,9} to fire
despite the assay that reserved it not being present, we can conclude that
that particular allocation state, as a whole, is *vulnerable*.

When this happens we reject that chamber-set hypothesis as a home for the assay
type under consideration (P), and move on to consider the next hypothesis. If
we exhaust the possible chamber sets to use for (P), we are stuck and have
to abort. Conversely, if we make it to the end of the assays types which are
mandated by the experiment, we know we have produced an invulnerable allocation
scheme.

It is necessary to revisit the vulnerability of the entire allocation afresh 
as we consider each assay type, because the conclusions we reached last time
round must be re-examined in the context of an additional assay having been
allocated. I.e. now that we have allocated the replicas of 'P' - does that
mean that the chambers in the reserved chamber set for 'O' could all fire
because of the newly added P's, despite 'O' not being present? Etc.

# Note (001) Optimizations, Limitations, and *IMPLICATIONS*.

The number of possible targets-present sets, goes up exponentially with how 
many simultaneously-present targets we wish to protect ourselves from.

If are working with 20 assay types:

-  there are    1140 possible target sets of size 3
-  there are    4845 possible target sets of size 4
-  there are  15,504 possible target sets of size 5
-  there are  38,760 possible target sets of size 6
-  there are  77,520 possible target sets of size 7
-  there are 125,970 possible target sets of size 8

The algorithm has a setting in it that makes it ignore target sets with more
than N members (n_targets). (To avoid very long allocation run-times). 
Currently set to 5.

The algorithm does not bother with any target sets smaller than this upper 
limit either, because these cannot cause false positives that the larger sets
will not as well.

You cannot choose the number of replicas (n_replicas) independently of 
(n_targets). n_replicas must be > n_targets, or the allocation is vulnerable
(by definition).

To verify this assertion. Consider n_replicas = 3, and n_targets = 3. We
reserved {1,4,7} for assay 'P'. It is inevitable there exists a set of 3
targets that when present would cause {1,4,7} to fire despite 'P' not being
present? Any set that contains a representative assay drawn from the occupants
of each of {1,4,7} would do. Conversely, if we raise n_replicas to 4 and use
for example {1,4,7,14}, and leave n_targets at 3. We stand a chance of finding
a set of 3 targets that will not cause all of {1,4,7,14} to fire.
"""

from itertools import combinations

from model.allocation import Allocation
from model.possibletargets import PossibleTargets
from model.assay import Assay

class AvoidsFP:     # FP = False-Positive
    """
    Provides an allocation algorithm based on avoiding all possible false 
    positives, no matter which targets are present.
    """

    """
    A NOTE ON VARIABLE NAMING CONVENTIONS

    This code, in places, adopts a naming convention that is intended to convey
    both the generic nature of the variable, as well as a concrete example.

    Like this:

        chamber_set_147     # A chamber set that could be {1,4,7}
        target_set_ADFN     # A set of targets that could be {A,D,F,N}
        assay_P             # An assay type that could be P

    """


    def __init__(self, experiment_design):
        """
        Provide an ExperimentDesign object when initialising the allocator..
        """
        self._design = experiment_design
        # Prepare an Allocation object with which to register allocation
        # decisions as they progress.
        self.alloc = Allocation()
        # Prepare the set of all possible (hypothetical) target sets to 
        # consider during the allocation process.
        # NB, there are circa tens-of-thousands of these if we draw from a 
        # 20-member superset, and constrain the subsets to 5 or fewer members.
        number_of_targets = 4
        self._possible_target_sets = PossibleTargets.create(
            experiment_design, number_of_targets)


    def allocate(self):
        """
        Entry point to the allocation algorithm.
        """

        # Work through the assay types in the priority order specified by
        # the experiment design, and for each, allocate all the replicas
        # in one go.
        for assay_P in self._design.assay_types_in_priority_order():
            self._allocate_all_replicas_of_this_assay_type(assay_P)

        return self.alloc


    #------------------------------------------------------------------------
    # Private / implementation methods below.
    #------------------------------------------------------------------------

    def _allocate_all_replicas_of_this_assay_type(self, assay_P):
        """
        Find homes for all the replicas of assay_P.
        """
        # We will choose and use, a particular set of chambers to house the 
        # replicas for this assay type.

        # The allocation object keeps track of what chamber set we decided
        # upon (reserved) for each assay.

        # So we first prepare the candidate chamber sets - a set of sets of
        # requisite size.
        # That might look something like this, if we require 3 replicas for
        # assay_P: 
        # { {1,2,7}, {1,2,8}, ... {3,5,9} ... }

        chambers = self._design.set_of_all_chambers()
        chambers = self._remove_incompatible_chambers(chambers, assay_P)
        num_replicas = self._design.replicas[assay_P]
        possible_chamber_sets = self._draw_possible_chamber_sets_of_size(
            chambers, size=num_replicas)

        # Work through all the potential chamber sets, and use the first set 
        # we encounter that does not put the overall allocation into a
        # vulnerable state. (Where it can produce false positives.)

        for chamber_set_147 in possible_chamber_sets:
            # We cannot consider chamber sets which have already been
            # reserved for another assay.
            if self.alloc.is_chamber_set_already_reserved(chamber_set_147):
                continue
            # Would adding assay_P to this chamber set make the allocation
            # as a whole  vulnerable?
            vulnerable = self._is_allocation_with_assay_P_added_vulnerable(
                assay_P, chamber_set_147)

            # If it is not vulnerable, we need look no further. We've found a
            # suitable set of chambers for assay_P, so we tell our allocation
            # object to register and reserve them thus.

            if not vulnerable:
                print('XXX reserving %s for %s' % (chamber_set_147, assay_P))
                self.alloc.allocate(assay_P, chamber_set_147)
                return
            # If we get to here, that chamber set is vulnerable. Never mind,
            # let's move on to the net chamber set hypothesis.

        # If we get here, we couldn't find a suitable chamber set and have
        # to give up and abort.
        raise RuntimeError('Cannot allocate: %s' % assay_P)


    def _is_allocation_with_assay_P_added_vulnerable(
            self, assay_P, chamber_set_for_P):
        """
        Would the current allocation state, once assay_P is added into the
        suggested chamber set, become vulnerable to false postives?
        """

        # The rule here is that the resultant allocation is vulnerable, if any
        # of the reserved chamber sets we've established so far have any reason
        # to all-fire, other than because their reserving-assay is present
        # among the targets present.

        # Temporarily, add in assay_P as instructed.
        self.alloc.allocate(assay_P, chamber_set_for_P)

        # Ostensibly, we will consider all the previously reserved chamber
        # sets, but we can skip those of them that we haven't touched when
        # adding assay_P's replicas. (Their vulnerability cannot have been
        # changed).
        reserved_chamber_sets = set()
        for chamber_set in self.alloc.reserved_chamber_sets():
            if chamber_set.intersection(chamber_set_for_P):
                reserved_chamber_sets.add(chamber_set)

        # The outer loop iterates over those of the already-reserved 
        # chamber sets that could have become vulnerable.
        for reserved_chamber_set in reserved_chamber_sets:
            # This inner loop iterates over all the possible targets-present 
            # sets that could exist.
            for target_set_ADFN in self._possible_target_sets.sets:
                # Would all the chambers in the set fire in the presence of 
                # this targets-present set?
                all_would_fire =  self._all_would_fire(
                    reserved_chamber_set, target_set_ADFN)

                if all_would_fire:
                    # If so, are they doing so spuriously?
                    if self._spurious_fire(
                            reserved_chamber_set, target_set_ADFN):
                        # So we can return immediately, concluding that
                        # the allocation as a whole is vulnerable, but first
                        # we must back-out the temporary allocation.
                        self.alloc.unreserve_alloc_for(assay_P)
                        return True

        # To have got this far, we can conclude that the allocation as a whole
        # is not vulnerable, but first we must back out the temporary
        # allocation.
        self.alloc.unreserve_alloc_for(assay_P)
        return False


    def _all_would_fire(self, chamber_set_147, target_set_ADFN):
        """
        Would the presence of the targets {A,D,F,N} cause all of the chambers
        {1,4,7} to fire?
        """
        for chamber in chamber_set_147:
            occupants = self.alloc.assay_types_present_in(chamber)
            # Only needs one chamber to have no occupants in common
            # with the target set to conclude False.
            if len(occupants.intersection(target_set_ADFN)) == 0:
                return False
        return True

    def _spurious_fire(self, chamber_set, target_set_ADFN):
        """
        If all the chambers in the given reserved chamber set fired, have
        they done so, despite the reserving assay not being present among the 
        targets?
        """
        reserving_assay = self.alloc.which_assay_reserved_this_chamber_set(
                chamber_set)
        if reserving_assay in target_set_ADFN: # Not spurious.
            return False
        return True # Is spurious.


    def _remove_incompatible_chambers(self, chambers, assay_P):
        """
        Make (and return) a copy of the given set of chambers, from which
        have been removed, any chambers with existing occupants incompatible
        with adding in the given assay_P.
        """
        chambers_to_remove = set()
        for chamber in chambers:
            occupants = self.alloc.assay_types_present_in(chamber)
            legal = self._design.can_this_assay_type_go_into_this_mixture(
                assay_P, occupants)
            if not legal:
                chambers_to_remove.add(chamber)
        return chambers - chambers_to_remove


    def _draw_possible_chamber_sets_of_size(self, chambers, size):
        """
        Provide all the chamber subsets of size <size> that are available 
        from the set given. Returns the collection of subsets as a sorted 
        sequence for two reasons. Firstly to place desirable choices nearer
        the beginning, and secondly to make the algorithm deterministic to help
        with automated testing.
        """
        subsets = []
        [subsets.append(frozenset(c)) for c in combinations(chambers, size)]

        def _how_crowded(chamber_set):
            return sum([len(self.alloc.assay_types_present_in(c)) 
                    for c in chamber_set])

        return sorted(subsets, key=_how_crowded)
