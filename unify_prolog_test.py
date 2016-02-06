from unify_prolog import UnifiableProlog

up = UnifiableProlog("./unify.pl")
assert(up.is_unified("A^2+x", "C+x"))
assert(up.is_unified("A+x", "C+d") is False)
assert(up.is_unified("(msup(A,2)+mfrac(msqrt(B),C))", "(msup(E,2)+D)"))
assert(up.is_unified("(msup(A,2)+mfrac(msqrt(B),C))", "(E+D)"))
