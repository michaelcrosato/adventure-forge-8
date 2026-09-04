"""Smokehouse: hang-and-tend outcome, sheet divergence, salt-pans cross-effect."""

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


class SmokehouseTests(unittest.TestCase):
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
        ):
            trace = _trace(name)
            result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
            self.assertIn(outcome, result.state.outcomes, name)

    def test_smoke_cured_trace_replays(self) -> None:
        trace = _trace("marsh_smoke_cured")
        result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
        self.assertIn("smoke_cured", result.state.outcomes)
        self.assertTrue(self.content.outcome_ready("smoke_cured", result.state))
        self.assertEqual(result.fingerprint, trace["final_fingerprint"])
        accept_trace(self.content, trace)

    def test_yard_sheet_divergence(self) -> None:
        marsh = replay(self.content, 1, "marsh_scout", _trace("divergence_marsh_smoke")["actions"])
        city = replay(self.content, 1, "city_oath", _trace("divergence_city_smoke")["actions"])
        self.assertEqual(marsh.state.location, "smoke.yard")
        marsh_ids = {a.id for a in enumerate_legal(marsh.state, self.content)}
        city_ids = {a.id for a in enumerate_legal(city.state, self.content)}
        self.assertIn("know_the_wet_fish", marsh_ids)
        self.assertNotIn("know_the_wet_fish", city_ids)
        self.assertIn("read_the_cure_mark", city_ids)
        self.assertNotIn("read_the_cure_mark", marsh_ids)

    def test_salt_raked_changes_rack_verbs(self) -> None:
        plain = replay(self.content, 1, "marsh_scout", _trace("cross_plain_smoke")["actions"])
        salted = replay(self.content, 1, "marsh_scout", _trace("cross_salt_smoke")["actions"])
        self.assertEqual(plain.state.location, "smoke.racks")
        self.assertEqual(salted.state.location, "smoke.racks")
        plain_ids = {a.id for a in enumerate_legal(plain.state, self.content)}
        salted_ids = {a.id for a in enumerate_legal(salted.state, self.content)}
        self.assertNotIn("salt_the_racks", plain_ids)
        self.assertIn("salt_the_racks", salted_ids)
        self.assertIn("salt_raked", salted.state.outcomes)

    def test_player_plain_language_cures_smoke(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        lines = [
            "go to market",
            "go to causeway",
            "go to smokehouse",
            "go to smoke yard",
            "know the wet fish",
            "go to the fish racks",
            "take wet fish",
            "hang the wet fish",
            "go to smoke yard",
            "go to the smoke hearth",
            "tend the smoke",
            "go to smoke yard",
            "go to the cure loft",
            "take down the cure",
        ]
        for line in lines:
            turn = session.apply_line(line)
            self.assertTrue(turn.accepted, line)
        self.assertIn("smoke_cured", session.state.outcomes)
        self.assertIn("You can:", session.observation().text)
        self.assertLess(session.observation().prose_word_count, 120)

    def test_unmapped_text_still_noop_in_yard(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        for line in ("go to market", "go to causeway", "go to smokehouse"):
            self.assertTrue(session.apply_line(line).accepted, line)
        before = session.fingerprint()
        turn = session.apply_line("summon a dry wind")
        self.assertFalse(turn.accepted)
        self.assertEqual(session.fingerprint(), before)

    def test_i4_rejects_tampered_build_on_smoke_trace(self) -> None:
        trace = copy.deepcopy(_trace("marsh_smoke_cured"))
        accept_trace(self.content, copy.deepcopy(trace))
        trace["build_id"] = "tampered-build"
        with self.assertRaises(TraceReject):
            accept_trace(self.content, trace)


if __name__ == "__main__":
    unittest.main()
