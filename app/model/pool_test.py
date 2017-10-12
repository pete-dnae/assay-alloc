import unittest

from model.pool import Pool
from experimentinputs.experimentdesign import ExperimentDesign

class TestPool(unittest.TestCase):

    def setUp(self):
        pass


    def test_construction_creates_correct_initial_state(self):
        design = ExperimentDesign.make_reference_example()
        pool = Pool(design)

        self.assertEqual(len(pool.assays), 41)
        print('XXX pool str is: %s', pool)

