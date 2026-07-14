# Experiments

This directory contains bounded evidence-producing work for
RC-Agentic-Ecology. Experiments turn conceptual vocabulary and source evidence
into frozen questions, controls, reproducible artifacts, classified results,
and explicit handoffs. They do not become canonical specifications merely by
being placed here.

## Active Post-N30 program

- [Post-N30 Agentic-Ecology Demand and Composition Atlas roadmap](Post-N30-AgenticEcology-DemandCompositionAtlasRoadmap.md)
- [AE01 experiment workspace](2026-07-AE01-post-n30-demand-composition-atlas/README.md)
- [Why AE01 matters for agentic ecology](2026-07-AE01-post-n30-demand-composition-atlas/AGENTIC-ECOLOGY-OVERVIEW.md)
- [Master program plan](../implementation/PostN30-plan.md)
- [Master program checklist](../implementation/PostN30-checklist.md)

AE01 has passed Review R2 and `P1-GATE` at `AE01-C2`. P2-I1 is closed with one
bounded, explicitly constructed L01 result, and Review R3 passed without tuning
it. The P2-I2 brief gate has passed, with its source-current capability audit
pending as a named checklist iteration. Every remaining lane retains
independent calibration, registration, control-resolution, execution, and
claim boundaries.

## Experiment authority

Each experiment owns its hypotheses, local contracts, implementation records,
reconstruction procedures, selected evidence, reports, controls, and closeout.
Conceptual papers may motivate questions and supply ontology or control
vocabulary, but they are not runtime evidence. Graph-project records retain
their original evidence roles and claim ceilings.

Experiment-local contracts remain historical records after closeout. A
reusable contract moves to `specs/` only through an explicit promotion decision
supported by classified experiment evidence.

## Evidence-use tiers

Experiment work uses three progressively stronger tiers:

```text
exploratory_scratch -> registered_probe -> retained_evidence
```

Scratch is transient and may inform contract design but cannot support a
classification or gate. A registered probe has a frozen question, controls,
stopping conditions, and execution mode; its outputs remain transient until
selected. Retained evidence is declared in a manifest and must pass verified
clean reconstruction before supporting a classification, report fact, or gate.

Runtime identity, graph read-only behavior, evidence-class separation, and
claim ceilings do not weaken at earlier tiers. Every live run validates its
binding and creates a receipt even when that receipt remains in ignored local
output.

## Reconstruction convention

Every artifact that supports a classification or gate must be declared in a
manifest. Its reconstruction record must identify:

- a stable artifact ID and expected repository-relative path;
- the producing command and working-directory convention;
- environment, dependency, source-revision, and configuration identities;
- input digests and any random seeds;
- expected artifact kind, schema, semantic and file digests, and size;
- the required runtime, memory, disk, and hardware envelope; and
- a verification command and last verified reconstruction status.

Artifacts may reference versioned environment, command, dependency, resource,
and realization profiles to avoid repeated manual entry. Validation must
materialize an unambiguous resolved manifest containing every required field
before the artifact becomes retained evidence.

Tracked selected evidence belongs under its owning experiment. Disposable full
runs, raw telemetry, caches, duplicate reruns, and exploratory products belong
under the ignored top-level `outputs/` workspace. A local-only artifact cannot
support a gate unless its complete reconstruction contract has passed from a
clean work area.

Committed instructions and records must not contain checkout-specific or
machine-local paths. A PyGRC runtime location is local configuration and is
never committed. Artifact inspection is non-runtime; requested live execution
requires an explicitly compatible local PyGRC runtime and fails closed when it
is unavailable or incompatible.

RCAE treats the graph/PyGRC repository as read-only. No experiment, script,
test, adapter, or reconstruction command in this repository may modify it.

## Claim convention

Every experiment must separate:

```text
conceptual motivation
inherited source evidence
ecology-side interpretation
constructed ecology-side mechanism
observed or controlled experiment result
missing or unsuitable graph surface
candidate future graph-side discriminator
```

Negative, blocked, absent, producer-carried, and incomplete outcomes remain
visible. Demand is not substrate evidence, implementation is not admission,
and a domain-shaped fixture is not an admitted motif, regime, or domain
package.

## Directory creation rule

Create a directory only when current contract, execution, or closeout work owns
it. Empty target architecture is not scaffolded in advance. Every created path
must state its role and must not imply a positive result or stable public API.
