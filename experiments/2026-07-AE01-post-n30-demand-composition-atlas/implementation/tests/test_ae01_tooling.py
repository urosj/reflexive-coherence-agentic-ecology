from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
from types import ModuleType
import unittest


ROOT = Path(__file__).resolve().parents[4]
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
SCRIPTS = EXPERIMENT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ae01_tooling import (  # noqa: E402
    COMMON_CONTROL_IDS,
    ContractError,
    FAILURE_IDS,
    LANE_CONTROL_IDS,
    LANE_IDS,
    ReadOnlyTreeGuard,
    assemble_report,
    assert_synthesis_entry,
    build_artifact_inspection_receipt,
    build_artifact_manifest,
    build_runtime_binding_receipt,
    canonical_json_dumps,
    canonicalize_json_value,
    classify_threshold_relation,
    deterministic_id,
    digest_canonical_data,
    load_json,
    freeze_metric_resolution,
    pretty_json_dumps,
    resolve_execution_policy,
    validate_execution_policy,
    validate_interpretation_policy,
    validate_lane_projections,
    validate_portable_path,
    validate_record,
    validate_semantics,
)


class AE01ToolingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_json(
            EXPERIMENT / "contracts/schemas/ae01-contract.schema.json"
        )
        cls.registry = load_json(EXPERIMENT / "contracts/lane-registry.json")
        cls.profiles = load_json(EXPERIMENT / "configs/p1_i5_profiles.json")
        cls.policy = load_json(EXPERIMENT / "configs/p1_i5_execution_policy.json")
        cls.interpretation_policy = load_json(
            EXPERIMENT / "configs/p1_i4_developmental_interpretation_policy.json"
        )
        cls.metric_sheet = load_json(
            EXPERIMENT / "contracts/metric-sheets/AE01-L01.json"
        )

    def test_canonical_json_is_order_independent(self) -> None:
        left = {"b": [2, 1], "a": {"z", "x"}}
        right = {"a": {"x", "z"}, "b": [2, 1]}
        self.assertEqual(canonical_json_dumps(left), canonical_json_dumps(right))
        self.assertEqual(digest_canonical_data(left), digest_canonical_data(right))

    def test_canonical_json_matches_pygrc_profile(self) -> None:
        self.assertEqual(canonical_json_dumps({"b": 2, "a": 1}), '{"a":1,"b":2}')
        self.assertTrue(pretty_json_dumps({"b": 2, "a": 1}).endswith("\n"))

    def test_canonical_json_rejects_unsupported_values(self) -> None:
        with self.assertRaises(ContractError):
            canonicalize_json_value({1: "not a string key"})
        with self.assertRaises(ContractError):
            canonicalize_json_value(float("nan"))

    def test_deterministic_id_is_stable_and_sensitive(self) -> None:
        first = deterministic_id("fixture", {"a": 1})
        self.assertEqual(first, deterministic_id("fixture", {"a": 1}))
        self.assertNotEqual(first, deterministic_id("fixture", {"a": 2}))

    def test_portable_paths(self) -> None:
        self.assertEqual(validate_portable_path("experiments/example.json"), "experiments/example.json")
        self.assertEqual(validate_portable_path("."), ".")
        invalid = [
            f"{chr(47)}tmp{chr(47)}artifact.json",
            "C:\\artifact.json",
            "../artifact.json",
            "folder//artifact.json",
            "~/artifact.json",
        ]
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(ContractError):
                validate_portable_path(value)

    def test_valid_fixtures_pass(self) -> None:
        for path in sorted((EXPERIMENT / "contracts/fixtures/valid").glob("*.json")):
            with self.subTest(path=path.name):
                validate_record(load_json(path), self.schema)

    def test_invalid_fixtures_fail(self) -> None:
        for path in sorted((EXPERIMENT / "contracts/fixtures/invalid").glob("*.json")):
            with self.subTest(path=path.name), self.assertRaises(ContractError):
                validate_record(load_json(path), self.schema)

    def test_profiles_validate(self) -> None:
        validate_record(self.profiles, self.schema)

    def test_conceptual_source_cannot_become_runtime_or_positive_evidence(self) -> None:
        record = load_json(
            EXPERIMENT
            / "contracts/fixtures/valid/conceptual-source-negative.json"
        )
        record["record"]["sources"][0]["runtime_evidence_permission"] = True
        record["record"]["sources"][0]["positive_evidence_permission"] = True
        with self.assertRaises(ContractError):
            validate_record(record, self.schema)

    def test_unsafe_claim_flag_fails(self) -> None:
        record = deepcopy(self.registry)
        record["record"]["claim_boundary"]["unsafe_flags"][
            "positive_atlas_evidence_opened"
        ] = True
        with self.assertRaises(ContractError):
            validate_record(record, self.schema)

    def test_lane_registry_and_projections_validate(self) -> None:
        validate_record(self.registry, self.schema)
        validate_lane_projections(self.registry, ROOT)

    def _projection_registry(self, path: str) -> dict[str, object]:
        result = deepcopy(self.registry)
        result["record"]["projection_targets"] = [
            {
                "path": path,
                "projection_role": "test",
                "consistency_status": "validated",
            }
        ]
        return result

    def _projection_text(self, rows: list[tuple[str, str]]) -> str:
        header = "| Stable ID | Current display name | Detail |\n| --- | --- | --- |\n"
        return header + "".join(
            f"| `{lane_id}` | {name} | fixture |\n" for lane_id, name in rows
        )

    def test_projection_missing_duplicate_stale_and_reordered_fail(self) -> None:
        rows = [
            (lane["lane_id"], lane["current_display_name"])
            for lane in self.registry["record"]["lanes"]
        ]
        cases = {
            "missing": rows[:-1],
            "duplicate": rows + [rows[-1]],
            "stale": [(rows[0][0], "Stale lane name"), *rows[1:]],
            "reordered": [rows[1], rows[0], *rows[2:]],
        }
        for name, case_rows in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                path = root / "projection.md"
                path.write_text(self._projection_text(case_rows), encoding="utf-8")
                with self.assertRaises(ContractError):
                    validate_lane_projections(
                        self._projection_registry("projection.md"), root
                    )

    def test_execution_policy_is_complete_and_deterministic(self) -> None:
        validate_execution_policy(self.policy)
        first = resolve_execution_policy(self.policy)
        second = resolve_execution_policy(self.policy)
        self.assertEqual(first, second)
        self.assertEqual([lane["lane_id"] for lane in first["lanes"]], list(LANE_IDS))
        for lane in first["lanes"]:
            self.assertEqual(len(lane["comparison_cells"]), 7)
            self.assertEqual(
                set(lane["common_control_applicability"]), set(COMMON_CONTROL_IDS)
            )
            self.assertEqual(
                set(lane["lane_control_ids"]), set(LANE_CONTROL_IDS[lane["lane_id"]])
            )

    def test_interpretation_policy_and_metric_sheets_are_complete(self) -> None:
        validate_interpretation_policy(self.interpretation_policy)
        sheets = sorted((EXPERIMENT / "contracts/metric-sheets").glob("*.json"))
        self.assertEqual(len(sheets), 7)
        for path in sheets:
            validate_record(load_json(path), self.schema)

    def test_execution_policy_mutations_fail(self) -> None:
        bad = deepcopy(self.policy)
        bad["global_policy"]["deterministic_seeds"].append(401)
        with self.assertRaises(ContractError):
            validate_execution_policy(bad)
        bad = deepcopy(self.policy)
        bad["lanes"][0]["comparison_cells"].pop()
        with self.assertRaises(ContractError):
            validate_execution_policy(bad)
        bad = deepcopy(self.policy)
        bad["lanes"][0]["comparison_cells"][1]["cell_id"] = "reference"
        with self.assertRaises(ContractError):
            validate_execution_policy(bad)
        bad = deepcopy(self.policy)
        bad["lanes"][0]["comparison_cells"][6]["group"] = "candidate"
        with self.assertRaises(ContractError):
            validate_execution_policy(bad)
        bad = deepcopy(self.policy)
        bad["non_selection_conditions"].pop()
        with self.assertRaises(ContractError):
            validate_execution_policy(bad)

    def test_vocabulary_is_closed(self) -> None:
        self.assertEqual(len(COMMON_CONTROL_IDS), 19)
        self.assertEqual(len(FAILURE_IDS), 10)
        self.assertTrue(all(len(values) == 5 for values in LANE_CONTROL_IDS.values()))

    def test_threshold_relations_form_an_explicit_ladder(self) -> None:
        cases = {
            "robust_aligned": [0.08, 0.07, 0.09],
            "narrow_aligned": [0.08, 0.03, 0.06],
            "resolution_limited": [0.02, -0.03, 0.01],
            "mixed_direction": [0.08, -0.02, 0.06],
            "narrow_counter": [-0.08, -0.03, -0.06],
            "robust_counter": [-0.08, -0.07, -0.09],
        }
        for expected, margins in cases.items():
            with self.subTest(expected=expected):
                relation = classify_threshold_relation(
                    [
                        {"seed": seed, "margin": margin}
                        for seed, margin in zip((101, 211, 307), margins, strict=True)
                    ],
                    delta=0.04,
                )
                self.assertEqual(relation, expected)
        self.assertEqual(
            classify_threshold_relation(
                [{"seed": 101, "margin": 0.08}], delta=None
            ),
            "resolution_unknown",
        )

    def test_metric_resolution_freeze_is_candidate_blind_and_deterministic(self) -> None:
        calibration_input = {
            "candidate_blind": True,
            "seed_margins": [
                {"seed": seed, "matched_null_margin": margin}
                for seed, margin in zip(
                    (19, 43, 71, 109, 163),
                    (0.01, -0.04, 0.02, -0.03, 0.01),
                    strict=True,
                )
            ],
        }
        first = freeze_metric_resolution(self.metric_sheet, calibration_input)
        second = freeze_metric_resolution(self.metric_sheet, calibration_input)
        self.assertEqual(first, second)
        calibration, frozen_sheet = first
        validate_record(calibration, self.schema)
        validate_record(frozen_sheet, self.schema)
        self.assertEqual(calibration["record"]["delta"], 0.04)
        self.assertEqual(
            frozen_sheet["record"]["resolution_policy"]["status"], "frozen"
        )
        bad = deepcopy(calibration_input)
        bad["candidate_blind"] = False
        with self.assertRaises(ContractError):
            freeze_metric_resolution(self.metric_sheet, bad)

    def test_developmental_interpretation_guards_next_move(self) -> None:
        interpretation = load_json(
            EXPERIMENT
            / "contracts/fixtures/valid/narrow-developmental-interpretation.json"
        )
        validate_record(interpretation, self.schema)
        bad = deepcopy(interpretation)
        bad["record"]["classification_value"] = {
            "rung": "T0_observation_tag",
            "organizes_next_iteration": False,
            "rationale": "Deliberate local-only mutation",
        }
        with self.assertRaises(ContractError):
            validate_record(bad, self.schema)
        bad = deepcopy(interpretation)
        bad["record"]["next_move"]["disposition"] = "bounded_local_refinement"
        with self.assertRaises(ContractError):
            validate_record(bad, self.schema)
        guarded = deepcopy(interpretation)
        guarded["record"]["next_move"]["disposition"] = "bounded_local_refinement"
        guarded["record"]["local_optimization_guard"] = {
            "status": "applicable",
            "same_causal_question": True,
            "function_not_proxy": True,
            "one_bounded_change": True,
            "preserves_prior_result": True,
            "falsifiable": True,
            "advances": ["withdrawal_resistance"],
            "rationale": "One bounded support weakening tests the disclosed function",
        }
        validate_record(guarded, self.schema)

    def _realization(self) -> dict[str, object]:
        return load_json(
            EXPERIMENT
            / "contracts/fixtures/valid/unavailable-realization-profile.json"
        )["record"]

    def test_live_runtime_binding_passes_with_exact_fake_runtime(self) -> None:
        module = ModuleType("pygrc")
        module.PUBLIC_API_SURFACES = {
            "pygrc.core": "core",
            "pygrc.models": "models",
        }
        realization = self._realization()
        realization["availability"] = True
        realization["enabled"] = True
        receipt = build_runtime_binding_receipt(
            realization,
            run_id="fixture-live-pass",
            execution_class="pygrc_runtime_with_rcae_producer",
            requested_operations=["fixture_binding_check"],
            importer=lambda name: module,
            version_reader=lambda name: "0.1",
        )
        validate_record(receipt, self.schema)
        self.assertEqual(receipt["record"]["conformance_status"], "passed")
        self.assertNotIn("path", json.dumps(receipt).casefold())

    def test_live_runtime_binding_fails_without_runtime_and_does_not_fallback(self) -> None:
        calls: list[str] = []

        def missing(name: str) -> ModuleType:
            calls.append(name)
            raise ModuleNotFoundError(name)

        realization = self._realization()
        realization["availability"] = True
        realization["enabled"] = True
        receipt = build_runtime_binding_receipt(
            realization,
            run_id="fixture-live-missing",
            execution_class="pygrc_runtime_with_rcae_producer",
            requested_operations=["fixture_binding_check"],
            importer=missing,
            version_reader=lambda name: "0.1",
        )
        validate_record(receipt, self.schema)
        self.assertEqual(calls, ["pygrc"])
        self.assertEqual(receipt["record"]["conformance_status"], "failed")
        self.assertEqual(receipt["record"]["execution_class"], "pygrc_runtime_with_rcae_producer")
        self.assertIn("PyGRC runtime unavailable", receipt["record"]["failure"]["rationale"])

    def test_runtime_identity_and_capability_mismatch_fail(self) -> None:
        module = ModuleType("pygrc")
        module.PUBLIC_API_SURFACES = {"pygrc.core": "core"}
        realization = self._realization()
        realization["availability"] = True
        realization["enabled"] = True
        receipt = build_runtime_binding_receipt(
            realization,
            run_id="fixture-live-mismatch",
            execution_class="pygrc_runtime_with_rcae_producer",
            requested_operations=["fixture_binding_check"],
            importer=lambda name: module,
            version_reader=lambda name: "9.9",
        )
        self.assertEqual(receipt["record"]["conformance_status"], "failed")
        receipt = build_runtime_binding_receipt(
            realization,
            run_id="fixture-live-operation-mismatch",
            execution_class="pygrc_native_runtime",
            requested_operations=["undeclared_operation"],
            importer=lambda name: module,
            version_reader=lambda name: "0.1",
        )
        self.assertEqual(receipt["record"]["conformance_status"], "failed")
        self.assertIn("execution class", receipt["record"]["failure"]["rationale"])
        disabled = self._realization()
        receipt = build_runtime_binding_receipt(
            disabled,
            run_id="fixture-live-disabled",
            execution_class="pygrc_runtime_with_rcae_producer",
            requested_operations=["fixture_binding_check"],
            importer=lambda name: module,
            version_reader=lambda name: "0.1",
        )
        self.assertEqual(receipt["record"]["conformance_status"], "failed")
        self.assertIn("declares the runtime unavailable", receipt["record"]["failure"]["rationale"])

    def test_artifact_inspection_is_non_runtime(self) -> None:
        receipt = build_artifact_inspection_receipt(run_id="fixture-inspection")
        validate_record(receipt, self.schema)
        self.assertEqual(
            receipt["record"]["conformance_status"], "not_applicable_non_runtime"
        )
        self.assertNotIn("profile_id", receipt["record"])

    def test_read_only_guard_accepts_reads_and_rejects_writes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.txt"
            source.write_text("before", encoding="utf-8")
            with ReadOnlyTreeGuard(root):
                self.assertEqual(source.read_text(encoding="utf-8"), "before")
            with self.assertRaises(ContractError):
                with ReadOnlyTreeGuard(root):
                    source.write_text("after", encoding="utf-8")

    def _manifest_declaration(self, path: str, *, tier: str, claims: list[str]) -> dict[str, object]:
        return {
            "artifact_id": "ae01-fixture-artifact",
            "expected_path": path,
            "command_profile_ref": "ae01-command-validate-phase1-v1",
            "working_directory": ".",
            "environment_profile_ref": "ae01-environment-python311-v1",
            "dependency_profile_ref": "ae01-dependencies-phase1-v1",
            "configuration_id": "ae01-fixture-config",
            "input_digests": {},
            "random_seeds": [],
            "execution_class": "artifact_inspection",
            "realization_profile": {
                "status": "not_applicable",
                "rationale": "Artifact inspection has no live realization",
            },
            "artifact_kind": "fixture_json",
            "schema_version": "1.1.0",
            "retention_mode": "tracked_selected_evidence",
            "resource_profile_ref": "ae01-resource-phase1-v1",
            "verification_command_profile_ref": "ae01-command-validate-phase1-v1",
            "evidence_use_tier": tier,
            "claim_dependency_refs": claims,
        }

    def test_manifest_generation_and_duplicate_reconstruction_are_stable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            artifact = root / "artifact.json"
            artifact.write_text('{"b":2,"a":1}\n', encoding="utf-8")
            declaration = self._manifest_declaration(
                "artifact.json", tier="retained_evidence", claims=["fixture-claim"]
            )
            kwargs = {
                "manifest_id": "ae01-fixture-manifest",
                "profile_registry": self.profiles,
                "declarations": [declaration],
                "repository_root": root,
                "source_revisions": {"rcae": "0" * 40},
            }
            first = build_artifact_manifest(**kwargs)
            second = build_artifact_manifest(**kwargs)
            validate_record(first, self.schema)
            self.assertEqual(first, second)
            self.assertEqual(digest_canonical_data(first), digest_canonical_data(second))

            live_declaration = deepcopy(declaration)
            live_declaration["execution_class"] = "pygrc_runtime_with_rcae_producer"
            live_declaration["realization_profile"] = {
                "status": "applicable",
                "reference_id": "missing-realization",
                "rationale": "Live fixture declares its realization",
            }
            with self.assertRaises(ContractError):
                build_artifact_manifest(
                    manifest_id="ae01-fixture-live-manifest",
                    profile_registry=self.profiles,
                    declarations=[live_declaration],
                    repository_root=root,
                    source_revisions={"rcae": "0" * 40},
                )

    def test_scratch_and_registered_artifacts_cannot_support_claims(self) -> None:
        for tier in ("exploratory_scratch", "registered_probe"):
            with self.subTest(tier=tier), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / "artifact.json").write_text("{}\n", encoding="utf-8")
                declaration = self._manifest_declaration(
                    "artifact.json", tier=tier, claims=["fixture-claim"]
                )
                with self.assertRaises(ContractError):
                    build_artifact_manifest(
                        manifest_id="ae01-fixture-manifest",
                        profile_registry=self.profiles,
                        declarations=[declaration],
                        repository_root=root,
                        source_revisions={"rcae": "0" * 40},
                    )

    def test_negative_terminal_requires_completed_verified_evidence(self) -> None:
        record = {
            "schema_version": "1.1.0",
            "record_type": "terminal_classification",
            "record": {
                "terminal_record_id": "fixture-terminal",
                "lane_id": "AE01-L01",
                "classification": "not_supported",
                "stopping_condition": "fixture",
                "stopping_condition_reached": True,
                "attempted_work": [],
                "execution_status": "incomplete",
                "positive_signatures": [],
                "negative_signatures": ["fixture null"],
                "blocked_signatures": [],
                "missing_information": [],
                "control_refs": [],
                "retained_evidence_refs": [],
                "reconstruction_status": "not_available",
                "developmental_interpretation_ref": "fixture-interpretation",
                "debt_refs": [],
                "claim_impact": "none",
                "record_complete": True,
                "forces_n31_non_selection": False,
                "extensions": {},
            },
        }
        with self.assertRaises(ContractError):
            validate_record(record, self.schema)

    def _report_projection(self, mode: str) -> dict[str, object]:
        return {
            "schema_version": "1.1.0",
            "record_type": "report_projection",
            "record": {
                "report_id": "ae01-fixture-report",
                "mode": mode,
                "controlling_machine_record_refs": ["fixture-record"],
                "facts_projection": ["Fixture fact remains non-evidential"],
                "authored_sections": [] if mode == "generated_projection" else ["Interpretation"],
                "claim_boundary_ref": "fixture-claim-boundary",
                "blocked_statements": ["positive atlas evidence exists"],
                "assembly_profile_ref": "ae01-command-assemble-report-v1",
                "output_path": "outputs/fixture-report.md",
                "expected_output_digest": "0" * 64,
                "expected_file_sha256": "0" * 64,
                "consistency_status": "pending",
                "extensions": {},
            },
        }

    def test_report_assembly_is_deterministic_and_bounded(self) -> None:
        projection = self._report_projection("assembled_interpretation")
        validate_record(projection, self.schema)
        first = assemble_report(projection, authored_markdown="Bounded interpretation.")
        second = assemble_report(projection, authored_markdown="Bounded interpretation.")
        self.assertEqual(first, second)
        with self.assertRaises(ContractError):
            assemble_report(
                projection, authored_markdown="Positive atlas evidence exists."
            )

    def test_generated_report_rejects_authored_text(self) -> None:
        with self.assertRaises(ContractError):
            assemble_report(
                self._report_projection("generated_projection"),
                authored_markdown="Authored text",
            )

    def test_synthesis_requires_all_seven_terminal_records(self) -> None:
        records = [
            {
                "record_type": "terminal_classification",
                "record": {
                    "lane_id": lane_id,
                    "record_complete": True,
                    "developmental_interpretation_ref": f"interpretation-{lane_id}",
                },
            }
            for lane_id in LANE_IDS
        ]
        interpretations = [
            {
                "record_type": "developmental_interpretation",
                "record": {
                    "lane_id": lane_id,
                    "interpretation_id": f"interpretation-{lane_id}",
                },
            }
            for lane_id in LANE_IDS
        ]
        assert_synthesis_entry(records, interpretations)
        with self.assertRaises(ContractError):
            assert_synthesis_entry(records[:-1], interpretations)
        with self.assertRaises(ContractError):
            assert_synthesis_entry([*records[:-1], records[0]], interpretations)
        with self.assertRaises(ContractError):
            assert_synthesis_entry(records, interpretations[:-1])
        mismatched = deepcopy(interpretations)
        mismatched[0]["record"]["lane_id"] = "AE01-L02"
        with self.assertRaises(ContractError):
            assert_synthesis_entry(records, mismatched)

    def test_machine_local_path_in_record_fails_semantics(self) -> None:
        projection = self._report_projection("generated_projection")
        projection["record"]["output_path"] = f"{chr(47)}tmp{chr(47)}report.md"
        with self.assertRaises(ContractError):
            validate_semantics(projection)
        projection = self._report_projection("generated_projection")
        projection["record"]["facts_projection"] = [
            f"Generated from {chr(47)}tmp{chr(47)}private-result.json"
        ]
        with self.assertRaises(ContractError):
            validate_semantics(projection)

    def test_selected_ranking_requires_threshold_and_sensitivity_robustness(self) -> None:
        ranking = load_json(
            EXPERIMENT / "contracts/fixtures/valid/empty-ranking.json"
        )
        payload = ranking["record"]
        scores = {
            "cross_lane_recurrence": 2,
            "prerequisite_centrality": 2,
            "composition_leverage": 2,
            "transfer_value": 2,
            "gap_tension_specificity": 2,
            "future_discriminator_quality": 2,
            "control_feasibility": 2,
            "naturalization_debt_path": 2,
            "claim_safety": 2,
            "cost_feasibility": 2,
        }
        candidate = {
            "candidate_id": "ae01-fixture-candidate",
            "requirement_refs": ["ae01-fixture-requirement"],
            "lane_ids": ["AE01-L01"],
            "origin": "introduce",
            "eligibility_gates": {
                "classified_ae01_basis": True,
                "beyond_conceptual_motivation": True,
                "evidence_roles_separated": True,
                "operational_demand_defined": True,
                "discriminator_and_counterfactual_defined": True,
                "controls_feasible": True,
                "reconstruction_bounded": True,
                "no_unnamed_stronger_prerequisite": True,
            },
            "eligible": True,
            "scoring_status": "scored",
            "scores": scores,
            "group_totals": {
                "demand": 8,
                "experimental_readiness": 8,
                "safety_feasibility": 4,
            },
            "overall_total": 20,
            "threshold_checks": {
                "every_dimension": True,
                "demand": True,
                "experimental_readiness": True,
                "safety_feasibility": True,
                "overall": True,
                "critical_dimensions": True,
            },
            "threshold_passed": True,
            "tie_result": "not_in_tie_band",
            "tie_breaker_reached": "not_applicable",
            "sensitivity_profiles": [
                {"profile": "equal", "total": 20, "rank": 1, "wins_or_ties": True},
                {"profile": "doubled_demand", "total": 28, "rank": 1, "wins_or_ties": True},
                {"profile": "doubled_readiness_safety", "total": 32, "rank": 1, "wins_or_ties": True},
                {"profile": "conservative", "total": 20, "rank": 1, "wins_or_ties": True},
            ],
            "qualitative_rationale": "Fixture selection remains bounded",
            "investigator_prior": {
                "status": "not_applicable",
                "rationale": "No investigator prior used",
            },
            "ordering_disagreement": {
                "status": "not_applicable",
                "rationale": "No ordering disagreement",
            },
            "candidate_result": "selected",
        }
        payload["synthesis_refs"] = ["ae01-fixture-synthesis"]
        payload["candidates"] = [candidate]
        payload["selection_result"] = "selected"
        payload["selected_candidate"] = {
            "status": "selected",
            "candidate_id": "ae01-fixture-candidate",
            "rationale": "Fixture clears the frozen procedure",
        }
        payload["information_gathering_step"] = {
            "status": "not_applicable",
            "rationale": "A candidate was selected",
        }
        validate_record(ranking, self.schema)
        ranking["record"]["candidates"][0]["sensitivity_profiles"][3][
            "wins_or_ties"
        ] = False
        with self.assertRaises(ContractError):
            validate_record(ranking, self.schema)


if __name__ == "__main__":
    unittest.main()
