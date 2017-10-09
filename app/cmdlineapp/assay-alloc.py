from experimentinputs.experimentdesign_test import MakeReferenceExperiment
from model.assayallocator import AssayAllocator
from model.experimentreporter import ExperimentReporter

if __name__ == '__main__':

    print('Program starting...')

    experiment_design = MakeReferenceExperiment.make()
    assay_allocation = AssayAllocator().allocate(experiment_design)
    evaluator = ExperimentReporter(assay_allocation, experiment_design)
    results = evaluator.evaluate()

    print(results)

