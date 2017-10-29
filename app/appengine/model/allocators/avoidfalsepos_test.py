import unittest

from model.allocators.avoidfalsepos import AvoidsFP
from model.experimentdesign import ExperimentDesign
from model.assay import Assay
from model.allocation import Allocation



class TestAvoidsFP(unittest.TestCase):

    def setUp(self):
        pass

    # ------------------------------------------------------------------------
    # These tests are ordered bottom up - verifying the private utility
    # methods first, before moving on the more aggregate methods, and then
    # eventually the public API.
    # ------------------------------------------------------------------------


    def test_draw_possible_chamber_sets_of_size(self):
        """
        Ensures that this method produces exactly the right sequence of
        chamber sets, and in the design-in order.
        """
        design = ExperimentDesign.make_from_params(0, 0, 0, 0, 0)
        allocator = AvoidsFP(design)
        chambers = {3,1,2}
        size = 2

        subsets = allocator._draw_possible_chamber_sets_of_size(chambers, size)

        self.assertEqual(len(subsets), 3)

        self.assertEqual(subsets[0], set([1, 2]))
        self.assertEqual(subsets[1], set([1, 3]))
        self.assertEqual(subsets[2], set([2, 3]))

    def test_remove_incompatible_chambers(self):
        """
        Ensures that this method produces exactly the right sequence of
        chamber sets, and in the design-in order.
        """
        assays = 6
        chambers = 3
        replicas = 0
        dontmix = 1
        targets = 1

        design = ExperimentDesign.make_from_params(assays, chambers, 
                replicas, dontmix, targets)
        allocator = AvoidsFP(design)

        
        # The design should have make 'F' and 'A' incompatible.
        # The design should have decided that the only target present is 'A'.
        self.assertEqual(design.dontmix, [['F', 'A']])
        self.assertEqual(design.targets_present, set(['A']))

        # We will put 'A' into chamber 1, and
        # We will put 'F' into chamber 2

        allocator.alloc.allocate(Assay('A', 1), 1)
        allocator.alloc.allocate(Assay('F', 1), 2)

        # Now in the context of looking for homes for 'A'...
        # From the set {1,2,3}...
        # Chamber 1 should be removed because it already contains A.
        # Chamber 2 should be removed because it contains incompatible F.
        # Chamber 3 alone should remain.

        candidate_chambers = {1,2,3}
        candidate_chambers = allocator._remove_incompatible_chambers(
            candidate_chambers, assay_P='A')
        self.assertEqual(candidate_chambers, set([3]))


    def test_all_would_fire(self):
        """
        blah
        """
        assays = 6
        chambers = 6
        replicas = 0
        dontmix = 0
        targets = 0

        design = ExperimentDesign.make_from_params(assays, chambers, 
                replicas, dontmix, targets)
        allocator = AvoidsFP(design)

        # We will put 'A', 'B', 'C' into chambers 1,2,3 respectively.

        allocator.alloc.allocate(Assay('A', 1), 1)
        allocator.alloc.allocate(Assay('B', 1), 2)
        allocator.alloc.allocate(Assay('C', 1), 3)

        chamber_set = {2,3}

        # All would fire should be true for chambers {2,3} if
        #   1) both B and C are present
        #   2) all of A,B,C are present

        self.assertTrue(allocator._all_would_fire(chamber_set, {'B', 'C'}))
        self.assertTrue(allocator._all_would_fire(chamber_set, {'A', 'B', 'C'}))

        # All would fire should be false for chambers {2,3} if
        #   Either of 'B', 'C' is absent.
        self.assertFalse(allocator._all_would_fire(chamber_set, {'A', 'B'}))
        self.assertFalse(allocator._all_would_fire(chamber_set, {'A', 'C'}))




    def test_runs_without_crashing(self):
        assays = 20
        chambers = 24
        replicas = 4
        dontmix = 10
        targets = 0

        design = ExperimentDesign.make_from_params(assays, chambers, 
                replicas, dontmix, targets)
        allocator = AvoidsFP(design)
        allocation = allocator.allocate()

