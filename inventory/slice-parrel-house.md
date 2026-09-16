# Slice 111 uniqueness claim — Parrel House

Region id: `parrel_house`. Hamlet pocket. Not a reskin of deadeye loft score-reeve-seize, block loft score-strop, or fid seize-eye.

## Mechanic

Groove, thread, truss. The truck is grooved, the rib is threaded, and the parrel is trussed. Not score_the_deadeye, not reeve_the_strop, not seize_the_lanyard.

## Inhabitants

- Truck (yard)
- Rib (rib)
- Truss (truss)

## Locations

`par.path`, `par.yard`, `par.truck`, `par.rib`, `par.truss`. Linked from `ashfen.causeway` and `deye.path`.

## Outcome

`parrel_trussed` — flag `parrel_trussed`. Witness: `traces/marsh_parrel_trussed.json`.

## Sheet / deed gates

Same scene `par.yard`: marshborn/hunt `know_the_truck`; letters `read_the_parrel_list`.

## Cross-effect

Seized lanyard (`lanyard_seized`) unlocks `seize_the_truck` at the truck bench. Proven by `cross_deye_par` vs `cross_plain_par`.
