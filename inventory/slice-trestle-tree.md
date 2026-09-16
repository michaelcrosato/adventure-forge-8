# Slice 133 uniqueness claim — Trestle-tree House

Region id: `trestle_house`. Hamlet pocket. Not a reskin of crosstree square-spread-seize, spirketting score-plane-clench, or sash tenon-rail.

## Mechanic

Score, tenon, seize. The trestle is scored, the rest is tenoned, and the bib is seized. Not score_the_spirket, not tenon_the_rail, not seize_the_bolster.

## Inhabitants

- Trestle (yard)
- Rest (rest)
- Bib (bib)

## Locations

`trs.path`, `trs.yard`, `trs.trestle`, `trs.rest`, `trs.bib`. Linked from `ashfen.causeway` and `spi.path`. Crosstree owns “Go to the hounds”; cleat owns “Go to the bolt”; dado owns “Go to the cap”.

## Outcome

`bib_seized` — flag `bib_seized`. Witness: `traces/marsh_bib_seized.json`.

## Sheet / deed gates

Same scene `trs.yard`: marshborn/hunt `know_the_trestle`; letters `read_the_trestle_list`.

## Cross-effect

Clenched spirket (`spirket_clenched`) unlocks `clench_the_trestle` at the trestle bench. Proven by `cross_spi_trs` vs `cross_plain_trs`.
