"""Lens Ruin: light-path outcome, sheet divergence, peat-fold cross-effect."""

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


class LensRuinTests(unittest.TestCase):
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
        ):
            trace = _trace(name)
            result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
            self.assertIn(outcome, result.state.outcomes, name)

    def test_lens_set_trace_replays(self) -> None:
        trace = _trace("marsh_lens_set")
        result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
        self.assertIn("lens_set", result.state.outcomes)
        self.assertTrue(self.content.outcome_ready("lens_set", result.state))
        self.assertEqual(result.fingerprint, trace["final_fingerprint"])
        accept_trace(self.content, trace)

    def test_nave_sheet_divergence(self) -> None:
        marsh = replay(self.content, 1, "marsh_scout", _trace("divergence_marsh_glass")["actions"])
        city = replay(self.content, 1, "city_oath", _trace("divergence_city_glass")["actions"])
        self.assertEqual(marsh.state.location, "glass.nave")
        marsh_ids = {a.id for a in enumerate_legal(marsh.state, self.content)}
        city_ids = {a.id for a in enumerate_legal(city.state, self.content)}
        self.assertIn("know_the_low_sun", marsh_ids)
        self.assertNotIn("know_the_low_sun", city_ids)
        self.assertIn("read_the_sun_chart", city_ids)
        self.assertNotIn("read_the_sun_chart", marsh_ids)

    def test_fold_held_changes_glass_verbs(self) -> None:
        plain = replay(self.content, 1, "marsh_scout", _trace("cross_plain_glass")["actions"])
        held = replay(self.content, 1, "marsh_scout", _trace("cross_fold_glass")["actions"])
        self.assertEqual(plain.state.location, "glass.yard")
        self.assertEqual(held.state.location, "glass.yard")
        plain_ids = {a.id for a in enumerate_legal(plain.state, self.content)}
        held_ids = {a.id for a in enumerate_legal(held.state, self.content)}
        self.assertNotIn("trade_peat_for_lead", plain_ids)
        self.assertIn("trade_peat_for_lead", held_ids)
        self.assertIn("fold_held", held.state.outcomes)

    def test_player_plain_language_sets_lens(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        lines = [
            "go to market",
            "go to causeway",
            "go to lens ruin",
            "go to glass yard",
            "go to the nave",
            "know the low sun",
            "go to glass yard",
            "go to the pit",
            "take lens shard",
            "go to glass yard",
            "go to the nave",
            "go to the loft",
            "set the lens shard",
        ]
        for line in lines:
            turn = session.apply_line(line)
            self.assertTrue(turn.accepted, line)
        self.assertIn("lens_set", session.state.outcomes)
        self.assertIn("You can:", session.observation().text)
        self.assertLess(session.observation().prose_word_count, 120)

    def test_unmapped_text_still_noop_in_nave(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        for line in ("go to market", "go to causeway", "go to lens ruin"):
            self.assertTrue(session.apply_line(line).accepted, line)
        before = session.fingerprint()
        turn = session.apply_line("summon a second sun")
        self.assertFalse(turn.accepted)
        self.assertEqual(session.fingerprint(), before)

    def test_i4_rejects_tampered_build_on_lens_trace(self) -> None:
        trace = copy.deepcopy(_trace("marsh_lens_set"))
        accept_trace(self.content, copy.deepcopy(trace))
        trace["build_id"] = "tampered-build"
        with self.assertRaises(TraceReject):
            accept_trace(self.content, trace)


if __name__ == "__main__":
    unittest.main()
