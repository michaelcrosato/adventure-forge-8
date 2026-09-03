from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from adventure_forge.kernel.content import Content
from adventure_forge.kernel.replay import replay
from adventure_forge.paths import repo_root


def replay_fingerprint(content: Content, trace: dict) -> str:
    result = replay(content, trace["seed"], trace["sheet"], trace["actions"])
    return result.fingerprint


def check_i1(content: Content, traces: list[dict]) -> dict:
    fps = {}
    for trace in traces:
        a = replay_fingerprint(content, trace)
        b = replay_fingerprint(content, trace)
        if a != b:
            raise AssertionError(f"I1 in-process mismatch {trace.get('id')}")
        fps[trace["id"]] = a

    root = repo_root()
    for trace in traces:
        trace_path = root / "traces" / f"{trace['id']}.json"
        cmd = [
            sys.executable,
            "-c",
            (
                "import json,sys;"
                "sys.path.insert(0, sys.argv[1]);"
                "from adventure_forge.kernel.content import load_pack;"
                "from adventure_forge.kernel.replay import replay;"
                "c=load_pack();"
                "t=json.loads(open(sys.argv[2],encoding='utf-8').read());"
                "r=replay(c,t['seed'],t['sheet'],t['actions']);"
                "print(r.fingerprint)"
            ),
            str(root / "src"),
            str(trace_path),
        ]
        one = subprocess.check_output(cmd, cwd=root, text=True).strip().splitlines()[-1]
        two = subprocess.check_output(cmd, cwd=root, text=True).strip().splitlines()[-1]
        if one != two or one != fps[trace["id"]]:
            raise AssertionError(f"I1 subprocess mismatch {trace['id']}: {one} {two} {fps[trace['id']]}")
    return fps
