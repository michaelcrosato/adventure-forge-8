# Slice 29 uniqueness claim — Sounding Stage

Region id: `sounding_stage`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, net loft, or sail loft.

## Mechanic

Coil, mark, cast. The lead line is coiled, fathoms are marked, the lead is cast for depth. Not lens channel sight, not sail hoist, not ropewalk taut walk.

## Inhabitants

- Tern (yard)
- Gage (coil)
- Plumb (cast)

## Locations

`lead.path`, `lead.yard`, `lead.coil`, `lead.marks`, `lead.cast`. Linked from `ashfen.causeway` and `sail.path`.

## Outcome

`lead_cast` — flag `lead_cast`. Witness: `traces/marsh_lead_cast.json`.

## Sheet / deed gates

Same scene `lead.yard`: marshborn/hunt `know_the_fathom_mark`; letters `read_the_lead_list`.

## Cross-effect

Sail hoisted (`sail_hoisted`) unlocks `sound_under_sail` at the cast lip. Proven by `cross_sail_lead` vs `cross_plain_lead`.
