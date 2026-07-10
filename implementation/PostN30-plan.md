# Post-N30 Project Architecture, Atlas, Specification, and Implementation Plan

**Status:** active master program directive

**Plan revision:** 0.24

**Date:** 2026-07-10

**Scope:** repository architecture, directive hierarchy, Post-N30 atlas program,
LGRC consumption boundary, specification promotion, and implementation sequence

**Decision rule:** statements marked **Accepted** are active project decisions;
statements marked **Proposed** or **Deferred** are not yet binding

**Execution tracking:** [Post-N30 master checklist](PostN30-checklist.md)

## 1. Purpose

This document is the cross-cutting implementation plan for moving
RC-Agentic-Ecology from a conceptual paper repository into an evidence-backed
experiment, specification, and implementation workspace.

Its immediate target is the **Post-N30 Agentic-Ecology Demand and Composition
Atlas**, provisionally named `AE01`. The atlas consumes the graph project's N29
and N30 handoffs, interrogates several ecology-side shared-medium patterns, and
extracts the recurring missing substrate requirements that may justify a later
N31+ LGRC experiment.

This document does not contain atlas results and does not select N31. It defines
the structure and gates through which those results may be produced.

The central separation is:

```text
experiments discover and classify
specifications define admitted contracts
source code implements reusable abstractions
tests and telemetry verify conformance and replay
```

Source code is not evidence by itself. A conceptual mapping is not an admitted
primitive. A successful component is not a successful composition. An ecology
interpretation does not promote an LGRC claim.

## 2. Placement and document role

**Decision D-001 — Accepted.** This document belongs in `implementation/`.

Rationale:

- it governs several repository surfaces rather than one experiment;
- it defines sequencing, promotion gates, and architecture boundaries;
- it is not an experiment roadmap or an evidence artifact;
- it is not an admitted behavioral specification;
- it is not a conceptual paper.

The future Post-N30 atlas roadmap belongs under `experiments/`. Contracts
admitted after experiment closeout belong under `specs/`. Reusable executable
forms belong under `src/`.

This file is the active umbrella directive for the full Post-N30 program. Phase
plans, checklists, experiment contracts, closeouts, specifications, and
implementation records may elaborate individual parts of the program, but they
must cite this plan and may not silently redefine it. Phase 0 is the first
milestone governed by this document, not the document's terminal scope.

The companion checklist is the authoritative progress view for this plan. It
may refine task ordering and expose newly required work, but it may not change
accepted architecture or claim boundaries without a recorded plan revision.

## 3. Normative language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are
normative within this plan.

- **MUST** identifies a requirement needed to preserve project boundaries,
  evidence discipline, portability, or claim safety.
- **SHOULD** identifies the preferred design when no documented reason requires
  deviation.
- **MAY** identifies an allowed but optional choice.

Documented deviations are permitted when they preserve the relevant claim and
debt boundaries. Deviation does not itself discharge producer, medium,
naturalization, semantic, transfer, composition, measurement, or claim debt.

## 4. Directive and source-of-truth hierarchy

**Decision D-002 — Accepted.** Project directives are separated by role rather
than collected into one undifferentiated design document.

```text
papers
    define target ontology, vocabulary, and conceptual posture

external graph experiment handoffs
    define what LGRC/GRC evidence may actually be consumed

project implementation directives
    define repository architecture, sequencing, and cross-cutting boundaries

experiment roadmaps
    define research questions, lanes, phases, and expected artifacts

experiment contracts
    define local evidence gates, controls, debt fields, and claim ceilings

experiment reports and closeouts
    classify what was observed and what may be handed forward

specifications
    define reusable contracts admitted by evidence or explicitly marked conceptual

source code
    enacts contracts without increasing their claim level

tests and telemetry
    verify conformance, determinism, replay, controls, and boundary preservation
```

Conflict rules:

1. Implementation MUST NOT override the conceptual claim boundaries in the
   papers.
2. Conceptual papers MUST NOT be consumed as runtime evidence.
3. Later graph closeouts and handoffs control the current evidence status of
   earlier graph experiments.
4. Experiment-local positive claims MUST be supported by the experiment's own
   contracts, artifacts, controls, and closeout.
5. A specification MUST NOT promote a stronger claim than its source evidence.
6. Source placement or API naming MUST NOT be treated as evidence of admission,
   nativity, agency, coordination, or ecology regime.

Primary conceptual sources for this plan are:

- `papers/2026-06-FromStateToBecoming.md`
- `papers/2026-06-RC-AgenticEcology.md`
- `papers/2026-06-TheSharedMedium.md`
- `papers/2026-06-SharedMediumCoordination-EngineeringSpec.md`

Primary evidence and continuation sources are maintained in the graph project,
especially the N29 closeout, N30 closeout, and active N30+ shared-medium ecology
handoff. All repository records MUST use portable relative identifiers rather
than checkout-specific paths.

## 5. Project boundary

**Decision D-003 — Accepted.** The graph project and this project have
complementary ownership.

```text
graph-reflexive-coherence owns:
    GRC/LGRC runtime implementation
    substrate-level primitives and native mechanisms
    source-current evidence
    replay/control validation
    primitive and building-block admission experiments
    graph-side claim ceilings and handoffs

reflexive-coherence-agentic-ecology owns:
    ecology-side demand discovery
    shared-medium composition
    domain-shaped motif probes
    ecology regime candidates
    producer and medium debt carried by compositions
    downward discovery of missing LGRC distinctions
    portable bridges that consume admitted LGRC surfaces
```

The graph project MUST be treated as read-only by this project. Code and
records here MUST NOT depend on a particular sibling checkout location. The
bridge MUST consume public Python surfaces, installed packages, or portable
artifacts rather than traversing another repository's internal directory tree.

## 6. Accepted architecture decisions

The following decisions are active unless superseded through the change-control
process in Section 17.

| ID | Status | Decision |
| --- | --- | --- |
| D-001 | Accepted | This cross-cutting master program plan remains under `implementation/`. |
| D-002 | Accepted | Ontology, evidence, experiment contracts, specifications, implementation, and verification remain distinct directive layers. |
| D-003 | Accepted | The graph project owns LGRC substrate evidence; this project owns ecology-side composition and demand discovery. |
| D-004 | Accepted | The Post-N30 atlas begins as an experiment program, not as a stable specification or runtime implementation. |
| D-005 | Accepted | The first local experiment is provisionally `AE01`; it consumes N30 but does not become graph experiment N31. |
| D-006 | Accepted | Catalog layers remain `primitive -> building block -> ecology motif -> ecology regime`. Domain examples are a separate organizational dimension. |
| D-007 | Accepted | AE01 is one bounded atlas experiment with multiple comparable lanes, not a collection of unrelated experiments. |
| D-008 | Accepted | N31 selection is an allowed closeout result, not a required result. |
| D-009 | Accepted | Experiment-local contracts precede positive atlas conclusions. Successful contracts may be distilled into canonical specifications after closeout. |
| D-010 | Accepted | Reusable source items carry explicit maturity, evidence, debt, transfer, and claim metadata. Placement in `src/` does not imply admission or nativity. |
| D-011 | Accepted | LGRC integration is isolated behind a validated, read-only bridge that preserves provenance and claim status. |
| D-012 | Accepted, qualified by D-028 | Early stable or reusable implementation is limited to infrastructure required to execute and validate AE01. Bounded constructed mechanisms needed for AE01 demand discovery are permitted under D-028 without admission or nativity. |
| D-013 | Accepted | Raw conversation is decision provenance, not normative project authority. This plan is the maintained directive extracted from it. |
| D-014 | Accepted | Only the minimum structure required by the current phase should be scaffolded; speculative empty architecture is deferred. |
| D-015 | Accepted | The repository tree in Section 7 is the target structure, introduced incrementally rather than scaffolded all at once. |
| D-016 | Accepted | Catalog items follow the explicit demand-to-contract-to-evidence-to-specification-to-implementation lifecycle in Section 8. |
| D-017 | Accepted | Canonical specifications are operational contracts and must not become another conceptual-paper surface. |
| D-018 | Accepted | LGRC consumption is isolated behind the provenance-preserving adapter boundary in Section 10. |
| D-019 | Accepted | AE01 is an atlas-building experiment with specification-like local contracts, not itself a canonical specification. |
| D-020 | Accepted | AE01 begins with the seven comparable, independently executable shared-medium lanes listed in Section 11.3; only cross-lane synthesis requires every lane to close. |
| D-021 | Accepted | AE01 uses the C0-C6 acceptance ladder in Section 11.7, subject to contract-freeze review. |
| D-022 | Accepted, qualified by D-028 | Pre-closeout stable or reusable `src/` implementation remains limited to reproducibility, validation, provenance, and bridge infrastructure. Experiment-local constructed probes and explicitly experimental shared surfaces required by AE01 are permitted under D-028 and remain non-admitted. |
| D-023 | Accepted | Maintained decision records, not raw dialogue, are the normative way conversation-derived directives enter the repository. |
| D-024 | Accepted | AE01 carries all six unresolved N29 debts through source inventory, lane classification, synthesis, promotion, and closeout unless dedicated discharge evidence exists. |
| D-025 | Accepted | Native AE artifacts use the PyGRC-compatible canonical JSON and SHA-256 digest convention defined in the O-004 disposition. RFC 8785/JCS is deferred until a concrete non-Python LGRC or AE artifact consumer justifies an artifact-library migration. |
| D-026 | Accepted | AE01 uses the divided-authority dual schema representation defined in the O-005 disposition: Markdown contracts govern meaning, JSON Schema governs persisted shape, and Python types and validators implement runtime and semantic constraints. |
| D-027 | Accepted | AE01 uses the selected-output and mandatory artifact-reconstruction policy defined in the O-006 disposition. Uncommitted or oversized artifacts remain eligible evidence only when their complete portable reconstruction contract has passed verification. |
| D-028 | Accepted | The graph/agentic-ecology relation is a bidirectional spiral. AE01 prefers naturalized LGRC surfaces but may construct explicitly bounded ecology-side mechanisms to expose missing patterns, without relabeling them as native LGRC evidence or silently discharging debt. |
| D-029 | Accepted | AE01 applies the gated N31+ ranking and explicit non-selection policy defined in the O-009 disposition. Candidates may consume, extend, or introduce LGRC distinctions; current absence from graph implementation is not disqualifying. |
| D-030 | Accepted | AE01 reports use the two-mode authority and assembly policy defined in the O-010 disposition: generated machine facts remain controlling while explicitly authored Markdown may supply bounded interpretation. |
| D-031 | Accepted | The Python import root is `rc_agentic_ecology`. It identifies project ownership only and carries no admission, nativity, public API, compatibility, distribution, or release claim. |
| D-032 | Accepted deferral | Python distribution name and software version remain unset until P4-I1 or an earlier installable-package requirement. Repository publication version `0.1` is not a Python distribution release. |
| D-033 | Accepted | LGRC integration follows the strict dual-surface policy in the O-003 disposition: artifact inspection is non-runtime; all live execution requires a compatible local PyGRC runtime; constructed and native bindings never substitute silently. |
| D-034 | Accepted partial resolution and deferral | AE01 freezes replay-oriented mechanism contracts and explicit realization profiles rather than promising a general stable producer/plugin API. The graph/PyGRC repository remains strictly read-only from RCAE; any native implementation is separately authorized and performed under graph-project authority. |
| D-035 | Accepted partial resolution and deferral | Domain-package creation is admission-driven. Conceptual examples and experiment-local domain fixtures do not preselect reusable packages; the inventory beyond each explicitly promoted domain remains deferred. |
| D-036 | Accepted | The known tensions among constructed exploration, implementation restraint, reproducibility, local PyGRC resolution, deferred packaging, domain placement, and bounded lane closure are operationalized as explicit Phase 1 contract and tooling obligations without reopening P0-I2. |
| D-037 | Accepted | Evidence ceremony is graduated by evidential use, while runtime safety, graph read-only behavior, evidence-class separation, and claim ceilings remain fixed. Shared profiles and generated receipts SHOULD remove repeated manual entry; N31+ scoring remains a synthesis gate accompanied by independent qualitative rationale. |
| D-038 | Accepted | Frozen scientific thresholds are reference surfaces and highest-rung anchors, not universal accept/reject gates. Every valid lane result preserves machine-derived threshold relation, lowest valid boundary rung, support status, expected/adjacent/unexpected properties, separate becoming/development readings, claim ceiling, and a falsifiable next move. Hard execution-validity and claim-safety gates remain fail-closed. |

## 7. Target repository structure

**Decision D-015 — Accepted as target structure, not immediate scaffold.**

```text
papers/
    conceptual ontology and transition arguments

experiments/
    README.md
    Post-N30-AgenticEcology-DemandCompositionAtlasRoadmap.md
    Post-N30-AgenticEcology-Handoff.md

    2026-07-AE01-post-n30-demand-composition-atlas/
        README.md
        hypotheses/
        configs/
        contracts/
        implementation/
        scripts/
        outputs/
        reports/

specs/
    README.md

    catalog/
        <promoted catalog contracts>

    shared_medium/
        <promoted shared-medium contracts>

    bridge/
        <promoted LGRC consumption and provenance contracts>

    schemas/
        machine-readable schemas derived from admitted contracts

implementation/
    cross-cutting architecture, phase plans, checklists, decisions, and handoffs

src/
    rc_agentic_ecology/
        core/
        catalog/
        bridge/
            lgrc/
        primitives/
        building_blocks/
        motifs/
        regimes/
        domains/
            <promoted_domain>/
        telemetry/

tests/
    unit/
    contract/
    integration/
    replay/

examples/
    small explanatory uses of admitted or explicitly candidate components
```

Directory roles:

- `papers/` explains the ontology and method; it does not supply runtime
  evidence.
- `experiments/` contains questions, hypotheses, contracts, reconstruction
  paths, outputs, reports, controls, and closeouts.
- `specs/` contains operational contracts, not additional conceptual essays.
- `implementation/` contains plans and architecture decisions, not experiment
  evidence.
- `src/` contains reusable executable abstractions and bridge code.
- `tests/` verifies code and contract behavior; passing tests do not by
  themselves promote research claims.
- `examples/` explains use; examples are not evidence unless explicitly
  consumed by an experiment contract.

The hierarchy includes `motifs/` because motifs are a distinct N30+ catalog
layer. `domains/` contains ant, forest, farm, swarm, or other domain
compositions. A domain example is not automatically a motif or regime.

The `specs/` entries above are category placeholders, not a commitment to
particular filenames or a requirement to populate every category. Canonical
spec names and files MUST be determined by the Phase 3 promotion queue and
created only for admitted or explicitly conceptual contracts.

## 8. Catalog and promotion lifecycle

**Decision D-016 — Accepted.** Every promoted item follows an explicit
lifecycle.

```text
paper vocabulary or graph handoff
    -> ecology demand
    -> candidate contract
    -> candidate implementation or reconstruction probe
    -> replay and controls
    -> classified result
    -> admitted specification
    -> reusable source abstraction
    -> transfer and composition review
```

Minimum maturity vocabulary:

```text
candidate
observed
controlled
transferable
composable
admitted
```

Maturity and nativity are different axes. An item may be a controlled or
composable producer-mediated candidate without being native. An admitted
ecology abstraction may consume an artifact-level LGRC result without
retroactively promoting that result.

Every catalog item MUST expose or reference:

```text
catalog layer
maturity
source evidence and digests
runtime or reconstruction status
transfer scope
composition interface
producer debt
medium debt
naturalization debt
semantic debt
composition debt
measurement and claim debt where applicable
claim ceiling
blocked relabels
```

Promotion gates:

| Transition | Minimum gate |
| --- | --- |
| Demand -> candidate contract | Target ontology, carrier, missing distinction, and blocked claims are explicit. |
| Candidate contract -> experiment probe | Inputs, positive signatures, controls, debt fields, and failure conditions are frozen. |
| Probe -> classified result | Required artifacts exist, reconstruction is reproducible, controls fail closed, and claim guards pass. |
| Classified result -> specification | Reusable boundary, evidence envelope, transfer scope, and conformance requirements are stated. |
| Specification -> stable source abstraction | Contract tests pass and implementation does not exceed the specification's claim level. |
| Component -> composition | Shared carrier, compatible timescale, non-conflicting budget, visible interaction, combined controls, and no hidden producer bridge are demonstrated or explicitly marked unresolved. |

## 9. Specification discipline

**Decision D-017 — Accepted.** `specs/` MUST not become another paper
directory.

A specification SHOULD define:

```text
purpose and catalog layer
required inputs
carrier and surface semantics
state and event invariants
composition inputs and outputs
budget and lineage rules
positive signatures
mandatory controls
failure modes
debt fields
transfer scope
claim ceiling
blocked relabels
conformance tests
source evidence
```

Experiment-local contracts MAY contain proposed shapes. They remain historical
experiment records after closeout. A canonical spec is a distilled reusable
contract and MUST cite its source experiment and evidence classification.

## 10. LGRC bridge boundary

**Decision D-018 — Accepted.** LGRC consumption is isolated behind a narrow
adapter boundary.

```text
LGRC public runtime, snapshot, telemetry, or selected experiment artifact
    -> validated read-only adapter
    -> substrate-neutral ecology view
    -> primitive/building-block composition
    -> motif or regime probe
```

The bridge MUST preserve:

- source model family and schema version;
- source artifact and configuration digests;
- event, packet, topology, and identity lineage where present;
- runtime, replay, and transfer scope;
- source claim ceiling and blocked relabels;
- producer, medium, naturalization, semantic, and composition debt;
- whether each surface is native, source-current, inherited, constructed, or
  report-only;
- the distinction between source evidence and ecology-side interpretation.

The bridge MUST NOT:

- mutate the graph project;
- import experiment scripts as stable APIs;
- depend on checkout-specific paths;
- silently treat missing fields as positive evidence;
- convert conceptual labels into runtime evidence;
- retroactively upgrade producer-mediated records when later native support
  appears.

Domain code SHOULD consume substrate-neutral bridge protocols rather than deep
`pygrc` implementation modules. D-033 fixes the dependency mode and D-034 fixes
the replay-compatibility floor: live execution resolves a compatible PyGRC
runtime locally, while artifact inspection remains non-runtime. P1-I5 selects
only the repository-local tooling bootstrap needed by frozen contracts. It MUST
reopen O-002 before requiring installable-package metadata and MUST preserve the
read-only graph boundary in every mode.

### 10.1 Bidirectional spiral and constructed exploration

**Decision D-028 — Accepted.** Naturalization is a preferred maturity direction,
not an exploration prerequisite. The relationship between the two projects is
bidirectional:

```text
graph evidence and runtime surfaces
    -> agentic-ecology consumption and composition
    -> tension, failure, or missing pattern
    -> ecology-side constructed probe or provisional mechanism
    -> precisely extracted substrate demand
    -> proposed future LGRC discriminator and experiment
    -> graph-side implementation and evidence
    -> renewed ecology-side consumption
```

AE01 MAY design and execute an explicitly constructed, producer-mediated, or
ecology-local mechanism when the applicable graph surface is absent or creates
a composition tension. Such a result is valid only within its declared role as
demand-discovery, composition, or constructed-probe evidence. It MUST NOT be
consumed as native LGRC evidence, proof that the graph substrate already
supports the pattern, canonical primitive admission, or discharge of producer,
naturalization, transfer, or composition debt.

Every lane that constructs or proposes a missing surface MUST distinguish:

```text
inherited or source-current graph evidence
ecology-side interpretation
constructed ecology-side mechanism
missing or unsuitable substrate surface
proposed future LGRC discriminator
```

Constructed mechanisms belong under the experiment by default. A surface used
across lanes MAY be shared through `src/` only with explicit experimental and
constructed status, maturity, evidence class, debt, transfer scope, and claim
ceiling. Neither location nor successful execution admits it as a reusable
primitive or native LGRC capability.

A constructed probe MAY demonstrate that its declared construction behaves as
specified, that a composition becomes possible or fails in a particular way,
and that a missing pattern is useful to formulate. It MUST preserve the active
counterfactual question of whether an LGRC-native realization can reproduce the
relevant distinction under graph-side source-current evidence and controls.

The resulting tension, missing pattern, control requirements, and proposed
discriminator form an ecology-to-graph handoff. This repository remains
read-only with respect to the graph project; the graph project retains authority
over LGRC implementation, experiment naming, and substrate-evidence claims.
Future graph results return through the bridge and may support, revise,
supersede, or reject the constructed ecology-side account.

## 11. AE01 atlas experiment

### 11.1 Role

**Decision D-019 — Accepted.** AE01 is an experiment roadmap and atlas-building
program with specification-like local contracts. It is not itself a canonical
specification.

Core question:

```text
Given the bounded N30 minimal shared-medium participation result and the N29
ecology bridge, which ecology-side shared-medium demand patterns can be mapped
without overconsumption, what composition requirements recur across them, and
which missing substrate distinction is the strongest candidate for a later
N31+ LGRC experiment?
```

### 11.2 Required source posture

AE01 MUST consume:

- the four conceptual papers listed in Section 4 as ontology and method;
- N29 as the capability/debt/prototype bridge;
- N30 as bounded minimal shared-medium participation and trace-mediated
  eligibility evidence;
- the active N30+ handoff as the continuation rule.

Conceptual sources MUST NOT satisfy runtime evidence gates. N29 component
success MUST NOT become composition success. N30 MUST NOT be consumed as
shared-medium coordination, agency, parent-basin modulation, or ecology regime.
`agentic_ecology_demand_as_substrate_evidence` MUST remain false.

The Phase 1 source inventory MUST record the N29 closeout output digest:

```text
fa21662f0a69d582bfe574311110f2610a21e6e4e352991823ce47280e0e8ff5
```

It MUST also record and validate all ten load-bearing `source_artifacts` from
the N29 closeout, including each source ID, portable path, output digest, file
SHA-256, status, and acceptance state. The checklist contains the canonical
expected values to be verified during `P1-I1`.

The Phase 1 source inventory MUST symmetrically record the N30 closeout output
digest:

```text
7971163b1d7bd4027f5375270cfb2445cfe4698a8869b28e26f9273d0a5b5af6
```

This digest identifies the accepted N30-C6 post-N30 spiral-ready minimal
shared-medium participation closeout. Recording it does not widen N30's claim
ceiling.

#### N29 debt carry-forward

**Decision D-024 — Accepted.** AE01 inherits all six unresolved N29 debts. No
lane, composition, adapter, specification, or implementation may silently
discharge them.

| N29 debt | Direction | Blocks | AE01 carry-forward rule |
| --- | --- | --- | --- |
| `composed_ecology_runtime_harness_missing` | Outbound ecology | Ecology success and native ecology | AE01 may define or rank the missing harness; it cannot claim an executed composition until a dedicated runtime probe closes it. |
| `producer_mediated_cross_prototype_handoff` | Both | Native composition and native support | Every A/B/C/D handoff must remain producer-mediated or missing until source-backed discharge evidence exists. |
| `medium_debt_and_nonzero_leakage_policy` | Both | Native shared-medium coordination | Every relevant lane must retain leakage accounting and medium debt; zero or acceptable leakage cannot be assumed. |
| `ap4_ap5_gap_propagation` | Inbound N30+ | Native route-selection or proxy-target closure | AP4/AP5 NAT4 gaps remain explicit blockers and cannot close by inheritance or composition. |
| `resource_economy_cooperation_exploitation_semantics` | Outbound ecology | Resource economy and cooperation/exploitation | Capacity, nursery, pool, and circulation lanes must use substrate-visible support language and block semantic promotion. |
| `deviation_nativity_discharge` | Both | Retroactive native upgrade and producer removal without rerun | Contract deviation or later core nativity does not discharge old debt; native promotion requires a rerun or source-backed discharge record. |

The source inventory, lane records, debt matrix, promotion queue, and AE01
closeout MUST each carry an explicit disposition for these six debts.

### 11.3 Atlas lanes

**Decision D-020 — Accepted as initial scope.** AE01 begins as one experiment
with seven comparable lanes that may execute independently after the Phase 1
contract freeze:

1. `AE01-L01` — minimal shared-medium niche formation;
2. `AE01-L02` — shared-pool co-conditioning;
3. `AE01-L03` — trail or stigmergic field;
4. `AE01-L04` — nursery or support field;
5. `AE01-L05` — boundary-conditioned exchange;
6. `AE01-L06` — capacity circulation;
7. `AE01-L07` — parent-basin modulation demand and missing-surface
   classification.

Lane 1 is motivated by N30 trace-conditioned eligibility, N29 Prototype B's
boundary/shared-medium unit, N29 Prototype C's susceptibility/re-entry surface,
and the ecology-side question of how changed medium conditions alter later
formation, persistence, re-entry, cost, or susceptibility. `Niche` is an
ecology demand interpretation, not an N30-supported label.

Lane 4 is motivated by the N29 nursery-demand coverage/debt row, N29 Prototype
D's generative/extractive medium-reshaping surface, N22-style susceptibility
context, N28-style generative/extractive discipline, and the N30+
shared-support-redistribution direction. It is a support-field demand, not
evidence of semantic care, cooperation, reproduction, or generative agency.

Lane 7 deliberately interrogates a relation rung blocked by N30. Its expected
safe result is a demand and missing-surface classification. It MUST NOT be
designed to obtain positive M3/M4 evidence from N30 or conceptual sources.

All seven lanes MAY run in parallel after `P1-GATE` because none may consume
another lane's conclusion as input. Cross-lane synthesis begins only after all
required lane exit gates pass.

Lanes MAY be renamed during contract freeze if the new name improves ontology
or avoids a premature claim. A lane MUST NOT be removed merely because it fails
to support a positive candidate; failed or blocked lanes remain demand evidence.
P1-I2 MUST assign a stable lane ID to every accepted initial lane. P1-I3 MUST
freeze one machine-readable lane registry controlling stable IDs, current
display names, order, inclusion state, initial-name lineage, and rename
rationale. IDs survive renames. The roadmap and AE01 README remain independently
navigable narrative projections, but P1-I5 MUST validate them against the
registry and fail on missing, duplicate, stale, or reordered lane identities.
The plan preserves the accepted initial scope and must record any scope change
through normal change control.

Each lane contract MUST freeze finite terminal classifications and stopping
conditions. A negative, absent, producer-carried, or missing-surface result can
close a lane only after its required record, controls, and reconstruction pass.
An incomplete or unavailable execution is recorded as such and MUST NOT be
relabeled as a negative scientific result or kept open indefinitely.

### 11.4 Common lane contract

Every lane MUST record:

```text
pattern identifier
primary catalog layer and secondary observations
domain role, domain-specific versus transferable boundary, and placement rationale
field applicability status and rationale wherever a common field is not applicable
parent basin and persistence condition
local differentiations or participant carriers
shared medium and declared surfaces
participant/medium separation or co-constitution argument
coherence economy, reserve, costs, leakage, and maintenance
perturbation and attributable source
trace persistence, decay, reinforcement, and saturation
susceptibility and later continuation effect
possible co-response or parent-basin relevance
effect on parent closure
N29 prototypes and demand rows consumed
N30-supported legs
ecology-extrapolated legs
constructed ecology-side mechanisms and their evidence class
constructed-mechanism necessity, minimality, counterfactual, and withdrawal declaration
missing or unsuitable graph surfaces
proposed future LGRC discriminators
new substrate requirements
composition inputs, outputs, and interference risks
controls and withdrawal tests
execution class and runtime-binding/realization-profile receipt, if execution is requested
primary metric sheet, candidate-blind resolution calibration, and per-seed threshold relation
lane boundary ladder and highest valid rung
expected, adjacent, and unexpected expressed properties
support status and classification-value rung
separate becoming and development readings
falsifiable next move and local-optimization guard where applicable
all applicable debts
transfer scope
claim ceiling and blocked relabels
candidate N31+ implication, if any
terminal classification, stopping condition, and closure evidence
```

A constructed-mechanism declaration MUST identify the observed LGRC absence or
composition tension, justify the smallest added mechanism, define inputs and
outputs, state the counterfactual and scaffold-withdrawal test, preserve
producer and naturalization debt, cap its claims, and name the graph-side
discriminator it is meant to expose. Missing or weak justification fails the
construction closed; experimental status is not by itself sufficient.

Any requested live execution MUST reference a runtime-binding receipt and
realization profile that record the required and observed PyGRC identities,
capabilities, policies, schemas, execution class, conformance result, and
before/after state identities without recording a machine-local path. Artifact
inspection records that no live runtime was requested and cannot satisfy a live
execution requirement.

### 11.5 Required controls

At minimum, AE01 contracts MUST fail closed against:

```text
conceptual-paper-as-runtime-evidence
N30-as-coordination or ecology relabel
N29-component-success-as-composition-success
pre-given closed agent plus passive environment relabel
message bus or global variable disguised as shared medium
surface annotation without functional dependence
co-occurrence treated as composition
hidden producer or cross-prototype handoff
free trace, free memory, or unaccounted activity
absent parent-basin context
participant/medium boundary confusion
semantic communication, cooperation, intention, or agency promotion
constructed ecology mechanism relabeled as native LGRC evidence
fixed N31 selection before cross-lane synthesis
```

Additional lane-specific controls SHOULD include medium freezing, trace
shuffling, decay manipulation, susceptibility inversion, false trace injection,
parent-basin separation, scaffold withdrawal, budget controls, and transfer
variants where the lane makes those controls relevant.

### 11.6 Atlas outputs

Each lane SHOULD produce a machine-readable artifact and a human-readable
report. AE01-level outputs MUST include:

- source inventory and consumption boundaries;
- pattern-card collection;
- N29/N30 traceability matrix;
- N30 overconsumption guard;
- demand and missing-surface matrix;
- composition/dependency graph;
- cross-pattern recurring-requirement matrix;
- composition-interference and failure ledger;
- debt matrix;
- candidate N31+ ranking or explicit non-selection;
- specification-promotion queue;
- implementation queue;
- closeout and graph/ecology spiral handoff.

### 11.7 Acceptance ladder

**Decision D-021 — Accepted as initial ladder.**

```text
AE01-C0 = initialized, no atlas claim
AE01-C1 = source inventory and consumption boundaries accepted
AE01-C2 = lane schemas, controls, claim guards, metric sheets, calibration procedure, and developmental interpretation frozen
AE01-C3 = all required lane records classified
AE01-C4 = cross-lane requirements and composition dependencies synthesized
AE01-C5 = controls, debt, failure, and non-selection gates passed
AE01-C6 = atlas closeout and N31+ handoff complete
```

`AE01-C6` is an atlas and handoff rung. It does not mean an ecology runtime,
native shared-medium coordination, agency, an ecology motif, or an ecology
regime has been demonstrated.

### 11.8 N31+ selection rule

N31+ MUST NOT be selected by recurrence count alone. Ranking SHOULD consider:

```text
cross-lane recurrence
prerequisite centrality
current evidence gap
ability to define one bounded source-current discriminator
control feasibility
composition leverage
transfer value
potential to discharge producer or medium debt
claim-inflation risk
implementation and evidence cost
```

AE01 MAY close without selecting N31 when no candidate meets the selection
gate.

## 12. Phase plan

### Phase 0 — Project architecture and decision freeze

Purpose:

```text
turn the current design discussion into explicit, reviewable directives
freeze only decisions that block AE01
defer reversible or premature implementation choices
```

Required outputs:

- this active master program plan;
- the master program checklist with a finite Phase 0 decision section;
- a boundary/open-decision ledger if this document becomes too broad for
  effective review;
- accepted minimum repository structure;
- accepted AE01 naming and scope;
- accepted directive and change-control process.

Exit gate:

```text
all AE01-blocking architecture decisions are accepted or explicitly deferred
with a safe default
```

### Phase 1 — Atlas contract freeze

Required outputs:

- Post-N30 atlas roadmap;
- AE01 README;
- source inventory contract;
- hypotheses;
- common pattern-card contract;
- requirement-extraction contract;
- composition-assessment contract;
- claim-boundary contract;
- constructed-mechanism declaration contract;
- runtime-binding and realization-profile contract;
- catalog/domain placement and field-applicability rules;
- lane terminal-classification and stopping contract;
- metric-sheet and candidate-blind resolution contract;
- developmental-interpretation and lane boundary-ladder contract;
- implementation plan and checklist;
- expected artifact inventory.

No positive atlas conclusions may be assigned in this phase.

Exit gate:

```text
sources, lanes, schemas, controls, evidence classes, debt fields,
acceptance rungs, metric/calibration semantics, developmental interpretation,
and stopping conditions are frozen
```

### Phase 2 — Atlas execution

Required work:

- run and retain candidate-blind primary-metric calibration for each lane;
- freeze each lane's resolution band and complete lane registration before
  candidate execution;
- populate each lane from declared sources;
- generate reproducible artifacts and reports;
- distinguish N30 grounding from ecology extrapolation;
- classify missing requirements and failures;
- classify threshold relation, boundary rung, support status, unexpected
  properties, and two-axis developmental meaning before terminal synthesis;
- run contract, provenance, digest, and claim-boundary validation.

Cross-lane synthesis MUST occur only after every required lane has been
classified through the common contract.

Exit gate:

```text
all required lane records exist, validate, and preserve blocked claims
```

### Phase 3 — Closeout and promotion

Required outputs:

- final demand and composition atlas;
- cross-lane synthesis;
- N31+ ranking or non-selection decision;
- specification-promotion queue;
- implementation queue;
- closeout classification;
- bidirectional graph/ecology handoff.

Exit gate:

```text
AE01-C6 is supported without unsafe claim promotion
```

### Phase 4 — Specification and reusable implementation

Only admitted or explicitly candidate results with clear contracts proceed.

The Phase 4 iteration detail is a provisional implementation envelope, not a
preselected backlog. It MUST be revised by the Phase 3 promotion queue before
Phase 4 execution. No Phase 4 component, motif, regime, or domain runtime may
be implemented before AE01 closeout, except narrowly approved infrastructure
required by a frozen AE01 contract.

Possible work:

- canonical catalog and shared-medium specifications;
- LGRC bridge contract and adapter;
- reusable primitive or building-block implementations;
- motif composition interfaces;
- domain probes;
- conformance, integration, replay, and transfer tests.

Phase 4 MUST preserve the evidence and debt status assigned at AE01 closeout.

## 13. Early implementation boundary

**Decision D-022 — Accepted.** Before AE01 closeout, implementation SHOULD be
limited to infrastructure required to make the experiment reproducible and
claim-clean.

Allowed early:

```text
artifact schemas
schema validators
stable IDs and canonical digests
portable provenance helpers
claim-boundary validation
catalog record types
debt record types
selected LGRC artifact readers
minimal substrate-neutral adapter protocols
experiment reconstruction and report generation
```

Deferred unless directly required by a frozen AE01 contract:

```text
general ecology runtime
full primitive library
full building-block library
motif engine
regime engine
domain-complete ant, forest, or swarm runtime
native multi-component medium coupling
general semantic agency API
```

## 14. Artifact and verification policy

All committed experiment artifacts MUST:

- use repository-relative portable identifiers;
- avoid machine-local and checkout-specific paths;
- identify source records and their role;
- distinguish conceptual, inherited, constructed, report-only, and
  source-current fields;
- include stable schema and artifact kinds;
- include canonical digests when consumed by later records;
- carry claim ceilings and unsafe-claim flags where relevant;
- preserve debt and transfer scope;
- be reproducible from tracked scripts and declared inputs.

Human-readable reports SHOULD be projections of machine-readable records rather
than independent sources of stronger claims.

Tests SHOULD cover:

```text
schema validation
canonical serialization and digest stability
portable-path guards
source and lineage integrity
claim-boundary guards
required-control completeness
duplicate reconstruction
snapshot/artifact replay where runtime artifacts are consumed
bridge failure on missing or incompatible source fields
```

## 15. Open and deferred decisions

These decisions are intentionally not resolved by conversation alone.

| ID | Status | Decision needed | Must resolve before |
| --- | --- | --- | --- |
| O-001 | Accepted as D-031 | Python import package name `rc_agentic_ecology`. | Resolved before package creation. |
| O-002 | Deferred by D-032 | Distribution name and initial version. | P4-I1 or any earlier installable-package metadata. |
| O-003 | Accepted as D-033 | LGRC dependency mode: non-runtime artifact inspection plus installed-PyGRC runtime execution. | Resolved before bridge implementation. |
| O-004 | Accepted as D-025 | Canonical JSON serialization and digest conventions. | Resolved before AE01 artifact production. |
| O-005 | Accepted as D-026 | Schema representation: Python types, JSON Schema, or both. | Resolved before AE01 contract freeze. |
| O-006 | Accepted as D-027 | Selected-output commit and large-artifact policy. | Resolved before AE01 artifact production. |
| O-007 | Partially resolved and deferred by D-034 | Replay-frozen realization-profile compatibility is required now; a general stable public or producer/plugin API remains deferred. | Promoting reusable Phase 4 implementations or earlier repeated cross-experiment use. |
| O-008 | Partially resolved and deferred by D-035 | Domain packages are created individually from promotion and dedicated probe evidence; no domain inventory is predeclared. | Phase 3 selects a domain probe and its dedicated evidence supports reusable implementation. |
| O-009 | Accepted as D-029 | Exact N31+ selection scoring and tie policy. | Resolved before AE01 cross-lane synthesis contract freeze. |
| O-010 | Accepted as D-030 | Whether experiment-local reports are generated entirely from JSON or partly authored. | Resolved before AE01 report tooling. |

Open decisions SHOULD be resolved through the smallest document or probe that
can expose the tradeoff. They MUST NOT be silently decided by incidental code.

### 15.1 O-004 disposition — PyGRC-compatible canonical JSON

**Selected option:** native AE artifacts use the existing PyGRC-compatible
canonical JSON convention. For the JSON-native artifact boundary this means
string object keys, recursively sorted keys, semantically ordered arrays,
finite JSON numbers, compact separators, ASCII escaping, UTF-8 encoding, and no
trailing newline in the canonical digest payload. SHA-256 digests are lowercase
hexadecimal values.

Semantic and file identity remain distinct:

- `output_digest` hashes the explicitly scoped canonical payload after removing
  its own `output_digest` field;
- any further digest-scope exclusions MUST be declared by the controlling
  artifact schema rather than inferred from field names;
- tracked JSON files use sorted keys, two-space indentation, ASCII escaping,
  and one trailing newline; and
- a recorded file `sha256` hashes those exact file bytes rather than the
  semantic payload.

Nondeterministic metadata MUST be absent, deterministically derived, or
explicitly excluded by the schema's digest scope. Artifact contracts remain
JSON-native even if an implementation helper can normalize additional Python
container types before validation.

**Alternatives dispositioned:** RFC 8785/JCS is not adopted for native
artifacts at this stage because there is no concrete non-Python LGRC or AE
artifact producer or verifier. File-byte-only hashing is rejected because it
would conflate semantic identity with presentation changes. An undocumented
project-local convention is rejected because PyGRC already provides the
controlling compatibility behavior and source precedent.

**Rationale and source basis:** the graph project's core serialization and
digest helpers, together with N29/N30 artifact practice, establish the current
interoperability boundary. Reusing that boundary keeps AE artifacts directly
compatible with the evidence and runtime family they consume. Multi-language
portability is speculative until the project has sufficiently stable and
valuable content to justify another LGRC implementation.

**Reversibility:** this choice is inexpensive to reverse before native AE
artifacts are retained as stable evidence. After that point, changing the
canonicalization profile is a versioned migration that rebuilds the affected
artifact library while preserving old profile identifiers and source digests.

**Reopening condition:** reconsider JCS or another language-neutral profile
when a concrete non-Python LGRC implementation or independent AE artifact
producer/verifier enters the roadmap. Reopening affects artifact schemas,
serializer conformance vectors, digest validation, manifests, replay, and any
retained native artifact library.

### 15.2 O-005 disposition — Divided-authority dual representation

**Selected option:** AE01 uses JSON Schema Draft 2020-12 for persisted artifact
shape together with Python implementation types and semantic validators. This
is a dual representation, not dual normative authority:

- Markdown experiment contracts govern meaning, evidence roles, controls,
  acceptance, debt, and claim boundaries;
- versioned JSON Schemas govern serialized field structure, required values,
  local types, enumerations, and extension shape; and
- Python dataclasses or `TypedDict` views support code that consumes the
  records, while Python validators enforce cross-field, cross-artifact,
  provenance, digest, path, debt, and claim rules.

Experiment-local schemas remain with AE01 under `contracts/` until closeout.
Only schemas distilled from admitted contracts may later enter
`specs/schemas/`. Python views MUST be introduced only for records actually
consumed by implementation; every schema does not require a speculative Python
type.

Core artifact fields are closed by default. Reviewed extension fields MAY use
the `x_` namespace, but extensions MUST NOT replace required fields, alter the
meaning of core fields, discharge debt, or raise a claim ceiling. Shared valid
and invalid fixtures MUST verify JSON Schema behavior and the corresponding
Python round trip or semantic validator where one exists.

**Alternatives dispositioned:** Python-only schemas are rejected for persisted
AE01 artifacts because the producing script would remain the only effective
validator and contract readers would need implementation code. JSON
Schema-only representation is rejected because local shape validation cannot
enforce the required lineage, digest, source-role, cross-record, and claim
semantics. A Pydantic-first or automatically generated schema system is
deferred because no framework dependency or generation authority is yet
justified.

**Rationale and source basis:** PyGRC and N29/N30 demonstrate the value of
Python types, explicit versions, and semantic validation, while also exposing
the maintenance cost of bespoke required-field and enumeration dictionaries in
experiment builders. AE01 needs independently validatable JSON artifacts at
contract freeze without treating JSON Schema as a replacement for its research
contract or claim guards. Draft 2020-12 is the selected fixed dialect.

**Reversibility:** individual Python implementation views are replaceable while
their artifact schema and behavior remain stable. Changing the persisted schema
dialect or authority after contract freeze requires a versioned schema change,
new conformance fixtures, and reopening of every affected gate and artifact.

**Implementation boundary:** O-005 does not select a Python schema framework or
validation library. P1-I5 may select the smallest Draft 2020-12-conformant
validator and standard-library Python representation that satisfy the frozen
contracts. Incidental code MUST NOT make Pydantic or generated schemas
authoritative without reopening this decision.

### 15.3 O-006 disposition — Selected evidence and mandatory reconstruction

**Selected option:** AE01 uses two output tiers. Full runs, raw telemetry,
caches, duplicate reruns, transient logs, large checkpoints, and exploratory
products belong under the ignored top-level `outputs/` workspace.
Experiment-local `outputs/` contains only predeclared historical evidence
selected for audit, control, replay, closeout, handoff, or compact
reconstruction fixtures. Negative, partial, blocked, and rejected results are
eligible for selection on the same basis as positive results.

Every declared artifact, including a large artifact omitted from Git, MUST have
a portable reconstruction contract containing:

```text
artifact ID and expected relative path
producing target or command and working-directory convention
environment, dependency, and source revisions
input artifact digests, configuration, and random seeds
expected artifact kind, schema, semantic digest, file digest, and size
runtime, memory, disk, and hardware envelope
verification command and last verified reconstruction status
```

One reconstruction recipe MAY produce a related artifact set, but every output
MUST appear in the artifact manifest. Instructions MUST NOT depend on an
undocumented sibling-checkout location, machine-local file, hidden environment
variable, or manual post-generation edit. PyGRC/LGRC dependencies MUST identify
their required version or source revision and provide portable acquisition and
setup instructions.

Machine-readable evidence MUST reproduce its semantic `output_digest`.
Deterministically serialized files SHOULD also reproduce their exact-file
`sha256`. A permitted platform-sensitive visualization MUST declare its
deterministic source artifact and equivalence check and MUST NOT be the sole
evidence for a claim.

Before selection as evidence, reconstruction MUST pass from a clean work area
using the documented instructions. A large local-only artifact retains its
expected digests, size, recipe, resource envelope, and verification status in
the committed manifest. An uncommitted artifact without verified
reconstruction is transient scratch and cannot support a classification or
gate. Loss of reconstruction reopens or downgrades every dependent conclusion.

**Size review policy:** an individual file above 1 MiB or a complete selected
AE01 output set above 10 MiB triggers explicit retention review rather than
automatic rejection. Review MUST consider a compact summary, meaningful
partition, or deterministic local reconstruction without using compression to
hide an unauditable artifact. Git LFS and external artifact storage remain
deferred until a non-reducible evidence artifact establishes a concrete need.

**Alternatives dispositioned:** committing every generated output is rejected
because it would mix historical evidence with disposable runtime state.
Reconstruction-only retention with no selected committed evidence is rejected
because it weakens direct inspection and makes closeout depend entirely on
tool execution. Silent omission of large artifacts is rejected because size
does not discharge evidential dependencies.

**Rationale and source basis:** the graph project already separates ignored
top-level output from selected experiment-local historical evidence. N29 and
N30 demonstrate that compact source, control, classification, and closeout
artifacts can remain directly inspectable while runtime telemetry stays
reconstructable. AE01 strengthens that practice by making artifact-level
instructions and verified reconstruction mandatory rather than relying on the
mere existence of generating code.

**Reversibility and reopening:** size thresholds are review triggers and MAY be
revised without changing artifact identity, but a post-freeze policy change
must revisit affected manifests and retention decisions. Introducing Git LFS,
external storage, or allowing non-reconstructable evidence requires reopening
O-006 and every dependent gate.

### 15.4 O-009 disposition — Gated N31+ ranking and non-selection

**Selected option:** AE01 ranks one primary ecology-to-graph recommendation
only after all required lanes and cross-lane synthesis close. Every candidate
declares one origin mode:

```text
consume = an existing graph surface appears adequate but needs a dedicated probe
extend = an existing surface is relevant but creates a composition tension
introduce = the required distinction is absent and must be proposed
```

Origin mode does not add or subtract points. Naturalization is a preferred
direction and an explicit debt path, not an eligibility prerequisite.

Before scoring, a candidate MUST pass non-compensable eligibility gates. It
must trace to a classified AE01 demand, composition failure, or constructed
probe tension; go beyond conceptual motivation alone; preserve graph evidence,
ecology interpretation, construction, and absence as distinct roles; define an
operational primitive or building-block demand; propose a future graph-side
positive discriminator and counterfactual; admit feasible controls and bounded
reconstruction; and avoid dependence on an unnamed stronger prerequisite.
The proposed discriminator need not exist in current LGRC code.

Eligible candidates receive anchored integer scores from zero to three on ten
dimensions:

| Group | Dimension | Zero anchor | Three anchor |
| --- | --- | --- | --- |
| Demand | Cross-lane recurrence | No classified lane | Four or more independent lanes |
| Demand | Prerequisite centrality | No downstream dependency | Shared prerequisite across several lanes or layers |
| Demand | Composition leverage | Unblocks no composition | Resolves a recurring composition bottleneck |
| Demand | Transfer value | Fixture-specific with no transfer test | Substrate-neutral with meaningful variants |
| Experiment | Gap or tension specificity | Already supported or vaguely missing | Repeated, precisely bounded missing or unsuitable surface |
| Experiment | Future discriminator quality | No proposed source-current discriminator | Measurable signature, threshold, lineage, and counterfactual |
| Experiment | Control feasibility | Nearby explanations cannot be separated | Active nulls, ablation, replay, and alternative-mechanism controls |
| Experiment | Naturalization and debt path | Adds or ignores debt | Defines a credible less-producer-mediated test targeting canonical debt |
| Safety | Claim safety | Requires an unsafe semantic relabel | Precise substrate claim with explicit blocked relabels |
| Safety | Cost feasibility | Unbounded program of work | One bounded experiment using available or explicitly proposed surfaces |

Score `1` means weak, single-instance, mostly inferred, or costly support.
Score `2` means bounded, directly traceable, and adequate for a dedicated
probe. Constructed-probe evidence may support demand, composition, gap, and
control scores only within its declared ecology-side envelope; it cannot count
as native LGRC evidence.

Selection eligibility requires:

```text
every dimension >= 1
demand value >= 7 of 12
experimental readiness >= 8 of 12
safety and feasibility >= 4 of 6
overall >= 20 of 30
gap specificity, future discriminator, controls, and claim safety each >= 2
```

Candidates within one overall point form a tie band. Ties resolve in this
order: demonstrated prerequisite relation, higher experimental readiness,
higher safety and feasibility, then lower implementation/evidence cost.
Candidate identifiers, inherited N31/N32 order, or recurrence alone MUST NOT
break a tie. A remaining tie closes as non-selection with a ranked shortlist
and the evidence needed to separate it.

The ranking MUST be recomputed with equal weights, doubled demand-group weight,
doubled experimental-readiness and safety-group weights, and a conservative
profile that lowers every low-confidence score by one. A candidate is robust
only if it remains first or wins the declared tie procedure in every profile.

AE01 MUST close with explicit non-selection when no candidate clears every
gate and threshold, a tie remains, sensitivity changes the winner, required
lane or synthesis evidence is incomplete, conceptual demand is the primary
basis, reconstruction cannot be bounded, or a stronger unnamed prerequisite
is required. Non-selection still records the ranked shortlist, failure reasons,
missing discriminators, and recommended information-gathering step, and it does
not prevent AE01-C6.

**Alternatives dispositioned:** recurrence-only selection and unconstrained
weighted totals are rejected because strength in one area could hide an
untestable or unsafe candidate. Mandatory selection and discretionary tie
breaking are rejected because an unstable ecology-side demand ranking is itself
a valid result. Restricting candidates to current LGRC code is rejected under
D-028 because it would break the bidirectional spiral.

**Authority and reversibility:** selection is ecology-side demand guidance, not
LGRC evidence or automatic assignment of graph experiment N31. The graph
project retains authority over acceptance, naming, implementation, and
substrate evidence. Scoring anchors and thresholds are frozen before lane
results; changing them afterward reopens ranking, closeout, and every dependent
handoff.

### 15.5 O-010 disposition — Generated facts with authored interpretation

**Selected option:** every AE01 experiment-result report declares one of two
modes:

```text
generated_projection = deterministic report generated entirely from machine records
assembled_interpretation = deterministic generated facts plus tracked authored Markdown
```

Inventory, validation, control, and status reports SHOULD use
`generated_projection` when no distinct interpretive layer is needed. Lane
interpretation, cross-lane synthesis, ranking, and closeout reports MAY use
`assembled_interpretation` so that reasoning remains readable and reviewable
rather than being forced into JSON fields or embedded as long strings in Python
builders.

Machine artifacts remain authoritative for experiment facts: status,
acceptance state, metrics, thresholds, scores, source and artifact identities,
evidence classifications, control results, debt states, gates, ranking
outcomes, claim ceilings, and blocked relabels. Authored sources MAY explain
significance, composition tension, limitations, uncertainty, competing
interpretations, missing patterns, or future hypotheses and LGRC
discriminators. They MUST NOT silently change a machine-recorded fact or
introduce a stronger positive classification.

A result discovered while writing MUST first enter the appropriate machine
record before it can control acceptance or closeout. Otherwise it remains
explicitly labeled as interpretation, hypothesis, or proposed demand within the
report's claim ceiling. This rule does not reduce the exploratory role granted
by D-028; it keeps exploratory interpretation distinct from accepted machine
classification.

Authored sources are tracked separately under the experiment's `reports/`
area. Final evidence-bearing reports are generated artifacts and MUST NOT be
edited directly. Each final report or its report manifest records:

```text
report mode and claim ceiling
source artifact IDs and semantic digests
authored source path and file hash when applicable
generator identity
final report path and file hash
validation and reconstruction status
```

Report generation MUST be deterministic, documented, and verified under
D-027. Regeneration from a clean work area MUST produce no diff from the
committed final report. Validation MUST compare projected status, metrics,
claims, debts, gates, and rankings with the controlling machine artifacts.
Report hashes belong in an external artifact/report manifest so the source
artifact and generated report do not create a circular digest dependency.

Fully manual evidence-bearing final reports are rejected. README files,
hypotheses, contracts, design discussions, and authored report sources are not
generated result reports and remain directly authored documents.

**Alternatives dispositioned:** fully generated prose is rejected as a general
rule because AE01 requires substantive interpretation and storing that prose in
JSON or Python obscures review. Fully manual reports are rejected because
machine values and claim boundaries would drift. Embedding all authored
interpretation inside report-generation scripts is rejected because code would
become an awkward second home for narrative reasoning.

**Implementation boundary and reversibility:** O-010 does not select a template
engine. P1-I5 may implement the smallest deterministic assembler that preserves
this authority split. A report may change modes before contract freeze; after
freeze, a mode or source-boundary change requires regeneration, validation, and
review of the affected report and gates.

### 15.6 O-001 disposition — Python import root

**Selected option:** the project's Python import package is
`rc_agentic_ecology`, rooted at `src/rc_agentic_ecology/`. The `rc` prefix
preserves the established project identity and distinguishes the package from a
generic agentic-ecology library without introducing a shared
`reflexive_coherence` namespace across independently governed repositories.

The import name identifies ownership only. It does not imply that a contained
primitive or building block is admitted, that a surface is native LGRC, or that
top-level exports and compatibility are stable. Subpackages remain subject to
minimum scaffolding and are introduced only when accepted experiment, bridge,
or implementation work requires them.

**Alternatives dispositioned:** `agentic_ecology` is rejected as too generic;
`reflexive_coherence_agentic_ecology` is rejected as unnecessarily long; and a
`reflexive_coherence.agentic_ecology` namespace package is deferred because no
cross-repository namespace governance currently exists.

**Boundary and reversibility:** O-001 does not select the distribution name,
version, public API, or compatibility policy. Renaming is inexpensive before
package creation but becomes a migration after imports appear, so any later
change reopens packaging, tests, examples, and reconstruction instructions.

### 15.7 O-002 disposition — Distribution identity deferred

**Selected option:** distribution name and software version remain unset. The
accepted `rc_agentic_ecology` import root does not require a corresponding
distribution decision during Phase 0. The repository's existing `0.1` changelog
and citation version identifies its conceptual public snapshot and MUST NOT be
interpreted as an installable Python package release.

Before packaging, reconstruction identities use Git revisions, schema versions,
artifact digests, and dependency revisions. Phase 1 MAY add `pyproject.toml`
tool configuration without adding `[project]` distribution metadata. If a
frozen Phase 1 contract requires installation rather than documented
repository-local execution, O-002 MUST reopen before that metadata is created.

The likely distribution spelling `rc-agentic-ecology` remains a non-binding
candidate. Reopening at P4-I1 or earlier MUST jointly decide distribution name,
software version and versioning policy, its relationship to repository
publication versions, supported Python versions, dependency groups,
license/package-content boundary, publication target, and compatibility status.

**Safe default and reversibility:** no distribution is built or published, and
no software release meaning is inferred. Deferral avoids a later rename or
version reset and has no effect on artifact or source reconstruction because
those identities are already explicit under D-025 and D-027.

### 15.8 O-003 disposition — Strict dual-surface LGRC integration

**Selected option:** RCAE distinguishes non-runtime artifact inspection from
live execution through an installed PyGRC runtime. There are three explicit
execution classes:

```text
artifact_inspection
pygrc_runtime_with_rcae_producer
pygrc_native_runtime
```

Artifact inspection validates and interprets historical artifacts without
claiming execution and without requiring `pygrc`. Every live execution class
requires an available, compatible PyGRC installation and MUST fail immediately
when runtime identity or required capabilities cannot be established. Artifact
inspection, mock behavior, or an RCAE-local pseudo-runtime MUST NOT substitute
for a requested runtime mode.

The physical PyGRC location is machine- and user-specific. Python environment
resolution or an ignored local binding selects it; no checkout, environment,
or package path enters committed configuration, artifacts, reports, or
reconstruction receipts. Public reconstruction instructions record how to
obtain the required source revision. Each run validates and records the PyGRC
revision, relevant schema versions, capability set, and runtime identity. A
local binding that does not satisfy those identities fails closed.

RCAE exposes only narrow ecology-side boundaries needed by admitted use cases:

```text
validated LGRC state or snapshot
    -> minimal immutable ecology view
    -> explicit RCAE constructed producer
    -> declarative producer request
    -> narrow runtime adapter
    -> declared PyGRC public operation
    -> transition receipt and resulting state identity
```

The bridge MUST NOT mirror or re-export the PyGRC API, subclass or monkey-patch
LGRC to inject behavior, register global hooks at import time, mutate PyGRC
module state or registries, make PyGRC import RCAE, import graph experiment
scripts, or write into the graph repository. Intended runtime transitions occur
only through explicit session requests and record before/after identities,
provenance, and transition receipts.

Every mechanism freezes its binding mode, implementation identity, required
PyGRC identity, evidence class, claim ceiling, and remaining debt. A constructed
RCAE binding remains constructed even when a later PyGRC version offers related
native functionality. Native adoption requires a separate explicit binding,
capability/schema validation, new run identity and artifacts, comparison
against the constructed version, updated debt and claim classification, and an
explicit promotion or supersession decision. Existing runs remain
reconstructable against their pinned runtime and are never retroactively
naturalized.

RCAE sends the graph project a versioned demand contract describing the missing
mechanism, constructed semantics, inputs and outputs, discriminator,
counterfactuals, controls, debt, and expected native claim ceiling. It does not
inject its producer into PyGRC. The graph project independently implements and
tests a native realization, which RCAE may later consume through a new binding.

**Alternatives dispositioned:** artifact-only integration is rejected as the
sole mode because D-028 requires live comparisons and constructed probes when
useful. Runtime-only integration is rejected because historical evidence must
remain inspectable without a runtime. Automatic fallback, API mirroring,
monkey-patched extensions, and availability-based native substitution are
rejected because they destroy provenance, isolation, and reconstruction.

**Staging and reopening:** artifact inspection is the initial AE01 path; runtime
adapters are implemented only for frozen use cases. The detailed binding and
compatibility policy remains subject to O-007 review against actual LGRC
extension practice, but no later decision may weaken the explicit-mode,
no-silent-substitution, read-only, or runtime-identity requirements of D-033.

### 15.9 O-007 disposition — Replay-frozen realization profiles; general API deferred

**Selected option:** AE01 does not define a general stable RCAE producer,
plugin, or LGRC-extension API. Each retained runtime experiment instead freezes
a versioned mechanism contract and an explicit realization profile. The stable
unit for replay is the recorded experiment boundary, not a promise that all
future mechanisms share one Python interface.

Every realization profile MUST declare at least:

```text
mechanism-contract and realization-profile identifiers and versions
realization class: rcae_constructed | pygrc_native_candidate | pygrc_native_supported
exact PyGRC source/release identity and required public facade capabilities
required policy identifiers and input, output, state, and artifact schema versions
availability, enabled, validated, and supported status as separate fields
producer/transition discipline and allowed scheduling operations
claim ceiling, evidence class, remaining debt, and transfer scope
reconstruction, replay, controls, and compatibility-conformance procedure
```

Constructed RCAE producers inspect an immutable copy or validated projection of
LGRC state, emit evidence and declarative requests, and schedule work only
through the narrow public PyGRC operations named in their profile. They MUST NOT
retain or mutate internal PyGRC state. PyGRC `step()` or its declared successor
remains the transition consumer; an RCAE producer does not replace transition
semantics.

A native candidate and a supported native realization are distinct additive
profiles. The existence of a newer native capability never changes a retained
constructed profile, its replay target, or its historical claim class. Native
comparison requires a new profile, compatibility/conformance checks, controls,
artifacts, and an explicit promotion or supersession decision. A later PyGRC
revision likewise requires a new or revalidated profile rather than presumed
compatibility.

This policy follows the extension discipline observed in the graph project's
Phase 8 LGRC work: freeze a baseline before source changes; add default-off,
serialized, versioned policy; expose runtime-visible evidence; keep producers
separate from transition consumption; validate snapshot/artifact replay and
negative controls; distinguish enabled, validated, and supported states; and
close out the native surface before downstream adoption. The Phase 8 native
packet-loop path is the controlling precedent for treating constructed and
native rows as non-retroactive evidence rather than silently rewriting earlier
runs. This is a source-practice observation, not authorization for RCAE to
perform the graph-side changes.

**Hard repository boundary:** the graph/PyGRC repository is read-only from
RCAE. No RCAE command, script, adapter, experiment, test, reproduction recipe,
promotion workflow, or automation may edit it. RCAE may emit a portable demand
contract and later consume a graph-owned native result. Implementing or changing
the native PyGRC realization is a separately authorized graph-project action,
performed outside RCAE and under graph-project change control. This boundary is
non-negotiable within O-007 and reinforces D-003, D-018, D-028, and D-033.

**Alternatives dispositioned:** a stable general producer/plugin API is
deferred because PyGRC exposes mechanism-specific policies and public scheduling
operations rather than a general plugin contract, and AE01 has not yet produced
repeated use pressure from which to infer the right abstraction. Mirroring or
re-exporting the PyGRC API, importing deep internal modules, accepting mutable
runtime state, monkey-patching, global registration, or availability-driven
binding substitution is rejected under D-033. Treating current PyGRC research
surfaces as SemVer-stable is also rejected.

**Safe default, reversibility, and reopening:** new mechanisms remain
experiment-local and receive explicit replay profiles; no general public API or
cross-experiment compatibility promise is inferred. This is additive and
reversible because a later API can wrap retained profiles without changing
their identities or evidence. Reopen the general API question at P4-I1 when a
reusable implementation is actually promoted, or earlier when at least two
independent retained consumers require the same boundary. Reopening MUST retain
replay compatibility and the hard read-only graph boundary.

### 15.10 O-008 disposition — Admission-driven domain inventory

**Selected option:** no fixed domain-package inventory is declared. A reusable
domain package is created only when the Phase 3 promotion queue selects that
domain and a dedicated domain probe supports its implementation. Each later
domain is considered independently; admitting one domain does not reserve,
promise, or scaffold the others.

The ant colony remains the primary conceptual worked example in the papers, but
conceptual prominence does not make `ant` the first admitted implementation.
Likewise, ant, forest, farm, swarm, cell, society, and other examples name
transfer questions and possible domain contexts, not a source backlog. The
`<promoted_domain>/` target-tree entry is therefore a category boundary rather
than a list of promised packages.

AE01 lanes SHOULD remain substrate- and domain-neutral wherever their tested
distinction permits it. A lane MAY use domain-shaped fixtures, interpretations,
or constructed mechanisms, but these stay experiment-local and retain their
evidence class and claim ceiling. Domain-specific experimental success does not
admit a reusable domain package or establish the domain's biological, semantic,
coordination, or agency claims.

Before a domain package can be created, its promotion record MUST identify:

```text
dedicated domain contract and supporting probe classification
admitted or explicitly candidate primitive, building-block, motif, and regime dependencies
parent basin, persistence boundary, controls, and reconstruction procedure
domain-specific versus transferable responsibilities
producer scaffolds, debt, transfer scope, claim ceiling, and blocked relabels
implementation owner, public surface, conformance tests, and promotion status
```

Reusable behavior discovered through a domain probe belongs in a
substrate-neutral catalog layer only when its transfer evidence supports that
broader placement. It MUST NOT be generalized merely to avoid domain-local
code, and domain packages MUST NOT become a miscellaneous home for unclassified
primitives, bridge behavior, or runtime policy.

**Alternatives dispositioned:** precreating `ant`, `forest`, and `swarm`
packages is rejected because it would turn illustrative paper domains into an
implicit implementation commitment and create empty architecture without an
immediate owner. Automatically selecting RC-Ant first is rejected because its
worked-example role is conceptual rather than experimental admission evidence.
A fixed comprehensive inventory is rejected because AE01 and later graph/ecology
spirals may expose different domain boundaries.

**Safe default, reversibility, and reopening:** until a supported promotion
exists, no `domains/` package or empty domain subpackages are created; domain
work remains in its owning experiment. This deferral costs only a later additive
directory creation and avoids package removal or misleading public surfaces.
Reopen O-008 when Phase 3 selects the first domain probe and its dedicated
evidence supports reusable implementation. At that point decide only the
selected domain's package; inventory beyond it remains evidence-driven and
deferred by this policy.

### 15.11 R1 disposition — Graduated evidence ceremony

**Review finding:** the P0-I2 decision lattice is coherent and its strongest
features are the D-028 evidence classes, concrete reopening conditions, valid
non-selection under D-029, and the D-030 split between generated facts and
authored interpretation. Its highest friction-to-value risks are repetitive
reconstruction entry under D-027, runtime-binding ceremony under D-033/D-034,
false precision in D-029 scoring, and silent Markdown/schema/Python drift under
D-026. Strict promotion metadata could also discourage useful experiment-local
sharing, while strict live bindings could discourage informative comparisons.

**Selected resolution:** ceremony scales with evidential use; safety and claim
boundaries do not. AE01 freezes three evidence-use tiers:

```text
exploratory_scratch
    transient local work that may inform contract design
    cannot support a classification, gate, report fact, or promotion

registered_probe
    frozen question, controls, stopping conditions, and execution mode
    may use generated local receipts and transient outputs
    cannot support a classification until selected artifacts satisfy D-027

retained_evidence
    selected declared artifacts supporting classification, audit, or a gate
    requires a complete resolved manifest and verified clean reconstruction
```

Every live execution at every tier still validates and records its requested
execution class, PyGRC identity, required capabilities, and realization profile
and still fails closed without fallback. Exploratory status never authorizes a
pseudo-runtime, an incompatible binding, mutation of the graph repository, or
a stronger claim. A transient live receipt may remain in ignored local output,
but it must exist for the run.

Reconstruction manifests MAY reference versioned environment, dependency,
command, resource, and realization profiles. Tooling SHOULD generate receipts
and artifact entries from those profiles. Before an artifact becomes retained
evidence, validation MUST materialize a fully resolved view containing every
D-027 field; profile inheritance cannot hide, weaken, or ambiguously override a
required value.

D-026 remains a divided-authority model rather than three copies of one schema.
Markdown states meaning and claims, JSON Schema alone governs persisted shape,
and Python adds only required semantic and cross-record validation for records
actually consumed. Shared valid and invalid fixtures expose drift. Phase 1
SHOULD automate reference projections where doing so does not create a new
schema authority.

Constructed code used by multiple AE01 lanes MAY be shared within the AE01
experiment without promotion to `src/`. Its lanes MAY reference one common
construction declaration and implementation identity, but each use must retain
its applicable inputs, controls, debts, claim ceiling, and result lineage.
Cross-experiment reuse or a public surface reopens the `src/` promotion and
metadata question; experiment-local sharing alone does not.

D-029 scoring occurs only after eligible candidates and cross-lane synthesis
exist. Every candidate keeps an independently authored qualitative mechanism
rationale and any investigator-prior ordering separate from its machine-derived
scores. The report MUST expose disagreements between qualitative judgment,
thresholds, tie handling, and sensitivity profiles. Qualitative judgment may
motivate another discriminator or review but cannot silently override an
eligibility gate, frozen score, or required non-selection.

**Alternatives dispositioned:** full retained-evidence ceremony for transient
scratch is rejected as likely compliance theater. Relaxing runtime identity,
read-only behavior, evidence roles, reconstruction before retention, or claim
ceilings for exploration is rejected because those are safety and meaning
boundaries rather than documentation overhead. Manual duplication of shared
profile fields is rejected when a deterministic resolved manifest can preserve
the same information. Intuitive candidate selection is retained as explicit
qualitative rationale but rejected as an unrecorded scoring override.

**R1 conclusion:** D-027, D-029, D-033, and the other P0-I2 decisions remain in
force. D-037 governs their Phase 1 operationalization and closes Review R1
without reopening P0-I2. A later workflow that lets scratch support a claim,
lets profile inheritance conceal required identity, or makes qualitative
judgment an implicit override reopens the affected contract and gate.

### 15.12 D-038 disposition — Threshold anchors and developmental interpretation

**Observed tension:** revision 0.23 froze exact margins, full signature/control
passage, seed agreement, and non-selection paths correctly before execution,
but its language could be read as a binary accept/decline system. That would
discard structure below the target, over-read narrow success, and turn local
optimization toward the proxy rather than the function. It would also conflict
with the observation-first, bounded-probe, naturalization, two-axis,
measurement, and renewed-attunement directives supplied by the project owner.

**Selected resolution:** thresholds remain fixed but become reference surfaces
and highest-rung anchors. AE01 separates:

```text
hard execution validity:
  schema, runtime, reconstruction, identity, path, attempt, resource,
  and graph-read-only conformance

hard claim safety:
  evidence-role separation, unsafe relabel prevention, claim ceilings,
  and explicit constructed/native transitions

scientific interpretation:
  direction, resolution, boundary rung, causal controls, support dependence,
  transfer, recurrence, unexpected properties, and next questions
```

A valid causal control that contradicts the target is evidence. A missing or
invalid control leaves the execution incomplete. A below-threshold result may
remain a lower, adjacent, unexpected, reusable, or generative class. An above-
threshold result may remain narrow, resolution-limited, support-dependent, or
blocked at a lower claim ceiling.

Every lane receives a first-class primary metric sheet and candidate-blind
calibration record. Before candidate execution, the resolution band is:

```text
delta = max(
  declared measurement resolution,
  maximum absolute matched-null margin from frozen calibration seeds
)
```

The candidate-blind calibration seeds are distinct from candidate seeds and
cannot inspect candidate outcomes. Without frozen `delta`, narrow/robust
language and candidate execution remain blocked.

Every completed result also receives one first-class developmental-
interpretation record with per-seed relation, the cumulative lane boundary
ladder, highest valid rung, support status, expected/adjacent/unexpected
properties, T0-through-T4 classification value, separate becoming/development
readings, blocked claims, and one next move with a falsifier.

A bounded local refinement is not a retry. It must keep the causal question,
target the function rather than its proxy, change one surface, preserve the
prior result, name a falsifier, and advance source specificity, withdrawal
resistance, recurrence, transfer, broader regime validity, or native
expression. Otherwise the work becomes an alternative realization, new probe,
class/hypothesis revision, aim redescription, or explicit stop, each under a
new preregistration.

**Schema and gate effect:** this decision explicitly reopens P1-I3, P1-I4, and
P1-I5. The common schema advances from `1.0.0` to `1.1.0`; retained older
records never migrate silently. P1-I1 and P1-I2 remain closed because source
admission, lane identity, and atlas content did not change. P1-GATE remains
closed until revision 0.24 validation passes. When it passes, it authorizes
candidate-blind calibration and lane registration; candidate cells remain
blocked until their lane-local resolution freeze and registration gate pass.

**Alternatives dispositioned:** turning fixed thresholds into post-outcome
discretion is rejected because it invites rescue narratives. Keeping binary
threshold interpretation is rejected because it erases irreducible structure.
Hiding authoritative interpretation in `x_` extensions is rejected because
extensions cannot satisfy a gate or redefine terminal meaning. Treating every
local tag as a new research arc is rejected through the T0/T1 value boundary.

**Reopening condition:** a valid result exposes an important relation not
representable by the threshold vocabulary, lane ladder, support statuses,
classification-value ladder, or next-move dispositions; or the calibration
procedure proves unable to separate measurement resolution from candidate
behavior without leakage.

## 16. Immediate next steps

Current dependency order after revision 0.24:

1. Complete Review R2 over the refrozen P1-I1 through P1-I5 contract.
2. Disposition `AE01-C1`, `AE01-C2`, and any R2 findings without opening an
   evidential conclusion.
3. Pass `P1-GATE`; this opens candidate-blind calibration and lane registration
   only.
4. For each Phase 2 lane, freeze calibration and exact implementation
   registration before candidate execution.
5. Execute and classify lanes independently; synthesize only after all required
   terminal and developmental-interpretation records are comparable.
6. Close AE01 before promoting canonical specifications or stable source
   abstractions.

## 17. Conversation provenance and directive maintenance

**Decision D-023 — Accepted.** Raw conversation SHOULD NOT serve as the active
project directive.

Conversation is valuable for:

```text
design provenance
alternative options
discarded or superseded reasoning
the motivation behind accepted decisions
```

It is unsuitable as normative authority because it contains exploratory,
revised, and sometimes superseded statements without stable identifiers or a
clear conflict rule.

The maintained directive model is:

```text
conversation and review discussion
    -> decision extraction
    -> accepted decision IDs in this plan or a dedicated decision record
    -> roadmaps, contracts, specs, and implementation plans cite those IDs
    -> later changes update the decision and record why
```

If a transcript is retained in the repository, it SHOULD live in a clearly
non-normative discussion or provenance area and MUST begin with a banner such
as:

```text
Status: non-normative design provenance
Do not consume as an experiment contract, specification, or evidence source.
Current directives are maintained in implementation/PostN30-plan.md.
```

This plan preserves the durable content of the conversation by extracting it
into decisions, boundaries, gates, and open questions. Git history and a small
change log are preferable to leaving superseded advice mixed into the active
directive.

### Change log

| Date | Change |
| --- | --- |
| 2026-07-10 | Replaced the raw conversational copy with the master Post-N30 architecture, atlas, specification, and implementation directive; recorded accepted and open decisions. |
| 2026-07-10 | Linked the full-program execution checklist covering iteration boundaries, exit gates, implementation work, review points, and change control. |
| 2026-07-10 | Revision 0.2: carried forward six canonical N29 debts, required N29 closeout/source digests, reframed Lane 7 as expected-missing demand classification, documented Lane 1/4 motivation, enabled parallel lane execution, and made Phase 4/spec filenames explicitly provisional. |
| 2026-07-10 | Revision 0.3: added symmetric N30 closeout-digest traceability and aligned the recorded decision range through D-024. |
| 2026-07-10 | Revision 0.3 formally accepted by the project owner; checklist gate `P0-I1-GATE` closed. |
| 2026-07-10 | Revision 0.4: resolved O-004 as D-025 with a PyGRC-compatible canonical JSON profile and a concrete trigger for reconsidering language-neutral canonicalization. |
| 2026-07-10 | Revision 0.5: resolved O-005 as D-026 with JSON Schema Draft 2020-12 for persisted shape and Python types/validators for implementation and semantic constraints. |
| 2026-07-10 | Revision 0.6: resolved O-006 as D-027 with selected historical evidence, review thresholds for large outputs, and mandatory verified reconstruction for every declared artifact. |
| 2026-07-10 | Revision 0.7: accepted D-028, defining the graph/agentic-ecology relation as a bidirectional spiral that permits explicitly constructed ecology-side demand probes without promoting them to native LGRC evidence. |
| 2026-07-10 | Revision 0.8: resolved O-009 as D-029 with consume/extend/introduce candidate origins, non-compensable eligibility gates, anchored scoring, deterministic tie handling, sensitivity checks, and explicit non-selection. |
| 2026-07-10 | Revision 0.9: resolved O-010 as D-030 with generated report projections or deterministic assembly of generated facts and separately authored bounded interpretation. |
| 2026-07-10 | Revision 0.10: resolved O-001 as D-031, fixing `rc_agentic_ecology` as the Python import root without assigning distribution, release, or compatibility meaning. |
| 2026-07-10 | Revision 0.11: accepted D-032, explicitly deferring Python distribution name and software version while separating them from repository publication version `0.1`. |
| 2026-07-10 | Revision 0.12: resolved O-003 as D-033 with non-runtime artifact inspection, strict installed-PyGRC execution, local runtime resolution, narrow adapters, and explicit constructed-to-native transitions. |
| 2026-07-10 | Revision 0.13: partially resolved O-007 as D-034 with replay-frozen mechanism contracts and realization profiles, graph Phase 8 extension discipline, deferred general API stability, and an explicit prohibition on RCAE modifying the graph/PyGRC repository. |
| 2026-07-10 | Revision 0.14: partially resolved O-008 as D-035 with admission-driven domain packages, experiment-local domain fixtures, and no predeclared or empty domain inventory. P0-I2 decision resolution passed. |
| 2026-07-10 | Revision 0.15: accepted D-036, corrected stale Phase 0 dependency bookkeeping, and converted identified architecture tensions into explicit Phase 1 construction, runtime-binding, tooling-bootstrap, domain-placement, applicability, and bounded lane-closure obligations. |
| 2026-07-10 | Revision 0.16: completed the minimum P0-I3 scaffold with experiment and implementation indexes, the Post-N30 roadmap, the AE01 workspace, and only the contract, hypothesis, and experiment-implementation paths owned by Phase 1. |
| 2026-07-10 | Revision 0.17: accepted D-037 as the Review R1 resolution, introducing graduated evidence ceremony, resolved shared profiles, generated runtime receipts, experiment-local construction sharing, schema-drift controls, and qualitative rationale alongside synthesis-only scoring. P0-GATE passed. |
| 2026-07-10 | Revision 0.18: applied the post-scaffold review follow-ups by aligning the experiment reconstruction summary with every D-027 requirement and requiring stable lane IDs, a single machine-readable lane registry, rename provenance, and validated narrative projections during Phase 1. No completed gate reopened. |
| 2026-07-10 | Revision 0.19: passed P1-I1 source inventory and method admission with verified conceptual-source digests, N29 closeout and ten-artifact lineage, A-D prototype/debt boundaries, N30 replay/closeout evidence, mutable-roadmap provenance, and the current N30+ cross-project spiral rule. No positive AE01 evidence or acceptance rung opened. |
| 2026-07-10 | Revision 0.20: passed P1-I2 with a complete atlas content outline, stable `AE01-L01` through `AE01-L07` identities, lane motivations and ceilings, catalog/ontology rules, debt and terminal taxonomies, expected outputs, stopping/non-selection boundaries, and aligned roadmap/README projections. `AE01-C0` assigned with no positive evidence. |
| 2026-07-10 | Revision 0.21: passed P1-I3 with a versioned Markdown meaning contract, one discriminated JSON Schema Draft 2020-12 bundle for seventeen record types, and the controlling seven-lane machine registry. Contract closure did not open positive evidence or advance beyond `AE01-C0`; Python semantic validation and automated projection checks remain P1-I5 work. |
| 2026-07-10 | Revision 0.22: passed P1-I4 with seven lane hypotheses, recurring-demand and explicit-non-selection synthesis hypotheses, finite comparison/stopping rules, nineteen common fail-closed controls, ten preserved failure classifications, and an explicit P1-I5 implementation handoff. No lane executed and no result or higher acceptance rung opened. |
| 2026-07-10 | Revision 0.23: passed P1-I5 with experiment-local canonicalization, digests, schema and semantic guards, deterministic IDs, resolved manifests/profiles, finite comparison policy, strict runtime receipts, report assembly, validated lane projections, conformance fixtures, portable reconstruction commands, and focused tests. Infrastructure validation opened no lane evidence; P1-GATE and Review R2 remain open. |
| 2026-07-10 | Revision 0.24: accepted D-038 and explicitly reopened/refroze P1-I3 through P1-I5 with schema `1.1.0`, first-class metric sheets, candidate-blind calibration, machine-derived threshold relations, lane boundary ladders, two-axis developmental interpretations, classification-value and next-move discipline, and guarded local refinement. Thresholds remain frozen anchors without erasing lower or unexpected classes; no lane evidence opened. |

## 18. Program completion criteria

The program governed by this plan is complete when:

- its architecture and directive decisions have been reviewed and maintained;
- all phase-blocking decisions have resolutions or safe explicit defaults;
- the atlas roadmap and complete AE01 contract set exist;
- AE01 has executed all required lanes and closed at a supported rung;
- cross-lane requirements, composition failures, debts, and transfer limits
  have been classified;
- an N31+ candidate has been selected through the declared gate, or a justified
  non-selection handoff has been recorded;
- every AE01 result has been classified for specification promotion,
  implementation, further experiment, or rejection;
- canonical specifications exist for every result admitted for reuse;
- the required LGRC bridge surfaces have operational contracts, portable
  provenance, failure behavior, and conformance tests;
- reusable primitives, building blocks, motifs, regimes, and domain components
  selected by the promotion queue have been implemented and verified, or their
  deferral has been explicitly recorded;
- a final Post-N30 program closeout records the resulting repository state,
  remaining debt, blocked claims, and next graph/ecology spiral handoff.

Individual phase completion does not imply completion of this plan. Phase 0
closes architecture decisions; Phase 1 freezes the atlas contract; Phase 2
executes it; Phase 3 classifies and promotes results; Phase 4 specifies and
implements the admitted reusable surfaces. The master plan remains active until
the final program closeout supersedes it.

## 19. Claim boundary

This document supports a project architecture and research plan only.

It does not establish:

```text
an executed ecology runtime
an admitted ecology primitive or building block
an ecology motif or regime
native shared-medium coordination
parent-basin modulation evidence
semantic communication or cooperation
agentic_ecology_demand_as_substrate_evidence
agency, selfhood, sentience, organism, or life
N31 selection
Phase 8 completion
```

Its bounded positive claim is:

```text
RC-Agentic-Ecology now has an explicit architecture, directive hierarchy,
Post-N30 atlas program, promotion lifecycle, LGRC consumption boundary, and
phased path from demand discovery to specification and reusable implementation.
```
