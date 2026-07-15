from __future__ import annotations

import json
import os
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts"
if os.fspath(SCRIPTS) not in sys.path:
    sys.path.insert(0, os.fspath(SCRIPTS))

import p2_i2_c02_execution as c02


def test_c02_matrix_is_exact_234_row_cycle_translation() -> None:
    matrix = c02.translated_matrix(ROOT)
    assert matrix["cycle_id"] == "P2-I2-C02"
    assert matrix["primary_entry_count"] == 234
    assert matrix["scientific_projection_change_count"] == 0
    assert [row["sequence_index"] for row in matrix["entries"]] == list(range(1, 235))
    assert len({row["entry_id"] for row in matrix["entries"]}) == 234
    assert all("/c02/" in row["primary_output_path"] for row in matrix["entries"])


def test_c02_translation_changes_only_cycle_and_governed_paths() -> None:
    c01 = c02.load_json(ROOT / c02.C01_MATRIX_REL)
    c02_rows = c02.translated_matrix(ROOT)["entries"]
    for old, new in zip(c01["entries"], c02_rows, strict=True):
        projected = dict(new)
        projected["cycle_id"] = old["cycle_id"]
        projected["entry_id"] = old["entry_id"]
        for key in ("primary_claim_path", "retry_claim_path", "primary_output_path", "retry_output_path"):
            projected[key] = projected[key].replace("outputs/p2-i2/c02/", "outputs/p2-i2/c01/", 1)
        for key in ("normalized_primary_argv_template", "normalized_retry_argv_template"):
            projected[key] = [token.replace("outputs/p2-i2/c02/", "outputs/p2-i2/c01/", 1) for token in projected[key]]
        assert projected == old


def test_c02_policy_removes_only_address_space_enforcement() -> None:
    policy = c02.load_json(ROOT / c02.POLICY_REL)
    envelope = policy["resource_envelope_per_worker"]
    assert envelope == {
        "max_runtime_seconds": 180,
        "max_file_size_mb": 512,
        "address_space_limit": None,
        "RLIMIT_AS_applied": False,
        "hardware": "single_local_CPU_no_accelerator",
    }
    assert policy["scientific_projection"]["semantic_change_count"] == 0


def test_external_supervisor_observes_native_exit_without_attestation() -> None:
    command = [os.fspath(Path(sys.executable).resolve()), "-B", "-c", "import os; os._exit(77)"]
    result = c02._run_child_process(command, ROOT, os.environ, 10)
    assert result["timed_out"] is False
    assert result["returncode"] == 77
    assert c02._child_envelope(result["stdout"]) is None


def test_external_supervisor_reads_success_attestation() -> None:
    envelope = {"artifact_id": "P2-I2-C02-WORKER-ENVELOPE", "status": "success", "result": {}}
    code = "import json; print(json.dumps(" + repr(envelope) + "))"
    result = c02._run_child_process([os.fspath(Path(sys.executable).resolve()), "-B", "-c", code], ROOT, os.environ, 10)
    assert result["returncode"] == 0
    assert c02._child_envelope(result["stdout"]) == envelope


def test_unknown_or_native_phase_is_conservatively_nonretryable() -> None:
    source = (ROOT / c02.SOURCE_REL).read_text(encoding="utf-8")
    assert '"retry_unknown_phase_is_refused": not attested_failure' in source
    assert "and counters.get(\"model_or_adapter_construction_started\") == 0" in source
    assert "resource.setrlimit(resource.RLIMIT_AS" not in source
    assert '"C02 manifest activation hash drift"' in source
    assert '"C02 manifest committed byte drift"' in source
    assert '"C02 terminal output and failure both exist"' in source


def test_c02_paths_are_relative_and_unique() -> None:
    entries = c02.translated_matrix(ROOT)["entries"]
    paths = [
        path
        for row in entries
        for path in (
            row["primary_claim_path"],
            row["retry_claim_path"],
            row["primary_output_path"],
            row["retry_output_path"],
        )
    ]
    assert len(paths) == 936
    assert len(set(paths)) == 936
    assert all(not Path(path).is_absolute() for path in paths)


def test_c01_claim_and_outputs_are_not_mutated_by_translation() -> None:
    audit = c02.load_json(ROOT / c02.C01_AUDIT_REL)
    assert audit["mechanical_disposition"]["matrix_entries_claimed"] == 1
    assert audit["mechanical_disposition"]["matrix_entries_evaluable"] == 0
    assert audit["continuation_boundary"]["successor_cycle_id"] == "P2-I2-C02"
    assert (ROOT / c02.C01_CLAIM_REL).is_file()
