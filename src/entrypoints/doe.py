"""
A command line program that trys to do an allocation multiple times, with
different settings each time. Prints a success / fail line of output for each
attempt made.
"""

from lib.model.experimentdesign import ExperimentDesign

from lib.model.depletingpoolallocator import DepletingPoolAllocator

all_targets = (3,4,5)
all_assays = (13,16,18,20,22,25)
all_chambers = (14,17,19,21,23,26)

def run():
    print('TARGETS, ASSAYS, CHAMBERS, WORKED')
    for targets in all_targets:
        for assays in all_assays:
            for chambers in all_chambers:
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


