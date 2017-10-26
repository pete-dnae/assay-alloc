import unittest

from model.allocatorvariants.avoidfalsepos import AvoidsFP
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
        design = ExperimentDesign.make_reference_example()
        allocator = AvoidsFP(design)
        allocation = allocator.allocate()
