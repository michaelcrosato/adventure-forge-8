from __future__ import annotations

from adventure_forge.kernel.legal import LegalAction

UI_COMMANDS = frozenset({"more", "all", "help", "look", "inv", "inventory", "quit", "exit"})


def _norm(text: str) -> str:
    return " ".join(text.strip().lower().split())


def map_text(text: str, legal: list[LegalAction]) -> str | None:
    """Map plain language onto a legal id. Ambiguous or failed mapping returns None."""
    raw = text.strip()
    if not raw:
        return None
    lowered = _norm(raw)

    by_id = {a.id: a for a in legal}
    if raw in by_id:
        return raw
    if lowered in by_id:
        return lowered

    by_label: dict[str, list[str]] = {}
    for action in legal:
        by_label.setdefault(_norm(action.label), []).append(action.id)
    if lowered in by_label and len(by_label[lowered]) == 1:
        return by_label[lowered][0]

    hits: list[str] = []
    for action in legal:
        label = _norm(action.label)
        aid = action.id.lower()
        if label.startswith(lowered) or aid.startswith(lowered):
            hits.append(action.id)
        elif lowered in label or lowered in aid:
            hits.append(action.id)
    unique = list(dict.fromkeys(hits))
    if len(unique) == 1:
        return unique[0]
    return None


def is_ui_command(text: str) -> bool:
    lowered = _norm(text)
    if lowered in UI_COMMANDS:
        return True
    if lowered.startswith("filter ") or lowered.startswith("page "):
        return True
    if lowered.isdigit():
        return True
    return False
