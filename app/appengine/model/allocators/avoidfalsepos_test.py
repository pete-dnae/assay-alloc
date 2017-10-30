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

        allocator.alloc.allocate('A', {1})
        allocator.alloc.allocate('F', {2})

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

        allocator.alloc.allocate('A', {1})
        allocator.alloc.allocate('B', {2})
        allocator.alloc.allocate('C', {3})

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


    def xtest_vulnerable_to_false_positives_with_single_target_type(self):
        """
        Make sure the utility method _vulnerable_to_false_positives() provides 
        correct false and positive conclusions.
        """

        # The chamber set {1,4,7} would not work for assay 'P' if one of the
        # possible target sets was {'A'}, and each of {1,4,7} already
        # contains 'A'. Because the presence then of target 'A' would produce
        # a false positive for 'P'.

        # We set this scenario up artificially to ensure that the utility
        # method correctly makes this call.

        # But before that, we omit 'A' from chamber 7 to provide a control
        # test.

        assays = 26
        chambers = 26
        replicas = 0
        dontmix = 0
        targets = 0

        design = ExperimentDesign.make_from_params(assays, chambers, 
                replicas, dontmix, targets)
        allocator = AvoidsFP(design)

        # Override the allocators model for possible target sets, with just
        # our single special case.
        allocator._possible_target_sets.sets = ({'A'},)

        allocator.alloc.allocate('A', {1})
        allocator.alloc.allocate('A', {4})

        # This should say it is not vulnerable, because we haven't put 'A' 
        # into chamber 7 yet.
        vulnerable = allocator._vulnerable_to_false_positives({1,4,7})
        self.assertFalse(vulnerable)

        # Now it say not ok, because we have.
        allocator.alloc.allocate('A', {7})
        vulnerable = allocator._vulnerable_to_false_positives({1,4,7})
        self.assertTrue(vulnerable)


    def xtest_vulnerable_to_false_positives_with_multiple_targets_types(self):
        """
        See previous test. This differs only by exercising the logic
        where a false positive can be generated only by a variety of targets
        being present.
        """

        # The chamber set {1,4,7} would not work for assay 'P' if one of the
        # possible target sets was {'A'}, and each of {1,4,7} already
        # contains 'A'. Because the presence then of target 'A' would produce
        # a false positive for 'P'.

        # We set this scenario up artificially to ensure that the utility
        # method correctly makes this call.

        # But before that, we omit 'A' from chamber 7 to provide a control
        # test.

        assays = 26
        chambers = 26
        replicas = 0
        dontmix = 0
        targets = 0

        design = ExperimentDesign.make_from_params(assays, chambers, 
                replicas, dontmix, targets)
        allocator = AvoidsFP(design)

        # Override the allocators model for possible target sets, with just
        # our multiple-target special case.
        allocator._possible_target_sets.sets = ({'A', 'B', 'C'},)

        allocator.alloc.allocate('A', {1})
        allocator.alloc.allocate('B', {4})

        # This should say it is not vulnerable, because we haven't put 
        # anything into chamber 7 yet.
        vulnerable = allocator._vulnerable_to_false_positives({1,4,7})
        self.assertFalse(vulnerable)

        # Now it say not ok, because we have.
        allocator.alloc.allocate('C', {7})
        vulnerable = allocator._vulnerable_to_false_positives({1,4,7})
        self.assertTrue(vulnerable)

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

        self.assertEquals(allocation.chambers_for('A'), set([1, 2, 3]))
        self.assertEquals(allocation.chambers_for('B'), set([1, 2, 4]))

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
        self.assertEquals(allocation.chambers_for('A'), set([1, 2, 3]))
        self.assertEquals(allocation.chambers_for('B'), set([1, 2, 4]))
        self.assertEquals(allocation.chambers_for('F'), set([8, 1, 2]))

        # Now we collect the chamber set for every one of our assays.
        chamber_sets = set() # Set of frozenset of chamber numbers.
        assays = design.assay_types_in_priority_order()
        for assay in assays:
            chamber_set = allocation.chambers_for(assay)
            chamber_sets.add(frozenset(chamber_set))

        # Like this one for example.
        self.assertTrue(frozenset([1, 2, 10]) in chamber_sets)

        # There should be exactly 20 chamber sets.
        # Their being in a set, proves there are no two the same.
        self.assertEqual(len(chamber_sets), 20)

        # They should all be of length 3
        for chamber_set in chamber_sets:
            self.assertEqual(len(chamber_set), 3)


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

