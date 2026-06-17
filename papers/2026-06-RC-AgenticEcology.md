# RC Agentic Ecology

## A specification draft for translating state-rule agents into Reflexive Coherence systems, with RC-Ant Colony as the worked example

**Draft status:** conceptual specification, no implementation claims.
**Intended role:** educational blueprint for designing agentic ecologies through geometry, flux, coherence reserve, basin hierarchy, and producer-naturalization discipline.

Copyright © 2026 Uroš Jovanovič, CC BY-SA 4.0.

---

## Abstract

Classical agent models begin with entities that hold state, receive inputs, apply rules, and emit actions. This is useful for programming behavior, but it places agency inside discrete control variables and treats the world as an external stage. Reflexive Coherence asks for a different starting point. In RC, the primitive is not an agent with state, but a coherence field whose state defines geometry, whose geometry shapes flux, and whose flux updates the field again. In the repository’s shortest formulation, this loop is written as `C -> K[C] -> g[K] -> J[C,g] -> continuity -> C`; identity is a stable basin of the field, memory is persistent geometry, and agency is not an external controller. ([GitHub][1])

This paper proposes a general translation method from classical I/O state-rule agents into **RC agentic ecologies**. The central rule is simple: every apparent agent state should first be interpreted as geometry — basin structure, boundary condition, support distribution, flux affordance, coupling surface, aftereffect, signature, or persistence pressure. Only what cannot yet be carried by the RC/LGRC substrate should remain as explicit producer state. Every remaining producer-state variable is therefore a **naturalization debt**.

The worked example is an ant colony. In a classical model, ants are agents with modes such as foraging, returning, defending, nursing, building, or carrying waste. In RC-Ant, those modes are not primitive states. The colony is a higher-order basin. The nest, nursery, food storage, queen chamber, fungus garden, waste chamber, cemetery, guard boundary, trails, and mobile ants are subbasins or boundary expressions within the colony geometry. Food is an external support basin. Pheromone is a route-support aftereffect. Cargo is bound coherence. Movement is coherence-costly continuation. Reproduction is a surplus-supported split. Division of labor is not a table of task labels; it is the durable differentiation of role basins inside the parent colony basin.

The purpose of this specification is not to claim that LGRC already implements all of this natively. The graph repository currently treats LGRC9V3 as an active event-driven substrate for packetized coherence transport, delayed handoff, local proper-time evidence, route choice, memory/trail affordance, goal-proxy regulation, and bounded agentic-like integration; it also explicitly distinguishes producer-assisted evidence from fully native coherence-loop evidence. ([GitHub][2]) The purpose here is to define the target ontology and the engineering method: how to move from stateful agents toward basin ecologies, how to name the remaining scaffolding, and how to refine parent identities into specialized subbasins through the Arc of Becoming.

---

# 1. Motivation

Most agent systems are written in the following form:

```text
agent has state
agent reads input
agent evaluates rule or policy
agent emits action
agent updates memory
agent pursues goal
```

This form is practical. It is also misleading when used as an ontology.

It makes “state” appear to be inside the agent. It makes “input” appear to come from outside. It makes “decision” appear to be a discrete internal event. It makes “memory” appear to be a separate store. It makes “goal” appear to be a symbol held by the agent. It then asks how many such agents can be connected until collective behavior appears.

Reflexive Coherence invites a different question:

```text
What geometry must exist for this behavior to be a natural continuation?
```

The agent is not first an object with variables. The agent is a localized coherence geometry. Its behavior is the expression of basins, boundaries, support, flux, aftereffects, and coupling surfaces. The world is not passive. The world is also geometry, also support, also memory, also pressure. The apparent “agent” is one mobile locus of a larger ecology.

This matters for engineering because it changes how complex systems are built. Instead of assembling random parts and hoping some configuration survives, RC engineering begins with a parent identity basin, defines its persistence conditions, and then refines it into subbasins that survive within the parent substrate.

The ant colony is a useful example because it forces the issue. A simple ant model can be implemented as a collection of state machines. But a living colony is not merely a swarm of state machines. It is a hierarchical coherence economy: a parent colony basin with mobile boundary expressions, specialized nest regions, food couplings, trail memory, task differentiation, defense, waste isolation, reproduction, and construction.

The aim of RC-Ant is therefore not to simulate ants first. The aim is to learn how ordinary agent-state language can be translated into RC geometry.

---

# 2. The core inversion

The classical view begins with the agent.

```text
agent -> state -> input -> decision -> action -> world update
```

The RC view begins with the coherence ecology.

```text
coherence -> geometry -> flux -> aftereffect -> continuation -> coherence
```

The agent is not removed. It is reinterpreted.

An agent becomes a localized identity expression inside a support-defined world. Its state is not a hidden variable first. Its state is the current condition of its geometry. Its action is not an output command first. Its action is a coherence-costly transformation of coupling, flux, support, or world geometry.

The translation can be stated as follows:

| Classical agent concept | RC translation                                                                                                     |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Agent                   | Localized identity geometry or mobile boundary expression                                                          |
| Internal state          | Current basin condition, boundary condition, support distribution, or basin capture                                |
| Input                   | Local affordance contact, signature contact, flux condition, or aftereffect contact                                |
| Decision                | Collapse or continuation among compatible basin couplings                                                          |
| Action                  | Coherence-costly flux, support transfer, trace deposition, boundary repair, construction, or geometry modification |
| Memory                  | Persistent geometry or lowered re-entry cost                                                                       |
| Goal                    | Basin persistence, closure, repair, surplus, or reproduction pressure                                              |
| Reward                  | Support reinforcement, basin deepening, or reduced future continuation cost                                        |
| Skill                   | Repeated coupling that lowers future entry or action cost                                                          |
| Communication           | Shared field/trace/affordance modification                                                                         |
| Coordination            | Coupled basin dynamics through shared geometry                                                                     |
| Environment             | Active nested basin ecology                                                                                        |
| Failure                 | Loss of closure, support depletion, destructive leakage, or collapse into incompatible basin                       |

The important statement is not that agent state can be “represented differently.” The stronger statement is:

> In an RC translation, state is not primitive. State is geometry unless the current substrate cannot yet carry it.

---

# 3. The Producer Residue Principle

A practical implementation may not yet be able to place every part of agentic behavior into the substrate. This is especially true in early LGRC work, where producer layers may inspect substrate state and schedule events that the substrate does not yet produce natively.

This is allowed, but it must be named correctly.

> **Producer Residue Principle.** In an RC translation, explicit producer state is not part of the target ontology. It is residual scaffolding for mechanisms that have not yet been naturalized into basin geometry, flux, support, coupling, aftereffect, event history, or coherence reserve. Each explicit producer-state variable must be declared, mapped to its intended RC meaning, and treated as naturalization debt.

This principle prevents a common error. One might define an ant as having:

```text
mode = foraging
mode = returning
mode = defending
mode = nursing
```

and then say that the RC ant has a “portfolio of states.” That is not sufficient. It preserves the state-machine ontology under new names.

The RC target should say instead:

```text
the ant is a localized mobile geometry
with basin susceptibilities, boundaries, coupling surfaces,
bound support, emitted traces, and aftereffects
```

If the current implementation requires `mode = foraging`, that variable belongs to the producer scaffold. It is not the RC explanation. It is a proxy for food-basin susceptibility, route affordance, cargo condition, and colony demand that have not yet been fully naturalized.

A useful implementation ledger would therefore contain:

| Producer variable   | Intended RC meaning                        | Current status        | Naturalization debt                                              |
| ------------------- | ------------------------------------------ | --------------------- | ---------------------------------------------------------------- |
| `mode_proxy`        | Active basin capture or dominant coupling  | scaffolded            | Replace with substrate-carried basin competition                 |
| `cargo_proxy`       | Bound support carried by mobile geometry   | scaffolded or partial | Replace with conserved support packet or local coherence binding |
| `path_memory_proxy` | Route-support aftereffect                  | scaffolded or partial | Replace with persistent geometry/trail field                     |
| `task_proxy`        | Role-basin susceptibility and local demand | scaffolded            | Replace with demand/support geometry                             |
| `energy_proxy`      | Accessible coherence reserve               | scaffolded or partial | Replace with local reserve/fuel accounting                       |
| `reproduce_proxy`   | Surplus-supported split                    | scaffolded            | Replace with substrate-supported identity refinement             |

The goal is not to ban scaffolding. The goal is to prevent scaffolding from being mistaken for naturalized RC structure.

---

# 4. Coherence as reserve, fuel, and cost

A basin is not only a shape. It is also a reserve.

Coherence behaves, in this engineering vocabulary, in two complementary ways:

```text
mass-like:
    it gives a basin depth, inertia, persistence, resistance to perturbation

energy-like:
    it can be mobilized to fund motion, signaling, construction,
    repair, trace formation, defense, reproduction, or transformation
```

This is an analogy inside the RC engineering frame, not a claim that coherence is identical to physical mass or physical energy. The point is that coherence is not merely descriptive. It is also available support.

A basin therefore has:

```text
stored coherence
accessible coherence
bound coherence
free coherence
surplus coherence
spent coherence
leaked coherence
```

This changes how agentic systems are described.

Movement is no longer free. It is paid continuation.

```text
movement = coherence-costly continuation across geometry
```

Consumption is no longer deleting a resource object. It is support transfer and transformation.

```text
food basin support
    -> bound cargo
    -> movement cost
    -> nest reserve
    -> brood growth
    -> trail deposition
    -> construction
    -> reproduction
    -> waste or leakage
```

Memory is no longer free either. A pheromone trail or persistent route aftereffect requires deposition, reinforcement, or maintenance. If not maintained, it decays. If overproduced, it can drain the colony. This matters because it prevents “information” from floating outside the coherence economy.

A general rule follows:

> An RC agentic element can only continue where it can pay the local cost of continuation, or where another basin subsidizes that continuation.

For an ant, this means:

```text
empty ant:
    lower cargo cost, higher exploratory range

loaded ant:
    higher movement cost, stronger home coupling

starved ant:
    reduced continuation range, stronger food susceptibility

trail-supported route:
    lower effective continuation cost

hostile terrain:
    higher continuation cost

nest-supported corridor:
    subsidized movement
```

The same principle applies to farms, forests, societies, and swarms. Any active ecology must account for the cost of activity.

---

# 5. Reproduction and split

A dynamic colony must be able to produce new structure.

In a state-machine model, reproduction often appears as a threshold rule:

```text
if resource > threshold:
    spawn new agent
```

In RC, reproduction should be interpreted more carefully.

> **Reproduction is a surplus-supported split of coherent structure into a new identity or subidentity, while preserving the parent basin’s closure.**

This definition has several consequences.

First, reproduction requires surplus. A basin cannot split viable new identity if all available support is required for maintenance and repair.

Second, reproduction requires structure, not merely quantity. A surplus that cannot be organized into a stable subbasin is not yet reproductive.

Third, reproduction must preserve parent closure. If the parent destroys itself by splitting, the event may be collapse, leakage, fragmentation, or sacrifice, but not stable reproduction in the engineering sense.

Fourth, reproduction is not only biological. It includes several related forms of coherent differentiation:

| Event                 | RC interpretation                                                                   |
| --------------------- | ----------------------------------------------------------------------------------- |
| New ant               | A colony/nest/nursery basin allocates support into a new mobile boundary expression |
| New role              | Repeated activity stabilizes a specialized role basin                               |
| New chamber           | Nest surplus stabilizes a new internal subbasin                                     |
| New trail             | Repeated successful coupling stabilizes route-support geometry                      |
| New tool or structure | Coherence is bound into a persistent affordance surface                             |
| New colony            | Colony-level surplus supports a daughter colony identity basin                      |

The general form is:

```text
surplus + tension + repeated function + preserved parent closure
    -> split / refinement / new subbasin
```

This is where spark-split RC becomes an engineering method. A spark is not merely random novelty. In this context, it is a refinement event: a parent basin becomes too coarse, and tension, surplus, repeated activity, or missing closure reveals a site where new substructure can stabilize.

---

# 6. Hierarchical basins as engineering method

Hierarchical basins are especially important because they allow top-down coherence constraints and bottom-up viability to meet.

Ordinary bottom-up assembly asks:

```text
Can these parts interact until a viable whole appears?
```

Hierarchical basin engineering asks:

```text
What parent identity must persist?
What reserves, boundaries, costs, and couplings does it require?
What subbasins can specialize inside it without destroying it?
```

The parent basin is an engineering envelope. It defines what counts as persistence, what may be spent, what must be conserved, what may split, what must be repaired, what kinds of flows are allowed, and what forms of specialization are admissible.

A subbasin is not an arbitrary module. It is a refinement that survives within the parent geometry.

This is the key engineering transition:

```text
not:
    assemble random parts and hope they survive

but:
    define a parent basin
    define its persistence conditions
    refine it into subbasins
    test whether each subbasin survives within the parent closure
```

The repository’s core overview describes Fractal Reflexive Coherence as adding scale so identity can propagate through nested sub-identities rather than being trapped at one scale. ([GitHub][1]) The present specification does not claim a full FRC implementation. It uses a hierarchical basin definition as an engineering discipline compatible with that direction.

A cell can be defined this way.

```text
cell parent basin
    boundary / membrane subbasin
    reserve / metabolism subbasin
    repair subbasin
    reproduction subbasin
    sensing / coupling subbasin
    waste / export subbasin
```

The cell is not assembled from arbitrary parts first. The cell identity is specified as a basin, and its parts are introduced as refinements required by that identity’s persistence.

The ant colony can be defined the same way.

```text
colony parent basin
    nest basin
    mobile ant geometries
    food-coupling structures
    nursery basin
    storage basin
    defense basin
    waste basin
    trail basin
    reproduction basin
```

The parent colony basin defines the broader behavior. The subbasins are specialized structures that survive within and contribute to the parent.

---

# 7. Arc of Becoming as engineering discipline

The Arc of Becoming provides the methodological discipline for this kind of engineering. The arc is described as moving from vocabulary to method — language, reinforcement, classification, interrogation, naturalization, and cultivation — and asks how an embedded observer should understand and participate in becoming when the next meaningful class cannot be fully known in advance. ([GitHub][3])

For RC engineering, the arc becomes:

```text
Language:
    name the parent basin, boundaries, reserves, costs, couplings,
    affordances, aftereffects, splits, and subbasins

Classification:
    observe what the system actually expresses before forcing it
    into a predicted endpoint

Interrogation:
    apply bounded probes that ask what support, boundary,
    missing relation, or reserve makes a property possible

Naturalization:
    ask whether a behavior first produced under scaffolded support
    can become substrate-carried

Cultivation:
    refine, withdraw scaffolding where possible, integrate stable
    subbasins, and preserve the geometry of becoming
```

This is not a loose analogy. It gives a precise workflow for moving from state-rule systems to RC ecologies.

A designer begins with a coarse parent identity. The designer then classifies what the parent must express: intake, storage, movement, repair, reproduction, defense, waste handling, communication, specialization, and construction. Where expression fails, the designer interrogates. Is support missing? Is a boundary missing? Is a route too costly? Is memory not persistent? Is a producer variable hiding a geometry that should be naturalized? The answer suggests a split or refinement. A new subbasin is introduced. It is then cultivated until it either survives as part of the parent basin or is withdrawn.

The result is guided assembly under increasingly detailed conditions. It is not arbitrary bottom-up accumulation. It is also not rigid top-down programming. It is identity-first refinement through geometry.

---

# 8. Universal RC mapping rule

The universal rule can now be stated in full:

> **RC Naturalization Rule.** For any agentic ecology, every apparent agent state, rule, memory, goal, action, resource, cost, role, or communication channel must first be attempted as RC geometry: basin, boundary, support, flux, coupling, aftereffect, signature, affordance, reserve, or persistence condition. Only what cannot yet be carried by the substrate may remain as explicit producer state, and every such variable is naturalization debt.

This rule generalizes beyond ants.

It applies to farms, forests, societies, cells, robot swarms, institutions, markets, software agents, and artificial ecosystems. The mapping does not require that all native mechanisms already exist. It requires honest separation between target ontology, substrate mapping, and producer residue.

The three layers are:

```text
1. RC target ontology
   What the system should be in RC terms.

2. LGRC or substrate mapping
   Which parts can already be represented as support, flux, packets,
   traces, delays, event histories, route affordances, basin attributes,
   reserves, or topology.

3. Producer scaffold
   Temporary explicit state or policy needed because the substrate
   does not yet carry the mechanism natively.
```

The educational value of this rule is that it gives a repeatable question:

```text
Is this variable real in the RC world,
or is it an implementation residue?
```

---

# 9. RC agentic element

A classical agent might be written abstractly as:

```text
A = state + input + policy + action + memory + reward
```

The RC target should not be written as another tuple of hidden states. The better formulation is:

```text
A_RC = localized coherence geometry
```

This geometry includes:

```text
identity support:
    what lets this element remain itself across local change

boundary structure:
    what separates, filters, couples, or protects it

basin susceptibilities:
    what larger or local basins can capture its activity

coupling surfaces:
    where it can exchange support, signals, cargo, damage, or structure

coherence reserve:
    what it can spend to continue, move, repair, signal, or reproduce

bound support:
    cargo, body, internal reserve, attached material, or committed structure

aftereffect profile:
    persistent changes left by prior activity, internally or externally

emission profile:
    traces, signatures, perturbations, or support changes it leaves in the world

continuation landscape:
    the local geometry of possible next couplings
```

No item in this list is an internal finite state in the usual sense. Together they are the current geometry of the element.

A producer implementation may still need variables. But in the specification, the variables are not the agent. They are scaffolds for parts of the geometry not yet native.

---

# 10. RC ecology

An RC ecology is a set of nested and interacting coherence geometries.

It contains:

```text
parent basins
subbasins
mobile boundary expressions
resource basins
threat basins
repair basins
waste basins
reproduction basins
aftereffect fields
signature fields
coupling routes
cost surfaces
support reserves
surplus conditions
```

The ecology is not a container holding agents. The ecology is the active geometry in which agentic elements appear as local expressions.

A useful minimum definition is:

> An RC agentic ecology is a coherence economy in which identity basins maintain themselves through costly coupling, support transfer, boundary repair, trace formation, specialization, and surplus-supported refinement.

This definition includes agency, but it does not reduce agency to choice. The essays directory frames the interpretive extension around abundance, agency, persistence, sentience, and read-back; its agency summary specifically describes agency as persistence capacity of an identity basin across perturbation, withdrawal, substrate change, and proxy pressure, rather than merely choice. ([GitHub][4])

That is the standard used here. An ant colony is agentic not because each ant contains a symbolic chooser, but because the colony basin persists through uncertain, costly, distributed coupling.

---

# 11. RC-Ant Colony: central definition

An **RC-Ant Colony** is a hierarchical coherence-basin ecology in which a colony basin accumulates and spends support through nested subbasins, mobile boundary expressions, route aftereffects, and external resource couplings.

Ants are mobile geometries funded by colony and local reserves. Food is an external support basin. The nest is the colony’s internal support architecture. Pheromone is costly world-written route memory. Cargo is bound coherence. Movement is paid continuation. Specialization is persistent role-basin susceptibility. Reproduction is surplus-supported split. Division of labor is basin differentiation inside the parent colony identity.

Shorter:

> RC-Ant is not a swarm of agents in a world. It is a coherence economy in which a colony basin funds, shapes, and reproduces mobile boundary expressions to couple external support into its own hierarchical geometry.

---

# 12. The colony as parent basin

The colony is the highest active identity in the basic RC-Ant model.

It is not the sum of ants. It is the parent basin within which ants, nest chambers, trails, roles, and resource relations gain meaning.

```text
colony basin
    nest basin
        nursery basin
        food storage basin
        queen / reproduction basin
        fungus garden / cultivation basin
        waste basin
        cemetery / detachment basin
        guard entrance / boundary basin
        tunnel / conductance geometry
        construction / repair basin

    mobile boundary expressions
        scouts
        foragers
        carriers
        nurses
        builders
        guards
        waste removers
        cultivators

    external coupled basins
        food
        water
        prey
        seeds
        leaves
        fungus substrate
        threat
        obstacle
        toxic source
        shelter

    aftereffect structures
        foodward trails
        homeward trails
        alarm traces
        construction traces
        waste-isolation routes
        cemetery routes
        cultivation access traces
```

The colony parent basin defines:

```text
what support must be acquired
what support must be stored
what support may be spent
what boundaries must be defended
what waste must be isolated
what brood must be sustained
what routes must be maintained
what subbasins may split
what counts as surplus
what counts as collapse
```

This is why hierarchical basins matter for engineering. Once the parent basin is defined, specialized subbasins can be introduced as refinements. They are not arbitrary modules. They are structures that survive because they contribute to colony closure.

---

# 13. Nest as internal basin architecture

In a simple ant model, the nest is “home.”

In RC-Ant, the nest is not a single node. It is the colony’s internal support architecture.

The nest may contain:

| Nest structure    | RC meaning                                                                                   |
| ----------------- | -------------------------------------------------------------------------------------------- |
| Nursery           | Brood-support basin; attracts nursing, feeding, cleaning, and protection couplings           |
| Food storage      | Retained support basin; converts incoming cargo into accessible colony reserve               |
| Queen chamber     | Reproduction-continuity basin; stabilizes colony lineage and worker production               |
| Fungus garden     | Cultivation/conversion basin; turns gathered substrate into delayed support                  |
| Waste chamber     | Entropy-isolation basin; receives harmful residue and prevents leakage into active support   |
| Cemetery          | Detachment basin; routes dead or nonparticipating remnants out of active colony circulation  |
| Guard entrance    | Boundary-threat/filter basin; modulates outside-inside coupling                              |
| Tunnel network    | Conductance geometry; shapes movement cost, delay, congestion, and route support             |
| Construction site | Geometry-expansion or repair basin; consumes material and reserve to alter future affordance |

The nest is therefore both a basin and a basin system. It is a place of return, but more importantly it is the internal differentiation of the colony’s persistence.

---

# 14. Food as external support basin

Food is not merely a target.

Food has at least two aspects:

```text
resource role:
    food is a basin of consumable support

signature role:
    food may emit, leak, or induce an affordance field
```

This resolves the ambiguity between food as well and food as radiant source.

Materially, food is a well. Flux or support can flow into the ant from it. It can be depleted, bound, carried, transformed, or stored.

Operationally, food may be radiant. It may produce a signature that lets an empty ant move sourceward, perhaps by going against an emitted gradient.

The ant does not “know food” as a symbolic object. Its current geometry becomes susceptible to food-affordance structure when its reserve, cargo, role-basin capture, and local context make food coupling salient.

Different food types are different basin couplings.

| Food type          | RC interpretation                                                      |
| ------------------ | ---------------------------------------------------------------------- |
| Sugar              | Fast accessible support; funds movement and immediate activity         |
| Protein / prey     | Brood or queen support; slower developmental coupling                  |
| Seeds / grain      | Storage-compatible support basin                                       |
| Leaves / substrate | Cultivation input, not direct nutrition                                |
| Fungus             | Converted support produced inside cultivation basin                    |
| Water              | Transport, cooling, survival, and cultivation support                  |
| Toxic food         | False or harmful basin; attractive signature but destabilizing support |
| Dead insect        | Food basin plus contamination or waste coupling                        |

Thus “found food” is too coarse. The real question is:

```text
Which colony subbasin can this external support couple into,
at what cost, with what conversion, leakage, or risk?
```

---

# 15. Ant as mobile boundary expression

An ant is not primarily an object with a task state.

An ant is a mobile boundary expression of the colony basin.

It has local identity support, boundary structure, movement cost, reserve, coupling surfaces, susceptibility to food/home/trail/threat/nursery/construction fields, and the capacity to bind or release support.

A classical ant might be described as:

```text
if not carrying food:
    seek food
else:
    return home
```

The RC description is:

```text
low cargo and sufficient reserve
    -> food-coupling geometry becomes more salient

bound cargo
    -> home/nest coupling geometry becomes more salient

trail aftereffect
    -> lowers continuation cost for compatible movement

local threat
    -> may capture the ant into defense or alarm basin

brood contact
    -> may capture the ant into nursing basin

waste contact
    -> may capture the ant into isolation/removal basin
```

The ant does not switch states first. Its geometry changes which basins can capture it.

The words “forager,” “nurse,” “builder,” and “guard” remain useful, but they are descriptions of basin capture or specialization. They are not primitive internal labels.

---

# 16. Cargo as bound coherence

Cargo is not inventory first. It is bound support.

When an ant contacts a food basin, some support may become bound to the ant’s mobile geometry. That support changes the ant’s cost, susceptibility, and continuation landscape.

```text
unloaded ant:
    low cargo cost
    higher food susceptibility
    higher exploratory mobility

loaded ant:
    higher movement cost
    higher home susceptibility
    stronger pressure toward nest/storage coupling
```

Cargo may also be typed. Sugar cargo, protein cargo, waste cargo, brood cargo, construction material, and fungus substrate do not couple to the same nest subbasin.

Cargo therefore participates in task differentiation without requiring symbolic task state.

```text
protein cargo:
    nursery and queen support basins become salient

waste cargo:
    waste-isolation routes become salient

construction material:
    repair/construction basins become salient

fungus substrate:
    cultivation basin becomes salient
```

This gives richer behavior through geometry.

---

# 17. Pheromone as route-support aftereffect

Pheromone is not a command.

It is not “go here.”

In RC-Ant, pheromone is a persistent route-support aftereffect. It is the world retaining the history of prior passage or successful coupling in a way that alters future continuation cost, conductance, or affordance salience.

```text
pheromone = world-written memory of colony coupling
```

A trail is therefore not merely a path. It is an extended aftereffect that says:

```text
this continuation has participated in support transfer,
defense, construction, waste isolation, or another colony function
```

Pheromone should not be a single scalar unless the model is deliberately simplified. Different traces may be phase-sensitive:

| Trace type           | Salient for                                 |
| -------------------- | ------------------------------------------- |
| Foodward trail       | Empty foraging-susceptible ants             |
| Homeward trail       | Loaded home-susceptible ants                |
| Alarm trace          | Defense-susceptible ants                    |
| Construction trace   | Builder-susceptible ants                    |
| Waste route trace    | Waste carriers and avoidance dynamics       |
| Cemetery route trace | Detachment/removal behavior                 |
| Cultivation trace    | Substrate carriers and fungus-care behavior |

The same trace may have different effects depending on the ant’s current geometry. This is important. It lets the model coordinate without symbolic messages.

Pheromone also has cost. Deposition spends support. Maintenance requires reinforcement. Evaporation is loss of persistence. Overproduction can drain the colony.

---

# 18. Division of labor as basin differentiation

Division of labor should not be modeled first as fixed ant types.

It should be modeled as a stable differentiation of role basins inside the colony parent basin.

A role basin forms when repeated coupling, local demand, body geometry, age, support condition, and nest position make some continuation easier to re-enter.

```text
specialization =
    repeated role-basin occupation
    leaves an internal aftereffect
    lowering future entry cost into that role
```

This unifies several phenomena:

| Phenomenon                   | RC interpretation                                  |
| ---------------------------- | -------------------------------------------------- |
| Pheromone trail              | External route aftereffect                         |
| Worker specialization        | Internal role aftereffect                          |
| Nest chamber differentiation | Spatial subbasin aftereffect                       |
| Colony labor profile         | Parent-basin distribution of role susceptibilities |
| Skill                        | Reduced cost of future coupling                    |
| Habit                        | Stable re-entry into a basin                       |
| Caste-like behavior          | Deepened or constrained role-basin geometry        |

A forager is an ant captured by foraging basins often enough that foraging becomes easier to re-enter.

A nurse is an ant whose geometry is easily captured by brood-support basins.

A guard is an ant whose boundary-threat coupling dominates near entrances.

A builder is an ant whose material-coupling and construction-basin susceptibility are deepened.

This allows both flexible task switching and durable specialization.

---

# 19. Defense, waste, cemetery, and negative basins

A proper ecology must include destabilizing and isolating structures.

Not all basins are desirable attractors. Some are harmful. Some are necessary sinks. Some are quarantine structures.

| Structure        | RC role                                                       |
| ---------------- | ------------------------------------------------------------- |
| Threat basin     | Destabilizing external pressure; may capture defense behavior |
| Alarm trace      | Rapid route-support alteration under boundary threat          |
| Waste basin      | Entropy-isolation structure; prevents harmful recirculation   |
| Cemetery basin   | Detachment structure for dead support/remnants                |
| Toxic food basin | False affordance plus damaging support transfer               |
| Disease basin    | Self-reinforcing destabilizing geometry                       |
| Obstacle         | High-cost or blocked continuation geometry                    |

Waste handling is especially important because it shows that an ecology is not only about intake. Persistence also requires isolation, removal, leakage control, and boundary repair.

In RC-Ant, waste carriers are not agents with `task = waste`. They are mobile geometries captured by waste-isolation basins because of contact, local demand, route traces, and support conditions.

---

# 20. Construction and nest growth

Construction is support bound into future geometry.

When ants build, they spend coherence and material to alter movement cost, boundary strength, chamber capacity, route conductance, or basin separation.

```text
construction =
    costly transformation of current support
    into persistent future affordance geometry
```

A tunnel is not just a passage. It is conductance geometry.

A wall is not just matter. It is boundary reinforcement.

A chamber is not just space. It is a subbasin whose shape allows a function to persist.

A bridge or cleared path is not just convenience. It lowers future continuation cost.

Construction is therefore a central example of the RC loop: the colony’s current coherence modifies geometry, and the modified geometry shapes future flux.

---

# 21. Reproduction in RC-Ant

Reproduction appears at several levels.

## 21.1 New mobile ant

A new ant is a mobile boundary expression split from colony reserve through queen/nursery/reproduction structure.

It requires:

```text
surplus colony support
brood-support subbasin
developmental delay
boundary formation
reserve allocation
integration into colony traces and role susceptibilities
```

If implemented with a producer, `spawn_ant` is a proxy. The RC target is surplus-supported formation of a new mobile identity geometry.

## 21.2 New role

A new role can appear when repeated demand and activity stabilize a new role basin.

For example, if fungus cultivation becomes important, a generic carrier role may split into:

```text
substrate gatherer
fungus garden maintainer
waste remover
humidity/water carrier
```

This is not reproduction of biological bodies, but it is reproduction of functional identity.

## 21.3 New chamber

A chamber splits from nest geometry when colony surplus and repeated activity justify internal differentiation.

```text
food pile
    -> storage basin
    -> specialized storage chamber
    -> route traces and worker susceptibility around storage
```

## 21.4 New colony

A daughter colony requires surplus at the parent scale. It is not merely a new nest location. It is a new parent basin that can maintain closure, boundaries, resource coupling, reproduction, and role differentiation.

---

# 22. RC-Ant engineering workflow

The ant colony can now be designed through hierarchical basin engineering.

## Step 1 — Define the parent basin

```text
parent identity:
    colony

persistence requirements:
    acquire support
    store support
    fund movement
    maintain nest boundary
    care for brood
    reproduce mobile expressions
    remove waste
    defend boundary
    maintain route memory
    repair and expand geometry
```

## Step 2 — Define coherence economy

```text
reserves:
    nest reserve
    food storage
    ant local reserve
    bound cargo
    brood investment
    trail investment
    construction investment

costs:
    movement
    cargo transport
    trail deposition
    defense
    brood care
    construction
    waste removal
    reproduction
    maintenance
```

## Step 3 — Define external basin couplings

```text
food basin
water basin
threat basin
toxic basin
construction material basin
fungus substrate basin
shelter basin
```

## Step 4 — Split the nest into subbasins

```text
nursery
storage
queen/reproduction chamber
waste chamber
cemetery
guard entrance
construction zones
cultivation basin
```

Each subbasin must answer:

```text
What parent need does it serve?
What support funds it?
What boundary protects it?
What flows enter and leave it?
What aftereffects stabilize it?
What failure mode does it prevent?
```

## Step 5 — Define mobile boundary expressions

```text
generic worker geometry
foraging susceptibility
nursing susceptibility
defense susceptibility
building susceptibility
waste-removal susceptibility
cultivation susceptibility
```

These are not states. They are basin susceptibilities that may deepen into specialization.

## Step 6 — Define aftereffect fields

```text
route support
home support
food support
alarm support
waste-isolation support
construction support
cultivation support
```

Every aftereffect should have:

```text
deposition condition
maintenance condition
decay condition
cost
compatible ant geometry
effect on continuation cost or support
```

## Step 7 — Declare producer residue

For every mechanism not yet native:

```text
name the producer variable
state the target RC meaning
state why it is not yet naturalized
state what would count as naturalization
downgrade claims accordingly
```

## Step 8 — Cultivate

Run conceptual or later executable probes. Classify what appeared. Do not overclaim. Withdraw scaffolding where possible. Split or refine only where parent basin closure benefits.

---

# 23. Mapping to LGRC without code

The present paper does not specify implementation. It does, however, identify the likely mapping surface.

The substrate papers describe a lineage from graph RC, to basin-attribute graph RC, to nine-port mechanical graph RC, to event-driven graph RC, and then LGRC9V3 packet-loop and pulse-surface specializations. ([GitHub][5]) The graph implementation repository describes LGRC9V3 as the active event-driven causal-history substrate and explicitly allows declared producer/policy scaffolding while keeping native versus producer-assisted claims separate. ([GitHub][2])

A future LGRC mapping should therefore treat RC-Ant elements as follows:

| RC-Ant concept      | LGRC-facing interpretation                                      |
| ------------------- | --------------------------------------------------------------- |
| Colony basin        | Higher-order support geometry, initially declared/annotated     |
| Nest subbasin       | Local support/attribute region with coupling roles              |
| Food basin          | External support stock plus signature/affordance surface        |
| Ant                 | Producer-mediated mobile boundary expression                    |
| Cargo               | Bound support, initially producer-scaffolded or packet-carried  |
| Movement            | Coherence-costly scheduled continuation over local geometry     |
| Pheromone           | Persistent route-support aftereffect                            |
| Trail               | Multi-edge aftereffect of repeated successful coupling          |
| Role specialization | Internal susceptibility aftereffect, likely scaffolded at first |
| Task demand         | Basin pressure or support deficit                               |
| Reproduction        | Surplus-supported split, likely producer-scaffolded initially   |
| Construction        | Persistent geometry modification, likely scaffolded initially   |
| Waste               | Harmful support routed to isolation basin                       |
| Producer state      | Naturalization debt ledger                                      |

The claim should remain conservative:

```text
supported target:
    RC-Ant as a conceptual and producer-mediated basin ecology

not yet claimed:
    fully native ant agency
    fully native colony cognition
    full biological equivalence
    full FRC implementation
    substrate-native reproduction and specialization
```

---

# 24. Educational summary: how to translate any state-rule agent system

To translate a classical agentic system into RC:

1. **Find the parent basin.**
   Ask what identity must persist. Do not begin with parts.

2. **Name the coherence economy.**
   Identify reserves, costs, support flows, waste, surplus, and leakage.

3. **Translate state into geometry.**
   Replace modes with basin capture, susceptibility, support condition, or boundary state.

4. **Translate input into affordance contact.**
   Inputs are local contacts with signatures, traces, gradients, support deficits, or boundary pressures.

5. **Translate action into costly coupling.**
   Actions are fluxes, support transfers, trace deposits, repairs, constructions, emissions, or splits.

6. **Translate memory into aftereffect.**
   Memory persists as changed geometry, lowered cost, strengthened route, or internal susceptibility.

7. **Translate goals into persistence pressure.**
   Goals are basin closure, repair, surplus, reproduction, or compatible continuation.

8. **Split only inside parent closure.**
   New subbasins must survive within and contribute to the parent basin.

9. **Declare producer residue.**
   Any remaining state variable is scaffolding, not ontology.

10. **Cultivate.**
    Classify what appears, interrogate missing support, naturalize where possible, and refine without overclaiming.

---

# 25. Core thesis

The core thesis of this paper is:

> A state-rule agent system can be translated into RC by replacing internal state with geometry, input with affordance contact, decision with local continuation among compatible basin couplings, action with coherence-costly transformation, memory with persistent aftereffect, resource with accessible coherence reserve, reproduction with surplus-supported split, and goal with basin persistence pressure.

The ant colony then becomes the first detailed example:

> RC-Ant does not simulate ants as agents in an environment. It translates ant-colony life into a hierarchical coherence economy: a parent colony basin refines itself into nest subbasins, mobile ant geometries, resource couplings, route aftereffects, role specializations, waste isolation, construction, and reproduction.

---

# Appendix A — Farm as RC ecology

A farm is not merely land plus workers plus crops. It is a parent basin that couples soil, water, sunlight, labor, tools, animals, storage, waste, and seasonal cycles into a persistence economy.

```text
farm parent basin
    fields / cultivation basins
    irrigation / water-flux channels
    soil reserve / nutrient basin
    seed basin
    crop-growth basin
    storage basin
    compost / waste-to-support conversion basin
    animal basins
    worker/mobile boundary expressions
    tool affordance surfaces
    market/output coupling
```

Classical farm state:

```text
field_state = planted / growing / dry / ready_to_harvest
worker_task = irrigate / weed / harvest / repair
storage_count = N
```

RC translation:

```text
field condition:
    soil-water-nutrient-light support geometry

worker task:
    basin capture by irrigation, repair, harvest, or transport demand

storage:
    retained support basin

compost:
    waste-to-support conversion basin

harvest:
    costly transfer from crop basin to storage or market basin

season:
    changing external signature and cost geometry
```

Producer residue might include schedules, crop stage counters, or worker assignments until these can be represented as substrate-carried support, delay, and basin-pressure dynamics.

---

# Appendix B — Forest as RC ecology

A forest is a long-lived parent basin with many overlapping subbasins.

```text
forest parent basin
    tree basins
    canopy-light geometry
    root/water coupling
    mycorrhizal route-support network
    decomposer basins
    seed bank
    animal/pollinator mobile couplings
    fire/threat basin
    deadwood/waste-to-support basin
```

Classical forest state:

```text
tree_health
soil_moisture
fire_risk
species_distribution
```

RC translation:

```text
tree health:
    support basin depth and flux access

soil moisture:
    accessible support reserve and transport affordance

mycorrhiza:
    persistent route-support/coupling geometry

decomposition:
    waste-to-support transformation

fire:
    destabilizing basin that consumes support and rewrites geometry

species distribution:
    differentiated basin ecology across light, water, nutrient, and reproduction pressures
```

The forest shows that an RC ecology need not have a central nest. The parent basin may be distributed, slow, and multi-centered.

---

# Appendix C — Agentic swarm as RC ecology

A robot or software swarm is often modeled as many agents with local policies. RC translation begins with the swarm identity.

```text
swarm parent basin
    task basin
    mobile agent geometries
    communication aftereffects
    charging/resource basins
    repair basins
    boundary/threat basins
    route-support fields
    local specialization basins
```

Classical swarm state:

```text
agent.mode = search / carry / recharge / avoid / repair
agent.battery = x
agent.message_queue = [...]
```

RC translation:

```text
battery:
    accessible coherence reserve

search:
    weakly constrained continuation under unresolved affordance

carry:
    bound support or object-coupling geometry

recharge:
    reserve-restoration basin capture

message:
    trace/signature modification, not symbolic instruction if naturalized

repair:
    boundary or function-restoration basin

task allocation:
    basin competition under local demand and specialization aftereffects
```

Producer residue may remain high at first, especially for message parsing, battery bookkeeping, and explicit assignment. The ledger makes this honest.

---

# Appendix D — Society as RC ecology

A society is a large parent basin composed of institutions, roles, norms, infrastructure, resource flows, records, and reproduction systems.

```text
society parent basin
    institutions
    professions / role basins
    infrastructure / conductance geometry
    laws / constraint geometry
    norms / route-support aftereffects
    markets / exchange basins
    schools / reproduction and specialization basins
    waste and exclusion basins
    memory archives
    boundary/defense structures
```

Classical social state:

```text
person.role = teacher / farmer / engineer / guard
institution.status = stable / failing
market.price = p
law = rule
```

RC translation:

```text
profession:
    role-basin specialization

institution:
    persistent subbasin of social coherence

infrastructure:
    conductance geometry that shapes possible flows

law:
    constraint surface and route-cost modifier

norm:
    persistent aftereffect that lowers or raises social continuation cost

market price:
    signal of exchange-basin tension, scarcity, surplus, and route affordance

education:
    reproduction of role susceptibility and cultural geometry

archive:
    persistent geometry for read-back and coordination
```

This translation avoids treating society as only a set of choosing individuals. It describes persons and institutions as nested identity basins within a larger coherence ecology.

---

# Appendix E — Cell as RC ecology

A cell is a compact example of hierarchical basin engineering.

```text
cell parent basin
    membrane / boundary basin
    metabolism / reserve conversion basin
    genetic/read-back basin
    repair basin
    waste/export basin
    reproduction/split basin
    sensing/coupling surfaces
    internal transport geometry
```

Classical cell state:

```text
membrane_potential
nutrient_level
gene_expression_state
division_phase
stress_state
```

RC translation:

```text
membrane:
    boundary and coupling geometry

nutrient:
    accessible support reserve

gene expression:
    slow internal geometry that changes future coupling and construction

division:
    surplus-supported split preserving parent-lineage coherence

stress:
    destabilizing basin pressure and repair demand

waste export:
    leakage control and harmful-support isolation
```

The cell makes the engineering lesson clear. One does not need to start with arbitrary organelles. One can define the parent identity first and then ask which subbasins must exist for persistence, reserve conversion, repair, boundary control, and reproduction.

---

# Appendix F — Claim ladder

This specification supports the following claim ladder.

```text
Rung 0 — Vocabulary
    Classical state-rule concepts can be named in RC terms.

Rung 1 — Conceptual mapping
    Agent, state, input, action, memory, goal, resource, cost,
    reproduction, and role can be mapped to geometry and flux concepts.

Rung 2 — Hierarchical design
    Parent basins can be refined into specialized subbasins under
    persistence and coherence-economy constraints.

Rung 3 — Producer-mediated ecology
    A producer scaffold can enact parts of the mapping over LGRC-like
    substrates while preserving a naturalization ledger.

Rung 4 — Partial naturalization
    Some producer variables are replaced by substrate-carried geometry,
    flux, support, event history, trail aftereffect, or reserve dynamics.

Rung 5 — Native ecology
    The substrate itself carries the relevant behavior without explicit
    producer state for the core mechanism.

Rung 6 — Fractal/native hierarchy
    Nested identity propagation is substrate-native across scales.
```

The present paper targets Rungs 0–2 and prepares Rung 3. It does not claim Rungs 5–6.

---

# Appendix G — Blocked claims

This specification does **not** claim:

```text
ants have semantic goals in the model
LGRC already natively implements full ant-colony life
producer state is RC ontology
pheromones are symbolic instructions
division of labor is already naturalized
reproduction is already substrate-native
the colony is conscious
the model is biologically complete
hierarchical basin definition is the same as full implemented FRC
```

The disciplined claim is:

```text
RC-Ant provides a blueprint for translating ant-colony behavior
from I/O state-rule agents into hierarchical RC agentic ecology,
while explicitly separating target geometry from producer residue.
```

---

# Closing

The important shift is not from one implementation technique to another. It is from state-centered thinking to geometry-centered thinking.

In the classical frame, an agent contains state and acts on a world.

In the RC frame, the world is already active coherence geometry. The apparent agent is a local identity expression inside that geometry. Its “state” is its current basin condition. Its “input” is affordance contact. Its “action” is costly coupling. Its “memory” is aftereffect. Its “goal” is persistence pressure. Its “reproduction” is surplus-supported split. Its “society” is hierarchical basin ecology.

RC-Ant is the first detailed example because ant colonies make all of this visible: parent identity, mobile expressions, nest architecture, food coupling, trail memory, specialization, construction, waste isolation, defense, surplus, and reproduction.

The general method is broader:

```text
define the parent basin
name its coherence economy
translate state into geometry
translate activity into costly flux
split/refine subbasins where closure requires it
declare producer residue
naturalize what the substrate can carry
cultivate without overclaiming
```

That is the blueprint for moving from I/O state-rule agents toward Reflexive Coherence agentic ecologies.

[1]: https://github.com/urosj/geometric-reflexive-coherence "GitHub - urosj/geometric-reflexive-coherence: Papers and research notes for Geometric Reflexive Coherence: a self-describing theory of self-defined dynamic systems, with core RC/FRC papers, substrate work, observations, investigations, and basin-based collaboration artifacts. · GitHub"
[2]: https://github.com/urosj/graph-reflexive-coherence "GitHub - urosj/graph-reflexive-coherence: Reference Python implementation workspace for Graph Reflexive Coherence: GRC-v2/v3, GRC-9, LGRC9V3 models, landscape tooling, telemetry-backed experiments, visualization CLIs, and specs for graph-based self-defining RC substrates. · GitHub"
[3]: https://github.com/urosj/geometric-reflexive-coherence/tree/main/arc-of-becoming "geometric-reflexive-coherence/arc-of-becoming at main · urosj/geometric-reflexive-coherence · GitHub"
[4]: https://github.com/urosj/geometric-reflexive-coherence/tree/main/essays "geometric-reflexive-coherence/essays at main · urosj/geometric-reflexive-coherence · GitHub"
[5]: https://github.com/urosj/geometric-reflexive-coherence/tree/main/substrates "geometric-reflexive-coherence/substrates at main · urosj/geometric-reflexive-coherence · GitHub"
