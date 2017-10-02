class Solver(object):
    """
    The Solver class can take high-level responsibility for creating a
    PlacementSolution, by "choosing" a bin packing algorithm, introducing it to a
    an experimental mandate, and firing its solve() method.
    """

    def __init__(self, experimental_mandate):
        self.experimental_mandate = experimental_mandate


    def solve(self):
        # This is where we could drop in a different algorithm variant.
        algorithm = BinPackingAlgorithm()

        solution = algorithm.solve(self.experimental_mandate)
        return solution
