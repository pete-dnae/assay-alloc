from collections import defaultdict
from itertools import combinations

class Allocation:
    """
    Encapsulates a state model of which assays are allocated to which 
    chambers. And offers a set of convenience queries.
    """

    def __init__(self):
        self._assay_to_chamber_set = {}
        self._chamber_to_assays = defaultdict(set)


    def allocate(self, assay, chamber_set):
        self._assay_to_chamber_set[assay] = chamber_set
        for chamber in chamber_set:
            self._chamber_to_assays[chamber].add(assay)
        
    # ------------------------------------------------------------------------
    # History-based queries
    # ------------------------------------------------------------------------

    def reserved_chamber_sets(self):
        """
        Provides information about which chamber sets got used up till now
        for which assays.
        Returns a set of 2-tuples: (assay, chamber_set)
        """
        res = set()
        for assay, chamber_set in self._assay_to_chamber_set.items():
            res.add((assay, frozenset(chamber_set)))
        return res

    # ------------------------------------------------------------------------
    # Chamber-centric queries
    # ------------------------------------------------------------------------

    def all_chambers(self):
        return set(self._chamber_to_assays.keys())


    def chambers_for(self, assay):
        return self._assay_to_chamber_set[assay]


    def chamber_set_is_reserved_by_assay(self, chamber_set, assay):
        return self._assay_to_chamber_set[assay] == chamber_set


    # ------------------------------------------------------------------------
    # Assay-centric queries
    # ------------------------------------------------------------------------

    def assay_types_present_in(self, chamber):
        return set([assay for assay in self._chamber_to_assays[chamber]])

    def assay_is_present_in_all_of(self, assay, chamber_set):
        for chamber in chamber_set:
            occupants = self.assay_types_present_in(chamber)
            if assay not in occupants:
                return False
        return True

    # ------------------------------------------------------------------------
    # Reports
    # ------------------------------------------------------------------------

    def format_chambers(self):
        lines = []
        for chamber in self.all_chambers():
            lines.append(self.format_chamber(chamber))
        return (lines)

    def format_chamber(self, chamber):
        assays = self._chamber_to_assays[chamber]
        assays = sorted(assays)
        assays = ','.join(assays)
        return '%03d %s' % (chamber, assays)
