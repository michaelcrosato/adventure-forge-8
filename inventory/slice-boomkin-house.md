# Slice 125 uniqueness claim — Boomkin House

Region id: `boomkin_house`. Hamlet pocket. Not a reskin of davit sweep-band-ship, gammoning woold-ride-frap, or deadeye seize-lanyard.

## Mechanic

Steeve, bee, seize. The boomkin is steeved, the iron is beed, and the guy is seized. Not ship_the_davit, not seize_the_lanyard, not seize_the_bolster.

## Inhabitants

- Steeve (yard)
- Bee (bee)
- Guy (guy)

## Locations

`boom.path`, `boom.yard`, `boom.steeve`, `boom.bee`, `boom.guy`. Linked from `ashfen.causeway` and `dav.path`. Casing owns “Go to the tack” and actor Tack. Wash owns “Go to the beetle” internally.

## Outcome

`guy_seized` — flag `guy_seized`. Witness: `traces/marsh_guy_seized.json`.

## Sheet / deed gates

Same scene `boom.yard`: marshborn/hunt `know_the_steeve`; letters `read_the_boomkin_list`.

## Cross-effect

Shipped davit (`davit_shipped`) unlocks `ship_the_steeve` at the steeve bench. Proven by `cross_dav_boom` vs `cross_plain_boom`.
