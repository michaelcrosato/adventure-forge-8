from __future__ import annotations

from typing import Any

from adventure_forge.kernel.ops import COND_KEYS
from adventure_forge.kernel.state import GameState, tide, weather


class UnknownCondition(ValueError):
    pass


def matches(cond: dict[str, Any] | None, state: GameState, content: Any | None = None) -> bool:
    if cond is None:
        return True
    if not isinstance(cond, dict) or not cond:
        raise UnknownCondition(f"invalid condition: {cond!r}")
    keys = set(cond.keys())
    if not keys <= COND_KEYS:
        raise UnknownCondition(f"unknown condition keys: {keys - COND_KEYS}")
    if len(keys) != 1:
        raise UnknownCondition(f"condition must have one key: {cond!r}")
    key = next(iter(keys))
    val = cond[key]
    if key == "all":
        return all(matches(c, state, content) for c in val)
    if key == "any":
        return any(matches(c, state, content) for c in val)
    if key == "not":
        return not matches(val, state, content)
    if key == "at":
        return state.location == val
    if key == "has_flag":
        return bool(state.flags.get(val))
    if key == "not_flag":
        return not bool(state.flags.get(val))
    if key == "has_item":
        return val in state.inventory
    if key == "sheet":
        axis, need = val
        return state.sheet.get(axis) == need
    if key == "rep_gte":
        faction, n = val
        return int(state.rep.get(faction, 0)) >= int(n)
    if key == "rep_lt":
        faction, n = val
        return int(state.rep.get(faction, 0)) < int(n)
    if key == "remembers":
        actor, fact = val
        return fact in state.memory.get(actor, [])
    if key == "has_outcome":
        return val in state.outcomes
    if key == "hp_gte":
        return state.hp >= int(val)
    if key == "tide":
        return tide(state) == val
    if key == "weather":
        return weather(state) == val
    if key == "in_region":
        if content is None:
            raise UnknownCondition("in_region requires content")
        loc = content.locations.get(state.location, {})
        return loc.get("region") == val
    raise UnknownCondition(f"unhandled condition {key}")
