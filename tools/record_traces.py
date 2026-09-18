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


def recipes() -> list[dict]:
    path = Path(__file__).with_name("trace_recipes.json")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    content = load_pack()
    out_dir = ROOT / "traces"
    out_dir.mkdir(parents=True, exist_ok=True)
    wanted = set()
    for spec in recipes():
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
                raise SystemExit(
                    f"{spec['id']} failed to reach {spec['outcome']}: {result.state.outcomes}"
                )
        path = out_dir / f"{spec['id']}.json"
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        wanted.add(path.name)
        print(
            f"wrote {path} fp={result.fingerprint[:12]} loc={result.state.location} "
            f"outcomes={result.state.outcomes}"
        )
    for stale in out_dir.glob("*.json"):
        if stale.name.startswith("_"):
            continue
        if stale.name not in wanted:
            stale.unlink()
            print(f"removed stale {stale}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
