class BinPackingAlg:
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
    # Several of the methods below take an Allocation argument.
    # These are ALWAYS treated as immutable by the methods.
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
        allocation = Allocation()
        assays = self._exp_mandate.assay_collection.assays
        replicates_required = self._exp_mandate.replicates
        for assay in assays:
            for replicate in range(replicates_required):
                location_demand = LocationDemand(assay)
                # The call below generates recursion.

                # Note how this call both consumes and then overwrites
                # the allocation object.
                allocation = self._place_assay_somewhere(
                        location_demand, allocation)
        solution = PlacementSolution(allocation)
        return solution


    def _place_assay_somewhere(self, location_demand, allocation):
        """
        Places the assay specified in the given LocationDemand, with respect to
        the given current allocation, in any chamber that satisfies the 
        following:
        o  The rules in the LocationDemand.
        o  Any generated, knock-on location demands have also been satisfied
          (recursively).

        It tries target chambers in a heuristic-precedence order.

        When successful, it returns a copy of the incoming Allocation, 
        updated accordingly.

        When it fails it raises NoSolutionError.
        """
        chambers_tried = set()
        while True:
            legal_chambers = LocationDemandAssessor.chambers_that_satisfy_demand(
                    location_demand, allocation)
            available_chambers = legal_chambers - chambers_tried
            if len(available_chambers) == 0:
                raise NoSolutionError()
            next_chamber_to_try = AllocationHeuristics.preferred_chamber(
                    available_chambers, allocation)
            chambers_tried.add(next_chamber_to_try)

            succeeded, updated_allocation = \
                    self._attempt_to_place_assay_here(
                            location_demand.assay, next_chamber_to_try,
                            allocation)
            if succeeded:
                return updated_allocation


    def _attempt_to_place_assay_here(self, location_demand, chamber, allocation):
        """
        Places the assay specified in the given LocationDemand into the chamber
        specified. Then works out what knock-on effect LocationDemand(s) can be
        inferred because of new colocations created, and recursively satisfies
        these also.

        Returns a 2-tuple in which the first element is a success boolean.

        When successful, the second element is a copy of the incoming
        Allocation object - updated accordingly.
        """
        local_allocation = allocation.copy()
        local_allocation.place_assay_here(
                location_demand.assay, location_demand.chamber)

        # Work out if this assay placement created any new colocations, and when
        # so, the corresponding additional allocations we must make to
        # disambiguate calling the assay.
        generator = LocationDemandGenerator(location_demand, local_progress)
        new_location_demands = generator.generate()

        # And we must satisfy these demands also, for the initial placement to
        # be viewed as a success. (Recursively).
        for new_location_demand in new_local_demands:
            try:
                # The recursive call.
                local_assay = self._place_assay_somewhere(
                        new_location_demand, local_assay)
            except NoSolutionError as e:
                return False, None
        return True, local_assay
