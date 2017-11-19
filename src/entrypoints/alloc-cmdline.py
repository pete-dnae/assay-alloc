"""
A command line program that runs the assay allocator taking parameters from
the command line.
"""
import sys

from lib.model.experimentreporter import ExperimentReporter

from lib.model.depletingpoolallocator import DepletingPoolAllocator
from lib.model.experimentfromcmdline import ExperimentFromCmdLine


def run():
    experiment_design = ExperimentFromCmdLine.make(sys.argv)
    allocator = DepletingPoolAllocator(experiment_design)
    assay_allocation = allocator.allocate()
    reporter = ExperimentReporter(experiment_design, assay_allocation)
    report_txt = reporter.report()
    print report_txt


if __name__ == '__main__':
    run()


