from collections import defaultdict

class Allocation:
    """
    Encapsulates a model of which Assay(s) are allocated to which chambers.
    And offers a set of convenience queries.
    """

    def __init__(self, num_chambers):
        self._chamber_to_assays = {} # set<Assay> keyed on chamber number.
        self._assay_type_to_chambers = defaultdict(set) # Of int(s)

        for i in range(num_chambers):
            chamber = i + 1
            self._chamber_to_assays[chamber] = set()


    def allocate(self, assay, chamber):
        self._chamber_to_assays[chamber].add(assay)
        self._assay_type_to_chambers[assay.type].add(chamber)


    # Chamber-centric queries

    def all_chambers(self):
        return set(self._chamber_to_assays.keys())

    def which_chambers_contain_assay_type(self, assay_type):
        return self._assay_type_to_chambers[assay_type]


    def which_chambers_contain_assay_types(self, assay_types):
        res = set()
        for assay_type in assay_types:
            res = res.union(self.which_chambers_contain_assay_type(assay_type))
        return res


    def number_of_chambers_that_contain_assay_type(self, assay_type):
        return len(self.which_chambers_contain_assay_type(assay_type))


    def chambers_in_fewest_occupants_order(self):
        """
        Provides a sequence of the chamber numbers with the chambers with
        fewest occupants coming first. Within sets of chambers having the same
        occupant count, the chamber are ordered in increasing chamber number.
        """
        occupant_count = {}
        for chamber, assays in  self._chamber_to_assays.items():
            occupant_count[chamber] = len(assays)
        all_chambers = self.all_chambers()
        sorted_chambers = sorted(
            all_chambers,
            key = lambda chamber: (occupant_count[chamber], chamber))
        return tuple(sorted_chambers)


    # Assay centric queries


    def assay_types_present_in(self, chamber):
        return set([assay.type for assay in self._chamber_to_assays[chamber]])

    def number_of_this_assay_type_allocated(self, assay_type):
        return len(self._assay_type_to_chambers[assay_type])



