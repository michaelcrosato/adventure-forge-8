from __future__ import annotations

from pathlib import Path

from adventure_forge.paths import repo_root


def check_firewall() -> None:
    play_dir = repo_root() / "src" / "adventure_forge" / "play"
    banned = ("orchestrator", "verify.runner", "verify.i4", "traces_dir")
    paths = list(play_dir.glob("*.py"))
    paths.append(repo_root() / "src" / "adventure_forge" / "web.py")
    paths.append(repo_root() / "app.py")
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for token in banned:
            if token in text:
                raise AssertionError(f"play firewall: {path.name} mentions {token}")
        if "import adventure_forge.verify" in text or "from adventure_forge.verify" in text:
            raise AssertionError(f"play firewall: {path.name} imports verify")
