import unittest

from model.experimentdesign import ExperimentDesign
from model.targetsethypothesese import TargetSetHypothesese



class TestTargetSetHypothesese(unittest.TestCase):

    def setUp(self):
        pass

    def test_plausibility(self):
        """
        """

        design = ExperimentDesign.make_reference_example()
        hypoth = TargetSetHypothesese.create(design)

        self.assertTrue(frozenset(['A', 'B']) in hypoth.sets)
        self.assertTrue(frozenset(['F', 'G', 'M']) in hypoth.sets)







