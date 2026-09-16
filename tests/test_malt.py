"""Malt House: steep-turn-oast outcome, sheet divergence, wheelwright cross-effect."""

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


class MaltHouseTests(unittest.TestCase):
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
            ("marsh_soap_cut", "soap_cut"),
            ("marsh_cloth_fulled", "cloth_fulled"),
            ("marsh_coal_drawn", "coal_drawn"),
            ("marsh_lime_slaked", "lime_slaked"),
            ("marsh_joint_pointed", "joint_pointed"),
            ("marsh_roof_set", "roof_set"),
            ("marsh_cistern_filled", "cistern_filled"),
            ("marsh_wash_hung", "wash_hung"),
            ("marsh_paper_laid", "paper_laid"),
            ("marsh_frail_woven", "frail_woven"),
            ("marsh_loaf_drawn", "loaf_drawn"),
            ("marsh_wheel_salted", "wheel_salted"),
            ("marsh_web_sheared", "web_sheared"),
            ("marsh_lantern_hung", "lantern_hung"),
            ("marsh_nib_cut", "nib_cut"),
            ("marsh_heel_pegged", "heel_pegged"),
            ("marsh_keeve_bunged", "keeve_bunged"),
            ("marsh_mustard_potted", "mustard_potted"),
            ("marsh_sausage_linked", "sausage_linked"),
            ("marsh_pie_crimped", "pie_crimped"),
            ("marsh_jam_jarred", "jam_jarred"),
            ("marsh_crock_glazed", "crock_glazed"),
            ("marsh_hide_tanned", "hide_tanned"),
            ("marsh_flax_spun", "flax_spun"),
            ("marsh_nail_pointed", "nail_pointed"),
            ("marsh_tyre_set", "tyre_set"),
        ):
            trace = _trace(name)
            result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
            self.assertIn(outcome, result.state.outcomes, name)

    def test_malt_oasted_trace_replays(self) -> None:
        trace = _trace("marsh_malt_oasted")
        result = replay(self.content, trace["seed"], trace["sheet"], trace["actions"])
        self.assertIn("malt_oasted", result.state.outcomes)
        self.assertEqual(result.state.location, "malt.oast")
        self.assertTrue(self.content.outcome_ready("malt_oasted", result.state))
        self.assertEqual(result.fingerprint, trace["final_fingerprint"])
        accept_trace(self.content, trace)

    def test_yard_sheet_divergence(self) -> None:
        marsh = replay(self.content, 1, "marsh_scout", _trace("divergence_marsh_malt")["actions"])
        city = replay(self.content, 1, "city_oath", _trace("divergence_city_malt")["actions"])
        self.assertEqual(marsh.state.location, "malt.yard")
        marsh_ids = {a.id for a in enumerate_legal(marsh.state, self.content)}
        city_ids = {a.id for a in enumerate_legal(city.state, self.content)}
        self.assertIn("know_the_steep", marsh_ids)
        self.assertNotIn("know_the_steep", city_ids)
        self.assertIn("read_the_malt_list", city_ids)
        self.assertNotIn("read_the_malt_list", marsh_ids)

    def test_tyre_set_changes_steep_verbs(self) -> None:
        plain = replay(self.content, 1, "marsh_scout", _trace("cross_plain_malt")["actions"])
        hauled = replay(self.content, 1, "marsh_scout", _trace("cross_wain_malt")["actions"])
        self.assertEqual(plain.state.location, "malt.steep")
        self.assertEqual(hauled.state.location, "malt.steep")
        plain_ids = {a.id for a in enumerate_legal(plain.state, self.content)}
        hauled_ids = {a.id for a in enumerate_legal(hauled.state, self.content)}
        self.assertNotIn("wain_the_steep", plain_ids)
        self.assertIn("wain_the_steep", hauled_ids)
        self.assertIn("tyre_set", hauled.state.outcomes)

    def test_player_plain_language_oasts_malt(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        lines = [
            "go to market",
            "go to causeway",
            "go to the malt",
            "go to malt yard",
            "know the steep",
            "go to the steep",
            "steep the barley",
            "go to malt yard",
            "go to the piece",
            "turn the piece",
            "take green malt",
            "go to malt yard",
            "go to the oast",
            "oast the malt",
        ]
        for line in lines:
            turn = session.apply_line(line)
            self.assertTrue(turn.accepted, line)
        self.assertIn("malt_oasted", session.state.outcomes)
        self.assertIn("You can:", session.observation().text)
        self.assertLess(session.observation().prose_word_count, 120)

    def test_unmapped_text_still_noop_in_yard(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        for line in ("go to market", "go to causeway", "go to the malt"):
            self.assertTrue(session.apply_line(line).accepted, line)
        before = session.fingerprint()
        turn = session.apply_line("summon a dry wind")
        self.assertFalse(turn.accepted)
        self.assertEqual(session.fingerprint(), before)

    def test_i4_rejects_tampered_build_on_malt_trace(self) -> None:
        trace = copy.deepcopy(_trace("marsh_malt_oasted"))
        accept_trace(self.content, copy.deepcopy(trace))
        trace["build_id"] = "tampered-build"
        with self.assertRaises(TraceReject):
            accept_trace(self.content, trace)
