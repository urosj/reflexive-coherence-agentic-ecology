# P2-I2 APP-B4 Ordered Three-Token Capability Audit

**Status:** stopped before freeze; owner choice required; uncommitted

## Outcome

The unchanged accepted baseline supports 24 of the 27 ordered G/E/P triples.
Three rows are physically infeasible:

```text
EEG
EEE
EEP
```

P begins at `0.75`. The first E withdraws `0.4375`, leaving `0.3125`; a
consecutive second E requires another `0.4375` and is short by `0.125`.
Accordingly these rows cannot produce three admitted physical events under the
unchanged baseline. They are operationally outside the executable domain, not
scientific zeros.

All other 24 triples remain inside the native `[0, 9.25]` coherence domain.
Their maximum final P is `3.375` for PPP, and maximum active-history readout is
`1.326171875`. S1 and S2 have sufficient native reserves.

## Quantity and ordering coverage

The six sequences with the exact GEP native total `31/16` are:

```text
GEP GPE EGP EPG PGE PEG
```

No repeated-operation triple has that exact total. The proposed panel can
therefore separate raw cardinality, native-dose multiset, and ordering, but it
cannot independently identify operation type apart from the quantity/history
encoding. Operation complementarity remains blocked.

## Owner choices

### A. Unchanged-baseline feasible panel — recommended

Freeze the 24 executable triples plus one reference across three seeds: 75
fresh arms. This remains closest to APP-B2 and adds no scaffold. EEG/EEE/EEP
remain explicitly outside the tested physical domain.

### B. Uniform native pre-funding

Pre-fund P by `0.5625` in every arm using a native prehistory packet excluded
from H_C, then run all 27 triples plus reference across three seeds and three
unfunded GEP anchors: 87 arms. This covers the full sequence space but adds a
new scaffold and requires inertness/admission controls.

### C. Complete registry with infeasible rows

Keep the 84-arm registry and preregister EEG/EEE/EEP as operationally
infeasible. This preserves enumeration but cannot yield a complete evaluable
response landscape, so it is the weakest option.

## Boundary

Two pure `.venv` capability-audit starts ran: one check-only and one retained
artifact generation. They imported no PyGRC, constructed no model, and
generated no arm, producer call, or response. APP-B4 freeze, runtime, and
commit remain closed pending owner selection.
