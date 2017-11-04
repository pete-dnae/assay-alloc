import sys

from model.experimentdesign import ExperimentDesign
from model.experimentreporter import ExperimentReporter
from model.allocators.deduction import DeductionAllocator
from experimentfromcmdline import ExperimentFromCmdLine

if __name__ == '__main__':

    experiment_design = ExperimentFromCmdLine.make(sys.argv)

    allocator = DeductionAllocator(experiment_design)
    assay_allocation = allocator.allocate()
    reporter = ExperimentReporter(experiment_design, assay_allocation)
    report_txt = reporter.report()
    print report_txt

