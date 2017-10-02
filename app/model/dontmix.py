class DontMix(object):
    """
    The DontMix class encapsulates a set of assay pairs that must not be mixed.
    """

    def __init__(self):
        self.pairs = set()

    def add_pair(self, assay_a, assay_b):
        self.pairs.add((assay_a, assay_b))

    def copy(self):
        return self.pairs.copy()
