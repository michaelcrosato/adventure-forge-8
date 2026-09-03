from __future__ import annotations

import json
import sys
from pathlib import Path

from adventure_forge.kernel.content import load_pack
from adventure_forge.kernel.legal import enumerate_legal
from adventure_forge.kernel.replay import new_game
from adventure_forge.paths import repo_root, traces_dir
from adventure_forge.verify.crawler import crawl
from adventure_forge.verify.player_crawl import player_crawl
from adventure_forge.verify.firewall import check_firewall
from adventure_forge.verify.i1 import check_i1
from adventure_forge.verify.i4 import check_i4
from adventure_forge.verify.language import check_pack_language, check_walkthrough_budget
from adventure_forge.verify.tamper import check_tamper
from adventure_forge.verify.units import run_units


def load_traces() -> list[dict]:
    traces = []
    for path in sorted(traces_dir().glob("*.json")):
        if path.name.startswith("_"):
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        data.setdefault("id", path.stem)
        traces.append(data)
    if not traces:
        raise AssertionError("no traces in traces/")
    return traces


def _job(name: str, fn) -> None:
    fn()
    print(f"  {name} ................. OK")


def check_kernel_source_purity() -> None:
    kernel = repo_root() / "src" / "adventure_forge" / "kernel"
    banned = ("datetime.now", "time.time", "random.", "urandom", "requests.", "uuid.uuid4")
    for path in kernel.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        for token in banned:
            if token in text:
                raise AssertionError(f"kernel impurity {path.name} contains {token}")


def check_large_legal() -> None:
    content = load_pack()
    state, _cursor = new_game(content, 1, "marsh_scout")
    # Walk to salvage with real step so we drive shipped enumerate_legal.
    from adventure_forge.kernel.step import step
    from adventure_forge.kernel.seed import SeedCursor

    cursor = _cursor
    for action_id in ("go:saltfen.market", "go:saltfen.salvage"):
        result = step(state, action_id, content, cursor)
        if not result.accepted:
            raise AssertionError(f"cannot reach salvage via {action_id}")
        state, cursor = result.state, result.cursor
    legal = enumerate_legal(state, content)
    ids = [a.id for a in legal]
    if len(ids) != len(set(ids)):
        raise AssertionError("duplicate legal ids")
    salvage = [i for i in ids if i.startswith("take:salvage_")]
    if len(salvage) < 100:
        raise AssertionError(f"expected 100+ salvage takes, got {len(salvage)}")
    src = (repo_root() / "src" / "adventure_forge" / "kernel" / "legal.py").read_text(encoding="utf-8")
    for token in ("MAX_ACTIONS", "MAX_LEGAL", "[:8]", "[:10]", "truncate"):
        if token in src:
            raise AssertionError(f"legal.py contains cap token {token}")


def check_resume() -> None:
    from adventure_forge.play.session import PlaySession
    import tempfile

    content = load_pack()
    actions = ["go:saltfen.market", "use_marsh_cant", "wait"]
    live = PlaySession.start(content, 1, "marsh_scout")
    for action_id in actions:
        result = live.apply_line(action_id)
        if not result.accepted:
            raise AssertionError(f"resume setup rejected {action_id}")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "save.json"
        live.save(path)
        loaded = PlaySession.load(content, path)
        if loaded.fingerprint() != live.fingerprint():
            raise AssertionError("save/load fingerprint mismatch")
        more = ["ask_about_tablet", "slip_inside"]
        for action_id in more:
            live.apply_line(action_id)
            loaded.apply_line(action_id)
        if live.fingerprint() != loaded.fingerprint():
            raise AssertionError("resumed play diverged from uninterrupted play")


def run_verify() -> int:
    print("verify")
    try:
        content = load_pack()
        traces = load_traces()

        def i1() -> None:
            check_i1(content, [t for t in traces if t.get("outcome")])

        def i4() -> None:
            check_i4(content, traces)

        def language() -> None:
            errors = check_pack_language(content)
            errors.extend(check_walkthrough_budget(content, [t for t in traces if t.get("outcome")]))
            if errors:
                raise AssertionError("language\n" + "\n".join(errors[:20]))

        def crawler() -> None:
            crawl(content)

        def play_crawler() -> None:
            player_crawl(content)

        def tamper() -> None:
            check_tamper(content, traces)

        jobs = [
            ("I1 determinism", i1),
            ("I4 witnesses", i4),
            ("crawler", crawler),
            ("player-crawler", play_crawler),
            ("kernel-purity", check_kernel_source_purity),
            ("language-budget", language),
            ("large-legal", check_large_legal),
            ("resume", check_resume),
            ("tamper", tamper),
            ("firewall", check_firewall),
            ("units", run_units),
        ]
        for name, fn in jobs:
            _job(name, fn)
    except Exception as exc:  # noqa: BLE001 — the bar must surface any failure
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print("PASS")
    return 0
