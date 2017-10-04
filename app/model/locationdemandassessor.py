class LocationDemandAssessor:
    """
    The LocatationDemandAssessor class knows how to evaluate if a given
    LocationDemand can (primae facie) be met by a given chamber, in the context
    of a given Allocation object. We say primae facie because this does not
    consider the knock-on, recursive effects, just the various filters and
    blocking rules for this assay alone.
    """

    @classmethod
    def assess_demand_is_met(self, location_demand, chamber, allocation):

        assay = location_demand.assay

        # Can't use the chamber if it already contains the assay that is to be
        # placed.
        if allocation.chamber_contains_assay(chamber, assay):
            return False

        # Can't use the chamber if the LocationDemand has outlawed it..
        if chamber in location_demand.exclude_chambers:
            return False

        # Can't use the chamber if it contains an assay already that the
        # LocationDemand has outlawed colocation with.
        if allocation.assays_in_chamber(chamber).intersection(
                location_demand.exclude_assays):
            return False

        # Can't use the chamber if the Allocation object itself has 
        # outlawed it.
        if allocation.chamber_rejects_assay(chamber, assay):
            return False


        return True # Demand is met.
