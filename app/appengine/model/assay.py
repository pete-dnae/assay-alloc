class Assay:
    """
    Represents an assay that can be allocated to a chamber. Including which of
    the replicas it is, when several assays of this type are required.
    """

    def __init__(self, type, replica):
        self.type = type # E.g. 'B'
        self.replica = replica # E.g. 3 for the third instance.

    def __eq__(self, other):
            return hash(self) == hash(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):
        # Returns e.g. 'B3'
        return ('%s%d' % (self.type, self.replica))
