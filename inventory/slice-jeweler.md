# Slice 65 uniqueness claim — Jeweler

Region id: `jeweler`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, net loft, sail loft, sounding stage, chart house, buoy yard, kelp shore, soap house, fulling mill, charcoal clamp, lime kiln, mason yard, thatch croft, rain cistern, wash house, rag mill, osier holt, bakehouse, dairy, loom shed, horn lantern, gall house, cobble shop, cider house, mustard mill, sausage house, pie house, jam house, crock yard, tannery, flax house, nailery, wheelwright, malt house, brew house, vinegar house, glue house, bindery, or gilder's loft.

## Mechanic

Beat, seat, close. Gold foil is beaten, the gem is seated, and the collet is closed. Not gilding bole-lay-burnish, not cobble last-awl-peg, not nailery snip-head-point, not forge quench.

## Inhabitants

- Foil (yard)
- Seat (seat)
- Collet (collet)

## Locations

`gem.path`, `gem.yard`, `gem.foil`, `gem.seat`, `gem.collet`. Linked from `ashfen.causeway` and `gilt.path`.

## Outcome

`collet_closed` — flag `collet_closed`. Witness: `traces/marsh_collet_closed.json`.

## Sheet / deed gates

Same scene `gem.yard`: marshborn/hunt `know_the_foil`; letters `read_the_gem_list`.

## Cross-effect

Burnished plate (`plate_burnished`) unlocks `gilt_the_foil` at the foil bench. Proven by `cross_gilt_gem` vs `cross_plain_gem`.
