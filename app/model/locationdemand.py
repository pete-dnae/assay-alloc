class LocationDemand:
    """
    The LocationDemand class encapsulates the instruction (or need) to place a
    given assay A<n> "somewhere", including some conditions that must be met by
    "somewhere" for it to be legal.
   """

    def __init__(self, assay, exclude_chambers, exclude_assays):
        """ 
        Provide the constructor with a set of chambers that should be
        excluded because they are known in advance to be unsuitable. Also
        provide, similarly, a set of assays that are deemed unsuitable.
        """
        self.assay = assay
        self.exclude_chambers = exclude_chambers
        self.exclude_assays = exclude_assays
