# Slice 2 uniqueness claim — Reed Court

Region id: `reed_court`. Not a reskin of Saltfen (dock papers/tides), Hollow Stacks (climb), or Kiln Mill (heat/debt).

## Mechanic

Spoken law. Standing is earned, a witness must be heard, then a sentence can pass. No kiln heat, no climbing, no grain sacks.

## Inhabitants

- Bailiff Kesh (gate)
- Magistrate Orin (hall)
- Accused Tam (cell)
- Clerk Nia (archive)

## Locations

`court.gate`, `court.yard`, `court.hall`, `court.cell`, `court.archive`. Linked from `ashfen.causeway` and `mill.lane`.

## Outcome

`reed_sentence` — flag `reed_sentence_passed`. Witness: `traces/marsh_reed_sentence.json`.

## Sheet / deed gates

Same scene `court.hall`: marshborn/cant `speak_reed_custom`; cityward/court tongue `cite_city_law`.

## Cross-effect

Kiln pact (`kiln_pact_sealed`) unlocks `name_mill_pact` in the hall. Proven by `cross_kiln_court` vs `cross_plain_court`.
