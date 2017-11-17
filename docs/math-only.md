# Overview

If we admit 3 targets present, and we allocate 4 copies of assay P into a set 
of chambers that has no more than one chamber in common with any of the 
chamber sets used to allocate [A,B,C....O], then the presence of P will cause
4 out of 4 of its chambers to fire, whereas no other possible targets present
set can cause more than 3 out of 4 of them to fire.

    4 out of 4 is a call.
    3 out of 4 is not a call.

Let us call this the n+1 allocation. Our positive calling is predicated on a
one chamber (one bit) difference, and is thus defeated if just one chamber
that does contain P misfires for any reason.

We can improve this by allocating 5 copies (n+2). 5 out of 5 of P's
allocated chamber is a stong call, and 4 out of 5 is a weak call. And 3 out
of 5 is a non-call.

    5 out of 5 is a strong call.
    4 out of 5 is a weak call.
    3 out of 5 is a non call.

But what if one of the fires is spurious? We can no longer regard 4 out of 5
as a call, because one of the firest might be spurious, meanng there were
only 3 legit fires - which is a non call. And we must regard 5 out of 5 as a
weak call.

We can improve this by going to n+3.

    6 out of 6 is a strong call.
    5 out of 6 is a weak call.
    4 out of 6 or fewer is not a call.

    

 


