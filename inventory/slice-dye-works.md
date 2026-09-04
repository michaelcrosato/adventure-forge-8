# Slice 12 uniqueness claim — Dye Works

Region id: `dye_works`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, or eel weir.

## Mechanic

Vat and color. Charge a vat, dip cloth, hang it until the color sets. Not kiln heat, not smoke hang, not brine rake, not weir lift.

## Inhabitants

- Dyer Quill (yard)
- Fen (vats)
- Moss (loft)

## Locations

`dye.path`, `dye.yard`, `dye.vats`, `dye.loft`, `dye.store`. Linked from `ashfen.causeway` and `weir.path`.

## Outcome

`dye_struck` — flag `dye_struck`. Witness: `traces/marsh_dye_struck.json`.

## Sheet / deed gates

Same scene `dye.yard`: marshborn/hunt `know_the_reed_mordant`; letters `read_the_vat_list`.

## Cross-effect

Weir lifted (`weir_lifted`) unlocks `bind_eel_skin` at the vats. Proven by `cross_weir_dye` vs `cross_plain_dye`.
