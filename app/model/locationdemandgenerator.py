class LocationDemandGenerator:
    """
    Preamble: When an assay is placed into a chamber creates a new colocated
    assay pair, then new knock-on location demands are created implicitly to
    disambiguate the calling. This LocationDemandGenerator class knows how to
    make these inferences. This idea is ring-fenced by this class, so that more
    exotic knock-on effects can be considered in the future, without requiring
    any other code to change.
    """

    def __init__(self, trigger_location_demand, placement_progress):
        """
        The constructor parameters specify an assay and a chamber to which it
        has been added - which are potentially creating the location demands.
        """
        self._trigger_location_demand = trigger_location_demand
        self._placement_progress = placement_progress


    def generate(self):
        """
        Works out which new location demands are implicitly created, and
        returns these as a sequence of LocationDemand(s).
        """
        pass
