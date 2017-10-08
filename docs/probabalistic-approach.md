# Background

We have, let us say, 20 assays to deploy combinatorially to 100 chambers.
We spread a diverse range of 4-assay subsets to each chamber.

## Terminology
When a chamber registers a positive, we describe that chamber as having
"fired". 

Assumptions:
    o  Idealised / perfect performance of assays and system.
    o  Selection and distribution of 4-assay subsets approximates to a 
       statistically meaningful random distribution.

We talk about the following later:
- assay replication
- error tolerance from real world imperfections
- error tolerance from probability calcs with small samples
- assays that don't mix
- implementation considerations

## Visualisation
1 2 3 4 5 ... 100 Chambers

A B F N G ... 
Q R E R T ... 
G I R M A ... 
E L E P H ... 
  |
  |
  +-- This column is the assay subset deployed to chamber 2.
      4 assays drawn from a set of 20

# Worked example with literal numbers
See probability-support.xlsx

# Combinatorial Calling

We can hypothesise what will happen in terms of how many chambers fire, and the
assay constitution of those that do, in the presence of either 1,2,3,4... assay
targets.

It transpires that when we use these characteristics for the example numbers
above, they strongly indicate how MANY assay targets are present, when
this is 1, 2, 3 or 4, but then falls off. You can see this clearly in the
spreadsheet.

For example the presence of just one assay target will cause 20 chambers to fire,
and 80 not to fire. Whereas the presence of two targets causes very different
numbers: 40 to fire, and 60 not to fire.

Once we have concluded how many targets are present we can go on to call which
they are.

In the case of 2 targets present, we study the 40 chambers that fire and expect 
to see among their constituent assays, the following pattern.

- 2 distinct assays represented 20 times apiece. (our two called targets)
- The remainder spread between circa 18 groups of 7.

# Assay Replication to Cope with Real World Practicalities
We know that some of our assays are temperatmental, and we know that our system
will produce some level of false positives and negatives, and we wish to build in
some resilience to these things in the combinatorial assay allocation and
calling.

We can do this by simply doubling (or x3 or x4) up on on assays. We can treat 
these (for the most part) as if they were actually completely different assays.
Before we embarked on the calling above, we could post process the results to
aggregate the deliberately replicated  assays back to one. 

We can also cope by allowing some latitude on the pattern recognition. For
example treating a grouping of 18 firing targets as being a good enough match for
20 that might be expected.

# Implementation Considerations

There are parts of an implementation that must know that assay replicas are
really the same - like making sure two replicas of the same assay don't end up in
the same chamber.

# Todo

- error tolerance from probability calcs with small samples
- assays that don't mix
