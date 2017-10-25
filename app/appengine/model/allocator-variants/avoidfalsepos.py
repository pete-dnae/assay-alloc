
from model.allocation import Allocation

class AvoidsFP:
    """
    Encapsulates an allocation algorithm that deploys an allocation strategy
    based on avoiding all possible false positives, no matter which targets
    are present.
    """


    def __init__(self, experiment_design):
        """
        Provide an ExperimentDesign object.
        """
        self._design = experiment_design
        self.alloc = Allocation(experiment_design.num_chambers)
        self.targets_hypothesese = foo


    def allocate(self):
        """
        Entry point to the allocation algorithm.
        """

        # Work through the assay types in the priority order specified by
        # the experiment design.
        for assay_type in self._design.assay_types_in_priority_order():
            self._allocate_all_replicas_of_this_assay_type(assay_type)

        return self.alloc


    #------------------------------------------------------------------------
    # Private below.
    #------------------------------------------------------------------------

    def _allocate_this_assay_type(self, assay_type):
        replicas = self._design.replicas[assay_type]
        """
        Decide where to allocate all the replicas of the given assay type and
        update our Allocation object with this new status.
        """

        """
        chambers = all chambers

        incompatible assays = wont mix with assay_type

        chambers = remove any that contain an incompatible assay 

        chamber_sets = all sets of size<replica> from chambers

        for chamberset in chamber_sets:
            worked = can allocate in this chamber set(assay_type, chamberset)
            if worked:
                register allocation
                return
        oh dear, have to give up, no soln for this assay type
        """

    def can allocate in this chamber set(assay type, chamber set):
        for t_hypoth in all target set hypoth:
            creates_fp = doesalloc-create-fp(assay_type, chamberset, t_hypoth)
            if creates_fp:
                return false # sufficient cond to reject chamberset
        # this set works across all target h sets, so say can alloc
        return true

    def alloc-creates_fp(assay_type, chamberset, t_hypoth):
        # Only need 1 chamber to be free of every t in t_hypoth to say no
        for chamber in chamberset:
            if chamber contains none of(chamber, t_hypoth)
                return false
        return True
