# Shared-Medium Coordination
## An Engineering Specification for RC-Agentic-Ecology

**Draft status:** conceptual engineering specification / no code  
**Date:** 2026-06-18  
**Purpose:** engineering companion to *The Shared Medium: From Message Passing to Field Participation in RC-Agentic-Ecology*  
**Scope:** definitions, mapping rules, design discipline, ant-colony examples, substrate-facing targets, claim boundaries  

Copyright © 2026 Uroš Jovanovič, CC BY-SA 4.0.

---

## Abstract

The companion essay *The Shared Medium* introduced the mental-model transition from direct message passing toward field participation. It argued that message passing is not wrong. It is a valid boundary-cut view: a system is divided into sender, receiver, channel, message, and protocol. This view is powerful for many computational substrates, but it hides the shared geometry that makes relation possible.

This specification turns that transition into an engineering method.

In RC-Agentic-Ecology, agents should not be designed first as closed units that communicate only by sending payloads across explicit channels. They should first be interpreted as local differentiations within a shared coherence medium. Their activities perturb that medium. Other elements respond according to their own geometry, susceptibility, reserve, cost, and basin capture. What appears as communication may therefore be direct message exchange, but it may also be trace-mediated coordination, shared-field co-response, parent-basin modulation, resonance, common reserve pressure, route-cost deformation, or aftereffect-guided continuation.

The central engineering rule is:

> Do not begin by asking what message one agent sends to another. Begin by asking what shared medium makes their responses mutually relevant.

This specification defines the engineering vocabulary for shared-medium coordination. It introduces **medium surfaces**, **perturbations**, **susceptibilities**, **co-response**, **trace fields**, **pressure fields**, **parent-basin modulation**, **resonance**, **direct-message scaffolds**, and **medium debt**. It provides a design procedure for translating communication and coordination mechanisms into RC geometry, and it gives a detailed RC-Ant worked example.

The document does not forbid direct messages. Direct messages are valid engineering constructs. They may be necessary in early implementations. But when the intended RC meaning is shared-medium participation, a direct message must be treated as a scaffold. Every such scaffold is **medium debt** until the relation can be carried by substrate geometry, trace, pressure, reserve, cost, event history, or another shared-medium surface.

---

# 1. Purpose

The first RC-Agentic-Ecology specification translated state-rule agents into basin ecologies. Its central rule was that apparent agent state should first be attempted as geometry. What cannot yet be carried by the substrate remains producer scaffolding and becomes naturalization debt.

This specification applies the same discipline to relation.

The usual engineering view says:

```text
agent A sends message M to agent B
agent B receives M
agent B updates state
```

The RC view asks:

```text
what shared medium has been perturbed?
what geometry makes the perturbation relevant?
which elements are susceptible to the altered condition?
what cost, reserve, trace, pressure, or basin relation changed?
what response appears without direct transfer?
```

This document is therefore not about replacing one communication API with another. It is about shifting the engineering target from **message-first coordination** to **medium-first coordination**.

A message may still exist. But it is no longer treated as the primitive form of relation.

---

# 2. Scope and non-claims

This is a conceptual engineering specification. It does not define a runnable API and does not claim that LGRC or any current substrate already implements native shared-medium agency.

It supports the following bounded claim:

```text
Shared-Medium Coordination provides a vocabulary and engineering method for
translating direct communication, signaling, stigmergy, coordination, and
multi-agent relation into Reflexive Coherence terms: shared medium, perturbation,
trace, pressure, susceptibility, co-response, resonance, and parent-basin
modulation.
```

It does not claim:

```text
instantaneous physical nonlocality
magical action at a distance
that messages are false or useless
that all software systems should avoid message passing
that pheromones are irrelevant
that LGRC already natively implements shared-medium coordination
that every coordination effect is already substrate-carried
that ants, swarms, societies, or colonies are conscious by this mapping
```

The distinction is important.

Message passing is not rejected. It is classified.

---

# 3. Relation to the transition essay

The essay *The Shared Medium* performs the mental-model transition. This specification gives the engineering grammar.

The essay says:

```text
message passing is a valid boundary view,
but RC asks for the shared-medium view underneath it.
```

This specification says:

```text
when designing an RC agentic ecology,
classify every relation mechanism:
    direct message,
    boundary perturbation,
    trace-mediated coordination,
    shared-field co-response,
    parent-basin modulation,
    resonance,
    or native shared-medium organization.

If a direct message is used where the target is shared-medium relation,
record medium debt.
```

The essay teaches the reader what to see. This specification teaches the designer what to declare.

---

# 4. The fundamental distinction

A direct-message system cuts relation into discrete parts:

```text
sender
receiver
channel
payload
protocol
state update
```

An RC shared-medium system begins with a common context:

```text
parent basin
shared support geometry
cost surface
reserve condition
trace field
signature field
boundary pressure
route affordance
susceptible local geometries
```

The message view is often useful because it makes relation inspectable and modular. But the shared-medium view asks what relation looked like before the cut.

A message is what relation looks like after the medium has been divided into sender, receiver, channel, and payload.

A shared-medium relation is what remains when the designer asks:

```text
what changed in the world-field such that many local geometries
can now respond compatibly?
```

---

# 5. Core definitions

## 5.1 Shared medium

A **shared medium** is the distributed coherence geometry in which multiple agentic elements are differentiated and through which their activities become mutually relevant without requiring direct pairwise message transfer.

The medium may be carried by:

```text
support distribution
flux affordance
route cost
reserve pressure
trace field
signature field
boundary condition
parent-basin demand
event history
material structure
social/institutional geometry
physical substrate
software substrate
```

The medium is not necessarily a single scalar field in an implementation. In early systems, it may be approximated by multiple ledgers, surfaces, annotations, event histories, or producer-visible structures.

The important point is relational: the medium is the common context that lets separate local responses become coordinated.

## 5.2 Medium surface

A **medium surface** is a specific substrate-carried or scaffolded aspect of the shared medium that can be perturbed and later responded to.

Examples:

```text
route-support surface
food-affordance surface
home-affordance surface
alarm-pressure surface
nursery-demand surface
waste-isolation surface
construction-tension surface
congestion-cost surface
reserve-deficit surface
social-norm surface
market-pressure surface
soil-moisture surface
mycorrhizal support surface
```

A surface is not necessarily spatial in the ordinary sense. It is a geometry of relevance: a structured condition that can alter continuation.

## 5.3 Perturbation

A **perturbation** is a change to the shared medium caused by activity.

A perturbation may:

```text
increase route support
raise local cost
deepen a demand basin
release a signature
consume reserve
bind support into structure
weaken a boundary
strengthen a boundary
leave trace
alter susceptibility
trigger decay or repair
```

A perturbation is not a message by default. It is a medium change.

## 5.4 Trace

A **trace** is a persistent medium alteration left by prior activity.

In RC-Agentic-Ecology, trace is the general class of which pheromone is one ant-colony example.

Examples:

```text
pheromone trail
path worn into ground
queue forming at an entrance
construction mark
alarm residue
soil compaction
social norm
infrastructure
habit
protocol expectation
market memory
institutional record
```

A trace changes future affordance. It may lower cost, raise cost, attract, repel, stabilize, destabilize, classify, or route future activity.

## 5.5 Signature

A **signature** is an emitted or induced field of detectability or affordance.

Examples:

```text
food odor
home/nest signature
brood demand signature
alarm scent
water gradient
heat signature
crop stress signal
social invitation
institutional notice
```

A signature is not necessarily symbolic. It becomes meaningful only through compatibility with a susceptible geometry.

## 5.6 Pressure

A **pressure** is a medium condition that changes the likelihood or cost of continuation.

Examples:

```text
colony hunger
brood demand
storage deficit
threat boundary
congestion
repair need
reserve surplus
waste accumulation
market shortage
soil dryness
fire risk
```

Pressure often belongs to a parent basin. It can modulate many local elements without being a direct broadcast.

## 5.7 Susceptibility

A **susceptibility** is the way a local geometry can be captured, shaped, or redirected by a medium condition.

An unloaded ant may be highly susceptible to food-affordance traces. A loaded ant may be highly susceptible to home-affordance traces. A guard-like ant may be highly susceptible to alarm pressure. A nurse-like ant may be highly susceptible to brood demand.

Susceptibility is not a message inbox. It is compatibility between local geometry and medium condition.

## 5.8 Co-response

A **co-response** occurs when multiple elements coordinate because they are shaped by the same medium condition, not because they directly inform one another.

Examples:

```text
many ants shift toward foraging because colony reserve pressure changes
multiple workers gather at a construction site because construction tension deepens
several robots move away from a congested corridor because route cost rises
farm workers respond to soil dryness without receiving direct commands
market participants alter behavior because shared price/inventory pressure changes
```

Co-response is one of the main engineering targets of shared-medium coordination.

## 5.9 Resonance

**Resonance** is compatibility between geometries such that a perturbation integrates rather than dissipates or destabilizes.

A trace resonates with an ant only if the ant’s current geometry can respond to it. A sentence resonates with a reader only if the reader’s interpretive geometry can unfold it. A social norm resonates only if the community geometry supports it.

Resonance is not identity of representation. It is compatibility of continuation.

## 5.10 Parent-basin modulation

**Parent-basin modulation** is a shared-medium relation in which a higher-order basin changes the affordance landscape for many sub-elements.

Examples:

```text
colony hunger increases foraging susceptibility
nest threat increases defense susceptibility
drought increases water-seeking and conservation behavior
institutional crisis changes social role pressure
swarm battery deficit increases charging pressure
```

This is not the parent basin sending individual commands. It is a change in common context.

## 5.11 Direct message

A **direct message** is a relation represented as payload transfer from one bounded unit to another through a channel or interface.

Direct messages are valid. They are often necessary. They become problematic only when treated as the complete ontology of relation.

## 5.12 Medium debt

**Medium debt** is any direct-message, global-variable, central-controller, or explicit communication scaffold used where the intended RC target is shared-medium perturbation, trace, pressure, resonance, or co-response.

Medium debt is not failure. It is an honest label for scaffolding.

---

# 6. The Shared-Medium Naturalization Rule

The communication counterpart to the RC Naturalization Rule is:

> For any agentic ecology, every apparent communication, signal, message, broadcast, command, or coordination event must first be attempted as shared-medium geometry: perturbation, trace, pressure, cost change, reserve condition, signature, susceptibility, parent-basin modulation, co-response, or resonance. Only what cannot yet be carried by the substrate may remain as explicit message passing, and every such mechanism is medium debt.

This rule does not forbid messages.

It asks the designer to classify them.

```text
If the target relation is truly discrete payload transfer:
    a message may be native to that substrate view.

If the target relation is shared context, trace, field pressure, or co-response:
    a message is probably scaffold.
```

The engineer should therefore ask:

```text
Is this message carrying content that must be explicit?
Or is it standing in for a medium perturbation that should eventually
be represented as geometry?
```

---

# 7. Communication mapping table

| Classical communication concept | RC shared-medium translation |
| --- | --- |
| Sender | Local geometry that perturbs the medium |
| Receiver | Local geometry susceptible to altered medium |
| Channel | Shared support geometry, route, field, or boundary interface |
| Message | Stabilized perturbation, trace, seed, or scaffolded payload |
| Broadcast | Parent-basin modulation or wide medium perturbation |
| Signal | Signature, pressure, gradient, trace, cost change, or field alteration |
| Protocol | Stable regularity of medium-mediated coupling |
| Meaning | Compatibility between perturbation and receiving geometry |
| Interpretation | Local unfolding of perturbation through susceptible geometry |
| Attention | Basin capture by a salient medium condition |
| Communication memory | Persistent trace or changed susceptibility |
| Coordination | Co-response through shared geometry or parent-basin pressure |
| Miscommunication | Perturbation fails to resonate, resonates wrongly, or is captured by incompatible basin |
| Noise | Perturbation that does not integrate into relevant geometry |
| Latency | Delay in medium propagation, susceptibility capture, or trace response |
| Bandwidth | Capacity of medium to sustain distinguishable perturbations |
| Routing | Geometry of affordance and cost shaping where perturbations travel or matter |
| Consensus | Stable alignment across multiple local geometries |
| Conflict | Competing basin pressures or incompatible medium captures |

---

# 8. Coordination ladder

Shared-medium coordination should be described with a ladder of relation forms. The ladder is not a moral ranking. Lower rungs are not wrong. They are different cuts and different substrate commitments.

## M0 — Direct message passing

```text
A sends payload to B.
B receives payload and updates state.
```

This is the classical sender-channel-receiver view.

It is useful when boundaries must be explicit, payloads must be inspectable, or distributed components must be modular.

RC classification:

```text
valid boundary abstraction
may be native in software substrates
may be scaffold if target relation is actually medium-mediated
```

## M1 — Boundary perturbation

```text
A perturbs B directly through contact, pressure, collision, exchange,
or boundary coupling.
```

The relation is not primarily symbolic. It is a change in boundary condition.

Examples:

```text
physical contact
resource handoff
crowding
blocking
local chemical contact
mechanical pressure
```

## M2 — Trace-mediated coordination

```text
A alters the medium.
The alteration persists.
B later responds to the changed medium.
```

This is the ordinary stigmergic form, but interpreted as changed geometry rather than message storage.

Examples:

```text
pheromone trail
worn path
construction marker
food deposit
queue
road
social record
```

## M3 — Shared-field co-response

```text
A and B respond compatibly because the same medium condition
captures both of their geometries.
```

There is no direct A-to-B message and no necessary persistent trace from A to B.

Examples:

```text
many ants respond to reserve deficit
several agents avoid a congested corridor
workers shift toward repair after boundary damage
plants and fungi respond to shared moisture condition
```

## M4 — Parent-basin modulation

```text
a parent basin changes pressure, cost, reserve, or affordance
across many sub-elements.
```

The parent does not command each element. The parent condition changes the common field.

Examples:

```text
colony hunger
nest alarm
farm drought
forest fire risk
market shortage
institutional crisis
```

## M5 — Resonant alignment

```text
multiple geometries become mutually compatible enough that perturbations
integrate and produce coordinated continuation.
```

This is the relational form closest to the Language of Becoming framing: communication as alignment rather than content transfer.

Examples:

```text
shared practice
trained team coordination
language understanding
swarm entrainment
ritualized social response
stable protocol expectation
```

## M6 — Native shared-medium organization

```text
the substrate itself carries relation through field, trace, pressure,
reserve, event history, geometry, or flux with minimal explicit messaging.
```

This is the RC target for many systems, but it should not be claimed until shown.

---

# 9. Medium-first design procedure

The engineering procedure is simple in outline, but demanding in discipline.

## Step 1 — Name the parent basin

Coordination is rarely only pairwise. Begin by identifying the parent basin that makes the relation meaningful.

Questions:

```text
What larger identity is being preserved?
What common context do the elements share?
What reserve, pressure, cost, or boundary belongs to the parent?
What would count as coordinated continuation for the parent basin?
```

Examples:

```text
ant colony
farm
forest
robot swarm
software service ecology
social institution
cell
tissue
```

## Step 2 — Identify the relation currently described as communication

Write the classical description plainly.

Examples:

```text
ant tells other ants where food is
nest broadcasts hunger
robot sends map update
worker receives task assignment
plant signals stress to neighboring plants
institution announces rule
```

Do not reject the description. Use it as the surface form.

## Step 3 — Ask what medium condition the message might be hiding

For each apparent message, ask:

```text
Is this really a trace?
Is it a pressure?
Is it a cost change?
Is it a reserve condition?
Is it a signature?
Is it parent-basin modulation?
Is it susceptibility capture?
Is it a persistent aftereffect?
Is it resonance through shared practice?
```

## Step 4 — Define the medium surface

A medium surface should specify:

```text
name
scope
carrier
quantity or condition
who/what can perturb it
who/what is susceptible to it
cost of perturbation
persistence / decay
interaction with other surfaces
claim status: target, partial, scaffolded, native
```

A surface may be physical, graph-based, event-history-based, social, material, or producer-scaffolded.

## Step 5 — Define perturbations

For each relation, define what changes in the medium.

Questions:

```text
What activity causes the perturbation?
How large is it?
Where is it located or scoped?
What does it cost?
Does it decay?
Can it be reinforced?
Can it saturate?
Can it conflict with other perturbations?
```

## Step 6 — Define susceptibilities

A perturbation matters only if some geometry can respond to it.

Questions:

```text
Which elements are susceptible?
Under what reserve/cargo/boundary/role condition?
Does susceptibility change with history?
Does parent-basin pressure modulate it?
Can it be inhibited?
Can it be miscaptured?
```

## Step 7 — Define co-response

A shared-medium design should define not only individual response but compatible group response.

Questions:

```text
What should multiple elements do when the same medium condition changes?
Do they converge, diverge, specialize, avoid, reinforce, repair, or split?
Is coordination possible without direct messages?
What observable would show co-response?
```

## Step 8 — Define persistence, decay, and maintenance

Medium memory must not be free unless deliberately simplified.

Questions:

```text
How long does the trace persist?
What reinforces it?
What erases it?
What does maintenance cost?
What happens if too much trace accumulates?
What prevents stale traces from dominating?
```

## Step 9 — Declare direct messages as native or scaffold

If a direct message remains, classify it.

```text
native-to-current-substrate:
    payload transfer is the intended relation at this abstraction level

scaffold:
    payload transfer approximates a target medium effect
```

If scaffold, record medium debt.

## Step 10 — Define controls and withdrawal tests

A shared-medium claim requires controls.

Examples:

```text
remove direct messages
shuffle traces
freeze medium surfaces
remove decay
invert susceptibility
separate parent basins
block a surface
inject false trace
withdraw producer support
compare to message-only baseline
```

Do not claim native shared-medium relation unless behavior persists under appropriate scaffold withdrawal.

---

# 10. Medium surface template

The following template can be used in papers, configs, or future implementation notes.

```text
MediumSurface:
    name:
    parent_basin:
    scope:
    carrier:
    target_RC_meaning:
    quantity_or_condition:
    perturbation_sources:
    susceptible_elements:
    susceptibility_conditions:
    effect_on_continuation:
    cost_of_perturbation:
    persistence:
    decay:
    reinforcement:
    saturation:
    conflicts:
    observable_evidence:
    current_substrate_status:
    producer_or_message_scaffold:
    medium_debt:
    naturalization_condition:
    claim_boundary:
```

Example, conceptually:

```text
MediumSurface:
    name: foodward route support
    parent_basin: ant colony
    scope: nest-food route region
    carrier: route-support aftereffect surface
    target_RC_meaning: repeated successful coupling lowers future foodward continuation cost
    perturbation_sources: unloaded traversal, successful food contact, returning cargo confirmation
    susceptible_elements: low-cargo ants with food-coupling susceptibility
    effect_on_continuation: increases sourceward route affinity / lowers effective movement cost
    cost_of_perturbation: trail deposition and movement reserve
    decay: evaporation / non-reinforcement
    current_substrate_status: scaffolded or partial
    medium_debt: if represented only as direct message or global route label
```

---

# 11. Medium debt ledger

Medium debt should be recorded whenever a direct communication mechanism stands in for shared-medium relation.

| Field | Meaning |
| --- | --- |
| `scaffold_name` | Name of direct message, global variable, or controller mechanism |
| `surface_target` | Intended medium surface or shared-field meaning |
| `why_scaffolded` | Why the current substrate cannot yet carry it natively |
| `affected_claims` | Which claims must be downgraded |
| `withdrawal_test` | What happens when the scaffold is removed or weakened |
| `naturalization_condition` | What would count as substrate-carried relation |
| `status` | scaffolded / partial / native / blocked |

Example:

| Scaffold | Target | Debt |
| --- | --- | --- |
| `broadcast_food_found` | foodward route-support surface plus food signature | High: direct message replaces trail/medium perturbation |
| `global_colony_hunger` | parent-basin reserve pressure | Medium: useful proxy until reserve dynamics modulate susceptibility |
| `task_assignment_message` | role-basin pressure and local demand capture | High: centralized command replaces basin competition |
| `alarm_event_to_all` | boundary-threat pressure field | Medium/high depending on whether alarm surface exists |
| `shared_blackboard_path` | persistent route aftereffect | Medium: may become native if blackboard is treated as medium surface with cost/decay |

Medium debt is parallel to naturalization debt. Naturalization debt concerns producer state. Medium debt concerns relation scaffolds.

Both can coexist.

---

# 12. RC-Ant shared-medium specification

The ant colony is the primary worked example because it contains many forms of relation that are often mistaken for message passing.

The classical description says:

```text
ants communicate with pheromones
ants signal alarm
ants recruit other ants to food
ants divide labor
ants care for brood
ants coordinate construction
```

The RC shared-medium description says:

```text
ants are mobile boundary expressions of a parent colony basin;
they perturb and respond to a shared colony-world medium;
pheromones are durable traces within that medium;
food, nest, brood, waste, alarm, congestion, and reserve conditions
change the common geometry of continuation.
```

## 12.1 The colony field

The colony field is the parent-basin context that makes ant responses mutually relevant.

It includes:

```text
nest reserve
food storage
brood demand
queen/reproduction demand
waste accumulation
threat pressure
route-support traces
home/food signatures
construction tension
crowding/congestion cost
ant local reserves
cargo distribution
trail decay
nest chamber structure
external food basins
```

No single ant needs to hold this as a global map. The colony field is distributed across the medium.

## 12.2 Food recruitment

Classical view:

```text
ant finds food
ant tells other ants
other ants go to food
```

RC shared-medium view:

```text
food basin emits or induces a food-affordance signature;
contact allows support binding;
traversal and successful coupling perturb route-support surfaces;
colony reserve condition modulates food-coupling susceptibility;
low-cargo ants co-respond to the altered route geometry;
repeated coupling deepens the trail until decay or depletion weakens it.
```

Engineering target surfaces:

```text
food signature surface
foodward route-support trace
homeward cargo-confirmation trace
colony reserve pressure
movement cost surface
trail decay surface
```

Direct-message scaffold to avoid unless declared:

```text
send_food_location_to_all_ants
```

If used, record medium debt.

## 12.3 Home return

Classical view:

```text
loaded ant switches to return-home state
```

RC shared-medium view:

```text
bound cargo changes ant susceptibility;
home/nest signature and homeward route support become more salient;
movement cost rises with cargo;
storage basin pressure captures successful return;
route trace is reinforced by completed food-to-nest coupling.
```

This is not a message from nest to ant. It is cargo-modulated susceptibility inside a shared home-affordance field.

## 12.4 Alarm

Classical view:

```text
ant sends alarm signal
nearby ants enter defense mode
```

RC shared-medium view:

```text
boundary threat perturbs alarm-pressure surface;
local route cost and defense susceptibility change;
ant geometries compatible with defense capture co-respond;
alarm traces may persist briefly and decay rapidly;
excess alarm has cost and can disrupt foraging or nursing.
```

Target surfaces:

```text
boundary-threat pressure
alarm trace
local defense susceptibility
avoidance/crowding cost
reserve expenditure for defense
```

## 12.5 Nursery demand

Classical view:

```text
brood requests care
nurse ants respond
```

RC shared-medium view:

```text
nursery basin has support deficit or developmental pressure;
nearby ants with nursing susceptibility are captured by brood-support geometry;
food type, cleanliness, temperature, and reserve alter the pressure;
repeated nursing deepens internal nurse-role susceptibility.
```

Target surfaces:

```text
brood-support demand
nursery cleanliness / waste pressure
protein-support pressure
temperature/humidity support
nursing role susceptibility
```

## 12.6 Waste and cemetery behavior

Classical view:

```text
ants carry waste or dead ants to disposal locations
```

RC shared-medium view:

```text
waste creates harmful-support or entropy pressure;
waste-isolation basin captures compatible carriers;
removal routes become traces;
active colony areas become less susceptible to waste retention;
cemetery/detachment basin stabilizes nonparticipating remnants outside active support circulation.
```

Target surfaces:

```text
waste pressure
contamination cost
waste-isolation route support
cemetery/detachment basin
active-area avoidance surface
```

## 12.7 Construction

Classical view:

```text
builder ants receive or follow construction signals
```

RC shared-medium view:

```text
boundary weakness, congestion, chamber demand, or route cost creates construction tension;
material-carrying ants are susceptible to construction basins;
construction binds support into future geometry;
completed structure changes route cost, chamber capacity, and boundary strength.
```

Target surfaces:

```text
construction tension
material availability
builder susceptibility
boundary repair pressure
route-cost deformation
persistent built geometry
```

## 12.8 Crowding

Classical view:

```text
ants avoid each other using local collision rules
```

RC shared-medium view:

```text
movement density raises local continuation cost;
route geometry deforms;
other paths become more favorable;
crowding can split trails, redirect flow, or trigger construction.
```

Crowding is a medium effect, not merely pairwise avoidance.

## 12.9 Colony hunger

Classical view:

```text
global hunger variable increases foraging probability
```

RC shared-medium view:

```text
nest reserve deficit alters parent-basin pressure;
food-coupling susceptibility increases across relevant mobile expressions;
nonessential costly activity may weaken;
foraging traces become more salient;
food storage coupling deepens.
```

If implemented as a global variable, this is acceptable scaffold, but the target is reserve-pressure modulation.

## 12.10 Division of labor

Classical view:

```text
ants communicate tasks or receive assignments
```

RC shared-medium view:

```text
role basins emerge from repeated capture by medium pressures;
internal susceptibility aftereffects lower re-entry cost;
parent-basin demand modulates availability;
workers specialize without requiring central command.
```

Division of labor is therefore field-mediated differentiation, not only information exchange.

---

# 13. Designing without message-first reflex

When designing an RC ant colony or any other agentic ecology, avoid starting with these questions:

```text
What messages do agents send?
What variables do agents read?
What state transition occurs after receiving a message?
```

Start with these instead:

```text
What parent basin is under pressure?
What medium surface carries that pressure?
What local geometries are susceptible?
What activity perturbs the medium?
What trace persists?
What does it cost?
What decays?
What co-response should appear?
What remains if direct messages are removed?
```

Only after this should direct messages be introduced, and only with their claim status declared.

---

# 14. Evidence and diagnostics

A shared-medium coordination claim should be supported by evidence that relation is carried by the medium, not only by direct payloads.

Useful diagnostics include:

## 14.1 Message removal

Remove direct messages while preserving medium surfaces. If coordination survives, the medium may be carrying relation.

## 14.2 Medium freezing

Freeze trace, cost, pressure, or reserve surfaces. If coordination collapses, the frozen surface was likely functional.

## 14.3 Trace shuffling

Shuffle traces spatially or relationally. If behavior follows the shuffled trace rather than the original source, the trace surface is functional.

## 14.4 Decay manipulation

Change trace decay rates. If coordination changes predictably, persistence/decay is part of relation.

## 14.5 Susceptibility inversion

Invert or neutralize susceptibility. If the same medium perturbation no longer produces the same response, relation depends on geometry compatibility.

## 14.6 Parent-basin separation

Separate agents into different parent-basin contexts while preserving local messages. If coordination weakens, common context matters.

## 14.7 False trace injection

Inject traces without corresponding support. If agents follow them temporarily but the pattern fails to stabilize, the trace is not sufficient without support closure.

## 14.8 Reserve-pressure manipulation

Change reserve pressure without direct messages. If role distribution changes, parent-basin modulation is active.

## 14.9 Scaffold withdrawal

Gradually reduce producer/message scaffolds. If behavior persists through substrate surfaces, naturalization has increased.

## 14.10 Cost accounting

Measure whether traces, movement, signaling, and maintenance consume support. Free relation may indicate hidden scaffold.

---

# 15. Metrics and observables

The following observables can support shared-medium analysis.

| Observable | Meaning |
| --- | --- |
| Co-response strength | Multiple elements respond compatibly to the same medium change |
| Trace dependence | Behavior changes when traces are altered |
| Susceptibility dependence | Only compatible geometries respond to a perturbation |
| Medium persistence | Perturbation remains long enough to shape future activity |
| Decay sensitivity | Behavior depends on trace decay or maintenance |
| Cost sensitivity | Activity changes when perturbation or movement cost changes |
| Reserve-pressure sensitivity | Role distribution changes with support deficit or surplus |
| Parent-basin dependence | Coordination weakens when common context is removed |
| Message independence | Coordination persists without direct messages |
| Scaffold withdrawal survival | Behavior remains after producer/message support is reduced |
| False-trace failure | Unsupported trace attracts but does not stabilize closure |
| Trail closure | Route support deepens only when full basin coupling succeeds |

No single metric proves native shared-medium coordination. The evidence should be comparative and controlled.

---

# 16. Failure modes

Shared-medium systems have their own failure modes.

## 16.1 Stale trace capture

Old traces persist after support conditions change, causing agents to follow obsolete geometry.

Mitigation:

```text
decay
negative reinforcement
support-confirmation coupling
trace competition
```

## 16.2 Medium saturation

Too much trace or pressure makes distinctions collapse.

Mitigation:

```text
costly deposition
saturation limits
decay
local competition
```

## 16.3 False affordance

A medium signature attracts response but does not support closure.

Example:

```text
toxic food with attractive signature
false trail
misleading market signal
stale alarm
```

Mitigation:

```text
confirmation loops
support transfer evidence
negative aftereffect
withdrawal testing
```

## 16.4 Over-coupling

Elements respond too strongly to shared pressure, causing collapse of diversity or congestion.

Mitigation:

```text
susceptibility diversity
cost increase under crowding
role specialization
negative feedback
```

## 16.5 Under-coupling

Medium perturbations fail to capture any local geometry.

Mitigation:

```text
increase signature clarity
lower response cost
deepen susceptibility
improve route conductance
```

## 16.6 Hidden controller

A central controller or producer message creates the appearance of medium coordination.

Mitigation:

```text
medium debt ledger
message removal controls
scaffold withdrawal
claim downgrade
```

## 16.7 Boundary confusion

The designer claims shared medium but has not defined what belongs to the parent basin, what is local, and what relation crosses boundaries.

Mitigation:

```text
explicit parent-basin map
surface scope declarations
claim boundaries
```

---

# 17. General ecology examples

## 17.1 Farm

Classical communication view:

```text
farmer receives irrigation alert
worker gets task assignment
sensor sends soil data
```

Shared-medium view:

```text
soil moisture, crop stress, storage reserve, weather pressure,
path wear, tool availability, and seasonal timing form the farm medium.
Workers and tools co-respond to field pressure when the farm geometry makes
irrigation, harvest, repair, or storage coupling salient.
```

Target surfaces:

```text
soil-water support
crop-growth pressure
storage capacity
path conductance
tool-readiness surface
seasonal signature
compost conversion basin
```

Direct alerts may remain, but they should be classified as messages or scaffolds.

## 17.2 Forest

Classical view:

```text
trees send chemical signals
fungi transfer information
animals respond to cues
```

Shared-medium view:

```text
canopy light, soil moisture, root/fungal coupling, decomposition,
fire risk, seed distribution, and animal movement form a distributed forest medium.
Coordination occurs through shared resource gradients, persistent route/support
networks, and slow aftereffects rather than only direct signals.
```

Target surfaces:

```text
water support
light geometry
mycorrhizal coupling
nutrient reserve
deadwood decomposition
fire pressure
seed-bank persistence
```

## 17.3 Robot swarm

Classical view:

```text
robots broadcast positions and task states
central planner assigns jobs
```

Shared-medium view:

```text
task fields, congestion costs, charging pressure, local map traces,
repair needs, and route affordances coordinate robots.
Direct messages may exist, but the RC target is a shared workspace geometry
that robots perturb and respond to.
```

Target surfaces:

```text
task pressure
battery/charging pressure
route congestion
worksite trace
hazard field
repair demand
coverage aftereffect
```

## 17.4 Society

Classical view:

```text
people exchange messages
institutions announce rules
markets transmit prices
```

Shared-medium view:

```text
infrastructure, law, norms, prices, queues, records, public space,
rituals, institutions, and shared memory form social medium.
Messages matter because they perturb an already structured interpretive and
material geometry.
```

Target surfaces:

```text
normative route support
institutional pressure
market scarcity/surplus
public attention
infrastructure conductance
legal constraint geometry
archive/read-back surface
```

A price is not merely a message. It is also a compressed trace of exchange pressure, scarcity, expectation, and route affordance inside a market basin.

## 17.5 Software service ecology

Classical view:

```text
service A sends event to service B
message queue carries payload
```

Shared-medium view:

```text
queues, logs, shared databases, cache states, load balancers,
backpressure, retries, rate limits, and observability traces form the software medium.
A direct event is valid, but its meaning depends on protocol, schema,
subscriber geometry, timing, and shared operational context.
```

Target surfaces:

```text
backpressure
queue depth
load cost
schema compatibility
failure trace
retry pressure
service health reserve
```

This example shows that direct messages may be native to a computational substrate while still depending on a wider medium.

---

# 18. Substrate-facing implications for LGRC

This document does not define code, but it does shape implementation direction.

A future LGRC-oriented implementation should avoid treating direct message passing as the default coordination primitive when the target phenomenon is shared-medium relation.

Prefer substrate-visible surfaces such as:

```text
node/edge support annotations
route-cost surfaces
packetized flux histories
pending-flux ledgers
event-history traces
local reserve conditions
trail aftereffects
boundary pressure markers
producer-visible demand fields
localized decay and reinforcement dynamics
```

A direct event can still be used. But the design question should be:

```text
Is this event the phenomenon,
or is it a scaffold for a medium perturbation?
```

In early systems, a producer may update or consult explicit surfaces. That is acceptable if declared.

Possible statuses:

```text
target:
    desired RC shared-medium meaning

scaffolded:
    implemented through producer/message/global variable

partial:
    some substrate surface exists, but producer still carries essential relation

native:
    relation is carried by substrate dynamics under appropriate controls

blocked:
    no current mechanism or evidence
```

---

# 19. Design patterns

## 19.1 Trace field instead of broadcast

Instead of broadcasting a discovery to all agents, deposit a trace in the medium.

Use when:

```text
future agents should respond based on location, route, compatibility, and decay
```

Avoid claiming native trace coordination if the trace is only a global flag.

## 19.2 Pressure field instead of task assignment

Instead of assigning tasks directly, deepen a demand basin.

Use when:

```text
multiple agents should self-select based on susceptibility, cost, and proximity
```

## 19.3 Cost surface instead of avoidance messages

Instead of agents warning each other away, raise local continuation cost.

Use when:

```text
congestion, hazard, depletion, or boundary stress should redirect flow
```

## 19.4 Reserve modulation instead of global mode switch

Instead of switching all agents into a new mode, alter parent-basin reserve pressure.

Use when:

```text
colony hunger, low battery, drought, or storage deficit should change behavior distribution
```

## 19.5 Susceptibility diversity instead of fixed roles

Instead of assigning roles by type, allow different geometries to respond differently to the same field.

Use when:

```text
division of labor should emerge through basin capture and history
```

## 19.6 Decay and maintenance instead of permanent memory

Instead of storing permanent marks, require traces to persist only when reinforced.

Use when:

```text
medium memory should remain adaptive
```

## 19.7 Confirmation loop instead of blind trace following

Strengthen traces only when they participate in successful parent-basin closure.

Use when:

```text
false trails or stale affordances are possible
```

---

# 20. Anti-patterns

## 20.1 Message bus disguised as medium

A global message bus is called a field, but agents still receive direct symbolic payloads and update state.

Fix:

```text
classify as direct message passing
record medium debt
introduce surfaces, cost, decay, susceptibility, and trace response if appropriate
```

## 20.2 Global variable disguised as parent basin

A global hunger variable directly changes every ant’s mode.

Fix:

```text
classify as reserve-pressure scaffold
map it to nest reserve, food storage, movement cost, and susceptibility modulation
```

## 20.3 Pheromone as command

Pheromone is implemented as “go here.”

Fix:

```text
represent pheromone as route-support/cost alteration with decay and compatibility
```

## 20.4 No cost for communication

Traces, signals, messages, and field changes are free.

Fix:

```text
account for deposition, maintenance, movement, attention, and reserve costs
```

## 20.5 No decay

Medium memory never fades.

Fix:

```text
define decay, reinforcement, saturation, and stale-trace failure
```

## 20.6 Uniform susceptibility

Every agent responds identically to every trace.

Fix:

```text
make response depend on geometry, reserve, cargo, role-basin susceptibility, history, and parent pressure
```

## 20.7 Coordination without parent basin

Agents coordinate, but the model never defines what larger identity makes their coordination meaningful.

Fix:

```text
define parent basin, support economy, persistence criteria, and claim boundary
```

---

# 21. Claim ladder

Shared-medium coordination claims should be stated with maturity levels.

```text
S0 — Vocabulary
    Communication concepts are named in shared-medium terms.

S1 — Conceptual mapping
    Messages, signals, broadcasts, traces, and coordination events are mapped
    to surfaces, perturbations, susceptibilities, and co-response.

S2 — Scaffolded demonstration
    Producers or direct messages approximate medium behavior, with medium debt declared.

S3 — Surface-mediated behavior
    Agents respond to explicit substrate surfaces such as traces, costs, pressures,
    and reserves, though producers may still maintain them.

S4 — Controlled shared-medium evidence
    Coordination persists under message removal and changes under medium controls.

S5 — Partial naturalization
    Some relation mechanisms are carried by substrate event history, flux, traces,
    support, or geometry with reduced producer/message scaffolding.

S6 — Native shared-medium coordination
    Core coordination is substrate-carried with minimal or no explicit relation scaffold.

S7 — Hierarchical native medium
    Parent-basin modulation and subbasin coordination are native across scales.
```

Most early RC-Agentic-Ecology work should claim S0-S3. Stronger claims require controls.

---

# 22. Checklist for new systems

Before adding a communication mechanism to an RC-Agentic-Ecology design, answer:

```text
1. What parent basin makes this relation meaningful?
2. What medium surface could carry the relation?
3. What perturbation changes that surface?
4. What does the perturbation cost?
5. What elements are susceptible to it?
6. What changes in continuation when they respond?
7. Does the perturbation persist?
8. How does it decay or get reinforced?
9. Could co-response occur without direct messages?
10. If a message remains, is it native or scaffold?
11. What medium debt is introduced?
12. What control would test the medium claim?
13. What would count as naturalization?
```

This checklist should be used before implementation, not after.

---

# 23. Minimal vocabulary for implementation notes

Future implementation documents should use the following labels consistently.

```text
medium_surface:
    a substrate or scaffold surface that carries shared relation

perturbation:
    a change to a medium surface caused by activity

susceptibility:
    compatibility of local geometry with a medium condition

co_response:
    coordinated behavior caused by shared medium condition

trace:
    persistent medium aftereffect

pressure:
    parent-basin or local-basin condition that changes continuation likelihood

resonance:
    successful integration of perturbation by compatible geometry

message_scaffold:
    explicit payload/channel used where shared-medium relation is target

medium_debt:
    declared debt introduced by message scaffold or global relation proxy

naturalization_condition:
    requirement for moving scaffolded relation into substrate-carried geometry
```

---

# 24. Relation to producer residue

Producer residue and medium debt are related but distinct.

```text
producer residue:
    explicit state or policy used to make an agentic element act
    before the substrate carries that mechanism natively

medium debt:
    explicit message, broadcast, global variable, or channel used to make
    relation happen before the medium carries that relation natively
```

Example:

```text
ant.mode = returning
    producer residue
    target: cargo-shaped home susceptibility

broadcast_food_found(food_id)
    medium debt
    target: food signature + route-support trace + reserve-pressure modulation
```

Both should be declared in the same system documentation.

A mature RC ecology reduces both.

---

# 25. Closing definition

Shared-Medium Coordination can be defined as follows:

> Shared-Medium Coordination is the RC-Agentic-Ecology engineering discipline in which relation is designed first as perturbation and response within a common coherence medium — through trace, pressure, cost, reserve, signature, susceptibility, co-response, resonance, and parent-basin modulation — while direct messages are treated as valid substrate abstractions or declared scaffolds rather than as the default ontology of communication.

The practical rule is:

```text
message passing is allowed,
but it must be classified.

If the message is the intended substrate relation, say so.
If the message stands in for a field, trace, pressure, or co-response,
record medium debt.
```

For ants, this means pheromone is not merely a message. It is one durable physical trace of a broader colony-world medium.

For farms, forests, swarms, societies, cells, and software ecologies, the same principle applies:

```text
design the medium first;
then decide which messages, if any, are still needed.
```

---

# References and source context

- Uroš Jovanovič, *The Language of Becoming: A Reflexive Coherence Framework for Understanding Intelligence, Identity, and Communication as Geometric Phenomena*, `geometric-reflexive-coherence/arc-of-becoming/2026-01-LanguageOfBecoming.md`.
- Uroš Jovanovič, `reflexive-coherence-agentic-ecology`, project repository for RC-Agentic-Ecology transition essays and specifications.
- Uroš Jovanovič, `geometric-reflexive-coherence`, core Reflexive Coherence theory, essays, substrates, and Arc of Becoming material.
- Uroš Jovanovič, `graph-reflexive-coherence`, graph/LGRC implementation and evidence workspace.
