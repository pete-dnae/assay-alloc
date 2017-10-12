class Assay:

    def __init__(self, type, replica):
        self.type = type # E.g. 'B'
        self.replica = replica # E.g. 3 for the third instance.


    def __str__(self):
        # Returns e.g. 'B3'
        return ('%s%d' % (self.type, self.replica))
