# AE01 Reports

This directory is reserved for deterministic reports backed by controlling
machine records. P1-I5 creates no evidential lane report or lane
interpretation; its interpretation fixture is infrastructure-only.

Reports use either:

- `generated_projection`, containing generated machine facts only; or
- `assembled_interpretation`, containing deterministic generated facts plus a
  separately tracked authored interpretation bounded by the same claim record.

Reports cannot alter identities, evidence roles, controls, debt, terminal
classifications, scores, selection, or claim ceilings. Disposable test reports
belong under ignored top-level `outputs/`. A lane report must preserve the
machine-derived threshold relation, boundary rungs, support status, and
classification value while keeping the separately authored becoming,
development, and next-move reading within the controlling claim boundary.
