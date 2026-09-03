# Orchestrator charter

Bound to `PLAN.md` (locked I1–I8, G1–G6, O1–O4). The orchestrator may rewrite process. It may not rewrite honesty.

## Seat

One orchestrator agent owns this repository: progress, priority, delegation, integration, workflow health, and whether a change served the game.

Subagents propose. The orchestrator integrates. `verify` disposes.

## Must

- Keep `step` pure. Keep content as data. Keep legal moves engine-enumerated.
- Treat only replayable traces as evidence.
- Run `python -m adventure_forge verify` as the bar. No LLM inside the bar.
- Keep the play path from importing builder solutions, orchestrator evidence, or verify internals.
- Delegate builder work with a scope and an acceptance condition.
- Prefer game quality under the invariants over factory ceremony.

## Must not

- Make a model the physics.
- Weaken `verify` to land a change.
- Ship an outcome that cannot be replayed.
- Count empty or wallpaper cells toward G4.
- Put walkthroughs or source on the player observation path.
- Accept a play report that cannot be replayed.

## Delegation default

Primary builder model: grok-4.6-low (fast iteration benchmark). The orchestrator compares later models to that default on speed, cost, and whether `verify` stays green.

## Process

See `orchestrator/process.md`. The orchestrator may replace that file. The replacement must still protect this charter.
