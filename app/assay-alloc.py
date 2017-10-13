import sys

from cmdlineapp.experimentfromcmdline import ExperimentFromCmdLine
from model.assayallocator import AssayAllocator
from model.experimentreporter import ExperimentReporter

if __name__ == '__main__':

    print('Program starting...')

    experiment_design = ExperimentFromCmdLine.make(sys.argv)
    #experiment_design = MakeReferenceExperiment.make()

    assay_allocation = AssayAllocator().allocate(experiment_design)
    reporter = ExperimentReporter(assay_allocation, experiment_design)
    results = reporter.report()

    print(results)

