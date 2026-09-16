# Slice 99 uniqueness claim — Launch Ways

Region id: `launch_ways`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, net loft, sail loft, sounding stage, chart house, buoy yard, kelp shore, soap house, fulling mill, charcoal clamp, lime kiln, mason yard, thatch croft, rain cistern, wash house, rag mill, osier holt, bakehouse, dairy, loom shed, horn lantern, gall house, cobble shop, cider house, mustard mill, sausage house, pie house, jam house, crock yard, tannery, flax house, nailery, wheelwright, malt house, brew house, vinegar house, glue house, bindery, gilder's loft, jeweler, glazier, sash house, putty house, paint house, varnish house, latch house, hinge house, stay house, sill house, casing house, skirting house, dado house, picture rail, cornice house, stair house, newel house, handrail house, baluster house, tread house, floorboard house, joist house, lath house, chimney house, mantel house, flue house, fireback house, grate house, brick yard, tile house, slate yard, flashing house, block loft, or oar loft.

## Mechanic

Grease, poppet, trip. The ways are greased, the poppet is set, and the trigger is tripped. Not oar loft round-spoon-bind, not ferry slip crossing, not caulk pay-seam, not block strop.

## Inhabitants

- Grease (yard)
- Poppet (poppet)
- Trigger (trigger)

## Locations

`ways.path`, `ways.yard`, `ways.grease`, `ways.poppet`, `ways.trigger`. Linked from `ashfen.causeway` and `oar.path`.

## Outcome

`hull_launched` — flag `hull_launched`. Witness: `traces/marsh_hull_launched.json`.

## Sheet / deed gates

Same scene `ways.yard`: marshborn/hunt `know_the_grease`; letters `read_the_ways_list`.

## Cross-effect

Bound grip (`grip_bound`) unlocks `grip_the_grease` at the grease bench. Proven by `cross_oar_ways` vs `cross_plain_ways`.
