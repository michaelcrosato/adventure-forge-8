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
