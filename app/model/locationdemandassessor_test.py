import unittest

from allocation import Allocation
from locationdemand import LocationDemand
from locationdemandassessor import LocationDemandAssessor


class TestLocationDemandAssessor(unittest.TestCase):

    def setUp(self):
        pass


    def xest_already_present_check(self):

        # If we place 'foo' in chamber 2, a subsequent demand that 'foo' be
        # placed, should reject chamber 2, because it already holds 'foo'.

        alloc = Allocation(3)
        alloc.place_assay_here('foo', 2)
        demand = LocationDemand('foo', 
                exclude_chambers = set(),
                exclude_assays = set())
        self.assertFalse(LocationDemandAssessor.assess_demand_is_met(
            demand, chamber=2, allocation=alloc))

        # Whereas, chamber 1 should be accepted.
        self.assertTrue(LocationDemandAssessor.assess_demand_is_met(
            demand, chamber=1, allocation=alloc))


    def xtest_chamber_outlawed_by_location_demand(self):

        # If we create a LocationDemand that outlaws the use of chamber 2,
        # then the assessor should judge the demand as un-met for chamber 2.
        alloc = Allocation(3)
        demand = LocationDemand('foo', 
                exclude_chambers = set((2,)),
                exclude_assays = set())
        self.assertFalse(LocationDemandAssessor.assess_demand_is_met(
            demand, chamber=2, allocation=alloc))

        # But as being met for chamber 1.
        self.assertTrue(LocationDemandAssessor.assess_demand_is_met(
            demand, chamber=1, allocation=alloc))


    def test_chamber_outlawed_because_of_assays_already_in_it(self):

        # If we place 'foo' in chamber 2, and use a LocationDemand that says
        # that any chamber that contains 'foo' is outlawed, then the assessor
        # should reject chamber 2 as a home for any assay, but accept any other
        # chamber.
        alloc = Allocation(3)
        alloc.place_assay_here('foo', 2)
        demand = LocationDemand('irrelevant', 
                exclude_chambers = set(),
                exclude_assays = set(('foo',)))
        self.assertFalse(LocationDemandAssessor.assess_demand_is_met(
            demand, chamber=2, allocation=alloc))
        self.assertTrue(LocationDemandAssessor.assess_demand_is_met(
            demand, chamber=1, allocation=alloc))


    def test_chamber_outlawed_by_allocation_object(self):
        # If we set up an Allocation object and tell it in advance that it
        # should bar 'foo' from chamber 2, then the assessor should reject
        # chamber 2 as a home for 'foo'. But accept other chambers.
        alloc = Allocation(3)
        alloc.bar_this_assay_from_chamber('foo', 2)
        demand = LocationDemand('foo', 
                exclude_chambers = set(),
                exclude_assays = set())
        self.assertFalse(LocationDemandAssessor.assess_demand_is_met(
            demand, chamber=2, allocation=alloc))
        self.assertTrue(LocationDemandAssessor.assess_demand_is_met(
            demand, chamber=1, allocation=alloc))
        
if __name__ == '__main__':
    unittest.main()
