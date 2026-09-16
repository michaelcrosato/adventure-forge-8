# Slice 63 uniqueness claim — Bindery

Region id: `bindery`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, net loft, sail loft, sounding stage, chart house, buoy yard, kelp shore, soap house, fulling mill, charcoal clamp, lime kiln, mason yard, thatch croft, rain cistern, wash house, rag mill, osier holt, bakehouse, dairy, loom shed, horn lantern, gall house, cobble shop, cider house, mustard mill, sausage house, pie house, jam house, crock yard, tannery, flax house, nailery, wheelwright, malt house, brew house, vinegar house, or glue house.

## Mechanic

Gather, sew, nip. Quires are gathered, bands are sewn, and the board is nipped. Not rag mill couch-press paper, not gall crush-mix-nib, not chart rutter, not glue trim-seethe-cake.

## Inhabitants

- Quire (yard)
- Band (sew)
- Nip (nip)

## Locations

`bind.path`, `bind.yard`, `bind.quire`, `bind.sew`, `bind.nip`. Linked from `ashfen.causeway` and `glue.path`.

## Outcome

`book_bound` — flag `book_bound`. Witness: `traces/marsh_book_bound.json`.

## Sheet / deed gates

Same scene `bind.yard`: marshborn/hunt `know_the_quire`; letters `read_the_bind_list`.

## Cross-effect

Caked glue (`glue_caked`) unlocks `glue_the_quire` at the gathering bench. Proven by `cross_glue_bind` vs `cross_plain_bind`.
