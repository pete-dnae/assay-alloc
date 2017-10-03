class LocationDemand:
    """
    The LocationDemand class encapsulates the instruction (or need) to place a
    given assay A<n> "somewhere", including the conditions that must be met by
    "somewhere" for it to be legal. For example, a  list of assays that must not
    already been incumbent.
    """

    def __init__(self, demanding_assay, demanding_chamber=None):
        """
        The demanding chamber parameter is for when the demand for this
        placement demand has come into being as a knock-on effect of placing a
        different assay somewhere else.
        """
        self.demanding_chamber =  demanding_chamber
        self.demanding_assay = demanding_assay
