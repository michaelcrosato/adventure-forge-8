# Slice 3 uniqueness claim — Drowned Road

Region id: `drowned_road`. Not a reskin of harbor, stacks, mill, or court.

## Mechanic

Weather is a turn-derived cycle (`clear` / `rain` / `fog`) from the seed-cursor clock, not wall time. Rain and fog unlock unique road verbs. Encounters write lasting flags.

## Inhabitants

- Dike keeper Rell
- Hut widow Cal

## Locations

`road.ford`, `road.dike`, `road.hut`, `road.drownway`, `road.beacon`. Linked from `ashfen.causeway`.

## Outcome

`road_beacon` — flag `beacon_lit`. Witness: `traces/marsh_road_beacon.json`.

## Sheet / deed gates

Same scene `road.hut`: hunt `track_drowned_prints`; might `force_hut_latch`.

## Cross-effect

Reed sentence (`reed_sentence_passed`) unlocks `name_the_sentence` at the hut. Proven by `cross_court_road` vs `cross_plain_road`.
