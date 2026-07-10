# Post-N30 Master Program Checklist

**Status:** active master tracking checklist

**Baseline revision:** 0.21

**Date:** 2026-07-10

**Companion directive:** [Post-N30 master plan](PostN30-plan.md)

**Scope:** architecture, AE01 contract and execution, closeout, specification
promotion, LGRC bridge, reusable implementation, verification, and final handoff

## 1. How to use this checklist

This checklist is the visible execution surface for the Post-N30 master plan.
The plan defines rationale, authority, and boundaries. This file records what is
pending, in progress, completed, blocked, revised, or deliberately deferred.

Checkbox convention:

```text
[ ] pending or not yet demonstrated
[x] completed with evidence, or explicitly dispositioned as deferred/superseded
```

Rules:

- A checked item SHOULD cite the artifact, report, test, or decision that closes
  it.
- A phase is not complete until every mandatory exit-gate item is checked.
- A document existing is not enough when the item requires review, validation,
  replay, controls, or acceptance.
- Conditional items may be checked as explicitly deferred only when a reason,
  scope, and reopening condition are recorded.
- Requirements MAY change as implementation and experiments expose better
  distinctions.
- A post-freeze change MUST be recorded in Section 16 and MUST reopen every
  affected gate and downstream conclusion.
- Completed history MUST NOT be silently deleted. Superseded items should be
  retained or referenced from a change record.
- This checklist MUST NOT be used to promote claims beyond the master plan or
  the controlling experiment/specification evidence.

## 2. Program dashboard

| Program surface | Status | Current gate | Exit evidence |
| --- | --- | --- | --- |
| Master directive | Active at revision 0.21 | Maintained under change control | `implementation/PostN30-plan.md` and `implementation/PostN30-checklist.md` |
| Phase 0 — Architecture and decisions | Complete | P0-GATE | P0-GATE passed |
| Phase 1 — AE01 contract freeze | In progress | P1-I4-GATE | P1-I3-GATE passed |
| Phase 2 — Atlas execution | Blocked by Phase 1 | P2-GATE | Pending |
| Phase 3 — Closeout and promotion | Blocked by Phase 2 | P3-GATE | Pending |
| Phase 4 — Specs and implementation | Blocked by Phase 3 except approved infrastructure | P4-GATE | Pending |
| Final Post-N30 closeout | Blocked | FINAL-GATE | Pending |

AE01 ladder dashboard:

| Rung | Meaning | Status |
| --- | --- | --- |
| AE01-C0 | Initialized, no atlas claim | Assigned at P1-I2; no positive evidence |
| AE01-C1 | Source inventory and consumption boundaries accepted | Not assigned |
| AE01-C2 | Lane schemas, controls, and claim guards frozen | Not assigned |
| AE01-C3 | All required lane records classified | Not assigned |
| AE01-C4 | Cross-lane requirements and dependencies synthesized | Not assigned |
| AE01-C5 | Controls, debt, failure, and non-selection gates passed | Not assigned |
| AE01-C6 | Atlas closeout and N31+ handoff complete | Not assigned |

## 3. Global boundaries that apply to every iteration

These are non-negotiable unless the master plan itself is revised.

- [x] The graph project is designated read-only from this project. Evidence:
  master-plan decisions D-003 and D-018.
- [x] Repository records require portable relative identifiers rather than
  checkout-specific paths. Evidence: master plan Sections 5, 10, and 14.
- [x] Papers are ontology and method sources, not runtime evidence. Evidence:
  master-plan directive hierarchy.
- [x] N29 component evidence is not ecology composition evidence. Evidence:
  master-plan AE01 source posture.
- [x] All six unresolved N29 closeout debts are mandatory carry-forward inputs
  to AE01. Evidence: master-plan decision D-024.
- [x] N30 is bounded minimal shared-medium participation and trace-mediated
  eligibility evidence, not shared-medium coordination, agency, parent-basin
  modulation, or ecology regime evidence.
- [x] Source placement, class names, examples, and passing unit tests do not by
  themselves promote research claims.
- [x] Producer, medium, naturalization, semantic, transfer, composition,
  measurement, and claim debt remain visible until explicitly discharged.
- [x] Domain examples remain distinct from catalog-layer admission.
- [x] N31+ selection is permitted but not required.
- [x] `agentic_ecology_demand_as_substrate_evidence` is explicitly blocked.
- [x] Naturalization is a preferred maturity direction, not an exploration
  prerequisite. AE01 may construct bounded ecology-side mechanisms to expose
  missing patterns, but must preserve their constructed evidence class and all
  applicable debt. Evidence: master-plan decision D-028.
- [ ] Add automated portable-path validation before the first committed
  machine-readable experiment artifact.
- [ ] Add automated unsafe-claim validation before the first positive AE01
  classification.
- [ ] Add source-role validation that distinguishes conceptual, inherited,
  constructed, report-only, and source-current records.

Iteration-wide blocked claims unless a later controlling contract explicitly
opens them:

```text
native shared-medium coordination
semantic communication or cooperation
agency or selfhood
sentience or consciousness
organism or life
native ant or colony agency
ecology regime
unrestricted autonomy
Phase 8 completion
agentic_ecology_demand_as_substrate_evidence
```

## 4. Phase 0 — Project architecture and decision freeze

### P0-I1 — Master directive synthesis

Entry condition:

- [x] The Post-N30 discussion and source-project boundary have been reviewed.
- [x] The four current project papers have been identified as conceptual
  sources.
- [x] The N29/N30 graph handoff role has been identified.

Required work:

- [x] Place the cross-cutting directive under `implementation/`.
- [x] Replace raw conversational prose with a maintained master plan.
- [x] Extend the plan across architecture, atlas execution, closeout,
  specification, implementation, and final handoff.
- [x] Record accepted decisions D-001 through D-024.
- [x] Record open and deferred decisions O-001 through O-010.
- [x] Define conversation as non-normative provenance rather than project
  authority.
- [x] Create this master checklist.
- [x] Review the master plan for acceptance, revision, or explicit objections.
  Evidence: revision 0.3 accepted by project owner on 2026-07-10.
- [x] Record the review result in the master-plan change log.

Iteration boundary:

```text
P0-I1 organizes directives only.
It does not initialize AE01, freeze an experiment contract, produce atlas
evidence, select N31, admit specifications, or authorize a general runtime.
```

Exit gate `P0-I1-GATE`:

- [x] Master-plan scope is accepted as full-program scope.
- [x] Decision IDs and conflict rules are accepted.
- [x] Checklist change-control rules are accepted.
- [x] Any requested changes have been applied and reviewed.

### P0-I2 — Blocking-decision resolution

Entry condition:

- [x] `P0-I1-GATE` passed.

AE01-blocking decisions:

- [x] Resolve O-004: canonical JSON serialization and digest convention.
  Evidence: master-plan decision D-025 and O-004 disposition.
- [x] Resolve O-005: Python types, JSON Schema, or dual-schema approach.
  Evidence: master-plan decision D-026 and O-005 disposition.
- [x] Resolve O-006: selected-output and large-artifact commit policy.
  Evidence: master-plan decision D-027 and O-006 disposition.
- [x] Resolve O-009: N31+ ranking dimensions, scoring, and tie/non-selection
  policy. Evidence: master-plan decision D-029 and O-009 disposition.
- [x] Resolve O-010: authored versus generated experiment reports. Evidence:
  master-plan decision D-030 and O-010 disposition.

Implementation-blocking decisions that MAY remain deferred until needed:

- [x] Resolve O-001: Python import package name. Evidence: master-plan decision
  D-031 and O-001 disposition.
- [x] Keep O-002 distribution name/version deferred. Evidence: master-plan
  decision D-032 and O-002 disposition; reopen at P4-I1 or before earlier
  installable-package metadata.
- [x] Resolve O-003: artifact inspection without runtime plus live execution
  only through an available compatible PyGRC installation. Evidence:
  master-plan decision D-033 and O-003 disposition.
- [x] Require replay-frozen realization profiles while keeping a general stable
  public/producer API deferred. Evidence: master-plan decision D-034 and O-007
  disposition; reopen at P4-I1 or earlier repeated cross-experiment use.
- [x] Make domain-package creation admission-driven and keep the unselected
  inventory deferred. Evidence: master-plan decision D-035 and O-008
  disposition; reopen for the selected domain after dedicated probe evidence.

Accepted decision evidence:

| Open item | Decision | Selected option | Reopening condition |
| --- | --- | --- | --- |
| O-004 | D-025 | PyGRC-compatible canonical JSON; separate semantic `output_digest` and exact-file `sha256` | A concrete non-Python LGRC implementation or independent AE artifact producer/verifier enters the roadmap |
| O-005 | D-026 | JSON Schema Draft 2020-12 for persisted shape; Python types and validators for implementation and semantic constraints | Changing persisted schema authority or dialect, or making a Python framework authoritative |
| O-006 | D-027 | Selected experiment-local evidence plus mandatory verified reconstruction for every declared artifact | Git LFS/external storage, non-reconstructable evidence, or materially revised size/retention policy becomes necessary |
| O-009 | D-029 | Eligibility gates plus anchored 0–3 scoring, deterministic tie handling, sensitivity checks, and explicit non-selection | Post-freeze scoring changes or a proposed discretionary/mandatory selection override |
| O-010 | D-030 | Generated projections or deterministic assembly of generated facts with separately authored bounded interpretation | Making manual final reports authoritative or changing a frozen report mode/source boundary |
| O-001 | D-031 | Python import root `rc_agentic_ecology` | A later cross-repository namespace or package rename requires migration |
| O-002 | D-032 | Explicitly deferred; no distribution or software version assigned | P4-I1 or any earlier need for installable-package metadata |
| O-003 | D-033 | Non-runtime artifact inspection plus strict installed-PyGRC runtime bindings with no silent constructed/native substitution | Any proposal for a pseudo-runtime, automatic fallback, API mirroring, or implicit binding migration |
| O-007 | D-034 | Replay-frozen mechanism contracts and explicit realization profiles; general API stability deferred; graph/PyGRC remains read-only from RCAE | P4-I1 reusable promotion or earlier when two independent retained consumers require the same boundary |
| O-008 | D-035 | Admission-driven domain-package creation; no predeclared inventory or empty domain placeholders | Phase 3 selects a domain and dedicated probe evidence supports reusable implementation |

Required decision-record behavior:

- [x] Record selected option and rejected alternatives. Evidence: master-plan
  O-001 through O-010 dispositions and decisions D-025 through D-035.
- [x] Record rationale and source basis. Evidence: each applicable disposition
  records conceptual, N29/N30, PyGRC-practice, or implementation-boundary basis.
- [x] Record reversibility and work affected. Evidence: disposition reopening
  conditions and affected artifacts, gates, packages, or compatibility surfaces.
- [x] Record the safe default for every deferred blocking decision. Evidence:
  D-032, D-034, and D-035 dispositions and deferred-work ledger.
- [x] Update the master-plan decision/open-decision tables. Evidence: plan
  revision 0.14.

Iteration boundary:

```text
P0-I2 chooses architecture and contract conventions only.
Incidental code must not silently decide open questions.
No choice in this iteration counts as atlas evidence or primitive admission.
```

Exit gate `P0-I2-GATE`:

- [x] Every Phase 1 blocking decision is accepted or explicitly deferred with a
  safe default.
- [x] No accepted choice conflicts with portability, read-only graph
  consumption, or claim discipline.
- [x] Master plan and checklist reflect the accepted decision state.
- [x] `P0-I2-GATE` passed. Evidence: plan/checklist revision 0.14, accepted by
  the project owner on 2026-07-10.

### P0-I3 — Minimum repository scaffold

Entry condition:

- [x] `P0-I2-GATE` passed.

Required work:

- [x] Create `experiments/README.md` with reconstruction and claim-boundary
  conventions. Evidence: experiment index at plan revision 0.16.
- [x] Create the Post-N30 atlas roadmap path. Evidence:
  `experiments/Post-N30-AgenticEcology-DemandCompositionAtlasRoadmap.md`.
- [x] Create the minimum AE01 experiment directory. Evidence:
  `experiments/2026-07-AE01-post-n30-demand-composition-atlas/README.md`.
- [x] Create only experiment subdirectories required by the accepted Phase 1
  work. Evidence: owned `contracts/`, `hypotheses/`, and `implementation/`
  indexes; no speculative configuration, script, report, or output paths.
- [x] Add `implementation/README.md` because the plan and checklist require an
  index.
- [x] Defer `specs/README.md` until the first promoted or explicitly conceptual
  operational contract owns that surface. Evidence: D-017 and the P0-I3
  iteration boundary.
- [x] Defer installable-package scaffolding because P0-I3 has no reusable source
  requirement. Evidence: D-032; reopen O-002 if P1 tooling requires
  installation.
- [x] Update the repository README map for the new experiment and implementation
  surfaces.
- [x] Verify no generated scaffold contains machine-local paths. Evidence:
  portability scan at revision 0.16.

Iteration boundary:

```text
P0-I3 creates navigable structure, not speculative empty architecture.
Directory creation does not admit the concepts named by those directories.
```

Exit gate `P0-I3-GATE`:

- [x] The minimum Phase 1 paths exist and are documented.
- [x] Every created path has an immediate owner and purpose.
- [x] No stable `src` API or positive research claim has been implied.
- [x] Repository navigation points to the master plan and checklist.
- [x] `P0-I3-GATE` passed. Evidence: revision 0.16 scaffold and portability
  verification.

### Phase 0 exit gate `P0-GATE`

- [x] `P0-I1-GATE` passed.
- [x] `P0-I2-GATE` passed.
- [x] `P0-I3-GATE` passed.
- [x] All AE01-blocking architecture decisions are accepted or safely deferred.
- [x] Phase 1 can proceed without deciding semantics through incidental code.
- [x] Mandatory Review R1 completed against the revision 0.16 scaffold.
  Evidence: D-037 and revision 0.17 R1 disposition.
- [x] `P0-GATE` passed. Evidence: revision 0.17, accepted by the project owner
  on 2026-07-10.

Phase 0 boundary:

```text
Passing P0-GATE establishes project architecture only.
It does not assign AE01-C0 or support any atlas, ecology, or implementation
claim.
```

## 5. Phase 1 — AE01 contract freeze

### P1-I1 — Source inventory and method admission

Entry condition:

- [x] `P0-GATE` passed.

Required conceptual-source records:

- [x] `papers/2026-06-FromStateToBecoming.md` recorded as ontology/method only.
- [x] `papers/2026-06-RC-AgenticEcology.md` recorded as ontology/method only.
- [x] `papers/2026-06-TheSharedMedium.md` recorded as ontology/method only.
- [x] `papers/2026-06-SharedMediumCoordination-EngineeringSpec.md` recorded as
  ontology/method/control vocabulary only.

Required graph-source records:

- [x] N29 closeout recorded as capability/debt/prototype bridge input.
- [x] N29 closeout output digest matches
  `fa21662f0a69d582bfe574311110f2610a21e6e4e352991823ce47280e0e8ff5`.
- [x] N29 A/B/C/D prototype classifications and composition-contract limits
  recorded.
- [x] All ten N29 closeout `source_artifacts` are recorded with portable path,
  source ID, output digest, file SHA-256, status, and acceptance state.
- [x] N30 closeout recorded at its exact supported participant and relation
  rungs.
- [x] N30 closeout output digest matches
  `7971163b1d7bd4027f5375270cfb2445cfe4698a8869b28e26f9273d0a5b5af6`.
- [x] N30 replay/control evidence and medium debt recorded.
- [x] Active N30+ handoff recorded as the continuation rule.
- [x] Later closeouts are confirmed to control the status of earlier evidence.

Canonical N29 source-artifact values to verify:

| Source ID | Output digest | File SHA-256 |
| --- | --- | --- |
| `i5_ecology_demand_matrix` | `2503831622cdfc99d9f6083bfc841481a06c6fd67bcba1a9ad840c1e1c069fe9` | `61eb618e966069bffd834bd8fa32cc26050972a21132ce32777abf5dd4667e5e` |
| `i6_capability_supply_atlas` | `8b80dcc636f8d3333f6e344bbf33ffc12eebe256e7ce2e4f19db33573a6e7181` | `ba0e32f9f7a4c064e6235fe9c306424daa5458c07c0b02f0c34e2d400da4d74b` |
| `i7_demand_supply_coverage_debt` | `6fa29aa7ff520acb733920bb711e498bb421b091f9b6575a7663bc5f21710985` | `4aadbba5f303e893ff5ead7ace2b6acd4054160f5f7c593699a59aae609587d8` |
| `i8_bridge_motif_library` | `5617368e38bc0b09ef5b152699948a967d7c5d72eae09467c4705749bb372ad0` | `abd0c077dca7b5158f1e5ca0eae8d0e7f6ba849ffcf4542d75b8ba237929f073` |
| `i9_motif_relabel_nulls` | `a6869a090698bf0c54601e34758408345eda978408a135c883fc495bf7c55a28` | `4cb75e44959ed1a9f6d67cb6e3f47f9cbe79cc43ca45a0d18a6c607e36f44eab` |
| `i10_prototype_admission_schema` | `fed49575d0ae9bc598d54cfbb6d01a87d69a3f8229fe466f580182b7e2c49f4d` | `f6a4c85c23822f7819a3c4be93fc742c66394140156f3125a286a2dc2bc89e40` |
| `i15_prototype_atlas` | `e139dd61fcd2b0998282033e5fe1a041891291d5db036982063e510be33f7cd2` | `1a810918df2923b5f5fe475ec9d0cc1f843fe614640b8149ea25173aab985a26` |
| `i16_minimal_probe_contract` | `d34e209f2b97aeac6242279f1c887afbf4c2064dcdc6a8fe0dc29cfa1275ac53` | `44fbe5b9547279012bcc35f89cb7b66864fc4f06a57ff2ea0e8c42e3dcbdd58f` |
| `i17_alternative_probe_contract` | `d2af854a4065351aaed23e74ac7c77dc7ec495765b32cccd69019b20e31c6798` | `3fed33e4fe040da5eb35374af0ed89510e4a8f7ba3bda93849a0ce3e4eaf92cc` |
| `i17a_full_bridge_probe_contract` | `f135650c01d2d74c3eb9c33e8b923542077beb8e7b2e723f36a2f7be1f68d981` | `bbdc9009626200f41ce993adfe7f1e557fb6d8ee1d1cb77666a94f317339af31` |

Required N29 debt carry-forward records:

- [x] `composed_ecology_runtime_harness_missing` carried as open outbound debt.
- [x] `producer_mediated_cross_prototype_handoff` carried as open bidirectional
  debt.
- [x] `medium_debt_and_nonzero_leakage_policy` carried as open bidirectional
  debt.
- [x] `ap4_ap5_gap_propagation` carried as open inbound N30+ debt.
- [x] `resource_economy_cooperation_exploitation_semantics` carried as open
  outbound debt.
- [x] `deviation_nativity_discharge` carried as open bidirectional debt.
- [x] Every debt records the N29 blocked claims and its AE01 disposition rule.

Required validation:

- [x] Every source has a portable identifier.
- [x] Every source has a declared role and consumption boundary.
- [x] Runtime-evidence permission is false for conceptual sources.
- [x] No positive AE01 evidence is opened by source admission.
- [x] Source digests or stable source revisions are recorded where required by
  the accepted artifact policy.

Iteration boundary:

```text
P1-I1 admits sources and method only.
It cannot support a pattern lane, composition, primitive, building block,
motif, regime, or N31 candidate.
```

Exit gate `P1-I1-GATE`:

- [x] All required sources exist and have consumption roles.
- [x] Source precedence and claim ceilings are unambiguous.
- [x] No conceptual source is counted as runtime evidence.
- [x] AE01-C1 source-inventory prerequisites are satisfied.
- [x] `P1-I1-GATE` passed. Evidence:
  `experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/source-inventory.md`.

### P1-I2 — AE01 roadmap and experiment boundary

Entry condition:

- [x] `P1-I1-GATE` passed.

Required roadmap content:

- [x] State the core Post-N30 question.
- [x] State the graph/ecology spiral role.
- [x] Define AE01 as a local experiment rather than graph N31.
- [x] Define all seven initial lanes.
- [x] Assign one stable ID to each accepted initial lane and use it consistently
  in the roadmap and AE01 README.
- [x] Cite N30 trace-conditioned eligibility, N29 Prototype B, N29 Prototype C,
  and ecology demand mapping as the motivation for Lane 1 without treating
  `niche` as an N30-supported label.
- [x] Cite the N29 nursery-demand debt row, N29 Prototype D, N22 susceptibility
  context, N28 generative/extractive discipline, and N30+ support redistribution
  as the motivation for Lane 4.
- [x] Define Lane 7 as parent-basin modulation demand and expected
  missing-surface classification, not a positive M3/M4 search.
- [x] Define the catalog hierarchy and primary-layer rule.
- [x] Define domain-role, placement, and domain-specific versus transferable
  classification without preselecting a domain package.
- [x] Define shared-medium and parent-basin ontology requirements.
- [x] Define debt and failure taxonomies.
- [x] Define N29/N30 consumption constraints.
- [x] Define expected cross-lane outputs.
- [x] Define AE01-C0 through AE01-C6.
- [x] Define finite positive, negative, blocked, incomplete, non-selection, and
  closeout classifications and stopping conditions.
- [x] Define rename behavior: stable IDs persist; initial and current display
  names, contract revision, and rationale remain visible.
- [x] State blocked claims.

Required AE01 README content:

- [x] Core question and status.
- [x] Source lanes and non-evidence sources.
- [x] Experiment phases and iteration order.
- [x] Reconstruction entry points, including their explicit pending status.
- [x] Output/report relationship.
- [x] Claim ceiling and unsafe relabels.
- [x] Handoff role to specs, implementation, and graph N31+.

Iteration boundary:

```text
P1-I2 defines what AE01 will ask and how it will close.
It does not answer the atlas questions or preselect a winning building block.
```

Exit gate `P1-I2-GATE`:

- [x] Roadmap and README agree on scope, lanes, gates, and non-claims.
- [x] Roadmap and README agree on every stable lane ID, display
  name, order, and inclusion state.
- [x] Every lane has a declared reason for inclusion.
- [x] The roadmap contains no positive lane result or fixed N31 selection.
- [x] AE01-C0 assigned without implying positive evidence.
- [x] `P1-I2-GATE` passed. Evidence:
  `experiments/Post-N30-AgenticEcology-DemandCompositionAtlasRoadmap.md` and
  `experiments/2026-07-AE01-post-n30-demand-composition-atlas/README.md`.

### P1-I3 — Machine and narrative contract freeze

Entry condition:

- [x] `P1-I2-GATE` passed.

Required common contracts:

- [x] Source inventory contract.
- [x] Pattern-card contract.
- [x] Machine-readable lane-registry contract.
- [x] Medium-surface declaration contract.
- [x] Requirement-extraction contract.
- [x] Composition-assessment contract.
- [x] Debt-record contract.
- [x] Claim-boundary and unsafe-flag contract.
- [x] Constructed-mechanism declaration contract.
- [x] Runtime-binding receipt and realization-profile contract.
- [x] Catalog/domain placement and field-applicability contract.
- [x] Lane terminal-classification and stopping contract.
- [x] N31+ ranking and non-selection contract.
- [x] Artifact manifest contract.
- [x] Evidence-use tier, shared-profile resolution, and fully materialized
  manifest contract.
- [x] Human-readable report projection contract.

Pattern-card required fields:

- [x] Pattern ID, primary catalog layer, and secondary observations.
- [x] Evidence-use tier and prohibition on scratch supporting classification or
  a gate.
- [x] Domain role, placement rationale, and domain-specific versus transferable
  boundary.
- [x] Explicit applicability status and rationale for every inapplicable common
  field; no silent omission.
- [x] Parent basin and persistence condition.
- [x] Local differentiations or participant carriers.
- [x] Shared medium and carrier surfaces.
- [x] Participant/medium separation or co-constitution account.
- [x] Reserve, cost, leakage, maintenance, and coherence economy.
- [x] Perturbation and source attribution.
- [x] Trace persistence, decay, reinforcement, and saturation.
- [x] Susceptibility and later continuation effect.
- [x] Possible co-response and parent-closure relevance.
- [x] N29 prototype/demand consumption.
- [x] N30-supported versus ecology-extrapolated legs.
- [x] Constructed ecology-side mechanisms and their evidence class.
- [x] For every construction: LGRC absence/tension, necessity, minimality,
  inputs/outputs, counterfactual, withdrawal test, debt, claim ceiling, and
  proposed graph-side discriminator.
- [x] Requested execution class and runtime-binding/realization-profile receipt,
  including required and observed identities and conformance status.
- [x] Missing or unsuitable graph surfaces and proposed future LGRC
  discriminators.
- [x] Missing requirements and composition interfaces.
- [x] Controls, debts, transfer scope, and failure modes.
- [x] Claim ceiling, blocked relabels, and N31+ implication.
- [x] Terminal classification, stopping condition, closure evidence, and clear
  separation of scientific result from incomplete or unavailable execution.

Lane-registry required fields:

- [x] Stable lane ID and accepted initial display name.
- [x] Current display name, order, and inclusion state.
- [x] Lane motivation and source-role references.
- [x] Rename contract revision and rationale when the display name changes.
- [x] Projection targets and consistency status for the roadmap and AE01 README.

Iteration boundary:

```text
P1-I3 freezes record shapes and evaluation rules.
Schema completeness is not a positive pattern result.
```

Exit gate `P1-I3-GATE`:

- [x] Required fields are machine-validatable.
- [x] Narrative reports cannot carry stronger claims than machine records.
- [x] Missing required evidence fails closed.
- [x] Contract versions and compatibility behavior are explicit.
- [x] `P1-I3-GATE` passed. Evidence:
  `experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/common-contract.md`,
  `experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/schemas/ae01-contract.schema.json`,
  and
  `experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/lane-registry.json`.

### P1-I4 — Hypothesis, control, and failure freeze

Entry condition:

- [x] `P1-I3-GATE` passed.

Required hypotheses:

- [ ] Niche-formation demand hypothesis.
- [ ] Pool co-conditioning demand hypothesis.
- [ ] Trail/stigmergic demand hypothesis.
- [ ] Nursery/support demand hypothesis.
- [ ] Boundary-exchange demand hypothesis.
- [ ] Capacity-circulation demand hypothesis.
- [ ] Parent-basin modulation demand and missing-surface hypothesis.
- [ ] Cross-lane recurring-requirement hypothesis.
- [ ] Non-selection hypothesis when no candidate meets the N31+ gate.

Required fail-closed controls:

- [ ] Conceptual paper relabeled as runtime evidence.
- [ ] N30 relabeled as coordination, agency, or ecology regime.
- [ ] N29 component success relabeled as composition success.
- [ ] Pre-given closed agent plus passive environment relabeled as RC ecology.
- [ ] Message bus/global variable disguised as medium.
- [ ] Surface annotation without functional dependence.
- [ ] Co-occurrence relabeled as composition.
- [ ] Hidden producer or cross-prototype handoff.
- [ ] Free trace, memory, movement, maintenance, or communication.
- [ ] Missing parent-basin context.
- [ ] Participant/medium boundary confusion.
- [ ] Premature semantic communication, cooperation, intention, or agency.
- [ ] Fixed N31 selection before synthesis.
- [ ] Agentic-ecology demand relabeled as substrate evidence.
- [ ] Constructed ecology-side mechanism relabeled as native LGRC evidence.
- [ ] Constructed mechanism admitted without necessity, minimality,
  counterfactual, withdrawal, debt, and discriminator declarations.
- [ ] Artifact inspection, mock behavior, or automatic fallback substituted for
  requested live PyGRC execution.
- [ ] Domain-shaped fixture or conceptual example relabeled as a reusable motif
  or admitted domain package.
- [ ] Incomplete or runtime-unavailable execution relabeled as a negative lane
  result or valid lane closure.

Required failure classifications:

- [ ] No primitive.
- [ ] Primitive visible but unstable.
- [ ] Producer-carried only.
- [ ] Medium absent.
- [ ] Proxy success.
- [ ] Fixture lock.
- [ ] Composition interference.
- [ ] Claim inflation.
- [ ] Regime fragmentation.
- [ ] Dormancy ambiguity.

Iteration boundary:

```text
P1-I4 predeclares what would support, block, or downgrade a result.
Controls must not be tuned after seeing lane conclusions without a recorded
contract revision and rerun.
```

Exit gate `P1-I4-GATE`:

- [ ] Every lane has finite positive, negative, blocked, and incomplete outcomes
  with explicit stopping conditions.
- [ ] Every unsafe relabel has a fail-closed control.
- [ ] Failure remains a valid catalog input rather than disappearing from the
  atlas.

### P1-I5 — Artifact, tooling, and reconstruction freeze

Entry condition:

- [ ] `P1-I4-GATE` passed.

Required work:

- [ ] Implement or select canonical serialization.
- [ ] Implement stable artifact digests.
- [ ] Implement schema validation.
- [ ] Implement portable-path guards.
- [ ] Implement source-role and claim-boundary guards.
- [ ] Define deterministic ID policy.
- [ ] Define artifact manifest generation.
- [ ] Define authored/generated report boundary.
- [ ] Define `exploratory_scratch`, `registered_probe`, and `retained_evidence`
  roles so only verified retained evidence can support a classification or gate.
- [ ] Implement versioned shared environment, command, resource, dependency,
  and realization profiles with deterministic fully resolved manifest views.
- [ ] Implement lane-registry validation for unique/stable IDs, complete initial
  scope, ordering, rename provenance, and narrative projection consistency.
- [ ] Define duplicate reconstruction expectations.
- [ ] Define selected-output commit policy.
- [ ] Define commands for regenerating each artifact family.
- [ ] Select and document the minimum repository-local tooling bootstrap; do not
  add distribution metadata unless O-002 is reopened first.
- [ ] Implement runtime-binding receipt and realization-profile conformance for
  requested live modes, including fail-closed missing/incompatible PyGRC.
- [ ] Generate a per-run runtime receipt at every live evidence-use tier; allow
  transient storage for non-evidential runs but never omit identity validation.
- [ ] Add conformance fixtures proving Markdown meaning, JSON Schema shape, and
  Python semantic validation remain within their divided authority.
- [ ] Verify all tooling and reconstruction paths preserve the read-only graph
  repository boundary.
- [ ] Add focused tests for all Phase 1 infrastructure.

Iteration boundary:

```text
P1-I5 implements experiment infrastructure only.
Tooling success does not support any atlas lane or reusable ecology mechanism.
```

Exit gate `P1-I5-GATE`:

- [ ] Representative empty/negative fixtures validate deterministically.
- [ ] Missing fields and incompatible schemas fail closed.
- [ ] Duplicate reconstruction produces stable canonical records.
- [ ] No generated record contains a machine-local path.
- [ ] Missing or incompatible PyGRC fails every requested live mode without
  fallback to artifact inspection, mock behavior, or another realization.
- [ ] No RCAE tooling, test, or reconstruction command writes into the graph
  repository.
- [ ] Scratch and transient registered-probe outputs fail any attempt to satisfy
  a classification or gate until promoted through verified D-027 retention.
- [ ] Missing, duplicate, stale, or reordered lane identities fail projection
  validation before P1-GATE.

### Phase 1 exit gate `P1-GATE`

- [x] `P1-I1-GATE` passed.
- [x] `P1-I2-GATE` passed.
- [x] `P1-I3-GATE` passed.
- [ ] `P1-I4-GATE` passed.
- [ ] `P1-I5-GATE` passed.
- [ ] AE01-C1 is assigned with evidence.
- [ ] AE01-C2 is assigned with evidence.
- [ ] Positive atlas conclusions remain unopened.
- [ ] The frozen machine lane registry and all narrative lane projections agree.

Phase 1 boundary:

```text
Passing P1-GATE authorizes lane execution only.
It does not support an atlas pattern, composition, N31 candidate, canonical
specification, or general source implementation.
```

## 6. Phase 2 — Atlas execution

### Common lane completion contract

Every lane iteration below MUST complete the same minimum work:

- [ ] Confirm all declared input sources and digests.
- [ ] Populate the complete pattern-card contract.
- [ ] Separate N30-supported and ecology-extrapolated legs.
- [ ] Record the parent basin and effect on parent closure.
- [ ] Record medium carrier, perturbation, cost, persistence, and susceptibility.
- [ ] Record N29 prototype and composition dependencies.
- [ ] Extract missing substrate requirements without treating demand as proof.
- [ ] Run all common controls and relevant lane-specific controls.
- [ ] Record failures, debt, transfer scope, and claim ceiling.
- [ ] Generate a machine artifact and matching human-readable report.
- [ ] Validate manifest, digest, portable paths, and unsafe-claim flags.
- [ ] Preserve negative and blocked rows in the atlas.

Common lane boundary:

```text
One lane may support a bounded ecology-side demand pattern or candidate
composition requirement. It cannot by itself support cross-lane recurrence,
general reusability, N31 selection, shared-medium coordination, agency, motif,
or regime claims.
```

Lane execution policy:

```text
After P1-GATE, P2-I1 through P2-I7 may execute independently or in parallel.
No lane may consume another lane's conclusion as evidence.
P2-I8 is the first iteration allowed to compare and synthesize lane results,
and it requires every lane exit gate to pass.
```

### P2-I1 — Minimal shared-medium niche formation lane

Entry condition:

- [ ] `P1-GATE` passed.

Required lane work:

- [ ] Define niche as shared-medium condition-space, not passive environment.
- [ ] Define how local identity formation, persistence, re-entry, cost, or
  susceptibility changes.
- [ ] Test participant/medium co-constitution versus pre-given-agent framing.
- [ ] Identify inhabitability/support thresholds without semantic niche claims.
- [ ] Apply the common lane completion contract.

Lane-specific boundary:

```text
Maximum intended result: bounded niche-conditioning demand pattern.
Blocked: ecological niche proof, population ecology, agency, organism, or regime.
```

Exit gate `P2-I1-GATE`:

- [ ] Niche pattern is classified as supported candidate, partial, blocked, or
  failed with explicit reasons.
- [ ] New requirements and debts are recorded.
- [ ] No stronger ecological relabel is opened.

### P2-I2 — Shared-pool co-conditioning lane

Entry condition:

- [ ] `P1-GATE` passed.

Required lane work:

- [ ] Define the shared carrier and access scope.
- [ ] Distinguish common substrate memory from database/mailbox semantics.
- [ ] Define accumulation, mixing, depletion, saturation, and leakage.
- [ ] Define how multiple perturbations condition later continuation.
- [ ] Apply the common lane completion contract.

Lane-specific boundary:

```text
Maximum intended result: bounded shared-pool co-conditioning demand pattern.
Blocked: collective memory, communication, resource economy, or coordination.
```

Exit gate `P2-I2-GATE`:

- [ ] Pool pattern and sharedness are classified.
- [ ] Mixing, leakage, and hidden-controller risks are recorded.
- [ ] New requirements and debts are recorded.

### P2-I3 — Trail or stigmergic field lane

Entry condition:

- [ ] `P1-GATE` passed.

Required lane work:

- [ ] Define route-support aftereffect rather than symbolic trail message.
- [ ] Define deposition cost, reinforcement, decay, saturation, and stale-trace
  failure.
- [ ] Define susceptibility-dependent route or continuation effects.
- [ ] Include trace shuffle, false-trace, freeze, and decay controls where
  admissible.
- [ ] Apply the common lane completion contract.

Lane-specific boundary:

```text
Maximum intended result: bounded trail/stigmergic demand pattern.
Blocked: pheromone semantics, communication, coordination, learning, or ant
ecology implementation.
```

Exit gate `P2-I3-GATE`:

- [ ] Trail pattern is classified.
- [ ] Trace functionality is distinguished from labels and passive storage.
- [ ] New requirements and debts are recorded.

### P2-I4 — Nursery or support field lane

Entry condition:

- [ ] `P1-GATE` passed.

Required lane work:

- [ ] Define support deficit, fragile/local identity condition, and admissible
  support carrier.
- [ ] Define how earlier activity changes later formation or stability.
- [ ] Separate generative support from semantic care or cooperation.
- [ ] Record parent-basin reserve and subsidy requirements.
- [ ] Apply the common lane completion contract.

Lane-specific boundary:

```text
Maximum intended result: bounded support-conditioned admissibility demand
pattern.
Blocked: care, altruism, cooperation, generative agency, reproduction, or life.
```

Exit gate `P2-I4-GATE`:

- [ ] Nursery/support pattern is classified.
- [ ] Support transfer, subsidy, and closure requirements are recorded.
- [ ] New requirements and debts are recorded.

### P2-I5 — Boundary-conditioned exchange lane

Entry condition:

- [ ] `P1-GATE` passed.

Required lane work:

- [ ] Define boundary as maintained selective coupling rather than wall.
- [ ] Define ingress, egress, transformation, delay, and permeability surfaces.
- [ ] Define exchange cost, leakage, rejection, and boundary repair.
- [ ] Distinguish boundary contact from shared-medium relation.
- [ ] Apply the common lane completion contract.

Lane-specific boundary:

```text
Maximum intended result: bounded boundary-conditioned exchange demand pattern.
Blocked: membrane semantics, organism identity, communication, or native
multi-basin exchange.
```

Exit gate `P2-I5-GATE`:

- [ ] Boundary/exchange pattern is classified.
- [ ] Permeability, leakage, and lineage requirements are recorded.
- [ ] New requirements and debts are recorded.

### P2-I6 — Capacity circulation lane

Entry condition:

- [ ] `P1-GATE` passed.

Required lane work:

- [ ] Define conserved or audited capacity/support surfaces.
- [ ] Define circulation, redistribution, depletion, replenishment, and leakage.
- [ ] Define maintenance floors and surplus conditions.
- [ ] Distinguish circulation from producer-mediated transfers and semantic
  resource exchange.
- [ ] Apply the common lane completion contract.

Lane-specific boundary:

```text
Maximum intended result: bounded capacity-circulation demand pattern.
Blocked: resource economy, cooperation/exploitation, metabolism, or native
ecology circulation.
```

Exit gate `P2-I6-GATE`:

- [ ] Capacity-circulation pattern is classified.
- [ ] Budget, leakage, and redistribution requirements are recorded.
- [ ] New requirements and debts are recorded.

### P2-I7 — Parent-basin modulation demand and missing-surface lane

Entry condition:

- [ ] `P1-GATE` passed.

Required lane work:

- [ ] Define the higher-order identity and persistence condition.
- [ ] Define reserve, pressure, cost, or affordance modulation shared across
  local differentiations.
- [ ] Define separable susceptibilities and compatible local responses.
- [ ] Distinguish parent-basin modulation from global variables and central
  commands.
- [ ] Test parent-basin separation and susceptibility controls where admissible.
- [ ] Apply the common lane completion contract.

Lane-specific boundary:

```text
Maximum intended result: bounded parent-basin modulation demand with explicit
missing/blocked source-current surface classification.
Positive M3/M4 evidence is not an expected AE01 outcome and remains blocked,
as do coordination, colony agency, and ecology regime claims.
```

Exit gate `P2-I7-GATE`:

- [ ] Parent-basin modulation demand and missing source-current surface are
  classified.
- [ ] Global-controller alternatives fail closed.
- [ ] New requirements and debts are recorded.

### P2-I8 — Cross-lane requirement and dependency synthesis

Entry condition:

- [ ] `P2-I1-GATE` passed.
- [ ] `P2-I2-GATE` passed.
- [ ] `P2-I3-GATE` passed.
- [ ] `P2-I4-GATE` passed.
- [ ] `P2-I5-GATE` passed.
- [ ] `P2-I6-GATE` passed.
- [ ] `P2-I7-GATE` passed.

Required work:

- [ ] Build the cross-pattern demand matrix.
- [ ] Build the composition/dependency graph.
- [ ] Build the recurring-requirement matrix.
- [ ] Build the N29 prototype-consumption map.
- [ ] Build the N30-supported/extrapolated-leg matrix.
- [ ] Classify prerequisite centrality and composition leverage.
- [ ] Identify conflicting timescales, budgets, carriers, and interfaces.
- [ ] Identify requirements already supplied versus genuinely missing.
- [ ] Preserve lane failures as downward-discovery inputs.

Iteration boundary:

```text
P2-I8 may identify recurring missing requirements.
It cannot yet select N31 or promote a canonical specification.
```

Exit gate `P2-I8-GATE`:

- [ ] Every synthesis row traces to lane records.
- [ ] Recurrence is distinguished from prerequisite value and testability.
- [ ] Composition co-occurrence is not treated as interaction evidence.
- [ ] Candidate requirements remain claim-bounded.

### P2-I9 — Control, replay, debt, and failure consolidation

Entry condition:

- [ ] `P2-I8-GATE` passed.

Required work:

- [ ] Run duplicate reconstruction for all required artifacts.
- [ ] Recompute cross-lane metrics from declared source records.
- [ ] Confirm all common controls fail closed.
- [ ] Confirm every lane-specific required control is present.
- [ ] Consolidate producer, medium, naturalization, semantic, transfer,
  composition, measurement, and claim debt.
- [ ] Consolidate failure taxonomy and unresolved observations.
- [ ] Validate all manifests and digests.
- [ ] Validate portable paths and source roles.
- [ ] Validate unsafe-claim flags.

Iteration boundary:

```text
P2-I9 validates and bounds the atlas evidence.
It does not itself turn demand records into graph-side primitive evidence.
```

Exit gate `P2-I9-GATE`:

- [ ] Required reconstruction and validation passes.
- [ ] No control fails open.
- [ ] No debt category is silently discharged.
- [ ] Any failed validation is classified and blocks affected downstream work.

### Phase 2 exit gate `P2-GATE`

- [ ] `P2-I1-GATE` through `P2-I9-GATE` passed.
- [ ] AE01-C3 is assigned with evidence.
- [ ] AE01-C4 is assigned with evidence.
- [ ] AE01-C5 is assigned with evidence.
- [ ] All lane and synthesis records preserve claim ceilings.

Phase 2 boundary:

```text
Passing P2-GATE supports an atlas evidence package only.
It does not itself select N31, admit reusable specs, or implement an ecology.
```

## 7. Phase 3 — Closeout, selection, and promotion

### P3-I1 — Candidate N31+ ranking and non-selection gate

Entry condition:

- [ ] `P2-GATE` passed.

Required work:

- [ ] Restrict scoring to eligible candidates after cross-lane synthesis.
- [ ] Record an independent qualitative mechanism rationale and any declared
  investigator-prior ordering for every eligible candidate.
- [ ] Rank candidates by cross-lane recurrence.
- [ ] Rank candidates by prerequisite centrality.
- [ ] Rank candidates by current evidence gap.
- [ ] Rank candidates by bounded source-current discriminator quality.
- [ ] Rank candidates by control feasibility.
- [ ] Rank candidates by composition leverage and transfer value.
- [ ] Rank candidates by potential debt discharge.
- [ ] Rank candidates by claim risk and implementation/evidence cost.
- [ ] Apply the declared tie policy.
- [ ] Apply the declared non-selection policy.
- [ ] Record sensitivity to reasonable scoring changes.
- [ ] Expose every disagreement between qualitative rationale, numeric ranking,
  tie procedure, and sensitivity result without allowing an implicit override.

Iteration boundary:

```text
The ranking is ecology-side demand guidance.
It is not LGRC evidence for the selected candidate.
```

Exit gate `P3-I1-GATE`:

- [ ] Ranking is reproducible from the synthesis artifacts.
- [ ] Frequency alone does not determine selection.
- [ ] Selected candidate or non-selection result has an explicit rationale.
- [ ] Unsafe semantic and implementation claims remain false.

### P3-I2 — Specification and implementation promotion queues

Entry condition:

- [ ] `P3-I1-GATE` passed.

Required work:

- [ ] Classify every result as promote to canonical spec, retain as candidate,
  send to further experiment, reject, or defer.
- [ ] Record the evidence envelope for each promotion candidate.
- [ ] Record required conformance tests.
- [ ] Record remaining debt and transfer limits.
- [ ] Record required LGRC bridge surfaces.
- [ ] Record required reusable source modules.
- [ ] Record domain probes enabled or still blocked.
- [ ] Ensure rejected/failed candidates remain in the historical atlas.

Iteration boundary:

```text
A promotion queue authorizes scoped follow-up work.
It does not mean the specification or implementation already exists.
```

Exit gate `P3-I2-GATE`:

- [ ] Every AE01 output has exactly one explicit disposition.
- [ ] No promoted item exceeds its evidence envelope.
- [ ] Dependencies and ordering are explicit.

### P3-I3 — AE01 closeout and bidirectional handoff

Entry condition:

- [ ] `P3-I2-GATE` passed.

Required work:

- [ ] Produce final atlas classification report.
- [ ] Produce final machine-readable closeout.
- [ ] Record final AE01 ladder rung.
- [ ] Record N31+ candidate or non-selection.
- [ ] Produce graph-side primitive/building-block demand handoff.
- [ ] Produce ecology-side spec/implementation handoff.
- [ ] Record remaining open debt and blocked claims.
- [ ] Record all source and output digests.
- [ ] Confirm graph repository source diff remains absent from this work.
- [ ] Update roadmap and active handoff pointers.

Iteration boundary:

```text
AE01 closeout is an atlas/handoff result.
It is not an executed ecology runtime, native coordination, agency, motif, or
regime closeout.
```

Exit gate `P3-I3-GATE`:

- [ ] AE01-C6 is supported.
- [ ] All required closeout artifacts and handoffs exist.
- [ ] Claims, debts, failures, and transfer scope are internally consistent.

### Phase 3 exit gate `P3-GATE`

- [ ] `P3-I1-GATE` passed.
- [ ] `P3-I2-GATE` passed.
- [ ] `P3-I3-GATE` passed.
- [ ] AE01 is closed without unsafe promotion.
- [ ] Phase 4 work is bounded by an explicit promotion queue.

## 8. Phase 4 — Canonical specifications and reusable implementation

Phase 4 is a provisional implementation envelope, not a preselected backlog.
Its iteration details MUST be reviewed and revised from the Phase 3 promotion
queue before execution. No Phase 4 component, motif, regime, or domain runtime
may be implemented before AE01 closeout, except narrowly approved
infrastructure required by a frozen AE01 contract. A conditional item may be
dispositioned as deferred only with a reason and reopening gate.

### P4-I1 — Package and quality foundation

Entry condition:

- [ ] `P3-GATE` passed, or an earlier infrastructure exception is documented by
  a frozen AE01 contract.

Required work:

- [ ] Resolve package import and distribution names.
- [ ] Add `pyproject.toml` with supported Python version and dependency groups.
- [ ] Create the minimum `src` package.
- [ ] Define public versus research-tooling import surfaces.
- [ ] Define error and validation conventions.
- [ ] Configure formatting, linting, typing, and tests.
- [ ] Configure deterministic test and artifact environments.
- [ ] Document dependency and compatibility policy.
- [ ] Add continuous verification if/when repository workflow policy permits.

Iteration boundary:

```text
Package infrastructure is not evidence of any ecology capability.
```

Exit gate `P4-I1-GATE`:

- [ ] Clean install succeeds in the declared environment.
- [ ] Import smoke tests pass.
- [ ] Formatting, linting, typing, and focused tests pass.
- [ ] No speculative public API is implied.

### P4-I2 — Core catalog, artifact, provenance, and debt model

Entry condition:

- [ ] `P4-I1-GATE` passed.

Required work:

- [ ] Implement stable identifiers and canonical serialization.
- [ ] Implement evidence references and source-role types.
- [ ] Implement catalog-layer and maturity types.
- [ ] Implement claim ceilings and blocked-relabel guards.
- [ ] Implement all required debt records.
- [ ] Implement transfer and composition scope records.
- [ ] Implement artifact manifests and digests.
- [ ] Implement schema restoration and compatibility failures.
- [ ] Add unit, contract, round-trip, and negative tests.

Iteration boundary:

```text
Core records describe evidence and contracts; they do not create evidence.
```

Exit gate `P4-I2-GATE`:

- [ ] Canonical round trips are deterministic.
- [ ] Missing/incompatible evidence fails closed.
- [ ] Claim and debt metadata survive serialization.
- [ ] Contract tests pass.

### P4-I3 — Canonical specification set

Entry condition:

- [ ] `P4-I2-GATE` passed.

Required work for every promoted spec:

- [ ] State catalog layer and purpose.
- [ ] State required primitives and inputs.
- [ ] State carrier and medium-surface semantics.
- [ ] State dynamics generator and invariants.
- [ ] State composition inputs and outputs.
- [ ] State budget, lineage, timing, and transfer rules.
- [ ] State positive signatures and mandatory controls.
- [ ] State failure modes and debt.
- [ ] State claim ceiling and blocked relabels.
- [ ] State conformance tests and evidence sources.
- [ ] Version the specification.

Iteration boundary:

```text
A canonical spec admits a reusable contract within its evidence envelope.
It does not imply that a conforming implementation exists or is native.
```

Exit gate `P4-I3-GATE`:

- [ ] Every promoted spec passes completeness review.
- [ ] Every spec cites its controlling evidence.
- [ ] No spec promotes a stronger claim than its source closeout.

### P4-I4 — LGRC bridge specification and adapter

Entry condition:

- [ ] `P4-I3-GATE` passed for the required bridge contracts.

Required specification work:

- [ ] Define installed-runtime and/or artifact-only consumption modes.
- [ ] Define accepted public model, snapshot, telemetry, and artifact surfaces.
- [ ] Define capability and schema negotiation.
- [ ] Define source-current/inherited/constructed/report-only preservation.
- [ ] Define lineage, digest, claim, debt, replay, and transfer preservation.
- [ ] Define missing-field and incompatible-version failure behavior.
- [ ] Define read-only and no-checkout-path requirements.

Required implementation work:

- [ ] Implement substrate-neutral bridge protocols.
- [ ] Implement selected public `pygrc` adapters if admitted.
- [ ] Implement selected portable-artifact adapters if admitted.
- [ ] Implement provenance and lineage validation.
- [ ] Implement fail-closed compatibility errors.
- [ ] Add fixture, replay, round-trip, and negative integration tests.
- [ ] Verify no graph repository mutation or path dependence.

Iteration boundary:

```text
The bridge transports bounded evidence and state surfaces.
It does not upgrade LGRC claims or establish ecology composition success.
```

Exit gate `P4-I4-GATE`:

- [ ] All admitted bridge modes conform to their specs.
- [ ] Provenance, claim, debt, and lineage survive consumption.
- [ ] Missing and unsafe inputs fail closed.
- [ ] Read-only integration tests pass.

### P4-I5 — Promoted primitive implementations

Entry condition:

- [ ] `P4-I3-GATE` passed for each selected primitive.
- [ ] Required bridge/core dependencies pass their gates.

For each promoted primitive:

- [ ] Implement the smallest contract-conforming abstraction.
- [ ] Preserve maturity and nativity as separate axes.
- [ ] Implement positive and negative fixtures.
- [ ] Implement serialization and telemetry.
- [ ] Implement conformance, replay, and transfer tests required by the spec.
- [ ] Record remaining debt and claim ceiling.
- [ ] Add an example only if it cannot be mistaken for stronger evidence.

Iteration boundary:

```text
Primitive implementation supports only the primitive's admitted distinction.
It does not establish a reusable building block, motif, regime, or agency.
```

Exit gate `P4-I5-GATE`:

- [ ] Every selected primitive conforms to its spec.
- [ ] Every non-implemented promotion item is explicitly deferred.
- [ ] No primitive is promoted by directory placement alone.

### P4-I6 — Promoted building-block implementations

Entry condition:

- [ ] Required primitive gates passed.
- [ ] Required building-block specs passed `P4-I3-GATE`.

For each promoted building block:

- [ ] Implement structural condition and dynamics generator.
- [ ] Implement composition inputs and outputs.
- [ ] Implement budget, timing, carrier, and lineage invariants.
- [ ] Implement isolated controls and combined controls.
- [ ] Test transfer scope and declared failure modes.
- [ ] Test hidden-producer and medium-debt guards.
- [ ] Record maturity, remaining debt, and claim ceiling.

Iteration boundary:

```text
Building-block success does not establish a domain motif or ecology regime.
```

Exit gate `P4-I6-GATE`:

- [ ] Every selected block conforms to its spec.
- [ ] Composition interfaces are executable and tested.
- [ ] Fixture lock and composition interference are classified.

### P4-I7 — Motif probes and implementations

Entry condition:

- [ ] Required building-block gates passed.
- [ ] A motif contract and evidence plan exist.

For each promoted motif:

- [ ] Define the domain-shaped pattern and parent basin.
- [ ] Compose required blocks through visible interaction terms.
- [ ] Run separable component controls.
- [ ] Run combined composition controls.
- [ ] Test timescale, budget, carrier, and susceptibility compatibility.
- [ ] Record producer/message scaffolds and debt.
- [ ] Record motif claim ceiling and blocked regime relabels.

Iteration boundary:

```text
A motif is a domain-shaped controlled composition.
It is not an integrated parent-basin regime, organism, or agent.
```

Exit gate `P4-I7-GATE`:

- [ ] Every selected motif has controlled composition evidence or an explicit
  failure classification.
- [ ] No motif is promoted from plausible interpretation alone.

### P4-I8 — Regime and domain ecology probes

Entry condition:

- [ ] Required motif gates passed.
- [ ] A dedicated regime evidence contract exists.

For each promoted regime/domain probe:

- [ ] Define parent-basin persistence and boundary.
- [ ] Define cross-time continuity and turnover.
- [ ] Define internal differentiation and shared-medium integration.
- [ ] Define reserve, perturbation, recovery, and fragmentation tests.
- [ ] Define boundary exchange and generative/extractive effects.
- [ ] Run persistence, perturbation, turnover, recovery, and separation controls.
- [ ] Record regime claim ceiling and all biological/agency blocked claims.

Iteration boundary:

```text
Regime-candidate evidence does not automatically establish life, organism
identity, agency, sentience, or consciousness.
```

Exit gate `P4-I8-GATE`:

- [ ] Selected regime/domain probes are classified through dedicated evidence.
- [ ] Fragmented motifs are not promoted to regimes.
- [ ] Unsupported semantic and biological claims remain blocked.

### P4-I9 — Telemetry, examples, documentation, and public surfaces

Entry condition:

- [ ] Required promoted implementation gates passed.

Required work:

- [ ] Define telemetry contracts for admitted surfaces.
- [ ] Provide artifact-driven reports and visualizations where they materially
  aid inspection.
- [ ] Provide examples separated from evidence claims.
- [ ] Document stable versus research-tooling APIs.
- [ ] Document bridge setup without checkout-specific paths.
- [ ] Document reconstruction and replay commands.
- [ ] Update repository README, specs index, experiment index, and source API
  index.
- [ ] Verify publication and license metadata for new surfaces.

Iteration boundary:

```text
Documentation, examples, and visuals explain admitted behavior.
They do not add evidence unless a controlling experiment consumes them.
```

Exit gate `P4-I9-GATE`:

- [ ] Documentation matches actual contracts and APIs.
- [ ] Examples and visuals preserve claim boundaries.
- [ ] All public links and portable identifiers validate.

### P4-I10 — Full verification and implementation closeout

Entry condition:

- [ ] All required Phase 4 promotion items are implemented or explicitly
  deferred.

Required verification:

- [ ] Formatting passes.
- [ ] Linting passes.
- [ ] Static typing passes at the declared strictness.
- [ ] Unit tests pass.
- [ ] Contract tests pass.
- [ ] Integration tests pass.
- [ ] Replay and round-trip tests pass.
- [ ] Transfer tests pass where required.
- [ ] Portable-path and provenance guards pass.
- [ ] Claim-boundary and unsafe-relabel guards pass.
- [ ] Required experiment reconstruction checks pass.
- [ ] Documentation and examples execute where applicable.
- [ ] Working tree contains no unintended generated or unrelated changes.

Required closeout:

- [ ] Record implemented, deferred, rejected, and superseded items.
- [ ] Record final evidence and maturity states.
- [ ] Record remaining debt and open failures.
- [ ] Record compatibility and public API status.
- [ ] Produce Phase 4 closeout and next-step handoff.

Iteration boundary:

```text
Implementation closeout proves conformance to admitted contracts.
It does not promote claims beyond the experiments and specifications that
control those contracts.
```

Exit gate `P4-I10-GATE`:

- [ ] All required verification passes.
- [ ] All conditional work has an explicit disposition.
- [ ] Phase 4 closeout is internally consistent and claim-clean.

### Phase 4 exit gate `P4-GATE`

- [ ] `P4-I1-GATE` through `P4-I4-GATE` passed where required.
- [ ] `P4-I5-GATE` through `P4-I9-GATE` passed or explicitly dispositioned
  according to the Phase 3 promotion queue.
- [ ] `P4-I10-GATE` passed.
- [ ] Canonical specs and source implementations remain aligned.
- [ ] Required reusable surfaces are implemented, or deferral is explicit.

## 9. Final Post-N30 program closeout

### FINAL-I1 — Program synthesis and handoff

Entry condition:

- [ ] `P3-GATE` passed.
- [ ] `P4-GATE` passed.

Required work:

- [ ] Summarize architecture and decision changes since revision 0.1.
- [ ] Summarize AE01 findings and final ladder rung.
- [ ] Summarize N31+ selection/non-selection and graph-side status.
- [ ] Summarize canonical specifications and implementation status.
- [ ] Summarize bridge capabilities and limitations.
- [ ] Summarize primitive, building-block, motif, regime, and domain status.
- [ ] Summarize all remaining debt and blocked claims.
- [ ] Produce the next active graph/ecology spiral handoff.
- [ ] Update active roadmap, handoff, README, and index pointers.
- [ ] Mark superseded program directives without deleting their history.

Final boundary:

```text
Program completion reports what was actually admitted, implemented, and
verified. It does not collapse remaining claim boundaries or debt.
```

Exit gate `FINAL-GATE`:

- [ ] Every master-plan completion criterion has evidence.
- [ ] All phases have passed or have explicit bounded dispositions.
- [ ] Final closeout and next active handoff exist.
- [ ] Master plan and checklist are marked completed or superseded.

## 10. Implementation coverage matrix

This matrix provides a shorter view of the implementation work detailed in
Phase 4.

| Implementation surface | Contract required | Code required | Verification required | Current status |
| --- | --- | --- | --- | --- |
| Packaging and quality configuration | Yes | Yes | Install/import/lint/type/test | Pending |
| Stable IDs and canonical serialization | Yes | Yes | Round-trip/digest | Contract shape frozen; code/verification pending |
| Evidence provenance and source roles | Yes | Yes | Negative/compatibility | Contract shape frozen; code/verification pending |
| Debt and claim-boundary model | Yes | Yes | Fail-closed claim tests | Contract shape frozen; code/verification pending |
| Artifact manifests and schema restoration | Yes | Yes | Replay/round-trip | Contract shape frozen; code/verification pending |
| LGRC runtime/artifact bridge | Yes | Conditional modes | Integration/read-only | Runtime-binding shape frozen; implementation pending |
| Primitive catalog implementations | Per promotion queue | Conditional | Contract/replay/transfer | Blocked by AE01 |
| Building-block implementations | Per promotion queue | Conditional | Composition/control | Blocked by AE01 |
| Motif implementations | Dedicated motif contract | Conditional | Combined controls | Blocked by blocks |
| Regime/domain probes | Dedicated regime contract | Conditional | Persistence/recovery | Blocked by motifs |
| Telemetry and reports | Yes | Yes for admitted surfaces | Artifact comparison | Report-projection shape frozen; implementation pending |
| Examples and public documentation | Yes | Conditional | Execution/link checks | Pending |

## 11. Required indexes and traceability records

- [ ] Project directive index.
- [ ] Experiment index.
- [ ] Specification index.
- [ ] Source/public API index.
- [ ] Decision-to-document traceability table.
- [ ] Experiment-output-to-specification promotion table.
- [ ] Specification-to-source conformance table.
- [ ] Source-to-test coverage table.
- [ ] Debt discharge and carry-forward ledger.
- [ ] Active roadmap and handoff pointer.

## 12. Review checkpoints

Mandatory review points:

- [x] Review R0 after master-plan/checklist acceptance. Evidence: revision 0.3
  accepted by project owner on 2026-07-10.
- [x] Review R1 before `P0-GATE`. Evidence: project-owner review of the P0-I2
  decision lattice, D-037 disposition, and revision 0.16 scaffold audit.
- [ ] Review R2 before AE01 contract freeze at `P1-GATE`.
- [ ] Review R3 after the first completed lane to assess contract adequacy
  without tuning conclusions.
- [ ] Review R4 before cross-lane synthesis.
- [ ] Review R5 before N31+ selection/non-selection.
- [ ] Review R6 before specification promotion.
- [ ] Review R7 before stable source API promotion.
- [ ] Review R8 before final program closeout.

Review rule:

```text
A review may revise future work.
A review may reopen completed work when a controlling assumption changes.
A review may not retroactively preserve conclusions whose gates are no longer
satisfied.
```

## 13. Deferred-work ledger

Use this section when checking a conditional item as deferred.

| Item ID | Decision | Reason | Preserved boundary | Reopening condition | Status |
| --- | --- | --- | --- | --- | --- |
| O-002 | D-032 | Distribution identity would be premature before an installable package exists. | No distribution or software-release meaning is inferred from repository publication version `0.1`. | P4-I1 or any earlier installable-package requirement. | Deferred with safe default |
| O-007 | D-034 | AE01 has replayable mechanism boundaries but insufficient repeated use pressure for a general producer/plugin API. | Explicit realization profiles, replay compatibility, no silent substitution, and strict read-only graph consumption. | P4-I1 reusable promotion or two independent retained consumers requiring the same boundary. | Partially resolved; general API deferred |
| O-008 | D-035 | Conceptual domain examples and experiment-local fixtures do not establish a reusable package inventory. | Domain packages require promotion and dedicated probe evidence; no empty placeholders. | A Phase 3-selected domain has dedicated evidence supporting reusable implementation. | Partially resolved; unselected inventory deferred |

## 14. Blocked-work ledger

| Item ID | Blocker | First observed | Attempts/alternatives | Required change | Status |
| --- | --- | --- | --- | --- | --- |
| — | — | — | — | — | Empty |

## 15. Evidence links for completed gates

| Gate | Evidence | Date | Reviewer/status |
| --- | --- | --- | --- |
| P0-I1-GATE | Master plan and checklist revision 0.3; all P0-I1 exit items checked | 2026-07-10 | Accepted by project owner; passed |
| P0-I2-GATE | Master plan and checklist revision 0.14; O-001 through O-010 dispositioned with decisions D-025 through D-035 and explicit safe defaults | 2026-07-10 | Accepted item-by-item by project owner; passed |
| P0-I3-GATE | Revision 0.16 experiment/implementation indexes, Post-N30 roadmap, AE01 workspace, owned Phase 1 paths, README navigation, and portability scan | 2026-07-10 | Self-audited; passed |
| P0-GATE | Revision 0.17; P0-I1 through P0-I3 passed; Review R1 accepted as D-037 with no P0-I2 reopening | 2026-07-10 | Accepted by project owner; passed |
| P1-I1-GATE | Revision 0.19 narrative source inventory; verified paper, N29, N30, and active N30+ identities, roles, precedence, debts, and claim ceilings | 2026-07-10 | Self-audited; passed pending later R2 review of the full Phase 1 freeze |
| P1-I2-GATE | Revision 0.20 roadmap and AE01 README; stable lane projection, atlas outline, ontology, taxonomies, terminal states, outputs, and claim boundaries | 2026-07-10 | Self-audited; passed pending later R2 review of the full Phase 1 freeze |
| P1-I3-GATE | Revision 0.21 common meaning contract, JSON Schema Draft 2020-12 bundle, and controlling machine lane registry | 2026-07-10 | Self-audited; passed pending later R2 review of the full Phase 1 freeze |
| P1-GATE | Pending | — | Open; P1-I4 ready |
| P2-GATE | Pending | — | Blocked |
| P3-GATE | Pending | — | Blocked |
| P4-GATE | Pending | — | Blocked |
| FINAL-GATE | Pending | — | Blocked |

## 16. Checklist change control

Changes are expected as the work exposes better distinctions. They must remain
visible and traceable.

Before an iteration contract freezes:

- requirements MAY be added, removed, split, or reordered;
- the change log MUST record why;
- affected dashboard and entry-gate status MUST be updated.

After an iteration contract freezes:

- the controlling contract version MUST change;
- the affected iteration MUST be reopened;
- affected controls and artifacts MUST be rerun;
- downstream synthesis or closeout relying on the old contract MUST be reopened
  or explicitly shown unaffected;
- the old record MUST remain available as superseded history.

Change-record fields:

```text
change_id
date
requested_change
reason and source
affected decisions
affected checklist items and gates
affected artifacts/specs/code/tests
replay or rerun required
claim/debt impact
status
```

Change log:

| Change ID | Date | Summary | Affected gates | Status |
| --- | --- | --- | --- | --- |
| CL-001 | 2026-07-10 | Created full-program checklist baseline revision 0.1. | P0-I1-GATE onward | Superseded by CL-002 |
| CL-002 | 2026-07-10 | Revision 0.2 applied external review: exact N29 debt/digest traceability, demand-as-evidence blocker, safer Lane 7, parallel lane execution, and provisional Phase 4 boundary. | P0-I1-GATE onward | Superseded by CL-003 |
| CL-003 | 2026-07-10 | Revision 0.3 added symmetric N30 closeout-digest traceability and corrected the accepted-decision range through D-024. | P0-I1-GATE onward | Superseded by CL-004 |
| CL-004 | 2026-07-10 | Revision 0.4 resolved O-004 as D-025: PyGRC-compatible canonical JSON now, with language-neutral canonicalization deferred to a concrete non-Python interoperability need. | P0-I2-GATE onward | Superseded by CL-005 |
| CL-005 | 2026-07-10 | Revision 0.5 resolved O-005 as D-026: JSON Schema Draft 2020-12 governs persisted shape while Python types and validators implement runtime and semantic constraints. | P0-I2-GATE onward | Superseded by CL-006 |
| CL-006 | 2026-07-10 | Revision 0.6 resolved O-006 as D-027: selected historical evidence and mandatory verified artifact-level reconstruction, including omitted large artifacts. | P0-I2-GATE onward | Superseded by CL-007 |
| CL-007 | 2026-07-10 | Revision 0.7 accepted D-028: naturalization remains preferred but AE01 may use bounded constructed mechanisms to expose missing patterns in the bidirectional graph/ecology spiral. | P0-I2-GATE onward | Superseded by CL-008 |
| CL-008 | 2026-07-10 | Revision 0.8 resolved O-009 as D-029: gated consume/extend/introduce candidate ranking with fixed thresholds, sensitivity checks, and explicit non-selection. | P0-I2-GATE onward | Superseded by CL-009 |
| CL-009 | 2026-07-10 | Revision 0.9 resolved O-010 as D-030: generated projections or deterministic assembly of generated facts with separately authored bounded interpretation. | P0-I2-GATE onward | Superseded by CL-010 |
| CL-010 | 2026-07-10 | Revision 0.10 resolved O-001 as D-031: the Python import root is `rc_agentic_ecology`, independently of distribution and compatibility policy. | P0-I2-GATE onward | Superseded by CL-011 |
| CL-011 | 2026-07-10 | Revision 0.11 accepted D-032: distribution name and software version remain deferred and distinct from repository publication version `0.1`. | P0-I2-GATE onward | Superseded by CL-012 |
| CL-012 | 2026-07-10 | Revision 0.12 resolved O-003 as D-033: artifact inspection remains non-runtime while live execution requires explicit compatible local PyGRC bindings with no silent constructed/native transition. | P0-I2-GATE onward | Superseded by CL-013 |
| CL-013 | 2026-07-10 | Revision 0.13 partially resolved O-007 as D-034: replay-frozen realization profiles govern AE01, a general API remains deferred, and no RCAE workflow may modify the graph/PyGRC repository. | P0-I2-GATE onward | Superseded by CL-014 |
| CL-014 | 2026-07-10 | Revision 0.14 partially resolved O-008 as D-035 with admission-driven domain packages and no predeclared inventory; the complete decision audit passed P0-I2-GATE. | P0-I2-GATE onward | Superseded by CL-015 |
| CL-015 | 2026-07-10 | Revision 0.15 accepted D-036, corrected stale gate/dependency bookkeeping, and added explicit Phase 1 guardrails for constructed mechanisms, runtime bindings, tooling bootstrap, domain placement, applicability, artifact roles, and bounded lane closure. | P0-I3-GATE and P1-GATE onward | Superseded by CL-016 |
| CL-016 | 2026-07-10 | Revision 0.16 completed P0-I3 with the minimum owned scaffold and navigation, while explicitly deferring specs, source packaging, and execution/output paths. | P0-I3-GATE onward | Superseded by CL-017 |
| CL-017 | 2026-07-10 | Revision 0.17 accepted D-037 as the R1 resolution: ceremony scales with evidential use while safety remains fixed; shared profiles, generated receipts, experiment-local construction sharing, schema-drift controls, and qualitative ranking rationale reduce compliance friction. P0-GATE passed. | P0-GATE and P1-GATE onward | Superseded by CL-018 |
| CL-018 | 2026-07-10 | Revision 0.18 aligned the experiment reconstruction summary with D-027 and added Phase 1 stable lane IDs, a single machine lane registry, rename provenance, and narrative projection validation. Completed Phase 0 gates remain closed. | P1-I2-GATE onward | Superseded by CL-019 |
| CL-019 | 2026-07-10 | Revision 0.19 passed P1-I1 with a verified narrative source inventory, explicit mutable-roadmap provenance, all N29 debts carried, and N30 bounded at P2/M2. No AE01 rung or positive result opened. | P1-I1-GATE onward | Superseded by CL-020 |
| CL-020 | 2026-07-10 | Revision 0.20 passed P1-I2 with a complete atlas content outline, stable lane IDs, source motivations, ontology and placement rules, debt/failure/terminal taxonomies, stopping conditions, and aligned narrative projections. `AE01-C0` assigned without positive evidence. | P1-I2-GATE onward | Superseded by CL-021 |
| CL-021 | 2026-07-10 | Revision 0.21 passed P1-I3 with one normative meaning contract, a discriminated schema bundle for seventeen closed record shapes, and the controlling seven-lane registry. Semantic validators and automated projection checks remain P1-I5 work; no positive evidence or higher rung opened. | P1-I3-GATE onward | Active |

## 17. Current next actions

The next unchecked actions in dependency order are:

1. [ ] Complete P1-I4 hypothesis, control, and failure freeze.
2. [ ] Freeze all lane, synthesis, and non-selection hypotheses.
3. [ ] Pass `P1-I4-GATE` without executing a lane or opening positive evidence.
