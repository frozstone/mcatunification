# mcatunification
Unification code for MCAT system for NTCIR12-Math3

The procedure is as follows:

1. Generalize math expression at different levels (v)
2. Perform unification between the all levels (v)

UNIFICATION Process:

1. Flatten the math expression
    1. If the direct descendant of a subtree do not contain mo, then convert them into prefix notation (v)
    2. Otherwise, convert into infix notation (v)
    3. Naming the mi: Var_k
    4. (opt) naming the mn
2. Use unify.pl to do unification (v)
