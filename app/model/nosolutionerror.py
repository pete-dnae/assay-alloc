class NoSolutionError(Exception):
    """
    The NoSolutionError is an Exception that encapsulates no solution 
    being reachable (in a particular context). If the context is the global
    solution it represents a complete allocation failure. But it can also signal
    a failed attempt lower in the algorithm, which can/should be recovered from.
    """

    def __init__(self):
        super(self)

    todo - know this constructor syntax is not right
