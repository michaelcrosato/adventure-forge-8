from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from adventure_forge.kernel.content import Content
from adventure_forge.kernel.fingerprint import fingerprint
from adventure_forge.kernel.replay import new_game
from adventure_forge.kernel.seed import SeedCursor
from adventure_forge.kernel.state import GameState
from adventure_forge.kernel.step import step
from adventure_forge.play.mapper import map_text
from adventure_forge.play.observe import PAGE_SIZE, Observation, observe

# An untrusted dump is rebuilt by replaying every id, so its cost is linear in
# the history. Bound it so one request cannot buy unbounded server work.
MAX_CLIENT_ACTIONS = 1000


@dataclass
class TurnResult:
    observation: Observation
    accepted: bool
    mapped: str | None
    ui: bool
    message: str


class PlaySession:
    """Player-surface session. World moves only through engine step on a legal id."""

    def __init__(self, content: Content, state: GameState, cursor: SeedCursor):
        self.content = content
        self.state = state
        self.cursor = cursor
        self.page = 0
        self.group: str | None = None
        self.history: list[str] = []

    @classmethod
    def start(cls, content: Content, seed: int, sheet: str | dict[str, str]) -> PlaySession:
        state, cursor = new_game(content, seed, sheet)
        return cls(content, state, cursor)

    def observation(self) -> Observation:
        return observe(self.state, self.content, page=self.page, group=self.group)

    def fingerprint(self) -> str:
        return fingerprint(self.state, self.cursor)

    def apply_line(self, line: str) -> TurnResult:
        text = line.strip()
        obs = self.observation()
        lowered = " ".join(text.lower().split())

        if lowered in {"", "look"}:
            return TurnResult(obs, False, None, True, obs.text)
        if lowered in {"help"}:
            msg = "Type a verb, a number, more, all, filter <group>, quit."
            return TurnResult(obs, False, None, True, msg)
        if lowered in {"inv", "inventory"}:
            names = []
            for item_id in self.state.inventory:
                names.append(str(self.content.items[item_id]["name"]))
            msg = "You carry: " + (", ".join(names) if names else "nothing.")
            return TurnResult(obs, False, None, True, msg)
        if lowered == "more":
            filtered = [a for a in obs.actions if self.group is None or a.group == self.group]
            if filtered:
                max_page = max(0, (len(filtered) - 1) // PAGE_SIZE)
                self.page = min(self.page + 1, max_page)
            return TurnResult(self.observation(), False, None, True, self.observation().text)
        if lowered == "all":
            self.page = 0
            self.group = None
            # Asked explicitly: list every id. Engine set is unchanged.
            lines = [f"{a.id}\t{a.label}" for a in obs.actions]
            msg = "Legal ids:\n" + "\n".join(lines)
            return TurnResult(obs, False, None, True, msg)
        if lowered.startswith("filter "):
            group = lowered.split(" ", 1)[1].strip()
            self.group = None if group in {"all", ""} else group
            self.page = 0
            return TurnResult(self.observation(), False, None, True, self.observation().text)
        if lowered.isdigit():
            idx = int(lowered) - 1
            if 0 <= idx < len(obs.visible):
                return self._step(obs.visible[idx].id)
            return TurnResult(obs, False, None, False, "That does nothing.")

        mapped = map_text(text, obs.actions)
        if mapped is None:
            return TurnResult(obs, False, None, False, "That does nothing.")
        return self._step(mapped)

    def _step(self, action_id: str) -> TurnResult:
        before = self.fingerprint()
        result = step(self.state, action_id, self.content, self.cursor)
        self.state = result.state
        self.cursor = result.cursor
        self.page = 0
        if result.accepted:
            self.history.append(action_id)
        obs = self.observation()
        if not result.accepted:
            assert self.fingerprint() == before
            return TurnResult(obs, False, action_id, False, "That does nothing.")
        return TurnResult(obs, True, action_id, False, obs.text)

    def dump(self, *, compact: bool = False) -> dict:
        """Serializable player session. Compact form is seed + accepted ids for HTTP."""
        if compact:
            return {
                "build_id": self.content.build_id,
                "seed": self.cursor.seed,
                "sheet": dict(self.state.sheet),
                "actions": list(self.history),
                "page": int(self.page),
                "group": self.group,
            }
        return {
            "build_id": self.content.build_id,
            "seed": self.cursor.seed,
            "cursor": self.cursor.to_dict(),
            "sheet": dict(self.state.sheet),
            "actions": list(self.history),
            "state": self.state.to_dict(),
            "fingerprint": self.fingerprint(),
            "page": int(self.page),
            "group": self.group,
        }

    @classmethod
    def from_dump(cls, content: Content, payload: dict, *, trusted: bool = True) -> PlaySession:
        """Rebuild a session from a dump.

        `trusted=True` is the local save file: the owner may hand back a
        materialized `state`/`cursor` and we restore it directly.

        `trusted=False` is any dump that crossed a network boundary. A caller
        there does not get to declare the world. We accept seed + sheet +
        accepted action ids only, and rebuild by replaying every id through the
        real `step`, so the reconstructed state is one the engine agreed to.
        """
        if not isinstance(payload, dict):
            raise ValueError("session must be an object")
        if payload.get("build_id") != content.build_id:
            raise ValueError("save build does not match current pack")

        materialized = "state" in payload or "cursor" in payload
        if materialized and not trusted:
            # The whole product claim is that the world moves only through step.
            # A client-supplied state is the world moving without step.
            raise ValueError("session state is not accepted from this surface")

        if materialized and trusted:
            if "state" not in payload or "cursor" not in payload:
                raise ValueError("save is missing state or cursor")
            state = GameState.from_dict(payload["state"])
            cursor = SeedCursor.from_dict(payload["cursor"])
            session = cls(content, state, cursor)
            session.history = list(payload.get("actions", []))
            session._restore_view(payload)
            return session

        actions = payload.get("actions", [])
        if not isinstance(actions, list):
            raise ValueError("session actions must be a list")
        if not trusted and len(actions) > MAX_CLIENT_ACTIONS:
            raise ValueError("session too long to replay")
        try:
            seed = int(payload.get("seed", 1))
        except (TypeError, ValueError) as exc:
            raise ValueError("session seed must be an integer") from exc
        sheet = payload.get("sheet") or "marsh_scout"
        if not isinstance(sheet, (str, dict)):
            raise ValueError("session sheet must be a name or a sheet object")
        session = cls.start(content, seed, sheet)
        for action_id in actions:
            result = session._step(str(action_id))
            if not result.accepted:
                raise ValueError("session replay rejected")
        session._restore_view(payload)
        return session

    def _restore_view(self, payload: dict) -> None:
        """Restore presentation-only fields. These never touch the world."""
        try:
            self.page = max(0, int(payload.get("page", 0)))
        except (TypeError, ValueError):
            self.page = 0
        group = payload.get("group")
        self.group = None if group in {None, ""} else str(group)

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(self.dump(), indent=2, sort_keys=True) + "\n", encoding="utf-8")

    @classmethod
    def load(cls, content: Content, path: Path) -> PlaySession:
        return cls.from_dump(content, json.loads(path.read_text(encoding="utf-8")))
