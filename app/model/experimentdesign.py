class ExperimentDesign:
    """
    Encapsulates the mandate for the allocation experiment.
    """

    def __init__(self):
        # Apparatus and mandate.
        self.assay_types = set() # Of assay names, e.g. 'B'.
        self.replicas = {} # Replica count, keyed on assay type.
        self.num_chambers =  None
        self.dontmix = []  # Of 2-tuples, e.g. ['chalk', 'cheese']

        # Simulated test to run.
        self.targets_present = set() # Of assay names.


    @classmethod
    def make_reference_example(cls):
        """
        This makes the canonical variant of an ExperimentDesign object for
        unit tests.
        """
        design = ExperimentDesign()
        LETTERS = 'ABCDEFGHIJKLMN'
        design.assay_types = set(LETTERS)
        for i, _type in enumerate(LETTERS):
            # We mix {2,3,4} as our replica numbers.
            how_many = 2 + (i % 3)
            design.replicas[_type] = how_many
        design.num_chambers = 8
        design.dontmix = [['A', 'H'], ['C', 'L']]
        design.targets_present = ['G', 'H']
        return design


    @classmethod
    def make_reference_example_without_dontmix(cls):
        """
        This makes the canonical variant of an ExperimentDesign object for
        unit tests, but not specifying any don't mix pairs.
        """
        design = cls.make_reference_example()
        design.dontmix = []
        return design


    def can_this_assay_go_into_this_mixture(self, assay, mixture):
        """
        Is it legal to add the given assay to a chamber that already
        contains the given mixture. (set() of assay types).
        """
        # Not legal if this assay type already present.
        if assay.type in mixture:
            return False
        # Not legal if would create an illegal pairing.
        for chalk, cheese in self.dontmix:
            if (chalk in mixture) and (assay.type == cheese):
                return False
            if (cheese in mixture) and (assay.type == chalk ):
                return False
        return True

    def format_all_assays(self):
        lines = []
        for _type in sorted(self.assay_types):
            assays = []
            for i in range(self.replicas[_type]):
                replica = i + 1
                assay = '%s%d' % (_type, replica)
                assays.append(assay)
            line_formatted = ' '.join(assays)
            lines.append(line_formatted)
        return lines

