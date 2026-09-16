# Slice 23 uniqueness claim — Tide Forge

Region id: `tide_forge`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, or pickle house.

## Mechanic

Bellows, bloom, quench. Tide wind banks the fire, a bog-iron bloom is hammered, the iron is quenched. Not kiln grain-debt heat, not stave-and-hoop raising, not pickle pack-and-lid.

## Inhabitants

- Smith Keld (yard)
- Brunt (bellows)
- Nessa (trough)

## Locations

`forge.path`, `forge.yard`, `forge.bellows`, `forge.anvil`, `forge.trough`. Linked from `ashfen.causeway` and `pickle.path`.

## Outcome

`iron_quenched` — flag `iron_quenched`. Witness: `traces/marsh_iron_quenched.json`.

## Sheet / deed gates

Same scene `forge.yard`: marshborn/hunt `know_the_bog_iron`; letters `read_the_forge_list`.

## Cross-effect

Pickle lidded (`pickle_lidded`) unlocks `brine_the_quench` at the trough. Proven by `cross_pickle_forge` vs `cross_plain_forge`.
