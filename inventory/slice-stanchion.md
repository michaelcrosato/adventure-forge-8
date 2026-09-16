# Slice 141 uniqueness claim — Stanchion House

Region id: `stanchion_house`. Hamlet pocket. Not a reskin of pointer bevel-bed-dump, stair wedge-riser, or binnacle true-hood.

## Mechanic

True, wedge, spike. The stanchion is trued, the prop is wedged, and the foot is spiked. Not true_the_hood, not wedge_the_riser, not spike_the_pointer. Actor Plumb already exists, so the yard inhabitant is Stanchion.

## Inhabitants

- Stanchion (yard)
- Prop (prop)
- Foot (foot)

## Locations

`stn.path`, `stn.yard`, `stn.true`, `stn.prop`, `stn.foot`. Linked from `ashfen.causeway` and `ptr.path`. Path label is “Go to the stanchions” so thatch “Go to the stand” is not a causeway substring. Stem owns “Go to the forefoot” (not a substring of “Go to the foot”). Dado owns “Go to the cap”.

## Outcome

`foot_spiked` — flag `foot_spiked`. Witness: `traces/marsh_foot_spiked.json`.

## Sheet / deed gates

Same scene `stn.yard`: marshborn/hunt `know_the_stanchion`; letters `read_the_stanchion_list`.

## Cross-effect

Dumped compound (`compound_dumped`) unlocks `dump_the_stanchion` at the true bench. Proven by `cross_ptr_stn` vs `cross_plain_stn`.
