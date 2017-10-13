import copy

from model.allocation import Allocation
from model.pool import Pool

class AssayAllocator:

    def __init__(self, experiment_design):
        self._design = experiment_design
        self.alloc = Allocation(experiment_design.num_chambers)

    def allocate(self):
        """
        Entry point to the allocation algorithm.
        """
        pool = Pool(self._design)
        # We make a copy of the set of assays in the pool to iterate over,
        # so that we are free to deplete the pool itself inside the loop.
        ordered_assays = pool.assays_present_in_deterministic_order()
        self._allocate_from_pool_until_get_stuck(ordered_assays, pool)
        #self._attempt_to_finish_allocation_by_swapping_assays(pool)
        if len(pool.assays) == 0:
            return self.alloc
        # Failed to allocate everything.
        raise RuntimeError(
                'Allocation failed because these were left over: %s' % str(pool))


    #------------------------------------------------------------------------
    # Private below.
    #------------------------------------------------------------------------

    def _allocate_from_pool_until_get_stuck(self, ordered_assays, pool):
        """
        Iterates over the assays in the pool in the sequence stipulated
        allocating those that can be allocated, and removing from the pool
        those placed.
        """
        for assay in ordered_assays:
            ok = self._allocate_this_assay_if_possible(assay)
            if ok:
                pool.assays.remove(assay)


    def _allocate_this_assay_if_possible(self, assay):
        """
        Place the given assay into a chamber - trying all chambers, but
        favouring those with fewest occupants.
        """

        # We re-evaluate the preferential chamber order, for each assay afresh,
        # because it changes after each successful allocation.
        chamber_seq = self.alloc.chambers_in_fewest_occupants_order()
        for chamber in chamber_seq:
            legal = self._design.can_this_assay_go_into_this_mixture(
                assay, self.alloc.assay_types_present_in(chamber))
            if legal:
                self.alloc.allocate(assay, chamber)
                return True
        return False


