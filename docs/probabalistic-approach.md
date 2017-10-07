# Background

Assumes idealised / perfect behaviour

We talk about the following later:
- replication
- error tolerance from the real world
- error tolerance from probability calcs with small samples
- assays that don't mix
- implementation considerations

# Worked example with literal numbers

## Parameters
20 assay types {ABC...T}
100 chambers
4 assays per chamber in randomly chosen sets

## Derived numbers
400 deployed assays
Deploys circa 20 of each assay type.
Hence the number of chambers that contain a given assay is circa 20.
And...
The number of chambers that do not contain a given assay is circa 80.

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

## Expectations for firing vs. non-firing chambers as f(number assays present)

When 1 assay only is present -> 20 fires    80 non-fires      ratio = 0.25
When 2 assay is present      -> 40 fires    60 non-fires      ratio = 0.67
When 3 assay is present      -> 60 fires    40 non-fires      ratio = 1.50
When 4 assay is present      -> 80 fires    20 non-fires      ratio = 4.00

These absolute numbers and the ratios taken together - being so spread, 
give strong evidence of how many assays are present.

## Expectations for firing chamber content as f(number assays present)

When one assay(M) only is present:
    - the 20 firing chambers comprise 80 assays
    - in which can expect that 20 are M (all of the Ms)
    - and that the remaining 60 are a mix of the other 19 assays, 
      with circa 3 copies of each.

When two assays only are present (P,Q):
    - the 40 firing chambers comprise 160 assays
    - in which we can expect that 20 are P (all of the P)
    - in which we can expect that 20 are Q (all of the Q)
    - and that the remaining 120 are a mix of the other 18 assays,
      with circa 7 copies of each.

When three assays only are present (A,B,C):
    - the 60 firing chambers comprise 240 assays
    - in which we can expect that 20 are A (all of the A)
    - in which we can expect that 20 are B (all of the B)
    - in which we can expect that 20 are C (all of the C)
    - and that the remaining 180 are a mix of the other 17 assays,
      with circa 10 copies of each.

# Abstracted to formulaic probabilities

We have just 3 input parameters:

## Independent Parameters
Number of assay types           AssayTypes
Number of chambers              NumChambers
Number of assays per chamber    NPlex // make divisor of NumChambers

## Derived Parameters
a

## Calling one only assay present

Expected number of chambers to fire = 



When 1 assay only is present -> 20 fires    80 non-fires      ratio = 0.25
