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
    )
    missing = [name for name in required if name not in by_id]
    if missing:
        raise AssertionError(f"I4 missing traces {missing}")

    for trace in traces:
        accept_trace(content, trace)

    compact = replay(content, by_id["marsh_harbor_compact"]["seed"], by_id["marsh_harbor_compact"]["sheet"], by_id["marsh_harbor_compact"]["actions"])
    relic = replay(content, by_id["marsh_stack_relic"]["seed"], by_id["marsh_stack_relic"]["sheet"], by_id["marsh_stack_relic"]["actions"])
    kiln = replay(content, by_id["marsh_kiln_pact"]["seed"], by_id["marsh_kiln_pact"]["sheet"], by_id["marsh_kiln_pact"]["actions"])
    if "harbor_compact" not in compact.state.outcomes:
        raise AssertionError("harbor_compact predicate failed")
    if "stack_relic" not in relic.state.outcomes:
        raise AssertionError("stack_relic predicate failed")
    if "kiln_pact" not in kiln.state.outcomes:
        raise AssertionError("kiln_pact predicate failed")
    if len({compact.fingerprint, relic.fingerprint, kiln.fingerprint}) != 3:
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

    return {
        "harbor_compact": compact.fingerprint,
        "stack_relic": relic.fingerprint,
        "kiln_pact": kiln.fingerprint,
        "marsh_only": sorted(m_ids - c_ids),
        "city_only": sorted(c_ids - m_ids),
        "mill_marsh_only": sorted(mill_m_ids - mill_c_ids),
        "mill_city_only": sorted(mill_c_ids - mill_m_ids),
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
