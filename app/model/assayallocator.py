import copy

from model.allocation import Allocation
from model.pool import Pool
from model.assay import Assay
from model.setcomparisons import SetComparisons

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
        using a chamber-desirability heuristic.
        """
        print('XXXX allocating: %s' % assay)
        # We re-evaluate the preferential chamber order, for each assay afresh,
        # because it changes after each successful allocation.
        chamber_seq = self._chambers_in_desirability_order(assay)
        for chamber in chamber_seq:
            legal = self._design.can_this_assay_go_into_this_mixture(
                assay, self.alloc.assay_types_present_in(chamber))
            if legal:
                self.alloc.allocate(assay, chamber)
                return True
        return False


    def _chambers_in_desirability_order(self, assay):
        """
        Sort the chambers available into an order that places the most
        desirable ones for placing the assay first.
        """

        """
        Our heuristic is formed by a ranking chambers using two measures,
        in precedence order.
        
        The first is to favour a chamber, that when the assay is added to it
        creates maximum variation of the mixes present. We measure this with
        respect to one rival cell using a set-difference, but normalised by
        dividing by the size of the set produced, so as to avoid favouring the
        production of large mixtures. Then we aggregate this measure for all the
        existing mixtures.
        
        The second precedence measure is to favour chambers with fewer 
        existing assays in them.
        
        There is a third, but only to make this algorithm deterministic, which
        is to favour lower numbered chambers.
        """
        # Sort according to our comparators, citing the highest precedence
        # criteria last in the list.
        chambers = self.alloc.all_chambers()
        """
        chambers = sorted(chambers,
                key = lambda chamber, assay_type=assay.type : (
                    self._chamber_number_order(chamber),
                    self._few_incumbents(chamber),
                    self._max_difference(chamber, assay_type)))
        """
        chambers = sorted(chambers,
                key = lambda chamber, assay_type=assay.type : (
                    self._max_difference(chamber, assay_type)))
        return chambers


    def _max_difference(self, chamber, assay_type):
        """
        Score the given chamber, by measuring how different the mixture created
        by adding the given assay type to this chamber would be, to all the
        mixes that are already present. Give lower scores to the highest
        differences.
        """
        if (assay_type == 'I'):
            foo = 42
        if (chamber == 25):
            foo = 42
        mix_created_here = self.alloc.assay_types_present_in(
            chamber).union(assay_type)
        other_chambers = self.alloc.all_chambers() - {chamber}
        other_mixes = []
        for other_chamber in other_chambers:
            other_mixes.append(self.alloc.assay_types_present_in(other_chamber))
        diff = SetComparisons.how_disimilar_from_most_similar_of_these(
            mix_created_here, other_mixes)
        if (assay_type == 'I'):
            print('XXXX  diff of for chamber %d is: %f' % (chamber, diff))
        return diff


    def _few_incumbents(self, chamber):
        """
        Score the given chamber, such that a chamber with fewer existing assay
        types in it gets a lower score.
        """
        return 1
        return self.alloc.assay_types_present_in(chamber)


    def _chamber_number_order(self, chamber):
        """
        Score the given chamber according to the chamber number, giving
        lower chamber numbers a lower score.
        """
        return 1
        return chamber

