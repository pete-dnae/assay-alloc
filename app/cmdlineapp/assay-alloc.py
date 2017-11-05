import sys
import cProfile
import pstats

from model.experimentdesign import ExperimentDesign
from model.experimentreporter import ExperimentReporter
from model.allocators.deduction import DeductionAllocator
from experimentfromcmdline import ExperimentFromCmdLine


def run():
    experiment_design = ExperimentFromCmdLine.make(sys.argv)

    allocator = DeductionAllocator(experiment_design)
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


