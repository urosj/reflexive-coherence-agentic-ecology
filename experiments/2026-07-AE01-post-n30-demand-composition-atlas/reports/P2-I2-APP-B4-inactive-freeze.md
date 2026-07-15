# P2-I2-APP-B4 Inactive 75-Arm Freeze

**Status:** technically complete and review-ready; inactive, uncommitted, and
candidate-free

## Outcome

The owner-selected unchanged-baseline panel is frozen as one deterministic
history-carried campaign:

```text
seeds = 101, 211, 307
feasible ordered triples per seed = 24
fresh reference rows per seed = 1
total rows = 3 x (24 + 1) = 75
excluded as operationally infeasible = EEG, EEE, EEP
```

The excluded sequences are outside the unchanged-baseline executable domain.
They are neither expected runtime outputs nor scientific zeros. No reservoir
pre-funding, dose change, baseline change, new admission rule, new producer,
or APP-B2 outcome selection is present.

## Frozen interpretation boundary

The analysis separates:

1. raw three-event cardinality across all feasible triples;
2. native-dose multiset effects;
3. ordering effects only among permutations of the same multiset; and
4. GEP uniqueness within the unchanged-baseline feasible domain.

Every aggregate positive discriminator requires the same categorical response
pattern at all three frozen seeds. Exact numeric response invariance is
reported separately. A deliberately seed-divergent pure case fails closed.

Even a positive GEP-specific result can establish at most an ordered
quantitative-history pattern in this realization. Operation complementarity
remains unclaimed because no repeated-operation triple matches both the GEP
cardinality and its total native dose.

## Reused P2-I2 machinery

The freeze binds the accepted history-carried realization, native G/E/P
routes and amounts, topology and initial coherences, source-label-free H_C
admission, M_H materialization, feedback threshold, response window,
restoration and contamination checks, strongest-of-seven-proper-subsets
estimator, cumulative output, retained-only reconstruction, one campaign
attempt, and zero retries.

Every future parent and child command is lexically rooted at
`.venv/bin/python`. All persisted paths are repository-relative. The graph
checkout remains read-only. A separate committed activation artifact and clean
authority HEAD are required before the runner can claim the campaign.

## Candidate-free validation

The retained validator passes the inactive package:

```text
registry rows = 75
ordered triple rows / reference rows = 72 / 3
feasible / excluded sequences = 24 / 3
bound authority and implementation hashes = 15
pure classifier cases = 4
accepted-envelope identity projection cases = 1
activation / claim / output / reconstruction present = 0 / 0 / 0 / 0
PyGRC imports / models / producers / arms / responses = 0 / 0 / 0 / 0 / 0
status = passed_inactive_owner_review_pending
```

The identity projection preserves the accepted I04 physical-order identity
and records the actual APP-B4 operation sequence in a separate, subordinate
measurement-projection field. It changes no measurement payload.

## Construction ledger

```text
capability-audit starts = 2
freeze-builder starts = 6
freeze-validator starts = 9 (8 passed, 1 failed before runtime)
focused pure identity-projection tests = 1 failed before runtime
campaign claims / parent starts / child starts = 0 / 0 / 0
runtime or scientific retries = 0
```

The failed validator start was a self-matching outcome-quarantine diagnostic.
The focused projection test then correctly rejected an APP-B4 sequence placed
in the accepted I04 `physical_order_id`; the projection was corrected to keep
that accepted identity unchanged. A final source review removed seven inherited
absolute shebangs because APP-B4 is invoked explicitly through the repository
`.venv`; the freeze and validation identities were then regenerated. A final
classifier audit replaced seed-101-only aggregate booleans with an all-seed
fail-closed rule. Four earlier uncommitted validation outputs were superseded
while binding transitive hashes, correcting the identity and seed projections,
and enforcing path portability. No failure imported PyGRC, constructed a
model, consumed a claim, or generated an arm or response.

## Lifecycle disposition

This artifact freezes implementation and analysis only. It does not authorize
a commit, activation artifact, campaign claim, PyGRC simulation, result, or
scientific interpretation. Those remain closed pending owner review.

Evidence: [inactive freeze](../contracts/p2-i2/app-b4-inactive-75-arm-freeze.json),
[inactive validation](../contracts/p2-i2/app-b4-inactive-freeze-validation.json),
[capability audit](../contracts/p2-i2/app-b4-unchanged-baseline-capability-audit.json),
[freeze builder](../scripts/p2_i2_app_b4_freeze.py),
[runner](../scripts/p2_i2_app_b4_run.py),
[analysis](../scripts/p2_i2_app_b4_analysis.py),
[reconstructor](../scripts/p2_i2_app_b4_reconstruct.py), and
[validator](../scripts/p2_i2_app_b4_validate.py).
