import unittest

from model.assayallocator import AssayAllocator
from model.experimentdesign import ExperimentDesign
from model.assay import Assay
from model.allocation import Allocation



class TestAssayAllocator(unittest.TestCase):

    def setUp(self):
        pass

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

    # The following tests do a full allocation, but starting off by
    # not having any dontmix pairs specified and also by
    # artificially reducing the heuristic factors in play, so that their
    # individual impact can be seen.

    # Later tests gradually mix back in all the features.

    def test_without_dontmix_clamping_heuristics_to_chamber_only(self):
        """
        Test the results of the allocation, starting from the reference
        experiment design, with the dontmix turned off, and clamping down
        the chamber preference heuristics, to use only the chamber number
        criteria.

        Expect to see the assays crammed into the low numbered chambers.
        """
        design = ExperimentDesign.make_reference_example_without_dontmix()
        allocator = AssayAllocator(design)

        # Turn off all but the chamber number heuristic.
        allocator._defeat_existing_occupant_count_heuristic = True
        allocator._defeat_duplicate_pairs_heuristic = True
        allocation = allocator.allocate()

        # Because the only measure of chamber desirability in this experiment,
        # We should expect chambers 1 and 2 to be the same, containing the
        # first and second copy of all our assay types. E.g. A1, B1, C1, ... N1
        # respectively.
        # Then chamber 3, will the third replica of all assay types for which
        # the reference experiment design calls for 3 or more replicas.
        # Then chamber 4, will the fourth replica of all assay types for which
        # the reference experiment design calls for 4 or more replicas.

        self.assertEqual(allocation.format_chamber(1),
                         '001 A1,B1,C1,D1,E1,F1,G1,H1,I1,J1,K1,L1,M1,N1')
        self.assertEqual(allocation.format_chamber(2),
                         '002 A2,B2,C2,D2,E2,F2,G2,H2,I2,J2,K2,L2,M2,N2')
        self.assertEqual(allocation.format_chamber(3),
                         '003 B3,C3,E3,F3,H3,I3,K3,L3,N3')
        self.assertEqual(allocation.format_chamber(4),
                         '004 C4,F4,I4,L4')


    def test_without_dontmix_clamping_heuristics_to_chamber_and_occupant_count_only(self):
        """
        Test the results of the allocation, starting from the reference
        experiment design, with the dontmix turned off, and clamping down
        the chamber preference heuristics, to use only the chamber number
        and the chamber occupant count criteria.

        Should see chambers filled to level up occupancy, despite creating
        undesirably repeated pairs.
        """
        design = ExperimentDesign.make_reference_example_without_dontmix()
        allocator = AssayAllocator(design)
        allocator._defeat_duplicate_pairs_heuristic = True
        allocation = allocator.allocate()

        self.assertEqual(allocation.format_chamber(1),
                         '001 A1,C4,F3,I2,L1,N3')
        self.assertEqual(allocation.format_chamber(2),
                         '002 A2,D1,F4,I3,L2')
        self.assertEqual(allocation.format_chamber(3),
                         '003 B1,D2,G1,I4,L3')
        self.assertEqual(allocation.format_chamber(4),
                         '004 B2,E1,G2,J1,L4')
        self.assertEqual(allocation.format_chamber(5),
                         '005 B3,E2,H1,J2,M1')
        self.assertEqual(allocation.format_chamber(6),
                         '006 C1,E3,H2,K1,M2')
        self.assertEqual(allocation.format_chamber(7),
                         '007 C2,F1,H3,K2,N1')
        self.assertEqual(allocation.format_chamber(8),
                         '008 C3,F2,I1,K3,N2')


    def test_all_heuristics_without_dontmix_(self):
        """
        Test the results of the allocation, starting from the reference
        experiment design (excluding dontmix), with the full set of heuristics.

        Should see similar results to
        test_without_dontmix_clamping_heuristics_to_chamber_and_occupant_count_only,
        but with changes creeping in to avoid making more duplicate pairs
        than is necessary.
        """
        design = ExperimentDesign.make_reference_example_without_dontmix()
        allocator = AssayAllocator(design)
        #allocator._assay_to_trace = Assay('F', 3)
        allocation = allocator.allocate()

        self.assertEqual(allocation.format_chamber(1),
                         '001 A1,C4,G1,H3,K2')
        self.assertEqual(allocation.format_chamber(2),
                         '002 A2,D1,E3,F3,L3,N2')
        self.assertEqual(allocation.format_chamber(3),
                         '003 B1,D2,G2,I3,L2')
        self.assertEqual(allocation.format_chamber(4),
                         '004 B2,E1,H1,J1,L4,N3')
        self.assertEqual(allocation.format_chamber(5),
                         '005 B3,F1,I1,K1,M1')
        self.assertEqual(allocation.format_chamber(6),
                         '006 C1,E2,I2,K3,N1')
        self.assertEqual(allocation.format_chamber(7),
                         '007 C2,F2,H2,L1,M2')
        self.assertEqual(allocation.format_chamber(8),
                         '008 C3,F4,I4,J2')


    def test_fully_features(self):
        """
        Test the results of the allocation, starting from the reference
        experiment design (including dontmix), with the full set of heuristics.

        Should see variations from
        test_all_heuristics_without_dontmix
        because of the dontmix rules kicking in.
        """
        design = ExperimentDesign.make_reference_example()
        allocator = AssayAllocator(design)
        #allocator._assay_to_trace = Assay('F', 3)
        allocation = allocator.allocate()

        self.assertEqual(allocation.format_chamber(1),
                         '001 A1,C4,G1,I3,M2')
        self.assertEqual(allocation.format_chamber(2),
                         '002 A2,D1,E3,F3,L1,N3')
        self.assertEqual(allocation.format_chamber(3),
                         '003 B1,D2,G2,H3,K3,L4')
        self.assertEqual(allocation.format_chamber(4),
                         '004 B2,E1,H1,J1,L2')
        self.assertEqual(allocation.format_chamber(5),
                         '005 B3,F1,I1,K1,L3')
        self.assertEqual(allocation.format_chamber(6),
                         '006 C1,E2,I2,K2,N1')
        self.assertEqual(allocation.format_chamber(7),
                         '007 C2,F2,H2,M1,N2')
        self.assertEqual(allocation.format_chamber(8),
                         '008 C3,F4,I4,J2')




