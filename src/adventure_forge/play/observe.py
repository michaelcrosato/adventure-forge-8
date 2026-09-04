from __future__ import annotations

from dataclasses import dataclass

from adventure_forge.kernel.conditions import matches
from adventure_forge.kernel.content import Content
from adventure_forge.kernel.legal import LegalAction, enumerate_legal
from adventure_forge.kernel.state import GameState, tide, weather

# UI only. Never used to drop ids from the engine legal set.
PAGE_SIZE = 12


@dataclass(frozen=True)
class Observation:
    title: str
    situation: str
    last_text: str
    actions: list[LegalAction]
    visible: list[LegalAction]
    page: int
    group: str | None
    total: int
    text: str
    prose: str

    @property
    def prose_word_count(self) -> int:
        return len(self.prose.split())


def situation_text(state: GameState, content: Content) -> str:
    loc = content.locations[state.location]
    parts = [str(loc["situation"])]
    for extra in loc.get("situation_if", []):
        if matches(extra["when"], state, content):
            parts.append(str(extra["text"]))
    if loc.get("show_tide"):
        parts.append(f"The tide is {tide(state)}.")
    if loc.get("show_weather"):
        parts.append(f"The weather is {weather(state)}.")
    return " ".join(parts)


def _visible_slice(
    actions: list[LegalAction],
    page: int,
    group: str | None,
) -> tuple[list[LegalAction], int, int]:
    filtered = [a for a in actions if group is None or a.group == group]
    if page < 0:
        page = 0
    start = page * PAGE_SIZE
    if start >= len(filtered) and filtered:
        page = (len(filtered) - 1) // PAGE_SIZE
        start = page * PAGE_SIZE
    visible = filtered[start : start + PAGE_SIZE]
    return visible, page, len(filtered)


def observe(
    state: GameState,
    content: Content,
    page: int = 0,
    group: str | None = None,
) -> Observation:
    loc = content.locations[state.location]
    title = str(loc["name"])
    situation = situation_text(state, content)
    last_text = state.last_text
    actions = enumerate_legal(state, content)
    visible, page, filtered_total = _visible_slice(actions, page, group)
    lines = [title, "", situation]
    if last_text:
        lines.extend(["", last_text])
    lines.extend(["", "You can:"])
    for i, action in enumerate(visible, start=1):
        lines.append(f"  {i}  [{action.group}] {action.label}")
    hidden = filtered_total - len(visible)
    group_note = group or "all"
    lines.append("")
    lines.append(
        f"(showing {len(visible)} of {filtered_total}, group {group_note}; {len(actions)} legal)"
    )
    if hidden > 0:
        lines.append("more | all | filter <group>")
    if state.outcomes:
        lines.append("Outcomes: " + ", ".join(state.outcomes))
    prose_parts = [situation]
    if last_text:
        prose_parts.append(last_text)
    prose = " ".join(prose_parts)
    return Observation(
        title=title,
        situation=situation,
        last_text=last_text,
        actions=actions,
        visible=visible,
        page=page,
        group=group,
        total=len(actions),
        text="\n".join(lines),
        prose=prose,
    )


def format_observation(obs: Observation) -> str:
    return obs.text
