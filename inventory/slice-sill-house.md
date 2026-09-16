# Slice 74 uniqueness claim — Sill House

Region id: `sill_house`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, net loft, sail loft, sounding stage, chart house, buoy yard, kelp shore, soap house, fulling mill, charcoal clamp, lime kiln, mason yard, thatch croft, rain cistern, wash house, rag mill, osier holt, bakehouse, dairy, loom shed, horn lantern, gall house, cobble shop, cider house, mustard mill, sausage house, pie house, jam house, crock yard, tannery, flax house, nailery, wheelwright, malt house, brew house, vinegar house, glue house, bindery, gilder's loft, jeweler, glazier, sash house, putty house, paint house, varnish house, latch house, hinge house, or stay house.

## Mechanic

Bed, kerf, seat. Sill is bedded, drip is kerfed, and the stool is seated. Not stay slot-rivet-peg, not sash rebate-tenon-pin, not mason point-joint, not thatch roof-set.

## Inhabitants

- Sill (yard)
- Drip (drip)
- Stool (stool)

## Locations

`sill.path`, `sill.yard`, `sill.bed`, `sill.drip`, `sill.stool`. Linked from `ashfen.causeway` and `stay.path`.

## Outcome

`stool_seated` — flag `stool_seated`. Witness: `traces/marsh_stool_seated.json`.

## Sheet / deed gates

Same scene `sill.yard`: marshborn/hunt `know_the_sill`; letters `read_the_sill_list`.

## Cross-effect

Stayed casement (`casement_stayed`) unlocks `stay_the_sill` at the sill bed. Proven by `cross_stay_sill` vs `cross_plain_sill`.
