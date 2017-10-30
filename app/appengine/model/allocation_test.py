import unittest

from model.allocation import Allocation
from model.assay import Assay

class TestAllocation(unittest.TestCase):

    def setUp(self):
        pass

    def test_construction(self):
        alloc = Allocation()

    #-----------------------------------------------------------------------
    # History Based 
    #-----------------------------------------------------------------------

    def test_reserved_chamber_sets(self):
        alloc = Allocation()
        alloc.allocate('A', frozenset({1,2,3}))
        alloc.allocate('B', frozenset({1,2,4}))
        sets = alloc.reserved_chamber_sets()
        self.assertEqual(sets, 
                set([frozenset([1, 2, 3]), frozenset([1, 2, 4])]))
            

    def test_is_chamber_set_already_reserved(self):
        alloc = Allocation()
        alloc.allocate('A', frozenset({1,2,3}))
        self.assertTrue(alloc.is_chamber_set_already_reserved(
                frozenset({1,2,3})))
        self.assertFalse(alloc.is_chamber_set_already_reserved(
                frozenset({1,2,4})))


    def test_unreserve_alloc_for(self):
        alloc = Allocation()
        alloc.allocate('A', frozenset({1,2,3}))
        alloc.allocate('B', frozenset({1,2,4}))

        alloc.unreserve_alloc_for('B')

        # assays in 1234 should all not see B
        for chamber in (1,2,3,4):
            self.assertFalse('B' in alloc.assay_types_present_in(chamber))
        # but 123 should still see A
        for chamber in (1,2,3):
            self.assertTrue('A' in alloc.assay_types_present_in(chamber))

        # homes for A should be 123
        self.assertEqual(alloc.chambers_for('A'), set([1, 2, 3]))

        # homes for B might should be key error
        self.assertRaises(KeyError, alloc.chambers_for, 'B')


    #-----------------------------------------------------------------------
    # Chamber centric
    #-----------------------------------------------------------------------

    def test_all_chambers(self):
        alloc = Allocation()
        alloc.allocate('A', frozenset({1,2,3}))
        self.assertEqual(alloc.all_chambers(), {1,2,3})

    def test_chambers_for(self):
        alloc = Allocation()
        alloc.allocate('A', frozenset({1,2,3}))
        self.assertEqual(alloc.chambers_for('A'), {1,2,3})

    #-----------------------------------------------------------------------
    # Assay centric
    #-----------------------------------------------------------------------

    def test_assay_types_present_in(self):
        alloc = Allocation()
        alloc.allocate('A', {1,2,3})
        alloc.allocate('B', {3,4,5})
        self.assertEqual(alloc.assay_types_present_in(3), set(['A', 'B']))

    def test_assay_is_present_in_all_of(self):
        alloc = Allocation()
        alloc.allocate('A', frozenset({1,2,3}))
        alloc.allocate('B', frozenset({1,2,4}))
        self.assertTrue(alloc.assay_is_present_in_all_of('A', {1,2,3}))
        self.assertFalse(alloc.assay_is_present_in_all_of('B', {1,2,3}))

    def test_which_assay_reserved_this_chamber_set(self):
        alloc = Allocation()
        alloc.allocate('A', frozenset({1,2,3}))
        alloc.allocate('B', frozenset({1,2,4}))
        self.assertEqual(alloc.which_assay_reserved_this_chamber_set(
                frozenset({1,2,4})), 'B')


    def test_assay_types_present_in(self):
        alloc = Allocation()
        # Place two assays of differing types in a single chamber.
        alloc.allocate('A', frozenset({4}))
        alloc.allocate('B', frozenset({4}))
        assay_types = alloc.assay_types_present_in(4)
        self.assertEqual(assay_types, {'A', 'B'})
