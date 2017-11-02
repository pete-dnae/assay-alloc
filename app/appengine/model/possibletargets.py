from itertools import combinations

class PossibleTargets:
    """
    Holds knowledge about what set of targets could be present (theoretically)
    during an experiment. In other words, roughly speaking, all possible sets
    of targets that can be made from the set of all targets.

    Truncated to avoid very large sets, see within.
    """

    def __init__(self):
        # Whilst logically we wish to expose a set of sets, we choose a
        # sorted sequence of sets. Because we anticipate that client 
        # algorithms will want to iterate over them in a deterministic 
        # order - so as to make automated testing repeatable.

        self.sets = () # Of set() of assay type.

    @classmethod
    def create(cls, experiment_design, sim_targets):
        """
        Makes the set of sets. 
        The client must speicify how many simultaneous targets-present
        should be modelled. This has a computational cost that goes up
        factorily.
        """
        res = PossibleTargets()
        assay_types = experiment_design.assay_types_in_priority_order()

        sets = []
        # Note that combinations() guarantees a deterministic ordering.
        for combi in combinations(assay_types, sim_targets):
            sets.append(set(combi))

        res = PossibleTargets()
        # Prefer a tuple to speed up 'contains' queries down the line.
        # Take the hit of conversion from list to tuple here, where it need
        # only be done once.
        res.sets = tuple(sets)
        return res
