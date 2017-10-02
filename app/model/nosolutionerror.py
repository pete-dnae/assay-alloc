class NoSolutionError(Exception):
    """
    The NoSolutionError is an Exception that encapsulates no global solution 
    being reachable. It is strictly an exception, and should not be used to
    indicate the failure of a test or experiment in part of the algorithm - 
    because that kind of failure is not an error.
    """

    def __init__(self):
        super(self)

    todo - know this constructor syntax is not right
