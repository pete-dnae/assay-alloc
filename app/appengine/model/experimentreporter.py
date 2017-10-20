from collections import defaultdict
import yaml

class ExperimentReporter:
    """
    Knows how to make a report on the outcome of an experiment by looking up
    what went on in the Allocation object provided and the ExperimentDesign
    provided.
    """

    def __init__(self, allocation, experiment_design):
        self.alloc = allocation
        self.design = experiment_design

    def report(self):
        lines = []
        lines.append('\n')
        lines.extend(self._assays())
        lines.extend(self._experiment_design())
        lines.append('\n')
        lines.append('Allocation...')
        lines.append('\n')
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

    def _assays(self):
        res = ['Assay Replicas To Be Allocated:', '\n']
        assay_lines = self.design.format_all_assays()
        res.extend(assay_lines)
        return res

    def _experiment_design(self):
        lines = ['\n']
        lines.append('Dont mix: %s' % self.design.dontmix)
        lines.append('\n')
        lines.append('Simulated targets present: %s' % self.design.targets_present)
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
        assay_message = defaultdict(str)

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
            assay_message[assay_type] = \
                self._assay_message(assay_type, count, num_allocated)
        assays_sorted_by_percent = reversed(sorted(
            assay_percent.keys(), key=lambda assay: assay_percent[assay]))
        # 3 out of 3 chambers that contain A fired (100%)
        res = []
        for assay in assays_sorted_by_percent:
            res.append(
                '%d out of %d chambers that contain <%s> fired. (%03d%%) %s' %
               (assay_counts[assay],
                self.alloc.number_of_this_assay_type_allocated(assay),
                assay,
                assay_percent[assay],
                assay_message[assay]))
        return res


    def _assay_message(self, assay_type, count, num_allocated):
        if count != num_allocated:
            return ''
        if assay_type in self.design.targets_present:
            return 'POSITIVE CALL'
        else:
            return 'POSITIVE CALL (FALSE)'





