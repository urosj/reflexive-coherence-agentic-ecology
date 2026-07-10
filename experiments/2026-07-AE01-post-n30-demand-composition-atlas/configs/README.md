# AE01 Configurations

P1-I5 owns two committed configuration surfaces:

- `p1_i5_profiles.json` is the schema-valid shared environment, command,
  dependency, and resource profile registry.
- `p1_i5_execution_policy.json` freezes the seven-by-seven comparison matrix,
  full logical-group accounting, seeds, attempts, resources, artifact roles,
  success/invalid/infrastructure-failure criteria, normalized threshold
  boundary, control priority, synthesis entry, and eight non-selection
  conditions.

Configurations are experiment inputs, not result records or positive evidence.
The resolved execution-policy view is generated deterministically into ignored
top-level `outputs/` and exposes every inherited common-control disposition as
well as every cell's deterministic configuration identity and fully inherited
execution contract.

PyGRC installation location, graph checkout location, secrets, and machine
resource overrides are local inputs and are never committed. A lane-specific
live probe must add an explicit realization profile and runtime receipt before
execution; absence fails closed.
