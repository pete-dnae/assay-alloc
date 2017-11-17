from model.experimentdesign import ExperimentDesign
from model.experimentreporter import ExperimentReporter
from model.allocators.deduction import DeductionAllocator


def run():
    print('TARGETS, ASSAYS, CHAMBERS, WORKED')
    for targets in (3,4,5):
        for assays in (13,16,18,20,22,25):
            for chambers in (14,17,19,21,23,26):
                experiment_design = ExperimentDesign.make_from_params(
                        assays, chambers, targets, 0)
                allocator = DeductionAllocator(experiment_design)
                try:
                    assay_allocation = allocator.allocate()
                    status = 'y'
                except RuntimeError as e:
                    status = ''
                print('%d, %d, %d, %s' % (targets, assays, chambers, status))

if __name__ == '__main__':
    # Run normally
    run()


