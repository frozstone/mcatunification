from unify_prolog import UnifiableProlog

up = UnifiableProlog("./unify.pl")
assert(up.is_unified("A^2+x", "C+x"))
assert(up.is_unified("A+x", "C+d") is False)

