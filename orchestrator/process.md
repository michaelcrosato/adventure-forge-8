# Process v2

Rewritten by the orchestrator. Honesty unchanged: `verify` is still the bar. Players still cannot see solutions. The model is still not the physics.

## Why rewrite

v1 was serial and kept subagents idle. That slowed the factory without protecting I1–I8. Delegation is now the default for bounded builder tasks. The orchestrator still integrates and still cannot capture the bar.

## Loop

1. Assess gaps against PLAN.md (constraints first, then G4 unique depth).
2. Delegate bounded builder work (content, tests, crawler reports) with a written acceptance condition.
3. Integrate on a green `python -m adventure_forge verify`.
4. Record traces. Push.
5. Discard reports that cannot be replayed.

## Defaults

- Builder model: grok-4.6-low (speed/cost benchmark).
- Content changes go through `tools/build_pack.py` then `tools/record_traces.py`.
- Kernel physics changes require I1 + impurity crawler still green.
- Never edit `verify` to ignore a failing proof.

## Still forbidden

Deleting proofs, play-time model physics, wallpaper cells counted as G4, putting walkthroughs on the player observation path.

