class AllocationHeuristics:
    """
    The AllocationHeuristics class is a helper for the BinPackingAlgorithm.
    It is separated out, so that the bin packing algorithm can be limited to 
    irrefutable logic, but delegate out matters of choice or policy to something
    outside.

    Isolating the heuristics this way means they can be changed without affecting
    other parts of the code, and the logic is more amenable to being unit tested.
    """

    @classmethod
    def preferred_chamber(cls, available_chambers, allocation):
        """ 
        Makes a judgement call, about which chamber from the given set of 
        (pre-qualified) legal chambers would make the most fertile choice to 
        consider next. You provide an Allocation object so that the heuristics
        can look up various comparative properties of chambers using it.

        (Like how many assays already live in a particular chamber).
        """

        # The only heuristic we have so far, is to favour chambers which have
        # fewer assays in, over those which have more.

        return min(available_chambers, key=lambda chamber:
                allocation.number_of_assays_in_chamber(chamber))
