# Slice 33 uniqueness claim — Soap House

Region id: `soap_house`. Hamlet pocket. Not a reskin of harbor, stacks, mill, court, road, fever camp, namehouse, peat fold, lens ruin, ropewalk, salt pans, smokehouse, eel weir, dye works, toll ferry, windpump, oyster park, counting house, ice cellar, wreck chapel, bee skeps, mead house, cooperage, pickle house, tide forge, decoy pond, rushlight house, caulk yard, net loft, sail loft, sounding stage, chart house, buoy yard, or kelp shore.

## Mechanic

Leach, boil, cut. Ash is leached to lye, fat is boiled to a curd, cakes are cut. Not kelp-ash burning, not pickle brine, not dye vat, not mead mash.

## Inhabitants

- Soda (yard)
- Lye (leach)
- Bar (cut)

## Locations

`soap.path`, `soap.yard`, `soap.leach`, `soap.boil`, `soap.cut`. Linked from `ashfen.causeway` and `kelp.path`.

## Outcome

`soap_cut` — flag `soap_cut`. Witness: `traces/marsh_soap_cut.json`.

## Sheet / deed gates

Same scene `soap.yard`: marshborn/hunt `know_the_lye_run`; letters `read_the_soap_list`.

## Cross-effect

Burned kelp (`kelp_burned`) unlocks `charge_the_soda` at the leach tub. Proven by `cross_kelp_soap` vs `cross_plain_soap`.
