"""Eel Weir: set-and-lift outcome, sheet divergence, smokehouse cross-effect."""

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


class EelWeirTests(unittest.TestCase):
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
        ):
            trace = _trace(name)
            result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
            self.assertIn(outcome, result.state.outcomes, name)

    def test_weir_lifted_trace_replays(self) -> None:
        trace = _trace("marsh_weir_lifted")
        result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
        self.assertIn("weir_lifted", result.state.outcomes)
        self.assertTrue(self.content.outcome_ready("weir_lifted", result.state))
        self.assertEqual(result.fingerprint, trace["final_fingerprint"])
        accept_trace(self.content, trace)

    def test_yard_sheet_divergence(self) -> None:
        marsh = replay(self.content, 1, "marsh_scout", _trace("divergence_marsh_weir")["actions"])
        city = replay(self.content, 1, "city_oath", _trace("divergence_city_weir")["actions"])
        self.assertEqual(marsh.state.location, "weir.yard")
        marsh_ids = {a.id for a in enumerate_legal(marsh.state, self.content)}
        city_ids = {a.id for a in enumerate_legal(city.state, self.content)}
        self.assertIn("know_the_eel_run", marsh_ids)
        self.assertNotIn("know_the_eel_run", city_ids)
        self.assertIn("read_the_weir_right", city_ids)
        self.assertNotIn("read_the_weir_right", marsh_ids)

    def test_smoke_cured_changes_stake_verbs(self) -> None:
        plain = replay(self.content, 1, "marsh_scout", _trace("cross_plain_weir")["actions"])
        smoked = replay(self.content, 1, "marsh_scout", _trace("cross_smoke_weir")["actions"])
        self.assertEqual(plain.state.location, "weir.stakes")
        self.assertEqual(smoked.state.location, "weir.stakes")
        plain_ids = {a.id for a in enumerate_legal(plain.state, self.content)}
        smoked_ids = {a.id for a in enumerate_legal(smoked.state, self.content)}
        self.assertNotIn("bait_the_weir", plain_ids)
        self.assertIn("bait_the_weir", smoked_ids)
        self.assertIn("smoke_cured", smoked.state.outcomes)

    def test_player_plain_language_lifts_weir(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        lines = [
            "go to market",
            "go to causeway",
            "go to eel weir",
            "go to weir yard",
            "know the eel run",
            "go to the weir hut",
            "take weir basket",
            "go to weir yard",
            "go to the stakes",
            "set the baskets",
            "lift the weir",
        ]
        for line in lines:
            turn = session.apply_line(line)
            self.assertTrue(turn.accepted, line)
        self.assertIn("weir_lifted", session.state.outcomes)
        self.assertIn("You can:", session.observation().text)
        self.assertLess(session.observation().prose_word_count, 120)

    def test_unmapped_text_still_noop_in_yard(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        for line in ("go to market", "go to causeway", "go to eel weir"):
            self.assertTrue(session.apply_line(line).accepted, line)
        before = session.fingerprint()
        turn = session.apply_line("summon a dry wind")
        self.assertFalse(turn.accepted)
        self.assertEqual(session.fingerprint(), before)

    def test_i4_rejects_tampered_build_on_weir_trace(self) -> None:
        trace = copy.deepcopy(_trace("marsh_weir_lifted"))
        accept_trace(self.content, copy.deepcopy(trace))
        trace["build_id"] = "tampered-build"
        with self.assertRaises(TraceReject):
            accept_trace(self.content, trace)


if __name__ == "__main__":
    unittest.main()
