from collections import defaultdict
from itertools import combinations
import math
import os

class Allocation:
    """
    Encapsulates a state model of which assays are allocated to which 
    chambers. And offers a set of convenience queries.
    """

    def __init__(self):
        self._assay_to_chamber_set = {}
        self._chamber_set_to_reserving_assay = {}
        self._chamber_to_assays = defaultdict(set)


    def allocate(self, assay, chamber_set):
        self._assay_to_chamber_set[assay] = chamber_set
        self._chamber_set_to_reserving_assay[chamber_set] = assay
        for chamber in chamber_set:
            self._chamber_to_assays[chamber].add(assay)

    def unreserve_alloc_for(self, assay):
        # Make temp copy of chambers involved.
        chamber_set = self._assay_to_chamber_set[assay]
        del(self._chamber_set_to_reserving_assay[chamber_set])
        chamber_set = tuple(chamber_set)
        del(self._assay_to_chamber_set[assay])
        for chamber in chamber_set:
            occupants = self._chamber_to_assays[chamber]
            self._chamber_to_assays[chamber] = occupants - {assay}

        
    # ------------------------------------------------------------------------
    # Chamber-centric queries
    # ------------------------------------------------------------------------

    def reserved_chamber_sets(self):
        """
        Provides information about which chamber sets have been reserved
        so far.
        Returns a set of frozensets of int.
        """
        return set(self._assay_to_chamber_set.values())


    def all_chambers(self):
        return set(self._chamber_to_assays.keys())


    def chambers_for(self, assay):
        return self._assay_to_chamber_set[assay]


    def is_chamber_set_already_reserved(self, chamber_set):
        return chamber_set in self._chamber_set_to_reserving_assay


    # ------------------------------------------------------------------------
    # Assay-centric queries
    # ------------------------------------------------------------------------

    def assay_types_present_in(self, chamber):
        res =  set([assay for assay in self._chamber_to_assays[chamber]])
        return res

    def assay_is_present_in_all_of(self, assay, chamber_set):
        for chamber in chamber_set:
            occupants = self.assay_types_present_in(chamber)
            if assay not in occupants:
                return False
        return True

    def which_assay_reserved_this_chamber_set(self, chamber_set):
        return self._chamber_set_to_reserving_assay[chamber_set]

    def max_colocation(self):
        """
        How many assays in the most occupied chamber?
        """
        counts = [len(self.assay_types_present_in(c)) for 
                c in self.all_chambers()]
        return max(counts)
            

    # ------------------------------------------------------------------------
    # Reports
    # ------------------------------------------------------------------------

    def format_chambers(self, columns):
        """
        Provides a table showing which assays are in which chambers, in the
        form of one big single string.
        """
        width = self.max_colocation()
        chambers = [self.format_chamber(chamber, width) for chamber in 
                    self.all_chambers()] 
        rows = []
        for i in range(int(math.ceil(len(chambers) / float(columns)))):
            start = i *columns
            end = start + columns
            row_chambers = chambers[start: end]
            row_str = ' '.join(row_chambers)
            rows.append(row_str)
        return os.linesep.join(rows)

    def format_chamber(self, chamber, width):
        """
        Provides a string like this: '007 [BF]'
        """
        assays = self._chamber_to_assays[chamber]
        assays = sorted(assays)
        assays = ''.join(assays)
        return '%03d [%-*s]' % (chamber, width, assays)

    def format_calling_table_for(self, assay_sequence):
        rows = []
        for assay in assay_sequence:
            chambers = sorted(self.chambers_for(assay))
            chambers = [('%2d' % c) for c in chambers]
            chambers = ' '.join(chambers)
            line = '%s: %s' % (assay, chambers)
            rows.append(line)
        return os.linesep.join(rows)
        
