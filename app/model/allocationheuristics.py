class AllocationHeuristics:
    """
    The AllocationHeuristics class is a helper for the BinPackingAlgorithm.
    It is separated out, so that the bin packing algorithm can be limited to cold
    logic, and delegate out matters of judgement and tradeoffs to this class.

    Isolating the heuristics this way means they can be changed without affecting
    other parts of the code, and the logic is more amenable to being unit tested.
    """

    def __init__(self):
        pass


    def next_chamber_to_try(location_demand, chambers_to_exclude, allocation):
        """ 
        Makes a judgement call, about which chamber in the given Allocation
        object would make the most fertile (and legal) choice to consider next 
        to satisfy the LocationDemand object provided.

        Returns a chamber number of None.

        Legal is defined as:

            o  Not containing the incoming assay already.
            o  Would not contravene the colocation exclusions specifed in the
               LocationDemand.
            o  Not being a chamber that is excluded by the exclusion list 
               passed in.
            o  Not being a chamber that this chamber in the Allocation 
               provided has barred.

        A most fertile chamber is defined using this precedance:

            o  Contains fewer assays already than rivals.
        """

        return chamber
