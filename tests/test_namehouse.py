"""Namehouse slice: restored-name outcome, sheet divergence, fever cross-effect."""

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


class NamehouseTests(unittest.TestCase):
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
        ):
            trace = _trace(name)
            result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
            self.assertIn(outcome, result.state.outcomes, name)

    def test_name_restored_trace_replays(self) -> None:
        trace = _trace("marsh_name_restored")
        result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
        self.assertIn("name_restored", result.state.outcomes)
        self.assertTrue(self.content.outcome_ready("name_restored", result.state))
        self.assertEqual(result.fingerprint, trace["final_fingerprint"])
        accept_trace(self.content, trace)

    def test_hall_sheet_divergence(self) -> None:
        marsh = replay(self.content, 1, "marsh_scout", _trace("divergence_marsh_name")["actions"])
        city = replay(self.content, 1, "city_oath", _trace("divergence_city_name")["actions"])
        self.assertEqual(marsh.state.location, "name.hall")
        self.assertEqual(city.state.location, "name.hall")
        marsh_ids = {a.id for a in enumerate_legal(marsh.state, self.content)}
        city_ids = {a.id for a in enumerate_legal(city.state, self.content)}
        self.assertIn("speak_the_old_name", marsh_ids)
        self.assertNotIn("speak_the_old_name", city_ids)
        self.assertIn("copy_the_bone_name", city_ids)
        self.assertNotIn("copy_the_bone_name", marsh_ids)

    def test_fever_deed_changes_namehouse_verbs(self) -> None:
        plain = replay(self.content, 1, "marsh_scout", _trace("cross_plain_name")["actions"])
        fever = replay(self.content, 1, "marsh_scout", _trace("cross_fever_name")["actions"])
        self.assertEqual(plain.state.location, "name.hall")
        self.assertEqual(fever.state.location, "name.hall")
        plain_ids = {a.id for a in enumerate_legal(plain.state, self.content)}
        fever_ids = {a.id for a in enumerate_legal(fever.state, self.content)}
        self.assertNotIn("file_ren_living", plain_ids)
        self.assertIn("file_ren_living", fever_ids)
        self.assertIn("fever_broken", fever.state.outcomes)

    def test_player_plain_language_restores_name(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        lines = [
            "go to market",
            "go to causeway",
            "go to namehouse",
            "go to name yard",
            "go to name hall",
            "speak the old name",
            "go to name yard",
            "go to crypt",
            "take bone name",
            "go to name yard",
            "go to name hall",
            "restore the name",
        ]
        for line in lines:
            turn = session.apply_line(line)
            self.assertTrue(turn.accepted, line)
        self.assertIn("name_restored", session.state.outcomes)
        self.assertIn("You can:", session.observation().text)
        self.assertLess(session.observation().prose_word_count, 120)

    def test_unmapped_text_still_noop_in_hall(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        for line in ("go to market", "go to causeway", "go to namehouse"):
            self.assertTrue(session.apply_line(line).accepted, line)
        before = session.fingerprint()
        turn = session.apply_line("rewrite every dead name at once")
        self.assertFalse(turn.accepted)
        self.assertEqual(session.fingerprint(), before)

    def test_i4_rejects_tampered_build_on_name_trace(self) -> None:
        trace = copy.deepcopy(_trace("marsh_name_restored"))
        accept_trace(self.content, copy.deepcopy(trace))
        trace["build_id"] = "tampered-build"
        with self.assertRaises(TraceReject):
            accept_trace(self.content, trace)


if __name__ == "__main__":
    unittest.main()
