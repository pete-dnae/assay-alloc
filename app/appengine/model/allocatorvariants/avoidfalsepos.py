from itertools import combinations

from model.allocation import Allocation
from model.possibletargets import PossibleTargets
from model.assay import Assay

class AvoidsFP:
    """
    Provides an allocation algorithm based on avoiding all possible false positives, 
    no matter which targets are present.
    """


    def __init__(self, experiment_design):
        """
        Provide an ExperimentDesign object.
        """
        self._design = experiment_design
        # Prepare an Allocation object with which to register allocation
        # decisions as they progress.
        self.alloc = Allocation(experiment_design.num_chambers)
        # Prepare the set of all possible target sets to consider during the
        # allocation process..
        self._possible_target_sets = PossibleTargets.create(
            experiment_design, (2,3))


    def allocate(self):
        """
        Entry point to the allocation algorithm.
        """

        # Work through the assay types in the priority order specified by
        # the experiment design.
        for assay_type in self._design.assay_types_in_priority_order():
            self._allocate_all_replicas_of_this_assay_type(assay_type)

        return self.alloc


    #------------------------------------------------------------------------
    # Private below.
    #------------------------------------------------------------------------

    def _allocate_all_replicas_of_this_assay_type(self, assay_type):
        """
        Decide where to allocate all the replicas of the given assay type and
        update our Allocation object with this new status.
        """
        # Prepare the legal, possible, candidate chamber sets of the right size
        # for the number of replicas wanted for this assay. For example, if
        # we want 3 replicas of assay A, this data structure will look like
        # this:
        # ( {1,2,7}, {1,2,8}, ... {3,5,9} ... )

        chambers = self.alloc.all_chambers()
        self._remove_incompatible_chambers(chambers, assay_type)
        replicas = self._design.replicas[assay_type]
        possible_chamber_sets = self._draw_possible_chamber_sets_of_size(
            chambers, size=replicas)

        # Use the first chamber set we can find in this set, that cannot 
        # stimulate a false positive, regardless of which set of targets is
        # present.

        for chamber_set in possible_chamber_sets:
            ok = self._chamber_set_works_for_assay(chamber_set, assay_type)
            if ok:
                print('XXX for assay %s, we are using chamber set %s' %
                (assay_type, chamber_set))
                self._register_allocation(chamber_set, assay_type)
                return
        raise RuntimeError('Cannot allocate: %s' % assay_type)


    def _chamber_set_works_for_assay(self, chamber_set, assay_type):
        """
        Can we gaurantee that using the given set of chambers to home all 
        replicas of the given assay type, this cannot create false positives, 
        regardless of which targets are present?
        """


        # We can conclude that this chamber set works, provided that, for
        # all possible target set possibilities, at least one of the chambers
        # in the set does not contain any of the targets in that target set.

        for target_set in self._possible_target_sets.sets:
            # As soon as we encounter a target set for which this chamber
            # set does not work, we can conclude immediately that the chamber
            # set does not work.
            works =  self._chamber_set_works_for_target_set(
                chamber_set, target_set)
            if not works:
                return False

        return True


    def _chamber_set_works_for_target_set(self, chamber_set, target_set):
        """
        Does at least one of the chambers in the given chamber set, NOT
        contain any of the targets in the given target set?
        """
        for chamber in chamber_set:
            occupants = self.alloc.assay_types_present_in(chamber)
            assays_in_common = occupants.intersection(target_set)
            number_of_assays_in_common = len(assays_in_common)
            if number_of_assays_in_common == 0:
                return True
        return False


    def _remove_incompatible_chambers(self, chambers, assay_type):
        """
        Remove (in place), all the chambers from the given set of chambers
        that contain assays that must not be mixed with the given assay 
        type.
        """
        chambers_to_remove = set()
        for chamber in chambers:
            occupants = self.alloc.assay_types_present_in(chamber)
            willmix = self._design.can_this_assay_type_go_into_this_mixture(
                assay_type, occupants)
            if not willmix:
                chambers_to_remove.add(chamber)
        chambers = chambers - chambers_to_remove

    def _draw_possible_chamber_sets_of_size(self, chambers, size):
        sets = set()
        [sets.add(frozenset(c)) for c in combinations(chambers, size)]
        return sets


    def _register_allocation(self, chamber_set, assay_type):
        for i, chamber in enumerate(chamber_set):
            replica = i + 1
            assay = Assay(assay_type, replica)
            self.alloc.allocate(assay, chamber)
