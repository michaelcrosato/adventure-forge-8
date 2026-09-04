# Adventure Forge 8 — Orchestrator plan

Status: executing. This file is the live constitution for the repository.
Supersedes the four original briefs (now in `archive/original-briefs/`).
On conflict, the locked parts below win. They are taken from the x46 kernel brief.

**Freedom in design. Honesty in verification. The model never is the world.**
**The orchestrator owns the factory. The bar owns the truth. The game is the score.**
**Plain words. Real verbs. One world. The sheet you brought changes the room you enter.**

---

## Locked honesty invariants

These do not move. A better game that violates them is a different product.

### I1. Pure step

```text
step(state, action, content, seed-cursor) → state'
```

- No wall clock, network, or ambient RNG inside the transition.
- All game randomness is an explicit serializable cursor derived from a seed.
- Same content + same seed + same action sequence + same character sheet ⇒ identical observable run.
- A canonical fingerprint is the definition of “same run.”

### I2. Content is data; rules are code

World, inhabitants, reactions, items, dialogue, and outcomes are data the engine interprets.

- Closed effect/condition vocabulary. New verbs ship with a checker in the same change.
- A model may draft or patch data. A model may not invent a one-off side effect that only exists in prose.
- Illegal actions are rejected by code. The model is never the physics.

### I3. Enumerated legal moves

Each observation exposes legal actions with stable identities.

- Choosing an action is the only way the world advances.
- Surfaces do not reimplement legality.
- Free text is sugar that maps onto a legal id. Failed mapping does not move the world.

### I4. Claims are proofs

For every shipped region or outcome:

- A primary walkthrough replays to the advertised success predicate.
- Every other advertised distinct outcome has its own replayable witness.
- References resolve.
- Character-conditioned reactions have a witness pair: same scene, two sheets, different legal outcomes or world reactions, both replayable.
- The acceptor is mechanical.

### I5. `verify` is the bar

One machine command, no LLM required:

1. The I1 property.
2. I4 proofs for every shipped slice.
3. A non-LLM crawler on the real engine (crash, empty legal-set, bounds, impurity).
4. Load-bearing unit/type checks.
5. Plain-language and observation-budget tests (G2, G5, I8).

A change that fails `verify` did not land. The orchestrator may replace the *implementation* of the bar with a stricter or faster one. It may not delete the *job* of the bar.

### I6. Play / build firewall

| Loop | Sees source / solutions | Changes the tree | Must produce |
|---|---|---|---|
| Play | No | No | Replay-verified session + structured findings |
| Build | Yes | Yes, as the orchestrator allows | Changes that leave `verify` green |

Unreplayable reports are discarded. Builders’ knowledge does not ride the player path.

### I7. Autonomy with a non-LLM driver

Builders and the orchestrator choose what to build and how the factory runs. They may not delete proofs to go green, hide rules in prose, let the player surface invent actions, or commit a trace the engine cannot replay.

### I8. Agent-playable on a budget

A competent agent takes a full turn from one observation. Observation size is bounded and tested. A large legal set stays playable by grouping, paging, or filter — never by silent truncation, never by dumping an unreadable menu.

---

## Locked game-product requirements

### G1. One world

One contiguous world. No second campaign, no pocket universe that is a different game. Travel, towns, dungeons, and talk are regions of the same state.

### G2. Plain speech

UI labels, menus, speech, and description use simple, short, straight language. Flavor is allowed. Fog is not. Testable with length budgets on shipped strings and on official-walkthrough observations.

### G3. A character the world can see

The protagonist is customizable on real axes (origin, body, skill, creed, mark, tongue). The world queries the sheet as data:

- Legal actions may appear, vanish, or change cost by sheet.
- NPC stance, prices, access, and offered verbs may change by sheet and by deeds.
- Two sheets through the same opening must produce a proven divergence (I4).

Cosmetic-only customization does not satisfy G3.

### G4. Scope north star

Target shape: geographic / travel scale on the order of a Skyrim-sized playable map; per-area interaction depth on the order of a Baldur’s Gate 3 locale.

Honest scale:

- A node with no unique verbs, no unique inhabitants, and no unique consequences does not count.
- Procedural fill is substrate. Authored depth is what the rubric scores.
- The factory ships the world in slices. Each shipped slice meets I4. Unshipped wilderness is not a claim.

Empty miles are a disqualification. This scored revision ships a **credible unique-area slice** plus this executing G4 plan. Full unique-location count is the standing north star after the bar is green, not a license to fail the slice, and not a license to pass with wallpaper.

### G5. Action first

Observations lead with situation + legal verbs. Prose exists to make the next verb intelligible, then stops. A scene that can only be enjoyed by reading a page and clicking Continue is a defect.

### G6. No artificial scene cap

If a verb is implemented for that state, it may be offered. There is no design rule “a scene may have at most N choices.”

Allowed bounds: the closed DSL, the observation budget, legality. Unlimited means no ceiling on programmed options. It does not mean the model may invent options at play time.

---

## Orchestrator authority

The orchestrator agent owns this repository: priority, delegation, integration, workflow health, and whether a change served the game.

Process is fluid. The orchestrator may rewrite scripts, queues, prompts, branching, and factory internals as often as needed.

Authority stops at the invariants. The orchestrator may not: make the model the physics; drop the firewall; ship unreplayable outcomes; count empty map as G4; replace G2 with purple prose; call a cosmetic title-picker G3; edit `verify` to ignore a failing proof.

Success is both constraint satisfaction and game quality under those constraints. Process volume is not success.

---

## First scored slice (executing now)

World: **Ashfen Coast** — one drowned river mouth.

| Region | Mechanic (not a reskin) | Role |
|---|---|---|
| Saltfen Harbor | Law, papers, prices, tides, dock compact | Social / institutional |
| Hollow Stacks | Vertical climb, guyline, collapse, relic | Spatial / risk |
| Kiln Mill | Heat states, craft damper, grain-debt pact | Craft / debt |

Character axes the world queries: origin, body, skill, creed, mark, tongue.

Authored outcomes:

1. `harbor_compact` — the dock compact is restored.
2. `stack_relic` — the ash relic is taken.
3. `kiln_pact` — the mill grain-debt is sealed in the kiln.

Witness pair: Saltfen Market, `marsh_scout` vs `city_oath`, different legal verbs, both replayable.

Large legal set: Saltfen salvage yard, 100+ programmed take-actions, no engine cap, player surface pages/groups.

Surfaces:

- Player: `python -m adventure_forge play` (plain language, mapper-or-no-op).
- Builder: repository + `verify`.
- Bar: `python -m adventure_forge verify` (also `scripts/verify`).

Capabilities on this slice: seeded new game, resume, trace record, trace replay, I1, I4, crawler, language/budget, unit checks, orchestrator charter, one delegation, one process rewrite, one flywheel turn, one rejected unreplayable report.

---

## G4 executing plan (after the bar is green)

Each new slice must add unique verbs, inhabitants, and consequences. Wallpaper cells do not ship.

1. **Slice 0:** Saltfen + Stacks, two outcomes, sheet divergence, salvage stress scene.
2. **Slice 1 (shipping):** Kiln Mill — heat, craft, grain-debt. Cross-effect: compact restored unlocks dock rates at the mill yard.
3. **Slice 2:** Reed court — law argument, witness, sentence. Sheet and deeds gate standing.
4. **Slice 3:** Drowned road — travel graph, weather-as-turn, encounters that write lasting flags.
5. **Slice 4+:** Authored pockets (camps, ruins, hamlets) on generated substrate. Crawler hunts *sameness* and rejects reskins.
6. **Scale rule:** stop counting a cell when a sameness crawler cannot tell it from another cell by verbs + inhabitants + effects.

The factory may generate substrate. Authored depth is what we claim.

---

## How to run

```text
python3 -m adventure_forge play --preset marsh_scout --seed 1
python3 -m adventure_forge play --preset marsh_scout --seed 1 --commands-file traces/marsh_harbor_compact.json
python3 -m adventure_forge verify
```

Play does not read traces as solutions except when a builder explicitly asks it to execute a command file. The play module does not import orchestrator evidence or verify internals.

---

## Non-goals (this scored revision)

- Copying Skyrim or Baldur’s Gate 3 plots, factions, IP, 3D, shouts, or Larian combat.
- Play-time LLM improvisation of rooms, rulings, or outcomes.
- A GUI (CLI is enough).
- Treating commit count, test count, or agent volume as success.
- Keeping the four original briefs as live law.
