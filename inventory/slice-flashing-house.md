# Slice 96 uniqueness claim — Flashing House

Region id: `flash_house`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, net loft, sail loft, sounding stage, chart house, buoy yard, kelp shore, soap house, fulling mill, charcoal clamp, lime kiln, mason yard, thatch croft, rain cistern, wash house, rag mill, osier holt, bakehouse, dairy, loom shed, horn lantern, gall house, cobble shop, cider house, mustard mill, sausage house, pie house, jam house, crock yard, tannery, flax house, nailery, wheelwright, malt house, brew house, vinegar house, glue house, bindery, gilder's loft, jeweler, glazier, sash house, putty house, paint house, varnish house, latch house, hinge house, stay house, sill house, casing house, skirting house, dado house, picture rail, cornice house, stair house, newel house, handrail house, baluster house, tread house, floorboard house, joist house, lath house, chimney house, mantel house, flue house, fireback house, grate house, brick yard, tile house, or slate yard.

## Mechanic

Roll, boss, dress. The lead sheet is rolled, the welt is bossed, and the flash is dressed. Not sounding lead-cast, not cistern gutter hang, not slate scapple-punch-lap, not pie roll-crust, not sill drip.

## Inhabitants

- Roll (yard)
- Welt (welt)
- Apron (apron)

## Locations

`flash.path`, `flash.yard`, `flash.sheet`, `flash.welt`, `flash.apron`. Linked from `ashfen.causeway` and `slate.path`.

## Outcome

`flash_dressed` — flag `flash_dressed`. Witness: `traces/marsh_flash_dressed.json`.

## Sheet / deed gates

Same scene `flash.yard`: marshborn/hunt `know_the_roll`; letters `read_the_flash_list`.

## Cross-effect

Lapped slate (`slate_lapped`) unlocks `lap_the_sheet` at the sheet bench. Proven by `cross_slate_flash` vs `cross_plain_flash`.
