# Slice 39 uniqueness claim — Rain Cistern

Region id: `rain_cistern`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, net loft, sail loft, sounding stage, chart house, buoy yard, kelp shore, soap house, fulling mill, charcoal clamp, lime kiln, mason yard, or thatch croft.

## Mechanic

Hang, set, dip. A gutter is hung, the tun is set, and a pail is dipped. Not windpump vanes, not eel-weir lift, not ice-cellar pack, not pickle tub.

## Inhabitants

- Eave (yard)
- Tun (tun)
- Dip (dip)

## Locations

`cistern.path`, `cistern.yard`, `cistern.eave`, `cistern.tun`, `cistern.dip`. Linked from `ashfen.causeway` and `thatch.path`.

## Outcome

`cistern_filled` — flag `cistern_filled`. Witness: `traces/marsh_cistern_filled.json`.

## Sheet / deed gates

Same scene `cistern.yard`: marshborn/hunt `know_the_eave_run`; letters `read_the_cistern_list`.

## Cross-effect

Set roof (`roof_set`) unlocks `hang_under_roof` at the eave. Proven by `cross_thatch_cistern` vs `cross_plain_cistern`.
