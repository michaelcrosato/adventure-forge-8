"""Wreck Chapel: wash-and-lay outcome, sheet divergence, ice-cellar cross-effect."""

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


class WreckChapelTests(unittest.TestCase):
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
            ("marsh_flats_drained", "flats_drained"),
            ("marsh_oyster_culled", "oyster_culled"),
            ("marsh_tally_closed", "tally_closed"),
            ("marsh_ice_held", "ice_held"),
        ):
            trace = _trace(name)
            result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
            self.assertIn(outcome, result.state.outcomes, name)

    def test_wreck_laid_trace_replays(self) -> None:
        trace = _trace("marsh_wreck_laid")
        result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
        self.assertIn("wreck_laid", result.state.outcomes)
        self.assertEqual(result.state.location, "wreck.altar")
        self.assertTrue(self.content.outcome_ready("wreck_laid", result.state))
        self.assertEqual(result.fingerprint, trace["final_fingerprint"])
        accept_trace(self.content, trace)

    def test_yard_sheet_divergence(self) -> None:
        marsh = replay(self.content, 1, "marsh_scout", _trace("divergence_marsh_wreck")["actions"])
        city = replay(self.content, 1, "city_oath", _trace("divergence_city_wreck")["actions"])
        self.assertEqual(marsh.state.location, "wreck.yard")
        marsh_ids = {a.id for a in enumerate_legal(marsh.state, self.content)}
        city_ids = {a.id for a in enumerate_legal(city.state, self.content)}
        self.assertIn("know_the_drowned_mark", marsh_ids)
        self.assertNotIn("know_the_drowned_mark", city_ids)
        self.assertIn("read_the_wreck_list", city_ids)
        self.assertNotIn("read_the_wreck_list", marsh_ids)

    def test_ice_held_changes_hull_verbs(self) -> None:
        plain = replay(self.content, 1, "marsh_scout", _trace("cross_plain_wreck")["actions"])
        iced = replay(self.content, 1, "marsh_scout", _trace("cross_ice_wreck")["actions"])
        self.assertEqual(plain.state.location, "wreck.hull")
        self.assertEqual(iced.state.location, "wreck.hull")
        plain_ids = {a.id for a in enumerate_legal(plain.state, self.content)}
        iced_ids = {a.id for a in enumerate_legal(iced.state, self.content)}
        self.assertNotIn("keep_the_drowned_cold", plain_ids)
        self.assertIn("keep_the_drowned_cold", iced_ids)
        self.assertIn("ice_held", iced.state.outcomes)

    def test_player_plain_language_lays_wreck(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        lines = [
            "go to market",
            "go to causeway",
            "go to wreck chapel",
            "go to wreck yard",
            "know the drowned mark",
            "go to the wreck hull",
            "take drowned token",
            "go to wreck yard",
            "go to the wreck wash",
            "wash the token",
            "go to wreck yard",
            "go to the wreck altar",
            "lay the token",
        ]
        for line in lines:
            turn = session.apply_line(line)
            self.assertTrue(turn.accepted, line)
        self.assertIn("wreck_laid", session.state.outcomes)
        self.assertIn("You can:", session.observation().text)
        self.assertLess(session.observation().prose_word_count, 120)

    def test_unmapped_text_still_noop_in_yard(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        for line in ("go to market", "go to causeway", "go to wreck chapel"):
            self.assertTrue(session.apply_line(line).accepted, line)
        before = session.fingerprint()
        turn = session.apply_line("summon a dry wind")
        self.assertFalse(turn.accepted)
        self.assertEqual(session.fingerprint(), before)

    def test_i4_rejects_tampered_build_on_wreck_trace(self) -> None:
        trace = copy.deepcopy(_trace("marsh_wreck_laid"))
        accept_trace(self.content, copy.deepcopy(trace))
        trace["build_id"] = "tampered-build"
        with self.assertRaises(TraceReject):
            accept_trace(self.content, trace)


if __name__ == "__main__":
    unittest.main()
