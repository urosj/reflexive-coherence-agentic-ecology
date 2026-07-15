"""PyGRC-free retained-output reconstruction for APP-B4."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import sys
from typing import Any

from p2_i2_app_b4_analysis import analyze_receipts, canonical_bytes, digest_value


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT_REL = "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
MACHINE_REL = f"{EXPERIMENT_REL}/configs/p2_i2_i04r2_machine_policy.json"
PARENT_REL = f"{EXPERIMENT_REL}/configs/p2_i2_i04r1_analysis_policy.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON object required: {path}")
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    for value in (args.freeze, args.input, args.output):
        require(not PurePosixPath(value).is_absolute() and not PureWindowsPath(value).is_absolute(), "absolute path refused")
    require(Path(sys.executable) == ROOT / ".venv/bin/python", "reconstructor not launched through lexical repository .venv")
    require(Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(), "repository .venv inactive")
    require(sys.dont_write_bytecode, "reconstructor requires -B")
    freeze = load_json(ROOT / args.freeze)
    retained = load_json(ROOT / args.input)
    without_digest = {key: value for key, value in retained.items() if key != "canonical_payload_digest"}
    require(digest_value(without_digest) == retained["canonical_payload_digest"], "retained digest drifted")
    require((ROOT / args.input).read_bytes() == canonical_bytes(retained), "retained output noncanonical")
    reconstructed_native = analyze_receipts(
        retained["receipts"],
        freeze,
        load_json(ROOT / MACHINE_REL),
        load_json(ROOT / PARENT_REL),
    )
    reconstructed = json.loads(canonical_bytes(reconstructed_native))
    require(canonical_bytes(reconstructed_native) == canonical_bytes(retained["analysis"]), "APP-B4 canonical analysis bytes differ")
    require(reconstructed == retained["analysis"], "APP-B4 analysis reconstruction differs")
    result = {
        "artifact_id": "P2-I2-APP-B4-RECONSTRUCTION-AND-CLOSEOUT",
        "artifact_version": "1.0",
        "retained_input": {"path": args.input, "sha256": sha256(ROOT / args.input)},
        "freeze": {"path": args.freeze, "sha256": sha256(ROOT / args.freeze)},
        "analysis_reconstruction_byte_identical": canonical_bytes(reconstructed) == canonical_bytes(retained["analysis"]),
        "json_seed_key_normalization_applied": True,
        "arm_count_reconstructed": len(retained["receipts"]),
        "runtime_generation_count": 0,
        "PyGRC_import_count": 0,
        "model_count": 0,
        "producer_count": 0,
        "output_readback_reconstruction_count": 1,
        "scientific_retry_count": 0,
        "analysis": reconstructed,
        "final_owner_acceptance_required": True,
        "result_commit_authorized": False,
    }
    result["canonical_payload_digest"] = digest_value(result)
    output = ROOT / args.output
    require(not output.exists(), "APP-B4 closeout output already exists")
    output.write_bytes(canonical_bytes(result))
    require(load_json(output) == result, "APP-B4 closeout readback drifted")
    print(json.dumps({"status": "reconstructed", "arms": len(retained["receipts"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
