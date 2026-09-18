"""The sameness crawler.

PLAN.md promised this twice and the factory never built it:

    "Crawler hunts *sameness* and rejects reskins."
    "Scale rule: stop counting a cell when a sameness crawler cannot tell it
     from another cell by verbs + inhabitants + effects."

Without it, `verify` could only ask "does this replay?" — never "is this a
different place?" — so 119 structurally identical regions shipped green. Every
metric here is mechanical and LLM-free, like the rest of the bar.

The bar is a ratchet, not a grade. `sameness-baseline.json` records what the
pack measures today; this check fails when a number moves the wrong way. That
makes the current debt visible and makes adding more of it impossible.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from typing import Any

from adventure_forge.kernel.content import Content
from adventure_forge.kernel.ops import COND_KEYS, EFFECT_OPS
from adventure_forge.paths import repo_root

# Structural, not cosmetic. Renaming "stave" to "spirket" must not buy a region
# a new fingerprint.
CONTROL_KEYS = frozenset({"all", "any", "not"})


class SamenessFail(AssertionError):
    pass


def baseline_path():
    return repo_root() / "sameness-baseline.json"


def _walk_conditions(node: Any, out: list[tuple[str, Any]]) -> None:
    if not isinstance(node, dict):
        return
    for key, value in node.items():
        if key in CONTROL_KEYS:
            children = value if isinstance(value, list) else [value]
            for child in children:
                _walk_conditions(child, out)
        else:
            out.append((key, value))


def condition_kinds(when: Any) -> list[str]:
    found: list[tuple[str, Any]] = []
    _walk_conditions(when or {}, found)
    return [k for k, _ in found]


def action_locations(action: dict) -> list[str]:
    found: list[tuple[str, Any]] = []
    _walk_conditions(action.get("when") or {}, found)
    return [str(v) for k, v in found if k == "at"]


def _actions_by_region(content: Content) -> dict[str, list[dict]]:
    region_of = {lid: loc.get("region") for lid, loc in content.locations.items()}
    grouped: dict[str, list[dict]] = defaultdict(list)
    for action in content.actions:
        regions = {region_of.get(loc) for loc in action_locations(action)}
        for region in regions:
            if region:
                grouped[region].append(action)
    return grouped


def region_fingerprint(content: Content, region_id: str, grouped: dict[str, list[dict]]) -> tuple:
    """Verbs + inhabitants + effects, with every proper noun stripped.

    Two regions share a fingerprint when a player could not tell them apart by
    what they can do, who is there, and what changes — only by what things are
    called. That is precisely what G4 says does not count.
    """
    locations = [lid for lid, loc in content.locations.items() if loc.get("region") == region_id]
    actors = {a for lid in locations for a in content.locations[lid].get("actors", [])}
    shape = []
    for action in sorted(grouped.get(region_id, []), key=lambda a: a["id"]):
        effects = tuple(sorted(str(e.get("op")) for e in action.get("effects", [])))
        conditions = tuple(sorted(set(condition_kinds(action.get("when")))))
        shape.append((effects, conditions, str(action.get("group", "do"))))
    exits = tuple(sorted(len(content.locations[lid].get("exits", [])) for lid in locations))
    return (len(locations), len(actors), exits, tuple(sorted(shape)))


def clone_classes(content: Content) -> dict[str, list[str]]:
    """Regions grouped by structural fingerprint. A class of one is a real place."""
    grouped = _actions_by_region(content)
    classes: dict[str, list[str]] = defaultdict(list)
    for region_id in content.regions:
        key = json.dumps(region_fingerprint(content, region_id, grouped), sort_keys=True)
        classes[key].append(region_id)
    return {k: sorted(v) for k, v in classes.items()}


def wallpaper_locations(content: Content) -> list[str]:
    """Locations that offer no verb of their own. Empty miles."""
    with_actions = {loc for action in content.actions for loc in action_locations(action)}
    return sorted(lid for lid in content.locations if lid not in with_actions)


def hub_dominance(content: Content) -> tuple[str, float]:
    """The worst single point of failure in the world graph.

    G1 wants one contiguous world. A world where removing one node strands
    everything else is not contiguous — it is a hub with pocket universes
    hanging off it.
    """
    graph: dict[str, set[str]] = defaultdict(set)
    for lid, loc in content.locations.items():
        graph[lid]  # ensure isolated nodes exist
        for spec in loc.get("exits", []):
            other = str(spec["to"])
            graph[lid].add(other)
            graph[other].add(lid)

    start = str(content.start["location"])
    total = len(content.locations)

    def reachable(without: str | None) -> int:
        if start == without:
            return 0
        seen = {start}
        queue = [start]
        while queue:
            node = queue.pop()
            for nxt in graph.get(node, ()):
                if nxt != without and nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
        return len(seen)

    worst_node, worst_cut = "", 0.0
    # Every node, not the high-degree ones. A cut point need not have high
    # degree: `saltfen.market` has degree 7 and strands 99.7% of the world,
    # while the causeway it guards has degree 144. Sampling by degree misses
    # exactly the bridges that matter, and the full scan costs ~0.1s.
    # The start is skipped: "remove where the player begins" is not a claim
    # about the world's shape.
    for node in sorted(graph):
        if node == start:
            continue
        cut = (total - 1 - reachable(node)) / max(1, total - 1)
        if cut > worst_cut:
            worst_node, worst_cut = node, cut
    return worst_node, round(worst_cut, 4)


def vocabulary_usage(content: Content) -> tuple[list[str], list[str]]:
    """Ops and conditions the engine implements but the world never uses.

    Dead vocabulary is the tell for a world with one mechanic: `hurt` unused
    means nothing can go wrong, `remembers` unused means NPC memory is
    write-only.
    """
    used_ops: Counter = Counter()
    used_conds: Counter = Counter()
    for action in content.actions:
        for effect in action.get("effects", []):
            used_ops[str(effect.get("op"))] += 1
        for kind in condition_kinds(action.get("when")):
            used_conds[kind] += 1
    for spec in content.outcomes.values():
        for kind in condition_kinds(spec.get("when")):
            used_conds[kind] += 1
    for loc in content.locations.values():
        for extra in loc.get("situation_if", []):
            for kind in condition_kinds(extra.get("when")):
                used_conds[kind] += 1
    dead_ops = sorted(op for op in EFFECT_OPS if not used_ops[op])
    dead_conds = sorted(c for c in COND_KEYS if c not in CONTROL_KEYS and not used_conds[c])
    return dead_ops, dead_conds


def outcome_flags(content: Content) -> set[str]:
    """The flags an outcome actually depends on.

    An outcome id is not always the flag that satisfies it: `harbor_compact` is
    satisfied by `compact_restored`. Reading the predicate rather than assuming
    the names line up is the difference between measuring G3 and guessing at it.
    """
    flags: set[str] = set()
    for spec in content.outcomes.values():
        pairs: list[tuple[str, Any]] = []
        _walk_conditions(spec.get("when") or {}, pairs)
        for kind, value in pairs:
            if kind in ("has_flag", "not_flag") and isinstance(value, str):
                flags.add(value)
    return flags


def sheet_gated_outcomes(content: Content) -> list[str]:
    """Actions where the character sheet decides whether an outcome is reachable.

    G3: "Two sheets through the same opening must produce a proven divergence."
    A divergence that only changes which verb is printed, while both verbs set
    the same flag, is cosmetic. This counts the load-bearing kind.
    """
    flags = outcome_flags(content)
    found = []
    for action in content.actions:
        kinds = set(condition_kinds(action.get("when")))
        if "sheet" not in kinds:
            continue
        for effect in action.get("effects", []):
            if effect.get("op") == "set_flag" and effect.get("flag") in flags:
                found.append(str(action["id"]))
                break
    return sorted(found)


def measure(content: Content) -> dict[str, Any]:
    """Every sameness number in one mechanical pass."""
    classes = clone_classes(content)
    sizes = sorted((len(v) for v in classes.values()), reverse=True)
    dead_ops, dead_conds = vocabulary_usage(content)
    hub_node, hub_cut = hub_dominance(content)
    return {
        "regions": len(content.regions),
        "distinct_region_fingerprints": len(classes),
        "largest_clone_class": sizes[0] if sizes else 0,
        "regions_in_clone_classes": sum(n for n in sizes if n > 1),
        "wallpaper_locations": len(wallpaper_locations(content)),
        "worst_hub": hub_node,
        "worst_hub_cut_fraction": hub_cut,
        "unused_effect_ops": dead_ops,
        "unused_condition_kinds": dead_conds,
        "sheet_gated_outcome_actions": len(sheet_gated_outcomes(content)),
    }


def load_baseline() -> dict[str, Any]:
    path = baseline_path()
    if not path.exists():
        raise SamenessFail(
            f"missing {path.name}: the sameness ratchet has no baseline to compare against"
        )
    return json.loads(path.read_text(encoding="utf-8"))


# metric -> ("up" means worse, or "down" means worse)
RATCHET: dict[str, str] = {
    "distinct_region_fingerprints": "down",
    "largest_clone_class": "up",
    "regions_in_clone_classes": "up",
    "wallpaper_locations": "up",
    "worst_hub_cut_fraction": "up",
    "sheet_gated_outcome_actions": "down",
}


def check_sameness(content: Content) -> dict[str, Any]:
    """Fail when the world got more same than it already is."""
    baseline = load_baseline()
    limits = baseline.get("limits", {})
    now = measure(content)
    errors: list[str] = []

    for metric, worse in RATCHET.items():
        if metric not in limits:
            errors.append(f"{metric}: no limit recorded in {baseline_path().name}")
            continue
        allowed = limits[metric]
        actual = now[metric]
        if worse == "up" and actual > allowed:
            errors.append(f"{metric} rose to {actual} (limit {allowed})")
        if worse == "down" and actual < allowed:
            errors.append(f"{metric} fell to {actual} (floor {allowed})")

    # Dead vocabulary is a list, so it ratchets by membership: an op that is
    # live today may not go dark tomorrow.
    for key in ("unused_effect_ops", "unused_condition_kinds"):
        allowed = set(limits.get(key, []))
        actual = set(now[key])
        newly_dead = sorted(actual - allowed)
        if newly_dead:
            errors.append(f"{key}: {newly_dead} became unused")

    if errors:
        classes = clone_classes(content)
        worst = max(classes.values(), key=len) if classes else []
        detail = ""
        if len(worst) > 1:
            detail = (
                f"\n  largest clone class ({len(worst)} regions): "
                + ", ".join(worst[:8])
                + (" ..." if len(worst) > 8 else "")
            )
        raise SamenessFail(
            "sameness ratchet\n  "
            + "\n  ".join(errors)
            + detail
            + f"\n  If this change genuinely makes the world less same, update "
            f"{baseline_path().name} in the same commit and say why."
        )
    return now
