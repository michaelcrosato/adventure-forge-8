"""Player-surface finding must replay on the shipped engine."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from adventure_forge.kernel.content import load_pack
from adventure_forge.kernel.replay import replay
from adventure_forge.play.session import PlaySession


class FindingReplayTests(unittest.TestCase):
    def test_mira_finding_session_replays(self) -> None:
        finding = json.loads(
            (ROOT / "orchestrator" / "evidence" / "player-finding-mira.json").read_text(encoding="utf-8")
        )
        content = load_pack()
        result = replay(content, finding["seed"], finding["sheet"], finding["actions"])
        self.assertEqual(result.state.location, "stacks.base")
        self.assertTrue(result.state.flags.get("marsh_friend"))
        session = PlaySession.start(content, finding["seed"], finding["sheet"])
        for action_id in finding["actions"]:
            turn = session.apply_line(action_id)
            self.assertTrue(turn.accepted, action_id)
        self.assertEqual(session.fingerprint(), result.fingerprint)
