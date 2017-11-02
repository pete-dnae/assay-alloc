import unittest
import sys

from model.allocators.avoidfalsepos import AvoidsFP
from model.experimentdesign import ExperimentDesign
from model.allocation import Allocation



class TestAvoidsFP(unittest.TestCase):

    def setUp(self):
        pass

    # ------------------------------------------------------------------------
    # These tests are ordered bottom up - verifying the simplest utility
    # methods first, before moving on the more aggregate methods, and then
    # eventually the public API.
    # ------------------------------------------------------------------------


    def xtest_draw_possible_chamber_sets_of_size(self):
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



    def xtest_filter_reserved_chamber_sets(self):
        # Do some allocation so that reserved chamber sets exist.
        # Then make sure the method under test reports these back to us,
        # omitting those specified in the filter.
        assays = 3
        chambers = 3
        replicas = 0
        dontmix = 0
        targets = 0

        design = ExperimentDesign.make_from_params(assays, chambers, 
                replicas, dontmix, targets)
        allocator = AvoidsFP(design)
        allocator.alloc.allocate('A', frozenset({1,2,3,4}))
        allocator.alloc.allocate('B', frozenset({1,2,3,5}))
        filter = {5}
        filtered = allocator._filter_reserved_chamber_sets(filter)
        self.assertEqual(filtered, set([frozenset([1, 2, 3, 5])]))

    def xtest_target_set_need_not_be_tested(self):
        assays = 0
        chambers = 0
        replicas = 0
        dontmix = 0
        targets = 0

        design = ExperimentDesign.make_from_params(assays, chambers, 
                replicas, dontmix, targets)
        allocator = AvoidsFP(design)

        #  Should say True when the target set contains the reserving assay.
        target_set = {'A', 'B', 'C'}
        reserving_assay = 'B'
        incoming_assay = None
        self.assertTrue(
            allocator._target_set_need_not_be_tested(
                target_set, reserving_assay, incoming_assay))

        #  Should say True when the target set doesn't have the incoming
        #  assay in it.
        target_set = {'A', 'B', 'C'}
        reserving_assay = None
        incoming_assay = 'D'
        self.assertTrue(
            allocator._target_set_need_not_be_tested(
                target_set, reserving_assay, incoming_assay))

        # Should say False otherwise.
        target_set = {'A', 'B', 'C'}
        reserving_assay = 'D'
        incoming_assay = 'A'
        self.assertFalse(
            allocator._target_set_need_not_be_tested(
                target_set, reserving_assay, incoming_assay))

    def xtest_assemble_chamber_sets_to_consider_for(self):
        # Make sure that sets that would breach the no mix rules
        # get rejected. And the set size requirement is honoured.
        assays = 4
        chambers = 5
        replicas = 2
        dontmix = 1
        targets = 0

        design = ExperimentDesign.make_from_params(assays, chambers, 
                replicas, dontmix, targets)
        allocator = AvoidsFP(design)
        allocator.alloc.allocate('A', frozenset({1,2,3}))
        allocator.alloc.allocate('B', frozenset({2,3,4}))
        allocator.alloc.allocate('C', frozenset({3,4,5}))
        sets = allocator._assemble_chamber_sets_to_consider_for('D')

        # Double check what the experiment design decided about dontmix
        # pairs.
        self.assertEqual(design.dontmix, [['D', 'A']])

        # So the answer should rule out any set that contains 1 or 2 or 3,
        # which only leaves {4,5}
        self.assertEqual(sets, [frozenset([4, 5])])


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

        allocator.alloc.allocate('A', frozenset({1,2,3}))
        allocator.alloc.allocate('B', frozenset({2,3,4}))
        allocator.alloc.allocate('C', frozenset({3,4,5}))
        allocator.alloc.allocate('M', frozenset({1}))

        # {1,2,3} will all fire in the presence of 'B', 'M' and 'C'
        chamber_set = {1,2,3}
        reserving_assay = 'A'
        target_set = {'B', 'M', 'C'}
        self.assertTrue(allocator._all_would_fire(
            chamber_set, reserving_assay, target_set))

        # But not if we leave out 'M'
        target_set = {'B', 'C'}
        self.assertFalse(allocator._all_would_fire(
            chamber_set, reserving_assay, target_set))

    def xtest_that_skips_already_reserved_chamber_sets(self):
        """
        Checks that this bit of conditional logic in the code gets
        executed.
        """
        assays = 5; chambers = 6; replicas = 2; dontmix = 0; targets = 0
        design = ExperimentDesign.make_from_params(assays, chambers, 
                replicas, dontmix, targets)
        allocator = AvoidsFP(design)
        tracer = AssertThisTraceMessageGetsLogged(self,
                'because already reserved')
        allocator.tracer = tracer
        # Note that allocate() will be terminated early by the tracer in
        # this test.
        allocation = allocator.allocate()
        self.fail('Tracer did not receive: %s', tracer.message_fragment)

    def xtest_that_target_set_is_judged_harmless(self):
        """
        Checks that this bit of conditional logic in the code gets
        executed.
        """
        assays = 5; chambers = 6; replicas = 2; dontmix = 0; targets = 0
        design = ExperimentDesign.make_from_params(assays, chambers, 
                replicas, dontmix, targets)
        allocator = AvoidsFP(design)
        tracer = AssertThisTraceMessageGetsLogged(self,
                'Target set need not be tested')
        allocator.tracer = tracer
        # Note that allocate() will be terminated early by the tracer in
        # this test.
        allocation = allocator.allocate()
        self.fail('Tracer did not receive: %s', tracer.message_fragment)

    def test__is_allocation_with_assay_P_added_vulnerable(self):
        """
        reserve 123 for A
        reserve 456 for B

        Adding C to 234 makes the allocation vulnerable because in the 
        presence of AB, all of 234 fire despite C not being present.
        """
        assays = 3; chambers = 3; replicas = 3; dontmix = 0; targets = 0
        design = ExperimentDesign.make_from_params(assays, chambers, 
                replicas, dontmix, targets)
        allocator = AvoidsFP(design)

        allocator.alloc.allocate('A', frozenset({1,2,3}))
        allocator.alloc.allocate('B', frozenset({4,5,6}))

        vulnerable = allocator._is_allocation_with_assay_P_added_vulnerable(
            'C', frozenset({2,3,4}))
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

        #self.assertEquals(allocation.chambers_for('A'), set([1, 2, 3]))
        #self.assertEquals(allocation.chambers_for('B'), set([1, 2, 4]))

    def xtest_realistic_sized_example_without_dontmix(self):
        assays = 20
        chambers = 24
        replicas = 5
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

class AssertThisTraceMessageGetsLogged:
    """
    An object that exposes a trace(message) method to which clients to send
    strings.  It can be constructed to react to one particular message fragment
    by telling the current test case to immediately "pass".
    """

    def __init__(self, testcase, message_fragment):
        self._testcase = testcase
        self.message_fragment = message_fragment

    def trace(self, incoming_message):
        if self.message_fragment in incoming_message:
            self._testcase.skipTest(None)
