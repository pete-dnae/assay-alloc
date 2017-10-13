from collections import defaultdict
import yaml

class ExperimentReporter:

    def __init__(self, allocation, experiment_design):
        self.alloc = allocation
        self.design = experiment_design

    def report(self):
        d = [self._mk_header(),
             self._mk_design(),
             self._mk_allocation(),
             self._mk_calling()]
        return yaml.dump(d)


    def _mk_header(self):
        return {'Note': 'This is machine readable YAML format.'}

    def _mk_design(self):
        return {'Experiment Setup':[
            {'Numbers of chambers': self.design.num_chambers},
            {'Assay types deployed': ''.join(sorted(list(self.design.assay_types)))},
            {'Do not mix': self.design.dontmix},
            {'Targets present': ''.join(sorted(list(self.design.targets_present)))},
            ]
        }

    def _mk_allocation(self):
        return {'Allocation':[
            {'Chamber map': self._mk_chamber_map()},
            ]
        }


    def _mk_calling(self):
        did_fire = self.alloc.number_of_chambers_that_contain_assay_types(
                     self.design.targets_present)
        did_not_fire = self.design.num_chambers - did_fire
        return {'Calling':[
            {'Number of chambers that fired':did_fire},
            {'Number of chambers that did not fire':did_not_fire},
            {'Assays, in order of prevalence in firing chambers': self._mk_prevalence()},
            ]
        }

    def _mk_chamber_map(self):
        return self.alloc.format_chambers()

    def _mk_prevalence(self):
        assay_counts = defaultdict(int)  # keyed on assay
        fired = self.alloc.which_chambers_contain_assay_types(
            self.design.targets_present)
        for chamber in fired:
            assays = self.alloc.assay_types_present_in(chamber)
            for assay in assays:
                assay_counts[assay] = assay_counts[assay] + 1
        # Convert assay counts to percentages of those deployed
        for assay, count in assay_counts.items():
            num_allocated = self.alloc.number_of_this_assay_type_allocated(assay)
            percent = 100 * count / num_allocated
            assay_counts[assay] = percent
        assays_sorted_by_count = reversed(sorted(
            assay_counts.keys(), key=lambda assay: assay_counts[assay]))
        res = []
        for assay in assays_sorted_by_count:
            count = assay_counts[assay]
            line = [assay,
                    '%d%% of those deployed' % count]
            res.append(line)
        return res






