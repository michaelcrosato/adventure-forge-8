# Slice 100 uniqueness claim — Clinker Shed

Region id: `clinker_shed`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, net loft, sail loft, sounding stage, chart house, buoy yard, kelp shore, soap house, fulling mill, charcoal clamp, lime kiln, mason yard, thatch croft, rain cistern, wash house, rag mill, osier holt, bakehouse, dairy, loom shed, horn lantern, gall house, cobble shop, cider house, mustard mill, sausage house, pie house, jam house, crock yard, tannery, flax house, nailery, wheelwright, malt house, brew house, vinegar house, glue house, bindery, gilder's loft, jeweler, glazier, sash house, putty house, paint house, varnish house, latch house, hinge house, stay house, sill house, casing house, skirting house, dado house, picture rail, cornice house, stair house, newel house, handrail house, baluster house, tread house, floorboard house, joist house, lath house, chimney house, mantel house, flue house, fireback house, grate house, brick yard, tile house, slate yard, flashing house, block loft, oar loft, or launch ways.

## Mechanic

Steam, clench, fair. The strake is steamed, the land is clenched, and the garboard is faired. Not oar loft round-spoon-bind, not launch ways grease-poppet-trip, not caulk pay-seam, not ferry slip.

## Inhabitants

- Steam (yard)
- Land (land)
- Garboard (garboard)

## Locations

`clink.path`, `clink.yard`, `clink.steam`, `clink.land`, `clink.garboard`. Linked from `ashfen.causeway` and `ways.path`.

## Outcome

`garboard_faired` — flag `garboard_faired`. Witness: `traces/marsh_garboard_faired.json`.

## Sheet / deed gates

Same scene `clink.yard`: marshborn/hunt `know_the_steam`; letters `read_the_clinker_list`.

## Cross-effect

Launched hull (`hull_launched`) unlocks `launch_the_steam` at the steam bench. Proven by `cross_ways_clink` vs `cross_plain_clink`.
