import copy

from model.allocation import Allocation
from model.pool import Pool
from model.assay import Assay
from model.setcomparisons import SetComparisons

class AssayAllocator:

    # These allow unit test clients to dependency-inject, which heuristics
    # to enable in the allocate() method. Normal clients should use the
    # default value.
    H_CHAMBER = '_h_chamber'
    H_POPULATION_COUNT = '_h_pop_count'
    H_DUPE_PAIRS = '_h_dupe_pairs'

    def __init__(self, experiment_design):
        self._design = experiment_design
        self.alloc = Allocation(experiment_design.num_chambers)

    def allocate(
            self,
            which_heuristics={H_CHAMBER, H_POPULATION_COUNT,H_DUPE_PAIRS}):
        """
        Entry point to the allocation algorithm.
        """
        pool = Pool(self._design)
        # We make a copy of the set of assays in the pool to iterate over,
        # so that we are free to deplete the pool itself inside the loop.
        ordered_assays = pool.assays_present_in_deterministic_order()
        self._allocate_from_pool_until_get_stuck(
            ordered_assays, pool, which_heuristics)
        #self._attempt_to_finish_allocation_by_swapping_assays(pool)
        if len(pool.assays) == 0:
            return self.alloc
        # Failed to allocate everything.
        raise RuntimeError(
                'Allocation failed because these were left over: %s' % str(pool))


    #------------------------------------------------------------------------
    # Private below.
    #------------------------------------------------------------------------

    def _allocate_from_pool_until_get_stuck(
            self, ordered_assays, pool, which_heuristics):
        """
        Iterates over the assays in the pool in the sequence stipulated
        allocating those that can be allocated, and removing from the pool
        those placed.
        """
        for assay in ordered_assays:
            ok = self._allocate_this_assay_if_possible(assay, which_heuristics)
            if ok:
                pool.assays.remove(assay)


    def _allocate_this_assay_if_possible(self, assay, which_heuristics):
        """
        Place the given assay into a chamber in the context of the current
        allocation state. Tries all chambers, but uses a chamber-desirability
        heuristic.
        """
        # We re-evaluate the preferential chamber order, for each assay afresh,
        # because it changes after each successful allocation.
        chamber_seq = self._chambers_in_desirability_order(
            assay, which_heuristics)

        for chamber in chamber_seq:
            legal = self._design.can_this_assay_go_into_this_mixture(
                assay, self.alloc.assay_types_present_in(chamber))
            if legal:
                self.alloc.allocate(assay, chamber)
                return True
        return False


    def _chambers_in_desirability_order(self, assay, which_heuristics):
        """
        Sort the chambers available into an order that places the most
        desirable ones for placing the assay first - taking into account
        the properties of the current allocation state thus far.
        """

        # Our primary criteria is to minimise the creation of duplicated
        # co-located assay pairs. I.e. if one chamber already contains {A,B}
        # then it is beneficial to avoid creating another such pair somewhere
        # else, because this is wasting both calling and discrimination
        # abilities.

        # The second criteria is to prefer using chambers with fewer existing
        # occupants - so as to fill the chambers evenly.

        # The third is to prefer lower numbered chambers. This one is included
        # only to make the algorithm more intuitive, and it makes it
        # deterministic, which helps with testing.

        # First cut out chambers that already contain the incoming assay type
        # from the set to order.

        candidate_chambers = \
            [c for c in self.alloc.all_chambers()
             if assay.type not in self.alloc.assay_types_present_in(c)]

        # One of the filters needs to know what co-located assay pairs are
        # already present in the allocation, so we capture that here to avoid
        # doing it inside the (implied) loop.
        pairs = self.alloc.unique_assay_type_pairs()

        # Now sort the candidate chambers into desirability order.

        # We use the lowest precedence heuristics first.

        if self.H_CHAMBER in which_heuristics:
            candidate_chambers.sort() # Default key is chamber number itself.

        if self.H_POPULATION_COUNT in which_heuristics:
            candidate_chambers.sort(
                key=lambda chamber: self._existing_occupant_count(chamber))

        if self.H_DUPE_PAIRS in which_heuristics:
            candidate_chambers.sort(
                key=lambda chamber, assay_type=assay.type, existing_pairs=pairs:
                self._duplicate_pairs_made(chamber, assay_type, pairs))

        return candidate_chambers


    def _duplicate_pairs_made(self, chamber, assay_type, existing_pairs):
        """
        Preamble: The addition of the given assay type to the given chamber,
        will create new co-located assay pairs in the chamber, made up from
        each of the incumbents, paired with the incomer.

        This function returns a count of how many of these would be duplicates
        of co-located assay pairs that already exist in other chambers.
        """
        return 1
        count = 0
        for incumbent_type in self.alloc.assay_types_present_in(chamber):
            pair_made = {assay_type, incumbent_type}
            if pair_made in existing_pairs:
                count += 1
        return count


    def _existing_occupant_count(self, chamber):
        return 1
        # return self.alloc.assay_types_present_in(chamber)

