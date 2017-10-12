from model.assay import Assay

class Pool:

    def __init__(self, experiment_design):
        self.assays = set() # Of Assay(s)
        for _type in experiment_design.assay_types:
            for i in range(experiment_design.replicas[_type]):
                replica = i + 1
                self.assays.add(Assay(_type, replica))


    def most_favoured_assay(self):
        # We favour assays that we are most eager to remove from the pool.
        # This is a heuristic.
        # Let us choose those that are most picky about being colocated.
        types_in_pool = self._unique_assay_types_in_pool()
        most_picky = self._experiment_design.most_picky_mixer(types_in_pool)
        return self._any_assay_with_this_type(most_picky)


    def _unique_assay_names_in_pool(self):
        return {[assay.name for assay in self.assays]}


    def _any_assay_with_this_type(self, _type):
        assays = [assay for assay in self.assays if assay.type == _type]
        if len(assays) == 0:
            return None
        return assays.pop()


