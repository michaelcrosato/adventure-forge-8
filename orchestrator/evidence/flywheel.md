# Flywheel turn 1

## Finding (player surface)

`orchestrator/evidence/player-finding-mira.json`

Marsh scout, seed 1, played only through the player CLI / legal ids:

`go:saltfen.market` → `use_marsh_cant` → `go:ashfen.causeway` → `go:stacks.base` → `talk:mira` → `ask_mira_for_tip`

Replay on the shipped engine: location `stacks.base`, flag `marsh_friend` set. Mira still offered only the generic tip. No marsh-specific verb.

## Rejected report (not this turn's fix)

`orchestrator/evidence/rejected-report.json` — `buy_the_harbor` does not replay. Discarded.

## Builder change

Delegated to grok-4.6-low. Authored data action `share_marsh_path` in `tools/build_pack.py` / `content/ashfen/pack.json`.

Closed vocab: `at`, `has_flag`, `set_flag`, `remember`. Kernel physics unchanged. `verify` not edited to pass.

## Prior traces

`marsh_harbor_compact` and `marsh_stack_relic` action sequences still replay to their outcomes (`tests/test_flywheel.py`). Fingerprints refreshed because `build_id` includes pack bytes.

## After

Marsh friend at stack base has `share_marsh_path`. city_oath without that flag does not.
