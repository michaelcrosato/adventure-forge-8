from __future__ import annotations

import re
from typing import Any, Iterable

from adventure_forge.kernel.content import Content
from adventure_forge.kernel.replay import new_game, replay
from adventure_forge.play.observe import observe

MAX_SENTENCE_WORDS = 20
MAX_LABEL_WORDS = 8
MAX_OBS_PROSE_WORDS = 120

BANNED = (
    "ancient malice",
    "tapestry",
    "myriad",
    "eldritch",
    "begins to unfold",
    "aura of",
    "whispered secrets",
)


def sentences(text: str) -> list[str]:
    parts = re.split(r"[.!?]+", text)
    return [p.strip() for p in parts if p.strip()]


def word_count(text: str) -> int:
    return len(text.split())


def check_text(text: str, where: str, label: bool = False) -> list[str]:
    errors: list[str] = []
    lower = text.lower()
    for banned in BANNED:
        if banned in lower:
            errors.append(f"{where}: banned phrase {banned!r}")
    if label:
        n = word_count(text)
        if n > MAX_LABEL_WORDS:
            errors.append(f"{where}: label has {n} words (max {MAX_LABEL_WORDS}): {text!r}")
        return errors
    for sent in sentences(text):
        n = word_count(sent)
        if n > MAX_SENTENCE_WORDS:
            errors.append(f"{where}: sentence has {n} words (max {MAX_SENTENCE_WORDS}): {sent!r}")
    return errors


def _walk_strings(node: Any, prefix: str) -> Iterable[tuple[str, str]]:
    if isinstance(node, str):
        yield prefix, node
    elif isinstance(node, dict):
        for k, v in node.items():
            yield from _walk_strings(v, f"{prefix}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from _walk_strings(v, f"{prefix}[{i}]")


def check_pack_language(content: Content) -> list[str]:
    errors: list[str] = []
    for action in content.actions:
        errors.extend(check_text(str(action["label"]), f"action {action['id']} label", label=True))
        if action.get("text"):
            errors.extend(check_text(str(action["text"]), f"action {action['id']} text"))
    for loc_id, loc in content.locations.items():
        errors.extend(check_text(str(loc["situation"]), f"{loc_id} situation"))
        for extra in loc.get("situation_if", []):
            errors.extend(check_text(str(extra["text"]), f"{loc_id} situation_if"))
        for exit_spec in loc.get("exits", []):
            errors.extend(check_text(str(exit_spec["label"]), f"{loc_id} exit", label=True))
    for actor_id, actor in content.actors.items():
        errors.extend(check_text(str(actor["name"]), f"actor {actor_id} name", label=True))
        errors.extend(check_text(str(actor.get("idle", "")), f"actor {actor_id} idle"))
    for item_id, item in content.items.items():
        errors.extend(check_text(f"Take {item['name']}", f"item {item_id}", label=True))
    return errors


def check_walkthrough_budget(content: Content, traces: list[dict]) -> list[str]:
    errors: list[str] = []
    for trace in traces:
        state, cursor = new_game(content, trace["seed"], trace["sheet"])
        obs = observe(state, content)
        if obs.prose_word_count > MAX_OBS_PROSE_WORDS:
            errors.append(f"{trace.get('id', 'trace')} start obs {obs.prose_word_count} words")
        result = replay(content, trace["seed"], trace["sheet"], trace["actions"])
        # Re-step to observe each turn
        state, cursor = new_game(content, trace["seed"], trace["sheet"])
        from adventure_forge.kernel.step import step

        for action_id in trace["actions"]:
            stepped = step(state, action_id, content, cursor)
            state, cursor = stepped.state, stepped.cursor
            obs = observe(state, content)
            if obs.prose_word_count > MAX_OBS_PROSE_WORDS:
                errors.append(
                    f"{trace.get('id', 'trace')} after {action_id} obs {obs.prose_word_count} words"
                )
        _ = result
    return errors
