from operator import itemgetter

class ExperimentReporter:
    """
    Offers a suite of queries about experiment results that provide conveniently
    packaged data ready to be used in reports or views.

    Specifically non-trivial queries that require cross referencing the
    ExperimentDesign with a resultant Allocation object.
    """

    def __init__(self, allocation, experiment_design):
        self.alloc = allocation
        self.design = experiment_design

    def did_this_chamber_fire(self, chamber):
        assay_types_in_chamber = self.alloc.assay_types_present_in(chamber)
        return len(assay_types_in_chamber.intersection(
            self.design.targets_present)) != 0

    def chambers_that_fired(self):
        fired = set()
        for chamber in self.alloc.all_chambers():
            if self.did_this_chamber_fire(chamber):
                fired.add(chamber)
        return fired

    def which_firing_chambers_contain(self, assay_type):
        chambers = set()
        for chamber in self.chambers_that_fired():
            if assay_type in self.alloc.assay_types_present_in(chamber):
                chambers.add(chamber)
        return chambers

    def format_assays_in_chambers_that_fired(self):
        """
        Provides a string like this "ACFI" - comprised of the set of assay types
        that are present in the chambers that fired. Sorted into alphabetical
        order.
        """
        assay_types = self.assays_in_chambers_that_fired()
        return ''.join(sorted(list(assay_types)))

    def assays_in_chambers_that_fired(self):
        """
        Provides the set of assay types that exist across all the chambers
        that fired.
        """
        chambers = self.alloc.which_chambers_contain_assay_types(
            self.design.targets_present)
        assay_types = set()
        for chamber in chambers:
            assay_types = assay_types.union(
                self.alloc.assay_types_present_in(chamber))
        return assay_types

    def firing_row_stats_rows(self):
        """
        Provides a data structure containing rows that describes the firing
        statistics of each assay type.
        The returned object is a sequence of dictionaries like this:
        {'assay_type': 'A', 'firing_message': '3 of 3 (100%)', 'percent': 100}

        The sequence is sorted according to the percentage value in the firing
        message - highest first.
        """
        assays = self.assays_in_chambers_that_fired()
        rows = []
        for assay in assays:
            row = self.firing_stats_for_assay(assay)
            rows.append(row)
        rows.sort(key = itemgetter('assay_type'))
        rows.sort(key = itemgetter('percent'), reverse=True)
        return rows

    def firing_stats_for_assay(self, assay_type):
        """
        Returns a dictionary like this:
        {
            'assay_type': 'A',
            'firing_message':
            '3 of 3 (100%)',
            'percent': 100,
            'status': 'good' # or 'bad' or None
        }
        """
        fired_count = len(self.which_firing_chambers_contain(assay_type))
        placed_count = self.design.replicas[assay_type]
        percent = int(100 * fired_count / float(placed_count))
        status = None
        if (percent == 100):
            if assay_type in self.design.targets_present:
                status = "good"
            else:
                status = "bad"
        message = '%d of %d (%3d%%)' % (fired_count, placed_count, percent)
        return {'assay_type': assay_type,
                'firing_message': message,
                'percent': percent,
                'status': status}







