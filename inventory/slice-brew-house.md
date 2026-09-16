# Slice 60 uniqueness claim — Brew House

Region id: `brew_house`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, net loft, sail loft, sounding stage, chart house, buoy yard, kelp shore, soap house, fulling mill, charcoal clamp, lime kiln, mason yard, thatch croft, rain cistern, wash house, rag mill, osier holt, bakehouse, dairy, loom shed, horn lantern, gall house, cobble shop, cider house, mustard mill, sausage house, pie house, jam house, crock yard, tannery, flax house, nailery, wheelwright, or malt house.

## Mechanic

Charge, hop, rack. Grist is charged, the wort is hopped, and the gyle is racked. Not mead mash-bung-tap, not malt steep-turn-oast, not cider mill-wrap-bung.

## Inhabitants

- Grist (yard)
- Wort (wort)
- Gyle (gyle)

## Locations

`brew.path`, `brew.yard`, `brew.grist`, `brew.wort`, `brew.gyle`. Linked from `ashfen.causeway` and `malt.path`.

## Outcome

`gyle_racked` — flag `gyle_racked`. Witness: `traces/marsh_gyle_racked.json`.

## Sheet / deed gates

Same scene `brew.yard`: marshborn/hunt `know_the_grist`; letters `read_the_brew_list`.

## Cross-effect

Oasted malt (`malt_oasted`) unlocks `malt_the_grist` at the hopper. Proven by `cross_malt_brew` vs `cross_plain_brew`.
