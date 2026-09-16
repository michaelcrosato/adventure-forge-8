# Slice 97 uniqueness claim — Block Loft

Region id: `block_loft`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, net loft, sail loft, sounding stage, chart house, buoy yard, kelp shore, soap house, fulling mill, charcoal clamp, lime kiln, mason yard, thatch croft, rain cistern, wash house, rag mill, osier holt, bakehouse, dairy, loom shed, horn lantern, gall house, cobble shop, cider house, mustard mill, sausage house, pie house, jam house, crock yard, tannery, flax house, nailery, wheelwright, malt house, brew house, vinegar house, glue house, bindery, gilder's loft, jeweler, glazier, sash house, putty house, paint house, varnish house, latch house, hinge house, stay house, sill house, casing house, skirting house, dado house, picture rail, cornice house, stair house, newel house, handrail house, baluster house, tread house, floorboard house, joist house, lath house, chimney house, mantel house, flue house, fireback house, grate house, brick yard, tile house, slate yard, or flashing house.

## Mechanic

Bore, score, strop. The cheek is bored, the sheave is scored, and the block is stropped. Not flashing roll-boss-dress, not buoy spar, not lime shells, not newel blank, not pickle hoop, not glazier score-quarry.

## Inhabitants

- Cheek (yard)
- Sheave (sheave)
- Strop (strop)

## Locations

`block.path`, `block.yard`, `block.cheek`, `block.sheave`, `block.strop`. Linked from `ashfen.causeway` and `flash.path`.

## Outcome

`block_stropped` — flag `block_stropped`. Witness: `traces/marsh_block_stropped.json`.

## Sheet / deed gates

Same scene `block.yard`: marshborn/hunt `know_the_cheek`; letters `read_the_block_list`.

## Cross-effect

Dressed flash (`flash_dressed`) unlocks `dress_the_cheek` at the cheek bench. Proven by `cross_flash_block` vs `cross_plain_block`.
