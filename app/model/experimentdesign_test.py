import unittest

from model.experimentdesign import ExperimentDesign
from model.assay import Assay


class TestExperimentDesign(unittest.TestCase):

    def setUp(self):
        pass


    def test_make_reference_example(self):
        ref = ExperimentDesign.make_reference_example()

        self.assertEqual(len(ref.assay_types), 14)
        self.assertTrue('A' in ref.assay_types)
        self.assertTrue('N' in ref.assay_types)
        self.assertFalse('O' in ref.assay_types)

        self.assertEqual(len(ref.replicas), 14)
        self.assertEqual(ref.replicas['A'], 2)
        self.assertEqual(ref.replicas['B'], 3)
        self.assertEqual(ref.replicas['C'], 4)
        self.assertEqual(ref.replicas['D'], 2)
        self.assertEqual(ref.replicas['N'], 3)

        self.assertEqual(ref.num_chambers, 8)

        self.assertEqual(len(ref.dontmix), 2)
        self.assertEqual(str(ref.dontmix[0]), "['A', 'B']")
        self.assertEqual(str(ref.dontmix[1]), "['C', 'D']")

        self.assertEqual(len(ref.targets_present), 2)
        self.assertEqual(ref.targets_present[0], 'G')
        self.assertEqual(ref.targets_present[1], 'H')

    def test_can_this_assay_go_into_this_mixture(self):

        ref = ExperimentDesign.make_reference_example()

        # Note this reference example says that you must not mix A with B,
        # or, C with D.

        # Should say no when you ask to add an assay of type 'E' to a mixture
        # that already includes the type 'E'.
        allowed = ref.can_this_assay_go_into_this_mixture(Assay('E', 1), {'E'})
        self.assertFalse(allowed)

        # Should say yes when you ask to add an assay of type 'E' to a mixture
        # that does not include the type 'E'.
        allowed = ref.can_this_assay_go_into_this_mixture(Assay('E', 1), {'F'})
        self.assertTrue(allowed)

        # Should say no when you ask to add an assay of type 'A' to a mixture
        # that contains 'B' because this is outlawed by the experiment's
        # don't mix rules.
        allowed = ref.can_this_assay_go_into_this_mixture(Assay('A', 1), {'B'})
        self.assertFalse(allowed)
        # Check the same thing but with reversed roles.
        allowed = ref.can_this_assay_go_into_this_mixture(Assay('B', 1), {'A'})
        self.assertFalse(allowed)
        # Do a control check with an assay that the dontmix rules talk about,
        # but combined in a mixture that doesn't contain the counterpart.
        allowed = ref.can_this_assay_go_into_this_mixture(Assay('A', 1), {'E'})
        self.assertTrue(allowed)

