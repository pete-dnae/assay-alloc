from collections import defaultdict

class Allocation:

    def __init__(self, num_chambers):
        self.chamber_to_assays = defaultdict(set)
        self.assay_to_chambers = defaultdict(set)

    def allocate(self, chamber, assay):
        self.chamber_to_assays[chamber].add(assay)
        self.assay_to_chambers[assay].add(chamber)


    def assays_present_in(self, chamber):
        return self.chamber_to_assays[chamber]
