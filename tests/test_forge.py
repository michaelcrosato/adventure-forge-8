"""Tide Forge: bellows-bloom-quench outcome, sheet divergence, pickle-house cross-effect."""

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


class TideForgeTests(unittest.TestCase):
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
            ("marsh_wreck_laid", "wreck_laid"),
            ("marsh_hive_kept", "hive_kept"),
            ("marsh_mead_drawn", "mead_drawn"),
            ("marsh_barrel_raised", "barrel_raised"),
            ("marsh_pickle_lidded", "pickle_lidded"),
        ):
            trace = _trace(name)
            result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
            self.assertIn(outcome, result.state.outcomes, name)

    def test_iron_quenched_trace_replays(self) -> None:
        trace = _trace("marsh_iron_quenched")
        result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
        self.assertIn("iron_quenched", result.state.outcomes)
        self.assertEqual(result.state.location, "forge.trough")
        self.assertTrue(self.content.outcome_ready("iron_quenched", result.state))
        self.assertEqual(result.fingerprint, trace["final_fingerprint"])
        accept_trace(self.content, trace)

    def test_yard_sheet_divergence(self) -> None:
        marsh = replay(self.content, 1, "marsh_scout", _trace("divergence_marsh_forge")["actions"])
        city = replay(self.content, 1, "city_oath", _trace("divergence_city_forge")["actions"])
        self.assertEqual(marsh.state.location, "forge.yard")
        marsh_ids = {a.id for a in enumerate_legal(marsh.state, self.content)}
        city_ids = {a.id for a in enumerate_legal(city.state, self.content)}
        self.assertIn("know_the_bog_iron", marsh_ids)
        self.assertNotIn("know_the_bog_iron", city_ids)
        self.assertIn("read_the_forge_list", city_ids)
        self.assertNotIn("read_the_forge_list", marsh_ids)

    def test_pickle_lidded_changes_trough_verbs(self) -> None:
        plain = replay(self.content, 1, "marsh_scout", _trace("cross_plain_forge")["actions"])
        brined = replay(self.content, 1, "marsh_scout", _trace("cross_pickle_forge")["actions"])
        self.assertEqual(plain.state.location, "forge.trough")
        self.assertEqual(brined.state.location, "forge.trough")
        plain_ids = {a.id for a in enumerate_legal(plain.state, self.content)}
        brined_ids = {a.id for a in enumerate_legal(brined.state, self.content)}
        self.assertNotIn("brine_the_quench", plain_ids)
        self.assertIn("brine_the_quench", brined_ids)
        self.assertIn("pickle_lidded", brined.state.outcomes)

    def test_player_plain_language_quenches_iron(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        lines = [
            "go to market",
            "go to causeway",
            "go to tide forge",
            "go to forge yard",
            "know the bog iron",
            "go to the bellows",
            "bank the bellows",
            "go to forge yard",
            "go to the anvil",
            "hammer the bloom",
            "take bloom iron",
            "go to forge yard",
            "go to the trough",
            "quench the iron",
        ]
        for line in lines:
            turn = session.apply_line(line)
            self.assertTrue(turn.accepted, line)
        self.assertIn("iron_quenched", session.state.outcomes)
        self.assertIn("You can:", session.observation().text)
        self.assertLess(session.observation().prose_word_count, 120)

    def test_unmapped_text_still_noop_in_yard(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        for line in ("go to market", "go to causeway", "go to tide forge"):
            self.assertTrue(session.apply_line(line).accepted, line)
        before = session.fingerprint()
        turn = session.apply_line("summon a dry wind")
        self.assertFalse(turn.accepted)
        self.assertEqual(session.fingerprint(), before)

    def test_i4_rejects_tampered_build_on_forge_trace(self) -> None:
        trace = copy.deepcopy(_trace("marsh_iron_quenched"))
        accept_trace(self.content, copy.deepcopy(trace))
        trace["build_id"] = "tampered-build"
        with self.assertRaises(TraceReject):
            accept_trace(self.content, trace)


if __name__ == "__main__":
    unittest.main()
