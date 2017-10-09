from collections import defaultdict

class AllocQuery:

    def __init__(self, allocation):
        self._alloc = allocation

    # Chamber centric

    def chambers_that_contain(self, assay):
        return self._alloc.assay_to_chambers[assay]

    def chambers_that_contain(self, targets):
        res = set()
        for assay in targets:
            res = res.union(self._alloc.assay_to_chambers[assay])
        return res

    def number_of_chambers_that_contain(self, targets):
        return len(self.chambers_that_contain(targets))

    # Assay centric

    def assay_types_present_in(self, chamber):
        return self._alloc.chamber_to_assays[chamber]

    def number_of_these_allocated(self, assay):
        return len(self._alloc.assay_to_chambers[assay])

    def number_of_assays_deployed(self):
        return sum([len(assay_list) for assay_list in
                    self.alloc._chamber_to_assays.values()])