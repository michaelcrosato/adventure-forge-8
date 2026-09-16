# Slice 72 uniqueness claim — Hinge House

Region id: `hinge_house`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, net loft, sail loft, sounding stage, chart house, buoy yard, kelp shore, soap house, fulling mill, charcoal clamp, lime kiln, mason yard, thatch croft, rain cistern, wash house, rag mill, osier holt, bakehouse, dairy, loom shed, horn lantern, gall house, cobble shop, cider house, mustard mill, sausage house, pie house, jam house, crock yard, tannery, flax house, nailery, wheelwright, malt house, brew house, vinegar house, glue house, bindery, gilder's loft, jeweler, glazier, sash house, putty house, paint house, varnish house, or latch house.

## Mechanic

Form, drift, ship. Knuckle is formed, pintle is drifted, and the gudgeon is shipped. Not latch file-fit-throw, not sash rebate-tenon-pin, not nailery snip-head-point, not forge quench.

## Inhabitants

- Knuckle (yard)
- Pintle (pintle)
- Gudgeon (gudgeon)

## Locations

`hinge.path`, `hinge.yard`, `hinge.knuckle`, `hinge.pintle`, `hinge.gudgeon`. Linked from `ashfen.causeway` and `latch.path`.

## Outcome

`gudgeon_shipped` — flag `gudgeon_shipped`. Witness: `traces/marsh_gudgeon_shipped.json`.

## Sheet / deed gates

Same scene `hinge.yard`: marshborn/hunt `know_the_knuckle`; letters `read_the_hinge_list`.

## Cross-effect

Thrown latch (`latch_thrown`) unlocks `latch_the_knuckle` at the knuckle form. Proven by `cross_latch_hinge` vs `cross_plain_hinge`.
