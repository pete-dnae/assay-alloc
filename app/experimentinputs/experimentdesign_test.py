from experimentinputs.experimentdesign import ExperimentDesign

class MakeReferenceExperiment:

    @classmethod
    def make(cls):
        exp = ExperimentDesign()
        exp.assays = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split()
        exp.num_chambers = 100
        exp.replicas = 3
        exp.dontmix = (('A', 'B'), ('C', 'D'))

        return exp