class LocationDemandGenerator(object):
    """
    The LocationDemandGenerator is a factory for making GeneratedLocationDemands.
    It exists so that the data model of GeneratedLocationDemands is kept separate
    from the reasoning that brings them into being. The idea being that the
    reasoning and inference required is a black box that can be altered without
    affecting any other code.

    For example the first implementation might deal only with pairs of chambers
    helping each other out in disambiguation, whereas later implementations might
    be more ambitious and consider sets of 3.
    """

    def __init__(self):
        pass


    def generate(self, assay_just_added, chamber):
        """
        Returns a GeneratedLocationDemands object.
        """
        demands = self._build_generated_location_demands(
                assay_just_added, chamber)
        return demands
