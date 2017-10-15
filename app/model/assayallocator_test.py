import unittest

from model.assayallocator import AssayAllocator
from model.experimentdesign import ExperimentDesign
from model.assay import Assay
from model.allocation import Allocation



class TestAssayAllocator(unittest.TestCase):

    def setUp(self):
        pass


    def test_full_allocate_run_doesnt_crash(self):
        design = ExperimentDesign.make_reference_example()
        allocator = AssayAllocator(design)
        allocator.allocate()

    # ------------------------------------------------------------------------
    # Test utility methods - despite them being private.
    # ------------------------------------------------------------------------

    def test__duplicate_pairs_made(self):
        """
        Put
        {A,B} in chamber 1
        {B,D} in chamber 2
        {A,Z} in chamber 3

        Ask the duplicate_pairs_made() method, how many existing co-located
        pairs would be made if {B} were added to 3.

        The new pairs will be {BA}, {BZ}.
        Of which only one {BA} is a duplicate of an existing one.
        """

        design = ExperimentDesign.make_reference_example()
        allocator = AssayAllocator(design)
        allocator.alloc.allocate(Assay('A', 1), 1)
        allocator.alloc.allocate(Assay('B', 1), 1)
        allocator.alloc.allocate(Assay('B', 2), 2)
        allocator.alloc.allocate(Assay('D', 1), 2)
        allocator.alloc.allocate(Assay('A', 2), 3)
        allocator.alloc.allocate(Assay('Z', 1), 3)

        pairs = allocator.alloc.unique_assay_type_pairs()

        count = allocator._duplicate_pairs_made(3, 'B', pairs)
        self.assertEqual(count, 1)



    def test_without_dontmix_clamping_heuristics_to_chamber_only(self):
        """
        Test the results of the allocation, starting from the reference
        experiment design, with the dontmix turned off, and clamping down
        the chamber preference heuristics, to use only the chamber number
        criteria.
        """
        design = ExperimentDesign.make_reference_example_without_dontmix()
        allocator = AssayAllocator(design)
        allocation = allocator.allocate(
            which_heuristics={AssayAllocator.H_CHAMBER})

        for row in allocation.format_chambers():
            print('XXXX %s' % row)

        """
        self.assertEqual(allocation.format_chamber(1), '001 A1,C4,F3,I2,L1,N3')
        self.assertEqual(allocation.format_chamber(2), '002 A2,D1,F4,I3,L2')
        self.assertEqual(allocation.format_chamber(3), '003 B1,D2,G1,I4,L3')
        self.assertEqual(allocation.format_chamber(4), '004 B2,E1,G2,J1,L4')
        self.assertEqual(allocation.format_chamber(5), '005 B3,E2,H1,J2,M1')
        self.assertEqual(allocation.format_chamber(6), '006 C1,E3,H2,K1,M2')
        self.assertEqual(allocation.format_chamber(7), '007 C2,F1,H3,K2,N1')
        self.assertEqual(allocation.format_chamber(8), '008 C3,F2,I1,K3,N2')
        """


