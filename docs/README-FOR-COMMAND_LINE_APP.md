# Assay Allocation Command Line App - User Manual


# Usage

Copy "assay-alloc.exe" into C:\temp (or somewhere else of your choice).

Open a windows command shell window and navigate to C:\temp:

    (Type 'cmd' in the search box)

    cd c:\temp

Run the program, providing command line arguments:

    assay-alloc --assays 20 --replicas 3 --chambers 24 --dontmix 3 --targets 2

If you want to run it again with different parameters:

    Press up-arrow to bring up your previous command.
    Use left and right-arrow to type in changed parameters.
    Press ENTER when done.

If you want to capture the output in a text file do this:

    assay-alloc --assays 20 ...as-above... > myfile.txt

If you want to accumulate the output from several runs in a file do this:

    assay-alloc --assays 20 ...as-above... >> myfile.txt



# Allocation Algorithm Contract

- To place exactly the number of replicas specified for each assay type.
  (No more. No less).
- To never co-locate assays that are forbidden by one of 'dontmix' pairs.

# Allocation Algorithm Steering Criteria

1) To distribute a similar number of assays to all chambers.

2) To reduce to a minimum the creation of identical, or similar assay mixtures
   in different chambers.

# Allocation Algorithm Used

The algorithm is in the style of a *bin packing algorithm*. These are the family
of algorithms that eat up a stream of things arriving and have to decide where to
put them without being able to look ahead to see what is coming later, and
without being able to change their mind later.

In our case the things arriving are the assay replicas that must must be placed,
(we choose alphabetical order to make things easier for humans to reason about).
I.e. A1 A2 A3 B2 B2 ... etc.

The opportunity to optimize the allocation comes in by looking dynamically at 
what the state of play in the allocation thus far is as each new assay 
replica "arrives".

As each assay replica arrives, the algorithm scores the desirability of each
(legal) potential chamber and uses the highest scoring one. There are 3 scoring
criteria, stated here in least-dominant to most-dominant order:

1) Highest score to chamber with lowest number. (I.e. start at 1, then 
   use 2 etc). (Easier for humans to follow and track, and finishes the job of  
   making the algorithm deterministic and thus unit-testable.)

2) Highest score to chambers with lowest number of existing occupants.

3) Highest score to chambers that, by adding the incoming assay type, would
   create fewest, new, assay-type pair *duplicates*.

   For example if a chamber contains AB and we add C, we are creating two
   new co-located assay pairs: AC and BC. If say, the existing allocation
   scenario already has the pair AC in another chamber,  but does not
   have the pair BC elsewhere, we can say we are creating just one *new*
   duplicated assay pair.
   
   Duplicated assay pairs are a kind of *waste* because they provide no *new* 
   discriminating information, and waste the space for assays that could. 
   Hence this criteria strives to keep the mixtures in each chamber as globally 
   disimilar from each other as we can.
