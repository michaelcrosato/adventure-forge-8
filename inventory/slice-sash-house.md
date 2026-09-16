# Slice 67 uniqueness claim — Sash House

Region id: `sash_house`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, net loft, sail loft, sounding stage, chart house, buoy yard, kelp shore, soap house, fulling mill, charcoal clamp, lime kiln, mason yard, thatch croft, rain cistern, wash house, rag mill, osier holt, bakehouse, dairy, loom shed, horn lantern, gall house, cobble shop, cider house, mustard mill, sausage house, pie house, jam house, crock yard, tannery, flax house, nailery, wheelwright, malt house, brew house, vinegar house, glue house, bindery, gilder's loft, jeweler, or glazier.

## Mechanic

Rebate, tenon, pin. The stile is rebated, the rail is tenoned, and the sash is pinned. Not glazier score-groze-came, not wheelwright dish-spoke-tyre, not mason point-joint, not thatch roof-set.

## Inhabitants

- Stile (yard)
- Rail (rail)
- Pin (pin)

## Locations

`sash.path`, `sash.yard`, `sash.stile`, `sash.rail`, `sash.pin`. Linked from `ashfen.causeway` and `glaz.path`.

## Outcome

`sash_pinned` — flag `sash_pinned`. Witness: `traces/marsh_sash_pinned.json`.

## Sheet / deed gates

Same scene `sash.yard`: marshborn/hunt `know_the_stile`; letters `read_the_sash_list`.

## Cross-effect

Camed pane (`pane_camed`) unlocks `came_the_rebate` at the stile bench. Proven by `cross_glaz_sash` vs `cross_plain_sash`.
