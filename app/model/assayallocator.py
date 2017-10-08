import random

from model.allocation import Allocation

class AssayAllocator:

    _MAX_ATTEMPTS = 20

    @classmethod
    def allocate(cls, experiment_design):
        chamber = 0
        allocation = Allocation(experiment_design.num_chambers)
        for i in range(experiment_design.num_chambers):
            chamber = i + 1
            assay_mix = cls._make_random_legal_assay_mix(experiment_design)
            allocation.allocate(chamber, assay_mix)

        return allocation


    #------------------------------------------------------------------------
    # Private below.
    #------------------------------------------------------------------------

    @classmethod
    def _make_random_legal_assay_mix(cls, experiment_design):
        # Make random assay mixes until reach one that doesn't contain
        #  banned assay pairs.
        for i in range(cls._MAX_ATTEMPTS):
            mix = random.sample(
                experiment_design.assays, experiment_design.stack_height)
            if cls._does_not_contain_illegal_pair(mix, experiment_design):
                return mix
        raise RuntimeError(
            'Too many attempts to find legal assay mix (%d)' % cls._MAX_ATTEMPTS)

    @classmethod
    def _does_not_contain_illegal_pair(cls, mix, experiment_design):
        for a,b in experiment_design.dontmix:
            if ((a in mix) and (b in mix)):
                return False
        return True