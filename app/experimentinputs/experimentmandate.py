class ExperimentMandate:
    """
    The ExperimentMandate class knows the constraints and parameters for the
    allocation problem to solve.
    """


    """
    Construct with integer parameters for number of chambers available and how
    many replicates are required, plus a DontMix object.
    """
    def __init__(self, num_chambers, replicates, dontmix):
        self.num_chambers =  num_chambers
        self.replicates = replicates
        self.dontmix = dontmix
