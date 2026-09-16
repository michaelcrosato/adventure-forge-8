# Slice 130 uniqueness claim — Tabernacle House

Region id: `tabernacle_house`. Hamlet pocket. Not a reskin of carling notch-lodge-spike, hinge pintle-gudgeon, or hawse bore-pay.

## Mechanic

Score, mortise, pin. The tabernacle is scored, the gate is mortised, and the keeper is pinned. Not score_the_knight, not mortise_the_jaw, not pin_the_sash.

## Inhabitants

- Tabernacle (yard)
- Gate (gate)
- Keeper (keeper)

## Locations

`tab.path`, `tab.yard`, `tab.socket`, `tab.gate`, `tab.keeper`. Linked from `ashfen.causeway` and `carl.path`. Hinge owns “Go to the pintle”; hawse owns “Go to the bore”; sash owns “Go to the pin”.

## Outcome

`keeper_pinned` — flag `keeper_pinned`. Witness: `traces/marsh_keeper_pinned.json`.

## Sheet / deed gates

Same scene `tab.yard`: marshborn/hunt `know_the_tabernacle`; letters `read_the_tabernacle_list`.

## Cross-effect

Spiked carling (`carling_spiked`) unlocks `spike_the_socket` at the socket bench. Proven by `cross_carl_tab` vs `cross_plain_tab`.
