# P2-I2-I09A Normalized-Estimator Correction

**Status:** review-ready; owner acceptance, commit, CONTROL-GATE reconciliation, and I10 resumption pending

**Evidence effect:** corrected derived control projection over retained I08 evidence only

## Result

I09A passes 24/24 deterministic checks with 0 blockers. Before correction it reconstructs the accepted I09 index, validation, and report byte-identically. It then routes all 18 retained mode/order/seed tuples through `p2_i2_i04r2_analysis.primary_margin`.

The retained raw responses do not change: candidate and leave-one values remain `0.125` or `0.0`, and exact comparator ties retain deterministic `q1-only` provenance without scientific meaning. The corrected normalized margins are twelve `1.0` values and six `0.0` values:

| Mode | q1 then q2 | q2 then q1 | Comparison disposition |
| --- | ---: | ---: | --- |
| `state_carried` | `1.0` | `1.0` | `pass` |
| `history_carried` | `1.0` | `0.0` | `pass` |
| `hybrid` | `1.0` | `0.0` | `pass` |

All dependent layers were rebuilt after the correction. The outcome remains 38/38 comparison-rule passes, 15/15 mode-local L02 control passes, and 56 program-mode passes plus one explicit not-applicable state-carried `AE01-CTRL-16`. Thus the defect changes the numeric normalized-margin projection and its prose, but no control disposition.

## Boundary

Accepted I09 remains immutable historical authority. I09A imports no PyGRC, constructs no model or adapter, runs no candidate/control branch, regenerates no matrix entry, introduces no scientific input, and assigns no `R01`–`R05`, support status, mode ranking, or terminal class. CONTROL-GATE remains reopened pending explicit owner acceptance; this package does not authorize commit or resume I10.
