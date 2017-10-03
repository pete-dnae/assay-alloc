from copy import deepcopy

class Allocation:
    """
    The Allocation class models the state of assays having been allocated to a
    set of chambers. It includes not only which assays have been allocated to
    which chamber, but also metadata. For example which assays are barred from
    certain chambers during subsequent evolution of this Allocation.

    Note chambers are numbered from 1, not zero.
    """

    # Implementation warning
    #
    # This class has a copy method that uses copy.deepcopy() under the hood.
    # So developer! - beware of inadvertanetly adding reference members that
    # bring in a long tail of downstream references.

    def __init__(self, num_chambers):
        self.num_chambers = num_chambers

        # Holds allocation info about each chamber. Keyed on chamber number.
        # Values are _ChamberData objects.
        self.chambers_info = {}
        for i in range(num_chambers):
            chamber = i + 1
            self.chambers_info[chamber] = _ChamberMeta(chamber)


    def place_assay_here(self, assay, chamber):
        chamber_meta = _ChamberMeta(chamber)
        self.chambers_info[chamber].add_assay(assay)


    def bar_this_assay_from_chamber(self, assay, chamber):
        chamber_info = self.chambers_info[chamber]
        chamber_info.add_barred_assay(assay)


    def copy(self):
        return deepcopy(self)

    


class _ChamberMeta:
    """
    Models stuff we no about one chamber.
    """

    def __init__(self, chamber):
        self.assays = set()

        # The barred attribute holds a sequence of assays that are no longer
        # allowed in this chamber because of prior allocation decisions.
        self.now_barred = set()


    def add_assay(self, assay):
        self.assays.add(assay)


    def add_barred_assay(self, assay):
        self.now_barred.add(assay)
