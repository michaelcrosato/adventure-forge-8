# Slice 61 uniqueness claim — Vinegar House

Region id: `vinegar_house`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, net loft, sail loft, sounding stage, chart house, buoy yard, kelp shore, soap house, fulling mill, charcoal clamp, lime kiln, mason yard, thatch croft, rain cistern, wash house, rag mill, osier holt, bakehouse, dairy, loom shed, horn lantern, gall house, cobble shop, cider house, mustard mill, sausage house, pie house, jam house, crock yard, tannery, flax house, nailery, wheelwright, malt house, or brew house.

## Mechanic

Pitch, sour, cork. Mother is pitched, ale is soured, and the cruet is corked. Not brew charge-hop-rack, not mead mash-bung-tap, not pickle pack-lid, not cider mill-wrap-bung.

## Inhabitants

- Mother (yard)
- Sour (sour)
- Cruet (cruet)

## Locations

`acet.path`, `acet.yard`, `acet.mother`, `acet.sour`, `acet.cruet`. Linked from `ashfen.causeway` and `brew.path`.

## Outcome

`cruet_corked` — flag `cruet_corked`. Witness: `traces/marsh_cruet_corked.json`.

## Sheet / deed gates

Same scene `acet.yard`: marshborn/hunt `know_the_mother`; letters `read_the_vinegar_list`.

## Cross-effect

Racked gyle (`gyle_racked`) unlocks `ale_the_mother` at the mother vat. Proven by `cross_brew_acet` vs `cross_plain_acet`.
