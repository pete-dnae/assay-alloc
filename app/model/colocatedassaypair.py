class ColocatedAssayPair(object):
    """
    The ColocatedAssayPair class encapsulates two assays that are colocated in
    a chamber in terms of the assay names and the chamber.
    """

    def __init__(self, assay_a, assay_b, chamber):
        self.assay_a = assay_a
        self.assay_b = assay_b
        self.chamber = chamber
