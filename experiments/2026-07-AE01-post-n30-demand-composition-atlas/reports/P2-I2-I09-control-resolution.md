# P2-I2-I09 Control Resolution

**Status:** review-ready; owner acceptance and commit pending

**Evidence effect:** compact control projection over retained I03/I04/I06/I08 artifacts only

## Result

The deterministic I09 projection passes 21/21 checks with 0 blockers. It resolves all 19 program-common controls separately by mode (56 pass, one explicit state-carried `AE01-CTRL-16` not-applicable), all 38 frozen comparison rules, and all 15 mode-local L02 controls.

No registered branch varies across seeds. State-carried preserves the frozen order-invariant relation (`0.125`, `0.125`) and primary margins (`0.125`, `0.125`); history-carried and hybrid preserve their order-conditioned responses (`0.125`, `0.0`) and primary margins (`0.125`, `0.0`). Both original-source-alone and all symmetric leave-one arms are `0.0`; quantity-matched single-source repetitions are `0.125` and remain non-gating. Private one-partition paths are `0.0`; direct/controller diagnostics are `0.125` but are receipt-derived causal exclusions, so numerical equivalence is not promoted into candidate-chain evidence.

## Mode-local L02 controls

| Mode | Control | Disposition |
| --- | --- | --- |
| `state_carried` | `AE01-L02-CTRL-01` | `pass` |
| `state_carried` | `AE01-L02-CTRL-02` | `pass` |
| `state_carried` | `AE01-L02-CTRL-03` | `pass` |
| `state_carried` | `AE01-L02-CTRL-04` | `pass` |
| `state_carried` | `AE01-L02-CTRL-05` | `pass` |
| `history_carried` | `AE01-L02-CTRL-01` | `pass` |
| `history_carried` | `AE01-L02-CTRL-02` | `pass` |
| `history_carried` | `AE01-L02-CTRL-03` | `pass` |
| `history_carried` | `AE01-L02-CTRL-04` | `pass` |
| `history_carried` | `AE01-L02-CTRL-05` | `pass` |
| `hybrid` | `AE01-L02-CTRL-01` | `pass` |
| `hybrid` | `AE01-L02-CTRL-02` | `pass` |
| `hybrid` | `AE01-L02-CTRL-03` | `pass` |
| `hybrid` | `AE01-L02-CTRL-04` | `pass` |
| `hybrid` | `AE01-L02-CTRL-05` | `pass` |

## Boundary

This package does not assign `R01`-`R05`, rank or collapse modes, select a terminal class, regenerate an entry, or create schema authority. Program-common terminal/report guards are valid only at the I09 artifact boundary and must be revalidated against I11 closeout. `P2-I2-CONTROL-GATE` is review-ready, not owner-passed, and I10 remains unauthorized until review.
