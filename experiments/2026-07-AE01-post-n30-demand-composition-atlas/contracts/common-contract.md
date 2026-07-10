# AE01 Common Machine and Narrative Contract

**Status:** frozen at P1-I3

**Contract version:** `1.0.0`

**Machine shape:** [schemas/ae01-contract.schema.json](schemas/ae01-contract.schema.json)

**Lane registry instance:** [lane-registry.json](lane-registry.json)

**Source admission:** [source-inventory.md](source-inventory.md)

**Evidence effect:** no positive AE01 evidence opened

## 1. Authority split

This Markdown contract governs meaning, evidence roles, cross-record
relationships, debt, controls, compatibility, and claim boundaries.

The JSON Schema Draft 2020-12 bundle governs persisted field shape, required
values, local types, enumerations, and closed extension placement.

Python types and validators may later implement views and semantic checks for
records actually consumed by tooling. They do not become a third schema
authority and must not redefine Markdown meaning or JSON shape.

When layers disagree, the record fails closed:

```text
meaning disagreement       -> contract revision required
shape disagreement         -> schema validation failure
semantic invariant failure -> validator failure
missing implementation     -> unsupported tooling path, not inferred success
```

## 2. Record envelope and versioning

Every persisted AE01 machine record uses:

```json
{
  "schema_version": "1.0.0",
  "record_type": "<declared type>",
  "record": {}
}
```

Core record fields are closed. Reviewed experimental additions belong only
inside an `extensions` object with keys beginning `x_`. Extensions cannot
replace required fields, change core meaning, discharge debt, raise a claim
ceiling, or satisfy a gate.

Compatibility rules:

- exact `schema_version` support is required;
- changing a required field, enum meaning, authority, or semantic invariant
  requires a new schema version;
- optional `x_` extensions are ignorable only when the consuming contract says
  they are non-authoritative;
- unknown core fields, unknown enum values, and missing required fields fail;
- retained evidence keeps its original schema and does not migrate silently.

## 3. Common vocabularies

### 3.1 Evidence roles

| Value | Meaning | Positive-evidence permission |
| --- | --- | --- |
| `conceptual_motivation` | Paper ontology, method, or interpretation | Never |
| `inherited_graph_evidence` | Admitted graph artifact within its original ceiling | Only within source ceiling |
| `ecology_interpretation` | RCAE reading or demand mapping | Demand/interpretation only |
| `constructed_ecology_mechanism` | Explicit RCAE-added mechanism | Constructed behavior and demand only |
| `observed_ae01_result` | Result of a frozen AE01 probe | Only after retained evidence and controls |
| `missing_graph_surface` | Absent or unsuitable graph capability | Gap/demand only |
| `proposed_graph_discriminator` | Suggested future source-current test | Proposal only |

Every pattern card must keep these roles distinct. A field may reference several
roles, but it may not collapse them into one evidence claim.

### 3.2 Evidence-use tiers

```text
exploratory_scratch
registered_probe
retained_evidence
```

Scratch cannot support a report fact, terminal scientific classification, or
gate. A registered probe has frozen inputs, controls, stopping conditions, and
execution mode, but its outputs remain non-evidential until selected and
verified. Retained evidence requires a resolved manifest and successful clean
reconstruction.

Runtime identity, graph read-only behavior, evidence roles, and claim ceilings
apply at every tier.

### 3.3 Catalog layers and maturity

Primary catalog layer:

```text
primitive
building_block
ecology_motif
ecology_regime
```

Maturity:

```text
candidate
observed
controlled
transferable
composable
admitted
```

Layer, maturity, and nativity are independent. The current contract permits
machine representation of every value but does not assign any positive value
to an AE01 lane.

### 3.4 Domain roles

```text
absent
illustrative
test_fixture
interpretation_context
integrated_candidate
```

No value admits a domain package. `integrated_candidate` still requires a
dedicated post-atlas promotion record and evidence.

### 3.5 Applicability

Every common field that does not apply must use an explicit applicability
record:

```text
applicable
not_applicable
unknown
not_tested
blocked
```

`not_applicable` requires a rationale. `unknown`, `not_tested`, and `blocked`
remain missing knowledge and cannot be interpreted as a negative result.

### 3.6 Execution and realization

Execution classes:

```text
artifact_inspection
pygrc_runtime_with_rcae_producer
pygrc_native_runtime
```

Realization classes:

```text
rcae_constructed
pygrc_native_candidate
pygrc_native_supported
```

Artifact inspection is non-runtime. Every requested live mode requires an
available compatible PyGRC binding and a per-run receipt. No fallback or
availability-driven substitution is allowed.

### 3.7 Terminal classifications

```text
supported_bounded_candidate
partial_or_mixed
not_supported
blocked_missing_prerequisite
incomplete_execution
```

`incomplete_execution` is an operational terminal state, not a scientific null.
It contributes no recurrence score and forces N31+ non-selection.

## 4. Source-inventory contract

The machine source inventory must record inventory/experiment IDs, verification
baselines, repository identities, ordered precedence, portable source IDs and
paths, repository revision or file digest, source and evidence roles, evidence
permissions, claim ceilings, blocked relabels, mutable-source historical/current
identities, and refresh conditions.

The P1-I1 Markdown inventory is the accepted source content. Machine
materialization cannot add a stronger source role.

## 5. Lane-registry contract

The registry controls stable lane ID, accepted initial/current names, order,
inclusion state, motivation/source references, rename provenance, maximum
intended result, blocked relabels, and projection consistency.

Stable IDs survive renames. Scope changes require plan change control. P1-I5
must validate the plan, roadmap, and AE01 README against the registry.

## 6. Pattern-card contract

Every lane produces one pattern card with:

- pattern and lane IDs and evidence-use tier;
- primary catalog layer, secondary observations, maturity, domain role,
  placement rationale, transfer boundary, and field applicability;
- parent basin, persistence condition, local differentiations, and medium
  surfaces;
- participant/medium separation or co-constitution account;
- reserve, cost, leakage, maintenance, and coherence-economy declarations;
- perturbation, source attribution, trace dynamics, and later response;
- possible co-response and parent-closure relevance;
- N29/N30 references and separated source/evidence legs;
- construction, requirement, composition, control, execution-class,
  realization-profile, runtime-receipt, debt, and claim references;
- transfer scope, failure modes, and N31+ implication; and
- terminal classification and closure evidence.

A pattern card is an index and synthesis boundary. Referenced records retain
their own authority and cannot be replaced by prose in the card.

## 7. Medium-surface contract

A medium declaration records carrier/access scope, non-private status,
participant boundary, attributable perturbation, surface-change signature,
trace persistence/decay/reinforcement/saturation, later-response dependency,
costs/budgets/leakage/maintenance, causal lineage, parent-basin relevance,
evidence role, controls, claim ceiling, and debt.

A label, mailbox, database, global variable, post-hoc trace, or hidden producer
cannot satisfy the contract without an explicit constructed role and blocked
native claim.

## 8. Requirement-extraction contract

Each requirement records stable ID, affected lanes, `consume`/`extend`/
`introduce` origin, requested catalog layer, precise existing/missing/unsuitable
surface, source tension, evidence roles, future discriminator, counterfactual,
prerequisites, composition leverage, transfer scope, construction/debt path,
claim ceiling, blocked relabels, and ranking eligibility.

The requirement is demand evidence, not proof that the graph surface exists or
will succeed.

## 9. Composition-assessment contract

Every composition records component IDs, ordered dependency, interaction term,
interfaces, carriers, timescales, susceptibility, budgets, leakage, lineage,
state handoff, separable and combined controls, producer/fixture/interference
results, realization references, status, debt, transfer boundary, and claim
ceiling.

Component success never supplies composition success. A missing runtime or
cross-prototype handoff remains explicit debt.

## 10. Debt-record contract

Debt categories are:

```text
producer
medium
naturalization
semantic
transfer
composition
measurement
claim
```

Every debt records a source description, direction, status, blocked
claims/gates, affected lanes, disposition, discharge requirements, and
evidence. An inherited debt also records its predecessor debt ID; a genuinely
local AE01 debt has no invented predecessor. The six canonical N29 debts must
appear as named records in every applicable downstream matrix.

Allowed status is `open`, `carried`, `discharged`, `not_applicable`, or
`superseded`. Only dedicated admitted evidence may discharge debt.

## 11. Claim-boundary contract

A claim-boundary record contains subject ID, claim ceiling, allowed bounded
claims, blocked relabels, false unsafe-claim flags, controlling evidence,
debt/terminal effects, and reopening condition.

Missing flags, unknown blocked relabels, or a ceiling above controlling evidence
fail closed. Narrative reports inherit the machine ceiling.

## 12. Constructed-mechanism contract

Every construction declares mechanism ID, lanes, observed LGRC absence/tension,
necessity, minimality, inputs/outputs/state/scheduling, implementation identity,
counterfactual, withdrawal test, debts, evidence role, claim ceiling, graph
discriminator, and realization profile.

Experimental status alone is insufficient. A construction with no necessity,
counterfactual, withdrawal test, or discriminator fails closed.

## 13. Realization-profile and runtime-binding contracts

A realization profile freezes mechanism/profile IDs and versions, realization
class, required PyGRC identity/capabilities, policy IDs, input/output/state/
artifact schema versions, separate availability/enabled/validated/supported
states, producer/transition discipline, scheduling operations, evidence role,
debts, transfer, claim ceiling, and conformance/replay procedure.

A runtime receipt records requested execution class and failure state. For a
live execution it also records profile ID, observed runtime identity and
capabilities, conformance, before/after state identities, requested operations,
and transition receipts. For `artifact_inspection`, conformance is explicitly
`not_applicable_non_runtime` and live identity/state fields are absent. A
receipt never records a machine-local path. Every live run creates one and
cannot fall back.

## 14. Catalog/domain placement contract

Placement records declare primary layer, secondary observations, maturity,
domain role, domain-specific/transferable responsibilities, applicability,
evidence basis, debts, and blocked promotions.

One primary layer is required. Secondary observations do not raise maturity.
Domain-shaped interpretation does not create a domain package.

## 15. Terminal-classification contract

A terminal record declares lane ID, classification, stopping condition and
whether reached, attempted work, execution status, positive/negative/blocked/
missing signatures, controls, retained evidence, reconstruction, missing
information, debts, claim impact, record completeness, and forced non-selection.

An incomplete execution may close only when its record is complete. It cannot
be scored as recurrence, positive evidence, or refutation.

## 16. N31+ ranking and non-selection contract

Only eligible post-synthesis candidates may be scored. The record embeds the
fixed D-029 dimension, group, critical-dimension, overall, tie, and sensitivity
policy. Every candidate records requirement/lane references, origin, the eight
named eligibility gates, scoring status, independent qualitative rationale and
prior, numeric/qualitative disagreement, selection/non-selection, and missing
information. Every scored candidate additionally records all ten 0–3 scores,
group/overall totals, individual threshold results, tie results, and four
sensitivity profiles. Ineligible candidates are explicitly unscored. A
selected result must carry the selected candidate ID; non-selection must carry
reasons and an applicable information-gathering step.

Scoring cannot occur before synthesis. Intuition cannot silently override a
gate, score, tie, sensitivity result, or required non-selection.

## 17. Artifact-manifest and profile-resolution contract

Every retained artifact entry resolves artifact ID/path, producing command and
working directory, environment/dependency/source/configuration identities,
input digests/seeds, execution and realization class, artifact
kind/schema/digests/size, resource envelope, verification command/status,
tracked-versus-reconstructable retention mode, size-review disposition,
evidence tier, and claim dependencies. The manifest also records complete-set
size and its retention review.

Shared profiles may remove repeated authoring, but pre-retention
materialization must embed the resolved shared and realization profiles and
expose every D-027 value. Scratch and transient registered output cannot
support a gate. Omitted large artifacts use `reconstructable_local_only` and
require the same verified entry as tracked selected evidence.

## 18. Human-readable report-projection contract

Every report declares ID, `generated_projection` or
`assembled_interpretation` mode, controlling machine sources/facts, authored
sections, claim ceiling, blocked statements, deterministic assembly profile,
output path/digests, and consistency status.

Machine facts remain authoritative. Authored interpretation cannot invent
evidence, alter a terminal result, discharge debt, change a score, or raise a
claim ceiling.

## 19. Cross-record semantic invariants

P1-I5 validators must enforce at least:

1. Stable IDs are unique and references resolve.
2. Portable paths contain no checkout-specific or machine-local location.
3. Conceptual sources cannot occupy runtime or observed-result roles.
4. Scratch and unretained output cannot support facts or gates.
5. Constructed mechanisms never become native by availability or naming.
6. Live execution has an explicit compatible profile and per-run receipt.
7. Claim ceilings do not exceed controlling sources and terminal state.
8. Unsafe flags are present and false.
9. Debt discharge cites dedicated admitted evidence.
10. Component success cannot satisfy composition success.
11. `incomplete_execution` forces non-selection and contributes no score.
12. Ranking starts only after all terminal records and synthesis.
13. Machine facts and report projections agree.
14. Lane registry and narrative lane projections agree.
15. A retained-artifact manifest resolves every D-027 field.

## 20. P1-I3 claim boundary

This contract freezes record meaning and shape only. Schema completeness,
registry consistency, or a valid empty record does not support a lane result,
composition, catalog admission, domain package, or N31+ candidate.

`AE01-C0` remains the highest assigned rung. `AE01-C1` and `AE01-C2` remain
unassigned until the full Phase 1 gate and R2 review.
