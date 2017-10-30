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
    def make_from_html_input_form_dict(cls, form_dict):
        assays = int(form_dict['assays'])
        chambers = int(form_dict['chambers'])
        replicas = int(form_dict['replicas'])
        dontmix = int(form_dict['dontmix'])
        targets = int(form_dict['targets'])

        design = cls.make_from_params(
            assays, chambers, replicas, dontmix, targets)
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


    def set_of_all_chambers(self):
        return set([i + 1 for i in range(self.num_chambers)])


    def can_this_assay_go_into_this_mixture(self, assay, mixture):
        """
        Is it legal to add the given assay to a chamber that already
        contains the given mixture. (set() of assay types).
        """
        return self.can_this_assay_type_go_into_this_mixture(
                assay.type, mixture)


    def can_this_assay_type_go_into_this_mixture(self, assay_type, mixture):
        # Not legal if this assay type already present.
        if assay_type in mixture:
            return False
        # Not legal if would create an illegal pairing.
        for chalk, cheese in self.dontmix:
            if (chalk in mixture) and (assay_type == cheese):
                return False
            if (cheese in mixture) and (assay_type == chalk ):
                return False
        return True


    def all_assay_types_as_single_string(self):
        """
        Provides a string like this: 'ABCD...O'
        """
        letters = ''.join(sorted((self.assay_types)))
        if len(letters) < 7:
            return letters
        start_fragment = letters[:3]
        end_fragment = letters[-1:]
        return start_fragment + ' ... ' + end_fragment


    def assay_types_in_priority_order(self):
        """
        Provides a sequence of assay types in the order in which they
        should be allocated.
        """
        # Use alphabetical order for now.
        return sorted(self.assay_types)

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


