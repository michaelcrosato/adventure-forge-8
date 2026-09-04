# Slice 4 uniqueness claim — Fever Camp

Region id: `fever_camp`. Not a reskin of harbor, stacks, mill, court, or road.

## Mechanic

Isolation and medicine. Herb or written order lets you brew a broth; the ward is cleared only when the sick take it. No kiln heat-debt, no climb, no court standing, no weather berm.

## Inhabitants

- Nurse Joss (yard)
- Ren the sick (ward)
- Still-hand Oat (still)

## Locations

`camp.gate`, `camp.yard`, `camp.ward`, `camp.still`, `camp.pits`. Linked from `ashfen.causeway` and `road.ford`.

## Outcome

`fever_broken` — flag `fever_broken`. Witness: `traces/marsh_fever_broken.json`.

## Sheet / deed gates

Same scene `camp.yard`: marshborn/hunt `cut_reed_herb`; letters `read_isolation_order`.

## Cross-effect

Road beacon (`beacon_lit`) unlocks `hail_clean_boat` at the camp gate. Proven by `cross_beacon_camp` vs `cross_plain_camp`.
