"""Unreplayable reports are not evidence."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from adventure_forge.kernel.content import load_pack
from adventure_forge.kernel.replay import ReplayError, replay


class RejectedReportTests(unittest.TestCase):
    def test_buy_the_harbor_does_not_replay(self) -> None:
        report = json.loads(
            (ROOT / "orchestrator" / "evidence" / "rejected-report.json").read_text(encoding="utf-8")
        )
        content = load_pack()
        with self.assertRaises(ReplayError):
            replay(content, report["seed"], report["sheet"], report["actions"], require_accepted=True)
