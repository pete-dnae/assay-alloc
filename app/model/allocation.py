from collections import defaultdict

class Allocation:
    """
    Encapsulates a model of which Assay(s) are allocated to which chambers.
    And offers a set of convenience queries.
    """

    def __init__(self, num_chambers):
        self._chamber_to_assays = defaultdict(set) # Of Assay(s)
        self._assay_type_to_chambers = defaultdict(set) # Of int(s)


    def allocate(self, assay, chamber):
        self._chamber_to_assays[chamber].add(assay)
        self._assay_type_to_chambers[assay.type].add(chamber)


    # Chamber-centric queries

    def which_chambers_contain_assay_type(self, assay_type):
        return self._assay_type_to_chambers[assay_type]


    def which_chambers_contain_assay_types(self, assay_types):
        res = set()
        for assay_type in assay_types:
            res = res.union(self.which_chambers_contain_assay_type(assay_type))
        return res


    def number_of_chambers_that_contain_assay_type(self, assay_type):
        return len(self.which_chambers_contain_assay_type(assay_type))


    # Assay centric queries


    def assay_types_present_in(self, chamber):
        return set([assay.type for assay in self._chamber_to_assays[chamber]])

    def number_of_this_assay_type_allocated(self, assay_type):
        return len(self._assay_type_to_chambers[assay_type])



