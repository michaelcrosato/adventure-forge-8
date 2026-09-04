# Slice 21 uniqueness claim — Cooperage

Region id: `cooperage`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, or mead house.

## Mechanic

Soak, hoop, raise. A stave is soaked, hooped, and the barrel is raised. Not hemp taut-walk, not mash-and-tap, not mill grain-debt.

## Inhabitants

- Cooper Jute (yard)
- Corm (soak)
- Bess (raise)

## Locations

`coop.path`, `coop.yard`, `coop.soak`, `coop.hoop`, `coop.raise`. Linked from `ashfen.causeway` and `mead.path`.

## Outcome

`barrel_raised` — flag `barrel_raised`. Witness: `traces/marsh_barrel_raised.json`.

## Sheet / deed gates

Same scene `coop.yard`: marshborn/hunt `know_the_stave_soak`; letters `read_the_hoop_mark`.

## Cross-effect

Mead drawn (`mead_drawn`) unlocks `mark_the_mead_cask` at the hoop. Proven by `cross_mead_coop` vs `cross_plain_coop`.
