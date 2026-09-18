from __future__ import annotations

from collections import Counter

from adventure_forge.kernel.content import Content
from adventure_forge.kernel.fingerprint import fingerprint
from adventure_forge.kernel.legal import enumerate_legal
from adventure_forge.kernel.replay import new_game
from adventure_forge.kernel.step import step


class CrawlerFail(AssertionError):
    pass


# How many distinct states each action id gets probed for impurity.
#
# The old crawler probed every action at every node, which meant `step` ran
# three times per edge and the same id was re-probed thousands of times. An
# impure `step` — wall clock, ambient RNG, mutated content — shows on the first
# probe, not the four-thousandth. Probing each id in several distinct states
# keeps the state diversity that could expose a conditional impurity, and drops
# the redundancy that was costing ~4 minutes of every run.
PURITY_PROBES_PER_ACTION = 3

# Ceiling on shipped actions the crawl never touched.
#
# The crawler reported "regions: 144" while never probing 1009 of 1306 actions,
# so it read as full coverage while exercising a quarter of the world. Seeding
# from trace end states brought that to 323. This ceiling keeps the number from
# drifting back up unnoticed — if it trips, the crawl lost reach, or content
# shipped that no trace and no walk can get to.
MAX_ACTIONS_NEVER_PROBED = 400


def _impure(content: Content, state, cursor, action_id: str) -> bool:
    a = step(state, action_id, content, cursor)
    b = step(state, action_id, content, cursor)
    return fingerprint(a.state, a.cursor) != fingerprint(b.state, b.cursor)


def crawl(content: Content, *, max_nodes: int = 4000, seeds=None) -> dict:
    """Drive the real engine looking for crashes, dead ends, bounds and impurity.

    A breadth-first walk from a fresh game spends its whole budget near the
    start: at 4000 nodes it never probed 1009 of the 1306 shipped actions, so
    most of the world was crawled in name only. `seeds` accepts already-deep
    states — the end state of every recorded trace — which puts the walk inside
    all 144 regions before it spends a node on breadth.
    """
    seen: set[str] = set()
    salvage_ok = False
    empty = []
    impure = []
    crashes = []
    visited_regions: set[str] = set()
    probed: Counter = Counter()

    starts = [
        new_game(content, seed, sheet_name)
        for sheet_name, seed in (("marsh_scout", 1), ("city_oath", 1), ("marsh_scout", 7))
    ]
    starts.extend(seeds or [])

    # One FIFO queue over every start, so the budget spreads across the world
    # instead of draining into the first start's neighbourhood.
    queue = list(starts)
    while queue and len(seen) < max_nodes:
        state, cursor = queue.pop(0)
        fp = fingerprint(state, cursor)
        if fp in seen:
            continue
        seen.add(fp)
        visited_regions.add(content.location_region(state.location))
        try:
            legal = enumerate_legal(state, content)
        except Exception as exc:  # noqa: BLE001 — crawler must surface engine faults
            crashes.append(f"{state.location}: {exc}")
            continue
        if not legal:
            empty.append(state.location)
            continue
        if state.hp < 1 or state.hp > 12:
            crashes.append(f"hp bounds {state.hp} at {state.location}")
        take_salvage = [a.id for a in legal if a.id.startswith("take:salvage_")]
        if state.location == "saltfen.salvage" and len(take_salvage) >= 100:
            salvage_ok = True
            # Do not expand every salvage take (branch bomb). Probe one, plus non-take.
        for action in legal:
            if state.location == "saltfen.salvage" and action.id.startswith("take:salvage_"):
                if action.id != "take:salvage_000":
                    continue
            try:
                if probed[action.id] < PURITY_PROBES_PER_ACTION:
                    probed[action.id] += 1
                    if _impure(content, state, cursor, action.id):
                        impure.append(action.id)
                        continue
                nxt = step(state, action.id, content, cursor)
                if nxt.accepted:
                    queue.append((nxt.state, nxt.cursor))
            except Exception as exc:  # noqa: BLE001
                crashes.append(f"{action.id} at {state.location}: {exc}")

    if empty:
        raise CrawlerFail(f"empty legal set: {empty[:5]}")
    if impure:
        raise CrawlerFail(f"impure step: {impure[:5]}")
    if crashes:
        raise CrawlerFail(f"crawler crashes: {crashes[:5]}")
    if not salvage_ok:
        raise CrawlerFail("salvage yard never offered 100+ take actions")
    if visited_regions != set(content.regions):
        raise CrawlerFail(f"crawler missed regions {set(content.regions) - visited_regions}")
    unprobed = {a["id"] for a in content.actions} - set(probed)
    if len(unprobed) > MAX_ACTIONS_NEVER_PROBED:
        raise CrawlerFail(
            f"crawl never probed {len(unprobed)} of {len(content.actions)} actions "
            f"(ceiling {MAX_ACTIONS_NEVER_PROBED}); coverage regressed or unreachable "
            f"content shipped: {sorted(unprobed)[:5]}"
        )
    return {
        "nodes": len(seen),
        "regions": sorted(visited_regions),
        "purity_probes": sum(probed.values()),
        "actions_never_probed": len(unprobed),
    }


def trace_seeds(content: Content, traces: list[dict]) -> list[tuple]:
    """End states of recorded traces, as crawl starting points.

    The traces already walk into every shipped region. Reusing them as seeds
    turns evidence the repo already has into crawler coverage it did not.
    """
    from adventure_forge.kernel.replay import replay

    out = []
    for trace in traces:
        try:
            result = replay(content, trace["seed"], trace["sheet"], trace["actions"])
        except Exception:  # noqa: BLE001 — a bad trace is I4's job to report
            continue
        out.append((result.state, result.cursor))
    return out
