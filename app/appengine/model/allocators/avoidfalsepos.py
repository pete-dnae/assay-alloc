"""
Definition of how this algorithm works.

Nb. In what follows we use the terms assays and targets almost interchangeably. 

We iterate over assay types in some priority order.  And in each iteration we
allocate all of the replicas of that assay to a chamber set. For example if 3
replicas are needed it could be {1,2,9}.  We refer to that chamber set as the
chamber set that has been *reserved* by that assay.  It is reserved in the
sense that we want to be able to rely on the fact that when all the chambers in
that set fire, that is an uniequivocal indicator that the target that reserved
it is present.  It follows that we must make sure there can be no reason for
all of those chambers to fire when its target is not present.  Regardless, that
is, of what other targets might be present. This is to guarantee there can be 
no false positives.

We describe the allocation as a whole as vulnerable (to false positive calls),
when there is some particular combinations of targets that could be present,
which would cause all of the chambers in one of the reserved chamber sets to
fire, when its intended target is not present.

Our approach as we incrementally consider each assay type in turn, is to
hypothesise chamber sets that we might use to home its replicas. We consider
all legal chamber set possibilities in fact. Legal being allocations that do
not break the don't-mix rules.

To measure the vulnerability we must consider target sets that might be
present. In fact we look at all the possible (reasonable) target sets that
could be present. Reasonable meaning we only consider up to maybe 5 targets
present simultaneously. (Configurable).  If we can find for any of our reserved
chamber sets, a potential targets-present set that would cause all its chambers
to fire despite the assay that reserved it not being present, we can conclude
that the allocation as a whole is vulnerable.

When this happens we reject that chamber-set hypothesis as a home for the assay
type under consideration, and move on to consider the next hypothesis.

It is necessary to revisit the vulnerability of the allocation as a whole at
each stage, because the logical vulnerability conclusions must account for
all the assays allocated so far.
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
        sizes_wanted = (1,2,3,4,5)
        self._possible_target_sets = PossibleTargets.create(
            experiment_design, sizes_wanted)


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
            # If it doesn't, we need look no further. We've found a suitable 
            # set of chambers for assay_P, so we tell our allocation object
            # to register and reserve them thus.
            if not vulnerable:
                print('XXX reserving %s for %s' % (chamber_set_147, assay_P))
                self.alloc.allocate(assay_P, chamber_set_147)
                return
            # Never mind, let's move on to the net chamber set hypothesis.

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

        # Ostensibly we will consider all the previously reserved chamber
        # sets, but we can skip those of them that we haven't touched when
        # adding assay_P's replicas. (Their vulnerability cannot have been
        # changed).
        reserved_chamber_sets = set()
        for chamber_set in self.alloc.reserved_chamber_sets():
            if chamber_set.intersection(chamber_set_for_P):
                #print('XXX keeping %s' % chamber_set)
                reserved_chamber_sets.add(chamber_set)
            else:
                #print('XXX NOT keeping %s' % chamber_set)
                pass

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
