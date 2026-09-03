from __future__ import annotations

from adventure_forge.kernel.content import Content
from adventure_forge.kernel.fingerprint import fingerprint
from adventure_forge.kernel.legal import enumerate_legal
from adventure_forge.kernel.replay import new_game
from adventure_forge.kernel.step import step


class CrawlerFail(AssertionError):
    pass


def _impure(content: Content, state, cursor, action_id: str) -> bool:
    a = step(state, action_id, content, cursor)
    b = step(state, action_id, content, cursor)
    return fingerprint(a.state, a.cursor) != fingerprint(b.state, b.cursor)


def crawl(content: Content, *, max_nodes: int = 4000) -> dict:
    seen: set[str] = set()
    salvage_ok = False
    empty = []
    impure = []
    crashes = []
    visited_regions: set[str] = set()

    for sheet_name, seed in (("marsh_scout", 1), ("city_oath", 1), ("marsh_scout", 7)):
        state, cursor = new_game(content, seed, sheet_name)
        queue = [(state, cursor)]
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
    return {"nodes": len(seen), "regions": sorted(visited_regions)}
