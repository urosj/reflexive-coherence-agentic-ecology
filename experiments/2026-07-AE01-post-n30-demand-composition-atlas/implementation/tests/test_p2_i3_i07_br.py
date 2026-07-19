from __future__ import annotations

import ast
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import jsonschema


def repository_root(start: Path) -> Path:
    resolved = start.resolve()
    for candidate in (resolved.parent, *resolved.parents):
        if (candidate / ".git").exists():
            return candidate
    raise RuntimeError("repository root could not be discovered")


ROOT = repository_root(Path(__file__))
SCRIPTS = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import p2_i3_br_execution_runtime as runtime


EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
POLICY_PATH = EXPERIMENT / "configs/p2_i3_br_i07_execution_policy.json"
SCHEMA_PATH = EXPERIMENT / "contracts/p2-i3/i07-br-execution-authority.schema.json"
REGISTRATION_PATH = EXPERIMENT / "contracts/p2-i3/i06-br-exact-registration.json"
FREEZE_SOURCE = EXPERIMENT / "scripts/p2_i3_i07_br_freeze.py"
VALIDATOR_SOURCE = EXPERIMENT / "scripts/p2_i3_i07_br_validate.py"
SUPERVISOR_SOURCE = EXPERIMENT / "scripts/p2_i3_i08_br_supervisor.py"
CASE_SOURCE = EXPERIMENT / "scripts/p2_i3_i08_br_case.py"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def tree(path: Path) -> ast.AST:
    return ast.parse(path.read_text(encoding="utf-8"), filename=path.as_posix())


def imported_roots(parsed: ast.AST) -> set[str]:
    roots: set[str] = set()
    for node in ast.walk(parsed):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def function_source(path: Path, name: str) -> str:
    source = path.read_text(encoding="utf-8")
    parsed = ast.parse(source, filename=path.as_posix())
    matches = [
        node
        for node in ast.walk(parsed)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name
    ]
    if len(matches) != 1:
        raise AssertionError(f"function {name!r} is not unique in {path}")
    segment = ast.get_source_segment(source, matches[0])
    if segment is None:
        raise AssertionError(f"source segment unavailable for {name!r}")
    return segment


def load_source_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load source module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class I07SourcePackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.policy = load(POLICY_PATH)
        cls.schema = load(SCHEMA_PATH)
        cls.registration = load(REGISTRATION_PATH)
        cls.rows = runtime.build_entry_rows(cls.registration, cls.policy)

    def test_01_policy_is_portable_and_inactive(self) -> None:
        text = POLICY_PATH.read_text(encoding="utf-8")
        self.assertNotIn("/home/", text)
        self.assertEqual(self.policy["environment"]["retained_graph_root"], "${RCAE_PYGRC_ROOT}")
        self.assertFalse(self.policy["authorization"]["freeze_acceptance_authorizes_execution"])
        self.assertTrue(self.policy["authorization"]["activation_requires_separate_owner_direction"])
        self.assertFalse(self.policy["authorization"]["campaign_claim_crosses_p5"])

    def test_02_source_package_is_complete(self) -> None:
        for relative in self.policy["source_package"]["files"]:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_03_schema_is_valid(self) -> None:
        jsonschema.Draft202012Validator.check_schema(self.schema)

    def test_04_exact_governed_entry_and_case_populations(self) -> None:
        self.assertEqual(len(self.rows), 456)
        self.assertEqual([row["schedule_ordinal"] for row in self.rows], list(range(1, 457)))
        self.assertEqual(len({row["entry_id"] for row in self.rows}), 456)
        self.assertEqual(len({row["case_id"] for row in self.rows if row["case_id"] is not None}), 450)
        self.assertEqual(sum(row["entry_kind"] == "operational_baseline_construction" for row in self.rows), 6)

    def test_05_execution_class_population(self) -> None:
        observed = {
            name: sum(row["execution_class"] == name for row in self.rows)
            for name in self.registration["resource_governance"]["class_counts"]
        }
        self.assertEqual(observed, self.registration["resource_governance"]["class_counts"])

    def test_06_expected_terminal_set_is_closed(self) -> None:
        terminals = runtime.build_expected_terminal_set(self.rows, self.registration)
        self.assertEqual(len(terminals), 919)
        self.assertEqual(len({row["terminal_id"] for row in terminals}), 919)
        self.assertEqual(sum(row["root_class"] == "case_resolution" for row in terminals), 450)
        self.assertEqual(sum(row["root_class"] == "operational_baseline_terminal" for row in terminals), 6)
        self.assertEqual(sum(row["root_class"] == "attempt_slot_closure" for row in terminals), 456)

    def test_07_all_case_paths_are_distinct_and_portable(self) -> None:
        observed: set[str] = set()
        for row in self.rows:
            for relative in row["governed_paths"].values():
                runtime.portable_path(relative)
                self.assertNotIn(relative, observed)
                observed.add(relative)
        self.assertEqual(len(observed), 456 * 26)

    def test_08_every_case_preserves_p0_p7_and_p5(self) -> None:
        for row in self.rows:
            self.assertEqual(tuple(row["phases"]), runtime.ENTRY_PHASES)
            self.assertIn("P5_entry_specific_dispatch_authorized", row["phases"])

    def test_09_public_api_and_call_site_registries_are_closed(self) -> None:
        i03 = load(EXPERIMENT / "contracts/p2-i3/i03-br-bounded-conformance-input-freeze.json")
        self.assertEqual(tuple(row["symbol"] for row in i03["required_public_calls"]), runtime.LIVE_OPERATION_SYMBOLS)
        self.assertEqual(tuple(row["symbol"] for row in i03["blocked_public_calls"]), runtime.FORBIDDEN_SYMBOLS)
        self.assertEqual(set(runtime.CALL_SITE_REGISTRY), set(runtime.LIVE_OPERATION_SYMBOLS))

    def test_10_supervisor_cannot_import_candidate_runtime(self) -> None:
        roots = imported_roots(tree(SUPERVISOR_SOURCE))
        self.assertNotIn("pygrc", roots)
        self.assertNotIn("p2_i3_i08_br_case", roots)
        self.assertNotIn("p2_i3_i06_br_registration", roots)

    def test_11_case_has_no_dynamic_import_or_getattr_dispatch(self) -> None:
        parsed = tree(CASE_SOURCE)
        self.assertNotIn("importlib", imported_roots(parsed))
        called_names = {
            node.func.id
            for node in ast.walk(parsed)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        self.assertNotIn("__import__", called_names)
        unsafe_getattrs = [
            node
            for node in ast.walk(parsed)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "getattr"
            and not (
                len(node.args) >= 2
                and isinstance(node.args[0], ast.Name)
                and node.args[0].id == "os"
                and isinstance(node.args[1], ast.Constant)
                and node.args[1].value == "O_NOFOLLOW"
            )
        ]
        self.assertFalse(unsafe_getattrs)

    def test_12_i07_builder_has_no_live_method_call_sites(self) -> None:
        parsed = tree(FREEZE_SOURCE)
        attributes = {
            node.func.attr
            for node in ast.walk(parsed)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }
        forbidden_leaves = {
            "from_state",
            "get_state",
            "schedule_packet_departure",
            "step",
            "run_event_queue",
            "snapshot",
            "save",
            "load",
            "reset",
        }
        self.assertFalse(attributes & forbidden_leaves)

    def test_13_i07_validator_has_no_live_method_call_sites(self) -> None:
        parsed = tree(VALIDATOR_SOURCE)
        attributes = {
            node.func.attr
            for node in ast.walk(parsed)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }
        forbidden_leaves = {
            "from_state",
            "get_state",
            "schedule_packet_departure",
            "step",
            "run_event_queue",
            "snapshot",
            "save",
            "load",
            "reset",
        }
        self.assertFalse(attributes & forbidden_leaves)

    def test_14_governed_symlink_parent_refuses(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            outside = root / "outside"
            outside.mkdir()
            (root / "governed").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(runtime.ExecutionContractError):
                runtime.ensure_no_symlink_components(root, "governed/claim.json")

    def test_15_exclusive_claim_refuses_repeat(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "claim.json"
            runtime.write_exclusive_json(path, {"claim": 1})
            with self.assertRaises(FileExistsError):
                runtime.write_exclusive_json(path, {"claim": 2})

    def test_16_canonical_digest_detects_mutation(self) -> None:
        record = runtime.with_digest({"artifact_id": "test", "value": 1})
        runtime.verify_digest(record)
        record["value"] = 2
        with self.assertRaises(runtime.ExecutionContractError):
            runtime.verify_digest(record)

    def test_17_probe_artifact_roles_bind_response_and_no_interpretation(self) -> None:
        probe = next(row for row in self.rows if row.get("branch_kind") == "terminal_probe")
        self.assertIn("signed_admissibility_margin", probe["expected_artifact_roles"])
        self.assertIn("native_disposition", probe["expected_artifact_roles"])
        self.assertNotIn("rung_assignment", probe["expected_artifact_roles"])

    def test_18_integrity_cases_remain_quarantined(self) -> None:
        integrity = [row for row in self.rows if row["case_kind"] == "quarantined_integrity_fault"]
        self.assertEqual(len(integrity), 72)
        self.assertTrue(all(row["expected_case_terminal"] == "atomic_fail_closed_quarantined_no_scientific_continuation" for row in integrity))

    def test_19_primary_evidence_loss_is_not_rerun_authority(self) -> None:
        self.assertFalse(self.policy["authorization"]["scientific_rerun_is_reconstruction"])
        source = (EXPERIMENT / "scripts/p2_i3_i07_br_freeze.py").read_text(encoding="utf-8")
        self.assertIn("evidence_unavailable_no_rerun", source)

    def test_20_freeze_acceptance_and_activation_paths_are_distinct(self) -> None:
        paths = self.policy["future_authority_paths"]
        self.assertNotEqual(paths["freeze_acceptance"], paths["activation"])

    def test_21_i06a_authority_is_exactly_bound(self) -> None:
        package = self.policy["authority"]["i06_package"]
        self.assertEqual(package["package_version"], "1.0.2")
        self.assertEqual(package["canonical_case_count"], 450)
        self.assertEqual(package["operational_baseline_entry_count"], 6)
        self.assertEqual(package["governed_entry_count"], 456)
        self.assertEqual(package["maximum_governed_child_starts"], 460)

    def test_22_dependency_dag_is_strictly_topological(self) -> None:
        ordinals = {row["entry_id"]: row["schedule_ordinal"] for row in self.rows}
        for row in self.rows:
            for parent in row["parent_entry_ids"]:
                self.assertIn(parent, ordinals)
                self.assertLess(ordinals[parent], row["schedule_ordinal"])

    def test_23_baseline_entries_are_scientifically_inert(self) -> None:
        baselines = [row for row in self.rows if row["entry_kind"] == "operational_baseline_construction"]
        self.assertEqual(len(baselines), 6)
        for row in baselines:
            self.assertIsNone(row["case_id"])
            self.assertEqual(row["scientific_evidence_effect"], "none")
            self.assertTrue(all(value == 0 for value in row["scientific_operation_counts"].values()))
            self.assertIn("operational_baseline_terminal", row["expected_artifact_roles"])

    def test_24_supervisor_waits_for_child_readiness_before_p5(self) -> None:
        source = function_source(SUPERVISOR_SOURCE, "run_child")
        self.assertLess(source.index("subprocess.Popen("), source.index("ready_path.is_file()"))
        self.assertLess(source.index("ready_path.is_file()"), source.index("write_exclusive_json(p5_path"))
        self.assertIn('"scientific_or_integrity_operation_count"] == 0', source)

    def test_25_timeout_terminates_the_complete_process_group(self) -> None:
        source = function_source(SUPERVISOR_SOURCE, "terminate_process_group")
        self.assertIn("os.killpg", source)
        self.assertIn("signal.SIGTERM", source)
        self.assertIn("wait(timeout=10)", source)
        self.assertIn("signal.SIGKILL", source)
        self.assertIn("start_new_session=True", function_source(SUPERVISOR_SOURCE, "run_child"))

    def test_26_child_prepares_before_waiting_for_p5(self) -> None:
        source = function_source(CASE_SOURCE, "command_run_case")
        self.assertLess(source.index("prepare_entry("), source.index("write_exclusive_json(Path(args.ready).resolve(), ready)"))
        self.assertLess(source.index("write_exclusive_json(Path(args.ready).resolve(), ready)"), source.index("wait_for_p5("))
        self.assertLess(source.index("wait_for_p5("), source.index("execute_operational_baseline("))

    def test_27_baseline_is_loaded_by_dependent_entries(self) -> None:
        source = CASE_SOURCE.read_text(encoding="utf-8")
        self.assertIn("def execute_operational_baseline(", source)
        self.assertIn("def load_operational_baseline(", source)
        self.assertIn("verify_registered_reset(loaded, baseline_identity)", source)
        self.assertIn("prepared_baseline_identity", source)

    def test_28_retry_and_resume_authority_is_materialized(self) -> None:
        source = SUPERVISOR_SOURCE.read_text(encoding="utf-8")
        for name in (
            "allocate_retry_token",
            "retry_token_path",
            "validate_no_unresolved_attempt_claims",
            "resume_claim_document",
        ):
            self.assertIn(f"def {name}(", source)
        self.assertIn('sub.add_parser("resume-campaign")', source)
        self.assertIn("campaign_clock_reset\": False", source)

    def test_29_old_case_only_runtime_projection_is_absent(self) -> None:
        sources = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (FREEZE_SOURCE, VALIDATOR_SOURCE, SUPERVISOR_SOURCE, CASE_SOURCE)
        )
        self.assertNotIn('matrix["cases"]', sources)
        self.assertNotIn("maximum_governed_child_starts\"] == 454", sources)
        self.assertNotIn('"P0_case_claim_durable"', sources)

    def test_30_invalid_git_is_ancestor_check_is_absent(self) -> None:
        source = FREEZE_SOURCE.read_text(encoding="utf-8")
        self.assertNotIn('"--is-ancestor"', source)
        self.assertIn('git(ROOT, "merge-base", retained_commit, "HEAD") == retained_commit', source)

    def test_31_policy_binds_exact_retained_i06a_bytes(self) -> None:
        authority = self.policy["authority"]
        package = authority["i06_package"]
        bindings = {
            "registration_sha256": authority["i06_registration"],
            "registration_validation_sha256": authority["i06_registration_validation"],
            "reg_gate_sha256": authority["i06_reg_gate"],
        }
        for key, relative in bindings.items():
            actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
            self.assertEqual(actual, package[key])

    def test_32_source_package_uses_repository_discovery(self) -> None:
        source = (EXPERIMENT / "scripts/p2_i3_br_execution_runtime.py").read_text(encoding="utf-8")
        self.assertIn("def repository_root(", source)
        self.assertNotIn("Path(__file__).resolve().parents[4]", source)

    def test_33_run_matrix_binds_resources_and_attempts(self) -> None:
        source = FREEZE_SOURCE.read_text(encoding="utf-8")
        self.assertIn('"campaign_resource_envelope"', source)
        self.assertIn('"attempt_governance"', source)
        self.assertIn('"maximum_governed_child_starts"', source)

    def test_34_log_overflow_retains_only_typed_prefix(self) -> None:
        supervisor = load_source_module("p2_i3_i08_br_supervisor_test", SUPERVISOR_SOURCE)
        with tempfile.TemporaryDirectory() as raw:
            partial = Path(raw) / "stdout.bin.partial"
            final = Path(raw) / "stdout.bin"
            partial.write_bytes(b"abcdef")
            retained, overflow = supervisor.finalize_captured_stream(partial, final, ceiling=3)
            self.assertTrue(overflow)
            self.assertEqual(retained, b"abc")
            self.assertEqual(final.read_bytes(), b"abc")
            self.assertFalse(partial.exists())

    def test_35_phase_ledger_is_valid_jsonl(self) -> None:
        supervisor = load_source_module("p2_i3_i08_br_supervisor_phase_test", SUPERVISOR_SOURCE)
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "phases.jsonl"
            supervisor.append_phase(path, phase=runtime.ENTRY_PHASES[0], entry_id="entry", case_id=None, attempt=1)
            supervisor.append_phase(path, phase=runtime.ENTRY_PHASES[1], entry_id="entry", case_id=None, attempt=1)
            rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual([row["phase"] for row in rows], list(runtime.ENTRY_PHASES[:2]))

    def test_36_freeze_acceptance_and_activation_are_closed_twice(self) -> None:
        supervisor = load_source_module("p2_i3_i08_br_supervisor_authority_test", SUPERVISOR_SOURCE)
        digest = "0" * 64
        commit = "1" * 40
        acceptance = runtime.with_digest(
            {
                "artifact_id": "P2-I3-BR-I07-FREEZE-ACCEPTANCE",
                "artifact_version": "1.0.0",
                "iteration_id": "P2-I3-I07",
                "branch_id": "P2-I3-BR",
                "freeze_retention_commit": commit,
                "accepted_freeze": {"path": "freeze.json", "sha256": digest},
                "execution_authorized": False,
                "activation_construction_permitted": True,
            }
        )
        activation = runtime.with_digest(
            {
                "artifact_id": "P2-I3-BR-I07-EXECUTION-ACTIVATION",
                "artifact_version": "1.0.0",
                "iteration_id": "P2-I3-I07",
                "branch_id": "P2-I3-BR",
                "freeze_acceptance": {"path": "acceptance.json", "sha256": digest},
                "accepted_freeze": {"path": "freeze.json", "sha256": digest},
                "freeze_retention_commit": commit,
                "owner_execution_direction": True,
                "launch_head_binding": "runtime_argument_verified_and_retained_in_campaign_claim",
                "launch_environment": {
                    "required_environment": deepcopy(self.policy["environment"]["required_environment"]),
                    "pythonpath_template": self.policy["environment"]["normalized_pythonpath"],
                    "pythonhome": "absent",
                    "ambient_or_installed_fallback_allowed": False,
                },
                "interpreter_binding": {
                    "invocation_path": ".venv/bin/python",
                    "resolved_target_sha256": digest,
                    "resolved_target_kind": "regular_file",
                    "python_version": "3.12.3",
                    "python_implementation": "CPython",
                },
                "graph_root_binding": {
                    "environment_variable": "RCAE_PYGRC_ROOT",
                    "retained_root": "${RCAE_PYGRC_ROOT}",
                    "resolved_target_revision": "565706f8b7647f6b7638b9afbe52372e170bf724",
                    "resolved_target_source_root": "src",
                    "resolved_target_pygrc_init_sha256": digest,
                    "machine_local_path_retained": False,
                },
                "governed_path_policy": {
                    "claims_no_symlink_components": True,
                    "outputs_no_symlink_components": True,
                    "temporaries_no_symlink_components": True,
                    "content_store_no_symlink_components": True,
                },
                "consumed": False,
            }
        )
        for name, record, fields in (
            ("freeze acceptance", acceptance, supervisor.FREEZE_ACCEPTANCE_FIELDS),
            ("activation", activation, supervisor.ACTIVATION_FIELDS),
        ):
            jsonschema.validate(record, self.schema)
            supervisor.require_exact_fields(record, fields, name)
            opened = {**record, "unknown": True}
            with self.assertRaises(jsonschema.ValidationError):
                jsonschema.validate(opened, self.schema)
            with self.assertRaises(runtime.ExecutionContractError):
                supervisor.require_exact_fields(opened, fields, name)

    def test_37_retained_commands_bind_complete_normalized_environment(self) -> None:
        runtime.validate_policy_command_environments(self.policy)
        changed = deepcopy(self.policy)
        changed["commands"]["validate_inactive_freeze"] = changed["commands"]["validate_inactive_freeze"].replace(
            " PYTHONHASHSEED=0", ""
        )
        with self.assertRaises(runtime.ExecutionContractError):
            runtime.validate_policy_command_environments(changed)

    def test_38_retry_token_model_closes_all_four_states(self) -> None:
        classify = runtime.classify_retry_token_closure
        self.assertEqual(
            classify(token_present=False, attempt_2_claim_present=False, attempt_2_terminal_status=None, attempt_2_descendant_count=0),
            "unused",
        )
        self.assertEqual(
            classify(token_present=True, attempt_2_claim_present=False, attempt_2_terminal_status=None, attempt_2_descendant_count=0),
            "allocated_before_attempt_2_claim",
        )
        self.assertEqual(
            classify(token_present=True, attempt_2_claim_present=True, attempt_2_terminal_status="invalid_execution", attempt_2_descendant_count=4),
            "attempt_2_failed",
        )
        self.assertEqual(
            classify(token_present=True, attempt_2_claim_present=True, attempt_2_terminal_status="valid_terminal", attempt_2_descendant_count=4),
            "attempt_2_valid_terminal",
        )
        with self.assertRaises(runtime.ExecutionContractError):
            classify(token_present=False, attempt_2_claim_present=False, attempt_2_terminal_status=None, attempt_2_descendant_count=1)
        with self.assertRaises(runtime.ExecutionContractError):
            classify(token_present=True, attempt_2_claim_present=True, attempt_2_terminal_status=None, attempt_2_descendant_count=1)

    def test_39_terminal_set_declares_model_a_descendant_ownership(self) -> None:
        terminals = runtime.build_expected_terminal_set(self.rows, self.registration)
        token_roots = [row for row in terminals if row["root_class"] == "retry_token_closure"]
        self.assertEqual(len(token_roots), 4)
        self.assertTrue(all(row["closure_model"] == "token_root_owns_optional_attempt_2_descendants" for row in token_roots))
        self.assertTrue(all(tuple(row["allowed"]) == runtime.RETRY_TOKEN_CLOSURE_STATES for row in token_roots))

    def test_40_importable_ambient_pygrc_is_rejected_before_runtime_call(self) -> None:
        graph_root = ROOT.parent / "graph-reflexive-coherence"
        self.assertTrue(graph_root.is_dir())
        with tempfile.TemporaryDirectory() as raw:
            temp = Path(raw)
            fake_package = temp / "pygrc"
            fake_package.mkdir()
            sentinel = temp / "public-call-sentinel"
            (fake_package / "__init__.py").write_text(
                "def public_runtime_call():\n"
                "    from pathlib import Path\n"
                "    import os\n"
                "    Path(os.environ['I07_PUBLIC_CALL_SENTINEL']).write_text('called')\n",
                encoding="utf-8",
            )
            env = os.environ.copy()
            env.update(self.policy["environment"]["required_environment"])
            env["RCAE_PYGRC_ROOT"] = "../graph-reflexive-coherence"
            env["PYTHONPATH"] = os.pathsep.join((str(temp), str(SCRIPTS)))
            env["I07_PUBLIC_CALL_SENTINEL"] = str(sentinel)
            env.pop("PYTHONHOME", None)
            result = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(FREEZE_SOURCE.relative_to(ROOT)),
                    "build",
                    "--graph-root",
                    "../graph-reflexive-coherence",
                    "--allow-dirty-preview",
                    "--output-dir",
                    str(temp / "preview"),
                ],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("PyGRC did not import from exact source root", result.stderr)
            self.assertFalse(sentinel.exists())


if __name__ == "__main__":
    unittest.main()
