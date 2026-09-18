from __future__ import annotations

import json
import os
import subprocess
import sys

from adventure_forge.kernel.content import Content
from adventure_forge.kernel.replay import replay
from adventure_forge.paths import repo_root

# Replay every trace in one child and print the whole fingerprint map. The old
# shape spawned two children per trace — 288 interpreter starts, each re-parsing
# a 1.2 MB pack — which is where the bar's ten minutes went.
_CHILD = (
    "import json,sys;"
    "sys.path.insert(0, sys.argv[1]);"
    "from adventure_forge.kernel.content import load_pack;"
    "from adventure_forge.kernel.replay import replay;"
    "c=load_pack();"
    "out={};"
    "ts=json.loads(open(sys.argv[2],encoding='utf-8').read());"
    "\nfor t in ts:\n"
    "    r=replay(c,t['seed'],t['sheet'],t['actions']);"
    "    out[t['id']]=r.fingerprint\n"
    "print(json.dumps(out,sort_keys=True))"
)


def replay_fingerprint(content: Content, trace: dict) -> str:
    result = replay(content, trace["seed"], trace["sheet"], trace["actions"])
    return result.fingerprint


def _child_fingerprints(payload_path, hash_seed: str) -> dict[str, str]:
    """Fingerprints computed in a fresh interpreter under a given hash seed.

    Varying PYTHONHASHSEED is the point: it is how a set or dict iteration order
    leaking into the transition would show up. The previous per-trace shape
    inherited this process's seed in both children, so it could never catch that.
    """
    root = repo_root()
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = hash_seed
    raw = subprocess.check_output(
        [sys.executable, "-c", _CHILD, str(root / "src"), str(payload_path)],
        cwd=root,
        text=True,
        env=env,
    )
    return json.loads(raw.strip().splitlines()[-1])


def check_i1(content: Content, traces: list[dict]) -> dict:
    if not traces:
        return {}

    # 1. Same process, twice: no hidden state carried between replays.
    fps: dict[str, str] = {}
    for trace in traces:
        first = replay_fingerprint(content, trace)
        second = replay_fingerprint(content, trace)
        if first != second:
            raise AssertionError(f"I1 in-process mismatch {trace.get('id')}")
        fps[trace["id"]] = first

    # 2. Fresh interpreters, two different hash seeds: no ambient ordering.
    import tempfile
    from pathlib import Path

    payload = [
        {"id": t["id"], "seed": t["seed"], "sheet": t["sheet"], "actions": t["actions"]}
        for t in traces
    ]
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "traces.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        for hash_seed in ("0", "12345"):
            child = _child_fingerprints(path, hash_seed)
            if child != fps:
                drift = sorted(
                    tid for tid in fps if child.get(tid) != fps[tid]
                )
                raise AssertionError(
                    f"I1 subprocess mismatch under PYTHONHASHSEED={hash_seed}: {drift[:5]}"
                )
    return fps
