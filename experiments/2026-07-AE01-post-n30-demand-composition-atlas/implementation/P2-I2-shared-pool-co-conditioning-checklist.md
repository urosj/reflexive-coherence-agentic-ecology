# P2-I2 Shared-Pool Co-Conditioning Checklist

**Status:** bounded `P2-I2-I09A` and `P2-I2-I10` are owner-accepted and
retained at commit `b28ef17` under DEC-059/CHG-063. I09A passes 24/24 with
zero blockers. I10 generation and independent byte reconstruction each pass
24/24 with zero blockers. CONTROL-GATE and RECON-GATE are passed. CHG-062
corrected the v2 raw-witness
criterion to the admitted native contract after a state-only diagnostic found
exactly the deterministic normalization surface declared and tested by
PyGRC; identity, continuation, reset, exact adapter bytes, and refusal of every
unexpected native difference remain mandatory. The
owner-accepted I08 package is retained at
commit `625a411`; C02 contains 234/234 evaluable terminals, no missing,
nonevaluable, or ambiguous matrix entry, and one cumulative mechanical ledger.
Historical I09 derived the compact mode-separated control-resolution index
required by R3 and was accepted at commit `cfa19fe`. I10 later found its
primary-margin estimator bypass, reopening CONTROL-GATE. Accepted I09A
recomputes the corrected margins and confirms that all 38 comparison rules and
15 mode-local controls still pass while the 19 program controls still resolve
to 56 mode-level passes and one explicit not-applicable. I11 retained-evidence
interpretation construction is technically complete under DEC-060/CHG-064.
The retained-evidence build and independent reconstruction pass 30/30 with
zero blockers or scientific/runtime operations. Under DEC-061/CHG-065 the
owner accepts the exact reviewed package, passes CLOSE-GATE, and authorizes one
containing commit without opening cross-lane synthesis or the next move.

Historical I00–I07 gate and iteration detail remains retained below.

**Iteration:** `P2-I2`

**Lane:** `AE01-L02`

**Current activity iteration:** `P2-I2-I11` is complete and owner-accepted
under DEC-061/CHG-065; the containing commit is authorized.

**Current local gate:** `P2-I2-BRIEF-GATE=passed`;
`P2-I2-SOURCE-AUDIT-GATE=passed_after_revalidation`;
`P2-I2-SOURCE-ADMISSION-GATE=passed_after_i02r2_revalidation`;
`P2-I2-DISCRIMINATOR-GATE=passed`;
`P2-I2-CAL-PRE-GATE=passed_after_explicit_owner_acceptance_of_I04R2`;
`P2-I2-CAL-GATE=passed_after_explicit_owner_acceptance_of_I05J_closeout`;
`P2-I2-REG-GATE=passed_after_explicit_owner_acceptance_of_I06B`;
`P2-I2-EXEC-FREEZE=passed_for_accepted_C02`;
`P2-I2-EXEC-GATE=passed_234_of_234_evaluable`;
`P2-I2-CONTROL-GATE=passed_after_explicit_owner_acceptance_of_I09A`;
`P2-I2-RECON-GATE=passed_after_explicit_owner_acceptance_of_I10`;
`P2-I2-CLOSE-GATE=passed_after_explicit_owner_acceptance_of_I11`

**Acceptance ceiling:** `AE01-C2`; the bounded L02 result is accepted exactly
at R05 under scaffold dependence. No cross-lane recurrence, N31+ selection,
native implementation priority, or next-move execution is assigned.

**Semantic authority:**
[accepted P2-I2 brief](P2-I2-shared-pool-co-conditioning-brief.md)

**Operational hypothesis projections:**
[P2-I2 operational hypotheses](../hypotheses/p2-i2-operational-hypotheses.md)

**Cumulative lane decisions:**
[P2-I2 decision record](P2-I2-decision-record.md)

**Frozen authorities:**
[L02 hypothesis](../hypotheses/lane-hypotheses.md),
[post-R3 ecology-discriminator amendment](../hypotheses/post-r3-ecology-discriminator-amendment.md),
[outcome and stopping contract](../hypotheses/outcome-and-stopping-contract.md),
[developmental interpretation contract](../hypotheses/developmental-interpretation-contract.md),
[L02 metric sheet](../contracts/metric-sheets/AE01-L02.json),
[execution policy](../configs/p1_i5_execution_policy.json), and
[P1-I5 tooling contract](P1-I5-tooling-contract.md)

**Program cover:** [Post-N30 master checklist](../../../implementation/PostN30-checklist.md)

## 1. How to use this checklist

This is the detailed planning, activity, evidence, and learning surface for
P2-I2. The master checklist records stable cover gates. This file projects the
common lane contract and the accepted P2-I2 brief into named lane-local
iterations.

The operating rule is:

> No P2-I2 activity occurs off-ledger. Every audit, decision campaign,
> artifact-construction step, calibration, registration action, execution,
> control resolution, reconstruction, interpretation, or closeout is a named
> checklist iteration with retained evidence.

An activity iteration must declare before work begins:

```text
iteration_id
purpose
entry_authority
frozen_inputs_or_input_freeze_action
mutation_and_repository_boundary
required_outputs
evidence_effect
exit_gate
```

Checkbox convention:

```text
[ ] pending, blocked, unresolved, or not yet demonstrated
[x] completed with cited retained evidence or explicit disposition
```

Rules:

- A checked evidential item cites an accepted decision, retained artifact,
  reconstruction, report, or owner disposition.
- Creating or editing this checklist is itself recorded in the active
  iteration before the iteration closes.
- Reading a source to design an audit does not count as completing the audit.
  Preparatory observations carry no capability, source-admission, realization,
  calibration, or result authority.
- An iteration may prepare the next iteration's inputs, but it cannot silently
  perform or pass that next iteration.
- The checklist is living between candidate probe cycles and frozen within a
  probe cycle.
- Every evidence-triggered addition receives a change ID and names the
  affected iteration and rerun scope.
- Scientific changes after calibration require a new preregistration and a
  separately frozen candidate cycle; infrastructure retries cannot carry
  scientific refinement.
- Native, producer-assisted, constructed, and ecology-owned state roles remain
  explicit throughout.
- The graph/PyGRC repository remains read-only from RCAE.
- A conflict with a frozen Phase 1 authority reopens that authority; it cannot
  be resolved inside this checklist.
- No terminal checkbox can be inferred from a positive metric alone.

## 2. Local gate dashboard

| Gate | Meaning | Status | Exit evidence or blocker |
| --- | --- | --- | --- |
| `P2-I2-BRIEF-GATE` | L02 semantic center, D-039 delta, dependence modes, causal factorization, controls, timing, and claim ceiling accepted | Passed after mode-family scope clarification | Owner acceptance dated 2026-07-14; `P2-I2-DEC-001`; owner-accepted three-mode retention correction `P2-I2-DEC-011`; accepted brief |
| `P2-I2-SOURCE-AUDIT-GATE` | Source-current public PyGRC capability audit completed under one frozen audit scope | Passed after revalidation | I01R1 quarantines the custom probe, corrects CAP-04, and revalidates all claims from admissible evidence |
| `P2-I2-SOURCE-ADMISSION-GATE` | Exact graph sources and any restoration-profile transition admitted for lane use | Passed after I02R2 revalidation | Updated revision `83e3a300426631ee4df71b661b67d4fcfdfed594`, 31 sources/callables, persisted reset baseline, v1/v2 provider boundary, legacy fail-closed policy, and `P2-I2-DEC-009` |
| `P2-I2-DISCRIMINATOR-GATE` | Realization, dependence mode, factorization, access witness, and subordinate operational hypotheses frozen | Passed after owner acceptance of compact I03F | DEC-020; opens I04 construction only; all three modes remain retained and unranked |
| `P2-I2-CAL-PRE-GATE` | Candidate-blind null, response, comparator, signed controls, and analysis identity preregistered | Passed after explicit owner acceptance of I04R2 | DEC-026 accepts I04R2 as sole progression authority after 16/16 checks and 7/7 pure tests; opens only separately frozen single-invocation I05 arithmetic calibration; no null/runtime/candidate execution occurred at passage |
| `P2-I2-CAL-GATE` | Reconstructable matched-null calibration freezes `delta` without candidate input | Passed after explicit owner acceptance of I05J/I05JA | Complete I05 closeout; delta `1e-12`; 11/11 validation; exact process/package accounting; no scientific effect; opens I06 construction only |
| `P2-I2-REG-GATE` | Exact realization, cells, controls, identities, artifacts, and reconstruction bundle accepted | Passed after explicit I06B owner acceptance | Accepted I06/I06A remain immutable; accepted I06B closes all three I07-found execution-readiness gaps with 15/15 candidate-free checks and zero blockers; opens only resumed I07 freeze construction |
| `P2-I2-EXEC-FREEZE` | One exact candidate cycle authorized before its first operation | Consumed and retained | C01 closed bounded-incomplete; owner-accepted C02 completed under its exact activation and admitted checkpoint rule |
| `P2-I2-EXEC-GATE` | Frozen finite matrix completes or closes validly blocked/incomplete | Passed at 234/234 evaluable | Accepted C02 manifest; zero missing, nonevaluable, or ambiguous terminals; no terminal interpretation |
| `P2-I2-CONTROL-GATE` | Every mandatory common and L02 control receives a retained fail-closed disposition | Passed after explicit I09A owner acceptance | DEC-059 accepts I09A's exact 24/24 correction: 18 margins through I04R2, 38 comparison, 15 lane-control, and 57 program-mode dispositions, with no disposition change |
| `P2-I2-RECON-GATE` | Retained evidence, identities, and reports reconstruct independently | Passed after explicit I10 owner acceptance | DEC-059 accepts I10's two 24/24 passes, 234 terminals/470 paths, three-mode restoration/continuation/reset checks, zero blockers, and zero scientific operation |
| `P2-I2-INTERPRET-GATE` | Boundary rungs, metric relation, support, two-axis reading, debts, and next move resolve | Passed after explicit I11 owner acceptance | DEC-061 accepts all five rungs, three mode dispositions, support/T-classification, observation/debt ledgers, two-axis reading, claim ceiling, and next-move falsifier |
| `P2-I2-CLOSE-GATE` | One terminal classification and compact control-resolution index close the lane | Passed after explicit I11 owner acceptance | DEC-061 accepts the exact 30/30 I11 package, bounded R05/scaffold-dependent terminal result, next-move falsifier, and claim ceiling |

`P2-I2-GATE` in the master checklist is equivalent to
`P2-I2-CLOSE-GATE` here.

## 3. Stable entry and claim boundaries

- [x] `P1-GATE` passed. Evidence: [R2 closeout](../reports/R2-closeout.md).
- [x] Review R3 passed and requires a compact lane-local control-resolution
  index before P2-I2 terminal closure. Evidence:
  [R3 review](../reports/R3-contract-adequacy-review.md).
- [x] Stable lane ID is `AE01-L02`.
- [x] Frozen hypothesis authority is `AE01-H-L02`.
- [x] The accepted post-R3 D-039 amendment applies before calibration.
- [x] The P2-I2 brief is accepted as lane-local semantic authority. Evidence:
  `P2-I2-DEC-001`.
- [x] The operational hypotheses are subordinate projections, not new lane
  hypotheses or schema vocabulary.
- [x] Frozen maximum claim is
  `bounded shared-pool co-conditioning demand pattern`.
- [x] The seven Phase 1 L02 logical cells and five L02 controls remain fixed.
- [x] Nonlinearity is optional; joint functional dependence is mandatory.
- [x] Native support is preferred when adequate; a minimal explicit producer
  or constructed mechanism remains allowed when native support is absent or
  inadequate.
- [x] State-carried, history-carried, and hybrid are retained as three
  mode-specific realizations through registration, execution, control
  resolution, and interpretation. Selection is among native, minimally
  producer-assisted, or missing-prerequisite dispositions within each mode;
  the three modes are not candidates in a winner-selection step. Evidence:
  owner acceptance dated 2026-07-14 and `P2-I2-DEC-011`.
- [x] Graph revision
  `3d3d2ef25903d4210a67980f11fdd3ec21e9b6e5` is the exact historical I02R1
  admission and remains retained provenance.
- [x] Updated graph revision
  `83e3a300426631ee4df71b661b67d4fcfdfed594` is the exact I02R2 admission;
  this source identity alone selects no provider or realization.
- [x] No source audit, source admission, realization selection, calibration,
  registration, candidate execution, control outcome, or P2-I2 result is
  inferred from brief preparation.
- [x] Collective memory, communication, resource economy, cooperation,
  coordination, agency, organism, native pool primitive, motif, regime, life,
  cross-lane recurrence, and N31+ selection remain blocked.

## 4. Activity-iteration ledger

| Iteration | Activity | Entry dependency | Status | Exit gate/effect |
| --- | --- | --- | --- | --- |
| `P2-I2-I00` | Authority bootstrap: brief acceptance, checklist, operational-hypothesis scaffold, and cumulative decision record | Owner acceptance | Complete | `P2-I2-BRIEF-GATE=passed`; no scientific evidence |
| `P2-I2-I00R1` | Post-bootstrap artifact review, provenance correction, and compact validation retention | I00 plus external review | Complete | `P2-I2-CHG-001`; brief gate remains passed |
| `P2-I2-I01` | Source-current PyGRC capability audit | I00R1 | Complete as executed; corrected by I01R1 | Historical audit disposition retained; current gate effect owned by I01R1 |
| `P2-I2-I01R1` | Capability-audit closeout revalidation and candidate-probe quarantine review | I01 plus owner-supplied closeout review | Complete; probe quarantined, CAP-04 corrected, static audit revalidated | `P2-I2-SOURCE-AUDIT-GATE=passed_after_revalidation` |
| `P2-I2-I02` | Source admission and restoration-profile transition disposition | I01R1 | Complete | `P2-I2-SOURCE-ADMISSION-GATE=passed`; no scientific evidence |
| `P2-I2-I02R1` | Admission closeout revalidation: identity, authority, imported-package provenance, callable/provider contract, and transition boundary | I02 plus owner-supplied closeout review | Complete; governance/import/provider/coverage package revalidated | `P2-I2-SOURCE-ADMISSION-GATE=passed_after_revalidation`; no scientific evidence |
| `P2-I2-I02R2` | Updated PyGRC reset-baseline persistence and restoration-identity revalidation | I02R1 plus updated graph revision supplied by project owner | Complete; reset persistence and v2 identity validated, updated source admitted | `P2-I2-SOURCE-ADMISSION-GATE=passed_after_i02r2_revalidation`; no scientific evidence |
| `P2-I2-I03` | Staged realization, discriminator, dependence-mode, and operational-hypothesis program | I01R1–I02R2 plus owner staging direction | Complete and owner-accepted through compact I03F under DEC-020 | `P2-I2-DISCRIMINATOR-GATE=passed`; opened only I04 |
| `P2-I2-I03A` | 8A state-carried realization and operational-hypothesis freeze | I02R2 plus owner staging direction | Causal design accepted as I03AR1 baseline; runtime adequacy unassigned | `P2-I2-I03A-REVIEW-READY`; opened only I03AR1 under DEC-012 |
| `P2-I2-I03AR1` | 8A-R1 quarantined state-carried realization runtime conformance | Owner acceptance of stronger conformance path after I03A review | Owner accepted for progression on 2026-07-14; scientific effect remains none | Opens I03B only under its own declaration/freeze; does not open I03C/I04 |
| `P2-I2-I03B` | 8B history-carried realization, operational-hypothesis freeze, and bounded runtime conformance | Owner acceptance/progression direction after I03AR1 | Owner accepted for staged progression on 2026-07-14; minimally producer-assisted design and 252/252 runtime conformance retained | Opens I03C only under DEC-015; no scientific or I04 effect |
| `P2-I2-I03BR1` | I03B closeout revalidation of latest-contact dataflow, active-history identity, producer minimality, lifecycle, restoration, and quarantine | I03B plus owner-supplied validation review | Complete and owner accepted for progression; 21/21 checks, six downstream obligations, zero blockers | `P2-I2-I03BR1-CLOSEOUT-PASSED`; obligations retained for I04/I06 |
| `P2-I2-I03C` | 8C hybrid realization, operational-hypothesis freeze, and bounded runtime conformance | Owner acceptance of I03B/I03BR1 under DEC-015 | Owner accepted for staged progression on 2026-07-14; minimally producer-assisted design and 258/258 byte-reconstructed runtime conformance retained | Opens I03F only under its own declaration/freeze; no scientific or direct I04 effect |
| `P2-I2-I03CR1` | 8C-R1 zero-runtime hybrid causal-well-formedness and acceptance closeout revalidation | I03C plus owner-supplied twenty-six-point/seventeen-condition review | Complete and owner accepted for progression; 26/26 review checks, 17/17 acceptance conditions, eight downstream obligations, zero blockers | `P2-I2-I03CR1-CLOSEOUT-PASSED`; opened I03F only |
| `P2-I2-I03F` | 8.1 compact zero-runtime umbrella three-mode family closeout | Owner acceptance/progression direction after I03C/I03CR1 | Complete and owner accepted; 12/12 integration checks and 9/9 acceptance conditions passed with zero blockers | `P2-I2-DISCRIMINATOR-GATE=passed`; opens I04 construction only |
| `P2-I2-I04` | Three-mode calibration preregistration construction | Passed discriminator gate under owner-accepted I03F | Static package validated, but owner review withheld CAL-PRE passage and reopened the comparator/window/null boundary | Superseded for progression by I04R1; retained history only |
| `P2-I2-I04R1` | I04-R1 comparator, order, analytic-null, fixed-window, B-purity, mode-isolation, and evidence-derived-chain correction | Owner-supplied critical review of I04 | Complete immutable historical correction; 19/19 focused checks and 15/15 pure tests | Superseded for progression by owner-accepted I04R2; no independent execution authority |
| `P2-I2-I04R2` | Conditional two-arm estimator, diversion, response-gain, window, diagnostic, order, and causal-receipt machine verification | Owner-supplied conditional I04R1 acceptance review | Complete and owner-accepted; 16/16 focused checks and 7/7 pure tests; future I05 bypass and reconstruction enforcement corrected | Sole I04 progression authority; `P2-I2-CAL-PRE-GATE=passed`; opens only separately frozen I05 authorization |
| `P2-I2-I05` | Matched-null calibration execution and metric-sheet freeze under the preregistered shared/mode-specific rule | Owner-accepted I04R2 and passed CAL-PRE | Complete and owner-accepted: single arithmetic-null attempt with one builder call and zero retries; native metric closeout passes 11/11 with delta `1e-12` and exact process/package accounting | `P2-I2-CAL-GATE` passed; opens unstarted I06 construction only |
| `P2-I2-I05A` | Pre-acceptance one-shot consumption, committed-authority revalidation, and readback-only reconstruction safety audit | Owner-supplied three-item execution-safety review of the I05 candidate | Complete: 3/8 passed, five blockers, zero governed execution; no source correction | Proposed DEC-027 blocked; cannot open I05 execution or CAL-GATE |
| `P2-I2-I05B` | I05-owned one-shot wrapper, policy, claim/final receipt, committed-authority preflight, and zero-null safety correction | Explicit owner authorization after I05A | Owner-accepted: 12/12 tests, 12/12 checks, byte reconstruction; I04R2 immutable; commit authorized, null launch separate | Accepted authority package committed under DEC-029/CHG-022 |
| `P2-I2-I05C` | Pre-claim active-repository-venv command/target identity correction | Final 10.4 preflight failure plus owner direction “always use venv” | Owner-approved and committed at `9d81f15`; 13/13 tests and 12/12 checks preceded the later single attempt | Historical authority; current portable projections governed by I05E |
| `P2-I2-I05D` | P2-I2-wide persisted-path portability audit | Owner rule that absolute paths are never allowed | Accepted exact inventory: 312 value-redacted findings in 70 of 135 files | Opens one reviewed I05E correction group at a time |
| `P2-I2-I05E` | First bounded historical-to-portable correction group | Owner acceptance of I05D and authorization of the I05 group | Complete and retained at `6dd6898`: 10/10 checks, zero group violations, 13/13 focused helper tests | Opens only I05F under DEC-034; CAL-GATE remains closed |
| `P2-I2-I05F` | I04/I05 authority-dependency historical-to-portable correction | Owner acceptance/commit of I05E and direction to continue | Owner-accepted and commit-authorized: 10/10, 30 to zero findings, original freeze retained, and 13-versus-three process deviation accepted additively under DEC-035/036 | Retain complete package; no later group or CAL-GATE passage |
| `P2-I2-I05G` | Third bounded accepted-audit portability correction group | Owner direction after accepted I05F commit `99c64dd` | Complete and retained at `62882ef`: 10/10 checks, 30 lineage pairs, 201 to zero findings, 105 pointer projections and 44 identical targets; zero runtime/scientific operations | Opens only I05H under DEC-038; CAL-GATE remains closed |
| `P2-I2-I05H` | Fourth bounded accepted-audit portability correction group | Owner acceptance/commit of I05G and direction to move to the fourth group | Complete and retained at `1279e17`: 10/10 checks, 10 lineage pairs, 35 to zero findings, four exact JSON, three exact report, and three exact Python projections; zero runtime/scientific operations | Opens only I05I reconciliation under DEC-039; CAL-GATE remains closed |
| `P2-I2-I05I` | Fifth/final governance-navigation/shared-projection portability correction | Owner acceptance/commit of I05H, remaining-file check, direction not to create a standalone review, owner identification of two root-constructor validators, and guard identification of one shebang-constructor validator | Complete and retained at `b5d0acb`: 10/10 checks, nine lineage pairs, terminal 14 literal findings plus four constructed absolute surfaces to zero, complete P2-I2 audit scope zero; zero runtime/scientific operations | Opens only I05J under DEC-040; CAL-GATE remains closed |
| `P2-I2-I05J` | Arithmetic-resolution and metric-sheet closeout | Owner accepts/commits I05I and directs return to 10.4/10.4A | Owner-accepted and retained at `3be9073`: exact ten-row/two-order evidence projects to five estimator-preserving seed envelopes; native outputs reconstruct byte-exactly; 11/11 checks; delta `1e-12`; additive process/package closeout; zero runtime/scientific work | I05 complete; CAL-GATE passed; accepted I06/I06A now governs progression |
| `P2-I2-I05JA` | Failed-closed native dependency correction | First I05J native start reports missing pinned `jsonschema` before output | Complete and accepted with I05J: failed start retained, exact `jsonschema==4.26.0` installed/verified in `.venv`, and one unchanged native retry succeeded | Retained inside accepted I05 package; no independent scientific effect |
| `P2-I2-I06` | Exact three-mode implementation registration and evidence-bundle construction | Passed CAL-GATE and explicit owner direction | Owner-accepted: exact three-mode bundle; 7 cells/26 subconfigurations; 5 lane controls; 14/14 validation; three save/load/reset-stable baselines; nine refusal checks; zero candidate/scientific operations | Accepted with I06A under DEC-042; REG-GATE passed; I07 freeze construction authorized |
| `P2-I2-I06A` | Owner-review conformance/provenance closeout | Owner-supplied I06 review identifies two potential blockers and four critical confirmations | Complete and owner-accepted: separately authorized replacement passes 14/14; both blockers resolved; four confirmation groups pass; zero PyGRC/baseline/candidate/scientific work | Checkpoint amendment authorized; REG-GATE passed; I07 freeze construction authorized; candidate execution unauthorized |
| `P2-I2-I06B` | Additive execution-readiness registration correction | I07 authority audit plus explicit owner `+1` on DEC-043 recommendation | Complete and owner-accepted: exact overlay freezes all three missing primitives; 15/15 checks, zero blockers, immutable accepted bytes, zero PyGRC/model/packet/scientific work | REG-GATE restored under DEC-044/CHG-038; resumed I07 only; commit and candidate execution unauthorized |
| `P2-I2-I07` | Mode-indexed candidate-cycle execution freeze | Owner-accepted I06B and restored REG-GATE | Retained reviewed history: exact 234-entry matrix; 7/7 focused tests; 25/25 final validation; CHG-041 later found four cross-entry-isolation blockers | Superseded for progression by I07A; no candidate/scientific effect |
| `P2-I2-I07A` | Cross-entry-isolation correction | DEC-046/CHG-042 owner direction after CHG-041 audit | Owner-accepted: all four blockers closed; 234 entries unchanged; 21 bound files; 15/15 focused tests; 17/17 final validation; zero PyGRC/model/packet/candidate/scientific activity | DEC-047 passes inactive `P2-I2-EXEC-FREEZE` and authorizes checkpoint commit; live activation, I08, and candidate execution remain closed |
| `P2-I2-I08` | Finite live three-mode candidate/control matrix execution | Owner-accepted C01 activation, then owner-accepted I08A/C02 successor | Mechanically complete under C02: 234/234 evaluable terminals; C01 retained byte-exactly as bounded-incomplete operational history | `P2-I2-EXEC-GATE=passed_234_of_234_evaluable`; no terminal interpretation |
| `P2-I2-I08A` | C02 native-exit supervisor and resource-envelope correction | DEC-050 owner direction after C01 entry-001 native termination | Owner-accepted and complete: 8/8 tests, 18/18 correction validation, 19/19 activation validation, and accepted C02 execution | Successor correction retained; C02 supplied the complete I08 matrix without changing its scientific projections |
| `P2-I2-I09` | Mode-specific control resolution and compact index generation | Accepted I08 commit `625a411` | Owner-accepted and retained: 21/21 checks; 38/38 comparison rules; 15/15 L02 mode-controls | `P2-I2-CONTROL-GATE=passed_after_explicit_owner_acceptance`; I10 ready but unstarted |
| `P2-I2-I09A` | Additive normalized-estimator control-projection correction | DEC-056 finding plus explicit owner `+1` under DEC-057 | Owner-accepted: 24/24, zero blockers, exact reconstruction, no downstream disposition change | DEC-059 passes CONTROL-GATE and authorizes containing commit |
| `P2-I2-I10` | Retained-evidence reconstruction and identity verification | Accepted I09 commit `cfa19fe`, CHG-055 failure, I09A correction, and DEC-058 completion direction | Owner-accepted: generation and independent reconstruction each pass 24/24; zero blockers; three modes pass native restoration/continuation/reset contract | DEC-059 passes RECON-GATE and authorizes containing commit; I11 ready after retention but unstarted |
| `P2-I2-I11` | Developmental interpretation, terminal classification, and lane closeout | Accepted I09A/I10 and passed CONTROL/RECON gates | Complete and owner-accepted at 30/30 | CLOSE-GATE passed; containing commit authorized |

No iteration may be marked complete merely because a later iteration produced
an artifact that should have been created earlier. Missing iteration evidence
fails closed and must be reconstructed or explicitly classified.

## 5. `P2-I2-I00` — Authority bootstrap

**Purpose:** establish accepted semantic authority and the lane-local process
surfaces before any capability or realization work begins.

**Evidence effect:** none; authority and process only.

**Mutation boundary:** P2-I2 narrative artifacts and stable navigation only;
no graph-repository writes, runtime probes, calibration, registration, or
candidate execution.

- [x] Project owner explicitly accepted the revised P2-I2 brief on
  2026-07-14.
- [x] Brief status records owner acceptance without assigning evidence.
- [x] This evidence-expandable checklist exists and makes every later activity
  a named iteration.
- [x] Subordinate operational-hypothesis projections reside under the
  experiment's `hypotheses/` authority surface and are indexed there without
  selecting a realization, dependence mode, response, comparator, or outcome.
- [x] One cumulative P2-I2 decision record exists.
- [x] `P2-I2-DEC-001` retains the accepted semantic and claim boundaries.
- [x] `P2-I2-DEC-002` retains the checklist-first, no-off-ledger activity rule.
- [x] `P2-I2-DEC-003` retains the subordinate operational-hypothesis lifecycle.
- [x] Brief-preparation inspection is explicitly not counted as I01 audit
  evidence.
- [x] Capability audit, source admission, realization selection, calibration,
  registration, and execution remain unopened.

### 5.1 I00 construction and validation record — 2026-07-14

- [x] P2-I1's accepted checklist and cumulative-decision conventions plus R3's
  proportionality constraints were inspected only to scaffold P2-I2 process;
  no P2-I1 conclusion or realization was reused as evidence.
- [x] All local Markdown links from the brief, checklist, decision record,
  operational hypotheses, and lane indexes resolve to existing files.
- [x] The checklist contains exactly the declared I00–I11 activity sequence,
  and the hypothesis artifact contains OP-01 through OP-09.
- [x] Required Phase 1 L02 cell, control, rung, metric, and D-039 identities
  remain present in the accepted brief and linked artifacts.
- [x] `git diff --check` and trailing-whitespace scans passed for the complete
  I00 documentation change.
- [x] The graph/PyGRC worktree remained clean after I00 validation.
- [x] The validation did not execute the I01 capability questions, admit the
  candidate graph revision, or run PyGRC candidate behavior.

Compact reconstructable evidence for these checks is retained in the
[I00 validation provenance](../reports/P2-I2-I00-validation.md).

### 5.2 `P2-I2-I00R1` — Post-bootstrap review correction

**Status:** complete

**Trigger:** the owner-supplied artifact-stack review received after I00.

**Change ID:** `P2-I2-CHG-001`

**Evidence effect:** integrity and process clarification only; no capability,
source-admission, calibration, or lane evidence.

- [x] Acceptance provenance was checked against the actual conversation and
  workspace. The explicit owner statement “yes, it is acceptance” supports
  DEC-001 and the accepted brief; the review's stale draft-status premise does
  not reopen `P2-I2-BRIEF-GATE`.
- [x] DEC-002 is identified as an explicit owner-directed process decision;
  DEC-003 is identified as derived and accepted under the I00 package rather
  than a separate owner statement.
- [x] I01 now distinguishes authorized input-freeze construction from
  unauthorized source inspection, API invocation, and conformance checks.
- [x] I03 owns causal intervention meaning, held-fixed variables, qualitative
  expected relations, and fail-closed scientific interpretation.
- [x] I04 owns exact measurement and machine evaluation without revising I03's
  causal expectations.
- [x] I05 retains a separate metric-calibration record and generated frozen
  metric-sheet artifact rather than mutating the base L02 sheet.
- [x] I08 now quantifies exact matrix-entry execution and explicitly retains
  `reference-pool` responses.
- [x] OP-09 is a falsifiable bounded-retention projection with supported,
  not-supported, and blocked/incomplete readings.
- [x] Compact validation provenance retains commands, exit codes, checked
  files, graph status, and authority-package digests.
- [x] No I01 source inspection occurred during I00R1.

Exit gate `P2-I2-BRIEF-GATE`:

```text
accepted brief + checklist + subordinate hypothesis scaffold
+ cumulative decision record + no evidence overclaim
= passed
```

Disposition: `P2-I2-I00=complete` and `P2-I2-BRIEF-GATE=passed`.
This opens only the input-freeze work for I01.

## 6. `P2-I2-I01` — Source-current capability audit

**Status:** complete; Section 6.1 input freeze preceded source inspection, all
questions and outputs are retained, and the graph checkout remained unchanged.

**Purpose:** determine which public surfaces of one exact source-current PyGRC
revision can natively express the accepted L02 discriminator and which are
absent or inadequate.

**Evidence effect:** capability and missing-surface classification only; no
source admission, realization selection, calibration, or lane result.

Writing and reviewing the audit scope, permitted commands, identity boundary,
and output contract is authorized now. Reading additional graph/PyGRC source
files for capability classification, invoking public APIs, or running
conformance checks begins only after every Section 6.1 input-freeze item is
checked with retained evidence.

### 6.1 Input freeze before audit activity

Frozen artifact:
[I01 audit-input freeze](../contracts/p2-i2/i01-audit-input-freeze.json).

- [x] Record the exact graph repository revision and worktree state to audit.
  Evidence: clean `main` checkout at
  `3d3d2ef25903d4210a67980f11fdd3ec21e9b6e5`.
- [x] Freeze the repository-relative file/API scope and audit questions.
- [x] Freeze allowed read-only commands and any non-mutating conformance checks.
- [x] Declare whether installed-package inspection is needed and how package
  identity will be separated from checkout identity.
- [x] Freeze output paths for the narrative audit, machine-readable capability
  matrix if needed, command provenance, and file-digest inventory.
- [x] Record that audit failure or absence cannot become a negative L02 result.

The freeze fixes eleven question IDs (`P2-I2-CAP-01` through
`P2-I2-CAP-11`), the `adequate` / `inadequate` / `absent` / `unresolved`
classification contract, checkout-only package identity, graph read-only
boundaries, fixed output paths, and the change-control rule for any audit-scope
correction. Its entry-authority digests bind the accepted state at RCAE commit
`430f77206790c2d27b8283e58d4b8a58737a7ad3` before this checklist advanced
I01 to source inspection.

The first in-scope packaging-manifest read showed that the checkout package
root is `src/pygrc/**`. `P2-I2-CHG-002` added that exact tracked path and fixed
checkout import root before any package source file was read or any capability
was classified. No rerun was required.

### 6.2 Required capability questions

- [x] Is there a public native non-private carrier with reconstructible
  identity and declared access scope? Disposition: one declared node-coherence
  carrier is `adequate`; pool role/access semantics remain RCAE declarations.
- [x] Can at least two attributable contribution paths alter one carrier
  without source-private response reads? Disposition: `adequate` through
  multiple native packets crediting one target while lineage stays in the
  separate packet ledger.
- [x] Is there a carrier-scoped read, susceptibility, or eligibility path that
  does not require contributor addressing? Disposition: `adequate` through the
  native feedback-eligibility surface and feedback producer.
- [x] Can encounter state, active history, or both persist and be intervened on
  independently of audit metadata? Disposition: `adequate` for encounter-state
  mode; no native aggregate pool-history object was established.
- [x] Can the audit-only label permutation and common-carrier intervention be
  expressed without causal bypass? Disposition: `adequate`; the audit probe
  retained invariant causal projections under swapped lineage labels.
- [x] Can pool write freeze and mode-relevant clamp interventions be expressed?
  Disposition: `inadequate` as a complete native surface; route/producer
  withdrawal is available, but no atomic pool-specific gate/clamp exists.
- [x] Can a private-partition counterfactual preserve marginal contributions
  and opportunity without recreating a common state? Disposition: native
  topology primitives exist, but the matched-control/no-common-read contract
  is `inadequate` and remains RCAE-orchestrated.
- [x] Are reserve, accumulation, mixing, depletion, saturation, leakage, and
  maintenance observable or classifiably inapplicable? Disposition: reserve,
  accumulation/mixing, and depletion are native; generic capacity/saturation,
  leakage, and maintenance are `inadequate` beyond passive conserved mode.
- [x] What native state is covered by restoration identity, and what ecology
  pool/intervention state would remain external? Disposition: native node,
  queue, ledger, routes, histories, producer configuration, events, and
  observables are covered; RCAE roles, controls, schedules, and any constructed
  state remain external.
- [x] Does each candidate surface classify as `adequate`, `inadequate`,
  `absent`, or `unresolved`, with a precise reason and evidence reference?
  Evidence: [capability matrix](../contracts/p2-i2/i01-capability-matrix.json).
- [x] What is the smallest producer or constructed transition needed for each
  otherwise promising inadequate surface? Evidence: CAP-06 through CAP-11 and
  the narrative audit's minimal-demand table; no fallback is selected.

### 6.3 Audit outputs and exit

- [x] Retain one [narrative capability-audit report](../reports/P2-I2-I01-source-current-capability-audit.md).
- [x] Retain one compact requirement-to-surface matrix or explicitly justify
  why the report itself is the compact projection.
- [x] Retain exact source revision, source paths, callable names, relevant file
  digests, and command provenance.
- [x] Separate public API facts, inferred adequacy, missing surfaces, and open
  questions.
- [x] Record a bounded shortlist or a classified absence without selecting the
  P2-I2 realization.
- [x] Record all audit-derived decisions in the cumulative decision record.
  Evidence: `P2-I2-DEC-005`.
- [x] Validate that no graph-repository file changed. Evidence: frozen revision
  unchanged and final `git status --short` empty.

Exit gate `P2-I2-SOURCE-AUDIT-GATE`:

```text
frozen audit scope + complete capability matrix + exact provenance
+ native adequacy classifications + missing-surface distinctions
+ no source admission or lane-result overclaim
= passed
```

Disposition: `P2-I2-I01=complete` and
`P2-I2-SOURCE-AUDIT-GATE=passed` at original closeout. I01R1 has since
reopened that gate for fail-closed review; this historical disposition is not
the current gate state.

## 6A. `P2-I2-I01R1` — Capability-audit closeout revalidation

**Status:** complete; this subsection was frozen before any revalidation
inspection or classification beyond reading the owner-supplied review that
triggered the iteration.

**Iteration ID:** `P2-I2-I01R1`

**Purpose:** test the I01 package against the supplied capability-audit
closeout standard, quarantine any inadmissible candidate behavior from I01
evidence, and determine whether the source-audit gate can be re-passed from
admissible source-current evidence alone.

**Entry authority:** accepted P2-I2 brief, I01 input freeze and retained
outputs, cumulative decisions through `P2-I2-DEC-005`, and the owner-supplied
I01 closeout review received 2026-07-14.

**Frozen inputs and scope:** exact graph revision
`3d3d2ef25903d4210a67980f11fdd3ec21e9b6e5`; the retained I01 freeze,
narrative, matrix, provenance, source digests, decision, checklist, and
operational-hypothesis projection; and the thirteen review sections plus ten
final closeout conditions in the supplied review. Static read-only inspection
may revisit only the I01-frozen graph scope. No new dynamic candidate,
combined-versus-single, response, calibration, or boundary-rung probe is
authorized.

**Mutation and repository boundary:** RCAE P2-I2 governance, audit, matrix,
provenance, and revalidation-report artifacts only. The graph repository
remains read-only. Existing commands and outputs may be retained for
historical provenance while being explicitly excluded from capability or
scientific evidence.

**Required outputs:** one retained I01R1 revalidation report; an admissibility
disposition for every I01 command/evidence class; corrected audit, matrix,
decision, checklist, hypotheses, and navigation where required; exact
integrity validation; and either a re-passed source-audit gate or a retained
precise blocker.

**Evidence effect:** capability-audit validity and process correction only.
No source admission, realization or dependence-mode choice, calibration,
candidate evidence, control outcome, or L02 result.

### 6A.1 Frozen revalidation checks

- [x] Verify exact revision/worktree, path/callable/command scope, package
  identity, scope corrections, and the separation from brief preparation.
- [x] Validate the complete native causal composition without treating a bag
  of APIs or ecology-side reduction/injection as adequate.
- [x] Recheck the one-pool, attribution-only, public-support, intervention,
  and active-runtime-versus-audit-log boundaries.
- [x] Recheck state/history-mode neutrality without binding a realization or
  dependence mode.
- [x] Recheck restoration callable/digest/input/ownership/continuation
  boundaries and retain a state-ownership table.
- [x] Revalidate all eleven classifications under exactly the four frozen
  values and distinguish source facts, audit inferences, adequacy judgments,
  and open questions.
- [x] Revalidate minimal producer/constructed demands without selecting a
  design, response, comparator, or control matrix.
- [x] Confirm the shortlist remains bounded and non-selective.
- [x] Classify every executable I01 check as admissible interface evidence or
  quarantined candidate behavior; candidate behavior cannot support I01.
- [x] Cross-check narrative/matrix/provenance/digests/decisions/checklist,
  portable identities, stable IDs, reopening conditions, and graph status.

### 6A.2 Exit disposition

- [x] Retain the [I01R1 revalidation report](../reports/P2-I2-I01R1-capability-audit-closeout-revalidation.md)
  and all required corrections.
- [x] Demonstrate that every surviving capability claim is supported without
  quarantined candidate behavior.
- [x] Re-pass `P2-I2-SOURCE-AUDIT-GATE` or record the exact failed condition
  and keep I02 blocked.

Exit rule:

```text
all thirteen review areas + all ten final closeout conditions
+ candidate-behavior quarantine
+ capability matrix support from admissible evidence alone
+ no later-gate decision or evidence
+ unchanged graph worktree
= source-audit gate re-passed; otherwise fail closed
```

## 7. `P2-I2-I02` — Source admission and restoration transition

**Status:** complete as executed; corrected and revalidated by I02R1;
`P2-I2-SOURCE-ADMISSION-GATE=passed_after_revalidation`.

**Purpose:** admit only the source identities relevant to the selected next
decision and define any explicit restoration-provider transition.

**Iteration ID:** `P2-I2-I02`

**Entry authority:** accepted P2-I2 brief; corrected I01/I01R1 audit package;
`P2-I2-DEC-006`; RCAE entry revision
`10c18fad2ba8ecac9ddacb0f0bc55813e6356c60`.

**Frozen-input action:** construct and validate
[the I02 source-admission input freeze](../contracts/p2-i2/i02-source-admission-input-freeze.json)
from retained I01R1 evidence before recomputing a graph digest, rereading a
graph source/callable for admission, importing PyGRC, or writing an admission
disposition.

**Mutation and repository boundary:** RCAE P2-I2 contract, report, decision,
checklist, hypothesis-prerequisite, source-inventory, navigation, and master-
governance artifacts only. The graph repository remains read-only. Generated
temporary validation output may exist only under `${TMPDIR}`.

**Required outputs:** frozen I02 input contract; admitted-source digest and
callable manifest or reviewed non-admission record; narrative source-admission
and restoration-transition report; source-inventory update; cumulative
decision; checklist/evidence/change ledgers; integrity validation.

**Evidence effect:** exact source and provider admission only. No realization,
dependence-mode, response, comparator, calibration, candidate, control,
boundary-rung, or L02-result effect.

### 7.1 Input freeze before admission activity

- [x] Bind the exact RCAE entry revision, proposed graph revision, clean
  worktree requirement, and repository-relative identity rule.
- [x] Freeze the I01R1-derived proposed runtime-source, evidence-source, and
  public-callable scopes without treating them as admitted.
- [x] Freeze native-provider inputs, unsupported inputs, identity/digest
  distinction, external-state boundary, and prior/fallback-provider question.
- [x] Freeze the bounded equal-input continuation obligation separately from
  identity equality; do not execute it in I02.
- [x] Freeze read-only commands, output paths, classification values, change
  control, and fail-closed/non-evidence rules.
- [x] Validate the input-freeze JSON and record that only the freeze may be
  constructed before all preceding checks are complete.

Passing Section 7.1 authorizes only the exact read-only source-admission review
frozen there. It does not itself admit a source or provider.

The first in-scope runtime read exposed omitted public construction, queue-
processing, save, reset, and route-configuration callables before any admission
role or provider decision was assigned. `P2-I2-CHG-004` updates the freeze to
version `1.0.1`; the complete callable review was rerun before admission
closure.

### 7.2 Admission and provider disposition

- [x] Select the exact graph revision proposed for admission from I01 evidence.
- [x] Recompute and retain admitted file digests from that revision.
- [x] Bind repository revision, source files, runtime/package identity, and
  public callable identity without machine-local paths.
- [x] Bind native restoration identity and digest callables when applicable.
- [x] State accepted input scope and unsupported inputs.
- [x] Declare ecology-owned pool, producer, intervention, and configuration
  state outside native identity.
- [x] Declare the prior/fallback identity provider and its allowed scope.
- [x] Forbid silent provider upgrade or downgrade.
- [x] Define bounded equal-input continuation obligations separately from
  restoration-identity equality.
- [x] Preserve the graph closeout claim boundary.
- [x] Update the AE01 source inventory or retain a reviewed non-admission
  disposition.

### 7.3 Outputs and exit

- [x] Retain the admitted-source digest/callable manifest or reviewed non-
  admission record.
- [x] Retain the narrative source-admission and restoration-transition report.
- [x] Record all I02 decisions and evidence/change-ledger additions.
- [x] Validate JSON, portable paths, callable/source references, digests,
  Markdown links, graph revision/status, and no-I03-overreach.

Exit gate `P2-I2-SOURCE-ADMISSION-GATE` requires exact admitted identities or a
reviewed absence/inadequacy disposition. It grants no calibration or execution
authority.

## 7A. `P2-I2-I02R1` — Admission closeout revalidation

**Status:** complete;
`P2-I2-SOURCE-ADMISSION-GATE=passed_after_revalidation`.

**Trigger:** owner-supplied I02 closeout review received 2026-07-14.

**Change ID:** `P2-I2-CHG-005`

**Purpose:** independently revalidate I02 as an exact identity, authority, and
provider-transition result; correct any retention/governance defects without
selecting an I03 realization or treating restoration identity as restoration
correctness.

**Entry authority:** accepted P2-I2 brief; I01R1 audit package; I02 freeze,
manifest, report, source-inventory update, `P2-I2-DEC-007`, and checklist state
at review entry; owner-supplied I02 closeout review.

**Frozen-input action:** retain and validate an I02R1 closeout-review input
freeze that binds all entry artifact digests, the exact graph revision, the
review's fourteen areas and twelve gate conditions, read-only commands,
environment-bootstrap boundary, required outputs, and no-I03/no-evidence
rules before inspecting new graph source ranges, importing PyGRC, or running a
provider conformance check.

**Mutation and repository boundary:** RCAE P2-I2 contracts, reports,
validation script, decisions, checklist, hypothesis prerequisite, source
inventory, navigation, master governance, ignored local `.venv`, and `${TMPDIR}`
validation artifacts only. The graph repository remains read-only.

**Required outputs:** frozen I02R1 input contract; CHG-004 predecessor/current
freeze transition record; corrected admitted-source/provider manifest;
retained generic validator plus import-provenance and provider-contract
validation record; complete identity-coverage table; I02R1 narrative
revalidation; corrected source inventory, decision/checklist/change/evidence
ledgers, and navigation; integrity validation.

**Evidence effect:** admission integrity and provider-contract authority only.
No realization, dependence mode, response, comparator, calibration, candidate,
control, boundary-rung, restoration-correctness, or L02-result effect.

### 7A.1 Input freeze

- [x] Bind exact RCAE review-entry artifact digests separately from graph
  revision and graph file digests.
- [x] Freeze all review questions, source/callable/provider/coverage checks,
  CHG-004 governance checks, cross-artifact checks, and I03-leakage scan.
- [x] Freeze a generic imported-package provenance check that cannot execute
  candidate behavior.
- [x] Authorize ignored RCAE `.venv` creation only if needed for the frozen
  generic checks; forbid dependency substitution and graph-repository writes.
- [x] Freeze outputs, classification values, failure effects, and change
  control.
- [x] Parse and validate the I02R1 input contract before new review activity.

### 7A.2 Identity, authority, and provider checks

- [x] Reconstruct exact source identity, revision existence, clean/unchanged
  worktree, repository-relative paths, digests, and separate RCAE entry state.
- [x] Classify every source by runtime, public API, contract/schema, evidence/
  closeout, test/conformance, or documentation role as applicable.
- [x] Tie raw imported `pygrc` and callable provenance to the admitted checkout
  and normalize only the stable manifest identity.
- [x] Reconstruct CHG-004's predecessor scope, correct its governance class,
  retain predecessor/current semantic and file digests, and rerun the complete
  callable review without retaining an incomplete-scope conclusion.
- [x] Bind every public symbol's signature/accepted shape, source digest,
  supported/unsupported scope, causal relevance, and claim boundary.
- [x] Independently validate restoration-provider input rejection, identity
  determinism/canonicality, digest algorithm/encoding/recomputation, and raw-
  snapshot distinction without claiming restoration correctness.
- [x] Retain complete continuation-relevant native/external/unsupported
  identity coverage and block later branching on any unresolved component.
- [x] Revalidate conditional admission, configured provider selection,
  no-silent-fallback, provider-match, and identity-versus-continuation rules.
- [x] Revalidate lane-scoped non-retroactive source inventory and cross-
  artifact agreement.
- [x] Confirm no I03 scientific choice or positive evidence leaked into I02.

### 7A.3 Outputs and exit

- [x] Retain all required corrected machine and narrative artifacts.
- [x] Record `P2-I2-DEC-008`, CHG-005, evidence-ledger additions, and any
  exact correction to DEC-007 without erasing its historical disposition.
- [x] Run final JSON, digest, import/callable, provider, path/link, checklist,
  claim-boundary, graph-read-only, and `git diff --check` validation.
- [x] Re-pass `P2-I2-SOURCE-ADMISSION-GATE` or retain the exact failed
  condition and keep I03 blocked.

## 7B. `P2-I2-I02R2` — Reset-baseline persistence revalidation

**Status:** complete;
`P2-I2-SOURCE-ADMISSION-GATE=passed_after_i02r2_revalidation`.

**Trigger:** project owner reports that PyGRC has been updated to correct the
reset-baseline persistence gap retained by I02R1.

**Change ID:** `P2-I2-CHG-006`

**Purpose:** determine whether updated PyGRC preserves the public `reset()`
baseline across native snapshot/save/load restoration and covers that baseline
in the restoration identity, without selecting an I03 realization or treating
generic restoration conformance as scientific evidence.

**Entry authority:** accepted P2-I2 brief; I01R1 audit; I02/I02R1 admission
package and `P2-I2-DEC-008`; clean updated graph revision
`83e3a300426631ee4df71b661b67d4fcfdfed594`; owner request dated 2026-07-14.

**Frozen-input action:** before inspecting changed graph source or executing a
reset check, retain and validate an I02R2 input freeze binding the old and new
graph revisions, clean/read-only worktree, RCAE entry authority, changed-path
discovery rule, reset/snapshot/save/load/provider contract questions, generic
fixtures, legacy-compatibility checks, required outputs, and no-I03/no-evidence
boundary.

**Mutation and repository boundary:** RCAE P2-I2 contracts, validator, report,
decision, checklist, hypothesis prerequisite, source inventory, navigation,
and master governance only. PyGRC remains read-only. Generated validation
artifacts may be retained in RCAE or written temporarily under `${TMPDIR}`.

**Required outputs:** I02R2 input freeze; exact old-to-new graph source and
public-contract transition; checkout-bound reset/provider validator and
machine record; narrative revalidation; updated or failed admission manifest;
source inventory, decision, checklist/change/evidence ledgers, hypothesis
prerequisite, navigation, and integrity checks.

**Evidence effect:** source/provider restoration conformance only. No
realization, carrier, dependence mode, response, comparator, calibration,
candidate, control, restoration correctness beyond the tested generic reset
contract, boundary rung, or L02 result.

### 7B.1 Input freeze

- [x] Bind exact RCAE entry authority and old/new graph revisions separately.
- [x] Require graph worktree cleanliness before and after every check.
- [x] Freeze changed-path discovery plus affected source/callable/provider
  scope before reading changed implementation ranges.
- [x] Freeze generic reset-baseline fixtures and prohibit P2-I2 candidate
  behavior.
- [x] Freeze output paths, failure effects, change control, and I03 blocking.
- [x] Parse and validate the I02R2 freeze before source inspection or runtime
  validation.

### 7B.2 Reset and identity validation

- [x] Verify exact changed source/test/contract identities and checkout-bound
  imports at the updated revision.
- [x] Determine the declared reset-baseline serialization schema, provider
  schema/version transition, and legacy snapshot policy.
- [x] Show that a model and its native save/load restoration have equal current
  identity and equal `reset()` outcomes.
- [x] Show that reset-baseline-only differences change restoration identity or
  otherwise fail closed before branch comparison.
- [x] Show that repeated save/load cycles preserve the reset baseline.
- [x] Verify `set_state()` and any explicit rebasing operation follow their
  declared baseline semantics without silent rebasing.
- [x] Verify malformed or unsupported reset-baseline payloads fail according
  to the declared compatibility contract, with no fallback.
- [x] Confirm the old I02R1 reset restriction is removed only if every affected
  contract passes and the new source revision is admitted.

### 7B.3 Outputs and exit

- [x] Retain machine and narrative validation with exact source/import/test
  provenance and no candidate behavior.
- [x] Record `P2-I2-DEC-009`, CHG-006, source-inventory/manifest transition,
  and all affected hypothesis/checklist/navigation updates.
- [x] Run JSON, digest, import/provider, link/path, claim-boundary,
  graph-read-only, and `git diff --check` validation.
- [x] Re-pass `P2-I2-SOURCE-ADMISSION-GATE` or retain the exact failed
  condition and keep I03 blocked.

## 8. `P2-I2-I03` — Staged realization and operational-hypothesis program

**Status:** in progress through three review-separated mode sub-iterations.

**Purpose:** instantiate the subordinate operational hypotheses for all three
declared dependence modes without changing `AE01-H-L02`, resolving only one
mode per owner-reviewed sub-iteration.

Owner direction dated 2026-07-14 fixes this order and boundary:

```text
8A / P2-I2-I03A = state_carried
owner review
8B / P2-I2-I03B = history_carried
owner review
8C / P2-I2-I03C = hybrid
owner review
```

No later mode may be inspected, bound, or resolved inside an earlier mode's
sub-iteration. The umbrella discriminator gate remains open until the staged
program is complete and reviewed. This staging direction arrived after the
generic I03 input freeze validated but before realization comparison or
selection; `P2-I2-CHG-007` narrows that freeze to 8A without undoing a
scientific choice.

### 8.0 Owner-accepted mode-family retention correction

`P2-I2-CHG-008` records the project owner's 2026-07-14 acceptance of the
following scope rule before further I03A work:

```text
P2-I2 retains and tests state_carried, history_carried, and hybrid.
No later iteration selects one of those modes as the winner.
Within each mode, native is preferred when adequate; otherwise the smallest
adequate producer-assisted realization or a reviewed missing prerequisite is
retained.
```

- [x] Record the clarification in this active I03 checklist before editing the
  brief, hypothesis projection, decision record, or downstream iteration
  descriptions.
- [x] Preserve the original I03A input freeze and its entry digests; the
  clarification is a later owner-authorized scope transition, not a
  retrospective rewrite of what preceded state-carried comparison.
- [x] Correct the brief's singular `selected dependence mode` and `selected
  realization` language under `P2-I2-DEC-011`.
- [x] Require I04–I11 artifacts to remain mode-indexed and prohibit
  convenience-, availability-, calibration-, or outcome-based mode dropping.
- [x] Retain one bounded lane-level terminal classification while preserving
  separate realization, calibration, execution, control, and interpretation
  dispositions for all three modes.
- [x] Revalidate the current I03A package after the scope correction without
  executing a candidate, cell, control, matched null, or calibration action.

This accepted correction changes downstream scope but does not accept or
revise `P2-I2-DEC-010`, authorize I03B/I04, or assign scientific evidence.

### 8A. `P2-I2-I03A` — State-carried realization freeze

**Status:** causal design accepted by the project owner as the immutable
I03AR1 baseline; runtime adequacy and scientific support remain unassigned.

#### 8A.1 I03A activity declaration — 2026-07-14

```text
iteration_id = P2-I2-I03A
purpose = freeze one bounded state-carried realization, discriminator,
          interventions, and state-carried OP-01..OP-09 profile
entry_authority = RCAE 26811d395c0662473629d5710983e3c1fdb4f58f;
                  admitted PyGRC 83e3a300426631ee4df71b661b67d4fcfdfed594;
                  I01R1 and I02R2 passed
frozen_inputs_or_input_freeze_action = construct and validate the scoped
                  contracts/p2-i2/i03a-state-carried-realization-freeze-input.json
                  before implementation-surface comparison
mutation_and_repository_boundary = RCAE I03A contracts, hypotheses, decisions,
                  report, checklist, and navigation only; graph/PyGRC read-only;
                  no candidate, calibration, or matched-null execution
required_outputs = I03A input freeze; state-carried realization/discriminator
                   contract; state-carried operational-hypothesis profile;
                   I03A report; DEC-010; checklist disposition
evidence_effect = causal preregistration authority only; no calibration,
                  candidate evidence, control result, or L02 support result
exit_gate = P2-I2-I03A-REVIEW-READY; stop for owner review without starting
            I03B or opening I04
```

- [x] Record the I03A activity declaration before realization work.
- [x] Revise and parse the scoped I03A input freeze; retain exact entry
  revisions and authority digests while binding state-carried-only questions,
  the review stop, native-first selection rule, mutation boundary, required
  outputs, and failure effects. Evidence:
  [`i03a-state-carried-realization-freeze-input.json`](../contracts/p2-i2/i03a-state-carried-realization-freeze-input.json),
  SHA-256 `34d0903c746fb67abff5a1c12bb252b5cb15933d2de75e56f1232fbe7dfd0845`;
  15/15 entry digests and all 12 state-carried questions validated.
- [x] Confirm the graph/PyGRC worktree is clean at the admitted revision before
  reading admitted implementation sources for I03A. Evidence: exact revision
  `83e3a300426631ee4df71b661b67d4fcfdfed594`, clean after scoped-freeze
  validation.

The initial generic I03 freeze validated before the owner's staging direction:

- [x] Fifteen of fifteen entry-revision authority digests and all twelve
  generic questions validated in the same turn. Its pre-staging SHA-256 was
  `fb96012b3d353a0e0f8d69827317f0610d60a69f2b1b1bf16a167119ef9b51d2`.
- [x] The graph/PyGRC worktree was clean at admitted revision
  `83e3a300426631ee4df71b661b67d4fcfdfed594` before the staging direction.

I03A freezes causal meaning for `state_carried`: intervention targets,
causally held-fixed variables, qualitative invariance/divergence or direction,
and fail-closed scientific interpretation. It does not define numerical
resolution or a machine pass rule.

Evidence for every checked I03A design item below is
[`i03a-state-carried-realization-and-discriminator-contract.json`](../contracts/p2-i2/i03a-state-carried-realization-and-discriminator-contract.json),
[`P2-I2-I03A-state-carried-realization-and-operational-hypothesis-freeze.md`](../reports/P2-I2-I03A-state-carried-realization-and-operational-hypothesis-freeze.md),
`P2-I2-DEC-010`, and the
[static validation](../contracts/p2-i2/i03a-state-carried-realization-validation.json).

- [x] Select and justify one state-carried realization class—native,
  producer-assisted, or constructed—or retain why no bounded state-carried
  realization can preserve the discriminator.
- [x] Record every state-carried native-adequacy and producer-minimality
  consequence.
- [x] Bind `pool_dependence_mode = state_carried`; do not compare or bind
  `history_carried` or `hybrid` profiles in I03A.
- [x] Bind the common encounter-state carrier identity, non-private access
  witness, sources, contribution operations, and audit lineage.
- [x] Bind the state-carried `C_P`/`L`/`V` causal factorization to actual
  runtime interfaces.
- [x] Demonstrate from admitted dataflow that arbitrary attribution labels do
  not enter the response path.
- [x] Bind a state-changing common-carrier intervention and a state-preserving
  order/shuffle invariance; audit history remains non-causal in this profile.
- [x] Map all nine operational projections to state-carried cells, controls,
  expected qualitative relations, causally held-fixed variables, and
  fail-closed scientific effects.
- [x] Preserve all seven logical cells and five L02 controls.
- [x] Freeze the private-partition competitor and non-private access witness.
- [x] Record unresolved measurement choices for I04 rather than silently
  selecting them here.
- [x] Retain an I03A contract, report, DEC-010, hypothesis-profile update,
  validation evidence, and explicit owner-review stop.

Exit state `P2-I2-I03A-REVIEW-READY` is satisfied by the complete state-carried
package. It neither passes the umbrella `P2-I2-DISCRIMINATOR-GATE` nor
authorizes I03B, I04, calibration, or candidate execution.

### 8A-R1. `P2-I2-I03AR1` — State-carried runtime conformance

**Status:** `P2-I2-I03AR1-REVIEW-READY`; replacement evidence and its one
reconstruction passed 136/136 assertions after governed I03AR1R1 correction.

#### 8A-R1.1 Activity declaration — 2026-07-14

```text
iteration_id = P2-I2-I03AR1
purpose = determine whether the accepted I03A state-carried native candidate
          actually executes its declared writes, interventions, invariances,
          private guard, response path, restoration, and continuation
entry_authority = accepted I03A causal design; owner-accepted DEC-012/CHG-009;
                  admitted PyGRC 83e3a300426631ee4df71b661b67d4fcfdfed594
frozen_inputs_or_input_freeze_action = construct and validate a separate
          I03AR1 conformance freeze before the first mode-specific runtime call
mutation_and_repository_boundary = RCAE I03AR1 contracts, harness, reports,
          decisions, checklist, hypotheses, and navigation only; graph/PyGRC
          read-only; temporary artifacts permitted under ${TMPDIR}
required_outputs = immutable input freeze; deterministic harness; runtime
          receipt; raw conformance record; reconstruction; narrative report;
          DEC-012/CHG-009 disposition; explicit owner-review stop
evidence_effect = realization implementation-conformance only; no calibration,
          L02 support/falsification, control result, boundary rung, or terminal
          effect
exit_gate = P2-I2-I03AR1-REVIEW-READY or reviewed realization-inadequate stop;
            never automatic I03B authorization
```

- [x] Record I03AR1 in the checklist before new conformance design,
  implementation inspection, or runtime execution.
- [x] Project the owner-accepted conformance boundary into the hypothesis
  artifact before runtime work.
- [x] Complete the ignored RCAE `.venv` with exact direct dependency versions
  from the admitted graph `uv.lock`, retain the environment receipt, and
  prohibit ambient/system-package substitution.
- [x] Retain and parse an exact I03AR1 input freeze before the first runtime
  operation.
- [x] Bind one deterministic fixture, exact values, assertions, run/attempt
  count, environment, admitted imports, outputs, and reconstruction command.
- [x] Prohibit parameter search, rescue variants, scientific response/
  comparator selection, delta/calibration input, and use as L02 evidence.
- [x] Exercise the accepted native write, carrier intervention, lineage-label
  invariance, state-preserving order invariance, private-partition guard,
  later response, save/load/reset, and equal-input continuation boundaries.
- [x] Retain exact runtime/import/source identities and graph read-only guards.
- [x] Reconstruct the conformance record byte-for-byte and stop for owner
  review without beginning I03B.

### 8A-R1-R1. `P2-I2-I03AR1R1` — Frozen scalar-comparison correction

**Status:** complete; original invocation retained as `infrastructure_invalid`;
revised evidence and reconstruction passed; I03B remains unauthorized.

#### 8A-R1-R1.1 Activity declaration — 2026-07-14

```text
iteration_id = P2-I2-I03AR1R1
trigger = the one authorized I03AR1 evidence invocation stopped at
          combined_s1_s2.response_delta because native 0.5 + 0.1 was observed
          as 0.09999999999999998 after subtraction and the harness required
          strict equality with literal 0.1
classification = infrastructure_invalid; floating-point representation in the
                 assertion harness, not realization_inadequate and not an L02
                 result
retained_failed_attempt = freeze SHA-256 d21cc390ab6655ce98c7dbf6827a73d9b3d537c9d90cb98b81f8e2da510a1d94;
          harness SHA-256 3d2a12345343cd71e830a7dad6fc02bd6665cda60712f937d0ace4ce58fb5332;
          exit 1; no conformance output written
authorized_correction = compare only derived response deltas with frozen
          absolute tolerance 1e-12 and zero relative tolerance; retain every
          fixture value, branch, native call, causal assertion, run boundary,
          quarantine, and graph/source identity
run_effect = original invocation is permanently invalid; revised freeze may
          authorize one replacement evidence invocation and one reconstruction
          invocation; no additional retry
evidence_effect = none from the stopped invocation; replacement remains
          implementation-conformance only
exit_gate = return to P2-I2-I03AR1 review-ready work or stop fail-closed;
            never automatic I03B authorization
```

- [x] Record the stopped invocation, exact failure, absent output, and
  `infrastructure_invalid` classification before revising code or freeze.
- [x] Project the correction into the operational-hypothesis artifact before
  revising code or freeze.
- [x] Revise only the derived response-delta comparator and freeze its exact
  absolute/relative tolerances.
- [x] Retain a revised freeze and harness identity before the replacement
  runtime invocation.
- [x] Execute exactly one replacement evidence invocation and one
  reconstruction invocation; retain the original failed-attempt provenance.
- [x] Return to the I03AR1 owner-review stop without beginning I03B.

Exit state `P2-I2-I03AR1-REVIEW-READY` is satisfied by the immutable base
freeze, governed I03AR1R1 freeze revision, 136/136 replacement conformance,
byte-identical reconstruction, retained failed-attempt provenance, clean graph
guards, and scientific-evidence quarantine. It does not authorize I03B.

### 8B. `P2-I2-I03B` — History-carried realization freeze

**Status:** owner-accepted for staged progression under `P2-I2-DEC-015`. The
causal design and exact runtime sub-freeze were retained before execution;
bounded conformance passed and reconstructed byte-identically. At I03B close,
only I03C opened under its own freeze; DEC-020 later opened I04 after the
complete family closeout.

#### 8B.1 Activity declaration — 2026-07-14

```text
iteration_id = P2-I2-I03B
purpose = independently select and freeze the history-carried realization,
          causal factorization, interventions, private/access guards, and
          operational-hypothesis profile; then determine bounded runtime
          conformance under a second freeze
entry_authority = owner acceptance of the review-ready I03A/I03AR1 package and
                  explicit direction to move to 8B; DEC-011/DEC-012; admitted
                  PyGRC 83e3a300426631ee4df71b661b67d4fcfdfed594
frozen_inputs_or_input_freeze_action = first retain an I03B design/source-
          comparison freeze; select native, minimally producer-assisted, or
          missing-prerequisite disposition within history_carried mode; only
          then retain a separate exact runtime-conformance freeze before the
          first history-carried runtime call
mutation_and_repository_boundary = RCAE I03B contracts, harness, reports,
          decisions, checklist, hypotheses, and navigation only; graph/PyGRC
          read-only; temporary artifacts permitted under ${TMPDIR}
required_outputs = immutable design input freeze; source/dataflow comparison;
          history-carried realization and operational-hypothesis contract;
          static validation; if realizable, immutable runtime input freeze,
          deterministic harness, runtime receipt, raw conformance record,
          byte reconstruction, narrative report, decision/change disposition,
          and explicit owner-review stop
evidence_effect = causal-design authority plus quarantined realization
          implementation-conformance only; no calibration, L02 support/
          falsification, control result, boundary rung, or terminal effect
exit_gate = P2-I2-I03B-REVIEW-READY or reviewed history-carried missing-
            prerequisite/inadequate stop; never automatic I03C authorization
```

- [x] Record I03B in the checklist before history-carried source comparison,
  design selection, harness construction, or runtime execution.
- [x] Project I03B's active/unbound and no-scientific-evidence status into the
  operational-hypothesis artifact before design work.
- [x] Retain and validate an I03B design input freeze before comparing history-
  carried realization candidates.
- [x] Prohibit I03A/I03AR1 observed outputs from selecting the I03B carrier,
  values, interventions, response, or realization class.
- [x] Define active causal history versus audit-only lineage, including the
  exact response read path and forbidden state-only/controller shortcuts.
- [x] Apply native-first selection within `history_carried`: use admitted
  native machinery when adequate, otherwise the minimal explicit RCAE
  producer, or retain a missing-prerequisite disposition.
- [x] Freeze source roles, common non-private access, contribution/history
  constitution, history intervention, state-preserving history contrast,
  private-partition competitor, restoration ownership, and producer boundary.
- [x] Preserve all seven logical cells, five L02 controls, and OP-01..OP-09
  without rewriting the accepted state-carried profile.
- [x] Retain a machine contract, static validator/result, narrative design
  report, and decision disposition before any history-carried runtime call.
- [x] If the design is realizable, retain and validate a separate exact runtime
  fixture, assertions, import/source identities, one evidence invocation, one
  reconstruction invocation, zero retries, and full scientific quarantine.
- [x] Exercise only the frozen history-carried causal path, interventions,
  guards, restoration/reset, and equal-input continuation boundaries.
- [x] Reconstruct byte-for-byte and stop for owner review without beginning
  I03C or I04.

#### 8B.2 Frozen design disposition

`P2-I2-DEC-014` selects `minimally_producer_assisted` after static comparison
of the three frozen dispositions. PyGRC's ordered packet/contact history is
native, restored, and useful as audit/input authority, but its rows are
passive evidence. Native feedback reads the latest contact plus live node
state; neither that path nor LGRC-0 annotations supplies an active,
independently intervenable multi-event history.

The selected `RCAEActiveHistoryAdapterV1` owns one missing separable
operation: one ordered, source-label-free, independently intervenable history
carrier `H_P` over admitted physical contribution rows. It materializes a
deterministic order-sensitive readout at native node `M_H` through public
native balancing packets. It stops there. It may not mutate PyGRC state
directly, retain source identity in causal tokens, inspect response state,
apply the response threshold, write success, or schedule the later response.
PyGRC owns native coherence mutation and the complete M_H-to-feedback-to-later-
packet response path.

The design freezes active-history reorder/clamp, state-only separation,
native write diversion, pure-label invariance, separate H1/H2 private
carriers with no common read, and one H_P/M_H access scope. Native v2 identity
must be composed with adapter current state, cursor/configuration,
interventions, and adapter reset baseline. Save/load/reset are paired
composite operations; no one-sided reset or implicit rebase is permitted.

Machine authority:
[I03B contract](../contracts/p2-i2/i03b-history-carried-realization-and-discriminator-contract.json),
SHA-256 `8fc575089017c0e429f04bb221092493634bba4a6adcd4fc22ca36a5b238c38d`.
No history-carried model was instantiated and no runtime operation occurred
during this design selection.

#### 8B.3 Runtime-conformance freeze

The separate
[I03B runtime freeze](../contracts/p2-i2/i03b-history-carried-runtime-conformance-input-freeze.json),
SHA-256 `dd0146f656f3f480d5ff3265696cacf39322fa5fe13991aed822614eee217720`,
validated without model instantiation. It binds the adapter and harness,
environment/import/source identities, twelve exact fixture branches,
history/order and label guards, active-history clamp, state-only separation,
private partitions, alternate access, paired composite save/load/reset,
equal-input continuation, one evidence invocation, one reconstruction, zero
retries, and the full scientific-evidence quarantine.

The exact conformance values are fixture-only and prohibited from I04/I06 or
scientific reuse. The next permitted action is the sole evidence invocation;
failure follows the frozen realization/missing-prerequisite/infrastructure
classification and cannot trigger tuning or a rescue branch.

#### 8B.4 Runtime-conformance disposition and review stop

The sole evidence invocation passed `252/252` frozen assertions. The sole
reconstruction produced the same SHA-256
`4465ff2174d285d26ffa8a6cb4bebaf644b150d24bea0d69563eb5f51d8c177d`
and was byte-identical to the retained
[runtime conformance](../contracts/p2-i2/i03b-history-carried-runtime-conformance.json).
The
[reconstruction receipt](../contracts/p2-i2/i03b-runtime-reconstruction-receipt.json)
records one evidence invocation, one reconstruction, zero retries, twelve
branches per invocation, clean graph identity, and paired composite
save/load/reset/continuation witnesses.

The fixture demonstrated only implementation conformance: equal-marginal and
equal-P physical order variants produced different H_P/readout/native-response
branches; lineage permutation was causally invariant; active-history clamp
changed the response with P retained; state-only P debit preserved the
H_P/M_H response; private histories remained separately readable only; and
alternate access used the same M_H/B_ref path. The adapter never computed or
scheduled success, and PyGRC owned every native mutation and later response.

`P2-I2-I03B-REVIEW-READY` is satisfied. No fixture value, branch outcome, or
digest may enter I04/I06 or scientific evidence. I03C and I04 remain
unauthorized pending explicit owner review/acceptance.

No history-carried surface comparison or binding occurred during I03A/I03AR1.
I03B may cite those artifacts only as fixed earlier-mode and governance
boundaries, never as history-carried selection evidence.

### 8B-R1. `P2-I2-I03BR1` — I03B closeout revalidation

**Status:** complete; zero-runtime closeout revalidation passed with no
blocking finding. Owner acceptance remains pending. I03C/I04 remain
unauthorized.

#### 8B-R1.1 Activity declaration — 2026-07-14

```text
iteration_id = P2-I2-I03BR1
purpose = independently revalidate I03B against the owner-supplied twenty-one-
          point acceptance review, prioritizing exclusion of a hidden latest-
          contact response path and confirmation that H_P plus its M_H output
          port is the functional active-history pool
entry_authority = review-ready I03B package plus project-owner request for the
                  supplied validation suggestions to be checked
frozen_inputs_or_input_freeze_action = retain a machine-readable review/input
          freeze before inspecting the frozen harness, native source dataflow,
          conformance branches, identities, and control mappings
mutation_and_repository_boundary = RCAE I03BR1 checklist, hypothesis,
          validation contract/result, report, decision/change record, and
          navigation only; graph/PyGRC read-only; I03B freezes, harness,
          adapter, and retained runtime evidence immutable
runtime_policy = zero model instantiations and zero new evidence,
          reconstruction, retry, rescue, calibration, candidate, or control
          invocations; exhausted I03B invocation accounting is preserved
evidence_effect = source/dataflow and retained-artifact acceptance validation
          only; no scientific evidence, calibration input, registration value,
          R01-R05 assignment, mode ranking, or terminal effect
exit_gate = P2-I2-I03BR1-CLOSEOUT-PASSED or explicit blocking finding; never
            automatic I03C/I04 authorization
```

- [x] Record I03BR1 in the checklist before revalidation activity.
- [x] Project I03BR1's active, zero-runtime, no-scientific-effect status into
  the operational hypotheses before revalidation activity.
- [x] Retain a machine-readable input freeze mapping all twenty-one review
  sections and twelve concise acceptance statements to exact audit tests.
- [x] Trace every field consumed by native feedback emission and production;
  establish a matched neutral latest contact or prove differing contact fields
  are outside V.
- [x] Verify H_P is persistent, independently intervenable active state and
  M_H is its declared native output port, including clamp semantics.
- [x] Revalidate the complete P/H_P/L/U_H/R_H/M_H/V factorization, physical
  token typing, exact admission rule, cursor/idempotency isolation, order-state
  matching, and bounded history claim.
- [x] Revalidate stable history clamp, state-only debit exclusion, matched
  write diversion, private no-common-read, and alternate-access eligibility.
- [x] Revalidate adapter forbidden/allowed operations and counterfactual
  producer minimality against all admitted native candidates.
- [x] Classify H_P capacity, saturation, leakage, depletion, maintenance, and
  replacement semantics without selecting scientific numeric values.
- [x] Revalidate complete composite current/reset identity, paired operations,
  partial-load failure, no implicit rebase, and cursor continuation.
- [x] Verify mechanical scientific quarantine and the complete isolated
  twelve-branch matrix using only retained artifacts.
- [x] Confirm I03A remains independently retained, I03C remains untouched, and
  any later owner acceptance can authorize only I03C while I04 stays blocked.
- [x] Retain machine validation, narrative closeout report, and governance
  disposition; stop for owner review without beginning I03C.

#### 8B-R1.2 Closeout disposition

The frozen
[I03BR1 machine revalidation](../contracts/p2-i2/i03br1-closeout-revalidation.json)
passed all twenty-one review checks: fifteen directly and six with explicit
downstream obligations. There were zero blockers, zero model instantiations,
and zero runtime, reconstruction, retry, rescue, candidate, control,
calibration, or scientific invocations. The
[closeout report](../reports/P2-I2-I03BR1-history-carried-closeout-revalidation.md)
retains the full source/dataflow reasoning.

The two priority findings are:

1. A common neutral contact follows materialization. Across the order branches
   its physical route/contact/schedule fields match. Only node-proper-time and
   derived digests differ; native feedback does not use those differences in
   the polarity/threshold decision, and `expected_source_surface_digest` is
   null. The response difference is carried by M_H.
2. H_P is persistent adapter state and the clamp replaces H_P itself before
   R_H recomputation and native M_H rematerialization. The functional pool is
   H_P plus its M_H output-port binding, never P or M_H alone.

The selected lifecycle is run-bounded append-only under normal admission,
with explicit whole-history replacement and no autonomous depletion,
saturation, leakage, or maintenance transition. The bounded claim is active
ordered history causally materialized through a scalar readout; irreducible
raw-history and non-Markovian claims remain prohibited.

Six non-blocking duties remain explicit for later stages: I06 must preserve a
unique source-to-P path or register a route key, resolve scientific access,
bound lifecycle/event counts, make paired restoration the only registered
continuation interface with manifest-hash validation, and retain branch
identity obligations; I04/I06 validators must reject every conformance fixture
value/digest while importing only the pre-runtime structural family.

`P2-I2-I03BR1-CLOSEOUT-PASSED` is satisfied. At that review boundary it made
I03B acceptance-ready but did not itself accept I03B, authorize I03C/I04, pass
the umbrella gate, assign R01-R05, or create scientific evidence. The later
owner decisions remain separate authority.

### 8C. `P2-I2-I03C` — Hybrid realization freeze

**Status:** owner-accepted for progression under `P2-I2-DEC-018`; design/static
validation and the separately frozen 258/258 byte-reconstructed runtime
conformance passed. No hybrid source comparison, design selection, or runtime
operation preceded this declaration/freeze sequence. I04 opened only later
under DEC-020 after compact family closeout.

#### 8C.1 Activity declaration — 2026-07-14

```text
iteration_id = P2-I2-I03C
purpose = independently select and freeze the hybrid realization, separable
          state/history factorization, interventions, private/access guards,
          restoration ownership, and operational-hypothesis profile; then
          determine bounded runtime conformance under a second freeze
entry_authority = owner acceptance of I03B/I03BR1 for staged progression and
                  explicit direction that 8C is next; DEC-011, DEC-012, and
                  DEC-015; admitted PyGRC revision
                  83e3a300426631ee4df71b661b67d4fcfdfed594
frozen_inputs_or_input_freeze_action = first retain an I03C design/source-
          comparison freeze; compare native, minimally producer-assisted, and
          missing-prerequisite dispositions within hybrid mode; only then may
          a separate exact runtime-conformance freeze authorize one bounded run
mutation_and_repository_boundary = RCAE I03C contracts, adapter/harness if
          selected, reports, decisions, checklist, hypotheses, and navigation
          only; graph/PyGRC read-only; I03A/I03B artifacts immutable
required_outputs = immutable design input freeze; native-first source/dataflow
          comparison; hybrid realization and operational-hypothesis contract;
          static validation; if realizable, immutable runtime input freeze,
          deterministic harness, runtime receipt, raw conformance record,
          byte reconstruction, narrative report, and owner-review stop
evidence_effect = hybrid causal-design authority plus quarantined realization
          implementation-conformance only; no calibration, L02 support/
          falsification, control result, boundary rung, mode ranking, or
          terminal effect
exit_gate = P2-I2-I03C-REVIEW-READY or reviewed hybrid missing-prerequisite/
            inadequate stop; never automatic discriminator-gate or I04 pass
```

- [x] Record I03C in the checklist before hybrid source comparison, design
  selection, harness construction, or runtime execution.
- [x] Project I03C's active/unbound and no-scientific-evidence status into the
  operational hypotheses before design work.
- [x] Retain and validate an I03C design input freeze before comparing hybrid
  realization candidates.
- [x] Import I03A and I03B only as fixed earlier-mode causal/governance
  boundaries; prohibit their fixture observations from selecting I03C values,
  response, factorization, or realization class.
- [x] Define a genuinely hybrid factorization with separately identified
  state and active-history causal components, one joint response read, and no
  relabeling of either earlier mode as hybrid.
- [x] Freeze independent history-only, state-only, joint, write-diversion,
  label-invariance, private-partition, and alternate-access interventions that
  distinguish hybrid dependence from state-only or history-only shortcuts.
- [x] Apply native-first selection within `hybrid`: use admitted native
  machinery where adequate, otherwise the minimal explicit RCAE producer, or
  retain a missing-prerequisite disposition.
- [x] Freeze exact ownership and permitted/forbidden inputs for native state,
  active history, readout/materialization, joint V, audit lineage, adapter or
  producer, and later native response.
- [x] Preserve all seven logical cells, five L02 controls, and OP-01..OP-09
  without rewriting the accepted state-carried or history-carried profiles.
- [x] Freeze composite current/reset identity and paired continuation duties
  for every external state component; retain all I03BR1 admission,
  restoration, lifecycle, branch-identity, and quarantine obligations.
- [x] Retain a machine contract, static validator/result, narrative design
  report, and decision disposition before any hybrid runtime call.
- [x] If realizable, retain and validate a separate exact runtime fixture,
  assertions, import/source identities, one evidence invocation, one
  reconstruction invocation, zero retries, and full scientific quarantine.
- [x] Exercise only the frozen hybrid causal path, independent interventions,
  guards, paired restoration/reset, and equal-input continuation boundaries.
- [x] Reconstruct byte-for-byte and stop for owner review without beginning
  I04 or passing the umbrella discriminator gate.

Exit state `P2-I2-I03C-REVIEW-READY` is satisfied by the immutable design and
runtime freezes, passed static validation, one `258/258` evidence invocation,
one `258/258` byte-identical reconstruction, complete P-only/H-only joint-path
guards, paired save/load/reset and equal-input continuation, clean graph
guards, and scientific quarantine. Runtime SHA-256:
`217c8972e8e1199409343fb72b0eca12b2ba24dceb6a1f213c97af9143f0e96c`.
This does not pass the umbrella discriminator gate or authorize I04.

No hybrid surface comparison or binding occurred during I03A, I03B, or
I03BR1. I03C may cite those artifacts only as immutable prior-mode and
governance boundaries.

### 8C-R1. `P2-I2-I03CR1` — Hybrid closeout revalidation

**Status:** `P2-I2-I03CR1-CLOSEOUT-PASSED`; 26/26 review checks and 17/17
acceptance conditions passed with zero blockers. Eight fail-closed downstream
obligations are retained. I03C is acceptance-ready but not owner-accepted by
this audit; the umbrella closeout and I04 remain unauthorized.

#### 8C-R1.1 Activity declaration — 2026-07-14

```text
iteration_id = P2-I2-I03CR1
purpose = revalidate the bounded hybrid package against the exact twenty-six
          review areas and seventeen acceptance conditions; retain explicit
          carrier/authority/factorial/admission/neutral-contact/restoration/
          lifecycle/quarantine meanings and classify every non-blocking
          registration duty without rewriting or rerunning I03C
entry_authority = owner-supplied review at attachment SHA-256
                  df1e823f2ff640713638b2b08266de45b99c5410bdd880f4380e75016e7a0298;
                  DEC-011, DEC-012, DEC-015, DEC-016; exact retained I03C hashes
frozen_inputs_or_input_freeze_action = retain an immutable I03CR1 input that
          binds the review digest, I03C artifacts/source identities, all audit
          questions, zero-runtime policy, and direct-pass/clarification/
          downstream-obligation/blocker classification rules before audit
mutation_and_repository_boundary = RCAE I03CR1 freeze, static validator,
          closeout result/report, checklist, hypotheses, decision/change
          records, and a machine quarantine/obligation registry only; no I03C
          artifact rewrite; graph/PyGRC read-only
required_outputs = exact review input freeze; machine-readable hybrid carrier,
          qualitative 2x2, admission exclusion, layered identity, lifecycle,
          and fixture-quarantine registry; static validator/result; closeout
          report; explicit blocker count and next-authority boundary
runtime_budget = zero model instantiations, zero candidate/control/conformance
          branches, zero reruns, zero reconstructions, zero parameter search
evidence_effect = retained-artifact causal-well-formedness and acceptance
          validation only; no new implementation or scientific evidence
exit_gate = P2-I2-I03CR1-CLOSEOUT-PASSED with owner acceptance still pending,
            or explicit retained blocker; never automatic umbrella/I04 pass
```

- [x] Record I03CR1 and its zero-runtime boundary before auditing the review.
- [x] Project the active closeout review and no-I04 effect into the operational
  hypotheses before audit.
- [x] Freeze the exact review digest, retained I03C artifact identities,
  twenty-six review areas, seventeen acceptance tests, and classification
  rules before source/evidence inspection.
- [x] Establish one stable hybrid carrier identity over P, authoritative H_P,
  M_H output-port binding, `[P,M_H]/[B_ref]` access, V, and separate L; reject
  P/H_P/M_H/mask/adapter/feedback-row substitutions.
- [x] Retain the bounded architectural distinction between native current-
  state response mechanics and independently persistent/intervenable H_P;
  explicitly reject irreducible-history or non-Markovian overclaim.
- [x] Verify P and H_P each enter the same native V independently, neither is
  encoded in the other, and both intervention chains preserve held-fixed
  components rather than acting through scheduler/contact/configuration side
  effects.
- [x] Freeze the complete qualitative P reference/candidate × H reference/
  candidate 2x2 for I04/I06 without importing fixture values or requiring all
  four cells to have been executed during conformance.
- [x] Retain raw P, R_H/M_H, native joint score/polarity, schedule decision, and
  later continuation; prohibit threshold crossing from defining hybrid and
  prohibit nonlinear interaction/synergy/irreducibility claims.
- [x] Prove from exact filter/dataflow identities that only registered
  physical S-role-to-common-P arrivals are admissible exactly once and that
  materialization, neutral contact, debit, response, feedback, reset/load,
  private, and diversion traffic cannot self-admit.
- [x] Resolve unique-route adequacy for the conformance fixture and retain the
  I06 explicit route/channel-key duty without using arbitrary labels or row/
  packet/event digests as causal authorization.
- [x] Validate the neutral contact's common configuration, final relative
  position, causal neutrality, admission exclusion, empty-queue boundary,
  latest-row role, and null digest requirement; classify absolute audit time/
  digest differences only after proving they do not enter score/threshold.
- [x] Validate exact-once distinct P/M_H masks, fixed B_ref, no aliases/extra
  nodes, live-state rather than stale-cache reads, order-insensitive native
  summation, and private-pair-only masks.
- [x] Retain one common P/H_P/M_H pool binding and verify private native nodes,
  adapters, cursors, baselines, masks, and no-dispatch/no-cross-pair guards;
  carry exact cross-load rejection into I06 if not executable in conformance.
- [x] Retain a complete layered identity over native v2, adapter current/reset,
  code/schema/filter/readout, joint/private bindings, masks, neutral/intervention
  policy, fixture/freeze, snapshot manifest, and evidence identities; distinguish
  demonstrated composite equality from the still-deferred registered atomic
  load/reset interface.
- [x] Verify H_P is authoritative, M_H must equal registered R_H(H_P) before V,
  and disagreement fails closed; cover pre-response, clamp/order, save/load,
  reset, and equal-input continuation boundaries.
- [x] Classify history length/overflow/window/truncation/saturation/leakage/
  clamp/reset/maintenance and P/M_H bounds as implemented, fixture-bounded,
  deferred, not applicable, or construction debt with rationale.
- [x] Audit all nine OPs for hybrid-specific meanings without rewriting I03A
  or I03B and without assigning R01-R05.
- [x] Retain a machine rejection registry for every I03A/I03B/I03C fixture
  coefficient, amount, threshold, topology/branch identity, observation,
  comparator, assertion result, and evidence digest; require later I04/I06
  validators to reject direct or trivial serialized reuse.
- [x] Verify 258/258 remains machine-classified as implementation conformance
  only, all three modes remain retained/unranked, and owner acceptance can open
  only a separately declared umbrella I03 family closeout—not I04 directly.
- [x] Produce a direct-pass/clarification/downstream-obligation/blocker matrix,
  run zero-runtime validation, and stop for owner review without opening the
  umbrella gate or I04.

#### 8C-R1.2 Closeout disposition — 2026-07-14

The immutable input and machine registry validated all twenty-six review areas
and all seventeen acceptance conditions. Classification counts are seventeen
direct passes, four closure clarifications, five downstream-obligation passes,
and zero blockers. The audit instantiated no model, ran no retained branch,
and left the single I03C evidence invocation and single reconstruction
unchanged.

The closeout explicitly records three bounded qualifications: I03C did not
execute the complete future scientific 2x2; restoration authority is a
layered package rather than one new native atomic API; and neutral-contact
absolute scheduler slots differ after explicit intervention operations even
though those slots do not enter the native score or threshold. Eight exact
fail-closed I04/I06/family-closeout obligations retain the corresponding
future work.

Exit state `P2-I2-I03CR1-CLOSEOUT-PASSED` is satisfied by the
[input freeze](../contracts/p2-i2/i03cr1-closeout-revalidation-input.json),
[hybrid closeout registry](../contracts/p2-i2/i03cr1-hybrid-closeout-registry.json),
[machine revalidation](../contracts/p2-i2/i03cr1-closeout-revalidation.json),
[validator](../scripts/p2_i2_i03cr1_validate.py), and
[closeout report](../reports/P2-I2-I03CR1-hybrid-closeout-revalidation.md).
This makes I03C acceptance-ready only. Owner acceptance may authorize a new
checklist-first umbrella I03 family closeout; it may not authorize I04
directly.

### 8.1 Umbrella I03 exit boundary

**Iteration:** `P2-I2-I03F`

**Status:** complete and owner accepted; compact composition passed 12/12
integration checks and 9/9 acceptance conditions with zero blockers. No mode
review was repeated. `P2-I2-DISCRIMINATOR-GATE=passed`; I04 construction is
authorized under its own declaration.

#### 8.1.1 Activity declaration — 2026-07-14

```text
iteration_id = P2-I2-I03F
purpose = close the staged I03 family without choosing among modes by composing
          the already accepted mode closeouts into one lossless index over
          retained profiles, OP-01..OP-09, obligations, quarantine, restoration
          ownership, and unchanged mode-indexed I04 import
entry_authority = owner direction "we can move to 8.1 next" after
                  P2-I2-I03CR1-CLOSEOUT-PASSED; DEC-011, DEC-012, DEC-013,
                  DEC-015, DEC-016, DEC-017; all retained I03 mode artifacts
frozen_inputs_or_input_freeze_action = retain an immutable I03F input binding
          the accepted terminal authority for each mode, exact closeout/evidence
          identities, graph revision, compact integration checks, zero-runtime
          policy, and gate/owner-review effect before family composition
mutation_and_repository_boundary = RCAE I03F input, compact machine family
          index, static index validator/result, report, checklist, hypotheses,
          and decision/change records only; no reopening of accepted mode
          capability/source/dataflow findings, no I03 rewrite, graph read-only
required_outputs = exact compact family-closeout input; lossless three-mode OP,
          restoration-owner, obligation, quarantine, and I04-import index;
          static index validation; closeout report; explicit blocker count and
          owner-review boundary
runtime_budget = zero model instantiations, zero conformance/reconstruction/
          candidate/control branches, zero retries, zero parameter search
evidence_effect = accepted-authority composition and discriminator-gate
          readiness only; no repeated mode review, new implementation evidence,
          or scientific evidence
exit_gate = P2-I2-I03F-REVIEW-READY or explicit retained blocker; only a later
            owner disposition may pass P2-I2-DISCRIMINATOR-GATE and open I04
```

- [x] Record I03C/I03CR1 owner acceptance for progression and declare I03F in
  the checklist before any family audit.
- [x] Project I03F's zero-runtime, no-ranking, no-I04 boundary into the
  operational hypotheses before audit.
- [x] Freeze the accepted terminal decision/closeout authority for each mode
  plus exact evidence identities needed to prevent substitution; do not replay
  already accepted mode reviews.
- [x] Retain state-carried, history-carried, and hybrid as three required
  downstream modes with realization classes `pygrc_native_candidate`,
  `minimally_producer_assisted`, and `minimally_producer_assisted`; perform no
  selection, rank, preference, or supersession.
- [x] Cross-check only the accepted contract identities needed to show that
  I03B/I03C do not replace I03A, I03C does not replace I03B, and shared symbols
  retain mode-qualified rather than collapsed meanings.
- [x] Index, without re-proving, each accepted mode's carrier, write/update
  relation, access mask, intervention family, private/common binding, producer
  prohibition, and realization class.
- [x] Build a complete OP-01..OP-09 × three-mode pointer index and verify no OP
  or mode is absent; do not reassess the accepted mode-level causal evidence.
- [x] Retain the accepted native-first/producer-minimality boundary and index
  restoration ownership as native v2 for state-carried versus paired native-v2/
  adapter identity for history-carried and hybrid.
- [x] Consolidate every I03BR1 and I03CR1 downstream obligation without loss,
  duplication ambiguity, premature discharge, or transfer to the wrong owner
  iteration.
- [x] Consolidate the complete I03A/I03B/I03C fixture quarantine and require
  mechanical I04/I06 rejection of exact and trivially serialized reuse.
- [x] Freeze the I04 import boundary: all three profiles enter unchanged and
  mode-indexed; I04 may select measurements/comparators/calibration identities
  but cannot alter I03 causal semantics, remove a mode, or inherit fixture
  values/outcomes.
- [x] Verify the admitted graph revision remains clean/unchanged and that no
  source-capability re-audit, model/runtime, or reconstruction execution occurred
  in I03F.
- [x] Produce a machine blocker/gate-readiness result and family closeout report,
  then stop for owner review without passing the discriminator gate or opening
  I04 automatically.

#### 8.1.2 Compact family-closeout disposition — 2026-07-14

The compact validator matched all eleven terminal authorities to accepted
baseline commit `fc3fb0f638eb0b180cb05d081e6dc447f24af66b` and passed all
twelve integration checks and nine acceptance conditions with zero blockers.
It did not repeat any mode-level capability, source, dataflow, restoration, or
runtime review.

The retained index contains three unranked required modes, 27 exact OP pointers,
fourteen losslessly copied source obligations mapped exactly once into nine
consolidated duties, the complete seven-source fixture quarantine, mode-specific
restoration ownership, and an unchanged mode-indexed I04 import rule. At I03F
freeze no source obligation was discharged and the family-gate duty remained
pending; DEC-020 subsequently supplied that owner disposition without rewriting
the immutable index.

Exit state `P2-I2-I03F-REVIEW-READY` is satisfied by the
[input freeze](../contracts/p2-i2/i03f-family-closeout-input.json),
[family index](../contracts/p2-i2/i03f-family-closeout-index.json),
[machine validation](../contracts/p2-i2/i03f-family-closeout-validation.json),
[validator](../scripts/p2_i2_i03f_validate.py), and
[compact report](../reports/P2-I2-I03F-family-closeout.md). DEC-020 subsequently
accepted this package, passed the discriminator gate, and opened only I04.

Exit gate `P2-I2-DISCRIMINATOR-GATE` requires the complete reviewed staged
family and opens calibration preregistration only. If no bounded realization
can preserve one or more mode-specific discriminators, I03 may instead retain
a reviewed missing-prerequisite disposition without treating it as a negative
L02 result.

## 9. `P2-I2-I04` — Calibration preregistration construction

**Status:** original candidate-free package retained as validated history after
owner review withheld CAL-PRE passage. I04R1 resolved the primary-comparator
conflict and response/null correctness duties and passed focused validation;
I04R2 is the owner-accepted sole progression authority under DEC-026. No
matched-null or candidate execution occurred during I04–I04R2.

### 9.1 Activity declaration — 2026-07-14

```text
iteration_id = P2-I2-I04
purpose = freeze before any calibration or candidate outcome the exact
          mode-indexed scientific response, orientation, closest insufficient-
          repetition comparator, aggregation/missingness, signed control rules,
          candidate-blind matched-null design, analysis identity, and stopping
          policy imported unchanged from the accepted I03 family
entry_authority = owner direction "in that case, let's continue with I04";
                  owner-accepted I03F under DEC-020; accepted P2-I2 brief,
                  L02 metric sheet, I03F family index, and all frozen common
                  outcome/stopping/interpretation contracts
frozen_inputs_or_input_freeze_action = first retain an I04 choice-resolution
          input binding accepted semantic authorities, candidate/runtime/null
          absence, complete I03 fixture quarantine, available response/
          comparator options, and decision criteria; freeze the final
          preregistration only after those choices are justified
mutation_and_repository_boundary = RCAE I04 input, measurement/calibration
          preregistration, pure analysis/null-generation policy or code only
          if required, static validators/results, report, checklist,
          hypotheses, and decisions; graph/PyGRC read-only
required_outputs = exact per-mode response/comparator/control matrix; shared-
          versus-mode-specific equivalence decisions; aggregation/missingness/
          resolution rules; candidate-blind null freeze for I05; fixture-reuse
          rejection; analysis identity; machine validation; I04 report
execution_budget = zero candidate operations and zero matched-null calibration
          executions; static validation and candidate-free config construction
          only
evidence_effect = scientific measurement and calibration-method preregistration
          only; no resolution result, implementation registration, control
          outcome, R01-R05 assignment, or L02 support/falsification
exit_gate = P2-I2-CAL-PRE-GATE after owner review, or explicit retained blocker;
            never automatic I05 execution or candidate authority
```

- [x] Record owner acceptance of I03F, pass only the discriminator gate, and
  declare I04 before resolving any measurement choice.
- [x] Project I04's candidate-free choice boundary into the operational
  hypotheses before studying response/comparator options.

I04 imports all three reviewed I03 causal profiles unchanged. It freezes their
exact raw measurement, equality/resolution rule, numerical orientation,
primary comparator, aggregation, missingness, and machine-executable
pass/ambiguous/fail evaluation. It must preregister whether any measurement,
comparator, or calibration identity is validly shared or must be mode-specific;
it may not drop a mode. Numerical operationalization may not revise an I03
qualitative causal expectation.

- [x] Freeze an exact raw later-response family and orientation for each mode,
  sharing a definition only where semantic comparability is justified.
- [x] Freeze each mode's primary candidate response and closest registered
  insufficient-repetition comparator with rationale.
- [x] Freeze aggregation, pairing, normalized-margin, denominator-floor, and
  missingness policies shared by calibration and live analysis.
- [x] Freeze the candidate-blind matched-null generator(s), explicitly decide
  shared versus mode-specific calibration identity, and prove candidate and
  runtime exclusion.
- [x] Freeze calibration inputs, seeds, resource limit, expected artifacts,
  reconstruction command, and stopping rule.
- [x] Convert every imported qualitative expectation and fail-closed effect
  into an exact measurement, equality/resolution rule, and machine-executable
  pass/ambiguous/fail evaluation.
- [x] Freeze raw-response retention for all cells and subconfigurations.
- [x] Freeze analysis code/policy identity and change-control boundary.
- [x] Reject every I03A/I03B/I03C conformance-fixture coefficient, amount,
  type, time, threshold, packet amount, branch ID, response observation,
  implementation comparator, and evidence digest as calibration or scientific
  input; import only each pre-runtime frozen structural family and causal
  boundary.
- [x] Validate the preregistration without running the candidate or matched
  null.
- [x] Prove that no retained mode was removed or demoted by convenience,
  expected margin, or anticipated implementation cost.

### 9.2 Frozen substantive choices and validation

The [choice-resolution input](../contracts/p2-i2/i04-choice-resolution-input.json)
binds the accepted I03F baseline, ten controlling authorities, complete
fixture quarantine, candidate/null absence, admissible response/comparator
options, and decision criteria before the final choices.

The frozen [calibration preregistration](../contracts/p2-i2/i04-calibration-preregistration.json)
and [analysis policy](../configs/p2_i2_analysis_policy.json) select:

```text
response = native B-target coherence gain across one native response window
orientation = identity; higher is aligned
candidate = two-source combined constitution in both source-role orders
comparator = quantity-and-timing-matched repeated contribution by one source
primary panel = 3 seeds x 2 separately retained orders per mode
```

The response/analysis/null identity is validly shared because causal response
meaning, unit/orientation, window, comparator role, aggregation, missingness,
and calibration population are equal. Upstream carrier causes and controls
remain mode-specific. State retains equal-P order invariance, history retains
active-order divergence with P exclusion, and hybrid retains the complete
qualitative P-by-H_P four-cell factorial without imposing synergy.

Scientific no-response is zero. Operational failure leaves the complete
mode/seed two-order primary panel not evaluable; no imputation or denominator
removal is allowed. Every seed/order/cell/subconfiguration response remains
raw. Nine common and 3/3/5 mode-specific rules are frozen as numerical or
causal-chain `pass`/`ambiguous`/`fail` evaluations.

The [candidate-blind calibration policy](../configs/p2_i2_calibration_policy.json)
freezes five calibration seeds by two equal exact-rational order pairs and the
base metric estimator. I04 froze but did not invoke the future I05 entry point;
the entry point refuses to run without a future owner-authorized I05 freeze
binding all I04 identities and exactly one null invocation. `delta` remains
pending.

The retained [validation](../contracts/p2-i2/i04-calibration-preregistration-validation.json)
passed 16/16 static checks and 10/10 pure analysis tests. It confirmed all
seven semantic-equivalence fields, all seven I03 quarantine sources, no
fixture-value/branch/digest reuse, no PyGRC import/model, no matched-null or
candidate invocation, and an exact clean graph checkout. The compact
[I04 report](../reports/P2-I2-I04-calibration-preregistration.md) records the
review surface without reopening accepted I03 mode reviews.

Historical disposition: original `P2-I2-I04-REVIEW-READY` construction was not
owner-accepted and is superseded for progression under DEC-022/DEC-023. Its
artifacts remain byte-exact history; I05 and all candidate execution remained
unauthorized.

### 9.3 `P2-I2-I04R1` — Critical-review correction

**Status:** corrected candidate-free package review-ready; owner acceptance
pending

```text
iteration_id = P2-I2-I04R1
purpose = correct the I04 contract conflict that promoted an equivalence-
          permitted quantity-matched one-source scope diagnostic into a
          required-divergence primary comparator; harden source symmetry,
          order-conditioned interpretation, analytic-null scope, fixed
          response window, B-purity, per-mode isolation, evidence-derived
          causal-chain controls, and choice-rationale quarantine
entry_authority = owner-supplied critical I04 review withholding
                  P2-I2-CAL-PRE-GATE passage
frozen_inputs_or_input_freeze_action = retain original I04 package and review
          verbatim as historical inputs; revise only through a new I04R1
          choice/correction freeze before replacing preregistration identities
mutation_and_repository_boundary = RCAE I04R1 contracts, policies, pure
          analysis/future-null code, validators/tests/results, report,
          checklist, hypotheses, and decisions; admitted graph source may be
          read for public operation semantics but remains unmodified
required_outputs = corrected primary comparator and symmetric quantity-matched
          diagnostic; per-order/mode disposition rules; analysis-only delta
          meaning and I06 numeric admissibility; exact outcome-independent
          native operation window; B-purity guards; per-mode evidence boundary;
          evidence-derived causal-chain evaluation; quarantine provenance;
          static validation and revised report
execution_budget = zero PyGRC model instantiations, zero matched-null
          invocations, and zero candidate/control invocations; static source,
          policy, code, and pure unit validation only
evidence_effect = correction of candidate-free measurement/calibration
          authority only; no resolution result, control result, R01-R05,
          L02 support/falsification, or terminal classification
exit_gate = revised P2-I2-I04-REVIEW-READY for explicit owner review or a
            retained blocker; never automatic CAL-PRE passage or I05 authority
```

- [x] Freeze the owner review and original I04 identities before correction.
- [x] Restore quantity-matched repeated-S1 and repeated-S2 conditions to a
  symmetric scope diagnostic whose valid equivalence cannot fail R03.
- [x] Select a primary comparator that changes the mode-relevant common carrier
  without outcome-based choice and resolve source-role symmetry.
- [x] Separate failure of the full top signature from valid order-conditioned
  or mixed history/hybrid relations.
- [x] State that I05 calibrates analysis arithmetic only, keep runtime/
  continuation tolerances separate, and freeze I06 numeric-domain admission.
- [x] Freeze an exact outcome-independent native operation window for scheduled,
  unscheduled, delayed, blocked, and operationally invalid responses.
- [x] Require B-baseline matching and prove that only the registered response
  packet may change B, or use an attributable/subtracted response instead.
- [x] Keep primary margins, controls, metric relations, support, and rung inputs
  independent per mode with no cross-mode compensation.
- [x] Derive private/controller causal-chain control status from retained masks,
  identities, calls, lineage, guards, configuration, and receipts rather than
  authored booleans.
- [x] Reconstruct every I04 choice rationale from pre-runtime causal contracts
  and accepted theory without conformance observations.
- [x] Validate the revised package without executing PyGRC, the matched null,
  or any candidate/control cell, then return for owner review.

The [correction input](../contracts/p2-i2/i04r1-critical-review-correction-input.json)
binds the owner review, all ten original I04 identities, three pre-runtime mode
contracts, and two admitted public-source identities. The corrected
[preregistration](../contracts/p2-i2/i04r1-calibration-preregistration.json)
selects the strongest symmetric leave-one common-carrier admission comparator;
repeated-S1/S2 in both physical orders is a separate equivalence-permitted
scope diagnostic.

The response is fixed-window B gain with one feedback-row emission, one
producer evaluation, and exactly two step calls. Scientific zero requires two
empty-queue steps, unchanged B, and no packet. B purity, binary-like response
semantics, per-mode isolation, evidence-derived causal status, analytic-only
I05 delta, and I06 floor/ULP/tolerance admission are machine-frozen in the
corrected analysis policy.

The focused [validation](../contracts/p2-i2/i04r1-calibration-preregistration-validation.json)
passed 19/19 checks and 15/15 pure tests. It repeated no I03 mode review and
executed zero PyGRC models, matched nulls, candidates, or controls. The compact
[correction report](../reports/P2-I2-I04R1-calibration-preregistration-correction.md)
is the owner-review surface.

Historical disposition: `P2-I2-I04-REVIEW-READY` under DEC-023. I04R1 is now
immutable history superseded for progression by owner-accepted I04R2; it has no
parallel calibration or execution authority.

### 9.4 `P2-I2-I04R2` — Conditional machine-invariant closure

**Status:** complete and explicitly owner-accepted; sole I04 progression
authority under DEC-026

```text
iteration_id = P2-I2-I04R2
purpose = verify and, where required, correct the machine implementation of
          I04R1's complete two-arm comparator evaluability, exact I05 primary-
          estimator route, I06 diversion and response-gain admissibility,
          window-before-zero validation, non-gating scope diagnostic, order-
          conditioned classification, and receipt-derived causal controls
entry_authority = owner-supplied conditional I04R1 acceptance review,
                  SHA-256 78a49384609cdc4198a2dbce359c21d03694822fb7da96d1c2ff5f3333741d5d
frozen_inputs_or_input_freeze_action = retain the complete I04/I04R1 package
          and conditional review as exact history; freeze an I04R2 verification
          input before changing any corrected policy/code identity
mutation_and_repository_boundary = RCAE I04R2 contracts, corrected policy/
          pure analysis/future-I05 code, tests, focused validator/result,
          report, checklist, hypotheses, and decisions; admitted PyGRC public
          source may be inspected but graph repository remains unmodified
required_outputs = all-or-none primary tuple rule; future I05 three-arm route;
          exact diversion noninterference duties; B-domain/identity-gain guard;
          step-event/evaluation contamination guards; explicit non-gating and
          order/causal derivations; focused validation and review surface
execution_budget = zero matched-null invocations, zero PyGRC models, and zero
          candidate/control invocations; static inspection and pure unit tests
          only
evidence_effect = conditional candidate-free machine-preregistration integrity
          only; no resolution, runtime, control, R01-R05, or L02 result
exit_gate = I04R2 acceptance-readiness confirmation for explicit owner review,
            or retained blocker; never automatic CAL-PRE or I05 execution
```

- [x] Freeze the conditional review and exact I04R1 identities before machine
  verification.
- [x] Prove candidate, leave-q1, and leave-q2 are all required before `max`,
  and that `max` is computed only within one mode/seed/physical-order tuple.
- [x] Route the future I05 arithmetic null through raw candidate, leave-q1,
  and leave-q2 records and the exact live strongest-marginal estimator path.
- [x] Freeze I06 diversion matching and inert-sink noninterference over every
  continuation-relevant carrier, mask, policy, eligibility, and B surface.
- [x] Require measured B gain to equal the registered native arrival gain
  within a separate runtime tolerance, remain inside the registered native
  coherence domain, and exclude clipping/projection/budget corrections.
- [x] Validate evaluation, producer, exact step-event, queue, and contamination
  identities before assigning scientific zero.
- [x] Confirm repeated-S1/S2 equivalence has no primary, top-signature, R03, or
  lowering effect.
- [x] Confirm non-top order panels remain independently classifiable from raw
  order/control/causal evidence and never imply hypothesis failure directly.
- [x] Confirm candidate/private/controller status remains derived from exact
  masks, arrivals, calls, lineage, guards, configurations, and receipts.
- [x] Run only focused static validation and pure tests, reconstruct the result,
  and return the package for explicit owner acceptance.

The [I04R2 input freeze](../contracts/p2-i2/i04r2-conditional-machine-verification-input.json)
binds the conditional review and all ten I04R1 identities. Focused inspection
found one real machine gap: the I04R1 future calibration entry point fed an
already paired response directly into normalized-difference arithmetic. The
corrected [future I05 entry point](../scripts/p2_i2_i04r2_calibration.py) now
builds raw candidate, q1-only, and q2-only response envelopes and invokes the
same all-or-none [primary analyzer](../scripts/p2_i2_i04r2_analysis.py) used by
the preregistered live route, then writes, reads, parses, and byte-reconstructs
the governed output before successful exit.

The [machine policy](../configs/p2_i2_i04r2_machine_policy.json) freezes
diversion noninterference, native identity-gain/domain admission,
window-before-zero receipts, repeated-source non-gating scope, independent
order classification, and receipt-derived causal status. The focused
[validation](../contracts/p2-i2/i04r2-machine-verification-validation.json)
passed 16/16 checks and 7/7 pure tests and reconstructed byte-identically. It
executed zero matched nulls, PyGRC models, candidate/control cells, or graph
mutations. Its retained test receipt excludes wall-clock timing so an
independent validator run is byte-stable. The compact
[verification report](../reports/P2-I2-I04R2-conditional-machine-verification.md)
is the owner-review surface.

Owner disposition: accepted under DEC-026. I04R2 is the sole progression
authority; original I04 and I04R1 remain immutable historical artifacts with
no parallel execution authority. `P2-I2-CAL-PRE-GATE` is passed and authorizes
only construction of a separate, exact, single-invocation I05 arithmetic-null
freeze. It does not invoke I05 or open I06, candidate execution, or a result.

Exit gate `P2-I2-CAL-PRE-GATE` authorizes only I05 matched-null calibration.

## 10. `P2-I2-I05` — Candidate-blind calibration

**Status:** the authorization candidate, failed-closed I05A audit, and accepted
I05B/I05C corrections remain historical authority. The sole governed
arithmetic-null attempt completed with one builder call and zero retries;
portability corrections through I05I are retained; I05J freezes the candidate-
blind arithmetic resolution and is under uncommitted closure amendment.
CAL-GATE remains closed pending owner review.

### 10.1 Single-invocation authorization-freeze construction

```text
activity_id = P2-I2-I05-AUTHORIZATION-FREEZE
purpose = construct and statically validate authority for exactly one I05
          analysis-arithmetic matched-null invocation
entry_authority = DEC-026 + passed CAL-PRE + accepted I04 lineage commit
accepted_I04_commit = b7b008c402d837b529962a1a5edb062927939d28
mutation_boundary = I05 authorization contract, focused zero-invocation
                    validator/result, report, and navigation/governance records
governed_invocations_during_construction = 0
PyGRC_invocations_during_construction = 0
candidate_or_control_invocations_during_construction = 0
graph_repository = read_only
evidence_effect = permission/integrity only; no calibrated delta, metric-sheet
                  result, operational-hypothesis evidence, or scientific result
exit = one validated, unconsumed authorization candidate returned for owner
       review; activation and commit each require explicit owner authorization,
       and P2-I2-CAL-GATE remains closed
```

- [x] Bind the authority to accepted I04 commit
  `b7b008c402d837b529962a1a5edb062927939d28`, DEC-026, the owner-acceptance
  record, and the exact active I04R2 machine/analysis/calibration/preregistration
  identities.
- [x] Encode a ceiling of exactly one governed invocation and set candidate
  execution to false; this becomes active only after owner acceptance and the
  separately authorized retention commit.
- [x] Validate only through the frozen I04R2 authorization validator; do not
  call the calibration builder, calibration entry point, or PyGRC.
- [x] Verify that the governed I05 output is absent and record zero
  matched-null, PyGRC, candidate, and control invocations.
- [x] Reconstruct the authorization-validation result byte-identically.
- [x] Obtain owner review and explicit acceptance/commit authorization.
- [x] Commit the accepted, unconsumed authorization before any request to
  execute it; do not pass `P2-I2-CAL-GATE` during this activity.

### 10.2 `P2-I2-I05A` — Pre-acceptance execution-safety audit

**Status:** complete and blocked; 3/8 checks passed, five execution-safety
blockers retained, with zero governed-null, PyGRC, candidate, or control
invocation and no source correction.

```text
entry = review-ready uncommitted I05 authorization candidate + owner review
scope = existing entry point, freeze, validation, reconstruction policy, and
        commit/environment/command bindings only
mutation_boundary = checklist, hypothesis projection, audit result/report,
                    and navigation records; no execution-source correction
governed_null_invocations = 0
reconstruction_generations = 0
candidate_or_control_invocations = 0
acceptance_effect = none until owner review of the audit disposition
```

- [x] Inspect atomic attempt-time consumption and concurrent exclusion: failed;
  no consumption token, exclusive claim, or lock exists before governed work.
- [x] Inspect immediate preflight binding: failed; it binds only accepted I04
  commit/identities, not a committed I05 authority, exact launch interpreter/
  command, or clean RCAE authority files.
- [x] Inspect reconstruction generation: passed; the existing main path calls
  the builder once, then reads, parses, canonicalizes, and compares retained
  output without a second envelope generation.
- [x] Inspect separate retained counts and refusal witness: failed; no
  consumption receipt, generation/readback counts, or refused-second-start fact
  is emitted.
- [x] Inspect failure/retry semantics: failed; one governed invocation and one
  infrastructure retry are configured without an attempt-token distinction.
- [x] Fail proposed DEC-027 closed and return a precise
  correction scope for owner authorization; do not implement it in I05A.

### 10.3 `P2-I2-I05B` — I05-owned one-shot safety correction

**Status:** owner-accepted for retention under DEC-029/CHG-022; 12/12 zero-null
tests and 12/12 machine checks passed with byte-identical reconstruction.

```text
allowed_scope = one I05 governed wrapper + one I05 one-shot policy + atomic
                claim/final receipt mechanics + zero-null tests/validation
I04R2_scientific_bytes = immutable
max_governed_attempts = 1
max_infrastructure_retries = 0
claim_timing = atomic and before accepted builder call
claim_lifecycle = survives every success/failure/crash; deletion forbidden
committed_authority_binding = runtime expected-HEAD argument + committed-blob
                              equality + owner-acceptance presence; no
                              self-referential hash inside the freeze
null_invocations_during_I05B = 0
commit_authorized = true
CAL_GATE = closed
exit = accepted, committed correction and byte-reconstructed zero-execution
       validation; null launch remains a distinct 10.4 authority
```

- [x] Add one I05-owned governed wrapper and one one-shot policy without
  changing accepted I04R2 estimator, analysis, comparator, calibration policy,
  preregistration, or test bytes.
- [x] Atomically create an exclusive claim receipt before any builder call;
  never delete or reuse it, and make every later/concurrent start fail closed.
- [x] Require one governed attempt and zero retries; a failure or crash after
  claim remains consumed.
- [x] Bind runtime `HEAD` supplied after the future authority commit, prove all
  required authority/code blobs are in that commit and equal working bytes,
  require clean index/worktree authority state, and bind interpreter plus
  normalized command.
- [x] Bind the existing authorization candidate, wrapper/policy identities, and
  unchanged I04R2 hashes in the claim receipt.
- [x] Make the future governed path call the accepted I04R2 builder exactly
  once and reconstruct only by retained-output read/parse/canonical comparison.
- [x] Retain final counts/status for one attempt, zero reconstruction
  generations, one readback, consumed authority, and mechanical second-start
  refusal.
- [x] Demonstrate all eight owner-required refusal cases with zero accepted-
  builder invocations during safety validation.
- [x] Reconstruct the validation byte-identically; retain zero null/PyGRC/
  candidate/control execution and return uncommitted for owner review.

#### 10.3.1 I05B owner acceptance and commit packaging

```text
activity_id = P2-I2-I05B-ACCEPTANCE-COMMIT
entry_authority = explicit project-owner approval of I05B and authorization
                  to commit, dated 2026-07-14
purpose = retain immutable owner acceptance and commit the complete reviewed
          I05/I05A/I05B authority package without authorizing or invoking the
          arithmetic null
authority_split = I05B owner acceptance + commit authorization now;
                  null-launch authorization only in separately directed 10.4
mutation_boundary = I05B acceptance/launch authority split, machine acceptance
                    record, zero-null validation, governance/navigation, and
                    digest consequences only; accepted I04R2 bytes immutable
null_invocations = 0
candidate_or_control_invocations = 0
CAL_GATE = closed
exit = accepted committed I05B authority package; 10.4 remains blocked on a
       separate explicit null-launch authorization
```

- [x] Record I05B owner acceptance and commit authorization under a new
  decision/change identity without rewriting DEC-027 or DEC-028.
- [x] Split immutable package acceptance (`null_invocation_authorized=false`)
  from the future 10.4 launch authority; require both exact records before any
  attempt claim can be created.
- [x] Retain the permanent claim on a repository-local non-temporary path and
  preserve `O_CREAT|O_EXCL` refusal for empty, partial, symlink, concurrent,
  crashed, or earlier claim-path occupation.
- [x] Recompute affected wrapper/policy/acceptance/validation identities and
  rerun focused plus combined zero-execution tests.
- [x] Verify accepted I04R2 bytes, graph/PyGRC cleanliness, absent claim/final/
  governed output, zero builder/null/candidate/control operations, and closed
  CAL-GATE immediately before retention.
- [x] Commit the complete accepted package; do not create the separate launch
  record or execute the null in this activity.

### 10.4 Authorized arithmetic-null execution and metric-sheet freeze

**Status:** the single governed attempt completed at historical commit
`c3eabf3` with one builder call, zero retries, one readback, zero reconstruction
generations, and a refused second start. All required portability corrections
are retained through `b5d0acb`; I05J generated and reconstructed the frozen
metric artifacts and now remains under uncommitted closure amendment.

```text
activity_id = P2-I2-I05-ARITHMETIC-NULL-EXECUTION
entry_authority = owner direction "after commit" to proceed with 10.4;
                  accepted I05B authority commit
                  c1f821dfd543d10d8555ddf2b52dbd56dfa76c13
purpose = consume the single governed arithmetic-null permission, retain and
          reconstruct its exact output, and freeze only the preregistered
          analysis-arithmetic resolution fields
launch_authority = exact P2-I2-I05-NULL-LAUNCH-AUTHORIZATION under DEC-030/
                   CHG-023, committed before the attempt and bound by the
                   accepted I05B wrapper/policy
max_governed_attempts = 1
max_infrastructure_retries = 0
accepted_builder_invocations = 1
null_reconstruction_generation_count = 0
output_readback_reconstruction_count = 1
candidate_or_control_invocations = 0
PyGRC_model_instantiations = 0
mutation_boundary = exact launch record/commit; governed attempt/final/output;
                    deterministic readback validation; designated frozen
                    metric-sheet fields; checklist/hypothesis/decision/report
evidence_effect = arithmetic/serialization resolution only; no runtime
                  tolerance, candidate/control evidence, R01-R05 assignment,
                  L02 support/falsification, or mode selection/ranking
exit = P2-I2-I05-EXECUTION-REVIEW-READY with CAL-GATE still closed pending
       owner review of exact receipts, reconstruction, and metric-sheet freeze
```

- [x] Record DEC-030/CHG-023 and create the exact separate launch record bound
  to accepted commit `c1f821d`, owner acceptance, authorization, wrapper,
  policy, and unchanged I04R2 hashes.
- [x] Validate the launch record without calling the accepted builder, null,
  PyGRC, candidate, or control path; require absent claim/final/output.
- [x] Commit the exact launch authority and revalidate exact HEAD, clean
  index/worktree, committed/local byte equality, interpreter, command, local
  ext4 claim storage, and accepted I04R2 identities immediately before start.
- [x] Invoke the accepted one-shot wrapper exactly once; treat any post-claim
  failure as consumed and perform no infrastructure retry.
- [x] Retain the permanent claim, final receipt, and governed output with the
  required attempt/builder/generation/readback/consumption/refusal counts.
- [x] Reconstruct only from retained output and require byte identity; do not
  invoke the builder or regenerate response envelopes during validation.

#### 10.4A `P2-I2-I05C` — Pre-claim venv-interpreter path correction proposal

**Status:** correction was owner-approved and committed at `9d81f15` under the
explicit direction “always use venv”; 13/13 tests and 12/12 zero-null checks
passed before the later single governed attempt.

```text
trigger = accepted wrapper validates expected .venv/bin/python through the
          generic repository-data-path resolver
observed_resolution = .venv/bin/python -> digest-bound host Python target
failure = OneShotError: path escapes repository root: .venv/bin/python
claim_created = false
accepted_builder_invocations = 0
governed_null_invocations = 0
output_or_final_receipt_created = false
authority_consumed = false
proposed_scope = distinguish the frozen repo-relative command path from its
                 resolved executable target; retain exact target digest,
                 implementation/version, command, and all other preflight
                 guards; update consequential wrapper/policy/acceptance/launch
                 identities and add a direct real-venv preflight test
scientific_change = none
```

- [x] Stop on the preflight failure without creating the permanent claim or
  calling the builder.
- [x] Identify the direct cause as reuse of the repository-data `_path()` guard
  for an intentionally external-resolving venv interpreter symlink.
- [x] Obtain explicit owner authorization before changing the accepted I05B
  wrapper, policy hash, acceptance record, launch record, tests, or committed
  authority.
- [x] Freeze the exact correction under DEC-031/CHG-024, prove
  the real `.venv` interpreter passes while wrong command/path/digest fail,
  rerun zero-null validation, and return for review. The sole governed attempt
  remains available because no claim exists; infrastructure retries remain
  zero.
- [x] Obtain owner review and explicit commit authorization, commit the complete
  corrected authority together, and require a clean exact-HEAD preflight before
  the one-shot attempt.

- [x] Execute only the frozen shared pure analysis-arithmetic matched-null
  structure.
- [x] Retain reconstructable generator provenance and all per-seed margins.
- [x] Verify candidate/runtime exclusion and absence of post-hoc inputs.
- [x] After portability corrections are accepted, freeze the preregistered shared
  `analysis_arithmetic_delta`
  disposition under the metric-sheet estimator without selecting a mode or
  inferring any runtime/measurement tolerance.
- [x] Retain a lane-local metric-calibration record and generated frozen
  metric-sheet artifact linked to the unchanged base L02 metric sheet;
  populate only the frozen artifact's designated resolution-status,
  `analysis_arithmetic_delta`, rationale, and calibration-reference fields.
- [x] Retain schema-valid raw calibration/provenance and exact portable
  projection lineage records.
- [x] Reconstruct the calibration independently and verify semantic digests.
- [x] Preserve narrow/robust language as relation to frozen resolution, not a
  terminal verdict.

#### 10.4B `P2-I2-I05D` — P2-I2-wide persisted-path portability audit

**Status:** corrected full-scope audit accepted under DEC-032/DEC-033;
312 value-redacted violations are retained across 70 of 135 scanned files, and
the owner authorized only the first I05 correction group.

```text
activity_id = P2-I2-I05D-PERSISTED-PATH-PORTABILITY-AUDIT
trigger = committed I05 execution closeout exposed filesystem-absolute paths;
          project owner states that absolute paths are never allowed
scope = current-tree P2-I2 contracts, configs, outputs, reports,
        implementation/governance, tests, and scripts under the AE01
        experiment; historical Git objects are immutable provenance only
invalid_path = any persisted filesystem-absolute POSIX path, drive-prefixed
               path, home-expanded path, or machine-local absolute path token
               embedded in a persisted command/value/literal
allowed_path = normalized repository-relative POSIX identity, stable logical
               external-repository ID, content digest, or non-path URI
mutation_boundary = checklist/hypothesis/decision audit authority; exact audit
                    policy, scanner, input freeze, inventory, and validation
                    only; no affected artifact correction in I05D
runtime_boundary = static current-tree inspection only; always use repository
                   .venv; no null builder, PyGRC model, candidate/control,
                   conformance, calibration, or response-envelope operation
historical_boundary = do not rewrite Git history and do not copy forbidden
                      path strings into new audit/governance artifacts; retain
                      historical lineage by commit and SHA-256 only
exit = P2-I2-I05D-PORTABILITY-AUDIT-REVIEW-READY with CAL-GATE closed
```

During I05D construction, the first discovery pass showed that two recursive
selectors selected directories rather than nested files. The selectors and
coverage guards were corrected inside I05D before the retained inventory was
created; this changed no classification, redaction, grouping, or gate rule and
does not constitute a separate iteration.

- [x] Record the owner-authorized audit under a new decision/change identity
  without weakening the project-wide no-absolute-path rule.
- [x] Freeze a deterministic scanner scope and classification policy before
  scanning affected files.
- [x] Correct the in-iteration recursive selector form, bind the final policy/
  scanner freeze, and require explicit nested contract/output coverage before
  retaining the audit.
- [x] Scan every in-scope current-tree P2-I2 persisted artifact and relevant
  source literal; reject filesystem-absolute paths regardless of whether they
  occur in JSON values, commands, receipts, reports, tests, or code.
- [x] Distinguish filesystem paths from non-path URIs and mathematical slash
  notation without permitting machine-location exceptions.
- [x] Retain a portable inventory containing only repository-relative affected
  file identities, field/line locations, violation classes, counts, and file
  digests; never reproduce the forbidden path values.
- [x] Group the inventory into dependency-aware correction batches with I05
  active execution/closeout first and earlier accepted lineages afterward.
- [x] Prove the audit itself imports/calls no null builder, one-shot wrapper,
  PyGRC, candidate/control, conformance, or scientific path.
- [x] Return the audit uncommitted for owner review; do not correct affected
  artifacts, reopen the one-shot attempt, freeze delta, or pass CAL-GATE.

#### 10.4C `P2-I2-I05E` — Bounded portable-path correction groups

**Status:** first I05 correction group owner-accepted and commit-authorized
after 10/10 machine checks, zero remaining violations across the exact eleven-
file scope, and 13/13 focused helper tests. The next group remains inactive
until this package is committed.

```text
activity_id = P2-I2-I05E-BOUNDED-PORTABLE-PATH-CORRECTION
entry = owner-accepted I05D inventory and exact correction-group freeze
group_order = I05 active execution/closeout first; dependency-ordered upstream
              P2-I2 groups afterward; one reviewed group at a time
path_rule = current-tree persisted filesystem identities are normalized
            repository-relative POSIX strings or stable logical external IDs;
            machine identity is retained by digest/version/capability facts,
            never by an absolute location
execution_evidence = original governed-attempt/output/final bytes remain
                     immutable in Git history and are referenced only by commit
                     and digest; active portable projections must declare their
                     derivation and cannot impersonate original raw receipts
null_invocations = 0
infrastructure_retries = 0
candidate_or_control_invocations = 0
PyGRC_model_instantiations = 0
scientific_change = none; accepted I04R2 estimator, three-arm values, margins,
                    delta arithmetic, and candidate/runtime exclusions immutable
gate_effect = CAL-GATE remains closed until all required corrections and I05
              post-run metric artifacts pass review
```

The first correction group binds these eleven affected files plus only the
consequential I05 authority/projection identities required to keep their
historical and current meanings explicit:

- `contracts/p2-i2/i05c-preclaim-interpreter-path-failure.json`
- `contracts/p2-i2/i05c-zero-null-interpreter-validation.json`
- `implementation/tests/test_p2_i2_i05b_one_shot.py`
- `outputs/p2-i2/i05/complete-three-arm-analysis-arithmetic-calibration.json`
- `outputs/p2-i2/i05/i05b-attempt-claim.json`
- `reports/P2-I2-I05C-preclaim-venv-correction.md`
- `scripts/p2_i2_i05_authorization_validate.py`
- `scripts/p2_i2_i05a_safety_audit.py`
- `scripts/p2_i2_i05b_one_shot.py`
- `scripts/p2_i2_i05b_validate.py`
- `scripts/p2_i2_i05c_validate.py`

- [x] Accept and bind the exact I05D audit before editing an affected artifact.
- [x] Freeze the first I05 correction group's exact files, fields, upstream
  hashes, derived-historical lineage, allowed transformations, and validators.
- [x] Replace absolute repository locations with normalized repository-relative
  identities and external machine locations with stable logical IDs plus exact
  digests/version facts; never persist resolved absolute targets or prefixes.
- [x] Preserve the permanent consumed-attempt guard and one-attempt/zero-retry
  fact without rerunning, regenerating, or fabricating the governed null.
- [x] Preserve original raw execution identities by historical commit/digest,
  create explicitly labelled portable projections, and update only downstream
  identities authorized by the correction freeze.
- [x] Rerun the portability scanner and bounded semantic/integrity validation;
  require zero absolute-path violations in the completed correction group.
- [x] Return the first correction group uncommitted for owner review and explicit
  commit authorization before beginning the next group.
- [x] Record owner acceptance and commit authorization; begin no later group
  until the accepted package is retained.

#### 10.4D `P2-I2-I05F` — I04/I05 authority-dependency portability correction

**Status:** owner-accepted and commit-authorized under DEC-036 after bounded
in-place process-deviation closeout under DEC-035. The exact group remains
technically 10/10 with zero findings; the original freeze and complete
13-start ledger are retained, and no technical-validator rerun occurred.

```text
activity_id = P2-I2-I05F-I04-I05-AUTHORITY-DEPENDENCY-PORTABILITY-CORRECTION
entry = owner-accepted I05D/I05E commit 6dd6898 plus DEC-034/CHG-027
baseline_group = i04_i05_authority_dependencies
baseline_findings = 30 across 13 files
path_rule = repository artifacts use normalized repository-relative POSIX
            identities; external repositories use stable logical IDs plus
            admitted revision/digest facts; no persisted machine location
historical_boundary = accepted I04/I04R1/I04R2 bytes remain Git evidence by
                      commit and SHA-256; current changed artifacts declare
                      portable projection lineage and cannot impersonate raw
                      preregistrations or validations
scientific_boundary = accepted I04R2 estimator, comparator, window, response,
                      calibration policy, and CAL-PRE meaning are immutable
runtime_boundary = .venv static validation only; zero calibration builder,
                   null, one-shot wrapper, PyGRC model, candidate/control,
                   conformance, or scientific invocation
gate_effect = CAL-GATE remains closed; no I06 or later correction group opens
exit = P2-I2-I05F-I04-I05-GROUP-REVIEW-READY, uncommitted
```

The exact affected files are:

- `configs/p2_i2_i04r2_machine_policy.json`
- `contracts/p2-i2/i04-calibration-preregistration.json`
- `contracts/p2-i2/i04r1-calibration-preregistration-validation.json`
- `contracts/p2-i2/i04r1-calibration-preregistration.json`
- `contracts/p2-i2/i04r1-critical-review-correction-input.json`
- `contracts/p2-i2/i04r2-conditional-machine-verification-input.json`
- `contracts/p2-i2/i04r2-machine-verification-preregistration.json`
- `contracts/p2-i2/i04r2-machine-verification-validation.json`
- `scripts/p2_i2_i04_validate.py`
- `scripts/p2_i2_i04r1_calibration.py`
- `scripts/p2_i2_i04r1_validate.py`
- `scripts/p2_i2_i04r2_calibration.py`
- `scripts/p2_i2_i04r2_validate.py`

- [x] Retain the accepted first correction group at `6dd6898` before opening
  this group.
- [x] Bind the exact I05D group identity: 13 files and 30 findings.
- [x] Freeze every source hash, allowed field transformation, historical
  authority identity, consequential downstream identity, and validator before
  editing an affected file.
- [x] Replace repository and external-source locations with repository-relative
  or stable logical identities; remove machine-selecting shebangs.
- [x] Preserve exact historical I04/I04R1/I04R2 semantics and reconstruct every
  changed JSON projection mechanically from its historical bytes.
- [x] Preserve accepted I04R2 and I05 arithmetic identities by explicit
  historical-to-current lineage; do not silently update raw receipt hashes.
- [x] Require zero path findings across the exact group, parseable corrected
  source, and bounded semantic/integrity validation under `.venv`.
- [x] Return the group uncommitted for owner review; do not begin I03 or another
  correction group, freeze the metric sheet, or pass CAL-GATE.
- [x] Record the owner's `+1` authorization for an I05F-owned in-place
  process-deviation closeout under DEC-035/CHG-028; do not reinterpret or
  rewrite the original freeze.
- [x] Retain one additive closeout record binding the frozen ceiling, actual
  13-start ledger, technical 10/10 result, zero-runtime boundary, and exact
  owner-authorized disposition.
- [x] Restore I05F to uncommitted owner-review readiness without any Python,
  technical-validator, builder, null, wrapper, PyGRC, candidate/control,
  conformance, or scientific rerun.
- [x] Record the owner's instruction that completed closeout also constitutes
  full I05F acceptance and commit authorization under DEC-036/CHG-029.
- [x] Retain a separate owner-acceptance artifact so the earlier deviation
  closeout remains an accurate pre-acceptance record.
- [x] Confirm with non-Python precommit checks that both new authority records
  parse, the diff has no whitespace errors, HEAD is the accepted `6dd6898`
  parent on `p2-i2-experiment`, and the closeout/navigation artifacts contain
  no machine-local path or machine-selecting shebang.
- [x] Commit the complete I05F package only after closeout/navigation is
  complete; do not begin the next group in the same commit.

The frozen ceiling was three static-validation invocations. Actual preparation
used 13 `.venv/bin/python` process starts: eight JSON syntax checks, one
five-file compile check, three governed I05F validator starts, and one
read-only scanner diagnostic. Validator attempt 1 failed closed at `I05F-04`
because its own historical-shebang literals triggered the portability scanner.
The diagnostic localized those three self-findings. Attempt 2 failed closed at
`I05F-06` because the path-only Python-diff whitelist omitted two syntax-only
added lines. Attempt 3 passed 10/10 and alone wrote the retained technical
validation artifact. Neither failed validator attempt wrote an output. All 13
starts invoked zero builder, null, one-shot wrapper, PyGRC model,
candidate/control, conformance, or scientific operation. The original freeze
remains immutable; I05F cannot pass its exit gate without explicit owner
disposition of this process deviation. DEC-035 now supplies that disposition:
the additive closeout record accepts the deviation while preserving the
original noncompliance fact. I05F is review-ready, but full-package acceptance
and commit authorization are now supplied by DEC-036. This does not open a
later group or pass CAL-GATE.

#### 10.4E `P2-I2-I05G` — Third bounded portability correction group

**Status:** exact third group corrected and review-ready as
`i03_realization_and_conformance`: 30 files, 201 to zero findings, and 10/10
static checks. No affected file was edited before policy/freeze retention; the
package is uncommitted pending owner review.

```text
activity_id = P2-I2-I05G-THIRD-BOUNDED-PORTABILITY-CORRECTION
entry = owner direction after accepted I05F commit 99c64dd plus DEC-037/CHG-030
scope_source = accepted I05D policy order and value-redacted inventory
resolved_group = i03_realization_and_conformance
resolved_scope = 201 findings across exactly 30 files
scope_resolution = completed read-only before the immutable source/
                   transformation freeze and every affected-file edit
mutation_boundary = exact frozen 30-file correction plus additive I05G
                    lineage, validation, report, and governance only
path_rule = no persisted machine-local absolute path or machine-selecting
            interpreter identity
historical_boundary = retain source bytes by accepted commit and SHA-256;
                      current corrections must be explicit portable projections
scientific_boundary = no accepted realization, restoration, calibration,
                      estimator, comparator, response, gate, or evidence meaning
                      may change
runtime_boundary = .venv only for any later Python validation; zero builder,
                   null, wrapper, PyGRC model, candidate/control, conformance,
                   or scientific invocation
gate_effect = CAL-GATE remains closed; no fourth correction group or I06 opens
exit = exact third-group correction review-ready and uncommitted
```

- [x] Retain accepted I05F at `99c64dd` before opening I05G.
- [x] Record the owner's direction that the third bounded group is next under
  DEC-037/CHG-030.
- [x] Resolve the exact third group, file count, finding count, and affected
  paths from the accepted I05D inventory without editing an affected file.
- [x] Freeze the accepted parent commit, exact source hashes, allowed
  transformations, historical identities, invocation ceilings, outputs, and
  review stop before affected-file edits.
- [x] Correct only the frozen third group and mechanically retain
  historical-to-portable lineage.
- [x] Demonstrate zero remaining findings in the exact group without changing
  scientific/runtime semantics or invoking a governed/runtime path.
- [x] Return I05G uncommitted for owner review and explicit acceptance/commit
  authorization; do not begin a fourth group or pass CAL-GATE.

The exact affected files are:

- `contracts/p2-i2/i03ar1-environment-receipt.json`
- `contracts/p2-i2/i03ar1-state-carried-runtime-conformance-input-freeze.json`
- `contracts/p2-i2/i03ar1-state-carried-runtime-conformance.json`
- `contracts/p2-i2/i03ar1r1-runtime-reconstruction-receipt.json`
- `contracts/p2-i2/i03ar1r1-state-carried-runtime-conformance-input-freeze.json`
- `contracts/p2-i2/i03b-environment-receipt.json`
- `contracts/p2-i2/i03b-history-carried-realization-freeze-input.json`
- `contracts/p2-i2/i03b-history-carried-runtime-conformance-input-freeze.json`
- `contracts/p2-i2/i03b-history-carried-runtime-conformance.json`
- `contracts/p2-i2/i03b-runtime-reconstruction-receipt.json`
- `contracts/p2-i2/i03br1-closeout-revalidation-input.json`
- `contracts/p2-i2/i03c-environment-receipt.json`
- `contracts/p2-i2/i03c-hybrid-realization-freeze-input.json`
- `contracts/p2-i2/i03c-hybrid-runtime-conformance-input-freeze.json`
- `contracts/p2-i2/i03c-hybrid-runtime-conformance.json`
- `contracts/p2-i2/i03c-runtime-reconstruction-receipt.json`
- `contracts/p2-i2/i03cr1-closeout-revalidation-input.json`
- `contracts/p2-i2/i03f-family-closeout-index.json`
- `contracts/p2-i2/i03f-family-closeout-input.json`
- `contracts/p2-i2/i03f-family-closeout-validation.json`
- `reports/P2-I2-I03AR1-state-carried-runtime-conformance.md`
- `scripts/p2_i2_i03a_validate.py`
- `scripts/p2_i2_i03ar1_conform.py`
- `scripts/p2_i2_i03b_conform.py`
- `scripts/p2_i2_i03b_validate.py`
- `scripts/p2_i2_i03br1_validate.py`
- `scripts/p2_i2_i03c_conform.py`
- `scripts/p2_i2_i03c_validate.py`
- `scripts/p2_i2_i03cr1_validate.py`
- `scripts/p2_i2_i03f_validate.py`

The 201 accepted findings comprise machine-local historical checkout,
environment, command, temporary-output, attachment, and script identities plus
slash-leading JSON-pointer strings. The latter are semantic pointers, not
filesystem paths; I05G must project them to structured segment arrays with
identical resolution rather than relabel them as repository paths.

Scope resolution used eight read-only, non-Python inspection commands and zero
affected-file edits or runtime/scientific operations. The retained policy and
input freeze bind all 30 source hashes at parent commit `99c64dd`, the exact
path/pointer transformation classes, raw-evidence separation, at most three
dedicated I05G-validator starts, and zero other Python starts after freeze.

The retained validator result is 10/10, SHA-256
`cea397d4ca4c5fc80726fb15616a03ccd14a2054ba911309a3c6cf4a65bc8183`.
It reconstructs all 30 accepted source identities, binds all 30 projected
identities through lineage SHA-256
`ffbc846dca1e50aa4eba5339624698e7e13e117cec4d8f07ee33cb539bf4fa7f`,
closes the accepted 201 findings to zero, exactly reconstructs all 20 JSON and
10 text projections, converts 105 legacy pointer occurrences to ordered
segments, and resolves all 44 indexed targets identically.

Two `.venv/bin/python` validator entry-point starts were used after freeze.
Start one failed closed before output because the validator projector omitted
the admitted I03CR1 owner-attachment identity; correcting that validator-only
mapping changed no affected source. Start two passed and alone wrote the
retained validation. The count is within the ceiling of three. Other Python
starts, PyGRC imports/model instantiations, conformance/scientific operations,
candidate/control operations, builder/null/wrapper invocations, and retries
are all zero.

#### 10.4F `P2-I2-I05H` — Fourth bounded portability correction group

**Status:** exact fourth group corrected and review-ready as
`i01_i02_source_and_identity`: 10 files, 35 to zero findings, and 10/10 static
checks. No affected file was edited before immutable policy/freeze retention;
the package is uncommitted pending owner review.

```text
activity_id = P2-I2-I05H-FOURTH-BOUNDED-PORTABILITY-CORRECTION
entry = owner acceptance/commit of I05G at 62882ef plus DEC-038/CHG-031
scope_source = accepted I05D policy order and value-redacted inventory
resolved_group = i01_i02_source_and_identity
resolved_scope = 35 findings across exactly 10 files
scope_resolution = completed read-only; immutable source/transformation freeze
                   must be retained before affected-file edits
mutation_boundary = checklist, hypothesis, and decision scaffolding only until
                    the exact I05H input freeze is retained
path_rule = no persisted machine-local absolute path or machine-selecting
            interpreter identity
historical_boundary = retain source bytes by accepted commit and SHA-256;
                      current corrections must be explicit portable projections
scientific_boundary = no accepted source finding, identity authority, reset
                      baseline, realization, restoration, calibration, gate,
                      or evidence meaning may change
runtime_boundary = .venv only for any later Python validation; zero builder,
                   null, wrapper, PyGRC model, candidate/control, conformance,
                   or scientific invocation
gate_effect = CAL-GATE remains closed; no fifth correction group or I06 opens
exit = exact fourth-group correction review-ready and uncommitted
```

- [x] Retain owner-accepted I05G at `62882ef` before opening I05H.
- [x] Record the owner's acceptance/commit and direction to move to the fourth
  bounded group under DEC-038/CHG-031.
- [x] Resolve the exact fourth group, file count, finding count, affected
  paths, source hashes, and violation classes from the accepted I05D inventory
  without editing an affected file.
- [x] Freeze the accepted parent commit, exact source hashes, allowed
  transformations, historical identities, invocation ceilings, outputs, and
  review stop before affected-file edits.
- [x] Correct only the frozen fourth group and mechanically retain
  historical-to-portable lineage.
- [x] Demonstrate zero remaining findings in the exact group without changing
  scientific/runtime semantics or invoking a governed/runtime path.
- [x] Return I05H uncommitted for owner review and explicit acceptance/commit
  authorization; do not begin a fifth group or pass CAL-GATE.

The exact affected files are:

- `contracts/p2-i2/i01-audit-input-freeze.json`
- `contracts/p2-i2/i02-source-admission-input-freeze.json`
- `contracts/p2-i2/i02r1-identity-authority-validation.json`
- `contracts/p2-i2/i02r2-reset-baseline-validation.json`
- `reports/P2-I2-I01-command-provenance.md`
- `reports/P2-I2-I01R1-capability-audit-closeout-revalidation.md`
- `reports/P2-I2-I02R1-admission-closeout-revalidation.md`
- `scripts/p2_i2_i02r1_validate.py`
- `scripts/p2_i2_i02r2_build_manifest.py`
- `scripts/p2_i2_i02r2_validate.py`

The 35 accepted findings comprise 24 embedded machine-local absolute tokens
and 11 exact POSIX absolute values. Scope resolution and freeze preparation used eight read-only,
non-Python commands after the I05G commit and zero affected-file edits or
runtime/scientific operations. I05H must freeze the exact transformations and
source identities before correcting any of these files.

The retained validator result is 10/10, SHA-256
`c9090b66b3fcbc1b2db2b8fe9ee4889e06a5cb2f071918414689f8adf77cdbb4`.
It reconstructs all ten accepted source identities, binds all ten projected
identities through lineage SHA-256
`4afca69931e8d876a46486561dfee222a7925375163fea055b236605ed354c7f`,
closes the accepted 35 findings to zero, and exactly reconstructs the four
JSON, three report, and three Python projections. The active-source diff is
limited to three shebang removals and five system-selected `tempfile`
temporary-directory contexts.

One `.venv/bin/python` validator entry-point start was used after freeze and
passed on its first attempt. Other Python starts, PyGRC imports/model
instantiations, historical validator/manifest-builder execution,
conformance/scientific operations, candidate/control operations,
builder/null/wrapper invocations, and retries are all zero.

#### 10.4G `P2-I2-I05I` — Fifth/final portability correction group

**Status:** exact terminal group corrected and review-ready as
`p2_i2_governance_navigation_and_shared_projections`: one accepted group, six
files, and 14 literal findings, supplemented before validation by two owner-
identified validator files with three constructed roots. The second failed-
closed start adds the I05F validator's constructed historical shebang. All
nine correction sources are
review-ready at zero findings with 10/10 static checks. The package
is uncommitted pending owner review.

```text
activity_id = P2-I2-I05I-FIFTH-FINAL-PORTABILITY-CORRECTION
entry = owner acceptance/commit of I05H at 1279e17 plus DEC-039/CHG-032
resolved_group = p2_i2_governance_navigation_and_shared_projections
resolved_scope = one residual group with 14 literal findings across six files,
                 plus two owner-identified validators with three constructed
                 machine-root surfaces and one guard-identified validator
                 with a constructed shebang; nine correction sources total
combination_disposition = not applicable; no second residual group exists
authority_sources = accepted I05D ordered inventory, source commit 1279e17,
                    and matching current-tree absolute-path file set
mutation_boundary = checklist/hypothesis/decision self-governance declaration
                    only before freeze; all source projections bind 1279e17
runtime_boundary = .venv only for static validation; zero builder, null,
                   wrapper, PyGRC, candidate/control, conformance, or
                   scientific invocation
scientific_boundary = no hypothesis, decision, gate, calibration, source,
                      realization, evidence, or navigation meaning may change
gate_effect = CAL-GATE remains closed; I06 remains closed
exit = exact final correction review-ready and uncommitted
```

- [x] Retain owner-accepted I05H at `1279e17` before reconciliation.
- [x] Record the owner's request to check remaining files and consider whether
  two residual groups should be combined under DEC-039/CHG-032.
- [x] Reconstruct the remaining accepted I05D group/file/finding inventory.
- [x] Compare it with current-tree absolute-path-bearing files after I05E–I05H.
- [x] Determine whether one or two accepted residual groups remain and whether
  a merge is meaningful.
- [x] Resolve that only one six-file/14-finding residual group exists, so no
  combination is meaningful and no standalone inventory-review iteration is
  needed.
- [x] Record before validation that `p2_i2_i05g_validate.py` and
  `p2_i2_i05h_validate.py` construct three forbidden machine-specific roots
  missed by the literal-token scanner, and add them to I05I without a suffix.
- [x] Record the second failed-closed start at I05I-04 and add
  `p2_i2_i05f_validate.py` after the expanded constructor guard finds its
  historical shebang constant; retain I05I without a suffix.
- [x] Freeze the accepted parent commit, exact nine source hashes, allowed
  transformations, self-governance boundary, invocation ceilings, outputs,
  and review stop before non-governance affected-file edits.
- [x] Correct only the exact terminal group and retain historical-to-portable
  lineage for the six accepted-audit files plus all three validator sources.
- [x] Demonstrate zero remaining P2-I2 audit-scope literal or constructed path findings without
  changing semantics or invoking a governed/runtime path.
- [x] Return I05I uncommitted for owner review and explicit commit authority;
  do not pass CAL-GATE in the correction itself.

The exact affected files are:

- `hypotheses/p2-i2-operational-hypotheses.md`
- `implementation/P2-I2-decision-record.md`
- `implementation/P2-I2-shared-pool-co-conditioning-checklist.md`
- `reports/P2-I2-I00-validation.md`
- `scripts/README.md`
- `scripts/p2_i2_calibration.py`
- `scripts/p2_i2_i05f_validate.py`
- `scripts/p2_i2_i05g_validate.py`
- `scripts/p2_i2_i05h_validate.py`

All 14 accepted findings are embedded machine-local absolute tokens. The
accepted inventory and current P2-I2 audit boundary identify the same six
files. Owner inspection additionally identifies three constructed machine-
root surfaces across the two validators; the final correction therefore binds
nine sources after the expanded guard identifies one constructed historical
shebang in the I05F validator. Broader experiment-directory text search also
finds older P2-I1/shared
AE01 sources, but those are outside the accepted P2-I2 audit and correction
authority and therefore cannot be folded into I05I.

The retained static validator passes 10/10 on its third of three allowed
starts. The first start fails closed at I05I-02 before output because the
initial policy carried three stale pre-I05H governance source digests; those
identities are corrected to the exact `1279e17` bytes in the policy, freeze,
and lineage. The second fails closed at I05I-04 before output because the
expanded guard finds the I05F constructed shebang; the source is added and
corrected. The passing start reconstructs all nine sources
from `1279e17`, binds all nine portable projections, verifies the three
ordinary non-governance transformations exactly, verifies removal of
constructed absolute bindings from all three validator sources, bounds the three self-governance diffs
to DEC-039/CHG-032/I05I plus the frozen path substitutions, and scans the
complete current P2-I2 audit scope to zero findings. Three `.venv/bin/python`
validator entry-point starts are used; all other Python, PyGRC, historical
validator/manifest-builder, candidate/control, conformance/scientific,
builder/null/wrapper, and retry counts are zero.

#### 10.4H `P2-I2-I05J` — Arithmetic-resolution and metric-sheet closeout

**Status:** owner-accepted and commit-authorized under DEC-040/DEC-041 and
CHG-033/CHG-034; native generation, bounded validation, additive process/package
closeout, and current-projection synchronization are complete; CAL-GATE passed
and I06 registration construction is authorized but not begun.

```text
activity_id = P2-I2-I05J-METRIC-CLOSEOUT
entry = owner acceptance/commit of I05I at b5d0acb and direction to return to
        10.4/10.4A
scope_resolution = I05C/10.4A already complete; three deferred 10.4 metric
                   obligations remain
input = retained portable I05 three-arm analysis-arithmetic output: five seeds
        by two physical orders, plus unchanged base AE01-L02 metric sheet
projection = per seed, maximum absolute normalized margin across both required
             physical orders; global estimator preserved exactly
native_generation = two .venv entry-point starts: one missing-dependency
                    failure before output plus one unchanged successful retry
outputs = lane-local metric-calibration record and frozen metric-sheet projection
runtime_boundary = zero null rerun, PyGRC, candidate/control, conformance, or
                   scientific execution
semantic_boundary = analysis/serialization resolution only; no runtime or
                    measurement tolerance and no mode selection/ranking
gate_effect = owner accepted and commit authorized; CAL-GATE passed; I06
              registration construction authorized but not begun
closure_amendment = complete; every freeze/output/generated validation is
                    preserved; one honest process/package closeout and current-
                    status synchronization are retained without execution/rerun
```

- [x] Record I05I owner acceptance/commit and exact I05J scope under
  DEC-040/CHG-033 before metric-closeout generation.
- [x] Reconcile that I05C/10.4A is already complete and that the three
  unchecked lines following it are deferred 10.4 metric obligations.
- [x] Freeze the parent commit, base metric sheet, I04R2 estimator policy,
  portable governed output/lineage, I05I validation, native tooling/schema,
  output paths, invocation ceilings, and review stop.
- [x] Materialize the exact five-seed calibration-input projection from all ten
  retained seed/order margins without rerunning or regenerating the null.
- [x] Retain the failed-closed first native start and invoke its one
  correction-authorized unchanged `.venv` retry; retain schema-valid lane-local
  metric-calibration and frozen metric-sheet artifacts.
- [x] Reconstruct the input projection and both native outputs, require exact
  bytes/semantics, and verify that only designated resolution fields changed
  from the unchanged base sheet.
- [x] Preserve `analysis_arithmetic_delta = 1e-12` as analysis/serialization
  resolution only; preserve narrow/robust language as relation to that frozen
  resolution and infer no runtime/measurement tolerance or scientific verdict.
- [x] Close the three deferred 10.4 checkboxes and the stale I05F zero-path
  evidence checkbox from retained accepted evidence; do not rewrite history.
- [x] Return I05J uncommitted for owner review; do not pass CAL-GATE or open I06.
- [x] Preserve the original I05J/I05JA freezes, native outputs, and generated
  11/11 validation byte-for-byte during the closure amendment.
- [x] Retain one additive I05J process/package closeout that records two actual
  dependency-install process starts, both native starts, both validator starts,
  the successful outputs, the failed validator disposition, final report hash,
  and the complete non-self package inventory without presenting reconstructed
  process history as a machine-generated execution receipt.
- [x] Synchronize stale current-status projections in the lane checklist and
  hypotheses, experiment/implementation navigation, overview, and master
  plan/checklist without rewriting immutable historical decisions or reports.
- [x] Verify final hashes, JSON shape, no machine-local absolute paths, and zero
  null/native/validator/PyGRC/candidate/control/runtime/scientific reruns.
- [x] Return the amended I05J package uncommitted for owner review; do not pass
  CAL-GATE or open I06.
- [x] Record explicit owner acceptance and commit authorization for the complete
  I05J/I05JA package; pass CAL-GATE and authorize only unstarted I06
  registration construction, with no candidate or scientific operation.

#### 10.4HA `P2-I2-I05JA` — Failed-closed native dependency correction

**Status:** complete and owner-accepted with I05J under DEC-041/CHG-034; the
original I05J freeze and failed start are immutable, the exact dependency is
installed, and the one unchanged native retry succeeded.

- [x] Retain that the original one-start ceiling was consumed by a pre-output
  missing-dependency failure and that both metric outputs remained absent after
  that failed start.
- [x] Identify the missing dependency as the common tooling contract's exact
  `jsonschema==4.26.0`, not a scientific or runtime prerequisite.
- [x] Freeze the original freeze/failure identities, exact dependency install,
  unchanged native retry command, retry ceiling, and review stop.
- [x] Install only the pinned dependency into the repository `.venv` and verify
  its exact installed version.
- [x] Retry the unchanged native command exactly once and retain both outputs.
- [x] Validate two total native starts, one failed-closed pre-output start, one
  successful generation, and zero other governed/runtime/scientific activity.
- [x] Return the combined I05J/I05JA package uncommitted for owner review.

Exit gate `P2-I2-CAL-GATE` opens registration construction only.

## 11. `P2-I2-I06` — Exact implementation registration

**Status:** exact three-mode registration package owner-accepted for progression;
14/14 checks pass, all three baseline composite identities survive
save/load/reset, nine continuation mismatches refuse, and no candidate or
scientific operation occurred. I06A closes the two review blockers; the owner
passes `P2-I2-REG-GATE` and authorizes I07 freeze construction only.

```text
activity_id = P2-I2-I06-EXACT-THREE-MODE-REGISTRATION
entry = owner-accepted I05 closeout at 3be9073 and passed P2-I2-CAL-GATE
authority = accepted I03F three-mode family, I04R2 measurement/comparator,
            I05J delta and metric sheet, I02R2 restoration-provider boundary
mode_scope = state_carried + history_carried + hybrid; retain and register all
             three without selection, ranking, or scalar collapse
native_first = use public PyGRC for every adequate state, transport, response,
               and restoration transition; retain only the accepted minimal
               active-history producer for history-carried and hybrid gaps
artifact_scope = one policy/input freeze, one exact three-mode registration
                 bundle, one artifact manifest, one control-index template,
                 one validator/validation, and one compact report
allowed_preflight = read-only source/runtime/environment identity, schema and
                    public-callability checks, baseline-only composite
                    restoration binding and negative mismatch checks after the
                    exact registration freeze
candidate_operation = prohibited: no S1/S2 contribution, active-history token
                      admission, neutral encounter, response evaluation,
                      candidate/control cell, comparator, or scientific window
fixture_quarantine = reject all I03 conformance exact values, branch/topology
                     IDs, observations, outcomes, comparators, and digests;
                     import structural code and accepted causal form only
gate_effect = owner-accepted after I06A; REG-GATE passed; I07 freeze may begin
```

- [x] Record the passed CAL-GATE, explicit owner direction, one-iteration I06
  artifact scope, native-first rule, fixture quarantine, and candidate-free
  registration boundary before source inspection or value selection.
- [x] Revalidate the exact clean PyGRC checkout, active repository `.venv`,
  imported package identity, public callability, accepted I02R2 restoration
  providers, and structural adapter source before freezing registration. Retain
  one initial diagnostic import failure caused by omitting the declared
  `PYTHONPATH`, followed by the exact accepted binding: revision `83e3a3...`,
  clean worktree, 31/31 source hashes, 31/31 public callables, active `.venv`,
  and exact locked direct dependencies.
- [x] Audit the accepted structural active-history adapter against I03 fixture
  quarantine and I04 runtime-tolerance separation. Finding: its two hardcoded
  `abs_tol=1e-12` materialization comparisons are the explicitly quarantined
  I03 implementation comparator, so the source cannot be registered unchanged.
- [x] Add one I06-owned minimal adapter revision that makes materialization
  tolerance an explicit configuration/restoration-identity field derived from
  the I06 numeric domain; preserve the accepted token/readout/native-handoff
  boundary and prohibit response-state reads or response scheduling.
- [x] Bind the exact accepted I03F/I04R2/I05J inputs and prove that historical
  portability projections resolve to their retained current bytes.

- [x] Bind exact source, runtime, realization, analysis, and restoration
  identities separately for all three retained modes.
- [x] Materialize each mode's exact source/carrier/write/read and
  common-state/active-history/audit-lineage mappings.
- [x] Materialize all seven logical cells and five lane controls for every
  mode, including signed and mode-specific subconfigurations.
- [x] Freeze the primary comparator and all mandatory secondary controls.
- [x] Freeze contribution amounts, order/timing, mixing, support, reserve,
  leakage, maintenance, saturation, and applicability dispositions.
- [x] For history-carried registration, preserve one unique registered source-
  to-P admission path or add an explicit route/channel admission key; bind
  run/event capacity and retain or formally revise the I03BR1 lifecycle class.
- [x] Freeze branch-point and complete composite restoration identity.
- [x] Register one paired native-v2/adapter continuation interface that
  validates manifest component hashes and the complete composite before use;
  prohibit one-sided load/reset, implicit rebase, and fabricated legacy
  adapter baseline.
- [x] Reject every I03 conformance fixture value, branch identifier,
  comparator, response observation, and evidence/reconstruction digest as a
  registered candidate value or evidence source.
- [x] Freeze seeds, attempts, one infrastructure-retry scope, resources,
  isolation, and contamination checks.
- [x] Freeze expected artifacts, manifests, reconstruction commands, report
  assembly, and claim boundary.
- [x] Retain an explicit registration evidence bundle and compact summary.
- [x] Prepare the lane-local control-resolution-index template as a projection,
  not evidence.
- [x] Validate registration without executing a candidate operation: the sole
  output-producing baseline-only start passed 14/14, constructed three fresh
  and three loaded native models, preserved all three composite identities
  through reset, refused all nine negative cases, and recorded zero candidate,
  history-admission, neutral-contact, response, cell, comparator, or scientific
  operations.
- [x] Run the terminal portability scan and correct its one source-only finding
  inside I06: replace literal absolute/legacy-root rejection patterns in the
  validator with generic POSIX/Windows absolute-token and `*_ROOT` placeholder
  detection. Retain old/new source hashes in manifest v1.0.1; pass two no-model
  static correction starts, first over four documents/five manifest hashes/
  three negative cases and then with the accepted I05D scanner over all eight
  I06 package files at zero findings; do not rerun the consumed baseline
  validation or change its projected result.
- [x] Return the complete I06 package uncommitted for explicit owner review;
  do not pass REG-GATE or begin I07.

Exit gate `P2-I2-REG-GATE` does not itself authorize execution.

### 11.1 `P2-I2-I06A` — Registration review closeout

**Status:** complete and owner-accepted. After the retained six-versus-seven
assertion failure, the owner authorized one separately bound replacement at
checkpoint `7761d3e`. It passes 14/14 with exact failed-start accounting, zero
infrastructure retries, zero PyGRC imports/models, zero baseline reruns, and zero
candidate/control/scientific operations. The owner authorizes amendment of the
closeout into the checkpoint, passes REG-GATE, and opens I07 freeze construction.

```text
activity_id = P2-I2-I06A-REGISTRATION-REVIEW-CLOSEOUT
entry = uncommitted I06 package + owner-supplied conditional review
blocker_1 = AdapterV2 conformance authority relative to I03-tested AdapterV1
blocker_2 = honest historical-validator/final-validator manifest provenance
confirmation_scope = registered tolerance domain + diversion/admission purity
                     + positive mode isolation + exact retry semantics
allowed = source/AST equivalence proof, pure adapter tests, static bundle and
          manifest proof, additive provenance artifacts, compact report update
forbidden = baseline validation rerun, PyGRC model construction, candidate or
            control operation, contribution/history admission, response,
            comparator/scientific window, result or mode ranking
gate_effect = accepted; amend checkpoint; REG-GATE passed; I07 freeze authorized
```

- [x] Record the owner-supplied review and both potential blockers before I06A
  inspection or correction.
- [x] Freeze exact I06/I03 source, manifest, validation, and review identities.
- [x] Prove AdapterV2 changes only registered materialization tolerance and
  identity/schema/load plumbing; prove inherited token admission, ordering,
  fold, cursor/idempotency, intervention, and response prohibition are exact.
- [x] Pure-test configured comparison, identity inclusion, packet construction,
  native handoff, and save/load/reset behavior without a PyGRC model or
  candidate fixture.
- [x] Preserve the exact historical five-file manifest and reconstruct the exact
  validator bytes that produced the retained 14/14 artifact.
- [x] Prove the current validator differs only in portability guard imports/body
  and that model construction, all 14 checks, restoration/refusals, and output
  projection are unchanged.
- [x] Bind historical execution validator, current validator, producing
  manifest, final manifest, and transition proof without implying that the
  corrected validator produced the retained validation.
- [x] Confirm the tolerance domain and response-gain inequalities without
  reusing runtime tolerance as scientific resolution.
- [x] Confirm complete diversion matching, unique H_P admission exclusions,
  positive per-mode isolation, and exact one-retry semantics.
- [x] Run only frozen no-model static/pure validation under `.venv`, retain
  exact process accounting, and return uncommitted for owner review: the
  replacement passes 14/14 and final manifest v1.1.1 binds all 15 non-self
  authority files with distinct historical-producer/current-source roles.
- [x] Preserve the first I06A validation start as failed closed before output:
  one prevalidation syntax/JSON start; one output-intended no-model start; eight
  fake packet-interface instances; zero PyGRC imports/models, baseline reruns,
  candidate/control/history/response/scientific operations; zero validation
  outputs and zero retries.
- [x] Correct only the validator's retry-input cardinality assertion from seven
  to the frozen policy's actual six classes and update future process
  accounting. Do not execute the corrected candidate without new owner
  direction.
- [x] Record the owner's direction to commit the current failed-closed
  checkpoint. This authorizes retention only; it does not authorize a
  replacement validation start, pass REG-GATE, or open I07.
- [x] After checkpoint commit `7761d3e`, record the owner's explicit direction
  to continue I06A and bind one corrected replacement no-model start. Preserve
  the failed start separately, allow zero infrastructure retries, and consume
  replacement authority on any failure.
- [x] Record the owner's acceptance of the complete I06/I06A package and
  authorization to amend it into the checkpoint. Pass REG-GATE and authorize
  only I07 candidate-cycle freeze construction; do not execute a candidate.

### 11.2 `P2-I2-I06B` — Execution-readiness registration correction

**Status:** complete and explicitly owner-accepted under DEC-044/CHG-038. This
additive three-primitives-only correction passes 15/15 candidate-free checks
with zero blockers. It does not rewrite accepted I06/I06A artifacts or execute
a model. Acceptance restores REG-GATE and resumes I07 freeze construction only;
commit and candidate execution remain unauthorized.

```text
activity_id = P2-I2-I06B-EXECUTION-READINESS-REGISTRATION-CORRECTION
entry = I07 authority audit + owner +1 on DEC-043 recommendation
purpose = freeze the three exact primitives I07 cannot lawfully invent
frozen_inputs = accepted I06/I06A identities; blocked I07 audit; DEC-043;
                exact source-current public call signatures read-only
mutation_boundary = additive I06B freeze/overlay/manifest/validator/validation/
                    report plus governance projections only
allowed = hash/schema/arithmetic/signature/matrix/refusal validation under
          repository .venv; no-model source inspection
forbidden = modifying accepted I06/I06A bytes; PyGRC import/model; packet
            scheduling or stepping; contribution/history admission; response,
            cell/control/comparator/scientific operation; tuning or mode ranking
required_outputs = exact input freeze; additive execution-readiness overlay;
                   progression manifest; candidate-free validation; report
evidence_effect = implementation-registration readiness only; no OP/R01-R05
exit = uncommitted package returned for explicit owner review; REG-GATE remains
       reopened and I07/EXEC-FREEZE/I08 remain closed
```

- [x] Record DEC-043/CHG-037 and the owner's explicit `+1` construction
  authorization before I06B artifact construction.
- [x] Freeze the correction as exactly three missing primitives and prohibit a
  fourth primitive or any accepted-I06/I06A byte change.
- [x] Bind exact accepted I06/I06A, blocked-I07, source/runtime, `.venv`, and
  governance input identities in an additive input freeze.
- [x] Freeze one order-invariant reserved intervention slot after history
  materialization and before neutral contact; preserve contribution timing and
  the neutral-arrival-to-response-arrival lag; require explicit no-op use when
  a branch does not intervene.
- [x] Freeze the full reference-P native debit as exact registered `q1 + q2`,
  distinct from the accepted diagnostic debit, with exact applicable branches
  and native P-to-K_P route.
- [x] Freeze exact direct-address and controller-assembled public-call
  primitives while retaining both as diagnostic causal exclusions outside the
  candidate chain.
- [x] Bind overlay precedence narrowly: it supersedes only I06 execution timing
  and the three absent primitives for future I07/I08; accepted historical
  registration evidence and all other I06 semantics remain unchanged.
- [x] Candidate-free validate hashes, exact arithmetic, matched schedule,
  branch applicability, public-call signatures, bounds, overlay completeness,
  absence of absolute paths, immutable accepted inputs, and closed gates under
  `.venv` without importing PyGRC or constructing a model: 15/15 checks pass,
  all nine accepted and two blocked-I07 inputs reconstruct, and zero blockers
  remain.
- [x] Retain exact process counts proving zero PyGRC imports/models, packet
  operations, candidate/control/response/comparator/scientific operations, and
  return the complete package uncommitted for explicit owner review in the
  [I06B report](../reports/P2-I2-I06B-execution-readiness-correction.md).
- [x] Record the owner's explicit I06B acceptance, restore REG-GATE, and
  authorize only resumption of the already-declared candidate-free I07 freeze.
- [x] Retain a [machine acceptance record](../contracts/p2-i2/i06b-owner-acceptance-and-reg-gate.json)
  binding the exact accepted I06B
  package hashes and the still-closed commit/EXEC-FREEZE/I08 boundaries.

I06B did not pass REG-GATE by its own output. Explicit owner acceptance restores
the gate; commit authority remains separate and absent.

## 12. `P2-I2-I07` — Candidate-cycle execution freeze

**Status:** review-ready, candidate-free, inactive, and uncommitted. The exact
234-entry matrix, binding receipt, and inactive freeze reconstruct; focused
tests pass 7/7 and final validation passes 25/25. The missing-`pytest` start is
retained, and the owner-directed in-place I07 continuation is fully accounted
under DEC-045/CHG-040. EXEC-FREEZE and candidate execution remain unauthorized
pending explicit owner acceptance.

```text
activity_id = P2-I2-I07-CANDIDATE-CYCLE-EXECUTION-FREEZE
entry = accepted I06/I06A at 49c74e1 + passed P2-I2-REG-GATE
cycle_scope = one exact P2-I2 mode-indexed candidate/control cycle
allowed = read-only accepted-authority audit; exact cycle/policy/binding freeze;
          candidate-free static/schema/hash/matrix/refusal validation; compact
          review report and authority projections
forbidden = PyGRC model construction for a candidate/control cell; contribution
            or history admission; response evaluation; comparator/scientific
            window; result, ranking, tuning, or candidate-derived correction
retry_boundary = one preregistered infrastructure retry per matrix entry only;
                 scientific/control outcomes are never retryable
authority_boundary = I07 may prepare EXEC-FREEZE for owner review; it may not
                     pass the gate or authorize I08 by its own output
exit = complete exact-cycle package returned uncommitted for owner review
```

- [x] Assign unique candidate cycle ID `P2-I2-C01`.
- [x] Bind the exact tracked source/runtime, registration, calibration, policy,
  code, and manifest identities.
- [x] Freeze the finite mode × cell × subconfiguration × seed × attempt ×
  resource matrix, retaining valid mode-specific missing-prerequisite entries.
- [x] Freeze infrastructure-retry eligibility separately from scientific
  change.
- [x] Freeze stop conditions, expected receipts, graph read-only guard, and
  candidate-effect boundary.
- [x] Verify that no candidate operation preceded this freeze.
- [x] Retain a cycle-scoped authorization review. Evidence:
  [I07 inactive EXEC-FREEZE review](../reports/P2-I2-I07-EXEC-FREEZE-review.md).
- [x] Record the owner direction and I07 candidate-free scope before executable-
  policy inspection. The initial orientation read only located existing I07 and
  P2-I1 EXEC-FREEZE surfaces; it constructed no model and selected no value.
- [x] Record DEC-044/CHG-038 owner acceptance of I06B, restore REG-GATE, and
  resume this existing I07 iteration without granting commit or execution.
- [x] Preserve both blocked I07 draft files byte-exact because accepted I06B
  binds their audit hashes; construct versioned successor freeze/policy files
  rather than rewriting that retained history.
- [x] Freeze 16 accepted authority inputs plus the registered three-mode/cell/
  seed/resource/retry projection.
- [x] Audit whether every registered branch can be instantiated without new
  semantics. Stop before execution-source construction on three blockers:
  (1) no registered event/index slot for a hybrid native P debit after M_H
  materialization and before neutral contact; (2) the registered `0.4375` debit
  does not implement full reference P, which requires derived `q1+q2 = 1.5`;
  (3) direct/controller bypasses lack exact execution-call primitives.
- [x] Confirm PyGRC supplies no public state-only intervention that removes the
  scheduling gap. The admitted native mechanism remains packet debit, so the
  gap belongs to exact registration rather than runtime availability.
- [x] Obtain owner direction on a bounded upstream registration correction.
  I06B passed 15/15 with zero blockers and is explicitly owner-accepted;
  REG-GATE is restored and the retained draft may now be corrected, completed,
  and candidate-free validated under I07.
- [x] Execute authorized construction start 1 under `.venv`; generate exactly
  234 primary entries, 234 conditional-retry ceilings, a 20-file binding
  receipt, and an inactive freeze with candidate execution false.
- [x] Retain authorized validation start 2 as failed before collection:
  `.venv/bin/python -m pytest` reports `No module named pytest`. No test module,
  PyGRC, model builder, packet, candidate/control operation, response, or
  scientific window ran. Evidence: [failed-start receipt](../contracts/p2-i2/c01/i07-focused-tests-failed-start.json).
- [x] Obtain explicit owner direction before installing the missing dependency
  or authorizing any replacement test/validator start. The owner states that
  installing `pytest` does not require I07A and directs installation plus an
  in-place I07 update. DEC-045/CHG-040 preserve the failed start and authorize
  only the bounded candidate-free continuation.
- [x] Install `pytest` into `.venv` and retain its exact resolved version.
  Evidence: [environment receipt](../contracts/p2-i2/c01/i07-pytest-environment-receipt.json).
- [x] Refresh only validator process accounting and the derived binding/freeze
  hashes; preserve policy, execution semantics, matrix, tests, and all accepted
  upstream authorities. Evidence: [refresh receipt](../contracts/p2-i2/c01/i07-binding-refresh-receipt.json).
- [x] Run the one authorized replacement focused-test start and one final
  validator start. The unchanged suite passes 7/7 and the validator passes
  25/25 with zero blockers. Evidence: [final validation](../contracts/p2-i2/c01/i07-candidate-free-validation.json).
- [x] Record the owner-requested post-validation cross-entry-isolation audit
  before inspection. Scope: earlier-output dataflow, fresh process/baseline,
  unique and non-shadowing paths, mutable cache/temp/queue/RNG isolation,
  per-entry claim authorization, incomplete-entry independence, retry derivation,
  and fail-closed complete/evaluable matrix closure. This is read-only I07
  review work; it authorizes no runtime correction or candidate execution.
- [x] Complete the cross-entry-isolation audit and disposition every requested
  invariant before I07 acceptance. The row-local read set, fresh-process guard,
  fresh registered construction, branch/parameter independence, textual path
  uniqueness, entry-local primary preflight, incomplete-earlier-entry
  independence, and adapter/temporary/queue/RNG boundaries pass. Four
  enforcement blockers remain: output-root ancestor symlinks are not rejected;
  ignored shared Python bytecode caches may cross entries; retry authorization
  trusts a committed ledger boolean without reconstructing eligibility from the
  same entry's retained primary failure receipt; and no implemented manifest
  closeout fails closed over all 234 missing or nonevaluable entries. Evidence:
  [I07 inactive EXEC-FREEZE review](../reports/P2-I2-I07-EXEC-FREEZE-review.md).
- [x] Obtain owner direction before correcting the four cross-entry-isolation
  blockers. No frozen source, policy, matrix, binding, validation, or activation
  authority may change under the audit alone; EXEC-FREEZE and I08 remain closed.
  The owner assigns the bounded correction to I07A under DEC-046/CHG-042.

Exit gate `P2-I2-EXEC-FREEZE` authorizes only the named exact cycle.

## 12A. `P2-I2-I07A` — Cross-entry-isolation correction

**Status:** owner-accepted; candidate-free; commit-authorized; inactive.

**Authority:** the owner explicitly directs that CHG-041's four substantive
post-review blockers be corrected as `P2-I2-I07A`. That construction authority
opened only the bounded execution-safety correction below and did not accept
I07A or open I08. Acceptance and inactive-gate passage are supplied separately
by DEC-047/CHG-043; no candidate/control operation is authorized.

- [x] Name I07A and freeze its checklist/hypothesis scope before changing any
  frozen runner, policy, test, validator, matrix, binding, or freeze byte.
- [x] Retain an I07A input freeze binding the reviewed I07 policy, source,
  tests, matrix, binding, inactive freeze, validation, and CHG-041 audit report.
  Evidence: [I07A input freeze](../contracts/p2-i2/c01/i07a-cross-entry-isolation-input-freeze.json).
- [x] Replace leaf-only output checks with beneath-root, no-symlink-component
  traversal and exclusive creation for every claim, output, and failure receipt;
  require every current-entry artifact leaf to have its frozen unique role.
- [x] Bind live execution to `.venv/bin/python -B`; reject any project/PyGRC
  import cache before local runtime import and after execution, so ignored
  `__pycache__`, `.pyc`, or `.pyo` state cannot cross entries.
- [x] Remove shared retry-ledger dataflow. A conditional attempt 2 may read only
  its own frozen row, exact retained attempt-1 claim/failure receipt, and common
  accepted authorities; it must mechanically reconstruct pre-construction
  eligibility and may not inspect another entry's receipt or outcome.
- [x] Implement an exact-path cycle-completion builder that enumerates the 234
  frozen rows rather than directories, accepts exactly one evaluable terminal
  output per row, and creates no execution manifest if any row is missing,
  ambiguous, malformed, or operationally null.
- [x] Add focused candidate-free positive and negative tests for ancestor
  symlinks, physical containment, occupied receipt leaves, cache refusal,
  row-local retry reconstruction, cross-entry receipt refusal, and missing/null/
  duplicate completion states. Evidence:
  [focused-test receipt](../contracts/p2-i2/c01/i07a-focused-tests-receipt.json),
  15/15 passed.
- [x] Use at most three candidate-free Python starts, all through `.venv` with
  `-B`: one derived I07A refresh, one focused pytest start, and one final I07A
  validator start. Any failed start stops for owner direction; no replacement is
  inferred. Exactly three passed starts and zero retries are retained.
- [x] Preserve the exact 234-row scientific matrix, I04R2/I05J/I06–I06B
  semantics, registered values, mode retention, resource ceilings, and zero-
  candidate boundary. Only isolation mechanics and consequential hashes change;
  all 234 entry objects reconstruct byte-semantically unchanged.
- [x] Return the complete uncommitted I07A package for owner review with
  EXEC-FREEZE and I08 still closed. Evidence:
  [I07A validation](../contracts/p2-i2/c01/i07a-candidate-free-validation.json),
  17/17 passed with zero blockers, and
  [I07A review](../reports/P2-I2-I07A-cross-entry-isolation-correction.md).
- [x] Record explicit owner acceptance and commit authorization under
  DEC-047/CHG-043. The exact inactive EXEC-FREEZE passes; live activation,
  I08, cache cleanup, candidate execution, and scientific evidence remain
  separately closed. Evidence:
  [owner acceptance](../contracts/p2-i2/c01/i07a-owner-acceptance-and-exec-freeze.json).

## 13. `P2-I2-I08` — Finite matrix execution

**Status:** mechanically complete through the owner-accepted C02 successor:
234/234 exact terminals are evaluable and `P2-I2-EXEC-GATE` passed. C01 remains
retained byte-exactly as bounded-incomplete operational history under DEC-050:
its entry 1 terminated natively after the permanent claim and before either
governed output, its attempt 2 remains mechanically unauthorized, and its other
233 entries remain unattempted. C02 does not retroactively rewrite C01.

**Activation boundary:** the owner states `ok, let's do I08`. This is the
separate direction required by DEC-047 and opens I08 preparation, including the
required exact import-cache cleanup. It does not pre-accept bytes that did not
yet exist, permit an uncommitted activation, or authorize a candidate start
before the package returns for review.

- [x] Open I08 in the checklist and hypotheses before any activation artifact,
  cache removal, output-root creation, PyGRC import, or matrix entry.
- [x] Retain one I08 activation input freeze binding commit `5c2c248`, the exact
  accepted inactive authority hashes, graph revision, interpreter, 234-entry
  matrix, output/manifest absence, and owner construction direction.
- [x] Remove only ignored `__pycache__`, `.pyc`, and `.pyo` artifacts beneath
  the two frozen live import roots; retain the exact before/after inventory and
  do not change tracked graph or RCAE bytes. The exact receipt retains 207
  before and zero after, with zero tracked-byte changes.
- [x] Construct one inactive activation candidate with `owner_acceptance=false`,
  `candidate_execution_authorized=false`, and `I08_authorized=false`; bind all
  hashes required by the frozen live validator and avoid a self-referential
  commit hash.
- [x] Candidate-free validate exact committed/local authorities, clean graph
  revision, repository `.venv` and interpreter digest, relative normalized
  command, cache-free import roots, empty governed output/claim/failure state,
  absent execution manifest, all 234 unique rows, and no scientific operation:
  18/18 checks pass with zero blockers.
- [x] Return the exact activation package uncommitted for explicit owner review.
  Only that later acceptance may set the three live acceptance/authorization
  booleans true and authorize committing the activation. Evidence:
  [I08 activation review](../reports/P2-I2-I08-activation-preflight.md).
- [x] Record the owner's `+1 and make a commit` as DEC-049/CHG-045; bind the
  exact reviewed candidate hash, set only the reviewed activation fields true,
  retain `activation_commit_head=null`, and authorize the complete I08
  activation package commit without running a matrix entry.
- [x] Apply the owner's post-commit navigation correction in place: extend the
  cumulative decision index from DEC-045 through the already-retained DEC-049
  sections and amend the activation commit. This changes no decision text,
  authority, activation hash, matrix byte, output, or scientific boundary.
- [x] After the accepted activation commit, bind its full HEAD through every
  normalized entry command and revalidate clean authority/index/graph state,
  committed/local byte equality, cache absence, and empty current-entry paths
  immediately before the first claim. Exact preflight passed at `c265279`.
- [x] Invoke sequence entry 1 exactly once and retain its permanent claim.
  Native OpenBLAS termination during the common import path emits neither
  success output nor the required failure receipt.
- [x] Refuse attempt 2 because the exact failure receipt and zero-state counters
  required by the frozen retry predicate do not exist; do not delete or rewrite
  the attempt-1 claim.
- [x] Stop before sequence entry 2, retain 0/234 evaluable and no scientific
  result, and close C01 bounded incomplete after owner direction. Evidence:
  [entry-001 audit](../contracts/p2-i2/c01/i08-entry-001-native-termination-audit.json)
  and [failed-start review](../reports/P2-I2-I08-entry-001-failed-start.md).
- [x] Execute primary entries in ascending frozen `sequence_index`, each in a
  fresh `.venv/bin/python -B` process with a fresh/restored registered composite
  baseline under a separately accepted successor cycle. Do not use parallel
  workers or allow a prior outcome to change a later entry's parameters, order,
  eligibility, or branch.

- [x] Execute every registered matrix entry—mode × cell × subconfiguration ×
  seed × allowed attempt—exactly once, except for its one preregistered
  eligible infrastructure retry.
- [x] Retain per-run runtime receipts, raw responses, state identities,
  operation order, costs, leakage, and failures.
- [x] Preserve every `reference-pool`, individual-source, combined-order,
  shuffle, label-permutation, removal, freeze/clamp, private-partition,
  controller/direct-path, quantity-matched, and transfer-contrast response.
- [x] Stop under the frozen rule without adding rescue variants.
- [x] Retain incomplete or blocked evidence without converting it into a
  negative scientific result.
- [x] Generate and validate the execution manifest.

These seven generic I08 obligations were fulfilled by the separately accepted
C02 successor, not by rewriting or completing C01. The retained C02 manifest
records 234/234 evaluable terminals, 233 primary successes, one accepted
preregistered infrastructure-retry success, 235 permanent claims, one retained
pre-model failure, and zero missing, nonevaluable, or ambiguous entries. This
2026-07-15 projection reconciliation changes no authority, receipt, response,
control result, or scientific interpretation.

Exit gate `P2-I2-EXEC-GATE` records completion state only; it does not assign
the terminal class.

## 13A. `P2-I2-I08A` — C02 native-exit and resource correction

**Status:** owner-accepted and complete. The candidate-free correction and
activation validations passed, C02 subsequently completed 234/234 evaluable
terminals, and the full I08 package is retained at commit `625a411`.

**Authority:** after the C01 entry-001 audit, the owner states that there is no
need for a 512 MiB space limit on a 128 GB RAM machine. DEC-050/CHG-047 retain
C01 as bounded incomplete and authorize only the successor construction below.

- [x] Open I08A in the checklist and hypotheses before changing any execution
  machinery or constructing C02 authority.
- [x] Retain C01, its accepted activation, permanent claim, missing-output
  facts, and 0/234 evaluable disposition byte-exactly as historical authority.
- [x] Freeze C02 with new cycle, claim, failure, output, manifest, binding, and
  activation identities while preserving all 234 scientific entry projections,
  ordering, seeds, modes, cells, branches, registered values, and controls.
  Evidence: [C02 run matrix](../contracts/p2-i2/c02/run-matrix.json), 234 rows
  and zero scientific projection changes.
- [x] Remove only `RLIMIT_AS` enforcement. Retain the 180-second runtime ceiling,
  512 MiB file-size ceiling, single-local-CPU rule, `.venv/bin/python -B`, and
  graph read-only/cache-free boundaries. Evidence:
  [C02 policy](../configs/p2_i2_c02_execution_policy.json).
- [x] Put permanent claim and final success/failure receipt ownership in an
  external supervisor process. A native worker exit must retain exact exit code,
  bounded stderr digest/text, phase boundary, output absence, and conservative
  retry disposition even when Python cleanup cannot run. Evidence:
  [C02 execution source](../scripts/p2_i2_c02_execution.py).
- [x] Preserve receipt-derived retry: only a supervisor-proven pre-model,
  pre-adapter, pre-candidate failure may authorize attempt 2; unknown phase or
  missing child attestation consumes the entry and is not retryable.
- [x] Candidate-free validate C01 immutability, C02 matrix equivalence, unique
  paths, no absolute paths, supervisor native-exit behavior, no address-space
  cap, retained runtime/file ceilings, restoration, isolation, and fail-closed
  completion without importing PyGRC or running a scientific entry.
  Evidence: [focused tests](../contracts/p2-i2/c02/i08a-focused-tests-receipt.json)
  pass 8/8 and [final validation](../contracts/p2-i2/c02/i08a-candidate-free-validation.json)
  passes 18/18 with zero blockers.
- [x] Return the complete C02 freeze uncommitted for owner review. No C02 claim,
  activation, commit, or scientific evidence may be inferred from construction.
  Evidence: [I08A review](../reports/P2-I2-I08A-C02-resource-supervisor-correction.md).
- [x] Record the owner's explicit I08A acceptance and direction to continue
  through deterministic activation, commit, post-commit preflight, and entry 1
  without a duplicate activation review. Evidence: DEC-051/CHG-048.
- [x] Construct the owner-accepted C02 activation record from the reviewed
  hashes, candidate-free validate it in `.venv/bin/python -B`, and fail closed
  on any drift without executing a matrix entry. Evidence:
  [activation](../contracts/p2-i2/c02/owner-accepted-execution-authorization.json)
  and [19/19 validation](../contracts/p2-i2/c02/i08a-activation-validation.json).
- [x] Commit the complete I08A/activation package, including the permanent C01
  claim and bounded-incomplete history, before live use.
- [x] Run the read-only exact post-commit preflight against the resulting full
  HEAD, clean authority/index/graph state, committed/local byte equality,
  cache-free import roots, and absent current C02 claim/output/failure paths.
  The start fails closed because the supplied HEAD `12ff83b30…` differs from
actual commit `12ff83be7…`; no claim or entry operation occurs. Evidence:
  [failed-start receipt](../contracts/p2-i2/c02/i08a-postcommit-preflight-failed-start.json).
- [x] Record the owner direction to retry immediately because the transcribed
  HEAD is an operator fault unrelated to the experiment. One corrected
  read-only preflight is authorized; the failed command remains retained and
  is not treated as a successful preflight.
- [x] Invoke only corrected I08 sequence entry 1 under its exact normalized
  command. Retain either the externally supervised success output or failure
  receipt and stop for review before entry 2. Attempt 2 succeeds with an
  attested child, valid fixed window, empty queues, measured/registered gain
  `0.0`, and `scientific_zero=true`; interpretation remains null.
- [x] Retain the corrected-preflight entry-001 attempt-1 claim and external
  failure receipt: `ModuleNotFoundError: matplotlib`, all pre-model counters
  zero, output absent, and receipt-derived retry eligibility true.
- [x] Diagnose the failure as an I05C regression, not a missing dependency:
  `matplotlib==3.10.9` is already in `.venv`, while `_worker_command` used
  `Path(sys.executable).resolve()` and launched the resolved host interpreter.
- [x] Correct the existing I08A/I08 infrastructure in place—no I08B, C03, or
  scientific revision—so every governed Python process uses lexical
  `.venv/bin/python`; resolved targets remain digest identity only.
- [x] Add a child-process regression check for exact `sys.executable`, active
  repository `sys.prefix`, declared dependency import, and no direct system-
  Python launch; audit all P2-I2 governed Python subprocess launch sites.
- [x] Preserve attempt-1 claim/failure bytes and explicitly bridge its frozen
  eligible retry across only the committed infrastructure-source correction.
- [x] Candidate-free validate the in-place correction: 8/8 focused tests and
  18/18 validation checks pass with zero PyGRC, model, candidate, control, or
  scientific-window activity and zero infrastructure retries.
- [x] Commit the exact correction package at `6b920fb`, exact-preflight attempt
  2, and consume no more than the already-frozen same-entry retry. Retain claim
  SHA-256 `6a8e429d…` and success SHA-256 `ece9e4df…`; stop before entry 2.
- [x] Record owner acceptance of entry 1 and the direction not to create one
  narrative file per entry. Keep the preregistered governed claim/output path
  per matrix entry, but maintain one cumulative I08 execution ledger.
- [x] Admit the accepted entry-001 checkpoint across the necessary authority
  commit by exact old HEAD, entry/attempt, claim hash, output hash, source hash,
  and policy hash; do not weaken current-head authority for entries 2–234.
- [x] Replace the manifest's global single-HEAD assumption with the exact
  admitted-checkpoint rule. Unknown or mismatched historical heads fail closed.
- [x] Candidate-free test the continuation authority and historical retry
  provenance path: 9/9 focused tests pass through `.venv`, including refusal of
  an unlisted historical HEAD.
- [x] Commit the continuation authority at `180a1bf`, then run
  entries 2–234 at that one committed HEAD without per-entry commits. Stop on
  the first terminal failure/nonevaluable result; build the cumulative manifest
  only when all 234 exact terminals are evaluable. All continuation entries
  succeed on primary attempt 1; the manifest passes at 234/234 evaluable.
- [x] Produce one aggregate I08 mechanical closeout from the manifest and
  frozen matrix. Report exact response/receipt distributions without assigning
  `R01`–`R05`, resolving controls, or drawing an L02 conclusion. Evidence:
  [cumulative execution ledger](../reports/P2-I2-I08-execution.md).
- [x] Return the complete I08 output set, manifest, and cumulative ledger
  uncommitted for owner review. Do not start I09 or commit results yet.
- [x] Record owner acceptance of the complete 234/234 I08 package and explicit
  commit authorization. Commit the manifest, governed receipts, cumulative
  ledger, and synchronized authority records together; do not start I09 in the
  commit operation.

## 14. `P2-I2-I09` — Control resolution

**Status:** owner-accepted; CONTROL-GATE passed and commit authorized under
DEC-054. I10 remains unstarted until the containing commit is retained.

```text
iteration_id = P2-I2-I09
purpose = resolve retained common and L02 control projections separately by mode
entry_authority = accepted I08 commit 625a411 plus explicit owner direction
frozen_inputs_or_input_freeze_action = bind exact accepted I04R2 analysis,
  I06 registration/template, I08 matrix/manifest, common-control register,
  operational hypotheses, and R3 representation requirement before building
mutation_and_repository_boundary = additive I09 contracts/script/report and
  synchronized cumulative ledgers only; no accepted authority/evidence rewrite,
  PyGRC/model/adapter/packet/runtime invocation, or output regeneration
required_outputs = input freeze, deterministic builder/validator, compact
  control-resolution index, validation receipt, and one cumulative report
evidence_effect = control_projection_over_retained_evidence_only
exit_gate = owner review of P2-I2-CONTROL-GATE; no commit or I10 authority
```

- [x] Open I09 in the checklist and operational hypotheses before constructing
  its freeze, builder, index, validation receipt, or report.
- [x] Audit the P2-I1/R3 precedent and the accepted I04R2, I06, and I08 evidence
  shape. Retain one compact index rather than one file per control; cover all
  nineteen program-common controls, the frozen common/mode comparison rules,
  and all five L02 controls separately for each mode.
- [x] Freeze exact input paths and hashes, allowed outcomes/stages, derivation
  rules, no-new-evidence boundary, and the I09/I11 interpretation separation.
- [x] Build and validate the index solely by reading retained artifacts.
- [x] Retain exact per-mode/per-seed response relations and causal receipts
  without scalar mode aggregation or outcome-dependent rule changes.

- [x] Resolve every applicable common control separately by mode.
- [x] Resolve all five L02 controls and every required subconfiguration for
  each retained mode.
- [x] Distinguish planned applicability, resolution stage, observed outcome,
  and fail-closed effect.
- [x] Preserve mode-specific invariance and divergence expectations.
- [x] Preserve cross-mode differences without ranking the modes or collapsing
  them into one aggregate pass/fail result.
- [x] Preserve ambiguous outcomes rather than forcing pass/fail. No matched
  configuration is seed-varying, so none is assigned in the retained result.
- [x] Generate one compact lane-local control-resolution index from retained
  evidence.
- [x] Verify that the index introduces no new evidence or schema authority.

Process accounting is retained honestly inside I09: build start 1 failed
before output on the C01 audit's nested no-result fields; build start 2 emitted
a 16/20 failed-closed candidate because the validator incorrectly required one
role rather than one private partition in hybrid; the in-place schema and
single-partition corrections changed no frozen rule or evidence. Final build
and independent reconstruction each pass 21/21 through `.venv/bin/python -B`.
Across all starts there are zero PyGRC imports, models/adapters, candidate or
control invocations, matrix regenerations, or scientific interpretations.
Evidence: [input freeze](../contracts/p2-i2/i09-control-resolution-input-freeze.json),
[compact index](../contracts/p2-i2/i09-control-resolution-index.json),
[21/21 validation](../contracts/p2-i2/i09-control-resolution-validation.json),
[builder/validator](../scripts/p2_i2_i09_control_resolution.py), and
[cumulative report](../reports/P2-I2-I09-control-resolution.md).

- [x] Record the owner's `please commit` as explicit I09 acceptance, pass
  CONTROL-GATE, bind the reviewed technical hashes in the
  [acceptance record](../contracts/p2-i2/i09-owner-acceptance-and-control-gate.json),
  and authorize the containing commit without assigning interpretation.

Exit gate `P2-I2-CONTROL-GATE` passes under DEC-054 with every mandatory
control resolved; it continues to fail closed on any later identity drift or
I11 terminal-guard violation.

### 14A. `P2-I2-I09A` — Normalized-estimator correction

**Status:** complete and owner-accepted under DEC-059/CHG-063 after 24/24
generation and exact reconstruction with zero blockers. CONTROL-GATE is passed
and one containing commit is authorized.

```text
iteration_id = P2-I2-I09A
purpose = correct only the I09 primary-margin projection so every retained
          mode/order/seed tuple traverses the accepted I04R2 exact three-arm
          normalized estimator, then recompute every dependent disposition
entry_authority = I10 failed start 001, DEC-056 finding, and owner "+1"
frozen_inputs_or_input_freeze_action = bind accepted I09 commit cfa19fe,
          accepted I09 artifacts, exact I04R2 estimator/policies, I05 delta,
          I08 matrix/manifest/raw terminals, and authorized correction builder
mutation_and_repository_boundary = additive I09A freeze/index/validation/
          report/script and synchronized ledgers only; accepted I09 and
          I04R2/I05/I06/I08 bytes are immutable
required_outputs = one portable input freeze, corrected compact index, exact
          validation, one cumulative correction report, and one deterministic
          builder/validator
evidence_effect = corrected derived control projection over retained evidence;
          no raw-evidence, schema, mode-ranking, or terminal authority
exit_gate = complete uncommitted package returned for explicit owner review;
          CONTROL-GATE, commit, I10 retry, RECON-GATE, and I11 remain closed
```

- [x] Record DEC-057/CHG-056 and the I09A operational-hypothesis declaration
  before constructing any correction artifact or running its builder.
- [x] Retain accepted I09 freeze/index/validation/script/report byte-exactly as
  historical authority and prove their committed identities before correction.
- [x] Freeze exact retained inputs, accepted estimator route, `delta`, allowed
  additive outputs, zero-runtime boundary, and exact process ceiling.
- [x] Rebuild the accepted I09 projection from retained I08 evidence and prove
  it is byte-identical before replacing any derived estimator field in memory.
- [x] Route all 18 mode/order/seed three-envelope tuples through
  `p2_i2_i04r2_analysis.primary_margin`; preserve raw candidate and leave-one
  responses and deterministic exact-tie provenance.
- [x] Rebuild the compact I09A index, validation, and cumulative correction
  report; recompute all 38 comparison-rule, 15 lane-control, and 57 program-
  mode dispositions rather than carrying authored outcomes forward.
- [x] Verify no accepted artifact changed, no PyGRC/model/adapter/packet/C02
  worker ran, no absolute path was persisted, and no scientific interpretation,
  mode ranking, `R01`–`R05`, terminal class, or new evidence was assigned.
- [x] Independently reconstruct every I09A output byte-exactly through
  `.venv/bin/python -B` and return the uncommitted package for owner review.

Failed start 001 is retained under CHG-057. It verified all thirteen frozen
inputs, reconstructed the accepted I09 index/validation/report byte-exactly,
and loaded the 234 retained terminals, then failed before the first estimator
evaluation because the builder supplied the I04R2 preregistration document
instead of the separately accepted machine-policy JSON. It created zero I09A
outputs and performed zero PyGRC, model, candidate/control, matrix-regeneration,
or scientific-runtime operations. The in-place correction changes only that
input binding and counts the corrected build as a separate infrastructure
start; it does not create another experiment iteration.

The corrected build and independent reconstruction each pass 24/24 checks.
Each pass invokes the accepted exact three-arm estimator for all eighteen
retained tuples. Twelve positive margins normalize from the historical raw-
difference projection `0.125` to `1.0`; six zero margins remain `0.0`.
State-carried is therefore `1.0/1.0` across physical orders, while history-
carried and hybrid are `1.0/0.0`. All raw response values and causal receipts
remain exact. Recomputed outcomes remain 38/38 comparison passes, 15/15 lane-
control passes, and 56 program-mode passes plus one explicit not-applicable.

Evidence: [input freeze](../contracts/p2-i2/i09a-control-resolution-input-freeze.json),
[failed start 001](../contracts/p2-i2/i09a-failed-start-001.json),
[corrected index](../contracts/p2-i2/i09a-control-resolution-index.json),
[24/24 validation](../contracts/p2-i2/i09a-control-resolution-validation.json),
[builder/validator](../scripts/p2_i2_i09a_control_resolution.py), and
[cumulative correction report](../reports/P2-I2-I09A-normalized-estimator-correction.md).

I09A corrects only derived normalized margins and text that states those
margins. It changes none of the retained response values (`0.125` or `0.0`),
scientific zeros, causal receipts, frozen rule meanings, threshold `delta`,
registration, matrix, accepted I09 bytes, or downstream dispositions. DEC-059
accepts those exact bytes and passes CONTROL-GATE.

## 15. `P2-I2-I10` — Reconstruction and identity verification

**Status:** complete and owner-accepted under DEC-059/CHG-063. Generation and
independent reconstruction each pass 24/24 with zero blockers. Failed starts
001–003 and the v1 freeze remain retained; accepted I09A supplies the exact
hash-bound additive v2 input. RECON-GATE is passed and one containing commit is
authorized. I11 becomes ready only after retention and remains unstarted.

```text
iteration_id = P2-I2-I10
purpose = independently reconstruct the retained calibration, registration,
          C02 execution manifest, I09 control projection, and deterministic
          reports; verify portable identity and registered restoration
          continuation without regenerating a scientific matrix entry
entry_authority = owner direction "I'd do I10 next" after accepted I09 commit
                  cfa19fe and passed CONTROL-GATE
frozen_inputs_or_input_freeze_action = bind exact accepted I05J, I06/I06A/I06B,
                  I08/C02, and I09 authorities, retained terminal paths/hashes,
                  deterministic builders, report targets, schema/profile
                  authorities, repository-venv identity, and admitted graph
                  revision before any reconstruction start
allowed_runtime = one bounded candidate-free restoration-continuation check per
                  retained mode in each declared reconstruction/validation
                  pass, using only the registered baseline, paired save/load,
                  one identical no-packet native step, and paired reset
forbidden = C02 entry regeneration; candidate/control contribution; response
            or comparator window; new seed/value/branch; output overwrite;
            mode selection/ranking; R01-R05, support, or terminal assignment;
            graph mutation; system-Python launch; persisted absolute path
failure_effect = fail RECON-GATE closed; preserve retained evidence unchanged;
                 never convert reconstruction failure into scientific null
output = one portable input freeze, one compact reconstruction manifest, one
         validation artifact, one cumulative report, and one validator
exit = complete uncommitted package returned for owner review; RECON-GATE and
       I11 remain closed pending explicit acceptance
```

- [x] Record DEC-055/CHG-054 and open I10 in checklist and operational-
  hypothesis projections before constructing an I10 artifact or running a
  restoration-continuation check. One preparatory read-only Python
  introspection command failed at parsing before this declaration; it imported
  no PyGRC, constructed no model, read no governed output, and wrote nothing.
- [x] Retain an exact portable I10 input freeze and verify every bound input
  before the first reconstruction start.
- [x] Reconstruct calibration, registration, execution, controls, and reports
  from retained inputs into memory or temporary paths; never overwrite an
  accepted artifact.
- [x] Verify semantic digests, portable paths, schema, unsafe-claim flags, and
  graph read-only evidence across the complete reconstructed bundle.
- [x] Verify restoration identity separately from raw snapshot observations
  for state-carried, history-carried, and hybrid.
- [x] Run the frozen bounded equal-input continuation check once per mode in
  each declared pass and retain exact invocation accounting.
- [x] Recompute every mode/order/seed primary margin and threshold relation
  through the accepted I04R2 estimator.
- [x] Verify no missing artifact is silently replaced or regenerated with new
  scientific inputs and no C02 entry worker is invoked.
- [x] Return one compact review package with RECON-GATE still closed pending
  explicit owner acceptance.

- [x] Retain [failed start 001](../contracts/p2-i2/i10-reconstruction-failed-start.json)
  under CHG-055. The pass verified 41 frozen inputs, reconstructed all ten
  calibration rows through I04R2, and rebuilt the 234-terminal C02 manifest in
  memory from 470 governed paths. It then stopped on the first state-carried
  primary-margin mismatch. It created no I10 output, imported no PyGRC,
  constructed no model, invoked no C02 worker, and changed no graph byte.
- [x] Obtain owner direction before correcting the accepted I09 projection. The
  owner responded `+1`, authorizing bounded additive I09A construction under
  DEC-057/CHG-056. The correction
  is I09A: replace only the raw-difference bypass with the accepted I04R2
  estimator, rebuild the I09 index/validation/report, re-evaluate every control
  disposition, preserve I08 raw evidence and I04R2/I05/I06 bytes, and return
  uncommitted for review. I10 remains paused; after separately accepted and
  retained I09A it would receive an additive v2 input freeze, while failed
  start 001 remains immutable.
- [x] Record the owner's direction that I10 must be finished, rather than
  stopping at I09A, under DEC-058/CHG-058 before constructing v2. This permits
  one additive v2 freeze over exact uncommitted I09A hashes for combined review;
  it does not accept/commit I09A or pass CONTROL-GATE/RECON-GATE.
- [x] Retain the v1 freeze and failed start 001 byte-exactly; create one
  additive v2 freeze that binds all historical committed inputs plus the exact
  six-file I09A correction package and the corrected I10 builder.
- [x] Retain failed start 002 under CHG-059 after the first v2 generation
  verifies 47 frozen inputs, calibration, C02, and all corrected margins, then
  fails before I10 continuation checks because live I06 validation is not byte-
  identical to its retained validation. Zero I10 outputs or scientific actions
  occurred; diagnose the exact difference before changing the criterion.
- [x] Classify the one-field I06 difference under accepted I06A provenance.
  Retained validation is the exact historical five-file producer projection;
  the current accepted validator correctly sees the final 15-file manifest and
  is explicitly not the retained producer. All other bytes match. CHG-060
  requires live 15-file validation plus byte-exact reconstruction of the
  historical five-file projection; neither layer may substitute for the other.
- [x] Retain failed start 003 under CHG-061 after the provenance-corrected
  replacement reaches state-carried paired load, matches composite identity,
  but fails the separate raw-snapshot witness before any no-packet step. It
  created no I10 output or scientific action. Authorize one state-only
  structural diagnostic; do not waive or redefine either witness beforehand.
- [x] Complete the CHG-061 state-only diagnostic and classify all 20 raw
  differences before another generation start. The current and reset-baseline
  copies each contain only deterministic budget-source, parameter-identity,
  and RNG-state materialization plus canonical orientation of three
  undirected zero-flux edges. Admitted PyGRC source and its restoration matrix
  explicitly make restoration identity and continuation stable while raw full-
  snapshot digests are not a fixed point.
- [x] Record CHG-062 before another runtime start and amend the still-
  unaccepted v2 freeze in place. Require exact adapter raw equality; compare
  and retain native raw witnesses separately; admit only the exact closed
  normalization set; fail on any unexpected difference; and continue to
  require exact restoration identity, equal-input continuation, and paired
  reset for all three modes. This is not a PyGRC modification or a raw-witness
  waiver.
- [x] Run exactly one CHG-062 replacement generation and one independent
  byte-reconstruction validation through repository `.venv`, retaining exact
  model/step/start accounting and no scientific operation. Each pass passes
  24/24 with zero blockers, instantiates six I06-validation models plus six
  continuation-pair models, executes six native no-packet steps, verifies all
  three modes and 18 margins, and invokes zero C02 workers or scientific
  operations. The independent pass reproduces manifest `5e02b64a...`,
  validation `eba9d8fe...`, and report `40dabd10...` byte-exactly.
- [x] Record the owner's `commit all` as combined I09A/I10 acceptance under
  DEC-059/CHG-063; bind the fifteen reviewed technical hashes in one self-
  reference-free acceptance record; pass CONTROL-GATE and RECON-GATE;
  authorize one containing commit; and leave I11 ready but unstarted with all
  scientific interpretation fields still unassigned.

Exit gate `P2-I2-RECON-GATE` requires an independently auditable retained
bundle or a valid earlier blocked/incomplete bundle.

## 16. `P2-I2-I11` — Interpretation and closeout

**Status:** complete and owner-accepted under DEC-061/CHG-065 after retained
commit `b28ef17`. Build and independent reconstruction pass 30/30 with zero
blockers; CLOSE-GATE is passed and one containing commit is authorized. The
next move, cross-lane synthesis, and N31+ remain unopened.

```text
iteration_id = P2-I2-I11
purpose = classify the complete retained L02 evidence once, preserving all
          three dependence modes inside one lane terminal record, and close
          P2-I2 at the lowest honest boundary
entry_authority = owner direction "now the last one, I11" after accepted and
                  retained I09A/I10 commit b28ef17
frozen_inputs_or_input_freeze_action = bind the accepted brief, hypothesis and
                  interpretation contracts, metric sheet and calibration,
                  exact registration, complete C02 manifest, corrected I09A
                  index, I10 reconstruction, and governing schemas before
                  constructing a classification
allowed_runtime = deterministic retained-file parsing, schema validation,
                  report assembly, digesting, and one independent byte
                  reconstruction through repository .venv
forbidden = PyGRC/model/adapter/packet construction; C02 worker or response
            execution; new seed/value/branch/control; accepted-byte mutation;
            mode selection or scalar collapse; cross-lane synthesis/ranking;
            N31+ selection; graph mutation; system Python; persisted absolute
            path
required_outputs = one input freeze, one developmental interpretation, one
                   requirement extraction, one terminal classification, one
                   closeout manifest, one validation, one human report, one
                   deterministic closeout builder, and synchronized atlas
                   navigation/governance projections
evidence_effect = interpretation of accepted retained evidence only; no new
                  scientific observation
exit = complete uncommitted package returned for owner review; CLOSE-GATE,
       acceptance, commit, and any future naturalization work remain closed
```

- [x] Record DEC-060/CHG-064 and open I11 in the checklist and operational-
  hypothesis projection before constructing any I11 machine artifact or
  invoking the closeout builder.
- [x] Retain one portable, exact I11 input freeze and verify every accepted
  authority and retained-evidence identity before construction.
- [x] Build and validate only from retained files, with zero scientific or
  graph runtime operation and zero accepted-evidence mutation.
- [x] Revalidate the ten I09A program-common terminal guards against the final
  machine records and report claims; do not copy an authored pass boolean.

- [x] Assign all five L02 boundary-rung dispositions. R01–R05 are each reached
  in all three modes; the lane-wide support ceiling remains separate.
- [x] Preserve separate state-carried, history-carried, and hybrid realization,
  support, control, and developmental dispositions inside the one lane-level
  terminal classification.
- [x] Preserve every per-seed and physical-order metric relation without
  scalar collapse: state is six `1.0`; history and hybrid each retain three
  `1.0` and three `0.0` margins.
- [x] Assign support status, T0–T4 classification value, realization class,
  and one terminal state independently.
- [x] Record expected, adjacent, unexpected, null, mixed, and counter-
  directional observations.
- [x] Record separate becoming and development readings.
- [x] Preserve native, producer, construction, medium, leakage, transfer,
  measurement, composition, semantic, and claim debts as applicable.
- [x] Separate the observed relation from the LGRC demand implication.
- [x] State the strongest valid claim and every blocked relabel.
- [x] Record one next move with a falsifier under D-038.
- [x] Retain a human-readable report, machine terminal records, updated atlas
  projections, and the compact control-resolution index.
- [x] Stop P2-I2 after one complete terminal classification. No mode ranking,
  N31+ selection, naturalization start, or scientific rerun occurred.

Technical disposition returned for review:

```text
terminal classification = supported_bounded_candidate
highest valid rung = AE01-L02-R05
lane support status = scaffold_dependent
classification value = T3_operational_class
state_carried = native_expression_candidate / robust_aligned
history_carried = scaffold_dependent / mixed_direction_order_conditioned
hybrid = scaffold_dependent / mixed_direction_order_conditioned
strongest valid claim = bounded shared-pool co-conditioning demand pattern
terminal guard revalidation = 30/30 pass
schema and independent byte reconstruction = 30/30 pass
scientific/runtime operations = 0
owner acceptance = accepted under DEC-061
P2-I2-CLOSE-GATE = passed_after_explicit_owner_acceptance
commit authorization = one containing commit authorized
```

Exit gate `P2-I2-CLOSE-GATE`:

```text
valid terminal classification + reconstructed evidence
+ resolved mandatory controls + lowest honest boundary
+ bounded next move + claim ceiling preserved
= passed
```

## 17. Open-question and decision-timing ledger

| Question ID | Question | Earliest iteration | Status | Decision/evidence |
| --- | --- | --- | --- | --- |
| `L02-Q00` | Which public PyGRC surfaces could carry one pool? | I01/I01R1 | Decided for audit | `P2-I2-DEC-006`: node coherence + native packet contribution + feedback response composition candidate |
| `L02-Q01` | Is any native surface adequate to the L02 discriminator? | I01/I01R1 | Decided for audit | `P2-I2-DEC-006`: composition-capable native surfaces exist; complete realization adequacy is not assigned and control gaps remain |
| `L02-Q02` | Which graph sources and restoration provider are admitted? | I02/I02R1/I02R2 | Decided after reset revalidation | `P2-I2-DEC-009`: updated checkout-bound identities admitted; v1 current-only and v2 reset-aware providers available but unselected; legacy rebase provenance remains external; P2-I1 projection historical-only |
| `L02-Q03` | Which realization class is selected for each staged mode? | I03A/I03AR1, then I03B, then I03C | All three design classes are owner-accepted, runtime-conformant, and retained unranked in the I03F family index | DEC-010/DEC-012: state-carried `pygrc_native_candidate`; DEC-014: history-carried `minimally_producer_assisted`; DEC-016/DEC-017: hybrid `minimally_producer_assisted`; DEC-018/DEC-019 retain all three without selection |
| `L02-Q04` | Which dependence-mode profiles are required, and in what order? | I03 | Decided; all three design-bound | DEC-011: retain all three through execution; 8A `state_carried`, review, 8B `history_carried`, review, 8C `hybrid`, review; realization selection occurs within modes |
| `L02-Q05` | What are the exact sources, carrier, factorization, and access witness? | I03 concept; I06 exact | Owner-accepted exact registration | DEC-042 binds all node/edge IDs, per-mode masks, native P, active H_P/native M_H, joint `[P,M_H]`, and alternate-responder access witness without collapsing modes |
| `L02-Q06` | What contribution and mixing rule constitutes common state or active history? | I03 concept; I04/I06 exact | Owner-accepted exact registration | I06 registers binary-exact q1/q2 native arrivals, additive P, ordered source-label-free history with independently registered recency, and the hybrid composition; no fixture outcome informed the values |
| `L02-Q07` | Which one later response is primary? | I04/I04R1/I04R2; I06 exact | Accepted meaning and exact implementation | DEC-026 retains fixed two-step native B-target coherence gain; DEC-042 binds B baseline/gain/domain, mode masks, native producer routes, runtime tolerance, and required window receipts |
| `L02-Q08` | Which nearest insufficient-repetition comparator owns the margin? | I04/I04R1/I04R2 | Accepted under I04R2 | DEC-026 retains the all-or-none maximum of symmetric q1-only/q2-only common-carrier admission responses within one tuple; repeated-S1/S2 remains a non-failing scope diagnostic |
| `L02-Q09` | What matched null and resolution freeze `delta`? | I04–I05 | Decided and owner-accepted: governed arithmetic-null output and complete portability closeout are retained; I05J freezes `analysis_arithmetic_delta = 1e-12` into byte-reconstructed lane-local metric artifacts | DEC-030 consumed exactly one attempt with zero retries; DEC-040/041 bind the accepted native metric closeout and dependency correction; no runtime tolerance or candidate authority |
| `L02-Q10` | How do all cells and signed controls materialize? | I03 concept; I06 exact | Owner-accepted exact registration | I06 binds seven cells, 26 unique subconfigurations, five controls, nine common analysis-control mappings, and 3/3/5 mode-specific mappings; the control index remains outcome-free |
| `L02-Q11` | How are pool economy properties observed or dispositioned? | I03 concept; I06 exact | Owner-accepted exact registration | I06 registers reserves, accumulation/mixing/depletion, no-window leakage/maintenance/saturation dispositions, token/event/queue bounds, finite coherence intervals, and fail-closed overflow semantics |
| `L02-Q12` | Which capacity, contributor, or access contrast tests R05? | I03 concept; I06 exact; I11 interpretation | Accepted retained-evidence disposition | DEC-042 registers the `A_ALTERNATE` access-scope contrast; accepted I11 finds the mode-specific relation retained in all three modes and reaches R05 without inferring broader transfer |
| `L02-Q13` | What is the lane terminal class, support boundary, and next move? | I11 | Decided and owner-accepted | DEC-061 accepts `supported_bounded_candidate` through R05, lane-wide `scaffold_dependent`, `T3_operational_class`; state is native-expression candidate, history/hybrid share active-history naturalization debt; one future native substitution probe is named but not started |

Questions may move only through cumulative decisions. A later answer must not
rewrite an earlier retained decision without its reopening condition.

## 18. Evidence-triggered checklist change control

Every addition after I00 receives an ID:

```text
P2-I2-CHG-NNN
triggering_iteration
triggering_evidence
change_class
added_or_revised_items
affected_gate
rerun_scope
preserved_result_or_boundary
status
```

Allowed change classes are:

- `audit_scope_correction` before I01 completion;
- `source_admission_scope_correction` before the affected admission closes or
  during a named admission revalidation;
- `source_admission_revision_update` during a named revalidation when an
  upstream admitted dependency revision changes;
- `audit_evidence_quarantine` preserving historical provenance;
- `infrastructure_correction` with no scientific change;
- `scientific_refinement` requiring new preregistration/cycle;
- `control_or_measurement_expansion` with explicit gate/rerun effect;
- `hypothesis_projection_revision` preserving `AE01-H-L02` authority;
- `aim_redescription_or_redirect`; or
- `closure_only_retention_fix`.

No change may erase a null, negative, blocked, incomplete, or inconvenient
result. No checklist expansion may serve only to obtain support.

### 18.1 Change ledger

| Change ID | Triggering iteration/evidence | Class | Revision | Gate/rerun effect | Preserved boundary | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `P2-I2-CHG-001` | I00R1 owner-supplied artifact-stack review | `closure_only_retention_fix` plus pre-execution clarification | Acceptance provenance/status roles; I01 authorization wording; I03/I04 boundary; I05 metric artifact policy; I08 matrix quantification; OP-09 falsifiability; compact validation evidence | No gate reopened; no rerun; `BRIEF-GATE` remains passed and I01 source inspection remains unopened | Accepted brief, frozen L02/D-039 authorities, no P2-I2 evidence, graph read-only boundary | Complete |
| `P2-I2-CHG-002` | I01 in-scope `pyproject.toml` package-root declaration | `audit_scope_correction` | Add tracked `src/pygrc/**`; bind checkout-only imports to `${GRC}/src` | No gate reopened; no rerun because no package source or capability classification preceded the correction | Exact graph revision, read-only boundary, public-surface/classification/output contracts, no-evidence effect | Complete |
| `P2-I2-CHG-003` | I01R1 owner-supplied capability-audit closeout review | `audit_evidence_quarantine` plus `closure_only_retention_fix` | Quarantine candidate-shaped custom probe; rerun classifications from admissible static/generic-test evidence; correct CAP-04 to inadequate; add mode-neutral, public-support, intervention, causal-history, and restoration-ownership checks | Source-audit gate reopened during I01R1 and re-passed after corrected static revalidation; no candidate rerun | Full historical probe provenance, exact graph revision, graph read-only boundary, no source admission/realization/calibration/result | Complete |
| `P2-I2-CHG-004` | I02 first in-scope LGRC9V3 runtime read | `source_admission_scope_correction` (corrected by I02R1 before re-passing the admission gate) | Add public construction, queue-processing, save, reset, and route-configuration methods omitted from the frozen callable list; no source path added | Complete 24-symbol review rerun before original disposition and enriched I02R1 review; predecessor semantics/current file retained under explicit limits | Exact revisions/source paths, graph read-only and no-candidate rules, output/classification contracts, no-realization/no-evidence effect | Complete after I02R1 revalidation |
| `P2-I2-CHG-005` | I02R1 owner-supplied identity/authority/transition closeout review | `closure_only_retention_fix` plus `source_admission_scope_correction` | Reopen admission gate; correct CHG-004 governance; retain imported-package provenance, granular roles/callable contracts, provider validation, identity coverage, explicit invariants, and cross-artifact/no-I03 checks | All fourteen review areas and twelve gate conditions passed; source-admission gate re-passed; I03 ready | Historical I02 provenance and DEC-007, exact graph revision, read-only boundary, conditional authority, no restoration-correctness/scientific evidence | Complete |
| `P2-I2-CHG-006` | I02R2 owner-reported upstream PyGRC reset-baseline correction at revision `83e3a300426631ee4df71b661b67d4fcfdfed594` | `source_admission_revision_update` | Reopen exact graph source/provider admission; validate reset-baseline persistence, identity coverage, schema transition, and compatibility policy before re-admission | Full affected/effective source/import/callable/provider review, 68 tests plus 32 subtests, and generic reset-conformance rerun passed; I03 readiness restored | Historical I02/I02R1 provenance, graph read-only boundary, provider remains unselected, no realization/scientific evidence | Complete |
| `P2-I2-CHG-007` | I03 owner direction after generic input-freeze validation and before realization comparison | `hypothesis_projection_revision` preserving `AE01-H-L02` | Replace one single-mode I03 resolution with review-separated 8A state-carried, 8B history-carried, and 8C hybrid profiles; narrow the active freeze to I03A and prohibit later-mode work | I03A package is review-ready; umbrella discriminator gate remains open; I03B/I03C/I04 unauthorized pending intervening owner reviews | Exact entry authority/digests, accepted brief and OP-01..OP-09 semantics, native-first rule, no candidate/calibration/evidence effect | Complete; I03A accepted as I03AR1 baseline under DEC-012 |
| `P2-I2-CHG-008` | I03A owner clarification after static design validation and before I03A acceptance | `owner_accepted_mode_family_scope_correction` | Correct singular mode-selection language: retain and test all three profiles through I04–I11; select native/producer/missing-prerequisite disposition within each mode; preserve one lane terminal classification with separate mode dispositions | Brief gate remains passed under DEC-011; revalidate affected I03A cross-artifact invariants; no I03B/I04 authorization and no runtime/scientific rerun | Frozen Phase 1 L02 authority, seven cells, five controls, OP-01..OP-09, I03A causal meaning, native-first rule, original I03A entry freeze, graph read-only boundary | Complete; owner accepted 2026-07-14 |
| `P2-I2-CHG-009` | Owner acceptance of the stronger runtime-conformance path after I03A review | `owner_accepted_precalibration_realization_conformance_scope` | Add 8A-R1 before I03B; require bounded runtime conformance inside later I03B/I03C mode freezes; distinguish conformance from I04–I08 scientific work; preserve original I03A freeze | I03AR1 active only after its own freeze; I03B/I03C/I04 remain unauthorized; failure reopens realization adequacy rather than assigning an L02 result | Accepted I03A causal meaning, all three retained modes, scientific calibration/registration/execution sequence, no-tuning rule, claim ceiling, graph read-only boundary | I03AR1 portion complete and review-ready; continues to govern I03B/I03C |
| `P2-I2-CHG-010` | First frozen I03AR1 evidence invocation stopped before output on strict equality between derived `0.09999999999999998` and literal `0.1` | `infrastructure_assertion_representation_correction` | Add I03AR1R1; freeze absolute tolerance `1e-12` and relative tolerance `0` for derived response-delta comparisons only; issue new harness/freeze identities | Original invocation permanently invalid with no output/evidence; one replacement evidence invocation plus one reconstruction may run only after revised-freeze validation | All fixture values, branches, native calls, causal assertions, source/import identities, quarantine, no-search rule, graph read-only boundary | Complete; replacement 136/136 and reconstruction byte-identical |
| `P2-I2-CHG-011` | I03BR1 owner-supplied twenty-one-point acceptance review | `closure_only_retention_fix` | Add a frozen zero-runtime closeout audit; retain latest-contact exclusion, functional H_P/M_H identity, exact lifecycle, layered restoration, mechanical quarantine rejection set, and six downstream obligations | No runtime rerun and no I03B artifact rewrite; 21/21 checks passed with zero blockers; later DEC-015 opened only I03C and kept I04 blocked | Exact I03B hashes and invocation accounting, minimally producer-assisted class, I03A independence, no scientific evidence, graph read-only boundary | Complete; owner accepted for progression under DEC-015 |
| `P2-I2-CHG-012` | Owner progression acceptance of I03B/I03BR1 and direction that 8C is next | `owner_accepted_staged_progression_and_hybrid_entry` | Accept I03B for progression only; open checklist/hypothesis-first I03C; freeze native-first hybrid selection as native P plus active H_P/M_H under one native joint feedback read | No I03B rewrite or mode ranking; separate runtime freeze passed 258/258 and byte reconstruction; I04 and the umbrella gate remain blocked | Three retained modes, I03A/I03B identities, six I03BR1 duties, no fixture-value reuse, graph read-only and scientific quarantine boundaries | Complete; I03C later owner-accepted under DEC-018 |
| `P2-I2-CHG-013` | I03CR1 owner-supplied twenty-six-area/seventeen-condition hybrid acceptance review | `closure_only_retention_fix_and_acceptance_revalidation` | Add a frozen zero-runtime audit; retain exact composite-carrier authority, qualitative 2x2, admission/self-feedback exclusions, neutral-contact qualification, layered identity, lifecycle classifications, and complete fixture-quarantine registry | No I03C artifact rewrite or runtime rerun; 26/26 review checks and 17/17 acceptance conditions passed with zero blockers; eight downstream obligations retained; umbrella gate and I04 remain blocked | Exact I03C hashes/invocation accounting, minimally producer-assisted class, three unranked modes, scientific quarantine, graph read-only boundary | Complete; owner accepted for progression on 2026-07-14 |
| `P2-I2-CHG-014` | Owner acceptance of I03C/I03CR1 for progression and direction that section 8.1 is next | `owner_accepted_staged_progression_and_family_closeout_entry` | Accept I03C for progression only; declare checklist/hypothesis-first I03F; freeze a compact zero-runtime terminal-authority composition over mode/OP/restoration/obligation/quarantine/I04-import indexes without repeating mode reviews | No I03 artifact rewrite, mode ranking, source/capability re-audit, runtime rerun, discriminator-gate passage, or I04 authorization; 12/12 integration checks and 9/9 acceptance conditions passed and I03F returned for owner review | Three accepted mode identities/classes, all retained conformance and closeout boundaries, fourteen source obligations mapped exactly once into nine duties, graph read-only and scientific quarantine boundaries | Complete; I03F owner-accepted under DEC-020 |
| `P2-I2-CHG-015` | Owner acceptance of compact I03F and direction to continue with I04 | `owner_accepted_discriminator_gate_and_calibration_preregistration_entry` | Pass only `P2-I2-DISCRIMINATOR-GATE`; declare checklist/hypothesis-first I04; require substantive response/comparator/null/analysis choices before any calibration or candidate result | I04 construction produced a 16/16 validated candidate-free package; I05, I06, and candidate execution remain blocked pending owner review; no I03 review replay or conformance-fixture reuse | Three retained unranked modes, I03 causal meanings, fourteen source obligations/nine duties, complete quarantine, graph read-only boundary, no scientific result | Complete through `P2-I2-I04-REVIEW-READY`; CAL-PRE pending owner review |
| `P2-I2-CHG-016` | Owner-supplied critical I04 review withholding CAL-PRE passage | `scientific_preregistration_correction_before_calibration` | Add I04R1; restore quantity-matched repetition to an equivalence-permitted symmetric scope diagnostic; replace the primary required-divergence contrast; harden order, analytic-null, fixed-window, B-purity, mode-isolation, evidence-derived-chain, and quarantine semantics | Corrected package passed 19/19 focused checks and 15/15 pure tests; CAL-PRE remains pending explicit owner acceptance; original I04 retained history; zero null/candidate/runtime execution | Accepted brief/L02/D-039 authority, all three I03 modes and causal semantics, graph read-only boundary, no scientific result | Complete through corrected `P2-I2-I04-REVIEW-READY` under DEC-023 |
| `P2-I2-CHG-017` | Owner-supplied conditional I04R1 acceptance review | `closure_only_retention_fix` plus future-null estimator-path correction | Add I04R2; verify all-or-none two-arm evaluability, route future I05 through the exact raw three-arm estimator, and harden I06 diversion/gain plus response-window receipts without executing any governed null/runtime/candidate | 16/16 focused checks and 7/7 pure tests passed; future-I05 bypass corrected; zero matched-null/PyGRC/candidate/control execution; package returned for explicit owner acceptance | I04R1 conceptual correction, three retained modes, pre-runtime rationale/quarantine, graph read-only boundary, no scientific result | Complete through `P2-I2-I04R2-ACCEPTANCE-READY` under DEC-025 |
| `P2-I2-CHG-018` | Explicit project-owner acceptance of I04R2 and direction to pass CAL-PRE, commit, and authorize only one separately frozen I05 arithmetic-null invocation | `owner_accepted_progression_authority_and_gate_passage` plus navigation closeout | Accept I04R2 as sole progression authority; pass only CAL-PRE; mark original I04/I04R1 immutable historical; audit navigation/authority fields; keep I05 invocation, I06, and candidates closed behind separate gates | CAL-PRE passed under DEC-026; I05 ready but not begun; no authorization/output/null/runtime/candidate operation created during I04R2 closeout | Exact accepted I04R2 identities and validation, historical I04/I04R1 bytes, all three modes, tie-rule non-scientific meaning, no scientific result | Complete; opens only checklist/hypothesis-first I05 authorization construction after accepted-I04 commit |
| `P2-I2-CHG-019` | DEC-026 direction to construct a separately frozen ceiling for one I05 arithmetic-null invocation after the accepted-I04 commit | `single_invocation_authorization_construction` | Declare and construct a commit-bound I05 authorization candidate plus focused static validation; encode exactly one governed arithmetic-null invocation with candidate execution false | Zero-invocation construction only; no calibration builder/entry point, PyGRC, null, candidate, or control call; CAL-GATE remains closed | Accepted I04R2 commit and exact identities, owner-acceptance record, one-invocation ceiling, output absence, graph read-only boundary, no scientific result | Review-ready after 12/12 byte-reconstructed validation; proposed DEC-027, acceptance, and retention commit pending explicit owner authorization |
| `P2-I2-CHG-020` | Owner-supplied pre-acceptance review requiring genuine single-use consumption, committed-I05 binding, and readback-only reconstruction | `execution_safety_audit_before_authorization_acceptance` | Add zero-null-execution I05A audit; inspect existing mechanics without changing execution source; fail proposed DEC-027 closed if any safety item is absent | 3/8 passed with five blockers; no acceptance, commit, invocation, retry, source correction, CAL-GATE passage, or downstream authority | Exact I04R2/I05 candidate bytes, uncommitted/inactive status, one-attempt meaning, atomic-start duty, committed-authority binding, zero-generation reconstruction, graph read-only boundary | Complete and blocked; correction authorized separately under DEC-028/CHG-021 |
| `P2-I2-CHG-021` | Explicit owner authorization of a bounded correction after I05A failed closed | `I05_owned_execution_safety_correction` | Add one governed wrapper, one one-shot policy, atomic permanent claim/final receipts, committed-HEAD/clean-state/interpreter/command binding, readback-only reconstruction accounting, and zero-null refusal tests | 10/10 tests and 12/12 checks pass; commit and null invocation unauthorized; CAL-GATE closed; returned for review | All accepted I04R2 scientific bytes and identities, candidate-free boundary, one-attempt/zero-retry limit, no self-referential commit hash, graph read-only boundary, no scientific result | Complete and owner-review-ready under DEC-028 |
| `P2-I2-CHG-022` | Explicit owner acceptance of I05B and commit authorization, followed by direction to proceed to 10.4 after retention | `owner_acceptance_commit_and_launch_authority_split` | Retain exact machine acceptance with commit true/null launch false; require a separate committed 10.4 launch record; validate local ext4 non-temporary non-symlink claim storage and occupied-path refusal | 12/12 tests and 12/12 checks pass; accepted package committed; launch record/claim/output absent; CAL-GATE closed | I04R2 bytes, one attempt/zero retries, permanent claim, readback-only reconstruction, candidate-free/scientific quarantine | Complete under DEC-029; opens checklist/hypothesis-governed 10.4 only after commit |
| `P2-I2-CHG-023` | Project-owner direction to proceed with 10.4 after accepted I05B commit `c1f821d` | `separate_single_null_launch_authority` | Record DEC-030; create and commit the exact launch record required by the accepted wrapper; execute one attempt with zero retries; retain/reconstruct output and freeze only arithmetic resolution | One governed attempt completed with one builder call, zero retries, one readback, zero reconstruction generations, and second-start refusal | Accepted I05B/I04R2 bytes, immutable acceptance, candidate/PyGRC exclusion, one-shot claim, no scientific interpretation | Complete at historical evidence commit `c3eabf3`; metric closeout remains gated |
| `P2-I2-CHG-024` | Final preflight at launch commit `98770ae` failed before claim because the valid active `.venv/bin/python` symlink resolves outside the repository; owner direction: “always use venv” | `preclaim_active_venv_path_identity_correction` | Validate exact lexical `.venv/bin/python` command and active repository venv separately from the resolved target; retain exact binary digest/version; update consequential hashes and add direct positive/negative tests | 13/13 tests and 12/12 zero-null checks passed; no claim/output/builder/null operation occurred during correction | I04R2/null bytes, one attempt/zero retries, normalized command, target digest, claim/output mechanics, candidate/PyGRC exclusion | Complete, owner-approved, and committed at `9d81f15`; enabled the later single attempt |
| `P2-I2-CHG-025` | Committed I05 evidence exposed forbidden absolute paths; owner rule: absolute paths are never allowed; `+1` on a P2-I2-wide audit/correction freeze | `persisted_path_portability_audit_before_correction` | Add checklist/hypothesis-first I05D; freeze and execute a static current-tree audit; correct recursive selector coverage within I05D before retaining the inventory; group future corrections beginning with I05 | Audit only; no affected-artifact edit, history rewrite, null/wrapper/PyGRC/candidate/control/conformance/calibration operation, metric freeze, or gate passage | Current-tree P2-I2 scope, repository-relative inventory, value-redaction, exact digests, explicit nested coverage, historical commit/digest lineage, `.venv` execution | Complete and owner-accepted under DEC-032/033: 312 violations, 70 affected files, 135 scanned files |
| `P2-I2-CHG-026` | Owner accepts the I05D inventory as the right next move and opens the first bounded correction group | `i05_historical_to_portable_projection_correction` | Correct the eleven affected I05 files plus exact consequential identity/projection records; replace persisted machine locations with relative/logical identities; retain historical raw hashes and one-shot facts | 10/10 validation and 13/13 focused helper tests pass; zero corrected-group violations; no governed null/wrapper/PyGRC/candidate/control/conformance/calibration/scientific invocation | I05D inventory, commit/digest-only historical lineage, consumed attempt, I04R2 numbers/estimator/exclusions, zero I05-group violations | Complete, owner-accepted, and commit-authorized under DEC-033; next group begins only after retention |
| `P2-I2-CHG-027` | Owner accepts/commits the first portability group and directs progression to the next group | `i04_i05_authority_dependency_portable_projection_correction` | Add I05F; freeze and correct only the 13 I04/I05 authority-dependency files plus exact consequential lineage identities; retain accepted semantics by historical commit/digest | Technical result 10/10 and 30 to zero findings; 13 static Python starts exceeded the frozen ceiling of three; zero builder/null/wrapper/PyGRC/candidate/control/conformance/calibration/scientific invocation; no I03 or later group | Commit `6dd6898`, accepted I05D group, historical I04/I04R1/I04R2 bytes, unchanged I05 output/claim/final, CAL-PRE meaning, original immutable freeze | Technically complete; process deviation closed under DEC-035/CHG-028 and package accepted under DEC-036/CHG-029 |
| `P2-I2-CHG-028` | Owner `+1` authorizes the proposed I05F in-place process-deviation closeout | `I05F_additive_static_validation_deviation_closeout` | Retain one additive record binding the immutable three-invocation ceiling, actual 13-start ledger, technical 10/10 result, zero-runtime boundary, and package/commit exclusions; perform no rerun | Process deviation accepted without claiming freeze compliance; zero Python, validator, builder/null/wrapper/PyGRC/candidate/control/conformance/scientific rerun during closeout construction | Original I05F freeze/policy, technical validation and lineage hashes, complete attempt ledger, DEC-035, no full-package acceptance at closeout-record time | Complete; later full-package acceptance supplied separately by DEC-036/CHG-029 |
| `P2-I2-CHG-029` | Owner states completed closeout is also I05F acceptance and may be committed | `I05F_owner_acceptance_and_commit_authority` | Retain separate owner-acceptance authority binding the deviation closeout and accepted technical identities; commit the complete I05F package without rerun or later-group work | Full I05F package accepted and commit-authorized; zero Python/validator/runtime/scientific rerun; later group and CAL-GATE remain closed | DEC-036, immutable closeout record, I05F validation/lineage identities, parent commit `6dd6898`, complete package boundary | Complete; package commit authorized |
| `P2-I2-CHG-030` | Owner directs “third group is next” after accepted I05F commit `99c64dd` | `I03_realization_and_conformance_portable_projection_correction` | Add I05G checklist/hypothesis-first; resolve and freeze the exact third I05D group before edits; correct only its 30 files/201 findings, including structured JSON-pointer segments; retain lineage, validation, and report | Complete uncommitted correction: 10/10, 201 to zero findings, 30 lineage pairs, 105 pointer projections, 44 identical targets; two of three `.venv` validator starts used, first failed closed pre-output and second passed; zero other Python/runtime/scientific operations | Accepted I05D order/inventory, parent commit `99c64dd`, I03 historical bytes/semantics/evidence quarantine, no fourth group | Review-ready under DEC-037; awaits explicit owner acceptance/commit authority |
| `P2-I2-CHG-031` | Owner accepts/commits I05G and directs progression to the fourth group | `I01_I02_source_and_identity_portable_projection_correction` | Retain I05G at `62882ef`; add I05H checklist/hypothesis-first; resolve and freeze the exact fourth I05D group before edits; correct only its 10 files/35 findings; retain lineage, validation, and report | Complete uncommitted correction: 10/10, 35 to zero findings, 10 lineage pairs, four exact JSON, three exact report, and three exact Python projections; one of three `.venv` validator starts used and passed; zero other Python/runtime/scientific operations | Accepted I05D order/inventory, parent commit `62882ef`, I01/I02 historical bytes/source/identity/reset semantics, no fifth group | Review-ready under DEC-038; awaits explicit owner acceptance/commit authority |
| `P2-I2-CHG-032` | Owner accepts/commits I05H, requests a remaining-file check, directs no standalone review, and identifies constructed roots in the I05G/I05H validators | `terminal_governance_navigation_shared_projection_portability_correction` | Retain I05H at `1279e17`; resolve one six-file/14-finding group; add two root-constructor validators and one guard-identified shebang-constructor validator; fold all into checklist/hypothesis-first fifth/final I05I correction | Complete uncommitted correction: 10/10, terminal 14 literal findings and four constructed absolute surfaces to zero, nine lineage pairs, complete P2-I2 audit scope zero; three `.venv` validator starts (two failed closed pre-output, third passed) and zero other Python/runtime/scientific operations | Accepted I05D inventory, commit `1279e17`, current P2-I2 boundary, owner and guard constructor findings; older P2-I1/shared AE01 sources excluded | Review-ready under DEC-039; awaits explicit owner acceptance/commit authority; CAL-GATE closed |
| `P2-I2-CHG-033` | Owner accepts/commits I05I and directs return to 10.4/10.4A, then directs closure findings to amend I05J in place | `I05_analysis_arithmetic_resolution_metric_sheet_and_closure_amendment` | Retain I05I at `b5d0acb`; reconcile completed I05C from deferred metric obligations; freeze exact inputs; derive one estimator-preserving margin per seed from both orders; retain one successful native freeze generation under the I05JA correction; validate generated metric artifacts; add process/package closeout and synchronize current projections without rerun | Owner-accepted and commit-authorized: 11/11 generated checks; native outputs reconstruct byte-exactly; delta `1e-12`; complete non-self package inventory and exact process reconstruction retained; zero null rerun, PyGRC, candidate/control, runtime, or scientific operation | Accepted I04R2 estimator, governed I05 output/receipts, I05E lineage, I05I validation, unchanged base AE01-L02 metric sheet, native tooling/schema, immutable I05J/I05JA freezes/outputs/validation | Complete; CAL-GATE passed; I06 construction authorized but not begun |
| `P2-I2-CHG-034` | Original I05J native start fails before output because `.venv` lacks the pinned schema dependency | `I05JA_failed_closed_native_dependency_correction` | Preserve original freeze and failure; install only `jsonschema==4.26.0` into `.venv`; bind one unchanged native retry; extend validation accounting without changing metric semantics | Complete and accepted with I05J: two dependency-install process starts are honestly retained as one sandbox-blocked/no-change start plus one successful install; two native starts comprise one pre-output failure and one successful generation; the second of two validator starts passes 11/11; zero null/PyGRC/candidate/runtime/scientific activity | Original I05J freeze, common tooling dependency profile, exact failure/output absence, unchanged command/input/output identities, additive I05J process closeout | Retained inside accepted I05 package; no independent gate or scientific effect |
| `P2-I2-CHG-035` | Owner accepts the complete I06/I06A package and authorizes amendment into the last checkpoint commit | `I06_I06A_owner_acceptance_and_progression_authority` | Retain the successful 14/14 I06A closeout with the already committed I06 checkpoint; mark DEC-042 accepted; pass REG-GATE; open only I07 checklist/hypothesis-first freeze construction | Accepted package contains one I06 baseline validation and the honestly retained I06A failed/replacement starts; zero candidate/control/scientific operations; no rerun during acceptance/amendment | Exact I06/I06A artifacts and identities, checkpoint `7761d3e`, unchanged three unranked modes, candidate-execution prohibition | Complete; commit amendment authorized; I07 freeze construction authorized, candidate-cycle execution unauthorized |
| `P2-I2-CHG-036` | Owner directs I07 as the last preparation before actual runs | `exact_mode_indexed_candidate_cycle_freeze_construction` | Activate checklist/hypothesis-first I07; audit accepted I03–I06 and prior P2-I1 mechanics; construct one exact policy, binding receipt, cycle freeze, candidate-free validation, and review | Stopped before execution source: exact 234-entry projection identified, but three registration gaps prohibit a faithful runner; zero PyGRC imports/models and zero candidate/control/response/scientific operations | Accepted DEC-042/REG-GATE, all three unranked modes, exact I04R2/I05J/I06 identities, per-entry retry boundary, graph read-only rule, `.venv`, portability | Paused; owner authorized I06B under CHG-037 and its candidate is review-ready; EXEC-FREEZE closed |
| `P2-I2-CHG-037` | Owner `+1` accepts DEC-043's recommendation for bounded I06B | `additive_execution_readiness_registration_correction` | Pause I07; preserve accepted I06/I06A bytes; freeze only the missing native intervention schedule, full reference-P debit identity, and exact direct/controller bypass primitives; candidate-free validate under `.venv` | Review-ready at 15/15 with zero blockers; one validation start, zero retries, no PyGRC import/model, packet, candidate/control/response/comparator/scientific operation; REG-GATE reopened and EXEC-FREEZE closed | Accepted I06/I06A identities, blocked I07 audit, three-gap ceiling, native-first rule, graph read-only boundary, portability | Complete construction; uncommitted package awaits explicit owner acceptance |
| `P2-I2-CHG-038` | Owner states `sure, i accept` after confirming I06B permits return to I07 | `I06B_owner_acceptance_REG_GATE_restoration_and_I07_resumption` | Bind the exact six-file I06B package in a machine acceptance record; restore REG-GATE; resume existing I07 from its retained audit and 234-entry projection | I06B accepted with 15/15 and zero blockers; no rerun or candidate/scientific operation; commit, EXEC-FREEZE, I08, and live execution remain closed | Exact I06B hashes, immutable accepted I06/I06A, DEC-044, retained blocked I07 drafts | Complete; I07 candidate-free construction resumed |
| `P2-I2-CHG-039` | Execute the owner-authorized resumed I07 candidate-free construction/validation boundary | `I07_exact_freeze_construction_and_failed_validation_start` | Freeze final policy/source/tests/validator; use only the three declared `.venv` starts with zero retries | Start 1 generated 234 entries, 20 bound files, and inactive EXEC-FREEZE; start 2 failed before collection because `.venv` lacks `pytest`; start 3 unused; zero PyGRC/model/packet/candidate/control/scientific activity | DEC-044/CHG-038, I07 resumption freeze, accepted I06B, frozen zero-retry process boundary | Failed closed pending owner direction; no install, replacement, validator, commit, EXEC-FREEZE passage, or I08 authority |
| `P2-I2-CHG-040` | Owner: `installing pytest doesnt need I07A, just install it and udate I07 after it is installed` | `I07_environment_prerequisite_install_and_in_place_validation_continuation` | Preserve CHG-039 failure; install `pytest` only in `.venv`; update honest I07 process accounting; candidate-free refresh derived binding/freeze hashes; authorize one replacement focused-test start and one final validator start | Complete: pytest 9.1.1 installed; policy/source/tests/matrix byte-exact; binding refresh passed; tests 7/7; final validation 25/25; six starts honestly retained; zero PyGRC/model/packet/candidate/control/scientific activity | Exact CHG-039 failed-start receipt; unchanged scientific/execution policy, run matrix, tests, upstream authorities, no-candidate boundary, portability | Review-ready inside I07; no I07A, commit, EXEC-FREEZE passage, I08, or candidate execution authority |
| `P2-I2-CHG-041` | Owner requests a mechanical guarantee that earlier C01 outputs cannot influence later entries | `I07_cross_entry_isolation_audit` | Audit exact source dataflow, process/baseline construction, all derived claim/output/failure paths, cache/temp/queue/RNG state, entry-local authorization, retry derivation, and complete/evaluable matrix closeout; make no runtime correction | Row-local semantics pass and 1,404/1,404 governed paths are unique, relative, and under the declared output root; four enforcement blockers remain: ancestor-symlink containment, shared ignored bytecode caches, receipt-derived retry eligibility, and implemented fail-closed completion | Existing frozen I07 bytes, read-only shell/static inspection, no Python/runtime/candidate/scientific start, no inferred correction authority | Audit complete; EXEC-FREEZE and I08 remain closed pending owner direction |
| `P2-I2-CHG-042` | Owner states that CHG-041's four blockers can be I07A | `I07A_bounded_cross_entry_isolation_correction` | Add checklist/hypothesis-first I07A; preserve reviewed I07 hashes; correct only safe artifact containment, import-cache isolation, current-entry retry reconstruction, and exact-path fail-closed completion; use at most three `.venv/bin/python -B` starts | Complete uncommitted candidate: 15/15 focused tests and 17/17 final checks; 234 entry objects unchanged; three passed starts, zero retries, zero PyGRC/model/packet/candidate/scientific activity | DEC-046, CHG-041 audit, exact reviewed I07 hashes, immutable upstream scientific/registration semantics, zero-candidate boundary | Review-ready with zero technical blockers; EXEC-FREEZE/I08/commit remain closed pending owner acceptance |
| `P2-I2-CHG-043` | Owner states `ok, time to commit` after the complete I07A handoff | `I07A_owner_acceptance_inactive_EXEC_FREEZE_passage_and_checkpoint_commit` | Bind the exact zero-blocker I07A package in an additive acceptance record; pass only the inactive EXEC-FREEZE; commit the complete accumulated I06B/I07/I07A checkpoint | Owner-accepted: 15/15 tests, 17/17 checks, 234 entries unchanged, three passed starts, zero retries, zero runtime/scientific activity; acceptance artifact retained | DEC-047, exact I07A technical hashes, absent activation/output/manifest, branch `p2-i2-experiment`, parent `49c74e1` | Commit authorized; live activation, cache cleanup, I08, candidate execution, and scientific evidence remain closed |
| `P2-I2-CHG-044` | Owner states `ok, let's do I08` after retained commit `5c2c248` | `I08_inactive_activation_preparation` | Open I08 checklist/hypothesis-first; freeze exact inactive activation inputs; remove only frozen ignored import caches; candidate-free validate the proposed activation; return uncommitted | Complete: exact 207-to-zero cache inventory, no tracked-byte change, 18/18 checks, two `.venv/bin/python -B` starts, zero retries, zero PyGRC/model/packet/candidate/scientific activity | Accepted I07A technical hashes, exact 234 entries, inactive flags, no self-referential HEAD, no output/manifest, no commit without review | Review-ready; activation remains false/uncommitted and no matrix entry is authorized |
| `P2-I2-CHG-045` | Owner states `+1 and make a commit` after the complete I08 activation preflight handoff | `I08_owner_acceptance_and_live_activation_commit` | Accept candidate hash `52d420b`; transition only artifact version/status and acceptance/authorization fields; bind preparation hashes; commit the exact package | Activation hash `f46ebd3`; all accepted live technical hashes unchanged; no output/manifest/claim; 0/234 entries | DEC-049, exact 18/18 validation, 207-to-zero cleanup receipt, self-reference-free full-HEAD command rule | Owner-accepted and commit-authorized; live use begins only from resulting committed HEAD after exact preflight |
| `P2-I2-CHG-046` | Owner identifies that the cumulative decision index stops at DEC-045 although DEC-046–049 sections are retained, then directs update and amend | `I08_navigation_only_index_reconciliation` | Add DEC-046–049 index rows and amend the activation commit | No decision body, activation, authority, matrix, output, or scientific byte changes | Existing DEC-046–049 sections and accepted I08 activation package | Complete; navigation projection synchronized through DEC-049 |
| `P2-I2-CHG-047` | C01 entry 1 terminates natively after its permanent claim; owner states the 512 MiB space limit is unnecessary on the 128 GB host | `I08_C01_bounded_incomplete_and_I08A_C02_resource_supervisor_correction` | Retain C01 at 1 claim/0 evaluable; remove only successor `RLIMIT_AS`; externalize native-exit receipt capture; preserve the exact scientific matrix | Complete uncommitted correction: 234 unchanged projections, 29 bound files, 8/8 tests, 18/18 validation, zero blockers and zero candidate/scientific activity | C01 claim/authority/history, 234 scientific projections, receipt-derived retry, runtime/file ceilings, graph/venv/isolation boundaries | Review-ready; no C02 activation, execution, commit, or scientific evidence |
| `P2-I2-CHG-048` | Owner accepts I08A and directs steps 2–4, explicitly omitting a duplicate activation-review checkpoint | `I08A_owner_acceptance_deterministic_activation_commit_and_entry_001_resumption` | Create one hash-bound activation, validate candidate-free, commit the complete package, run exact post-commit preflight, then invoke only corrected entry 1 | Activation passes 19/19 with zero blockers and zero candidate/scientific activity; commit, preflight, and one live entry remain | Accepted I08A hashes, C01 bounded-incomplete history, no-second-review direction, full-HEAD command rule, external supervisor | Commit authorized; no entry 2, manifest, interpretation, or result commit |
| `P2-I2-CHG-049` | First post-commit C02 preflight is supplied a transcribed full HEAD that differs from the actual resulting commit | `I08A_postcommit_preflight_failed_start` | Retain exact command/error and prove zero claim/output/failure/PyGRC/candidate activity; retry only after owner direction | Failed closed at HEAD equality check; owner classifies it as unrelated operator fault and authorizes one immediate corrected preflight | DEC-051, committed activation, exact output absence, zero runtime counters, owner retry direction | Corrected read-only preflight authorized; entry 1 remains untouched until it passes |
| `P2-I2-CHG-050` | Corrected-preflight entry 1 proves the C02 child launcher resolves `.venv/bin/python` to system Python, repeating the I05C anti-pattern | `I08A_in_place_active_venv_child_launcher_regression_correction` | No new iteration/cycle; preserve eligible failure; apply I05C lexical-command/resolved-identity separation to every governed Python child; validate and bridge only the frozen retry | Attempt 1 retained exactly; 8/8 tests and 18/18 validation pass; commit `6b920fb`, attempt-2 preflight, and retry yield one valid evaluable terminal | I05C accepted invariant, C02 attempt-1 claim/failure, attempt-2 claim/success, same 234 projections, everything-through-venv direction | CHG-050 complete; 1/234 evaluable, entry 2 and manifest closed pending review; interpretation remains null |
| `P2-I2-CHG-051` | Owner accepts entry 1 and rejects one narrative report per entry; the accepted checkpoint necessarily precedes the continuation execution HEAD | `I08_exact_checkpoint_admission_and_cumulative_reporting` | No new iteration/cycle; admit only the exact accepted entry-001 terminal across the continuation commit; bind entries 2–234 to one current HEAD; use one cumulative I08 ledger | Commit `180a1bf`; entries 2–234 all succeed on primary attempt 1; manifest passes 234/234; aggregate mechanical closeout retained | Accepted entry-001 claim/output hashes, manifest fail-closed completion rule, exact matrix, owner acceptance | I08 review-ready uncommitted; I09 closed and interpretation null |
| `P2-I2-CHG-052` | Owner states that it is time to commit after reviewing the complete cumulative I08 closeout | `I08_complete_package_acceptance_and_checkpoint_commit` | Accept 234/234 mechanical completion and commit the complete cumulative package without starting I09 or assigning interpretation | Owner acceptance and commit authorization explicit | Exact manifest, all governed receipts, one cumulative ledger, synchronized checklist/hypothesis/decision projections | Commit authorized; I09 remains unstarted |
| `P2-I2-CHG-053` | Owner states `please commit` after the complete I09 review handoff | `I09_owner_acceptance_CONTROL_GATE_passage_and_retention_commit` | Bind the five reviewed technical artifacts byte-exactly, pass CONTROL-GATE, and commit the complete I09 package without starting I10 or assigning `R01`–`R05` | Owner acceptance and commit authorization explicit; reviewed technical hashes unchanged | DEC-054, 21/21 validation, 38/38 comparison rules, 15/15 L02 controls, 56 pass plus one not-applicable program-mode results, I11 revalidation duty | Complete; containing commit authorized; I10 ready only after retention |
| `P2-I2-CHG-054` | Owner states `I'd do I10 next` after accepted I09 commit `cfa19fe` | `I10_bounded_reconstruction_and_identity_verification` | Freeze accepted I05J/I06/I08/I09 identities; independently reconstruct derived calibration, registration, execution-manifest, controls, and reports; run only registered-baseline paired restoration/continuation checks | Construction opened; one preparatory read-only Python introspection command failed at parsing with zero import/read/write effect | DEC-055, passed CONTROL-GATE, accepted retained evidence, repository `.venv`, admitted graph revision, no-new-scientific-input boundary | In progress; RECON-GATE, I11, acceptance, and commit remain closed |
| `P2-I2-CHG-055` | First frozen I10 reconstruction pass fails on accepted I09 primary-margin bytes | `I10_failed_closed_I09_estimator_bypass_finding` | Preserve the exact failure; inspect accepted I04R2 and I09 source without changing evidence; propose only a bounded I09A correction | I09 computes `candidate - strongest` and labels it `primary_margin`; I04R2 normalizes by the maximum response/floor, so twelve positive rows are `1.0`, not `0.125`; six zero rows remain `0.0` | Exact I10 freeze/script, 41 verified inputs, ten reconstructed calibration rows, 234-terminal in-memory manifest, 470 governed paths, no PyGRC/model/output | Failed closed; CONTROL-GATE requires reconciliation; I09A correction, retry, commit, RECON-GATE, and I11 unauthorized |
| `P2-I2-CHG-056` | Owner responds `+1` to the bounded DEC-056 I09A recommendation | `I09A_normalized_estimator_correction_authorization` | Freeze accepted I09/I04R2/I05/I08 identities; prove historical I09 reconstruction; correct only 18 derived primary margins through the exact I04R2 estimator; recompute every disposition; validate with zero runtime | Complete after CHG-057: build and reconstruction each pass 24/24; 12 margins `1.0`, six `0.0`; 38/38 comparison, 15/15 lane, and 56 pass plus one not-applicable program-mode outcomes unchanged | DEC-057, accepted I09 commit `cfa19fe`, failed I10 start 001, immutable accepted bytes, repository `.venv`, no-runtime boundary | Review-ready uncommitted; acceptance, commit, CONTROL-GATE passage, I10 retry, RECON-GATE, and I11 unauthorized |
| `P2-I2-CHG-057` | I09A build start 001 fails before estimator evaluation on the wrong I04R2 policy-document binding | `I09A_in_place_machine_policy_binding_correction` | Retain exact failed start; replace only the preregistration-path binding with accepted `configs/p2_i2_i04r2_machine_policy.json`; refresh freeze/builder identities and honest process ceiling; retry within I09A | 13 inputs and historical I09 bytes verified; 234 retained terminals read; zero output, completed estimator call, PyGRC/model/candidate/control/scientific runtime | DEC-057 scope, failed-start receipt, accepted machine-policy hash, immutable evidence and accepted I09 | In-place infrastructure correction only; no new iteration or scientific authority; acceptance/commit/CONTROL-GATE/I10 remain closed |
| `P2-I2-CHG-058` | Owner states I10 needs to be finished or its tasks properly marked done after the I09A review handoff | `I10_v2_hash_bound_resume_and_combined_review` | Preserve v1/failed start; bind exact six-file local I09A package in additive v2; correct I10 targets/report to normalized margins; run one build and one duplicate reconstruction; close only demonstrated checklist tasks | Authority declaration complete before v2/script edits or runtime | DEC-058, I09A 24/24 and exact reconstruction, accepted committed lineage, repository `.venv`, read-only graph | I10 completion authorized without new iteration; combined acceptance, commit, CONTROL/RECON gates, and I11 remain closed |
| `P2-I2-CHG-059` | First I10 v2 generation fails on byte comparison of live versus retained I06 validation | `I10_in_place_I06_reconstruction_difference_diagnosis` | Retain failed start 002; permit one candidate-free I06 validation diagnostic that reports only exact differing fields; do not relax byte identity until classified | Before failure: 47 inputs, 10 calibration rows, 234 terminals/470 paths, and 18 corrected margins verified; I06 validator constructed six models; zero I10 output/scientific action | DEC-058, failed-start receipt, exact retained I06 source/validation, repository `.venv`, read-only graph | Diagnosis only inside I10; replacement build, acceptance, commit, gates, and I11 remain closed |
| `P2-I2-CHG-060` | CHG-059 diagnostic finds only `I06-12.bound_file_count` differs 5 historical versus 15 current, exactly as accepted I06A provenance declares | `I10_historical_and_current_I06_provenance_reconstruction` | Keep current live 14/14 validation against the 15-file final manifest; separately substitute only the I06A-authorized historical five-file count and require byte-exact retained-validation reconstruction; verify I06A hashes/claims | Diagnostic launcher start 1 failed pre-import; corrected diagnostic passes 14/14 with six models; one field differs and all others match; no candidate/scientific action | I06A check I06A-12, historical execution manifest hash/count, retained validation hash, current manifest/validator roles | In-place I10 reconstruction correction authorized by accepted provenance; replacement build/duplicate validation only; acceptance/commit/gates/I11 closed |
| `P2-I2-CHG-061` | Provenance-corrected I10 replacement matches state-carried composite identity after save/load but not the separate raw snapshot | `I10_state_carried_raw_load_witness_diagnosis` | Retain failed start 003; run one state-carried-only save/load structural diff; inspect exact fields before changing raw witness or loader criterion | Prior layers pass; current/historical I06 witnesses pass; six I06 plus two state-pair models; zero no-packet step, output, candidate, or scientific action | Failed-start receipt, accepted registration/build/load/composite identity, raw-witness separation, read-only graph | Diagnostic only inside I10; further replacement, acceptance, commit, gates, I11 closed |
| `P2-I2-CHG-062` | CHG-061 state-only diagnostic plus admitted PyGRC source/test contract classify all 20 differences as deterministic load normalization | `I10_in_place_native_restoration_contract_alignment` | Amend only unaccepted I10 v2: exact adapter raw equality; closed-set native raw classification; exact native restoration identity, equal-input continuation, and paired reset; refuse every unexpected raw difference | Complete: generation and independent byte reconstruction each pass 24/24; all three modes each retain exactly 20 classified differences at load/post-step/reset and zero unexpected differences; six native no-packet steps per pass; zero scientific operation | Failed start 003, graph revision `83e3a300`, admitted v1/v2 restoration identities, native restoration-matrix expectation that raw digest is not a fixed point | Complete and review-ready inside I10; no new iteration, PyGRC mutation, witness waiver, acceptance, commit, gate passage, I11, or interpretation |
| `P2-I2-CHG-063` | Owner states `commit all` after the complete combined I09A/I10 handoff | `I09A_I10_owner_acceptance_CONTROL_RECON_gate_passage_and_retention_commit` | Bind all fifteen reviewed technical artifacts byte-exactly; accept I09A and I10; pass CONTROL-GATE and RECON-GATE; authorize one containing commit | Explicit owner acceptance; I09A and I10 each pass 24/24 twice with zero blockers; no technical byte changes after review | DEC-059, exact acceptance-record hashes, unassigned R01–R05/support/ranking/terminal meaning, I11 common-guard duty | Complete; containing commit authorized; I11 ready only after retention and remains unstarted |
| `P2-I2-CHG-064` | Owner states `now the last one, I11` after retained I09A/I10 commit `b28ef17` | `I11_retained_evidence_interpretation_and_closeout_construction` | Bind exact accepted authorities and retained evidence; construct one mode-preserving lane interpretation, requirement extraction, terminal record, closeout report/manifest, and independent reconstruction | Checklist/hypothesis declaration precedes every I11 artifact and builder start; zero PyGRC/model/C02/scientific runtime permitted | DEC-060, passed CONTROL/RECON gates, accepted C02/I09A/I10, frozen terminal/developmental vocabularies | Technically complete at 30/30 build/reconstruction with zero blockers; review-ready uncommitted; CLOSE-GATE and owner acceptance pending |
| `P2-I2-CHG-065` | Owner states `commit changes` after the complete I11 review handoff | `I11_owner_acceptance_CLOSE_GATE_passage_and_retention_commit` | Bind the eight reviewed technical artifacts byte-exactly; accept the terminal/developmental/requirement interpretation; pass CLOSE-GATE; authorize one containing commit and final navigation projections | Explicit owner acceptance and commit authorization; reviewed technical hashes unchanged; additive acceptance record distinguishes reviewed versus final navigation status | DEC-061, 30/30 validation, five byte-identical reconstructed outputs, R01–R05, scaffold-dependent/T3 boundary, exact blocked claims and next-move falsifier | Complete; containing commit authorized; P2-I2 closed; cross-lane synthesis, naturalization probe, and N31+ remain unopened |

## 19. Evidence ledger

| Evidence ID | Iteration | Artifact or disposition | Evidence effect | Status |
| --- | --- | --- | --- | --- |
| `P2-I2-I00-BRIEF` | I00 | Accepted P2-I2 brief | Semantic authority only | Retained |
| `P2-I2-I00-CHECKLIST` | I00 | This checklist | Process and gate authority only | Retained |
| `P2-I2-I00-OPHYP` | I00 | [Operational-hypothesis scaffold](../hypotheses/p2-i2-operational-hypotheses.md) | Subordinate projection only | Retained |
| `P2-I2-I00-DECISIONS` | I00–I07 | Cumulative decision record through decided DEC-044, including accepted I06/I06A/I06B and resumed candidate-free I07 | Decision authority only | Retained; REG-GATE passed, I07 resumed, EXEC-FREEZE closed |
| `P2-I2-I00-VALIDATION` | I00R1 | [Compact validation provenance](../reports/P2-I2-I00-validation.md) | Integrity/process only | Retained |
| `P2-I2-I00R1-REVIEW` | I00R1 | Section 5.2 review disposition and `P2-I2-CHG-001` | Process correction only | Retained |
| `P2-I2-I01-FREEZE` | I01 | [Audit-input freeze](../contracts/p2-i2/i01-audit-input-freeze.json) | Preregistered capability-audit scope and process only | Retained |
| `P2-I2-I01-AUDIT` | I01 | [Narrative audit](../reports/P2-I2-I01-source-current-capability-audit.md) | Public capability and missing-surface classification only | Retained |
| `P2-I2-I01-MATRIX` | I01 | [Capability matrix](../contracts/p2-i2/i01-capability-matrix.json) | Compact native adequacy and producer-demand projection only | Retained |
| `P2-I2-I01-PROVENANCE` | I01 | [Command provenance](../reports/P2-I2-I01-command-provenance.md) and [source digests](../contracts/p2-i2/i01-source-digests.json) | Reconstructibility and integrity only | Retained |
| `P2-I2-I01R1-REVALIDATION` | I01R1 | [Capability-audit closeout revalidation](../reports/P2-I2-I01R1-capability-audit-closeout-revalidation.md), `P2-I2-CHG-003`, and `P2-I2-DEC-006` | Audit validity/process correction only; quarantined probe has no capability or scientific effect | Retained |
| `P2-I2-I02-FREEZE` | I02 | [Source-admission input freeze](../contracts/p2-i2/i02-source-admission-input-freeze.json) version 1.0.1 and `P2-I2-CHG-004` | Preregistered source/provider review scope and scope correction only | Retained |
| `P2-I2-I02-ADMISSION` | I02 | [Admitted-source and restoration manifest](../contracts/p2-i2/i02-admitted-source-and-restoration-manifest.json), [transition report](../reports/P2-I2-I02-source-admission-and-restoration-transition.md), source-inventory update, and `P2-I2-DEC-007` | Exact source/provider admission only; no realization or scientific evidence | Retained |
| `P2-I2-I02R1-FREEZE` | I02R1 | [Closeout-review input freeze](../contracts/p2-i2/i02r1-closeout-review-input-freeze.json) | Preregistered identity/authority/provider review only | Retained |
| `P2-I2-I02R1-VALIDATION` | I02R1 | [CHG-004 transition](../contracts/p2-i2/i02r1-chg-004-freeze-transition.json), [validator output](../contracts/p2-i2/i02r1-identity-authority-validation.json), and [revalidation report](../reports/P2-I2-I02R1-admission-closeout-revalidation.md) | Admission integrity/provider-contract authority only; reset boundary retained; no restoration correctness or scientific evidence | Retained |
| `P2-I2-I02R2-FREEZE` | I02R2 | [Reset-baseline revalidation input freeze](../contracts/p2-i2/i02r2-reset-baseline-revalidation-input-freeze.json) | Preregistered updated-source/reset/provider review only | Retained |
| `P2-I2-I02R2-SOURCE` | I02R2 | [Exact graph source transition](../contracts/p2-i2/i02r2-graph-source-transition.json) and [updated admission manifest](../contracts/p2-i2/i02r2-admitted-source-and-reset-provider-manifest.json) | Exact updated source/provider authority only | Retained |
| `P2-I2-I02R2-VALIDATION` | I02R2 | [Machine reset validation](../contracts/p2-i2/i02r2-reset-baseline-validation.json), [validator](../scripts/p2_i2_i02r2_validate.py), and [revalidation report](../reports/P2-I2-I02R2-reset-baseline-persistence-revalidation.md) | Generic reset/provider conformance only; no realization or scientific evidence | Retained |
| `P2-I2-I03A-FREEZE` | I03A | [State-carried input freeze](../contracts/p2-i2/i03a-state-carried-realization-freeze-input.json) and `P2-I2-CHG-007` | Review scope, staging, and no-later-mode authority only | Retained |
| `P2-I2-I03A-CONTRACT` | I03A | [State-carried realization/discriminator contract](../contracts/p2-i2/i03a-state-carried-realization-and-discriminator-contract.json), [operational-hypothesis profile](../hypotheses/p2-i2-operational-hypotheses.md), [I03A report](../reports/P2-I2-I03A-state-carried-realization-and-operational-hypothesis-freeze.md), and `P2-I2-DEC-010` | State-carried causal preregistration only; no scientific evidence | Retained; owner accepted for progression under DEC-013 |
| `P2-I2-I03A-VALIDATION` | I03A | [Static machine validation](../contracts/p2-i2/i03a-state-carried-realization-validation.json) and [validator](../scripts/p2_i2_i03a_validate.py) | Authority/source-dataflow/cross-artifact integrity only; no candidate or calibration execution | Retained |
| `P2-I2-I03AR1-ENVIRONMENT` | I03AR1 | [RCAE `.venv` and admitted-import receipt](../contracts/p2-i2/i03ar1-environment-receipt.json) | Environment/import identity only; no runtime or scientific evidence | Retained |
| `P2-I2-I03AR1-FREEZE` | I03AR1 | [Immutable base runtime-conformance freeze](../contracts/p2-i2/i03ar1-state-carried-runtime-conformance-input-freeze.json) | Exact synthetic conformance fixture/run/quarantine authority; original invocation stopped infrastructure-invalid | Retained |
| `P2-I2-I03AR1R1-FREEZE` | I03AR1R1 | [Governed comparator freeze revision](../contracts/p2-i2/i03ar1r1-state-carried-runtime-conformance-input-freeze.json) and `P2-I2-CHG-010` | Infrastructure correction only; one replacement plus one reconstruction authority | Retained |
| `P2-I2-I03AR1-CONFORMANCE` | I03AR1/I03AR1R1 | [Raw conformance record and embedded runtime receipt](../contracts/p2-i2/i03ar1-state-carried-runtime-conformance.json) and [narrative report](../reports/P2-I2-I03AR1-state-carried-runtime-conformance.md) | Quarantined realization implementation-conformance only; 136/136; no calibration or L02 result | Retained; owner accepted for progression under DEC-013 |
| `P2-I2-I03AR1-RECONSTRUCTION` | I03AR1R1 | [Attempt and byte-reconstruction receipt](../contracts/p2-i2/i03ar1r1-runtime-reconstruction-receipt.json) | Attempt provenance and reconstructibility only; original invalid invocation has no evidence effect | Retained |
| `P2-I2-I03B-DESIGN-FREEZE` | I03B | [History-carried design input freeze](../contracts/p2-i2/i03b-history-carried-realization-freeze-input.json) | Exact native-first comparison and no-runtime design authority only | Retained |
| `P2-I2-I03B-DESIGN` | I03B | [History-carried realization contract](../contracts/p2-i2/i03b-history-carried-realization-and-discriminator-contract.json), [static validation](../contracts/p2-i2/i03b-history-carried-realization-validation.json), [validator](../scripts/p2_i2_i03b_validate.py), [report](../reports/P2-I2-I03B-history-carried-realization-and-operational-hypothesis-freeze.md), and `P2-I2-DEC-014` | Minimally producer-assisted causal-design authority only; no scientific evidence | Retained; owner accepted for progression under DEC-015 |
| `P2-I2-I03B-ENVIRONMENT` | I03B | [RCAE `.venv` and admitted-import receipt](../contracts/p2-i2/i03b-environment-receipt.json) | Environment/import identity only; no model or runtime evidence | Retained |
| `P2-I2-I03B-RUNTIME-FREEZE` | I03B | [Immutable history-carried runtime-conformance freeze](../contracts/p2-i2/i03b-history-carried-runtime-conformance-input-freeze.json) | Exact twelve-branch conformance fixture/run/quarantine authority only | Retained |
| `P2-I2-I03B-CONFORMANCE` | I03B | [Raw conformance record and embedded runtime receipt](../contracts/p2-i2/i03b-history-carried-runtime-conformance.json) | Quarantined realization implementation-conformance only; 252/252; no calibration or L02 result | Retained; owner accepted for progression under DEC-015 |
| `P2-I2-I03B-RECONSTRUCTION` | I03B | [Byte-reconstruction receipt](../contracts/p2-i2/i03b-runtime-reconstruction-receipt.json) | Invocation provenance, paired restoration witness, and byte reconstructibility only | Retained; owner accepted for progression under DEC-015 |
| `P2-I2-I03BR1-FREEZE` | I03BR1 | [Closeout-revalidation input freeze](../contracts/p2-i2/i03br1-closeout-revalidation-input.json) and `P2-I2-CHG-011` | Exact owner-review scope and zero-runtime audit authority only | Retained |
| `P2-I2-I03BR1-VALIDATION` | I03BR1 | [Machine revalidation](../contracts/p2-i2/i03br1-closeout-revalidation.json), [validator](../scripts/p2_i2_i03br1_validate.py), and [closeout report](../reports/P2-I2-I03BR1-history-carried-closeout-revalidation.md) | Source/dataflow and retained-artifact acceptance validation only; 21/21, zero blockers, no scientific effect | Retained; owner accepted for progression under DEC-015 |
| `P2-I2-I03C-DESIGN-FREEZE` | I03C | [Hybrid design input freeze](../contracts/p2-i2/i03c-hybrid-realization-freeze-input.json) and `P2-I2-CHG-012` | Exact native-first comparison, cross-mode guard, and no-runtime design authority only | Retained |
| `P2-I2-I03C-DESIGN` | I03C | [Hybrid realization contract](../contracts/p2-i2/i03c-hybrid-realization-and-discriminator-contract.json), [design report](../reports/P2-I2-I03C-hybrid-realization-and-operational-hypothesis-freeze.md), and `P2-I2-DEC-016` | Minimally producer-assisted hybrid causal-design authority only; no scientific evidence | Retained; owner accepted for progression under DEC-018 |
| `P2-I2-I03C-VALIDATION` | I03C | [Static machine validation](../contracts/p2-i2/i03c-hybrid-realization-validation.json) and [validator](../scripts/p2_i2_i03c_validate.py) | Authority/source-dataflow/producer/restoration integrity only; no model or scientific execution | Retained |
| `P2-I2-I03C-ENVIRONMENT` | I03C | [RCAE `.venv` and admitted-import receipt](../contracts/p2-i2/i03c-environment-receipt.json) | Environment/import identity only; no model or runtime evidence | Retained |
| `P2-I2-I03C-RUNTIME-FREEZE` | I03C | [Immutable hybrid runtime-conformance freeze](../contracts/p2-i2/i03c-hybrid-runtime-conformance-input-freeze.json) | Exact fresh-value twelve-branch fixture, invocation, source/import, and quarantine authority only | Retained |
| `P2-I2-I03C-CONFORMANCE` | I03C | [Raw conformance record and embedded runtime receipt](../contracts/p2-i2/i03c-hybrid-runtime-conformance.json) | Quarantined realization implementation-conformance only; 258/258; no calibration or L02 result | Retained; owner accepted for progression under DEC-018 |
| `P2-I2-I03C-RECONSTRUCTION` | I03C | [Byte-reconstruction receipt](../contracts/p2-i2/i03c-runtime-reconstruction-receipt.json) | Invocation provenance, paired restoration witness, and byte reconstructibility only | Retained; owner accepted for progression under DEC-018 |
| `P2-I2-I03CR1-FREEZE` | I03CR1 | [Closeout-revalidation input freeze](../contracts/p2-i2/i03cr1-closeout-revalidation-input.json) and `P2-I2-CHG-013` | Exact owner-review scope, immutable I03C identities, classification rules, and zero-runtime authority only | Retained |
| `P2-I2-I03CR1-REGISTRY` | I03CR1 | [Hybrid closeout registry](../contracts/p2-i2/i03cr1-hybrid-closeout-registry.json) | Machine carrier/factorial/admission/identity/lifecycle/quarantine authority plus eight fail-closed downstream obligations | Retained |
| `P2-I2-I03CR1-VALIDATION` | I03CR1 | [Machine revalidation](../contracts/p2-i2/i03cr1-closeout-revalidation.json), [validator](../scripts/p2_i2_i03cr1_validate.py), and [closeout report](../reports/P2-I2-I03CR1-hybrid-closeout-revalidation.md) | Zero-runtime source/dataflow and retained-artifact acceptance validation only; 26/26 and 17/17 with zero blockers; no scientific effect | Retained; owner accepted for progression under DEC-018 |
| `P2-I2-I03F-FREEZE` | I03F | [Compact family-closeout input](../contracts/p2-i2/i03f-family-closeout-input.json) and `P2-I2-CHG-014` | Exact accepted terminal-authority and no-repeated-review scope only | Retained |
| `P2-I2-I03F-INDEX` | I03F | [Three-mode family index](../contracts/p2-i2/i03f-family-closeout-index.json) | Lossless mode/OP/restoration/obligation/quarantine/I04-import composition only | Retained |
| `P2-I2-I03F-VALIDATION` | I03F | [Compact validation](../contracts/p2-i2/i03f-family-closeout-validation.json), [validator](../scripts/p2_i2_i03f_validate.py), and [report](../reports/P2-I2-I03F-family-closeout.md) | Terminal-authority identity and index traceability only; 12/12 and 9/9 with zero blockers; no repeated mode review or scientific effect | Retained; owner-accepted under DEC-020 |
| `P2-I2-I04-INPUT` | I04 | [Choice-resolution input](../contracts/p2-i2/i04-choice-resolution-input.json) | Candidate-free authority/options/quarantine/absence freeze only | Retained |
| `P2-I2-I04-PREREGISTRATION` | I04 | [Calibration preregistration](../contracts/p2-i2/i04-calibration-preregistration.json), [analysis policy](../configs/p2_i2_analysis_policy.json), [calibration policy](../configs/p2_i2_calibration_policy.json), and [report](../reports/P2-I2-I04-calibration-preregistration.md) | Historical measurement, comparison, control, analysis, and future-null construction only; no calibration or scientific evidence | Retained history; superseded for progression under DEC-022/DEC-023 |
| `P2-I2-I04-VALIDATION` | I04 | [Static validation](../contracts/p2-i2/i04-calibration-preregistration-validation.json), [validator](../scripts/p2_i2_i04_validate.py), [pure analysis module](../scripts/p2_i2_analysis.py), and 10-test suite | Historical candidate-free construction integrity only; 16/16 and 10/10; zero PyGRC/null/candidate invocations | Retained history; owner withheld CAL-PRE |
| `P2-I2-I04R1-INPUT` | I04R1 | [Critical-review correction input](../contracts/p2-i2/i04r1-critical-review-correction-input.json) and `P2-I2-CHG-016` | Exact owner-review, historical-I04, pre-runtime-authority, public-source, correction, and zero-execution freeze only | Retained |
| `P2-I2-I04R1-PREREGISTRATION` | I04R1 | [Corrected preregistration](../contracts/p2-i2/i04r1-calibration-preregistration.json), [analysis policy](../configs/p2_i2_i04r1_analysis_policy.json), [calibration policy](../configs/p2_i2_i04r1_calibration_policy.json), and [correction report](../reports/P2-I2-I04R1-calibration-preregistration-correction.md) | Corrected candidate-free response/comparator/scope/null-domain/window/purity/isolation/causal-analysis history only; no calibration or scientific evidence | Immutable retained history; superseded for progression by I04R2 under DEC-026 |
| `P2-I2-I04R1-VALIDATION` | I04R1 | [Focused validation](../contracts/p2-i2/i04r1-calibration-preregistration-validation.json), [validator](../scripts/p2_i2_i04r1_validate.py), [pure analysis module](../scripts/p2_i2_i04r1_analysis.py), and 15-test suite | Candidate-free correction integrity only; 19/19 and 15/15; zero PyGRC/null/candidate/control invocations and no repeated I03 review | Immutable retained history; no independent execution authority |
| `P2-I2-I04R2-INPUT` | I04R2 | [Conditional machine-verification input](../contracts/p2-i2/i04r2-conditional-machine-verification-input.json) and `P2-I2-CHG-017` | Exact conditional review, ten-artifact I04R1 history, admitted-source identities, correction scope, and zero-execution freeze only | Retained |
| `P2-I2-I04R2-MACHINE` | I04R2 | [Machine policy](../configs/p2_i2_i04r2_machine_policy.json), [future calibration policy](../configs/p2_i2_i04r2_calibration_policy.json), [machine preregistration](../contracts/p2-i2/i04r2-machine-verification-preregistration.json), [primary analyzer](../scripts/p2_i2_i04r2_analysis.py), and [future I05 entry point](../scripts/p2_i2_i04r2_calibration.py) | Candidate-free machine-preregistration and future-estimator identity only; no null or scientific evidence | Owner-accepted sole progression authority under DEC-026; CAL-PRE passed |
| `P2-I2-I04R2-VALIDATION` | I04R2 | [Focused validation](../contracts/p2-i2/i04r2-machine-verification-validation.json), [validator](../scripts/p2_i2_i04r2_validate.py), 7-test suite, and [verification report](../reports/P2-I2-I04R2-conditional-machine-verification.md) | Conditional machine-integrity evidence only; 16/16 and 7/7; byte-identical reconstruction; zero PyGRC/null/candidate/control invocations | Retained and owner-accepted under DEC-026; sole progression authority |
| `P2-I2-I04R2-ACCEPTANCE` | I04R2 | [Owner-acceptance and CAL-PRE gate record](../contracts/p2-i2/i04r2-owner-acceptance-and-cal-pre-gate.json), `P2-I2-CHG-018`, and `P2-I2-DEC-026` | Progression and CAL-PRE gate authority only; no calibration or scientific evidence | Retained; passes CAL-PRE and opens only separately frozen I05 authorization construction |
| `P2-I2-I05-AUTHORIZATION` | I05 | [Single-invocation freeze candidate](../contracts/p2-i2/i05-calibration-execution-freeze.json), `P2-I2-CHG-019`, and proposed `P2-I2-DEC-027` | Historical base permission and exact-identity boundary only; encodes one arithmetic-null ceiling and no candidate | Retained inside the corrected I05B authority; proposed DEC-027 remains failed-closed; CAL-GATE closed |
| `P2-I2-I05-AUTHORIZATION-VALIDATION` | I05 | [12/12 machine validation](../contracts/p2-i2/i05-calibration-authorization-validation.json), [zero-invocation validator](../scripts/p2_i2_i05_authorization_validate.py), and [authorization report](../reports/P2-I2-I05-single-invocation-authorization-freeze.md) | Authorization-candidate identity integrity and byte reconstruction only; zero null/PyGRC/candidate/control invocations; no scientific effect | Retained as construction validation; insufficient for acceptance after I05A |
| `P2-I2-I05A-SAFETY-AUDIT` | I05A | [3/8 machine audit](../contracts/p2-i2/i05a-execution-safety-audit.json), [static auditor](../scripts/p2_i2_i05a_safety_audit.py), and [audit report](../reports/P2-I2-I05A-execution-safety-audit.md) | One-shot/commit-binding/reconstruction safety only; zero governed execution and no scientific effect | Retained history; five blockers, proposed DEC-027 fails closed; corrected by I05B |
| `P2-I2-I05B-CORRECTION` | I05B | [One-shot policy](../configs/p2_i2_i05b_one_shot_policy.json), [governed wrapper](../scripts/p2_i2_i05b_one_shot.py), [owner acceptance](../contracts/p2-i2/i05b-owner-acceptance.json), and DEC-028/029 plus CHG-021/022 | I05 execution-safety and authority-separation mechanics only; no change to I04R2 scientific bytes or evidence | Owner-accepted and committed; launch authority remains separate |
| `P2-I2-I05B-VALIDATION` | I05B | [Historical 12/12 zero-null validation with exact then-12-test identity](../contracts/p2-i2/i05b-zero-null-safety-validation.json), [validator](../scripts/p2_i2_i05b_validate.py), and [correction report](../reports/P2-I2-I05B-one-shot-safety-correction.md) | Atomic/commit-binding/refusal/readback integrity only; zero accepted-builder/null/PyGRC/candidate/control invocations | Byte-reconstructed and owner-accepted at commit `c1f821d`; later test identity is owned by I05C |
| `P2-I2-I05C-FAILURE` | I05C | [Pre-claim failure record](../contracts/p2-i2/i05c-preclaim-interpreter-path-failure.json) and DEC-031/CHG-024 | Exact failed final-preflight provenance only; active venv was used; zero governed attempt and no scientific effect | Retained history; correction later accepted and committed before the governed attempt |
| `P2-I2-I05C-VALIDATION` | I05C | [12/12 zero-null validation](../contracts/p2-i2/i05c-zero-null-interpreter-validation.json), [validator](../scripts/p2_i2_i05c_validate.py), [13-test suite](tests/test_p2_i2_i05b_one_shot.py), and [correction report](../reports/P2-I2-I05C-preclaim-venv-correction.md) | Active-repository-venv command/target identity integrity only; zero attempt/builder/null/PyGRC/candidate/control operations | Byte-reconstructed, owner-approved, and committed at `9d81f15`; later portability debt is governed by I05D/I05E |
| `P2-I2-I05-RAW-EXECUTION` | I05 | Governed output, permanent attempt claim, and final receipt under `outputs/p2-i2/i05/` at commit `c3eabf3` | One pure arithmetic-null attempt, one builder call, zero retries, one readback, refused second start; no scientific result | Historical raw evidence retained by commit/digest; current-tree output/claim are explicitly labelled I05E projections |
| `P2-I2-I05D-AUDIT` | I05D | [Audit freeze](../contracts/p2-i2/i05d-portability-audit-input-freeze.json), [accepted inventory](../contracts/p2-i2/i05d-portability-audit.json), [scanner](../scripts/p2_i2_i05d_portability_audit.py), and [report](../reports/P2-I2-I05D-portability-audit.md) | Static value-redacted current-tree portability audit only; 135 files, 312 violations, 70 affected files; zero affected-artifact correction or runtime/scientific operation | Accepted under DEC-033; opened only the first I05E correction group |
| `P2-I2-I05E-I05-GROUP` | I05E | [Correction freeze](../contracts/p2-i2/i05e-portability-correction-input-freeze.json), [lineage manifest](../contracts/p2-i2/i05e-portable-projection-lineage.json), [10/10 validation](../contracts/p2-i2/i05e-portability-correction-validation.json), [validator](../scripts/p2_i2_i05e_validate.py), and [report](../reports/P2-I2-I05E-portability-correction.md) | Historical-to-portable projection integrity only; eleven files, zero remaining group violations, no governed execution or scientific effect | Owner-accepted and retained at `6dd6898` under DEC-033/034; opened I05F only |
| `P2-I2-I05F-I04-I05-GROUP` | I05F | [Correction freeze](../contracts/p2-i2/i05f-portability-correction-input-freeze.json), [lineage manifest](../contracts/p2-i2/i05f-portable-projection-lineage.json), [10/10 technical validation](../contracts/p2-i2/i05f-portability-correction-validation.json), [validator](../scripts/p2_i2_i05f_validate.py), [deviation closeout](../contracts/p2-i2/i05f-static-validation-deviation-closeout.json), [owner acceptance](../contracts/p2-i2/i05f-owner-acceptance-and-commit-authority.json), and [report](../reports/P2-I2-I05F-portability-correction.md) | Historical-to-portable projection integrity only; thirteen files, 30 to zero group findings, no governed execution or scientific effect; process deviation accepted without claiming freeze compliance | Owner-accepted and commit-authorized under DEC-036; later group and CAL-GATE closed |
| `P2-I2-I05G-I03-GROUP` | I05G | [Correction freeze](../contracts/p2-i2/i05g-portability-correction-input-freeze.json), [lineage manifest](../contracts/p2-i2/i05g-portable-projection-lineage.json), [10/10 validation](../contracts/p2-i2/i05g-portability-correction-validation.json), [validator](../scripts/p2_i2_i05g_validate.py), and [report](../reports/P2-I2-I05G-portability-correction.md) | Historical-to-portable projection integrity only; thirty files, 201 to zero findings, 105 structured pointer projections and 44 identical target resolutions; zero governed/runtime/scientific effect | Owner-accepted and retained at `62882ef` under DEC-038; opened I05H only; CAL-GATE remains closed |
| `P2-I2-I05H-I01-I02-GROUP` | I05H | [Correction freeze](../contracts/p2-i2/i05h-portability-correction-input-freeze.json), [lineage manifest](../contracts/p2-i2/i05h-portable-projection-lineage.json), [10/10 validation](../contracts/p2-i2/i05h-portability-correction-validation.json), [validator](../scripts/p2_i2_i05h_validate.py), and [report](../reports/P2-I2-I05H-portability-correction.md) | Historical-to-portable projection integrity only; ten files, 35 to zero findings, four JSON, three report, and three Python projections; zero governed/runtime/scientific effect | Owner-accepted and retained at `1279e17` under DEC-039; opened read-only I05I reconciliation only; CAL-GATE remains closed |
| `P2-I2-I05I-TERMINAL-GROUP` | I05I | [Correction freeze](../contracts/p2-i2/i05i-portability-correction-input-freeze.json), [lineage manifest](../contracts/p2-i2/i05i-portable-projection-lineage.json), [10/10 validation](../contracts/p2-i2/i05i-portability-correction-validation.json), [validator](../scripts/p2_i2_i05i_validate.py), and [report](../reports/P2-I2-I05I-portability-correction.md) | Historical-to-portable projection integrity only; nine files, terminal 14 literal findings and four constructed absolute surfaces to zero, complete current P2-I2 audit scope zero; zero governed/runtime/scientific effect | Owner-accepted and retained at `b5d0acb` under DEC-040; opened only I05J; CAL-GATE remains closed |
| `P2-I2-I05J-METRIC-CLOSEOUT` | I05J | [Policy](../configs/p2_i2_i05j_metric_closeout_policy.json), [input freeze](../contracts/p2-i2/i05j-metric-closeout-input-freeze.json), [five-seed projection](../contracts/p2-i2/i05j-analysis-arithmetic-resolution-input.json), [metric calibration](../contracts/p2-i2/metric-calibration.json), [frozen metric sheet](../contracts/p2-i2/frozen-metric-sheet.json), [11/11 validation](../contracts/p2-i2/i05j-metric-closeout-validation.json), [additive process/package closeout](../contracts/p2-i2/i05j-process-and-projection-closeout.json), [validator](../scripts/p2_i2_i05j_validate.py), and [report](../reports/P2-I2-I05J-metric-closeout.md) | Candidate-blind analysis/serialization resolution only; preserves the exact strongest-marginal estimator across both orders; no runtime/measurement tolerance or scientific verdict | Owner-accepted and retained at `3be9073`; CAL-GATE passed; accepted I06/I06A now governs progression |
| `P2-I2-I05JA-DEPENDENCY-CORRECTION` | I05JA | [Original failed-start record](../contracts/p2-i2/i05ja-native-dependency-failure.json) and [additive correction freeze](../contracts/p2-i2/i05ja-native-dependency-correction-freeze.json) | Native tooling environment correction only; exact pinned dependency plus one unchanged retry; zero scientific effect | Complete and accepted inside I05J package |
| `P2-I2-I06-REGISTRATION` | I06 | [Input freeze](../contracts/p2-i2/i06-registration-input-freeze.json), [exact three-mode bundle](../contracts/p2-i2/i06-three-mode-registration.json), [manifest](../contracts/p2-i2/i06-registration-manifest.json), [outcome-free control index](../contracts/p2-i2/i06-control-resolution-index-template.json), [14/14 validation](../contracts/p2-i2/i06-registration-validation.json), [adapter revision](../scripts/p2_i2_i06_history_adapter.py), [validator](../scripts/p2_i2_i06_registration.py), and [report](../reports/P2-I2-I06-exact-registration.md) | Exact implementation/identity/control/restoration registration integrity only; baseline-only save/load/reset checks; zero candidate or scientific evidence | Owner-accepted with I06A under DEC-042; REG-GATE passed; I07 freeze construction authorized |
| `P2-I2-I06A-REVIEW-CLOSEOUT` | I06A | [Review freeze](../contracts/p2-i2/i06a-registration-review-input-freeze.json), [policy](../contracts/p2-i2/i06a-registration-review-policy.json), [historical execution manifest](../contracts/p2-i2/i06-registration-execution-manifest.json), [post-portability manifest](../contracts/p2-i2/i06-registration-post-portability-manifest.json), [failed-start receipt](../contracts/p2-i2/i06a-validation-failed-start.json), [replacement authority](../contracts/p2-i2/i06a-replacement-validation-authorization.json), [14/14 validation](../contracts/p2-i2/i06a-registration-review-validation.json), [validator](../scripts/p2_i2_i06a_validate.py), final manifest v1.1.1, and the amended [report](../reports/P2-I2-I06-exact-registration.md) | AdapterV2 implementation-conformance and exact registration-provenance integrity only; pure no-model confirmation of tolerance, admission/diversion, isolation, and retry semantics; no scientific evidence | Owner-accepted; both review blockers resolved; checkpoint amendment authorized; REG-GATE passed; I07 freeze construction authorized, candidate execution unauthorized |
| `P2-I2-I06B-EXECUTION-READINESS` | I06B | [Input freeze](../contracts/p2-i2/i06b-execution-readiness-correction-input-freeze.json), [additive overlay](../contracts/p2-i2/i06b-execution-readiness-overlay.json), [manifest](../contracts/p2-i2/i06b-execution-readiness-manifest.json), [15/15 validation](../contracts/p2-i2/i06b-execution-readiness-validation.json), [validator](../scripts/p2_i2_i06b_validate.py), [report](../reports/P2-I2-I06B-execution-readiness-correction.md), [owner acceptance](../contracts/p2-i2/i06b-owner-acceptance-and-reg-gate.json), and DEC-043/044 plus CHG-037/038 | Implementation-registration readiness and progression authority only; accepted I06/I06A bytes exact; no scientific evidence | Owner-accepted with zero blockers; REG-GATE passed; I07 resumed candidate-free; EXEC-FREEZE closed |
| `P2-I2-I07-EXEC-FREEZE-CANDIDATE` | I07 | [Resumption freeze](../contracts/p2-i2/c01/i07-candidate-cycle-resumption-input-freeze.json), [25/25 historical validation](../contracts/p2-i2/c01/i07-candidate-free-validation.json), [review and CHG-041 audit](../reports/P2-I2-I07-EXEC-FREEZE-review.md), and the reviewed hashes preserved by the [I07A input freeze](../contracts/p2-i2/c01/i07a-cross-entry-isolation-input-freeze.json) | Historical candidate-free cycle freeze and cross-entry-isolation audit only; no candidate or scientific evidence | Retained history; four blockers superseded for progression by I07A |
| `P2-I2-I07A-ISOLATED-EXEC-FREEZE-CANDIDATE` | I07A | [Input freeze](../contracts/p2-i2/c01/i07a-cross-entry-isolation-input-freeze.json), [corrected policy](../configs/p2_i2_c01_execution_policy_v2.json), [execution source](../scripts/p2_i2_execution.py), [run matrix](../contracts/p2-i2/c01/run-matrix.json), [binding](../contracts/p2-i2/c01/execution-binding-receipt.json), [inactive freeze](../contracts/p2-i2/c01/exec-freeze.json), [refresh receipt](../contracts/p2-i2/c01/i07a-derived-refresh-receipt.json), [15/15 test receipt](../contracts/p2-i2/c01/i07a-focused-tests-receipt.json), [17/17 validation](../contracts/p2-i2/c01/i07a-candidate-free-validation.json), and [review](../reports/P2-I2-I07A-cross-entry-isolation-correction.md) | Beneath-root artifact safety, import-cache isolation, row-local retry reconstruction, and exact-path fail-closed completion authority only; no candidate or scientific evidence | Zero-blocker technical package accepted by DEC-047 and the following acceptance entry; inactive EXEC-FREEZE passed |
| `P2-I2-I07A-OWNER-ACCEPTANCE` | I07A | [Owner acceptance and inactive EXEC-FREEZE](../contracts/p2-i2/c01/i07a-owner-acceptance-and-exec-freeze.json), DEC-047, and CHG-043 | Acceptance, inactive gate passage, and checkpoint-commit authority only; no activation or candidate/scientific evidence | Owner-accepted and commit-authorized; live activation and I08 remain closed |
| `P2-I2-I08-PREACTIVATION` | I08 | [Input freeze](../contracts/p2-i2/c01/i08-activation-input-freeze.json), [cache-cleanup receipt](../contracts/p2-i2/c01/i08-import-cache-cleanup-receipt.json), inactive candidate hash `52d420b`, [18/18 validation](../contracts/p2-i2/c01/i08-preactivation-validation.json), [cleanup source](../scripts/p2_i2_i08_cleanup_import_caches.py), [validator](../scripts/p2_i2_i08_preactivation_validate.py), and [review](../reports/P2-I2-I08-activation-preflight.md) | Candidate-free activation readiness only; 207 ignored cache artifacts removed, zero tracked-byte changes, no PyGRC/model/packet/candidate/control/scientific operation | Historical inactive preactivation passed; exact candidate subsequently accepted by the following entry |
| `P2-I2-I08-LIVE-ACTIVATION` | I08 | [Owner-accepted execution authorization](../contracts/p2-i2/c01/owner-accepted-execution-authorization.json), DEC-049, and CHG-045 | Exact cycle activation and commit authority only; live HEAD remains command-bound rather than self-referential; no candidate/scientific result | Owner-accepted and commit-authorized; 0/234 entries; first claim requires resulting committed HEAD and exact preflight |
| `P2-I2-I08-ENTRY-001-FAILED-START` | I08 | [Permanent claim](../outputs/p2-i2/c01/claims/state_carried/reference-pool/reference_pool_empty/not_applicable/seed-101/attempt-1.json), [native-termination audit](../contracts/p2-i2/c01/i08-entry-001-native-termination-audit.json), and [review](../reports/P2-I2-I08-entry-001-failed-start.md) | Operational failure evidence only; no governed response, retry authority, OP/R01–R05 evidence, or scientific result | C01 bounded incomplete; 1 claimed, 0/234 evaluable, 233 unattempted; I08A construction authorized |
| `P2-I2-I08A-C02-CORRECTION` | I08A | [Input freeze](../contracts/p2-i2/c02/i08a-c02-input-freeze.json), [policy](../configs/p2_i2_c02_execution_policy.json), [external supervisor](../scripts/p2_i2_c02_execution.py), [234-row matrix](../contracts/p2-i2/c02/run-matrix.json), [binding](../contracts/p2-i2/c02/execution-binding-receipt.json), [inactive freeze](../contracts/p2-i2/c02/exec-freeze.json), [8/8 test receipt](../contracts/p2-i2/c02/i08a-focused-tests-receipt.json), [18/18 validation](../contracts/p2-i2/c02/i08a-candidate-free-validation.json), and [review](../reports/P2-I2-I08A-C02-resource-supervisor-correction.md) | Infrastructure-only C02 correction: no address-space cap, retained runtime/file ceilings, external native-exit receipt boundary, exact scientific projection | Owner-accepted under DEC-051; zero blockers, PyGRC imports, models/adapters, candidate/control operations, or scientific windows; activation separately validated below |
| `P2-I2-I08A-C02-ACTIVATION` | I08A | [Activation input freeze](../contracts/p2-i2/c02/i08a-activation-input-freeze.json), [owner-accepted activation](../contracts/p2-i2/c02/owner-accepted-execution-authorization.json), [19/19 validation](../contracts/p2-i2/c02/i08a-activation-validation.json), [validator](../scripts/p2_i2_i08a_activation_validate.py), and [post-commit preflight](../scripts/p2_i2_c02_postcommit_preflight.py) | Acceptance, deterministic activation, commit, and one-entry progression authority only; no scientific evidence | Owner-accepted and commit-authorized under DEC-051; zero blockers and zero candidate/scientific activity; live use requires resulting full HEAD and exact preflight |
| `P2-I2-I08A-C02-PREFLIGHT-FAILED-START` | I08A | [Failed-start receipt](../contracts/p2-i2/c02/i08a-postcommit-preflight-failed-start.json) | Exact post-commit command/HEAD failure provenance only; no runtime or scientific evidence | Failed closed before claim; owner authorizes one corrected read-only preflight as an operator-only correction |
| `P2-I2-I08-C02-EXECUTION` | I08 | [Exact 234/234 manifest](../contracts/p2-i2/c02/execution-manifest.json), governed machine receipts under `outputs/p2-i2/c02/`, and [one cumulative ledger](../reports/P2-I2-I08-execution.md) | Registered raw response and causal/control receipt evidence; no control resolution or terminal interpretation | Owner-accepted and retained at `625a411`; EXEC-GATE passed; opened I09 |
| `P2-I2-I09-CONTROL-RESOLUTION` | I09 | [Input freeze](../contracts/p2-i2/i09-control-resolution-input-freeze.json), [compact index](../contracts/p2-i2/i09-control-resolution-index.json), [21/21 validation](../contracts/p2-i2/i09-control-resolution-validation.json), [builder/validator](../scripts/p2_i2_i09_control_resolution.py), [cumulative report](../reports/P2-I2-I09-control-resolution.md), and [owner acceptance](../contracts/p2-i2/i09-owner-acceptance-and-control-gate.json) | Deterministic control projection over retained evidence; 38/38 comparison rules, 15/15 L02 mode-controls, and 56 pass plus one not-applicable program-mode dispositions; no R01–R05 or terminal result | Owner-accepted under DEC-054; CONTROL-GATE passed and containing commit authorized; I10 not begun |
| `P2-I2-I09A-NORMALIZED-CORRECTION` | I09A | [Input freeze](../contracts/p2-i2/i09a-control-resolution-input-freeze.json), [failed start](../contracts/p2-i2/i09a-failed-start-001.json), [corrected index](../contracts/p2-i2/i09a-control-resolution-index.json), [24/24 validation](../contracts/p2-i2/i09a-control-resolution-validation.json), [builder](../scripts/p2_i2_i09a_control_resolution.py), and [report](../reports/P2-I2-I09A-normalized-estimator-correction.md) | Corrects 18 derived margins through accepted I04R2; raw evidence unchanged; every dependent disposition recomputed and unchanged | Owner-accepted under DEC-059; CONTROL-GATE passed; containing commit authorized |
| `P2-I2-I10-RECONSTRUCTION` | I10 | [v1 freeze](../contracts/p2-i2/i10-reconstruction-input-freeze.json), [v2 freeze](../contracts/p2-i2/i10-reconstruction-input-freeze-v2.json), failed starts [001](../contracts/p2-i2/i10-reconstruction-failed-start.json), [002](../contracts/p2-i2/i10-reconstruction-failed-start-002.json), and [003](../contracts/p2-i2/i10-reconstruction-failed-start-003.json), [manifest](../contracts/p2-i2/i10-reconstruction-manifest.json), [24/24 validation](../contracts/p2-i2/i10-reconstruction-validation.json), [builder](../scripts/p2_i2_i10_reconstruct.py), and [report](../reports/P2-I2-I10-reconstruction-and-identity.md) | Independent retained-evidence reconstruction plus candidate-free three-mode restoration identity, raw normalization classification, equal-input no-packet continuation, and paired reset; no new scientific evidence | Owner-accepted under DEC-059; RECON-GATE passed; containing commit authorized; I11 ready after retention |
| `P2-I2-I09A-I10-OWNER-ACCEPTANCE` | I09A/I10 | [Combined acceptance and gate record](../contracts/p2-i2/i09a-i10-owner-acceptance-and-gates.json), DEC-059, and CHG-063 | Exact technical-byte acceptance, CONTROL/RECON gate passage, and one retention-commit authority only; no interpretation | Owner-accepted by `commit all`; commit head intentionally self-reference-free; I11 remains unstarted |
| `P2-I2-I11-TERMINAL-CLOSEOUT` | I11 | [Input freeze](../contracts/p2-i2/i11-interpretation-input-freeze.json), [developmental interpretation](../contracts/p2-i2/i11-developmental-interpretation.json), [requirement extraction](../contracts/p2-i2/i11-requirement-extraction.json), [terminal classification](../contracts/p2-i2/i11-terminal-classification.json), [manifest](../contracts/p2-i2/i11-closeout-manifest.json), [30/30 validation](../contracts/p2-i2/i11-closeout-validation.json), [owner acceptance](../contracts/p2-i2/i11-owner-acceptance-and-close-gate.json), [builder](../scripts/p2_i2_i11_closeout.py), and [report](../reports/P2-I2-I11-terminal-closeout.md) | Retained-evidence interpretation only: R01–R05 reached; one mode-preserving terminal record; explicit support/realization/debt/demand boundaries; 30/30 terminal guards; zero new scientific or graph runtime | Owner-accepted under DEC-061/CHG-065; CLOSE-GATE passed; containing commit authorized; cross-lane synthesis and next-move execution remain unopened |

The ledger expands only when a named iteration retains evidence. It never
lists an intended artifact as though it already exists.
