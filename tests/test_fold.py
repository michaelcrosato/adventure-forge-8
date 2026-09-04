"""Peat Fold hamlet: share outcome, sheet divergence, namehouse cross-effect."""

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


class PeatFoldTests(unittest.TestCase):
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
        ):
            trace = _trace(name)
            result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
            self.assertIn(outcome, result.state.outcomes, name)

    def test_fold_held_trace_replays(self) -> None:
        trace = _trace("marsh_fold_held")
        result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
        self.assertIn("fold_held", result.state.outcomes)
        self.assertTrue(self.content.outcome_ready("fold_held", result.state))
        self.assertEqual(result.fingerprint, trace["final_fingerprint"])
        accept_trace(self.content, trace)

    def test_green_sheet_divergence(self) -> None:
        marsh = replay(self.content, 1, "marsh_scout", _trace("divergence_marsh_fold")["actions"])
        city = replay(self.content, 1, "city_oath", _trace("divergence_city_fold")["actions"])
        self.assertEqual(marsh.state.location, "fold.green")
        marsh_ids = {a.id for a in enumerate_legal(marsh.state, self.content)}
        city_ids = {a.id for a in enumerate_legal(city.state, self.content)}
        self.assertIn("know_the_soft_cut", marsh_ids)
        self.assertNotIn("know_the_soft_cut", city_ids)
        self.assertIn("read_the_share_board", city_ids)
        self.assertNotIn("read_the_share_board", marsh_ids)

    def test_name_restored_changes_fold_verbs(self) -> None:
        plain = replay(self.content, 1, "marsh_scout", _trace("cross_plain_fold")["actions"])
        named = replay(self.content, 1, "marsh_scout", _trace("cross_name_fold")["actions"])
        self.assertEqual(plain.state.location, "fold.green")
        self.assertEqual(named.state.location, "fold.green")
        plain_ids = {a.id for a in enumerate_legal(plain.state, self.content)}
        named_ids = {a.id for a in enumerate_legal(named.state, self.content)}
        self.assertNotIn("cite_the_restored_name", plain_ids)
        self.assertIn("cite_the_restored_name", named_ids)
        self.assertIn("name_restored", named.state.outcomes)

    def test_player_plain_language_holds_the_fold(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        lines = [
            "go to market",
            "go to causeway",
            "go to peat fold",
            "go to the green",
            "know the soft cut",
            "go to the cut",
            "cut a safe brick",
            "go to the green",
            "go to the shed",
            "set the peat share",
        ]
        for line in lines:
            turn = session.apply_line(line)
            self.assertTrue(turn.accepted, line)
        self.assertIn("fold_held", session.state.outcomes)
        self.assertIn("You can:", session.observation().text)
        self.assertLess(session.observation().prose_word_count, 120)

    def test_unmapped_text_still_noop_on_green(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        for line in ("go to market", "go to causeway", "go to peat fold"):
            self.assertTrue(session.apply_line(line).accepted, line)
        before = session.fingerprint()
        turn = session.apply_line("summon a dry summer")
        self.assertFalse(turn.accepted)
        self.assertEqual(session.fingerprint(), before)

    def test_i4_rejects_tampered_build_on_fold_trace(self) -> None:
        trace = copy.deepcopy(_trace("marsh_fold_held"))
        accept_trace(self.content, copy.deepcopy(trace))
        trace["build_id"] = "tampered-build"
        with self.assertRaises(TraceReject):
            accept_trace(self.content, trace)


if __name__ == "__main__":
    unittest.main()
