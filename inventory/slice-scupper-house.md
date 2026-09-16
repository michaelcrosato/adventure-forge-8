# Slice 117 uniqueness claim — Scupper House

Region id: `scupper_house`. Hamlet pocket. Not a reskin of transom scribe-fit-spike, pickle lid, or brick plug.

## Mechanic

Broach, chase, plug. The scupper is broached, the drain is chased, and the mouth is plugged. Not spike_the_stern, not lid_the_pickle, not plug_the_brick.

## Inhabitants

- Broach (yard)
- Drain (drain)
- Mouth (mouth)

## Locations

`scup.path`, `scup.yard`, `scup.broach`, `scup.drain`, `scup.mouth`. Linked from `ashfen.causeway` and `tran.path`. Actor Plug already exists (brick), so the outcome inhabitant is Mouth.

## Outcome

`mouth_plugged` — flag `mouth_plugged`. Witness: `traces/marsh_mouth_plugged.json`.

## Sheet / deed gates

Same scene `scup.yard`: marshborn/hunt `know_the_broach`; letters `read_the_scupper_list`.

## Cross-effect

Spiked stern (`stern_spiked`) unlocks `spike_the_broach` at the broach bench. Proven by `cross_tran_scup` vs `cross_plain_scup`.
