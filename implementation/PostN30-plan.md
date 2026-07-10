# Post-N30 Project Architecture, Atlas, Specification, and Implementation Plan

**Status:** active master program directive

**Plan revision:** 0.3

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
| D-012 | Accepted | Early implementation is limited to infrastructure required to execute and validate AE01. |
| D-013 | Accepted | Raw conversation is decision provenance, not normative project authority. This plan is the maintained directive extracted from it. |
| D-014 | Accepted | Only the minimum structure required by the current phase should be scaffolded; speculative empty architecture is deferred. |
| D-015 | Accepted | The repository tree in Section 7 is the target structure, introduced incrementally rather than scaffolded all at once. |
| D-016 | Accepted | Catalog items follow the explicit demand-to-contract-to-evidence-to-specification-to-implementation lifecycle in Section 8. |
| D-017 | Accepted | Canonical specifications are operational contracts and must not become another conceptual-paper surface. |
| D-018 | Accepted | LGRC consumption is isolated behind the provenance-preserving adapter boundary in Section 10. |
| D-019 | Accepted | AE01 is an atlas-building experiment with specification-like local contracts, not itself a canonical specification. |
| D-020 | Accepted | AE01 begins with the seven comparable, independently executable shared-medium lanes listed in Section 11.3; only cross-lane synthesis requires every lane to close. |
| D-021 | Accepted | AE01 uses the C0-C6 acceptance ladder in Section 11.7, subject to contract-freeze review. |
| D-022 | Accepted | Pre-closeout implementation remains limited to reproducibility, validation, provenance, and bridge infrastructure required by AE01. |
| D-023 | Accepted | Maintained decision records, not raw dialogue, are the normative way conversation-derived directives enter the repository. |
| D-024 | Accepted | AE01 carries all six unresolved N29 debts through source inventory, lane classification, synthesis, promotion, and closeout unless dedicated discharge evidence exists. |

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
            ant/
            forest/
            swarm/
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
`pygrc` implementation modules. The exact dependency and package-installation
mechanism remains an open program decision that must be resolved during Phase
0 before bridge implementation begins.

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

1. minimal shared-medium niche formation;
2. shared-pool co-conditioning;
3. trail or stigmergic field;
4. nursery or support field;
5. boundary-conditioned exchange;
6. capacity circulation;
7. parent-basin modulation demand and missing-surface classification.

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

### 11.4 Common lane contract

Every lane MUST record:

```text
pattern identifier
primary catalog layer and secondary observations
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
new substrate requirements
composition inputs, outputs, and interference risks
controls and withdrawal tests
all applicable debts
transfer scope
claim ceiling and blocked relabels
candidate N31+ implication, if any
```

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
AE01-C2 = lane schemas, controls, and claim guards frozen
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
- implementation plan and checklist;
- expected artifact inventory.

No positive atlas conclusions may be assigned in this phase.

Exit gate:

```text
sources, lanes, schemas, controls, evidence classes, debt fields,
acceptance rungs, and stopping conditions are frozen
```

### Phase 2 — Atlas execution

Required work:

- populate each lane from declared sources;
- generate reproducible artifacts and reports;
- distinguish N30 grounding from ecology extrapolation;
- classify missing requirements and failures;
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
| O-001 | Proposed | Python import package name `rc_agentic_ecology`. | Creating the installable package. |
| O-002 | Deferred | Distribution name and initial version. | Packaging or release work. |
| O-003 | Open | LGRC dependency mode: installed `pygrc`, artifact-only adapter, or both. | Implementing the bridge. |
| O-004 | Open | Canonical JSON serialization and digest conventions. | Producing AE01 artifacts consumed across iterations. |
| O-005 | Open | Schema representation: Python types, JSON Schema, or both. | Freezing AE01 machine contracts. |
| O-006 | Open | Selected-output commit and large-artifact policy. | First generated AE01 outputs. |
| O-007 | Deferred | Stable public API and compatibility policy. | Promoting reusable Phase 4 implementations. |
| O-008 | Deferred | Domain package inventory beyond the first admitted probe. | Domain implementation. |
| O-009 | Open | Exact N31+ selection scoring and tie policy. | AE01 cross-lane synthesis contract freeze. |
| O-010 | Open | Whether experiment-local reports are generated entirely from JSON or partly authored. | AE01 report tooling. |

Open decisions SHOULD be resolved through the smallest document or probe that
can expose the tradeoff. They MUST NOT be silently decided by incidental code.

## 16. Immediate next steps

After this plan is accepted:

1. Review and accept or revise this plan and its companion master checklist.
2. Record the review result and pass the checklist's `P0-I1-GATE`.
3. Resolve only the open decisions that block the AE01 contract freeze.
4. Create the minimum `experiments/` structure and its README.
5. Draft the Post-N30 atlas roadmap without positive conclusions.
6. Draft the AE01 README, hypotheses, common lane contract, controls, and
   acceptance ladder.
7. Define the initial machine-readable contract and artifact policy.
8. Scaffold only the code and directories required to validate and execute the
   frozen AE01 contract.
9. Execute and classify one lane at a time; synthesize only after all required
   lanes are comparable.
10. Close AE01 before promoting canonical specifications or stable source
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
