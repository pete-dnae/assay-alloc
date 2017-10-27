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
        Makes the set of sets. The caller must specify what sized-sets
        are of interest. E.g. (2,3,4).
        """
        res = PossibleTargets()
        assay_types = experiment_design.assay_types

        for i in set_sizes_wanted:
            for combi in combinations(assay_types, i):
                frozen = frozenset(combi)
                res.sets.add(frozen)

        return res
