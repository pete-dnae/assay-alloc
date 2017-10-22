import copy

from model.allocation import Allocation
from model.pool import Pool

class AssayAllocator:
    """
    Encapsulates the allocation algorithm.
    """


    def __init__(self, experiment_design):
        self._design = experiment_design
        self.alloc = Allocation(experiment_design.num_chambers)

        # These are for unit tests only - so that the affect of individual
        # parts of the combined heuristics can be isolated and tested more
        # easily.
        self._defeat_chamber_number_hueristic = False
        self._defeat_existing_occupant_count_heuristic = False
        self._defeat_duplicate_pairs_heuristic = False

        # Clients can set self._assay_to_trace to a particular Assay, e.g.
        # Assay('B', 3), in order to stimulate trace / diagnostic output while
        # that assay is being placed.
        self._assay_to_trace = None # E.g. Assay('B', 3)
        self._tracing = False

    def allocate(self):
        """
        Entry point to the allocation algorithm.
        """
        # Make a pool of all the assay replicas we are mandated to allocate.
        pool = Pool(self._design)

        # We make a copy of the set of assays in the pool to iterate over,
        # so that we are free to deplete the pool itself inside the loop.
        # We choose alphabetic order to make the order deterministic and also
        # because it's easier to follow when debugging.
        ordered_assays = pool.assays_present_in_alphabetic_order()
        self._allocate_from_pool_until_get_stuck(
            ordered_assays, pool)
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
        Place the given assay into a chamber in the context of the current
        allocation state. Tries all chambers, but uses a chamber-desirability
        heuristic.
        """

        # We re-evaluate the preferential chamber order, for each assay afresh,
        # because it changes after each successful allocation.
        self._tracing = (assay == self._assay_to_trace)
        self._t('Tracing: %s' % assay)
        chamber_seq = self._chambers_in_desirability_order(assay)

        # No legal candidates?
        if len(chamber_seq) == 0:
            self._t('Finished (failure) Tracing: %s' % assay)
            self._tracing = False
            return False

        # Allocation is possible. Use the first (most preferential) chamber.
        chamber = chamber_seq[0]
        self.alloc.allocate(assay, chamber)
        self._t('Finished (success) Tracing: %s' % assay)
        self._tracing = False
        return True


    def _chambers_in_desirability_order(self, assay):
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

        # First cut out chambers that would be illegal for this assay type.

        candidate_chambers = []
        for chamber in self.alloc.all_chambers():
            incumbent_mix = self.alloc.assay_types_present_in(chamber)
            if self._design.can_this_assay_go_into_this_mixture(
                    assay, incumbent_mix):
                candidate_chambers.append(chamber)

        self._t('Default chamber preference order: %s' % candidate_chambers)

        # One of the filters needs to know what co-located assay pairs are
        # already present in the allocation, so we capture that here to avoid
        # doing it inside the (implied) loop.
        pairs = self.alloc.unique_assay_type_pairs()

        # Now sort the candidate chambers into desirability order.

        # We sort repeatedly, using the heuristics in lowest to highest
        # precedence order.

        if not self._defeat_chamber_number_hueristic:
            candidate_chambers.sort() # Default key is chamber number itself.
        self._t('Chamber preference order using lowest chamber number: %s' %
                candidate_chambers)

        if not self._defeat_existing_occupant_count_heuristic:
            candidate_chambers.sort(
                key=lambda chamber: self._existing_occupant_count(chamber))
        self._t('Chamber preference order using, also, fewer occupants: %s' %
                candidate_chambers)

        if not self._defeat_duplicate_pairs_heuristic:
            candidate_chambers.sort(
                key=lambda chamber, assay_type=assay.type, existing_pairs=pairs:
                self._duplicate_pairs_made(chamber, assay_type, pairs))
        self._t('Final chamber preference order: %s' % candidate_chambers)

        return candidate_chambers


    def _duplicate_pairs_made(self, chamber, assay_type, existing_pairs):
        """
        Preamble: The addition of the given assay type to the given chamber,
        will create new co-located assay pairs in the chamber, made up from
        each of the incumbents, paired with the incomer.

        This function returns a count of how many of these would be duplicates
        of co-located assay pairs that already exist in other chambers.
        """
        count = 0
        pairs = []
        for incumbent_type in self.alloc.assay_types_present_in(chamber):
            pair_made = {assay_type, incumbent_type}
            if pair_made in existing_pairs:
                count += 1
                pairs.append(pair_made)
        self._t('Using chamber: %d, would create %d new, duplicate pairs: %s' %
                (chamber, count, pairs))
        return count


    def _existing_occupant_count(self, chamber):
        count = self.alloc.how_many_assay_types_present_in(chamber)
        return count


    # ------------------------------------------------------------------------
    # Diagnostics Support
    # ------------------------------------------------------------------------

    def _t(self, msg):
        """
        Trace
        """
        if self._tracing == False:
            return
        print('XXX TRACE %s' % msg)

