from model.allocation import Allocation
from model.allocquery import AllocQuery
from model.pool import Pool

class AssayAllocator:

    def __init__(self, experiment_design):
        self._design = experiment_design
        self.allocation = Allocation()
        self.qry = AllocQuery(self.allocation)

    def allocate(self):
        """
        Entry point to the allocation algorithm.
        """
        pool = Pool(self._design)
        # We freeze an optimal sequence in which to try to allocated assays up
        # front, so that we are free to deplete the pool inside the loop.
        assay_sequence = self._optimal_sequence_from_pool()
        self._allocate_from_pool_until_get_stuck(assay_sequence, pool)
        #self._attempt_to_finish_allocation_by_swapping_assays(pool)
        if len(pool.assays) == 0:
            return self.allocation
        # Failed to allocate everything.
        raise RuntimeError(
                'Allocation failed because these were left over: %s' %
                ', '.join(pool))


    #------------------------------------------------------------------------
    # Private below.
    #------------------------------------------------------------------------

    def _allocate_from_pool_until_get_stuck(self, assay_sequence, pool):
        """
        Iterates over the assays in the pool in the sequence stipulated
        allocating those that can be allocated, and removing from the pool
        those placed.
        """
        for assay in assay_sequence:
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
        incumbent_types = self.qry.assay_types_present_in(chamber)
        if assay.type in incumbent_types:
            return False
        # Not legal if would create an illegal pairing.
        for chalk, cheese in self._design.dontmix:
            if (chalk in incumbent_types) and (assay == cheese):
                return False
            if (cheese in incumbent_types) and (assay == chalk):
                return False
        return True
