# AE01 P1-I1 Source Inventory and Method Admission

**Status:** accepted P1-I1 narrative source-admission record

**Evidence effect:** no positive AE01 evidence opened

**Machine contract status:** deferred to P1-I3

**Verification date:** 2026-07-10

## 1. Purpose and authority

This record admits the conceptual method sources and graph-project evidence
needed to freeze AE01. Admission means only that a source has a declared role,
identity, precedence, claim ceiling, and consumption boundary. It does not
support an AE01 lane, composition, primitive, building block, motif, regime, or
N31+ candidate.

The master plan and checklist remain the program authority. Graph artifacts
retain their graph-side evidence scope. Conceptual papers remain ontology and
method sources only.

## 2. Portable source identifiers and verification baseline

Committed records use repository identities and repository-relative paths:

```text
rcae:<repository-relative path>
grc:<repository-relative path>
```

These identifiers do not assume sibling checkout placement. Local verification
used clean source trees at:

| Repository ID | Verified Git revision | Worktree state | Role |
| --- | --- | --- | --- |
| `rcae` | `868faae55f99e4a84145e0ca107739bc91556d01` | clean before P1-I1 edits | Conceptual source file-digest baseline |
| `grc` | `1f42cb1d1e591159afc2ca54cc656b574d41c8d3` | clean | Graph evidence and current continuation baseline |

The graph revision identifies the source snapshot; no machine-local checkout
path is part of source identity. The graph repository was read only throughout
verification.

## 3. Source precedence

When sources differ or evolve, AE01 applies this order:

1. A later graph closeout or explicit active handoff controls the current
   status of earlier graph evidence.
2. A graph closeout's machine artifact controls its report, README, and roadmap
   summary for that experiment's evidence and claim ceiling.
3. Source-current graph artifacts control positive graph evidence; roadmap and
   candidate documents provide orientation only.
4. RCAE conceptual papers provide ontology, method, and control vocabulary but
   never runtime evidence.
5. Future AE01 claims require AE01's own frozen contracts, artifacts, controls,
   and closeout; source admission alone cannot open them.

At the verified graph revision, N30 is the latest numbered graph closeout. No
N31 experiment directory or N31 closeout is present. The active N30+ handoff
explicitly records `candidate_n31_selected = false` and
`next_lgrc_experiment_fixed = false`.

Before Phase 2 execution and at every source-current review, a later graph
closeout or replacement active handoff must be detected. If one exists, this
inventory and every affected contract or gate must be revised before its claims
are consumed.

## 4. Conceptual and method sources

All four papers have `runtime_evidence_permission = false` and
`positive_AE01_evidence_permission = false`.

| Portable source ID | File SHA-256 | Admitted role | Consumption boundary |
| --- | --- | --- | --- |
| `rcae:papers/2026-06-FromStateToBecoming.md` | `1d1c956150c45950a5ac2ec9ed0034bb5bcfb5fdd90cfad1ced7f6d709b71055` | Ontology and probe/cultivation method | May define geometry, flux, support, debt, and probe vocabulary; cannot establish implementation or runtime behavior. |
| `rcae:papers/2026-06-RC-AgenticEcology.md` | `2a297086ae9de709a840b385910433136440d920a092c290fafc62e3560021a3` | Agent-to-ecology mapping method and RC-Ant worked example | RC-Ant is conceptual motivation and domain-shaped interpretation, not an admitted domain runtime or agency result. |
| `rcae:papers/2026-06-TheSharedMedium.md` | `c2c2371525036b3a56e88a38d8ca51bf140a9b16a897378c50b01be5ec076c45` | Shared-medium relational ontology | May define trace, pressure, susceptibility, co-response, resonance, and parent-basin vocabulary; cannot raise N30 above M2. |
| `rcae:papers/2026-06-SharedMediumCoordination-EngineeringSpec.md` | `db249acdfc95a245e4fadbb90a31eec687c7550f51b59414734f4cabd57730df` | Method, mapping, control, and debt vocabulary | Despite its title, it is not an admitted runtime specification and cannot establish communication, coordination, cooperation, or agency. |

## 5. Historical graph arc context

These records preserve the closed N20-N29 arc and earlier roadmap context. They
are orientation and provenance, not substitutes for the N29 source artifacts.

| Portable source ID | Current file SHA-256 | Role |
| --- | --- | --- |
| `grc:experiments/N20-N29-LGRC-BecomingAgencyEcologyHandoff.md` | `78021a28fef8f516b132954b4e145d5130f5c8c01b18c6d8c2dd6c632c94405f` | Closed historical handoff for the becoming-primitive/ecology-bridge arc. |
| `grc:experiments/N20-N29-LGRC-BecomingAgencyEcologyRoadmap.md` | `911c5055d8cfcb87dc9e810b8b6a24f109bff83e809edb71549dcba57908e70e` | Historical roadmap and method context. |

N05-N28 sources are consumed transitively only through N29's verified
capability, demand, debt, motif, and prototype artifacts. If AE01 later needs a
stronger or different claim from an earlier experiment, that source must be
admitted directly rather than inferred from N29's summary.

## 6. N29 controlling closeout

| Field | Verified value |
| --- | --- |
| Portable source ID | `grc:experiments/2026-06-N29-lgrc-agentic-ecology-convergence-bridge/outputs/n29_closeout_and_ecology_handoff_i18.json` |
| Artifact ID | `n29_closeout_and_ecology_handoff_i18` |
| File SHA-256 | `842ba57e994bbb3e219acff741afd85c87d102bea5eec6d134f3b84f2445cb52` |
| Semantic `output_digest` | `fa21662f0a69d582bfe574311110f2610a21e6e4e352991823ce47280e0e8ff5` |
| Status | `passed` |
| Acceptance state | `accepted_agentic_ecology_convergence_bridge_handoff` |
| N29 rung | `N29-C6_agentic_ecology_probe_handoff_complete` |
| Bridge rung | `EB6_first_ecology_probe_contracts_and_handoff_supported` |
| Closeout scope | `bridge_and_probe_contract_handoff_only` |

AE01 may consume N29 as a claim-clean ecology demand model, N05-N28
capability/debt atlas, bridge motif library, prototype atlas, and source-backed
probe-contract handoff. It must not consume N29 as executed ecology runtime,
native ecology, native support, resource economy, cooperation/exploitation,
agency, life, sentience, or Phase 8 completion.

### 6.1 N29 closeout source artifacts

Every expected file SHA-256 below was recomputed from the verified graph
revision and matches the N29 closeout manifest.

| Source ID | Iteration | Acceptance state | Status | Semantic `output_digest` | File SHA-256 | Graph-repository-relative path |
| --- | --- | --- | --- | --- | --- | --- |
| `i5_ecology_demand_matrix` | I5 | `accepted_ecology_demand_matrix` | passed | `2503831622cdfc99d9f6083bfc841481a06c6fd67bcba1a9ad840c1e1c069fe9` | `61eb618e966069bffd834bd8fa32cc26050972a21132ce32777abf5dd4667e5e` | `experiments/2026-06-N29-lgrc-agentic-ecology-convergence-bridge/outputs/n29_ecology_demand_matrix_i5.json` |
| `i6_capability_supply_atlas` | I6 | `accepted_capability_supply_atlas` | passed | `8b80dcc636f8d3333f6e344bbf33ffc12eebe256e7ce2e4f19db33573a6e7181` | `ba0e32f9f7a4c064e6235fe9c306424daa5458c07c0b02f0c34e2d400da4d74b` | `experiments/2026-06-N29-lgrc-agentic-ecology-convergence-bridge/outputs/n29_capability_supply_atlas_i6.json` |
| `i7_demand_supply_coverage_debt` | I7 | `accepted_demand_supply_coverage_and_debt_matrix` | passed | `6fa29aa7ff520acb733920bb711e498bb421b091f9b6575a7663bc5f21710985` | `4aadbba5f303e893ff5ead7ace2b6acd4054160f5f7c593699a59aae609587d8` | `experiments/2026-06-N29-lgrc-agentic-ecology-convergence-bridge/outputs/n29_demand_supply_coverage_debt_i7.json` |
| `i8_bridge_motif_library` | I8 | `accepted_bridge_motif_library` | passed | `5617368e38bc0b09ef5b152699948a967d7c5d72eae09467c4705749bb372ad0` | `abd0c077dca7b5158f1e5ca0eae8d0e7f6ba849ffcf4542d75b8ba237929f073` | `experiments/2026-06-N29-lgrc-agentic-ecology-convergence-bridge/outputs/n29_bridge_motif_library_i8.json` |
| `i9_motif_relabel_nulls` | I9 | `accepted_phase_b_controls_fail_closed_ready_for_phase_c` | passed | `a6869a090698bf0c54601e34758408345eda978408a135c883fc495bf7c55a28` | `4cb75e44959ed1a9f6d67cb6e3f47f9cbe79cc43ca45a0d18a6c607e36f44eab` | `experiments/2026-06-N29-lgrc-agentic-ecology-convergence-bridge/outputs/n29_motif_relabel_nulls_i9.json` |
| `i10_prototype_admission_schema` | I10 | `accepted_prototype_admission_schema_frozen_no_prototype_rows` | passed | `fed49575d0ae9bc598d54cfbb6d01a87d69a3f8229fe466f580182b7e2c49f4d` | `f6a4c85c23822f7819a3c4be93fc742c66394140156f3125a286a2dc2bc89e40` | `experiments/2026-06-N29-lgrc-agentic-ecology-convergence-bridge/outputs/n29_prototype_admission_schema_i10.json` |
| `i15_prototype_atlas` | I15 | `accepted_prototype_atlas_with_debt_classification` | passed | `e139dd61fcd2b0998282033e5fe1a041891291d5db036982063e510be33f7cd2` | `1a810918df2923b5f5fe475ec9d0cc1f843fe614640b8149ea25173aab985a26` | `experiments/2026-06-N29-lgrc-agentic-ecology-convergence-bridge/outputs/n29_prototype_atlas_classification_i15.json` |
| `i16_minimal_probe_contract` | I16 | `accepted_minimal_ecology_probe_contract` | passed | `d34e209f2b97aeac6242279f1c887afbf4c2064dcdc6a8fe0dc29cfa1275ac53` | `44fbe5b9547279012bcc35f89cb7b66864fc4f06a57ff2ea0e8c42e3dcbdd58f` | `experiments/2026-06-N29-lgrc-agentic-ecology-convergence-bridge/outputs/n29_minimal_ecology_probe_contract_i16.json` |
| `i17_alternative_probe_contract` | I17 | `accepted_alternative_ecology_probe_contract` | passed | `d2af854a4065351aaed23e74ac7c77dc7ec495765b32cccd69019b20e31c6798` | `3fed33e4fe040da5eb35374af0ed89510e4a8f7ba3bda93849a0ce3e4eaf92cc` | `experiments/2026-06-N29-lgrc-agentic-ecology-convergence-bridge/outputs/n29_alternative_ecology_probe_contract_i17.json` |
| `i17a_full_bridge_probe_contract` | I17-A | `accepted_full_bridge_probe_contract` | passed | `f135650c01d2d74c3eb9c33e8b923542077beb8e7b2e723f36a2f7be1f68d981` | `bbdc9009626200f41ce993adfe7f1e557fb6d8ee1d1cb77666a94f317339af31` | `experiments/2026-06-N29-lgrc-agentic-ecology-convergence-bridge/outputs/n29_full_bridge_probe_contract_i17a.json` |

### 6.2 N29 prototype A-D classifications

| Prototype | Supported source role | Remaining claim/debt boundary |
| --- | --- | --- |
| A — trace/pressure/bounded response loop | Runtime/replay/stress-backed bridge exemplar and pressure/response loop skeleton. | Producer-assisted; no general decay law, semantic action, loop agency, or ecology success. |
| B — boundary/shared-medium unit | Runtime/replay/stress-backed separable medium/boundary exemplar. | Nonzero leakage tolerance and native shared-medium coordination remain unsupported; no multi-agent interaction. |
| C — proxy/susceptibility/re-entry | Runtime/replay/stress-backed two-geometry susceptibility/re-entry exemplar. | Producer-mediated susceptibility and AP4/AP5 debt remain; no learning, choice, native support, or ecology success. |
| D — generative/extractive/medium reshaping | Native/source-current motif layer plus replay/stress-backed producer-mediated composition-bridge catalogue. | Native composition remains blocked; no resource economy, cooperation/exploitation, closed native circulation, agency, or ecology success. |

N29's A+B, B+C, C+D, and A+D composition rows are source-backed
reconstruction candidates or probe-contract seeds only. In
`i15_prototype_atlas`, `composition_runtime_supported = false`; the N29 I18
closeout additionally records `runtime_probe_executed = false`. Their ordered
runtime compositions were not executed, and every composition claim remains
false. I16, I17, and I17-A are accepted probe contracts, not evidence that
their ecologies ran.

### 6.3 Required N29 debt carry-forward

| Debt ID | Direction | Still blocks | Mandatory AE01 disposition |
| --- | --- | --- | --- |
| `composed_ecology_runtime_harness_missing` | outbound ecology | Ecology success and native ecology | Keep open until a dedicated composed runtime probe supplies evidence; an atlas row cannot backfill it. |
| `producer_mediated_cross_prototype_handoff` | both | Native composition and native support | Classify every cross-prototype handoff as inherited, constructed, or native and preserve producer residue. |
| `medium_debt_and_nonzero_leakage_policy` | both | Native shared-medium coordination | Record leakage, costs, and medium debt in every applicable lane; do not assume zero or acceptable leakage. |
| `ap4_ap5_gap_propagation` | inbound N30+ | Native route-selection or proxy-target closure | Keep AP4/AP5 NAT4 gaps open unless a later source-current closeout explicitly discharges them. |
| `resource_economy_cooperation_exploitation_semantics` | outbound ecology | Resource economy and cooperation/exploitation | Use substrate-visible capacity/support language and keep semantic promotion blocked. |
| `deviation_nativity_discharge` | both | Retroactive native upgrade and producer removal without rerun | Record deviations and require explicit rerun/comparison before any constructed-to-native transition. |

Every debt carries the N29 claim ceiling into source inventory, lane records,
synthesis, promotion, and closeout unless dedicated discharge evidence is
admitted later.

## 7. N30 controlling evidence

### 7.1 N30 I7 replay, controls, and medium debt

| Field | Verified value |
| --- | --- |
| Portable source ID | `grc:experiments/2026-07-N30-lgrc-minimal-shared-medium-participation/outputs/n30_replay_controls_i7.json` |
| File SHA-256 | `bf29695841f87fc40b2464114129a19e8616c2f8e6efa49a09a472ed65cca264` |
| Semantic `output_digest` | `46f7eba93fa206355f4dc3eb5b2ae8e70dd1126eba975030a2e2fc15f1603fec` |
| Acceptance state | `accepted_replay_control_backed_C5_candidate_pending_I8_closeout` |
| Candidate rows | 3 |
| Required replay modes | artifact-only, duplicate, snapshot-load, later-response recomputation |
| Replay result | all 4 modes passed for all candidate rows |
| Controls | 20 required controls × 3 rows = 60 results; all failed closed; 0 failed-open; 0 not-run |
| Runtime origin | I7 `medium_debt_matrix.debt_rows`: all 3 rows record `runtime_origin = inherited_source_current_artifacts` and `n30_fresh_runtime = false` |
| Medium debt | artifact-level medium dependency supported; remaining nativity debt retained |

The I7 evidence supports a replay/control-backed M2 candidate only. It does not
support final N30 closeout by itself, native shared-medium organization,
coordination, or a fresh N30 runtime claim.

| I7 artifact role | Graph-repository-relative path | Verified file SHA-256 |
| --- | --- | --- |
| Replay/control matrix | `experiments/2026-07-N30-lgrc-minimal-shared-medium-participation/outputs/n30_replay_controls_i7_artifacts/i7_replay_control_matrix.json` | `df8887b333924f4718e9888eaf756bb39b7c24b8617ee9163fcbb78526f5966f` |
| Medium-debt matrix | `experiments/2026-07-N30-lgrc-minimal-shared-medium-participation/outputs/n30_replay_controls_i7_artifacts/i7_medium_debt_matrix.json` | `8c74cc30d095328e1deb0673c0e29a64f1f32f055e328440a26dc0e07509d580` |
| Claim-boundary guard | `experiments/2026-07-N30-lgrc-minimal-shared-medium-participation/outputs/n30_replay_controls_i7_artifacts/i7_claim_boundary_guard.json` | `527ff429799f84fdf756065017f1223b1493888a734d66bf653d31758e2478f3` |

### 7.2 N30 I8 closeout

| Field | Verified value |
| --- | --- |
| Portable source ID | `grc:experiments/2026-07-N30-lgrc-minimal-shared-medium-participation/outputs/n30_closeout_and_spiral_handoff_i8.json` |
| File SHA-256 | `ade32c848cbffa4d5757bfce50eaadb72a63a8252a8ba09e5fd562c6c100718c` |
| Semantic `output_digest` | `7971163b1d7bd4027f5375270cfb2445cfe4698a8869b28e26f9273d0a5b5af6` |
| Status | `passed` |
| Acceptance state | `accepted_N30_C6_post_N30_spiral_ready_minimal_shared_medium_participation_closeout` |
| Final closeout rung | `N30-C6_post_N30_spiral_ready_minimal_shared_medium_participation_closeout` |
| Participant rung | `P2_minimally_stable_participant_with_P4_guardrail_context` |
| Medium/relation rung | `M2_trace_mediated_eligibility_replay_control_backed_candidate` |
| Claim ceiling | `artifact_level_bounded_minimal_shared_medium_participation_candidate` |
| Candidate interface | available, not selected |
| Handoff mode | `cross_project_spiral` |

N30 supports the bounded chain:

```text
participant continuity
  -> non-private medium-surface perturbation
  -> source-current trace or surface change
  -> later eligibility/susceptibility depends on that changed surface
  -> replay/control validation
```

It may be consumed as a bounded minimal shared-medium participation candidate,
trace-mediated eligibility primitive/building-block candidate, and control
pattern for direct-message, label-only, hidden-controller, hidden-producer, and
post-hoc-trace blockers.

It must not be consumed as unqualified shared-medium participation,
shared-medium coordination, semantic communication, cooperation, agency,
selfhood, identity acceptance, native shared-medium organization, parent-basin
modulation, resonant alignment, sentience, organism/life, ecology regime,
executed agentic ecology, fixed N31 selection, Phase 8 completion, or
unrestricted autonomy.

| I8 artifact role | Graph-repository-relative path | Verified file SHA-256 |
| --- | --- | --- |
| Closeout classification | `experiments/2026-07-N30-lgrc-minimal-shared-medium-participation/outputs/n30_closeout_and_spiral_handoff_i8_artifacts/i8_closeout_classification_record.json` | `8ea4090617fa4b2439c7d020897e2a2910181dac64a7c0a0b16440c09b45aa30` |
| Post-N30 spiral handoff | `experiments/2026-07-N30-lgrc-minimal-shared-medium-participation/outputs/n30_closeout_and_spiral_handoff_i8_artifacts/i8_post_n30_spiral_handoff_contract.json` | `cc5e0cbde3ee1728fa58c87b2adab000f7eb14044a419d95f8f23cc7dc19eb42` |
| Claim-boundary guard | `experiments/2026-07-N30-lgrc-minimal-shared-medium-participation/outputs/n30_closeout_and_spiral_handoff_i8_artifacts/i8_claim_boundary_guard.json` | `64270da7020a870806b85fb41687d4bda911494fe3e0a3e479e3ce72979a9555` |

## 8. Current N30+ continuation records

The active continuation pointer is:

| Portable source ID | Current file SHA-256 | Role |
| --- | --- | --- |
| `grc:experiments/N30_plus_LGRC_SharedMediumEcologyHandoff.md` | `8fa69faf1631256fc1ef116715ee51387b578cc6d053df9ed3e51fdfcc831bb4` | Current handoff: N30 → agentic-ecology demand/composition pass → selected or non-selected N31+ graph probe. |

The active rule is:

```text
agentic_ecology_demand_pass_recommended = true
candidate_n31_interface_available = true
candidate_n31_selected = false
next_lgrc_experiment_fixed = false
```

Current roadmap/candidate files are orientation sources only. Both changed after
the N30 I8 closeout recorded their input hashes, so AE01 preserves historical
and current identities separately:

| Portable source ID | Historical SHA-256 recorded by N30 I8 | Current SHA-256 at graph baseline | Consumption rule |
| --- | --- | --- | --- |
| `grc:experiments/N30_plus_candidate_directions.md` | `47043d91d59c140a401f6b622bd7cb923ef9e06244ebbdae1ab134cc62c50722` | `6507b9e9f8ecce2537c678ad77d6898002543173cd462e39300cf2aff72dc7a1` | Historical hash belongs to N30 provenance; current file orients possible demands and records the N30 closeout addendum, but is not evidence. |
| `grc:experiments/N30_plus_experiment_catalog_roadmap.md` | `3c5ac6d9cbb05b134d38bf9defd42c6c938f025a8ac1751dafe1f6c500a926cf` | `247c0282e3200693ba800a02985aff5f55223ce15882924c7434045d2fc46ea6` | Historical hash belongs to N30 provenance; current file supplies catalog, debt, failure, and spiral method only. |

This evolution does not invalidate N30: the closeout preserves the exact inputs
it consumed, while the current active handoff controls continuation. Neither
roadmap may be used as positive substrate evidence.

## 9. P1-I1 admission result

- Every required source has a portable identifier, role, and consumption
  boundary.
- All four conceptual sources have runtime-evidence permission set to false.
- The N29 closeout digest and all ten source-artifact semantic/file digests
  match their verified files.
- The N29 A-D classifications, composition ceiling, and six canonical debts are
  carried without upgrade.
- The N30 I7 replay/control evidence, medium debt, I8 P2/M2 closeout, artifacts,
  and blocked relabels are recorded at their exact scope.
- The active N30+ continuation recommends AE01 demand/composition mapping and
  explicitly leaves N31+ unselected.
- Mutable orientation prose is separated from immutable closeout provenance.
- No source admission opens positive AE01 evidence.

`P1-I1-GATE` is supported by this record. Review R2 accepted these source and
consumption boundaries and assigned `AE01-C1` when P1-GATE passed. The
assignment opens no positive AE01 evidence.

## 10. P2-I2 lane-local source and restoration-provider admission

**Admission date:** 2026-07-14

**Lane-local gate:** `P2-I2-SOURCE-ADMISSION-GATE=passed`

**RCAE review-entry authority:** committed HEAD
`10c18fad2ba8ecac9ddacb0f0bc55813e6356c60`, separately from the graph
revision; the I02R1 input freeze binds the ten reviewed uncommitted I02
artifacts by exact SHA-256.

P2-I2 I02 adds a later lane-local admission without rewriting the historical
P1-I1 verification baseline in Section 2. The admitted graph identity is:

| Repository ID | Admitted Git revision | Worktree state | Scope |
| --- | --- | --- | --- |
| `grc` | `3d3d2ef25903d4210a67980f11fdd3ec21e9b6e5` | clean | Exact P2-I2-relevant package, runtime, restoration-provider, history-boundary, and supporting-evidence identities |

The controlling machine record is the
[I02 admitted-source and restoration manifest](p2-i2/i02-admitted-source-and-restoration-manifest.json),
with rationale and transition details in the
[I02 report](../reports/P2-I2-I02-source-admission-and-restoration-transition.md).
It binds seventeen repository-relative paths and twenty-four public symbols.
The file set is the reviewed P2-I2 admission scope, not a complete transitive
execution dependency lock; a later registration must bind the complete source
identity it executes.

The source-role totals are:

| Role | Count | Consumption boundary |
| --- | ---: | --- |
| `admitted_package_identity` | 3 | Package root and stable export identity only |
| `admitted_runtime_source` | 6 | May be considered by later P2-I2 realization/registration decisions; admission is not realization selection |
| `admitted_restoration_provider_source` | 1 | Native versioned branch identity for supported LGRC9V3 inputs only |
| `supporting_boundary_only` | 1 | Derived causal-history overlay boundary; not active runtime history |
| `supporting_evidence_only` | 6 | May justify admission and limits; not runtime dependencies by role |

### 10.1 Restoration-provider transition

At the admitted revision, P2-I2 makes the following native provider available
for conditional later selection:

```text
pygrc.models.lgrc9v3_restoration_identity_v1
pygrc.models.digest_lgrc9v3_restoration_identity_v1
```

The provider accepts a concrete `LGRC9V3` model or complete LGRC9V3
`pygrc.snapshot` version-1 mapping. It does not accept plain GRC9V3, raw digest,
RCAE projection, wrong-family, partial, malformed, or unsupported-version
inputs. The identity digest is a digest of the canonical versioned restoration
identity; it is not raw snapshot byte identity.

P2-I1 C02's `restoration_projection` remains historical evidence at RCAE
revision `c2def54c3721c506c28fc9f14390b1ba683a98ec`, source SHA-256
`d09955bf48b986729dc01acd283fdbe14f7515e9b5e8785c404f34ea53effa07`.
It is not an automatic P2-I2 fallback at the current graph revision. An older
revision or unavailable native helper must reopen I02 and explicitly admit a
fallback before use. Silent upgrade, downgrade, provider substitution, and
native relabeling of the RCAE projection are forbidden.

### 10.2 Composition and claim boundary

Native identity covers supported PyGRC-owned state only. A later complete
branch identity must separately compose selected RCAE role/access, pool or
active-history state not already native, producer/configuration, intervention,
matching/control, schedule, fixture, analysis, metric, calibration,
registration, and execution identities. Identity equality does not replace a
registered bounded equal-input continuation check.

This admission opens I03 realization review only. It does not select a native
or producer-assisted realization, choose a dependence mode, authorize a
candidate run, or support shared pooling, ecology, agency, identity acceptance,
organism/life, a cross-lane recurrence, or an N31+ candidate.

### 10.3 I02R1 identity and authority revalidation

The owner-supplied I02 closeout review reopened and re-passed the lane-local
admission gate under `P2-I2-I02R1`. The controlling
[I02R1 revalidation](../reports/P2-I2-I02R1-admission-closeout-revalidation.md)
and [machine validation](p2-i2/i02r1-identity-authority-validation.json)
establish these additional boundaries:

- all seventeen manifest, revision, and worktree file SHA-256 values match;
- imported `pygrc`, `pygrc.models`, and all twenty-four public symbol modules
  resolve under the admitted checkout's `grc:src` at the exact graph revision;
- each source now carries one or more granular `runtime_source`,
  `public_api_source`, `schema_or_contract_source`,
  `evidence_or_closeout_source`, `test_or_conformance_source`, or
  `documentation_only` classifications in addition to its admission role;
- every public symbol has a retained signature, implementation digest,
  accepted/unsupported shape, causal relevance, and claim ceiling;
- the provider schema remains `lgrc9v3_restoration_identity_v1`, and its
  digest is SHA-256 over UTF-8 canonical JSON for the identity document;
- provider selection remains `null` until a compatible I03 profile proposes
  it and I06 freezes it as registered configuration; and
- current native state is covered, but private `_initial_state` reset baseline
  is not separately covered. A later continuation must forbid reset or compose
  and compare an explicit reset-baseline identity.

`P2-I2-CHG-004` is correctly classified as
`source_admission_scope_correction`. Its byte-exact untracked `1.0.0` file was
not retained; the transition record therefore preserves an explicit semantic
reconstruction and digest rather than inventing a predecessor file hash.

The lane-local exact digest inventory is:

| Portable source | SHA-256 |
| --- | --- |
| `grc:pyproject.toml` | `b96f7e82c3e398502d12037548701e88aaf82b5b7c47f7153306fcea747a6d8b` |
| `grc:src/pygrc/__init__.py` | `3b1571b7cd4c8b11c014968c7255fca3ce54d16b3d06ef26df557357202b697e` |
| `grc:src/pygrc/models/__init__.py` | `31f7105365214c83f76f53aa7be1f1e0fcfc484bb96a88ab04729c1635df74dc` |
| `grc:src/pygrc/models/grc_9_v3_state.py` | `4ab5ffcb95d69a0767b24d6c95277ba3619a5d477c4865cc0d31735a2377918e` |
| `grc:src/pygrc/models/lgrc_9_v3.py` | `37f9f9a0452fba447c875f7e652d8632dc49bb159c0d1af5caecb4ce4acf48bb` |
| `grc:src/pygrc/models/lgrc_9_v3_contract.py` | `b86fb41ab530a7aa01abdf01dbc048da10c2e312a18c8b874cbd1386c4794680` |
| `grc:src/pygrc/models/lgrc_9_v3_packets.py` | `14d99292e18e2fe34e0fd5c6a1f69051e82115a051d142f10792775e2321e58f` |
| `grc:src/pygrc/models/lgrc_9_v3_runtime.py` | `40e886cd4310b45881c5e9ca22c0594cbb73f1241a63ddfd5ce57ea1373d6552` |
| `grc:src/pygrc/models/lgrc_9_v3_runtime_state.py` | `ef409403954749a45fbf444116a9a253b95b3e2d74a119006f1cbb364a83630c` |
| `grc:src/pygrc/models/lgrc_9_v3_restoration.py` | `57693baaa431ff5de9f299322cf80cb82f2114055ade4b27b06c52b36e9339df` |
| `grc:src/pygrc/models/lgrc_9_v3_timing.py` | `3a8528da792ee57ea6a229cdf952af38a52c3f2689525cf12adf63a27a63983c` |
| `grc:docs/reference/LGRC9V3-CausalHistory-ReferenceGuide.md` | `32277916241b2059d80645f9fc64d9c693bc66701ec63ccd89dc46eff961837d` |
| `grc:tests/models/test_lgrc_9_v3_contract.py` | `38574deb0bf0790ea9d63800d800478da5ffbe65073dd0c570f361dc85d5ba2b` |
| `grc:tests/models/test_lgrc_9_v3_runtime.py` | `19f310a120c5efaa4ee068fca7c6b7ffc9cedec745bc42e1f8156eb120b8736b` |
| `grc:tests/models/test_lgrc_9_v3_restoration.py` | `881e1596ee39594bb21ce1ae9e3928c1a9eafe79255dbc69438d4de98c9d5b97` |
| `grc:tests/models/test_lgrc_9_v3_restoration_matrix.py` | `b5c740545022c3be11e256d95645b57954bce993a46e7cc26edcca33517eb154` |
| `grc:implementation/Phase-8-LGRC9-RestorationIdentityCloseout.json` | `e9799e4b9a877e09ae71d93a4e76288237da219cfc1454821555f14ef7dfa9fe` |

This is lane-scoped prospective authority. It does not replace Section 2's
historical P1-I1 baseline, reinterpret P2-I1 through the native provider,
admit every graph file, establish restoration correctness, or open ecological
evidence.

## 11. P2-I2 reset-baseline persistence re-admission

**Admission date:** 2026-07-14

**Iteration/decision:** `P2-I2-I02R2`; `P2-I2-DEC-009`

**Lane-local gate:**
`P2-I2-SOURCE-ADMISSION-GATE=passed_after_i02r2_revalidation`

**RCAE review-entry authority:** committed HEAD
`10c18fad2ba8ecac9ddacb0f0bc55813e6356c60`, separately from graph revision
`83e3a300426631ee4df71b661b67d4fcfdfed594` and the exact frozen RCAE
worktree artifacts.

I02R2 supersedes the prospective P2-I2 graph dependency in Section 10 without
rewriting its historical evidence. The controlling
[I02R2 manifest](p2-i2/i02r2-admitted-source-and-reset-provider-manifest.json),
[machine validation](p2-i2/i02r2-reset-baseline-validation.json), and
[revalidation report](../reports/P2-I2-I02R2-reset-baseline-persistence-revalidation.md)
bind 31 exact source identities and 31 public callable contracts.

The reset-aware provider is available but unselected:

```text
current-only provider = pygrc.models.lgrc9v3_restoration_identity_v1
reset-aware provider  = pygrc.models.lgrc9v3_restoration_identity_v2
reset group schema    = pygrc.reset_baseline version 1
selected_provider     = null
```

V1 remains current-state-only. V2 contains current identity v1 plus reset-
baseline identity v1. New snapshots preserve construction or explicit-rebase
baseline across save/load. Legacy snapshots load current state but block reset
and v2 until explicit prospective rebase; historical construction state is not
recovered. RCAE must retain rebase provenance separately if that route is used.

The effective lane-local digest inventory is:

| Portable source | SHA-256 | Role |
| --- | --- | --- |
| `grc:pyproject.toml` | `b96f7e82c3e398502d12037548701e88aaf82b5b7c47f7153306fcea747a6d8b` | `admitted_package_identity` |
| `grc:src/pygrc/__init__.py` | `3b1571b7cd4c8b11c014968c7255fca3ce54d16b3d06ef26df557357202b697e` | `admitted_package_identity` |
| `grc:src/pygrc/models/__init__.py` | `23768e181455f4e7eb68908cdac532464c063fa5eb4250c4d05537eca0dcaa70` | `admitted_package_identity` |
| `grc:src/pygrc/models/grc_9_v3_state.py` | `4ab5ffcb95d69a0767b24d6c95277ba3619a5d477c4865cc0d31735a2377918e` | `admitted_runtime_source` |
| `grc:src/pygrc/models/lgrc_9_v3.py` | `37f9f9a0452fba447c875f7e652d8632dc49bb159c0d1af5caecb4ce4acf48bb` | `admitted_runtime_source` |
| `grc:src/pygrc/models/lgrc_9_v3_contract.py` | `b86fb41ab530a7aa01abdf01dbc048da10c2e312a18c8b874cbd1386c4794680` | `admitted_runtime_source` |
| `grc:src/pygrc/models/lgrc_9_v3_packets.py` | `14d99292e18e2fe34e0fd5c6a1f69051e82115a051d142f10792775e2321e58f` | `admitted_runtime_source` |
| `grc:src/pygrc/models/lgrc_9_v3_runtime.py` | `55d05aa03a4cf62cb42f18753aa572119011b6c4424bf2051a7ed0f6c78932d4` | `admitted_runtime_source` |
| `grc:src/pygrc/models/lgrc_9_v3_runtime_state.py` | `ef409403954749a45fbf444116a9a253b95b3e2d74a119006f1cbb364a83630c` | `admitted_runtime_source` |
| `grc:src/pygrc/models/lgrc_9_v3_restoration.py` | `e7c6b143c08eb0bda210152aeb0f6b12e0efcb666268416404ed3b649dd46931` | `admitted_restoration_provider_source` |
| `grc:src/pygrc/models/lgrc_9_v3_timing.py` | `3a8528da792ee57ea6a229cdf952af38a52c3f2689525cf12adf63a27a63983c` | `supporting_boundary_only` |
| `grc:docs/reference/LGRC9V3-CausalHistory-ReferenceGuide.md` | `c167362ce35c314a53b0d1e712c1fa9fc2aff91e2d82f278819b574221edb56c` | `supporting_evidence_only` |
| `grc:tests/models/test_lgrc_9_v3_contract.py` | `38574deb0bf0790ea9d63800d800478da5ffbe65073dd0c570f361dc85d5ba2b` | `supporting_evidence_only` |
| `grc:tests/models/test_lgrc_9_v3_runtime.py` | `19f310a120c5efaa4ee068fca7c6b7ffc9cedec745bc42e1f8156eb120b8736b` | `supporting_evidence_only` |
| `grc:tests/models/test_lgrc_9_v3_restoration.py` | `881e1596ee39594bb21ce1ae9e3928c1a9eafe79255dbc69438d4de98c9d5b97` | `supporting_evidence_only` |
| `grc:tests/models/test_lgrc_9_v3_restoration_matrix.py` | `b5c740545022c3be11e256d95645b57954bce993a46e7cc26edcca33517eb154` | `supporting_evidence_only` |
| `grc:implementation/Phase-8-LGRC9-RestorationIdentityCloseout.json` | `e9799e4b9a877e09ae71d93a4e76288237da219cfc1454821555f14ef7dfa9fe` | `supporting_evidence_only` |
| `grc:src/pygrc/core/__init__.py` | `1de90ece2242642584f399b744240207a15f1d56b1ee62247bfb1389647ec7ae` | `admitted_package_identity` |
| `grc:src/pygrc/core/interfaces.py` | `551d68fc103285608cef1a7ea4a69b9455181de21d9f91ea61cdd80c6065bc8f` | `admitted_runtime_source` |
| `grc:src/pygrc/core/serialization.py` | `a1ce1489870962af1032b8e69acc09ba8b9dcbcefaf86ea97250fc9a47009cf4` | `admitted_runtime_source` |
| `grc:src/pygrc/models/grc_9_v3.py` | `d297def1eddfaf79a7ad3d6b676caaeebb29e6d7235f4fac5c6729bd7e26ca9e` | `admitted_runtime_source` |
| `grc:specs/grc-common-interface.md` | `3ccc27250a3ddb2ecccdf27984436e3dee2b10b3f71de610bfbbbcd084ae7be6` | `supporting_boundary_only` |
| `grc:specs/grc-reset-baseline-persistence.md` | `20a75f525b1a46e97afaa3aa9e16f63adddc754ded088fa38cd666272ddc8891` | `supporting_boundary_only` |
| `grc:specs/lgrc-9-v3-restoration-identity.md` | `08c3ee95a9b76016648e14d028120bdebc88d2a109387874c32e4a462b037458` | `supporting_boundary_only` |
| `grc:specs/lgrc-9-v3-spec.md` | `a272102d8463359c2f9d7a40ce63b3be52509b517da67579127ab6845ff36dc4` | `supporting_boundary_only` |
| `grc:tests/core/test_interfaces.py` | `702c67b6cc8d98c8ae87e586f7270e5afab65d8c2178527b651a14effbc98e69` | `supporting_evidence_only` |
| `grc:tests/core/test_serialization_contract.py` | `f19f762830853ed35d243ab7390dc3e7337ee1c7fb05922b0c2742f3062c7bcc` | `supporting_evidence_only` |
| `grc:tests/models/test_reset_baseline_persistence.py` | `6236748f6bc7995dda86f7a207ccce373b33d1b7ecd90849106839baa305f01a` | `supporting_evidence_only` |
| `grc:implementation/corrections/PyGRC-ResetBaselinePersistenceChecklist.md` | `caccab6dbfeb845893762f5c7e9d8774e16de6317e8c409f56c53baa05e65d31` | `supporting_evidence_only` |
| `grc:implementation/corrections/PyGRC-ResetBaselinePersistenceCloseout.md` | `ef9b116f2c1724516960e0e6799c2816e4b178a4da2db4899c5f598180de6ad3` | `supporting_evidence_only` |
| `grc:implementation/corrections/PyGRC-ResetBaselinePersistencePlan.md` | `1ee265d39b6cabe56ac6e77bb4643aff502dd645e459be98bc76a075c1fb501f` | `supporting_evidence_only` |

This remains lane-scoped prospective dependency authority. It does not alter
P2-I1, admit every changed graph file as runtime, select v2 for P2-I2, recover
legacy construction provenance, cover RCAE-owned state, or establish an
ecological result.
