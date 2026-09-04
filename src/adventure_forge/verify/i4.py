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
    if len({compact.fingerprint, relic.fingerprint, kiln.fingerprint, court.fingerprint, beacon.fingerprint, fever.fingerprint, named.fingerprint, fold.fingerprint, lens.fingerprint}) != 9:
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
