import unittest

from allocationheuristics import AllocationHeuristics
from allocation import Allocation

class TestHeuristics(unittest.TestCase):

    def setUp(self):
        pass


    def test_heuristics(self):
        """
        If we set up an Allocation object with chamber 1 having fewer
        assays allocated to it than the others, then the preferred_chamber()
        method should return chamber 1.

        If we then alter the allocations in favour of chamber 2, we can
        check that the result switches to be chamber 2.
        """
        alloc = Allocation(3)
        alloc.place_assay_here('foo', 1)
        alloc.place_assay_here('foo', 2)
        alloc.place_assay_here('foo', 3)

        alloc.place_assay_here('bar', 2)
        alloc.place_assay_here('bar', 3)

        available_chambers = set((1,2,3))

        self.assertEqual(AllocationHeuristics.preferred_chamber(
            available_chambers, alloc), 1)

        alloc.place_assay_here('bar', 1)

        alloc.place_assay_here('baz', 1)
        alloc.place_assay_here('baz', 3)

        self.assertEqual(AllocationHeuristics.preferred_chamber(
            available_chambers, alloc), 2)





        
if __name__ == '__main__':
    unittest.main()
