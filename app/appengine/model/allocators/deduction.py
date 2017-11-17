"""
# EXPLANATION OF THE *DEDUCTION* ALGORITHM


# OVERVIEW

This algorithm tries to allocate multiple copies of a set of assays into
chambers combinatorially in such a way that each assay type gets a *reserved*
set of chambers, which, when they all *fire* guarantees the detection of that
assay's target. Regardless, that is, of which other assay targets might also be
present.  In other words, it guarantees to prevent false positive calls.

The algorithm is set-theoretic. Operating by modelling the interaction between
sets of chambers that contain assays with sets of assay targets that could be
present.

It works by making irreversible decisions about where to allocate the replicas
of the first assay, and then moving on to consider the next, using the previous
decisions (cumulatively) as constraints.


# MULTIPLE TARGETS PRESENT

Our allocation scheme must avoid false positives, even when multiple targets
are present. Say we choose to allocate assay P to the chamber set {1,2,9}. We
say that P has *reserved* this chamber set.  It is reserved in the sense that
we want to be able to rely on the fact that when all of {1,2,9} fire, that is
an unequivocal indicator that P's target is present.

It follows that we must make sure there can be no other reason for all of
{1,2,9} to fire when P's target is not present.  Regardless, that is, of what
other targets might be present. This is to guarantee there can be no false
positives.

In the P into {1,2,9} example case, we have chosen 3 chambers. But this
allocation cannot prevent the possibility of false positives if we accept that
as many as 3 targets might be present simultaneously. We can easily hypothesise
a set of 3 targets that would produce a false positive for P. Such a set of
targets must exclude P but contain targets that would cause each of {1,2,9} to
fire.  We can conjure such a targt set simply by sampling a different existing
assay from each of {1,2,9} and combining their targets into a set of 3.

It follows that we must set ourselves a reasonable upper limit for how many
targets might be present simultaneously *max_targets*, and then allocate at
least one more than this number of each assay to avoid inevitable false
positives scenarios. 

We wish also to be able to call when one chamber fails to file when it should
have done, and when one chamber does not fire when it should have done.
So we add an extra two of each assays.

I.e. num_targets + 3.


# METHOD

We begin by noting how many replicas of each assay we must allocate. I.e.
max_targets + 3.

Then we hypothesis all the possible chamber sets that are available to us at
the beginning of the process that we could consider to allocate each assay's
replicas. I.e. all the sets of size(replicas) that can be drawn from {all
chambers}. We refer to this as our *pool* of available chamber sets.

We allocate the replicas of the first assay, arbitrarily to the first chamber
set in the pool.

But that allocation step allows us to deduce that some of the chamber sets that
remain in the pool must no longer be consdidered candidates for subsequent
assay allocations; so we remove these from the pool before continuing to
allocating the next assay. And so on.

For the second and subsequent assays, we must also make sure we adhere to its
don't-mix rules. So instead of using simply the first chamber set from the
remaining pool, we look for one in the pool that does not contravene the mixing 
rules.


# WHICH CHAMBER SETS MUST BE REMOVED

See external PPT for the reason behind this.

The generalisation of the situation that must be avoided, is that no chamber
set can be reserved to call an assay, if that chamber set has more than 
(num_targets - 1) chambers in common, with any of the other reserved chamber 
sets.

So this defines the chamber sets we must remove from the pool after each assay
allocation (P). I.e. any chamber set that has more than (num_targets - 1) 
chambers in common with the chamber set used for P.
"""

from itertools import combinations

from model.allocation import Allocation
from model.possibletargets import PossibleTargets
from model.assay import Assay

class DeductionAllocator:
    """
    Provides an allocation algorithm based on avoiding all possible false 
    positives, no matter which targets are present.
    """


    def __init__(self, experiment_design):
        """
        Provide an ExperimentDesign object when initialising the allocator..
        """
        self._design = experiment_design
        # Prepare an Allocation object with which to register allocation
        # decisions as they progress.
        self.alloc = Allocation()
        # This algorithm requires that the number of replicas that get
        # placed for each assay, be at least one greater than the largest
        # number of simultaneous targets being considered.
        self._replicas = experiment_design.sim_targets + 3
        # Prepare the pool of chamber sets, that we can consider when searching
        # for a home of each assay's replicas. We deplete this as we go.
        # Nb. For replicas=6, chambers=20, there are approx 38,000 of these.
        self._pool_of_chamber_sets = \
                self._initial_set_of_available_chamber_sets(self._replicas)


    def allocate(self):
        """
        Entry point to the allocation algorithm.
        """

        # Work through the assay types in the priority order specified by
        # the experiment design, and for each, allocate all the replicas
        # in one go.
        for assay_P in self._design.assay_types_in_priority_order():
            chamber_set_used = self._allocate_all_replicas_of_this_assay_type(
                    assay_P)
            # Remove now from the chamber set pool, all those that would
            # inevitably cause false positives for the assay just allocated..
            self._curate_pool(chamber_set_used)

        return self.alloc


    #------------------------------------------------------------------------
    # Private / implementation methods below.
    #------------------------------------------------------------------------

    def _initial_set_of_available_chamber_sets(self, replicas):
        """
        Builds the initial set of chamber sets. (A set of sets), which can be 
        consdidered to house the replicas of each assay.
        """
        chambers = self._design.set_of_all_chambers()
        sets = set([frozenset(c) for c in combinations(chambers, replicas)])
        return sets

    def _allocate_all_replicas_of_this_assay_type(self, assay):
        """
        Find homes for all the replicas of assay(P). In the context of
        having previously allocated the replicas that precede assay(P) in
        allocation priority order.
        """

        # Use any encountered chamber set from the pool, that is legal for 
        # dontmix rules.
        chamber_set = self._find_legal_available_chamber_set(assay)

        if chamber_set is None:
            raise RuntimeError('Cannot allocate: %s' % assay)
        self.alloc.allocate(assay, chamber_set)
        return chamber_set


    def _find_legal_available_chamber_set(self, assay):
        """
        Look for a chamber set in the pool to which the given assay can
        legally be added to all of its chambers, without contravening any
        don't-mix rules.
        """
        for chamber_set in self._pool_of_chamber_sets:
            if self._compatible(chamber_set, assay):
                return chamber_set
        return None

    def _compatible(self, chamber_set, assay):
        """
        Is the given chamber set compatible with assay(P) being added, to all
        of its members - on the basis of assay(P)'s don't mix rules?
        """
        for chamber in chamber_set:
            occupants = self.alloc.assay_types_present_in(chamber)
            legal = self._design.can_this_assay_go_into_this_mixture(
                assay, occupants)
            if not legal:
                return False
        return True

    def _curate_pool(self, just_added_chamber_set):
        """
        Remove from our pool of available chamber sets, any that has
        more than (max_targets - 1) with the given set.
        """
        max_intersection = self._design.sim_targets - 1
        to_remove = set([cs for cs in self._pool_of_chamber_sets if 
                len(cs.intersection(just_added_chamber_set)) > 
                max_intersection])
        curated = self._pool_of_chamber_sets - to_remove
        self._pool_of_chamber_sets = curated
