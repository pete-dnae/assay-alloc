from model.assay import Assay

class Pool:
    """
    Contains a pool of Assay(s) that remain to be allocated at any one time.
    Assays will be consumed from this pool during allocation.
    """

    def __init__(self, experiment_design):
        self.assays = set() # Of Assay(s)
        for assay_type in experiment_design.assay_types:
            for i in range(experiment_design.replicas[assay_type]):
                replica = i + 1
                self.assays.add(Assay(assay_type, replica))

    def __str__(self):
        assay_strings = [str(assay) for assay in self.assays]
        sorted_assay_strings = sorted(assay_strings)
        fmt = ', '.join(sorted_assay_strings)
        return fmt

    def assays_present_in_alphabetic_order(self):
        """
        Provides a sequence of the Assay(s) present, but in a deterministic order
        (to aid testing).
        """
        # We just use alphabetical order.
        return sorted(self.assays, key = lambda a: str(a))



