import sys

from cmdlineapp.experimentfromcmdline import ExperimentFromCmdLine
from model.assayallocator import AssayAllocator
from model.experimentreporter import ExperimentReporter
from model.experimentdesign import ExperimentDesign

if __name__ == '__main__':

    print('Program starting...')

    experiment_design = ExperimentFromCmdLine.make(sys.argv)
    #experiment_design = ExperimentDesign.make_reference_example()

    #experiment_design = ExperimentFromCmdLine.make_from_params(
    #   assays=20, chambers=24, replicas=5, dontmix=3, targets=3)

    assay_allocation = AssayAllocator(experiment_design).allocate()
    reporter = ExperimentReporter(assay_allocation, experiment_design)
    report_lines = reporter.report()
    for line in report_lines:
        print(line)

