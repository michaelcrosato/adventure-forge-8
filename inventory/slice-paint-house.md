# Slice 69 uniqueness claim — Paint House

Region id: `paint_house`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, net loft, sail loft, sounding stage, chart house, buoy yard, kelp shore, soap house, fulling mill, charcoal clamp, lime kiln, mason yard, thatch croft, rain cistern, wash house, rag mill, osier holt, bakehouse, dairy, loom shed, horn lantern, gall house, cobble shop, cider house, mustard mill, sausage house, pie house, jam house, crock yard, tannery, flax house, nailery, wheelwright, malt house, brew house, vinegar house, glue house, bindery, gilder's loft, jeweler, glazier, sash house, or putty house.

## Mechanic

Mull, mix, brush. Colour is mulled, oil is mixed, and the coat is brushed. Not dye charge-dip, not gall crush-mix-nib, not gilding bole-lay-burnish, not putty whip-knife-dust.

## Inhabitants

- Mull (yard)
- Oil (oil)
- Brush (brush)

## Locations

`paint.path`, `paint.yard`, `paint.mull`, `paint.oil`, `paint.brush`. Linked from `ashfen.causeway` and `putty.path`.

## Outcome

`coat_brushed` — flag `coat_brushed`. Witness: `traces/marsh_coat_brushed.json`.

## Sheet / deed gates

Same scene `paint.yard`: marshborn/hunt `know_the_mull`; letters `read_the_paint_list`.

## Cross-effect

Dusted light (`light_dusted`) unlocks `dust_the_coat` at the mull stone. Proven by `cross_putty_paint` vs `cross_plain_paint`.
