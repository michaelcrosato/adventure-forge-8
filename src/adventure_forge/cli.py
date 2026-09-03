from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from adventure_forge.kernel.content import AXES, load_pack
from adventure_forge.kernel.replay import replay
from adventure_forge.play.session import PlaySession


def _add_sheet_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--preset", help="marsh_scout or city_oath")
    parser.add_argument("--seed", type=int, default=1)
    for axis in AXES:
        parser.add_argument(f"--{axis}")


def _sheet_from_args(args: argparse.Namespace) -> str | dict[str, str]:
    custom = {axis: getattr(args, axis) for axis in AXES if getattr(args, axis)}
    if custom and args.preset:
        raise SystemExit("pass --preset or axes, not both")
    if custom:
        return custom
    return args.preset or "marsh_scout"


def _load_commands(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        data = json.loads(text)
        if isinstance(data, dict) and "actions" in data:
            return [str(a) for a in data["actions"]]
        if isinstance(data, list):
            return [str(a) for a in data]
        raise SystemExit(f"cannot read commands from {path}")
    return [line.strip() for line in text.splitlines() if line.strip() and not line.startswith("#")]


def _cmd_play(args: argparse.Namespace) -> int:
    content = load_pack()
    if args.load:
        session = PlaySession.load(content, Path(args.load))
    else:
        session = PlaySession.start(content, args.seed, _sheet_from_args(args))

    commands: list[str] = []
    if args.commands_file:
        commands.extend(_load_commands(Path(args.commands_file)))
    if args.commands:
        commands.extend(args.commands)

    def emit(text: str) -> None:
        print(text)
        print()

    emit(session.observation().text)

    if commands:
        for line in commands:
            print(f"> {line}")
            result = session.apply_line(line)
            emit(result.message)
            if line.strip().lower() in {"quit", "exit"}:
                break
        if args.save:
            session.save(Path(args.save))
        if args.expect_outcome and args.expect_outcome not in session.state.outcomes:
            print(f"missing outcome {args.expect_outcome}", file=sys.stderr)
            return 1
        print(f"fingerprint {session.fingerprint()}")
        if session.state.outcomes:
            print("outcomes " + ",".join(session.state.outcomes))
        return 0

    if not sys.stdin.isatty() and not args.interactive:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(f"> {line}")
            result = session.apply_line(line)
            emit(result.message)
            if line.lower() in {"quit", "exit"}:
                break
        if args.save:
            session.save(Path(args.save))
        print(f"fingerprint {session.fingerprint()}")
        return 0

    while True:
        try:
            line = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if line.strip().lower() in {"quit", "exit"}:
            break
        result = session.apply_line(line)
        emit(result.message)
    if args.save:
        session.save(Path(args.save))
    return 0


def _cmd_replay(args: argparse.Namespace) -> int:
    content = load_pack()
    trace = json.loads(Path(args.trace).read_text(encoding="utf-8"))
    result = replay(content, trace["seed"], trace["sheet"], trace["actions"])
    print(result.fingerprint)
    print("outcomes " + ",".join(result.state.outcomes))
    if trace.get("final_fingerprint") and result.fingerprint != trace["final_fingerprint"]:
        if trace.get("build_id") == content.build_id:
            print("fingerprint mismatch on same build", file=sys.stderr)
            return 1
    return 0


def _cmd_verify(_args: argparse.Namespace) -> int:
    from adventure_forge.verify.runner import run_verify

    return run_verify()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="adventure-forge")
    sub = parser.add_subparsers(dest="cmd", required=True)

    play = sub.add_parser("play", help="player surface")
    _add_sheet_args(play)
    play.add_argument("--commands", nargs="*", default=[])
    play.add_argument("--commands-file")
    play.add_argument("--save")
    play.add_argument("--load")
    play.add_argument("--expect-outcome")
    play.add_argument("--interactive", action="store_true")
    play.set_defaults(func=_cmd_play)

    verify = sub.add_parser("verify", help="mechanical bar")
    verify.set_defaults(func=_cmd_verify)

    replay_p = sub.add_parser("replay", help="replay a trace")
    replay_p.add_argument("trace")
    replay_p.set_defaults(func=_cmd_replay)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))
