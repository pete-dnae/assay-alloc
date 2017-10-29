import unittest

from possibletargets import PossibleTargets
from model.experimentdesign import ExperimentDesign


class TestPossibleTargets(unittest.TestCase):

    def setUp(self):
        pass


    def test_create_produces_exactly_what_is_expected(self):
        """
        This test ensures that the sets produces are exhaustively
        correct, and in the delibarately organised sequence required, and
        properly in response to the list of set-sizes passed in..
        """
        assays = 4
        chambers = 3
        replicas = 2
        dontmix = 0
        targets = 0

        design = ExperimentDesign.make_from_params(
            assays, chambers, replicas, dontmix, targets)

        set_sizes = (1,2)
        pt = PossibleTargets.create(design, set_sizes)

        self.assertEqual(len(pt.sets), 10)

        self.assertEqual(pt.sets[0], set('A'))
        self.assertEqual(pt.sets[1], set(['B']))
        self.assertEqual(pt.sets[2], set(['C']))
        self.assertEqual(pt.sets[3], set(['D']))
        self.assertEqual(pt.sets[4], set(['A', 'B']))
        self.assertEqual(pt.sets[5], set(['A', 'C']))
        self.assertEqual(pt.sets[6], set(['A', 'D']))
        self.assertEqual(pt.sets[7], set(['B', 'C']))
        self.assertEqual(pt.sets[8], set(['B', 'D']))
        self.assertEqual(pt.sets[9], set(['C', 'D']))
