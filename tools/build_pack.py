#!/usr/bin/env python3
"""Compile Ashfen Coast pack.json from authored data plus the salvage catalog."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "ashfen" / "pack.json"

ADJS = [
    "bent",
    "rusted",
    "salt",
    "tarred",
    "cracked",
    "braided",
    "pitted",
    "pale",
    "hooked",
    "knotted",
]
NOUNS = [
    "hook",
    "spike",
    "buckle",
    "shackle",
    "needle",
    "clasp",
    "ring",
    "wedge",
    "plate",
    "peg",
]


def salvage_catalog() -> tuple[dict[str, dict], list[str]]:
    items: dict[str, dict] = {}
    order: list[str] = []
    n = 0
    for adj in ADJS:
        for noun in NOUNS:
            item_id = f"salvage_{n:03d}"
            items[item_id] = {"name": f"{adj} {noun}", "kind": "salvage"}
            order.append(item_id)
            n += 1
    return items, order


def action(
    aid: str,
    label: str,
    group: str,
    when: dict,
    text: str,
    effects: list | None = None,
) -> dict:
    spec = {
        "id": aid,
        "label": label,
        "group": group,
        "when": when,
        "text": text,
        "effects": effects or [],
    }
    return spec


def build() -> dict:
    salvage_items, salvage_ids = salvage_catalog()
    authored = json.loads(
        (Path(__file__).with_name("ashfen_authored.json")).read_text(encoding="utf-8")
    )
    items = {k: v for k, v in authored["items"].items() if not str(k).startswith("salvage_")}
    items.update(salvage_items)
    authored["items"] = items
    authored["locations"]["saltfen.salvage"]["ground"] = list(salvage_ids)
    return authored


def main() -> int:
    pack = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(pack, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUT} locations={len(pack['locations'])} actions={len(pack['actions'])} items={len(pack['items'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
