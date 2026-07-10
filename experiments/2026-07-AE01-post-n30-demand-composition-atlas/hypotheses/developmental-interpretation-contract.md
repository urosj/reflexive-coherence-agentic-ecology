# AE01 Developmental Interpretation Contract

**Status:** frozen at P1-I4 revision 0.24

**Policy:** `configs/p1_i4_developmental_interpretation_policy.json`

**Evidence effect:** preregistration only

## 1. Methodological correction

AE01 uses fixed hypotheses, controls, and thresholds to discipline observation.
It does not let those provisional targets own the first interpretation of an
irreducible result.

Every valid result is read twice:

```text
becoming reading:
  what appeared, at what rung, under what support, with what claim ceiling?

development reading:
  what condition produced or blocked it, and what should be cultivated,
  varied, withdrawn, redesigned, redescribed, or stopped next?
```

This contract incorporates the observation-first classification, bounded
interrogation, naturalization, two-axis, measurement, and renewed-attunement
disciplines supplied by the project owner. Those sources are conceptual method
directives only. They cannot become observed AE01 or inherited LGRC evidence.

## 2. Gate partition

Three different questions must remain separate.

### 2.1 Execution validity

Schema, semantic, profile, runtime, reconstruction, digest, path, attempt,
resource, and graph-read-only requirements remain hard gates. Their failure
makes the requested scientific execution incomplete or invalid. It never
becomes a scientific null.

### 2.2 Claim safety

Evidence roles, construction/native separation, claim ceilings, and blocked
relabels remain hard gates. Their failure removes the unsafe claim or report.
Any lower observation that remains independently valid is preserved.

### 2.3 Scientific interpretation

Metric direction, signature strength, causal and withdrawal-control outcomes,
transfer, recurrence, and support dependence are interpreted on ladders. A
control that did not execute leaves the run incomplete. A valid control that
contradicts the expected relation is scientific information and helps classify
what appeared.

No below-threshold result is discarded solely because it missed the target.
No above-threshold result is treated as solved solely because it crossed zero.

## 3. Metric resolution and “narrow”

For each lane, the primary metric sheet freezes:

- candidate and comparator surfaces;
- numerator, denominator, direction, and zero-denominator behavior;
- paired seed/configuration semantics;
- the exact threshold `normalized_margin > 0`; and
- a candidate-blind resolution procedure.

Before candidate execution, matched-null calibration uses seeds `19`, `43`,
`71`, `109`, and `163`. It computes:

```text
delta = max(
  declared measurement resolution,
  maximum absolute matched-null margin over calibration seeds
)
```

The calibration may inspect no candidate outcome. Its record and frozen metric
sheet are retained. Candidate execution remains blocked until `delta` is
frozen. Artifact-only comparisons use `not_applicable`. If resolution is
unknown, the only allowed numeric interpretation is `resolution_unknown`.

For applicable per-seed margins `m_s`:

| Relation | Exact rule | Interpretation |
| --- | --- | --- |
| `robust_aligned` | every `m_s > delta` | Direction is separated from the frozen resolution band; higher rungs still require signatures and controls. |
| `narrow_aligned` | every `m_s > 0`, at least one `> delta`, and at least one `<= delta` | The zero threshold passed, but the relation is resolution-adjacent. |
| `resolution_limited` | every `abs(m_s) <= delta` | The observed relation cannot be separated from frozen null/measurement resolution. |
| `mixed_direction` | margins cross or touch zero and at least one lies outside the band | Seed/configuration dependence or bifurcation requires classification. |
| `narrow_counter` | every `m_s < 0`, at least one `< -delta`, and at least one `>= -delta` | The relation is counter-directional but resolution-adjacent. |
| `robust_counter` | every `m_s < -delta` | A controlled counter-direction is separated from the resolution band. |
| `resolution_unknown` | no frozen `delta` | Robust/narrow language is prohibited and candidate execution is not authorized. |
| `not_applicable` | no live numeric comparison | Preserve the artifact or qualitative classification without invented numbers. |

`threshold_passed` remains the exact fact that every registered live seed is
strictly above zero. It is not the terminal interpretation.

## 4. Orthogonal ladders

Every lane result preserves several axes rather than compressing them into one
score.

### 4.1 Boundary ladder

The lane-specific ladder identifies the lowest cumulative boundary actually
reached. A partial rung is visible. Later rungs cannot erase earlier failures.

### 4.2 Support status

```text
not_applicable
explicit_constructed_support
scaffold_dependent
weakened_support
substituted_support
endogenous_precondition_candidate
native_expression_candidate
unresolved
```

These values describe support relations. They do not establish agency or an
ecology regime.

### 4.3 Classification value

```text
T0 observation tag     local audit value only
T1 reusable class      travels beyond one setup or clarifies a contrast
T2 generative class    produces a new question, boundary, function, or rung
T3 operational class   defines a probe, comparison, or measurement rule
T4 theoretical class   requires revision of the working proposition
```

Only T1 or higher can organize another implementation iteration. A T0 result
may instead trigger class revision, aim redescription, or explicit stop.

## 5. Lane boundary ladders

| Lane | R1 | R2 | R3 | R4 | R5 |
| --- | --- | --- | --- | --- | --- |
| `AE01-L01` | Auditable medium history | Later formation/susceptibility sign | Medium-history-specific function | Withdrawal/source specificity | Carrier/timescale variation |
| `AE01-L02` | One non-private pool | Multiple attributable sources | Combined-history dependence | Mailbox/controller/shuffle controls | Capacity/contributor/access variation |
| `AE01-L03` | Costly attributable deposition | Persistent trace | Trace-dependent route function | Withdrawal/shuffle/false-trace specificity | Geometry/timescale variation |
| `AE01-L04` | Support field and fragile reference | Support-conditioned sign | Specific admissibility beyond allocation | Withdrawal/hidden-allocation specificity | Susceptibility/support variation |
| `AE01-L05` | Maintained selective boundary | Exchange sign | Boundary-specific exchange function | Neutralization/inversion/bypass specificity | Permeability/load/maintenance variation |
| `AE01-L06` | Audited capacity ledger | Circulation/floor sign | Capacity-history-specific eligibility | Disable/shuffle/free-injection/leakage specificity | Topology/timescale variation |
| `AE01-L07` | Source-current surfaces classified | Parent/local relation defined | Future discriminator separates alternatives | Construction/withdrawal role separation | Reusable graph-side demand class |

The machine policy controls the exact rung IDs and names. Markdown controls
their meaning.

## 6. Required result interpretation

Every completed lane result records:

1. raw per-seed relation to the frozen threshold and resolution band;
2. every boundary rung and the highest valid rung;
3. expected, adjacent, and unexpected expressed properties;
4. support status and classification value;
5. a becoming reading;
6. a development reading;
7. strongest valid claim and blocked stronger claims; and
8. one next move with a falsifier.

The terminal classification remains useful for cross-lane synthesis, but it
cannot replace this interpretation record.

## 7. Next moves

Allowed dispositions are:

```text
retain_current_implementation
bounded_local_refinement
alternative_realization
new_boundary_or_naturalization_probe
revise_working_class_or_hypothesis
redescribe_aim
stop_no_reusable_or_generative_value
```

A bounded local refinement must:

- preserve the same causal question;
- target an identified function rather than the margin or proxy itself;
- change one bounded surface;
- preserve the prior result and its classification;
- name a falsifier; and
- advance source specificity, withdrawal resistance, recurrence, transfer,
  broader regime validity, or native expression.

If these conditions do not hold, the change is an alternative realization,
new probe, hypothesis/class revision, or aim redescription. Every such change
requires a new preregistration. It is never the one infrastructure-only retry.

## 8. Non-selection and stopping

N31+ non-selection means no successor was justified. It does not erase atlas
results, failure classes, demands, missing surfaces, or next questions.

Stopping is honest when no reusable or generative value remains, when the aim
must be redescribed, or when the next required condition lies outside AE01.
Stopping cannot smooth over unresolved support, control, or claim debt.

## 9. Phase boundary

Revision 0.24 Phase 1 freezes interpretation infrastructure and candidate-
blind calibration procedure. Passing `P1-GATE` authorizes calibration and lane
registration only. A lane may execute candidate cells only after its metric
sheet has a frozen calibration record and its lane registration confirms the
exact implementation, controls, artifacts, and interpretation references.

This contract opens no lane result, native capacity, ecology regime, or N31+
selection.
