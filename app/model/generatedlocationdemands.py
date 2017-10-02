class GeneratedLocationDemands(object):
    """
    The GeneratedLocationDemands class holds a set of LocationDemand(s), that
    have been generated or inferred to be necessary as a side effect of having
    just colocated A<n> with other assays in a chamber.
    """

    def __init__(self, demanding_chamber, demanding_assay):
        self.demanding_chamber =  demanding_chamber
        self.demanding_assay = demanding_assay
