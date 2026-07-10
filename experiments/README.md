# Experiments

This directory contains bounded evidence-producing work for
RC-Agentic-Ecology. Experiments turn conceptual vocabulary and source evidence
into frozen questions, controls, reproducible artifacts, classified results,
and explicit handoffs. They do not become canonical specifications merely by
being placed here.

## Active Post-N30 program

- [Post-N30 Agentic-Ecology Demand and Composition Atlas roadmap](Post-N30-AgenticEcology-DemandCompositionAtlasRoadmap.md)
- [AE01 experiment workspace](2026-07-AE01-post-n30-demand-composition-atlas/README.md)
- [Master program plan](../implementation/PostN30-plan.md)
- [Master program checklist](../implementation/PostN30-checklist.md)

AE01 is currently an initialized workspace only. Its Phase 1 contract has not
been frozen, no acceptance rung has been assigned, and no atlas result is
supported.

## Experiment authority

Each experiment owns its hypotheses, local contracts, implementation records,
reconstruction procedures, selected evidence, reports, controls, and closeout.
Conceptual papers may motivate questions and supply ontology or control
vocabulary, but they are not runtime evidence. Graph-project records retain
their original evidence roles and claim ceilings.

Experiment-local contracts remain historical records after closeout. A
reusable contract moves to `specs/` only through an explicit promotion decision
supported by classified experiment evidence.

## Reconstruction convention

Every artifact that supports a classification or gate must be declared in a
manifest. Its reconstruction record must identify:

- a stable artifact ID and expected repository-relative path;
- the producing command and working-directory convention;
- source, dependency, schema, and configuration identities;
- input digests and any random seeds;
- expected semantic and file digests and size;
- the required runtime, memory, disk, and hardware envelope; and
- a verification command and last verified reconstruction status.

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
