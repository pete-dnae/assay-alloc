class AssayCollections(object):
    """
    The AssayCollections class is a library of AssayCollection(s).
    It exists mainly to make it convenient to serialise a the whole thing so that
    it can be persisted in a database.
    """

    def __init__(self):
        self._collections = set()
k
