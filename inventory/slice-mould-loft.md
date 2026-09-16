# Slice 102 uniqueness claim — Mould Loft

Region id: `mould_loft`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, net loft, sail loft, sounding stage, chart house, buoy yard, kelp shore, soap house, fulling mill, charcoal clamp, lime kiln, mason yard, thatch croft, rain cistern, wash house, rag mill, osier holt, bakehouse, dairy, loom shed, horn lantern, gall house, cobble shop, cider house, mustard mill, sausage house, pie house, jam house, crock yard, tannery, flax house, nailery, wheelwright, malt house, brew house, vinegar house, glue house, bindery, gilder's loft, jeweler, glazier, sash house, putty house, paint house, varnish house, latch house, hinge house, stay house, sill house, casing house, skirting house, dado house, picture rail, cornice house, stair house, newel house, handrail house, baluster house, tread house, floorboard house, joist house, lath house, chimney house, mantel house, flue house, fireback house, grate house, brick yard, tile house, slate yard, flashing house, block loft, oar loft, launch ways, clinker shed, or windlass house.

## Mechanic

Loft, spile, bevel. The grid is lofted, the plank is spiled, and the station is bevelled. Not windlass ship-pawl-heave, not picture-rail spring-mould, not wash “Go to the line”, not glass/rope “Go to the loft”.

## Inhabitants

- Grid (yard)
- Spile (spile)
- Bevel (bevel)

## Locations

`offs.path`, `offs.yard`, `offs.grid`, `offs.spile`, `offs.bevel`. Linked from `ashfen.causeway` and `wind.path`.

## Outcome

`station_bevelled` — flag `station_bevelled`. Witness: `traces/marsh_station_bevelled.json`.

## Sheet / deed gates

Same scene `offs.yard`: marshborn/hunt `know_the_grid`; letters `read_the_offset_list`.

## Cross-effect

Heaved round (`round_heaved`) unlocks `heave_the_grid` at the grid bench. Proven by `cross_wind_offs` vs `cross_plain_offs`.
