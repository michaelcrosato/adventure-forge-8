"""Kiln Mill slice: new outcome, sheet divergence, harbor cross-effect."""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from adventure_forge.kernel.content import load_pack
from adventure_forge.kernel.legal import enumerate_legal
from adventure_forge.kernel.replay import replay
from adventure_forge.play.session import PlaySession
from adventure_forge.verify.i4 import TraceReject, accept_trace


def _trace(name: str) -> dict:
    return json.loads((ROOT / "traces" / f"{name}.json").read_text(encoding="utf-8"))


class KilnMillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.content = load_pack()

    def test_prior_outcomes_still_replay(self) -> None:
        compact = _trace("marsh_harbor_compact")
        relic = _trace("marsh_stack_relic")
        r1 = replay(self.content, compact["seed"], compact["sheet"], compact["actions"])
        r2 = replay(self.content, relic["seed"], relic["sheet"], relic["actions"])
        self.assertIn("harbor_compact", r1.state.outcomes)
        self.assertIn("stack_relic", r2.state.outcomes)
        self.assertTrue(self.content.outcome_ready("harbor_compact", r1.state))
        self.assertTrue(self.content.outcome_ready("stack_relic", r2.state))

    def test_kiln_pact_trace_replays_to_predicate(self) -> None:
        trace = _trace("marsh_kiln_pact")
        result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
        self.assertIn("kiln_pact", result.state.outcomes)
        self.assertTrue(self.content.outcome_ready("kiln_pact", result.state))
        self.assertTrue(result.state.flags.get("kiln_pact_sealed"))
        self.assertEqual(result.fingerprint, trace["final_fingerprint"])
        accept_trace(self.content, trace)

    def test_mill_yard_sheet_divergence(self) -> None:
        marsh = replay(self.content, 1, "marsh_scout", _trace("divergence_marsh_mill")["actions"])
        city = replay(self.content, 1, "city_oath", _trace("divergence_city_mill")["actions"])
        self.assertEqual(marsh.state.location, "mill.yard")
        self.assertEqual(city.state.location, "mill.yard")
        marsh_ids = {a.id for a in enumerate_legal(marsh.state, self.content)}
        city_ids = {a.id for a in enumerate_legal(city.state, self.content)}
        self.assertIn("offer_reed_grain", marsh_ids)
        self.assertNotIn("offer_reed_grain", city_ids)
        self.assertIn("read_debt_ledger", city_ids)
        self.assertNotIn("read_debt_ledger", marsh_ids)

    def test_compact_deed_changes_mill_verbs(self) -> None:
        plain = replay(self.content, 1, "marsh_scout", _trace("cross_plain_mill")["actions"])
        compact = replay(self.content, 1, "marsh_scout", _trace("cross_compact_mill")["actions"])
        self.assertEqual(plain.state.location, compact.state.location)
        self.assertEqual(plain.state.location, "mill.yard")
        plain_ids = {a.id for a in enumerate_legal(plain.state, self.content)}
        compact_ids = {a.id for a in enumerate_legal(compact.state, self.content)}
        self.assertNotIn("cite_dock_compact", plain_ids)
        self.assertIn("cite_dock_compact", compact_ids)
        self.assertIn("harbor_compact", compact.state.outcomes)

    def test_player_plain_language_reaches_kiln_pact(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        lines = [
            "go to market",
            "go to causeway",
            "go to mill lane",
            "go to mill yard",
            "offer reed grain",
            "go to kiln",
            "kindle the kiln",
            "stoke the kiln",
            "fire the grain pact",
        ]
        for line in lines:
            turn = session.apply_line(line)
            self.assertTrue(turn.accepted, line)
        self.assertIn("kiln_pact", session.state.outcomes)
        obs = session.observation()
        self.assertIn("You can:", obs.text)
        self.assertLess(obs.prose_word_count, 120)

    def test_unmapped_text_still_noop(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        session.apply_line("go to market")
        session.apply_line("go to causeway")
        session.apply_line("go to mill lane")
        before = session.fingerprint()
        turn = session.apply_line("enchant the millstone with starfire")
        self.assertFalse(turn.accepted)
        self.assertEqual(session.fingerprint(), before)

    def test_i4_still_rejects_tampered_build_id(self) -> None:
        trace = copy.deepcopy(_trace("marsh_kiln_pact"))
        accept_trace(self.content, copy.deepcopy(trace))
        trace["build_id"] = "tampered-build"
        with self.assertRaises(TraceReject) as ctx:
            accept_trace(self.content, trace)
        self.assertIn("build_id", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
