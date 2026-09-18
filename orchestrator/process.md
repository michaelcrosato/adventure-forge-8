# Process v3

Rewritten by the orchestrator. Honesty unchanged: `verify` is still the bar. Players still cannot see solutions. The model is still not the physics.

## Why rewrite

v2 made delegation the default and got faster. It got faster at the wrong thing.

Between slice 25 and slice 143 the factory shipped 118 regions that a crawler
cannot tell apart — same verb shapes, same effect shapes, same five rooms, new
vocabulary — in a single commit, under a green bar. The bar was green because
nothing in it could ask "is this a different place?". It could only ask "does
this replay?", and a reskin replays perfectly.

Two things were true at once and neither was caught:

- PLAN.md promised a sameness crawler in writing, twice, and it was never built.
- The one surface a player could actually reach accepted a client-supplied world
  state, which handed out 139 of 144 outcomes in a single request.

v3 exists so that neither failure can repeat silently.

## Loop

1. Assess gaps against PLAN.md (constraints first, then G4 *unique* depth).
2. Delegate bounded builder work with a written acceptance condition.
3. Integrate on a green `python -m adventure_forge verify`.
4. Record traces. Push.
5. Discard reports that cannot be replayed.

## Defaults

- Builder model: grok-4.6-low (speed/cost benchmark). Record the comparison when
  a different model is used — the charter asks for it and no record exists yet.
- Content changes go through `tools/build_pack.py` then `tools/record_traces.py`.
- Kernel physics changes require I1 + impurity crawler still green.
- Never edit `verify` to ignore a failing proof.
- Install the hook once: `scripts/install-hooks`. CI runs the full bar on push.

## Counting rule

**A slice counts when the sameness crawler can tell it from every shipped
region.** Not when it has a new name, a new noun, or a new flag.

`verify`'s `sameness` job enforces this against `sameness-baseline.json`. The
limits in that file are debt, recorded honestly. Moving a limit toward its
target is the work. Moving one away from its target requires a reason in the
commit message, and a reviewer should treat it the way they would treat editing
a failing test to pass.

Before shipping a region, ask the three questions G4 actually asks:

- Does it have a **verb** no other region has?
- Does it have an **inhabitant** who does something no other inhabitant does?
- Does it have a **consequence** that changes play somewhere else?

Three no's is a reskin. Ship nothing.

## Volume is not progress

PLAN.md already lists this as a non-goal: "Treating commit count, test count, or
agent volume as success." The 118-region commit added 23,195 lines of tests,
714 traces, and 3,705 lines of proof code, and improved the game by nothing that
a player could perceive. Those numbers went up because they are easy to make go
up.

The quantity to watch is `distinct_region_fingerprints`. It is printed by every
`verify` run.

Measured across the commit that did the damage:

| | before `35ceceb` | after |
|---|---|---|
| regions shipped | 24 | 144 |
| regions a crawler can tell apart | 20 | **21** |
| largest indistinguishable class | 3 | **118** |
| rooms with no verb | 27 | **148** |

**120 regions bought one distinguishable place.** Every other number went the
wrong way. The bar was green throughout, because nothing in it was looking.

Re-baselining the ratchet at the pre-commit numbers and running the current pack
against it reproduces the block:

```
largest_clone_class rose to 118 (limit 3)
regions_in_clone_classes rose to 126 (limit 6)
wallpaper_locations rose to 148 (limit 27)
```

## Trust boundaries

A dump that crossed the network is not a save file. `PlaySession.from_dump`
takes `trusted=`; HTTP passes `trusted=False` and gets replay-only
reconstruction. Any new surface must do the same, and must be exercised by
`verify/web_surface.py` — the firewall's import scan proves what a surface
imports, never what it accepts.

## Still forbidden

Deleting proofs, play-time model physics, wallpaper cells counted as G4, putting
walkthroughs on the player observation path, and shipping a region the sameness
crawler cannot distinguish from one already shipped.
