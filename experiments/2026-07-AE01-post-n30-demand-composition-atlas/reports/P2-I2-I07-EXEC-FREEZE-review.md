# P2-I2 I07 Inactive EXEC-FREEZE Review

**Iteration:** `P2-I2-I07`

**Cycle:** `P2-I2-C01`

**Status:** candidate-free, inactive, uncommitted, and review-blocked by the
cross-entry-isolation audit

**Gate under review:** `P2-I2-EXEC-FREEZE`

## Outcome

I07 now freezes one exact three-mode candidate/control cycle without executing
it. The package contains 234 primary entries and at most 234 separately
authorized pre-construction retries. It binds the accepted I04R2/I05J/I06–I06B
authorities, the exact PyGRC revision, the repository `.venv`, relative command
lines, resource ceilings, permanent attempt claims, expected receipts, failure
receipts, and an inactive activation boundary.

The focused tests pass 7/7 and final candidate-free validation passes 25/25
with zero blockers. No PyGRC module, model, adapter, packet, candidate/control
operation, response evaluation, comparator window, or scientific window ran.

## Exact matrix

| Mode | Branch/order combinations | Seeds | Primary entries |
| --- | ---: | ---: | ---: |
| `state_carried` | 24 | 3 | 72 |
| `history_carried` | 25 | 3 | 75 |
| `hybrid` | 29 | 3 | 87 |
| **Total** | **78** | **3** | **234** |

Every entry binds mode, cell, branch, physical-order identity, seed, attempt,
resource envelope, claim path, output path, and normalized relative command.
All three modes remain retained and unranked.

## Execution-safety boundary

The future one-entry surface requires, before a claim:

- an explicit owner-accepted activation record;
- a separately owner-authorized full committed HEAD supplied through the
  normalized command, avoiding a self-referential commit hash;
- committed/local byte equality for the policy, source, validator, tests,
  matrix, binding, inactive freeze, activation, and validation;
- a clean authority tree, allowing only earlier governed C01 outputs;
- the exact clean PyGRC checkout and runtime-source digest;
- the repository `.venv` interpreter digest and relative graph-root argument;
- one exact matrix entry and output path; and
- absence of both the permanent claim and governed output.

The claim uses exclusive creation and is written before any PyGRC import or
model construction. One fresh process may execute only one entry. A retry is
possible only after a retained primary failure before model/adapter
construction and before candidate/control activity, with zero output,
byte-identical authority, a separately committed retry ledger, and explicit
owner authorization. Candidate or control outcomes never authorize retries.

The live path also freezes graph read-only checks, runtime/memory/disk ceilings,
registered baseline identity checks, exact response-source/edge/amount/timing,
B-target contamination checks, queue and capacity bounds, causal receipts, and
scientific-zero validity. It provides no fallback, tuning, rescue variant, mode
ranking, or scientific interpretation.

## Retained environment correction

The original second Python start failed before test collection because
`pytest` was absent from `.venv`. The failure is retained in the
[failed-start receipt](../contracts/p2-i2/c01/i07-focused-tests-failed-start.json).
The owner directed an in-place I07 correction rather than I07A under
DEC-045/CHG-040.

The continuation:

1. installed `pytest 9.1.1`, `iniconfig 2.3.0`, and `pluggy 1.6.0` only into
   `.venv`;
2. preserved the execution policy, source, focused tests, and all 234 matrix
   entries byte-exact;
3. refreshed only validator/process-derived binding fields;
4. passed the unchanged focused suite 7/7; and
5. passed the final validator 25/25.

The complete process ledger contains six candidate-free Python starts: initial
freeze construction, retained failed test launch, dependency installation,
derived-binding refresh, successful replacement tests, and final validation.
There were zero candidate-entry infrastructure retries. At the construction
layer, the original failed test launch has exactly one explicitly
owner-authorized replacement under DEC-045/CHG-040; it is not hidden by the
candidate-entry retry counter. There were zero candidate/scientific effects.

## Post-validation cross-entry-isolation audit

The owner-requested static audit confirms the central row-local design but does
not confirm the stronger end-to-end isolation guarantee.

| Requested invariant | Disposition | Mechanical basis |
| --- | --- | --- |
| Exact frozen row and accepted-authority inputs only | Pass | `_find_entry` selects one unique row; runtime reads are fixed authority paths, with no result-tree enumeration. |
| Fresh process per entry | Pass | Each entry is a normalized `run-entry` CLI process; `_LIVE_ENTRY_STARTS` rejects a second entry in the same process. |
| Fresh/restored registered baseline | Pass | `_build_model` constructs new topology/state and rebases reset; mode/branch adapters are newly constructed from registered profiles; initial composite identity is retained. |
| No prior-result scan or outcome-derived branch/parameters | Pass | The source contains no `glob`, `rglob`, `walk`, `scandir`, or result-directory read; branch, seed, schedule, and amounts come from the selected row and bound policy/registration. |
| Unique textual artifact paths | Pass | 234 rows produce 1,404/1,404 unique primary/retry output, claim, and failure paths; all are relative and under the declared C01 output root. |
| Adapter, temporary-file, queue, and RNG state isolation | Pass | These are newly created/process-local; no runtime temporary-file surface exists; `random.seed` is row-local. |
| Later primary after incomplete earlier entry | Pass | Primary activation does not inspect sequence completion or any earlier claim/output/failure. |
| Non-shadowing physical output paths | Blocked | Leaf checks and `O_EXCL` do not reject symlink parent components or prove resolved containment; the allowed untracked output subtree may contain such a parent. |
| No shared mutable cache across entries | Blocked | Experiment and PyGRC imports use ignored shared `__pycache__` trees; the command binds no disabled or entry-local bytecode-cache policy. |
| Retry eligibility independent of earlier outcomes | Blocked | Attempt 2 filters the shared ledger to the current `entry_id`, but trusts its authored `retry_eligible` boolean instead of deriving it from that entry's retained primary failure receipt and zero-state counters. |
| Fail-closed complete/evaluable matrix closeout | Blocked | The policy names `execution-manifest.json`, but no builder/validator requires all 234 terminal records or rejects missing/`operational_null` records. |

The unique textual paths mean one normally governed entry cannot write another
entry's leaf. That is insufficient against physical aliasing until every parent
component is verified as a real directory beneath a resolved governed root.
Likewise, current later-primary authorization is independent of an incomplete
earlier entry, but cycle completion is not yet implemented.

The audit used only shell/static reads and `jq`; it started no Python process,
imported no PyGRC module, and performed no model, packet, candidate, control,
response, comparator, or scientific operation. It changed no frozen runtime
artifact.

## Primary identities

| Artifact | SHA-256 |
| --- | --- |
| [Resumption input freeze](../contracts/p2-i2/c01/i07-candidate-cycle-resumption-input-freeze.json) | `c73b4c814a33bfd80c3fbb072928b4f4f9f59de5ba9dbe3bf8c424526a261c98` |
| [Successor policy](../configs/p2_i2_c01_execution_policy_v2.json) | `9a0649f18e99dff3c3f5bc7f8927ea8b369adde17e5160013a508e045c7d047e` |
| [Execution source](../scripts/p2_i2_execution.py) | `42b8486908831a928535f9594c7a15cc0d634c0025391d28ce32fc3b75fb6a61` |
| [Focused tests](../implementation/tests/test_p2_i2_execution_freeze.py) | `927f48c72e96bb6a8a49cd683a5c581d26de12a3435aebb02c6d585cd29f6ea2` |
| [Run matrix](../contracts/p2-i2/c01/run-matrix.json) | `57953a5fc93e8e05a95cdb7ca260c72bc28ea9388fd0804b064c1279ce8c48e8` |
| [Execution binding](../contracts/p2-i2/c01/execution-binding-receipt.json) | `c73276a0de176ce250691fbc03740a9011d938ea46acbf46510bcf5fed9811e6` |
| [Inactive EXEC-FREEZE](../contracts/p2-i2/c01/exec-freeze.json) | `c703eca51bc6155f44c5a3164c938361285b1f11dda506515fd4bc2fd4c93f1d` |
| [Final validation](../contracts/p2-i2/c01/i07-candidate-free-validation.json) | `f0e4d6da3b5ce12c5ab41a410fd18427c35d45493f988f9d56a2405306867141` |

The final validation reconstructs the run matrix, binding receipt, and inactive
freeze byte-semantically. All paths are portable and repository-relative.

## Gate disposition

```text
REG-GATE:                       passed after explicit I06B acceptance
I07 candidate-free checks:      25/25
focused tests:                  7/7
remaining blockers:             4 cross-entry-isolation enforcement gaps
candidate execution performed:  false
candidate execution authorized: false
EXEC-FREEZE:                    closed pending correction and owner acceptance
I08 authorized:                 false
commit authorized:              false
scientific evidence:            none
```

The currently frozen cycle should not pass `P2-I2-EXEC-FREEZE`. A bounded,
checklist-governed correction must first close the four enforcement gaps and
refresh only the consequential derived identities and candidate-free checks.
That correction requires separate owner direction. This review does not itself
activate the cycle, authorize I08, or assign any OP/R01–R05 result.
