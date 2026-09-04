"""Drowned Road slice: beacon outcome, sheet divergence, weather, court cross-effect."""

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
from adventure_forge.kernel.replay import new_game, replay
from adventure_forge.kernel.state import weather
from adventure_forge.kernel.step import step
from adventure_forge.play.session import PlaySession
from adventure_forge.verify.i4 import TraceReject, accept_trace


def _trace(name: str) -> dict:
    return json.loads((ROOT / "traces" / f"{name}.json").read_text(encoding="utf-8"))


class DrownedRoadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.content = load_pack()

    def test_prior_outcomes_still_replay(self) -> None:
        for name, outcome in (
            ("marsh_harbor_compact", "harbor_compact"),
            ("marsh_stack_relic", "stack_relic"),
            ("marsh_kiln_pact", "kiln_pact"),
            ("marsh_reed_sentence", "reed_sentence"),
        ):
            trace = _trace(name)
            result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
            self.assertIn(outcome, result.state.outcomes, name)

    def test_road_beacon_trace_replays(self) -> None:
        trace = _trace("marsh_road_beacon")
        result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
        self.assertIn("road_beacon", result.state.outcomes)
        self.assertTrue(self.content.outcome_ready("road_beacon", result.state))
        self.assertEqual(result.fingerprint, trace["final_fingerprint"])
        accept_trace(self.content, trace)

    def test_hut_sheet_divergence(self) -> None:
        marsh = replay(self.content, 1, "marsh_scout", _trace("divergence_marsh_road")["actions"])
        city = replay(self.content, 1, "city_oath", _trace("divergence_city_road")["actions"])
        self.assertEqual(marsh.state.location, "road.hut")
        marsh_ids = {a.id for a in enumerate_legal(marsh.state, self.content)}
        city_ids = {a.id for a in enumerate_legal(city.state, self.content)}
        self.assertIn("track_drowned_prints", marsh_ids)
        self.assertNotIn("track_drowned_prints", city_ids)
        self.assertIn("force_hut_latch", city_ids)
        self.assertNotIn("force_hut_latch", marsh_ids)

    def test_reed_sentence_changes_road_verbs(self) -> None:
        plain = replay(self.content, 1, "marsh_scout", _trace("cross_plain_road")["actions"])
        court = replay(self.content, 1, "marsh_scout", _trace("cross_court_road")["actions"])
        self.assertEqual(plain.state.location, "road.hut")
        self.assertEqual(court.state.location, "road.hut")
        plain_ids = {a.id for a in enumerate_legal(plain.state, self.content)}
        court_ids = {a.id for a in enumerate_legal(court.state, self.content)}
        self.assertNotIn("name_the_sentence", plain_ids)
        self.assertIn("name_the_sentence", court_ids)
        self.assertIn("reed_sentence", court.state.outcomes)

    def test_rain_unlocks_flood_berm_via_step(self) -> None:
        state, cursor = new_game(self.content, 1, "marsh_scout")
        for action_id in ("go:saltfen.market", "go:ashfen.causeway", "go:road.ford", "go:road.dike"):
            result = step(state, action_id, self.content, cursor)
            self.assertTrue(result.accepted, action_id)
            state, cursor = result.state, result.cursor
        self.assertEqual(state.location, "road.dike")
        while weather(state) != "rain":
            result = step(state, "wait", self.content, cursor)
            self.assertTrue(result.accepted)
            state, cursor = result.state, result.cursor
            self.assertLess(state.turn, 20)
        ids = {a.id for a in enumerate_legal(state, self.content)}
        self.assertIn("walk_the_flood_berm", ids)
        result = step(state, "walk_the_flood_berm", self.content, cursor)
        self.assertTrue(result.accepted)
        self.assertTrue(result.state.flags.get("walked_berm"))

    def test_player_plain_language_lights_beacon(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        lines = [
            "go to market",
            "go to causeway",
            "go to drowned road",
            "go to dike",
            "go to hut",
            "track drowned prints",
            "go to beacon",
            "light the road beacon",
        ]
        for line in lines:
            turn = session.apply_line(line)
            self.assertTrue(turn.accepted, line)
        self.assertIn("road_beacon", session.state.outcomes)
        self.assertIn("You can:", session.observation().text)
        self.assertLess(session.observation().prose_word_count, 120)

    def test_i4_rejects_tampered_build_on_road_trace(self) -> None:
        trace = copy.deepcopy(_trace("marsh_road_beacon"))
        accept_trace(self.content, copy.deepcopy(trace))
        trace["build_id"] = "tampered-build"
        with self.assertRaises(TraceReject):
            accept_trace(self.content, trace)


if __name__ == "__main__":
    unittest.main()
