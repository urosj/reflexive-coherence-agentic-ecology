# AE01 Hypotheses

**Status:** P1-I4 hypothesis, control, and failure freeze complete

**Acceptance state:** preregistration only; `AE01-C0` remains the highest
assigned rung

## Frozen P1-I4 set

- [Outcome and stopping contract](outcome-and-stopping-contract.md) defines the
  universal terminal meanings, finite comparison groups, bounded attempts, and
  stopping procedure.
- [Lane hypotheses](lane-hypotheses.md) defines `AE01-H-L01` through
  `AE01-H-L07`, their positive/null/partial/blocked/incomplete signatures,
  mandatory controls, and lane ceilings.
- [Cross-lane and non-selection hypotheses](synthesis-hypotheses.md) defines
  `AE01-H-S01` recurring operational demand and `AE01-H-S02` explicit N31+
  non-selection.
- [Control and failure register](control-and-failure-register.md) defines common
  controls `AE01-CTRL-01` through `AE01-CTRL-19` and failures `AE01-F01`
  through `AE01-F10`.

These documents preserve the distinction between N29/N30 evidence, ecology
interpretation, constructed RCAE mechanisms, observed AE01 results, missing
graph surfaces, and proposed graph discriminators.

## Hypothesis interpretation

The seven lanes are not seven attempts to simulate complete ecologies. They
are seven views of one deeper question: what must exist for local formations
to be conditioned by a shared history that is carried outside any one closed
participant?

The sequence exposes progressively different demands:

| Hypothesis | Interpreted demand |
| --- | --- |
| `AE01-H-L01` | A changed medium can alter later local formation or susceptibility. |
| `AE01-H-L02` | Multiple attributable histories can co-condition one shared carrier. |
| `AE01-H-L03` | Costly traces can persist and alter later route or continuation eligibility. |
| `AE01-H-L04` | Earlier activity can reshape support conditions for later fragile formations. |
| `AE01-H-L05` | Maintained boundary state can condition exchange and closure. |
| `AE01-H-L06` | Auditable capacity history can circulate and alter later eligibility. |
| `AE01-H-L07` | Parent-level state may require a missing distinction to modulate separable local susceptibilities. |
| `AE01-H-S01` | Independent lanes may expose the same operational prerequisite. |
| `AE01-H-S02` | The atlas can close without forcing a successor when evidence is insufficient or unstable. |

The atlas therefore searches for recurring causal interfaces, not for the most
evocative ecology metaphor. A positive-looking lane that depends on a hidden
producer, passive storage, free budget, fixture-specific code, or semantic
relabel is deliberately more valuable as a classified failure than as an
inflated success.

Lane 7 is intentionally asymmetric. Its successful outcome may be a precise
missing-surface classification and future discriminator. It does not seek to
manufacture positive M3/M4 evidence that N30 did not provide.

The synthesis hypothesis separates recurrence from selection. Two independent
lanes can establish a recurring demand, while the stricter D-029 thresholds,
tie procedure, sensitivity profiles, reconstruction, and claim-safety gates
still produce non-selection. That is an informative closeout rather than a
failed program.

## Implementation handoff

P1-I4 freezes logical semantics; P1-I5 must make them executable without
changing them. The implementation must:

1. treat hypothesis, control, lane-control, and failure IDs as closed validator
   vocabularies, with lane IDs resolving one-to-one to lane hypothesis IDs;
2. use the existing P1-I3 pattern-card, medium, requirement, composition, debt,
   claim, construction, runtime, terminal, ranking, manifest, and report
   records rather than inventing a second result schema;
3. materialize each lane's required comparison groups into a finite config
   matrix with deterministic seeds or a no-seed declaration, exact thresholds,
   attempt limits, time/resource envelopes, and expected artifacts;
4. generate control references and require an explicit applicability
   disposition for every common control;
5. prevent `supported_bounded_candidate` unless every mandatory support
   signature and control passes on verified retained evidence;
6. permit `not_supported` only after a valid complete probe, never after runtime
   absence, fallback, or failed reconstruction;
7. preserve every failure in pattern, terminal, debt, synthesis, and report
   projections;
8. keep constructed mechanisms constructed across runtime availability changes
   and require explicit transition/rerun for a native profile;
9. validate that cross-lane recurrence uses independent lineage rather than
   repeated names, fixtures, or copied constructions, and block synthesis until
   all seven lane terminal records exist;
10. enforce the fixed D-029 non-selection rules without scoring ineligible
    candidates or allowing qualitative intuition to become a silent override;
    and
11. treat the graph/PyGRC repository as read-only in every inspection,
    validation, execution, test, and reconstruction path.

Each lane currently has exactly five lane-specific controls. P1-I5 should
validate those frozen AE01 IDs, but the symmetry is an AE01-local structural
convention rather than a requirement for future experiments. A lane's
“especially direct” common controls determine implementation priority only;
all nineteen common controls still require an explicit applicability
disposition for every lane.

P1-I5 should implement these stable IDs as semantic-validator vocabulary and
tests. It must not add a persisted hypothesis-register record under schema
version `1.0.0`. If a persisted registry becomes necessary, the P1-I3 schema
must receive a new version and the affected gate must reopen explicitly.

## Freeze and evidence boundary

Metric thresholds, fixtures, seed sets, profiles, and commands remain P1-I5
work because they depend on the tooling and reconstruction envelope. They must
be frozen before P1-GATE and cannot be tuned after lane outcomes without a
contract revision and affected rerun.

No hypothesis result, control result, failure occurrence, terminal
classification, recurring requirement, or N31+ candidate is recorded by this
P1-I4 freeze.

P1-I5 materializes this handoff in the
[artifact, tooling, and reconstruction contract](../implementation/P1-I5-tooling-contract.md)
without changing the P1-I4 hypothesis meanings.
