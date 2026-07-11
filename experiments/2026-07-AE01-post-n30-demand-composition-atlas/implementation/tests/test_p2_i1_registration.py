from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys
import unittest


def _find_repository_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        experiment = parent / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
        if (parent / ".git").exists() and experiment.is_dir():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _find_repository_root()
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
SCRIPTS = EXPERIMENT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ae01_tooling import ContractError, digest_canonical_data, load_json  # noqa: E402
from p2_i1 import CONFIG_PATHS  # noqa: E402
from p2_i1_registration import (  # noqa: E402
    EXPECTED_EVIDENCE_BINDINGS,
    INHERITED_SOURCES,
    RETAINED_GENERATED_PATHS,
    _source_changes_from_porcelain,
    derive_control_lifecycle,
    load_registration_profile_registry,
    validate_baseline_registry,
    validate_inherited_verification,
    validate_registration_records,
    validate_registration_policy,
)
from p2_i1_runtime import resolve_node_coherences, resolve_reader_packet_amount  # noqa: E402


class P2I1RegistrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.configs = {
            name: load_json(EXPERIMENT / path) for name, path in CONFIG_PATHS.items()
        }
        cls.policy = load_json(EXPERIMENT / "configs/p2_i1_registration_policy.json")

    def test_registration_policy_matches_frozen_calibration_identities(self) -> None:
        result = validate_registration_policy(self.policy, self.configs)
        self.assertEqual(result["status"], "passed")
        self.assertTrue(result["measurement_identity_match"])
        self.assertTrue(result["realization_identity_match"])
        self.assertEqual(result["control_count"], 24)
        self.assertFalse(result["candidate_execution_authorized"])

    def test_policy_declares_obligations_not_control_outcomes(self) -> None:
        for control in self.policy["control_plans"]:
            self.assertNotIn("outcome_status", control)
        scaffold = self.policy["control_plans"][-1]
        self.assertEqual(scaffold["control_id"], "AE01-L01-CTRL-05")
        self.assertEqual(scaffold["applicability"], "not_applicable")
        self.assertEqual(scaffold["not_applicable_decision_ref"], "P2-I1-DEC-025")

    def test_registration_rejects_authored_control_outcome(self) -> None:
        bad = deepcopy(self.policy)
        bad["control_plans"][0]["outcome_status"] = "resolved"
        with self.assertRaises(ContractError):
            validate_registration_policy(bad, self.configs)

    def test_registration_rejects_measurement_identity_drift(self) -> None:
        bad = deepcopy(self.policy)
        bad["identity_imports"]["calibration_measurement_identity_digest"] = "0" * 64
        with self.assertRaises(ContractError):
            validate_registration_policy(bad, self.configs)

    def test_existing_schema_registration_records_cross_resolve(self) -> None:
        profile = load_json(
            EXPERIMENT / "contracts/p2-i1/registration-realization-profile.json"
        )
        resolved = validate_registration_records(
            EXPERIMENT / "contracts/p2-i1/registration-records", profile
        )
        self.assertEqual(
            resolved["pattern_card"]["record"]["pattern_id"],
            "rcae-p2-i1-l01-registered-probe",
        )
        self.assertEqual(len(resolved["debt_records"]), 4)

    def test_registration_reconstruction_profiles_are_path_free(self) -> None:
        registry = load_registration_profile_registry()
        profiles = registry["record"]["profiles"]
        self.assertEqual(len(profiles), 9)
        rendered = str(registry)
        self.assertNotIn(str(ROOT), rendered)
        self.assertIn("LOCAL_GRAPH_CHECKOUT", rendered)

    def test_source_cleanliness_ignores_only_generated_registration_outputs(self) -> None:
        retained = sorted(RETAINED_GENERATED_PATHS)[0]
        status = f"?? {retained}\n M experiments/source.py\n"
        self.assertEqual(
            _source_changes_from_porcelain(status),
            [" M experiments/source.py"],
        )

    def test_control_lifecycle_separates_registration_from_execution(self) -> None:
        evidence_ids = {
            value
            for bindings in EXPECTED_EVIDENCE_BINDINGS.values()
            for value in bindings
        }
        controls = derive_control_lifecycle(self.policy, evidence_ids)
        self.assertEqual(len(controls), 24)
        by_id = {row["control_id"]: row for row in controls}
        self.assertEqual(by_id["AE01-CTRL-01"]["outcome_status"], "resolved")
        mixed = by_id["AE01-CTRL-04"]
        self.assertEqual(mixed["outcome_status"], "pending_execution")
        self.assertEqual(
            [leg["outcome_status"] for leg in mixed["legs"]],
            ["resolved", "pending_execution"],
        )
        scaffold = by_id["AE01-L01-CTRL-05"]
        self.assertEqual(scaffold["outcome_status"], "not_applicable")
        self.assertEqual(scaffold["decision_ref"], "P2-I1-DEC-025")

    def test_control_lifecycle_blocks_missing_exact_evidence(self) -> None:
        evidence_ids = {
            value
            for bindings in EXPECTED_EVIDENCE_BINDINGS.values()
            for value in bindings
        }
        evidence_ids.remove("source-inventory")
        controls = derive_control_lifecycle(self.policy, evidence_ids)
        by_id = {row["control_id"]: row for row in controls}
        self.assertEqual(by_id["AE01-CTRL-01"]["outcome_status"], "blocked")
        self.assertEqual(
            by_id["AE01-CTRL-01"]["legs"][0]["missing_evidence_refs"],
            ["source-inventory"],
        )

    def test_registration_rejects_evidence_binding_substitution(self) -> None:
        bad = deepcopy(self.policy)
        bad["control_plans"][0]["legs"][0]["evidence_binding_refs"] = [
            "rcae-p2-i1-l01-registered-probe"
        ]
        with self.assertRaises(ContractError):
            validate_registration_policy(bad, self.configs)

    def test_registration_rejects_unbacked_evidence_description(self) -> None:
        bad = deepcopy(self.policy)
        bad["control_plans"][0]["legs"][0]["required_evidence"] = [
            "evidence that does not exist anywhere"
        ]
        with self.assertRaises(ContractError):
            validate_registration_policy(bad, self.configs)

    def _inherited_verification(self) -> dict[str, object]:
        rows = []
        for source in INHERITED_SOURCES:
            row = {
                "reference_id": source["reference_id"],
                "source_path": f"grc:{source['graph_relative_path']}",
                "file_sha256": source["file_sha256"],
                "inherited_role": source["inherited_role"],
                "identical_scope_verification": {
                    "carrier": False,
                    "mechanism": False,
                    "intervention": False,
                    "claim_scope": False,
                    "identical_scope": False,
                    "rationale": "fresh P2-I1 scope",
                },
                "must_not_consume_as": source["must_not_consume_as"],
                "new_lane_execution_required": True,
            }
            if source["output_digest"] is not None:
                row["output_digest"] = source["output_digest"]
            rows.append(row)
        result: dict[str, object] = {
            "artifact_kind": "p2_i1_inherited_control_verification",
            "schema_version": "1.0.0",
            "evidence_effect": "registration_only_inherited_boundary",
            "lane_id": "AE01-L01",
            "cycle_id": "P2-I1-C00",
            "graph_source_revision": "1f42cb1d1e591159afc2ca54cc656b574d41c8d3",
            "graph_source_worktree_clean": True,
            "graph_repository_write_observed": False,
            "source_revision": "0" * 40,
            "source_worktree_clean": True,
            "retention_eligible": True,
            "preview_only": False,
            "source_count": len(rows),
            "sources": rows,
            "candidate_artifacts_consumed": False,
            "candidate_execution_performed": False,
            "lane_specific_causal_evidence_inherited": False,
            "new_lane_execution_required": True,
        }
        result["canonical_payload_digest"] = digest_canonical_data(result)
        return result

    def test_inherited_verification_rejects_scope_promotion(self) -> None:
        record = self._inherited_verification()
        validate_inherited_verification(record)
        bad = deepcopy(record)
        bad["sources"][0]["identical_scope_verification"][  # type: ignore[index]
            "carrier"
        ] = True
        bad["canonical_payload_digest"] = digest_canonical_data(
            {
                key: value
                for key, value in bad.items()
                if key != "canonical_payload_digest"
            }
        )
        with self.assertRaises(ContractError):
            validate_inherited_verification(bad)

    def test_execution_control_requires_exact_cells(self) -> None:
        bad = deepcopy(self.policy)
        control = next(
            row for row in bad["control_plans"] if row["control_id"] == "AE01-CTRL-06"
        )
        control["legs"][0].pop("exact_cells")
        with self.assertRaises(ContractError):
            validate_registration_policy(bad, self.configs)

    def test_execution_control_requires_causal_discriminator_fields(self) -> None:
        bad = deepcopy(self.policy)
        control = next(
            row for row in bad["control_plans"] if row["control_id"] == "AE01-CTRL-06"
        )
        control["legs"][0].pop("preserved_fields")
        with self.assertRaises(ContractError):
            validate_registration_policy(bad, self.configs)

    def _baseline_registry(self) -> dict[str, object]:
        validation = validate_registration_policy(self.policy, self.configs)
        entries: list[dict[str, object]] = []
        cells = {row["cell_id"]: row for row in self.configs["cells"]["cells"]}
        for index, cell_id in enumerate(self.policy["execution_policy"]["cell_order"]):
            for seed_index, seed in enumerate(self.policy["execution_policy"]["seeds"]):
                projection = {
                    "cell_id": cell_id,
                    "seed": seed,
                    "fixture_config_digest": digest_canonical_data(
                        self.configs["fixture"]
                    ),
                    "cell_configuration_digest": digest_canonical_data(cells[cell_id]),
                    "runtime_config_digest": digest_canonical_data(self.configs["runtime"]),
                    "resolved_node_coherences": resolve_node_coherences(
                        self.configs["fixture"], seed, cell_id, self.configs["cells"]
                    ),
                    "reader_packet_amount": resolve_reader_packet_amount(
                        self.configs["fixture"], self.configs["cells"], cell_id
                    ),
                    "route_aspect_digest": "1" * 64,
                    "snapshot_digest": f"{index * 3 + seed_index + 1:064x}",
                    "queue_digest": digest_canonical_data([]),
                    "focal_surface_digest": digest_canonical_data([]),
                }
                entries.append(
                    {
                        **projection,
                        "expected_composite_baseline_digest": digest_canonical_data(
                            projection
                        ),
                    }
                )
        result: dict[str, object] = {
            "artifact_kind": "p2_i1_baseline_identity_registry",
            "schema_version": "1.0.0",
            "evidence_effect": "none_registration_infrastructure_only",
            "lane_id": "AE01-L01",
            "cycle_id": "P2-I1-C00",
            "source_revision": "0" * 40,
            "source_worktree_clean": True,
            "retention_eligible": True,
            "preview_only": False,
            "registration_policy_digest": validation["registration_policy_digest"],
            "realization_profile_id": "rcae-p2-i1-registered-realization-v1",
            "fresh_worker_per_entry": True,
            "entry_count": 21,
            "candidate_operations_executed": False,
            "candidate_outcomes_absent": True,
            "entries": entries,
        }
        result["canonical_payload_digest"] = digest_canonical_data(result)
        return result

    def test_baseline_registry_preserves_all_21_candidate_free_entries(self) -> None:
        registry = self._baseline_registry()
        validate_baseline_registry(registry, self.policy, self.configs)
        self.assertEqual(registry["entry_count"], 21)

    def test_baseline_registry_rejects_worker_reuse_or_state_drift(self) -> None:
        registry = self._baseline_registry()
        registry["fresh_worker_per_entry"] = False
        with self.assertRaises(ContractError):
            validate_baseline_registry(registry, self.policy, self.configs)
        registry = self._baseline_registry()
        registry["entries"][0]["queue_digest"] = "0" * 64  # type: ignore[index]
        with self.assertRaises(ContractError):
            validate_baseline_registry(registry, self.policy, self.configs)

    def test_baseline_preview_cannot_enter_retention_validation(self) -> None:
        registry = self._baseline_registry()
        registry["artifact_kind"] = "p2_i1_baseline_identity_registry_preview"
        registry["source_worktree_clean"] = False
        registry["retention_eligible"] = False
        registry["preview_only"] = True
        registry["canonical_payload_digest"] = digest_canonical_data(
            {
                key: value
                for key, value in registry.items()
                if key != "canonical_payload_digest"
            }
        )
        with self.assertRaises(ContractError):
            validate_baseline_registry(registry, self.policy, self.configs)
        validate_baseline_registry(
            registry, self.policy, self.configs, allow_preview=True
        )


if __name__ == "__main__":
    unittest.main()
