from experimentinputs.experimentdesign_test import MakeReferenceExperiment
from model.assayallocator import AssayAllocator
from model.experimentevaluator import ExperimentEvaluator

if __name__ == '__main__':

    print('Program starting...')

    experiment_design = MakeReferenceExperiment.make()
    assay_allocation = AssayAllocator().allocate(experiment_design)
    evaluator = ExperimentEvaluator(assay_allocation, experiment_design)
    results = evaluator.evaluate()

    print(results)

