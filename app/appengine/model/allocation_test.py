import unittest

from model.allocation import Allocation
from model.assay import Assay

class TestAllocation(unittest.TestCase):

    def setUp(self):
        pass

    def test_construction(self):
        alloc = Allocation(3)

    def test_all_chambers(self):
        alloc = Allocation(3)
        self.assertEqual(alloc.all_chambers(), {1,2,3})


    def test_can_allocate(self):
        alloc = Allocation(3)
        assay = Assay('A', 1)
        chamber = 1
        alloc.allocate(assay, chamber)


    def test_which_chambers_contain_assay_type(self):
        alloc = Allocation(6)
        # Place a replicaca of 'A' in two different chambers.
        a1 = Assay('A', 1)
        a2 = Assay('A', 2)
        alloc.allocate(a1, 4)
        alloc.allocate(a2, 5)
        chambers = alloc.which_chambers_contain_assay_type('A')
        self.assertTrue(chambers == {4,5})


    def test_which_chambers_contain_assay_types(self):
        alloc = Allocation(6)
        # Place one assays of differing types into two different chambers.
        a1 = Assay('A', 1)
        b1 = Assay('B', 1)
        alloc.allocate(a1, 4)
        alloc.allocate(b1, 5)
        chambers = alloc.which_chambers_contain_assay_types({'A', 'B'})
        self.assertTrue(chambers == {4,5})


    def test_number_of_chambers_that_contain_assay_type(self):
        alloc = Allocation(6)
        # Place a replicaca of 'A' in two different chambers.
        a1 = Assay('A', 1)
        a2 = Assay('A', 2)
        alloc.allocate(a1, 4)
        alloc.allocate(a2, 5)
        count = alloc.number_of_chambers_that_contain_assay_type('A')
        self.assertEqual(count, 2)

    def test_assays_present_in(self):
        alloc = Allocation(6)
        # Place two assays of differing types in a single chamber.
        a1 = Assay('A', 1)
        b1 = Assay('B', 1)
        alloc.allocate(a1, 4)
        alloc.allocate(b1, 4)
        assays = alloc.assays_present_in(4)
        self.assertEqual(assays, {Assay('A', 1), Assay('B', 1)})


    def test_assay_types_present_in(self):
        alloc = Allocation(6)
        # Place two assays of differing types in a single chamber.
        a1 = Assay('A', 1)
        b1 = Assay('B', 1)
        alloc.allocate(a1, 4)
        alloc.allocate(b1, 4)
        assay_types = alloc.assay_types_present_in(4)
        self.assertEqual(assay_types, {'A', 'B'})


    def test_number_of_this_assay_type_allocated(self):
        alloc = Allocation(6)
        # Place a replicaca of 'A' in two different chambers.
        a1 = Assay('A', 1)
        a2 = Assay('A', 2)
        alloc.allocate(a1, 4)
        alloc.allocate(a2, 5)
        count = alloc.number_of_this_assay_type_allocated('A')
        self.assertEqual(count, 2)

    def test_assay_type_pairs_in_chamber(self):
        alloc = Allocation(6)
        alloc.allocate(Assay('A', 1), 1)
        alloc.allocate(Assay('B', 1), 1)
        alloc.allocate(Assay('C', 1), 1)
        pairs = alloc.assay_type_pairs_in_chamber(1)
        self.assertEqual(
            pairs,
            {frozenset({'A', 'B'}), frozenset({'A', 'C'}), frozenset({'B', 'C'})})

    def test_which_assay_type_pairs_present(self):
        """
        Put ABC into chamber 1, and ABD into chamber 2.
        ensure the query declares the unique pairs present to be:
        AB, AC, AD, BC, BD.
        """
        alloc = Allocation(6)
        alloc.allocate(Assay('A', 1), 1)
        alloc.allocate(Assay('B', 1), 1)
        alloc.allocate(Assay('C', 1), 1)

        alloc.allocate(Assay('A', 2), 2)
        alloc.allocate(Assay('B', 2), 2)
        alloc.allocate(Assay('D', 1), 2)

        pairs = alloc.unique_assay_type_pairs()
        self.assertEqual(len(pairs), 5)
        self.assertTrue(frozenset({'A', 'B'}) in pairs)
        self.assertTrue(frozenset({'A', 'C'}) in pairs)
        self.assertTrue(frozenset({'A', 'D'}) in pairs)
        self.assertTrue(frozenset({'B', 'C'}) in pairs)
        self.assertTrue(frozenset({'B', 'D'}) in pairs)


