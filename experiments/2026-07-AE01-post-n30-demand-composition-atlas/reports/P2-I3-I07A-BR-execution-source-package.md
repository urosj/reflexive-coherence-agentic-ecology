# P2-I3 I07-A B-R execution-source package

Date: 2026-07-19; bounded authority-hardening correction 2026-07-20

## Outcome

I07-A is review-ready as a candidate-free source package. It consumes the
owner-accepted I06A package `1.0.2` retained at commit `0769e5c`, projects its
unchanged 450-case evidence registry into the corrected 456-entry execution
schedule, and proves that an inactive-freeze preview can be constructed against
the exact admitted PyGRC source without invoking a public runtime operation.

This is not I07-B and is not an execution freeze. The preview is explicitly
retention-ineligible because the I07-A source tree is not yet committed. No
candidate, control, integrity-fault, model-construction, packet, event, native
save/load/reset, response, or scientific/ecology operation occurred.

## Why I07-A follows accepted I06A

I06A answers whether the complete future execution inventory is registered.
I07-A asks whether clean committed source can represent and enforce that
inventory. The owner accepted I06A specifically so this later layer could find
remaining executability defects without pretending REG-GATE already certified
the harness.

The audit found source-package defects, not a change to the registered science:

1. the paused runtime projected only the 450 evidence cases and ignored the six
   operational baseline entries;
2. its fixed repository-parent count resolved one directory above the clone;
3. it used a 906-root terminal set and the superseded 454-start ceiling;
4. baseline entries had no dispatch, terminal, or dependent-load path;
5. the supervisor wrote P2 through P5 before starting the child, so the claimed
   restoration-before-dispatch order was false;
6. timeout used a single-process convenience call rather than process-group
   termination and did not materialize the registered retry/resume transaction;
7. captured log overflow could leave an oversized final stream artifact; and
8. the first predecessor checks assumed an obsolete exact CAL-GATE string and
   a canonical-payload encoding without the repository-standard trailing
   newline.

All eight were corrected inside I07-A. The 450 scientific/integrity identities,
90 configurations, case-set selectors, estimator, values, controls, resource
classes, and scientific claim boundaries remain unchanged.

## Exact source projection

The source policy binds:

```text
I06A retention commit                 0769e5c6e3fefbb25c7841a3878da2d29c8d0604
I06A registration SHA-256             7d5987223f42ef053beefbb5afb5fd88cf1fcd150a0048818b96f5718ae878b6
I06A validation SHA-256               d02e59b978b5cad22251c76ad0f703c8842b1792593e807a99a21e5faa47f1f1
I06A REG-GATE SHA-256                 376ddd9272d8880bc9b9d8d47a7f5eb06cbb9a2814d486e5f8b92caf34049c94
canonical evidence cases              450
operational baseline entries            6
governed execution entries            456
maximum governed child starts         460
expected terminal roots               919
public PyGRC entries                    18
blocked PyGRC entries                    4
```

Every governed entry receives one schedule identity, execution class, resource
assignment, primary and retry position, exact dependency set, P0-P7 phase
protocol, expected artifact roles, and 26 portable governed paths. The six
baseline entries remain outside every scientific selector and retain zero
formation, export, encounter, scientific-control, and integrity-fault counts.

The expected terminal set contains:

```text
campaign claim closure                   1
primary attempt-slot closures          456
scientific/integrity case resolutions  450
operational baseline terminals           6
class retry-token closures                4
supervisor resume closure                 1
cycle closeout                            1
                                        ---
                                        919
```

## P4/P5 execution handshake

The child and supervisor now implement an actual two-party boundary:

```text
durable entry claim
  -> fresh child starts
  -> child loads authorities and restores or validates its immutable parent
  -> child writes a zero-operation P4 readiness receipt
  -> supervisor validates readiness
  -> supervisor durably issues entry-specific P5
  -> child atomically consumes P5
  -> exactly one registered entry dispatch may begin
```

For an operational baseline, pre-P5 preparation validates the exact planned
realization and delay profile but does not construct a model. Model
construction, content-addressed save/load verification, and reset-identity
verification occur only after P5. Scientific trajectories and integrity cases
load the already retained operational baseline in a fresh interpreter before
P5. Terminal probes load their exact trajectory checkpoint before P5 and do
not reconstruct or advance the parent trajectory.

The campaign claim still does not cross P5. Freeze acceptance, activation, the
campaign claim, the governed-entry claim, readiness, and P5 consumption remain
separate authorities.

## Pre-anchor authority hardening

Owner review accepted the scientific and schedule projection but found two
source-level authorization gaps. Both are corrected before the clean I07-A
anchor:

1. `freeze_acceptance` and `activation` are closed records. Their schemas
   declare every base and record-specific field with
   `additionalProperties=false`, and the supervisor independently requires the
   exact field sets before interpreting either record.
2. Every retained build, validation, reconstruction, and future-launch command
   carries the complete normalized environment. Activation separately binds
   the exact environment, normalized `PYTHONPATH`, resolved interpreter-file
   digest, graph revision and PyGRC-root digest, and the no-symlink policy for
   governed claims, outputs, temporaries, and content storage. Launch validates
   these bindings before importing or dispatching the case harness.

An adversarial test supplies an importable ambient `pygrc` package rather than
depending on the installed package being stale. The builder refuses its module
location before resolving or invoking a public runtime symbol, and a sentinel
confirms that no fake public call occurred.

## Why 919 terminal roots remain exact

I07-A selects closure-root Model A. The four permanent class retry-token roots
own any optional attempt-2 claim, phase ledger, P5 records, logs, resource
receipt, terminal, output, and final entry resolution as digest-bound
descendants. Attempt-2 terminals therefore do not add four independent roots.

Each class-token root closes in exactly one state:

```text
unused
allocated_before_attempt_2_claim
attempt_2_failed
attempt_2_valid_terminal
```

The supervisor rejects a retry descendant without a class token, a descendant
owned by another entry in the class, an attempt-2 terminal without its claim,
or a claimed attempt without a terminal. All four states and the orphan/
unresolved cases are covered adversarially. Thus `919` counts closure roots,
not every possible descendant file.

## Failure, resource, retry, and resumption source

The external supervisor imports neither PyGRC nor the case-runtime module. It:

- launches each child in a fresh process group and observes process-tree RSS;
- terminates the complete process group with `SIGTERM`, exactly ten seconds of
  grace, and `SIGKILL` if required;
- writes supervisor-owned JSONL phases and terminal/resource receipts;
- captures stdout and stderr through governed partial paths, stops on overflow,
  retains only the registered prefix, and atomically promotes the prefix to
  the final path;
- permits no experiment-imposed `RLIMIT_AS` or RSS kill threshold;
- allocates each class retry token exclusively and permanently only from an
  externally attested pre-P5 infrastructure failure;
- preserves attempt 1 and admits attempt 2 only through one final entry
  resolution; and
- permits one same-boot resume only when no claimed attempt lacks a terminal,
  without resetting the campaign clock, schedule, or resource budget.

These are frozen source semantics. No failure was injected and no live child
was started during I07-A.

## Candidate-free verification

Use the repository-local environment and exact admitted graph source:

```bash
env \
  RCAE_PYGRC_ROOT=../graph-reflexive-coherence \
  PYTHONPATH=../graph-reflexive-coherence/src:experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts \
  PYTHONNOUSERSITE=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONHASHSEED=0 \
  OMP_NUM_THREADS=1 \
  OPENBLAS_NUM_THREADS=1 \
  MKL_NUM_THREADS=1 \
  NUMEXPR_NUM_THREADS=1 \
  BLIS_NUM_THREADS=1 \
  VECLIB_MAXIMUM_THREADS=1 \
  .venv/bin/python -B \
  experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i3_i07_br_freeze.py \
  build \
  --graph-root ../graph-reflexive-coherence \
  --allow-dirty-preview \
  --output-dir /tmp/p2-i3-i07a-preview
```

Focused source verification:

```bash
.venv/bin/python -m unittest \
  experiments/2026-07-AE01-post-n30-demand-composition-atlas/implementation/tests/test_p2_i3_i07_br.py
```

Observed results:

```text
focused I07-A tests                  40 / 40 passed
I06A plus I07-A unittest closure    82 / 82 passed
dirty preview construction           passed
second byte-identical preview         passed
preview governed entries               456
preview expected terminal roots         919
preview public symbol invocations         0
preview candidate/control operations       0
preview retained absolute paths             0
```

The first adjacent test invocation without the source binding failed while
importing the stale installed PyGRC distribution, before test execution. The
same 82-test command passed with the exact admitted graph `src` binding. A
separate controlled test now supplies an otherwise importable ambient PyGRC
and proves it is rejected by source ownership before any public call. This is
an intentional no-fallback result, not an incidental version mismatch or a
dependency workaround.

An additional historical I05 inactive-freeze test still expects the later
I05 launch-authorization file to be absent; it now reports one stale-state
failure because I05 has already completed. The other 71 I04/I05 pytest checks
pass. I07-A does not alter that historical test.

## Current gate boundary

```text
I06A REG-GATE:                       passed and retained
I07-A source package:                review-ready, uncommitted
I07-A dirty preview:                 passed, retention-ineligible
I07-B inactive freeze:               not constructed
P2-I3-EXEC-FREEZE:                   unopened
freeze acceptance:                   absent
execution activation:                absent
campaign claim:                      absent
candidate/control/integrity execution: unauthorized and absent
```

The next permitted action after review is the clean I07-A source-anchor
commit. Only that commit permits construction of I07-B retained freeze records
and their independent validation. I07-B acceptance still would not authorize
execution; explicit activation remains separate.
