# Slice 89 uniqueness claim — Mantel House

Region id: `mantel_house`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, net loft, sail loft, sounding stage, chart house, buoy yard, kelp shore, soap house, fulling mill, charcoal clamp, lime kiln, mason yard, thatch croft, rain cistern, wash house, rag mill, osier holt, bakehouse, dairy, loom shed, horn lantern, gall house, cobble shop, cider house, mustard mill, sausage house, pie house, jam house, crock yard, tannery, flax house, nailery, wheelwright, malt house, brew house, vinegar house, glue house, bindery, gilder's loft, jeweler, glazier, sash house, putty house, paint house, varnish house, latch house, hinge house, stay house, sill house, casing house, skirting house, dado house, picture rail, cornice house, stair house, newel house, handrail house, baluster house, tread house, floorboard house, joist house, lath house, or chimney house.

## Mechanic

Bed, set, pin. The lintel is bedded, the corbel is set, and the mantel is pinned. Not chimney bed-set-lime, not sill bed-kerf-seat, not sash rebate-tenon-pin, not dairy shelf.

## Inhabitants

- Lintel (yard)
- Corbel (corbel)
- Mantel (overmantel)

## Locations

`mant.path`, `mant.yard`, `mant.lintel`, `mant.corbel`, `mant.over`. Linked from `ashfen.causeway` and `chim.path`. Outcome exit is `Go to the overmantel` (dairy already owns `Go to the shelf`; sash owns `Go to the pin`).

## Outcome

`mantel_pinned` — flag `mantel_pinned`. Witness: `traces/marsh_mantel_pinned.json`.

## Sheet / deed gates

Same scene `mant.yard`: marshborn/hunt `know_the_lintel`; letters `read_the_mantel_list`.

## Cross-effect

Limed breast (`breast_limed`) unlocks `lime_the_lintel` at the lintel bench. Proven by `cross_chim_mant` vs `cross_plain_mant`.
