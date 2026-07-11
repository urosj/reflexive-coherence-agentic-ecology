from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
from types import ModuleType
import unittest
from unittest.mock import patch

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

from ae01_tooling import ContractError, load_json  # noqa: E402
from p2_i1 import (  # noqa: E402
    CONFIG_PATHS,
    analyze_records,
    build_cal_pre_identity,
    validate_configs,
)
from p2_i1_analysis import (  # noqa: E402
    aggregate_seed,
    generate_matched_null,
    paired_margin,
    policy_projection_digests,
    resolved_profile_identity,
    selectivity_interaction,
    static_profile_identities,
    validate_cross_cell_static_profile_matching,
    validate_analysis_policy,
    validate_opportunity,
)
from p2_i1_runtime import (  # noqa: E402
    bind_runtime,
    resolve_node_coherences,
    resolve_reader_packet_amount,
    validate_runtime_operation_capabilities,
)


class P2I1Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.configs = {
            name: load_json(EXPERIMENT / path) for name, path in CONFIG_PATHS.items()
        }

    def _opportunity(
        self,
        *,
        seed: int = 101,
        cell: str = "candidate-conditioning",
        index: int,
        response: int | None,
        status: str = "observed",
    ) -> dict[str, object]:
        context = "A" if index < 2 else "B"
        group = "aligned" if index % 2 == 0 else "inverted"
        profile = f"ctx-{context.casefold()}-{group}"
        scientific = status in {"observed", "inadmissible", "structurally_unavailable"}
        return {
            "opportunity_id": f"{cell}-{seed}-{index}",
            "seed": seed,
            "cell_id": cell,
            "relation_chain_id": f"chain-{cell}-{seed}-{index}",
            "writer_carrier_id": f"participant-{seed}",
            "writer_event_id": f"writer-{seed}",
            "medium_surface_id": f"medium-{cell}-{seed}",
            "medium_change_event_id": f"medium-event-{cell}-{seed}",
            "medium_history_digest": f"history-{cell}-{seed}",
            "later_opportunity_event_id": f"later-{cell}-{seed}-{index}",
            "reader_or_local_differentiation_id": f"reader-{context}",
            "opportunity_index": index,
            "profile_id": profile,
            "context": context,
            "selectivity_group": group,
            "raw_response": response,
            "oriented_response": response,
            "admissibility": "admissible" if scientific else "not_evaluable",
            "opportunity_status": status,
            "complete_registered_chain": response == 1,
            "causal_order_verified": response == 1,
            "medium_dependency_control_refs": ["AE01-CTRL-06"],
        }

    def _panel(
        self,
        values: list[int | None],
        *,
        seed: int = 101,
        cell: str = "candidate-conditioning",
        statuses: list[str] | None = None,
    ) -> list[dict[str, object]]:
        status_values = statuses or ["observed"] * 4
        return [
            self._opportunity(
                seed=seed,
                cell=cell,
                index=index,
                response=value,
                status=status_values[index],
            )
            for index, value in enumerate(values)
        ]

    def test_configs_validate_and_do_not_authorize_execution(self) -> None:
        result = validate_configs(self.configs)
        self.assertEqual(result["status"], "passed")
        self.assertFalse(result["candidate_execution_authorized"])
        self.assertFalse(self.configs["runtime"]["candidate_execution_authorized"])
        self.assertEqual(
            self.configs["runtime"]["candidate_execution_authorization_mode"],
            "explicit_cycle_exec_freeze_only",
        )
        self.assertTrue(self.configs["runtime"]["execution_freeze_required"])
        self.assertEqual(
            self.configs["runtime"]["execution_freeze_gate"],
            "P2-I1-EXEC-FREEZE",
        )
        self.assertEqual(
            self.configs["runtime"]["execution_close_gate"],
            "P2-I1-EXEC-GATE",
        )

    def test_parent_context_transform_preserves_score_and_reduces_support(self) -> None:
        for seed in (101, 211, 307):
            with self.subTest(seed=seed):
                candidate = resolve_node_coherences(
                    self.configs["fixture"],
                    seed,
                    "candidate-conditioning",
                    self.configs["cells"],
                )
                support = resolve_node_coherences(
                    self.configs["fixture"],
                    seed,
                    "parent-context-contrast",
                    self.configs["cells"],
                )
                candidate_score = (candidate["W"] + 0.25) - (
                    candidate["A"] + candidate["B"]
                )
                support_score = (support["W"] + 0.25) - (
                    support["A"] + support["B"]
                )
                self.assertEqual(candidate_score, support_score)
                self.assertEqual(candidate["P"], support["P"])
                self.assertEqual(support["A"], 0.25)
                self.assertEqual(support["B"], 0.25)
                self.assertEqual(
                    sum(candidate.values()) - sum(support.values()), 1.0
                )

    def test_carrier_load_override_is_separate_from_coherence_transform(self) -> None:
        candidate = resolve_node_coherences(
            self.configs["fixture"],
            211,
            "candidate-conditioning",
            self.configs["cells"],
        )
        contrast = resolve_node_coherences(
            self.configs["fixture"],
            211,
            "carrier-timescale-contrast",
            self.configs["cells"],
        )
        self.assertEqual(candidate, contrast)
        self.assertEqual(
            resolve_reader_packet_amount(
                self.configs["fixture"],
                self.configs["cells"],
                "candidate-conditioning",
            ),
            0.125,
        )
        self.assertEqual(
            resolve_reader_packet_amount(
                self.configs["fixture"],
                self.configs["cells"],
                "carrier-timescale-contrast",
            ),
            0.25,
        )

    def test_analysis_policy_rejects_unknown_top_level_field(self) -> None:
        bad = deepcopy(self.configs["analysis"])
        bad["silent_extension"] = True
        with self.assertRaises(ContractError):
            validate_analysis_policy(bad)

    def test_analysis_policy_rejects_unknown_projection_field(self) -> None:
        bad = deepcopy(self.configs["analysis"])
        bad["rung_classifier_policy"]["silent_extension"] = True
        with self.assertRaises(ContractError):
            validate_analysis_policy(bad)

    def test_calibration_provenance_prohibits_pygrc_and_candidate_inputs(self) -> None:
        bad = deepcopy(self.configs)
        bad["provenance"]["dependency_profile"][
            "pygrc_required_for_calibration"
        ] = True
        with self.assertRaises(ContractError):
            validate_configs(bad)
        bad = deepcopy(self.configs)
        bad["provenance"]["input_identity_policy"][
            "candidate_artifacts_allowed"
        ] = True
        with self.assertRaises(ContractError):
            validate_configs(bad)

    def test_seed_aggregation_preserves_fixed_denominator_and_counts(self) -> None:
        aggregate = aggregate_seed(
            self._panel([1, 0, 1, 0]), self.configs["analysis"]
        )
        self.assertEqual(aggregate["formation_fraction"], 0.5)
        self.assertEqual(aggregate["formed_count"], 2)
        self.assertEqual(aggregate["planned_count"], 4)
        self.assertEqual(aggregate["status_counts"]["observed"], 4)

    def test_operational_missingness_invalidates_whole_seed(self) -> None:
        panel = self._panel(
            [1, 0, 1, None],
            statuses=["observed", "observed", "observed", "censored_runtime"],
        )
        aggregate = aggregate_seed(panel, self.configs["analysis"])
        self.assertFalse(aggregate["evaluable"])
        self.assertIsNone(aggregate["formation_fraction"])
        self.assertEqual(aggregate["status_counts"]["censored_runtime"], 1)

    def test_structural_unavailability_is_scientific_zero(self) -> None:
        panel = self._panel(
            [1, 0, 0, 0],
            statuses=["observed", "observed", "structurally_unavailable", "observed"],
        )
        aggregate = aggregate_seed(panel, self.configs["analysis"])
        self.assertTrue(aggregate["evaluable"])
        self.assertEqual(aggregate["formation_fraction"], 0.25)

    def test_formation_requires_complete_ordered_chain(self) -> None:
        record = self._opportunity(index=0, response=1)
        record["causal_order_verified"] = False
        with self.assertRaises(ContractError):
            validate_opportunity(record)

    def test_paired_margin_retains_sparse_coverage(self) -> None:
        candidate = aggregate_seed(
            self._panel([1, 0, 0, 0]), self.configs["analysis"]
        )
        comparator = aggregate_seed(
            self._panel([0, 0, 0, 0], cell="reference"),
            self.configs["analysis"],
        )
        result = paired_margin(candidate, comparator, self.configs["analysis"])
        self.assertEqual(result["candidate_fraction"], 0.25)
        self.assertEqual(result["raw_paired_difference"], 0.25)
        self.assertEqual(result["normalized_margin"], 1.0)

    def test_analysis_derives_frozen_comparison_roles_without_authored_selection(self) -> None:
        records = []
        for seed in (101, 211, 307):
            records.extend(
                self._panel(
                    [1, 0, 1, 0], seed=seed, cell="candidate-conditioning"
                )
            )
            records.extend(self._panel([0, 0, 0, 0], seed=seed, cell="reference"))
            records.extend(
                self._panel(
                    [0, 0, 0, 0],
                    seed=seed,
                    cell="medium-freeze-withdrawal",
                )
            )
        result = analyze_records(
            {"opportunity_records": records}, self.configs["analysis"]
        )
        self.assertTrue(result["analysis_completeness"]["complete"])
        self.assertEqual(len(result["paired_margins"]), 6)
        roles = {row["metric_role"] for row in result["paired_margins"]}
        self.assertEqual(
            roles, {"primary_normalized_margin", "causal_control_diagnostic"}
        )
        primary = [
            row for row in result["paired_margins"]
            if row["metric_role"] == "primary_normalized_margin"
        ]
        self.assertTrue(all(row["comparator_cell_id"] == "reference" for row in primary))
        self.assertEqual(len(result["selectivity_results"]), 3)

    def test_analysis_rejects_authored_comparison_selection(self) -> None:
        with self.assertRaises(ContractError):
            analyze_records(
                {"opportunity_records": [], "paired_comparisons": []},
                self.configs["analysis"],
            )

    def test_matched_null_uses_all_discrete_fractions_and_freezes_expected_delta(self) -> None:
        result = generate_matched_null(
            self.configs["calibration"], self.configs["analysis"]
        )
        self.assertEqual(
            [row["null_a"]["formation_fraction"] for row in result["panel_results"]],
            [0.0, 0.25, 0.5, 0.75, 1.0],
        )
        self.assertEqual(
            [row["matched_null_margin"] for row in result["seed_margins"]],
            [0.0] * 5,
        )
        self.assertEqual(result["delta"], 1e-12)
        self.assertFalse(result["runtime_execution"])
        self.assertFalse(result["pygrc_imported"])

    def test_selectivity_keeps_pair_disagreement_visible(self) -> None:
        candidate = self._panel([1, 0, 0, 1])
        comparator = self._panel(
            [0, 0, 0, 0], cell="medium-freeze-withdrawal"
        )
        result = selectivity_interaction(candidate, comparator)
        self.assertEqual(result["selectivity_relation"], "mixed")
        self.assertEqual(
            [row["pair_interaction"] for row in result["pair_interactions"]],
            [1, -1],
        )
        self.assertFalse(result["uses_calibrated_delta"])

    def test_zero_selectivity_pairs_are_generic_or_no_effect_not_weak(self) -> None:
        candidate = self._panel([0, 0, 0, 0])
        comparator = self._panel(
            [0, 0, 0, 0], cell="medium-freeze-withdrawal"
        )
        result = selectivity_interaction(candidate, comparator)
        self.assertEqual(result["selectivity_margin"], 0.0)
        self.assertEqual(
            result["selectivity_relation"], "generic_main_effect_or_no_effect"
        )

    def test_static_profiles_have_four_profile_and_two_reader_identities(self) -> None:
        identities = static_profile_identities(self.configs["fixture"])
        self.assertEqual(len({row["opportunity_profile_digest"] for row in identities}), 4)
        self.assertEqual(len({row["reader_configuration_digest"] for row in identities}), 2)

    def test_cross_cell_static_profile_matching_fails_on_drift(self) -> None:
        identities = static_profile_identities(self.configs["fixture"])
        panels = {
            cell["cell_id"]: deepcopy(identities)
            for cell in self.configs["cells"]["cells"]
        }
        validate_cross_cell_static_profile_matching(panels)
        panels["trace-shuffle"][0]["opportunity_profile_digest"] = "drifted"
        with self.assertRaises(ContractError):
            validate_cross_cell_static_profile_matching(panels)

    def test_resolved_profile_identity_binds_lineage_and_rejects_carryover(self) -> None:
        static = static_profile_identities(self.configs["fixture"])[0]
        first = resolved_profile_identity(
            static,
            pulse_contact_surface_digest="pulse-arrival",
            medium_history_digest="medium-candidate",
            branch_point_snapshot_digest="branch-point",
            restored_snapshot_digest="branch-point",
            cross_branch_state_carryover=False,
        )
        second = resolved_profile_identity(
            static,
            pulse_contact_surface_digest="pulse-arrival",
            medium_history_digest="medium-reference",
            branch_point_snapshot_digest="branch-point",
            restored_snapshot_digest="branch-point",
            cross_branch_state_carryover=False,
        )
        self.assertEqual(
            first["opportunity_profile_digest"], second["opportunity_profile_digest"]
        )
        self.assertNotEqual(
            first["resolved_opportunity_profile_digest"],
            second["resolved_opportunity_profile_digest"],
        )
        with self.assertRaises(ContractError):
            resolved_profile_identity(
                static,
                pulse_contact_surface_digest="pulse-arrival",
                medium_history_digest="medium-candidate",
                branch_point_snapshot_digest="branch-point",
                restored_snapshot_digest="branch-point",
                cross_branch_state_carryover=True,
            )
        with self.assertRaises(ContractError):
            resolved_profile_identity(
                static,
                pulse_contact_surface_digest="pulse-arrival",
                medium_history_digest="medium-candidate",
                branch_point_snapshot_digest="branch-point",
                restored_snapshot_digest="different-branch",
                cross_branch_state_carryover=False,
            )

    def test_policy_projection_digests_are_stable_and_distinct(self) -> None:
        first = policy_projection_digests(self.configs["analysis"])
        second = policy_projection_digests(self.configs["analysis"])
        self.assertEqual(first, second)
        self.assertEqual(len(set(first.values())), 3)

    def test_cal_pre_identity_contains_no_absolute_paths_or_candidate_authority(self) -> None:
        with patch("p2_i1._git_worktree_status", return_value=[" M review-change"]):
            identity = build_cal_pre_identity(
                self.configs, allow_dirty_preview=True
            )
        serialized = json.dumps(identity)
        self.assertFalse(identity["candidate_execution_authorized"])
        self.assertTrue(identity["candidate_outcomes_absent"])
        self.assertFalse(identity["retention_eligible"])
        self.assertEqual(
            identity["identity_id"],
            "rcae-p2-i1-cal-pre-identity-preview-v2",
        )
        self.assertEqual(
            identity["supersedes_identity_id"],
            "rcae-p2-i1-cal-pre-identity-v1",
        )
        self.assertNotIn(str(ROOT), serialized)
        self.assertNotIn("graph-reflexive-coherence", serialized)

    def test_cal_pre_freeze_identity_rejects_dirty_worktree(self) -> None:
        with patch("p2_i1._git_worktree_status", return_value=[" M fixture"]):
            with self.assertRaises(ContractError):
                build_cal_pre_identity(self.configs)

    def test_cal_pre_freeze_identity_is_retention_eligible_only_when_clean(self) -> None:
        with patch("p2_i1._git_worktree_status", return_value=[]):
            identity = build_cal_pre_identity(self.configs)
        self.assertTrue(identity["source_tree_clean"])
        self.assertTrue(identity["retention_eligible"])
        self.assertEqual(identity["working_tree_change_count"], 0)

    def test_runtime_binding_fails_closed_when_profile_is_unavailable(self) -> None:
        profile = {
            "availability": False,
            "enabled": False,
            "supported": False,
            "validated": False,
            "required_pygrc_identity": "pygrc==0.1",
            "allowed_scheduling_operations": [],
        }
        calls: list[str] = []

        def importer(name: str) -> ModuleType:
            calls.append(name)
            return ModuleType(name)

        with self.assertRaises(ContractError):
            bind_runtime(
                self.configs["runtime"],
                profile,
                importer=importer,
                version_reader=lambda name: "0.1",
            )
        self.assertEqual(calls, [])

    def test_runtime_binding_validates_public_facades_without_path_capture(self) -> None:
        root = ModuleType("pygrc")
        root.PUBLIC_API_SURFACES = {"pygrc.core": "core", "pygrc.models": "models"}
        core = ModuleType("pygrc.core")
        core.PortGraphBackend = object
        models = ModuleType("pygrc.models")

        class RuntimeFacade:
            from_state = staticmethod(lambda *args, **kwargs: None)
            get_state = lambda self: None
            snapshot = lambda self: {}
            load = staticmethod(lambda *args, **kwargs: None)
            step = lambda self: None
            emit_feedback_eligibility_surface_row = lambda self, **kwargs: None
            set_feedback_coupled_pulse_producer = lambda self, **kwargs: None

        for symbol in (
            "GRC9V3NodeState",
            "GRC9V3State",
            "LGRC9V3",
            "LGRC9V3RouteAspect",
            "LGRC9V3RouteAspectChannel",
            "LGRC9V3RouteAspectHop",
            "PortEdge",
            "slot_to_port_id",
            "validate_lgrc9v3_route_aspect",
        ):
            setattr(models, symbol, object)
        models.LGRC9V3 = RuntimeFacade
        modules = {"pygrc": root, "pygrc.core": core, "pygrc.models": models}
        profile = {
            "availability": True,
            "enabled": True,
            "supported": True,
            "validated": True,
            "required_pygrc_identity": "pygrc==0.1",
            "allowed_scheduling_operations": [
                self.configs["runtime"]["preflight_operation_id"],
                *self.configs["runtime"]["required_operations"],
            ],
        }
        bound = bind_runtime(
            self.configs["runtime"],
            profile,
            importer=lambda name: modules[name],
            version_reader=lambda name: "0.1",
        )
        self.assertEqual(set(bound), {"pygrc", "core", "models"})

    def test_runtime_operation_conformance_rejects_missing_native_method(self) -> None:
        models = ModuleType("pygrc.models")

        class IncompleteRuntime:
            from_state = staticmethod(lambda *args, **kwargs: None)
            get_state = lambda self: None
            snapshot = lambda self: {}
            load = staticmethod(lambda *args, **kwargs: None)
            step = lambda self: None
            emit_feedback_eligibility_surface_row = lambda self, **kwargs: None

        models.LGRC9V3 = IncompleteRuntime
        models.validate_lgrc9v3_route_aspect = lambda *args, **kwargs: None
        operations = [
            self.configs["runtime"]["preflight_operation_id"],
            *self.configs["runtime"]["required_operations"],
        ]
        with self.assertRaises(ContractError):
            validate_runtime_operation_capabilities({"models": models}, operations)


if __name__ == "__main__":
    unittest.main()
