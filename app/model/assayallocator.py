from model.allocation import Allocation

class AssayAllocator:

    def __init__(self, experiment_design):
        self._design = experiment_design
        self.allocation = Allocation()
        self.qry = AllocQuery(self.allocation)

    def allocate(self):
        pool = Pool(experiment_design)
        self._allocate_from_pool_until_get_stuck(pool)
        #self._attempt_to_finish_allocation_by_swapping(pool)
        if pool.is_empty():
            return self.allocation
        # Failed to allocate everything.
        raise RuntimeError(
                'Allocation failed because these were left over: %s' %
                ', '.join(pool))


    #------------------------------------------------------------------------
    # Private below.
    #------------------------------------------------------------------------

    def _allocate_from_pool_until_get_stuck(self, pool):
        """
        Place just the most favourable assay choice from the pool into a chamber,
        if there is a chamber that will accept it. Then recurse to re-enter 
        this method without that assay in the pool.
        """
        assay = pool.most_favoured_assay()
        self._allocate_this_assay_if_possible(assay)
        pool.remove_assay(assay)
        self._allocate_from_pool_until_get_stuck(self, pool):


    def _allocate_this_assay_if_possible(self, assay):
        """
        Place the given assay into a chamber - trying all chambers. If one is
        available that will accept it.
        """
        for chamber in self._chambers_in_preference_order():
            succeeded = self._allocate_here_if_legal(assay, chamber)
            if succeeded
                return


    def _allocate_here_if_legal(self, assay, chamber):
        incumbent_types = self.qry.assay_types_present_in(chamber)
        if assay.type in incumbent_types:
            return
        wont_mix = self._design.assay_types_that_wont_mix_with(assay.type)
        if wont_mix.intersection(incumbent_types):
            return
        self.allocation.allocate(assay, chamber)


    def _chambers_in_preference_order(self):
        """
        Provide a sequence of all chambers, sorted according to how eager we are
        to put something in them.
        """

        # We favour chambers with the fewest occupants so far.
        return self.allocation.chambers_in_order_of_occupant_count()
