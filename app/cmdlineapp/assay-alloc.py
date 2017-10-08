from .experimentinputs.experimentdesign_test import MakeReferenceExperiment
from .model.assayallocator import AssayAllocator
from .model.experimentevaluator import ExperimentEvaluator
from .model.reporter import Reporter

if __name__ == '__main__':

    print('Program starting...')

    experiment_design = MakeReferenceExperiment.make()
    assay_allocation = AssayAllocator.allocate()
    results = ExperimentEvaluator.evaluate(assay_allocation)
    report = Reporter.report(results)

    print('Done')

