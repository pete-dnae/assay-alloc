import unittest

from model.experimentreporter import ExperimentReporter

from model.assayallocator import AssayAllocator
from model.experimentdesign import ExperimentDesign
from model.assay import Assay
from model.allocation import Allocation


class TestExperimentReporter(unittest.TestCase):

    def setUp(self):
        pass


    def test_did_chamber_fire(self):
        design = ExperimentDesign.make_reference_example()
        allocator = AssayAllocator(design)
        allocation = allocator.allocate()
        reporter = ExperimentReporter(allocation, design)

        self.assertTrue(reporter.did_this_chamber_fire(1))
        self.assertFalse(reporter.did_this_chamber_fire(8))


    def test_chambers_that_fired(self):
        design = ExperimentDesign.make_reference_example()
        allocator = AssayAllocator(design)
        allocation = allocator.allocate()
        reporter = ExperimentReporter(allocation, design)

        self.assertEqual(reporter.chambers_that_fired(), set([1, 3, 4, 7]))

    def test_assays_in_chambers_that_fired(self):
        design = ExperimentDesign.make_reference_example()
        allocator = AssayAllocator(design)
        allocation = allocator.allocate()
        reporter = ExperimentReporter(allocation, design)

        self.assertEqual(
            reporter.assays_in_chambers_that_fired(),
            set(['A', 'C', 'B', 'E', 'D', 'G', 'F', 'I', 'H', 'K', 'J', 'M', 'L', 'N']))

    def test_format_assays_in_chambers_that_fired(self):
        design = ExperimentDesign.make_reference_example()
        allocator = AssayAllocator(design)
        allocation = allocator.allocate()
        reporter = ExperimentReporter(allocation, design)

        self.assertEqual(
            reporter.format_assays_in_chambers_that_fired(), 'ABCDEFGHIJKLMN')

    def test_which_firing_chambers_contain(self):
        design = ExperimentDesign.make_reference_example()
        allocator = AssayAllocator(design)
        allocation = allocator.allocate()
        reporter = ExperimentReporter(allocation, design)

        self.assertEqual(
            reporter.which_firing_chambers_contain('D'),  set([3]))


    def test_firing_stats_for_assay(self):
        design = ExperimentDesign.make_reference_example()
        allocator = AssayAllocator(design)
        allocation = allocator.allocate()
        reporter = ExperimentReporter(allocation, design)

        self.assertEqual(
            reporter.firing_stats_for_assay('A'),
            {'firing_message': '1 of 2 ( 50%)', 'percent': 50, 'assay_type': 'A'})


