from __future__ import annotations

from adventure_forge.kernel.content import Content
from adventure_forge.kernel.legal import enumerate_legal
from adventure_forge.kernel.replay import ReplayError, new_game, replay
from adventure_forge.kernel.step import step


class TraceReject(AssertionError):
    """I4 acceptor rejection. Tampered or stale evidence is not a proof."""


def accept_trace(content: Content, trace: dict):
    """Fail unless this trace is bound to the current pack and replays to its fingerprint."""
    tid = trace.get("id", "?")
    if not trace.get("build_id"):
        raise TraceReject(f"{tid} missing build_id")
    if trace["build_id"] != content.build_id:
        raise TraceReject(f"{tid} build_id does not match current pack")
    if not trace.get("final_fingerprint"):
        raise TraceReject(f"{tid} missing final_fingerprint")
    try:
        result = replay(content, trace["seed"], trace["sheet"], trace["actions"])
    except ReplayError as exc:
        raise TraceReject(f"{tid} replay rejected: {exc}") from exc
    if result.fingerprint != trace["final_fingerprint"]:
        raise TraceReject(f"{tid} fingerprint mismatch")
    if result.state.build_id != content.build_id:
        raise TraceReject(f"{tid} replay state build_id drifted")
    outcome = trace.get("outcome")
    if outcome and outcome not in result.state.outcomes:
        raise TraceReject(f"{tid} missing outcome {outcome}: {result.state.outcomes}")
    # Traces record an `outcomes` list as well as the singular headline outcome.
    # Only the singular one used to be asserted, so 570 of 714 traces proved
    # nothing beyond "this replays to the hash we took of it replaying".
    recorded = trace.get("outcomes") or []
    if not isinstance(recorded, list):
        raise TraceReject(f"{tid} outcomes must be a list")
    reached = set(result.state.outcomes)
    missing = [o for o in recorded if o not in reached]
    if missing:
        raise TraceReject(f"{tid} missing recorded outcomes {missing}: {sorted(reached)}")
    return result


def check_i4(content: Content, traces: list[dict]) -> dict:
    by_id = {t["id"]: t for t in traces}
    required = (
        "marsh_harbor_compact",
        "marsh_stack_relic",
        "marsh_kiln_pact",
        "divergence_marsh_market",
        "divergence_city_market",
        "divergence_marsh_mill",
        "divergence_city_mill",
        "cross_plain_mill",
        "cross_compact_mill",
        "marsh_reed_sentence",
        "divergence_marsh_court",
        "divergence_city_court",
        "cross_plain_court",
        "cross_kiln_court",
        "marsh_road_beacon",
        "divergence_marsh_road",
        "divergence_city_road",
        "cross_plain_road",
        "cross_court_road",
        "marsh_fever_broken",
        "divergence_marsh_camp",
        "divergence_city_camp",
        "cross_plain_camp",
        "cross_beacon_camp",
        "marsh_name_restored",
        "divergence_marsh_name",
        "divergence_city_name",
        "cross_plain_name",
        "cross_fever_name",
        "marsh_fold_held",
        "divergence_marsh_fold",
        "divergence_city_fold",
        "cross_plain_fold",
        "cross_name_fold",
        "marsh_lens_set",
        "divergence_marsh_glass",
        "divergence_city_glass",
        "cross_plain_glass",
        "cross_fold_glass",
        "marsh_rope_walked",
        "divergence_marsh_rope",
        "divergence_city_rope",
        "cross_plain_rope",
        "cross_lens_rope",
        "marsh_salt_raked",
        "divergence_marsh_salt",
        "divergence_city_salt",
        "cross_plain_salt",
        "cross_rope_salt",
        "marsh_smoke_cured",
        "divergence_marsh_smoke",
        "divergence_city_smoke",
        "cross_plain_smoke",
        "cross_salt_smoke",
        "marsh_weir_lifted",
        "divergence_marsh_weir",
        "divergence_city_weir",
        "cross_plain_weir",
        "cross_smoke_weir",
        "marsh_dye_struck",
        "divergence_marsh_dye",
        "divergence_city_dye",
        "cross_plain_dye",
        "cross_weir_dye",
        "marsh_ferry_crossed",
        "divergence_marsh_ferry",
        "divergence_city_ferry",
        "cross_plain_ferry",
        "cross_dye_ferry",
        "marsh_flats_drained",
        "divergence_marsh_pump",
        "divergence_city_pump",
        "cross_plain_pump",
        "cross_ferry_pump",
        "marsh_oyster_culled",
        "divergence_marsh_oyster",
        "divergence_city_oyster",
        "cross_plain_oyster",
        "cross_pump_oyster",
        "marsh_tally_closed",
        "divergence_marsh_count",
        "divergence_city_count",
        "cross_plain_count",
        "cross_oyster_count",
        "marsh_ice_held",
        "divergence_marsh_ice",
        "divergence_city_ice",
        "cross_plain_ice",
        "cross_count_ice",
        "marsh_wreck_laid",
        "divergence_marsh_wreck",
        "divergence_city_wreck",
        "cross_plain_wreck",
        "cross_ice_wreck",
        "marsh_hive_kept",
        "divergence_marsh_hive",
        "divergence_city_hive",
        "cross_plain_hive",
        "cross_wreck_hive",
        "marsh_mead_drawn",
        "divergence_marsh_mead",
        "divergence_city_mead",
        "cross_plain_mead",
        "cross_hive_mead",
        "marsh_barrel_raised",
        "divergence_marsh_coop",
        "divergence_city_coop",
        "cross_plain_coop",
        "cross_mead_coop",
        "marsh_pickle_lidded",
        "divergence_marsh_pickle",
        "divergence_city_pickle",
        "cross_plain_pickle",
        "cross_coop_pickle",
        "marsh_iron_quenched",
        "divergence_marsh_forge",
        "divergence_city_forge",
        "cross_plain_forge",
        "cross_pickle_forge",
        "marsh_fowl_taken",
        "divergence_marsh_decoy",
        "divergence_city_decoy",
        "cross_plain_decoy",
        "cross_forge_decoy",
        "marsh_lights_bound",
        "divergence_marsh_rush",
        "divergence_city_rush",
        "cross_plain_rush",
        "cross_decoy_rush",
        "marsh_seam_caulked",
        "divergence_marsh_caulk",
        "divergence_city_caulk",
        "cross_plain_caulk",
        "cross_rush_caulk",
        "marsh_net_tarred",
        "divergence_marsh_net",
        "divergence_city_net",
        "cross_plain_net",
        "cross_caulk_net",
        "marsh_sail_hoisted",
        "divergence_marsh_sail",
        "divergence_city_sail",
        "cross_plain_sail",
        "cross_net_sail",
        "marsh_lead_cast",
        "divergence_marsh_lead",
        "divergence_city_lead",
        "cross_plain_lead",
        "cross_sail_lead",
        "marsh_rutter_sealed",
        "divergence_marsh_chart",
        "divergence_city_chart",
        "cross_plain_chart",
        "cross_lead_chart",
        "marsh_buoy_set",
        "divergence_marsh_buoy",
        "divergence_city_buoy",
        "cross_plain_buoy",
        "cross_chart_buoy",
        "marsh_kelp_burned",
        "divergence_marsh_kelp",
        "divergence_city_kelp",
        "cross_plain_kelp",
        "cross_buoy_kelp",
        "marsh_soap_cut",
        "divergence_marsh_soap",
        "divergence_city_soap",
        "cross_plain_soap",
        "cross_kelp_soap",
        "marsh_cloth_fulled",
        "divergence_marsh_full",
        "divergence_city_full",
        "cross_plain_full",
        "cross_soap_full",
        "marsh_coal_drawn",
        "divergence_marsh_char",
        "divergence_city_char",
        "cross_plain_char",
        "cross_full_char",
        "marsh_lime_slaked",
        "divergence_marsh_lime",
        "divergence_city_lime",
        "cross_plain_lime",
        "cross_coal_lime",
        "marsh_joint_pointed",
        "divergence_marsh_mason",
        "divergence_city_mason",
        "cross_plain_mason",
        "cross_lime_mason",
        "marsh_roof_set",
        "divergence_marsh_thatch",
        "divergence_city_thatch",
        "cross_plain_thatch",
        "cross_mason_thatch",
        "marsh_cistern_filled",
        "divergence_marsh_cistern",
        "divergence_city_cistern",
        "cross_plain_cistern",
        "cross_thatch_cistern",
        "marsh_wash_hung",
        "divergence_marsh_wash",
        "divergence_city_wash",
        "cross_plain_wash",
        "cross_cistern_wash",
        "marsh_paper_laid",
        "divergence_marsh_rag",
        "divergence_city_rag",
        "cross_plain_rag",
        "cross_wash_rag",
        "marsh_frail_woven",
        "divergence_marsh_osier",
        "divergence_city_osier",
        "cross_plain_osier",
        "cross_rag_osier",
        "marsh_loaf_drawn",
        "divergence_marsh_bake",
        "divergence_city_bake",
        "cross_plain_bake",
        "cross_osier_bake",
        "marsh_wheel_salted",
        "divergence_marsh_dairy",
        "divergence_city_dairy",
        "cross_plain_dairy",
        "cross_bake_dairy",
        "marsh_web_sheared",
        "divergence_marsh_loom",
        "divergence_city_loom",
        "cross_plain_loom",
        "cross_dairy_loom",
        "marsh_lantern_hung",
        "divergence_marsh_horn",
        "divergence_city_horn",
        "cross_plain_horn",
        "cross_loom_horn",
        "marsh_nib_cut",
        "divergence_marsh_gall",
        "divergence_city_gall",
        "cross_plain_gall",
        "cross_horn_gall",
        "marsh_heel_pegged",
        "divergence_marsh_cobble",
        "divergence_city_cobble",
        "cross_plain_cobble",
        "cross_gall_cobble",
        "marsh_keeve_bunged",
        "divergence_marsh_cider",
        "divergence_city_cider",
        "cross_plain_cider",
        "cross_cobble_cider",
        "marsh_mustard_potted",
        "divergence_marsh_must",
        "divergence_city_must",
        "cross_plain_must",
        "cross_cider_must",
        "marsh_sausage_linked",
        "divergence_marsh_link",
        "divergence_city_link",
        "cross_plain_link",
        "cross_must_link",
        "marsh_pie_crimped",
        "divergence_marsh_pie",
        "divergence_city_pie",
        "cross_plain_pie",
        "cross_link_pie",
        "marsh_jam_jarred",
        "divergence_marsh_jam",
        "divergence_city_jam",
        "cross_plain_jam",
        "cross_pie_jam",
        "marsh_crock_glazed",
        "divergence_marsh_crock",
        "divergence_city_crock",
        "cross_plain_crock",
        "cross_jam_crock",
        "marsh_hide_tanned",
        "divergence_marsh_hide",
        "divergence_city_hide",
        "cross_plain_hide",
        "cross_crock_hide",
        "marsh_flax_spun",
        "divergence_marsh_flax",
        "divergence_city_flax",
        "cross_plain_flax",
        "cross_hide_flax",
        "marsh_nail_pointed",
        "divergence_marsh_nail",
        "divergence_city_nail",
        "cross_plain_nail",
        "cross_flax_nail",
        "marsh_tyre_set",
        "divergence_marsh_wain",
        "divergence_city_wain",
        "cross_plain_wain",
        "cross_nail_wain",
        "marsh_malt_oasted",
        "divergence_marsh_malt",
        "divergence_city_malt",
        "cross_plain_malt",
        "cross_wain_malt",
        "marsh_gyle_racked",
        "divergence_marsh_brew",
        "divergence_city_brew",
        "cross_plain_brew",
        "cross_malt_brew",
        "marsh_cruet_corked",
        "divergence_marsh_acet",
        "divergence_city_acet",
        "cross_plain_acet",
        "cross_brew_acet",
        "marsh_glue_caked",
        "divergence_marsh_glue",
        "divergence_city_glue",
        "cross_plain_glue",
        "cross_acet_glue",
        "marsh_book_bound",
        "divergence_marsh_bind",
        "divergence_city_bind",
        "cross_plain_bind",
        "cross_glue_bind",
        "marsh_plate_burnished",
        "divergence_marsh_gilt",
        "divergence_city_gilt",
        "cross_plain_gilt",
        "cross_bind_gilt",
        "marsh_collet_closed",
        "divergence_marsh_gem",
        "divergence_city_gem",
        "cross_plain_gem",
        "cross_gilt_gem",
        "marsh_pane_camed",
        "divergence_marsh_glaz",
        "divergence_city_glaz",
        "cross_plain_glaz",
        "cross_gem_glaz",
        "marsh_sash_pinned",
        "divergence_marsh_sash",
        "divergence_city_sash",
        "cross_plain_sash",
        "cross_glaz_sash",
        "marsh_light_dusted",
        "divergence_marsh_putty",
        "divergence_city_putty",
        "cross_plain_putty",
        "cross_sash_putty",
        "marsh_coat_brushed",
        "divergence_marsh_paint",
        "divergence_city_paint",
        "cross_plain_paint",
        "cross_putty_paint",
        "marsh_varnish_flowed",
        "divergence_marsh_varn",
        "divergence_city_varn",
        "cross_plain_varn",
        "cross_paint_varn",
        "marsh_latch_thrown",
        "divergence_marsh_latch",
        "divergence_city_latch",
        "cross_plain_latch",
        "cross_varn_latch",
        "marsh_gudgeon_shipped",
        "divergence_marsh_hinge",
        "divergence_city_hinge",
        "cross_plain_hinge",
        "cross_latch_hinge",
        "marsh_casement_stayed",
        "divergence_marsh_stay",
        "divergence_city_stay",
        "cross_plain_stay",
        "cross_hinge_stay",
        "marsh_stool_seated",
        "divergence_marsh_sill",
        "divergence_city_sill",
        "cross_plain_sill",
        "cross_stay_sill",
        "marsh_casing_tacked",
        "divergence_marsh_case",
        "divergence_city_case",
        "cross_plain_case",
        "cross_sill_case",
        "marsh_plinth_fixed",
        "divergence_marsh_skirt",
        "divergence_city_skirt",
        "cross_plain_skirt",
        "cross_case_skirt",
        "marsh_rail_capped",
        "divergence_marsh_dado",
        "divergence_city_dado",
        "cross_plain_dado",
        "cross_skirt_dado",
        "marsh_rail_sprung",
        "divergence_marsh_pic",
        "divergence_city_pic",
        "cross_plain_pic",
        "cross_dado_pic",
        "marsh_cornice_floated",
        "divergence_marsh_corn",
        "divergence_city_corn",
        "cross_plain_corn",
        "cross_pic_corn",
        "marsh_riser_wedged",
        "divergence_marsh_stair",
        "divergence_city_stair",
        "cross_plain_stair",
        "cross_corn_stair",
        "marsh_finial_dowelled",
        "divergence_marsh_newel",
        "divergence_city_newel",
        "cross_plain_newel",
        "cross_stair_newel",
        "marsh_ramp_wreathed",
        "divergence_marsh_hand",
        "divergence_city_hand",
        "cross_plain_hand",
        "cross_newel_hand",
        "marsh_neck_shouldered",
        "divergence_marsh_bal",
        "divergence_city_bal",
        "cross_plain_bal",
        "cross_hand_bal",
        "marsh_end_returned",
        "divergence_marsh_tread",
        "divergence_city_tread",
        "cross_plain_tread",
        "cross_bal_tread",
        "marsh_nail_secreted",
        "divergence_marsh_floor",
        "divergence_city_floor",
        "cross_plain_floor",
        "cross_tread_floor",
        "marsh_camber_crowned",
        "divergence_marsh_joist",
        "divergence_city_joist",
        "cross_plain_joist",
        "cross_floor_joist",
        "marsh_coat_haired",
        "divergence_marsh_lath",
        "divergence_city_lath",
        "cross_plain_lath",
        "cross_joist_lath",
        "marsh_breast_limed",
        "divergence_marsh_chim",
        "divergence_city_chim",
        "cross_plain_chim",
        "cross_lath_chim",
        "marsh_mantel_pinned",
        "divergence_marsh_mant",
        "divergence_city_mant",
        "cross_plain_mant",
        "cross_chim_mant",
        "marsh_cowl_hung",
        "divergence_marsh_flue",
        "divergence_city_flue",
        "cross_plain_flue",
        "cross_mant_flue",
        "marsh_back_bedded",
        "divergence_marsh_fb",
        "divergence_city_fb",
        "cross_plain_fb",
        "cross_flue_fb",
        "marsh_slide_registered",
        "divergence_marsh_grate",
        "divergence_city_grate",
        "cross_plain_grate",
        "cross_fb_grate",
        "marsh_hack_set",
        "divergence_marsh_brick",
        "divergence_city_brick",
        "cross_plain_brick",
        "cross_grate_brick",
        "marsh_arris_nicked",
        "divergence_marsh_tile",
        "divergence_city_tile",
        "cross_plain_tile",
        "cross_brick_tile",
        "marsh_slate_lapped",
        "divergence_marsh_slate",
        "divergence_city_slate",
        "cross_plain_slate",
        "cross_tile_slate",
        "marsh_flash_dressed",
        "divergence_marsh_flash",
        "divergence_city_flash",
        "cross_plain_flash",
        "cross_slate_flash",
        "marsh_block_stropped",
        "divergence_marsh_block",
        "divergence_city_block",
        "cross_plain_block",
        "cross_flash_block",
        "marsh_grip_bound",
        "divergence_marsh_oar",
        "divergence_city_oar",
        "cross_plain_oar",
        "cross_block_oar",
        "marsh_hull_launched",
        "divergence_marsh_ways",
        "divergence_city_ways",
        "cross_plain_ways",
        "cross_oar_ways",
        "marsh_garboard_faired",
        "divergence_marsh_clink",
        "divergence_city_clink",
        "cross_plain_clink",
        "cross_ways_clink",
        "marsh_round_heaved",
        "divergence_marsh_wind",
        "divergence_city_wind",
        "cross_plain_wind",
        "cross_clink_wind",
        "marsh_station_bevelled",
        "divergence_marsh_offs",
        "divergence_city_offs",
        "cross_plain_offs",
        "cross_wind_offs",
        "marsh_trunnel_driven",
        "divergence_marsh_trun",
        "divergence_city_trun",
        "cross_plain_trun",
        "cross_offs_trun",
        "marsh_hog_bolted",
        "divergence_marsh_dead",
        "divergence_city_dead",
        "cross_plain_dead",
        "cross_trun_dead",
        "marsh_partner_hooped",
        "divergence_marsh_mast",
        "divergence_city_mast",
        "cross_plain_mast",
        "cross_dead_mast",
        "marsh_knee_hung",
        "divergence_marsh_stem",
        "divergence_city_stem",
        "cross_plain_stem",
        "cross_mast_stem",
        "marsh_eye_seized",
        "divergence_marsh_fid",
        "divergence_city_fid",
        "cross_plain_fid",
        "cross_stem_fid",
        "marsh_base_bolted",
        "divergence_marsh_cleat",
        "divergence_city_cleat",
        "cross_plain_cleat",
        "cross_fid_cleat",
        "marsh_collar_paid",
        "divergence_marsh_haw",
        "divergence_city_haw",
        "cross_plain_haw",
        "cross_cleat_haw",
        "marsh_lanyard_seized",
        "divergence_marsh_deye",
        "divergence_city_deye",
        "cross_plain_deye",
        "cross_haw_deye",
        "marsh_parrel_trussed",
        "divergence_marsh_par",
        "divergence_city_par",
        "cross_plain_par",
        "cross_deye_par",
        "marsh_cable_belayed",
        "divergence_marsh_bitt",
        "divergence_city_bitt",
        "cross_plain_bitt",
        "cross_par_bitt",
        "marsh_gammon_frapped",
        "divergence_marsh_gam",
        "divergence_city_gam",
        "cross_plain_gam",
        "cross_bitt_gam",
        "marsh_tiller_yoked",
        "divergence_marsh_till",
        "divergence_city_till",
        "cross_plain_till",
        "cross_gam_till",
        "marsh_fluke_fished",
        "divergence_marsh_cath",
        "divergence_city_cath",
        "cross_plain_cath",
        "cross_till_cath",
        "marsh_stern_spiked",
        "divergence_marsh_tran",
        "divergence_city_tran",
        "cross_plain_tran",
        "cross_cath_tran",
        "marsh_mouth_plugged",
        "divergence_marsh_scup",
        "divergence_city_scup",
        "cross_plain_scup",
        "cross_tran_scup",
        "marsh_card_locked",
        "divergence_marsh_binn",
        "divergence_city_binn",
        "cross_plain_binn",
        "cross_scup_binn",
        "marsh_belly_clenched",
        "divergence_marsh_futt",
        "divergence_city_futt",
        "cross_plain_futt",
        "cross_binn_futt",
        "marsh_bolster_seized",
        "divergence_marsh_cros",
        "divergence_city_cros",
        "cross_plain_cros",
        "cross_futt_cros",
        "marsh_waterway_paid",
        "divergence_marsh_wtr",
        "divergence_city_wtr",
        "cross_plain_wtr",
        "cross_cros_wtr",
        "marsh_coaming_coaked",
        "divergence_marsh_coam",
        "divergence_city_coam",
        "cross_plain_coam",
        "cross_wtr_coam",
        "marsh_bolt_dumped",
        "divergence_marsh_wale",
        "divergence_city_wale",
        "cross_plain_wale",
        "cross_coam_wale",
        "marsh_davit_shipped",
        "divergence_marsh_dav",
        "divergence_city_dav",
        "cross_plain_dav",
        "cross_wale_dav",
        "marsh_guy_seized",
        "divergence_marsh_boom",
        "divergence_city_boom",
        "cross_plain_boom",
        "cross_dav_boom",
        "marsh_strap_set",
        "divergence_marsh_chan",
        "divergence_city_chan",
        "cross_plain_chan",
        "cross_boom_chan",
        "marsh_kevel_clenched",
        "divergence_marsh_kev",
        "divergence_city_kev",
        "cross_plain_kev",
        "cross_chan_kev",
        "marsh_knight_lashed",
        "divergence_marsh_kni",
        "divergence_city_kni",
        "cross_plain_kni",
        "cross_kev_kni",
        "marsh_carling_spiked",
        "divergence_marsh_carl",
        "divergence_city_carl",
        "cross_plain_carl",
        "cross_kni_carl",
        "marsh_keeper_pinned",
        "divergence_marsh_tab",
        "divergence_city_tab",
        "cross_plain_tab",
        "cross_carl_tab",
        "marsh_edge_dumped",
        "divergence_marsh_psh",
        "divergence_city_psh",
        "cross_plain_psh",
        "cross_tab_psh",
        "marsh_spirket_clenched",
        "divergence_marsh_spi",
        "divergence_city_spi",
        "cross_plain_spi",
        "cross_psh_spi",
        "marsh_bib_seized",
        "divergence_marsh_trs",
        "divergence_city_trs",
        "cross_plain_trs",
        "cross_spi_trs",
        "marsh_hook_fayed",
        "divergence_marsh_brh",
        "divergence_city_brh",
        "cross_plain_brh",
        "cross_trs_brh",
        "marsh_lodging_nicked",
        "divergence_marsh_lod",
        "divergence_city_lod",
        "cross_plain_lod",
        "cross_brh_lod",
        "marsh_sirmark_marked",
        "divergence_marsh_dag",
        "divergence_city_dag",
        "cross_plain_dag",
        "cross_lod_dag",
        "marsh_wring_dumped",
        "divergence_marsh_rid",
        "divergence_city_rid",
        "cross_plain_rid",
        "cross_dag_rid",
        "marsh_sister_bolted",
        "divergence_marsh_ksn",
        "divergence_city_ksn",
        "cross_plain_ksn",
        "cross_rid_ksn",
        "marsh_crotch_spiked",
        "divergence_marsh_cru",
        "divergence_city_cru",
        "cross_plain_cru",
        "cross_ksn_cru",
        "marsh_compound_dumped",
        "divergence_marsh_ptr",
        "divergence_city_ptr",
        "cross_plain_ptr",
        "cross_cru_ptr",
        "marsh_foot_spiked",
        "divergence_marsh_stn",
        "divergence_city_stn",
        "cross_plain_stn",
        "cross_ptr_stn",
        "marsh_queen_shored",
        "divergence_marsh_pil",
        "divergence_city_pil",
        "cross_plain_pil",
        "cross_stn_pil",
    )
    missing = [name for name in required if name not in by_id]
    if missing:
        raise AssertionError(f"I4 missing traces {missing}")

    for trace in traces:
        accept_trace(content, trace)

    compact = replay(content, by_id["marsh_harbor_compact"]["seed"], by_id["marsh_harbor_compact"]["sheet"], by_id["marsh_harbor_compact"]["actions"])
    relic = replay(content, by_id["marsh_stack_relic"]["seed"], by_id["marsh_stack_relic"]["sheet"], by_id["marsh_stack_relic"]["actions"])
    kiln = replay(content, by_id["marsh_kiln_pact"]["seed"], by_id["marsh_kiln_pact"]["sheet"], by_id["marsh_kiln_pact"]["actions"])
    court = replay(content, by_id["marsh_reed_sentence"]["seed"], by_id["marsh_reed_sentence"]["sheet"], by_id["marsh_reed_sentence"]["actions"])
    beacon = replay(content, by_id["marsh_road_beacon"]["seed"], by_id["marsh_road_beacon"]["sheet"], by_id["marsh_road_beacon"]["actions"])
    fever = replay(content, by_id["marsh_fever_broken"]["seed"], by_id["marsh_fever_broken"]["sheet"], by_id["marsh_fever_broken"]["actions"])
    named = replay(content, by_id["marsh_name_restored"]["seed"], by_id["marsh_name_restored"]["sheet"], by_id["marsh_name_restored"]["actions"])
    fold = replay(content, by_id["marsh_fold_held"]["seed"], by_id["marsh_fold_held"]["sheet"], by_id["marsh_fold_held"]["actions"])
    lens = replay(content, by_id["marsh_lens_set"]["seed"], by_id["marsh_lens_set"]["sheet"], by_id["marsh_lens_set"]["actions"])
    rope = replay(content, by_id["marsh_rope_walked"]["seed"], by_id["marsh_rope_walked"]["sheet"], by_id["marsh_rope_walked"]["actions"])
    salt = replay(content, by_id["marsh_salt_raked"]["seed"], by_id["marsh_salt_raked"]["sheet"], by_id["marsh_salt_raked"]["actions"])
    smoke = replay(content, by_id["marsh_smoke_cured"]["seed"], by_id["marsh_smoke_cured"]["sheet"], by_id["marsh_smoke_cured"]["actions"])
    weir = replay(content, by_id["marsh_weir_lifted"]["seed"], by_id["marsh_weir_lifted"]["sheet"], by_id["marsh_weir_lifted"]["actions"])
    dye = replay(content, by_id["marsh_dye_struck"]["seed"], by_id["marsh_dye_struck"]["sheet"], by_id["marsh_dye_struck"]["actions"])
    ferry = replay(content, by_id["marsh_ferry_crossed"]["seed"], by_id["marsh_ferry_crossed"]["sheet"], by_id["marsh_ferry_crossed"]["actions"])
    pump = replay(content, by_id["marsh_flats_drained"]["seed"], by_id["marsh_flats_drained"]["sheet"], by_id["marsh_flats_drained"]["actions"])
    oyster = replay(content, by_id["marsh_oyster_culled"]["seed"], by_id["marsh_oyster_culled"]["sheet"], by_id["marsh_oyster_culled"]["actions"])
    tally = replay(content, by_id["marsh_tally_closed"]["seed"], by_id["marsh_tally_closed"]["sheet"], by_id["marsh_tally_closed"]["actions"])
    ice = replay(content, by_id["marsh_ice_held"]["seed"], by_id["marsh_ice_held"]["sheet"], by_id["marsh_ice_held"]["actions"])
    wreck = replay(content, by_id["marsh_wreck_laid"]["seed"], by_id["marsh_wreck_laid"]["sheet"], by_id["marsh_wreck_laid"]["actions"])
    hive = replay(content, by_id["marsh_hive_kept"]["seed"], by_id["marsh_hive_kept"]["sheet"], by_id["marsh_hive_kept"]["actions"])
    mead = replay(content, by_id["marsh_mead_drawn"]["seed"], by_id["marsh_mead_drawn"]["sheet"], by_id["marsh_mead_drawn"]["actions"])
    barrel = replay(content, by_id["marsh_barrel_raised"]["seed"], by_id["marsh_barrel_raised"]["sheet"], by_id["marsh_barrel_raised"]["actions"])
    pickle = replay(content, by_id["marsh_pickle_lidded"]["seed"], by_id["marsh_pickle_lidded"]["sheet"], by_id["marsh_pickle_lidded"]["actions"])
    iron = replay(content, by_id["marsh_iron_quenched"]["seed"], by_id["marsh_iron_quenched"]["sheet"], by_id["marsh_iron_quenched"]["actions"])
    fowl = replay(content, by_id["marsh_fowl_taken"]["seed"], by_id["marsh_fowl_taken"]["sheet"], by_id["marsh_fowl_taken"]["actions"])
    rush = replay(content, by_id["marsh_lights_bound"]["seed"], by_id["marsh_lights_bound"]["sheet"], by_id["marsh_lights_bound"]["actions"])
    caulk = replay(content, by_id["marsh_seam_caulked"]["seed"], by_id["marsh_seam_caulked"]["sheet"], by_id["marsh_seam_caulked"]["actions"])
    netted = replay(content, by_id["marsh_net_tarred"]["seed"], by_id["marsh_net_tarred"]["sheet"], by_id["marsh_net_tarred"]["actions"])
    hoisted = replay(content, by_id["marsh_sail_hoisted"]["seed"], by_id["marsh_sail_hoisted"]["sheet"], by_id["marsh_sail_hoisted"]["actions"])
    sounding = replay(content, by_id["marsh_lead_cast"]["seed"], by_id["marsh_lead_cast"]["sheet"], by_id["marsh_lead_cast"]["actions"])
    rutter = replay(content, by_id["marsh_rutter_sealed"]["seed"], by_id["marsh_rutter_sealed"]["sheet"], by_id["marsh_rutter_sealed"]["actions"])
    buoy = replay(content, by_id["marsh_buoy_set"]["seed"], by_id["marsh_buoy_set"]["sheet"], by_id["marsh_buoy_set"]["actions"])
    kelp = replay(content, by_id["marsh_kelp_burned"]["seed"], by_id["marsh_kelp_burned"]["sheet"], by_id["marsh_kelp_burned"]["actions"])
    soap = replay(content, by_id["marsh_soap_cut"]["seed"], by_id["marsh_soap_cut"]["sheet"], by_id["marsh_soap_cut"]["actions"])
    cloth = replay(content, by_id["marsh_cloth_fulled"]["seed"], by_id["marsh_cloth_fulled"]["sheet"], by_id["marsh_cloth_fulled"]["actions"])
    coal = replay(content, by_id["marsh_coal_drawn"]["seed"], by_id["marsh_coal_drawn"]["sheet"], by_id["marsh_coal_drawn"]["actions"])
    lime = replay(content, by_id["marsh_lime_slaked"]["seed"], by_id["marsh_lime_slaked"]["sheet"], by_id["marsh_lime_slaked"]["actions"])
    pointed = replay(content, by_id["marsh_joint_pointed"]["seed"], by_id["marsh_joint_pointed"]["sheet"], by_id["marsh_joint_pointed"]["actions"])
    roof = replay(content, by_id["marsh_roof_set"]["seed"], by_id["marsh_roof_set"]["sheet"], by_id["marsh_roof_set"]["actions"])
    filled = replay(content, by_id["marsh_cistern_filled"]["seed"], by_id["marsh_cistern_filled"]["sheet"], by_id["marsh_cistern_filled"]["actions"])
    hung = replay(content, by_id["marsh_wash_hung"]["seed"], by_id["marsh_wash_hung"]["sheet"], by_id["marsh_wash_hung"]["actions"])
    laid = replay(content, by_id["marsh_paper_laid"]["seed"], by_id["marsh_paper_laid"]["sheet"], by_id["marsh_paper_laid"]["actions"])
    woven = replay(content, by_id["marsh_frail_woven"]["seed"], by_id["marsh_frail_woven"]["sheet"], by_id["marsh_frail_woven"]["actions"])
    loaf = replay(content, by_id["marsh_loaf_drawn"]["seed"], by_id["marsh_loaf_drawn"]["sheet"], by_id["marsh_loaf_drawn"]["actions"])
    salted = replay(content, by_id["marsh_wheel_salted"]["seed"], by_id["marsh_wheel_salted"]["sheet"], by_id["marsh_wheel_salted"]["actions"])
    sheared = replay(content, by_id["marsh_web_sheared"]["seed"], by_id["marsh_web_sheared"]["sheet"], by_id["marsh_web_sheared"]["actions"])
    lantern = replay(content, by_id["marsh_lantern_hung"]["seed"], by_id["marsh_lantern_hung"]["sheet"], by_id["marsh_lantern_hung"]["actions"])
    nibbed = replay(content, by_id["marsh_nib_cut"]["seed"], by_id["marsh_nib_cut"]["sheet"], by_id["marsh_nib_cut"]["actions"])
    pegged = replay(content, by_id["marsh_heel_pegged"]["seed"], by_id["marsh_heel_pegged"]["sheet"], by_id["marsh_heel_pegged"]["actions"])
    bunged = replay(content, by_id["marsh_keeve_bunged"]["seed"], by_id["marsh_keeve_bunged"]["sheet"], by_id["marsh_keeve_bunged"]["actions"])
    potted = replay(content, by_id["marsh_mustard_potted"]["seed"], by_id["marsh_mustard_potted"]["sheet"], by_id["marsh_mustard_potted"]["actions"])
    linked = replay(content, by_id["marsh_sausage_linked"]["seed"], by_id["marsh_sausage_linked"]["sheet"], by_id["marsh_sausage_linked"]["actions"])
    crimped = replay(content, by_id["marsh_pie_crimped"]["seed"], by_id["marsh_pie_crimped"]["sheet"], by_id["marsh_pie_crimped"]["actions"])
    jarred = replay(content, by_id["marsh_jam_jarred"]["seed"], by_id["marsh_jam_jarred"]["sheet"], by_id["marsh_jam_jarred"]["actions"])
    glazed = replay(content, by_id["marsh_crock_glazed"]["seed"], by_id["marsh_crock_glazed"]["sheet"], by_id["marsh_crock_glazed"]["actions"])
    tanned = replay(content, by_id["marsh_hide_tanned"]["seed"], by_id["marsh_hide_tanned"]["sheet"], by_id["marsh_hide_tanned"]["actions"])
    spun = replay(content, by_id["marsh_flax_spun"]["seed"], by_id["marsh_flax_spun"]["sheet"], by_id["marsh_flax_spun"]["actions"])
    nailed = replay(content, by_id["marsh_nail_pointed"]["seed"], by_id["marsh_nail_pointed"]["sheet"], by_id["marsh_nail_pointed"]["actions"])
    tyred = replay(content, by_id["marsh_tyre_set"]["seed"], by_id["marsh_tyre_set"]["sheet"], by_id["marsh_tyre_set"]["actions"])
    oasted = replay(content, by_id["marsh_malt_oasted"]["seed"], by_id["marsh_malt_oasted"]["sheet"], by_id["marsh_malt_oasted"]["actions"])
    gyled = replay(content, by_id["marsh_gyle_racked"]["seed"], by_id["marsh_gyle_racked"]["sheet"], by_id["marsh_gyle_racked"]["actions"])
    corked = replay(content, by_id["marsh_cruet_corked"]["seed"], by_id["marsh_cruet_corked"]["sheet"], by_id["marsh_cruet_corked"]["actions"])
    glued = replay(content, by_id["marsh_glue_caked"]["seed"], by_id["marsh_glue_caked"]["sheet"], by_id["marsh_glue_caked"]["actions"])
    booked = replay(content, by_id["marsh_book_bound"]["seed"], by_id["marsh_book_bound"]["sheet"], by_id["marsh_book_bound"]["actions"])
    gilded = replay(content, by_id["marsh_plate_burnished"]["seed"], by_id["marsh_plate_burnished"]["sheet"], by_id["marsh_plate_burnished"]["actions"])
    gemmed = replay(content, by_id["marsh_collet_closed"]["seed"], by_id["marsh_collet_closed"]["sheet"], by_id["marsh_collet_closed"]["actions"])
    camed = replay(content, by_id["marsh_pane_camed"]["seed"], by_id["marsh_pane_camed"]["sheet"], by_id["marsh_pane_camed"]["actions"])
    sashed = replay(content, by_id["marsh_sash_pinned"]["seed"], by_id["marsh_sash_pinned"]["sheet"], by_id["marsh_sash_pinned"]["actions"])
    dusted = replay(content, by_id["marsh_light_dusted"]["seed"], by_id["marsh_light_dusted"]["sheet"], by_id["marsh_light_dusted"]["actions"])
    coated = replay(content, by_id["marsh_coat_brushed"]["seed"], by_id["marsh_coat_brushed"]["sheet"], by_id["marsh_coat_brushed"]["actions"])
    varnished = replay(content, by_id["marsh_varnish_flowed"]["seed"], by_id["marsh_varnish_flowed"]["sheet"], by_id["marsh_varnish_flowed"]["actions"])
    latched = replay(content, by_id["marsh_latch_thrown"]["seed"], by_id["marsh_latch_thrown"]["sheet"], by_id["marsh_latch_thrown"]["actions"])
    hinged = replay(content, by_id["marsh_gudgeon_shipped"]["seed"], by_id["marsh_gudgeon_shipped"]["sheet"], by_id["marsh_gudgeon_shipped"]["actions"])
    stayed = replay(content, by_id["marsh_casement_stayed"]["seed"], by_id["marsh_casement_stayed"]["sheet"], by_id["marsh_casement_stayed"]["actions"])
    seated = replay(content, by_id["marsh_stool_seated"]["seed"], by_id["marsh_stool_seated"]["sheet"], by_id["marsh_stool_seated"]["actions"])
    cased = replay(content, by_id["marsh_casing_tacked"]["seed"], by_id["marsh_casing_tacked"]["sheet"], by_id["marsh_casing_tacked"]["actions"])
    skirted = replay(content, by_id["marsh_plinth_fixed"]["seed"], by_id["marsh_plinth_fixed"]["sheet"], by_id["marsh_plinth_fixed"]["actions"])
    dadoed = replay(content, by_id["marsh_rail_capped"]["seed"], by_id["marsh_rail_capped"]["sheet"], by_id["marsh_rail_capped"]["actions"])
    sprung = replay(content, by_id["marsh_rail_sprung"]["seed"], by_id["marsh_rail_sprung"]["sheet"], by_id["marsh_rail_sprung"]["actions"])
    coved = replay(content, by_id["marsh_cornice_floated"]["seed"], by_id["marsh_cornice_floated"]["sheet"], by_id["marsh_cornice_floated"]["actions"])
    staired = replay(content, by_id["marsh_riser_wedged"]["seed"], by_id["marsh_riser_wedged"]["sheet"], by_id["marsh_riser_wedged"]["actions"])
    newelled = replay(content, by_id["marsh_finial_dowelled"]["seed"], by_id["marsh_finial_dowelled"]["sheet"], by_id["marsh_finial_dowelled"]["actions"])
    wreathed = replay(content, by_id["marsh_ramp_wreathed"]["seed"], by_id["marsh_ramp_wreathed"]["sheet"], by_id["marsh_ramp_wreathed"]["actions"])
    balustered = replay(content, by_id["marsh_neck_shouldered"]["seed"], by_id["marsh_neck_shouldered"]["sheet"], by_id["marsh_neck_shouldered"]["actions"])
    trod = replay(content, by_id["marsh_end_returned"]["seed"], by_id["marsh_end_returned"]["sheet"], by_id["marsh_end_returned"]["actions"])
    floored = replay(content, by_id["marsh_nail_secreted"]["seed"], by_id["marsh_nail_secreted"]["sheet"], by_id["marsh_nail_secreted"]["actions"])
    joisted = replay(content, by_id["marsh_camber_crowned"]["seed"], by_id["marsh_camber_crowned"]["sheet"], by_id["marsh_camber_crowned"]["actions"])
    lathed = replay(content, by_id["marsh_coat_haired"]["seed"], by_id["marsh_coat_haired"]["sheet"], by_id["marsh_coat_haired"]["actions"])
    chimneyed = replay(content, by_id["marsh_breast_limed"]["seed"], by_id["marsh_breast_limed"]["sheet"], by_id["marsh_breast_limed"]["actions"])
    mantelled = replay(content, by_id["marsh_mantel_pinned"]["seed"], by_id["marsh_mantel_pinned"]["sheet"], by_id["marsh_mantel_pinned"]["actions"])
    flued = replay(content, by_id["marsh_cowl_hung"]["seed"], by_id["marsh_cowl_hung"]["sheet"], by_id["marsh_cowl_hung"]["actions"])
    backed = replay(content, by_id["marsh_back_bedded"]["seed"], by_id["marsh_back_bedded"]["sheet"], by_id["marsh_back_bedded"]["actions"])
    grated = replay(content, by_id["marsh_slide_registered"]["seed"], by_id["marsh_slide_registered"]["sheet"], by_id["marsh_slide_registered"]["actions"])
    bricked = replay(content, by_id["marsh_hack_set"]["seed"], by_id["marsh_hack_set"]["sheet"], by_id["marsh_hack_set"]["actions"])
    tiled = replay(content, by_id["marsh_arris_nicked"]["seed"], by_id["marsh_arris_nicked"]["sheet"], by_id["marsh_arris_nicked"]["actions"])
    slated = replay(content, by_id["marsh_slate_lapped"]["seed"], by_id["marsh_slate_lapped"]["sheet"], by_id["marsh_slate_lapped"]["actions"])
    flashed = replay(content, by_id["marsh_flash_dressed"]["seed"], by_id["marsh_flash_dressed"]["sheet"], by_id["marsh_flash_dressed"]["actions"])
    stropped = replay(content, by_id["marsh_block_stropped"]["seed"], by_id["marsh_block_stropped"]["sheet"], by_id["marsh_block_stropped"]["actions"])
    oared = replay(content, by_id["marsh_grip_bound"]["seed"], by_id["marsh_grip_bound"]["sheet"], by_id["marsh_grip_bound"]["actions"])
    launched = replay(content, by_id["marsh_hull_launched"]["seed"], by_id["marsh_hull_launched"]["sheet"], by_id["marsh_hull_launched"]["actions"])
    clinked = replay(content, by_id["marsh_garboard_faired"]["seed"], by_id["marsh_garboard_faired"]["sheet"], by_id["marsh_garboard_faired"]["actions"])
    heaved = replay(content, by_id["marsh_round_heaved"]["seed"], by_id["marsh_round_heaved"]["sheet"], by_id["marsh_round_heaved"]["actions"])
    lofted = replay(content, by_id["marsh_station_bevelled"]["seed"], by_id["marsh_station_bevelled"]["sheet"], by_id["marsh_station_bevelled"]["actions"])
    trunnelled = replay(content, by_id["marsh_trunnel_driven"]["seed"], by_id["marsh_trunnel_driven"]["sheet"], by_id["marsh_trunnel_driven"]["actions"])
    hogged = replay(content, by_id["marsh_hog_bolted"]["seed"], by_id["marsh_hog_bolted"]["sheet"], by_id["marsh_hog_bolted"]["actions"])
    masted = replay(content, by_id["marsh_partner_hooped"]["seed"], by_id["marsh_partner_hooped"]["sheet"], by_id["marsh_partner_hooped"]["actions"])
    stemmed = replay(content, by_id["marsh_knee_hung"]["seed"], by_id["marsh_knee_hung"]["sheet"], by_id["marsh_knee_hung"]["actions"])
    fidded = replay(content, by_id["marsh_eye_seized"]["seed"], by_id["marsh_eye_seized"]["sheet"], by_id["marsh_eye_seized"]["actions"])
    cleated = replay(content, by_id["marsh_base_bolted"]["seed"], by_id["marsh_base_bolted"]["sheet"], by_id["marsh_base_bolted"]["actions"])
    hawsed = replay(content, by_id["marsh_collar_paid"]["seed"], by_id["marsh_collar_paid"]["sheet"], by_id["marsh_collar_paid"]["actions"])
    deadeyed = replay(content, by_id["marsh_lanyard_seized"]["seed"], by_id["marsh_lanyard_seized"]["sheet"], by_id["marsh_lanyard_seized"]["actions"])
    parreled = replay(content, by_id["marsh_parrel_trussed"]["seed"], by_id["marsh_parrel_trussed"]["sheet"], by_id["marsh_parrel_trussed"]["actions"])
    belayed = replay(content, by_id["marsh_cable_belayed"]["seed"], by_id["marsh_cable_belayed"]["sheet"], by_id["marsh_cable_belayed"]["actions"])
    gammoned = replay(content, by_id["marsh_gammon_frapped"]["seed"], by_id["marsh_gammon_frapped"]["sheet"], by_id["marsh_gammon_frapped"]["actions"])
    tillered = replay(content, by_id["marsh_tiller_yoked"]["seed"], by_id["marsh_tiller_yoked"]["sheet"], by_id["marsh_tiller_yoked"]["actions"])
    catheaded = replay(content, by_id["marsh_fluke_fished"]["seed"], by_id["marsh_fluke_fished"]["sheet"], by_id["marsh_fluke_fished"]["actions"])
    transomed = replay(content, by_id["marsh_stern_spiked"]["seed"], by_id["marsh_stern_spiked"]["sheet"], by_id["marsh_stern_spiked"]["actions"])
    scuppered = replay(content, by_id["marsh_mouth_plugged"]["seed"], by_id["marsh_mouth_plugged"]["sheet"], by_id["marsh_mouth_plugged"]["actions"])
    binnacled = replay(content, by_id["marsh_card_locked"]["seed"], by_id["marsh_card_locked"]["sheet"], by_id["marsh_card_locked"]["actions"])
    futtocked = replay(content, by_id["marsh_belly_clenched"]["seed"], by_id["marsh_belly_clenched"]["sheet"], by_id["marsh_belly_clenched"]["actions"])
    crosstreed = replay(content, by_id["marsh_bolster_seized"]["seed"], by_id["marsh_bolster_seized"]["sheet"], by_id["marsh_bolster_seized"]["actions"])
    waterwayed = replay(content, by_id["marsh_waterway_paid"]["seed"], by_id["marsh_waterway_paid"]["sheet"], by_id["marsh_waterway_paid"]["actions"])
    coamed = replay(content, by_id["marsh_coaming_coaked"]["seed"], by_id["marsh_coaming_coaked"]["sheet"], by_id["marsh_coaming_coaked"]["actions"])
    gunwaled = replay(content, by_id["marsh_bolt_dumped"]["seed"], by_id["marsh_bolt_dumped"]["sheet"], by_id["marsh_bolt_dumped"]["actions"])
    davited = replay(content, by_id["marsh_davit_shipped"]["seed"], by_id["marsh_davit_shipped"]["sheet"], by_id["marsh_davit_shipped"]["actions"])
    boomkined = replay(content, by_id["marsh_guy_seized"]["seed"], by_id["marsh_guy_seized"]["sheet"], by_id["marsh_guy_seized"]["actions"])
    channeled = replay(content, by_id["marsh_strap_set"]["seed"], by_id["marsh_strap_set"]["sheet"], by_id["marsh_strap_set"]["actions"])
    keveled = replay(content, by_id["marsh_kevel_clenched"]["seed"], by_id["marsh_kevel_clenched"]["sheet"], by_id["marsh_kevel_clenched"]["actions"])
    knighted = replay(content, by_id["marsh_knight_lashed"]["seed"], by_id["marsh_knight_lashed"]["sheet"], by_id["marsh_knight_lashed"]["actions"])
    carlinged = replay(content, by_id["marsh_carling_spiked"]["seed"], by_id["marsh_carling_spiked"]["sheet"], by_id["marsh_carling_spiked"]["actions"])
    tabernacled = replay(content, by_id["marsh_keeper_pinned"]["seed"], by_id["marsh_keeper_pinned"]["sheet"], by_id["marsh_keeper_pinned"]["actions"])
    edged = replay(content, by_id["marsh_edge_dumped"]["seed"], by_id["marsh_edge_dumped"]["sheet"], by_id["marsh_edge_dumped"]["actions"])
    spirketed = replay(content, by_id["marsh_spirket_clenched"]["seed"], by_id["marsh_spirket_clenched"]["sheet"], by_id["marsh_spirket_clenched"]["actions"])
    trestled = replay(content, by_id["marsh_bib_seized"]["seed"], by_id["marsh_bib_seized"]["sheet"], by_id["marsh_bib_seized"]["actions"])
    fayed = replay(content, by_id["marsh_hook_fayed"]["seed"], by_id["marsh_hook_fayed"]["sheet"], by_id["marsh_hook_fayed"]["actions"])
    lodginged = replay(content, by_id["marsh_lodging_nicked"]["seed"], by_id["marsh_lodging_nicked"]["sheet"], by_id["marsh_lodging_nicked"]["actions"])
    sirmarked = replay(content, by_id["marsh_sirmark_marked"]["seed"], by_id["marsh_sirmark_marked"]["sheet"], by_id["marsh_sirmark_marked"]["actions"])
    wrung = replay(content, by_id["marsh_wring_dumped"]["seed"], by_id["marsh_wring_dumped"]["sheet"], by_id["marsh_wring_dumped"]["actions"])
    sistered = replay(content, by_id["marsh_sister_bolted"]["seed"], by_id["marsh_sister_bolted"]["sheet"], by_id["marsh_sister_bolted"]["actions"])
    crotched = replay(content, by_id["marsh_crotch_spiked"]["seed"], by_id["marsh_crotch_spiked"]["sheet"], by_id["marsh_crotch_spiked"]["actions"])
    compounded = replay(content, by_id["marsh_compound_dumped"]["seed"], by_id["marsh_compound_dumped"]["sheet"], by_id["marsh_compound_dumped"]["actions"])
    stanchioned = replay(content, by_id["marsh_foot_spiked"]["seed"], by_id["marsh_foot_spiked"]["sheet"], by_id["marsh_foot_spiked"]["actions"])
    pillared = replay(content, by_id["marsh_queen_shored"]["seed"], by_id["marsh_queen_shored"]["sheet"], by_id["marsh_queen_shored"]["actions"])
    if "harbor_compact" not in compact.state.outcomes:
        raise AssertionError("harbor_compact predicate failed")
    if "stack_relic" not in relic.state.outcomes:
        raise AssertionError("stack_relic predicate failed")
    if "kiln_pact" not in kiln.state.outcomes:
        raise AssertionError("kiln_pact predicate failed")
    if "reed_sentence" not in court.state.outcomes:
        raise AssertionError("reed_sentence predicate failed")
    if "road_beacon" not in beacon.state.outcomes:
        raise AssertionError("road_beacon predicate failed")
    if "fever_broken" not in fever.state.outcomes:
        raise AssertionError("fever_broken predicate failed")
    if "name_restored" not in named.state.outcomes:
        raise AssertionError("name_restored predicate failed")
    if "fold_held" not in fold.state.outcomes:
        raise AssertionError("fold_held predicate failed")
    if "lens_set" not in lens.state.outcomes:
        raise AssertionError("lens_set predicate failed")
    if "rope_walked" not in rope.state.outcomes:
        raise AssertionError("rope_walked predicate failed")
    if "salt_raked" not in salt.state.outcomes:
        raise AssertionError("salt_raked predicate failed")
    if "smoke_cured" not in smoke.state.outcomes:
        raise AssertionError("smoke_cured predicate failed")
    if "weir_lifted" not in weir.state.outcomes:
        raise AssertionError("weir_lifted predicate failed")
    if "dye_struck" not in dye.state.outcomes:
        raise AssertionError("dye_struck predicate failed")
    if "ferry_crossed" not in ferry.state.outcomes:
        raise AssertionError("ferry_crossed predicate failed")
    if "flats_drained" not in pump.state.outcomes:
        raise AssertionError("flats_drained predicate failed")
    if "oyster_culled" not in oyster.state.outcomes:
        raise AssertionError("oyster_culled predicate failed")
    if "tally_closed" not in tally.state.outcomes:
        raise AssertionError("tally_closed predicate failed")
    if "ice_held" not in ice.state.outcomes:
        raise AssertionError("ice_held predicate failed")
    if "wreck_laid" not in wreck.state.outcomes:
        raise AssertionError("wreck_laid predicate failed")
    if "hive_kept" not in hive.state.outcomes:
        raise AssertionError("hive_kept predicate failed")
    if "mead_drawn" not in mead.state.outcomes:
        raise AssertionError("mead_drawn predicate failed")
    if "barrel_raised" not in barrel.state.outcomes:
        raise AssertionError("barrel_raised predicate failed")
    if "pickle_lidded" not in pickle.state.outcomes:
        raise AssertionError("pickle_lidded predicate failed")
    if "iron_quenched" not in iron.state.outcomes:
        raise AssertionError("iron_quenched predicate failed")
    if "fowl_taken" not in fowl.state.outcomes:
        raise AssertionError("fowl_taken predicate failed")
    if "lights_bound" not in rush.state.outcomes:
        raise AssertionError("lights_bound predicate failed")
    if "seam_caulked" not in caulk.state.outcomes:
        raise AssertionError("seam_caulked predicate failed")
    if "net_tarred" not in netted.state.outcomes:
        raise AssertionError("net_tarred predicate failed")
    if "sail_hoisted" not in hoisted.state.outcomes:
        raise AssertionError("sail_hoisted predicate failed")
    if "lead_cast" not in sounding.state.outcomes:
        raise AssertionError("lead_cast predicate failed")
    if "rutter_sealed" not in rutter.state.outcomes:
        raise AssertionError("rutter_sealed predicate failed")
    if "buoy_set" not in buoy.state.outcomes:
        raise AssertionError("buoy_set predicate failed")
    if "kelp_burned" not in kelp.state.outcomes:
        raise AssertionError("kelp_burned predicate failed")
    if "soap_cut" not in soap.state.outcomes:
        raise AssertionError("soap_cut predicate failed")
    if "cloth_fulled" not in cloth.state.outcomes:
        raise AssertionError("cloth_fulled predicate failed")
    if "coal_drawn" not in coal.state.outcomes:
        raise AssertionError("coal_drawn predicate failed")
    if "lime_slaked" not in lime.state.outcomes:
        raise AssertionError("lime_slaked predicate failed")
    if "joint_pointed" not in pointed.state.outcomes:
        raise AssertionError("joint_pointed predicate failed")
    if "roof_set" not in roof.state.outcomes:
        raise AssertionError("roof_set predicate failed")
    if "cistern_filled" not in filled.state.outcomes:
        raise AssertionError("cistern_filled predicate failed")
    if "wash_hung" not in hung.state.outcomes:
        raise AssertionError("wash_hung predicate failed")
    if "paper_laid" not in laid.state.outcomes:
        raise AssertionError("paper_laid predicate failed")
    if "frail_woven" not in woven.state.outcomes:
        raise AssertionError("frail_woven predicate failed")
    if "loaf_drawn" not in loaf.state.outcomes:
        raise AssertionError("loaf_drawn predicate failed")
    if "wheel_salted" not in salted.state.outcomes:
        raise AssertionError("wheel_salted predicate failed")
    if "web_sheared" not in sheared.state.outcomes:
        raise AssertionError("web_sheared predicate failed")
    if "lantern_hung" not in lantern.state.outcomes:
        raise AssertionError("lantern_hung predicate failed")
    if "nib_cut" not in nibbed.state.outcomes:
        raise AssertionError("nib_cut predicate failed")
    if "heel_pegged" not in pegged.state.outcomes:
        raise AssertionError("heel_pegged predicate failed")
    if "keeve_bunged" not in bunged.state.outcomes:
        raise AssertionError("keeve_bunged predicate failed")
    if "mustard_potted" not in potted.state.outcomes:
        raise AssertionError("mustard_potted predicate failed")
    if "sausage_linked" not in linked.state.outcomes:
        raise AssertionError("sausage_linked predicate failed")
    if "pie_crimped" not in crimped.state.outcomes:
        raise AssertionError("pie_crimped predicate failed")
    if "jam_jarred" not in jarred.state.outcomes:
        raise AssertionError("jam_jarred predicate failed")
    if "crock_glazed" not in glazed.state.outcomes:
        raise AssertionError("crock_glazed predicate failed")
    if "hide_tanned" not in tanned.state.outcomes:
        raise AssertionError("hide_tanned predicate failed")
    if "flax_spun" not in spun.state.outcomes:
        raise AssertionError("flax_spun predicate failed")
    if "nail_pointed" not in nailed.state.outcomes:
        raise AssertionError("nail_pointed predicate failed")
    if "tyre_set" not in tyred.state.outcomes:
        raise AssertionError("tyre_set predicate failed")
    if "malt_oasted" not in oasted.state.outcomes:
        raise AssertionError("malt_oasted predicate failed")
    if "gyle_racked" not in gyled.state.outcomes:
        raise AssertionError("gyle_racked predicate failed")
    if "cruet_corked" not in corked.state.outcomes:
        raise AssertionError("cruet_corked predicate failed")
    if "glue_caked" not in glued.state.outcomes:
        raise AssertionError("glue_caked predicate failed")
    if "book_bound" not in booked.state.outcomes:
        raise AssertionError("book_bound predicate failed")
    if "plate_burnished" not in gilded.state.outcomes:
        raise AssertionError("plate_burnished predicate failed")
    if "collet_closed" not in gemmed.state.outcomes:
        raise AssertionError("collet_closed predicate failed")
    if "pane_camed" not in camed.state.outcomes:
        raise AssertionError("pane_camed predicate failed")
    if "sash_pinned" not in sashed.state.outcomes:
        raise AssertionError("sash_pinned predicate failed")
    if "light_dusted" not in dusted.state.outcomes:
        raise AssertionError("light_dusted predicate failed")
    if "coat_brushed" not in coated.state.outcomes:
        raise AssertionError("coat_brushed predicate failed")
    if "varnish_flowed" not in varnished.state.outcomes:
        raise AssertionError("varnish_flowed predicate failed")
    if "latch_thrown" not in latched.state.outcomes:
        raise AssertionError("latch_thrown predicate failed")
    if "gudgeon_shipped" not in hinged.state.outcomes:
        raise AssertionError("gudgeon_shipped predicate failed")
    if "casement_stayed" not in stayed.state.outcomes:
        raise AssertionError("casement_stayed predicate failed")
    if "stool_seated" not in seated.state.outcomes:
        raise AssertionError("stool_seated predicate failed")
    if "casing_tacked" not in cased.state.outcomes:
        raise AssertionError("casing_tacked predicate failed")
    if "plinth_fixed" not in skirted.state.outcomes:
        raise AssertionError("plinth_fixed predicate failed")
    if "rail_capped" not in dadoed.state.outcomes:
        raise AssertionError("rail_capped predicate failed")
    if "rail_sprung" not in sprung.state.outcomes:
        raise AssertionError("rail_sprung predicate failed")
    if "cornice_floated" not in coved.state.outcomes:
        raise AssertionError("cornice_floated predicate failed")
    if "riser_wedged" not in staired.state.outcomes:
        raise AssertionError("riser_wedged predicate failed")
    if "finial_dowelled" not in newelled.state.outcomes:
        raise AssertionError("finial_dowelled predicate failed")
    if "ramp_wreathed" not in wreathed.state.outcomes:
        raise AssertionError("ramp_wreathed predicate failed")
    if "neck_shouldered" not in balustered.state.outcomes:
        raise AssertionError("neck_shouldered predicate failed")
    if "end_returned" not in trod.state.outcomes:
        raise AssertionError("end_returned predicate failed")
    if "nail_secreted" not in floored.state.outcomes:
        raise AssertionError("nail_secreted predicate failed")
    if "camber_crowned" not in joisted.state.outcomes:
        raise AssertionError("camber_crowned predicate failed")
    if "coat_haired" not in lathed.state.outcomes:
        raise AssertionError("coat_haired predicate failed")
    if "breast_limed" not in chimneyed.state.outcomes:
        raise AssertionError("breast_limed predicate failed")
    if "mantel_pinned" not in mantelled.state.outcomes:
        raise AssertionError("mantel_pinned predicate failed")
    if "cowl_hung" not in flued.state.outcomes:
        raise AssertionError("cowl_hung predicate failed")
    if "back_bedded" not in backed.state.outcomes:
        raise AssertionError("back_bedded predicate failed")
    if "slide_registered" not in grated.state.outcomes:
        raise AssertionError("slide_registered predicate failed")
    if "hack_set" not in bricked.state.outcomes:
        raise AssertionError("hack_set predicate failed")
    if "arris_nicked" not in tiled.state.outcomes:
        raise AssertionError("arris_nicked predicate failed")
    if "slate_lapped" not in slated.state.outcomes:
        raise AssertionError("slate_lapped predicate failed")
    if "flash_dressed" not in flashed.state.outcomes:
        raise AssertionError("flash_dressed predicate failed")
    if "block_stropped" not in stropped.state.outcomes:
        raise AssertionError("block_stropped predicate failed")
    if "grip_bound" not in oared.state.outcomes:
        raise AssertionError("grip_bound predicate failed")
    if "hull_launched" not in launched.state.outcomes:
        raise AssertionError("hull_launched predicate failed")
    if "garboard_faired" not in clinked.state.outcomes:
        raise AssertionError("garboard_faired predicate failed")
    if "round_heaved" not in heaved.state.outcomes:
        raise AssertionError("round_heaved predicate failed")
    if "station_bevelled" not in lofted.state.outcomes:
        raise AssertionError("station_bevelled predicate failed")
    if "trunnel_driven" not in trunnelled.state.outcomes:
        raise AssertionError("trunnel_driven predicate failed")
    if "hog_bolted" not in hogged.state.outcomes:
        raise AssertionError("hog_bolted predicate failed")
    if "partner_hooped" not in masted.state.outcomes:
        raise AssertionError("partner_hooped predicate failed")
    if "knee_hung" not in stemmed.state.outcomes:
        raise AssertionError("knee_hung predicate failed")
    if "eye_seized" not in fidded.state.outcomes:
        raise AssertionError("eye_seized predicate failed")
    if "base_bolted" not in cleated.state.outcomes:
        raise AssertionError("base_bolted predicate failed")
    if "collar_paid" not in hawsed.state.outcomes:
        raise AssertionError("collar_paid predicate failed")
    if "lanyard_seized" not in deadeyed.state.outcomes:
        raise AssertionError("lanyard_seized predicate failed")
    if "parrel_trussed" not in parreled.state.outcomes:
        raise AssertionError("parrel_trussed predicate failed")
    if "cable_belayed" not in belayed.state.outcomes:
        raise AssertionError("cable_belayed predicate failed")
    if "gammon_frapped" not in gammoned.state.outcomes:
        raise AssertionError("gammon_frapped predicate failed")
    if "tiller_yoked" not in tillered.state.outcomes:
        raise AssertionError("tiller_yoked predicate failed")
    if "fluke_fished" not in catheaded.state.outcomes:
        raise AssertionError("fluke_fished predicate failed")
    if "stern_spiked" not in transomed.state.outcomes:
        raise AssertionError("stern_spiked predicate failed")
    if "mouth_plugged" not in scuppered.state.outcomes:
        raise AssertionError("mouth_plugged predicate failed")
    if "card_locked" not in binnacled.state.outcomes:
        raise AssertionError("card_locked predicate failed")
    if "belly_clenched" not in futtocked.state.outcomes:
        raise AssertionError("belly_clenched predicate failed")
    if "bolster_seized" not in crosstreed.state.outcomes:
        raise AssertionError("bolster_seized predicate failed")
    if "waterway_paid" not in waterwayed.state.outcomes:
        raise AssertionError("waterway_paid predicate failed")
    if "coaming_coaked" not in coamed.state.outcomes:
        raise AssertionError("coaming_coaked predicate failed")
    if "bolt_dumped" not in gunwaled.state.outcomes:
        raise AssertionError("bolt_dumped predicate failed")
    if "davit_shipped" not in davited.state.outcomes:
        raise AssertionError("davit_shipped predicate failed")
    if "guy_seized" not in boomkined.state.outcomes:
        raise AssertionError("guy_seized predicate failed")
    if "strap_set" not in channeled.state.outcomes:
        raise AssertionError("strap_set predicate failed")
    if "kevel_clenched" not in keveled.state.outcomes:
        raise AssertionError("kevel_clenched predicate failed")
    if "knight_lashed" not in knighted.state.outcomes:
        raise AssertionError("knight_lashed predicate failed")
    if "carling_spiked" not in carlinged.state.outcomes:
        raise AssertionError("carling_spiked predicate failed")
    if "keeper_pinned" not in tabernacled.state.outcomes:
        raise AssertionError("keeper_pinned predicate failed")
    if "edge_dumped" not in edged.state.outcomes:
        raise AssertionError("edge_dumped predicate failed")
    if "spirket_clenched" not in spirketed.state.outcomes:
        raise AssertionError("spirket_clenched predicate failed")
    if "bib_seized" not in trestled.state.outcomes:
        raise AssertionError("bib_seized predicate failed")
    if "hook_fayed" not in fayed.state.outcomes:
        raise AssertionError("hook_fayed predicate failed")
    if "lodging_nicked" not in lodginged.state.outcomes:
        raise AssertionError("lodging_nicked predicate failed")
    if "sirmark_marked" not in sirmarked.state.outcomes:
        raise AssertionError("sirmark_marked predicate failed")
    if "wring_dumped" not in wrung.state.outcomes:
        raise AssertionError("wring_dumped predicate failed")
    if "sister_bolted" not in sistered.state.outcomes:
        raise AssertionError("sister_bolted predicate failed")
    if "crotch_spiked" not in crotched.state.outcomes:
        raise AssertionError("crotch_spiked predicate failed")
    if "compound_dumped" not in compounded.state.outcomes:
        raise AssertionError("compound_dumped predicate failed")
    if "foot_spiked" not in stanchioned.state.outcomes:
        raise AssertionError("foot_spiked predicate failed")
    if "queen_shored" not in pillared.state.outcomes:
        raise AssertionError("queen_shored predicate failed")
    if len({compact.fingerprint, relic.fingerprint, kiln.fingerprint, court.fingerprint, beacon.fingerprint, fever.fingerprint, named.fingerprint, fold.fingerprint, lens.fingerprint, rope.fingerprint, salt.fingerprint, smoke.fingerprint, weir.fingerprint, dye.fingerprint, ferry.fingerprint, pump.fingerprint, oyster.fingerprint, tally.fingerprint, ice.fingerprint, wreck.fingerprint, hive.fingerprint, mead.fingerprint, barrel.fingerprint, pickle.fingerprint, iron.fingerprint, fowl.fingerprint, rush.fingerprint, caulk.fingerprint, netted.fingerprint, hoisted.fingerprint, sounding.fingerprint, rutter.fingerprint, buoy.fingerprint, kelp.fingerprint, soap.fingerprint, cloth.fingerprint, coal.fingerprint, lime.fingerprint, pointed.fingerprint, roof.fingerprint, filled.fingerprint, hung.fingerprint, laid.fingerprint, woven.fingerprint, loaf.fingerprint, salted.fingerprint, sheared.fingerprint, lantern.fingerprint, nibbed.fingerprint, pegged.fingerprint, bunged.fingerprint, potted.fingerprint, linked.fingerprint, crimped.fingerprint, jarred.fingerprint, glazed.fingerprint, tanned.fingerprint, spun.fingerprint, nailed.fingerprint, tyred.fingerprint, oasted.fingerprint, gyled.fingerprint, corked.fingerprint, glued.fingerprint, booked.fingerprint, gilded.fingerprint, gemmed.fingerprint, camed.fingerprint, sashed.fingerprint, dusted.fingerprint, coated.fingerprint, varnished.fingerprint, latched.fingerprint, hinged.fingerprint, stayed.fingerprint, seated.fingerprint, cased.fingerprint, skirted.fingerprint, dadoed.fingerprint, sprung.fingerprint, coved.fingerprint, staired.fingerprint, newelled.fingerprint, wreathed.fingerprint, balustered.fingerprint, trod.fingerprint, floored.fingerprint, joisted.fingerprint, lathed.fingerprint, chimneyed.fingerprint, mantelled.fingerprint, flued.fingerprint, backed.fingerprint, grated.fingerprint, bricked.fingerprint, tiled.fingerprint, slated.fingerprint, flashed.fingerprint, stropped.fingerprint, oared.fingerprint, launched.fingerprint, clinked.fingerprint, heaved.fingerprint, lofted.fingerprint, trunnelled.fingerprint, hogged.fingerprint, masted.fingerprint, stemmed.fingerprint, fidded.fingerprint, cleated.fingerprint, hawsed.fingerprint, deadeyed.fingerprint, parreled.fingerprint, belayed.fingerprint, gammoned.fingerprint, tillered.fingerprint, catheaded.fingerprint, transomed.fingerprint, scuppered.fingerprint, binnacled.fingerprint, futtocked.fingerprint, crosstreed.fingerprint, waterwayed.fingerprint, coamed.fingerprint, gunwaled.fingerprint, davited.fingerprint, boomkined.fingerprint, channeled.fingerprint, keveled.fingerprint, knighted.fingerprint, carlinged.fingerprint, tabernacled.fingerprint, edged.fingerprint, spirketed.fingerprint, trestled.fingerprint, fayed.fingerprint, lodginged.fingerprint, sirmarked.fingerprint, wrung.fingerprint, sistered.fingerprint, crotched.fingerprint, compounded.fingerprint, stanchioned.fingerprint, pillared.fingerprint}) != 144:
        raise AssertionError("distinct outcomes share a fingerprint")

    marsh = by_id["divergence_marsh_market"]
    city = by_id["divergence_city_market"]
    m_ids, c_ids = _diverge_legal(content, marsh, city)
    if "use_marsh_cant" not in m_ids:
        raise AssertionError("marsh_scout missing use_marsh_cant")
    if "show_city_papers" not in c_ids:
        raise AssertionError("city_oath missing show_city_papers")
    if "use_marsh_cant" in c_ids or "show_city_papers" in m_ids:
        raise AssertionError("sheet verbs leaked across sheets")

    mill_m = by_id["divergence_marsh_mill"]
    mill_c = by_id["divergence_city_mill"]
    mill_m_ids, mill_c_ids = _diverge_legal(content, mill_m, mill_c)
    if "offer_reed_grain" not in mill_m_ids:
        raise AssertionError("marsh_scout missing offer_reed_grain at mill")
    if "read_debt_ledger" not in mill_c_ids:
        raise AssertionError("city_oath missing read_debt_ledger at mill")
    if "offer_reed_grain" in mill_c_ids or "read_debt_ledger" in mill_m_ids:
        raise AssertionError("mill sheet verbs leaked across sheets")

    plain = replay(content, by_id["cross_plain_mill"]["seed"], by_id["cross_plain_mill"]["sheet"], by_id["cross_plain_mill"]["actions"])
    with_compact = replay(content, by_id["cross_compact_mill"]["seed"], by_id["cross_compact_mill"]["sheet"], by_id["cross_compact_mill"]["actions"])
    if plain.state.location != with_compact.state.location:
        raise AssertionError("cross-area pair left different locations")
    if plain.state.location != "mill.yard":
        raise AssertionError("cross-area pair not at mill.yard")
    plain_ids = {a.id for a in enumerate_legal(plain.state, content)}
    compact_ids = {a.id for a in enumerate_legal(with_compact.state, content)}
    if "cite_dock_compact" not in compact_ids:
        raise AssertionError("compact deed did not unlock cite_dock_compact")
    if "cite_dock_compact" in plain_ids:
        raise AssertionError("cite_dock_compact leaked without compact")
    if "harbor_compact" not in with_compact.state.outcomes:
        raise AssertionError("cross compact run lost harbor_compact")

    court_m = by_id["divergence_marsh_court"]
    court_c = by_id["divergence_city_court"]
    court_m_ids, court_c_ids = _diverge_legal(content, court_m, court_c)
    if "speak_reed_custom" not in court_m_ids:
        raise AssertionError("marsh_scout missing speak_reed_custom at court")
    if "cite_city_law" not in court_c_ids:
        raise AssertionError("city_oath missing cite_city_law at court")
    if "speak_reed_custom" in court_c_ids or "cite_city_law" in court_m_ids:
        raise AssertionError("court sheet verbs leaked across sheets")

    plain_court = replay(content, by_id["cross_plain_court"]["seed"], by_id["cross_plain_court"]["sheet"], by_id["cross_plain_court"]["actions"])
    kiln_court = replay(content, by_id["cross_kiln_court"]["seed"], by_id["cross_kiln_court"]["sheet"], by_id["cross_kiln_court"]["actions"])
    if plain_court.state.location != kiln_court.state.location:
        raise AssertionError("court cross-area pair left different locations")
    if plain_court.state.location != "court.hall":
        raise AssertionError("court cross-area pair not at court.hall")
    plain_court_ids = {a.id for a in enumerate_legal(plain_court.state, content)}
    kiln_court_ids = {a.id for a in enumerate_legal(kiln_court.state, content)}
    if "name_mill_pact" not in kiln_court_ids:
        raise AssertionError("kiln pact did not unlock name_mill_pact")
    if "name_mill_pact" in plain_court_ids:
        raise AssertionError("name_mill_pact leaked without kiln pact")
    if "kiln_pact" not in kiln_court.state.outcomes:
        raise AssertionError("cross kiln-court run lost kiln_pact")

    road_m = by_id["divergence_marsh_road"]
    road_c = by_id["divergence_city_road"]
    road_m_ids, road_c_ids = _diverge_legal(content, road_m, road_c)
    if "track_drowned_prints" not in road_m_ids:
        raise AssertionError("marsh_scout missing track_drowned_prints")
    if "force_hut_latch" not in road_c_ids:
        raise AssertionError("city_oath missing force_hut_latch")
    if "track_drowned_prints" in road_c_ids or "force_hut_latch" in road_m_ids:
        raise AssertionError("road sheet verbs leaked across sheets")

    plain_road = replay(content, by_id["cross_plain_road"]["seed"], by_id["cross_plain_road"]["sheet"], by_id["cross_plain_road"]["actions"])
    court_road = replay(content, by_id["cross_court_road"]["seed"], by_id["cross_court_road"]["sheet"], by_id["cross_court_road"]["actions"])
    if plain_road.state.location != court_road.state.location:
        raise AssertionError("road cross-area pair left different locations")
    if plain_road.state.location != "road.hut":
        raise AssertionError("road cross-area pair not at road.hut")
    plain_road_ids = {a.id for a in enumerate_legal(plain_road.state, content)}
    court_road_ids = {a.id for a in enumerate_legal(court_road.state, content)}
    if "name_the_sentence" not in court_road_ids:
        raise AssertionError("reed sentence did not unlock name_the_sentence")
    if "name_the_sentence" in plain_road_ids:
        raise AssertionError("name_the_sentence leaked without reed sentence")
    if "reed_sentence" not in court_road.state.outcomes:
        raise AssertionError("cross court-road run lost reed_sentence")

    camp_m = by_id["divergence_marsh_camp"]
    camp_c = by_id["divergence_city_camp"]
    camp_m_ids, camp_c_ids = _diverge_legal(content, camp_m, camp_c)
    if "cut_reed_herb" not in camp_m_ids:
        raise AssertionError("marsh_scout missing cut_reed_herb")
    if "read_isolation_order" not in camp_c_ids:
        raise AssertionError("city_oath missing read_isolation_order")
    if "cut_reed_herb" in camp_c_ids or "read_isolation_order" in camp_m_ids:
        raise AssertionError("camp sheet verbs leaked across sheets")

    plain_camp = replay(content, by_id["cross_plain_camp"]["seed"], by_id["cross_plain_camp"]["sheet"], by_id["cross_plain_camp"]["actions"])
    beacon_camp = replay(content, by_id["cross_beacon_camp"]["seed"], by_id["cross_beacon_camp"]["sheet"], by_id["cross_beacon_camp"]["actions"])
    if plain_camp.state.location != beacon_camp.state.location:
        raise AssertionError("camp cross-area pair left different locations")
    if plain_camp.state.location != "camp.gate":
        raise AssertionError("camp cross-area pair not at camp.gate")
    plain_camp_ids = {a.id for a in enumerate_legal(plain_camp.state, content)}
    beacon_camp_ids = {a.id for a in enumerate_legal(beacon_camp.state, content)}
    if "hail_clean_boat" not in beacon_camp_ids:
        raise AssertionError("road beacon did not unlock hail_clean_boat")
    if "hail_clean_boat" in plain_camp_ids:
        raise AssertionError("hail_clean_boat leaked without beacon")
    if "road_beacon" not in beacon_camp.state.outcomes:
        raise AssertionError("cross beacon-camp run lost road_beacon")

    name_m = by_id["divergence_marsh_name"]
    name_c = by_id["divergence_city_name"]
    name_m_ids, name_c_ids = _diverge_legal(content, name_m, name_c)
    if "speak_the_old_name" not in name_m_ids:
        raise AssertionError("marsh_scout missing speak_the_old_name")
    if "copy_the_bone_name" not in name_c_ids:
        raise AssertionError("city_oath missing copy_the_bone_name")
    if "speak_the_old_name" in name_c_ids or "copy_the_bone_name" in name_m_ids:
        raise AssertionError("namehouse sheet verbs leaked across sheets")

    plain_name = replay(content, by_id["cross_plain_name"]["seed"], by_id["cross_plain_name"]["sheet"], by_id["cross_plain_name"]["actions"])
    fever_name = replay(content, by_id["cross_fever_name"]["seed"], by_id["cross_fever_name"]["sheet"], by_id["cross_fever_name"]["actions"])
    if plain_name.state.location != fever_name.state.location:
        raise AssertionError("namehouse cross-area pair left different locations")
    if plain_name.state.location != "name.hall":
        raise AssertionError("namehouse cross-area pair not at name.hall")
    plain_name_ids = {a.id for a in enumerate_legal(plain_name.state, content)}
    fever_name_ids = {a.id for a in enumerate_legal(fever_name.state, content)}
    if "file_ren_living" not in fever_name_ids:
        raise AssertionError("fever broken did not unlock file_ren_living")
    if "file_ren_living" in plain_name_ids:
        raise AssertionError("file_ren_living leaked without fever broken")
    if "fever_broken" not in fever_name.state.outcomes:
        raise AssertionError("cross fever-name run lost fever_broken")

    fold_m = by_id["divergence_marsh_fold"]
    fold_c = by_id["divergence_city_fold"]
    fold_m_ids, fold_c_ids = _diverge_legal(content, fold_m, fold_c)
    if "know_the_soft_cut" not in fold_m_ids:
        raise AssertionError("marsh_scout missing know_the_soft_cut")
    if "read_the_share_board" not in fold_c_ids:
        raise AssertionError("city_oath missing read_the_share_board")
    if "know_the_soft_cut" in fold_c_ids or "read_the_share_board" in fold_m_ids:
        raise AssertionError("fold sheet verbs leaked across sheets")

    plain_fold = replay(content, by_id["cross_plain_fold"]["seed"], by_id["cross_plain_fold"]["sheet"], by_id["cross_plain_fold"]["actions"])
    name_fold = replay(content, by_id["cross_name_fold"]["seed"], by_id["cross_name_fold"]["sheet"], by_id["cross_name_fold"]["actions"])
    if plain_fold.state.location != name_fold.state.location:
        raise AssertionError("fold cross-area pair left different locations")
    if plain_fold.state.location != "fold.green":
        raise AssertionError("fold cross-area pair not at fold.green")
    plain_fold_ids = {a.id for a in enumerate_legal(plain_fold.state, content)}
    name_fold_ids = {a.id for a in enumerate_legal(name_fold.state, content)}
    if "cite_the_restored_name" not in name_fold_ids:
        raise AssertionError("name restored did not unlock cite_the_restored_name")
    if "cite_the_restored_name" in plain_fold_ids:
        raise AssertionError("cite_the_restored_name leaked without name restored")
    if "name_restored" not in name_fold.state.outcomes:
        raise AssertionError("cross name-fold run lost name_restored")

    glass_m = by_id["divergence_marsh_glass"]
    glass_c = by_id["divergence_city_glass"]
    glass_m_ids, glass_c_ids = _diverge_legal(content, glass_m, glass_c)
    if "know_the_low_sun" not in glass_m_ids:
        raise AssertionError("marsh_scout missing know_the_low_sun")
    if "read_the_sun_chart" not in glass_c_ids:
        raise AssertionError("city_oath missing read_the_sun_chart")
    if "know_the_low_sun" in glass_c_ids or "read_the_sun_chart" in glass_m_ids:
        raise AssertionError("glass sheet verbs leaked across sheets")

    plain_glass = replay(content, by_id["cross_plain_glass"]["seed"], by_id["cross_plain_glass"]["sheet"], by_id["cross_plain_glass"]["actions"])
    fold_glass = replay(content, by_id["cross_fold_glass"]["seed"], by_id["cross_fold_glass"]["sheet"], by_id["cross_fold_glass"]["actions"])
    if plain_glass.state.location != fold_glass.state.location:
        raise AssertionError("glass cross-area pair left different locations")
    if plain_glass.state.location != "glass.yard":
        raise AssertionError("glass cross-area pair not at glass.yard")
    plain_glass_ids = {a.id for a in enumerate_legal(plain_glass.state, content)}
    fold_glass_ids = {a.id for a in enumerate_legal(fold_glass.state, content)}
    if "trade_peat_for_lead" not in fold_glass_ids:
        raise AssertionError("fold held did not unlock trade_peat_for_lead")
    if "trade_peat_for_lead" in plain_glass_ids:
        raise AssertionError("trade_peat_for_lead leaked without fold held")
    if "fold_held" not in fold_glass.state.outcomes:
        raise AssertionError("cross fold-glass run lost fold_held")

    rope_m = by_id["divergence_marsh_rope"]
    rope_c = by_id["divergence_city_rope"]
    rope_m_ids, rope_c_ids = _diverge_legal(content, rope_m, rope_c)
    if "know_the_hemp_twist" not in rope_m_ids:
        raise AssertionError("marsh_scout missing know_the_hemp_twist")
    if "read_the_walk_mark" not in rope_c_ids:
        raise AssertionError("city_oath missing read_the_walk_mark")
    if "know_the_hemp_twist" in rope_c_ids or "read_the_walk_mark" in rope_m_ids:
        raise AssertionError("rope sheet verbs leaked across sheets")

    plain_rope = replay(content, by_id["cross_plain_rope"]["seed"], by_id["cross_plain_rope"]["sheet"], by_id["cross_plain_rope"]["actions"])
    lens_rope = replay(content, by_id["cross_lens_rope"]["seed"], by_id["cross_lens_rope"]["sheet"], by_id["cross_lens_rope"]["actions"])
    if plain_rope.state.location != lens_rope.state.location:
        raise AssertionError("rope cross-area pair left different locations")
    if plain_rope.state.location != "rope.walk":
        raise AssertionError("rope cross-area pair not at rope.walk")
    plain_rope_ids = {a.id for a in enumerate_legal(plain_rope.state, content)}
    lens_rope_ids = {a.id for a in enumerate_legal(lens_rope.state, content)}
    if "sight_the_channel" not in lens_rope_ids:
        raise AssertionError("lens set did not unlock sight_the_channel")
    if "sight_the_channel" in plain_rope_ids:
        raise AssertionError("sight_the_channel leaked without lens set")
    if "lens_set" not in lens_rope.state.outcomes:
        raise AssertionError("cross lens-rope run lost lens_set")

    salt_m = by_id["divergence_marsh_salt"]
    salt_c = by_id["divergence_city_salt"]
    salt_m_ids, salt_c_ids = _diverge_legal(content, salt_m, salt_c)
    if "know_the_brine_cut" not in salt_m_ids:
        raise AssertionError("marsh_scout missing know_the_brine_cut")
    if "read_the_pan_list" not in salt_c_ids:
        raise AssertionError("city_oath missing read_the_pan_list")
    if "know_the_brine_cut" in salt_c_ids or "read_the_pan_list" in salt_m_ids:
        raise AssertionError("salt sheet verbs leaked across sheets")

    plain_salt = replay(content, by_id["cross_plain_salt"]["seed"], by_id["cross_plain_salt"]["sheet"], by_id["cross_plain_salt"]["actions"])
    rope_salt = replay(content, by_id["cross_rope_salt"]["seed"], by_id["cross_rope_salt"]["sheet"], by_id["cross_rope_salt"]["actions"])
    if plain_salt.state.location != rope_salt.state.location:
        raise AssertionError("salt cross-area pair left different locations")
    if plain_salt.state.location != "pans.beds":
        raise AssertionError("salt cross-area pair not at pans.beds")
    plain_salt_ids = {a.id for a in enumerate_legal(plain_salt.state, content)}
    rope_salt_ids = {a.id for a in enumerate_legal(rope_salt.state, content)}
    if "rig_the_rake_line" not in rope_salt_ids:
        raise AssertionError("rope walked did not unlock rig_the_rake_line")
    if "rig_the_rake_line" in plain_salt_ids:
        raise AssertionError("rig_the_rake_line leaked without rope walked")
    if "rope_walked" not in rope_salt.state.outcomes:
        raise AssertionError("cross rope-salt run lost rope_walked")

    smoke_m = by_id["divergence_marsh_smoke"]
    smoke_c = by_id["divergence_city_smoke"]
    smoke_m_ids, smoke_c_ids = _diverge_legal(content, smoke_m, smoke_c)
    if "know_the_wet_fish" not in smoke_m_ids:
        raise AssertionError("marsh_scout missing know_the_wet_fish")
    if "read_the_cure_mark" not in smoke_c_ids:
        raise AssertionError("city_oath missing read_the_cure_mark")
    if "know_the_wet_fish" in smoke_c_ids or "read_the_cure_mark" in smoke_m_ids:
        raise AssertionError("smoke sheet verbs leaked across sheets")

    plain_smoke = replay(content, by_id["cross_plain_smoke"]["seed"], by_id["cross_plain_smoke"]["sheet"], by_id["cross_plain_smoke"]["actions"])
    salt_smoke = replay(content, by_id["cross_salt_smoke"]["seed"], by_id["cross_salt_smoke"]["sheet"], by_id["cross_salt_smoke"]["actions"])
    if plain_smoke.state.location != salt_smoke.state.location:
        raise AssertionError("smoke cross-area pair left different locations")
    if plain_smoke.state.location != "smoke.racks":
        raise AssertionError("smoke cross-area pair not at smoke.racks")
    plain_smoke_ids = {a.id for a in enumerate_legal(plain_smoke.state, content)}
    salt_smoke_ids = {a.id for a in enumerate_legal(salt_smoke.state, content)}
    if "salt_the_racks" not in salt_smoke_ids:
        raise AssertionError("salt raked did not unlock salt_the_racks")
    if "salt_the_racks" in plain_smoke_ids:
        raise AssertionError("salt_the_racks leaked without salt raked")
    if "salt_raked" not in salt_smoke.state.outcomes:
        raise AssertionError("cross salt-smoke run lost salt_raked")

    weir_m = by_id["divergence_marsh_weir"]
    weir_c = by_id["divergence_city_weir"]
    weir_m_ids, weir_c_ids = _diverge_legal(content, weir_m, weir_c)
    if "know_the_eel_run" not in weir_m_ids:
        raise AssertionError("marsh_scout missing know_the_eel_run")
    if "read_the_weir_right" not in weir_c_ids:
        raise AssertionError("city_oath missing read_the_weir_right")
    if "know_the_eel_run" in weir_c_ids or "read_the_weir_right" in weir_m_ids:
        raise AssertionError("weir sheet verbs leaked across sheets")

    plain_weir = replay(content, by_id["cross_plain_weir"]["seed"], by_id["cross_plain_weir"]["sheet"], by_id["cross_plain_weir"]["actions"])
    smoke_weir = replay(content, by_id["cross_smoke_weir"]["seed"], by_id["cross_smoke_weir"]["sheet"], by_id["cross_smoke_weir"]["actions"])
    if plain_weir.state.location != smoke_weir.state.location:
        raise AssertionError("weir cross-area pair left different locations")
    if plain_weir.state.location != "weir.stakes":
        raise AssertionError("weir cross-area pair not at weir.stakes")
    plain_weir_ids = {a.id for a in enumerate_legal(plain_weir.state, content)}
    smoke_weir_ids = {a.id for a in enumerate_legal(smoke_weir.state, content)}
    if "bait_the_weir" not in smoke_weir_ids:
        raise AssertionError("smoke cured did not unlock bait_the_weir")
    if "bait_the_weir" in plain_weir_ids:
        raise AssertionError("bait_the_weir leaked without smoke cured")
    if "smoke_cured" not in smoke_weir.state.outcomes:
        raise AssertionError("cross smoke-weir run lost smoke_cured")

    dye_m = by_id["divergence_marsh_dye"]
    dye_c = by_id["divergence_city_dye"]
    dye_m_ids, dye_c_ids = _diverge_legal(content, dye_m, dye_c)
    if "know_the_reed_mordant" not in dye_m_ids:
        raise AssertionError("marsh_scout missing know_the_reed_mordant")
    if "read_the_vat_list" not in dye_c_ids:
        raise AssertionError("city_oath missing read_the_vat_list")
    if "know_the_reed_mordant" in dye_c_ids or "read_the_vat_list" in dye_m_ids:
        raise AssertionError("dye sheet verbs leaked across sheets")

    plain_dye = replay(content, by_id["cross_plain_dye"]["seed"], by_id["cross_plain_dye"]["sheet"], by_id["cross_plain_dye"]["actions"])
    weir_dye = replay(content, by_id["cross_weir_dye"]["seed"], by_id["cross_weir_dye"]["sheet"], by_id["cross_weir_dye"]["actions"])
    if plain_dye.state.location != weir_dye.state.location:
        raise AssertionError("dye cross-area pair left different locations")
    if plain_dye.state.location != "dye.vats":
        raise AssertionError("dye cross-area pair not at dye.vats")
    plain_dye_ids = {a.id for a in enumerate_legal(plain_dye.state, content)}
    weir_dye_ids = {a.id for a in enumerate_legal(weir_dye.state, content)}
    if "bind_eel_skin" not in weir_dye_ids:
        raise AssertionError("weir lifted did not unlock bind_eel_skin")
    if "bind_eel_skin" in plain_dye_ids:
        raise AssertionError("bind_eel_skin leaked without weir lifted")
    if "weir_lifted" not in weir_dye.state.outcomes:
        raise AssertionError("cross weir-dye run lost weir_lifted")

    ferry_m = by_id["divergence_marsh_ferry"]
    ferry_c = by_id["divergence_city_ferry"]
    ferry_m_ids, ferry_c_ids = _diverge_legal(content, ferry_m, ferry_c)
    if "know_the_channel_cut" not in ferry_m_ids:
        raise AssertionError("marsh_scout missing know_the_channel_cut")
    if "read_the_toll_board" not in ferry_c_ids:
        raise AssertionError("city_oath missing read_the_toll_board")
    if "know_the_channel_cut" in ferry_c_ids or "read_the_toll_board" in ferry_m_ids:
        raise AssertionError("ferry sheet verbs leaked across sheets")

    plain_ferry = replay(content, by_id["cross_plain_ferry"]["seed"], by_id["cross_plain_ferry"]["sheet"], by_id["cross_plain_ferry"]["actions"])
    dye_ferry = replay(content, by_id["cross_dye_ferry"]["seed"], by_id["cross_dye_ferry"]["sheet"], by_id["cross_dye_ferry"]["actions"])
    if plain_ferry.state.location != dye_ferry.state.location:
        raise AssertionError("ferry cross-area pair left different locations")
    if plain_ferry.state.location != "ferry.yard":
        raise AssertionError("ferry cross-area pair not at ferry.yard")
    plain_ferry_ids = {a.id for a in enumerate_legal(plain_ferry.state, content)}
    dye_ferry_ids = {a.id for a in enumerate_legal(dye_ferry.state, content)}
    if "show_the_dyed_fare" not in dye_ferry_ids:
        raise AssertionError("dye struck did not unlock show_the_dyed_fare")
    if "show_the_dyed_fare" in plain_ferry_ids:
        raise AssertionError("show_the_dyed_fare leaked without dye struck")
    if "dye_struck" not in dye_ferry.state.outcomes:
        raise AssertionError("cross dye-ferry run lost dye_struck")

    pump_m = by_id["divergence_marsh_pump"]
    pump_c = by_id["divergence_city_pump"]
    pump_m_ids, pump_c_ids = _diverge_legal(content, pump_m, pump_c)
    if "know_the_wind_cut" not in pump_m_ids:
        raise AssertionError("marsh_scout missing know_the_wind_cut")
    if "read_the_pump_mark" not in pump_c_ids:
        raise AssertionError("city_oath missing read_the_pump_mark")
    if "know_the_wind_cut" in pump_c_ids or "read_the_pump_mark" in pump_m_ids:
        raise AssertionError("pump sheet verbs leaked across sheets")

    plain_pump = replay(content, by_id["cross_plain_pump"]["seed"], by_id["cross_plain_pump"]["sheet"], by_id["cross_plain_pump"]["actions"])
    ferry_pump = replay(content, by_id["cross_ferry_pump"]["seed"], by_id["cross_ferry_pump"]["sheet"], by_id["cross_ferry_pump"]["actions"])
    if plain_pump.state.location != ferry_pump.state.location:
        raise AssertionError("pump cross-area pair left different locations")
    if plain_pump.state.location != "pump.tower":
        raise AssertionError("pump cross-area pair not at pump.tower")
    plain_pump_ids = {a.id for a in enumerate_legal(plain_pump.state, content)}
    ferry_pump_ids = {a.id for a in enumerate_legal(ferry_pump.state, content)}
    if "brace_the_sail" not in ferry_pump_ids:
        raise AssertionError("ferry crossed did not unlock brace_the_sail")
    if "brace_the_sail" in plain_pump_ids:
        raise AssertionError("brace_the_sail leaked without ferry crossed")
    if "ferry_crossed" not in ferry_pump.state.outcomes:
        raise AssertionError("cross ferry-pump run lost ferry_crossed")

    oyster_m = by_id["divergence_marsh_oyster"]
    oyster_c = by_id["divergence_city_oyster"]
    oyster_m_ids, oyster_c_ids = _diverge_legal(content, oyster_m, oyster_c)
    if "know_the_spat_set" not in oyster_m_ids:
        raise AssertionError("marsh_scout missing know_the_spat_set")
    if "read_the_bed_list" not in oyster_c_ids:
        raise AssertionError("city_oath missing read_the_bed_list")
    if "know_the_spat_set" in oyster_c_ids or "read_the_bed_list" in oyster_m_ids:
        raise AssertionError("oyster sheet verbs leaked across sheets")

    plain_oyster = replay(content, by_id["cross_plain_oyster"]["seed"], by_id["cross_plain_oyster"]["sheet"], by_id["cross_plain_oyster"]["actions"])
    pump_oyster = replay(content, by_id["cross_pump_oyster"]["seed"], by_id["cross_pump_oyster"]["sheet"], by_id["cross_pump_oyster"]["actions"])
    if plain_oyster.state.location != pump_oyster.state.location:
        raise AssertionError("oyster cross-area pair left different locations")
    if plain_oyster.state.location != "oyster.beds":
        raise AssertionError("oyster cross-area pair not at oyster.beds")
    plain_oyster_ids = {a.id for a in enumerate_legal(plain_oyster.state, content)}
    pump_oyster_ids = {a.id for a in enumerate_legal(pump_oyster.state, content)}
    if "work_the_dry_beds" not in pump_oyster_ids:
        raise AssertionError("flats drained did not unlock work_the_dry_beds")
    if "work_the_dry_beds" in plain_oyster_ids:
        raise AssertionError("work_the_dry_beds leaked without flats drained")
    if "flats_drained" not in pump_oyster.state.outcomes:
        raise AssertionError("cross pump-oyster run lost flats_drained")

    count_m = by_id["divergence_marsh_count"]
    count_c = by_id["divergence_city_count"]
    count_m_ids, count_c_ids = _diverge_legal(content, count_m, count_c)
    if "know_the_shell_count" not in count_m_ids:
        raise AssertionError("marsh_scout missing know_the_shell_count")
    if "read_the_tally_roll" not in count_c_ids:
        raise AssertionError("city_oath missing read_the_tally_roll")
    if "know_the_shell_count" in count_c_ids or "read_the_tally_roll" in count_m_ids:
        raise AssertionError("count sheet verbs leaked across sheets")

    plain_count = replay(content, by_id["cross_plain_count"]["seed"], by_id["cross_plain_count"]["sheet"], by_id["cross_plain_count"]["actions"])
    oyster_count = replay(content, by_id["cross_oyster_count"]["seed"], by_id["cross_oyster_count"]["sheet"], by_id["cross_oyster_count"]["actions"])
    if plain_count.state.location != oyster_count.state.location:
        raise AssertionError("count cross-area pair left different locations")
    if plain_count.state.location != "count.desk":
        raise AssertionError("count cross-area pair not at count.desk")
    plain_count_ids = {a.id for a in enumerate_legal(plain_count.state, content)}
    oyster_count_ids = {a.id for a in enumerate_legal(oyster_count.state, content)}
    if "lay_the_oyster_lot" not in oyster_count_ids:
        raise AssertionError("oyster culled did not unlock lay_the_oyster_lot")
    if "lay_the_oyster_lot" in plain_count_ids:
        raise AssertionError("lay_the_oyster_lot leaked without oyster culled")
    if "oyster_culled" not in oyster_count.state.outcomes:
        raise AssertionError("cross oyster-count run lost oyster_culled")

    ice_m = by_id["divergence_marsh_ice"]
    ice_c = by_id["divergence_city_ice"]
    ice_m_ids, ice_c_ids = _diverge_legal(content, ice_m, ice_c)
    if "know_the_ice_cut" not in ice_m_ids:
        raise AssertionError("marsh_scout missing know_the_ice_cut")
    if "read_the_cold_mark" not in ice_c_ids:
        raise AssertionError("city_oath missing read_the_cold_mark")
    if "know_the_ice_cut" in ice_c_ids or "read_the_cold_mark" in ice_m_ids:
        raise AssertionError("ice sheet verbs leaked across sheets")

    plain_ice = replay(content, by_id["cross_plain_ice"]["seed"], by_id["cross_plain_ice"]["sheet"], by_id["cross_plain_ice"]["actions"])
    count_ice = replay(content, by_id["cross_count_ice"]["seed"], by_id["cross_count_ice"]["sheet"], by_id["cross_count_ice"]["actions"])
    if plain_ice.state.location != count_ice.state.location:
        raise AssertionError("ice cross-area pair left different locations")
    if plain_ice.state.location != "ice.yard":
        raise AssertionError("ice cross-area pair not at ice.yard")
    plain_ice_ids = {a.id for a in enumerate_legal(plain_ice.state, content)}
    count_ice_ids = {a.id for a in enumerate_legal(count_ice.state, content)}
    if "cite_the_ice_right" not in count_ice_ids:
        raise AssertionError("tally closed did not unlock cite_the_ice_right")
    if "cite_the_ice_right" in plain_ice_ids:
        raise AssertionError("cite_the_ice_right leaked without tally closed")
    if "tally_closed" not in count_ice.state.outcomes:
        raise AssertionError("cross count-ice run lost tally_closed")

    wreck_m = by_id["divergence_marsh_wreck"]
    wreck_c = by_id["divergence_city_wreck"]
    wreck_m_ids, wreck_c_ids = _diverge_legal(content, wreck_m, wreck_c)
    if "know_the_drowned_mark" not in wreck_m_ids:
        raise AssertionError("marsh_scout missing know_the_drowned_mark")
    if "read_the_wreck_list" not in wreck_c_ids:
        raise AssertionError("city_oath missing read_the_wreck_list")
    if "know_the_drowned_mark" in wreck_c_ids or "read_the_wreck_list" in wreck_m_ids:
        raise AssertionError("wreck sheet verbs leaked across sheets")

    plain_wreck = replay(content, by_id["cross_plain_wreck"]["seed"], by_id["cross_plain_wreck"]["sheet"], by_id["cross_plain_wreck"]["actions"])
    ice_wreck = replay(content, by_id["cross_ice_wreck"]["seed"], by_id["cross_ice_wreck"]["sheet"], by_id["cross_ice_wreck"]["actions"])
    if plain_wreck.state.location != ice_wreck.state.location:
        raise AssertionError("wreck cross-area pair left different locations")
    if plain_wreck.state.location != "wreck.hull":
        raise AssertionError("wreck cross-area pair not at wreck.hull")
    plain_wreck_ids = {a.id for a in enumerate_legal(plain_wreck.state, content)}
    ice_wreck_ids = {a.id for a in enumerate_legal(ice_wreck.state, content)}
    if "keep_the_drowned_cold" not in ice_wreck_ids:
        raise AssertionError("ice held did not unlock keep_the_drowned_cold")
    if "keep_the_drowned_cold" in plain_wreck_ids:
        raise AssertionError("keep_the_drowned_cold leaked without ice held")
    if "ice_held" not in ice_wreck.state.outcomes:
        raise AssertionError("cross ice-wreck run lost ice_held")

    hive_m = by_id["divergence_marsh_hive"]
    hive_c = by_id["divergence_city_hive"]
    hive_m_ids, hive_c_ids = _diverge_legal(content, hive_m, hive_c)
    if "know_the_hive_hum" not in hive_m_ids:
        raise AssertionError("marsh_scout missing know_the_hive_hum")
    if "read_the_skep_mark" not in hive_c_ids:
        raise AssertionError("city_oath missing read_the_skep_mark")
    if "know_the_hive_hum" in hive_c_ids or "read_the_skep_mark" in hive_m_ids:
        raise AssertionError("hive sheet verbs leaked across sheets")

    plain_hive = replay(content, by_id["cross_plain_hive"]["seed"], by_id["cross_plain_hive"]["sheet"], by_id["cross_plain_hive"]["actions"])
    wreck_hive = replay(content, by_id["cross_wreck_hive"]["seed"], by_id["cross_wreck_hive"]["sheet"], by_id["cross_wreck_hive"]["actions"])
    if plain_hive.state.location != wreck_hive.state.location:
        raise AssertionError("hive cross-area pair left different locations")
    if plain_hive.state.location != "hive.skeps":
        raise AssertionError("hive cross-area pair not at hive.skeps")
    plain_hive_ids = {a.id for a in enumerate_legal(plain_hive.state, content)}
    wreck_hive_ids = {a.id for a in enumerate_legal(wreck_hive.state, content)}
    if "bless_the_skep" not in wreck_hive_ids:
        raise AssertionError("wreck laid did not unlock bless_the_skep")
    if "bless_the_skep" in plain_hive_ids:
        raise AssertionError("bless_the_skep leaked without wreck laid")
    if "wreck_laid" not in wreck_hive.state.outcomes:
        raise AssertionError("cross wreck-hive run lost wreck_laid")

    mead_m = by_id["divergence_marsh_mead"]
    mead_c = by_id["divergence_city_mead"]
    mead_m_ids, mead_c_ids = _diverge_legal(content, mead_m, mead_c)
    if "know_the_wild_must" not in mead_m_ids:
        raise AssertionError("marsh_scout missing know_the_wild_must")
    if "read_the_cask_mark" not in mead_c_ids:
        raise AssertionError("city_oath missing read_the_cask_mark")
    if "know_the_wild_must" in mead_c_ids or "read_the_cask_mark" in mead_m_ids:
        raise AssertionError("mead sheet verbs leaked across sheets")

    plain_mead = replay(content, by_id["cross_plain_mead"]["seed"], by_id["cross_plain_mead"]["sheet"], by_id["cross_plain_mead"]["actions"])
    hive_mead = replay(content, by_id["cross_hive_mead"]["seed"], by_id["cross_hive_mead"]["sheet"], by_id["cross_hive_mead"]["actions"])
    if plain_mead.state.location != hive_mead.state.location:
        raise AssertionError("mead cross-area pair left different locations")
    if plain_mead.state.location != "mead.mash":
        raise AssertionError("mead cross-area pair not at mead.mash")
    plain_mead_ids = {a.id for a in enumerate_legal(plain_mead.state, content)}
    hive_mead_ids = {a.id for a in enumerate_legal(hive_mead.state, content)}
    if "pitch_true_comb" not in hive_mead_ids:
        raise AssertionError("hive kept did not unlock pitch_true_comb")
    if "pitch_true_comb" in plain_mead_ids:
        raise AssertionError("pitch_true_comb leaked without hive kept")
    if "hive_kept" not in hive_mead.state.outcomes:
        raise AssertionError("cross hive-mead run lost hive_kept")

    coop_m = by_id["divergence_marsh_coop"]
    coop_c = by_id["divergence_city_coop"]
    coop_m_ids, coop_c_ids = _diverge_legal(content, coop_m, coop_c)
    if "know_the_stave_soak" not in coop_m_ids:
        raise AssertionError("marsh_scout missing know_the_stave_soak")
    if "read_the_hoop_mark" not in coop_c_ids:
        raise AssertionError("city_oath missing read_the_hoop_mark")
    if "know_the_stave_soak" in coop_c_ids or "read_the_hoop_mark" in coop_m_ids:
        raise AssertionError("coop sheet verbs leaked across sheets")

    plain_coop = replay(content, by_id["cross_plain_coop"]["seed"], by_id["cross_plain_coop"]["sheet"], by_id["cross_plain_coop"]["actions"])
    mead_coop = replay(content, by_id["cross_mead_coop"]["seed"], by_id["cross_mead_coop"]["sheet"], by_id["cross_mead_coop"]["actions"])
    if plain_coop.state.location != mead_coop.state.location:
        raise AssertionError("coop cross-area pair left different locations")
    if plain_coop.state.location != "coop.hoop":
        raise AssertionError("coop cross-area pair not at coop.hoop")
    plain_coop_ids = {a.id for a in enumerate_legal(plain_coop.state, content)}
    mead_coop_ids = {a.id for a in enumerate_legal(mead_coop.state, content)}
    if "mark_the_mead_cask" not in mead_coop_ids:
        raise AssertionError("mead drawn did not unlock mark_the_mead_cask")
    if "mark_the_mead_cask" in plain_coop_ids:
        raise AssertionError("mark_the_mead_cask leaked without mead drawn")
    if "mead_drawn" not in mead_coop.state.outcomes:
        raise AssertionError("cross mead-coop run lost mead_drawn")

    pickle_m = by_id["divergence_marsh_pickle"]
    pickle_c = by_id["divergence_city_pickle"]
    pickle_m_ids, pickle_c_ids = _diverge_legal(content, pickle_m, pickle_c)
    if "know_the_pickle_cut" not in pickle_m_ids:
        raise AssertionError("marsh_scout missing know_the_pickle_cut")
    if "read_the_pickle_list" not in pickle_c_ids:
        raise AssertionError("city_oath missing read_the_pickle_list")
    if "know_the_pickle_cut" in pickle_c_ids or "read_the_pickle_list" in pickle_m_ids:
        raise AssertionError("pickle sheet verbs leaked across sheets")

    plain_pickle = replay(content, by_id["cross_plain_pickle"]["seed"], by_id["cross_plain_pickle"]["sheet"], by_id["cross_plain_pickle"]["actions"])
    coop_pickle = replay(content, by_id["cross_coop_pickle"]["seed"], by_id["cross_coop_pickle"]["sheet"], by_id["cross_coop_pickle"]["actions"])
    if plain_pickle.state.location != coop_pickle.state.location:
        raise AssertionError("pickle cross-area pair left different locations")
    if plain_pickle.state.location != "pickle.lid":
        raise AssertionError("pickle cross-area pair not at pickle.lid")
    plain_pickle_ids = {a.id for a in enumerate_legal(plain_pickle.state, content)}
    coop_pickle_ids = {a.id for a in enumerate_legal(coop_pickle.state, content)}
    if "hoop_the_pickle" not in coop_pickle_ids:
        raise AssertionError("barrel raised did not unlock hoop_the_pickle")
    if "hoop_the_pickle" in plain_pickle_ids:
        raise AssertionError("hoop_the_pickle leaked without barrel raised")
    if "barrel_raised" not in coop_pickle.state.outcomes:
        raise AssertionError("cross coop-pickle run lost barrel_raised")

    forge_m = by_id["divergence_marsh_forge"]
    forge_c = by_id["divergence_city_forge"]
    forge_m_ids, forge_c_ids = _diverge_legal(content, forge_m, forge_c)
    if "know_the_bog_iron" not in forge_m_ids:
        raise AssertionError("marsh_scout missing know_the_bog_iron")
    if "read_the_forge_list" not in forge_c_ids:
        raise AssertionError("city_oath missing read_the_forge_list")
    if "know_the_bog_iron" in forge_c_ids or "read_the_forge_list" in forge_m_ids:
        raise AssertionError("forge sheet verbs leaked across sheets")

    plain_forge = replay(content, by_id["cross_plain_forge"]["seed"], by_id["cross_plain_forge"]["sheet"], by_id["cross_plain_forge"]["actions"])
    pickle_forge = replay(content, by_id["cross_pickle_forge"]["seed"], by_id["cross_pickle_forge"]["sheet"], by_id["cross_pickle_forge"]["actions"])
    if plain_forge.state.location != pickle_forge.state.location:
        raise AssertionError("forge cross-area pair left different locations")
    if plain_forge.state.location != "forge.trough":
        raise AssertionError("forge cross-area pair not at forge.trough")
    plain_forge_ids = {a.id for a in enumerate_legal(plain_forge.state, content)}
    pickle_forge_ids = {a.id for a in enumerate_legal(pickle_forge.state, content)}
    if "brine_the_quench" not in pickle_forge_ids:
        raise AssertionError("pickle lidded did not unlock brine_the_quench")
    if "brine_the_quench" in plain_forge_ids:
        raise AssertionError("brine_the_quench leaked without pickle lidded")
    if "pickle_lidded" not in pickle_forge.state.outcomes:
        raise AssertionError("cross pickle-forge run lost pickle_lidded")

    decoy_m = by_id["divergence_marsh_decoy"]
    decoy_c = by_id["divergence_city_decoy"]
    decoy_m_ids, decoy_c_ids = _diverge_legal(content, decoy_m, decoy_c)
    if "know_the_decoy_run" not in decoy_m_ids:
        raise AssertionError("marsh_scout missing know_the_decoy_run")
    if "read_the_decoy_list" not in decoy_c_ids:
        raise AssertionError("city_oath missing read_the_decoy_list")
    if "know_the_decoy_run" in decoy_c_ids or "read_the_decoy_list" in decoy_m_ids:
        raise AssertionError("decoy sheet verbs leaked across sheets")

    plain_decoy = replay(content, by_id["cross_plain_decoy"]["seed"], by_id["cross_plain_decoy"]["sheet"], by_id["cross_plain_decoy"]["actions"])
    forge_decoy = replay(content, by_id["cross_forge_decoy"]["seed"], by_id["cross_forge_decoy"]["sheet"], by_id["cross_forge_decoy"]["actions"])
    if plain_decoy.state.location != forge_decoy.state.location:
        raise AssertionError("decoy cross-area pair left different locations")
    if plain_decoy.state.location != "decoy.tunnel":
        raise AssertionError("decoy cross-area pair not at decoy.tunnel")
    plain_decoy_ids = {a.id for a in enumerate_legal(plain_decoy.state, content)}
    forge_decoy_ids = {a.id for a in enumerate_legal(forge_decoy.state, content)}
    if "hook_the_take" not in forge_decoy_ids:
        raise AssertionError("iron quenched did not unlock hook_the_take")
    if "hook_the_take" in plain_decoy_ids:
        raise AssertionError("hook_the_take leaked without iron quenched")
    if "iron_quenched" not in forge_decoy.state.outcomes:
        raise AssertionError("cross forge-decoy run lost iron_quenched")

    rush_m = by_id["divergence_marsh_rush"]
    rush_c = by_id["divergence_city_rush"]
    rush_m_ids, rush_c_ids = _diverge_legal(content, rush_m, rush_c)
    if "know_the_rush_peel" not in rush_m_ids:
        raise AssertionError("marsh_scout missing know_the_rush_peel")
    if "read_the_rush_list" not in rush_c_ids:
        raise AssertionError("city_oath missing read_the_rush_list")
    if "know_the_rush_peel" in rush_c_ids or "read_the_rush_list" in rush_m_ids:
        raise AssertionError("rush sheet verbs leaked across sheets")

    plain_rush = replay(content, by_id["cross_plain_rush"]["seed"], by_id["cross_plain_rush"]["sheet"], by_id["cross_plain_rush"]["actions"])
    decoy_rush = replay(content, by_id["cross_decoy_rush"]["seed"], by_id["cross_decoy_rush"]["sheet"], by_id["cross_decoy_rush"]["actions"])
    if plain_rush.state.location != decoy_rush.state.location:
        raise AssertionError("rush cross-area pair left different locations")
    if plain_rush.state.location != "rush.bind":
        raise AssertionError("rush cross-area pair not at rush.bind")
    plain_rush_ids = {a.id for a in enumerate_legal(plain_rush.state, content)}
    decoy_rush_ids = {a.id for a in enumerate_legal(decoy_rush.state, content)}
    if "tallow_the_rush" not in decoy_rush_ids:
        raise AssertionError("fowl taken did not unlock tallow_the_rush")
    if "tallow_the_rush" in plain_rush_ids:
        raise AssertionError("tallow_the_rush leaked without fowl taken")
    if "fowl_taken" not in decoy_rush.state.outcomes:
        raise AssertionError("cross decoy-rush run lost fowl_taken")

    caulk_m = by_id["divergence_marsh_caulk"]
    caulk_c = by_id["divergence_city_caulk"]
    caulk_m_ids, caulk_c_ids = _diverge_legal(content, caulk_m, caulk_c)
    if "know_the_oakum_tease" not in caulk_m_ids:
        raise AssertionError("marsh_scout missing know_the_oakum_tease")
    if "read_the_caulk_list" not in caulk_c_ids:
        raise AssertionError("city_oath missing read_the_caulk_list")
    if "know_the_oakum_tease" in caulk_c_ids or "read_the_caulk_list" in caulk_m_ids:
        raise AssertionError("caulk sheet verbs leaked across sheets")

    plain_caulk = replay(content, by_id["cross_plain_caulk"]["seed"], by_id["cross_plain_caulk"]["sheet"], by_id["cross_plain_caulk"]["actions"])
    rush_caulk = replay(content, by_id["cross_rush_caulk"]["seed"], by_id["cross_rush_caulk"]["sheet"], by_id["cross_rush_caulk"]["actions"])
    if plain_caulk.state.location != rush_caulk.state.location:
        raise AssertionError("caulk cross-area pair left different locations")
    if plain_caulk.state.location != "caulk.seam":
        raise AssertionError("caulk cross-area pair not at caulk.seam")
    plain_caulk_ids = {a.id for a in enumerate_legal(plain_caulk.state, content)}
    rush_caulk_ids = {a.id for a in enumerate_legal(rush_caulk.state, content)}
    if "light_the_seam" not in rush_caulk_ids:
        raise AssertionError("lights bound did not unlock light_the_seam")
    if "light_the_seam" in plain_caulk_ids:
        raise AssertionError("light_the_seam leaked without lights bound")
    if "lights_bound" not in rush_caulk.state.outcomes:
        raise AssertionError("cross rush-caulk run lost lights_bound")

    net_m = by_id["divergence_marsh_net"]
    net_c = by_id["divergence_city_net"]
    net_m_ids, net_c_ids = _diverge_legal(content, net_m, net_c)
    if "know_the_mesh_hang" not in net_m_ids:
        raise AssertionError("marsh_scout missing know_the_mesh_hang")
    if "read_the_net_list" not in net_c_ids:
        raise AssertionError("city_oath missing read_the_net_list")
    if "know_the_mesh_hang" in net_c_ids or "read_the_net_list" in net_m_ids:
        raise AssertionError("net sheet verbs leaked across sheets")

    plain_net = replay(content, by_id["cross_plain_net"]["seed"], by_id["cross_plain_net"]["sheet"], by_id["cross_plain_net"]["actions"])
    caulk_net = replay(content, by_id["cross_caulk_net"]["seed"], by_id["cross_caulk_net"]["sheet"], by_id["cross_caulk_net"]["actions"])
    if plain_net.state.location != caulk_net.state.location:
        raise AssertionError("net cross-area pair left different locations")
    if plain_net.state.location != "net.tar":
        raise AssertionError("net cross-area pair not at net.tar")
    plain_net_ids = {a.id for a in enumerate_legal(plain_net.state, content)}
    caulk_net_ids = {a.id for a in enumerate_legal(caulk_net.state, content)}
    if "pitch_the_net" not in caulk_net_ids:
        raise AssertionError("seam caulked did not unlock pitch_the_net")
    if "pitch_the_net" in plain_net_ids:
        raise AssertionError("pitch_the_net leaked without seam caulked")
    if "seam_caulked" not in caulk_net.state.outcomes:
        raise AssertionError("cross caulk-net run lost seam_caulked")

    sail_m = by_id["divergence_marsh_sail"]
    sail_c = by_id["divergence_city_sail"]
    sail_m_ids, sail_c_ids = _diverge_legal(content, sail_m, sail_c)
    if "know_the_canvas_cut" not in sail_m_ids:
        raise AssertionError("marsh_scout missing know_the_canvas_cut")
    if "read_the_sail_list" not in sail_c_ids:
        raise AssertionError("city_oath missing read_the_sail_list")
    if "know_the_canvas_cut" in sail_c_ids or "read_the_sail_list" in sail_m_ids:
        raise AssertionError("sail sheet verbs leaked across sheets")

    plain_sail = replay(content, by_id["cross_plain_sail"]["seed"], by_id["cross_plain_sail"]["sheet"], by_id["cross_plain_sail"]["actions"])
    net_sail = replay(content, by_id["cross_net_sail"]["seed"], by_id["cross_net_sail"]["sheet"], by_id["cross_net_sail"]["actions"])
    if plain_sail.state.location != net_sail.state.location:
        raise AssertionError("sail cross-area pair left different locations")
    if plain_sail.state.location != "sail.hoist":
        raise AssertionError("sail cross-area pair not at sail.hoist")
    plain_sail_ids = {a.id for a in enumerate_legal(plain_sail.state, content)}
    net_sail_ids = {a.id for a in enumerate_legal(net_sail.state, content)}
    if "tar_the_twine" not in net_sail_ids:
        raise AssertionError("net tarred did not unlock tar_the_twine")
    if "tar_the_twine" in plain_sail_ids:
        raise AssertionError("tar_the_twine leaked without net tarred")
    if "net_tarred" not in net_sail.state.outcomes:
        raise AssertionError("cross net-sail run lost net_tarred")

    lead_m = by_id["divergence_marsh_lead"]
    lead_c = by_id["divergence_city_lead"]
    lead_m_ids, lead_c_ids = _diverge_legal(content, lead_m, lead_c)
    if "know_the_fathom_mark" not in lead_m_ids:
        raise AssertionError("marsh_scout missing know_the_fathom_mark")
    if "read_the_lead_list" not in lead_c_ids:
        raise AssertionError("city_oath missing read_the_lead_list")
    if "know_the_fathom_mark" in lead_c_ids or "read_the_lead_list" in lead_m_ids:
        raise AssertionError("lead sheet verbs leaked across sheets")

    plain_lead = replay(content, by_id["cross_plain_lead"]["seed"], by_id["cross_plain_lead"]["sheet"], by_id["cross_plain_lead"]["actions"])
    sail_lead = replay(content, by_id["cross_sail_lead"]["seed"], by_id["cross_sail_lead"]["sheet"], by_id["cross_sail_lead"]["actions"])
    if plain_lead.state.location != sail_lead.state.location:
        raise AssertionError("lead cross-area pair left different locations")
    if plain_lead.state.location != "lead.cast":
        raise AssertionError("lead cross-area pair not at lead.cast")
    plain_lead_ids = {a.id for a in enumerate_legal(plain_lead.state, content)}
    sail_lead_ids = {a.id for a in enumerate_legal(sail_lead.state, content)}
    if "sound_under_sail" not in sail_lead_ids:
        raise AssertionError("sail hoisted did not unlock sound_under_sail")
    if "sound_under_sail" in plain_lead_ids:
        raise AssertionError("sound_under_sail leaked without sail hoisted")
    if "sail_hoisted" not in sail_lead.state.outcomes:
        raise AssertionError("cross sail-lead run lost sail_hoisted")

    chart_m = by_id["divergence_marsh_chart"]
    chart_c = by_id["divergence_city_chart"]
    chart_m_ids, chart_c_ids = _diverge_legal(content, chart_m, chart_c)
    if "know_the_coast_hand" not in chart_m_ids:
        raise AssertionError("marsh_scout missing know_the_coast_hand")
    if "read_the_rutter_list" not in chart_c_ids:
        raise AssertionError("city_oath missing read_the_rutter_list")
    if "know_the_coast_hand" in chart_c_ids or "read_the_rutter_list" in chart_m_ids:
        raise AssertionError("chart sheet verbs leaked across sheets")

    plain_chart = replay(content, by_id["cross_plain_chart"]["seed"], by_id["cross_plain_chart"]["sheet"], by_id["cross_plain_chart"]["actions"])
    lead_chart = replay(content, by_id["cross_lead_chart"]["seed"], by_id["cross_lead_chart"]["sheet"], by_id["cross_lead_chart"]["actions"])
    if plain_chart.state.location != lead_chart.state.location:
        raise AssertionError("chart cross-area pair left different locations")
    if plain_chart.state.location != "chart.press":
        raise AssertionError("chart cross-area pair not at chart.press")
    plain_chart_ids = {a.id for a in enumerate_legal(plain_chart.state, content)}
    lead_chart_ids = {a.id for a in enumerate_legal(lead_chart.state, content)}
    if "prick_the_fathom" not in lead_chart_ids:
        raise AssertionError("lead cast did not unlock prick_the_fathom")
    if "prick_the_fathom" in plain_chart_ids:
        raise AssertionError("prick_the_fathom leaked without lead cast")
    if "lead_cast" not in lead_chart.state.outcomes:
        raise AssertionError("cross lead-chart run lost lead_cast")

    buoy_m = by_id["divergence_marsh_buoy"]
    buoy_c = by_id["divergence_city_buoy"]
    buoy_m_ids, buoy_c_ids = _diverge_legal(content, buoy_m, buoy_c)
    if "know_the_shoal_line" not in buoy_m_ids:
        raise AssertionError("marsh_scout missing know_the_shoal_line")
    if "read_the_buoy_list" not in buoy_c_ids:
        raise AssertionError("city_oath missing read_the_buoy_list")
    if "know_the_shoal_line" in buoy_c_ids or "read_the_buoy_list" in buoy_m_ids:
        raise AssertionError("buoy sheet verbs leaked across sheets")

    plain_buoy = replay(content, by_id["cross_plain_buoy"]["seed"], by_id["cross_plain_buoy"]["sheet"], by_id["cross_plain_buoy"]["actions"])
    chart_buoy = replay(content, by_id["cross_chart_buoy"]["seed"], by_id["cross_chart_buoy"]["sheet"], by_id["cross_chart_buoy"]["actions"])
    if plain_buoy.state.location != chart_buoy.state.location:
        raise AssertionError("buoy cross-area pair left different locations")
    if plain_buoy.state.location != "buoy.drop":
        raise AssertionError("buoy cross-area pair not at buoy.drop")
    plain_buoy_ids = {a.id for a in enumerate_legal(plain_buoy.state, content)}
    chart_buoy_ids = {a.id for a in enumerate_legal(chart_buoy.state, content)}
    if "place_by_rutter" not in chart_buoy_ids:
        raise AssertionError("rutter sealed did not unlock place_by_rutter")
    if "place_by_rutter" in plain_buoy_ids:
        raise AssertionError("place_by_rutter leaked without rutter sealed")
    if "rutter_sealed" not in chart_buoy.state.outcomes:
        raise AssertionError("cross chart-buoy run lost rutter_sealed")

    kelp_m = by_id["divergence_marsh_kelp"]
    kelp_c = by_id["divergence_city_kelp"]
    kelp_m_ids, kelp_c_ids = _diverge_legal(content, kelp_m, kelp_c)
    if "know_the_wrack_tide" not in kelp_m_ids:
        raise AssertionError("marsh_scout missing know_the_wrack_tide")
    if "read_the_kelp_list" not in kelp_c_ids:
        raise AssertionError("city_oath missing read_the_kelp_list")
    if "know_the_wrack_tide" in kelp_c_ids or "read_the_kelp_list" in kelp_m_ids:
        raise AssertionError("kelp sheet verbs leaked across sheets")

    plain_kelp = replay(content, by_id["cross_plain_kelp"]["seed"], by_id["cross_plain_kelp"]["sheet"], by_id["cross_plain_kelp"]["actions"])
    buoy_kelp = replay(content, by_id["cross_buoy_kelp"]["seed"], by_id["cross_buoy_kelp"]["sheet"], by_id["cross_buoy_kelp"]["actions"])
    if plain_kelp.state.location != buoy_kelp.state.location:
        raise AssertionError("kelp cross-area pair left different locations")
    if plain_kelp.state.location != "kelp.bank":
        raise AssertionError("kelp cross-area pair not at kelp.bank")
    plain_kelp_ids = {a.id for a in enumerate_legal(plain_kelp.state, content)}
    buoy_kelp_ids = {a.id for a in enumerate_legal(buoy_kelp.state, content)}
    if "cut_the_outer_bank" not in buoy_kelp_ids:
        raise AssertionError("buoy set did not unlock cut_the_outer_bank")
    if "cut_the_outer_bank" in plain_kelp_ids:
        raise AssertionError("cut_the_outer_bank leaked without buoy set")
    if "buoy_set" not in buoy_kelp.state.outcomes:
        raise AssertionError("cross buoy-kelp run lost buoy_set")

    soap_m = by_id["divergence_marsh_soap"]
    soap_c = by_id["divergence_city_soap"]
    soap_m_ids, soap_c_ids = _diverge_legal(content, soap_m, soap_c)
    if "know_the_lye_run" not in soap_m_ids:
        raise AssertionError("marsh_scout missing know_the_lye_run")
    if "read_the_soap_list" not in soap_c_ids:
        raise AssertionError("city_oath missing read_the_soap_list")
    if "know_the_lye_run" in soap_c_ids or "read_the_soap_list" in soap_m_ids:
        raise AssertionError("soap sheet verbs leaked across sheets")

    plain_soap = replay(content, by_id["cross_plain_soap"]["seed"], by_id["cross_plain_soap"]["sheet"], by_id["cross_plain_soap"]["actions"])
    kelp_soap = replay(content, by_id["cross_kelp_soap"]["seed"], by_id["cross_kelp_soap"]["sheet"], by_id["cross_kelp_soap"]["actions"])
    if plain_soap.state.location != kelp_soap.state.location:
        raise AssertionError("soap cross-area pair left different locations")
    if plain_soap.state.location != "soap.leach":
        raise AssertionError("soap cross-area pair not at soap.leach")
    plain_soap_ids = {a.id for a in enumerate_legal(plain_soap.state, content)}
    kelp_soap_ids = {a.id for a in enumerate_legal(kelp_soap.state, content)}
    if "charge_the_soda" not in kelp_soap_ids:
        raise AssertionError("kelp burned did not unlock charge_the_soda")
    if "charge_the_soda" in plain_soap_ids:
        raise AssertionError("charge_the_soda leaked without kelp burned")
    if "kelp_burned" not in kelp_soap.state.outcomes:
        raise AssertionError("cross kelp-soap run lost kelp_burned")

    full_m = by_id["divergence_marsh_full"]
    full_c = by_id["divergence_city_full"]
    full_m_ids, full_c_ids = _diverge_legal(content, full_m, full_c)
    if "know_the_full_walk" not in full_m_ids:
        raise AssertionError("marsh_scout missing know_the_full_walk")
    if "read_the_full_list" not in full_c_ids:
        raise AssertionError("city_oath missing read_the_full_list")
    if "know_the_full_walk" in full_c_ids or "read_the_full_list" in full_m_ids:
        raise AssertionError("full sheet verbs leaked across sheets")

    plain_full = replay(content, by_id["cross_plain_full"]["seed"], by_id["cross_plain_full"]["sheet"], by_id["cross_plain_full"]["actions"])
    soap_full = replay(content, by_id["cross_soap_full"]["seed"], by_id["cross_soap_full"]["sheet"], by_id["cross_soap_full"]["actions"])
    if plain_full.state.location != soap_full.state.location:
        raise AssertionError("full cross-area pair left different locations")
    if plain_full.state.location != "full.web":
        raise AssertionError("full cross-area pair not at full.web")
    plain_full_ids = {a.id for a in enumerate_legal(plain_full.state, content)}
    soap_full_ids = {a.id for a in enumerate_legal(soap_full.state, content)}
    if "soap_the_web" not in soap_full_ids:
        raise AssertionError("soap cut did not unlock soap_the_web")
    if "soap_the_web" in plain_full_ids:
        raise AssertionError("soap_the_web leaked without soap cut")
    if "soap_cut" not in soap_full.state.outcomes:
        raise AssertionError("cross soap-full run lost soap_cut")

    char_m = by_id["divergence_marsh_char"]
    char_c = by_id["divergence_city_char"]
    char_m_ids, char_c_ids = _diverge_legal(content, char_m, char_c)
    if "know_the_coppice" not in char_m_ids:
        raise AssertionError("marsh_scout missing know_the_coppice")
    if "read_the_coal_list" not in char_c_ids:
        raise AssertionError("city_oath missing read_the_coal_list")
    if "know_the_coppice" in char_c_ids or "read_the_coal_list" in char_m_ids:
        raise AssertionError("char sheet verbs leaked across sheets")

    plain_char = replay(content, by_id["cross_plain_char"]["seed"], by_id["cross_plain_char"]["sheet"], by_id["cross_plain_char"]["actions"])
    full_char = replay(content, by_id["cross_full_char"]["seed"], by_id["cross_full_char"]["sheet"], by_id["cross_full_char"]["actions"])
    if plain_char.state.location != full_char.state.location:
        raise AssertionError("char cross-area pair left different locations")
    if plain_char.state.location != "char.clamp":
        raise AssertionError("char cross-area pair not at char.clamp")
    plain_char_ids = {a.id for a in enumerate_legal(plain_char.state, content)}
    full_char_ids = {a.id for a in enumerate_legal(full_char.state, content)}
    if "cover_the_clamp" not in full_char_ids:
        raise AssertionError("cloth fulled did not unlock cover_the_clamp")
    if "cover_the_clamp" in plain_char_ids:
        raise AssertionError("cover_the_clamp leaked without cloth fulled")
    if "cloth_fulled" not in full_char.state.outcomes:
        raise AssertionError("cross full-char run lost cloth_fulled")

    lime_m = by_id["divergence_marsh_lime"]
    lime_c = by_id["divergence_city_lime"]
    lime_m_ids, lime_c_ids = _diverge_legal(content, lime_m, lime_c)
    if "know_the_shell_burn" not in lime_m_ids:
        raise AssertionError("marsh_scout missing know_the_shell_burn")
    if "read_the_lime_list" not in lime_c_ids:
        raise AssertionError("city_oath missing read_the_lime_list")
    if "know_the_shell_burn" in lime_c_ids or "read_the_lime_list" in lime_m_ids:
        raise AssertionError("lime sheet verbs leaked across sheets")

    plain_lime = replay(content, by_id["cross_plain_lime"]["seed"], by_id["cross_plain_lime"]["sheet"], by_id["cross_plain_lime"]["actions"])
    coal_lime = replay(content, by_id["cross_coal_lime"]["seed"], by_id["cross_coal_lime"]["sheet"], by_id["cross_coal_lime"]["actions"])
    if plain_lime.state.location != coal_lime.state.location:
        raise AssertionError("lime cross-area pair left different locations")
    if plain_lime.state.location != "lime.charge":
        raise AssertionError("lime cross-area pair not at lime.charge")
    plain_lime_ids = {a.id for a in enumerate_legal(plain_lime.state, content)}
    coal_lime_ids = {a.id for a in enumerate_legal(coal_lime.state, content)}
    if "fire_with_coal" not in coal_lime_ids:
        raise AssertionError("coal drawn did not unlock fire_with_coal")
    if "fire_with_coal" in plain_lime_ids:
        raise AssertionError("fire_with_coal leaked without coal drawn")
    if "coal_drawn" not in coal_lime.state.outcomes:
        raise AssertionError("cross coal-lime run lost coal_drawn")

    mason_m = by_id["divergence_marsh_mason"]
    mason_c = by_id["divergence_city_mason"]
    mason_m_ids, mason_c_ids = _diverge_legal(content, mason_m, mason_c)
    if "know_the_bed_joint" not in mason_m_ids:
        raise AssertionError("marsh_scout missing know_the_bed_joint")
    if "read_the_mason_list" not in mason_c_ids:
        raise AssertionError("city_oath missing read_the_mason_list")
    if "know_the_bed_joint" in mason_c_ids or "read_the_mason_list" in mason_m_ids:
        raise AssertionError("mason sheet verbs leaked across sheets")

    plain_mason = replay(content, by_id["cross_plain_mason"]["seed"], by_id["cross_plain_mason"]["sheet"], by_id["cross_plain_mason"]["actions"])
    lime_mason = replay(content, by_id["cross_lime_mason"]["seed"], by_id["cross_lime_mason"]["sheet"], by_id["cross_lime_mason"]["actions"])
    if plain_mason.state.location != lime_mason.state.location:
        raise AssertionError("mason cross-area pair left different locations")
    if plain_mason.state.location != "mason.mix":
        raise AssertionError("mason cross-area pair not at mason.mix")
    plain_mason_ids = {a.id for a in enumerate_legal(plain_mason.state, content)}
    lime_mason_ids = {a.id for a in enumerate_legal(lime_mason.state, content)}
    if "temper_the_lime" not in lime_mason_ids:
        raise AssertionError("lime slaked did not unlock temper_the_lime")
    if "temper_the_lime" in plain_mason_ids:
        raise AssertionError("temper_the_lime leaked without lime slaked")
    if "lime_slaked" not in lime_mason.state.outcomes:
        raise AssertionError("cross lime-mason run lost lime_slaked")

    thatch_m = by_id["divergence_marsh_thatch"]
    thatch_c = by_id["divergence_city_thatch"]
    thatch_m_ids, thatch_c_ids = _diverge_legal(content, thatch_m, thatch_c)
    if "know_the_yealm" not in thatch_m_ids:
        raise AssertionError("marsh_scout missing know_the_yealm")
    if "read_the_thatch_list" not in thatch_c_ids:
        raise AssertionError("city_oath missing read_the_thatch_list")
    if "know_the_yealm" in thatch_c_ids or "read_the_thatch_list" in thatch_m_ids:
        raise AssertionError("thatch sheet verbs leaked across sheets")

    plain_thatch = replay(content, by_id["cross_plain_thatch"]["seed"], by_id["cross_plain_thatch"]["sheet"], by_id["cross_plain_thatch"]["actions"])
    mason_thatch = replay(content, by_id["cross_mason_thatch"]["seed"], by_id["cross_mason_thatch"]["sheet"], by_id["cross_mason_thatch"]["actions"])
    if plain_thatch.state.location != mason_thatch.state.location:
        raise AssertionError("thatch cross-area pair left different locations")
    if plain_thatch.state.location != "thatch.ridge":
        raise AssertionError("thatch cross-area pair not at thatch.ridge")
    plain_thatch_ids = {a.id for a in enumerate_legal(plain_thatch.state, content)}
    mason_thatch_ids = {a.id for a in enumerate_legal(mason_thatch.state, content)}
    if "set_on_stone" not in mason_thatch_ids:
        raise AssertionError("joint pointed did not unlock set_on_stone")
    if "set_on_stone" in plain_thatch_ids:
        raise AssertionError("set_on_stone leaked without joint pointed")
    if "joint_pointed" not in mason_thatch.state.outcomes:
        raise AssertionError("cross mason-thatch run lost joint_pointed")

    cistern_m = by_id["divergence_marsh_cistern"]
    cistern_c = by_id["divergence_city_cistern"]
    cistern_m_ids, cistern_c_ids = _diverge_legal(content, cistern_m, cistern_c)
    if "know_the_eave_run" not in cistern_m_ids:
        raise AssertionError("marsh_scout missing know_the_eave_run")
    if "read_the_cistern_list" not in cistern_c_ids:
        raise AssertionError("city_oath missing read_the_cistern_list")
    if "know_the_eave_run" in cistern_c_ids or "read_the_cistern_list" in cistern_m_ids:
        raise AssertionError("cistern sheet verbs leaked across sheets")

    plain_cistern = replay(content, by_id["cross_plain_cistern"]["seed"], by_id["cross_plain_cistern"]["sheet"], by_id["cross_plain_cistern"]["actions"])
    thatch_cistern = replay(content, by_id["cross_thatch_cistern"]["seed"], by_id["cross_thatch_cistern"]["sheet"], by_id["cross_thatch_cistern"]["actions"])
    if plain_cistern.state.location != thatch_cistern.state.location:
        raise AssertionError("cistern cross-area pair left different locations")
    if plain_cistern.state.location != "cistern.eave":
        raise AssertionError("cistern cross-area pair not at cistern.eave")
    plain_cistern_ids = {a.id for a in enumerate_legal(plain_cistern.state, content)}
    thatch_cistern_ids = {a.id for a in enumerate_legal(thatch_cistern.state, content)}
    if "hang_under_roof" not in thatch_cistern_ids:
        raise AssertionError("roof set did not unlock hang_under_roof")
    if "hang_under_roof" in plain_cistern_ids:
        raise AssertionError("hang_under_roof leaked without roof set")
    if "roof_set" not in thatch_cistern.state.outcomes:
        raise AssertionError("cross thatch-cistern run lost roof_set")

    wash_m = by_id["divergence_marsh_wash"]
    wash_c = by_id["divergence_city_wash"]
    wash_m_ids, wash_c_ids = _diverge_legal(content, wash_m, wash_c)
    if "know_the_wash_run" not in wash_m_ids:
        raise AssertionError("marsh_scout missing know_the_wash_run")
    if "read_the_wash_list" not in wash_c_ids:
        raise AssertionError("city_oath missing read_the_wash_list")
    if "know_the_wash_run" in wash_c_ids or "read_the_wash_list" in wash_m_ids:
        raise AssertionError("wash sheet verbs leaked across sheets")

    plain_wash = replay(content, by_id["cross_plain_wash"]["seed"], by_id["cross_plain_wash"]["sheet"], by_id["cross_plain_wash"]["actions"])
    cistern_wash = replay(content, by_id["cross_cistern_wash"]["seed"], by_id["cross_cistern_wash"]["sheet"], by_id["cross_cistern_wash"]["actions"])
    if plain_wash.state.location != cistern_wash.state.location:
        raise AssertionError("wash cross-area pair left different locations")
    if plain_wash.state.location != "wash.pan":
        raise AssertionError("wash cross-area pair not at wash.pan")
    plain_wash_ids = {a.id for a in enumerate_legal(plain_wash.state, content)}
    cistern_wash_ids = {a.id for a in enumerate_legal(cistern_wash.state, content)}
    if "fill_the_pan" not in cistern_wash_ids:
        raise AssertionError("cistern filled did not unlock fill_the_pan")
    if "fill_the_pan" in plain_wash_ids:
        raise AssertionError("fill_the_pan leaked without cistern filled")
    if "cistern_filled" not in cistern_wash.state.outcomes:
        raise AssertionError("cross cistern-wash run lost cistern_filled")

    rag_m = by_id["divergence_marsh_rag"]
    rag_c = by_id["divergence_city_rag"]
    rag_m_ids, rag_c_ids = _diverge_legal(content, rag_m, rag_c)
    if "know_the_rag_run" not in rag_m_ids:
        raise AssertionError("marsh_scout missing know_the_rag_run")
    if "read_the_rag_list" not in rag_c_ids:
        raise AssertionError("city_oath missing read_the_rag_list")
    if "know_the_rag_run" in rag_c_ids or "read_the_rag_list" in rag_m_ids:
        raise AssertionError("rag sheet verbs leaked across sheets")

    plain_rag = replay(content, by_id["cross_plain_rag"]["seed"], by_id["cross_plain_rag"]["sheet"], by_id["cross_plain_rag"]["actions"])
    wash_rag = replay(content, by_id["cross_wash_rag"]["seed"], by_id["cross_wash_rag"]["sheet"], by_id["cross_wash_rag"]["actions"])
    if plain_rag.state.location != wash_rag.state.location:
        raise AssertionError("rag cross-area pair left different locations")
    if plain_rag.state.location != "rag.stamp":
        raise AssertionError("rag cross-area pair not at rag.stamp")
    plain_rag_ids = {a.id for a in enumerate_legal(plain_rag.state, content)}
    wash_rag_ids = {a.id for a in enumerate_legal(wash_rag.state, content)}
    if "sort_the_white" not in wash_rag_ids:
        raise AssertionError("wash hung did not unlock sort_the_white")
    if "sort_the_white" in plain_rag_ids:
        raise AssertionError("sort_the_white leaked without wash hung")
    if "wash_hung" not in wash_rag.state.outcomes:
        raise AssertionError("cross wash-rag run lost wash_hung")

    osier_m = by_id["divergence_marsh_osier"]
    osier_c = by_id["divergence_city_osier"]
    osier_m_ids, osier_c_ids = _diverge_legal(content, osier_m, osier_c)
    if "know_the_holt_cut" not in osier_m_ids:
        raise AssertionError("marsh_scout missing know_the_holt_cut")
    if "read_the_osier_list" not in osier_c_ids:
        raise AssertionError("city_oath missing read_the_osier_list")
    if "know_the_holt_cut" in osier_c_ids or "read_the_osier_list" in osier_m_ids:
        raise AssertionError("osier sheet verbs leaked across sheets")

    plain_osier = replay(content, by_id["cross_plain_osier"]["seed"], by_id["cross_plain_osier"]["sheet"], by_id["cross_plain_osier"]["actions"])
    rag_osier = replay(content, by_id["cross_rag_osier"]["seed"], by_id["cross_rag_osier"]["sheet"], by_id["cross_rag_osier"]["actions"])
    if plain_osier.state.location != rag_osier.state.location:
        raise AssertionError("osier cross-area pair left different locations")
    if plain_osier.state.location != "osier.holt":
        raise AssertionError("osier cross-area pair not at osier.holt")
    plain_osier_ids = {a.id for a in enumerate_legal(plain_osier.state, content)}
    rag_osier_ids = {a.id for a in enumerate_legal(rag_osier.state, content)}
    if "wrap_the_holt" not in rag_osier_ids:
        raise AssertionError("paper laid did not unlock wrap_the_holt")
    if "wrap_the_holt" in plain_osier_ids:
        raise AssertionError("wrap_the_holt leaked without paper laid")
    if "paper_laid" not in rag_osier.state.outcomes:
        raise AssertionError("cross rag-osier run lost paper_laid")

    bake_m = by_id["divergence_marsh_bake"]
    bake_c = by_id["divergence_city_bake"]
    bake_m_ids, bake_c_ids = _diverge_legal(content, bake_m, bake_c)
    if "know_the_sponge" not in bake_m_ids:
        raise AssertionError("marsh_scout missing know_the_sponge")
    if "read_the_bake_list" not in bake_c_ids:
        raise AssertionError("city_oath missing read_the_bake_list")
    if "know_the_sponge" in bake_c_ids or "read_the_bake_list" in bake_m_ids:
        raise AssertionError("bake sheet verbs leaked across sheets")

    plain_bake = replay(content, by_id["cross_plain_bake"]["seed"], by_id["cross_plain_bake"]["sheet"], by_id["cross_plain_bake"]["actions"])
    osier_bake = replay(content, by_id["cross_osier_bake"]["seed"], by_id["cross_osier_bake"]["sheet"], by_id["cross_osier_bake"]["actions"])
    if plain_bake.state.location != osier_bake.state.location:
        raise AssertionError("bake cross-area pair left different locations")
    if plain_bake.state.location != "bake.sponge":
        raise AssertionError("bake cross-area pair not at bake.sponge")
    plain_bake_ids = {a.id for a in enumerate_legal(plain_bake.state, content)}
    osier_bake_ids = {a.id for a in enumerate_legal(osier_bake.state, content)}
    if "proof_in_frail" not in osier_bake_ids:
        raise AssertionError("frail woven did not unlock proof_in_frail")
    if "proof_in_frail" in plain_bake_ids:
        raise AssertionError("proof_in_frail leaked without frail woven")
    if "frail_woven" not in osier_bake.state.outcomes:
        raise AssertionError("cross osier-bake run lost frail_woven")

    dairy_m = by_id["divergence_marsh_dairy"]
    dairy_c = by_id["divergence_city_dairy"]
    dairy_m_ids, dairy_c_ids = _diverge_legal(content, dairy_m, dairy_c)
    if "know_the_rennet" not in dairy_m_ids:
        raise AssertionError("marsh_scout missing know_the_rennet")
    if "read_the_dairy_list" not in dairy_c_ids:
        raise AssertionError("city_oath missing read_the_dairy_list")
    if "know_the_rennet" in dairy_c_ids or "read_the_dairy_list" in dairy_m_ids:
        raise AssertionError("dairy sheet verbs leaked across sheets")

    plain_dairy = replay(content, by_id["cross_plain_dairy"]["seed"], by_id["cross_plain_dairy"]["sheet"], by_id["cross_plain_dairy"]["actions"])
    bake_dairy = replay(content, by_id["cross_bake_dairy"]["seed"], by_id["cross_bake_dairy"]["sheet"], by_id["cross_bake_dairy"]["actions"])
    if plain_dairy.state.location != bake_dairy.state.location:
        raise AssertionError("dairy cross-area pair left different locations")
    if plain_dairy.state.location != "dairy.keel":
        raise AssertionError("dairy cross-area pair not at dairy.keel")
    plain_dairy_ids = {a.id for a in enumerate_legal(plain_dairy.state, content)}
    bake_dairy_ids = {a.id for a in enumerate_legal(bake_dairy.state, content)}
    if "scald_the_milk" not in bake_dairy_ids:
        raise AssertionError("loaf drawn did not unlock scald_the_milk")
    if "scald_the_milk" in plain_dairy_ids:
        raise AssertionError("scald_the_milk leaked without loaf drawn")
    if "loaf_drawn" not in bake_dairy.state.outcomes:
        raise AssertionError("cross bake-dairy run lost loaf_drawn")

    loom_m = by_id["divergence_marsh_loom"]
    loom_c = by_id["divergence_city_loom"]
    loom_m_ids, loom_c_ids = _diverge_legal(content, loom_m, loom_c)
    if "know_the_warp" not in loom_m_ids:
        raise AssertionError("marsh_scout missing know_the_warp")
    if "read_the_loom_list" not in loom_c_ids:
        raise AssertionError("city_oath missing read_the_loom_list")
    if "know_the_warp" in loom_c_ids or "read_the_loom_list" in loom_m_ids:
        raise AssertionError("loom sheet verbs leaked across sheets")

    plain_loom = replay(content, by_id["cross_plain_loom"]["seed"], by_id["cross_plain_loom"]["sheet"], by_id["cross_plain_loom"]["actions"])
    dairy_loom = replay(content, by_id["cross_dairy_loom"]["seed"], by_id["cross_dairy_loom"]["sheet"], by_id["cross_dairy_loom"]["actions"])
    if plain_loom.state.location != dairy_loom.state.location:
        raise AssertionError("loom cross-area pair left different locations")
    if plain_loom.state.location != "loom.beam":
        raise AssertionError("loom cross-area pair not at loom.beam")
    plain_loom_ids = {a.id for a in enumerate_legal(plain_loom.state, content)}
    dairy_loom_ids = {a.id for a in enumerate_legal(dairy_loom.state, content)}
    if "wrap_the_warp" not in dairy_loom_ids:
        raise AssertionError("wheel salted did not unlock wrap_the_warp")
    if "wrap_the_warp" in plain_loom_ids:
        raise AssertionError("wrap_the_warp leaked without wheel salted")
    if "wheel_salted" not in dairy_loom.state.outcomes:
        raise AssertionError("cross dairy-loom run lost wheel_salted")

    horn_m = by_id["divergence_marsh_horn"]
    horn_c = by_id["divergence_city_horn"]
    horn_m_ids, horn_c_ids = _diverge_legal(content, horn_m, horn_c)
    if "know_the_horn" not in horn_m_ids:
        raise AssertionError("marsh_scout missing know_the_horn")
    if "read_the_lantern_list" not in horn_c_ids:
        raise AssertionError("city_oath missing read_the_lantern_list")
    if "know_the_horn" in horn_c_ids or "read_the_lantern_list" in horn_m_ids:
        raise AssertionError("horn sheet verbs leaked across sheets")

    plain_horn = replay(content, by_id["cross_plain_horn"]["seed"], by_id["cross_plain_horn"]["sheet"], by_id["cross_plain_horn"]["actions"])
    loom_horn = replay(content, by_id["cross_loom_horn"]["seed"], by_id["cross_loom_horn"]["sheet"], by_id["cross_loom_horn"]["actions"])
    if plain_horn.state.location != loom_horn.state.location:
        raise AssertionError("horn cross-area pair left different locations")
    if plain_horn.state.location != "horn.scrape":
        raise AssertionError("horn cross-area pair not at horn.scrape")
    plain_horn_ids = {a.id for a in enumerate_legal(plain_horn.state, content)}
    loom_horn_ids = {a.id for a in enumerate_legal(loom_horn.state, content)}
    if "wick_the_horn" not in loom_horn_ids:
        raise AssertionError("web sheared did not unlock wick_the_horn")
    if "wick_the_horn" in plain_horn_ids:
        raise AssertionError("wick_the_horn leaked without web sheared")
    if "web_sheared" not in loom_horn.state.outcomes:
        raise AssertionError("cross loom-horn run lost web_sheared")

    gall_m = by_id["divergence_marsh_gall"]
    gall_c = by_id["divergence_city_gall"]
    gall_m_ids, gall_c_ids = _diverge_legal(content, gall_m, gall_c)
    if "know_the_gall_run" not in gall_m_ids:
        raise AssertionError("marsh_scout missing know_the_gall_run")
    if "read_the_ink_list" not in gall_c_ids:
        raise AssertionError("city_oath missing read_the_ink_list")
    if "know_the_gall_run" in gall_c_ids or "read_the_ink_list" in gall_m_ids:
        raise AssertionError("gall sheet verbs leaked across sheets")

    plain_gall = replay(content, by_id["cross_plain_gall"]["seed"], by_id["cross_plain_gall"]["sheet"], by_id["cross_plain_gall"]["actions"])
    horn_gall = replay(content, by_id["cross_horn_gall"]["seed"], by_id["cross_horn_gall"]["sheet"], by_id["cross_horn_gall"]["actions"])
    if plain_gall.state.location != horn_gall.state.location:
        raise AssertionError("gall cross-area pair left different locations")
    if plain_gall.state.location != "gall.crush":
        raise AssertionError("gall cross-area pair not at gall.crush")
    plain_gall_ids = {a.id for a in enumerate_legal(plain_gall.state, content)}
    horn_gall_ids = {a.id for a in enumerate_legal(horn_gall.state, content)}
    if "light_the_crush" not in horn_gall_ids:
        raise AssertionError("lantern hung did not unlock light_the_crush")
    if "light_the_crush" in plain_gall_ids:
        raise AssertionError("light_the_crush leaked without lantern hung")
    if "lantern_hung" not in horn_gall.state.outcomes:
        raise AssertionError("cross horn-gall run lost lantern_hung")

    cobble_m = by_id["divergence_marsh_cobble"]
    cobble_c = by_id["divergence_city_cobble"]
    cobble_m_ids, cobble_c_ids = _diverge_legal(content, cobble_m, cobble_c)
    if "know_the_last" not in cobble_m_ids:
        raise AssertionError("marsh_scout missing know_the_last")
    if "read_the_cobble_list" not in cobble_c_ids:
        raise AssertionError("city_oath missing read_the_cobble_list")
    if "know_the_last" in cobble_c_ids or "read_the_cobble_list" in cobble_m_ids:
        raise AssertionError("cobble sheet verbs leaked across sheets")

    plain_cobble = replay(content, by_id["cross_plain_cobble"]["seed"], by_id["cross_plain_cobble"]["sheet"], by_id["cross_plain_cobble"]["actions"])
    gall_cobble = replay(content, by_id["cross_gall_cobble"]["seed"], by_id["cross_gall_cobble"]["sheet"], by_id["cross_gall_cobble"]["actions"])
    if plain_cobble.state.location != gall_cobble.state.location:
        raise AssertionError("cobble cross-area pair left different locations")
    if plain_cobble.state.location != "cobble.sole":
        raise AssertionError("cobble cross-area pair not at cobble.sole")
    plain_cobble_ids = {a.id for a in enumerate_legal(plain_cobble.state, content)}
    gall_cobble_ids = {a.id for a in enumerate_legal(gall_cobble.state, content)}
    if "mark_the_last" not in gall_cobble_ids:
        raise AssertionError("nib cut did not unlock mark_the_last")
    if "mark_the_last" in plain_cobble_ids:
        raise AssertionError("mark_the_last leaked without nib cut")
    if "nib_cut" not in gall_cobble.state.outcomes:
        raise AssertionError("cross gall-cobble run lost nib_cut")

    cider_m = by_id["divergence_marsh_cider"]
    cider_c = by_id["divergence_city_cider"]
    cider_m_ids, cider_c_ids = _diverge_legal(content, cider_m, cider_c)
    if "know_the_fruit" not in cider_m_ids:
        raise AssertionError("marsh_scout missing know_the_fruit")
    if "read_the_cider_list" not in cider_c_ids:
        raise AssertionError("city_oath missing read_the_cider_list")
    if "know_the_fruit" in cider_c_ids or "read_the_cider_list" in cider_m_ids:
        raise AssertionError("cider sheet verbs leaked across sheets")

    plain_cider = replay(content, by_id["cross_plain_cider"]["seed"], by_id["cross_plain_cider"]["sheet"], by_id["cross_plain_cider"]["actions"])
    cobble_cider = replay(content, by_id["cross_cobble_cider"]["seed"], by_id["cross_cobble_cider"]["sheet"], by_id["cross_cobble_cider"]["actions"])
    if plain_cider.state.location != cobble_cider.state.location:
        raise AssertionError("cider cross-area pair left different locations")
    if plain_cider.state.location != "cider.fruit":
        raise AssertionError("cider cross-area pair not at cider.fruit")
    plain_cider_ids = {a.id for a in enumerate_legal(plain_cider.state, content)}
    cobble_cider_ids = {a.id for a in enumerate_legal(cobble_cider.state, content)}
    if "leather_the_hopper" not in cobble_cider_ids:
        raise AssertionError("heel pegged did not unlock leather_the_hopper")
    if "leather_the_hopper" in plain_cider_ids:
        raise AssertionError("leather_the_hopper leaked without heel pegged")
    if "heel_pegged" not in cobble_cider.state.outcomes:
        raise AssertionError("cross cobble-cider run lost heel_pegged")

    must_m = by_id["divergence_marsh_must"]
    must_c = by_id["divergence_city_must"]
    must_m_ids, must_c_ids = _diverge_legal(content, must_m, must_c)
    if "know_the_seed" not in must_m_ids:
        raise AssertionError("marsh_scout missing know_the_seed")
    if "read_the_mustard_list" not in must_c_ids:
        raise AssertionError("city_oath missing read_the_mustard_list")
    if "know_the_seed" in must_c_ids or "read_the_mustard_list" in must_m_ids:
        raise AssertionError("must sheet verbs leaked across sheets")

    plain_must = replay(content, by_id["cross_plain_must"]["seed"], by_id["cross_plain_must"]["sheet"], by_id["cross_plain_must"]["actions"])
    cider_must = replay(content, by_id["cross_cider_must"]["seed"], by_id["cross_cider_must"]["sheet"], by_id["cross_cider_must"]["actions"])
    if plain_must.state.location != cider_must.state.location:
        raise AssertionError("must cross-area pair left different locations")
    if plain_must.state.location != "must.quern":
        raise AssertionError("must cross-area pair not at must.quern")
    plain_must_ids = {a.id for a in enumerate_legal(plain_must.state, content)}
    cider_must_ids = {a.id for a in enumerate_legal(cider_must.state, content)}
    if "cider_the_quern" not in cider_must_ids:
        raise AssertionError("keeve bunged did not unlock cider_the_quern")
    if "cider_the_quern" in plain_must_ids:
        raise AssertionError("cider_the_quern leaked without keeve bunged")
    if "keeve_bunged" not in cider_must.state.outcomes:
        raise AssertionError("cross cider-must run lost keeve_bunged")

    link_m = by_id["divergence_marsh_link"]
    link_c = by_id["divergence_city_link"]
    link_m_ids, link_c_ids = _diverge_legal(content, link_m, link_c)
    if "know_the_chop" not in link_m_ids:
        raise AssertionError("marsh_scout missing know_the_chop")
    if "read_the_sausage_list" not in link_c_ids:
        raise AssertionError("city_oath missing read_the_sausage_list")
    if "know_the_chop" in link_c_ids or "read_the_sausage_list" in link_m_ids:
        raise AssertionError("link sheet verbs leaked across sheets")

    plain_link = replay(content, by_id["cross_plain_link"]["seed"], by_id["cross_plain_link"]["sheet"], by_id["cross_plain_link"]["actions"])
    must_link = replay(content, by_id["cross_must_link"]["seed"], by_id["cross_must_link"]["sheet"], by_id["cross_must_link"]["actions"])
    if plain_link.state.location != must_link.state.location:
        raise AssertionError("link cross-area pair left different locations")
    if plain_link.state.location != "link.chop":
        raise AssertionError("link cross-area pair not at link.chop")
    plain_link_ids = {a.id for a in enumerate_legal(plain_link.state, content)}
    must_link_ids = {a.id for a in enumerate_legal(must_link.state, content)}
    if "mustard_the_chop" not in must_link_ids:
        raise AssertionError("mustard potted did not unlock mustard_the_chop")
    if "mustard_the_chop" in plain_link_ids:
        raise AssertionError("mustard_the_chop leaked without mustard potted")
    if "mustard_potted" not in must_link.state.outcomes:
        raise AssertionError("cross must-link run lost mustard_potted")

    pie_m = by_id["divergence_marsh_pie"]
    pie_c = by_id["divergence_city_pie"]
    pie_m_ids, pie_c_ids = _diverge_legal(content, pie_m, pie_c)
    if "know_the_crust" not in pie_m_ids:
        raise AssertionError("marsh_scout missing know_the_crust")
    if "read_the_pie_list" not in pie_c_ids:
        raise AssertionError("city_oath missing read_the_pie_list")
    if "know_the_crust" in pie_c_ids or "read_the_pie_list" in pie_m_ids:
        raise AssertionError("pie sheet verbs leaked across sheets")

    plain_pie = replay(content, by_id["cross_plain_pie"]["seed"], by_id["cross_plain_pie"]["sheet"], by_id["cross_plain_pie"]["actions"])
    link_pie = replay(content, by_id["cross_link_pie"]["seed"], by_id["cross_link_pie"]["sheet"], by_id["cross_link_pie"]["actions"])
    if plain_pie.state.location != link_pie.state.location:
        raise AssertionError("pie cross-area pair left different locations")
    if plain_pie.state.location != "pie.crust":
        raise AssertionError("pie cross-area pair not at pie.crust")
    plain_pie_ids = {a.id for a in enumerate_legal(plain_pie.state, content)}
    link_pie_ids = {a.id for a in enumerate_legal(link_pie.state, content)}
    if "lard_the_crust" not in link_pie_ids:
        raise AssertionError("sausage linked did not unlock lard_the_crust")
    if "lard_the_crust" in plain_pie_ids:
        raise AssertionError("lard_the_crust leaked without sausage linked")
    if "sausage_linked" not in link_pie.state.outcomes:
        raise AssertionError("cross link-pie run lost sausage_linked")

    jam_m = by_id["divergence_marsh_jam"]
    jam_c = by_id["divergence_city_jam"]
    jam_m_ids, jam_c_ids = _diverge_legal(content, jam_m, jam_c)
    if "know_the_pulp" not in jam_m_ids:
        raise AssertionError("marsh_scout missing know_the_pulp")
    if "read_the_jam_list" not in jam_c_ids:
        raise AssertionError("city_oath missing read_the_jam_list")
    if "know_the_pulp" in jam_c_ids or "read_the_jam_list" in jam_m_ids:
        raise AssertionError("jam sheet verbs leaked across sheets")

    plain_jam = replay(content, by_id["cross_plain_jam"]["seed"], by_id["cross_plain_jam"]["sheet"], by_id["cross_plain_jam"]["actions"])
    pie_jam = replay(content, by_id["cross_pie_jam"]["seed"], by_id["cross_pie_jam"]["sheet"], by_id["cross_pie_jam"]["actions"])
    if plain_jam.state.location != pie_jam.state.location:
        raise AssertionError("jam cross-area pair left different locations")
    if plain_jam.state.location != "jam.pulp":
        raise AssertionError("jam cross-area pair not at jam.pulp")
    plain_jam_ids = {a.id for a in enumerate_legal(plain_jam.state, content)}
    pie_jam_ids = {a.id for a in enumerate_legal(pie_jam.state, content)}
    if "pie_the_glaze" not in pie_jam_ids:
        raise AssertionError("pie crimped did not unlock pie_the_glaze")
    if "pie_the_glaze" in plain_jam_ids:
        raise AssertionError("pie_the_glaze leaked without pie crimped")
    if "pie_crimped" not in pie_jam.state.outcomes:
        raise AssertionError("cross pie-jam run lost pie_crimped")

    crock_m = by_id["divergence_marsh_crock"]
    crock_c = by_id["divergence_city_crock"]
    crock_m_ids, crock_c_ids = _diverge_legal(content, crock_m, crock_c)
    if "know_the_throw" not in crock_m_ids:
        raise AssertionError("marsh_scout missing know_the_throw")
    if "read_the_crock_list" not in crock_c_ids:
        raise AssertionError("city_oath missing read_the_crock_list")
    if "know_the_throw" in crock_c_ids or "read_the_crock_list" in crock_m_ids:
        raise AssertionError("crock sheet verbs leaked across sheets")

    plain_crock = replay(content, by_id["cross_plain_crock"]["seed"], by_id["cross_plain_crock"]["sheet"], by_id["cross_plain_crock"]["actions"])
    jam_crock = replay(content, by_id["cross_jam_crock"]["seed"], by_id["cross_jam_crock"]["sheet"], by_id["cross_jam_crock"]["actions"])
    if plain_crock.state.location != jam_crock.state.location:
        raise AssertionError("crock cross-area pair left different locations")
    if plain_crock.state.location != "crock.throw":
        raise AssertionError("crock cross-area pair not at crock.throw")
    plain_crock_ids = {a.id for a in enumerate_legal(plain_crock.state, content)}
    jam_crock_ids = {a.id for a in enumerate_legal(jam_crock.state, content)}
    if "jam_the_flux" not in jam_crock_ids:
        raise AssertionError("jam jarred did not unlock jam_the_flux")
    if "jam_the_flux" in plain_crock_ids:
        raise AssertionError("jam_the_flux leaked without jam jarred")
    if "jam_jarred" not in jam_crock.state.outcomes:
        raise AssertionError("cross jam-crock run lost jam_jarred")

    hide_m = by_id["divergence_marsh_hide"]
    hide_c = by_id["divergence_city_hide"]
    hide_m_ids, hide_c_ids = _diverge_legal(content, hide_m, hide_c)
    if "know_the_flesh" not in hide_m_ids:
        raise AssertionError("marsh_scout missing know_the_flesh")
    if "read_the_hide_list" not in hide_c_ids:
        raise AssertionError("city_oath missing read_the_hide_list")
    if "know_the_flesh" in hide_c_ids or "read_the_hide_list" in hide_m_ids:
        raise AssertionError("hide sheet verbs leaked across sheets")

    plain_hide = replay(content, by_id["cross_plain_hide"]["seed"], by_id["cross_plain_hide"]["sheet"], by_id["cross_plain_hide"]["actions"])
    crock_hide = replay(content, by_id["cross_crock_hide"]["seed"], by_id["cross_crock_hide"]["sheet"], by_id["cross_crock_hide"]["actions"])
    if plain_hide.state.location != crock_hide.state.location:
        raise AssertionError("hide cross-area pair left different locations")
    if plain_hide.state.location != "hide.flesh":
        raise AssertionError("hide cross-area pair not at hide.flesh")
    plain_hide_ids = {a.id for a in enumerate_legal(plain_hide.state, content)}
    crock_hide_ids = {a.id for a in enumerate_legal(crock_hide.state, content)}
    if "crock_the_rinse" not in crock_hide_ids:
        raise AssertionError("crock glazed did not unlock crock_the_rinse")
    if "crock_the_rinse" in plain_hide_ids:
        raise AssertionError("crock_the_rinse leaked without crock glazed")
    if "crock_glazed" not in crock_hide.state.outcomes:
        raise AssertionError("cross crock-hide run lost crock_glazed")

    flax_m = by_id["divergence_marsh_flax"]
    flax_c = by_id["divergence_city_flax"]
    flax_m_ids, flax_c_ids = _diverge_legal(content, flax_m, flax_c)
    if "know_the_rett" not in flax_m_ids:
        raise AssertionError("marsh_scout missing know_the_rett")
    if "read_the_flax_list" not in flax_c_ids:
        raise AssertionError("city_oath missing read_the_flax_list")
    if "know_the_rett" in flax_c_ids or "read_the_flax_list" in flax_m_ids:
        raise AssertionError("flax sheet verbs leaked across sheets")

    plain_flax = replay(content, by_id["cross_plain_flax"]["seed"], by_id["cross_plain_flax"]["sheet"], by_id["cross_plain_flax"]["actions"])
    hide_flax = replay(content, by_id["cross_hide_flax"]["seed"], by_id["cross_hide_flax"]["sheet"], by_id["cross_hide_flax"]["actions"])
    if plain_flax.state.location != hide_flax.state.location:
        raise AssertionError("flax cross-area pair left different locations")
    if plain_flax.state.location != "flax.rett":
        raise AssertionError("flax cross-area pair not at flax.rett")
    plain_flax_ids = {a.id for a in enumerate_legal(plain_flax.state, content)}
    hide_flax_ids = {a.id for a in enumerate_legal(hide_flax.state, content)}
    if "glove_the_rett" not in hide_flax_ids:
        raise AssertionError("hide tanned did not unlock glove_the_rett")
    if "glove_the_rett" in plain_flax_ids:
        raise AssertionError("glove_the_rett leaked without hide tanned")
    if "hide_tanned" not in hide_flax.state.outcomes:
        raise AssertionError("cross hide-flax run lost hide_tanned")

    nail_m = by_id["divergence_marsh_nail"]
    nail_c = by_id["divergence_city_nail"]
    nail_m_ids, nail_c_ids = _diverge_legal(content, nail_m, nail_c)
    if "know_the_snip" not in nail_m_ids:
        raise AssertionError("marsh_scout missing know_the_snip")
    if "read_the_nail_list" not in nail_c_ids:
        raise AssertionError("city_oath missing read_the_nail_list")
    if "know_the_snip" in nail_c_ids or "read_the_nail_list" in nail_m_ids:
        raise AssertionError("nail sheet verbs leaked across sheets")

    plain_nail = replay(content, by_id["cross_plain_nail"]["seed"], by_id["cross_plain_nail"]["sheet"], by_id["cross_plain_nail"]["actions"])
    flax_nail = replay(content, by_id["cross_flax_nail"]["seed"], by_id["cross_flax_nail"]["sheet"], by_id["cross_flax_nail"]["actions"])
    if plain_nail.state.location != flax_nail.state.location:
        raise AssertionError("nail cross-area pair left different locations")
    if plain_nail.state.location != "nail.snip":
        raise AssertionError("nail cross-area pair not at nail.snip")
    plain_nail_ids = {a.id for a in enumerate_legal(plain_nail.state, content)}
    flax_nail_ids = {a.id for a in enumerate_legal(flax_nail.state, content)}
    if "flax_the_grip" not in flax_nail_ids:
        raise AssertionError("flax spun did not unlock flax_the_grip")
    if "flax_the_grip" in plain_nail_ids:
        raise AssertionError("flax_the_grip leaked without flax spun")
    if "flax_spun" not in flax_nail.state.outcomes:
        raise AssertionError("cross flax-nail run lost flax_spun")

    wain_m = by_id["divergence_marsh_wain"]
    wain_c = by_id["divergence_city_wain"]
    wain_m_ids, wain_c_ids = _diverge_legal(content, wain_m, wain_c)
    if "know_the_hub" not in wain_m_ids:
        raise AssertionError("marsh_scout missing know_the_hub")
    if "read_the_wain_list" not in wain_c_ids:
        raise AssertionError("city_oath missing read_the_wain_list")
    if "know_the_hub" in wain_c_ids or "read_the_wain_list" in wain_m_ids:
        raise AssertionError("wain sheet verbs leaked across sheets")

    plain_wain = replay(content, by_id["cross_plain_wain"]["seed"], by_id["cross_plain_wain"]["sheet"], by_id["cross_plain_wain"]["actions"])
    nail_wain = replay(content, by_id["cross_nail_wain"]["seed"], by_id["cross_nail_wain"]["sheet"], by_id["cross_nail_wain"]["actions"])
    if plain_wain.state.location != nail_wain.state.location:
        raise AssertionError("wain cross-area pair left different locations")
    if plain_wain.state.location != "wain.hub":
        raise AssertionError("wain cross-area pair not at wain.hub")
    plain_wain_ids = {a.id for a in enumerate_legal(plain_wain.state, content)}
    nail_wain_ids = {a.id for a in enumerate_legal(nail_wain.state, content)}
    if "nail_the_box" not in nail_wain_ids:
        raise AssertionError("nail pointed did not unlock nail_the_box")
    if "nail_the_box" in plain_wain_ids:
        raise AssertionError("nail_the_box leaked without nail pointed")
    if "nail_pointed" not in nail_wain.state.outcomes:
        raise AssertionError("cross nail-wain run lost nail_pointed")

    malt_m = by_id["divergence_marsh_malt"]
    malt_c = by_id["divergence_city_malt"]
    malt_m_ids, malt_c_ids = _diverge_legal(content, malt_m, malt_c)
    if "know_the_steep" not in malt_m_ids:
        raise AssertionError("marsh_scout missing know_the_steep")
    if "read_the_malt_list" not in malt_c_ids:
        raise AssertionError("city_oath missing read_the_malt_list")
    if "know_the_steep" in malt_c_ids or "read_the_malt_list" in malt_m_ids:
        raise AssertionError("malt sheet verbs leaked across sheets")

    plain_malt = replay(content, by_id["cross_plain_malt"]["seed"], by_id["cross_plain_malt"]["sheet"], by_id["cross_plain_malt"]["actions"])
    wain_malt = replay(content, by_id["cross_wain_malt"]["seed"], by_id["cross_wain_malt"]["sheet"], by_id["cross_wain_malt"]["actions"])
    if plain_malt.state.location != wain_malt.state.location:
        raise AssertionError("malt cross-area pair left different locations")
    if plain_malt.state.location != "malt.steep":
        raise AssertionError("malt cross-area pair not at malt.steep")
    plain_malt_ids = {a.id for a in enumerate_legal(plain_malt.state, content)}
    wain_malt_ids = {a.id for a in enumerate_legal(wain_malt.state, content)}
    if "wain_the_steep" not in wain_malt_ids:
        raise AssertionError("tyre set did not unlock wain_the_steep")
    if "wain_the_steep" in plain_malt_ids:
        raise AssertionError("wain_the_steep leaked without tyre set")
    if "tyre_set" not in wain_malt.state.outcomes:
        raise AssertionError("cross wain-malt run lost tyre_set")

    brew_m = by_id["divergence_marsh_brew"]
    brew_c = by_id["divergence_city_brew"]
    brew_m_ids, brew_c_ids = _diverge_legal(content, brew_m, brew_c)
    if "know_the_grist" not in brew_m_ids:
        raise AssertionError("marsh_scout missing know_the_grist")
    if "read_the_brew_list" not in brew_c_ids:
        raise AssertionError("city_oath missing read_the_brew_list")
    if "know_the_grist" in brew_c_ids or "read_the_brew_list" in brew_m_ids:
        raise AssertionError("brew sheet verbs leaked across sheets")

    plain_brew = replay(content, by_id["cross_plain_brew"]["seed"], by_id["cross_plain_brew"]["sheet"], by_id["cross_plain_brew"]["actions"])
    malt_brew = replay(content, by_id["cross_malt_brew"]["seed"], by_id["cross_malt_brew"]["sheet"], by_id["cross_malt_brew"]["actions"])
    if plain_brew.state.location != malt_brew.state.location:
        raise AssertionError("brew cross-area pair left different locations")
    if plain_brew.state.location != "brew.grist":
        raise AssertionError("brew cross-area pair not at brew.grist")
    plain_brew_ids = {a.id for a in enumerate_legal(plain_brew.state, content)}
    malt_brew_ids = {a.id for a in enumerate_legal(malt_brew.state, content)}
    if "malt_the_grist" not in malt_brew_ids:
        raise AssertionError("malt oasted did not unlock malt_the_grist")
    if "malt_the_grist" in plain_brew_ids:
        raise AssertionError("malt_the_grist leaked without malt oasted")
    if "malt_oasted" not in malt_brew.state.outcomes:
        raise AssertionError("cross malt-brew run lost malt_oasted")

    acet_m = by_id["divergence_marsh_acet"]
    acet_c = by_id["divergence_city_acet"]
    acet_m_ids, acet_c_ids = _diverge_legal(content, acet_m, acet_c)
    if "know_the_mother" not in acet_m_ids:
        raise AssertionError("marsh_scout missing know_the_mother")
    if "read_the_vinegar_list" not in acet_c_ids:
        raise AssertionError("city_oath missing read_the_vinegar_list")
    if "know_the_mother" in acet_c_ids or "read_the_vinegar_list" in acet_m_ids:
        raise AssertionError("acet sheet verbs leaked across sheets")

    plain_acet = replay(content, by_id["cross_plain_acet"]["seed"], by_id["cross_plain_acet"]["sheet"], by_id["cross_plain_acet"]["actions"])
    brew_acet = replay(content, by_id["cross_brew_acet"]["seed"], by_id["cross_brew_acet"]["sheet"], by_id["cross_brew_acet"]["actions"])
    if plain_acet.state.location != brew_acet.state.location:
        raise AssertionError("acet cross-area pair left different locations")
    if plain_acet.state.location != "acet.mother":
        raise AssertionError("acet cross-area pair not at acet.mother")
    plain_acet_ids = {a.id for a in enumerate_legal(plain_acet.state, content)}
    brew_acet_ids = {a.id for a in enumerate_legal(brew_acet.state, content)}
    if "ale_the_mother" not in brew_acet_ids:
        raise AssertionError("gyle racked did not unlock ale_the_mother")
    if "ale_the_mother" in plain_acet_ids:
        raise AssertionError("ale_the_mother leaked without gyle racked")
    if "gyle_racked" not in brew_acet.state.outcomes:
        raise AssertionError("cross brew-acet run lost gyle_racked")

    glue_m = by_id["divergence_marsh_glue"]
    glue_c = by_id["divergence_city_glue"]
    glue_m_ids, glue_c_ids = _diverge_legal(content, glue_m, glue_c)
    if "know_the_paring" not in glue_m_ids:
        raise AssertionError("marsh_scout missing know_the_paring")
    if "read_the_glue_list" not in glue_c_ids:
        raise AssertionError("city_oath missing read_the_glue_list")
    if "know_the_paring" in glue_c_ids or "read_the_glue_list" in glue_m_ids:
        raise AssertionError("glue sheet verbs leaked across sheets")

    plain_glue = replay(content, by_id["cross_plain_glue"]["seed"], by_id["cross_plain_glue"]["sheet"], by_id["cross_plain_glue"]["actions"])
    acet_glue = replay(content, by_id["cross_acet_glue"]["seed"], by_id["cross_acet_glue"]["sheet"], by_id["cross_acet_glue"]["actions"])
    if plain_glue.state.location != acet_glue.state.location:
        raise AssertionError("glue cross-area pair left different locations")
    if plain_glue.state.location != "glue.paring":
        raise AssertionError("glue cross-area pair not at glue.paring")
    plain_glue_ids = {a.id for a in enumerate_legal(plain_glue.state, content)}
    acet_glue_ids = {a.id for a in enumerate_legal(acet_glue.state, content)}
    if "acet_the_paring" not in acet_glue_ids:
        raise AssertionError("cruet corked did not unlock acet_the_paring")
    if "acet_the_paring" in plain_glue_ids:
        raise AssertionError("acet_the_paring leaked without cruet corked")
    if "cruet_corked" not in acet_glue.state.outcomes:
        raise AssertionError("cross acet-glue run lost cruet_corked")

    bind_m = by_id["divergence_marsh_bind"]
    bind_c = by_id["divergence_city_bind"]
    bind_m_ids, bind_c_ids = _diverge_legal(content, bind_m, bind_c)
    if "know_the_quire" not in bind_m_ids:
        raise AssertionError("marsh_scout missing know_the_quire")
    if "read_the_bind_list" not in bind_c_ids:
        raise AssertionError("city_oath missing read_the_bind_list")
    if "know_the_quire" in bind_c_ids or "read_the_bind_list" in bind_m_ids:
        raise AssertionError("bind sheet verbs leaked across sheets")

    plain_bind = replay(content, by_id["cross_plain_bind"]["seed"], by_id["cross_plain_bind"]["sheet"], by_id["cross_plain_bind"]["actions"])
    glue_bind = replay(content, by_id["cross_glue_bind"]["seed"], by_id["cross_glue_bind"]["sheet"], by_id["cross_glue_bind"]["actions"])
    if plain_bind.state.location != glue_bind.state.location:
        raise AssertionError("bind cross-area pair left different locations")
    if plain_bind.state.location != "bind.quire":
        raise AssertionError("bind cross-area pair not at bind.quire")
    plain_bind_ids = {a.id for a in enumerate_legal(plain_bind.state, content)}
    glue_bind_ids = {a.id for a in enumerate_legal(glue_bind.state, content)}
    if "glue_the_quire" not in glue_bind_ids:
        raise AssertionError("glue caked did not unlock glue_the_quire")
    if "glue_the_quire" in plain_bind_ids:
        raise AssertionError("glue_the_quire leaked without glue caked")
    if "glue_caked" not in glue_bind.state.outcomes:
        raise AssertionError("cross glue-bind run lost glue_caked")

    gilt_m = by_id["divergence_marsh_gilt"]
    gilt_c = by_id["divergence_city_gilt"]
    gilt_m_ids, gilt_c_ids = _diverge_legal(content, gilt_m, gilt_c)
    if "know_the_bole" not in gilt_m_ids:
        raise AssertionError("marsh_scout missing know_the_bole")
    if "read_the_gilt_list" not in gilt_c_ids:
        raise AssertionError("city_oath missing read_the_gilt_list")
    if "know_the_bole" in gilt_c_ids or "read_the_gilt_list" in gilt_m_ids:
        raise AssertionError("gilt sheet verbs leaked across sheets")

    plain_gilt = replay(content, by_id["cross_plain_gilt"]["seed"], by_id["cross_plain_gilt"]["sheet"], by_id["cross_plain_gilt"]["actions"])
    bind_gilt = replay(content, by_id["cross_bind_gilt"]["seed"], by_id["cross_bind_gilt"]["sheet"], by_id["cross_bind_gilt"]["actions"])
    if plain_gilt.state.location != bind_gilt.state.location:
        raise AssertionError("gilt cross-area pair left different locations")
    if plain_gilt.state.location != "gilt.bole":
        raise AssertionError("gilt cross-area pair not at gilt.bole")
    plain_gilt_ids = {a.id for a in enumerate_legal(plain_gilt.state, content)}
    bind_gilt_ids = {a.id for a in enumerate_legal(bind_gilt.state, content)}
    if "bind_the_bole" not in bind_gilt_ids:
        raise AssertionError("book bound did not unlock bind_the_bole")
    if "bind_the_bole" in plain_gilt_ids:
        raise AssertionError("bind_the_bole leaked without book bound")
    if "book_bound" not in bind_gilt.state.outcomes:
        raise AssertionError("cross bind-gilt run lost book_bound")

    gem_m = by_id["divergence_marsh_gem"]
    gem_c = by_id["divergence_city_gem"]
    gem_m_ids, gem_c_ids = _diverge_legal(content, gem_m, gem_c)
    if "know_the_foil" not in gem_m_ids:
        raise AssertionError("marsh_scout missing know_the_foil")
    if "read_the_gem_list" not in gem_c_ids:
        raise AssertionError("city_oath missing read_the_gem_list")
    if "know_the_foil" in gem_c_ids or "read_the_gem_list" in gem_m_ids:
        raise AssertionError("gem sheet verbs leaked across sheets")

    plain_gem = replay(content, by_id["cross_plain_gem"]["seed"], by_id["cross_plain_gem"]["sheet"], by_id["cross_plain_gem"]["actions"])
    gilt_gem = replay(content, by_id["cross_gilt_gem"]["seed"], by_id["cross_gilt_gem"]["sheet"], by_id["cross_gilt_gem"]["actions"])
    if plain_gem.state.location != gilt_gem.state.location:
        raise AssertionError("gem cross-area pair left different locations")
    if plain_gem.state.location != "gem.foil":
        raise AssertionError("gem cross-area pair not at gem.foil")
    plain_gem_ids = {a.id for a in enumerate_legal(plain_gem.state, content)}
    gilt_gem_ids = {a.id for a in enumerate_legal(gilt_gem.state, content)}
    if "gilt_the_foil" not in gilt_gem_ids:
        raise AssertionError("plate burnished did not unlock gilt_the_foil")
    if "gilt_the_foil" in plain_gem_ids:
        raise AssertionError("gilt_the_foil leaked without plate burnished")
    if "plate_burnished" not in gilt_gem.state.outcomes:
        raise AssertionError("cross gilt-gem run lost plate_burnished")

    glaz_m = by_id["divergence_marsh_glaz"]
    glaz_c = by_id["divergence_city_glaz"]
    glaz_m_ids, glaz_c_ids = _diverge_legal(content, glaz_m, glaz_c)
    if "know_the_score" not in glaz_m_ids:
        raise AssertionError("marsh_scout missing know_the_score")
    if "read_the_glazier_list" not in glaz_c_ids:
        raise AssertionError("city_oath missing read_the_glazier_list")
    if "know_the_score" in glaz_c_ids or "read_the_glazier_list" in glaz_m_ids:
        raise AssertionError("glaz sheet verbs leaked across sheets")

    plain_glaz = replay(content, by_id["cross_plain_glaz"]["seed"], by_id["cross_plain_glaz"]["sheet"], by_id["cross_plain_glaz"]["actions"])
    gem_glaz = replay(content, by_id["cross_gem_glaz"]["seed"], by_id["cross_gem_glaz"]["sheet"], by_id["cross_gem_glaz"]["actions"])
    if plain_glaz.state.location != gem_glaz.state.location:
        raise AssertionError("glaz cross-area pair left different locations")
    if plain_glaz.state.location != "glaz.score":
        raise AssertionError("glaz cross-area pair not at glaz.score")
    plain_glaz_ids = {a.id for a in enumerate_legal(plain_glaz.state, content)}
    gem_glaz_ids = {a.id for a in enumerate_legal(gem_glaz.state, content)}
    if "gem_the_score" not in gem_glaz_ids:
        raise AssertionError("collet closed did not unlock gem_the_score")
    if "gem_the_score" in plain_glaz_ids:
        raise AssertionError("gem_the_score leaked without collet closed")
    if "collet_closed" not in gem_glaz.state.outcomes:
        raise AssertionError("cross gem-glaz run lost collet_closed")

    sash_m = by_id["divergence_marsh_sash"]
    sash_c = by_id["divergence_city_sash"]
    sash_m_ids, sash_c_ids = _diverge_legal(content, sash_m, sash_c)
    if "know_the_stile" not in sash_m_ids:
        raise AssertionError("marsh_scout missing know_the_stile")
    if "read_the_sash_list" not in sash_c_ids:
        raise AssertionError("city_oath missing read_the_sash_list")
    if "know_the_stile" in sash_c_ids or "read_the_sash_list" in sash_m_ids:
        raise AssertionError("sash sheet verbs leaked across sheets")

    plain_sash = replay(content, by_id["cross_plain_sash"]["seed"], by_id["cross_plain_sash"]["sheet"], by_id["cross_plain_sash"]["actions"])
    glaz_sash = replay(content, by_id["cross_glaz_sash"]["seed"], by_id["cross_glaz_sash"]["sheet"], by_id["cross_glaz_sash"]["actions"])
    if plain_sash.state.location != glaz_sash.state.location:
        raise AssertionError("sash cross-area pair left different locations")
    if plain_sash.state.location != "sash.stile":
        raise AssertionError("sash cross-area pair not at sash.stile")
    plain_sash_ids = {a.id for a in enumerate_legal(plain_sash.state, content)}
    glaz_sash_ids = {a.id for a in enumerate_legal(glaz_sash.state, content)}
    if "came_the_rebate" not in glaz_sash_ids:
        raise AssertionError("pane camed did not unlock came_the_rebate")
    if "came_the_rebate" in plain_sash_ids:
        raise AssertionError("came_the_rebate leaked without pane camed")
    if "pane_camed" not in glaz_sash.state.outcomes:
        raise AssertionError("cross glaz-sash run lost pane_camed")

    putty_m = by_id["divergence_marsh_putty"]
    putty_c = by_id["divergence_city_putty"]
    putty_m_ids, putty_c_ids = _diverge_legal(content, putty_m, putty_c)
    if "know_the_whip" not in putty_m_ids:
        raise AssertionError("marsh_scout missing know_the_whip")
    if "read_the_putty_list" not in putty_c_ids:
        raise AssertionError("city_oath missing read_the_putty_list")
    if "know_the_whip" in putty_c_ids or "read_the_putty_list" in putty_m_ids:
        raise AssertionError("putty sheet verbs leaked across sheets")

    plain_putty = replay(content, by_id["cross_plain_putty"]["seed"], by_id["cross_plain_putty"]["sheet"], by_id["cross_plain_putty"]["actions"])
    sash_putty = replay(content, by_id["cross_sash_putty"]["seed"], by_id["cross_sash_putty"]["sheet"], by_id["cross_sash_putty"]["actions"])
    if plain_putty.state.location != sash_putty.state.location:
        raise AssertionError("putty cross-area pair left different locations")
    if plain_putty.state.location != "putty.whip":
        raise AssertionError("putty cross-area pair not at putty.whip")
    plain_putty_ids = {a.id for a in enumerate_legal(plain_putty.state, content)}
    sash_putty_ids = {a.id for a in enumerate_legal(sash_putty.state, content)}
    if "sash_the_bed" not in sash_putty_ids:
        raise AssertionError("sash pinned did not unlock sash_the_bed")
    if "sash_the_bed" in plain_putty_ids:
        raise AssertionError("sash_the_bed leaked without sash pinned")
    if "sash_pinned" not in sash_putty.state.outcomes:
        raise AssertionError("cross sash-putty run lost sash_pinned")

    paint_m = by_id["divergence_marsh_paint"]
    paint_c = by_id["divergence_city_paint"]
    paint_m_ids, paint_c_ids = _diverge_legal(content, paint_m, paint_c)
    if "know_the_mull" not in paint_m_ids:
        raise AssertionError("marsh_scout missing know_the_mull")
    if "read_the_paint_list" not in paint_c_ids:
        raise AssertionError("city_oath missing read_the_paint_list")
    if "know_the_mull" in paint_c_ids or "read_the_paint_list" in paint_m_ids:
        raise AssertionError("paint sheet verbs leaked across sheets")

    plain_paint = replay(content, by_id["cross_plain_paint"]["seed"], by_id["cross_plain_paint"]["sheet"], by_id["cross_plain_paint"]["actions"])
    putty_paint = replay(content, by_id["cross_putty_paint"]["seed"], by_id["cross_putty_paint"]["sheet"], by_id["cross_putty_paint"]["actions"])
    if plain_paint.state.location != putty_paint.state.location:
        raise AssertionError("paint cross-area pair left different locations")
    if plain_paint.state.location != "paint.mull":
        raise AssertionError("paint cross-area pair not at paint.mull")
    plain_paint_ids = {a.id for a in enumerate_legal(plain_paint.state, content)}
    putty_paint_ids = {a.id for a in enumerate_legal(putty_paint.state, content)}
    if "dust_the_coat" not in putty_paint_ids:
        raise AssertionError("light dusted did not unlock dust_the_coat")
    if "dust_the_coat" in plain_paint_ids:
        raise AssertionError("dust_the_coat leaked without light dusted")
    if "light_dusted" not in putty_paint.state.outcomes:
        raise AssertionError("cross putty-paint run lost light_dusted")

    varn_m = by_id["divergence_marsh_varn"]
    varn_c = by_id["divergence_city_varn"]
    varn_m_ids, varn_c_ids = _diverge_legal(content, varn_m, varn_c)
    if "know_the_cook" not in varn_m_ids:
        raise AssertionError("marsh_scout missing know_the_cook")
    if "read_the_varnish_list" not in varn_c_ids:
        raise AssertionError("city_oath missing read_the_varnish_list")
    if "know_the_cook" in varn_c_ids or "read_the_varnish_list" in varn_m_ids:
        raise AssertionError("varnish sheet verbs leaked across sheets")

    plain_varn = replay(content, by_id["cross_plain_varn"]["seed"], by_id["cross_plain_varn"]["sheet"], by_id["cross_plain_varn"]["actions"])
    paint_varn = replay(content, by_id["cross_paint_varn"]["seed"], by_id["cross_paint_varn"]["sheet"], by_id["cross_paint_varn"]["actions"])
    if plain_varn.state.location != paint_varn.state.location:
        raise AssertionError("varnish cross-area pair left different locations")
    if plain_varn.state.location != "varn.cook":
        raise AssertionError("varnish cross-area pair not at varn.cook")
    plain_varn_ids = {a.id for a in enumerate_legal(plain_varn.state, content)}
    paint_varn_ids = {a.id for a in enumerate_legal(paint_varn.state, content)}
    if "prime_the_gum" not in paint_varn_ids:
        raise AssertionError("coat brushed did not unlock prime_the_gum")
    if "prime_the_gum" in plain_varn_ids:
        raise AssertionError("prime_the_gum leaked without coat brushed")
    if "coat_brushed" not in paint_varn.state.outcomes:
        raise AssertionError("cross paint-varn run lost coat_brushed")

    latch_m = by_id["divergence_marsh_latch"]
    latch_c = by_id["divergence_city_latch"]
    latch_m_ids, latch_c_ids = _diverge_legal(content, latch_m, latch_c)
    if "know_the_keep" not in latch_m_ids:
        raise AssertionError("marsh_scout missing know_the_keep")
    if "read_the_latch_list" not in latch_c_ids:
        raise AssertionError("city_oath missing read_the_latch_list")
    if "know_the_keep" in latch_c_ids or "read_the_latch_list" in latch_m_ids:
        raise AssertionError("latch sheet verbs leaked across sheets")

    plain_latch = replay(content, by_id["cross_plain_latch"]["seed"], by_id["cross_plain_latch"]["sheet"], by_id["cross_plain_latch"]["actions"])
    varn_latch = replay(content, by_id["cross_varn_latch"]["seed"], by_id["cross_varn_latch"]["sheet"], by_id["cross_varn_latch"]["actions"])
    if plain_latch.state.location != varn_latch.state.location:
        raise AssertionError("latch cross-area pair left different locations")
    if plain_latch.state.location != "latch.keep":
        raise AssertionError("latch cross-area pair not at latch.keep")
    plain_latch_ids = {a.id for a in enumerate_legal(plain_latch.state, content)}
    varn_latch_ids = {a.id for a in enumerate_legal(varn_latch.state, content)}
    if "varnish_the_keep" not in varn_latch_ids:
        raise AssertionError("varnish flowed did not unlock varnish_the_keep")
    if "varnish_the_keep" in plain_latch_ids:
        raise AssertionError("varnish_the_keep leaked without varnish flowed")
    if "varnish_flowed" not in varn_latch.state.outcomes:
        raise AssertionError("cross varn-latch run lost varnish_flowed")

    hinge_m = by_id["divergence_marsh_hinge"]
    hinge_c = by_id["divergence_city_hinge"]
    hinge_m_ids, hinge_c_ids = _diverge_legal(content, hinge_m, hinge_c)
    if "know_the_knuckle" not in hinge_m_ids:
        raise AssertionError("marsh_scout missing know_the_knuckle")
    if "read_the_hinge_list" not in hinge_c_ids:
        raise AssertionError("city_oath missing read_the_hinge_list")
    if "know_the_knuckle" in hinge_c_ids or "read_the_hinge_list" in hinge_m_ids:
        raise AssertionError("hinge sheet verbs leaked across sheets")

    plain_hinge = replay(content, by_id["cross_plain_hinge"]["seed"], by_id["cross_plain_hinge"]["sheet"], by_id["cross_plain_hinge"]["actions"])
    latch_hinge = replay(content, by_id["cross_latch_hinge"]["seed"], by_id["cross_latch_hinge"]["sheet"], by_id["cross_latch_hinge"]["actions"])
    if plain_hinge.state.location != latch_hinge.state.location:
        raise AssertionError("hinge cross-area pair left different locations")
    if plain_hinge.state.location != "hinge.knuckle":
        raise AssertionError("hinge cross-area pair not at hinge.knuckle")
    plain_hinge_ids = {a.id for a in enumerate_legal(plain_hinge.state, content)}
    latch_hinge_ids = {a.id for a in enumerate_legal(latch_hinge.state, content)}
    if "latch_the_knuckle" not in latch_hinge_ids:
        raise AssertionError("latch thrown did not unlock latch_the_knuckle")
    if "latch_the_knuckle" in plain_hinge_ids:
        raise AssertionError("latch_the_knuckle leaked without latch thrown")
    if "latch_thrown" not in latch_hinge.state.outcomes:
        raise AssertionError("cross latch-hinge run lost latch_thrown")

    stay_m = by_id["divergence_marsh_stay"]
    stay_c = by_id["divergence_city_stay"]
    stay_m_ids, stay_c_ids = _diverge_legal(content, stay_m, stay_c)
    if "know_the_slot" not in stay_m_ids:
        raise AssertionError("marsh_scout missing know_the_slot")
    if "read_the_stay_list" not in stay_c_ids:
        raise AssertionError("city_oath missing read_the_stay_list")
    if "know_the_slot" in stay_c_ids or "read_the_stay_list" in stay_m_ids:
        raise AssertionError("stay sheet verbs leaked across sheets")

    plain_stay = replay(content, by_id["cross_plain_stay"]["seed"], by_id["cross_plain_stay"]["sheet"], by_id["cross_plain_stay"]["actions"])
    hinge_stay = replay(content, by_id["cross_hinge_stay"]["seed"], by_id["cross_hinge_stay"]["sheet"], by_id["cross_hinge_stay"]["actions"])
    if plain_stay.state.location != hinge_stay.state.location:
        raise AssertionError("stay cross-area pair left different locations")
    if plain_stay.state.location != "stay.slot":
        raise AssertionError("stay cross-area pair not at stay.slot")
    plain_stay_ids = {a.id for a in enumerate_legal(plain_stay.state, content)}
    hinge_stay_ids = {a.id for a in enumerate_legal(hinge_stay.state, content)}
    if "hinge_the_slot" not in hinge_stay_ids:
        raise AssertionError("gudgeon shipped did not unlock hinge_the_slot")
    if "hinge_the_slot" in plain_stay_ids:
        raise AssertionError("hinge_the_slot leaked without gudgeon shipped")
    if "gudgeon_shipped" not in hinge_stay.state.outcomes:
        raise AssertionError("cross hinge-stay run lost gudgeon_shipped")

    sill_m = by_id["divergence_marsh_sill"]
    sill_c = by_id["divergence_city_sill"]
    sill_m_ids, sill_c_ids = _diverge_legal(content, sill_m, sill_c)
    if "know_the_sill" not in sill_m_ids:
        raise AssertionError("marsh_scout missing know_the_sill")
    if "read_the_sill_list" not in sill_c_ids:
        raise AssertionError("city_oath missing read_the_sill_list")
    if "know_the_sill" in sill_c_ids or "read_the_sill_list" in sill_m_ids:
        raise AssertionError("sill sheet verbs leaked across sheets")

    plain_sill = replay(content, by_id["cross_plain_sill"]["seed"], by_id["cross_plain_sill"]["sheet"], by_id["cross_plain_sill"]["actions"])
    stay_sill = replay(content, by_id["cross_stay_sill"]["seed"], by_id["cross_stay_sill"]["sheet"], by_id["cross_stay_sill"]["actions"])
    if plain_sill.state.location != stay_sill.state.location:
        raise AssertionError("sill cross-area pair left different locations")
    if plain_sill.state.location != "sill.bed":
        raise AssertionError("sill cross-area pair not at sill.bed")
    plain_sill_ids = {a.id for a in enumerate_legal(plain_sill.state, content)}
    stay_sill_ids = {a.id for a in enumerate_legal(stay_sill.state, content)}
    if "stay_the_sill" not in stay_sill_ids:
        raise AssertionError("casement stayed did not unlock stay_the_sill")
    if "stay_the_sill" in plain_sill_ids:
        raise AssertionError("stay_the_sill leaked without casement stayed")
    if "casement_stayed" not in stay_sill.state.outcomes:
        raise AssertionError("cross stay-sill run lost casement_stayed")

    case_m = by_id["divergence_marsh_case"]
    case_c = by_id["divergence_city_case"]
    case_m_ids, case_c_ids = _diverge_legal(content, case_m, case_c)
    if "know_the_mitre" not in case_m_ids:
        raise AssertionError("marsh_scout missing know_the_mitre")
    if "read_the_casing_list" not in case_c_ids:
        raise AssertionError("city_oath missing read_the_casing_list")
    if "know_the_mitre" in case_c_ids or "read_the_casing_list" in case_m_ids:
        raise AssertionError("casing sheet verbs leaked across sheets")

    plain_case = replay(content, by_id["cross_plain_case"]["seed"], by_id["cross_plain_case"]["sheet"], by_id["cross_plain_case"]["actions"])
    sill_case = replay(content, by_id["cross_sill_case"]["seed"], by_id["cross_sill_case"]["sheet"], by_id["cross_sill_case"]["actions"])
    if plain_case.state.location != sill_case.state.location:
        raise AssertionError("casing cross-area pair left different locations")
    if plain_case.state.location != "case.mitre":
        raise AssertionError("casing cross-area pair not at case.mitre")
    plain_case_ids = {a.id for a in enumerate_legal(plain_case.state, content)}
    sill_case_ids = {a.id for a in enumerate_legal(sill_case.state, content)}
    if "stool_the_mitre" not in sill_case_ids:
        raise AssertionError("stool seated did not unlock stool_the_mitre")
    if "stool_the_mitre" in plain_case_ids:
        raise AssertionError("stool_the_mitre leaked without stool seated")
    if "stool_seated" not in sill_case.state.outcomes:
        raise AssertionError("cross sill-case run lost stool_seated")

    skirt_m = by_id["divergence_marsh_skirt"]
    skirt_c = by_id["divergence_city_skirt"]
    skirt_m_ids, skirt_c_ids = _diverge_legal(content, skirt_m, skirt_c)
    if "know_the_cope" not in skirt_m_ids:
        raise AssertionError("marsh_scout missing know_the_cope")
    if "read_the_skirting_list" not in skirt_c_ids:
        raise AssertionError("city_oath missing read_the_skirting_list")
    if "know_the_cope" in skirt_c_ids or "read_the_skirting_list" in skirt_m_ids:
        raise AssertionError("skirting sheet verbs leaked across sheets")

    plain_skirt = replay(content, by_id["cross_plain_skirt"]["seed"], by_id["cross_plain_skirt"]["sheet"], by_id["cross_plain_skirt"]["actions"])
    case_skirt = replay(content, by_id["cross_case_skirt"]["seed"], by_id["cross_case_skirt"]["sheet"], by_id["cross_case_skirt"]["actions"])
    if plain_skirt.state.location != case_skirt.state.location:
        raise AssertionError("skirting cross-area pair left different locations")
    if plain_skirt.state.location != "skirt.cope":
        raise AssertionError("skirting cross-area pair not at skirt.cope")
    plain_skirt_ids = {a.id for a in enumerate_legal(plain_skirt.state, content)}
    case_skirt_ids = {a.id for a in enumerate_legal(case_skirt.state, content)}
    if "case_the_cope" not in case_skirt_ids:
        raise AssertionError("casing tacked did not unlock case_the_cope")
    if "case_the_cope" in plain_skirt_ids:
        raise AssertionError("case_the_cope leaked without casing tacked")
    if "casing_tacked" not in case_skirt.state.outcomes:
        raise AssertionError("cross case-skirt run lost casing_tacked")

    dado_m = by_id["divergence_marsh_dado"]
    dado_c = by_id["divergence_city_dado"]
    dado_m_ids, dado_c_ids = _diverge_legal(content, dado_m, dado_c)
    if "know_the_plough" not in dado_m_ids:
        raise AssertionError("marsh_scout missing know_the_plough")
    if "read_the_dado_list" not in dado_c_ids:
        raise AssertionError("city_oath missing read_the_dado_list")
    if "know_the_plough" in dado_c_ids or "read_the_dado_list" in dado_m_ids:
        raise AssertionError("dado sheet verbs leaked across sheets")

    plain_dado = replay(content, by_id["cross_plain_dado"]["seed"], by_id["cross_plain_dado"]["sheet"], by_id["cross_plain_dado"]["actions"])
    skirt_dado = replay(content, by_id["cross_skirt_dado"]["seed"], by_id["cross_skirt_dado"]["sheet"], by_id["cross_skirt_dado"]["actions"])
    if plain_dado.state.location != skirt_dado.state.location:
        raise AssertionError("dado cross-area pair left different locations")
    if plain_dado.state.location != "dado.plough":
        raise AssertionError("dado cross-area pair not at dado.plough")
    plain_dado_ids = {a.id for a in enumerate_legal(plain_dado.state, content)}
    skirt_dado_ids = {a.id for a in enumerate_legal(skirt_dado.state, content)}
    if "plinth_the_dado" not in skirt_dado_ids:
        raise AssertionError("plinth fixed did not unlock plinth_the_dado")
    if "plinth_the_dado" in plain_dado_ids:
        raise AssertionError("plinth_the_dado leaked without plinth fixed")
    if "plinth_fixed" not in skirt_dado.state.outcomes:
        raise AssertionError("cross skirt-dado run lost plinth_fixed")

    pic_m = by_id["divergence_marsh_pic"]
    pic_c = by_id["divergence_city_pic"]
    pic_m_ids, pic_c_ids = _diverge_legal(content, pic_m, pic_c)
    if "know_the_chalk" not in pic_m_ids:
        raise AssertionError("marsh_scout missing know_the_chalk")
    if "read_the_picture_list" not in pic_c_ids:
        raise AssertionError("city_oath missing read_the_picture_list")
    if "know_the_chalk" in pic_c_ids or "read_the_picture_list" in pic_m_ids:
        raise AssertionError("picture sheet verbs leaked across sheets")

    plain_pic = replay(content, by_id["cross_plain_pic"]["seed"], by_id["cross_plain_pic"]["sheet"], by_id["cross_plain_pic"]["actions"])
    dado_pic = replay(content, by_id["cross_dado_pic"]["seed"], by_id["cross_dado_pic"]["sheet"], by_id["cross_dado_pic"]["actions"])
    if plain_pic.state.location != dado_pic.state.location:
        raise AssertionError("picture cross-area pair left different locations")
    if plain_pic.state.location != "pic.chalk":
        raise AssertionError("picture cross-area pair not at pic.chalk")
    plain_pic_ids = {a.id for a in enumerate_legal(plain_pic.state, content)}
    dado_pic_ids = {a.id for a in enumerate_legal(dado_pic.state, content)}
    if "rail_the_chalk" not in dado_pic_ids:
        raise AssertionError("rail capped did not unlock rail_the_chalk")
    if "rail_the_chalk" in plain_pic_ids:
        raise AssertionError("rail_the_chalk leaked without rail capped")
    if "rail_capped" not in dado_pic.state.outcomes:
        raise AssertionError("cross dado-pic run lost rail_capped")

    corn_m = by_id["divergence_marsh_corn"]
    corn_c = by_id["divergence_city_corn"]
    corn_m_ids, corn_c_ids = _diverge_legal(content, corn_m, corn_c)
    if "know_the_cove" not in corn_m_ids:
        raise AssertionError("marsh_scout missing know_the_cove")
    if "read_the_cornice_list" not in corn_c_ids:
        raise AssertionError("city_oath missing read_the_cornice_list")
    if "know_the_cove" in corn_c_ids or "read_the_cornice_list" in corn_m_ids:
        raise AssertionError("cornice sheet verbs leaked across sheets")

    plain_corn = replay(content, by_id["cross_plain_corn"]["seed"], by_id["cross_plain_corn"]["sheet"], by_id["cross_plain_corn"]["actions"])
    pic_corn = replay(content, by_id["cross_pic_corn"]["seed"], by_id["cross_pic_corn"]["sheet"], by_id["cross_pic_corn"]["actions"])
    if plain_corn.state.location != pic_corn.state.location:
        raise AssertionError("cornice cross-area pair left different locations")
    if plain_corn.state.location != "corn.cove":
        raise AssertionError("cornice cross-area pair not at corn.cove")
    plain_corn_ids = {a.id for a in enumerate_legal(plain_corn.state, content)}
    pic_corn_ids = {a.id for a in enumerate_legal(pic_corn.state, content)}
    if "spring_the_cove" not in pic_corn_ids:
        raise AssertionError("rail sprung did not unlock spring_the_cove")
    if "spring_the_cove" in plain_corn_ids:
        raise AssertionError("spring_the_cove leaked without rail sprung")
    if "rail_sprung" not in pic_corn.state.outcomes:
        raise AssertionError("cross pic-corn run lost rail_sprung")

    stair_m = by_id["divergence_marsh_stair"]
    stair_c = by_id["divergence_city_stair"]
    stair_m_ids, stair_c_ids = _diverge_legal(content, stair_m, stair_c)
    if "know_the_string" not in stair_m_ids:
        raise AssertionError("marsh_scout missing know_the_string")
    if "read_the_stair_list" not in stair_c_ids:
        raise AssertionError("city_oath missing read_the_stair_list")
    if "know_the_string" in stair_c_ids or "read_the_stair_list" in stair_m_ids:
        raise AssertionError("stair sheet verbs leaked across sheets")

    plain_stair = replay(content, by_id["cross_plain_stair"]["seed"], by_id["cross_plain_stair"]["sheet"], by_id["cross_plain_stair"]["actions"])
    corn_stair = replay(content, by_id["cross_corn_stair"]["seed"], by_id["cross_corn_stair"]["sheet"], by_id["cross_corn_stair"]["actions"])
    if plain_stair.state.location != corn_stair.state.location:
        raise AssertionError("stair cross-area pair left different locations")
    if plain_stair.state.location != "stair.string":
        raise AssertionError("stair cross-area pair not at stair.string")
    plain_stair_ids = {a.id for a in enumerate_legal(plain_stair.state, content)}
    corn_stair_ids = {a.id for a in enumerate_legal(corn_stair.state, content)}
    if "float_the_string" not in corn_stair_ids:
        raise AssertionError("cornice floated did not unlock float_the_string")
    if "float_the_string" in plain_stair_ids:
        raise AssertionError("float_the_string leaked without cornice floated")
    if "cornice_floated" not in corn_stair.state.outcomes:
        raise AssertionError("cross corn-stair run lost cornice_floated")

    newel_m = by_id["divergence_marsh_newel"]
    newel_c = by_id["divergence_city_newel"]
    newel_m_ids, newel_c_ids = _diverge_legal(content, newel_m, newel_c)
    if "know_the_blank" not in newel_m_ids:
        raise AssertionError("marsh_scout missing know_the_blank")
    if "read_the_newel_list" not in newel_c_ids:
        raise AssertionError("city_oath missing read_the_newel_list")
    if "know_the_blank" in newel_c_ids or "read_the_newel_list" in newel_m_ids:
        raise AssertionError("newel sheet verbs leaked across sheets")

    plain_newel = replay(content, by_id["cross_plain_newel"]["seed"], by_id["cross_plain_newel"]["sheet"], by_id["cross_plain_newel"]["actions"])
    stair_newel = replay(content, by_id["cross_stair_newel"]["seed"], by_id["cross_stair_newel"]["sheet"], by_id["cross_stair_newel"]["actions"])
    if plain_newel.state.location != stair_newel.state.location:
        raise AssertionError("newel cross-area pair left different locations")
    if plain_newel.state.location != "newel.blank":
        raise AssertionError("newel cross-area pair not at newel.blank")
    plain_newel_ids = {a.id for a in enumerate_legal(plain_newel.state, content)}
    stair_newel_ids = {a.id for a in enumerate_legal(stair_newel.state, content)}
    if "wedge_the_blank" not in stair_newel_ids:
        raise AssertionError("riser wedged did not unlock wedge_the_blank")
    if "wedge_the_blank" in plain_newel_ids:
        raise AssertionError("wedge_the_blank leaked without riser wedged")
    if "riser_wedged" not in stair_newel.state.outcomes:
        raise AssertionError("cross stair-newel run lost riser_wedged")

    hand_m = by_id["divergence_marsh_hand"]
    hand_c = by_id["divergence_city_hand"]
    hand_m_ids, hand_c_ids = _diverge_legal(content, hand_m, hand_c)
    if "know_the_stick" not in hand_m_ids:
        raise AssertionError("marsh_scout missing know_the_stick")
    if "read_the_handrail_list" not in hand_c_ids:
        raise AssertionError("city_oath missing read_the_handrail_list")
    if "know_the_stick" in hand_c_ids or "read_the_handrail_list" in hand_m_ids:
        raise AssertionError("handrail sheet verbs leaked across sheets")

    plain_hand = replay(content, by_id["cross_plain_hand"]["seed"], by_id["cross_plain_hand"]["sheet"], by_id["cross_plain_hand"]["actions"])
    newel_hand = replay(content, by_id["cross_newel_hand"]["seed"], by_id["cross_newel_hand"]["sheet"], by_id["cross_newel_hand"]["actions"])
    if plain_hand.state.location != newel_hand.state.location:
        raise AssertionError("handrail cross-area pair left different locations")
    if plain_hand.state.location != "hand.stick":
        raise AssertionError("handrail cross-area pair not at hand.stick")
    plain_hand_ids = {a.id for a in enumerate_legal(plain_hand.state, content)}
    newel_hand_ids = {a.id for a in enumerate_legal(newel_hand.state, content)}
    if "newel_the_stick" not in newel_hand_ids:
        raise AssertionError("finial dowelled did not unlock newel_the_stick")
    if "newel_the_stick" in plain_hand_ids:
        raise AssertionError("newel_the_stick leaked without finial dowelled")
    if "finial_dowelled" not in newel_hand.state.outcomes:
        raise AssertionError("cross newel-hand run lost finial_dowelled")

    bal_m = by_id["divergence_marsh_bal"]
    bal_c = by_id["divergence_city_bal"]
    bal_m_ids, bal_c_ids = _diverge_legal(content, bal_m, bal_c)
    if "know_the_square" not in bal_m_ids:
        raise AssertionError("marsh_scout missing know_the_square")
    if "read_the_baluster_list" not in bal_c_ids:
        raise AssertionError("city_oath missing read_the_baluster_list")
    if "know_the_square" in bal_c_ids or "read_the_baluster_list" in bal_m_ids:
        raise AssertionError("baluster sheet verbs leaked across sheets")

    plain_bal = replay(content, by_id["cross_plain_bal"]["seed"], by_id["cross_plain_bal"]["sheet"], by_id["cross_plain_bal"]["actions"])
    hand_bal = replay(content, by_id["cross_hand_bal"]["seed"], by_id["cross_hand_bal"]["sheet"], by_id["cross_hand_bal"]["actions"])
    if plain_bal.state.location != hand_bal.state.location:
        raise AssertionError("baluster cross-area pair left different locations")
    if plain_bal.state.location != "bal.square":
        raise AssertionError("baluster cross-area pair not at bal.square")
    plain_bal_ids = {a.id for a in enumerate_legal(plain_bal.state, content)}
    hand_bal_ids = {a.id for a in enumerate_legal(hand_bal.state, content)}
    if "wreath_the_square" not in hand_bal_ids:
        raise AssertionError("ramp wreathed did not unlock wreath_the_square")
    if "wreath_the_square" in plain_bal_ids:
        raise AssertionError("wreath_the_square leaked without ramp wreathed")
    if "ramp_wreathed" not in hand_bal.state.outcomes:
        raise AssertionError("cross hand-bal run lost ramp_wreathed")

    tread_m = by_id["divergence_marsh_tread"]
    tread_c = by_id["divergence_city_tread"]
    tread_m_ids, tread_c_ids = _diverge_legal(content, tread_m, tread_c)
    if "know_the_going" not in tread_m_ids:
        raise AssertionError("marsh_scout missing know_the_going")
    if "read_the_tread_list" not in tread_c_ids:
        raise AssertionError("city_oath missing read_the_tread_list")
    if "know_the_going" in tread_c_ids or "read_the_tread_list" in tread_m_ids:
        raise AssertionError("tread sheet verbs leaked across sheets")

    plain_tread = replay(content, by_id["cross_plain_tread"]["seed"], by_id["cross_plain_tread"]["sheet"], by_id["cross_plain_tread"]["actions"])
    bal_tread = replay(content, by_id["cross_bal_tread"]["seed"], by_id["cross_bal_tread"]["sheet"], by_id["cross_bal_tread"]["actions"])
    if plain_tread.state.location != bal_tread.state.location:
        raise AssertionError("tread cross-area pair left different locations")
    if plain_tread.state.location != "tread.going":
        raise AssertionError("tread cross-area pair not at tread.going")
    plain_tread_ids = {a.id for a in enumerate_legal(plain_tread.state, content)}
    bal_tread_ids = {a.id for a in enumerate_legal(bal_tread.state, content)}
    if "shoulder_the_going" not in bal_tread_ids:
        raise AssertionError("neck shouldered did not unlock shoulder_the_going")
    if "shoulder_the_going" in plain_tread_ids:
        raise AssertionError("shoulder_the_going leaked without neck shouldered")
    if "neck_shouldered" not in bal_tread.state.outcomes:
        raise AssertionError("cross bal-tread run lost neck_shouldered")

    floor_m = by_id["divergence_marsh_floor"]
    floor_c = by_id["divergence_city_floor"]
    floor_m_ids, floor_c_ids = _diverge_legal(content, floor_m, floor_c)
    if "know_the_shot" not in floor_m_ids:
        raise AssertionError("marsh_scout missing know_the_shot")
    if "read_the_floor_list" not in floor_c_ids:
        raise AssertionError("city_oath missing read_the_floor_list")
    if "know_the_shot" in floor_c_ids or "read_the_floor_list" in floor_m_ids:
        raise AssertionError("floor sheet verbs leaked across sheets")

    plain_floor = replay(content, by_id["cross_plain_floor"]["seed"], by_id["cross_plain_floor"]["sheet"], by_id["cross_plain_floor"]["actions"])
    tread_floor = replay(content, by_id["cross_tread_floor"]["seed"], by_id["cross_tread_floor"]["sheet"], by_id["cross_tread_floor"]["actions"])
    if plain_floor.state.location != tread_floor.state.location:
        raise AssertionError("floor cross-area pair left different locations")
    if plain_floor.state.location != "floor.shot":
        raise AssertionError("floor cross-area pair not at floor.shot")
    plain_floor_ids = {a.id for a in enumerate_legal(plain_floor.state, content)}
    tread_floor_ids = {a.id for a in enumerate_legal(tread_floor.state, content)}
    if "return_the_shot" not in tread_floor_ids:
        raise AssertionError("end returned did not unlock return_the_shot")
    if "return_the_shot" in plain_floor_ids:
        raise AssertionError("return_the_shot leaked without end returned")
    if "end_returned" not in tread_floor.state.outcomes:
        raise AssertionError("cross tread-floor run lost end_returned")

    joist_m = by_id["divergence_marsh_joist"]
    joist_c = by_id["divergence_city_joist"]
    joist_m_ids, joist_c_ids = _diverge_legal(content, joist_m, joist_c)
    if "know_the_span" not in joist_m_ids:
        raise AssertionError("marsh_scout missing know_the_span")
    if "read_the_joist_list" not in joist_c_ids:
        raise AssertionError("city_oath missing read_the_joist_list")
    if "know_the_span" in joist_c_ids or "read_the_joist_list" in joist_m_ids:
        raise AssertionError("joist sheet verbs leaked across sheets")

    plain_joist = replay(content, by_id["cross_plain_joist"]["seed"], by_id["cross_plain_joist"]["sheet"], by_id["cross_plain_joist"]["actions"])
    floor_joist = replay(content, by_id["cross_floor_joist"]["seed"], by_id["cross_floor_joist"]["sheet"], by_id["cross_floor_joist"]["actions"])
    if plain_joist.state.location != floor_joist.state.location:
        raise AssertionError("joist cross-area pair left different locations")
    if plain_joist.state.location != "joist.space":
        raise AssertionError("joist cross-area pair not at joist.space")
    plain_joist_ids = {a.id for a in enumerate_legal(plain_joist.state, content)}
    floor_joist_ids = {a.id for a in enumerate_legal(floor_joist.state, content)}
    if "board_the_span" not in floor_joist_ids:
        raise AssertionError("nail secreted did not unlock board_the_span")
    if "board_the_span" in plain_joist_ids:
        raise AssertionError("board_the_span leaked without nail secreted")
    if "nail_secreted" not in floor_joist.state.outcomes:
        raise AssertionError("cross floor-joist run lost nail_secreted")

    lath_m = by_id["divergence_marsh_lath"]
    lath_c = by_id["divergence_city_lath"]
    lath_m_ids, lath_c_ids = _diverge_legal(content, lath_m, lath_c)
    if "know_the_rive" not in lath_m_ids:
        raise AssertionError("marsh_scout missing know_the_rive")
    if "read_the_lath_list" not in lath_c_ids:
        raise AssertionError("city_oath missing read_the_lath_list")
    if "know_the_rive" in lath_c_ids or "read_the_lath_list" in lath_m_ids:
        raise AssertionError("lath sheet verbs leaked across sheets")

    plain_lath = replay(content, by_id["cross_plain_lath"]["seed"], by_id["cross_plain_lath"]["sheet"], by_id["cross_plain_lath"]["actions"])
    joist_lath = replay(content, by_id["cross_joist_lath"]["seed"], by_id["cross_joist_lath"]["sheet"], by_id["cross_joist_lath"]["actions"])
    if plain_lath.state.location != joist_lath.state.location:
        raise AssertionError("lath cross-area pair left different locations")
    if plain_lath.state.location != "lath.rive":
        raise AssertionError("lath cross-area pair not at lath.rive")
    plain_lath_ids = {a.id for a in enumerate_legal(plain_lath.state, content)}
    joist_lath_ids = {a.id for a in enumerate_legal(joist_lath.state, content)}
    if "crown_the_rive" not in joist_lath_ids:
        raise AssertionError("camber crowned did not unlock crown_the_rive")
    if "crown_the_rive" in plain_lath_ids:
        raise AssertionError("crown_the_rive leaked without camber crowned")
    if "camber_crowned" not in joist_lath.state.outcomes:
        raise AssertionError("cross joist-lath run lost camber_crowned")

    chim_m = by_id["divergence_marsh_chim"]
    chim_c = by_id["divergence_city_chim"]
    chim_m_ids, chim_c_ids = _diverge_legal(content, chim_m, chim_c)
    if "know_the_flag" not in chim_m_ids:
        raise AssertionError("marsh_scout missing know_the_flag")
    if "read_the_chimney_list" not in chim_c_ids:
        raise AssertionError("city_oath missing read_the_chimney_list")
    if "know_the_flag" in chim_c_ids or "read_the_chimney_list" in chim_m_ids:
        raise AssertionError("chimney sheet verbs leaked across sheets")

    plain_chim = replay(content, by_id["cross_plain_chim"]["seed"], by_id["cross_plain_chim"]["sheet"], by_id["cross_plain_chim"]["actions"])
    lath_chim = replay(content, by_id["cross_lath_chim"]["seed"], by_id["cross_lath_chim"]["sheet"], by_id["cross_lath_chim"]["actions"])
    if plain_chim.state.location != lath_chim.state.location:
        raise AssertionError("chimney cross-area pair left different locations")
    if plain_chim.state.location != "chim.flag":
        raise AssertionError("chimney cross-area pair not at chim.flag")
    plain_chim_ids = {a.id for a in enumerate_legal(plain_chim.state, content)}
    lath_chim_ids = {a.id for a in enumerate_legal(lath_chim.state, content)}
    if "hair_the_flag" not in lath_chim_ids:
        raise AssertionError("coat haired did not unlock hair_the_flag")
    if "hair_the_flag" in plain_chim_ids:
        raise AssertionError("hair_the_flag leaked without coat haired")
    if "coat_haired" not in lath_chim.state.outcomes:
        raise AssertionError("cross lath-chim run lost coat_haired")

    mant_m = by_id["divergence_marsh_mant"]
    mant_c = by_id["divergence_city_mant"]
    mant_m_ids, mant_c_ids = _diverge_legal(content, mant_m, mant_c)
    if "know_the_lintel" not in mant_m_ids:
        raise AssertionError("marsh_scout missing know_the_lintel")
    if "read_the_mantel_list" not in mant_c_ids:
        raise AssertionError("city_oath missing read_the_mantel_list")
    if "know_the_lintel" in mant_c_ids or "read_the_mantel_list" in mant_m_ids:
        raise AssertionError("mantel sheet verbs leaked across sheets")

    plain_mant = replay(content, by_id["cross_plain_mant"]["seed"], by_id["cross_plain_mant"]["sheet"], by_id["cross_plain_mant"]["actions"])
    chim_mant = replay(content, by_id["cross_chim_mant"]["seed"], by_id["cross_chim_mant"]["sheet"], by_id["cross_chim_mant"]["actions"])
    if plain_mant.state.location != chim_mant.state.location:
        raise AssertionError("mantel cross-area pair left different locations")
    if plain_mant.state.location != "mant.lintel":
        raise AssertionError("mantel cross-area pair not at mant.lintel")
    plain_mant_ids = {a.id for a in enumerate_legal(plain_mant.state, content)}
    chim_mant_ids = {a.id for a in enumerate_legal(chim_mant.state, content)}
    if "lime_the_lintel" not in chim_mant_ids:
        raise AssertionError("breast limed did not unlock lime_the_lintel")
    if "lime_the_lintel" in plain_mant_ids:
        raise AssertionError("lime_the_lintel leaked without breast limed")
    if "breast_limed" not in chim_mant.state.outcomes:
        raise AssertionError("cross chim-mant run lost breast_limed")

    flue_m = by_id["divergence_marsh_flue"]
    flue_c = by_id["divergence_city_flue"]
    flue_m_ids, flue_c_ids = _diverge_legal(content, flue_m, flue_c)
    if "know_the_parge" not in flue_m_ids:
        raise AssertionError("marsh_scout missing know_the_parge")
    if "read_the_flue_list" not in flue_c_ids:
        raise AssertionError("city_oath missing read_the_flue_list")
    if "know_the_parge" in flue_c_ids or "read_the_flue_list" in flue_m_ids:
        raise AssertionError("flue sheet verbs leaked across sheets")

    plain_flue = replay(content, by_id["cross_plain_flue"]["seed"], by_id["cross_plain_flue"]["sheet"], by_id["cross_plain_flue"]["actions"])
    mant_flue = replay(content, by_id["cross_mant_flue"]["seed"], by_id["cross_mant_flue"]["sheet"], by_id["cross_mant_flue"]["actions"])
    if plain_flue.state.location != mant_flue.state.location:
        raise AssertionError("flue cross-area pair left different locations")
    if plain_flue.state.location != "flue.parge":
        raise AssertionError("flue cross-area pair not at flue.parge")
    plain_flue_ids = {a.id for a in enumerate_legal(plain_flue.state, content)}
    mant_flue_ids = {a.id for a in enumerate_legal(mant_flue.state, content)}
    if "pin_the_parge" not in mant_flue_ids:
        raise AssertionError("mantel pinned did not unlock pin_the_parge")
    if "pin_the_parge" in plain_flue_ids:
        raise AssertionError("pin_the_parge leaked without mantel pinned")
    if "mantel_pinned" not in mant_flue.state.outcomes:
        raise AssertionError("cross mant-flue run lost mantel_pinned")

    fb_m = by_id["divergence_marsh_fb"]
    fb_c = by_id["divergence_city_fb"]
    fb_m_ids, fb_c_ids = _diverge_legal(content, fb_m, fb_c)
    if "know_the_sand" not in fb_m_ids:
        raise AssertionError("marsh_scout missing know_the_sand")
    if "read_the_fireback_list" not in fb_c_ids:
        raise AssertionError("city_oath missing read_the_fireback_list")
    if "know_the_sand" in fb_c_ids or "read_the_fireback_list" in fb_m_ids:
        raise AssertionError("fireback sheet verbs leaked across sheets")

    plain_fb = replay(content, by_id["cross_plain_fb"]["seed"], by_id["cross_plain_fb"]["sheet"], by_id["cross_plain_fb"]["actions"])
    flue_fb = replay(content, by_id["cross_flue_fb"]["seed"], by_id["cross_flue_fb"]["sheet"], by_id["cross_flue_fb"]["actions"])
    if plain_fb.state.location != flue_fb.state.location:
        raise AssertionError("fireback cross-area pair left different locations")
    if plain_fb.state.location != "fb.sand":
        raise AssertionError("fireback cross-area pair not at fb.sand")
    plain_fb_ids = {a.id for a in enumerate_legal(plain_fb.state, content)}
    flue_fb_ids = {a.id for a in enumerate_legal(flue_fb.state, content)}
    if "cowl_the_mould" not in flue_fb_ids:
        raise AssertionError("cowl hung did not unlock cowl_the_mould")
    if "cowl_the_mould" in plain_fb_ids:
        raise AssertionError("cowl_the_mould leaked without cowl hung")
    if "cowl_hung" not in flue_fb.state.outcomes:
        raise AssertionError("cross flue-fb run lost cowl_hung")

    grate_m = by_id["divergence_marsh_grate"]
    grate_c = by_id["divergence_city_grate"]
    grate_m_ids, grate_c_ids = _diverge_legal(content, grate_m, grate_c)
    if "know_the_swage" not in grate_m_ids:
        raise AssertionError("marsh_scout missing know_the_swage")
    if "read_the_grate_list" not in grate_c_ids:
        raise AssertionError("city_oath missing read_the_grate_list")
    if "know_the_swage" in grate_c_ids or "read_the_grate_list" in grate_m_ids:
        raise AssertionError("grate sheet verbs leaked across sheets")

    plain_grate = replay(content, by_id["cross_plain_grate"]["seed"], by_id["cross_plain_grate"]["sheet"], by_id["cross_plain_grate"]["actions"])
    fb_grate = replay(content, by_id["cross_fb_grate"]["seed"], by_id["cross_fb_grate"]["sheet"], by_id["cross_fb_grate"]["actions"])
    if plain_grate.state.location != fb_grate.state.location:
        raise AssertionError("grate cross-area pair left different locations")
    if plain_grate.state.location != "grate.swage":
        raise AssertionError("grate cross-area pair not at grate.swage")
    plain_grate_ids = {a.id for a in enumerate_legal(plain_grate.state, content)}
    fb_grate_ids = {a.id for a in enumerate_legal(fb_grate.state, content)}
    if "bed_the_swage" not in fb_grate_ids:
        raise AssertionError("back bedded did not unlock bed_the_swage")
    if "bed_the_swage" in plain_grate_ids:
        raise AssertionError("bed_the_swage leaked without back bedded")
    if "back_bedded" not in fb_grate.state.outcomes:
        raise AssertionError("cross fb-grate run lost back_bedded")

    brick_m = by_id["divergence_marsh_brick"]
    brick_c = by_id["divergence_city_brick"]
    brick_m_ids, brick_c_ids = _diverge_legal(content, brick_m, brick_c)
    if "know_the_pug" not in brick_m_ids:
        raise AssertionError("marsh_scout missing know_the_pug")
    if "read_the_brick_list" not in brick_c_ids:
        raise AssertionError("city_oath missing read_the_brick_list")
    if "know_the_pug" in brick_c_ids or "read_the_brick_list" in brick_m_ids:
        raise AssertionError("brick sheet verbs leaked across sheets")

    plain_brick = replay(content, by_id["cross_plain_brick"]["seed"], by_id["cross_plain_brick"]["sheet"], by_id["cross_plain_brick"]["actions"])
    grate_brick = replay(content, by_id["cross_grate_brick"]["seed"], by_id["cross_grate_brick"]["sheet"], by_id["cross_grate_brick"]["actions"])
    if plain_brick.state.location != grate_brick.state.location:
        raise AssertionError("brick cross-area pair left different locations")
    if plain_brick.state.location != "brick.pug":
        raise AssertionError("brick cross-area pair not at brick.pug")
    plain_brick_ids = {a.id for a in enumerate_legal(plain_brick.state, content)}
    grate_brick_ids = {a.id for a in enumerate_legal(grate_brick.state, content)}
    if "grate_the_pug" not in grate_brick_ids:
        raise AssertionError("slide registered did not unlock grate_the_pug")
    if "grate_the_pug" in plain_brick_ids:
        raise AssertionError("grate_the_pug leaked without slide registered")
    if "slide_registered" not in grate_brick.state.outcomes:
        raise AssertionError("cross grate-brick run lost slide_registered")

    tile_m = by_id["divergence_marsh_tile"]
    tile_c = by_id["divergence_city_tile"]
    tile_m_ids, tile_c_ids = _diverge_legal(content, tile_m, tile_c)
    if "know_the_horse" not in tile_m_ids:
        raise AssertionError("marsh_scout missing know_the_horse")
    if "read_the_tile_list" not in tile_c_ids:
        raise AssertionError("city_oath missing read_the_tile_list")
    if "know_the_horse" in tile_c_ids or "read_the_tile_list" in tile_m_ids:
        raise AssertionError("tile sheet verbs leaked across sheets")

    plain_tile = replay(content, by_id["cross_plain_tile"]["seed"], by_id["cross_plain_tile"]["sheet"], by_id["cross_plain_tile"]["actions"])
    brick_tile = replay(content, by_id["cross_brick_tile"]["seed"], by_id["cross_brick_tile"]["sheet"], by_id["cross_brick_tile"]["actions"])
    if plain_tile.state.location != brick_tile.state.location:
        raise AssertionError("tile cross-area pair left different locations")
    if plain_tile.state.location != "tile.horse":
        raise AssertionError("tile cross-area pair not at tile.horse")
    plain_tile_ids = {a.id for a in enumerate_legal(plain_tile.state, content)}
    brick_tile_ids = {a.id for a in enumerate_legal(brick_tile.state, content)}
    if "hack_the_horse" not in brick_tile_ids:
        raise AssertionError("hack set did not unlock hack_the_horse")
    if "hack_the_horse" in plain_tile_ids:
        raise AssertionError("hack_the_horse leaked without hack set")
    if "hack_set" not in brick_tile.state.outcomes:
        raise AssertionError("cross brick-tile run lost hack_set")

    slate_m = by_id["divergence_marsh_slate"]
    slate_c = by_id["divergence_city_slate"]
    slate_m_ids, slate_c_ids = _diverge_legal(content, slate_m, slate_c)
    if "know_the_scapple" not in slate_m_ids:
        raise AssertionError("marsh_scout missing know_the_scapple")
    if "read_the_slate_list" not in slate_c_ids:
        raise AssertionError("city_oath missing read_the_slate_list")
    if "know_the_scapple" in slate_c_ids or "read_the_slate_list" in slate_m_ids:
        raise AssertionError("slate sheet verbs leaked across sheets")

    plain_slate = replay(content, by_id["cross_plain_slate"]["seed"], by_id["cross_plain_slate"]["sheet"], by_id["cross_plain_slate"]["actions"])
    tile_slate = replay(content, by_id["cross_tile_slate"]["seed"], by_id["cross_tile_slate"]["sheet"], by_id["cross_tile_slate"]["actions"])
    if plain_slate.state.location != tile_slate.state.location:
        raise AssertionError("slate cross-area pair left different locations")
    if plain_slate.state.location != "slate.scapple":
        raise AssertionError("slate cross-area pair not at slate.scapple")
    plain_slate_ids = {a.id for a in enumerate_legal(plain_slate.state, content)}
    tile_slate_ids = {a.id for a in enumerate_legal(tile_slate.state, content)}
    if "arris_the_face" not in tile_slate_ids:
        raise AssertionError("arris nicked did not unlock arris_the_face")
    if "arris_the_face" in plain_slate_ids:
        raise AssertionError("arris_the_face leaked without arris nicked")
    if "arris_nicked" not in tile_slate.state.outcomes:
        raise AssertionError("cross tile-slate run lost arris_nicked")

    flash_m = by_id["divergence_marsh_flash"]
    flash_c = by_id["divergence_city_flash"]
    flash_m_ids, flash_c_ids = _diverge_legal(content, flash_m, flash_c)
    if "know_the_roll" not in flash_m_ids:
        raise AssertionError("marsh_scout missing know_the_roll")
    if "read_the_flash_list" not in flash_c_ids:
        raise AssertionError("city_oath missing read_the_flash_list")
    if "know_the_roll" in flash_c_ids or "read_the_flash_list" in flash_m_ids:
        raise AssertionError("flash sheet verbs leaked across sheets")

    plain_flash = replay(content, by_id["cross_plain_flash"]["seed"], by_id["cross_plain_flash"]["sheet"], by_id["cross_plain_flash"]["actions"])
    slate_flash = replay(content, by_id["cross_slate_flash"]["seed"], by_id["cross_slate_flash"]["sheet"], by_id["cross_slate_flash"]["actions"])
    if plain_flash.state.location != slate_flash.state.location:
        raise AssertionError("flash cross-area pair left different locations")
    if plain_flash.state.location != "flash.sheet":
        raise AssertionError("flash cross-area pair not at flash.sheet")
    plain_flash_ids = {a.id for a in enumerate_legal(plain_flash.state, content)}
    slate_flash_ids = {a.id for a in enumerate_legal(slate_flash.state, content)}
    if "lap_the_sheet" not in slate_flash_ids:
        raise AssertionError("slate lapped did not unlock lap_the_sheet")
    if "lap_the_sheet" in plain_flash_ids:
        raise AssertionError("lap_the_sheet leaked without slate lapped")
    if "slate_lapped" not in slate_flash.state.outcomes:
        raise AssertionError("cross slate-flash run lost slate_lapped")

    block_m = by_id["divergence_marsh_block"]
    block_c = by_id["divergence_city_block"]
    block_m_ids, block_c_ids = _diverge_legal(content, block_m, block_c)
    if "know_the_cheek" not in block_m_ids:
        raise AssertionError("marsh_scout missing know_the_cheek")
    if "read_the_block_list" not in block_c_ids:
        raise AssertionError("city_oath missing read_the_block_list")
    if "know_the_cheek" in block_c_ids or "read_the_block_list" in block_m_ids:
        raise AssertionError("block sheet verbs leaked across sheets")

    plain_block = replay(content, by_id["cross_plain_block"]["seed"], by_id["cross_plain_block"]["sheet"], by_id["cross_plain_block"]["actions"])
    flash_block = replay(content, by_id["cross_flash_block"]["seed"], by_id["cross_flash_block"]["sheet"], by_id["cross_flash_block"]["actions"])
    if plain_block.state.location != flash_block.state.location:
        raise AssertionError("block cross-area pair left different locations")
    if plain_block.state.location != "block.cheek":
        raise AssertionError("block cross-area pair not at block.cheek")
    plain_block_ids = {a.id for a in enumerate_legal(plain_block.state, content)}
    flash_block_ids = {a.id for a in enumerate_legal(flash_block.state, content)}
    if "dress_the_cheek" not in flash_block_ids:
        raise AssertionError("flash dressed did not unlock dress_the_cheek")
    if "dress_the_cheek" in plain_block_ids:
        raise AssertionError("dress_the_cheek leaked without flash dressed")
    if "flash_dressed" not in flash_block.state.outcomes:
        raise AssertionError("cross flash-block run lost flash_dressed")

    oar_m = by_id["divergence_marsh_oar"]
    oar_c = by_id["divergence_city_oar"]
    oar_m_ids, oar_c_ids = _diverge_legal(content, oar_m, oar_c)
    if "know_the_shaft" not in oar_m_ids:
        raise AssertionError("marsh_scout missing know_the_shaft")
    if "read_the_oar_list" not in oar_c_ids:
        raise AssertionError("city_oath missing read_the_oar_list")
    if "know_the_shaft" in oar_c_ids or "read_the_oar_list" in oar_m_ids:
        raise AssertionError("oar sheet verbs leaked across sheets")

    plain_oar = replay(content, by_id["cross_plain_oar"]["seed"], by_id["cross_plain_oar"]["sheet"], by_id["cross_plain_oar"]["actions"])
    block_oar = replay(content, by_id["cross_block_oar"]["seed"], by_id["cross_block_oar"]["sheet"], by_id["cross_block_oar"]["actions"])
    if plain_oar.state.location != block_oar.state.location:
        raise AssertionError("oar cross-area pair left different locations")
    if plain_oar.state.location != "oar.shaft":
        raise AssertionError("oar cross-area pair not at oar.shaft")
    plain_oar_ids = {a.id for a in enumerate_legal(plain_oar.state, content)}
    block_oar_ids = {a.id for a in enumerate_legal(block_oar.state, content)}
    if "strop_the_shaft" not in block_oar_ids:
        raise AssertionError("block stropped did not unlock strop_the_shaft")
    if "strop_the_shaft" in plain_oar_ids:
        raise AssertionError("strop_the_shaft leaked without block stropped")
    if "block_stropped" not in block_oar.state.outcomes:
        raise AssertionError("cross block-oar run lost block_stropped")

    ways_m = by_id["divergence_marsh_ways"]
    ways_c = by_id["divergence_city_ways"]
    ways_m_ids, ways_c_ids = _diverge_legal(content, ways_m, ways_c)
    if "know_the_grease" not in ways_m_ids:
        raise AssertionError("marsh_scout missing know_the_grease")
    if "read_the_ways_list" not in ways_c_ids:
        raise AssertionError("city_oath missing read_the_ways_list")
    if "know_the_grease" in ways_c_ids or "read_the_ways_list" in ways_m_ids:
        raise AssertionError("ways sheet verbs leaked across sheets")

    plain_ways = replay(content, by_id["cross_plain_ways"]["seed"], by_id["cross_plain_ways"]["sheet"], by_id["cross_plain_ways"]["actions"])
    oar_ways = replay(content, by_id["cross_oar_ways"]["seed"], by_id["cross_oar_ways"]["sheet"], by_id["cross_oar_ways"]["actions"])
    if plain_ways.state.location != oar_ways.state.location:
        raise AssertionError("ways cross-area pair left different locations")
    if plain_ways.state.location != "ways.grease":
        raise AssertionError("ways cross-area pair not at ways.grease")
    plain_ways_ids = {a.id for a in enumerate_legal(plain_ways.state, content)}
    oar_ways_ids = {a.id for a in enumerate_legal(oar_ways.state, content)}
    if "grip_the_grease" not in oar_ways_ids:
        raise AssertionError("grip bound did not unlock grip_the_grease")
    if "grip_the_grease" in plain_ways_ids:
        raise AssertionError("grip_the_grease leaked without grip bound")
    if "grip_bound" not in oar_ways.state.outcomes:
        raise AssertionError("cross oar-ways run lost grip_bound")

    clink_m = by_id["divergence_marsh_clink"]
    clink_c = by_id["divergence_city_clink"]
    clink_m_ids, clink_c_ids = _diverge_legal(content, clink_m, clink_c)
    if "know_the_steam" not in clink_m_ids:
        raise AssertionError("marsh_scout missing know_the_steam")
    if "read_the_clinker_list" not in clink_c_ids:
        raise AssertionError("city_oath missing read_the_clinker_list")
    if "know_the_steam" in clink_c_ids or "read_the_clinker_list" in clink_m_ids:
        raise AssertionError("clink sheet verbs leaked across sheets")

    plain_clink = replay(content, by_id["cross_plain_clink"]["seed"], by_id["cross_plain_clink"]["sheet"], by_id["cross_plain_clink"]["actions"])
    ways_clink = replay(content, by_id["cross_ways_clink"]["seed"], by_id["cross_ways_clink"]["sheet"], by_id["cross_ways_clink"]["actions"])
    if plain_clink.state.location != ways_clink.state.location:
        raise AssertionError("clink cross-area pair left different locations")
    if plain_clink.state.location != "clink.steam":
        raise AssertionError("clink cross-area pair not at clink.steam")
    plain_clink_ids = {a.id for a in enumerate_legal(plain_clink.state, content)}
    ways_clink_ids = {a.id for a in enumerate_legal(ways_clink.state, content)}
    if "launch_the_steam" not in ways_clink_ids:
        raise AssertionError("hull launched did not unlock launch_the_steam")
    if "launch_the_steam" in plain_clink_ids:
        raise AssertionError("launch_the_steam leaked without hull launched")
    if "hull_launched" not in ways_clink.state.outcomes:
        raise AssertionError("cross ways-clink run lost hull_launched")

    wind_m = by_id["divergence_marsh_wind"]
    wind_c = by_id["divergence_city_wind"]
    wind_m_ids, wind_c_ids = _diverge_legal(content, wind_m, wind_c)
    if "know_the_bars" not in wind_m_ids:
        raise AssertionError("marsh_scout missing know_the_bars")
    if "read_the_windlass_list" not in wind_c_ids:
        raise AssertionError("city_oath missing read_the_windlass_list")
    if "know_the_bars" in wind_c_ids or "read_the_windlass_list" in wind_m_ids:
        raise AssertionError("wind sheet verbs leaked across sheets")

    plain_wind = replay(content, by_id["cross_plain_wind"]["seed"], by_id["cross_plain_wind"]["sheet"], by_id["cross_plain_wind"]["actions"])
    clink_wind = replay(content, by_id["cross_clink_wind"]["seed"], by_id["cross_clink_wind"]["sheet"], by_id["cross_clink_wind"]["actions"])
    if plain_wind.state.location != clink_wind.state.location:
        raise AssertionError("wind cross-area pair left different locations")
    if plain_wind.state.location != "wind.bars":
        raise AssertionError("wind cross-area pair not at wind.bars")
    plain_wind_ids = {a.id for a in enumerate_legal(plain_wind.state, content)}
    clink_wind_ids = {a.id for a in enumerate_legal(clink_wind.state, content)}
    if "fair_the_bars" not in clink_wind_ids:
        raise AssertionError("garboard faired did not unlock fair_the_bars")
    if "fair_the_bars" in plain_wind_ids:
        raise AssertionError("fair_the_bars leaked without garboard faired")
    if "garboard_faired" not in clink_wind.state.outcomes:
        raise AssertionError("cross clink-wind run lost garboard_faired")

    offs_m = by_id["divergence_marsh_offs"]
    offs_c = by_id["divergence_city_offs"]
    offs_m_ids, offs_c_ids = _diverge_legal(content, offs_m, offs_c)
    if "know_the_grid" not in offs_m_ids:
        raise AssertionError("marsh_scout missing know_the_grid")
    if "read_the_offset_list" not in offs_c_ids:
        raise AssertionError("city_oath missing read_the_offset_list")
    if "know_the_grid" in offs_c_ids or "read_the_offset_list" in offs_m_ids:
        raise AssertionError("offs sheet verbs leaked across sheets")

    plain_offs = replay(content, by_id["cross_plain_offs"]["seed"], by_id["cross_plain_offs"]["sheet"], by_id["cross_plain_offs"]["actions"])
    wind_offs = replay(content, by_id["cross_wind_offs"]["seed"], by_id["cross_wind_offs"]["sheet"], by_id["cross_wind_offs"]["actions"])
    if plain_offs.state.location != wind_offs.state.location:
        raise AssertionError("offs cross-area pair left different locations")
    if plain_offs.state.location != "offs.grid":
        raise AssertionError("offs cross-area pair not at offs.grid")
    plain_offs_ids = {a.id for a in enumerate_legal(plain_offs.state, content)}
    wind_offs_ids = {a.id for a in enumerate_legal(wind_offs.state, content)}
    if "heave_the_grid" not in wind_offs_ids:
        raise AssertionError("round heaved did not unlock heave_the_grid")
    if "heave_the_grid" in plain_offs_ids:
        raise AssertionError("heave_the_grid leaked without round heaved")
    if "round_heaved" not in wind_offs.state.outcomes:
        raise AssertionError("cross wind-offs run lost round_heaved")

    trun_m = by_id["divergence_marsh_trun"]
    trun_c = by_id["divergence_city_trun"]
    trun_m_ids, trun_c_ids = _diverge_legal(content, trun_m, trun_c)
    if "know_the_billet" not in trun_m_ids:
        raise AssertionError("marsh_scout missing know_the_billet")
    if "read_the_trunnel_list" not in trun_c_ids:
        raise AssertionError("city_oath missing read_the_trunnel_list")
    if "know_the_billet" in trun_c_ids or "read_the_trunnel_list" in trun_m_ids:
        raise AssertionError("trun sheet verbs leaked across sheets")

    plain_trun = replay(content, by_id["cross_plain_trun"]["seed"], by_id["cross_plain_trun"]["sheet"], by_id["cross_plain_trun"]["actions"])
    offs_trun = replay(content, by_id["cross_offs_trun"]["seed"], by_id["cross_offs_trun"]["sheet"], by_id["cross_offs_trun"]["actions"])
    if plain_trun.state.location != offs_trun.state.location:
        raise AssertionError("trun cross-area pair left different locations")
    if plain_trun.state.location != "trun.billet":
        raise AssertionError("trun cross-area pair not at trun.billet")
    plain_trun_ids = {a.id for a in enumerate_legal(plain_trun.state, content)}
    offs_trun_ids = {a.id for a in enumerate_legal(offs_trun.state, content)}
    if "bevel_the_billet" not in offs_trun_ids:
        raise AssertionError("station bevelled did not unlock bevel_the_billet")
    if "bevel_the_billet" in plain_trun_ids:
        raise AssertionError("bevel_the_billet leaked without station bevelled")
    if "station_bevelled" not in offs_trun.state.outcomes:
        raise AssertionError("cross offs-trun run lost station_bevelled")

    dead_m = by_id["divergence_marsh_dead"]
    dead_c = by_id["divergence_city_dead"]
    dead_m_ids, dead_c_ids = _diverge_legal(content, dead_m, dead_c)
    if "know_the_dub" not in dead_m_ids:
        raise AssertionError("marsh_scout missing know_the_dub")
    if "read_the_deadwood_list" not in dead_c_ids:
        raise AssertionError("city_oath missing read_the_deadwood_list")
    if "know_the_dub" in dead_c_ids or "read_the_deadwood_list" in dead_m_ids:
        raise AssertionError("dead sheet verbs leaked across sheets")

    plain_dead = replay(content, by_id["cross_plain_dead"]["seed"], by_id["cross_plain_dead"]["sheet"], by_id["cross_plain_dead"]["actions"])
    trun_dead = replay(content, by_id["cross_trun_dead"]["seed"], by_id["cross_trun_dead"]["sheet"], by_id["cross_trun_dead"]["actions"])
    if plain_dead.state.location != trun_dead.state.location:
        raise AssertionError("dead cross-area pair left different locations")
    if plain_dead.state.location != "dead.dub":
        raise AssertionError("dead cross-area pair not at dead.dub")
    plain_dead_ids = {a.id for a in enumerate_legal(plain_dead.state, content)}
    trun_dead_ids = {a.id for a in enumerate_legal(trun_dead.state, content)}
    if "drive_the_dub" not in trun_dead_ids:
        raise AssertionError("trunnel driven did not unlock drive_the_dub")
    if "drive_the_dub" in plain_dead_ids:
        raise AssertionError("drive_the_dub leaked without trunnel driven")
    if "trunnel_driven" not in trun_dead.state.outcomes:
        raise AssertionError("cross trun-dead run lost trunnel_driven")

    mast_m = by_id["divergence_marsh_mast"]
    mast_c = by_id["divergence_city_mast"]
    mast_m_ids, mast_c_ids = _diverge_legal(content, mast_m, mast_c)
    if "know_the_sink" not in mast_m_ids:
        raise AssertionError("marsh_scout missing know_the_sink")
    if "read_the_mast_list" not in mast_c_ids:
        raise AssertionError("city_oath missing read_the_mast_list")
    if "know_the_sink" in mast_c_ids or "read_the_mast_list" in mast_m_ids:
        raise AssertionError("mast sheet verbs leaked across sheets")

    plain_mast = replay(content, by_id["cross_plain_mast"]["seed"], by_id["cross_plain_mast"]["sheet"], by_id["cross_plain_mast"]["actions"])
    dead_mast = replay(content, by_id["cross_dead_mast"]["seed"], by_id["cross_dead_mast"]["sheet"], by_id["cross_dead_mast"]["actions"])
    if plain_mast.state.location != dead_mast.state.location:
        raise AssertionError("mast cross-area pair left different locations")
    if plain_mast.state.location != "mast.sink":
        raise AssertionError("mast cross-area pair not at mast.sink")
    plain_mast_ids = {a.id for a in enumerate_legal(plain_mast.state, content)}
    dead_mast_ids = {a.id for a in enumerate_legal(dead_mast.state, content)}
    if "bolt_the_sink" not in dead_mast_ids:
        raise AssertionError("hog bolted did not unlock bolt_the_sink")
    if "bolt_the_sink" in plain_mast_ids:
        raise AssertionError("bolt_the_sink leaked without hog bolted")
    if "hog_bolted" not in dead_mast.state.outcomes:
        raise AssertionError("cross dead-mast run lost hog_bolted")

    stem_m = by_id["divergence_marsh_stem"]
    stem_c = by_id["divergence_city_stem"]
    stem_m_ids, stem_c_ids = _diverge_legal(content, stem_m, stem_c)
    if "know_the_hew" not in stem_m_ids:
        raise AssertionError("marsh_scout missing know_the_hew")
    if "read_the_stem_list" not in stem_c_ids:
        raise AssertionError("city_oath missing read_the_stem_list")
    if "know_the_hew" in stem_c_ids or "read_the_stem_list" in stem_m_ids:
        raise AssertionError("stem sheet verbs leaked across sheets")

    plain_stem = replay(content, by_id["cross_plain_stem"]["seed"], by_id["cross_plain_stem"]["sheet"], by_id["cross_plain_stem"]["actions"])
    mast_stem = replay(content, by_id["cross_mast_stem"]["seed"], by_id["cross_mast_stem"]["sheet"], by_id["cross_mast_stem"]["actions"])
    if plain_stem.state.location != mast_stem.state.location:
        raise AssertionError("stem cross-area pair left different locations")
    if plain_stem.state.location != "stem.hew":
        raise AssertionError("stem cross-area pair not at stem.hew")
    plain_stem_ids = {a.id for a in enumerate_legal(plain_stem.state, content)}
    mast_stem_ids = {a.id for a in enumerate_legal(mast_stem.state, content)}
    if "hoop_the_hew" not in mast_stem_ids:
        raise AssertionError("partner hooped did not unlock hoop_the_hew")
    if "hoop_the_hew" in plain_stem_ids:
        raise AssertionError("hoop_the_hew leaked without partner hooped")
    if "partner_hooped" not in mast_stem.state.outcomes:
        raise AssertionError("cross mast-stem run lost partner_hooped")

    fid_m = by_id["divergence_marsh_fid"]
    fid_c = by_id["divergence_city_fid"]
    fid_m_ids, fid_c_ids = _diverge_legal(content, fid_m, fid_c)
    if "know_the_turn" not in fid_m_ids:
        raise AssertionError("marsh_scout missing know_the_turn")
    if "read_the_fid_list" not in fid_c_ids:
        raise AssertionError("city_oath missing read_the_fid_list")
    if "know_the_turn" in fid_c_ids or "read_the_fid_list" in fid_m_ids:
        raise AssertionError("fid sheet verbs leaked across sheets")

    plain_fid = replay(content, by_id["cross_plain_fid"]["seed"], by_id["cross_plain_fid"]["sheet"], by_id["cross_plain_fid"]["actions"])
    stem_fid = replay(content, by_id["cross_stem_fid"]["seed"], by_id["cross_stem_fid"]["sheet"], by_id["cross_stem_fid"]["actions"])
    if plain_fid.state.location != stem_fid.state.location:
        raise AssertionError("fid cross-area pair left different locations")
    if plain_fid.state.location != "fid.turn":
        raise AssertionError("fid cross-area pair not at fid.turn")
    plain_fid_ids = {a.id for a in enumerate_legal(plain_fid.state, content)}
    stem_fid_ids = {a.id for a in enumerate_legal(stem_fid.state, content)}
    if "hang_the_fid" not in stem_fid_ids:
        raise AssertionError("knee hung did not unlock hang_the_fid")
    if "hang_the_fid" in plain_fid_ids:
        raise AssertionError("hang_the_fid leaked without knee hung")
    if "knee_hung" not in stem_fid.state.outcomes:
        raise AssertionError("cross stem-fid run lost knee_hung")

    cleat_m = by_id["divergence_marsh_cleat"]
    cleat_c = by_id["divergence_city_cleat"]
    cleat_m_ids, cleat_c_ids = _diverge_legal(content, cleat_m, cleat_c)
    if "know_the_saw" not in cleat_m_ids:
        raise AssertionError("marsh_scout missing know_the_saw")
    if "read_the_cleat_list" not in cleat_c_ids:
        raise AssertionError("city_oath missing read_the_cleat_list")
    if "know_the_saw" in cleat_c_ids or "read_the_cleat_list" in cleat_m_ids:
        raise AssertionError("cleat sheet verbs leaked across sheets")

    plain_cleat = replay(content, by_id["cross_plain_cleat"]["seed"], by_id["cross_plain_cleat"]["sheet"], by_id["cross_plain_cleat"]["actions"])
    fid_cleat = replay(content, by_id["cross_fid_cleat"]["seed"], by_id["cross_fid_cleat"]["sheet"], by_id["cross_fid_cleat"]["actions"])
    if plain_cleat.state.location != fid_cleat.state.location:
        raise AssertionError("cleat cross-area pair left different locations")
    if plain_cleat.state.location != "cleat.saw":
        raise AssertionError("cleat cross-area pair not at cleat.saw")
    plain_cleat_ids = {a.id for a in enumerate_legal(plain_cleat.state, content)}
    fid_cleat_ids = {a.id for a in enumerate_legal(fid_cleat.state, content)}
    if "seize_the_saw" not in fid_cleat_ids:
        raise AssertionError("eye seized did not unlock seize_the_saw")
    if "seize_the_saw" in plain_cleat_ids:
        raise AssertionError("seize_the_saw leaked without eye seized")
    if "eye_seized" not in fid_cleat.state.outcomes:
        raise AssertionError("cross fid-cleat run lost eye_seized")

    haw_m = by_id["divergence_marsh_haw"]
    haw_c = by_id["divergence_city_haw"]
    haw_m_ids, haw_c_ids = _diverge_legal(content, haw_m, haw_c)
    if "know_the_bore" not in haw_m_ids:
        raise AssertionError("marsh_scout missing know_the_bore")
    if "read_the_hawse_list" not in haw_c_ids:
        raise AssertionError("city_oath missing read_the_hawse_list")
    if "know_the_bore" in haw_c_ids or "read_the_hawse_list" in haw_m_ids:
        raise AssertionError("haw sheet verbs leaked across sheets")

    plain_haw = replay(content, by_id["cross_plain_haw"]["seed"], by_id["cross_plain_haw"]["sheet"], by_id["cross_plain_haw"]["actions"])
    cleat_haw = replay(content, by_id["cross_cleat_haw"]["seed"], by_id["cross_cleat_haw"]["sheet"], by_id["cross_cleat_haw"]["actions"])
    if plain_haw.state.location != cleat_haw.state.location:
        raise AssertionError("haw cross-area pair left different locations")
    if plain_haw.state.location != "haw.bore":
        raise AssertionError("haw cross-area pair not at haw.bore")
    plain_haw_ids = {a.id for a in enumerate_legal(plain_haw.state, content)}
    cleat_haw_ids = {a.id for a in enumerate_legal(cleat_haw.state, content)}
    if "bolt_the_bore" not in cleat_haw_ids:
        raise AssertionError("base bolted did not unlock bolt_the_bore")
    if "bolt_the_bore" in plain_haw_ids:
        raise AssertionError("bolt_the_bore leaked without base bolted")
    if "base_bolted" not in cleat_haw.state.outcomes:
        raise AssertionError("cross cleat-haw run lost base_bolted")

    deye_m = by_id["divergence_marsh_deye"]
    deye_c = by_id["divergence_city_deye"]
    deye_m_ids, deye_c_ids = _diverge_legal(content, deye_m, deye_c)
    if "know_the_rim" not in deye_m_ids:
        raise AssertionError("marsh_scout missing know_the_rim")
    if "read_the_deadeye_list" not in deye_c_ids:
        raise AssertionError("city_oath missing read_the_deadeye_list")
    if "know_the_rim" in deye_c_ids or "read_the_deadeye_list" in deye_m_ids:
        raise AssertionError("deye sheet verbs leaked across sheets")

    plain_deye = replay(content, by_id["cross_plain_deye"]["seed"], by_id["cross_plain_deye"]["sheet"], by_id["cross_plain_deye"]["actions"])
    haw_deye = replay(content, by_id["cross_haw_deye"]["seed"], by_id["cross_haw_deye"]["sheet"], by_id["cross_haw_deye"]["actions"])
    if plain_deye.state.location != haw_deye.state.location:
        raise AssertionError("deye cross-area pair left different locations")
    if plain_deye.state.location != "deye.rim":
        raise AssertionError("deye cross-area pair not at deye.rim")
    plain_deye_ids = {a.id for a in enumerate_legal(plain_deye.state, content)}
    haw_deye_ids = {a.id for a in enumerate_legal(haw_deye.state, content)}
    if "pay_the_rim" not in haw_deye_ids:
        raise AssertionError("collar paid did not unlock pay_the_rim")
    if "pay_the_rim" in plain_deye_ids:
        raise AssertionError("pay_the_rim leaked without collar paid")
    if "collar_paid" not in haw_deye.state.outcomes:
        raise AssertionError("cross haw-deye run lost collar_paid")

    par_m = by_id["divergence_marsh_par"]
    par_c = by_id["divergence_city_par"]
    par_m_ids, par_c_ids = _diverge_legal(content, par_m, par_c)
    if "know_the_truck" not in par_m_ids:
        raise AssertionError("marsh_scout missing know_the_truck")
    if "read_the_parrel_list" not in par_c_ids:
        raise AssertionError("city_oath missing read_the_parrel_list")
    if "know_the_truck" in par_c_ids or "read_the_parrel_list" in par_m_ids:
        raise AssertionError("par sheet verbs leaked across sheets")

    plain_par = replay(content, by_id["cross_plain_par"]["seed"], by_id["cross_plain_par"]["sheet"], by_id["cross_plain_par"]["actions"])
    deye_par = replay(content, by_id["cross_deye_par"]["seed"], by_id["cross_deye_par"]["sheet"], by_id["cross_deye_par"]["actions"])
    if plain_par.state.location != deye_par.state.location:
        raise AssertionError("par cross-area pair left different locations")
    if plain_par.state.location != "par.truck":
        raise AssertionError("par cross-area pair not at par.truck")
    plain_par_ids = {a.id for a in enumerate_legal(plain_par.state, content)}
    deye_par_ids = {a.id for a in enumerate_legal(deye_par.state, content)}
    if "seize_the_truck" not in deye_par_ids:
        raise AssertionError("lanyard seized did not unlock seize_the_truck")
    if "seize_the_truck" in plain_par_ids:
        raise AssertionError("seize_the_truck leaked without lanyard seized")
    if "lanyard_seized" not in deye_par.state.outcomes:
        raise AssertionError("cross deye-par run lost lanyard_seized")

    bitt_m = by_id["divergence_marsh_bitt"]
    bitt_c = by_id["divergence_city_bitt"]
    bitt_m_ids, bitt_c_ids = _diverge_legal(content, bitt_m, bitt_c)
    if "know_the_step" not in bitt_m_ids:
        raise AssertionError("marsh_scout missing know_the_step")
    if "read_the_bitts_list" not in bitt_c_ids:
        raise AssertionError("city_oath missing read_the_bitts_list")
    if "know_the_step" in bitt_c_ids or "read_the_bitts_list" in bitt_m_ids:
        raise AssertionError("bitt sheet verbs leaked across sheets")

    plain_bitt = replay(content, by_id["cross_plain_bitt"]["seed"], by_id["cross_plain_bitt"]["sheet"], by_id["cross_plain_bitt"]["actions"])
    par_bitt = replay(content, by_id["cross_par_bitt"]["seed"], by_id["cross_par_bitt"]["sheet"], by_id["cross_par_bitt"]["actions"])
    if plain_bitt.state.location != par_bitt.state.location:
        raise AssertionError("bitt cross-area pair left different locations")
    if plain_bitt.state.location != "bitt.step":
        raise AssertionError("bitt cross-area pair not at bitt.step")
    plain_bitt_ids = {a.id for a in enumerate_legal(plain_bitt.state, content)}
    par_bitt_ids = {a.id for a in enumerate_legal(par_bitt.state, content)}
    if "truss_the_step" not in par_bitt_ids:
        raise AssertionError("parrel trussed did not unlock truss_the_step")
    if "truss_the_step" in plain_bitt_ids:
        raise AssertionError("truss_the_step leaked without parrel trussed")
    if "parrel_trussed" not in par_bitt.state.outcomes:
        raise AssertionError("cross par-bitt run lost parrel_trussed")

    gam_m = by_id["divergence_marsh_gam"]
    gam_c = by_id["divergence_city_gam"]
    gam_m_ids, gam_c_ids = _diverge_legal(content, gam_m, gam_c)
    if "know_the_woold" not in gam_m_ids:
        raise AssertionError("marsh_scout missing know_the_woold")
    if "read_the_gammon_list" not in gam_c_ids:
        raise AssertionError("city_oath missing read_the_gammon_list")
    if "know_the_woold" in gam_c_ids or "read_the_gammon_list" in gam_m_ids:
        raise AssertionError("gam sheet verbs leaked across sheets")

    plain_gam = replay(content, by_id["cross_plain_gam"]["seed"], by_id["cross_plain_gam"]["sheet"], by_id["cross_plain_gam"]["actions"])
    bitt_gam = replay(content, by_id["cross_bitt_gam"]["seed"], by_id["cross_bitt_gam"]["sheet"], by_id["cross_bitt_gam"]["actions"])
    if plain_gam.state.location != bitt_gam.state.location:
        raise AssertionError("gam cross-area pair left different locations")
    if plain_gam.state.location != "gam.woold":
        raise AssertionError("gam cross-area pair not at gam.woold")
    plain_gam_ids = {a.id for a in enumerate_legal(plain_gam.state, content)}
    bitt_gam_ids = {a.id for a in enumerate_legal(bitt_gam.state, content)}
    if "belay_the_woold" not in bitt_gam_ids:
        raise AssertionError("cable belayed did not unlock belay_the_woold")
    if "belay_the_woold" in plain_gam_ids:
        raise AssertionError("belay_the_woold leaked without cable belayed")
    if "cable_belayed" not in bitt_gam.state.outcomes:
        raise AssertionError("cross bitt-gam run lost cable_belayed")

    till_m = by_id["divergence_marsh_till"]
    till_c = by_id["divergence_city_till"]
    till_m_ids, till_c_ids = _diverge_legal(content, till_m, till_c)
    if "know_the_shape" not in till_m_ids:
        raise AssertionError("marsh_scout missing know_the_shape")
    if "read_the_tiller_list" not in till_c_ids:
        raise AssertionError("city_oath missing read_the_tiller_list")
    if "know_the_shape" in till_c_ids or "read_the_tiller_list" in till_m_ids:
        raise AssertionError("till sheet verbs leaked across sheets")

    plain_till = replay(content, by_id["cross_plain_till"]["seed"], by_id["cross_plain_till"]["sheet"], by_id["cross_plain_till"]["actions"])
    gam_till = replay(content, by_id["cross_gam_till"]["seed"], by_id["cross_gam_till"]["sheet"], by_id["cross_gam_till"]["actions"])
    if plain_till.state.location != gam_till.state.location:
        raise AssertionError("till cross-area pair left different locations")
    if plain_till.state.location != "till.shape":
        raise AssertionError("till cross-area pair not at till.shape")
    plain_till_ids = {a.id for a in enumerate_legal(plain_till.state, content)}
    gam_till_ids = {a.id for a in enumerate_legal(gam_till.state, content)}
    if "frap_the_shape" not in gam_till_ids:
        raise AssertionError("gammon frapped did not unlock frap_the_shape")
    if "frap_the_shape" in plain_till_ids:
        raise AssertionError("frap_the_shape leaked without gammon frapped")
    if "gammon_frapped" not in gam_till.state.outcomes:
        raise AssertionError("cross gam-till run lost gammon_frapped")

    cath_m = by_id["divergence_marsh_cath"]
    cath_c = by_id["divergence_city_cath"]
    cath_m_ids, cath_c_ids = _diverge_legal(content, cath_m, cath_c)
    if "know_the_bill" not in cath_m_ids:
        raise AssertionError("marsh_scout missing know_the_bill")
    if "read_the_cathead_list" not in cath_c_ids:
        raise AssertionError("city_oath missing read_the_cathead_list")
    if "know_the_bill" in cath_c_ids or "read_the_cathead_list" in cath_m_ids:
        raise AssertionError("cath sheet verbs leaked across sheets")

    plain_cath = replay(content, by_id["cross_plain_cath"]["seed"], by_id["cross_plain_cath"]["sheet"], by_id["cross_plain_cath"]["actions"])
    till_cath = replay(content, by_id["cross_till_cath"]["seed"], by_id["cross_till_cath"]["sheet"], by_id["cross_till_cath"]["actions"])
    if plain_cath.state.location != till_cath.state.location:
        raise AssertionError("cath cross-area pair left different locations")
    if plain_cath.state.location != "cath.bill":
        raise AssertionError("cath cross-area pair not at cath.bill")
    plain_cath_ids = {a.id for a in enumerate_legal(plain_cath.state, content)}
    till_cath_ids = {a.id for a in enumerate_legal(till_cath.state, content)}
    if "yoke_the_bill" not in till_cath_ids:
        raise AssertionError("tiller yoked did not unlock yoke_the_bill")
    if "yoke_the_bill" in plain_cath_ids:
        raise AssertionError("yoke_the_bill leaked without tiller yoked")
    if "tiller_yoked" not in till_cath.state.outcomes:
        raise AssertionError("cross till-cath run lost tiller_yoked")

    tran_m = by_id["divergence_marsh_tran"]
    tran_c = by_id["divergence_city_tran"]
    tran_m_ids, tran_c_ids = _diverge_legal(content, tran_m, tran_c)
    if "know_the_wing" not in tran_m_ids:
        raise AssertionError("marsh_scout missing know_the_wing")
    if "read_the_transom_list" not in tran_c_ids:
        raise AssertionError("city_oath missing read_the_transom_list")
    if "know_the_wing" in tran_c_ids or "read_the_transom_list" in tran_m_ids:
        raise AssertionError("tran sheet verbs leaked across sheets")

    plain_tran = replay(content, by_id["cross_plain_tran"]["seed"], by_id["cross_plain_tran"]["sheet"], by_id["cross_plain_tran"]["actions"])
    cath_tran = replay(content, by_id["cross_cath_tran"]["seed"], by_id["cross_cath_tran"]["sheet"], by_id["cross_cath_tran"]["actions"])
    if plain_tran.state.location != cath_tran.state.location:
        raise AssertionError("tran cross-area pair left different locations")
    if plain_tran.state.location != "tran.wing":
        raise AssertionError("tran cross-area pair not at tran.wing")
    plain_tran_ids = {a.id for a in enumerate_legal(plain_tran.state, content)}
    cath_tran_ids = {a.id for a in enumerate_legal(cath_tran.state, content)}
    if "fish_the_wing" not in cath_tran_ids:
        raise AssertionError("fluke fished did not unlock fish_the_wing")
    if "fish_the_wing" in plain_tran_ids:
        raise AssertionError("fish_the_wing leaked without fluke fished")
    if "fluke_fished" not in cath_tran.state.outcomes:
        raise AssertionError("cross cath-tran run lost fluke_fished")

    scup_m = by_id["divergence_marsh_scup"]
    scup_c = by_id["divergence_city_scup"]
    scup_m_ids, scup_c_ids = _diverge_legal(content, scup_m, scup_c)
    if "know_the_broach" not in scup_m_ids:
        raise AssertionError("marsh_scout missing know_the_broach")
    if "read_the_scupper_list" not in scup_c_ids:
        raise AssertionError("city_oath missing read_the_scupper_list")
    if "know_the_broach" in scup_c_ids or "read_the_scupper_list" in scup_m_ids:
        raise AssertionError("scup sheet verbs leaked across sheets")

    plain_scup = replay(content, by_id["cross_plain_scup"]["seed"], by_id["cross_plain_scup"]["sheet"], by_id["cross_plain_scup"]["actions"])
    tran_scup = replay(content, by_id["cross_tran_scup"]["seed"], by_id["cross_tran_scup"]["sheet"], by_id["cross_tran_scup"]["actions"])
    if plain_scup.state.location != tran_scup.state.location:
        raise AssertionError("scup cross-area pair left different locations")
    if plain_scup.state.location != "scup.broach":
        raise AssertionError("scup cross-area pair not at scup.broach")
    plain_scup_ids = {a.id for a in enumerate_legal(plain_scup.state, content)}
    tran_scup_ids = {a.id for a in enumerate_legal(tran_scup.state, content)}
    if "spike_the_broach" not in tran_scup_ids:
        raise AssertionError("stern spiked did not unlock spike_the_broach")
    if "spike_the_broach" in plain_scup_ids:
        raise AssertionError("spike_the_broach leaked without stern spiked")
    if "stern_spiked" not in tran_scup.state.outcomes:
        raise AssertionError("cross tran-scup run lost stern_spiked")

    binn_m = by_id["divergence_marsh_binn"]
    binn_c = by_id["divergence_city_binn"]
    binn_m_ids, binn_c_ids = _diverge_legal(content, binn_m, binn_c)
    if "know_the_hood" not in binn_m_ids:
        raise AssertionError("marsh_scout missing know_the_hood")
    if "read_the_binnacle_list" not in binn_c_ids:
        raise AssertionError("city_oath missing read_the_binnacle_list")
    if "know_the_hood" in binn_c_ids or "read_the_binnacle_list" in binn_m_ids:
        raise AssertionError("binn sheet verbs leaked across sheets")

    plain_binn = replay(content, by_id["cross_plain_binn"]["seed"], by_id["cross_plain_binn"]["sheet"], by_id["cross_plain_binn"]["actions"])
    scup_binn = replay(content, by_id["cross_scup_binn"]["seed"], by_id["cross_scup_binn"]["sheet"], by_id["cross_scup_binn"]["actions"])
    if plain_binn.state.location != scup_binn.state.location:
        raise AssertionError("binn cross-area pair left different locations")
    if plain_binn.state.location != "binn.hood":
        raise AssertionError("binn cross-area pair not at binn.hood")
    plain_binn_ids = {a.id for a in enumerate_legal(plain_binn.state, content)}
    scup_binn_ids = {a.id for a in enumerate_legal(scup_binn.state, content)}
    if "plug_the_hood" not in scup_binn_ids:
        raise AssertionError("mouth plugged did not unlock plug_the_hood")
    if "plug_the_hood" in plain_binn_ids:
        raise AssertionError("plug_the_hood leaked without mouth plugged")
    if "mouth_plugged" not in scup_binn.state.outcomes:
        raise AssertionError("cross scup-binn run lost mouth_plugged")

    futt_m = by_id["divergence_marsh_futt"]
    futt_c = by_id["divergence_city_futt"]
    futt_m_ids, futt_c_ids = _diverge_legal(content, futt_m, futt_c)
    if "know_the_cant" not in futt_m_ids:
        raise AssertionError("marsh_scout missing know_the_cant")
    if "read_the_futtock_list" not in futt_c_ids:
        raise AssertionError("city_oath missing read_the_futtock_list")
    if "know_the_cant" in futt_c_ids or "read_the_futtock_list" in futt_m_ids:
        raise AssertionError("futt sheet verbs leaked across sheets")

    plain_futt = replay(content, by_id["cross_plain_futt"]["seed"], by_id["cross_plain_futt"]["sheet"], by_id["cross_plain_futt"]["actions"])
    binn_futt = replay(content, by_id["cross_binn_futt"]["seed"], by_id["cross_binn_futt"]["sheet"], by_id["cross_binn_futt"]["actions"])
    if plain_futt.state.location != binn_futt.state.location:
        raise AssertionError("futt cross-area pair left different locations")
    if plain_futt.state.location != "futt.cant":
        raise AssertionError("futt cross-area pair not at futt.cant")
    plain_futt_ids = {a.id for a in enumerate_legal(plain_futt.state, content)}
    binn_futt_ids = {a.id for a in enumerate_legal(binn_futt.state, content)}
    if "lock_the_cant" not in binn_futt_ids:
        raise AssertionError("card locked did not unlock lock_the_cant")
    if "lock_the_cant" in plain_futt_ids:
        raise AssertionError("lock_the_cant leaked without card locked")
    if "card_locked" not in binn_futt.state.outcomes:
        raise AssertionError("cross binn-futt run lost card_locked")

    cros_m = by_id["divergence_marsh_cros"]
    cros_c = by_id["divergence_city_cros"]
    cros_m_ids, cros_c_ids = _diverge_legal(content, cros_m, cros_c)
    if "know_the_tree" not in cros_m_ids:
        raise AssertionError("marsh_scout missing know_the_tree")
    if "read_the_crosstree_list" not in cros_c_ids:
        raise AssertionError("city_oath missing read_the_crosstree_list")
    if "know_the_tree" in cros_c_ids or "read_the_crosstree_list" in cros_m_ids:
        raise AssertionError("cros sheet verbs leaked across sheets")

    plain_cros = replay(content, by_id["cross_plain_cros"]["seed"], by_id["cross_plain_cros"]["sheet"], by_id["cross_plain_cros"]["actions"])
    futt_cros = replay(content, by_id["cross_futt_cros"]["seed"], by_id["cross_futt_cros"]["sheet"], by_id["cross_futt_cros"]["actions"])
    if plain_cros.state.location != futt_cros.state.location:
        raise AssertionError("cros cross-area pair left different locations")
    if plain_cros.state.location != "cros.tree":
        raise AssertionError("cros cross-area pair not at cros.tree")
    plain_cros_ids = {a.id for a in enumerate_legal(plain_cros.state, content)}
    futt_cros_ids = {a.id for a in enumerate_legal(futt_cros.state, content)}
    if "clench_the_tree" not in futt_cros_ids:
        raise AssertionError("belly clenched did not unlock clench_the_tree")
    if "clench_the_tree" in plain_cros_ids:
        raise AssertionError("clench_the_tree leaked without belly clenched")
    if "belly_clenched" not in futt_cros.state.outcomes:
        raise AssertionError("cross futt-cros run lost belly_clenched")

    return {
        "harbor_compact": compact.fingerprint,
        "stack_relic": relic.fingerprint,
        "kiln_pact": kiln.fingerprint,
        "reed_sentence": court.fingerprint,
        "road_beacon": beacon.fingerprint,
        "fever_broken": fever.fingerprint,
        "name_restored": named.fingerprint,
        "fold_held": fold.fingerprint,
        "lens_set": lens.fingerprint,
        "rope_walked": rope.fingerprint,
        "salt_raked": salt.fingerprint,
        "smoke_cured": smoke.fingerprint,
        "weir_lifted": weir.fingerprint,
        "dye_struck": dye.fingerprint,
        "ferry_crossed": ferry.fingerprint,
        "flats_drained": pump.fingerprint,
        "oyster_culled": oyster.fingerprint,
        "tally_closed": tally.fingerprint,
        "ice_held": ice.fingerprint,
        "wreck_laid": wreck.fingerprint,
        "hive_kept": hive.fingerprint,
        "mead_drawn": mead.fingerprint,
        "barrel_raised": barrel.fingerprint,
        "pickle_lidded": pickle.fingerprint,
        "iron_quenched": iron.fingerprint,
        "fowl_taken": fowl.fingerprint,
        "lights_bound": rush.fingerprint,
        "seam_caulked": caulk.fingerprint,
        "net_tarred": netted.fingerprint,
        "sail_hoisted": hoisted.fingerprint,
        "lead_cast": sounding.fingerprint,
        "rutter_sealed": rutter.fingerprint,
        "buoy_set": buoy.fingerprint,
        "kelp_burned": kelp.fingerprint,
        "soap_cut": soap.fingerprint,
        "cloth_fulled": cloth.fingerprint,
        "coal_drawn": coal.fingerprint,
        "lime_slaked": lime.fingerprint,
        "joint_pointed": pointed.fingerprint,
        "roof_set": roof.fingerprint,
        "cistern_filled": filled.fingerprint,
        "wash_hung": hung.fingerprint,
        "paper_laid": laid.fingerprint,
        "frail_woven": woven.fingerprint,
        "loaf_drawn": loaf.fingerprint,
        "wheel_salted": salted.fingerprint,
        "web_sheared": sheared.fingerprint,
        "lantern_hung": lantern.fingerprint,
        "nib_cut": nibbed.fingerprint,
        "heel_pegged": pegged.fingerprint,
        "keeve_bunged": bunged.fingerprint,
        "mustard_potted": potted.fingerprint,
        "sausage_linked": linked.fingerprint,
        "pie_crimped": crimped.fingerprint,
        "jam_jarred": jarred.fingerprint,
        "crock_glazed": glazed.fingerprint,
        "hide_tanned": tanned.fingerprint,
        "flax_spun": spun.fingerprint,
        "nail_pointed": nailed.fingerprint,
        "tyre_set": tyred.fingerprint,
        "malt_oasted": oasted.fingerprint,
        "gyle_racked": gyled.fingerprint,
        "cruet_corked": corked.fingerprint,
        "glue_caked": glued.fingerprint,
        "book_bound": booked.fingerprint,
        "plate_burnished": gilded.fingerprint,
        "collet_closed": gemmed.fingerprint,
        "pane_camed": camed.fingerprint,
        "sash_pinned": sashed.fingerprint,
        "light_dusted": dusted.fingerprint,
        "coat_brushed": coated.fingerprint,
        "varnish_flowed": varnished.fingerprint,
        "latch_thrown": latched.fingerprint,
        "gudgeon_shipped": hinged.fingerprint,
        "casement_stayed": stayed.fingerprint,
        "stool_seated": seated.fingerprint,
        "casing_tacked": cased.fingerprint,
        "plinth_fixed": skirted.fingerprint,
        "rail_capped": dadoed.fingerprint,
        "rail_sprung": sprung.fingerprint,
        "cornice_floated": coved.fingerprint,
        "riser_wedged": staired.fingerprint,
        "finial_dowelled": newelled.fingerprint,
        "ramp_wreathed": wreathed.fingerprint,
        "neck_shouldered": balustered.fingerprint,
        "end_returned": trod.fingerprint,
        "nail_secreted": floored.fingerprint,
        "camber_crowned": joisted.fingerprint,
        "coat_haired": lathed.fingerprint,
        "breast_limed": chimneyed.fingerprint,
        "mantel_pinned": mantelled.fingerprint,
        "cowl_hung": flued.fingerprint,
        "back_bedded": backed.fingerprint,
        "slide_registered": grated.fingerprint,
        "hack_set": bricked.fingerprint,
        "arris_nicked": tiled.fingerprint,
        "slate_lapped": slated.fingerprint,
        "flash_dressed": flashed.fingerprint,
        "block_stropped": stropped.fingerprint,
        "grip_bound": oared.fingerprint,
        "hull_launched": launched.fingerprint,
        "garboard_faired": clinked.fingerprint,
        "round_heaved": heaved.fingerprint,
        "station_bevelled": lofted.fingerprint,
        "trunnel_driven": trunnelled.fingerprint,
        "hog_bolted": hogged.fingerprint,
        "partner_hooped": masted.fingerprint,
        "knee_hung": stemmed.fingerprint,
        "eye_seized": fidded.fingerprint,
        "base_bolted": cleated.fingerprint,
        "collar_paid": hawsed.fingerprint,
        "lanyard_seized": deadeyed.fingerprint,
        "parrel_trussed": parreled.fingerprint,
        "cable_belayed": belayed.fingerprint,
        "gammon_frapped": gammoned.fingerprint,
        "tiller_yoked": tillered.fingerprint,
        "fluke_fished": catheaded.fingerprint,
        "stern_spiked": transomed.fingerprint,
        "mouth_plugged": scuppered.fingerprint,
        "card_locked": binnacled.fingerprint,
        "belly_clenched": futtocked.fingerprint,
        "bolster_seized": crosstreed.fingerprint,
        "marsh_only": sorted(m_ids - c_ids),
        "city_only": sorted(c_ids - m_ids),
        "mill_marsh_only": sorted(mill_m_ids - mill_c_ids),
        "mill_city_only": sorted(mill_c_ids - mill_m_ids),
        "court_marsh_only": sorted(court_m_ids - court_c_ids),
        "court_city_only": sorted(court_c_ids - court_m_ids),
        "road_marsh_only": sorted(road_m_ids - road_c_ids),
        "road_city_only": sorted(road_c_ids - road_m_ids),
        "camp_marsh_only": sorted(camp_m_ids - camp_c_ids),
        "camp_city_only": sorted(camp_c_ids - camp_m_ids),
        "name_marsh_only": sorted(name_m_ids - name_c_ids),
        "name_city_only": sorted(name_c_ids - name_m_ids),
        "fold_marsh_only": sorted(fold_m_ids - fold_c_ids),
        "fold_city_only": sorted(fold_c_ids - fold_m_ids),
        "glass_marsh_only": sorted(glass_m_ids - glass_c_ids),
        "glass_city_only": sorted(glass_c_ids - glass_m_ids),
        "rope_marsh_only": sorted(rope_m_ids - rope_c_ids),
        "rope_city_only": sorted(rope_c_ids - rope_m_ids),
        "salt_marsh_only": sorted(salt_m_ids - salt_c_ids),
        "salt_city_only": sorted(salt_c_ids - salt_m_ids),
        "smoke_marsh_only": sorted(smoke_m_ids - smoke_c_ids),
        "smoke_city_only": sorted(smoke_c_ids - smoke_m_ids),
        "weir_marsh_only": sorted(weir_m_ids - weir_c_ids),
        "weir_city_only": sorted(weir_c_ids - weir_m_ids),
        "dye_marsh_only": sorted(dye_m_ids - dye_c_ids),
        "dye_city_only": sorted(dye_c_ids - dye_m_ids),
        "ferry_marsh_only": sorted(ferry_m_ids - ferry_c_ids),
        "ferry_city_only": sorted(ferry_c_ids - ferry_m_ids),
        "pump_marsh_only": sorted(pump_m_ids - pump_c_ids),
        "pump_city_only": sorted(pump_c_ids - pump_m_ids),
        "oyster_marsh_only": sorted(oyster_m_ids - oyster_c_ids),
        "oyster_city_only": sorted(oyster_c_ids - oyster_m_ids),
        "count_marsh_only": sorted(count_m_ids - count_c_ids),
        "count_city_only": sorted(count_c_ids - count_m_ids),
        "ice_marsh_only": sorted(ice_m_ids - ice_c_ids),
        "ice_city_only": sorted(ice_c_ids - ice_m_ids),
        "wreck_marsh_only": sorted(wreck_m_ids - wreck_c_ids),
        "wreck_city_only": sorted(wreck_c_ids - wreck_m_ids),
        "hive_marsh_only": sorted(hive_m_ids - hive_c_ids),
        "hive_city_only": sorted(hive_c_ids - hive_m_ids),
        "mead_marsh_only": sorted(mead_m_ids - mead_c_ids),
        "mead_city_only": sorted(mead_c_ids - mead_m_ids),
        "coop_marsh_only": sorted(coop_m_ids - coop_c_ids),
        "coop_city_only": sorted(coop_c_ids - coop_m_ids),
        "pickle_marsh_only": sorted(pickle_m_ids - pickle_c_ids),
        "pickle_city_only": sorted(pickle_c_ids - pickle_m_ids),
        "forge_marsh_only": sorted(forge_m_ids - forge_c_ids),
        "forge_city_only": sorted(forge_c_ids - forge_m_ids),
        "decoy_marsh_only": sorted(decoy_m_ids - decoy_c_ids),
        "decoy_city_only": sorted(decoy_c_ids - decoy_m_ids),
        "rush_marsh_only": sorted(rush_m_ids - rush_c_ids),
        "rush_city_only": sorted(rush_c_ids - rush_m_ids),
        "caulk_marsh_only": sorted(caulk_m_ids - caulk_c_ids),
        "caulk_city_only": sorted(caulk_c_ids - caulk_m_ids),
        "net_marsh_only": sorted(net_m_ids - net_c_ids),
        "net_city_only": sorted(net_c_ids - net_m_ids),
        "sail_marsh_only": sorted(sail_m_ids - sail_c_ids),
        "sail_city_only": sorted(sail_c_ids - sail_m_ids),
        "lead_marsh_only": sorted(lead_m_ids - lead_c_ids),
        "lead_city_only": sorted(lead_c_ids - lead_m_ids),
        "chart_marsh_only": sorted(chart_m_ids - chart_c_ids),
        "chart_city_only": sorted(chart_c_ids - chart_m_ids),
        "buoy_marsh_only": sorted(buoy_m_ids - buoy_c_ids),
        "buoy_city_only": sorted(buoy_c_ids - buoy_m_ids),
        "kelp_marsh_only": sorted(kelp_m_ids - kelp_c_ids),
        "kelp_city_only": sorted(kelp_c_ids - kelp_m_ids),
        "soap_marsh_only": sorted(soap_m_ids - soap_c_ids),
        "soap_city_only": sorted(soap_c_ids - soap_m_ids),
        "full_marsh_only": sorted(full_m_ids - full_c_ids),
        "full_city_only": sorted(full_c_ids - full_m_ids),
        "char_marsh_only": sorted(char_m_ids - char_c_ids),
        "char_city_only": sorted(char_c_ids - char_m_ids),
        "lime_marsh_only": sorted(lime_m_ids - lime_c_ids),
        "lime_city_only": sorted(lime_c_ids - lime_m_ids),
        "mason_marsh_only": sorted(mason_m_ids - mason_c_ids),
        "mason_city_only": sorted(mason_c_ids - mason_m_ids),
        "thatch_marsh_only": sorted(thatch_m_ids - thatch_c_ids),
        "thatch_city_only": sorted(thatch_c_ids - thatch_m_ids),
        "cistern_marsh_only": sorted(cistern_m_ids - cistern_c_ids),
        "cistern_city_only": sorted(cistern_c_ids - cistern_m_ids),
        "wash_marsh_only": sorted(wash_m_ids - wash_c_ids),
        "wash_city_only": sorted(wash_c_ids - wash_m_ids),
        "rag_marsh_only": sorted(rag_m_ids - rag_c_ids),
        "rag_city_only": sorted(rag_c_ids - rag_m_ids),
        "osier_marsh_only": sorted(osier_m_ids - osier_c_ids),
        "osier_city_only": sorted(osier_c_ids - osier_m_ids),
        "bake_marsh_only": sorted(bake_m_ids - bake_c_ids),
        "bake_city_only": sorted(bake_c_ids - bake_m_ids),
        "dairy_marsh_only": sorted(dairy_m_ids - dairy_c_ids),
        "dairy_city_only": sorted(dairy_c_ids - dairy_m_ids),
        "loom_marsh_only": sorted(loom_m_ids - loom_c_ids),
        "loom_city_only": sorted(loom_c_ids - loom_m_ids),
        "horn_marsh_only": sorted(horn_m_ids - horn_c_ids),
        "horn_city_only": sorted(horn_c_ids - horn_m_ids),
        "gall_marsh_only": sorted(gall_m_ids - gall_c_ids),
        "gall_city_only": sorted(gall_c_ids - gall_m_ids),
        "cobble_marsh_only": sorted(cobble_m_ids - cobble_c_ids),
        "cobble_city_only": sorted(cobble_c_ids - cobble_m_ids),
        "cider_marsh_only": sorted(cider_m_ids - cider_c_ids),
        "cider_city_only": sorted(cider_c_ids - cider_m_ids),
        "must_marsh_only": sorted(must_m_ids - must_c_ids),
        "must_city_only": sorted(must_c_ids - must_m_ids),
        "link_marsh_only": sorted(link_m_ids - link_c_ids),
        "link_city_only": sorted(link_c_ids - link_m_ids),
        "pie_marsh_only": sorted(pie_m_ids - pie_c_ids),
        "pie_city_only": sorted(pie_c_ids - pie_m_ids),
        "jam_marsh_only": sorted(jam_m_ids - jam_c_ids),
        "jam_city_only": sorted(jam_c_ids - jam_m_ids),
        "crock_marsh_only": sorted(crock_m_ids - crock_c_ids),
        "crock_city_only": sorted(crock_c_ids - crock_m_ids),
        "hide_marsh_only": sorted(hide_m_ids - hide_c_ids),
        "hide_city_only": sorted(hide_c_ids - hide_m_ids),
        "flax_marsh_only": sorted(flax_m_ids - flax_c_ids),
        "flax_city_only": sorted(flax_c_ids - flax_m_ids),
        "nail_marsh_only": sorted(nail_m_ids - nail_c_ids),
        "nail_city_only": sorted(nail_c_ids - nail_m_ids),
        "wain_marsh_only": sorted(wain_m_ids - wain_c_ids),
        "wain_city_only": sorted(wain_c_ids - wain_m_ids),
        "malt_marsh_only": sorted(malt_m_ids - malt_c_ids),
        "malt_city_only": sorted(malt_c_ids - malt_m_ids),
        "brew_marsh_only": sorted(brew_m_ids - brew_c_ids),
        "brew_city_only": sorted(brew_c_ids - brew_m_ids),
        "acet_marsh_only": sorted(acet_m_ids - acet_c_ids),
        "acet_city_only": sorted(acet_c_ids - acet_m_ids),
        "glue_marsh_only": sorted(glue_m_ids - glue_c_ids),
        "glue_city_only": sorted(glue_c_ids - glue_m_ids),
        "bind_marsh_only": sorted(bind_m_ids - bind_c_ids),
        "bind_city_only": sorted(bind_c_ids - bind_m_ids),
        "gilt_marsh_only": sorted(gilt_m_ids - gilt_c_ids),
        "gilt_city_only": sorted(gilt_c_ids - gilt_m_ids),
        "gem_marsh_only": sorted(gem_m_ids - gem_c_ids),
        "gem_city_only": sorted(gem_c_ids - gem_m_ids),
        "glaz_marsh_only": sorted(glaz_m_ids - glaz_c_ids),
        "glaz_city_only": sorted(glaz_c_ids - glaz_m_ids),
        "sash_marsh_only": sorted(sash_m_ids - sash_c_ids),
        "sash_city_only": sorted(sash_c_ids - sash_m_ids),
        "putty_marsh_only": sorted(putty_m_ids - putty_c_ids),
        "putty_city_only": sorted(putty_c_ids - putty_m_ids),
        "paint_marsh_only": sorted(paint_m_ids - paint_c_ids),
        "paint_city_only": sorted(paint_c_ids - paint_m_ids),
        "varn_marsh_only": sorted(varn_m_ids - varn_c_ids),
        "varn_city_only": sorted(varn_c_ids - varn_m_ids),
        "latch_marsh_only": sorted(latch_m_ids - latch_c_ids),
        "latch_city_only": sorted(latch_c_ids - latch_m_ids),
        "hinge_marsh_only": sorted(hinge_m_ids - hinge_c_ids),
        "hinge_city_only": sorted(hinge_c_ids - hinge_m_ids),
        "stay_marsh_only": sorted(stay_m_ids - stay_c_ids),
        "stay_city_only": sorted(stay_c_ids - stay_m_ids),
        "sill_marsh_only": sorted(sill_m_ids - sill_c_ids),
        "sill_city_only": sorted(sill_c_ids - sill_m_ids),
        "case_marsh_only": sorted(case_m_ids - case_c_ids),
        "case_city_only": sorted(case_c_ids - case_m_ids),
        "skirt_marsh_only": sorted(skirt_m_ids - skirt_c_ids),
        "skirt_city_only": sorted(skirt_c_ids - skirt_m_ids),
        "dado_marsh_only": sorted(dado_m_ids - dado_c_ids),
        "dado_city_only": sorted(dado_c_ids - dado_m_ids),
        "pic_marsh_only": sorted(pic_m_ids - pic_c_ids),
        "pic_city_only": sorted(pic_c_ids - pic_m_ids),
        "corn_marsh_only": sorted(corn_m_ids - corn_c_ids),
        "corn_city_only": sorted(corn_c_ids - corn_m_ids),
        "stair_marsh_only": sorted(stair_m_ids - stair_c_ids),
        "stair_city_only": sorted(stair_c_ids - stair_m_ids),
        "newel_marsh_only": sorted(newel_m_ids - newel_c_ids),
        "newel_city_only": sorted(newel_c_ids - newel_m_ids),
        "hand_marsh_only": sorted(hand_m_ids - hand_c_ids),
        "hand_city_only": sorted(hand_c_ids - hand_m_ids),
        "bal_marsh_only": sorted(bal_m_ids - bal_c_ids),
        "bal_city_only": sorted(bal_c_ids - bal_m_ids),
        "tread_marsh_only": sorted(tread_m_ids - tread_c_ids),
        "tread_city_only": sorted(tread_c_ids - tread_m_ids),
        "floor_marsh_only": sorted(floor_m_ids - floor_c_ids),
        "floor_city_only": sorted(floor_c_ids - floor_m_ids),
        "joist_marsh_only": sorted(joist_m_ids - joist_c_ids),
        "joist_city_only": sorted(joist_c_ids - joist_m_ids),
        "lath_marsh_only": sorted(lath_m_ids - lath_c_ids),
        "lath_city_only": sorted(lath_c_ids - lath_m_ids),
        "chim_marsh_only": sorted(chim_m_ids - chim_c_ids),
        "chim_city_only": sorted(chim_c_ids - chim_m_ids),
        "mant_marsh_only": sorted(mant_m_ids - mant_c_ids),
        "mant_city_only": sorted(mant_c_ids - mant_m_ids),
        "flue_marsh_only": sorted(flue_m_ids - flue_c_ids),
        "flue_city_only": sorted(flue_c_ids - flue_m_ids),
        "fb_marsh_only": sorted(fb_m_ids - fb_c_ids),
        "fb_city_only": sorted(fb_c_ids - fb_m_ids),
        "grate_marsh_only": sorted(grate_m_ids - grate_c_ids),
        "grate_city_only": sorted(grate_c_ids - grate_m_ids),
        "brick_marsh_only": sorted(brick_m_ids - brick_c_ids),
        "brick_city_only": sorted(brick_c_ids - brick_m_ids),
        "tile_marsh_only": sorted(tile_m_ids - tile_c_ids),
        "tile_city_only": sorted(tile_c_ids - tile_m_ids),
        "slate_marsh_only": sorted(slate_m_ids - slate_c_ids),
        "slate_city_only": sorted(slate_c_ids - slate_m_ids),
        "flash_marsh_only": sorted(flash_m_ids - flash_c_ids),
        "flash_city_only": sorted(flash_c_ids - flash_m_ids),
        "block_marsh_only": sorted(block_m_ids - block_c_ids),
        "block_city_only": sorted(block_c_ids - block_m_ids),
        "oar_marsh_only": sorted(oar_m_ids - oar_c_ids),
        "oar_city_only": sorted(oar_c_ids - oar_m_ids),
        "ways_marsh_only": sorted(ways_m_ids - ways_c_ids),
        "ways_city_only": sorted(ways_c_ids - ways_m_ids),
        "clink_marsh_only": sorted(clink_m_ids - clink_c_ids),
        "clink_city_only": sorted(clink_c_ids - clink_m_ids),
        "wind_marsh_only": sorted(wind_m_ids - wind_c_ids),
        "wind_city_only": sorted(wind_c_ids - wind_m_ids),
        "offs_marsh_only": sorted(offs_m_ids - offs_c_ids),
        "offs_city_only": sorted(offs_c_ids - offs_m_ids),
        "trun_marsh_only": sorted(trun_m_ids - trun_c_ids),
        "trun_city_only": sorted(trun_c_ids - trun_m_ids),
        "dead_marsh_only": sorted(dead_m_ids - dead_c_ids),
        "dead_city_only": sorted(dead_c_ids - dead_m_ids),
        "mast_marsh_only": sorted(mast_m_ids - mast_c_ids),
        "mast_city_only": sorted(mast_c_ids - mast_m_ids),
        "stem_marsh_only": sorted(stem_m_ids - stem_c_ids),
        "stem_city_only": sorted(stem_c_ids - stem_m_ids),
        "fid_marsh_only": sorted(fid_m_ids - fid_c_ids),
        "fid_city_only": sorted(fid_c_ids - fid_m_ids),
        "cleat_marsh_only": sorted(cleat_m_ids - cleat_c_ids),
        "cleat_city_only": sorted(cleat_c_ids - cleat_m_ids),
        "haw_marsh_only": sorted(haw_m_ids - haw_c_ids),
        "haw_city_only": sorted(haw_c_ids - haw_m_ids),
        "deye_marsh_only": sorted(deye_m_ids - deye_c_ids),
        "deye_city_only": sorted(deye_c_ids - deye_m_ids),
        "par_marsh_only": sorted(par_m_ids - par_c_ids),
        "par_city_only": sorted(par_c_ids - par_m_ids),
        "bitt_marsh_only": sorted(bitt_m_ids - bitt_c_ids),
        "bitt_city_only": sorted(bitt_c_ids - bitt_m_ids),
        "gam_marsh_only": sorted(gam_m_ids - gam_c_ids),
        "gam_city_only": sorted(gam_c_ids - gam_m_ids),
        "till_marsh_only": sorted(till_m_ids - till_c_ids),
        "till_city_only": sorted(till_c_ids - till_m_ids),
        "cath_marsh_only": sorted(cath_m_ids - cath_c_ids),
        "cath_city_only": sorted(cath_c_ids - cath_m_ids),
        "tran_marsh_only": sorted(tran_m_ids - tran_c_ids),
        "tran_city_only": sorted(tran_c_ids - tran_m_ids),
        "scup_marsh_only": sorted(scup_m_ids - scup_c_ids),
        "scup_city_only": sorted(scup_c_ids - scup_m_ids),
        "binn_marsh_only": sorted(binn_m_ids - binn_c_ids),
        "binn_city_only": sorted(binn_c_ids - binn_m_ids),
        "futt_marsh_only": sorted(futt_m_ids - futt_c_ids),
        "futt_city_only": sorted(futt_c_ids - futt_m_ids),
        "cros_marsh_only": sorted(cros_m_ids - cros_c_ids),
        "cros_city_only": sorted(cros_c_ids - cros_m_ids),
    }


def _diverge_legal(content: Content, left: dict, right: dict) -> tuple[set[str], set[str]]:
    if left["actions"] != right["actions"]:
        raise AssertionError("divergence pair must share the same action prefix")
    l_state, l_cur = new_game(content, left["seed"], left["sheet"])
    r_state, r_cur = new_game(content, right["seed"], right["sheet"])
    for action_id in left["actions"]:
        l = step(l_state, action_id, content, l_cur)
        r = step(r_state, action_id, content, r_cur)
        if not l.accepted or not r.accepted:
            raise AssertionError(f"divergence prefix rejected: {action_id}")
        l_state, l_cur = l.state, l.cursor
        r_state, r_cur = r.state, r.cursor
    if l_state.location != r_state.location:
        raise AssertionError("divergence pair left different locations")
    l_ids = {a.id for a in enumerate_legal(l_state, content)}
    r_ids = {a.id for a in enumerate_legal(r_state, content)}
    if l_ids == r_ids:
        raise AssertionError("sheets produced identical legal sets in the shared scene")
    return l_ids, r_ids
