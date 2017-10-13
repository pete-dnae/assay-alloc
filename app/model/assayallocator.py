import copy

from model.allocation import Allocation
from model.pool import Pool

class AssayAllocator:

    def __init__(self, experiment_design):
        self._design = experiment_design
        self.allocation = Allocation(experiment_design.num_chambers)

    def allocate(self):
        """
        Entry point to the allocation algorithm.
        """
        pool = Pool(self._design)
        # We make a copy of the set of assays in the pool to iterate over,
        # so that we are free to deplete the pool itself inside the loop.
        assays = pool.assays_present_in_deterministic_order()
        self._allocate_from_pool_until_get_stuck(assays, pool)
        #self._attempt_to_finish_allocation_by_swapping_assays(pool)
        if len(pool.assays) == 0:
            return self.allocation
        # Failed to allocate everything.
        raise RuntimeError(
                'Allocation failed because these were left over: %s' % str(pool))


    #------------------------------------------------------------------------
    # Private below.
    #------------------------------------------------------------------------

    def _allocate_from_pool_until_get_stuck(self, assays, pool):
        """
        Iterates over the assays in the pool in the sequence stipulated
        allocating those that can be allocated, and removing from the pool
        those placed.
        """
        for assay in assays:
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
        chamber_seq = self.allocation.chambers_in_fewest_occupants_order()
        for chamber in chamber_seq:
            legal = self._can_this_assay_go_here(assay, chamber)
            if legal:
                self.allocation.allocate(assay, chamber)
                return True
        return False


    def _can_this_assay_go_here(self, assay, chamber):
        """
        Is the given assay compatible with the given chamber?
        """
        # Not legal if this assay type already present.
        incumbent_types = self.allocation.assay_types_present_in(chamber)
        if assay.type in incumbent_types:
            return False
        # Not legal if would create an illegal pairing.
        for chalk, cheese in self._design.dontmix:
            if (chalk in incumbent_types) and (assay == cheese):
                return False
            if (cheese in incumbent_types) and (assay == chalk):
                return False
        return True
