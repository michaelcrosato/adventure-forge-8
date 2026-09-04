"""Windpump: vanes-crank-hold outcome, sheet divergence, ferry cross-effect."""

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


class WindpumpTests(unittest.TestCase):
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
            ("marsh_fever_broken", "fever_broken"),
            ("marsh_name_restored", "name_restored"),
            ("marsh_fold_held", "fold_held"),
            ("marsh_lens_set", "lens_set"),
            ("marsh_rope_walked", "rope_walked"),
            ("marsh_salt_raked", "salt_raked"),
            ("marsh_smoke_cured", "smoke_cured"),
            ("marsh_weir_lifted", "weir_lifted"),
            ("marsh_dye_struck", "dye_struck"),
            ("marsh_ferry_crossed", "ferry_crossed"),
        ):
            trace = _trace(name)
            result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
            self.assertIn(outcome, result.state.outcomes, name)

    def test_flats_drained_trace_replays(self) -> None:
        trace = _trace("marsh_flats_drained")
        result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
        self.assertIn("flats_drained", result.state.outcomes)
        self.assertEqual(result.state.location, "pump.sump")
        self.assertTrue(self.content.outcome_ready("flats_drained", result.state))
        self.assertEqual(result.fingerprint, trace["final_fingerprint"])
        accept_trace(self.content, trace)

    def test_yard_sheet_divergence(self) -> None:
        marsh = replay(self.content, 1, "marsh_scout", _trace("divergence_marsh_pump")["actions"])
        city = replay(self.content, 1, "city_oath", _trace("divergence_city_pump")["actions"])
        self.assertEqual(marsh.state.location, "pump.yard")
        marsh_ids = {a.id for a in enumerate_legal(marsh.state, self.content)}
        city_ids = {a.id for a in enumerate_legal(city.state, self.content)}
        self.assertIn("know_the_wind_cut", marsh_ids)
        self.assertNotIn("know_the_wind_cut", city_ids)
        self.assertIn("read_the_pump_mark", city_ids)
        self.assertNotIn("read_the_pump_mark", marsh_ids)

    def test_ferry_crossed_changes_tower_verbs(self) -> None:
        plain = replay(self.content, 1, "marsh_scout", _trace("cross_plain_pump")["actions"])
        crossed = replay(self.content, 1, "marsh_scout", _trace("cross_ferry_pump")["actions"])
        self.assertEqual(plain.state.location, "pump.tower")
        self.assertEqual(crossed.state.location, "pump.tower")
        plain_ids = {a.id for a in enumerate_legal(plain.state, self.content)}
        crossed_ids = {a.id for a in enumerate_legal(crossed.state, self.content)}
        self.assertNotIn("brace_the_sail", plain_ids)
        self.assertIn("brace_the_sail", crossed_ids)
        self.assertIn("ferry_crossed", crossed.state.outcomes)

    def test_far_landing_links_to_windpump(self) -> None:
        result = replay(self.content, 1, "marsh_scout", _trace("marsh_ferry_crossed")["actions"])
        self.assertEqual(result.state.location, "ferry.far")
        ids = {a.id for a in enumerate_legal(result.state, self.content)}
        self.assertIn("go:pump.path", ids)

    def test_player_plain_language_drains_flats(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        lines = [
            "go to market",
            "go to causeway",
            "go to windpump",
            "go to pump yard",
            "know the wind cut",
            "go to the vane tower",
            "take vane pin",
            "set the vanes",
            "go to pump yard",
            "go to the crank",
            "crank the pump",
            "go to pump yard",
            "go to the sump",
            "hold the draw",
        ]
        for line in lines:
            turn = session.apply_line(line)
            self.assertTrue(turn.accepted, line)
        self.assertIn("flats_drained", session.state.outcomes)
        self.assertIn("You can:", session.observation().text)
        self.assertLess(session.observation().prose_word_count, 120)

    def test_unmapped_text_still_noop_in_yard(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        for line in ("go to market", "go to causeway", "go to windpump"):
            self.assertTrue(session.apply_line(line).accepted, line)
        before = session.fingerprint()
        turn = session.apply_line("summon a dry wind")
        self.assertFalse(turn.accepted)
        self.assertEqual(session.fingerprint(), before)

    def test_i4_rejects_tampered_build_on_pump_trace(self) -> None:
        trace = copy.deepcopy(_trace("marsh_flats_drained"))
        accept_trace(self.content, copy.deepcopy(trace))
        trace["build_id"] = "tampered-build"
        with self.assertRaises(TraceReject):
            accept_trace(self.content, trace)


if __name__ == "__main__":
    unittest.main()
