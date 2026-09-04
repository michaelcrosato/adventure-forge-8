"""Toll Ferry: fare-load-pole outcome, sheet divergence, dye-works cross-effect."""

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


class TollFerryTests(unittest.TestCase):
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
        ):
            trace = _trace(name)
            result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
            self.assertIn(outcome, result.state.outcomes, name)

    def test_ferry_crossed_trace_replays(self) -> None:
        trace = _trace("marsh_ferry_crossed")
        result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
        self.assertIn("ferry_crossed", result.state.outcomes)
        self.assertEqual(result.state.location, "ferry.far")
        self.assertTrue(self.content.outcome_ready("ferry_crossed", result.state))
        self.assertEqual(result.fingerprint, trace["final_fingerprint"])
        accept_trace(self.content, trace)

    def test_yard_sheet_divergence(self) -> None:
        marsh = replay(self.content, 1, "marsh_scout", _trace("divergence_marsh_ferry")["actions"])
        city = replay(self.content, 1, "city_oath", _trace("divergence_city_ferry")["actions"])
        self.assertEqual(marsh.state.location, "ferry.yard")
        marsh_ids = {a.id for a in enumerate_legal(marsh.state, self.content)}
        city_ids = {a.id for a in enumerate_legal(city.state, self.content)}
        self.assertIn("know_the_channel_cut", marsh_ids)
        self.assertNotIn("know_the_channel_cut", city_ids)
        self.assertIn("read_the_toll_board", city_ids)
        self.assertNotIn("read_the_toll_board", marsh_ids)

    def test_dye_struck_changes_yard_verbs(self) -> None:
        plain = replay(self.content, 1, "marsh_scout", _trace("cross_plain_ferry")["actions"])
        dyed = replay(self.content, 1, "marsh_scout", _trace("cross_dye_ferry")["actions"])
        self.assertEqual(plain.state.location, "ferry.yard")
        self.assertEqual(dyed.state.location, "ferry.yard")
        plain_ids = {a.id for a in enumerate_legal(plain.state, self.content)}
        dyed_ids = {a.id for a in enumerate_legal(dyed.state, self.content)}
        self.assertNotIn("show_the_dyed_fare", plain_ids)
        self.assertIn("show_the_dyed_fare", dyed_ids)
        self.assertIn("dye_struck", dyed.state.outcomes)

    def test_boat_board_is_gated_on_load(self) -> None:
        before = replay(
            self.content,
            1,
            "marsh_scout",
            [
                "go:saltfen.market",
                "go:ashfen.causeway",
                "go:ferry.path",
                "go:ferry.yard",
                "know_the_channel_cut",
                "take:toll_token",
                "go:ferry.slip",
            ],
        )
        before_ids = {a.id for a in enumerate_legal(before.state, self.content)}
        self.assertNotIn("go:ferry.boat", before_ids)
        loaded = replay(
            self.content,
            1,
            "marsh_scout",
            [
                "go:saltfen.market",
                "go:ashfen.causeway",
                "go:ferry.path",
                "go:ferry.yard",
                "know_the_channel_cut",
                "take:toll_token",
                "go:ferry.slip",
                "load_the_boat",
            ],
        )
        loaded_ids = {a.id for a in enumerate_legal(loaded.state, self.content)}
        self.assertIn("go:ferry.boat", loaded_ids)

    def test_pole_relocates_to_far_bank(self) -> None:
        result = replay(self.content, 1, "marsh_scout", _trace("marsh_ferry_crossed")["actions"][:-1])
        self.assertEqual(result.state.location, "ferry.far")
        self.assertIn("boat_poled", result.state.flags)
        self.assertNotIn("ferry_crossed", result.state.outcomes)

    def test_player_plain_language_crosses_ferry(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        lines = [
            "go to market",
            "go to causeway",
            "go to toll ferry",
            "go to ferry yard",
            "know the channel cut",
            "take toll token",
            "go to the slip",
            "load the boat",
            "board the boat",
            "pole the crossing",
            "claim the landing",
        ]
        for line in lines:
            turn = session.apply_line(line)
            self.assertTrue(turn.accepted, line)
        self.assertIn("ferry_crossed", session.state.outcomes)
        self.assertEqual(session.state.location, "ferry.far")
        self.assertIn("You can:", session.observation().text)
        self.assertLess(session.observation().prose_word_count, 120)

    def test_unmapped_text_still_noop_in_yard(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        for line in ("go to market", "go to causeway", "go to toll ferry"):
            self.assertTrue(session.apply_line(line).accepted, line)
        before = session.fingerprint()
        turn = session.apply_line("summon a dry wind")
        self.assertFalse(turn.accepted)
        self.assertEqual(session.fingerprint(), before)

    def test_i4_rejects_tampered_build_on_ferry_trace(self) -> None:
        trace = copy.deepcopy(_trace("marsh_ferry_crossed"))
        accept_trace(self.content, copy.deepcopy(trace))
        trace["build_id"] = "tampered-build"
        with self.assertRaises(TraceReject):
            accept_trace(self.content, trace)


if __name__ == "__main__":
    unittest.main()
