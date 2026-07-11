from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
import sys

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ae01_tooling import ContractError
from ae01_tooling import digest_canonical_data, pretty_json_dumps
from p2_i1_execution import (
    _git_revision,
    _expected_run_specs,
    _retry_ledger_payload,
    build_cycle_audit,
    build_exec_freeze,
    load_execution_policy,
    restoration_projection,
    validate_exec_freeze,
    validate_execution_policy,
    validate_execution_specific_capabilities,
    validate_retry_ledger,
)


class _CompleteFakeLGRC:
    @classmethod
    def schedule_packet_departure(cls) -> None:
        return None

    @classmethod
    def produce_events(cls) -> None:
        return None

    @classmethod
    def save(cls) -> None:
        return None

    @classmethod
    def load(cls) -> None:
        return None

    @classmethod
    def get_state(cls) -> None:
        return None

    @classmethod
    def snapshot(cls) -> None:
        return None


class P2I1ExecutionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = load_execution_policy()
        self._tmp = tempfile.TemporaryDirectory(dir=SCRIPTS.parents[2] / "outputs")
        self.addCleanup(self._tmp.cleanup)
        candidate_paths = patch(
            "p2_i1_execution._candidate_result_paths", return_value=[]
        )
        candidate_paths.start()
        self.addCleanup(candidate_paths.stop)
        self.binding_path = Path(self._tmp.name) / "binding-preview.json"
        body = {
            "artifact_kind": "p2_i1_c02_execution_binding_receipt_preview",
            "schema_version": "1.0.0",
            "cycle_id": "P2-I1-C02",
            "evidence_effect": "none_pre_execution_binding_only",
            "source_revision": _git_revision(),
            "source_worktree_clean": False,
            "retention_eligible": False,
            "preview_only": True,
            "source_status_entry_count": 1,
            "execution_policy_digest": digest_canonical_data(self.policy),
            "runtime_identity": "pygrc==0.1",
            "execution_class": "pygrc_runtime_with_rcae_producer",
            "binding_relation_to_registration": "strict_execution_specific_superset",
            "registered_operation_classes": self.policy["execution_identity"][
                "registered_operation_classes"
            ],
            "execution_specific_capabilities": self.policy["execution_identity"][
                "execution_specific_capability_paths"
            ],
            "graph_source_revision": "1f42cb1d1e591159afc2ca54cc656b574d41c8d3",
            "graph_repository_write_observed": False,
            "machine_local_runtime_path_recorded": False,
            "machine_local_graph_path_recorded": False,
            "candidate_operation_executed": False,
            "candidate_outcome_observed": False,
            "fallback_used": False,
            "conformance_status": "passed",
        }
        receipt = {
            **body,
            "canonical_payload_digest": digest_canonical_data(body),
        }
        self.binding_path.write_text(pretty_json_dumps(receipt), encoding="utf-8")

    def test_execution_policy_validates_without_candidate_authority(self) -> None:
        result = validate_execution_policy(self.policy)
        self.assertEqual(result["run_count"], 21)
        self.assertEqual(result["live_obligation_count"], 12)
        self.assertFalse(result["candidate_execution_authorized"])

    def test_restoration_projection_ignores_only_nested_base_cache(self) -> None:
        snapshot = {
            "metadata": {"model_family": "LGRC9V3", "step_index": 2},
            "topology": {"nodes": [0, 1], "edges": [0]},
            "basin_attributes": {"0": {"coherence": 1.0}},
            "edge_labels": {"0": "writer"},
            "dynamics": {"lgrc9v3_runtime": {"scheduler_event_index": 2}},
            "observables": {"total_energy": 1.0},
            "events": [{"kind": "arrival"}],
            "caches": {"base_grc9v3_snapshot": {"rng_state": None}},
        }
        normalized = deepcopy(snapshot)
        normalized["caches"]["base_grc9v3_snapshot"] = {
            "rng_state": {"engine": "python_random"},
            "params_identity": "materialized",
        }
        self.assertEqual(
            restoration_projection(snapshot), restoration_projection(normalized)
        )
        normalized["dynamics"]["lgrc9v3_runtime"]["scheduler_event_index"] = 3
        self.assertNotEqual(
            restoration_projection(snapshot), restoration_projection(normalized)
        )

    def test_execution_policy_rejects_unknown_semantic_field(self) -> None:
        changed = deepcopy(self.policy)
        changed["unreviewed_choice"] = True
        with self.assertRaises(ContractError):
            validate_execution_policy(changed)

    def test_execution_policy_rejects_medium_freeze_producer_drift(self) -> None:
        changed = deepcopy(self.policy)
        changed["cell_realizations"]["medium-freeze-withdrawal"][
            "expected_source_digest"
        ] = "none"
        with self.assertRaises(ContractError):
            validate_execution_policy(changed)

    def test_execution_policy_rejects_trace_shuffle_multi_axis_drift(self) -> None:
        changed = deepcopy(self.policy)
        changed["cell_realizations"]["trace-shuffle"]["broken_relation"] = (
            "source_and_quantity"
        )
        with self.assertRaises(ContractError):
            validate_execution_policy(changed)

    def test_exact_run_specs_cover_cell_seed_matrix_once(self) -> None:
        specs = _expected_run_specs(self.policy)
        self.assertEqual(len(specs), 21)
        self.assertEqual(
            len({(row["cell_id"], row["seed"]) for row in specs}), 21
        )
        self.assertEqual(len({row["worker_scope_id"] for row in specs}), 21)
        self.assertTrue(all(row["attempt"] == 1 for row in specs))

    def test_execution_specific_capability_superset_resolves(self) -> None:
        modules = {"models": SimpleNamespace(LGRC9V3=_CompleteFakeLGRC)}
        result = validate_execution_specific_capabilities(modules, self.policy)
        self.assertEqual(
            set(result),
            {
                "writer_packet_scheduling",
                "feedback_conditioned_packet_production",
                "branch_snapshot_persistence",
                "runtime_state_audit",
            },
        )

    def test_execution_specific_capability_missing_produce_events_fails(self) -> None:
        class MissingProduce:
            schedule_packet_departure = _CompleteFakeLGRC.schedule_packet_departure
            save = _CompleteFakeLGRC.save
            load = _CompleteFakeLGRC.load
            get_state = _CompleteFakeLGRC.get_state
            snapshot = _CompleteFakeLGRC.snapshot

        modules = {"models": SimpleNamespace(LGRC9V3=MissingProduce)}
        with self.assertRaises(ContractError):
            validate_execution_specific_capabilities(modules, self.policy)

    def test_dirty_preview_freeze_never_authorizes_candidate_execution(self) -> None:
        freeze = build_exec_freeze(
            execution_binding_path=self.binding_path,
            allow_dirty_preview=True,
        )
        self.assertEqual(freeze["artifact_kind"], "p2_i1_c02_exec_freeze_preview")
        self.assertFalse(freeze["retention_eligible"])
        self.assertTrue(freeze["preview_only"])
        self.assertFalse(freeze["candidate_execution_authorized"])
        with self.assertRaises(ContractError):
            validate_exec_freeze(freeze)

    def test_candidate_artifact_presence_blocks_freeze(self) -> None:
        with tempfile.TemporaryDirectory(dir=SCRIPTS.parents[2] / "outputs") as tmp_dir:
            candidate = Path(tmp_dir) / "candidate.json"
            candidate.write_text("{}\n", encoding="utf-8")
            with patch(
                "p2_i1_execution._candidate_result_paths",
                return_value=[candidate],
            ):
                with self.assertRaises(ContractError):
                    build_exec_freeze(
                        execution_binding_path=self.binding_path,
                        allow_dirty_preview=True,
                    )

    def test_retry_ledger_selects_lowest_failed_seed_per_cell(self) -> None:
        freeze = build_exec_freeze(
            execution_binding_path=self.binding_path,
            allow_dirty_preview=True,
        )
        failures = [
            {
                "cell_id": "reference",
                "seed": 307,
                "attempt": 1,
                "execution_configuration_digest": "digest-307",
                "exit_code": 2,
                "failure_class": "runtime_or_integrity_failure_pending_review",
                "diagnostic_digest": "error-307",
                "candidate_scientific_effect": "none_operational_only",
            },
            {
                "cell_id": "reference",
                "seed": 101,
                "attempt": 1,
                "execution_configuration_digest": "digest-101",
                "exit_code": 2,
                "failure_class": "runtime_or_integrity_failure_pending_review",
                "diagnostic_digest": "error-101",
                "candidate_scientific_effect": "none_operational_only",
            },
        ]
        ledger = _retry_ledger_payload(freeze=freeze, failures=failures)
        validate_retry_ledger(ledger, freeze=freeze)
        self.assertEqual(ledger["retry_authorizations"][0]["seed"], 101)

    def test_retry_ledger_rejects_authored_seed_substitution(self) -> None:
        freeze = build_exec_freeze(
            execution_binding_path=self.binding_path,
            allow_dirty_preview=True,
        )
        failures = [
            {
                "cell_id": "reference",
                "seed": 101,
                "attempt": 1,
                "execution_configuration_digest": "digest-101",
                "exit_code": 2,
                "failure_class": "runtime_or_integrity_failure_pending_review",
                "diagnostic_digest": "error-101",
                "candidate_scientific_effect": "none_operational_only",
            }
        ]
        ledger = _retry_ledger_payload(freeze=freeze, failures=failures)
        ledger["retry_authorizations"][0]["seed"] = 307
        with self.assertRaises(ContractError):
            validate_retry_ledger(ledger, freeze=freeze)

    def test_freeze_builder_does_not_bind_or_import_runtime(self) -> None:
        with patch(
            "p2_i1_execution.bind_runtime",
            side_effect=AssertionError("runtime must remain untouched"),
        ):
            freeze = build_exec_freeze(
                execution_binding_path=self.binding_path,
                allow_dirty_preview=True,
            )
        self.assertFalse(freeze["candidate_execution_performed_at_freeze"])

    def test_incomplete_matrix_cannot_pass_any_live_obligation(self) -> None:
        freeze = build_exec_freeze(
            execution_binding_path=self.binding_path,
            allow_dirty_preview=True,
        )
        missing = [row["run_id"] for row in freeze["run_specs"]]
        with patch("p2_i1_execution.validate_exec_freeze"), patch(
            "p2_i1_execution._load_effective_runs",
            return_value=([], missing),
        ):
            audit = build_cycle_audit(policy=self.policy, freeze=freeze)
        self.assertFalse(audit["audit_complete"])
        self.assertTrue(
            all(
                row["status"] == "blocked_or_incomplete"
                for row in audit["obligation_results"]
            )
        )


if __name__ == "__main__":
    unittest.main()
