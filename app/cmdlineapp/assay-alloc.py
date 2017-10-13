import sys

from cmdlineapp.experimentfromcmdline import ExperimentFromCmdLine
from model.assayallocator import AssayAllocator
from model.experimentreporter import ExperimentReporter
from model.experimentdesign import ExperimentDesign

if __name__ == '__main__':

    print('Program starting...')

    experiment_design = ExperimentFromCmdLine.make(sys.argv)
    experiment_design = ExperimentDesign.make_reference_example()

    assay_allocation = AssayAllocator(experiment_design).allocate()
    reporter = ExperimentReporter(assay_allocation, experiment_design)
    results = reporter.report()

    print(results)

