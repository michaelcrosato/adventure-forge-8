"""Reed Court slice: sentence outcome, sheet divergence, kiln-pact cross-effect."""

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


class ReedCourtTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.content = load_pack()

    def test_prior_outcomes_still_replay(self) -> None:
        for name, outcome in (
            ("marsh_harbor_compact", "harbor_compact"),
            ("marsh_stack_relic", "stack_relic"),
            ("marsh_kiln_pact", "kiln_pact"),
        ):
            trace = _trace(name)
            result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
            self.assertIn(outcome, result.state.outcomes, name)
            self.assertTrue(self.content.outcome_ready(outcome, result.state), name)

    def test_reed_sentence_trace_replays(self) -> None:
        trace = _trace("marsh_reed_sentence")
        result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
        self.assertIn("reed_sentence", result.state.outcomes)
        self.assertTrue(self.content.outcome_ready("reed_sentence", result.state))
        self.assertTrue(result.state.flags.get("reed_sentence_passed"))
        self.assertEqual(result.fingerprint, trace["final_fingerprint"])
        accept_trace(self.content, trace)

    def test_court_hall_sheet_divergence(self) -> None:
        marsh = replay(self.content, 1, "marsh_scout", _trace("divergence_marsh_court")["actions"])
        city = replay(self.content, 1, "city_oath", _trace("divergence_city_court")["actions"])
        self.assertEqual(marsh.state.location, "court.hall")
        self.assertEqual(city.state.location, "court.hall")
        marsh_ids = {a.id for a in enumerate_legal(marsh.state, self.content)}
        city_ids = {a.id for a in enumerate_legal(city.state, self.content)}
        self.assertIn("speak_reed_custom", marsh_ids)
        self.assertNotIn("speak_reed_custom", city_ids)
        self.assertIn("cite_city_law", city_ids)
        self.assertNotIn("cite_city_law", marsh_ids)

    def test_kiln_pact_changes_court_verbs(self) -> None:
        plain = replay(self.content, 1, "marsh_scout", _trace("cross_plain_court")["actions"])
        kiln = replay(self.content, 1, "marsh_scout", _trace("cross_kiln_court")["actions"])
        self.assertEqual(plain.state.location, kiln.state.location)
        self.assertEqual(plain.state.location, "court.hall")
        plain_ids = {a.id for a in enumerate_legal(plain.state, self.content)}
        kiln_ids = {a.id for a in enumerate_legal(kiln.state, self.content)}
        self.assertNotIn("name_mill_pact", plain_ids)
        self.assertIn("name_mill_pact", kiln_ids)
        self.assertIn("kiln_pact", kiln.state.outcomes)

    def test_player_plain_language_reaches_sentence(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        lines = [
            "go to market",
            "go to causeway",
            "go to reed court",
            "go to court yard",
            "go to hall",
            "speak reed custom",
            "go to court yard",
            "go to cell",
            "hear Tam as witness",
            "go to court yard",
            "go to hall",
            "pass the reed sentence",
        ]
        for line in lines:
            turn = session.apply_line(line)
            self.assertTrue(turn.accepted, line)
        self.assertIn("reed_sentence", session.state.outcomes)
        obs = session.observation()
        self.assertIn("You can:", obs.text)
        self.assertLess(obs.prose_word_count, 120)

    def test_unmapped_text_still_noop_in_hall(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        for line in ("go to market", "go to causeway", "go to reed court"):
            self.assertTrue(session.apply_line(line).accepted, line)
        before = session.fingerprint()
        turn = session.apply_line("overturn the sky with a writ")
        self.assertFalse(turn.accepted)
        self.assertEqual(session.fingerprint(), before)

    def test_i4_rejects_tampered_build_on_court_trace(self) -> None:
        trace = copy.deepcopy(_trace("marsh_reed_sentence"))
        accept_trace(self.content, copy.deepcopy(trace))
        trace["build_id"] = "tampered-build"
        with self.assertRaises(TraceReject) as ctx:
            accept_trace(self.content, trace)
        self.assertIn("build_id", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
