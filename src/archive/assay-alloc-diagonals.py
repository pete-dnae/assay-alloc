import sys

from lib.model import DiagonalsAllocator
from lib.model import ExperimentFromCmdLine
from lib.model import ExperimentReporter


def run():
    experiment_design = ExperimentFromCmdLine.make(sys.argv)


    # CHOOSE ALLOCATOR HERE
    allocator = DiagonalsAllocator(experiment_design)

    assay_allocation = allocator.allocate()
    reporter = ExperimentReporter(experiment_design, assay_allocation)
    report_txt = reporter.report()
    print report_txt


if __name__ == '__main__':
    # Run normally
    run()

    """
    #Run to profile.
    cProfile.run('run()', 'stats')
    p = pstats.Stats('stats')
    p.sort_stats('cumulative').print_stats(10)
    """


