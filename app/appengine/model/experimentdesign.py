class ExperimentDesign:
    """
    Encapsulates the mandate for the allocation experiment.
    Includes a few factory functions, and some convenience queries.
    """

    def __init__(self):
        # Apparatus and mandate.
        self.assay_types = set() # Of assay names, e.g. 'B', or 'Staph-C'.
        self.num_chambers =  None # E.g. 24
        self.sim_targets = None # Simultaneously present targets limit. E.g. 5
        self.dontmix = []  # Of 2-tuples, e.g. ['chalk', 'cheese']


    @classmethod
    def make_from_html_input_form_dict(cls, form_dict):
        raise RuntimeError('Not implemented')
        assays = int(form_dict['assays'])
        sim_targets = 0
        chambers = int(form_dict['chambers'])
        dontmix = int(form_dict['dontmix'])

        design = cls.make_from_params(assays, sim_targets, chambers, dontmix)
        return design

    @classmethod
    def make_from_params(cls, assays, chambers, sim_targets, dontmix):
        exp = ExperimentDesign()
        exp.assay_types = set([chr(ord('A') + i) for i in range(assays)])
        exp.sim_targets = sim_targets
        exp.num_chambers = chambers

        # Use <N> assay-pairs that draw members from either end of the list as
        # the dontmix pairs.
        exp.dontmix = []
        sorted_assay_types = exp.assay_types_in_priority_order()
        for i in range(dontmix):
            a = sorted_assay_types.pop() # last
            b = sorted_assay_types.pop(0) # first
            exp.dontmix.append([a, b])

        return exp


    def set_of_all_chambers(self):
        return set([i + 1 for i in range(self.num_chambers)])


    def can_this_assay_go_into_this_mixture(self, assay, mixture):
        """
        Is it legal to add the given assay to a chamber that already
        contains the given mixture. (set() of assay types).
        """
        # Not legal if this assay type already present.
        if assay in mixture:
            return False
        # Not legal if would create an illegal pairing.
        for chalk, cheese in self.dontmix:
            if (chalk in mixture) and (assay== cheese):
                return False
            if (cheese in mixture) and (assay == chalk ):
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
