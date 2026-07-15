# P2-I2 APP-A2 fresh-runtime matrix and closeout

## Current disposition

APP-A2 implementation construction is complete and review-ready. The exact
19-arm runner, pure receipt analysis, read-only reconstructor, inactive
activation freeze, and zero-science validator are frozen. Final inactive
validation passes 96/96. The scientific campaign has not started.

```text
retained APP-A1 authority:              commit 1f69816
frozen arms:                            19
campaign attempts authorized now:       0
child arm starts:                       0
scientific models:                      0
scientific gate signatures:             0
runtime aggregate:                      absent
reconstruction/closeout:                absent
Appendix result:                        unassigned
inactive validation:                    96/96 passed
owner acceptance:                       granted under DEC-070
containing implementation commit:       authorized, pending
```

## Implemented causal path

Every future arm is supplied as its one exact frozen row to a fresh repository
`.venv` child. The child constructs a fresh 12-node/28-edge LGRC9V3 model,
executes all three operation slots through either common-carrier or matched
diversion packet paths, applies only the registered intervention, invokes the
native carrier-only causal-flux response, and returns one canonical receipt to
the parent over stdout. It writes no per-arm file.

The receipt retains packet records and native departure/arrival events for
each operation, exact source/target/edge identities, predecessor/successor
restoration identities, the registered intervention target and public
packet-ledger rebase, native response-producer reasons, carrier-only source and
passive-R target identities, resource/budget evidence, and save/load,
continuation, and reset evidence. Operational validity and causal comparisons
are derived from those receipts; no child-authored result boolean can satisfy
the matrix.

## Entry isolation and fail-closed behavior

The parent makes one exclusive aggregate claim before the first arm. That
claim permanently consumes the one campaign attempt and prevents concurrent or
later starts. Each child receives only its arm row and retained authorities;
the implementation has no earlier-result scan, per-arm output, adaptive
parameter path, retry, outcome-dependent ordering, or shared adapter, cache,
queue, temporary path, or RNG across arms.

Static review found and corrected one preactivation isolation defect: the
first parent draft stopped on a failed arm. The frozen runner now records a
failed, timed-out, malformed, or refused arm attempt and continues to every
later frozen row. Thus an incomplete earlier arm cannot change later entry
authorization. Any missing or invalid receipt still makes the complete matrix
nonevaluable.

Output paths are restricted to the two registered JSON artifacts under the
P2-I2 contract directory and cannot shadow a Python module or configuration
file. No per-entry narrative is produced.

## Read-only reconstruction

The reconstructor imports no PyGRC and invokes no subprocess, model, producer,
or scientific generation path. It validates the retained aggregate and
authorities, reprojects analysis from the retained arm receipts, requires
byte-identical analysis, and then writes the single registered closeout through
exclusive creation. It cannot replace or regenerate the runtime campaign.

## Static process ledger

All 18 APP-A2 construction-time Python processes used `.venv/bin/python -B`.
They comprised one entry-identity probe, four compile/static syntax processes,
one environment identity probe, one validator diagnostic, and eleven validator
starts. None imported PyGRC or constructed a model.

The first validator check-only start reported 87/89 because two validator
rules were overbroad: its own generic path sentinel was treated as a persisted
absolute path, and the aggregate byte-write loop was mistaken for an adaptive
retry. No output was retained. Corrected rules passed 89/89 in check-only and
retained forms. A subsequent cache audit found four ignored bytecode files
created by explicit compilation; they were removed and cache absence was added
to preflight. The cache-aware check-only and retained validations both passed
90/90. A final authority-chain review made both the future runner and
reconstructor require that retained passing validation, producing 92/92
check-only and retained passes. The final portability audit then required the
runner, reconstructor, and validator to reject absolute CLI arguments rather
than merely normalize repository-local absolute paths. The final check-only
and retained validations passed 95/95. The final failure-path check also
normalizes the private temporary root before any error can enter a retained
failed-closed aggregate; final check-only and retained validations pass 96/96.
No APP-A2 bytecode cache remains.

## Activation boundary

The inactive freeze binds the retained APP-A1, graph, `.venv`, dependency,
implementation, command, output, isolation, resource, and one-attempt
identities. It deliberately does not contain an activation authorization.

The owner has accepted the exact inactive package and authorized its containing
implementation commit. After that commit succeeds, one activation
authorization may be constructed against it and returned for validation. Only
a later explicitly accepted and retained activation may make the exclusive
campaign claim. The campaign, scientific gates, reconstruction, and bounded
Appendix classification remain closed now.
