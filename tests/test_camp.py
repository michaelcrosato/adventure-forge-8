"""Fever Camp slice: medicine outcome, sheet divergence, beacon cross-effect."""

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


class FeverCampTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.content = load_pack()

    def test_prior_outcomes_still_replay(self) -> None:
        for name, outcome in (
            ("marsh_harbor_compact", "harbor_compact"),
            ("marsh_stack_relic", "stack_relic"),
            ("marsh_kiln_pact", "kiln_pact"),
            ("marsh_reed_sentence", "reed_sentence"),
            ("marsh_road_beacon", "road_beacon"),
        ):
            trace = _trace(name)
            result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
            self.assertIn(outcome, result.state.outcomes, name)

    def test_fever_broken_trace_replays(self) -> None:
        trace = _trace("marsh_fever_broken")
        result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
        self.assertIn("fever_broken", result.state.outcomes)
        self.assertTrue(self.content.outcome_ready("fever_broken", result.state))
        self.assertEqual(result.fingerprint, trace["final_fingerprint"])
        accept_trace(self.content, trace)

    def test_yard_sheet_divergence(self) -> None:
        marsh = replay(self.content, 1, "marsh_scout", _trace("divergence_marsh_camp")["actions"])
        city = replay(self.content, 1, "city_oath", _trace("divergence_city_camp")["actions"])
        self.assertEqual(marsh.state.location, "camp.yard")
        self.assertEqual(city.state.location, "camp.yard")
        marsh_ids = {a.id for a in enumerate_legal(marsh.state, self.content)}
        city_ids = {a.id for a in enumerate_legal(city.state, self.content)}
        self.assertIn("cut_reed_herb", marsh_ids)
        self.assertNotIn("cut_reed_herb", city_ids)
        self.assertIn("read_isolation_order", city_ids)
        self.assertNotIn("read_isolation_order", marsh_ids)

    def test_beacon_deed_changes_camp_verbs(self) -> None:
        plain = replay(self.content, 1, "marsh_scout", _trace("cross_plain_camp")["actions"])
        beacon = replay(self.content, 1, "marsh_scout", _trace("cross_beacon_camp")["actions"])
        self.assertEqual(plain.state.location, "camp.gate")
        self.assertEqual(beacon.state.location, "camp.gate")
        plain_ids = {a.id for a in enumerate_legal(plain.state, self.content)}
        beacon_ids = {a.id for a in enumerate_legal(beacon.state, self.content)}
        self.assertNotIn("hail_clean_boat", plain_ids)
        self.assertIn("hail_clean_boat", beacon_ids)
        self.assertIn("road_beacon", beacon.state.outcomes)

    def test_player_plain_language_breaks_fever(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        lines = [
            "go to market",
            "go to causeway",
            "go to fever camp",
            "go to camp yard",
            "cut reed herb",
            "go to still",
            "brew fever broth",
            "go to camp yard",
            "go to ward",
            "give Ren the broth",
        ]
        for line in lines:
            turn = session.apply_line(line)
            self.assertTrue(turn.accepted, line)
        self.assertIn("fever_broken", session.state.outcomes)
        self.assertIn("You can:", session.observation().text)
        self.assertLess(session.observation().prose_word_count, 120)

    def test_unmapped_text_still_noop_at_camp(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        for line in ("go to market", "go to causeway", "go to fever camp"):
            self.assertTrue(session.apply_line(line).accepted, line)
        before = session.fingerprint()
        turn = session.apply_line("banish the fever with a shout")
        self.assertFalse(turn.accepted)
        self.assertEqual(session.fingerprint(), before)

    def test_i4_rejects_tampered_build_on_camp_trace(self) -> None:
        trace = copy.deepcopy(_trace("marsh_fever_broken"))
        accept_trace(self.content, copy.deepcopy(trace))
        trace["build_id"] = "tampered-build"
        with self.assertRaises(TraceReject):
            accept_trace(self.content, trace)


if __name__ == "__main__":
    unittest.main()
