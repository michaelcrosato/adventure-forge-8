"""Drive the shipped ASGI play adapter. No mocked step."""

from __future__ import annotations

import asyncio
import json
import unittest

import app as vercel_entrypoint
from adventure_forge.web import app


def request(
    path: str = "/",
    method: str = "GET",
    *,
    body: bytes = b"",
    content_type: str = "text/plain",
    accept: str = "*/*",
    query: bytes = b"",
) -> list[dict]:
    sent: list[dict] = []
    remaining = body

    async def receive() -> dict:
        nonlocal remaining
        chunk = remaining
        remaining = b""
        return {"type": "http.request", "body": chunk, "more_body": False}

    async def send(message: dict) -> None:
        sent.append(message)

    scope = {
        "type": "http",
        "method": method,
        "path": path,
        "query_string": query,
        "headers": [
            (b"content-type", content_type.encode("ascii")),
            (b"accept", accept.encode("ascii")),
        ],
    }
    asyncio.run(app(scope, receive, send))
    return sent


def _json(messages: list[dict]) -> dict:
    return json.loads(messages[1]["body"])


class WebEntrypointTests(unittest.TestCase):
    def test_root_module_exports_app(self) -> None:
        self.assertIs(vercel_entrypoint.app, app)

    def test_home_is_playable(self) -> None:
        messages = request()
        self.assertEqual(messages[0]["status"], 200)
        body = messages[1]["body"]
        self.assertIn(b"Adventure Forge", body)
        self.assertIn(b"You can:", body)
        self.assertIn(b"Go to market", body)

    def test_health(self) -> None:
        messages = request("/health")
        self.assertEqual(messages[0]["status"], 200)
        payload = _json(messages)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["service"], "adventure-forge")
        self.assertEqual(payload["play"], "/play")

    def test_head_has_no_body(self) -> None:
        messages = request("/health", "HEAD")
        self.assertEqual(messages[0]["status"], 200)
        self.assertEqual(messages[1]["body"], b"")

    def test_unknown_path(self) -> None:
        messages = request("/missing")
        self.assertEqual(messages[0]["status"], 404)

    def test_unsupported_method(self) -> None:
        messages = request("/health", "POST")
        self.assertEqual(messages[0]["status"], 405)
        headers = dict(messages[0]["headers"])
        self.assertEqual(headers[b"allow"], b"GET, HEAD")

    def test_json_start_shows_verbs(self) -> None:
        messages = request("/play", accept="application/json")
        self.assertEqual(messages[0]["status"], 200)
        payload = _json(messages)
        self.assertEqual(payload["location"], "saltfen.dock")
        self.assertIn("You can:", payload["text"])
        self.assertTrue(payload["verbs"])
        self.assertIn("session", payload)
        self.assertFalse(payload["accepted"])

    def test_legal_line_advances_through_shipped_session(self) -> None:
        start = _json(request("/play", accept="application/json"))
        before = start["fingerprint"]
        messages = request(
            "/play",
            "POST",
            body=json.dumps({"session": start["session"], "line": "go to market"}).encode("utf-8"),
            content_type="application/json",
        )
        self.assertEqual(messages[0]["status"], 200)
        payload = _json(messages)
        self.assertTrue(payload["accepted"])
        self.assertEqual(payload["mapped"], "go:saltfen.market")
        self.assertEqual(payload["location"], "saltfen.market")
        self.assertNotEqual(payload["fingerprint"], before)
        self.assertIn("You can:", payload["text"])

    def test_unmapped_text_does_not_move_the_world(self) -> None:
        start = _json(request("/play", accept="application/json"))
        before = start["fingerprint"]
        messages = request(
            "/play",
            "POST",
            body=json.dumps({"session": start["session"], "line": "summon a dry wind"}).encode("utf-8"),
            content_type="application/json",
        )
        payload = _json(messages)
        self.assertFalse(payload["accepted"])
        self.assertIsNone(payload["mapped"])
        self.assertEqual(payload["fingerprint"], before)
        self.assertEqual(payload["location"], start["location"])


if __name__ == "__main__":
    unittest.main()
