# P2-I2 APP-A2 fresh-runtime matrix and closeout

## Current disposition

APP-A2 completed its one authorized 19-arm fresh-runtime campaign and
retained-aggregate-only reconstruction. All arms are operationally valid, the
frozen primary and causal relations pass, reconstruction is byte-identical,
and closeout validation passes 53/53. The exact bounded result is review-ready
and owner-accepted under DEC-074/CHG-079. Appendix A is closed and one
containing closeout commit is authorized.

```text
retained APP-A1 authority:              commit 1f69816
frozen arms:                            19
activation authority:                   retained at e61dacc
campaign claims consumed:               1
campaign invocations/retries:            1/0
child arm starts/retries:                19/0
fresh scientific models:                19
operationally valid arms:                19/19
scientific gate signatures:             19
runtime aggregate:                      retained uncommitted
reconstruction/closeout:                retained uncommitted
Appendix result:                        supported_bounded_candidate
inactive validation:                    96/96 passed
implementation owner acceptance:        granted under DEC-070
containing implementation commit:       retained at c435b00
activation candidate validation:         51/51 passed
activation commit:                       e61dacc
closeout validation:                     53/53 passed
owner result acceptance:                 granted under DEC-074
Appendix A:                              closed
result commit:                           authorized and pending
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

The implementation package is now retained at `c435b00`. The separately
constructed activation candidate binds that full commit and passes 51/51
zero-science checks. Its active-shaped runtime fields are deliberately
prospective: the candidate remains uncommitted, its present-effect fields deny
activation/campaign authority, and the runner refuses an authorization not
tracked byte-identically in HEAD.

The first activation-validator check-only start stopped at 50/51 because the
validator stripped the first `git status` row's leading status column. One
PyGRC-free diagnostic identified that parser defect; the corrected check-only
and retained runs pass 51/51. These four `.venv` processes imported no PyGRC,
constructed no model, and created no runtime output. Owner review of the exact
authorization and validation is now required before any activation commit or
campaign start.

The owner then stated `accept, continue`. DEC-072 accepted the exact 51/51
activation bytes and authorizes their containing commit, the runner's exact
clean-HEAD preflight and exclusive claim, the single 19-arm campaign, and the
frozen retained-aggregate-only reconstruction. Result acceptance and result
commit remained closed until the resulting evidence was returned for review.

## Runtime execution

The accepted activation was retained at `e61dacc`. Its exact clean-HEAD
preflight passed and the campaign atomically consumed its only claim before
starting the first child. It completed all 19 frozen rows once through fresh
processes and fresh 12-node/28-edge PyGRC models. There were no campaign or
child retries and no per-arm files.

```text
campaign invocations/retries:    1/0
child starts/retries:            19/0
fresh models:                    19
valid arms:                      19/19
operation packets:               228
response packets:                76
native packet events:            608
maximum queue length:            4
per-arm files:                   0
aggregate files:                 1
```

The full `GEP` arm passes the complete registered signature:

| Gate | Observed | Registered bound | Result |
| --- | ---: | ---: | --- |
| environment feedback | `0.046739999999999976` | `>= 0.04` | pass |
| support feedback | `0.02214000000000002` | `>= 0.02` | pass |
| phase residual | `0.01296` | `<= 0.015` | pass |
| route-merge leakage | `5.538584076652357e-16` | `<= 1e-12` | pass |
| configuration retention | `0.82` | exact registered value | pass |

Reference, `G`, `E`, `P`, `GE`, `GP`, and `EP` are all valid arms and all fail
the complete measured signature. The full-composition versus every-proper-
subset primary relation therefore passes without treating invalid execution as
scientific insufficiency.

## Causal and control resolution

The causal relation also passes. Removing each of `G`, `E`, and `P` changes
the later response, each corresponding mediator-restoration intervention
changes that response, and clamping the shared carrier changes the response.
Native response sources are carrier-only and the reference is fully diverted.
No external producer is load-bearing in the realized relation; the operation,
carrier, and later-response paths use the accepted native PyGRC machinery.

The one-source and cyclic contributor-role controls reproduce the relation,
and label permutation is invariant. Both tested adjacent order inversions,
`EGP` and `GPE`, pass. These controls resolve two tempting overclaims:
physical participant plurality is not load-bearing in this frozen fixture, and
the tested operation order is not load-bearing. The result concerns the three
physically distinct operations composing through the carrier, not a necessary
three-agent coalition or a unique sequence.

## Reconstruction and bounded disposition

The reconstructor read the retained aggregate exactly once, regenerated no
scientific state, and reproduced the analysis byte-identically. It made zero
PyGRC imports, model calls, child starts, producer calls, or scientific
generation calls. The corrected closeout validator passes 53/53 with the same
zero-regeneration boundary. Its first check-only start reported 52/53 only
because its source sentinel matched its own literal `import pygrc`; one
PyGRC-free diagnostic localized that self-match and the in-place sentinel
correction produced both passing check-only and retained runs.

```text
terminal classification = supported_bounded_candidate
bounded claim = bounded generator-extractor-redistributor shared-carrier
                composition candidate
functional scope = bounded functional complementarity through the common
                   carrier relative only to the frozen fixture and gates
main P2-I2 terminal changed = false
N29 metric equivalence claimed = false
```

The evidence does not establish coalition, functional cooperation,
coordination, resource economy, agency, collective identity, an ecology motif
or regime, cross-lane recurrence, or N31+ selection. DEC-073/CHG-078 retain
that exact claim ceiling.

## Owner acceptance and Appendix closeout

The owner states `ok, do close appendix and commit`. DEC-074/CHG-079 bind the
exact reviewed runtime, reconstruction, validation, validator, and pre-
acceptance report identities; accept the bounded result; close Appendix A; and
authorize one containing closeout commit. Acceptance changes no technical
result byte and opens no later synthesis, selection, graph mutation, or next
move.

The acceptance-integrity check initially reported 8/9 because it compared the
interpreter's lexical path with the resolved `.venv` path. One `.venv`-only
diagnostic showed every substantive identity check passed and isolated that
normalization mismatch. The corrected resolved-path check passes 9/9. Across
all three acceptance-integrity Python starts there were zero PyGRC imports,
models, children, producers, or scientific regeneration calls.
