class ChamberColocations:
    """
    The ChamberColocations class encapsulates the set of ColocatedAssayPair(s)
    that exist in a given chamber.
    """

    def __init__(chamber):
        self.chamber = chamber
        self._colocated_pairs = set()


    def add_pair(self, colocated_assay_pair):
        self._colocated_pairs.add(colocated_assay_pair)


