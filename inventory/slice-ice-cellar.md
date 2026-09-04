# Slice 17 uniqueness claim — Ice Cellar

Region id: `ice_cellar`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, or counting house.

## Mechanic

Pack and hold. Ice is packed in straw, then the door is barred so the cold stays. Not kiln heat, not smoke tend, not tally seal, not peat share.

## Inhabitants

- Packer Yul (yard)
- Saff (pit)
- Kest (door)

## Locations

`ice.path`, `ice.yard`, `ice.pit`, `ice.hold`, `ice.door`. Linked from `ashfen.causeway` and `count.path`.

## Outcome

`ice_held` — flag `ice_held`. Witness: `traces/marsh_ice_held.json`.

## Sheet / deed gates

Same scene `ice.yard`: marshborn/hunt `know_the_ice_cut`; letters `read_the_cold_mark`.

## Cross-effect

Tally closed (`tally_closed`) unlocks `cite_the_ice_right` at the yard. Proven by `cross_count_ice` vs `cross_plain_ice`.
