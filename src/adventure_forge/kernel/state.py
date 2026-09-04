from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def tide(state: GameState) -> str:
    return "low" if (state.turn // 4) % 2 == 0 else "high"


WEATHER_CYCLE = ("clear", "rain", "fog")


def weather(state: GameState) -> str:
    """Turn-derived weather. No wall clock."""
    return WEATHER_CYCLE[(state.turn // 3) % 3]


@dataclass
class GameState:
    build_id: str
    location: str
    sheet: dict[str, str]
    flags: dict[str, bool] = field(default_factory=dict)
    inventory: list[str] = field(default_factory=list)
    ground: dict[str, list[str]] = field(default_factory=dict)
    actors: dict[str, str] = field(default_factory=dict)
    memory: dict[str, list[str]] = field(default_factory=dict)
    rep: dict[str, int] = field(default_factory=dict)
    hp: int = 6
    turn: int = 0
    outcomes: list[str] = field(default_factory=list)
    log: list[dict[str, Any]] = field(default_factory=list)
    last_text: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "build_id": self.build_id,
            "location": self.location,
            "sheet": dict(sorted(self.sheet.items())),
            "flags": dict(sorted((k, bool(v)) for k, v in self.flags.items())),
            "inventory": list(self.inventory),
            "ground": {k: list(v) for k, v in sorted(self.ground.items())},
            "actors": dict(sorted(self.actors.items())),
            "memory": {k: list(v) for k, v in sorted(self.memory.items())},
            "rep": {k: int(v) for k, v in sorted(self.rep.items())},
            "hp": int(self.hp),
            "turn": int(self.turn),
            "outcomes": list(self.outcomes),
            "log": list(self.log),
            "last_text": self.last_text,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GameState:
        return cls(
            build_id=str(data["build_id"]),
            location=str(data["location"]),
            sheet={str(k): str(v) for k, v in data["sheet"].items()},
            flags={str(k): bool(v) for k, v in data.get("flags", {}).items()},
            inventory=[str(x) for x in data.get("inventory", [])],
            ground={str(k): [str(i) for i in v] for k, v in data.get("ground", {}).items()},
            actors={str(k): str(v) for k, v in data.get("actors", {}).items()},
            memory={str(k): [str(f) for f in v] for k, v in data.get("memory", {}).items()},
            rep={str(k): int(v) for k, v in data.get("rep", {}).items()},
            hp=int(data.get("hp", 6)),
            turn=int(data.get("turn", 0)),
            outcomes=[str(x) for x in data.get("outcomes", [])],
            log=list(data.get("log", [])),
            last_text=str(data.get("last_text", "")),
        )

    def clone(self) -> GameState:
        return GameState.from_dict(self.to_dict())
