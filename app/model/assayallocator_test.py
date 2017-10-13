import unittest

from model.assayallocator import AssayAllocator
from model.experimentdesign import ExperimentDesign
from model.assay import Assay


class TestAssayAllocator(unittest.TestCase):

    def setUp(self):
        pass


    def test_full_allocate_run_doesnt_crash(self):
        design = ExperimentDesign.make_reference_example()
        allocator = AssayAllocator(design)
        allocator.allocate()


    def test_chambers_used_in_preference_order(self):
        """
        We set up a very tiny experiment to help us check that
        allocations are being done in a way that tries to fill chambers
        evenly.
        """
        # Provide only two chambers. Ask for A1, B1, C1 to be placed. Ensure
        # that these are allocated in order to chambers 1,2,1 - in an attempt
        # to fill chambers evenly.
        design = ExperimentDesign()
        design.assay_types = {'A', 'B', 'C'}
        design.replicas['A'] = 1
        design.replicas['B'] = 1
        design.replicas['C'] = 1
        design.num_chambers = 2

        allocator = AssayAllocator(design)
        allocation = allocator.allocate()
        self.assertTrue(
            allocation.assays_present_in(1) == {Assay('A', 1), Assay('C', 1)})


    def test_full_allocate_run_on_reference_experiment(self):
        design = ExperimentDesign.make_reference_example()
        allocator = AssayAllocator(design)
        allocation = allocator.allocate()

        self.assertEqual(allocation.format_chamber(1), '001 A1,C4,F3,I2,L1,N3')
        self.assertEqual(allocation.format_chamber(2), '002 A2,D1,F4,I3,L2')
        self.assertEqual(allocation.format_chamber(3), '003 B1,D2,G1,I4,L3')
        self.assertEqual(allocation.format_chamber(4), '004 B2,E1,G2,J1,L4')
        self.assertEqual(allocation.format_chamber(5), '005 B3,E2,H1,J2,M1')
        self.assertEqual(allocation.format_chamber(6), '006 C1,E3,H2,K1,M2')
        self.assertEqual(allocation.format_chamber(7), '007 C2,F1,H3,K2,N1')
        self.assertEqual(allocation.format_chamber(8), '008 C3,F2,I1,K3,N2')


