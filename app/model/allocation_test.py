import unittest

from allocation import Allocation

class TestAllocation(unittest.TestCase):

    def setUp(self):
        pass


    def test_construction(self):
        alloc = Allocation(3)
        self.assertEqual(alloc.num_chambers, 3)


    def test_placing_of_assay(self):
        a = Allocation(3)
        a.place_assay_here('foo', 2)
        chamber_meta = a.chambers_info[2]
        self.assertTrue('foo' in chamber_meta.assays)


    def test_barring_an_assay(self):
        a = Allocation(3)
        a.place_assay_here('foo', 2)
        a.bar_this_assay_from_chamber('bar', 2)
        chamber_meta = a.chambers_info[2]
        self.assertTrue('bar' in chamber_meta.now_barred)


    def test_copying_an_allocation(self):
        a = Allocation(3)
        a.place_assay_here('foo', 2)
        a.bar_this_assay_from_chamber('bar', 2)

        b = a.copy()
        self.assertNotEqual(a, b) # Different objects
        # But same properties...
        chamber_meta = b.chambers_info[2]
        self.assertTrue('bar' in chamber_meta.now_barred)

        
if __name__ == '__main__':
    unittest.main()
