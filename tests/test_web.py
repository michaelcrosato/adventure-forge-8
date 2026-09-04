from __future__ import annotations

import asyncio
import json
import unittest

import app as vercel_entrypoint
from adventure_forge.web import app


def request(path: str = "/", method: str = "GET") -> list[dict]:
    sent: list[dict] = []

    async def receive() -> dict:
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message: dict) -> None:
        sent.append(message)

    scope = {"type": "http", "method": method, "path": path}
    asyncio.run(app(scope, receive, send))
    return sent


class WebEntrypointTests(unittest.TestCase):
    def test_root_module_exports_app(self) -> None:
        self.assertIs(vercel_entrypoint.app, app)

    def test_home(self) -> None:
        messages = request()
        self.assertEqual(messages[0]["status"], 200)
        self.assertIn(b"Adventure Forge", messages[1]["body"])

    def test_health(self) -> None:
        messages = request("/health")
        self.assertEqual(messages[0]["status"], 200)
        payload = json.loads(messages[1]["body"])
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["service"], "adventure-forge")

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


if __name__ == "__main__":
    unittest.main()
