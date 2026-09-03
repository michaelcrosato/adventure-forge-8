from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from adventure_forge import ENGINE_VERSION
from adventure_forge.kernel.canon import canonical_dumps, sha256_hex
from adventure_forge.kernel.conditions import matches
from adventure_forge.kernel.ops import COND_KEYS, EFFECT_OPS
from adventure_forge.paths import pack_path

AXES: dict[str, tuple[str, ...]] = {
    "origin": ("marshborn", "cityward", "exiled"),
    "body": ("might", "agile", "hardy"),
    "skill": ("craft", "hunt", "letters"),
    "creed": ("oathbound", "freehand", "quiet"),
    "mark": ("scarred", "clean", "branded"),
    "tongue": ("cant", "court", "plain"),
}


class ContentError(ValueError):
    pass


@dataclass(frozen=True)
class Content:
    raw: dict[str, Any]
    build_id: str

    @property
    def pack_id(self) -> str:
        return str(self.raw["id"])

    @property
    def regions(self) -> dict[str, Any]:
        return self.raw["regions"]

    @property
    def locations(self) -> dict[str, Any]:
        return self.raw["locations"]

    @property
    def actors(self) -> dict[str, Any]:
        return self.raw["actors"]

    @property
    def items(self) -> dict[str, Any]:
        return self.raw["items"]

    @property
    def actions(self) -> list[dict[str, Any]]:
        return self.raw["actions"]

    @property
    def outcomes(self) -> dict[str, Any]:
        return self.raw["outcomes"]

    @property
    def start(self) -> dict[str, Any]:
        return self.raw["start"]

    @property
    def sheets(self) -> dict[str, dict[str, str]]:
        return self.raw["sheets"]

    def location_region(self, loc_id: str) -> str:
        return str(self.locations[loc_id]["region"])

    def outcome_ready(self, outcome_id: str, state: Any) -> bool:
        spec = self.outcomes[outcome_id]
        return matches(spec["when"], state, self)


def compute_build_id(raw: dict[str, Any]) -> str:
    payload = {"engine": ENGINE_VERSION, "pack": raw}
    return sha256_hex(canonical_dumps(payload))


def _walk_conditions(node: Any, found: list[str]) -> None:
    if isinstance(node, dict):
        if node and set(node.keys()) <= COND_KEYS and len(node) == 1:
            found.extend(node.keys())
            val = next(iter(node.values()))
            if isinstance(val, list):
                for child in val:
                    _walk_conditions(child, found)
            elif isinstance(val, dict):
                _walk_conditions(val, found)
            return
        for v in node.values():
            _walk_conditions(v, found)
    elif isinstance(node, list):
        for child in node:
            _walk_conditions(child, found)


def _walk_effects(node: Any, found: list[str]) -> None:
    if isinstance(node, dict) and "op" in node:
        found.append(str(node["op"]))
        for key in ("on_pass", "on_fail", "mods"):
            if key in node:
                _walk_effects(node[key], found)
        return
    if isinstance(node, dict):
        for v in node.values():
            _walk_effects(v, found)
    elif isinstance(node, list):
        for child in node:
            _walk_effects(child, found)


def validate_pack(raw: dict[str, Any]) -> None:
    required = (
        "id",
        "regions",
        "locations",
        "actors",
        "items",
        "actions",
        "outcomes",
        "start",
        "sheets",
    )
    for key in required:
        if key not in raw:
            raise ContentError(f"pack missing {key}")
    locs = raw["locations"]
    items = raw["items"]
    actors = raw["actors"]
    regions = raw["regions"]
    if not locs:
        raise ContentError("no locations")
    start_loc = raw["start"]["location"]
    if start_loc not in locs:
        raise ContentError(f"start location missing: {start_loc}")
    for loc_id, loc in locs.items():
        region = loc.get("region")
        if region not in regions:
            raise ContentError(f"{loc_id} region {region} missing")
        for exit_spec in loc.get("exits", []):
            dest = exit_spec["to"]
            if dest not in locs:
                raise ContentError(f"{loc_id} exit to missing {dest}")
        for item_id in loc.get("ground", []):
            if item_id not in items:
                raise ContentError(f"{loc_id} ground item missing {item_id}")
        for actor_id in loc.get("actors", []):
            if actor_id not in actors:
                raise ContentError(f"{loc_id} actor missing {actor_id}")
    for action in raw["actions"]:
        if "id" not in action or "label" not in action:
            raise ContentError(f"action missing id/label: {action!r}")
        cond_ops: list[str] = []
        _walk_conditions(action.get("when"), cond_ops)
        for op in cond_ops:
            if op not in COND_KEYS:
                raise ContentError(f"action {action['id']} unknown cond {op}")
        eff_ops: list[str] = []
        _walk_effects(action.get("effects", []), eff_ops)
        for op in eff_ops:
            if op not in EFFECT_OPS:
                raise ContentError(f"action {action['id']} unknown effect {op}")
    for oid, spec in raw["outcomes"].items():
        if "when" not in spec:
            raise ContentError(f"outcome {oid} missing when")
    for name, sheet in raw["sheets"].items():
        validate_sheet(sheet, label=name)


def validate_sheet(sheet: dict[str, str], label: str = "sheet") -> None:
    missing = [axis for axis in AXES if axis not in sheet]
    if missing:
        raise ContentError(f"{label} missing axes {missing}")
    for axis, value in sheet.items():
        if axis not in AXES:
            raise ContentError(f"{label} unknown axis {axis}")
        if value not in AXES[axis]:
            raise ContentError(f"{label} bad {axis}={value}")


def load_pack(path: Path | None = None) -> Content:
    target = path or pack_path()
    raw = json.loads(target.read_text(encoding="utf-8"))
    validate_pack(raw)
    return Content(raw=raw, build_id=compute_build_id(raw))
