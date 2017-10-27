from collections import defaultdict
from itertools import combinations

class Allocation:
    """
    Encapsulates a state model of which Assay(s) are allocated to which 
    chambers. And offers a set of convenience queries.
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

    # ------------------------------------------------------------------------
    # Chamber-centric queries
    # ------------------------------------------------------------------------

    def all_chambers(self):
        return set(self._chamber_to_assays.keys())

    def which_chambers_contain_assay_type(self, assay_type):
        return self._assay_type_to_chambers[assay_type]


    def which_chambers_contain_assay_types(self, assay_types):
        res = set()
        for assay_type in assay_types:
            res = res.union(self.which_chambers_contain_assay_type(assay_type))
        return res

    def number_of_chambers_that_contain_assay_types(self, assay_types):
        chambers = self.which_chambers_contain_assay_types(assay_types)
        return len(chambers )


    def number_of_chambers_that_contain_assay_type(self, assay_type):
        return len(self.which_chambers_contain_assay_type(assay_type))


    # ------------------------------------------------------------------------
    # Assay-centric queries
    # ------------------------------------------------------------------------

    def assay_types_present_in(self, chamber):
        return set([assay.type for assay in self._chamber_to_assays[chamber]])

    def how_many_assay_types_present_in(self, chamber):
        return len(self.assay_types_present_in(chamber))

    def assays_present_in(self, chamber):
        return self._chamber_to_assays[chamber]

    def number_of_this_assay_type_allocated(self, assay_type):
        return len(self._assay_type_to_chambers[assay_type])

    def assay_type_pairs_in_chamber(self, chamber):
        """
        Provides the set of assay type pairs present in the given chamber.
        E.g. {{'A', 'B'}, {'B', 'C'},{'A', 'C'}}.
        This is a set-of-sets.
        Noting this from python reference:
        "To represent sets of sets, the inner sets must be frozenset objects"
        """
        pairs = set() # of frozenset
        types = self.assay_types_present_in(chamber)
        combis = combinations(types, 2)
        for a,b in combis:
            pair = frozenset((a,b))
            pairs.add(pair)
        return pairs


    def unique_assay_type_pairs(self):
        """
        Provides the set of assay type pairs present in all chambers.
        E.g. {frozenset{'A', 'B'}, frozenset{'B', 'C'}, frozenset{'A', 'C'}}
        """
        res = set()
        for chamber in self.all_chambers():
            pairs = self.assay_type_pairs_in_chamber(chamber)
            for pair in pairs:
                res.add(pair)
        return res

    # ------------------------------------------------------------------------
    # Reports
    # ------------------------------------------------------------------------

    def format_chambers(self):
        lines = []
        for chamber in self.all_chambers():
            lines.append(self.format_chamber(chamber))
        return (lines)

    def format_chamber(self, chamber):
        assays = self.assays_present_in(chamber)
        assays = sorted([str(a) for a in assays])
        assays = ','.join(assays)
        return '%03d %s' % (chamber, assays)






