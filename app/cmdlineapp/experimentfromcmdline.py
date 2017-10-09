import sys
from argparse import ArgumentParser

from experimentinputs.experimentdesign import ExperimentDesign


class ExperimentFromCmdLine:

    @classmethod
    def make(cls, argv):
        parser = ArgumentParser()

        parser.add_argument("--assays", type=int, required=True,
                            help="how many assay types to deploy")
        parser.add_argument("--chambers", type=int, required=True,
                            help="how many chambers")
        parser.add_argument("--stack", type=int, required=True,
                            help="how many assay per chamber")
        parser.add_argument("--dontmix", type=int, required=True,
                            help="how many assay pairs don't mix")
        parser.add_argument("--targets", type=int, required=True,
                            help="how many targets present")

        args = parser.parse_args()

        exp = ExperimentDesign()
        exp.assays = set([chr(ord('A') + i) for i in range(args.assays)])
        exp.num_chambers = args.chambers
        exp.stack_height = args.stack

        sorted_assays = sorted(list(exp.assays))

        for i in range(args.targets):
            exp.targets_present.add(sorted_assays.pop())

        exp.dontmix = []
        for i in range(args.dontmix):
            a = sorted_assays.pop()
            b = sorted_assays.pop()
            exp.dontmix.append([a, b])

        return exp
