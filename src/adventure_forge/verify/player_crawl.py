"""Crawler on the player surface (PlaySession), not a kernel double."""

from __future__ import annotations

from adventure_forge.kernel.content import Content
from adventure_forge.play.session import PlaySession


class PlayerCrawlFail(AssertionError):
    pass


def player_crawl(content: Content, *, max_nodes: int = 800) -> dict:
    seen: set[str] = set()
    empty = []
    for sheet in ("marsh_scout", "city_oath"):
        session = PlaySession.start(content, 1, sheet)
        queue = [session]
        while queue and len(seen) < max_nodes:
            session = queue.pop(0)
            fp = session.fingerprint()
            if fp in seen:
                continue
            seen.add(fp)
            obs = session.observation()
            if not obs.actions:
                empty.append(session.state.location)
                continue
            if "You can:" not in obs.text:
                raise PlayerCrawlFail(f"observation missing verbs at {session.state.location}")
            before = session.fingerprint()
            noop = session.apply_line("summon a star from the sea")
            if noop.accepted or session.fingerprint() != before:
                raise PlayerCrawlFail("unmapped text moved the world")
            # Expand a few legal ids through the player mapper/session, not raw step.
            for action in obs.actions:
                if session.state.location == "saltfen.salvage" and action.id.startswith("take:salvage_"):
                    if action.id != "take:salvage_000":
                        continue
                child = PlaySession(content, session.state.clone(), session.cursor.clone())
                child.history = list(session.history)
                result = child.apply_line(action.id)
                if result.accepted:
                    queue.append(child)
    if empty:
        raise PlayerCrawlFail(f"empty legal set on player surface: {empty[:5]}")
    return {"nodes": len(seen)}
