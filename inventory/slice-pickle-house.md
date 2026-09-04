# Slice 22 uniqueness claim — Pickle House

Region id: `pickle_house`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, or cooperage.

## Mechanic

Pack, brine, lid. Cut is packed under brine, a jar is taken, the cask is lidded. Not salt-cake raking, not fish-cure smoke, not stave-and-hoop raising.

## Inhabitants

- Keeper Rill (yard)
- Ora (tub)
- Tov (lid)

## Locations

`pickle.path`, `pickle.yard`, `pickle.tub`, `pickle.pack`, `pickle.lid`. Linked from `ashfen.causeway` and `coop.path`.

## Outcome

`pickle_lidded` — flag `pickle_lidded`. Witness: `traces/marsh_pickle_lidded.json`.

## Sheet / deed gates

Same scene `pickle.yard`: marshborn/hunt `know_the_pickle_cut`; letters `read_the_pickle_list`.

## Cross-effect

Barrel raised (`barrel_raised`) unlocks `hoop_the_pickle` at the lid. Proven by `cross_coop_pickle` vs `cross_plain_pickle`.
