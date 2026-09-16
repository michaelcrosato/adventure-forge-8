# Slice 85 uniqueness claim — Floorboard House

Region id: `floorboard_house`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, net loft, sail loft, sounding stage, chart house, buoy yard, kelp shore, soap house, fulling mill, charcoal clamp, lime kiln, mason yard, thatch croft, rain cistern, wash house, rag mill, osier holt, bakehouse, dairy, loom shed, horn lantern, gall house, cobble shop, cider house, mustard mill, sausage house, pie house, jam house, crock yard, tannery, flax house, nailery, wheelwright, malt house, brew house, vinegar house, glue house, bindery, gilder's loft, jeweler, glazier, sash house, putty house, paint house, varnish house, latch house, hinge house, stay house, sill house, casing house, skirting house, dado house, picture rail, cornice house, stair house, newel house, handrail house, baluster house, or tread house.

## Mechanic

Shoot, tongue, secret. Edge is shot on the plane, meeting is tongued and grooved, and the nail is secreted. Not tread mark-nosing-return, not nailery snip-head-point, not casing mitre-scribe-tack, not sash rebate-tenon-pin.

## Inhabitants

- Shot (yard)
- Groove (tongue)
- Blind (secret)

## Locations

`floor.path`, `floor.yard`, `floor.shot`, `floor.tongue`, `floor.secret`. Linked from `ashfen.causeway` and `tread.path`.

## Outcome

`nail_secreted` — flag `nail_secreted`. Witness: `traces/marsh_nail_secreted.json`.

## Sheet / deed gates

Same scene `floor.yard`: marshborn/hunt `know_the_shot`; letters `read_the_floor_list`.

## Cross-effect

Returned end (`end_returned`) unlocks `return_the_shot` at the shot bench. Proven by `cross_tread_floor` vs `cross_plain_floor`.
