class BinPackingAlg(object):
    """
    The BinPackingAlg class provides a thing that knows how to produce a
    PlacementSolution from an ExperimentalMandate. It encapsulates an
    algorithmic approach and relevant heuristics.
    """

    def __init__(self, experimental_mandate):
        self._experimental_mandate = experimental_mandate


    def solve(self):
        placement_solution = do_packing_things()
        return placement_solution

    #---------------------------------------------------------------------------
    # Private below
    #---------------------------------------------------------------------------
        
    def do_packing_things(self):
        return None
