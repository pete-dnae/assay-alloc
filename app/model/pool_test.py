import unittest

from model.assay import Assay
from model.experimentdesign import ExperimentDesign
from model.pool import Pool


class TestPool(unittest.TestCase):

    def setUp(self):
        pass


    def test_construction_creates_plausible_initial_state(self):
        design = ExperimentDesign.make_reference_example()
        pool = Pool(design)

        self.assertTrue(Assay('D', 2) in pool.assays)

    def test_assays_present_in_deterministic_order(self):
        """
        This method provides a copy of the assays present in the pool, but
        in the form of a sequence, and in a deterministic order (to help with
        testing)
        """
        design = ExperimentDesign.make_reference_example()
        pool = Pool(design)
        assays = pool.assays_present_in_deterministic_order()
        first = assays[0]
        last = assays.pop()
        self.assertEqual(first, Assay('A', 1))
        self.assertEqual(last, Assay('N', 3))


