# Slice 13 uniqueness claim — Toll Ferry

Region id: `toll_ferry`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, or dye works.

## Mechanic

Fare, load, pole. A token loads the hull; poling is the only way onto the far bank. Not road weather, not weir lift, not vat color, not a dock compact.

## Inhabitants

- Ferryman Bex (yard)
- Ivo (slip)
- Ama (far landing)

## Locations

`ferry.path`, `ferry.yard`, `ferry.slip`, `ferry.boat`, `ferry.far`. Linked from `ashfen.causeway` and `dye.path`.

## Outcome

`ferry_crossed` — flag `ferry_crossed`. Witness: `traces/marsh_ferry_crossed.json`.

## Sheet / deed gates

Same scene `ferry.yard`: marshborn/hunt `know_the_channel_cut`; letters `read_the_toll_board`.

## Cross-effect

Dye struck (`dye_struck`) unlocks `show_the_dyed_fare` at the yard. Proven by `cross_dye_ferry` vs `cross_plain_ferry`.
