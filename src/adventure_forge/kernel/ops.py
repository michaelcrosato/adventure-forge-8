"""Closed condition/effect vocabulary. New verbs must be added here with a checker."""

from __future__ import annotations

COND_KEYS = frozenset(
    {
        "all",
        "any",
        "not",
        "at",
        "has_flag",
        "not_flag",
        "has_item",
        "sheet",
        "rep_gte",
        "rep_lt",
        "remembers",
        "has_outcome",
        "hp_gte",
        "tide",
        "weather",
        "in_region",
    }
)

EFFECT_OPS = frozenset(
    {
        "set_flag",
        "clear_flag",
        "move",
        "add_item",
        "remove_item",
        "take_here",
        "drop_here",
        "add_rep",
        "remember",
        "hurt",
        "heal",
        "text",
        "check",
        "outcome",
        "open_exit",
    }
)
