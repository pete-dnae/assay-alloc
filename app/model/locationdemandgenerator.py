class LocationDemandGenerator:
    """
    Preamble: When an assay is placed into a chamber and thus creates a new
    colocated assay pair, then new knock-on location demands are created
    implicitly to disambiguate the calling. This LocationDemandGenerator class
    knows how to make these inferences. This idea is ring-fenced by this class,
    so that more exotic knock-on effects can be considered in the future, without
    requiring any other code to change.
    """

    def __init__(self, triggering_location_demand, allocation):
        """
        The constructor requires a LocationDemand that defines the placement that
        has just been made, and the Allocation object that models the current
        state of allocations.
        """
        self._triggering_location_demand = triggering_location_demand
        self._allocation = allocation


    def generate(self):
        """
        Works out which new location demands are implicitly required, and
        returns these as a set of LocationDemand(s).
        """

        # For the first implementation we create simple pairs to disambiguate 
        # calling.

        # Consider the case that we just added 'B' to a chamber that already had
        # 'A' in it.

        # This requires that two new disambiguation location demands are met. 
        # Namely that 'A' is located in a chamber that does not contain 'B', 
        # and vice versa.

        # We overlook for the time being that these might already be met by
        # coincidence. (And when fixing this, beware exploiting the
        # disambiguating location twice.

        # We also need to add to the generated location demand, that (in the
        # first case), the chamber chosen to satisfy it must from that point 
        # onward, never have 'B' added to it.
