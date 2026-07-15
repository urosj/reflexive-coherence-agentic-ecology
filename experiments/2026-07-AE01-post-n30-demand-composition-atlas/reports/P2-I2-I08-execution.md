# P2-I2-I08 Execution Ledger

**Status:** owner-accepted cumulative campaign record; 234/234 evaluable and
checkpoint commit authorized

This is the sole narrative execution ledger for I08. Governed claims,
successes, and failures remain one file per frozen matrix path because those
are the preregistered machine receipts; narrative reports are not created per
entry.

## Accepted checkpoint

The committed in-place venv correction at `6b920fb` passed its exact attempt-2
preflight. The sole frozen same-entry retry then completed successfully through
`.venv/bin/python -B`.

| Field | Retained result |
| --- | --- |
| Mode | `state_carried` |
| Cell / branch | `reference-pool` / `reference_pool_empty` |
| Seed / attempt | 101 / 2 |
| Child status | Return code 0; attestation present |
| Response window | Valid; queues empty |
| B before / after | 4.25 / 4.25 |
| Measured / registered gain | 0.0 / 0.0; within tolerance |
| Scientific-zero receipt | `true` |
| Candidate-chain status | Receipt-derived; feedback-coupled pulse subthreshold |
| Scientific interpretation | `null` |

The permanent attempt-2 claim has SHA-256 `6a8e429d…`; the retained success
record has SHA-256 `ece9e4df…`. Attempt 1 remains immutable as the eligible
pre-model infrastructure failure that justified this already-frozen retry.

This is one valid registered row, not a control, mode, or L02 conclusion.
At that checkpoint, `R01`–`R05` remained unassigned and no execution manifest
existed.

## Complete execution inventory

Commit `180a1bf` binds entries 2–234. Every one completes on primary attempt 1
through a fresh repository-venv process. The cumulative manifest accepts all
234 exact terminals with no missing, ambiguous, malformed, or nonevaluable
entry. Manifest SHA-256 is `d84935e7…`; its canonical payload digest is
`69864b8f…`.

| Execution surface | Count |
| --- | ---: |
| Required/evaluable terminals | 234 / 234 |
| Primary successes | 233 |
| Accepted retry successes | 1 |
| Permanent claims | 235 |
| Retained failures | 1 pre-model infrastructure failure |
| Missing / nonevaluable / ambiguous | 0 / 0 / 0 |
| Current-head / accepted-checkpoint terminals | 233 / 1 |

All 234 success records have an attested child return code 0, valid response
window, empty terminal queue, measured/native gain agreement, passed capacity
guards, and null scientific interpretation. No seed-matched configuration
varies across seeds 101, 211, and 307.

## Mechanical response distribution

| Scope | Entries | Gain 0.0 | Gain 0.125 |
| --- | ---: | ---: | ---: |
| All modes | 234 | 132 | 102 |
| State-carried | 72 | 36 | 36 |
| History-carried | 75 | 42 | 33 |
| Hybrid | 87 | 54 | 33 |

| Registered cell | Entries | Gain 0.0 | Gain 0.125 |
| --- | ---: | ---: | ---: |
| Reference pool | 18 | 18 | 0 |
| Individual contributions | 36 | 18 | 18 |
| Combined orders | 18 | 6 | 12 |
| Pooled-history shuffle | 27 | 6 | 21 |
| Contributor removal | 45 | 36 | 9 |
| Global-state exclusion | 72 | 48 | 24 |
| Access/capacity contrast | 18 | 0 | 18 |

The two order-sensitive cells are mechanically uniform across seeds. State-
carried returns 0.125 under both physical orders. History-carried and hybrid
return 0.125 under `q1_then_q2` and 0.0 under `q2_then_q1`, both in the combined-
order rows and their physical-order-reversal counterparts. This is a retained
order-conditioned observation, not yet a hypothesis verdict.

Producer reason receipts comprise 93 scheduled feedback-coupled packet
departures, 120 subthreshold pulses, 12 wrong-polarity pulses, and 9 direct
native schedules from controller predicates. Candidate-chain status is
receipt-derived for 198 rows, diagnostic-excluded for 18, and private-
partition-excluded for 18. `R01`–`R05` remain unassigned for all 234 rows.

## Boundary

This ledger reports execution mechanics and registered raw responses only.
I09 control resolution, I10 interpretation, and I11 lane disposition remain
closed pending owner review. No cross-mode ranking or L02 conclusion is made.
