"""
ALGORITHM EXPLANATION

OVERVIEW


This algorithm tries to allocate multiple copies of a set of assays into
chambers combinatorially in such a way that each assay type gets a *reserved*
set of chambers, which, when they all *fire* guarantees the detection of that
assay target, regardless of which other assay targets might also be present.
In other words, it guarantees to prevent false positive calls.

Nb, In what follows, we use the terms assays and targets almost
interchangeably. 

The algorithm is set-theoretic. Operating by modelling the interaction between 
sets of chambers with sets of targets.

It is based on two recognized algorithmic concepts:

- Bin Packing

    https://en.wikipedia.org/wiki/Bin_packing_problem

- Dynamic Programming

    https://en.wikipedia.org/wiki/Dynamic_programming

It adopts the bin-packing paradigm by making irreversible decisions about
where to allocate the first assay, and then moving on to consider the next,
using the previous decisions (cumulatively) as constraints.

It adopts the dynamic programming principle by building up knowledge as it
goes about where false-positive calls have been ruled-out, and only
re-evaluating those that could be compromised as each new assay type is mixed
in.


METHOD

We iterate over assay types in some priority order. E.g. (A,B,C...Q) etc.  In
each iteration we allocate all of the replicas of that assay (P) to a chamber
set. For example if 3 replicas are needed for (P), we might decide to use
{1,2,9}.  We refer to that chamber set as the chamber set that has been
*reserved* by assay (P).  It is reserved in the sense that we want to be able
to rely on the fact that when all of {1,2,9} fire, that is an unequivocal
indicator that (P) is present.  It follows that we must make sure there can be
no other reason for all of {1,2,9} to fire when (P) is not present.
Regardless, that is, of what other targets might be present. This is to
guarantee there can be no false positives.

We describe the allocation as a whole as *vulnerable* (to false positive
calls), when there is some particular combinations of targets that could be
present, which would cause all of the chambers in one of the reserved chamber
sets to fire, when its intended target is not present.

Our approach as we incrementally consider each assay type (P) in turn, is to
hypothesise chamber sets that we might use to house P's replicas. We consider
all legal chamber set possibilities (of the right size) in fact. For example:
{1,2,3}, {1,2,4}, {1,2,5}... {17,12,24} ... etc. Legal being defined as 
allocations that do not break the don't-mix rules specified in an experiment
mandate that is passed in to the algorithm from the outside world.

To measure the *vulnerability* we must consider target sets that might be
present. For example {A} on its own, or {A,B}, or {A,N,F} and so on. In fact we
look at all the possible target sets that could be present. (See Note 001 
below).

If we can find, for any of our reserved chamber sets e.g. {1,2,9}, a potential
targets-present set (e.g. {A,B,C,D} that would cause all of {1,2,9} to fire
despite the assay that reserved {1,2,9} not being present, we can conclude that
that particular allocation state, as a whole, is *vulnerable*.

When this happens we reject that chamber-set hypothesis as a home for the assay
type under consideration (P), and move on to consider the next hypothesis. If
we exhaust the possible chamber sets to use for (P), we are stuck and have
to abort. Conversely, if we make it to the end of the assays types which are
mandated by the experiment, we know we have produced an invulnerable allocation
scheme.

It is necessary to revisit the vulnerability of the entire allocation afresh as
we consider each assay type, because the conclusions we reached last time round
must be re-examined in the context of an additional assay having been
allocated. For example, now that we have allocated the replicas of 'P' - does
that mean that the chambers in the reserved chamber set for 'O' could now all
fire because of the newly added P's, despite 'O' not being present?

# NOTE (001) OPTIMIZATIONS, LIMITATIONS, AND *IMPLICATIONS*.

The number of possible targets-present sets, goes up factorially with how 
many simultaneously-present targets we wish to protect ourselves from.

If are working with 20 assay types:

-  there are    1140 possible target sets of size 3
-  there are    4845 possible target sets of size 4
-  there are  15,504 possible target sets of size 5
-  there are  38,760 possible target sets of size 6
-  there are  77,520 possible target sets of size 7
-  there are 125,970 possible target sets of size 8

The algorithm has a setting in it that makes it ignore target sets with more
than N members. We'll call this *sim_targets*. (A pragmatic compromise, to 
avoid very long program run-times). 

The algorithm does not model any target sets smaller than this upper limit. For
example for if we are working with sim_targets=5, a set could be {ADNPS}. We
can safely ignore all the smaller subsets like {ADN}, or {DPS} because any
false positives that would be caused by the presence of all the targets in one
of these smaller sets would also be caused by the presence of the larger
superset {ADNPS}.

# LINKAGE TO NUMBER OF REPLICAS.

If we want to guarantee that false positives cannot be produced, and we
decide that sim_targets=5, then every assay must have more than 5 replicas
(n_replicas).  At least one more.

This can be shown easily by considering the simpler case of sim_targets=3, and
n_replicas=3 (insufficient). Say we reserved {1,4,7} for assay 'P'. It is
inevitable there exists a set of 3 targets that when present would cause
{1,4,7} to fire despite 'P' not being present? Any set that contains a
representative assay drawn from the occupants of each of {1,4,7} would do.
Conversely, if we raise n_replicas to 4 and use for example {1,4,7,14}, and
leave n_targets at 3. We stand a chance of finding a set of 3 targets that will
not cause all of {1,4,7,14} to fire.

# RESILIENCE TO FAILING CHAMBERS

We stated above, that n_replicas must be at least one greater than sim_targets.
Consider that target 'P' is present, and we allocated the assays that target
'P' to {1,3,5,12}. We know that many fluke targets-present combinations could
cause three of these to fire, but that only the presence of 'P' will cause all
four to fire. However it only takes one of these chambers to misbehave, and we
lose our ability to detect P.

If however we insist that n_replicas be at least 2 bigger than sim_targets, we
can tolerate the failure of any one chamber.

IMPLEMENTATION OPTIMISATIONS

It is necessary to introduce some optimisations to prevent the code from taking
an excessive amount of time to run.  The code ostensibly operates nested loops
that consider all the relevant possible available within its constraints, at
each stage. However we can deduce that large chunks of these can be skipped
because they will not provide any new information. See the code comments to see
where these are deployed.
"""

from itertools import combinations

from model.allocation import Allocation
from model.possibletargets import PossibleTargets
from model.assay import Assay

class AvoidsFP:     # FP = False-Positive
    """
    Provides an allocation algorithm based on avoiding all possible false 
    positives, no matter which targets are present.
    """

    """
    A NOTE ON VARIABLE NAMING CONVENTIONS

    This code, in places, adopts a naming convention that is intended to convey
    both the generic nature of the variable, as well as a concrete example.

    Like this:

        chamber_set_147     # A chamber set that could be {1,4,7}
        target_set_ADFN     # A set of targets that could be {A,D,F,N}
        assay_P             # An assay type that could be P

    """


    def __init__(self, experiment_design):
        """
        Provide an ExperimentDesign object when initialising the allocator..
        """
        self._design = experiment_design
        # This is a diagnostics channel to support unit testing.
        # A few parts of the code send it messages to provide evidence that
        # something happened (if it is none none).
        self.tracer = None
        # Prepare an Allocation object with which to register allocation
        # decisions as they progress.
        self.alloc = Allocation()
        # Prepare the set of all possible (hypothetical) target sets to 
        # consider during the allocation process.
        # NB, there are circa tens-of-thousands of these if we draw from a 
        # 20-member superset, and constrain the subsets to 5 or fewer members.
        self._possible_target_sets = PossibleTargets.create(
            experiment_design, experiment_design.sim_targets)
        # This algorithm requires that the number of replicas that get
        # placed for each assay, be at least one greater than the largest
        # number of simultaneous targets being considered.
        self._replicas = experiment_design.sim_targets + 1


    def allocate(self):
        """
        Entry point to the allocation algorithm.
        """

        # Work through the assay types in the priority order specified by
        # the experiment design, and for each, allocate all the replicas
        # in one go.
        for assay_P in self._design.assay_types_in_priority_order():
            self._allocate_all_replicas_of_this_assay_type(assay_P)

        return self.alloc


    #------------------------------------------------------------------------
    # Private / implementation methods below.
    #------------------------------------------------------------------------

    def _allocate_all_replicas_of_this_assay_type(self, assay_P):
        """
        Find homes for all the replicas of assay_P. In the context of
        having previously allocated the replicas that precede assay P in
        allocation priority order.
        """

        possible_chamber_sets = self._assemble_chamber_sets_to_consider_for(
            assay_P)

        # Use the first chamber set we encounter that does not put the overall
        # allocation into a vulnerable state. (Where it can produce false
        # positives.)

        for chamber_set_147 in possible_chamber_sets:
            # We cannot consider chamber sets which have already been
            # reserved for another assay.
            if self.alloc.is_chamber_set_already_reserved(chamber_set_147):
                self._trace('Skipping %s because already reserved' %
                        chamber_set_147) 
                continue
            # Would adding assay_P to this chamber set make the allocation
            # as a whole  vulnerable?
            vulnerable = self._is_allocation_with_assay_P_added_vulnerable(
                assay_P, chamber_set_147)

            # If it is not vulnerable, we need look no further. We've found a
            # suitable set of chambers for assay_P, so we tell our allocation
            # object to register and reserve them thus.

            if not vulnerable:
                self.alloc.allocate(assay_P, chamber_set_147)
                return
            # If we get to here, that chamber set is vulnerable. Never mind,
            # let's move on to the net chamber set hypothesis.

        # If we get here, we couldn't find a suitable chamber set and have
        # to give up and abort.
        raise RuntimeError('Cannot allocate: %s' % assay_P)


    def _assemble_chamber_sets_to_consider_for(self, assay_P):
        """
        Provide the chamber sets that might be a good place to allocate
        the replicas of the given assay (P). A set of (frozen) sets.
        For example: { {1,2,7}, {1,2,8}, ... {3,5,9} ... }
        """
        chambers = self._design.set_of_all_chambers()
        chambers = self._remove_incompatible_chambers(chambers, assay_P)
        chamber_sets = self._draw_possible_chamber_sets_of_size(
                chambers, size=self._replicas)
        return chamber_sets


    def _is_allocation_with_assay_P_added_vulnerable(
            self, assay_P, chamber_set_for_P):
        """
        Would the current allocation state, once assay_P is added into the
        suggested chamber set, become vulnerable to false postives?
        """

        # The rule here is that the resultant allocation is vulnerable, if any
        # of the reserved chamber sets we've established so far have any reason
        # to all-fire, other than because their reserving-assay is present
        # among the targets present.

        # Temporarily, add in assay_P as instructed.
        self.alloc.allocate(assay_P, chamber_set_for_P)

        # Consider all the reserved chamber sets, but only those that
        # we just potentially compromised by adding P into them.
        filtered_reserved_chamber_sets = \
                self._filter_reserved_chamber_sets(chamber_set_for_P)

        for reserved_chamber_set in filtered_reserved_chamber_sets:
            # Reminder about what we know about this chamber set:
            # 1) Which assay (F) reserved it.
            # 2) (F) exists in each of its chambers.
            # 3) The assay we just added (P) exists in at least one of its 
            #    chambers.
            # 4) We know it wasn't vulnerable up till the point we added
            #    (P) into it.

            reserving_assay = self.alloc.which_assay_reserved_this_chamber_set(
                    reserved_chamber_set)

            # Consider all the possible targets-present sets that could exist.
            for target_set_ADFN in self._possible_target_sets.sets:

                # Do inexpensive tests first that avoid the more expensive
                # all-firing test.
                if reserving_assay in target_set_ADFN:
                    self._trace('Can avoid all firing test for %s' % 
                            target_set_ADFN) 
                    continue # Skip to next target set.

                # Now we've reached the more expensive test.
                all_fire = self._all_would_fire(reserved_chamber_set, 
                        reserving_assay, target_set_ADFN)
                if all_fire:
                    # The allocation as a whole is vulnerable, but before
                    # we return, let's leave things as we found them.
                    self.alloc.unreserve_alloc_for(assay_P)
                    return True # Is vulnerable.

                # Good, this this target set w.r.t. this chamber set is
                # does not make the allocation vulnerable.

            # Good this, chamber set does not make the allocation vulnerable,
            # across all target sets.

        # Good, none of the reserved chambers sets makes the allocation
        # vulnerable.

        # Leave things as we found them.
        self.alloc.unreserve_alloc_for(assay_P)

        # And report back that the allocation as a whole is not vulnerable.
        return False


    def _filter_reserved_chamber_sets(self, filtering_chamber_set):
        """
        Provide those of the reserved chamber sets that the allocation has
        comitted to, that have members in common with the cited filtering
        chamber set.
        """
        chamber_sets = set()
        for chamber_set in self.alloc.reserved_chamber_sets():
            if chamber_set.intersection(filtering_chamber_set):
                chamber_sets.add(chamber_set)
        return chamber_sets


    def _all_would_fire(
            self, chamber_set_147, reserving_assay, target_set_ADFN):
        """
        We are given a reserved chamber set, and the assay that reserved it.
        The caller guarantees that the reserving assay is not already present
        somewhere in this chamber set.
        We are also given a potential targets-present set.
        Would the presence of the targets {A,D,F,N} cause all of the chambers
        {1,4,7} to fire - thus proving that the chamber set is vulnerable to 
        calling a false positive?
        """
        # Trivial shortcut answer, when the 
        for chamber in chamber_set_147:
            occupants = self.alloc.assay_types_present_in(chamber)
            # Only needs one chamber to have no occupants in common
            # with the target set to conclude False.
            if len(occupants.intersection(target_set_ADFN)) == 0:
                return False
        return True

    def _remove_incompatible_chambers(self, chambers, assay_P):
        """
        Make (and return) a copy of the given set of chambers, from which
        have been removed, any chambers with existing occupants incompatible
        with adding in the given assay_P.
        """
        chambers_to_remove = set()
        for chamber in chambers:
            occupants = self.alloc.assay_types_present_in(chamber)
            legal = self._design.can_this_assay_go_into_this_mixture(
                assay_P, occupants)
            if not legal:
                chambers_to_remove.add(chamber)
        return chambers - chambers_to_remove


    def _draw_possible_chamber_sets_of_size(self, chambers, size):
        """
        Provide all the chamber subsets of size <size> that are available 
        from the set given. Returns the collection of subsets as a sorted 
        sequence for two reasons. Firstly to place desirable choices nearer
        the beginning, and secondly to make the algorithm deterministic to help
        with automated testing.
        """
        subsets = []
        [subsets.append(frozenset(c)) for c in combinations(chambers, size)]

        def _how_crowded(chamber_set):
            return sum([len(self.alloc.assay_types_present_in(c)) 
                    for c in chamber_set])

        return sorted(subsets, key=_how_crowded)


    def _trace(self, msg):
        """
        A convenience method that emits the given message to the listener
        that has been registered at self.tracer, if one has been registered.
        Intended for unit test clients.
        """
        if self.tracer is None:
            return
        self.tracer.trace(msg)
