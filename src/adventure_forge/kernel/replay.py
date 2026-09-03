from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from adventure_forge.kernel.content import AXES, Content, validate_sheet
from adventure_forge.kernel.fingerprint import fingerprint
from adventure_forge.kernel.seed import SeedCursor
from adventure_forge.kernel.state import GameState
from adventure_forge.kernel.step import StepResult, step


class ReplayError(ValueError):
    pass


def resolve_sheet(content: Content, sheet: str | dict[str, str]) -> dict[str, str]:
    if isinstance(sheet, str):
        if sheet not in content.sheets:
            raise ReplayError(f"unknown preset {sheet}")
        resolved = dict(content.sheets[sheet])
    else:
        resolved = dict(sheet)
    validate_sheet(resolved)
    return {axis: resolved[axis] for axis in AXES}


def new_game(content: Content, seed: int, sheet: str | dict[str, str]) -> tuple[GameState, SeedCursor]:
    resolved = resolve_sheet(content, sheet)
    start = content.start
    ground = {loc_id: list(loc.get("ground", [])) for loc_id, loc in content.locations.items()}
    actors = {}
    for loc_id, loc in content.locations.items():
        for actor_id in loc.get("actors", []):
            actors[actor_id] = loc_id
    inventory = list(start.get("inventory", []))
    if resolved.get("origin") == "cityward" and "city_papers" not in inventory:
        inventory.append("city_papers")
    state = GameState(
        build_id=content.build_id,
        location=str(start["location"]),
        sheet=resolved,
        flags={k: bool(v) for k, v in start.get("flags", {}).items()},
        inventory=inventory,
        ground=ground,
        actors=actors,
        memory={},
        rep={k: int(v) for k, v in start.get("rep", {}).items()},
        hp=int(start.get("hp", 6)),
        turn=0,
        outcomes=[],
        log=[],
        last_text="",
    )
    return state, SeedCursor(seed=int(seed), index=0)


@dataclass
class ReplayResult:
    state: GameState
    cursor: SeedCursor
    fingerprints: list[str]
    accepted: list[bool]

    @property
    def fingerprint(self) -> str:
        return fingerprint(self.state, self.cursor)


def replay(
    content: Content,
    seed: int,
    sheet: str | dict[str, str],
    actions: Iterable[str],
    require_accepted: bool = True,
) -> ReplayResult:
    state, cursor = new_game(content, seed, sheet)
    fps: list[str] = [fingerprint(state, cursor)]
    accepted: list[bool] = []
    for action_id in actions:
        result: StepResult = step(state, action_id, content, cursor)
        if require_accepted and not result.accepted:
            raise ReplayError(f"illegal action during replay: {action_id} at {state.location}")
        state = result.state
        cursor = result.cursor
        accepted.append(result.accepted)
        fps.append(fingerprint(state, cursor))
    return ReplayResult(state=state, cursor=cursor, fingerprints=fps, accepted=accepted)
