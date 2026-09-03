from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from adventure_forge.kernel.conditions import matches
from adventure_forge.kernel.content import Content
from adventure_forge.kernel.state import GameState

# Presentation may page. The engine returns the full programmed set.


@dataclass(frozen=True)
class LegalAction:
    id: str
    label: str
    group: str
    effects: tuple[dict[str, Any], ...]
    source: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "group": self.group,
            "source": self.source,
        }


def _item_name(content: Content, item_id: str) -> str:
    return str(content.items[item_id]["name"])


def _actor_name(content: Content, actor_id: str) -> str:
    return str(content.actors[actor_id]["name"])


def enumerate_legal(state: GameState, content: Content) -> list[LegalAction]:
    """Return every programmed legal action. No cap. Stable order by id."""
    found: dict[str, LegalAction] = {}

    def add(action: LegalAction) -> None:
        if action.id in found:
            raise ValueError(f"duplicate legal id {action.id}")
        found[action.id] = action

    loc = content.locations[state.location]

    add(
        LegalAction(
            id="wait",
            label="Wait",
            group="time",
            effects=(
                {"op": "text", "text": "Time passes."},
            ),
            source="systemic",
        )
    )

    for exit_spec in loc.get("exits", []):
        if not matches(exit_spec.get("when"), state, content):
            continue
        dest = exit_spec["to"]
        add(
            LegalAction(
                id=f"go:{dest}",
                label=str(exit_spec["label"]),
                group="go",
                effects=(
                    {"op": "move", "to": dest},
                    {"op": "text", "text": f"You go to {content.locations[dest]['name']}."},
                ),
                source="systemic",
            )
        )

    for item_id in list(state.ground.get(state.location, [])):
        name = _item_name(content, item_id)
        add(
            LegalAction(
                id=f"take:{item_id}",
                label=f"Take {name}",
                group="take",
                effects=(
                    {"op": "take_here", "item": item_id},
                    {"op": "text", "text": f"You take the {name}."},
                ),
                source="systemic",
            )
        )

    seen_inv: set[str] = set()
    for item_id in state.inventory:
        if item_id in seen_inv:
            continue
        seen_inv.add(item_id)
        name = _item_name(content, item_id)
        add(
            LegalAction(
                id=f"drop:{item_id}",
                label=f"Drop {name}",
                group="drop",
                effects=(
                    {"op": "drop_here", "item": item_id},
                    {"op": "text", "text": f"You drop the {name}."},
                ),
                source="systemic",
            )
        )

    for actor_id, actor_loc in state.actors.items():
        if actor_loc != state.location:
            continue
        name = _actor_name(content, actor_id)
        add(
            LegalAction(
                id=f"talk:{actor_id}",
                label=f"Talk to {name}",
                group="talk",
                effects=(
                    {"op": "text", "text": str(content.actors[actor_id].get("idle", f"{name} waits."))},
                ),
                source="systemic",
            )
        )

    for spec in content.actions:
        if not matches(spec.get("when"), state, content):
            continue
        effects = list(spec.get("effects", []))
        if spec.get("text"):
            effects = [{"op": "text", "text": spec["text"]}, *effects]
        add(
            LegalAction(
                id=str(spec["id"]),
                label=str(spec["label"]),
                group=str(spec.get("group", "do")),
                effects=tuple(effects),
                source="authored",
            )
        )

    return sorted(found.values(), key=lambda a: (a.group, a.id))
