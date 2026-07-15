#!/usr/bin/env python3
"""Remove only the frozen I08 live-import bytecode caches and retain a receipt."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any


EXPERIMENT = Path("experiments/2026-07-AE01-post-n30-demand-composition-atlas")
INPUT_FREEZE = EXPERIMENT / "contracts/p2-i2/c01/i08-activation-input-freeze.json"
RECEIPT = EXPERIMENT / "contracts/p2-i2/c01/i08-import-cache-cleanup-receipt.json"
EXPECTED_GRAPH_HEAD = "83e3a300426631ee4df71b661b67d4fcfdfed594"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git(repository: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", os.fspath(repository), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def inventory(label: str, root: Path) -> list[dict[str, str]]:
    require(root.is_dir() and not root.is_symlink(), f"unsafe import root: {label}")
    entries: list[dict[str, str]] = []
    for current, directories, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        relative = current_path.relative_to(root)
        for directory in sorted(directories):
            candidate = current_path / directory
            require(not candidate.is_symlink(), f"symlink below import root: {label}:{candidate.relative_to(root)}")
            if directory == "__pycache__":
                entries.append(
                    {
                        "root": label,
                        "path": (relative / directory).as_posix(),
                        "kind": "cache_directory",
                    }
                )
        for name in sorted(files):
            if name.endswith((".pyc", ".pyo")):
                candidate = current_path / name
                require(not candidate.is_symlink(), f"symlinked bytecode file: {label}:{candidate.relative_to(root)}")
                entries.append(
                    {
                        "root": label,
                        "path": (relative / name).as_posix(),
                        "kind": "bytecode_file",
                    }
                )
    return sorted(entries, key=lambda item: (item["root"], item["path"], item["kind"]))


def remove_inventory(roots: dict[str, Path], entries: list[dict[str, str]]) -> None:
    cache_directories = [entry for entry in entries if entry["kind"] == "cache_directory"]
    bytecode_files = [entry for entry in entries if entry["kind"] == "bytecode_file"]
    for entry in bytecode_files:
        path = roots[entry["root"]] / entry["path"]
        if any(parent.name == "__pycache__" for parent in path.parents):
            continue
        require(path.is_file() and not path.is_symlink(), f"bytecode path changed: {entry}")
        path.unlink()
    for entry in sorted(cache_directories, key=lambda item: item["path"].count("/"), reverse=True):
        path = roots[entry["root"]] / entry["path"]
        if not path.exists():
            continue
        require(path.is_dir() and not path.is_symlink() and path.name == "__pycache__", f"cache path changed: {entry}")
        shutil.rmtree(path)


def write_new(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(document, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(payload)
    except BaseException:
        if path.exists() and not path.is_symlink():
            path.unlink()
        raise


def main() -> int:
    repository = Path(__file__).resolve().parents[3]
    graph = (repository / "../graph-reflexive-coherence").resolve()
    require(sys.dont_write_bytecode, "cleanup requires .venv/bin/python -B")
    require(Path(sys.prefix).resolve() == (repository / ".venv").resolve(), "repository .venv inactive")
    require((repository / INPUT_FREEZE).is_file(), "I08 activation input freeze absent")
    require(not (repository / RECEIPT).exists(), "cleanup receipt already exists")
    require(git(graph, "rev-parse", "HEAD") == EXPECTED_GRAPH_HEAD, "graph revision drift")
    graph_status_before = git(graph, "status", "--porcelain", "--untracked-files=no")
    require(not graph_status_before, "tracked graph worktree dirty before cache cleanup")
    roots = {
        "experiment_scripts": repository / EXPERIMENT / "scripts",
        "pygrc_source": graph / "src",
    }
    before = inventory("experiment_scripts", roots["experiment_scripts"]) + inventory(
        "pygrc_source", roots["pygrc_source"]
    )
    require(before, "frozen cleanup start unexpectedly has no import caches")
    remove_inventory(roots, before)
    after = inventory("experiment_scripts", roots["experiment_scripts"]) + inventory(
        "pygrc_source", roots["pygrc_source"]
    )
    require(not after, "import cache remains after cleanup")
    graph_status_after = git(graph, "status", "--porcelain", "--untracked-files=no")
    require(not graph_status_after, "tracked graph worktree changed during cache cleanup")
    document = {
        "artifact_id": "P2-I2-I08-IMPORT-CACHE-CLEANUP-RECEIPT",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I08",
        "cycle_id": "P2-I2-C01",
        "status": "complete_candidate_free",
        "input_freeze_sha256": sha256(repository / INPUT_FREEZE),
        "cleanup_source_sha256": sha256(Path(__file__).resolve()),
        "command": [
            ".venv/bin/python",
            "-B",
            (EXPERIMENT / "scripts/p2_i2_i08_cleanup_import_caches.py").as_posix(),
        ],
        "roots": ["experiment_scripts", "pygrc_source"],
        "before_count": len(before),
        "before_inventory": before,
        "after_count": len(after),
        "after_inventory": after,
        "graph_revision_before_and_after": EXPECTED_GRAPH_HEAD,
        "graph_tracked_status_before": graph_status_before,
        "graph_tracked_status_after": graph_status_after,
        "tracked_bytes_changed": 0,
        "pygrc_imports": 0,
        "models_or_adapters_constructed": 0,
        "candidate_or_control_operations": 0,
        "scientific_windows": 0,
    }
    write_new(repository / RECEIPT, document)
    print(json.dumps({"removed": len(before), "remaining": len(after)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
