# Slice 35 uniqueness claim — Charcoal Clamp

Region id: `charcoal_clamp`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, net loft, sail loft, sounding stage, chart house, buoy yard, kelp shore, soap house, or fulling mill.

## Mechanic

Cut, stack, draw. Coppice is cut, stacked in a clamp, and drawn as coal. Not mill-kiln grain debt, not kelp-ash burn, not tide-forge quench, not peat fold cut.

## Inhabitants

- Copse (yard)
- Turf (clamp)
- Draw (draw)

## Locations

`char.path`, `char.yard`, `char.copse`, `char.clamp`, `char.draw`. Linked from `ashfen.causeway` and `full.path`.

## Outcome

`coal_drawn` — flag `coal_drawn`. Witness: `traces/marsh_coal_drawn.json`.

## Sheet / deed gates

Same scene `char.yard`: marshborn/hunt `know_the_coppice`; letters `read_the_coal_list`.

## Cross-effect

Fulled cloth (`cloth_fulled`) unlocks `cover_the_clamp` at the clamp. Proven by `cross_full_char` vs `cross_plain_char`.
