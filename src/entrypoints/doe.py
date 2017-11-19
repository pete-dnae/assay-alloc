"""
A command line program that trys to do an allocation multiple times, with
different settings each time. Prints a success / fail line of output for each
attempt made.
"""

from model.experimentdesign import ExperimentDesign

from lib.model.allocators.deduction import DepletingPoolAllocator


def run():
    print('TARGETS, ASSAYS, CHAMBERS, WORKED')
    for targets in (3,4,5):
        for assays in (13,16,18,20,22,25):
            for chambers in (14,17,19,21,23,26):
                experiment_design = ExperimentDesign.make_from_params(
                        assays, chambers, targets, 0)
                allocator = DepletingPoolAllocator(experiment_design)
                try:
                    assay_allocation = allocator.allocate()
                    status = 'y'
                except RuntimeError as e:
                    status = ''
                print('%d, %d, %d, %s' % (targets, assays, chambers, status))

if __name__ == '__main__':
    # Run normally
    run()


