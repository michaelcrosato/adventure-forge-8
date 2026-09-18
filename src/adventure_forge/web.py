"""ASGI surface for the Vercel deployment.

The kernel stays pure. This module loads the pack, wraps PlaySession, and
serves a playable HTTP page plus JSON turns. The model is never the physics.
"""

from __future__ import annotations

import html
import json
from collections.abc import Awaitable, Callable
from typing import Any
from urllib.parse import parse_qs

from adventure_forge import ENGINE_VERSION
from adventure_forge.kernel.content import load_pack
from adventure_forge.play.session import PlaySession

Send = Callable[[dict[str, Any]], Awaitable[None]]
Receive = Callable[[], Awaitable[dict[str, Any]]]

_PACK = None


def _content():
    global _PACK
    if _PACK is None:
        _PACK = load_pack()
    return _PACK


def _json_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


async def _read_body(receive: Receive) -> bytes:
    chunks: list[bytes] = []
    while True:
        message = await receive()
        chunks.append(message.get("body", b"") or b"")
        if not message.get("more_body"):
            return b"".join(chunks)


async def _send_response(
    send: Send,
    *,
    status: int,
    body: bytes,
    content_type: bytes,
    include_body: bool = True,
    extra_headers: list[tuple[bytes, bytes]] | None = None,
) -> None:
    headers = [
        (b"content-type", content_type),
        (b"content-length", str(len(body)).encode("ascii")),
        (b"cache-control", b"no-store"),
    ]
    if extra_headers:
        headers.extend(extra_headers)
    await send({"type": "http.response.start", "status": status, "headers": headers})
    await send({"type": "http.response.body", "body": body if include_body else b""})


def play_turn(
    *,
    seed: int = 1,
    sheet: str = "marsh_scout",
    session: dict[str, Any] | None = None,
    line: str | None = None,
) -> dict[str, Any]:
    """Drive the shipped PlaySession. Illegal text does not call step."""
    content = _content()
    if session:
        # Across HTTP the caller is untrusted: it may hand us ids to replay,
        # never a world to adopt.
        player = PlaySession.from_dump(content, session, trusted=False)
    else:
        player = PlaySession.start(content, int(seed), sheet or "marsh_scout")
    accepted = False
    mapped = None
    if line is not None and str(line).strip() != "":
        result = player.apply_line(str(line))
        accepted = bool(result.accepted)
        mapped = result.mapped
        text = result.message
    else:
        text = player.observation().text
    obs = player.observation()
    return {
        "accepted": accepted,
        "mapped": mapped,
        "text": text,
        # The page is the observation (I8). Keep it available even when the
        # turn message is a rejection, so a miss never blanks the room.
        "observation": obs.text,
        "location": player.state.location,
        "fingerprint": player.fingerprint(),
        "outcomes": list(player.state.outcomes),
        "session": player.dump(compact=True),
        "verbs": [{"id": a.id, "label": a.label} for a in obs.visible],
    }


def _html_page(payload: dict[str, Any]) -> bytes:
    session_json = json.dumps(payload["session"], separators=(",", ":"))
    # I8: a competent agent takes a full turn from one observation. Render the
    # room every time, and put any rejection above it as a short notice.
    observation = payload.get("observation") or payload["text"]
    message = payload["text"]
    notice = ""
    if message and message != observation:
        notice = f"<p role=\"status\"><strong>{html.escape(message)}</strong></p>"
    verbs = "".join(
        f"<li><code>{html.escape(v['id'])}</code> {html.escape(v['label'])}</li>"
        for v in payload.get("verbs", [])
    )
    body = (
        "<!doctype html><html lang=\"en\"><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        "<title>Adventure Forge</title>"
        "<style>body{font:16px/1.4 sans-serif;max-width:42rem;margin:1.5rem auto;padding:0 1rem}"
        "pre{white-space:pre-wrap;background:#f4f1ea;padding:1rem}"
        "input[type=text]{width:100%;padding:.4rem}button{margin-top:.5rem}</style>"
        "<body><main><h1>Adventure Forge</h1>"
        "<p>Type a verb. Illegal text does not move the world.</p>"
        f"{notice}"
        f"<pre>{html.escape(observation)}</pre>"
        "<form method=\"post\" action=\"/\">"
        f"<input type=\"hidden\" name=\"session\" value=\"{html.escape(session_json, quote=True)}\">"
        "<label>What do you do?<br>"
        "<input type=\"text\" name=\"line\" autofocus></label><br>"
        "<button type=\"submit\">Act</button></form>"
        "<p><a href=\"/\">New game</a> · <a href=\"/health\">Health</a></p>"
        f"<ul>{verbs}</ul>"
        "</main></body></html>"
    )
    return body.encode("utf-8")


def _header_map(scope: dict[str, Any]) -> dict[bytes, bytes]:
    return {k.lower(): v for k, v in scope.get("headers", [])}


def _wants_json(scope: dict[str, Any]) -> bool:
    accept = _header_map(scope).get(b"accept", b"").decode("latin-1", "replace")
    return "application/json" in accept


async def app(scope: dict[str, Any], receive: Receive, send: Send) -> None:
    """Serve health, a playable page, and JSON play turns."""
    if scope["type"] == "lifespan":
        while True:
            message = await receive()
            if message["type"] == "lifespan.startup":
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                await send({"type": "lifespan.shutdown.complete"})
                return

    if scope["type"] != "http":
        return

    method = scope.get("method", "GET").upper()
    path = scope.get("path", "/")
    include_body = method != "HEAD"
    query = parse_qs(scope.get("query_string", b"").decode("latin-1"))

    if path == "/health":
        if method not in {"GET", "HEAD"}:
            await _send_response(
                send,
                status=405,
                body=_json_bytes({"error": "method_not_allowed"}),
                content_type=b"application/json; charset=utf-8",
                extra_headers=[(b"allow", b"GET, HEAD")],
            )
            return
        # A health check that never loads the pack cannot detect the one
        # failure this deployment is actually shaped to have.
        try:
            content = _content()
        except Exception as exc:  # noqa: BLE001 — report any load failure as unhealthy
            await _send_response(
                send,
                status=503,
                body=_json_bytes(
                    {
                        "engine_version": ENGINE_VERSION,
                        "service": "adventure-forge",
                        "status": "unavailable",
                        "error": type(exc).__name__,
                    }
                ),
                content_type=b"application/json; charset=utf-8",
                include_body=include_body,
            )
            return
        await _send_response(
            send,
            status=200,
            body=_json_bytes(
                {
                    "engine_version": ENGINE_VERSION,
                    "service": "adventure-forge",
                    "status": "ok",
                    "play": "/play",
                    "build_id": content.build_id,
                    "locations": len(content.locations),
                }
            ),
            content_type=b"application/json; charset=utf-8",
            include_body=include_body,
        )
        return

    if path in {"/", "/play"}:
        if method not in {"GET", "HEAD", "POST"}:
            await _send_response(
                send,
                status=405,
                body=_json_bytes({"error": "method_not_allowed"}),
                content_type=b"application/json; charset=utf-8",
                extra_headers=[(b"allow", b"GET, HEAD, POST")],
            )
            return
        seed = 1
        sheet = "marsh_scout"
        session = None
        line = None
        content_type = _header_map(scope).get(b"content-type", b"").decode("latin-1", "replace")
        if method == "POST":
            raw = await _read_body(receive)
            if "application/json" in content_type:
                try:
                    data = json.loads(raw.decode("utf-8") or "{}")
                except json.JSONDecodeError:
                    await _send_response(
                        send,
                        status=400,
                        body=_json_bytes({"error": "bad_json"}),
                        content_type=b"application/json; charset=utf-8",
                    )
                    return
                if not isinstance(data, dict):
                    await _send_response(
                        send,
                        status=400,
                        body=_json_bytes({"error": "body must be a JSON object"}),
                        content_type=b"application/json; charset=utf-8",
                    )
                    return
                try:
                    seed = int(data.get("seed") or 1)
                except (TypeError, ValueError):
                    await _send_response(
                        send,
                        status=400,
                        body=_json_bytes({"error": "seed must be an integer"}),
                        content_type=b"application/json; charset=utf-8",
                    )
                    return
                sheet = str(data.get("sheet") or "marsh_scout")
                session = data.get("session")
                if session is not None and not isinstance(session, dict):
                    await _send_response(
                        send,
                        status=400,
                        body=_json_bytes({"error": "session must be an object"}),
                        content_type=b"application/json; charset=utf-8",
                    )
                    return
                line = data.get("line")
                if line is not None and not isinstance(line, str):
                    await _send_response(
                        send,
                        status=400,
                        body=_json_bytes({"error": "line must be a string"}),
                        content_type=b"application/json; charset=utf-8",
                    )
                    return
            else:
                form = parse_qs(raw.decode("utf-8", "replace"), keep_blank_values=True)
                try:
                    seed = int((form.get("seed") or ["1"])[0] or 1)
                except (TypeError, ValueError):
                    await _send_response(
                        send,
                        status=400,
                        body=_json_bytes({"error": "seed must be an integer"}),
                        content_type=b"application/json; charset=utf-8",
                    )
                    return
                sheet = (form.get("sheet") or ["marsh_scout"])[0] or "marsh_scout"
                line = (form.get("line") or [None])[0]
                raw_session = (form.get("session") or [""])[0]
                if raw_session:
                    try:
                        session = json.loads(raw_session)
                    except json.JSONDecodeError:
                        await _send_response(
                            send,
                            status=400,
                            body=_json_bytes({"error": "bad_session"}),
                            content_type=b"application/json; charset=utf-8",
                        )
                        return
                    if not isinstance(session, dict):
                        await _send_response(
                            send,
                            status=400,
                            body=_json_bytes({"error": "bad_session"}),
                            content_type=b"application/json; charset=utf-8",
                        )
                        return
        else:
            if query.get("seed"):
                try:
                    seed = int(query["seed"][0])
                except (TypeError, ValueError):
                    await _send_response(
                        send,
                        status=400,
                        body=_json_bytes({"error": "seed must be an integer"}),
                        content_type=b"application/json; charset=utf-8",
                    )
                    return
            if query.get("sheet"):
                sheet = query["sheet"][0]
            if query.get("line"):
                line = query["line"][0]
        try:
            payload = play_turn(seed=seed, sheet=sheet, session=session, line=line)
        except (ValueError, TypeError, KeyError) as exc:
            await _send_response(
                send,
                status=400,
                body=_json_bytes({"error": str(exc) or type(exc).__name__}),
                content_type=b"application/json; charset=utf-8",
            )
            return
        if path == "/play" or _wants_json(scope):
            await _send_response(
                send,
                status=200,
                body=_json_bytes(payload),
                content_type=b"application/json; charset=utf-8",
                include_body=include_body,
            )
            return
        await _send_response(
            send,
            status=200,
            body=_html_page(payload),
            content_type=b"text/html; charset=utf-8",
            include_body=include_body,
        )
        return

    await _send_response(
        send,
        status=404,
        body=_json_bytes({"error": "not_found"}),
        content_type=b"application/json; charset=utf-8",
        include_body=include_body,
    )
