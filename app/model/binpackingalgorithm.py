class BinPackingAlg(object):
    """
    The BinPackingAlg class provides a thing that knows how to produce a
    PlacementSolution from an ExperimentMandate. It encapsulates an
    algorithmic approach and relevant heuristics.
    """

    def __init__(self, experiment_mandate):
        self._exp_mandate = experiment_mandate


    def solve(self):
        """
        On success returns a PlacementSolution.
        On failure raises a NoSolutionError.
        """
        return self._solve()


    #---------------------------------------------------------------------------
    # Private below
    #---------------------------------------------------------------------------

    #---------------------------------------------------------------------------
    # Design note.
    #
    # Several of the methods below take a PlacementProgress argument.
    # The contract in each case with the caller, is that this object will not be
    # mutated.
    # In the case when a method wants to communicate back to the caller that
    # its operation has resulted in a changed placement model - it does so by 
    # returning a COPY of the incoming object - suitably mutated.
    # 
    #---------------------------------------------------------------------------
        
    def _solve(self):
        """
        Private entry point to the algorithm.

        An outer loop that iterates over all the assays called for by the
        experiment mandate. An inner loop that iterates until sufficient
        replicates of that assay have been placed.

        Raises NoSolutionError if no solution can be found.
        """
        placement_progress = PlacementProgress()
        assays = self._exp_mandate.assay_collection.assays
        replicates_required = self._exp_mandate.replicates
        for assay in assays:
            for replicate in range(replicates_required):
                location_demand = LocationDemand(assay)
                # The call below generates recursion.

                # Note how this call both consumes and then overwrites
                # the placement_progress object.
                placement_progress = self._place_assay_somewhere(
                        location_demand, placement_progress)
        solution = PlacementSolution(placement_progress)
        return solution


    def _place_assay_somewhere(self, location_demand, placement_progress):
        """
        Places the assay specified in the given LocationDemand, in any chamber 
        that satisfies the following:
        o  Does not contain A<n> already.
        o  Would not cause a colocation that is disallowed.
        o  Any generated, knock-on location demands can also be satisfied
          (recursively).

        It tries target chambers in a heuristic-precedence order.

        When successful, it returns a copy of the incoming placement_progress, 
        updated accordingly.

        When it fails it raises NoSolutionError.
        """
        chambers_tried = set()
        while True:
            fart move heuristics out
            next_chamber_to_try = self._most_promising_legal_untried_chamber(
                    placement_progress, chambers_tried)
            if next_chamber_to_try is None:
                raise NoSolutionError()
            succeeded, updated_placement_progress = \
                    self._attempt_to_place_assay_here(
                            location_demand.assay, next_chamber_to_try,
                            placement_progress)
            chambers_tried.add(next_chamber_to_try)
            if succeeded:
                return updated_placement_progress


    def _attempt_to_place_assay_here(self, assay, chamber, placement_progress):
        """
        Places the assay specified in location_demand into the chamber
        specified. Then works out what knock-on effect location demands can be
        inferred because of new colocations created, and recursively satisfies
        these also.

        Returns a 2-tuple in which the first element is a success boolean.

        When successful, the second element is a copy of the incoming
        placement_progress object - updated accordingly.
        """
        local_progress = placement_progress.copy()
        local_progress.place_assay_here(location_demand.assay, chamber)

        # Work out if this assay placement created any new colocations, and when
        # so, the corresponding additional allocations we must make to
        # disambiguate calling the assay.
        generator = LocationDemandGenerator(location_demand, local_progress)
        generated_location_demands = generator.generate()

        # And we must satisfy these demands also, for the initial placement to
        # be viewed as a success. (Recursively).
        for new_location_demand in generated_location_demands.demands:
            try:
                # The recursive call.
                local_progress = self._place_assay_somewhere(
                        new_location_demand, local_progress)
            except NoSolutionError as e:
                return False, None
        return True, local_progress

fart use class names in comments more
