import unittest

from model.pool import Pool
from model.assay import Assay
from experimentinputs.experimentdesign import ExperimentDesign

class TestPool(unittest.TestCase):

    def setUp(self):
        pass


    def test_construction_creates_plausible_initial_state(self):
        design = ExperimentDesign.make_reference_example()
        pool = Pool(design)

        self.assertTrue(Assay('D', 2) in pool.assays)


