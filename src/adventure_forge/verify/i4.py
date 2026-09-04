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
    if len({compact.fingerprint, relic.fingerprint, kiln.fingerprint, court.fingerprint, beacon.fingerprint, fever.fingerprint, named.fingerprint, fold.fingerprint, lens.fingerprint, rope.fingerprint, salt.fingerprint, smoke.fingerprint, weir.fingerprint, dye.fingerprint, ferry.fingerprint, pump.fingerprint}) != 16:
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
