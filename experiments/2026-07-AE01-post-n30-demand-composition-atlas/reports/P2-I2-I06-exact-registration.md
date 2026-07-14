# P2-I2-I06 exact three-mode registration

Date: 2026-07-14; I06A owner acceptance: 2026-07-15

Status: `P2-I2-I06-REGISTRATION-OWNER-ACCEPTED`

## Outcome

I06 registers all three required and unranked dependence modes:
`state_carried`, `history_carried`, and `hybrid`. The package materializes one
shared 23-node/16-edge opportunity topology, separate causal carriers and
response masks, seven logical cells with 26 exact subconfigurations, five lane
controls, the complete I04R2 response/comparator contract, and the I05J
analysis resolution boundary.

The sole output-producing registration validation passed 14/14 checks. It
performed baseline-only construction and restoration checks; it did not execute
any registered candidate or control branch.

## Native and producer boundary

State transport, packet scheduling, response configuration, model state, and
native reset-aware restoration remain owned by public PyGRC at graph revision
`83e3a300426631ee4df71b661b67d4fcfdfed594`.

The accepted I03 history adapter could not be registered byte-for-byte because
its materialization path hardcoded the quarantined I03 comparator tolerance
`1e-12`. The I06-owned `RCAEActiveHistoryAdapterV2` changes only that boundary:
materialization tolerance is now an explicit configuration and restoration-
identity field. The adapter retains the accepted source-label-free token fold,
intervention, and native `M_H` handoff. It neither reads response state nor
computes or schedules the later response.

The independently registered runtime tolerance is
`2.842170943040401e-14`, derived as 16 times the maximum binary64 ULP over the
registered finite domain. It is separate from the I05J
`analysis_arithmetic_delta = 1e-12`.

## Registration identities

The manifest binds five non-self authority files: the input freeze, exact
three-mode bundle, outcome-free control-index template, adapter revision, and
validator. The validation and report are downstream projections and are
excluded from that manifest to avoid circular identity.

Baseline-only restoration produced these composite identities:

- state-carried: `555bbd2d1a984509e0f003f94392cd0b59e83fa462df472a5df0b9971d7cdd8f`;
- history-carried: `f1dd074f5c140b0868255418283f5c293b24b0a66cd7755dd1f2c10fde5f8a96`;
- hybrid: `3dd25d8e8dbc65a23a991ccfcf623cf0733fb15da6b13daf8ce50d3c5f4fcc59`.

For each mode, the original, loaded, and reset composite digests are identical.
The paired interface refused partial manifests, component-hash mismatch,
history/hybrid cross-pairing, one-sided load, one-sided reset, repeated reset,
wrong baseline, wrong response mask, and stale readout binding.

## Execution accounting and evidence boundary

The retained governed I06 process accounting records two source/runtime
preflight starts, one adapter static-import check, and one final
output-producing registration start. The
final start constructed three fresh baselines and loaded three saved baselines.
It performed zero S1/S2 contribution operations, active-history token
admissions, neutral contacts, response evaluations, candidate/control cells,
comparator/scientific windows, and graph-repository mutations.

A terminal portability scan found literal absolute/legacy-root strings used
only by the validator's rejection guard. Manifest v1.0.1 retains the exact
pre/post source hashes and replaces those literals with generic POSIX/Windows
absolute-token and `*_ROOT` placeholder detection. Two no-model static starts
pass the four current documents, all five manifest hashes, and three generic
negative cases, then apply the accepted I05D scanner to all eight I06 package
files with zero findings. The already-consumed baseline validation was not rerun; its
projected artifact ID, manifest file count, baselines, refusals, and 14/14
result are unchanged.

This package establishes implementation registration integrity only. It does
not assign R01–R05, select or rank a mode, or provide L02 scientific evidence.
After the I06A closeout below, the owner accepts the complete package, passes
`P2-I2-REG-GATE`, and authorizes I07 freeze construction only. Candidate-cycle
execution remains unauthorized.

## I06A owner-review closeout

Owner review identified two potential blockers: AdapterV2 had not itself been
the I03 runtime-tested source, and the post-validation portability correction
needed exact two-stage provenance rather than a narrative old hash. I06A freezes
both questions plus four confirmation groups before any proof run.

AdapterV1 remains bound to the accepted 252-assertion I03B and 258-assertion
I03C runtime conformance artifacts. AdapterV2 inherits 13 state/history/
intervention/identity members exactly. After normalizing only the configured
tolerance and its audit-record field, its materialization AST is identical to
V1. Nine pure cases additionally verify ordered two-row ingestion, eight decoy
admission exclusions, cursor/idempotency, intervention/fold behavior, equal
positive and negative packet construction, configured deadband behavior,
identity sensitivity, and save/load/reset. The only model-call surface is
`get_state`, `schedule_packet_departure`, and `step`; response reads or schedules
remain zero.

The exact historical five-file producer manifest is retained byte-for-byte at
SHA-256 `3665e746d62afc602ab286d006465dd97ec674c7db30b611379a92ac89236613`.
The historical validator reconstructs to its exact
`f0b3f019bd3871876aa26f2a184887826900bb5b515a50de1bf41f844aeaca94`
execution hash. Machine comparison finds only `_assert_portable` plus its two
imports changed; all 24 other validation functions, including model
construction, restoration/refusals, and 14-check output projection, are exact.
Final manifest v1.1.1 therefore identifies the historical validator—not the
current corrected source—as producer of the retained I06 validation.

The confirmation checks establish the complete `[0.0, 9.25]` tolerance domain,
a minimum nonzero registered materialization delta of `0.078125`, twelve
mode/order/leave-one tuples, only `S1_TO_P` and `S2_TO_P` as H_P admission
edges, seven excluded traffic classes, positive per-mode/private-mask
isolation, and a one-retry ceiling scoped per matrix entry. Failed scientific
or control outcomes are never retryable.

The first no-model I06A start stopped on an authored seven-versus-six retry-
identity cardinality assertion before writing output. It is retained at
checkpoint `7761d3e`; the owner then authorized one separately bound
replacement, not an infrastructure retry. The replacement passes 14/14. Across
both static starts there are zero PyGRC imports/models, baseline reruns,
candidate/control operations, response evaluations, comparator/scientific
windows, or scientific effects.

The owner accepts the complete I06/I06A package and authorizes this successful
closeout to amend checkpoint `7761d3e`. REG-GATE is passed and I07 may begin its
checklist/hypothesis-first candidate-cycle freeze. This acceptance does not
authorize a candidate operation or scientific execution.

## Retained artifacts

- `contracts/p2-i2/i06-registration-input-freeze.json`
- `contracts/p2-i2/i06-three-mode-registration.json`
- `contracts/p2-i2/i06-registration-manifest.json`
- `contracts/p2-i2/i06-control-resolution-index-template.json`
- `contracts/p2-i2/i06-registration-validation.json`
- `contracts/p2-i2/i06-registration-execution-manifest.json`
- `contracts/p2-i2/i06-registration-post-portability-manifest.json`
- `contracts/p2-i2/i06a-registration-review-input-freeze.json`
- `contracts/p2-i2/i06a-registration-review-policy.json`
- `contracts/p2-i2/i06a-validation-failed-start.json`
- `contracts/p2-i2/i06a-replacement-validation-authorization.json`
- `contracts/p2-i2/i06a-registration-review-validation.json`
- `scripts/p2_i2_i06_history_adapter.py`
- `scripts/p2_i2_i06_registration.py`
- `scripts/p2_i2_i06a_validate.py`

The original I06 validation SHA-256 is
`1808a370c043055020ee34b7d30cc4bb27670009196b7c9ea8b2310537819c99`;
the I06A validation SHA-256 is
`aca1815418e18254cd63d4b78d56033090b1f7e22eaae16189d63151d99fa26d`;
and final manifest v1.1.1 SHA-256 is
`83f2889ebd7b83f65a3a194065f07f0cb850c8a779fc50d75ceaec60a1bc6eaf`.
