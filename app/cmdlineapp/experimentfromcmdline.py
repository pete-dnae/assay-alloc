from argparse import ArgumentParser

from model.experimentdesign import ExperimentDesign


class ExperimentFromCmdLine:

    @classmethod
    def make(cls, argv):
        parser = ArgumentParser()
        parser.usage = \
            'Please provide command line arguments like this:\n' + \
            '--assays 20 --replicas 3 ' + \
            '--chambers 24 --dontmix 3 --targets 2'

        parser.add_argument("--assays", type=int, required=True,
                            default=20,
                            metavar=20,
                            help="how many assay types to deploy")
        parser.add_argument("--replicas", type=int, required=True,
                            help="how many replicas")
        parser.add_argument("--chambers", type=int, required=True,
                            help="how many chambers")
        parser.add_argument("--dontmix", type=int, required=True,
                            help="how many assay pairs don't mix")
        parser.add_argument("--targets", type=int, required=True,
                            help="how many targets present")

        args = parser.parse_args()

        assays = args.assays
        chambers = args.chambers
        replicas = args.replicas
        dontmix = args.dontmix
        targets = args.targets

        return cls.make_from_params(assays, chambers, replicas, dontmix, targets)
