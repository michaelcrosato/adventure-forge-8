from pathlib import Path


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here, *here.parents, Path.cwd()]:
        if (parent / "content" / "ashfen" / "pack.json").is_file():
            return parent
    raise RuntimeError("cannot locate repo root (content/ashfen/pack.json)")


def pack_path() -> Path:
    return repo_root() / "content" / "ashfen" / "pack.json"


def traces_dir() -> Path:
    return repo_root() / "traces"
