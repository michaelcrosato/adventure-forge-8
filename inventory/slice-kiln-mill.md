# Slice 1 uniqueness claim — Kiln Mill

Region id: `kiln_mill`. Not a reskin of Saltfen (law/tides/papers) or Hollow Stacks (climb/collapse).

## Mechanic

Kiln heat is authored state (`kiln_lit` / `kiln_hot`). Grain-debt is a ledger the miller will not drop until a pact is fired in the hot kiln, sworn from the ledger, or cited from the dock compact.

## Inhabitants

- Brann the miller (yard): debt, pact, dock rates
- Pell the kiln-girl (kiln): heat, damper
- Sila the loft clerk (loft): grain sacks

## Locations

`mill.lane`, `mill.yard`, `mill.kiln`, `mill.loft`, `mill.sluice`. Linked from `ashfen.causeway`.

## Outcome

`kiln_pact` — flag `kiln_pact_sealed`. Witness: `traces/marsh_kiln_pact.json`.

## Sheet / deed gates

Same scene `mill.yard`: marshborn `offer_reed_grain`; letters `read_debt_ledger`; city papers `show_mill_papers`.

## Cross-effect

Harbor `compact_restored` unlocks `cite_dock_compact` at `mill.yard` and changes miller speech. Proven by `cross_compact_mill` vs `cross_plain_mill`.
