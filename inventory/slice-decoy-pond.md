# Slice 24 uniqueness claim — Decoy Pond

Region id: `decoy_pond`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, or tide forge.

## Mechanic

Pipes, drive, bag. Reed pipes are laid, ducks are driven into the curve, the fowl is bagged in the taking tunnel. Not eel-weir baskets, not oyster cull, not forge quench.

## Inhabitants

- Decoyman Wisp (yard)
- Lark (pipes)
- Nye (tunnel)

## Locations

`decoy.path`, `decoy.yard`, `decoy.pipes`, `decoy.screen`, `decoy.tunnel`. Linked from `ashfen.causeway` and `forge.path`.

## Outcome

`fowl_taken` — flag `fowl_taken`. Witness: `traces/marsh_fowl_taken.json`.

## Sheet / deed gates

Same scene `decoy.yard`: marshborn/hunt `know_the_decoy_run`; letters `read_the_decoy_list`.

## Cross-effect

Iron quenched (`iron_quenched`) unlocks `hook_the_take` at the tunnel. Proven by `cross_forge_decoy` vs `cross_plain_decoy`.
