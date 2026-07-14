# AE01 Scripts

This directory contains the experiment-local P1-I5 implementation. It is not a
reusable `rc_agentic_ecology` source package and does not change PyGRC.

## Entry point

All commands run from repository root with the pinned inspection dependency:

```text
uv run --with jsonschema==4.26.0 python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/ae01.py <command>
```

### `validate-phase1`

Validates the P1-I3 schema and records, P1-I4/P1-I5 vocabulary and policy,
lane projections, valid fixtures, and expected-invalid fixtures. With no
`--output`, the deterministic non-evidential summary is printed to stdout.

### `resolve-policy`

Materializes all shared defaults: configuration IDs, seeds, attempt/retry
limits, resources, artifact roles, completion/failure criteria, and the
applicability/priority of all nineteen common controls for every lane.

```bash
uv run --with jsonschema==4.26.0 python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/ae01.py resolve-policy --output outputs/ae01-resolved-policy.json
```

### `digest`

Reports canonical semantic digest, exact-file SHA-256, and size without
modifying the artifact.

```bash
uv run --with jsonschema==4.26.0 python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/ae01.py digest --input outputs/ae01-resolved-policy.json
```

### `freeze-resolution`

Consumes a pending primary metric sheet and candidate-blind matched-null input.
It writes a schema-valid calibration record and frozen metric sheet with:

```text
delta = max(measurement resolution, maximum absolute matched-null margin)
```

The input seeds must exactly match the sheet's calibration seed profile. The
command fails if candidate blindness, seeds, or resolution status differ.

```bash
uv run --with jsonschema==4.26.0 python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/ae01.py freeze-resolution --metric-sheet experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/metric-sheets/AE01-L01.json --calibration-input experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/fixtures/inputs/l01-candidate-blind-calibration-input.json --calibration-output outputs/ae01-l01-metric-calibration.json --frozen-sheet-output outputs/ae01-l01-frozen-metric-sheet.json
```

### `classify-margin`

Derives the threshold relation from a frozen sheet while preserving every
seed margin. A pending sheet produces `resolution_unknown`, never intuitive
“narrow” or “robust” wording.

```bash
uv run --with jsonschema==4.26.0 python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/ae01.py classify-margin --metric-sheet outputs/ae01-l01-frozen-metric-sheet.json --margin 101:0.08 --margin 211:0.03 --margin 307:0.06
```

### `runtime-receipt`

Requires a lane-local `realization_profile` record, explicit live class, run
ID, operations, and receipt output. The profile must explicitly declare the
realization available and enabled, the class and operations must match it, and
PyGRC must already be available in the local Python environment. Its location
is not committed or recorded.

```bash
uv run --with jsonschema==4.26.0 python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/ae01.py runtime-receipt --profile outputs/local-realization-profile.json --run-id ae01-local-run --execution-class pygrc_runtime_with_rcae_producer --operation binding-check --receipt-output outputs/ae01-local-runtime-receipt.json
```

This command validates the binding requested for those operations; it does not
pretend that the future lane operation itself ran. A Phase 2 lane runner must
use the same receipt boundary around its actual state transition. Pass
`--graph-root` with the locally configured graph checkout when source-tree
fingerprint guarding is required. That machine-local argument never enters the
receipt. Missing/incompatible PyGRC writes a failed receipt and exits nonzero;
there is no fallback.

### `build-manifest`

Consumes a descriptor containing profile-registry path, source revisions,
artifact declarations, and optional realization-profile paths. Every declared
artifact must already exist and pass digest/profile/tier checks.

```bash
uv run --with jsonschema==4.26.0 python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/ae01.py build-manifest --descriptor outputs/local-manifest-descriptor.json --output outputs/ae01-local-manifest.json
```

### `assemble-report`

Consumes a P1-I3 `report_projection` and optional separately authored Markdown.
Use `--preview-digest` first to calculate the deterministic digest fields for a
new projection without writing a report. Freeze those values in the projection,
then run the final assembly:

```bash
uv run --with jsonschema==4.26.0 python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/ae01.py assemble-report --projection outputs/local-report-projection.json --preview-digest
uv run --with jsonschema==4.26.0 python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/ae01.py assemble-report --projection outputs/local-report-projection.json --output outputs/ae01-local-report.md
```

For `assembled_interpretation`, also pass `--authored` with the portable path
to its tracked authored source.

## Reconstruction boundary

Commands write only to explicitly supplied RCAE-relative outputs. Disposable
products belong under ignored top-level `outputs/`. Only an explicit verified
manifest and retention decision can move selected evidence under the
experiment. No command writes into the graph/PyGRC repository.

## P2-I1 entry point

`p2_i1.py` is the thin file/CLI boundary. `p2_i1_analysis.py` contains pure
deterministic analysis and never imports PyGRC. `p2_i1_runtime.py` imports
PyGRC only inside an explicit runtime call and contains no candidate runner.
Candidate execution remains closed until `P2-I1-REG-GATE` passes and a
cycle-scoped `P2-I1-EXEC-FREEZE` authorizes the exact frozen run;
`P2-I1-EXEC-GATE` is the post-execution close gate.

Create the ignored local environment and install a non-editable build from the
locally configured PyGRC source plus the pinned validation dependency:

```bash
uv venv .venv
uv pip install --python .venv/bin/python LOCAL_PYGRC_SOURCE jsonschema==4.26.0
```

`LOCAL_PYGRC_SOURCE` is machine-specific and never enters shared records. A
retained runtime profile must instead record the installed `pygrc==0.1`
identity and source revision/digests.

### P2-I2 I04/I05 authority

`p2_i2_i04r2_analysis.py` and `p2_i2_i04r2_calibration.py` are the sole active
P2-I2 calibration-preregistration analysis path under owner-accepted I04R2.
The original I04 and I04R1 modules remain immutable historical inputs. The
separate I05 freeze binds the exact identities and encodes a one-invocation
ceiling; its corrected I05B authority package is owner-accepted for retention.
Validate proposed-permission integrity without running the null:

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i2_i05_authorization_validate.py --output /tmp/p2-i2-i05-authorization-validation.json
```

The governed I04R2 calibration entry point imports no PyGRC and grants no
candidate authority. I05A found that it lacks required one-shot mechanics, so
the old direct entry point may not run. Reproduce the historical zero-execution audit with:

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i2_i05a_safety_audit.py --output /tmp/p2-i2-i05a-safety-audit.json
```

`p2_i2_i05b_one_shot.py` is the sole accepted governed I05 wrapper. It claims
the attempt atomically before importing/calling the accepted builder and binds
the future committed authority without embedding a self-referential commit
hash. Its machine owner-acceptance record authorizes commit but explicitly not
the null; it cannot run until a separate exact 10.4 launch record is committed.
Reproduce the zero-null correction validation:

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i2_i05b_validate.py --output /tmp/p2-i2-i05b-validation.json
```

Validate the six committed P2-I1 configs:

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1.py validate-configs
```

Generate the CAL-PRE code, policy, fixture, cell, calibration, runtime, and
static-profile identity. The result records the current source revision and
therefore becomes a retained freeze artifact only after the implementation
commit is final:

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1.py build-cal-pre-identity --output outputs/p2-i1-cal-pre-identity.json
```

The freeze command fails when the worktree is dirty. During implementation
review, an explicitly non-retainable preview may be generated with
`--allow-dirty-preview`; its artifact kind, identity ID, clean-state flag, and
retention eligibility prevent it from masquerading as the final freeze.

Generate the candidate-blind matched null through the same opportunity
aggregation and paired-margin functions later used for live records:

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1.py generate-matched-null --output outputs/p2-i1-matched-null.json
```

Analyze retained raw opportunity records without authored recomputation:

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1.py analyze --input outputs/p2-i1-opportunities.json --output outputs/p2-i1-analysis.json
```

### Registration policy validation

`p2_i1_registration.py` is a registration-only boundary. It imports the six
frozen CAL-PRE configs and the experiment-local registration policy, proves
measurement and calibration-realization identity equality against the retained
v2 identity, validates all 24 control plans, and keeps candidate execution
closed:

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_registration.py validate-policy
```

This validation is not REG-GATE by itself. Runtime baseline identities,
path-free realization evidence, existing schema records, a registration freeze,
and a resolved manifest remain required.

Build the 21-entry W0 baseline registry with one fresh worker process per
cell/seed configuration. The realization profile and graph checkout arguments
are local paths and never enter the retained registry:

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_registration.py build-baseline-registry --realization-profile experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/registration-realization-profile.json --graph-root LOCAL_GRAPH_CHECKOUT --output experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/baseline-identity-registry.json
```

The command constructs and snapshots only W0. It requires empty queue and
surface state and does not schedule writer, medium, reader, or candidate
operations.

Verify the admitted N29/N30 sources against the clean, read-only graph source
snapshot. The retained result contains only `grc:` identities and digests, not
the local checkout argument. Every source is recorded as non-identical in
carrier, mechanism, intervention, and claim scope, so it cannot replace fresh
lane execution:

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_registration.py build-inherited-verification --graph-root LOCAL_GRAPH_CHECKOUT --output experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/inherited-control-verification.json
```

Generate the registration binding receipt with every operation class declared
by the retained realization profile:

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_registration.py build-runtime-receipt --graph-root LOCAL_GRAPH_CHECKOUT --output experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/registration-runtime-binding-receipt.json
```

After the source implementation is committed, combine those artifacts with
the existing-schema registration records into a derived freeze:

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_registration.py build-registration-freeze --baseline-registry experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/baseline-identity-registry.json --inherited-verification experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/inherited-control-verification.json --runtime-receipt experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/registration-runtime-binding-receipt.json --output experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/registration-freeze.json
```

The derived freeze may resolve deterministic registration and inherited-source
legs only. Causal and terminal legs remain `pending_execution`, and the freeze
does not pass REG-GATE or authorize candidate execution. The resolved manifest
is built afterward to avoid a recursive freeze/manifest digest.

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_registration.py build-registration-manifest --baseline-registry experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/baseline-identity-registry.json --inherited-verification experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/inherited-control-verification.json --runtime-receipt experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/registration-runtime-binding-receipt.json --registration-freeze experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/registration-freeze.json --output experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/registration-manifest.json
```

Retained generation fails when source files differ from the current commit.
The five expected generated registration outputs may be untracked while the
bundle is assembled; no other change is ignored. During source review only,
the inherited-verification, receipt, baseline, and freeze commands accept
`--allow-dirty-preview`. Such artifacts record a preview-specific kind,
`retention_eligible=false`, and `preview_only=true`; the manifest command has
no preview mode and rejects every preview input.

Registration-time control resolution is evidence-specific. Every resolvable
leg carries exact `evidence_binding_refs`; the derived freeze marks it resolved
only after those exact record, source, receipt, profile, or baseline identities
have passed their concrete validators. Changing descriptive evidence text or
substituting another existing record fails policy validation.

The runtime receipt additionally resolves every abstract operation class to
concrete callable PyGRC methods. Namespace/version availability alone cannot
establish conformance for feedback-surface emission, feedback-conditioned
production, stepping, or snapshot round-trip.

### Runtime preflight

Runtime preflight requires an ignored local `realization_profile` record whose
availability, enabled, supported, and validated fields are all true; whose
PyGRC identity is `pygrc==0.1`; and whose allowed operations contain
`p2_i1_runtime_preflight`. The local environment must already make that exact
PyGRC available. Its installation and checkout locations are arguments only
and never enter a shared record.

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1.py runtime-preflight --realization-profile outputs/p2-i1-local-realization-profile.json --run-id p2-i1-local-preflight --graph-root LOCAL_GRAPH_CHECKOUT --output outputs/p2-i1-runtime-preflight.json
```

Missing dependencies, an incompatible identity, a disabled local profile, or
an undeclared operation produces a failed binding receipt and no fallback.
The preflight builds and snapshots the baseline fixture only. It does not emit
a writer packet, medium row, opportunity, candidate result, or lane evidence.

### C01 execution and live-obligation audit

`p2_i1_execution.py` validates the exact C01 policy and keeps candidate
execution disabled during source review:

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_execution.py validate-policy
```

After the implementation source is committed, bind the exact C01-only call
superset without scheduling a writer, medium, or reader operation:

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_execution.py build-execution-binding --graph-root LOCAL_GRAPH_CHECKOUT --output experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c01/execution-binding-receipt.json
```

Then build the candidate-free cycle authorization at its declared path:

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_execution.py build-exec-freeze --execution-binding-receipt experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c01/execution-binding-receipt.json --output experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c01/exec-freeze.json
```

Dirty source may produce only a non-retainable preview with
`--allow-dirty-preview`. A preview records
`candidate_execution_authorized=false` and cannot pass the runtime guard. The
retained freeze must then be committed: `run-one` and `run-cycle` require its
bytes to match the current tracked `HEAD` record.

Once EXEC-FREEZE passes, execute all 21 primaries in fresh worker processes.
The graph checkout remains a local-only argument:

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_execution.py run-cycle --exec-freeze experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c01/exec-freeze.json --graph-root LOCAL_GRAPH_CHECKOUT --summary-output outputs/p2-i1-c01-run-summary.json
```

The orchestrator retains operational failures in the retry ledger and derives
at most one retry per cell for the lowest failed seed. A retry keeps the same
scientific configuration digest and cannot be allocated from candidate
outcomes.

After execution, derive the cross-run structural audit:

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_execution.py build-cycle-audit --exec-freeze experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c01/exec-freeze.json --output experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c01/cycle-audit.json
```

The audit resolves initialization, isolation, restoration, medium
reconstruction, exposure, support/budget, producer parity, trace-shuffle, and
runtime-receipt structure. It preserves observed responses but assigns no
threshold verdict, boundary rung, or terminal class.

Index the effective runs, retry ledger, and completed cycle audit only after
those files validate:

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_execution.py build-execution-manifest --exec-freeze experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c01/exec-freeze.json --output experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c01/execution-manifest.json
```

The execution manifest is a retention index. It cannot assign a boundary rung
or terminal classification, and it preserves each run's independent
reconstruction status.

## P2-I2 I03AR1 state-carried conformance

`p2_i2_i03ar1_conform.py` resolves and validates the immutable I03AR1 base
freeze plus its governed I03AR1R1 comparator revision. It checks the RCAE
`.venv`, admitted PyGRC import root, exact graph revision/source digests,
read-only graph status, harness identity, fixture, assertions, run limit, and
scientific-evidence quarantine before constructing a model.

The one replacement evidence invocation and one reconstruction invocation are
already exhausted. They passed 136/136 assertions and produced byte-identical
records. The exact historical commands remain in the freeze and
reconstruction receipt for audit; this README grants no rerun authority. See
the [I03AR1 report](../reports/P2-I2-I03AR1-state-carried-runtime-conformance.md)
and [attempt receipt](../contracts/p2-i2/i03ar1r1-runtime-reconstruction-receipt.json).
