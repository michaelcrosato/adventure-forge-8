# Slice 118 uniqueness claim — Binnacle House

Region id: `binnacle_house`. Hamlet pocket. Not a reskin of scupper broach-chase-plug, horn lanterns, or paint oil.

## Mechanic

True, fill, lock. The hood is trued, the lamp is filled, and the card is locked. Not plug_the_mouth, not hang_the_lantern, not mix_the_oil.

## Inhabitants

- Hood (yard)
- Lamp (lamp)
- Card (card)

## Locations

`binn.path`, `binn.yard`, `binn.hood`, `binn.lamp`, `binn.card`. Linked from `ashfen.causeway` and `scup.path`. Horn owns “Go to the lanterns”; paint owns “Go to the oil”.

## Outcome

`card_locked` — flag `card_locked`. Witness: `traces/marsh_card_locked.json`.

## Sheet / deed gates

Same scene `binn.yard`: marshborn/hunt `know_the_hood`; letters `read_the_binnacle_list`.

## Cross-effect

Plugged mouth (`mouth_plugged`) unlocks `plug_the_hood` at the hood bench. Proven by `cross_scup_binn` vs `cross_plain_binn`.
