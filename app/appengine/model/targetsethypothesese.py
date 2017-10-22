from itertools import combinations

class TargetSetHypothesese:
    """
    During the assay to chamber allocation process, we do not know which targets
    will be present during the experiment execution.
    It is most likely that one target will be present, but we capture here
    the sets possible of size 2 to use in allocation heuristics.
    """

    def __init__(self):
        self.sets = set() # Of frozen set, of assay type.

    @classmethod
    def create(cls, experiment_design):
        res = TargetSetHypothesese()
        assay_types = experiment_design.assay_types

        for i in (3,2):
            for combi in combinations(assay_types, i):
                frozen = frozenset(combi)
                res.sets.add(frozen)

        return res
