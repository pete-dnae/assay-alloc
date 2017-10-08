from collections import defaultdict

class Allocation:

    def __init__(self, num_chambers):
        self.chamber_to_assays = defaultdict(set)
        self.assay_to_chambers = defaultdict(set)


    def allocate(self, chamber, assay_mix):
        for assay in assay_mix:
            self.chamber_to_assays[chamber].add(assay)
            self.assay_to_chambers[assay].add(chamber)


    def assays_present_in(self, chamber):
        return self.chamber_to_assays[chamber]


    def number_of_these_allocated(self, assay):
        return len(self.assay_to_chambers[assay])

    def number_of_assays_deployed(self):
        return sum([len(assay_list) for assay_list in self.chamber_to_assays.values()])
