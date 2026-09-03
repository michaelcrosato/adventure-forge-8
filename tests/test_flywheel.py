"""Player-surface findings must land as shipped legal actions."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from adventure_forge.kernel.content import load_pack
from adventure_forge.kernel.legal import enumerate_legal
from adventure_forge.kernel.replay import replay


class FlywheelFindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.content = load_pack()

    def test_share_marsh_path_legal_after_marsh_cant(self) -> None:
        finding = json.loads(
            (ROOT / "orchestrator" / "evidence" / "player-finding-mira.json").read_text(
                encoding="utf-8"
            )
        )
        result = replay(self.content, finding["seed"], finding["sheet"], finding["actions"])
        self.assertEqual(result.state.location, "stacks.base")
        legal_ids = {a.id for a in enumerate_legal(result.state, self.content)}
        self.assertIn("share_marsh_path", legal_ids)

    def test_city_oath_lacks_share_marsh_path_at_stacks(self) -> None:
        result = replay(
            self.content,
            1,
            "city_oath",
            ["go:saltfen.market", "go:ashfen.causeway", "go:stacks.base"],
        )
        self.assertEqual(result.state.location, "stacks.base")
        legal_ids = {a.id for a in enumerate_legal(result.state, self.content)}
        self.assertNotIn("share_marsh_path", legal_ids)

    def test_prior_outcome_traces_still_replay(self) -> None:
        compact = json.loads(
            (ROOT / "traces" / "marsh_harbor_compact.json").read_text(encoding="utf-8")
        )
        relic = json.loads(
            (ROOT / "traces" / "marsh_stack_relic.json").read_text(encoding="utf-8")
        )
        r1 = replay(self.content, compact["seed"], compact["sheet"], compact["actions"])
        r2 = replay(self.content, relic["seed"], relic["sheet"], relic["actions"])
        self.assertIn("harbor_compact", r1.state.outcomes)
        self.assertIn("stack_relic", r2.state.outcomes)


if __name__ == "__main__":
    unittest.main()
