class LocationDemandAssessor:
    """
    The LocatationDemandAssessor class knows how to evaluate if a given 
    LocationDemand can (primae facie) be met in the context of a given 
    Allocation object. We say primae facie because this does not consider the
    knock-on, recursive effects, just the various filters and blocking
    rules for this assay.
   """

    @classmethod
    def assess_demand_is_met(self, location_demand, chamber, allocation):

        assay = location_demand.assay

        # Can't use the chamber that already contains the assay that is to be
        # placed.
        if allocation.chamber_contains_assay(chamber, assay):
            return False

        # Can't use chambers that the LocationDemand has outlawed.
        if chamber in location_demand.exclude_chambers:
            return False

        # Can't use chambers that contain an assay already that the
        # LocationDemand has outlawed.
        if assay in location_demand.exclude_assays:
            return False

        # Can't use chambers that the Allocation object itself has outlawed.
        if allocation.chamber_rejects_assay(chamber, assay):
            return False


        return True # Demand is met.
