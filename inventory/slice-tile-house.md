# Slice 94 uniqueness claim — Tile House

Region id: `tile_house`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, net loft, sail loft, sounding stage, chart house, buoy yard, kelp shore, soap house, fulling mill, charcoal clamp, lime kiln, mason yard, thatch croft, rain cistern, wash house, rag mill, osier holt, bakehouse, dairy, loom shed, horn lantern, gall house, cobble shop, cider house, mustard mill, sausage house, pie house, jam house, crock yard, tannery, flax house, nailery, wheelwright, malt house, brew house, vinegar house, glue house, bindery, gilder's loft, jeweler, glazier, sash house, putty house, paint house, varnish house, latch house, hinge house, stay house, sill house, casing house, skirting house, dado house, picture rail, cornice house, stair house, newel house, handrail house, baluster house, tread house, floorboard house, joist house, lath house, chimney house, mantel house, flue house, fireback house, grate house, or brick yard.

## Mechanic

Drape, pallet, nick. Clay is draped on the pantile horse, the green is palleted, and the arris is nicked. Not brick pug-strike-hack, not thatch ridge, not peat-fold green, not floorboard arris-shoot.

## Inhabitants

- Horse (yard)
- Pallet (pallet)
- Arris (arris)

## Locations

`tile.path`, `tile.yard`, `tile.horse`, `tile.pallet`, `tile.arris`. Linked from `ashfen.causeway` and `brick.path`.

## Outcome

`arris_nicked` — flag `arris_nicked`. Witness: `traces/marsh_arris_nicked.json`.

## Sheet / deed gates

Same scene `tile.yard`: marshborn/hunt `know_the_horse`; letters `read_the_tile_list`.

## Cross-effect

Set hack (`hack_set`) unlocks `hack_the_horse` at the horse bench. Proven by `cross_brick_tile` vs `cross_plain_tile`.
