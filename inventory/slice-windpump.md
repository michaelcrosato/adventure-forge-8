# Slice 14 uniqueness claim — Windpump

Region id: `windpump`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, or toll ferry.

## Mechanic

Vanes, crank, hold. Set the sail ring, crank the pump, hold the sump so the flats stay dry. Not mill sluice stone, not ferry pole, not road weather, not peat ditch bail.

## Inhabitants

- Keeper Od (yard)
- Rusk (tower)
- Hobb (sump)

## Locations

`pump.path`, `pump.yard`, `pump.tower`, `pump.crank`, `pump.sump`. Linked from `ashfen.causeway` and `ferry.far`.

## Outcome

`flats_drained` — flag `flats_drained`. Witness: `traces/marsh_flats_drained.json`.

## Sheet / deed gates

Same scene `pump.yard`: marshborn/hunt `know_the_wind_cut`; letters `read_the_pump_mark`.

## Cross-effect

Ferry crossed (`ferry_crossed`) unlocks `brace_the_sail` at the vane tower. Proven by `cross_ferry_pump` vs `cross_plain_pump`.
