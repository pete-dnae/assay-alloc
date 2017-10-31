import unittest

from model.allocators.avoidfalsepos import AvoidsFP
from model.experimentdesign import ExperimentDesign
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

        assays = 0
        chambers = 5
        replicas = 0
        dontmix = 0
        targets = 0

        design = ExperimentDesign.make_from_params(assays, chambers, 
                replicas, dontmix, targets)
        allocator = AvoidsFP(design)

        # We arrange for chamber 1 to have lots of occupants,
        # chamber 2 to have fewer, and chamber 3 to have fewer again.
        # Then then keep chamber 4 empty.

        # When we ask for possible chamber sets of size 2, we expect the least
        # populated first.
        # So, we should be offered {4,3} first, and {1,2} last.

        allocator.alloc.allocate('A', frozenset({1,2,3}))
        allocator.alloc.allocate('B', frozenset({1,2}))
        allocator.alloc.allocate('C', frozenset({1}))

        choose_from = {1,2,3,4}
        subsets = allocator._draw_possible_chamber_sets_of_size(
                choose_from, 2)

        self.assertEqual(len(subsets), 6)

        self.assertEqual(subsets[0], frozenset([3, 4]))
        self.assertEqual(subsets[5], frozenset([1, 2]))

    def xtest_remove_incompatible_chambers(self):
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

        allocator.alloc.allocate('A', frozenset({1}))
        allocator.alloc.allocate('F', frozenset({2}))

        # Now in the context of looking for homes for 'A'...
        # From the set {1,2,3}...
        # Chamber 1 should be removed because it already contains A.
        # Chamber 2 should be removed because it contains incompatible F.
        # Chamber 3 alone should remain.

        candidate_chambers = {1,2,3}
        candidate_chambers = allocator._remove_incompatible_chambers(
            candidate_chambers, assay_P='A')
        self.assertEqual(candidate_chambers, set([3]))


    def xtest_all_would_fire(self):
        """
        Make sure the utility method _all_would_fire() provides correct
        false and positive conclusions.
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

        allocator.alloc.allocate('A', frozenset({1}))
        allocator.alloc.allocate('B', frozenset({2}))
        allocator.alloc.allocate('C', frozenset({3}))

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

    def xtest_spurious_fire(self):
        assays = 4
        chambers = 10
        replicas = 0
        dontmix = 0
        targets = 0

        design = ExperimentDesign.make_from_params(assays, chambers, 
                replicas, dontmix, targets)
        allocator = AvoidsFP(design)

        # We set up a spurious fire by allocating 'D' to {3,4,5},
        # having previously allocated 'A' to 3, 'B' to 4, and 'C' to
        # 5. The spurious fire will occur in the presence of {ABC}, because
        # that will cause all of {3,4,5} to fire despite the assay that
        # reserved {3,4,5}, ie 'D' not being present.

        # Conversely, the firing of {3,4,5} in the presence of 'D' should be
        # judged to be not spurious.

        allocator.alloc.allocate('A', frozenset({3}))
        allocator.alloc.allocate('B', frozenset({4}))
        allocator.alloc.allocate('C', frozenset({5}))

        allocator.alloc.allocate('D', frozenset({3,4,5}))

        self.assertTrue(allocator._spurious_fire(
                frozenset({3,4,5}), {'A', 'B', 'C'}))
        self.assertFalse(allocator._spurious_fire(
                frozenset({3,4,5}), {'D'}))


    def xtest_tiny_real_example(self):
        """
        Cut down the real allocation behaviour by not having any
        dontmix pairs and use only 2 assay types, each with 3 replicas,
        into just 4 chambers.
        """
        assays = 2
        chambers = 4
        replicas = 3
        dontmix = 0
        targets = 0

        design = ExperimentDesign.make_from_params(assays, chambers, 
                replicas, dontmix, targets)
        allocator = AvoidsFP(design)
        allocation = allocator.allocate()

        #self.assertEquals(allocation.chambers_for('A'), set([1, 2, 3]))
        #self.assertEquals(allocation.chambers_for('B'), set([1, 2, 4]))

    def xtest_realistic_sized_example_without_dontmix(self):
        assays = 20
        chambers = 24
        replicas = 3
        dontmix = 0
        targets = 0

        design = ExperimentDesign.make_from_params(assays, chambers, 
                replicas, dontmix, targets)
        allocator = AvoidsFP(design)
        allocation = allocator.allocate()

        # A sprinkling of representative direct tests...
        """
        self.assertEquals(allocation.chambers_for('A'), set([1, 2, 3]))
        self.assertEquals(allocation.chambers_for('B'), set([1, 2, 3]))
        self.assertEquals(allocation.chambers_for('F'), set([8, 1, 2]))
        """

        # Now we collect the chamber set for every one of our assays.
        chamber_sets = set() # Set of frozenset of chamber numbers.
        assays = design.assay_types_in_priority_order()
        for assay in assays:
            chamber_set = allocation.chambers_for(assay)
            chamber_sets.add(frozenset(chamber_set))

        """
        # Like this one for example.
        self.assertTrue(frozenset([1, 2, 10]) in chamber_sets)

        # There should be exactly 20 chamber sets.
        # Their being in a set, proves there are no two the same.
        self.assertEqual(len(chamber_sets), 20)

        # They should all be of length 3
        for chamber_set in chamber_sets:
            self.assertEqual(len(chamber_set), 3)
        """


    def xtest_runs_without_crashing(self):
        assays = 20
        chambers = 24
        replicas = 4
        dontmix = 10
        targets = 0

        design = ExperimentDesign.make_from_params(assays, chambers, 
                replicas, dontmix, targets)
        allocator = AvoidsFP(design)
        allocation = allocator.allocate()

