"""Zero-calibration tests for the P2-I3 B-R I05 inactive freeze."""

from __future__ import annotations

import ast
from copy import deepcopy
from fractions import Fraction
import json
import os
from pathlib import Path
import stat
import sys

from jsonschema import Draft202012Validator
import pytest
from referencing import Registry, Resource


def _find_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _find_root()
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
SCRIPTS = EXPERIMENT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ae01_tooling import ContractError  # noqa: E402
from p2_i3_i04_br_analysis import (  # noqa: E402
    estimate_woe_triplet,
    validate_response_record,
)
from p2_i3_i05_br_calibration import (  # noqa: E402
    CALIBRATED_RELATION_IDS,
    DELTA_FORMULA,
    ENTERED_CASES,
    EXCLUDED_CONFORMANCE_CASE_IDS,
    MATCHED_NULL_PATH,
    Q_PROBE,
    build_calibration_outputs,
    build_q_half_response,
    exact_triplet_margins,
    validate_calibration_outputs,
    validate_builder_authorities,
    validate_null_case,
)
import p2_i3_i05_br_one_shot as one_shot  # noqa: E402


I04_POLICY_PATH = EXPERIMENT / "configs/p2_i3_br_i04_machine_policy.json"
I04_SCHEMA_PATH = EXPERIMENT / "contracts/p2-i3/i04-br-machine-records.schema.json"
I05_POLICY_PATH = EXPERIMENT / "configs/p2_i3_br_i05_one_shot_policy.json"
I05_SCHEMA_PATH = EXPERIMENT / "contracts/p2-i3/i05-br-calibration-output.schema.json"
METRIC_SHEET_PATH = EXPERIMENT / "contracts/metric-sheets/AE01-L03.json"
BUILDER_PATH = EXPERIMENT / "scripts/p2_i3_i05_br_calibration.py"
WRAPPER_PATH = EXPERIMENT / "scripts/p2_i3_i05_br_one_shot.py"
VALIDATOR_PATH = EXPERIMENT / "scripts/p2_i3_i05_br_freeze_validate.py"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _schema_validator() -> Draft202012Validator:
    i04 = _load(I04_SCHEMA_PATH)
    i05 = _load(I05_SCHEMA_PATH)
    registry = Registry().with_resource(i04["$id"], Resource.from_contents(i04))
    return Draft202012Validator(i05, registry=registry)


def _definition_validator(name: str) -> Draft202012Validator:
    i04 = _load(I04_SCHEMA_PATH)
    i05 = _load(I05_SCHEMA_PATH)
    registry = Registry().with_resource(i04["$id"], Resource.from_contents(i04))
    wrapper = {
        "$schema": i05["$schema"],
        "$defs": i05["$defs"],
        "$ref": f"#/$defs/{name}",
    }
    return Draft202012Validator(wrapper, registry=registry)


def _zero_case() -> dict:
    records = [
        build_q_half_response(case_id="EQ-ZERO", arm_id=arm, margin="0", seed_alias=71)
        for arm in ("W", "O", "E")
    ]
    return {
        "case_id": "EQ-ZERO",
        "response_records": records,
        "seed_alias": 71,
        "triplet_result": estimate_woe_triplet(records, epsilon_mu=1e-12),
    }


def _all_registered_margins() -> set[str]:
    policy = _load(I04_POLICY_PATH)
    margins = {
        value
        for case in policy["calibration"]["panel_a_exact_null"]
        for value in case["values"].values()
    }
    margins.update(
        value
        for case in policy["calibration"]["panels_b_c_estimator_conformance"]
        for value in case["values"].values()
    )
    return margins


def test_q_half_construction_is_exact_and_bounded_for_every_registered_margin() -> None:
    assert Q_PROBE == Fraction(1, 2)
    for index, margin in enumerate(sorted(_all_registered_margins())):
        record = build_q_half_response(
            case_id=f"construction-{index}",
            arm_id="W",
            margin=margin,
            seed_alias=19,
        )
        validate_response_record(record)
        c_pre = Fraction(record["c_pre_m_e"]["rational"])
        q_probe = Fraction(record["q_probe"]["rational"])
        assert q_probe == Fraction(1, 2)
        assert c_pre - q_probe == Fraction(margin)
        assert Fraction(0) <= c_pre <= Fraction(1)


def test_q_half_construction_keeps_one_request_identity() -> None:
    identities = set()
    requests = set()
    for arm in ("W", "O", "E"):
        record = build_q_half_response(
            case_id="EQ-ZERO", arm_id=arm, margin="0", seed_alias=71
        )
        identities.add(record["pairing"]["request_construction_id"])
        requests.add(record["q_probe"]["rational"])
    assert identities == {"p2-i3-i05-q-half-v1"}
    assert requests == {"1/2"}


def test_builder_authorities_validate_without_building_calibration() -> None:
    validate_builder_authorities(_load(I04_POLICY_PATH), _load(METRIC_SHEET_PATH))


def test_complete_builder_is_not_called_by_freeze_tests_or_validator() -> None:
    assert build_calibration_outputs.__name__ == "build_calibration_outputs"
    test_tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    validator_tree = ast.parse(VALIDATOR_PATH.read_text(encoding="utf-8"))
    for tree in (test_tree, validator_tree):
        calls = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "build_calibration_outputs"
        ]
        assert calls == []


def test_builder_and_wrapper_import_no_pygrc() -> None:
    for path in (BUILDER_PATH, WRAPPER_PATH, VALIDATOR_PATH):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module or "")
        assert not any(name == "pygrc" or name.startswith("pygrc.") for name in imports)


def test_builder_interface_accepts_no_candidate_shaped_argument() -> None:
    tree = ast.parse(BUILDER_PATH.read_text(encoding="utf-8"))
    function = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "build_calibration_outputs"
    )
    names = {argument.arg for argument in (*function.args.args, *function.args.kwonlyargs)}
    assert names == {"i04_policy", "metric_sheet", "source_metric_sheet_sha256"}
    assert not any(token in name for name in names for token in ("candidate", "runtime", "pygrc"))


def test_output_schema_root_is_closed() -> None:
    validator = _schema_validator()
    for invalid in ({}, {"nonsense": 1}, {"artifact_id": "garbage"}):
        assert not validator.is_valid(invalid)
    minimal_sheet = {
        "artifact_id": "P2-I3-I05-BR-FROZEN-METRIC-SHEET",
        "artifact_version": "1.0.2",
        "authority": {
            "freeze_id": "P2-I3-I05-BR-CALIBRATION-INVOCATION-FREEZE",
            "i04_source_anchor": "1097547ad30b77d4cf9312fb05753902f6d1cc81",
            "policy_id": "P2-I3-I05-BR-ONE-SHOT-POLICY",
        },
        "calibrated_relation_ids": ["m_trace", "m_export"],
        "candidate_blind": True,
        "delta": {"rational": "1/1000000000000", "value": 1e-12},
        "delta_scope": "shared_arithmetic_resolution_for_both_relations",
        "evidence_effect": "numeric_measurement_resolution_only",
        "lane_id": "AE01-L03",
        "measurement_resolution": {"rational": "1/1000000000000", "value": 1e-12},
        "metric_id": "trace_conditioned_route_normalized_margin",
        "metric_sheet_id": "ae01-l03-primary-metric-v1",
        "source_metric_sheet_sha256": "0" * 64,
        "status": "frozen_candidate_blind_calibration",
    }
    assert validator.is_valid(minimal_sheet)
    minimal_sheet["candidate_result"] = True
    assert not validator.is_valid(minimal_sheet)


def test_output_schema_resolves_accepted_i04_response_and_triplet_refs() -> None:
    i04 = _load(I04_SCHEMA_PATH)
    i05 = _load(I05_SCHEMA_PATH)
    registry = Registry().with_resource(i04["$id"], Resource.from_contents(i04))
    wrapper = {
        "$schema": i05["$schema"],
        "$defs": i05["$defs"],
        "$ref": "#/$defs/null_case",
    }
    records = [
        build_q_half_response(
            case_id="EQ-ZERO", arm_id=arm, margin="0", seed_alias=71
        )
        for arm in ("W", "O", "E")
    ]
    row = {
        "case_id": "EQ-ZERO",
        "response_records": records,
        "seed_alias": 71,
        "triplet_result": estimate_woe_triplet(records, epsilon_mu=1e-12),
    }
    Draft202012Validator(wrapper, registry=registry).validate(row)


def test_shared_calibration_registry_is_exact_for_both_estimators() -> None:
    policy = _load(I05_POLICY_PATH)["calibration_construction"]
    assert CALIBRATED_RELATION_IDS == ["m_trace", "m_export"]
    assert policy["calibrated_relation_ids"] == CALIBRATED_RELATION_IDS
    assert policy["exact_entered_case_ids"] == [case[0] for case in ENTERED_CASES]
    assert policy["entered_margin_count"] == 10
    assert policy["margins_per_case"] == {"m_trace": 1, "m_export": 1}
    assert policy["exact_excluded_conformance_case_ids"] == EXCLUDED_CONFORMANCE_CASE_IDS
    assert policy["shared_delta_formula"] == DELTA_FORMULA


def test_null_case_semantics_recompute_both_relations() -> None:
    trace, export = validate_null_case(
        _zero_case(),
        expected_id="EQ-ZERO",
        expected_seed=71,
        expected_margin="0",
        epsilon=Fraction(1, 1_000_000_000_000),
    )
    assert trace == export == 0


@pytest.mark.parametrize("mutation", ["case", "seed", "arm", "pair"])
def test_null_case_semantics_reject_identity_substitution(mutation: str) -> None:
    case = _zero_case()
    if mutation == "case":
        case["case_id"] = "EQ-POS-HALF"
    elif mutation == "seed":
        case["seed_alias"] = 109
    elif mutation == "arm":
        case["response_records"][0]["arm_id"] = "E"
    else:
        case["response_records"][0]["pair_id"] = "P2-I3-I05:wrong"
    with pytest.raises(ContractError):
        validate_null_case(
            case,
            expected_id="EQ-ZERO",
            expected_seed=71,
            expected_margin="0",
            epsilon=Fraction(1, 1_000_000_000_000),
        )


@pytest.mark.parametrize(
    ("rational", "value"),
    [("0/2", 0.0), ("1/2", 0.4), ("0", -0.0)],
)
def test_semantic_validator_rejects_noncanonical_rational_projection(
    rational: str, value: float
) -> None:
    case = _zero_case()
    case["response_records"][0]["admissibility_margin"] = {
        "rational": rational,
        "value": value,
    }
    with pytest.raises(ContractError):
        validate_null_case(
            case,
            expected_id="EQ-ZERO",
            expected_seed=71,
            expected_margin="0",
            epsilon=Fraction(1, 1_000_000_000_000),
        )


def test_metric_calibration_schema_freezes_authority_registry_path_and_relations() -> None:
    value = {
        "artifact_id": "P2-I3-I05-BR-METRIC-CALIBRATION",
        "artifact_version": "1.0.2",
        "authority": {
            "freeze_id": "P2-I3-I05-BR-CALIBRATION-INVOCATION-FREEZE",
            "i04_source_anchor": "1097547ad30b77d4cf9312fb05753902f6d1cc81",
            "policy_id": "P2-I3-I05-BR-ONE-SHOT-POLICY",
        },
        "calibrated_relation_ids": CALIBRATED_RELATION_IDS,
        "candidate_blind": True,
        "delta": {"rational": "1/1000000000000", "value": 1e-12},
        "delta_formula": DELTA_FORMULA,
        "entered_case_ids": [case[0] for case in ENTERED_CASES],
        "entered_margin_count": 10,
        "entered_margins": [
            {
                "case_id": case[0],
                "m_export": {"rational": "0", "value": 0.0},
                "m_trace": {"rational": "0", "value": 0.0},
            }
            for case in ENTERED_CASES
        ],
        "excluded_conformance_case_ids": EXCLUDED_CONFORMANCE_CASE_IDS,
        "lane_id": "AE01-L03",
        "margins_per_case": {"m_trace": 1, "m_export": 1},
        "matched_null_artifact_path": MATCHED_NULL_PATH,
        "maximum_absolute_matched_null_margin": {"rational": "0", "value": 0.0},
        "measurement_resolution": {"rational": "1/1000000000000", "value": 1e-12},
        "scientific_result": False,
    }
    validator = _definition_validator("metric_calibration")
    validator.validate(value)
    for key, replacement in (
        ("matched_null_artifact_path", "../../anything"),
        ("entered_case_ids", ["arbitrary"] * 5),
        ("calibrated_relation_ids", ["m_trace"]),
    ):
        invalid = dict(value)
        invalid[key] = replacement
        assert not validator.is_valid(invalid)
    invalid = json.loads(json.dumps(value))
    invalid["authority"]["i04_source_anchor"] = "0" * 40
    assert not validator.is_valid(invalid)


def test_activation_record_shape_is_frozen_while_values_remain_deferred() -> None:
    policy = _load(I05_POLICY_PATH)
    activation = {
        "artifact_id": "P2-I3-I05-BR-CALIBRATION-LAUNCH-AUTHORIZATION",
        "artifact_version": "1.0.2",
        "accepted_freeze_commit": "1" * 40,
        "attempt_claim_path": policy["outputs"]["attempt_claim"],
        "authority_sha256": {
            name: str(index) * 64
            for index, name in enumerate(
                ("builder", "freeze", "output_schema", "policy", "validator", "wrapper"),
                start=1,
            )
        },
        "branch_id": "P2-I3-BR",
        "calibration_invocation_authorized": True,
        "candidate_execution_authorized": False,
        "freeze_artifact_id": "P2-I3-I05-BR-CALIBRATION-INVOCATION-FREEZE",
        "freeze_sha256": "2" * 64,
        "governed_invocations_authorized": 1,
        "governed_paths": policy["outputs"],
        "interpreter_environment": {
            "binary_sha256": policy["environment"]["interpreter_binary_sha256"],
            "command": ".venv/bin/python",
            "jsonschema": "4.26.0",
            "process_environment": {
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONHASHSEED": "0",
            },
            "pytest": "9.1.1",
            "python": "3.12.3",
        },
        "iteration_id": "P2-I3-I05",
        "lane_id": "AE01-L03",
        "launch_head_binding_method": "runtime_expected_head_verified_clean_and_retained_in_claim_and_receipt",
        "normalized_command_prefix": policy["normalized_command_template"][:-1],
        "owner_accepted_freeze": True,
    }
    validator = _definition_validator("launch_authorization")
    validator.validate(activation)
    for key, replacement in (
        ("normalized_command_prefix", ["alternate"]),
        ("attempt_claim_path", "alternate-claim.json"),
        ("governed_paths", {**policy["outputs"], "matched_null": "alternate.json"}),
    ):
        invalid = deepcopy(activation)
        invalid[key] = replacement
        assert not validator.is_valid(invalid)
    activation["unexpected"] = True
    assert not validator.is_valid(activation)


def test_missing_or_failed_final_receipt_quarantines_outputs() -> None:
    policy = _load(I05_POLICY_PATH)
    hashes = {name: str(index) * 64 for index, name in enumerate(("matched_null", "metric_calibration", "frozen_metric_sheet"), start=1)}
    with pytest.raises(ContractError, match="missing final receipt"):
        one_shot.validate_consumable_closeout(
            policy=policy,
            receipt=None,
            claim_sha256="a" * 64,
            activation_sha256="b" * 64,
            output_sha256=hashes,
        )
    with pytest.raises(ContractError, match="failed final receipt"):
        one_shot.validate_consumable_closeout(
            policy=policy,
            receipt={"completion_status": "failed"},
            claim_sha256="a" * 64,
            activation_sha256="b" * 64,
            output_sha256=hashes,
        )


def test_wrapper_semantically_validates_before_write_and_after_readback() -> None:
    source = WRAPPER_PATH.read_text(encoding="utf-8")
    first_semantic = source.index("validate_calibration_outputs(")
    first_output_write = source.index("payloads[name] = _exclusive_write")
    second_semantic = source.index("validate_calibration_outputs(", first_semantic + 1)
    assert first_semantic < first_output_write < second_semantic


def test_exact_margin_path_never_round_trips_through_projected_float() -> None:
    records = [
        build_q_half_response(
            case_id="EXACT-NONZERO",
            arm_id=arm,
            margin=margin,
            seed_alias=19,
        )
        for arm, margin in (("W", "0"), ("O", "1/3"), ("E", "1/4"))
    ]
    trace, export = exact_triplet_margins(
        records, Fraction(1, 1_000_000_000_000)
    )
    assert trace == 1
    assert export == Fraction(1, 4)


def test_exact_boundary_dispositions_and_carriers() -> None:
    expected = {
        "-1/2": ("0", "field_limited_refusal"),
        "0": ("1/2", "admitted"),
        "1/2": ("1", "admitted"),
    }
    for margin, (carrier, disposition) in expected.items():
        record = build_q_half_response(
            case_id=f"BOUNDARY-{margin}",
            arm_id="E",
            margin=margin,
            seed_alias=19,
        )
        assert record["c_pre_m_e"]["rational"] == carrier
        assert record["native_disposition"] == disposition


def test_semantic_case_rejects_missing_export_relation() -> None:
    case = _zero_case()
    del case["triplet_result"]["export_relation"]
    with pytest.raises(ContractError, match="triplet result"):
        validate_null_case(
            case,
            expected_id="EQ-ZERO",
            expected_seed=71,
            expected_margin="0",
            epsilon=Fraction(1, 1_000_000_000_000),
        )


def test_semantic_case_rejects_swapped_export_orientation() -> None:
    case = _zero_case()
    relation = case["triplet_result"]["export_relation"]
    relation["arm_record_ids"] = list(reversed(relation["arm_record_ids"]))
    with pytest.raises(ContractError, match="triplet result"):
        validate_null_case(
            case,
            expected_id="EQ-ZERO",
            expected_seed=71,
            expected_margin="0",
            epsilon=Fraction(1, 1_000_000_000_000),
        )


def test_exclusive_write_fsyncs_file_and_parent_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    observed: list[str] = []
    real_fsync = os.fsync

    def recording_fsync(descriptor: int) -> None:
        mode = os.fstat(descriptor).st_mode
        observed.append("directory" if stat.S_ISDIR(mode) else "file")
        real_fsync(descriptor)

    monkeypatch.setattr(one_shot.os, "fsync", recording_fsync)
    monkeypatch.setattr(one_shot, "ROOT", tmp_path)
    one_shot._exclusive_write(tmp_path / "claim.json", {"claim": 1})
    assert observed == ["file", "directory"]


def test_failed_claim_flush_leaves_permanent_occupied_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(one_shot, "ROOT", tmp_path)

    def fail_fsync(_descriptor: int) -> None:
        raise OSError("injected fsync failure")

    monkeypatch.setattr(one_shot.os, "fsync", fail_fsync)
    claim = tmp_path / "claim.json"
    with pytest.raises(OSError, match="injected fsync failure"):
        one_shot._exclusive_write(claim, {"claim": 1})
    assert os.path.lexists(claim)
    with pytest.raises(FileExistsError):
        one_shot._exclusive_write(claim, {"claim": 2})


def test_zero_length_claim_permanently_refuses_repair(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(one_shot, "ROOT", tmp_path)
    claim = tmp_path / "claim.json"
    descriptor = os.open(claim, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    os.close(descriptor)
    assert claim.stat().st_size == 0
    with pytest.raises(FileExistsError):
        one_shot._exclusive_write(claim, {"repair": True})


@pytest.mark.parametrize("name", ["PYTHONDONTWRITEBYTECODE", "PYTHONHASHSEED"])
def test_missing_deterministic_environment_fails_before_claim(
    name: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    policy = _load(I05_POLICY_PATH)
    monkeypatch.delenv(name, raising=False)
    with pytest.raises(ContractError, match="process environment"):
        one_shot._process_environment(policy)


def test_postclaim_revalidation_precedes_builder_and_receipt_is_last() -> None:
    source = WRAPPER_PATH.read_text(encoding="utf-8")
    claim = source.index('claim_payload = _exclusive_write(outputs["attempt_claim"], claim)')
    revalidation = source.index("validate_postclaim(", claim)
    builder_import = source.index("from p2_i3_i05_br_calibration import (")
    final_receipt = source.index('_exclusive_write(outputs["final_receipt"], receipt)')
    assert claim < revalidation < builder_import
    assert final_receipt > source.index("after_second_start_refusal")


class _NoOpValidator:
    def validate(self, _value: object) -> None:
        return None


def _prepare_fake_transaction(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, Path, str]:
    policy = deepcopy(_load(I05_POLICY_PATH))
    policy["outputs"] = {
        "attempt_claim": "attempt-claim.json",
        "final_receipt": "final-receipt.json",
        "frozen_metric_sheet": "frozen-metric-sheet.json",
        "matched_null": "matched-null.json",
        "metric_calibration": "metric-calibration.json",
    }
    activation_path = tmp_path / "activation.json"
    activation_path.write_text('{"activation":true}\n', encoding="utf-8")
    for relative in (one_shot.FREEZE_PATH, one_shot.METRIC_SHEET_PATH):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}\n", encoding="utf-8")
    activation = {
        "artifact_id": "P2-I3-I05-BR-CALIBRATION-LAUNCH-AUTHORIZATION",
        "accepted_freeze_commit": "1" * 40,
    }
    current_hashes = {
        one_shot.BUILDER_PATH: "1" * 64,
        one_shot.FREEZE_PATH: "2" * 64,
        one_shot.I05_SCHEMA_PATH: "3" * 64,
        one_shot.POLICY_PATH: "4" * 64,
        one_shot.VALIDATOR_PATH: "5" * 64,
        one_shot.WRAPPER_PATH: "6" * 64,
    }
    interpreter = {
        "binary_sha256": policy["environment"]["interpreter_binary_sha256"],
        "command": ".venv/bin/python",
        "implementation": "CPython",
        "jsonschema": "4.26.0",
        "pytest": "9.1.1",
        "version": "3.12.3",
    }
    expected_head = "a" * 40
    monkeypatch.setattr(one_shot, "ROOT", tmp_path)
    monkeypatch.setattr(
        one_shot,
        "validate_preclaim",
        lambda **_kwargs: (
            policy,
            interpreter,
            current_hashes,
            [".venv/bin/python", "wrapper", "--policy", "policy", "--activation", "activation", "--expected-head", expected_head],
            activation,
            "activation.json",
        ),
    )
    monkeypatch.setattr(one_shot, "validate_postclaim", lambda **_kwargs: None)
    monkeypatch.setattr(one_shot, "_schema_validator", lambda: _NoOpValidator())
    monkeypatch.setattr(one_shot, "_load_relative", lambda _path: {})

    import p2_i3_i05_br_calibration as calibration

    def fake_outputs(**_kwargs: object) -> dict:
        return {
            "matched_null": {"case_count": 5, "response_record_count": 15},
            "metric_calibration": {
                "calibrated_relation_ids": ["m_trace", "m_export"],
                "delta": {"rational": "1/1000000000000", "value": 1e-12},
                "entered_margin_count": 10,
            },
            "frozen_metric_sheet": {},
        }

    monkeypatch.setattr(calibration, "build_calibration_outputs", fake_outputs)
    monkeypatch.setattr(calibration, "validate_calibration_outputs", lambda *_args, **_kwargs: None)
    return tmp_path / "policy.json", activation_path, expected_head


@pytest.mark.parametrize(
    "boundary",
    [
        "after_preflight_before_claim",
        "after_claim",
        "after_postclaim_revalidation",
        "before_builder_import",
        "after_builder_import",
        "after_builder_calculation",
        "after_in_memory_validation",
        "after_matched_null_write",
        "after_metric_calibration_write",
        "after_frozen_metric_sheet_write",
        "after_readback_validation",
        "after_second_start_refusal",
        "before_final_receipt",
    ],
)
def test_transaction_failure_boundaries_fail_closed(
    boundary: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    policy_path, activation_path, expected_head = _prepare_fake_transaction(
        tmp_path, monkeypatch
    )

    def inject(observed: str) -> None:
        if observed == boundary:
            raise RuntimeError(f"injected:{boundary}")

    with pytest.raises(RuntimeError, match=f"injected:{boundary}"):
        one_shot.run_once(
            policy_path=policy_path,
            activation_path=activation_path,
            expected_head=expected_head,
            _fault_injector=inject,
        )
    claim = tmp_path / "attempt-claim.json"
    receipt = tmp_path / "final-receipt.json"
    if boundary == "after_preflight_before_claim":
        assert not os.path.lexists(claim)
    else:
        assert os.path.lexists(claim)
        with pytest.raises(FileExistsError):
            one_shot._exclusive_write(claim, {"retry": True})
        with pytest.raises(ContractError, match="missing final receipt"):
            one_shot.validate_consumable_closeout(
                policy=deepcopy(_load(I05_POLICY_PATH)),
                receipt=None,
                claim_sha256="a" * 64,
                activation_sha256="b" * 64,
                output_sha256={
                    "matched_null": "c" * 64,
                    "metric_calibration": "d" * 64,
                    "frozen_metric_sheet": "e" * 64,
                },
            )
    assert not os.path.lexists(receipt)


def test_atomic_claim_is_permanent_and_refuses_second_start(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(one_shot, "ROOT", tmp_path)
    claim = tmp_path / "claim.json"
    one_shot._exclusive_write(claim, {"authorization_consumed": True})
    with pytest.raises(FileExistsError):
        one_shot._exclusive_write(claim, {"authorization_consumed": True})
    assert claim.exists()
    assert json.loads(claim.read_text(encoding="utf-8"))["authorization_consumed"] is True


def test_inactive_policy_has_one_attempt_zero_retry_and_no_authority() -> None:
    policy = _load(I05_POLICY_PATH)
    assert policy["attempt_policy"]["max_governed_attempts"] == 1
    assert policy["attempt_policy"]["max_infrastructure_retries"] == 0
    assert policy["attempt_policy"]["consume_before_builder"] is True
    assert policy["governed_invocation"]["calibration_invocation_authorized"] is False
    assert policy["candidate_blindness"]["candidate_execution_authorized"] is False


def test_wrapper_imports_builder_only_after_claim_source_order() -> None:
    source = WRAPPER_PATH.read_text(encoding="utf-8")
    claim = source.index('_exclusive_write(outputs["attempt_claim"], claim)')
    builder_import = source.index("from p2_i3_i05_br_calibration import (")
    builder_call = source.index("built = build_calibration_outputs(")
    assert claim < builder_import < builder_call


def test_governed_paths_and_launch_authority_are_absent() -> None:
    policy = _load(I05_POLICY_PATH)
    activation = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i3/i05-br-calibration-launch-authorization.json"
    assert not activation.exists()
    for relative in policy["outputs"].values():
        assert not os.path.lexists(ROOT / relative)


def test_no_negative_zero_or_candidate_seed_enters_frozen_panel() -> None:
    policy = _load(I04_POLICY_PATH)
    serialized = json.dumps(policy["calibration"]["panel_a_exact_null"], sort_keys=True)
    assert "-0" not in serialized
    aliases = {case["seed_alias"] for case in policy["calibration"]["panel_a_exact_null"]}
    assert aliases.isdisjoint(policy["calibration"]["candidate_seed_exclusions"])


def test_invalid_q_half_drift_fails_i04_validation() -> None:
    record = build_q_half_response(
        case_id="drift", arm_id="E", margin="1/4", seed_alias=19
    )
    record["q_probe"] = {"rational": "1/4", "value": 0.25}
    with pytest.raises(ContractError):
        validate_response_record(record)
