from itertools import combinations

class PossibleTargets:
    """
    Holds knowledge about what set of targets could be present (theoretically)
    during an experiment. In other words, roughly speaking, all possible sets
    of targets that can be made from the set of all targets.
    """

    def __init__(self):
        # Whilst logically we wish to expose a set of sets, we choose a
        # sorted sequence of sets. Because we anticipate that client 
        # algorithms will want to iterate over them in a deterministic 
        # order - so as to make automated testing repeatable.

        self.sets = () # Of set() of assay type.

    @classmethod
    def create(cls, experiment_design, set_sizes_wanted):
        """
        Makes the set of sets. The caller must specify what sized-sets
        are of interest. E.g. (2,3,4).
        """
        res = PossibleTargets()
        assay_types = experiment_design.assay_types

        sets = []
        for i in set_sizes_wanted:
            # Note that combinations() guarantees a deterministic ordering.
            for combi in combinations(assay_types, i):
                sets.append(set(combi))

        res = PossibleTargets()
        # Prefer a tuple to speed up 'contains' queries down the line.
        # Take the hit of conversion from list to tuple here, where it need
        # only be done once.
        res.sets = tuple(sets)
        return res
