# Slice 40 uniqueness claim — Wash House

Region id: `wash_house`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, net loft, sail loft, sounding stage, chart house, buoy yard, kelp shore, soap house, fulling mill, charcoal clamp, lime kiln, mason yard, thatch croft, or rain cistern.

## Mechanic

Soak, beat, hang. Cloth is soaked, beaten on the beetle, and hung on the line. Not fulling-mill walk, not soap leach-boil-cut, not cistern hang-set-dip, not cooperage soak.

## Inhabitants

- Suds (yard)
- Bat (beetle)
- Line (line)

## Locations

`wash.path`, `wash.yard`, `wash.pan`, `wash.beetle`, `wash.line`. Linked from `ashfen.causeway` and `cistern.path`.

## Outcome

`wash_hung` — flag `wash_hung`. Witness: `traces/marsh_wash_hung.json`.

## Sheet / deed gates

Same scene `wash.yard`: marshborn/hunt `know_the_wash_run`; letters `read_the_wash_list`.

## Cross-effect

Filled cistern (`cistern_filled`) unlocks `fill_the_pan` at the wash pan. Proven by `cross_cistern_wash` vs `cross_plain_wash`.
