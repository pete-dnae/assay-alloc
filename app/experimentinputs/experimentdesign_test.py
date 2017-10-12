import unittest

from .experimentdesign import ExperimentDesign

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
