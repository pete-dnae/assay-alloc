from collections import defaultdict
import yaml

class ExperimentReporter:

    def __init__(self, allocation, experiment_design):
        self.alloc = allocation
        self.design = experiment_design

    def report(self):
        lines = []
        lines.append('\n')
        lines.extend(self._experiment_design())
        lines.append('\n')
        lines.append('Allocation...')
        lines.extend(self.alloc.format_chambers())
        lines.append('\n')
        lines.append(self._firing_chambers())
        lines.append('\n')
        lines.append('Only the targets: %s should get 100%%' %
                     self.design.targets_present)
        lines.append('\n')
        lines.extend(self._calling())
        lines.append('\n')
        return lines

    def _experiment_design(self):
        lines = []
        lines.append('Assay types: %s' %
                     ''.join(sorted(list(self.design.assay_types))))
        # Although the ExperimentDesign models a replica count for each
        # assay, we are currently setting them all to be the same.
        lines.append('Replicas: %d' % self.design.replicas['A'])
        lines.append('Numer of chambers: %d' % self.design.num_chambers)
        lines.append('Dont mix: %s' % self.design.dontmix)
        lines.append('Targets: %s' % self.design.targets_present)
        return lines

    def _firing_chambers(self):
        chambers = self.alloc.which_chambers_contain_assay_types(
            self.design.targets_present)
        chambers = ['%03d' % i for i in chambers]
        chambers = ' '.join(chambers)
        return('Firing chambers: %s' % chambers)

    def _calling(self):
        assay_counts = defaultdict(int)  # keyed on assay type
        assay_percent = defaultdict(int)
        fired = self.alloc.which_chambers_contain_assay_types(
            self.design.targets_present)
        for chamber in fired:
            assay_types = self.alloc.assay_types_present_in(chamber)
            for assay_type in assay_types:
                assay_counts[assay_type] += 1
        # Capture assay counts as percentages of those deployed
        for assay_type, count in assay_counts.items():
            num_allocated = self.alloc.number_of_this_assay_type_allocated(
                assay_type)
            percent = 100 * count / num_allocated
            assay_percent[assay_type] = percent
        assays_sorted_by_percent = reversed(sorted(
            assay_percent.keys(), key=lambda assay: assay_percent[assay]))
        # 3 out of 3 chambers that contain A fired (100%)
        res = []
        for assay in assays_sorted_by_percent:
            res.append('%d out of %d chambers that contain <%s> fired. (%d%%)' %
                   (assay_counts[assay],
                    self.alloc.number_of_this_assay_type_allocated(assay),
                    assay,
                    assay_percent[assay]))
        return res







