class PlacementInProgress(object):
    """
    The PlacementInProgress class holds a snapshot of the allocation state at 
    any stage of an algorithm that is iterating in search of a solution.

    Calling code should use it immutably, and make copies as appropriate to allow
    roll-back when avenues are exhausted. There is a copy helper function to make
    this easier.
    """

    def __init__(self):
        pass

    def copy(self)
        return None

