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


    def test_draw_possible_chamber_sets_of_size(self):
        """
        Ensures that this method produces exactly the right sequence of
        chamber sets, and in the design-in order.
        """

        assays = 0
        chambers = 5
        sim_targets = 3
        dontmix = 0

        design = ExperimentDesign.make_from_params(assays, chambers, 
                sim_targets, dontmix)
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

    def test_remove_incompatible_chambers(self):
        """
        Ensures that this method produces exactly the right sequence of
        chamber sets, and in the design-in order.
        """
        assays = 6
        chambers = 3
        sim_targets = 3
        dontmix = 1

        design = ExperimentDesign.make_from_params(assays, chambers, 
                sim_targets, dontmix)
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



    def test_filter_reserved_chamber_sets(self):
        # Do some allocation so that reserved chamber sets exist.
        # Then make sure the method under test reports these back to us,
        # but only those caught by the filter.
        assays = 3
        chambers = 3
        sim_targets = 3
        dontmix = 0

        design = ExperimentDesign.make_from_params(assays, chambers, 
                sim_targets, dontmix)
        allocator = AvoidsFP(design)
        allocator.alloc.allocate('A', frozenset({1,2,3,4}))
        allocator.alloc.allocate('B', frozenset({1,2,3,5}))
        filter = {5}
        filtered = allocator._filter_reserved_chamber_sets(filter)
        self.assertEqual(filtered, set([frozenset([1, 2, 3, 5])]))


    def test_assemble_chamber_sets_to_consider_for(self):
        # Make sure that sets that would breach the no mix rules
        # get rejected. And the set size requirement is honoured.
        assays = 4
        chambers = 5
        sim_targets = 1
        dontmix = 1

        design = ExperimentDesign.make_from_params(assays, chambers, 
                sim_targets, dontmix)
        allocator = AvoidsFP(design)
        allocator.alloc.allocate('A', frozenset({1,2}))
        allocator.alloc.allocate('B', frozenset({3,4}))
        allocator.alloc.allocate('C', frozenset({4,5}))
        sets = allocator._assemble_chamber_sets_to_consider_for('D')

        # Double check what the experiment design decided about dontmix
        # pairs.
        self.assertEqual(design.dontmix, [['D', 'A']])

        # So the answer should rule out any set that contains 1 or 2,
        # which only leaves {3,4,5}
        self.assertEqual(sets,  
                [frozenset([3, 5]), frozenset([3, 4]), frozenset([4, 5])])


    def test_all_would_fire(self):
        """
        Make sure the utility method _all_would_fire() provides correct
        false and positive conclusions.
        """
        assays = 6
        chambers = 6
        sim_targets = 3
        dontmix = 0

        design = ExperimentDesign.make_from_params(assays, chambers, 
                sim_targets, dontmix)
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


    def test_that_bypasses_already_reserved_chamber_sets(self):
        """
        Checks bypasses reserved chamber.
        """
        assays = 5; chambers = 6; sim_targets = 3; dontmix = 0; 
        design = ExperimentDesign.make_from_params(assays, chambers, 
                sim_targets, dontmix)
        allocator = AvoidsFP(design)
        tracer = AssertThisTraceMessageGetsLogged(self,
                'because already reserved')
        allocator.tracer = tracer
        # Note that allocate() will be terminated early by the tracer in
        # this test.
        allocation = allocator.allocate()
        self.fail('Tracer did not receive: %s' % tracer.message_fragment)

    def test_logic_for_avoiding_the_all_firing_checks(self):
        """
        Checks avoids all firing test.
        """
        assays = 3; chambers = 3; sim_targets = 3; dontmix = 0; 
        design = ExperimentDesign.make_from_params(assays, chambers, 
                sim_targets, dontmix)
        allocator = AvoidsFP(design)

        allocator.alloc.allocate('A', frozenset({1,2,3}))

        tracer = AssertThisTraceMessageGetsLogged(self,
                'Can avoid all firing test')
        allocator.tracer = tracer
        # Call the method that will generate the trace message we are
        # looking for.
        allocator._is_allocation_with_assay_P_added_vulnerable(
            'B', frozenset({2,3,4}))
        self.fail('Tracer did not receive: %s' % tracer.message_fragment)

    def test_is_allocation_with_assay_P_added_vulnerable(self):
        """
        reserve 123 for A
        reserve 456 for B

        Adding C to 234 makes the allocation vulnerable because in the 
        presence of AB, all of 234 fire despite C not being present.
        """
        assays = 3; chambers = 8; sim_targets = 2; dontmix = 0; 
        design = ExperimentDesign.make_from_params(assays, chambers, 
                sim_targets, dontmix)
        allocator = AvoidsFP(design)

        allocator.alloc.allocate('A', frozenset({1,2,3}))
        allocator.alloc.allocate('B', frozenset({4,5,6}))

        vulnerable = allocator._is_allocation_with_assay_P_added_vulnerable(
            'C', frozenset({2,3,4}))
        self.assertTrue(vulnerable)

        # Conversely adding 'C' to {7,8} does not make the allocation
        # vulnerable. Because there is no set of targets present that would
        # make all of {7,8} fire unless it contains 'C'.
        vulnerable = allocator._is_allocation_with_assay_P_added_vulnerable(
            'C', frozenset({7,8}))
        self.assertFalse(vulnerable)


    def test_tiny_real_example(self):
        """
        Make a tiny example, that a person can reason about.
        Deploy just the assays A and B, and model the presence of just
        one target.
        """
        assays = 2
        chambers = 4
        sim_targets = 2
        dontmix = 0

        design = ExperimentDesign.make_from_params(assays, chambers, 
                sim_targets, dontmix)
        allocator = AvoidsFP(design)
        allocation = allocator.allocate()

        self.assertEquals(allocation.chambers_for('A'), set([1, 2, 3]))
        self.assertEquals(allocation.chambers_for('B'), set([1, 2, 4]))


class AssertThisTraceMessageGetsLogged:
    """
    An object that exposes a trace(message) method to which clients to send
    strings.  It can be constructed to react to one particular message fragment
    by telling the current test case to immediately "pass".
    """

    def __init__(self, t_case, message_fragment):
        self._case = t_case
        self.message_fragment = message_fragment

    def trace(self, incoming_message):
        if self.message_fragment in incoming_message:
            self._case.skipTest(None)
