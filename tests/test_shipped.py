"""Load-bearing tests against the shipped kernel and player mapping."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from adventure_forge.kernel.content import load_pack
from adventure_forge.kernel.fingerprint import fingerprint
from adventure_forge.kernel.legal import enumerate_legal
from adventure_forge.kernel.replay import new_game, replay
from adventure_forge.kernel.step import step
from adventure_forge.play.mapper import map_text
from adventure_forge.play.observe import observe
from adventure_forge.play.session import PlaySession


class ShippedKernelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.content = load_pack()

    def test_identical_fingerprint_on_two_replays(self) -> None:
        trace = json.loads((ROOT / "traces" / "marsh_harbor_compact.json").read_text(encoding="utf-8"))
        a = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
        b = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
        self.assertEqual(a.fingerprint, b.fingerprint)
        self.assertEqual(a.fingerprint, fingerprint(a.state, a.cursor))
        self.assertEqual(a.fingerprint, trace["final_fingerprint"])
        self.assertIn("harbor_compact", a.state.outcomes)

    def test_two_outcome_traces(self) -> None:
        compact = json.loads((ROOT / "traces" / "marsh_harbor_compact.json").read_text(encoding="utf-8"))
        relic = json.loads((ROOT / "traces" / "marsh_stack_relic.json").read_text(encoding="utf-8"))
        r1 = replay(self.content, compact["seed"], compact["sheet"], compact["actions"])
        r2 = replay(self.content, relic["seed"], relic["sheet"], relic["actions"])
        self.assertIn("harbor_compact", r1.state.outcomes)
        self.assertIn("stack_relic", r2.state.outcomes)
        self.assertTrue(self.content.outcome_ready("harbor_compact", r1.state))
        self.assertTrue(self.content.outcome_ready("stack_relic", r2.state))
        self.assertNotEqual(r1.fingerprint, r2.fingerprint)

    def test_two_sheet_divergence_same_scene(self) -> None:
        marsh_state, marsh_cur = new_game(self.content, 1, "marsh_scout")
        city_state, city_cur = new_game(self.content, 1, "city_oath")
        for action_id in ("go:saltfen.market",):
            marsh = step(marsh_state, action_id, self.content, marsh_cur)
            city = step(city_state, action_id, self.content, city_cur)
            self.assertTrue(marsh.accepted)
            self.assertTrue(city.accepted)
            marsh_state, marsh_cur = marsh.state, marsh.cursor
            city_state, city_cur = city.state, city.cursor
        self.assertEqual(marsh_state.location, "saltfen.market")
        self.assertEqual(city_state.location, "saltfen.market")
        marsh_ids = {a.id for a in enumerate_legal(marsh_state, self.content)}
        city_ids = {a.id for a in enumerate_legal(city_state, self.content)}
        self.assertIn("use_marsh_cant", marsh_ids)
        self.assertNotIn("use_marsh_cant", city_ids)
        self.assertIn("show_city_papers", city_ids)
        self.assertNotIn("show_city_papers", marsh_ids)
        replay(self.content, 1, "marsh_scout", ["go:saltfen.market"])
        replay(self.content, 1, "city_oath", ["go:saltfen.market"])

    def test_unmapped_and_illegal_do_not_change_state(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        before = session.fingerprint()
        result = session.apply_line("summon a dragon from the sky")
        self.assertFalse(result.accepted)
        self.assertIsNone(result.mapped)
        self.assertEqual(session.fingerprint(), before)
        stepped = step(session.state, "not_a_real_action", self.content, session.cursor)
        self.assertFalse(stepped.accepted)
        self.assertEqual(fingerprint(stepped.state, stepped.cursor), before)

    def test_plain_language_maps_to_legal_id(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        legal = enumerate_legal(session.state, self.content)
        mapped = map_text("go to market", legal)
        self.assertEqual(mapped, "go:saltfen.market")
        result = session.apply_line("go to market")
        self.assertTrue(result.accepted)
        self.assertEqual(session.state.location, "saltfen.market")

    def test_large_legal_set_has_no_cap(self) -> None:
        state, cursor = new_game(self.content, 1, "marsh_scout")
        for action_id in ("go:saltfen.market", "go:saltfen.salvage"):
            result = step(state, action_id, self.content, cursor)
            self.assertTrue(result.accepted, action_id)
            state, cursor = result.state, result.cursor
        legal = enumerate_legal(state, self.content)
        ids = [a.id for a in legal]
        salvage = [i for i in ids if i.startswith("take:salvage_")]
        self.assertGreaterEqual(len(salvage), 100)
        self.assertEqual(len(ids), len(set(ids)))
        src = (ROOT / "src" / "adventure_forge" / "kernel" / "legal.py").read_text(encoding="utf-8")
        self.assertNotIn("MAX_ACTIONS", src)
        obs = observe(state, self.content, page=0)
        self.assertLessEqual(len(obs.visible), 12)
        self.assertGreaterEqual(obs.total, 100)
        self.assertIn("more", obs.text)

    def test_save_resume_matches_uninterrupted(self) -> None:
        actions = [
            "go:saltfen.market",
            "use_marsh_cant",
            "ask_about_tablet",
            "slip_inside",
        ]
        live = PlaySession.start(self.content, 1, "marsh_scout")
        paused = PlaySession.start(self.content, 1, "marsh_scout")
        for action_id in actions[:2]:
            self.assertTrue(live.apply_line(action_id).accepted)
            self.assertTrue(paused.apply_line(action_id).accepted)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "save.json"
            paused.save(path)
            loaded = PlaySession.load(self.content, path)
        for action_id in actions[2:]:
            self.assertTrue(live.apply_line(action_id).accepted)
            self.assertTrue(loaded.apply_line(action_id).accepted)
        self.assertEqual(live.fingerprint(), loaded.fingerprint())
        self.assertEqual(live.state.location, loaded.state.location)

    def test_observation_is_action_first(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        text = session.observation().text
        self.assertIn("You can:", text)
        self.assertLess(text.index("Wet planks"), text.index("You can:"))
        self.assertLess(session.observation().prose_word_count, 120)


if __name__ == "__main__":
    unittest.main()
