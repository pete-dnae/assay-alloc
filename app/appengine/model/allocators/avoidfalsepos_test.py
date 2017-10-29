import unittest

from model.allocators.avoidfalsepos import AvoidsFP
from model.experimentdesign import ExperimentDesign
from model.assay import Assay
from model.allocation import Allocation



class TestAvoidsFP(unittest.TestCase):

    def setUp(self):
        pass

    # ------------------------------------------------------------------------
    # Test utility methods - despite them being private.
    # ------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    # Test get to run without crashing
    # ------------------------------------------------------------------------

    def test_runs_without_crashing(self):
        assays = 20
        chambers = 24
        replicas = 4
        dontmix = 10
        targets = 0

        design = ExperimentDesign.make_from_params(assays, chambers, 
                replicas, dontmix, targets)
        allocator = AvoidsFP(design)
        allocation = allocator.allocate()
