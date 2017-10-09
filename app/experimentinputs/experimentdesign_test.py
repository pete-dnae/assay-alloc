from experimentinputs.experimentdesign import ExperimentDesign

class MakeReferenceExperiment:

    @classmethod
    def make(cls):
        exp = ExperimentDesign()
        exp.assays = set(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        exp.num_chambers = 100
        exp.stack_height = 4
        exp.dontmix = [['A', 'B'], ['C', 'D']]

        exp.targets_present = {'N', 'F'}

        return exp