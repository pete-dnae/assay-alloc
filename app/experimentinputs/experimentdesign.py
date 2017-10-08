class ExperimentDesign:

    def __init__(self):
        self.assays = set() # Of assay names
        self.num_chambers =  None
        self.replicas = None
        self.dontmix = [] # Of (assayA, assayB)
