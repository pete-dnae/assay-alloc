from collections import defaultdict
import yaml
import json
import pprint

class ExperimentEvaluator:

    def __init__(self, allocation, experiment_design):
        self.alloc = allocation
        self.design = experiment_design

    def evaluate(self):

        d = ['first', 'second', {'results': {'b': 42, 'a': 99}}, 'third']
        d = [self.mk_header(), self.mk_design(), self.mk_allocation(), self.mk_calling()]

        return yaml.dump(d)


    def mk_header(self):
        return {'Note': 'This is machine readable YAML format.'}

    def mk_design(self):
        return {'Experiment Setup':[
            {'Numbers of chambers': self.design.num_chambers},
            {'Assay types deployed': ''.join(sorted(list(self.design.assays)))},
            {'Assays per chamber': self.design.stack_height},
            {'Do not mix': self.design.dontmix},
            {'Targets present': ''.join(sorted(list(self.design.targets_present)))},
            ]
        }

    def mk_allocation(self):
        return {'Allocation':[
            {'Chamber map': self._mk_chamber_map()},
            {'Assays by how many deployed': self._mk_deployed_count()},
            ]
        }

    def mk_calling(self):
        return 'calling'

    def _mk_chamber_map(self):
        res = []
        for i in range(self.design.num_chambers):
            chamber = i + 1
            present = ''.join(sorted(list(self.alloc.assay_types_present_in(chamber))))
            line = [chamber, present]
            res.append(line)
        return res

    def _mk_deployed_count(self):
        count_to_assays = defaultdict(list)
        for assay in self.design.assays:
            count = self.alloc.number_of_these_allocated(assay)
            count_to_assays[count].append(assay)
        res = []
        for count in sorted(count_to_assays.keys()):
            assays = count_to_assays[count]
            assays = ''.join(assays)
            line = [count, assays]
            res.append(line)
        return res



