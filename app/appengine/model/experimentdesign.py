class ExperimentDesign:
    """
    Encapsulates the mandate for the allocation experiment.
    Includes a few factory functions, and some convenience queries.
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
        design.targets_present = {'G', 'H'}
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

    @classmethod
    def make_from_params(cls, assays, chambers, replicas, dontmix, targets):
        exp = ExperimentDesign()
        exp.assay_types = set([chr(ord('A') + i) for i in range(assays)])
        for assay_type in exp.assay_types:
            exp.replicas[assay_type] = replicas
        exp.num_chambers = chambers

        # Use the first <N> assays as the targets present.
        sorted_assay_types = sorted(list(exp.assay_types))
        for i in range(targets):
            exp.targets_present.add(sorted_assay_types[i])

        # Use <N> assay-pairs that draw members from either end of the list as
        # the dontmix pairs.
        exp.dontmix = []
        for i in range(dontmix):
            a = sorted_assay_types.pop()
            b = sorted_assay_types.pop(0)
            exp.dontmix.append([a, b])

        return exp


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


    def all_assay_types_as_single_string(self):
        """
        Provides a string like this: 'ABCDE,...'
        """
        return ''.join(sorted((self.assay_types)))

    def dontmix_as_single_string(self):
        """
        Provides a string like this: 'AB ST'
        """
        pairs = []
        for pair in self.dontmix:
            chalk, cheese = sorted(pair, key=lambda pair: pair[0])
            pair = '%s%s' % (chalk, cheese)
            pairs.append(pair)
        return ' '.join(pairs)

    def targets_as_single_string(self):
        return ''.join(sorted(list(self.targets_present)))


