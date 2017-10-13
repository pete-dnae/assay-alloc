import unittest

from model.assayallocator import AssayAllocator
from experimentinputs.experimentdesign import ExperimentDesign

class TestAssayAllocator(unittest.TestCase):

    def setUp(self):
        pass


    def test_doesnt_crash(self):
        design = ExperimentDesign.make_reference_example()
        allocator = AssayAllocator(design)
        allocator.allocate()

