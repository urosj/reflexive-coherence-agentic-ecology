# P2-I2-I08 Execution Ledger

**Status:** cumulative campaign record; 1/234 evaluable, exact checkpoint
continuation passes 9/9 focused tests, and entry 2 awaits its authority commit

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
`R01`–`R05` remain unassigned and no execution manifest exists.
