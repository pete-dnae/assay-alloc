import unittest
import sys

from model.allocators.avoidfalsepos import AvoidsFP
from model.experimentdesign import ExperimentDesign
from model.allocation import Allocation



class TestAvoidsFP(unittest.TestCase):

    def setUp(self):
        pass


    def test_realistic_example(self):
        assays = 20; chambers = 24; sim_targets = 4; dontmix = 0;

        design = ExperimentDesign.make_from_params(
                assays, chambers, sim_targets, dontmix)
        allocator = AvoidsFP(design)
        allocation = allocator.allocate()
