"""Behavioral check on the deployed surface.

The firewall scans `web.py` for banned imports, which proves the surface does
not read builder knowledge. It says nothing about what the surface accepts from
a player. That gap is how a client-supplied `state` block — the world moving
without `step` — passed a green bar.

This drives the real ASGI app end to end. No LLM, no network.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

from adventure_forge.kernel.content import Content
from adventure_forge.play.session import MAX_CLIENT_ACTIONS, PlaySession
from adventure_forge.web import app, play_turn


class WebSurfaceFail(AssertionError):
    pass


def _request(
    method: str,
    path: str,
    *,
    body: bytes = b"",
    content_type: str = "application/json",
) -> tuple[int, bytes]:
    """Drive the ASGI app once and return (status, body)."""
    scope = {
        "type": "http",
        "method": method,
        "path": path,
        "query_string": b"",
        "headers": [
            (b"content-type", content_type.encode("ascii")),
            (b"accept", b"application/json"),
        ],
    }
    sent: list[dict[str, Any]] = []
    delivered = {"done": False}

    async def receive() -> dict[str, Any]:
        if delivered["done"]:
            return {"type": "http.request", "body": b"", "more_body": False}
        delivered["done"] = True
        return {"type": "http.request", "body": body, "more_body": False}

    async def send(message: dict[str, Any]) -> None:
        sent.append(message)

    asyncio.run(app(scope, receive, send))
    status = next((m["status"] for m in sent if m["type"] == "http.response.start"), 0)
    payload = b"".join(m.get("body", b"") for m in sent if m["type"] == "http.response.body")
    return status, payload


def check_web_surface(content: Content) -> dict:
    """The surface must move the world only through step, and never 500."""
    # 1. A forged world is refused. This is the whole product claim.
    player = PlaySession.start(content, 1, "marsh_scout")
    forged = json.loads(json.dumps(player.dump()))
    forged["state"]["flags"] = {flag: True for flag in content.outcomes}
    forged["state"]["location"] = sorted(content.locations)[-1]
    try:
        result = play_turn(session=forged, line="wait")
    except ValueError:
        pass
    else:
        raise WebSurfaceFail(
            "client-supplied state was accepted: "
            f"{len(result['outcomes'])} outcomes awarded without step"
        )

    status, body = _request(
        "POST", "/play", body=json.dumps({"session": forged, "line": "wait"}).encode()
    )
    if status != 400:
        raise WebSurfaceFail(f"forged state over HTTP returned {status}, expected 400")

    # 2. A cursor alone is the same attack with one field removed.
    half = {"build_id": content.build_id, "seed": 1, "sheet": "marsh_scout", "cursor": {"seed": 1, "n": 0}}
    try:
        play_turn(session=half)
    except ValueError:
        pass
    else:
        raise WebSurfaceFail("client-supplied cursor was accepted")

    # 3. A legitimate compact session still plays, and still moves the world.
    first = play_turn(seed=1, sheet="marsh_scout")
    if first["outcomes"]:
        raise WebSurfaceFail("a new game already holds outcomes")
    second = play_turn(session=first["session"], line="go to market")
    if not second["accepted"] or second["location"] == first["location"]:
        raise WebSurfaceFail("legitimate compact session did not advance")

    # 4. An unmapped line must not move the world, and must not blank the room.
    before = second["fingerprint"]
    missed = play_turn(session=second["session"], line="summon a star from the sea")
    if missed["accepted"] or missed["fingerprint"] != before:
        raise WebSurfaceFail("unmapped text moved the world on the web surface")
    if "You can:" not in (missed.get("observation") or ""):
        raise WebSurfaceFail("a rejected line left the response without an observation (I8)")

    # 5. Replay cost is bounded, so one request cannot buy unbounded work.
    long_session = {
        "build_id": content.build_id,
        "seed": 1,
        "sheet": "marsh_scout",
        "actions": ["wait"] * (MAX_CLIENT_ACTIONS + 1),
    }
    try:
        play_turn(session=long_session)
    except ValueError:
        pass
    else:
        raise WebSurfaceFail("an unbounded client history was replayed")

    # 6. Nothing a client can type may reach an unhandled exception.
    malformed: list[tuple[str, bytes]] = [
        ("non-object body", b'"hello"'),
        ("session as string", b'{"session":"pwn"}'),
        ("session as list", b'{"session":[1,2,3]}'),
        ("seed as word", b'{"seed":"abc"}'),
        ("line as number", b'{"line":5}'),
        ("empty object", b"{}"),
        ("null session", b'{"session":null}'),
        ("bad build id", b'{"session":{"build_id":"nope","actions":[]}}'),
        ("actions not a list", b'{"session":{"build_id":"' + content.build_id.encode() + b'","actions":"x"}}'),
    ]
    for name, raw in malformed:
        status, _ = _request("POST", "/play", body=raw)
        if status >= 500:
            raise WebSurfaceFail(f"{name} returned {status}; a client typo must not 500")
        if status not in {200, 400}:
            raise WebSurfaceFail(f"{name} returned an unexpected {status}")

    status, _ = _request("POST", "/play", body=b"not json at all")
    if status != 400:
        raise WebSurfaceFail(f"malformed JSON returned {status}, expected 400")

    # 7. Health must prove it can serve, not assert it.
    status, body = _request("GET", "/health")
    if status != 200:
        raise WebSurfaceFail(f"/health returned {status}")
    health = json.loads(body)
    if health.get("build_id") != content.build_id:
        raise WebSurfaceFail("/health does not report the live pack build")

    return {"checked": 7}
