#!/usr/bin/env python3
"""Record I4 witness traces against the shipped engine."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from adventure_forge.kernel.content import load_pack  # noqa: E402
from adventure_forge.kernel.replay import replay  # noqa: E402


TRACES = [
    {
        "id": "marsh_harbor_compact",
        "seed": 1,
        "sheet": "marsh_scout",
        "outcome": "harbor_compact",
        "actions": [
            "go:saltfen.market",
            "use_marsh_cant",
            "ask_about_tablet",
            "slip_inside",
            "take:compact_tablet",
            "go:saltfen.market",
            "go:saltfen.dock",
            "give_tablet",
            "sign_the_compact",
        ],
    },
    {
        "id": "marsh_stack_relic",
        "seed": 1,
        "sheet": "marsh_scout",
        "outcome": "stack_relic",
        "actions": [
            "take:frayed_rope",
            "go:saltfen.market",
            "go:ashfen.causeway",
            "go:stacks.base",
            "climb_switchback",
            "climb_to_mid",
            "climb_to_bridge",
            "crawl_across",
            "take:ash_relic",
        ],
    },
    {
        "id": "divergence_marsh_market",
        "seed": 1,
        "sheet": "marsh_scout",
        "actions": ["go:saltfen.market"],
    },
    {
        "id": "divergence_city_market",
        "seed": 1,
        "sheet": "city_oath",
        "actions": ["go:saltfen.market"],
    },
    {
        "id": "marsh_kiln_pact",
        "seed": 1,
        "sheet": "marsh_scout",
        "outcome": "kiln_pact",
        "actions": [
            "go:saltfen.market",
            "go:ashfen.causeway",
            "go:mill.lane",
            "go:mill.yard",
            "offer_reed_grain",
            "go:mill.kiln",
            "kindle_kiln",
            "stoke_kiln",
            "fire_the_pact",
        ],
    },
    {
        "id": "divergence_marsh_mill",
        "seed": 1,
        "sheet": "marsh_scout",
        "actions": [
            "go:saltfen.market",
            "go:ashfen.causeway",
            "go:mill.lane",
            "go:mill.yard",
        ],
    },
    {
        "id": "divergence_city_mill",
        "seed": 1,
        "sheet": "city_oath",
        "actions": [
            "go:saltfen.market",
            "go:ashfen.causeway",
            "go:mill.lane",
            "go:mill.yard",
        ],
    },
    {
        "id": "cross_plain_mill",
        "seed": 1,
        "sheet": "marsh_scout",
        "actions": [
            "go:saltfen.market",
            "go:ashfen.causeway",
            "go:mill.lane",
            "go:mill.yard",
        ],
    },
    {
        "id": "cross_compact_mill",
        "seed": 1,
        "sheet": "marsh_scout",
        "actions": [
            "go:saltfen.market",
            "use_marsh_cant",
            "ask_about_tablet",
            "slip_inside",
            "take:compact_tablet",
            "go:saltfen.market",
            "go:saltfen.dock",
            "give_tablet",
            "sign_the_compact",
            "go:saltfen.market",
            "go:ashfen.causeway",
            "go:mill.lane",
            "go:mill.yard",
        ],
    },
    {
        "id": "marsh_reed_sentence",
        "seed": 1,
        "sheet": "marsh_scout",
        "outcome": "reed_sentence",
        "actions": [
            "go:saltfen.market",
            "go:ashfen.causeway",
            "go:court.gate",
            "go:court.yard",
            "go:court.hall",
            "speak_reed_custom",
            "go:court.yard",
            "go:court.cell",
            "hear_tam_witness",
            "go:court.yard",
            "go:court.hall",
            "pass_reed_sentence",
        ],
    },
    {
        "id": "divergence_marsh_court",
        "seed": 1,
        "sheet": "marsh_scout",
        "actions": [
            "go:saltfen.market",
            "go:ashfen.causeway",
            "go:court.gate",
            "go:court.yard",
            "go:court.hall",
        ],
    },
    {
        "id": "divergence_city_court",
        "seed": 1,
        "sheet": "city_oath",
        "actions": [
            "go:saltfen.market",
            "go:ashfen.causeway",
            "go:court.gate",
            "go:court.yard",
            "go:court.hall",
        ],
    },
    {
        "id": "cross_plain_court",
        "seed": 1,
        "sheet": "marsh_scout",
        "actions": [
            "go:saltfen.market",
            "go:ashfen.causeway",
            "go:court.gate",
            "go:court.yard",
            "go:court.hall",
        ],
    },
    {
        "id": "cross_kiln_court",
        "seed": 1,
        "sheet": "marsh_scout",
        "actions": [
            "go:saltfen.market",
            "go:ashfen.causeway",
            "go:mill.lane",
            "go:mill.yard",
            "offer_reed_grain",
            "go:mill.kiln",
            "kindle_kiln",
            "stoke_kiln",
            "fire_the_pact",
            "go:mill.yard",
            "go:mill.lane",
            "go:court.gate",
            "go:court.yard",
            "go:court.hall",
        ],
    },
    {
        "id": "marsh_road_beacon",
        "seed": 1,
        "sheet": "marsh_scout",
        "outcome": "road_beacon",
        "actions": [
            "go:saltfen.market",
            "go:ashfen.causeway",
            "go:road.ford",
            "go:road.dike",
            "go:road.hut",
            "track_drowned_prints",
            "go:road.beacon",
            "light_the_beacon",
        ],
    },
    {
        "id": "divergence_marsh_road",
        "seed": 1,
        "sheet": "marsh_scout",
        "actions": [
            "go:saltfen.market",
            "go:ashfen.causeway",
            "go:road.ford",
            "go:road.dike",
            "go:road.hut",
        ],
    },
    {
        "id": "divergence_city_road",
        "seed": 1,
        "sheet": "city_oath",
        "actions": [
            "go:saltfen.market",
            "go:ashfen.causeway",
            "go:road.ford",
            "go:road.dike",
            "go:road.hut",
        ],
    },
    {
        "id": "cross_plain_road",
        "seed": 1,
        "sheet": "marsh_scout",
        "actions": [
            "go:saltfen.market",
            "go:ashfen.causeway",
            "go:road.ford",
            "go:road.dike",
            "go:road.hut",
        ],
    },
    {
        "id": "cross_court_road",
        "seed": 1,
        "sheet": "marsh_scout",
        "actions": [
            "go:saltfen.market",
            "go:ashfen.causeway",
            "go:court.gate",
            "go:court.yard",
            "go:court.hall",
            "speak_reed_custom",
            "go:court.yard",
            "go:court.cell",
            "hear_tam_witness",
            "go:court.yard",
            "go:court.hall",
            "pass_reed_sentence",
            "go:court.yard",
            "go:court.gate",
            "go:ashfen.causeway",
            "go:road.ford",
            "go:road.dike",
            "go:road.hut",
        ],
    },
    {
        "id": "marsh_fever_broken",
        "seed": 1,
        "sheet": "marsh_scout",
        "outcome": "fever_broken",
        "actions": [
            "go:saltfen.market",
            "go:ashfen.causeway",
            "go:camp.gate",
            "go:camp.yard",
            "cut_reed_herb",
            "go:camp.still",
            "brew_fever_broth",
            "go:camp.yard",
            "go:camp.ward",
            "give_broth_to_ren",
        ],
    },
    {
        "id": "divergence_marsh_camp",
        "seed": 1,
        "sheet": "marsh_scout",
        "actions": [
            "go:saltfen.market",
            "go:ashfen.causeway",
            "go:camp.gate",
            "go:camp.yard",
        ],
    },
    {
        "id": "divergence_city_camp",
        "seed": 1,
        "sheet": "city_oath",
        "actions": [
            "go:saltfen.market",
            "go:ashfen.causeway",
            "go:camp.gate",
            "go:camp.yard",
        ],
    },
    {
        "id": "cross_plain_camp",
        "seed": 1,
        "sheet": "marsh_scout",
        "actions": [
            "go:saltfen.market",
            "go:ashfen.causeway",
            "go:camp.gate",
        ],
    },
    {
        "id": "cross_beacon_camp",
        "seed": 1,
        "sheet": "marsh_scout",
        "actions": [
            "go:saltfen.market",
            "go:ashfen.causeway",
            "go:road.ford",
            "go:road.dike",
            "go:road.hut",
            "track_drowned_prints",
            "go:road.beacon",
            "light_the_beacon",
            "go:road.hut",
            "go:road.dike",
            "go:road.ford",
            "go:camp.gate",
        ],
    },
]


def main() -> int:
    content = load_pack()
    out_dir = ROOT / "traces"
    out_dir.mkdir(parents=True, exist_ok=True)
    for spec in TRACES:
        result = replay(content, spec["seed"], spec["sheet"], spec["actions"])
        payload = {
            "id": spec["id"],
            "build_id": content.build_id,
            "seed": spec["seed"],
            "sheet": spec["sheet"],
            "actions": spec["actions"],
            "final_fingerprint": result.fingerprint,
            "location": result.state.location,
            "outcomes": list(result.state.outcomes),
        }
        if spec.get("outcome"):
            payload["outcome"] = spec["outcome"]
            if spec["outcome"] not in result.state.outcomes:
                raise SystemExit(f"{spec['id']} failed to reach {spec['outcome']}: {result.state.outcomes}")
        path = out_dir / f"{spec['id']}.json"
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"wrote {path} fp={result.fingerprint[:12]} loc={result.state.location} outcomes={result.state.outcomes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
