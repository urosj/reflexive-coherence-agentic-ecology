"""Focused static and adversarial tests for P2-I3 B-R I06 registration."""

from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[4]
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
SCRIPT = EXPERIMENT / "scripts/p2_i3_i06_br_registration.py"
POLICY_RELATIVE = "experiments/2026-07-AE01-post-n30-demand-composition-atlas/configs/p2_i3_br_i06_registration_policy.json"
TIMING_RELATIVE = "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i3/i06-br-candidate-free-timing.json"
REGISTRATION_RELATIVE = "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i3/i06-br-exact-registration.json"
SCHEMA_RELATIVE = "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i3/i06-br-registration.schema.json"
EXECUTION_SCHEMA_RELATIVE = "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i3/i06-br-execution-records.schema.json"
VALIDATION_RELATIVE = "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i3/i06-br-registration-validation.json"


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class P2I3I06RegistrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        spec = importlib.util.spec_from_file_location("p2_i3_i06_br_registration", SCRIPT)
        assert spec is not None and spec.loader is not None
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)
        cls.policy = load(POLICY_RELATIVE)
        cls.timing = load(TIMING_RELATIVE)
        cls.registration = load(REGISTRATION_RELATIVE)
        cls.schema = load(SCHEMA_RELATIVE)
        cls.execution_schema = load(EXECUTION_SCHEMA_RELATIVE)
        cls.validation = load(VALIDATION_RELATIVE)

    def test_closed_population_counts(self) -> None:
        matrix = self.registration["matrix"]
        self.assertEqual((matrix["configuration_count"], matrix["scientific_branch_count"], matrix["integrity_case_count"], matrix["governed_case_count"]), (90, 378, 72, 450))

    def test_exact_family_counts(self) -> None:
        rows = self.registration["matrix"]["configurations"]
        observed = {name: sum(row["family_id"] == name for row in rows) for name, _, _, _ in self.module.FAMILIES}
        self.assertEqual(observed, {name: count for name, count, _, _ in self.module.FAMILIES})

    def test_exact_branch_expansion(self) -> None:
        rows = self.registration["matrix"]["scientific_branches"]
        configs = {row["configuration_id"]: row["family_id"] for row in self.registration["matrix"]["configurations"]}
        self.assertEqual(sum(configs[row["configuration_id"]] == "core" and row["branch_kind"] != "fresh_nondepositor_terminal_probe" for row in rows), 126)
        self.assertEqual(sum(configs[row["configuration_id"]] in {"formation_quantity_history", "causal_projection_matched_false_trace"} for row in rows), 60)
        self.assertEqual(sum(row["branch_kind"] == "fresh_nondepositor_terminal_probe" for row in rows), 12)

    def test_integrity_faults_are_quarantined_and_balanced(self) -> None:
        rows = self.registration["matrix"]["integrity_fault_cases"]
        for kind in ("invalid_load", "invalid_reset", "invalid_branch", "invalid_continuation"):
            self.assertEqual(sum(row["fault_type"] == kind for row in rows), 18)
        self.assertTrue(all(row["scientific_evidence_effect"] == "none" for row in rows))

    def test_execution_class_counts(self) -> None:
        self.assertEqual(self.registration["resource_governance"]["class_counts"], {"probe_only": 288, "standard_trajectory": 48, "complex_construction_or_comparison": 48, "integrity_fault": 72})

    def test_resource_envelope_is_bounded(self) -> None:
        resources = self.registration["resource_governance"]
        self.assertLessEqual(resources["campaign"]["exact_campaign_ceiling_seconds"], 30 * 3600)
        self.assertLessEqual(resources["bytes"]["governed_physical_projection_bytes"], 8 * self.module.GIB)
        self.assertIsNone(resources["memory"]["experiment_RLIMIT_AS"])

    def test_timing_is_candidate_free(self) -> None:
        self.assertTrue(all(value is False for value in self.timing["candidate_blindness"].values()))
        self.assertEqual(self.timing["repetitions_per_operation"], 7)
        self.assertEqual(set(self.timing["raw_monotonic_elapsed_ns"]), {"startup", "inert_load", "fixed_native_event_pair", "eight_component_bundle_serialization", "schema_validation", "eight_component_reconstruction_read"})

    def test_baseline_validation_has_no_candidate_operation(self) -> None:
        self.assertEqual(self.registration["candidate_design"]["baseline_constructor_validation"], {"model_instantiations": 6, "save_load_pairs": 6, "resets": 6, "candidate_operations": 0})

    def test_realizations_are_role_preserving_permutations(self) -> None:
        topologies = self.registration["candidate_design"]["topology_by_realization"]
        self.assertEqual(len({row["topology_identity"] if "topology_identity" in row else self.module.digest_data(row) for row in topologies}), 3)
        self.assertTrue(all(len(row["nodes"]) == 14 and len(row["edges"]) == 14 for row in topologies))
        self.assertTrue(all(row["interior_cross_route_edges"] == 0 and row["reservoir_outgoing_edges"] == 0 for row in topologies))

    def test_candidate_and_calibration_seed_sets_are_disjoint(self) -> None:
        seeds = self.registration["candidate_design"]["seed_sets"]
        self.assertTrue(seeds["disjoint"])
        self.assertFalse(set(seeds["candidate_deterministic_raw_id_realizations"]) & set(seeds["calibration_seeds"]))

    def test_control_and_requirement_closure(self) -> None:
        controls = self.registration["control_governance"]
        self.assertEqual((controls["control_leg_count"], controls["requirement_count"]), (42, 14))
        self.assertTrue(all("intervention_field_ids" in row and "held_fixed_field_ids" in row and "completion_rule" in row for row in controls["control_legs"]))
        case_sets = {row["case_set_id"]: row for row in controls["evidence_case_set_registry"]}
        self.assertEqual(len(case_sets), controls["evidence_case_set_count"])
        self.assertTrue(all(row["case_ordinals"] for row in case_sets.values()))
        self.assertTrue(all(row["exact_membership_digest"] for row in case_sets.values()))
        self.assertTrue(all(row["selected_case_set_ids"] for row in controls["requirements"]))
        self.assertTrue(all(row["selected_case_set_ids"] for row in controls["control_legs"] if row["scientific_or_guard_class"] == "scientific" and row["applicability"] == "applicable"))
        self.assertTrue(all(row["observed_resolution"] is None for row in controls["control_legs"] + controls["requirements"]))

    def test_exact_estimator_and_observation_semantics(self) -> None:
        design = self.registration["candidate_design"]
        self.assertEqual(design["metrics"]["m_trace"], "(mu_E-mu_W)/max(abs(mu_E),abs(mu_W),delta)")
        self.assertEqual(design["metrics"]["m_export"], "(mu_O-mu_E)/max(abs(mu_O),abs(mu_E),delta)")
        self.assertEqual(design["metrics"]["analysis_projection"]["m_trace"]["target"]["value"], 2.0)
        self.assertEqual(design["metrics"]["analysis_projection"]["m_export"]["target"]["numerator"], 4)
        self.assertEqual(design["observation_panels"]["functional_distance"]["source"], "registered_inverse_conductance_projection")
        self.assertTrue(design["observation_panels"]["experimental_causal_influence"]["mandatory"])

    def test_topology_separates_undirected_structure_and_request_direction(self) -> None:
        for topology in self.registration["candidate_design"]["topology_by_realization"]:
            self.assertEqual(topology["structural_edge_directionality"], "undirected")
            self.assertEqual(topology["packet_request_directionality"], "operation_role_whitelist")
            for edge in topology["edges"]:
                self.assertEqual(edge["native_structural_semantics"], "undirected_port_edge")
                self.assertEqual(edge["flux_uv"]["numerator"], 0)
                self.assertEqual(edge["flux_coupling"]["numerator"], 0)
                self.assertTrue(edge["unregistered_reverse_request_prohibited"])

    def test_role_id_permutation_is_not_role_exchange(self) -> None:
        legs = {row["leg_id"]: row for row in self.registration["control_governance"]["control_legs"]}
        leg = legs["P2-I3-BR-L03-CTRL-02-LEG-02-ROLE-ID-PERMUTATION"]
        self.assertEqual(leg["selected_case_set_ids"], ["P2-I3-BR-CASESET-RAW-ID-PERMUTATION"])
        self.assertIn("realization_id", leg["intervention_field_ids"])
        self.assertIn("role_assignment_id", leg["held_fixed_field_ids"])

    def test_universal_conservation_and_boundary_selectors(self) -> None:
        legs = {row["leg_id"]: row for row in self.registration["control_governance"]["control_legs"]}
        for leg_id in (
            "P2-I3-BR-CTRL-09-LEG-02-GLOBAL-CONSERVATION",
            "P2-I3-BR-CTRL-09-LEG-03-UNREGISTERED-LEAKAGE",
            "P2-I3-BR-CTRL-11-LEG-01-PARTICIPANT-MEDIUM-BOUNDARY",
        ):
            self.assertEqual(legs[leg_id]["selected_case_set_ids"], ["P2-I3-BR-CASESET-ALL-SCIENTIFIC"])
            self.assertEqual(legs[leg_id]["selected_case_count"], 378)

    def test_supplemental_discriminator_populations_are_exact(self) -> None:
        rows = {row["requirement_id"]: row for row in self.registration["control_governance"]["requirements"]}
        expected = {
            "P2-I3-BR-DISC-01-FORMATION-QUANTITY-TEMPORAL-MATCH": "P2-I3-BR-CASESET-FORMATION-HISTORY",
            "P2-I3-BR-DISC-02-EXPORT-MASS-ORGANIZATION": "P2-I3-BR-CASESET-EXPORT-MASS-ORGANIZATION",
            "P2-I3-BR-DISC-03-COMPLETE-STATE-HISTORY": "P2-I3-BR-CASESET-STATE-HISTORY-DISCRIMINATOR",
            "P2-I3-BR-DISC-04-GEOMETRY-OR-TIMESCALE": "P2-I3-BR-CASESET-TAU-VARIATION",
            "P2-I3-BR-DISC-05-FRESH-NONDEPOSITOR": "P2-I3-BR-CASESET-FRESH-NONDEPOSITOR",
        }
        for requirement_id, case_set_id in expected.items():
            self.assertEqual(rows[requirement_id]["selected_case_set_ids"], [case_set_id])
        self.assertEqual(rows["P2-I3-BR-DISC-05-FRESH-NONDEPOSITOR"]["selected_case_count"], 12)

    def test_execution_control_lifecycle_is_not_collapsed(self) -> None:
        valid = {
            "artifact_kind": "p2_i3_br_control_leg_resolution",
            "leg_id": "example",
            "execution_status": "executed_valid",
            "evidence_resolution": "mixed",
            "control_resolution": "resolved",
            "terminal_guard_status": "passed",
            "evidence_refs": ["sha256:example"],
        }
        self.module.jsonschema.validate(valid, self.execution_schema)
        invalid = {"artifact_kind": "p2_i3_br_control_leg_resolution", "leg_id": "example", "resolution": "generic_mass_effect", "evidence_refs": []}
        with self.assertRaises(self.module.jsonschema.ValidationError):
            self.module.jsonschema.validate(invalid, self.execution_schema)

    def test_operational_baseline_terminal_is_scientifically_inert(self) -> None:
        valid = {
            "artifact_kind": "p2_i3_br_operational_baseline_terminal",
            "entry_id": "P2-I3-BR-OPBASE-TAU-1-R101",
            "substrate_base_id": "P2-I3-BR-BASE-TAU-1-R101",
            "source_identity_digest": "0" * 64,
            "runtime_identity_digest": "1" * 64,
            "native_restoration_v2_digest": "2" * 64,
            "content_addressed_bundle_digest": "3" * 64,
            "scientific_operation_counts": {
                "formation": 0,
                "export": 0,
                "encounter_probe": 0,
                "scientific_control": 0,
                "integrity_fault_dispatch": 0,
            },
            "scientific_evidence_effect": "none",
            "status": "valid_operational_baseline",
        }
        self.module.jsonschema.validate(valid, self.execution_schema)
        invalid = deepcopy(valid)
        invalid["scientific_operation_counts"]["formation"] = 1
        with self.assertRaises(self.module.jsonschema.ValidationError):
            self.module.jsonschema.validate(invalid, self.execution_schema)

    def test_schedule_starts_with_baselines_then_integrity_block(self) -> None:
        schedule = self.registration["schedule"]
        baseline_ids = [row["entry_id"] for row in schedule["operational_baseline_entries"]]
        expected = [row["case_id"] for row in self.registration["matrix"]["integrity_fault_cases"]]
        self.assertEqual(schedule["order"][:6], baseline_ids)
        self.assertEqual(schedule["order"][6:78], expected)

    def test_case_registry_is_separate_and_unchanged(self) -> None:
        schedule = self.registration["schedule"]
        expected = [row["case_id"] for row in self.registration["matrix"]["integrity_fault_cases"] + self.registration["matrix"]["scientific_branches"]]
        self.assertEqual(schedule["canonical_case_registry_order"], expected)
        self.assertEqual(len(expected), 450)
        self.assertEqual(set(schedule["order"][6:]), set(expected))

    def test_schedule_is_topological(self) -> None:
        schedule = self.registration["schedule"]
        ordinals = {entry_id: index for index, entry_id in enumerate(schedule["order"], start=1)}
        self.assertEqual(len(ordinals), 456)
        for edge in schedule["dependency_dag"]:
            self.assertTrue(all(ordinals[parent] < ordinals[edge["entry_id"]] for parent in edge["parent_entry_ids"]))

    def test_baseline_failure_subtrees_are_exact_and_disjoint(self) -> None:
        schedule = self.registration["schedule"]
        observed: set[str] = set()
        for subtree in schedule["baseline_failure_subtrees"]:
            entries = set(subtree["dependent_entry_ids"])
            self.assertFalse(observed & entries)
            observed |= entries
            self.assertTrue(all(
                next(row for row in schedule["entries"] if row["entry_id"] == entry_id)["substrate_base_id"]
                == subtree["substrate_base_id"]
                for entry_id in entries
            ))
        self.assertEqual(observed, set(schedule["order"][6:]))

    def test_attempts_and_retry_tokens_are_finite(self) -> None:
        attempts = self.registration["attempt_governance"]
        self.assertEqual((attempts["registered_case_count"], attempts["registered_operational_baseline_entry_count"], attempts["primary_attempt_slots"], len(attempts["class_retry_tokens"]), attempts["maximum_governed_child_starts"]), (450, 6, 456, 4, 460))
        self.assertTrue(all(row["allocation"] is None for row in attempts["class_retry_tokens"]))

    def test_gate_stops_remain_closed(self) -> None:
        gate = self.registration["gate_boundary"]
        self.assertEqual(gate["P2-I3-REG-GATE"], "unopened_pending_owner_review")
        self.assertFalse(gate["candidate_execution_authorized"])
        self.assertFalse(gate["control_execution_authorized"])
        self.assertFalse(gate["integrity_fault_execution_authorized"])

    def test_appendix_is_absent(self) -> None:
        self.assertEqual(self.registration["matrix"]["appendix_case_count"], 0)
        self.assertTrue(all(row["appendix"] is False for row in self.registration["matrix"]["configurations"]))

    def test_payload_digests_are_exact(self) -> None:
        for artifact in (self.timing, self.registration, self.validation):
            payload = {key: value for key, value in artifact.items() if key != "canonical_payload_digest"}
            self.assertEqual(artifact["canonical_payload_digest"], self.module.digest_data(payload))

    def test_absolute_machine_path_is_rejected(self) -> None:
        with self.assertRaises(self.module.RegistrationError):
            self.module.assert_portable({"path": "/home/example/private/runtime"})
        self.module.assert_portable({"path": "${RCAE_PYGRC_ROOT}/src"})

    def test_adversarial_missing_case_is_rejected(self) -> None:
        changed = deepcopy(self.registration)
        changed["matrix"]["scientific_branches"].pop()
        changed["canonical_payload_digest"] = self.module.digest_data({key: value for key, value in changed.items() if key != "canonical_payload_digest"})
        with self.assertRaises(Exception):
            self.module.validate_registration(self.policy, self.timing, changed, self.schema)

    def test_adversarial_control_outcome_is_rejected(self) -> None:
        changed = deepcopy(self.registration)
        changed["control_governance"]["control_legs"][0]["observed_resolution"] = "supportive"
        changed["canonical_payload_digest"] = self.module.digest_data({key: value for key, value in changed.items() if key != "canonical_payload_digest"})
        with self.assertRaises(self.module.RegistrationError):
            self.module.validate_registration(self.policy, self.timing, changed, self.schema)

    def test_adversarial_gate_open_is_rejected(self) -> None:
        changed = deepcopy(self.registration)
        changed["gate_boundary"]["candidate_execution_authorized"] = True
        changed["canonical_payload_digest"] = self.module.digest_data({key: value for key, value in changed.items() if key != "canonical_payload_digest"})
        with self.assertRaises(Exception):
            self.module.validate_registration(self.policy, self.timing, changed, self.schema)

    def test_adversarial_assignment_drift_is_rejected(self) -> None:
        changed = deepcopy(self.registration)
        changed["resource_governance"]["assignments"][0]["execution_class"] = "probe_only"
        changed["canonical_payload_digest"] = self.module.digest_data({key: value for key, value in changed.items() if key != "canonical_payload_digest"})
        with self.assertRaises(self.module.RegistrationError):
            self.module.validate_registration(self.policy, self.timing, changed, self.schema)

    def test_adversarial_baseline_scientific_operation_is_rejected(self) -> None:
        changed = deepcopy(self.registration)
        changed["schedule"]["operational_baseline_entries"][0]["scientific_operation_counts"]["formation"] = 1
        self._assert_semantic_mutation_rejected(changed)

    def test_adversarial_probe_before_parent_is_rejected(self) -> None:
        changed = deepcopy(self.registration)
        order = changed["schedule"]["order"]
        probe = next(row for row in changed["matrix"]["scientific_branches"] if row.get("terminal_probe"))
        parent = next(parent for parent in probe["parent_ids"] if not parent.startswith("checkpoint:"))
        probe_index = order.index(probe["case_id"])
        parent_index = order.index(parent)
        order[parent_index], order[probe_index] = order[probe_index], order[parent_index]
        self._assert_semantic_mutation_rejected(changed)

    def test_adversarial_unknown_dependency_is_rejected(self) -> None:
        changed = deepcopy(self.registration)
        changed["matrix"]["scientific_branches"][0]["parent_ids"] = ["unknown-parent"]
        changed["canonical_payload_digest"] = self.module.digest_data({key: value for key, value in changed.items() if key != "canonical_payload_digest"})
        with self.assertRaises(self.module.RegistrationError):
            self.module.validate_registration(self.policy, self.timing, changed, self.schema)

    def _assert_semantic_mutation_rejected(self, changed: dict) -> None:
        changed["canonical_payload_digest"] = self.module.digest_data({key: value for key, value in changed.items() if key != "canonical_payload_digest"})
        with self.assertRaises(self.module.RegistrationError):
            self.module.validate_registration(self.policy, self.timing, changed, self.schema)

    def test_adversarial_estimator_formula_is_rejected(self) -> None:
        changed = deepcopy(self.registration)
        changed["candidate_design"]["metrics"]["m_trace"] = "(mu_E-mu_W)/max(abs(mu_E-mu_W),delta)"
        self._assert_semantic_mutation_rejected(changed)

    def test_adversarial_observation_surface_is_rejected(self) -> None:
        changed = deepcopy(self.registration)
        changed["candidate_design"]["observation_panels"]["functional_distance"]["disposition"] = "measured_native"
        self._assert_semantic_mutation_rejected(changed)

    def test_adversarial_edge_flux_is_rejected(self) -> None:
        changed = deepcopy(self.registration)
        changed["candidate_design"]["topology_by_realization"][0]["edges"][0]["flux_uv"] = self.module.fraction(self.module.Fraction(1, 64))
        self._assert_semantic_mutation_rejected(changed)

    def test_adversarial_edge_direction_is_rejected(self) -> None:
        changed = deepcopy(self.registration)
        changed["candidate_design"]["topology_by_realization"][0]["edges"][0]["native_structural_semantics"] = "directed_edge"
        self._assert_semantic_mutation_rejected(changed)

    def test_adversarial_family_selector_is_rejected(self) -> None:
        changed = deepcopy(self.registration)
        leg = next(row for row in changed["control_governance"]["control_legs"] if row["leg_id"].endswith("ROLE-ID-PERMUTATION"))
        leg["selected_case_set_ids"] = ["P2-I3-BR-CASESET-ROLE-EXCHANGE"]
        self._assert_semantic_mutation_rejected(changed)

    def test_adversarial_pairing_field_is_rejected(self) -> None:
        changed = deepcopy(self.registration)
        changed["pairing"]["fields"].pop()
        self._assert_semantic_mutation_rejected(changed)

    def test_adversarial_retry_class_is_rejected(self) -> None:
        changed = deepcopy(self.registration)
        changed["attempt_governance"]["class_retry_tokens"][0]["execution_class"] = "invented"
        self._assert_semantic_mutation_rejected(changed)

    def test_adversarial_producer_class_is_rejected(self) -> None:
        changed = deepcopy(self.registration)
        changed["producer_inventory"][0]["producer_class"] = "evidence_only"
        self._assert_semantic_mutation_rejected(changed)


if __name__ == "__main__":
    unittest.main()
