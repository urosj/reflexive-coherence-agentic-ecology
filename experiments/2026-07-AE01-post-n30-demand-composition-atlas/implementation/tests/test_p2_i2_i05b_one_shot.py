from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import threading
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

import p2_i2_i05b_one_shot as one_shot  # noqa: E402


class P2I2I05BOneShotSafetyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_policy = json.loads(
            (EXPERIMENT / "configs/p2_i2_i05b_one_shot_policy.json").read_text(
                encoding="utf-8"
            )
        )

    def setUp(self) -> None:
        (ROOT / "outputs").mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(
            prefix="p2-i2-i05b-safety-",
            dir=ROOT / "outputs",
        )
        self.temp_path = Path(self.temporary.name)
        self.policy = deepcopy(self.base_policy)
        for key, name in (
            ("attempt_receipt", "attempt.json"),
            ("final_receipt", "final.json"),
            ("governed_output", "calibration.json"),
        ):
            self.policy["paths"][key] = str(
                (self.temp_path / name).relative_to(ROOT)
            )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _claim(self, path: Path, barrier: threading.Barrier | None = None) -> str:
        if barrier is not None:
            barrier.wait()
        try:
            one_shot.claim_attempt(path, {"authorization_consumed": True})
        except one_shot.AttemptAlreadyClaimed:
            return "refused"
        return "claimed"

    def test_concurrent_second_start_is_refused(self) -> None:
        claim = self.temp_path / "concurrent-claim.json"
        barrier = threading.Barrier(2)
        with ThreadPoolExecutor(max_workers=2) as executor:
            outcomes = list(
                executor.map(lambda _: self._claim(claim, barrier), range(2))
            )
        self.assertEqual(sorted(outcomes), ["claimed", "refused"])
        self.assertTrue(claim.exists())

    def test_start_after_claimed_attempt_is_refused(self) -> None:
        claim = self.temp_path / "claimed.json"
        one_shot.claim_attempt(claim, {"authorization_consumed": True})
        with self.assertRaises(one_shot.AttemptAlreadyClaimed):
            one_shot.claim_attempt(claim, {"authorization_consumed": True})
        self.assertTrue(one_shot.demonstrate_second_start_refused(claim))

    def test_start_after_simulated_crash_following_claim_is_refused(self) -> None:
        claim = self.temp_path / "crash-claim.json"
        one_shot.claim_attempt(
            claim,
            {
                "authorization_consumed": True,
                "claim_state": "consumed_before_simulated_crash",
            },
        )
        self.assertFalse((self.temp_path / "final-after-crash.json").exists())
        with self.assertRaises(one_shot.AttemptAlreadyClaimed):
            one_shot.claim_attempt(claim, {"forbidden_retry": True})
        self.assertTrue(claim.exists())

    def test_dirty_authority_files_or_index_are_refused(self) -> None:
        head = "a" * 40
        for porcelain in (" M authority.json", "M  authority.json"):
            with self.subTest(porcelain=porcelain), self.assertRaises(
                one_shot.OneShotError
            ):
                one_shot.validate_repository_snapshot(
                    {
                        "head": head,
                        "index_clean": not porcelain.startswith("M "),
                        "porcelain": porcelain,
                        "worktree_clean": not porcelain.startswith(" M"),
                    },
                    head,
                )

    def test_wrong_head_is_refused(self) -> None:
        with self.assertRaises(one_shot.OneShotError):
            one_shot.validate_repository_snapshot(
                {
                    "head": "a" * 40,
                    "index_clean": True,
                    "porcelain": "",
                    "worktree_clean": True,
                },
                "b" * 40,
            )

    def test_wrong_interpreter_or_command_is_refused(self) -> None:
        identity = one_shot.interpreter_identity()
        wrong_identity = dict(identity)
        wrong_identity["invoked_executable_repo_relative"] = "wrong/python"
        with self.assertRaises(one_shot.OneShotError):
            one_shot.validate_interpreter(wrong_identity, self.policy)

        inactive_identity = dict(identity)
        inactive_identity["venv_active"] = False
        with self.assertRaises(one_shot.OneShotError):
            one_shot.validate_interpreter(inactive_identity, self.policy)

        wrong_digest = dict(identity)
        wrong_digest["binary_sha256"] = "0" * 64
        with self.assertRaises(one_shot.OneShotError):
            one_shot.validate_interpreter(wrong_digest, self.policy)

        head = "a" * 40
        command = one_shot.normalized_command(self.policy, head)
        command[1] = "experiments/wrong-wrapper.py"
        with self.assertRaises(one_shot.OneShotError):
            one_shot.validate_command(command, self.policy, head)

    def test_active_repository_venv_identity_passes(self) -> None:
        identity = one_shot.interpreter_identity()
        one_shot.validate_interpreter(identity, self.policy)
        self.assertTrue(identity["venv_active"])
        self.assertEqual(
            identity["invoked_executable_repo_relative"], ".venv/bin/python"
        )
        self.assertEqual(identity["venv_prefix_repo_relative"], ".venv")
        self.assertTrue(identity["base_runtime_separated"])

    def test_existing_governed_output_is_refused(self) -> None:
        output = ROOT / self.policy["paths"]["governed_output"]
        output.write_text("already present\n", encoding="utf-8")
        with self.assertRaises(one_shot.OneShotError):
            one_shot.validate_preclaim_absence(self.policy)

    def test_permanent_claim_storage_rejects_symlink_or_partial_claim(self) -> None:
        storage = one_shot.validate_claim_storage(self.policy)
        self.assertEqual(storage["filesystem_type"], "ext4")
        self.assertTrue(storage["repository_local"])
        claim = ROOT / self.policy["paths"]["attempt_receipt"]
        claim.symlink_to(self.temp_path / "missing-target")
        with self.assertRaises(one_shot.AttemptAlreadyClaimed):
            one_shot.validate_preclaim_absence(self.policy)
        claim.unlink()
        claim.write_bytes(b"")
        with self.assertRaises(one_shot.AttemptAlreadyClaimed):
            one_shot.validate_preclaim_absence(self.policy)

    def test_owner_acceptance_does_not_substitute_for_launch_authority(self) -> None:
        frozen = one_shot.validate_frozen_hashes(self.base_policy)
        policy_path = ROOT / self.base_policy["paths"]["policy"]
        policy_sha = hashlib.sha256(policy_path.read_bytes()).hexdigest()
        acceptance = one_shot.validate_owner_acceptance(
            self.base_policy,
            policy_sha256=policy_sha,
            frozen_hashes=frozen,
        )
        self.assertTrue(acceptance["owner_acceptance"])
        self.assertTrue(acceptance["commit_authorized"])
        self.assertFalse(acceptance["null_invocation_authorized"])
        no_launch_policy = deepcopy(self.base_policy)
        no_launch_policy["paths"]["null_launch_authorization"] = str(
            (self.temp_path / "absent-launch.json").relative_to(ROOT)
        )
        with self.assertRaises(one_shot.OneShotError):
            one_shot.validate_null_launch_authorization(
                no_launch_policy,
                owner_acceptance_sha256=hashlib.sha256(
                    (ROOT / self.base_policy["paths"]["owner_acceptance"]).read_bytes()
                ).hexdigest(),
                policy_sha256=policy_sha,
                frozen_hashes=frozen,
            )

    def test_builder_invocation_during_safety_validation_is_zero(self) -> None:
        head = "a" * 40
        with patch.object(one_shot, "_invoke_accepted_builder_once") as builder:
            with self.assertRaises(one_shot.OneShotError):
                one_shot.validate_repository_snapshot(
                    {
                        "head": "b" * 40,
                        "index_clean": True,
                        "porcelain": "",
                        "worktree_clean": True,
                    },
                    head,
                )
            with self.assertRaises(one_shot.OneShotError):
                one_shot.validate_command(["wrong"], self.policy, head)
            builder.assert_not_called()

    def test_policy_freezes_one_attempt_zero_retries_and_i04r2_hashes(self) -> None:
        one_shot.validate_policy(self.base_policy)
        self.assertEqual(
            self.base_policy["attempt_policy"]["max_governed_attempts"], 1
        )
        self.assertEqual(
            self.base_policy["attempt_policy"]["max_infrastructure_retries"], 0
        )
        actual = one_shot.validate_frozen_hashes(self.base_policy)
        self.assertEqual(actual, self.base_policy["frozen_hashes"])

    def test_final_receipt_shape_separates_generation_and_readback(self) -> None:
        receipt = one_shot._final_receipt(
            policy=self.base_policy,
            claim_sha256="a" * 64,
            status="completed",
            builder_invocations=1,
            readbacks=1,
            second_refused=True,
            output_sha256="b" * 64,
            failure=None,
        )
        self.assertEqual(receipt["null_invocation_count"], 1)
        self.assertEqual(receipt["accepted_builder_invocation_count"], 1)
        self.assertEqual(receipt["governed_attempt_count"], 1)
        self.assertEqual(receipt["null_reconstruction_generation_count"], 0)
        self.assertEqual(receipt["output_readback_reconstruction_count"], 1)
        self.assertTrue(receipt["authorization_consumed"])
        self.assertTrue(receipt["second_invocation_refused"])


if __name__ == "__main__":
    unittest.main()
