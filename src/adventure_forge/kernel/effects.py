from __future__ import annotations

from typing import Any

from adventure_forge.kernel.conditions import matches
from adventure_forge.kernel.ops import EFFECT_OPS
from adventure_forge.kernel.seed import SeedCursor
from adventure_forge.kernel.state import GameState


class UnknownEffect(ValueError):
    pass


def apply_effects(
    effects: list[dict[str, Any]] | tuple[dict[str, Any], ...],
    state: GameState,
    cursor: SeedCursor,
    content: Any,
) -> str:
    texts: list[str] = []
    for effect in effects:
        if not isinstance(effect, dict) or "op" not in effect:
            raise UnknownEffect(f"invalid effect: {effect!r}")
        op = effect["op"]
        if op not in EFFECT_OPS:
            raise UnknownEffect(f"unknown effect op: {op}")
        if op == "set_flag":
            state.flags[str(effect["flag"])] = True
        elif op == "clear_flag":
            state.flags[str(effect["flag"])] = False
        elif op == "move":
            dest = str(effect["to"])
            if dest not in content.locations:
                raise UnknownEffect(f"move to missing location {dest}")
            state.location = dest
        elif op == "add_item":
            item = str(effect["item"])
            if item not in content.items:
                raise UnknownEffect(f"add missing item {item}")
            state.inventory.append(item)
        elif op == "remove_item":
            item = str(effect["item"])
            if item in state.inventory:
                state.inventory.remove(item)
        elif op == "take_here":
            item = str(effect["item"])
            ground = state.ground.setdefault(state.location, [])
            if item in ground:
                ground.remove(item)
                state.inventory.append(item)
        elif op == "drop_here":
            item = str(effect["item"])
            if item in state.inventory:
                state.inventory.remove(item)
                state.ground.setdefault(state.location, []).append(item)
        elif op == "add_rep":
            faction = str(effect["faction"])
            state.rep[faction] = int(state.rep.get(faction, 0)) + int(effect["n"])
        elif op == "remember":
            actor = str(effect["actor"])
            fact = str(effect["fact"])
            bucket = state.memory.setdefault(actor, [])
            if fact not in bucket:
                bucket.append(fact)
        elif op == "hurt":
            state.hp = max(1, state.hp - int(effect["n"]))
        elif op == "heal":
            state.hp = min(12, state.hp + int(effect["n"]))
        elif op == "text":
            texts.append(str(effect["text"]))
        elif op == "open_exit":
            state.flags[str(effect["flag"])] = True
        elif op == "outcome":
            oid = str(effect["id"])
            if oid not in content.outcomes:
                raise UnknownEffect(f"unknown outcome {oid}")
            if oid not in state.outcomes:
                state.outcomes.append(oid)
        elif op == "check":
            roll = cursor.draw(100)
            bonus = 0
            for mod in effect.get("mods", []):
                if matches(mod.get("when"), state, content):
                    bonus += int(mod["bonus"])
            passed = roll + bonus >= int(effect["dc"])
            branch = effect.get("on_pass" if passed else "on_fail", [])
            nested = apply_effects(branch, state, cursor, content)
            if nested:
                texts.append(nested)
        else:
            raise UnknownEffect(f"unhandled effect {op}")
    return " ".join(t for t in texts if t)
