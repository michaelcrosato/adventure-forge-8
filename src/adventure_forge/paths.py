from pathlib import Path


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "PLAN.md").is_file() and (parent / "content").is_dir():
            return parent
    raise RuntimeError("cannot locate repo root (PLAN.md + content/)")


def pack_path() -> Path:
    return repo_root() / "content" / "ashfen" / "pack.json"


def traces_dir() -> Path:
    return repo_root() / "traces"
