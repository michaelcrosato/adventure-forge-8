# Slice 26 uniqueness claim — Caulk Yard

Region id: `caulk_yard`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, or rushlight house.

## Mechanic

Oakum, pitch, caulk. Old rope is teased into oakum, pitch is melted, the hull seam is caulked. Not ropewalk twist, not forge quench, not rushlight bind.

## Inhabitants

- Gull (yard)
- Tarn (oakum)
- Pike (seam)

## Locations

`caulk.path`, `caulk.yard`, `caulk.oakum`, `caulk.kettle`, `caulk.seam`. Linked from `ashfen.causeway` and `rush.path`.

## Outcome

`seam_caulked` — flag `seam_caulked`. Witness: `traces/marsh_seam_caulked.json`.

## Sheet / deed gates

Same scene `caulk.yard`: marshborn/hunt `know_the_oakum_tease`; letters `read_the_caulk_list`.

## Cross-effect

Lights bound (`lights_bound`) unlocks `light_the_seam` at the open seam. Proven by `cross_rush_caulk` vs `cross_plain_caulk`.
