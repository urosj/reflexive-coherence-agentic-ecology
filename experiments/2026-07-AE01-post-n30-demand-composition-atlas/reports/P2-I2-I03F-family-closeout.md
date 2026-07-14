# P2-I2-I03F Three-Mode Family Closeout

**Iteration:** `P2-I2-I03F` / checklist section 8.1

**Status:** compact family composition passed; ready for owner review

**Gate effect:** discriminator-gate readiness only. The gate is not passed and
I04 remains unauthorized.

## 1. Scope

I03F composes the already accepted state-carried, history-carried, and hybrid
packages. It does not repeat their capability, source, dataflow, restoration,
or runtime reviews.

The
[input freeze](../contracts/p2-i2/i03f-family-closeout-input.json), SHA-256
`0593c7821370ce138db4fba9bbbc5fd0bbd50f88788e22618acb6b421b2401e3`,
binds eleven terminal authorities to accepted baseline commit
`fc3fb0f638eb0b180cb05d081e6dc447f24af66b`. Inspection was limited to
omission, substitution, semantic collapse, cross-mode rewrite, incomplete OP
coverage, lost obligation/quarantine scope, wrong restoration ownership, and
unsafe I04 import.

No PyGRC module was imported, no model was instantiated, and no conformance or
reconstruction was rerun. The admitted PyGRC checkout remained clean at
`83e3a300426631ee4df71b661b67d4fcfdfed594`.

## 2. Retained family

The
[family index](../contracts/p2-i2/i03f-family-closeout-index.json), SHA-256
`f9c8591a9d3c30a90097548b359e399b3a9e73b01f06ea7cd63d5971ceeb3fa6`,
retains:

| Mode | Realization | Carrier and response |
| --- | --- | --- |
| State-carried | `pygrc_native_candidate` | native P; native `[P]/[B_ref]` response |
| History-carried | `minimally_producer_assisted` | authoritative H_P with M_H = R_H(H_P); native `[M_H]/[B_ref]` response |
| Hybrid | `minimally_producer_assisted` | native P plus authoritative H_P/M_H; native `[P,M_H]/[B_ref]` response |

All three remain required downstream. There is no selection, ranking,
preference, or supersession. P remains the complete state-carried pool,
non-primary and excluded from history-carried V, and one component of hybrid
V. H_P/M_H do not retroactively alter the accepted state-carried profile.

Producer assistance remains limited to active-history admission,
intervention, deterministic readout, and native M_H materialization. Native
PyGRC continues to own score, threshold, scheduling, coherence mutation, and
the later response.

Restoration ownership remains mode-specific: native-v2 plus declarative
binding for state-carried; paired native-v2/adapter composite identity for
history-carried; and the same layered pair plus joint/private binding for
hybrid.

## 3. OP, obligation, and quarantine integrity

The index contains a complete 9 × 3 pointer matrix: every H-L02-OP-01 through
H-L02-OP-09 points to its accepted projection in each mode contract. The
family closeout assigns no R01-R05 result.

All six I03BR1 qualifications and all eight I03CR1 obligations are copied
exactly. Nine consolidated duties cover the fourteen source obligations
exactly once. None is discharged. The umbrella-family duty remains in
progress until owner acceptance of this package; all I04/I06/I08 duties retain
their original owners.

The existing machine quarantine remains the authority over seven source
artifacts spanning all three modes. Fixture inputs, assertion specifications
and outcomes, branch/topology identities, implementation comparators, runtime
observations, run policy, and evidence/restoration digests remain prohibited
I04/I06 inputs, including direct and trivial serialized reuse.

## 4. I04 import boundary

If the project owner passes the discriminator gate, I04 must import all three
profiles unchanged and mode-indexed. I04 may freeze responses, orientations,
comparators, matched-null identities, aggregation/missingness, and evaluation
rules. It may not remove a mode, revise I03 causal semantics, rank modes, or
inherit any conformance value or outcome.

Any shared I04/I05 artifact requires an explicit semantic-equivalence proof
covering causal response meaning, units/orientation, time window, comparator
role, aggregation, missingness, and calibration population. Otherwise the
artifact remains mode-specific.

## 5. Validation and disposition

The
[machine validation](../contracts/p2-i2/i03f-family-closeout-validation.json),
SHA-256 `44b2db8e49b603ddd2b59f3e5bc2f367708b5b93b8b1e9e19e5b8c062cb93c9e`,
was produced by the
[compact validator](../scripts/p2_i2_i03f_validate.py), SHA-256
`9bcc9e1cddd0844b8415f77399df6204e17f3dbe0170a8d88003beaf211e2a21`.
It passed 12/12 integration checks and 9/9 acceptance conditions with zero
blockers.

`P2-I2-I03F-REVIEW-READY` is satisfied. This package does not itself pass
`P2-I2-DISCRIMINATOR-GATE` or authorize I04. Those effects require an explicit
owner disposition.
