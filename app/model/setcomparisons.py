class SetComparisons:
    """
    Provides various measures of how sets compare with each other.
    """

    @classmethod
    def how_similar_are_ab(cls, a, b):
        return len(a.intersection(b))

    @classmethod
    def how_disimilar_are_ab(cls, a, b):
        return -cls.how_similar_are_ab(a, b)

    @classmethod
    def how_disimilar_from_most_similar_of_these(cls, a, others):
        similars = sorted(
            others, key = lambda other: cls.how_disimilar_are_ab(a, other))
        most_similar = similars.pop(0)
        return cls.how_disimilar_are_ab(a, most_similar)

