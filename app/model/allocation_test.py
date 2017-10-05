import unittest

from allocation import Allocation
from locationdemand import LocationDemand

class TestAllocation(unittest.TestCase):

    def setUp(self):
        pass


    def test_construction(self):
        alloc = Allocation(3)
        self.assertEqual(len(alloc.chambers_info), 3)


    def test_placing_of_assay(self):
        a = Allocation(3)
        a.place_assay_here(2, LocationDemand('foo'))
        chamber_meta = a.chambers_info[2]
        self.assertTrue('foo' in chamber_meta.assays)


    def test_barring_an_assay(self):
        a = Allocation(3)

        # We bar the assay 'foo' from chamber 2 and assert that the accessor
        # method rejects 'foo' in 2, but accepts 'bar' in 2.
        a.bar_this_assay_from_chamber('foo', 2)
        self.assertTrue(a.chamber_rejects_assay(2, 'foo'))
        self.assertFalse(a.chamber_rejects_assay(2, 'bar'))

        # Assert the accessor accepts anything in a chamber from which nothing
        # has been barred.
        self.assertFalse(a.chamber_rejects_assay(1, 'fibble'))


    def test_chamber_contains_assay(self):
        a = Allocation(3)
        a.place_assay_here(1, LocationDemand('placed_in_1'))
        a.place_assay_here(2, LocationDemand('placed_in_2'))
        self.assertTrue(a.chamber_contains_assay(1, 'placed_in_1'))
        self.assertFalse(a.chamber_contains_assay(1, 'placed_in_2'))
        self.assertTrue(a.chamber_contains_assay(2, 'placed_in_2'))
        self.assertFalse(a.chamber_contains_assay(2, 'placed_in_1'))


    def test_assays_in_chamber(self):
        a = Allocation(3)
        a.place_assay_here(1, LocationDemand('foo'))
        a.place_assay_here(1, LocationDemand('bar'))
        self.assertTrue('foo' in a.assays_in_chamber(1))
        self.assertTrue('bar' in a.assays_in_chamber(1))


    def test_number_of_assays_in_chamber(self):
        a = Allocation(3)
        a.place_assay_here(1, LocationDemand('foo'))
        a.place_assay_here(1, LocationDemand('bar'))
        self.assertEqual(2, a.number_of_assays_in_chamber(1))


    def test_copying_an_allocation(self):
        a = Allocation(3)
        a.place_assay_here(1, LocationDemand('foo'))
        a.bar_this_assay_from_chamber('bar', 2)

        b = a.copy()
        self.assertNotEqual(a, b) # Different objects
        # But same properties...
        chamber_meta = b.chambers_info[2]
        self.assertTrue('bar' in chamber_meta.now_barred)

        
if __name__ == '__main__':
    unittest.main()
