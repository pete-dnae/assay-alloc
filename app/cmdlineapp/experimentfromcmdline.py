from argparse import ArgumentParser

from model.experimentdesign import ExperimentDesign


class ExperimentFromCmdLine:

    @classmethod
    def make(cls, argv):
        parser = ArgumentParser()
        parser.usage = \
            'Please provide a command line like this:\n' + \
            'assay-alloc --assays 10 --max_targets 3 --chambers 12 --dontmix 2'

        parser.add_argument("--assays", type=int, required=True,
                            default=20,
                            metavar=20,
                            help="How many assay types to deploy")
        parser.add_argument("--max_targets", type=int, required=True,
                            help="Guarantee no false positives for up to " + \
                            "this many targets present simultaneously")
        parser.add_argument("--chambers", type=int, required=True,
                            help="How many chambers")
        parser.add_argument("--dontmix", type=int, required=True,
                            help="Choose the first <N> first/last " + \
                            "assays as the ones that must not mix.")

        args = parser.parse_args()

        assays = args.assays
        max_targets = args.max_targets
        chambers = args.chambers
        dontmix = args.dontmix

        return ExperimentDesign.make_from_params(
                assays, chambers, max_targets, dontmix)
