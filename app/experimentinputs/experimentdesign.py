class ExperimentDesign:

    def __init__(self):
        # Apparatus and mandate.
        self.assay_types = set() # Of assay names, e.g. 'B'.
        self.replicas = {} # Replica count, keyed on assay type.
        self.num_chambers =  None
        self.dontmix = [] # Of 2-tuples, e.g. ['chalk', 'chees']

        # Simulated test to run.
        self.targets_present = set() # Of assay names.


    @classmethod
    def make_reference_example(cls):
        design = ExperimentDesign()
        LETTERS = 'ABCDEFGHIJKLMN'
        design.assay_types = set(LETTERS)
        for i, _type in enumerate(LETTERS):
            # We mix {2,3,4} as our replica numbers.
            how_many = 2 + (i % 3)
            design.replicas[_type] = how_many
        design.num_chambers = 8
        design.dontmix = [['A', 'B'], ['C', 'D']]
        design.targets_present = ['G', 'H']
        return design

