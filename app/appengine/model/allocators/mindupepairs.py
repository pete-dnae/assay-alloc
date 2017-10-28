import copy

from model.allocation import Allocation
from model.pool import Pool
from model.targetsethypothesese import TargetSetHypothesese

class MinDupePairs:
    """
    Encapsulates an allocation algorithm that is based on miminimizing the
    number of duplicated co-located assay type pairs..
    """


    def __init__(self, experiment_design):
        """
        Provide an ExperimentDesign object.
        """
        self._design = experiment_design
        self.alloc = Allocation(experiment_design.num_chambers)

        # These are for unit tests only - so that the affect of individual
        # parts of the combined heuristics can be isolated and tested more
        # easily.
        self._defeat_chamber_number_hueristic = False
        self._defeat_existing_occupant_count_heuristic = False
        self._defeat_false_positive_probability_heuristic = True
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

        # We prepare in-advance, a set of all the target-sets that could be
        # present in the experiment (up to size 3), for use in the downstream
        # algorithms.
        target_set_hypothesese = TargetSetHypothesese.create(self._design)

        self._allocate_from_pool_until_get_stuck(
            ordered_assays, pool, target_set_hypothesese)
        if len(pool.assays) == 0:
            return self.alloc
        # Failed to allocate everything.
        raise RuntimeError(
                'Allocation failed because these were left over: %s' % str(pool))


    #------------------------------------------------------------------------
    # Private below.
    #------------------------------------------------------------------------

    def _allocate_from_pool_until_get_stuck(
            self, ordered_assays, pool, target_set_hypothesese):
        """
        Iterates over the assays in the pool in the sequence stipulated
        allocating those that can be allocated, and removing from the pool
        those placed.

        The caller must provide a TargetSetHypothesese object.
        """
        for assay in ordered_assays:
            ok = self._allocate_this_assay_if_possible(
                assay, target_set_hypothesese)
            if ok:
                pool.assays.remove(assay)


    def _allocate_this_assay_if_possible(self, assay, target_set_hypothesese):
        """
        Place the given assay into a chamber in the context of the current
        allocation state. Tries all chambers, but uses a chamber-desirability
        heuristic.

        The caller must provide a TargetSetHypothesese object.
        """

        # We re-evaluate the preferential chamber order, for each assay afresh,
        # because it changes after each successful allocation.
        self._tracing = (assay == self._assay_to_trace)
        self._t('Tracing: %s' % assay)

        chamber_seq = self._chambers_in_desirability_order(
            assay, target_set_hypothesese)

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


    def _chambers_in_desirability_order(self, assay, target_set_hypothesese):
        """
        Sort the chambers available into an order that places the most
        desirable ones for placing the assay first - taking into account
        the properties of the current allocation state thus far.

        Caller must inject a TargetSetHypothesese object.
        """

        # First cut out chambers that would be illegal for this assay type.
        chambers = self._all_legal_chambers_for(assay)

        # One of the filters needs to know what co-located assay pairs are
        # already present in the allocation, so we capture that here to avoid
        # doing it repeatedly inside the (implied) loop.
        pairs = self.alloc.unique_assay_type_pairs()

        # Now sort repeatedly, using the heuristics in lowest to highest
        # precedence order.

        self._sort_by_chamber_number(
            chambers)
        self._sort_by_occupant_count(
            chambers)
        self._sort_by_duplicate_pair_creation(
            chambers, pairs, assay)
        self._sort_by_false_positive_probability(
            chambers, assay, target_set_hypothesese)

        return chambers


    def _all_legal_chambers_for(self, assay):
        """
        Provides a list of chambers that can legally accomodate the given
        assay.
        """
        chambers = []
        for chamber in self.alloc.all_chambers():
            incumbent_mix = self.alloc.assay_types_present_in(chamber)
            if self._design.can_this_assay_go_into_this_mixture(
                    assay, incumbent_mix):
                chambers.append(chamber)
        return chambers


    def _sort_by_chamber_number(self, chambers):
        """
        Sorts (in situ) the given list of chambers, according to chamber
        number (lowest first). This method only exists to make the call-site
        which also calls similar sorting methods - follow a uniform pattern.
        """
        if self._defeat_chamber_number_hueristic:
            return
        chambers.sort()


    def _sort_by_occupant_count(self, chambers):
        """
        Sorts (in situ) the given list of chambers, according the number of
        assays already present in the chamber, (lowest first).
        """
        if self._defeat_existing_occupant_count_heuristic:
            return
        chambers.sort(key=lambda chamber: self._existing_occupant_count(chamber))


    def _sort_by_duplicate_pair_creation(self, chambers, existing_pairs, assay):
        """
        Considers the number of co-located assay pairs created by adding the
        given assay to a chamber. Scores each chamber in accordance with how
        many of these duplicate pairs already exist elsewhere in the
        allocation.

        Sorts (in situ) the given list of chambers, in accordance with the
        number of number of new duplicated assay pairs created. (Lowest first).
        """
        if self._defeat_duplicate_pairs_heuristic:
            return
        def comparator(
                chamber, assay_type=assay.type, existing_pairs=existing_pairs):
            return self._duplicate_pairs_made(
                chamber, assay_type, existing_pairs)
        chambers.sort(key=comparator)


    def _sort_by_false_positive_probability(
            self, chambers, assay, target_set_hypothesese):
        """
        Considers how likely it is that adding the given assay to a chamber,
        will produce a false-positive result. For example if we hypothesise
        that the experiment's targets are A,B, and C, then if the incoming
        assay is placed in a chamber such that all instances of the incoming
        assay are co-located with either A, or B, or C, we will set up a false
        positive. But we are blind of what the targets set is, so we we have to
        assess this measure in relation to all the possible target-set
        hypothesese.

        Sorts the (in situ) the given list of chambers, in accordance with
        how likely the creation of false-positives is. Least likely first.
        """
        if self._defeat_false_positive_probability_heuristic:
            return

        def comparator(
                chamber,
                assay_type=assay.type,
                target_set_hypothesese=target_set_hypothesese):
            potential = self._potential_for_false_positives(
                chamber, assay.type, target_set_hypothesese)
            return potential

        chambers.sort(key=comparator)


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
        """
        Provides the number of occupants in the given chamber.
        """
        count = self.alloc.how_many_assay_types_present_in(chamber)
        return count

    def _potential_for_false_positives(
                self, chamber, assay_type, target_set_hypothesese):
        """
        Returns how many of the hypotheses inside the
        TargetSetHypothesese would cause the placement of the given assay, in
        the given chamber to create a false positive calling for the given
        assay.
        """
        how_many = 0
        for target_set in target_set_hypothesese.sets:
            if self._sets_up_a_false_positive(
                    target_set, chamber, assay_type):
                how_many += 1
        return how_many

    def _sets_up_a_false_positive(self, target_set, chamber, assay_type):
        """
        Returns True if the placement of the given assay type in the given
        chamber, would produce an overall allocation such that every instance
        of the given assay type is in a chamber that already contains one of
        the assays in the given target set.
        """
        # Capture all the chambers that the incoming assay would end up
        # being in.
        chambers = self.alloc.which_chambers_contain_assay_type(assay_type)
        chambers.add(chamber)

        # If any of these chambers, does not contain any of the target set,
        # then we can conclude we won't have set up a false positive.
        for chamber in chambers:
            if len(self.alloc.assay_types_present_in(chamber).intersection(
                    target_set)) == 0:
                return False
        return True


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

