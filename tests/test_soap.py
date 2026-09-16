"""Soap House: leach-boil-cut outcome, sheet divergence, kelp-shore cross-effect."""

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


class SoapHouseTests(unittest.TestCase):
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
            ("marsh_iron_quenched", "iron_quenched"),
            ("marsh_fowl_taken", "fowl_taken"),
            ("marsh_lights_bound", "lights_bound"),
            ("marsh_seam_caulked", "seam_caulked"),
            ("marsh_net_tarred", "net_tarred"),
            ("marsh_sail_hoisted", "sail_hoisted"),
            ("marsh_lead_cast", "lead_cast"),
            ("marsh_rutter_sealed", "rutter_sealed"),
            ("marsh_buoy_set", "buoy_set"),
            ("marsh_kelp_burned", "kelp_burned"),
        ):
            trace = _trace(name)
            result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
            self.assertIn(outcome, result.state.outcomes, name)

    def test_soap_cut_trace_replays(self) -> None:
        trace = _trace("marsh_soap_cut")
        result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
        self.assertIn("soap_cut", result.state.outcomes)
        self.assertEqual(result.state.location, "soap.cut")
        self.assertTrue(self.content.outcome_ready("soap_cut", result.state))
        self.assertEqual(result.fingerprint, trace["final_fingerprint"])
        accept_trace(self.content, trace)

    def test_yard_sheet_divergence(self) -> None:
        marsh = replay(self.content, 1, "marsh_scout", _trace("divergence_marsh_soap")["actions"])
        city = replay(self.content, 1, "city_oath", _trace("divergence_city_soap")["actions"])
        self.assertEqual(marsh.state.location, "soap.yard")
        marsh_ids = {a.id for a in enumerate_legal(marsh.state, self.content)}
        city_ids = {a.id for a in enumerate_legal(city.state, self.content)}
        self.assertIn("know_the_lye_run", marsh_ids)
        self.assertNotIn("know_the_lye_run", city_ids)
        self.assertIn("read_the_soap_list", city_ids)
        self.assertNotIn("read_the_soap_list", marsh_ids)

    def test_kelp_burned_changes_leach_verbs(self) -> None:
        plain = replay(self.content, 1, "marsh_scout", _trace("cross_plain_soap")["actions"])
        charged = replay(self.content, 1, "marsh_scout", _trace("cross_kelp_soap")["actions"])
        self.assertEqual(plain.state.location, "soap.leach")
        self.assertEqual(charged.state.location, "soap.leach")
        plain_ids = {a.id for a in enumerate_legal(plain.state, self.content)}
        charged_ids = {a.id for a in enumerate_legal(charged.state, self.content)}
        self.assertNotIn("charge_the_soda", plain_ids)
        self.assertIn("charge_the_soda", charged_ids)
        self.assertIn("kelp_burned", charged.state.outcomes)

    def test_player_plain_language_cuts_soap(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        lines = [
            "go to market",
            "go to causeway",
            "go to the soap",
            "go to soap yard",
            "know the lye run",
            "go to the leach",
            "leach the ash",
            "go to soap yard",
            "go to the boil",
            "boil the soap",
            "take soda lye",
            "go to soap yard",
            "go to the cakes",
            "cut the cakes",
        ]
        for line in lines:
            turn = session.apply_line(line)
            self.assertTrue(turn.accepted, line)
        self.assertIn("soap_cut", session.state.outcomes)
        self.assertIn("You can:", session.observation().text)
        self.assertLess(session.observation().prose_word_count, 120)

    def test_unmapped_text_still_noop_in_yard(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        for line in ("go to market", "go to causeway", "go to the soap"):
            self.assertTrue(session.apply_line(line).accepted, line)
        before = session.fingerprint()
        turn = session.apply_line("summon a dry wind")
        self.assertFalse(turn.accepted)
        self.assertEqual(session.fingerprint(), before)

    def test_i4_rejects_tampered_build_on_soap_trace(self) -> None:
        trace = copy.deepcopy(_trace("marsh_soap_cut"))
        accept_trace(self.content, copy.deepcopy(trace))
        trace["build_id"] = "tampered-build"
        with self.assertRaises(TraceReject):
            accept_trace(self.content, trace)


if __name__ == "__main__":
    unittest.main()
