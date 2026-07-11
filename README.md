# Reflexive Coherence Agentic Ecology

**Reflexive Coherence Agentic Ecology** is a research and engineering bridge
from classical state-rule agents to Reflexive Coherence ecologies.

It asks how systems usually described as agents, states, inputs, rules,
actions, goals, rewards, and memory can instead be described as coherence
geometry: basins, boundaries, flux, support, reserve, costly continuation,
aftereffects, hierarchy, persistence, and split. It also asks how relation
usually described as communication, signaling, message passing, or coordination
can instead be described as shared-medium participation: trace, pressure,
susceptibility, co-response, resonance, parent-basin modulation, and
field-mediated continuation.

The central principle is:

```text
State should first be translated into geometry.
What cannot yet be carried by the substrate remains producer scaffolding.
Every remaining producer-state variable is naturalization debt.

Relation should first be translated into shared-medium perturbation.
Every remaining message scaffold is medium debt.
```

## Core translation

| Conventional view | RC-Agentic-Ecology translation |
| --- | --- |
| Agent state | Basin condition / geometry |
| Action | Coherence-costly flux or coupling |
| Goal / reward | Persistence pressure, closure, reserve, surplus |
| Memory | Persistent geometry / aftereffect |
| Communication | Shared-medium perturbation |
| Coordination | Co-response through trace, pressure, susceptibility, and parent-basin modulation |
| Implementation shortcut | Producer scaffold or message scaffold |
| Remaining scaffold | Naturalization debt or medium debt |

This repository develops that transition as both theory and engineering method.
It is intended for readers and implementers moving from I/O state machines,
agent-based models, and multi-agent simulations toward Reflexive Coherence
systems whose behavior is cultivated through basin structure, flux dynamics,
coherence economy, and hierarchical refinement.

The first detailed worked example is `RC-Ant`: an ant-colony ecology in which
agents, roles, trails, nest regions, cargo, food, defense, waste, construction,
specialization, and reproduction are interpreted as mobile boundary
expressions, support basins, route aftereffects, coherence reserves, and
subbasin refinements of a parent colony basin.

## Who this is for

This repository is intended for:

- readers new to Reflexive Coherence who need an entry point from familiar
  agent, state, control, and communication language;
- researchers thinking about agent-based modeling, swarms, stigmergy,
  artificial life, or ecological simulation;
- implementers preparing LGRC-oriented experiments while keeping producer
  scaffolding and message scaffolding explicit;
- contributors who want to extend RC-Agentic-Ecology without overclaiming
  native agency, cognition, or communication.

## How to use this repository

- Read `From State to Becoming` first if you are coming from state machines,
  control systems, reinforcement learning, or agent-based modeling.
- Read `RC Agentic Ecology` if you want the general mapping rule and the
  RC-Ant worked example.
- Read `The Shared Medium` if you are thinking about communication, stigmergy,
  signaling, language, or multi-agent coordination.
- Read `Shared-Medium Coordination` if you want engineering vocabulary for
  traces, pressure fields, co-response, resonance, and medium debt.

## What this repository is

This repository is the conceptual center for the **RC-Agentic-Ecology** project.

It provides:

- a transition essay for readers moving from state-driven control toward
  Reflexive Coherence becoming;
- a general mapping rule from state-rule agents to RC agentic ecologies;
- a transition essay from direct message passing toward shared-medium
  participation;
- an engineering grammar for medium-first coordination;
- a vocabulary for producer scaffolding, naturalization debt, medium debt, and
  claim boundaries;
- the `RC-Ant` specification as the first detailed worked example;
- a foundation for future LGRC-oriented implementations of agentic ecologies
  and shared-medium coordination.

## Status and claim boundary

This is a conceptual and bounded experiment repository, not a reusable runtime
package. The Post-N30 workspace now contains one retained, explicitly
constructed P2-I1 result at the bounded niche-conditioning demand-pattern
ceiling. That result does not establish an admitted ecology primitive or a
complete agentic ecology.

It does not claim that a full RC ant colony, native agency, biological
identity, consciousness, native shared-medium coordination, or complete LGRC
naturalization has already been implemented.

The papers deliberately distinguish:

- target RC ontology: basin geometry, flux, support, aftereffect, reserve,
  hierarchy, persistence, and split;
- producer scaffolding: explicit variables or policies needed when a current
  substrate cannot yet carry the target behavior natively;
- naturalization debt: remaining work required to move scaffolded behavior into
  substrate-carried regularity;
- medium debt: explicit messages, broadcasts, global variables, or coordination
  scaffolds used where the target RC meaning is shared-medium perturbation,
  trace, pressure, susceptibility, or co-response.

## Maturity ladder

| Level | Meaning |
| --- | --- |
| Conceptual mapping | A classical concept has been translated into RC vocabulary. |
| Engineering specification | The target RC meaning, scaffold, and debt are defined. |
| Producer-mediated prototype | Behavior is produced with explicit scaffolding over a substrate. |
| Partial naturalization | Some scaffolding has moved into substrate-carried geometry, flux, trace, reserve, or event history. |
| Native substrate behavior | The substrate carries the behavior without the relevant producer or message scaffold. |

## Reading path

| Order | Document | Role |
| --- | --- | --- |
| 1 | [From State to Becoming](papers/2026-06-FromStateToBecoming.md) | Transition essay for readers moving from state, rule, action, reward, and control language toward RC geometry, costly flux, persistence pressure, and cultivation. |
| 2 | [RC Agentic Ecology](papers/2026-06-RC-AgenticEcology.md) | Specification draft for translating state-rule agents into RC agentic ecologies, with RC-Ant Colony as the detailed worked example. |
| 3 | [The Shared Medium](papers/2026-06-TheSharedMedium.md) | Transition essay for readers moving from direct communication and message-passing models toward shared-medium participation, co-response, trace, resonance, and field-mediated coordination. |
| 4 | [Shared-Medium Coordination](papers/2026-06-SharedMediumCoordination-EngineeringSpec.md) | Engineering specification for translating communication, signaling, stigmergy, and multi-agent relation into shared medium, perturbation, trace, pressure, susceptibility, co-response, resonance, and medium debt. |

## Relation to other repositories

This repository depends conceptually on the broader Reflexive Coherence line:

| Repository | Relationship |
| --- | --- |
| [geometric-reflexive-coherence](https://github.com/urosj/geometric-reflexive-coherence) | Core RC/FRC theory, essays, substrate notes, and Arc of Becoming material. |
| [graph-reflexive-coherence](https://github.com/urosj/graph-reflexive-coherence) | Graph-native Python implementation and evidence workspace for GRC/LGRC model families. |

The present repository is the agentic-ecology bridge: it explains how ordinary
agent-state and message-passing language should be translated into RC geometry
and shared-medium participation before implementation claims are made.

## Current repository map

- [`papers/`](papers/README.md): conceptual ontology, transition arguments, and
  engineering vocabulary.
- [`experiments/`](experiments/README.md): bounded experiment roadmaps,
  contracts, reconstruction conventions, evidence, and closeouts. The current
  AE01 workspace has passed Review R2 and `P1-GATE` at `AE01-C2`. P2-I1 is
  closed with one bounded, explicitly constructed L01 result, and Review R3
  passed without tuning it. P2-I2 is next; all remaining lane execution stays
  independently gated. New readers can begin with
  [why AE01 matters for agentic ecology](experiments/2026-07-AE01-post-n30-demand-composition-atlas/AGENTIC-ECOLOGY-OVERVIEW.md).
- [`implementation/`](implementation/README.md): active cross-cutting plans,
  decisions, checklists, and handoffs.
- `README.md`: public orientation and claim boundary.
- `CONTRIBUTING.md`: contribution scope and review expectations.
- `CITATION.cff`: citation metadata for GitHub and archival tooling.
- `PUBLICATION-CHECKLIST.md`: finite GitHub-readiness checklist.
- `RELEASE-NOTES.md`: first public snapshot notes.

## Claim boundary

Positive claims in this repository are conceptual unless a future document
explicitly links to implementation evidence. In particular, the current papers
support the following bounded claim:

```text
RC-Agentic-Ecology provides a vocabulary and engineering method for translating
state-rule agent systems into hierarchical Reflexive Coherence basin ecologies,
and for translating message-first coordination into shared-medium participation,
while explicitly separating target geometry from producer residue and medium
debt.
```

They do not claim:

- native ant-colony life in LGRC;
- native agency without producer scaffolding;
- native shared-medium coordination without evidence;
- biological completeness;
- semantic goals inside ants;
- consciousness or personhood;
- a finished software API.

## Citation

If you use this repository, cite it with the metadata in
[CITATION.cff](CITATION.cff), and cite the specific paper or section you used.
When the work depends on the theory or implementation lineage, also cite the
relevant source repository listed above.

## License

This is a mixed-license repository:

- `papers/` documents declare `CC BY-SA 4.0` in their headers.
- Repository metadata and non-paper support files are `GPL-2.0-only` unless a
  file states otherwise.

See [LICENSE](LICENSE) for the GPL-2.0-only text.
