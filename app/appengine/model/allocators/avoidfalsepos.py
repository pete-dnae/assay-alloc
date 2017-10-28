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
        self.alloc = Allocation(experiment_design.num_chambers)
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
        # We will choose and use, a particular set of chambers to house this 
        # assay type.

        # So we first prepare the candidate chamber sets - a set of sets. 
        # That might look something like this: 
        # { {1,2,7}, {1,2,8}, ... {3,5,9} ... }

        chambers = self.alloc.all_chambers()
        self._remove_incompatible_chambers(chambers, assay_type)
        num_replicas = self._design.replicas[assay_type]
        possible_chamber_sets = self._draw_possible_chamber_sets_of_size(
            chambers, size=num_replicas)

        # Work through the possible chamber sets, and use the first set we
        # encounter that cannot stimulate a false positive for assay_P,
        # regardless of which set of targets is present.

        for chamber_set_147 in possible_chamber_sets:
            ok = self._chamber_set_works_for_assay(chamber_set_147, assay_P)
            if ok:
                self._register_allocation(chamber_set_147, assay_P)
                return
        raise RuntimeError('Cannot allocate: %s' % assay_P)


    def _chamber_set_works_for_assay(self, chamber_set_147, assay_P):
        """
        If we allocate all (3) replicas of assay_P, to chambers {1,4,7}, can we
        be certain that there is no fluke set of possible targets present,
        (for example {A,D,F,N}, that would cause all of {1,4,7} to fire.

        This would make {1,4,7} an unacceptable choice of chambers to house
        assay_P, because this fluke target presence would then emit a false 
        positive call for assay_P.
        """

        # Iterate over, and consider, each hypothetically-possible target-set
        # in turn. As soon as we reach one that would cause all of {1,4,7} to
        # fire, we can conclude immediately that chamber_set_147 is not
        # suitable.

        for target_set_ADFN in self._possible_target_sets.sets:
            all_would_fire =  
                self._all_would_fire(chamber_set_147, target_set_ADFN)
            if all_would_fire
                return False

        return True


    def _all_would_fire(self, chamber_set_147, target_set_ADFN):
        """
        Would the presence of the targets {A,D,F,N} cause all of the chambers
        {1,4,7} to fire?
        """
        for chamber in chamber_set_147:
            occupants = self.alloc.assay_types_present_in(chamber)
            if len(occupants.intersection(target_set)) == 0:
                return False
        return True


    def _remove_incompatible_chambers(self, chambers, assay_P):
        """
        Remove (in place), all the chambers from the given set of chambers
        into which it would be illegal (because of mixing rules) 
        to place assay_P.
        """
        chambers_to_remove = set()
        for chamber in chambers:
            occupants = self.alloc.assay_types_present_in(chamber)
            legal = self._design.can_this_assay_type_go_into_this_mixture(
                assay_type, occupants)
            if not legal:
                chambers_to_remove.add(chamber)
        chambers = chambers - chambers_to_remove


    def _draw_possible_chamber_sets_of_size(self, chambers, size):
        """
        Provide all the chamber subsets of size <size> that are available 
        from the set given.
        """
        subsets = set()
        [subsets.add(frozenset(c)) for c in combinations(chambers, size)]
        return subsets


    def _register_allocation(self, chamber_set, assay_type):
        """
        Update the state we are tracking of which assays have been allocated
        to which chambers - with the given mandate..
        """
        for i, chamber in enumerate(chamber_set):
            replica = i + 1
            assay = Assay(assay_type, replica)
            self.alloc.allocate(assay, chamber)
