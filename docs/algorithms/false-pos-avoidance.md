# False Positive (FP) Avoidance

If the target Q is not present, but all the replicas of an assay Q are in
chambers that contain also one of the targets that are present, then all of Q's
chambers will fire, leading us to the false conclusion that Q is present.

An allocation can avoid false positives by choosing the set of chambers for
all replicas of assay Q, such that at least one of these does not already
contain one of the targets. ###

But we don't know which targets are present when we do the allocation.

But we do know which targets could be present. The possibilities being the 
set of sets comprising: any single target, any possible pair of targets, any 
possible trio, any possible four etc.

So re-writing paragraph ### in these terms:

An allocation can avoid false positives by choosing the set of chambers for
all replicas of assay Q, such that at least one of these (for all possible
target sets), does not already contain one of the targets.

# Optimisations

Prune the possible targets sets to exclude those with more than 5 members.

When more than one qualifying chamber set is available, favour one that 
passes the test when the clause 'at least one' is replaced with 'at least 
two' etc. 



