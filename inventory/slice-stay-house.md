# Slice 73 uniqueness claim — Stay House

Region id: `stay_house`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, net loft, sail loft, sounding stage, chart house, buoy yard, kelp shore, soap house, fulling mill, charcoal clamp, lime kiln, mason yard, thatch croft, rain cistern, wash house, rag mill, osier holt, bakehouse, dairy, loom shed, horn lantern, gall house, cobble shop, cider house, mustard mill, sausage house, pie house, jam house, crock yard, tannery, flax house, nailery, wheelwright, malt house, brew house, vinegar house, glue house, bindery, gilder's loft, jeweler, glazier, sash house, putty house, paint house, varnish house, latch house, or hinge house.

## Mechanic

Slot, rivet, peg. Bar is slotted, arm is riveted, and the stay is pegged. Not hinge form-drift-ship, not latch file-fit-throw, not sash rebate-tenon-pin, not cobble last-awl-peg.

## Inhabitants

- Slot (yard)
- Arm (arm)
- Eye (eye)

## Locations

`stay.path`, `stay.yard`, `stay.slot`, `stay.arm`, `stay.eye`. Linked from `ashfen.causeway` and `hinge.path`.

## Outcome

`casement_stayed` — flag `casement_stayed`. Witness: `traces/marsh_casement_stayed.json`.

## Sheet / deed gates

Same scene `stay.yard`: marshborn/hunt `know_the_slot`; letters `read_the_stay_list`.

## Cross-effect

Shipped gudgeon (`gudgeon_shipped`) unlocks `hinge_the_slot` at the stay slot. Proven by `cross_hinge_stay` vs `cross_plain_stay`.
