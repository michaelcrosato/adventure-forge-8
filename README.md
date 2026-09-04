# Adventure Forge 8

A single-world action adventure whose **rules are ordinary deterministic code**. AI may write content and manage work. **The model is never the physics.**

Live law: [`PLAN.md`](PLAN.md). Orchestrator: [`CHARTER.md`](CHARTER.md).

## Play

```bash
python3 -m adventure_forge play --preset marsh_scout --seed 1
python3 -m adventure_forge play --preset city_oath --seed 1
```

Plain language maps onto a legal action id, or the world does not move.

Presets: `marsh_scout`, `city_oath`. Or pass `--origin --body --skill --creed --mark --tongue`.

Resume: `--save FILE` / `--load FILE`.

Scripted session (player path, command list):

```bash
python3 -m adventure_forge play --preset marsh_scout --seed 1 --commands "go to market" "use marsh cant"
```

## Verify

```bash
python3 -m adventure_forge verify
# or
scripts/verify
```

No LLM. I1 determinism, I4 witnesses, crawler, language/budget, unit checks. Tampering with build, seed, actions, or final state fails.

## Deployment

Vercel loads the root `app.py` adapter for the dependency-free ASGI application.
The root path provides a small landing page, and `/health` reports deployment
health. The game and verification bar remain command-line applications.

## Layout

- `src/adventure_forge/kernel/` — pure `step`, legal set, fingerprint, replay
- `src/adventure_forge/play/` — observation, mapper, CLI (no builder knowledge)
- `src/adventure_forge/verify/` — the bar
- `content/ashfen/pack.json` — world as data
- `traces/` — I4 witnesses
- `archive/original-briefs/` — historical, not live law
