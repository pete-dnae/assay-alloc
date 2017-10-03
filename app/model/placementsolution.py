class PlacementSolution:
    """
    The PlacementSolution class encapsulates a successful placement solution
    being found. It holds the PlacementInProgress that has been decreed to be a
    success, and provides additional query apis. This is intended to keep the
    PlacementInProgress solely about holding state, and avoiding cluttering it
    with the additional query apis.
    """

    def __init__(self, placement_in_progress):
        self.placement_in_progress = placement_in_progress 


    def export(sefl):
        """ An example api method.
        """
        pass
