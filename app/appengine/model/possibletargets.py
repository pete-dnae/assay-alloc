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
    def create(cls, experiment_design, how_many_targets):
        """
        Makes the set of sets. The caller must specify the size of set
        they want. This should be largest you are interested in. For example,
        if you want to model up to 5 simultaneously present targets, specify 5.
        """
        res = PossibleTargets()
        assay_types = experiment_design.assay_types_in_priority_order()

        sets = []
        # Note that combinations() guarantees a deterministic ordering.
        how_many_targets = 2
        for combi in combinations(assay_types, how_many_targets):
            sets.append(set(combi))

        res = PossibleTargets()
        # Prefer a tuple to speed up 'contains' queries down the line.
        # Take the hit of conversion from list to tuple here, where it need
        # only be done once.
        res.sets = tuple(sets)
        return res
