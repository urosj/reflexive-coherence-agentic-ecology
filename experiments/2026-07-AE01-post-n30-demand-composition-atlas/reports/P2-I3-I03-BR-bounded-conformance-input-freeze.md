# P2-I3 I03 B-R Bounded-Conformance Input Freeze

**Status:** accepted and inactive

**Decision:** accepted `P2-I3-DEC-034`

**Runtime operations:** zero

**Scientific evidence effect:** none

## 1. Why this freeze exists

DEC-027 through DEC-033 now say what B-R must mean, but they do not yet prove
that the exact public PyGRC runtime and a narrow RCAE producer can express the
whole operation chain. This freeze places one review boundary before any
conformance model is constructed or stepped.

The conformance question is deliberately narrower than the scientific one:

```text
Can the accepted B-R lifecycle, fixed encounter, contrasts,
restoration, refusal, and quarantine interfaces be executed exactly?

!=

Does B-R support AE01-H-L03?
```

A passing fixture will establish operational expressibility only. A failure
will be source, implementation, restoration, or missing-surface evidence—never
a negative trail/stigmergy result.

## 2. Authority and source transition

The [machine freeze](../contracts/p2-i3/i03-br-bounded-conformance-input-freeze.json)
binds accepted RCAE commit `12763ba`, the I02 source-admission manifest, the
N31 return admission, the common comparison envelope, the contrast/restoration
design, and the operational hypotheses.

The graph runtime is bound to clean merged N31 revision `565706f`. This does
not silently re-admit a new PyGRC provider. The I02 manifest remains the
callable/source authority, while the accepted N31 transition records that the
protected PyGRC runtime sources did not change between its admitted provider
revision and the merged N31 revision. Nine exact graph source digests are
rechecked at the current revision.

The graph repository remains read-only. Its location is supplied locally by
`RCAE_PYGRC_ROOT`; no machine-specific or absolute path enters the freeze.

## 3. Exact public runtime surface

The freeze admits eighteen public symbols for this fixture:

- `PortGraphBackend`, `GRC9V3NodeState`, `GRC9V3State`, and `PortEdge` for
  deterministic construction;
- `LGRC9V3.from_state`, `get_state`, `schedule_packet_departure`, `step`, and
  `run_event_queue` for the LGRC9V3 event runtime;
- `snapshot`, `save`, `load`, and `reset` for native persistence;
- restoration identity v2 and its digest; and
- the geometric, functional, and causal distance interfaces for operational
  addressability only.

Synchronous `GRC9V3.step`/`apply_continuity`, direct `LGRC9V3.set_state`, and
reset-baseline rebasing are blocked. The freeze therefore cannot replace LGRC
with GRC relaxation or install the desired state through a shortcut.

## 4. RCAE ownership is narrow

The later `p2_i3_br_runtime.py` implementation is constrained to three
interfaces:

1. An export policy receives one route-local carrier coherence value, one
   exact receipt, frozen policy/structural bindings, and the predecessor
   composite identity. It returns a typed lifecycle transition and at most one
   native request. It never receives the model, destination state, other
   route, raw history, wall clock, or an outcome.
2. A blind encounter adapter receives structural opportunity data only. It
   cannot see carrier state and cannot author native admission/refusal.
3. A manifest-coordinated composite restoration interface binds native,
   policy, branch, reset, and audit state and fails before returning a runnable
   branch when any component is missing, stale, tampered, or cross-bound.

All invoked state transitions remain native LGRC9V3 transitions. These RCAE
interfaces stay explicit producer/naturalization debt even if conformance
passes.

## 5. Result-neutral fixture

The fixture contains two role-matched routes, each with source, carrier,
isolated reservoir, continuation, and isolated control destination roles.
There is no participant label, preferred route, or global selector.

Its values are chosen solely to expose both operation paths:

```text
initial carrier             0.1
two formation requests      0.2 + 0.2
formed carrier              0.5
export floor / cap          0.4 / 0.1
post-export carrier         0.4
fixed encounter request     0.45
```

Thus the same structural request is natively admissible before the export and
insufficient afterward. This is an intentional implementation boundary split,
not a calibrated threshold or expected scientific effect. Every topology,
number, time, disposition, and observation is prohibited from I04, I05, I06,
I08, controls, and terminal interpretation.

The fixture is deterministic, uses no seed, allows one attempt and zero
retries, and bounds each native queue at 32 events.

## 6. Eleven conformance cells

The frozen matrix checks:

1. exact runtime and operation binding;
2. two attributable native formation events and persistence;
3. one positive conservative export and settlement;
4. eligible-zero, invalid, duplicate, and pending-settlement semantics;
5. fixed local native admission plus exact atomic refusal;
6. separate addressability of all three Q-013 contrast constructors;
7. composite save/load/reset/fork/replay and bounded equal-input continuation;
8. partial, stale, tampered, and cross-bound load refusal;
9. distinct control/variation interfaces without assigning their outcomes;
10. forbidden-read and hidden-router exclusion; and
11. mechanical fixture quarantine.

The state/history conformance cell tests that the exact identity can retain
different audit histories while the causal projection excludes only declared
audit-only data. It does not claim that a scientifically valid pair has been
constructed, and projection equality is not treated as continuation evidence.
I06 still owns the exact scientific construction.

## 7. Quarantine mechanics and their honest limit

`p2_i3_conformance_quarantine.py` rejects the dedicated conformance namespace,
artifact-kind prefix, declared provenance tags, output digests, and fixture
value identities from calibration, registration-value, candidate, control,
scientific, and terminal payloads. The zero-runtime validator executes a
negative self-test for all eight forbidden consumer classes.

No validator can recognize a naked copied number after its provenance has
been dishonestly removed. The project therefore requires later builders to
retain declared value provenance; the guard mechanically rejects that
provenance when it points to I03 conformance. This is the proportional
boundary, not a claim of exploit-proof information flow.

## 8. Validation performed

The exact command was:

```bash
env RCAE_PYGRC_ROOT=../graph-reflexive-coherence .venv/bin/python -B experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i3_i03_br_freeze_validate.py --graph-root ../graph-reflexive-coherence
```

It passed 85 checks with:

```text
runtime operations:          0
conformance output exists:   false
graph revision exact:        true
graph worktree clean:        true
required public calls:       18/18 callable
fixture/matrix checks:       passed
quarantine negative tests:   8/8 rejected
```

The validator imported the exact local PyGRC source to verify public symbol
identity and callability. It did not construct an LGRC model, schedule a
packet, step a runtime, write an artifact, or inspect a conformance outcome.

## 9. Acceptance and next boundary

DEC-034 freezes this input and authorizes construction of the
exact runtime module and harness, followed by the one bounded conformance run
from a committed clean source state. The run must retain its environment,
source, freeze, harness, output, and reconstruction identities.

Acceptance does not pass `P2-I3-DISCRIMINATOR-GATE`, open I04, assign a
control outcome, or produce scientific evidence. Any concrete correction is
applied before the run; absent such a correction, the package is the complete
review boundary.

Results may later motivate a stronger topology, a narrower producer, a more
native realization, or a more discriminating comparison. That search remains
allowed and expected. It receives new realization, freeze, execution, and
artifact identities, preserves this result as history, and reruns affected
comparisons rather than retroactively tuning this fixture. The possibility of
stronger later proof neither weakens nor inflates the present bounded result.
