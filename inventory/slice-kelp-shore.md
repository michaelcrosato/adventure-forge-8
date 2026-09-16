# Slice 32 uniqueness claim — Kelp Shore

Region id: `kelp_shore`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, net loft, sail loft, sounding stage, chart house, or buoy yard.

## Mechanic

Cut, dry, burn. Wrack is cut from the bank, dried on stones, and burned to kelp ash. Not salt-pan rake, not dye vat, not smokehouse cure, not mill kiln grain, not buoy drop.

## Inhabitants

- Tang (yard)
- Drift (bank)
- Ure (hearth)

## Locations

`kelp.path`, `kelp.yard`, `kelp.bank`, `kelp.stones`, `kelp.hearth`. Linked from `ashfen.causeway` and `buoy.path`.

## Outcome

`kelp_burned` — flag `kelp_burned`. Witness: `traces/marsh_kelp_burned.json`.

## Sheet / deed gates

Same scene `kelp.yard`: marshborn/hunt `know_the_wrack_tide`; letters `read_the_kelp_list`.

## Cross-effect

Set buoy (`buoy_set`) unlocks `cut_the_outer_bank` at the wrack bank. Proven by `cross_buoy_kelp` vs `cross_plain_kelp`.
