# Slice 18 uniqueness claim — Wreck Chapel

Region id: `wreck_chapel`. Ruin pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, or ice cellar.

## Mechanic

Wash and lay. A drowned token is washed, then laid on the wreck altar. Not a living bone-name restore, not ice packing, not a road beacon.

## Inhabitants

- Warden Luth (yard)
- Kade (hull)
- Efa (altar)

## Locations

`wreck.path`, `wreck.yard`, `wreck.hull`, `wreck.wash`, `wreck.altar`. Linked from `ashfen.causeway` and `ice.path`.

## Outcome

`wreck_laid` — flag `wreck_laid`. Witness: `traces/marsh_wreck_laid.json`.

## Sheet / deed gates

Same scene `wreck.yard`: marshborn/hunt `know_the_drowned_mark`; letters `read_the_wreck_list`.

## Cross-effect

Ice held (`ice_held`) unlocks `keep_the_drowned_cold` at the hull. Proven by `cross_ice_wreck` vs `cross_plain_wreck`.
