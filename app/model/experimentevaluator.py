from collections import defaultdict

class ExperimentEvaluator:

    @classmethod
    def evaluate(cls, allocation, experiment_design):
        results = {}

        num_firing = len(cls._firing_chambers(allocation, experiment_design))
        num_not_firing = experiment_design.num_chambers - num_firing
        fired_histogram = cls._fired_histogram(allocation, experiment_design)

        results['chambers fired'] = num_firing
        results['chambers not fired'] = num_not_firing
        results['assay stats in firing chambers'] = fired_histogram

        return results


    @classmethod
    def _firing_chambers(cls, allocation, experiment_design):
        chambers = set()
        for assay in experiment_design.targets_present:
            chambers = chambers.union(allocation.chambers_that_contain(assay))
        return chambers


    @classmethod
    def _fired_histogram(cls, allocation, experiment_design):
        # for each fired chamber,
        # ask alloc what assays present
        # for each of these assays incr count for that assay
        # sort assay names as f(count for that assay)
        # compose list of assay name:count, assay_name:count in sorted order

        count = defaultdict(int) # Keyed on assay
        for chamber in cls._firing_chambers(allocation, experiment_design):
            assays_present = allocation.assay_types_present_in(chamber)
            for assay in assays_present:
                count[assay] += 1
        sorted_assays = sorted(count.keys(), key = lambda assay: count[assay])
        report = ', '.join(
            ['%s: %d' % (assay, count[assay]) for assay in sorted_assays])
        return report
