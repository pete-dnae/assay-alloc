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
    A NOTE ON NOMENCLATURE

    This code, in places, adopts a naming convention that is intended to convey
    both the generic nature of the variable, as well as a concrete example.

    Like this:

        chamber_set_147     # A chamber set that could be {1,4,7}
        target_set_ADFN     # A set of targets that could be {A,D,F,N}
        assay_P             # An assay type that could be P

    """


    def __init__(self, experiment_design):
        """
        Provide an ExperimentDesign object.
        """
        self._design = experiment_design
        # Prepare an Allocation object with which to register allocation
        # decisions as they progress.
        self.alloc = Allocation()
        # Prepare the set of all possible (hypothetical) target sets to 
        # consider during the allocation process.
        # NB, there are circa tens-of-thousands of these if we draw from a 
        # 20-member superset, and constrain the subsets to 5 or fewer members.
        self._possible_target_sets = PossibleTargets.create(
            experiment_design, (1,2,3,4,5))


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
    # Private below.
    #------------------------------------------------------------------------

    def _allocate_all_replicas_of_this_assay_type(self, assay_P):
        """
        Find homes for all the replicas of assay_P.
        """
        # We will choose and use, a particular set of chambers to house the 
        # replicas for this assay type.

        # The allocation object keeps track of what chamber set we decided
        # upon for each assay.

        # So we first prepare the candidate chamber sets - a set of sets. 
        # That might look something like this, if we require 3 replicas for
        # assay_P: 
        # { {1,2,7}, {1,2,8}, ... {3,5,9} ... }

        chambers = self._design.set_of_all_chambers()
        chambers = self._remove_incompatible_chambers(chambers, assay_P)
        num_replicas = self._design.replicas[assay_P]
        possible_chamber_sets = self._draw_possible_chamber_sets_of_size(
            chambers, size=num_replicas)

        # Work through all the possible chamber sets, and use the first set 
        # we encounter that we are happy about from a false positives
        # point of view.

        for chamber_set_147 in possible_chamber_sets:
            vulnerable = self._is_allocation_with_assay_P_added_vulnerable(
                assay_P, chamber_set_147)
            if not vulnerable:
                self.alloc.allocate(assay_P, chamber_set_147)
                return
        # Couldn't find a suitable chamber set?
        raise RuntimeError('Cannot allocate: %s' % assay_P)


    def _is_allocation_with_assay_P_added_vulnerable(
            self, assay_P, chamber_set_for_P):
        """
        If we allocate all of the replicas of assay_P to chamber_set_for_P
        - does our allocation scheme up as far, and including
        assay_P become vulnerable to false positives - regardless of which
        targets are present?
        """
        # First we do a temporary allocation of assay_P's replicas to the
        # chamber set suggested. And do all our analysis is this
        # context.
        self.alloc.allocate(assay_P, chamber_set_for_P)

        # We have an outer loop here that considers all the possible
        # targets-present sets that could exist.

        # Then an inner loop that considers the reserved chamber-sets we have 
        # previously comitted to for each of the assays up to, and including P.

        # Inside the inner loop, we look to see if that particular combination
        # of targets-present, and that particular chamber set, would cause all
        # of the chambers in that set to fire for spurious reasons. The only
        # time it isn't spurious is when that particular chamber set has been
        # previously nominated as the special reserved chamber set to call
        # one of the assays we have covered and that assay is present in all
        # of the chambers.

        # As soon as the inner loop encounters such a condition - we have
        # an overall allocation scheme that would be vulnerable to false 
        # positives.

        # Outer loop for all possible targets-present sets...
        for target_set_ADFN in self._possible_target_sets.sets:
            # Inner loop for all previously reserved chamber sets.
            reserved_chamber_sets = self.alloc.reserved_chamber_sets()
            for prev_assay, reserved_chamber_set in reserved_chamber_sets:
                all_would_fire =  self._all_would_fire(
                    reserved_chamber_set, target_set_ADFN)
                if all_would_fire and \
                        self._spurious_fire(reserved_chamber_set, prev_assay):
                    # Before we return that the allocation scheme is
                    # vulnerable, we must de-allocate assay_P from the
                    # chamber set we temporarily allocated it to.
                    foo
                    return True
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

    def _spurious_fire(self, chamber_set_147, assay_P):
        """
        Returns true unless the given chamber set has been reserved by the 
        given assay, and that assay is present in all of the sets' chambers.
        """
        if self.alloc.chamber_set_reserved_by_assay(
                chamber_set_147, assay_P) and \
                self.alloc.assay_is_present_in_all_of(
                    assay_P, chamber_set_147):
            return False
        return True


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
        sequence, to gaurantee that iterating over them produces a 
        deterministic order, which is necessary for automated testing.
        """
        subsets = []
        [subsets.append(set(c)) for c in combinations(chambers, size)]
        return sorted(subsets)
