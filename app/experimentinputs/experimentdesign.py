class ExperimentDesign:

    def __init__(self):
        self.assays = set() # Of assay names
        self.num_chambers =  None
        self.stack_height = None
        self.dontmix = [] # Of (assayA, assayB)
