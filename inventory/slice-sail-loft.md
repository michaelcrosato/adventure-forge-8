# Slice 28 uniqueness claim — Sail Loft

Region id: `sail_loft`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, or net loft.

## Mechanic

Cut, stitch, hoist. Canvas is cut, the sail is stitched, the spar is hoisted. Not net-loft mesh tar, not ropewalk taut walk, not dye cloth color.

## Inhabitants

- Gale (yard)
- Shear (canvas)
- Haly (hoist)

## Locations

`sail.path`, `sail.yard`, `sail.canvas`, `sail.stitch`, `sail.hoist`. Linked from `ashfen.causeway` and `net.path`.

## Outcome

`sail_hoisted` — flag `sail_hoisted`. Witness: `traces/marsh_sail_hoisted.json`.

## Sheet / deed gates

Same scene `sail.yard`: marshborn/hunt `know_the_canvas_cut`; letters `read_the_sail_list`.

## Cross-effect

Net tarred (`net_tarred`) unlocks `tar_the_twine` at the hoist. Proven by `cross_net_sail` vs `cross_plain_sail`.
