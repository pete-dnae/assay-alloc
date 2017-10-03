class AssayCollections:
    """
    The AssayCollections class is a container that helps clients to create 
    and maintain named collections of assays. I.e. named collections of
    strings.
    """

    def __init__(self):
        self._collections = set()
