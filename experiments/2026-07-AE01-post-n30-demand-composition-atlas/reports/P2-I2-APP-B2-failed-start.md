# P2-I2 APP-B2 Failed-Closed Start

**Status:** sole campaign claim consumed; first child failed before a receipt;
autonomous progression stopped

The clean committed preflight passed and atomically created the frozen claim.
The parent then attempted the first row,
`primary:state_carried:reference:seed-101`. That child exited with code one.
No arm receipt, child stderr receipt, aggregate runtime output, or per-arm
output was retained. No later child was started.

The parent launcher contains an infrastructure defect: it calls
`Path(sys.executable).resolve()` before spawning the child. Although the parent
was invoked through `.venv/bin/python`, resolution dereferenced that launcher
to the system-interpreter target, so the child was not invoked through the
repository venv. The binary bytes are identical, but the invocation path is
not: Python cannot discover the repository `pyvenv.cfg` from the dereferenced
system path. This violates the frozen all-process `.venv` boundary.

The same parent path used a check-raising subprocess call without persisting
captured stderr or a final failure receipt. Consequently, model/import/packet/
producer counts inside the failed child are unobservable and are recorded as
null rather than inferred.

This is an implementation/infrastructure failure, not a scientific result or
a detected defect in the frozen operation values, modes, estimator, controls,
or claim semantics. Nevertheless, the current authority explicitly grants
zero infrastructure retry and says that a consumed campaign failure stops the
autonomous cycle. The claim is permanent and must not be removed or reused.

No correction or replacement campaign is authorized. The required owner
decision is whether to permit an additive launcher/failure-receipt correction
and exactly one new replacement claim, with all scientific bytes unchanged.
