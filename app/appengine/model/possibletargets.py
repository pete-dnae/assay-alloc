from itertools import combinations

class PossibleTargets:
    """
    Holds knowledge about what set of targets could be present (theoretically)
    during an experiment. In other words, roughly speaking, all possible sets
    of targets that can be made from the set of all targets.
    """

    def __init__(self):
        self.sets = set() # Of frozen set, of assay type.

    @classmethod
    def create(cls, experiment_design, set_sizes_wanted):
        """
        Draws all the sets of size (p,q,r) that can be made from the set
        of all targets.
        """
        res = PossibleTargets()
        assay_types = experiment_design.assay_types

        for i in set_sizes_wanted:
            for combi in combinations(assay_types, i):
                frozen = frozenset(combi)
                res.sets.add(frozen)

        return res
