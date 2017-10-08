import random

from model.allocation import Allocation

class AssayAllocator:

    def __init__(self, experiment_design):
        self.experiment_design = experiment_design

    def allocate(self):
        chamber = -1
        allocation = Allocation(self.experiment_design.num_chambers)
        while self._allocation_unfinished():
            chamber = (chamber + 1) % self.experiment_design.num_chambers

            incumbents = allocation.assays_present_in(chamber)
            candidates = self.experiment_design.assays
            candidates = candidates - incumbents
            candidates = self._remove_those_that_would_make_illegal_pairings(
                candidates, incumbents)
            assay = random.choice(candidates)
            allocation.allocate(chamber, assay)
        return allocation


    #------------------------------------------------------------------------
    # Private below.
    #------------------------------------------------------------------------

    def _allocation_unfinished(self, allocation):
        min_required = self.experiment_design.replicas

        # We are unfinished if any assay has not reached its replica count yet.
        for assay in self.experiment_design.assays:
            if allocation.number_of_these_allocated(assay) < min_required:
                return True
        return False


    def _remove_those_that_would_make_illegal_pairings(
            self, candidates, incumbents):
        for a,b in self.experiment_design.dontmix:
            if a in incumbents:
                candidates = candidates - {b}
            if b in incumbents:
                candidates = candidates - {a}
        return candidates