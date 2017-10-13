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



