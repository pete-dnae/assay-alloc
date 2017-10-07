# A Set Theoretic Take on the Problem

## Fundamentals

Let our experiment deploy a set of assays ABCD...

We will refer to a positive result from an assay as that assay being
"present". And a positive result from a chamber as that chamber having
"fired".

Each chamber is designed to contain some subset of assays.

To start with, this narrative ignores replicas, and assumes perfect, idealised
behaviour.

We endeavour systematically to remove from the set of {all assays deployed},
those assays that we can prove are not present. Provided that we design the
assay subset allocation to give every assay the opportunity to furnish proof
that it is not present, then the assays that survice in the reduced set, are
by definition, those present.

We have two independent means of proof that an assay is not present, which we 
can combine.

### Chamber-not-fired proof

If a chamber N contains an assay subset {ABC} and that chamber does not fire
, then we have proof that the none of {ABC} are present.

### Not-all-chambers-fired proof

If not all of the chambers that contain assay C fired, then we have proved
that assay C is not present.


# Guaranteeing an Opportunity for Every Assay To Prove it Did Not Fire

For an assay to be guaranteed of the opportunity to prove it did not fire
it must satisfy either one or the other of the conditions (A) or (B) below.
These correspond to the Chamber-Not-Fired proof and the Not-All-Chambers-Fired
proof, respectively.

## (A) Chamber-Not-Fired

Consider our search for evidence that assay C is not present. A chamber might
contain the assay set {ABC}. If by chance, none of {ABC} are present the chamber
will not fire and this result delivers us the evidence we seek about C not being
present. However, if either A or B is present, it does fire, and we learn 
nothing.

We will only get a no-fire result from a chamber when none of its assay subset is
present.

XXX How to satisfy - maybe with assumption that fewer than 3 pathogens present or
cannot rely.

## (B) Not-All-Chambers-Fired

The assay Z existing in only one chamber's assay subset, and that chamber 
not firing, is sufficient proof that Z is not present. But it won't happen 





depdnent on giving v high prob of proof not fire
Softer
Replicates
What guides our subset design?
efficiency / space / mutex / fragility of chamber or assay
