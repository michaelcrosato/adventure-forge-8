from __future__ import annotations

from adventure_forge.kernel.content import Content
from adventure_forge.kernel.legal import enumerate_legal
from adventure_forge.kernel.replay import new_game, replay
from adventure_forge.kernel.step import step


def _load_ok(content: Content, trace: dict) -> None:
    result = replay(content, trace["seed"], trace["sheet"], trace["actions"])
    if content.build_id == trace.get("build_id") and result.fingerprint != trace["final_fingerprint"]:
        raise AssertionError(
            f"{trace['id']} fingerprint mismatch on same build"
        )
    outcome = trace.get("outcome")
    if outcome and outcome not in result.state.outcomes:
        raise AssertionError(f"{trace['id']} missing outcome {outcome}: {result.state.outcomes}")
    if result.state.build_id != content.build_id:
        raise AssertionError("replay state build_id drifted")


def check_i4(content: Content, traces: list[dict]) -> dict:
    by_id = {t["id"]: t for t in traces}
    required = ("marsh_harbor_compact", "marsh_stack_relic", "divergence_marsh_market", "divergence_city_market")
    missing = [name for name in required if name not in by_id]
    if missing:
        raise AssertionError(f"I4 missing traces {missing}")

    for trace in traces:
        _load_ok(content, trace)

    compact = replay(content, by_id["marsh_harbor_compact"]["seed"], by_id["marsh_harbor_compact"]["sheet"], by_id["marsh_harbor_compact"]["actions"])
    relic = replay(content, by_id["marsh_stack_relic"]["seed"], by_id["marsh_stack_relic"]["sheet"], by_id["marsh_stack_relic"]["actions"])
    if "harbor_compact" not in compact.state.outcomes:
        raise AssertionError("harbor_compact predicate failed")
    if "stack_relic" not in relic.state.outcomes:
        raise AssertionError("stack_relic predicate failed")
    if compact.fingerprint == relic.fingerprint:
        raise AssertionError("distinct outcomes share a fingerprint")

    marsh = by_id["divergence_marsh_market"]
    city = by_id["divergence_city_market"]
    if marsh["actions"] != city["actions"]:
        raise AssertionError("divergence pair must share the same action prefix")

    m_state, m_cur = new_game(content, marsh["seed"], marsh["sheet"])
    c_state, c_cur = new_game(content, city["seed"], city["sheet"])
    for action_id in marsh["actions"]:
        m = step(m_state, action_id, content, m_cur)
        c = step(c_state, action_id, content, c_cur)
        if not m.accepted or not c.accepted:
            raise AssertionError("divergence prefix rejected")
        m_state, m_cur = m.state, m.cursor
        c_state, c_cur = c.state, c.cursor
    if m_state.location != c_state.location:
        raise AssertionError("divergence pair left different locations")
    m_ids = {a.id for a in enumerate_legal(m_state, content)}
    c_ids = {a.id for a in enumerate_legal(c_state, content)}
    if m_ids == c_ids:
        raise AssertionError("sheets produced identical legal sets in the shared scene")
    if "use_marsh_cant" not in m_ids:
        raise AssertionError("marsh_scout missing use_marsh_cant")
    if "show_city_papers" not in c_ids:
        raise AssertionError("city_oath missing show_city_papers")
    if "use_marsh_cant" in c_ids or "show_city_papers" in m_ids:
        raise AssertionError("sheet verbs leaked across sheets")

    return {
        "harbor_compact": compact.fingerprint,
        "stack_relic": relic.fingerprint,
        "marsh_only": sorted(m_ids - c_ids),
        "city_only": sorted(c_ids - m_ids),
    }
