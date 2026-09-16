# Adventure Forge 8 — Orchestrator plan

Status: executing. This file is the live constitution for the repository.
Supersedes the four original briefs (now in `archive/original-briefs/`).
On conflict, the locked parts below win. They are taken from the x46 kernel brief.

**Freedom in design. Honesty in verification. The model never is the world.**
**The orchestrator owns the factory. The bar owns the truth. The game is the score.**
**Plain words. Real verbs. One world. The sheet you brought changes the room you enter.**

---

## Locked honesty invariants

These do not move. A better game that violates them is a different product.

### I1. Pure step

```text
step(state, action, content, seed-cursor) → state'
```

- No wall clock, network, or ambient RNG inside the transition.
- All game randomness is an explicit serializable cursor derived from a seed.
- Same content + same seed + same action sequence + same character sheet ⇒ identical observable run.
- A canonical fingerprint is the definition of “same run.”

### I2. Content is data; rules are code

World, inhabitants, reactions, items, dialogue, and outcomes are data the engine interprets.

- Closed effect/condition vocabulary. New verbs ship with a checker in the same change.
- A model may draft or patch data. A model may not invent a one-off side effect that only exists in prose.
- Illegal actions are rejected by code. The model is never the physics.

### I3. Enumerated legal moves

Each observation exposes legal actions with stable identities.

- Choosing an action is the only way the world advances.
- Surfaces do not reimplement legality.
- Free text is sugar that maps onto a legal id. Failed mapping does not move the world.

### I4. Claims are proofs

For every shipped region or outcome:

- A primary walkthrough replays to the advertised success predicate.
- Every other advertised distinct outcome has its own replayable witness.
- References resolve.
- Character-conditioned reactions have a witness pair: same scene, two sheets, different legal outcomes or world reactions, both replayable.
- The acceptor is mechanical.

### I5. `verify` is the bar

One machine command, no LLM required:

1. The I1 property.
2. I4 proofs for every shipped slice.
3. A non-LLM crawler on the real engine (crash, empty legal-set, bounds, impurity).
4. Load-bearing unit/type checks.
5. Plain-language and observation-budget tests (G2, G5, I8).

A change that fails `verify` did not land. The orchestrator may replace the *implementation* of the bar with a stricter or faster one. It may not delete the *job* of the bar.

### I6. Play / build firewall

| Loop | Sees source / solutions | Changes the tree | Must produce |
|---|---|---|---|
| Play | No | No | Replay-verified session + structured findings |
| Build | Yes | Yes, as the orchestrator allows | Changes that leave `verify` green |

Unreplayable reports are discarded. Builders’ knowledge does not ride the player path.

### I7. Autonomy with a non-LLM driver

Builders and the orchestrator choose what to build and how the factory runs. They may not delete proofs to go green, hide rules in prose, let the player surface invent actions, or commit a trace the engine cannot replay.

### I8. Agent-playable on a budget

A competent agent takes a full turn from one observation. Observation size is bounded and tested. A large legal set stays playable by grouping, paging, or filter — never by silent truncation, never by dumping an unreadable menu.

---

## Locked game-product requirements

### G1. One world

One contiguous world. No second campaign, no pocket universe that is a different game. Travel, towns, dungeons, and talk are regions of the same state.

### G2. Plain speech

UI labels, menus, speech, and description use simple, short, straight language. Flavor is allowed. Fog is not. Testable with length budgets on shipped strings and on official-walkthrough observations.

### G3. A character the world can see

The protagonist is customizable on real axes (origin, body, skill, creed, mark, tongue). The world queries the sheet as data:

- Legal actions may appear, vanish, or change cost by sheet.
- NPC stance, prices, access, and offered verbs may change by sheet and by deeds.
- Two sheets through the same opening must produce a proven divergence (I4).

Cosmetic-only customization does not satisfy G3.

### G4. Scope north star

Target shape: geographic / travel scale on the order of a Skyrim-sized playable map; per-area interaction depth on the order of a Baldur’s Gate 3 locale.

Honest scale:

- A node with no unique verbs, no unique inhabitants, and no unique consequences does not count.
- Procedural fill is substrate. Authored depth is what the rubric scores.
- The factory ships the world in slices. Each shipped slice meets I4. Unshipped wilderness is not a claim.

Empty miles are a disqualification. This scored revision ships a **credible unique-area slice** plus this executing G4 plan. Full unique-location count is the standing north star after the bar is green, not a license to fail the slice, and not a license to pass with wallpaper.

### G5. Action first

Observations lead with situation + legal verbs. Prose exists to make the next verb intelligible, then stops. A scene that can only be enjoyed by reading a page and clicking Continue is a defect.

### G6. No artificial scene cap

If a verb is implemented for that state, it may be offered. There is no design rule “a scene may have at most N choices.”

Allowed bounds: the closed DSL, the observation budget, legality. Unlimited means no ceiling on programmed options. It does not mean the model may invent options at play time.

---

## Orchestrator authority

The orchestrator agent owns this repository: priority, delegation, integration, workflow health, and whether a change served the game.

Process is fluid. The orchestrator may rewrite scripts, queues, prompts, branching, and factory internals as often as needed.

Authority stops at the invariants. The orchestrator may not: make the model the physics; drop the firewall; ship unreplayable outcomes; count empty map as G4; replace G2 with purple prose; call a cosmetic title-picker G3; edit `verify` to ignore a failing proof.

Success is both constraint satisfaction and game quality under those constraints. Process volume is not success.

---

## First scored slice (executing now)

World: **Ashfen Coast** — one drowned river mouth.

| Region | Mechanic (not a reskin) | Role |
|---|---|---|
| Saltfen Harbor | Law, papers, prices, tides, dock compact | Social / institutional |
| Hollow Stacks | Vertical climb, guyline, collapse, relic | Spatial / risk |
| Kiln Mill | Heat states, craft damper, grain-debt pact | Craft / debt |
| Reed Court | Standing, witness, sentence | Law |
| Drowned Road | Turn weather, encounters, beacon | Travel |
| Fever Camp | Isolation, herb/recipe broth, ward | Medicine |
| Namehouse | Names, rites, restored bone-name | Ruin |
| Peat Fold | Safe cut, share board, flood risk | Hamlet |
| Lens Ruin | Low sun, shard, channel mark | Ruin |
| Ropewalk | Twist, taut walk, hemp hank | Hamlet |
| Salt Pans | Brine, rake, weigh | Hamlet |
| Smokehouse | Hang, tend smoke, salt-cure | Hamlet |
| Eel Weir | Set baskets, lift catch | Hamlet |
| Dye Works | Charge vat, dip, hang color | Hamlet |
| Toll Ferry | Fare token, load, pole to far bank | Travel |
| Windpump | Set vanes, crank, hold the flats | Craft |
| Oyster Park | Seed spat, cull beds | Hamlet |
| Counting House | Mark tally, seal the day | Social / institutional |
| Ice Cellar | Pack ice, hold cold, bar door | Craft |
| Wreck Chapel | Wash drowned token, lay on altar | Ruin |
| Bee Skeps | Smoke hive, take comb, set skep | Hamlet |
| Mead House | Mash must, bung, tap cask | Hamlet |
| Cooperage | Soak stave, hoop, raise barrel | Hamlet |
| Pickle House | Pack brine, lid the pickle cask | Hamlet |
| Tide Forge | Bank bellows, hammer bloom, quench iron | Craft |
| Decoy Pond | Lay pipes, drive ducks, bag fowl | Hunt |
| Rushlight House | Peel pith, tallow, bind lights | Craft |
| Caulk Yard | Pick oakum, melt pitch, caulk seam | Craft |
| Net Loft | Rig mesh, mend, tar the net | Hamlet |
| Sail Loft | Cut canvas, stitch, hoist sail | Craft |
| Sounding Stage | Coil line, mark fathom, cast lead | Travel |
| Chart House | Lay ruler, ink rutter, seal book | Social / institutional |
| Buoy Yard | Stuff cage, lash spar, drop buoy | Travel |
| Kelp Shore | Cut wrack, dry stones, burn kelp ash | Hamlet |
| Soap House | Leach ash, boil soap, cut cakes | Craft |
| Fulling Mill | Wet web, walk stocks, hang tenters | Craft |
| Charcoal Clamp | Cut coppice, stack clamp, draw coal | Craft |
| Lime Kiln | Break shell, charge fire, slake lime | Craft |
| Mason Yard | Mix mortar, lay course, point joint | Craft |
| Thatch Croft | Cut thatch, bind yealm, set roof | Hamlet |
| Rain Cistern | Hang gutter, set tun, dip pail | Craft |
| Wash House | Soak cloth, beat wash, hang line | Hamlet |

Character axes the world queries: origin, body, skill, creed, mark, tongue.

Authored outcomes:

1. `harbor_compact` — the dock compact is restored.
2. `stack_relic` — the ash relic is taken.
3. `kiln_pact` — the mill grain-debt is sealed in the kiln.
4. `reed_sentence` — the reed court passes sentence.
5. `road_beacon` — the drowned-road beacon is lit.
6. `fever_broken` — the camp fever is broken.
7. `name_restored` — the stolen bone-name is set back on the wall.
8. `fold_held` — the peat share is set even.
9. `lens_set` — the lens shard marks the channel.
10. `rope_walked` — the hemp hank is walked taut.
11. `salt_raked` — a salt cake is raked and weighed.
12. `smoke_cured` — wet fish hangs, takes smoke, and comes down cured.
13. `weir_lifted` — baskets are set and the eel catch is lifted.
14. `dye_struck` — cloth takes vat color and hangs dry.
15. `ferry_crossed` — a loaded hull is poled to the far bank.
16. `flats_drained` — vanes are set, the pump is cranked, and the sump holds.
17. `oyster_culled` — spat is seeded and the beds are culled.
18. `tally_closed` — the day's tally is marked and sealed.
19. `ice_held` — ice is packed and the door is barred.
20. `wreck_laid` — a drowned token is washed and laid on the wreck altar.
21. `hive_kept` — the hive is smoked, comb taken, and the skep set.
22. `mead_drawn` — the must is mashed, bunged, and the cask tapped.
23. `barrel_raised` — a stave is soaked, hooped, and the barrel raised.
24. `pickle_lidded` — cut is packed under brine and the pickle cask is lidded.
25. `iron_quenched` — bellows are banked, the bloom is hammered, and the iron is quenched.
26. `fowl_taken` — pipes are laid, ducks are driven, and the fowl is bagged.
27. `lights_bound` — rush is peeled to pith and bound into lights.
28. `seam_caulked` — oakum is picked, pitch is melted, and the hull seam is caulked.
29. `net_tarred` — mesh is rigged, mended, and tarred.
30. `sail_hoisted` — canvas is cut, the sail is stitched, and the spar is hoisted.
31. `lead_cast` — the line is coiled, fathoms are marked, and the lead is cast.
32. `rutter_sealed` — a ruler is laid, the rutter is inked, and the book is sealed.
33. `buoy_set` — a cage is stuffed, the spar is lashed, and the buoy is dropped.
34. `kelp_burned` — wrack is cut, dried on the stones, and burned to ash.
35. `soap_cut` — ash is leached, soap is boiled, and the cakes are cut.
36. `cloth_fulled` — a web is wetted, walked in the stocks, and hung on tenters.
37. `coal_drawn` — coppice is cut, stacked in a clamp, and drawn as coal.
38. `lime_slaked` — shell is broken, charged on the fire, and slaked with water.
39. `joint_pointed` — mortar is mixed, a course is laid, and the joint is pointed.
40. `roof_set` — thatch is cut, bound into a yealm, and set on the ridge.
41. `cistern_filled` — a gutter is hung, the tun is set, and a pail is dipped.
42. `wash_hung` — cloth is soaked, beaten on the beetle, and hung on the line.
43. `paper_laid` — rag is stamped, couched on a deckle, and packed on the post.
44. `frail_woven` — withy is cut, braked, and woven into a frail.
45. `loaf_drawn` — leaven is set, the oven is heated, and the batch is drawn.
46. `wheel_salted` — curd is set, wrapped, and the cheese wheel is salted.
47. `web_sheared` — warp is beamed, the shuttle is thrown, and the web is sheared.
48. `lantern_hung` — horn is scraped, set as a pane, and hung as a lantern.
49. `nib_cut` — oak gall is crushed, mixed to ink, and a nib is cut.
50. `heel_pegged` — a sole is lasted, the upper is awled, and the heel is pegged.
51. `keeve_bunged` — fruit is milled, pomace is wrapped, and the keeve is bunged.
52. `mustard_potted` — seed is milled, wetted to paste, and potted.
53. `sausage_linked` — forcemeat is chopped, the skin is filled, and the links are tied.
54. `pie_crimped` — crust is rolled, the pie is filled, and the lid is crimped.
55. `jam_jarred` — pulp is boiled, foam is skimmed, and the jam is jarred.
56. `crock_glazed` — clay is thrown, biscuit-fired, and the crock is glazed.
57. `hide_tanned` — hide is fleshed, bated, and tanned with oak bark.
58. `flax_spun` — flax is retted, heckled to tow, and spun to line.
59. `nail_pointed` — rod is snipped, the nail is headed, and the shank is pointed.
60. `tyre_set` — the hub is dished, spokes are set, and the felloe is tyred.
61. `malt_oasted` — barley is steeped, the piece is turned, and malt is oasted.
62. `gyle_racked` — grist is charged, the wort is hopped, and the gyle is racked.
63. `cruet_corked` — mother is pitched, ale is soured, and the cruet is corked.

Witness pair: Saltfen Market, `marsh_scout` vs `city_oath`, different legal verbs, both replayable.

Large legal set: Saltfen salvage yard, 100+ programmed take-actions, no engine cap, player surface pages/groups.

Surfaces:

- Player: `python -m adventure_forge play` (plain language, mapper-or-no-op).
- Web: Vercel `/` and `/play` wrap the same `PlaySession` (not a second physics).
- Builder: repository + `verify`.
- Bar: `python -m adventure_forge verify` (also `scripts/verify`).

Capabilities on this slice: seeded new game, resume, trace record, trace replay, I1, I4, crawler, language/budget, unit checks, orchestrator charter, one delegation, one process rewrite, one flywheel turn, one rejected unreplayable report.

---

## G4 executing plan (after the bar is green)

Each new slice must add unique verbs, inhabitants, and consequences. Wallpaper cells do not ship.

1. **Slice 0:** Saltfen + Stacks, two outcomes, sheet divergence, salvage stress scene.
2. **Slice 1:** Kiln Mill — heat, craft, grain-debt. Cross-effect: compact restored unlocks dock rates at the mill yard.
3. **Slice 2:** Reed Court — standing, witness, sentence. Cross-effect: kiln pact unlocks mill proof in the hall.
4. **Slice 3:** Drowned Road — weather-as-turn, encounters, beacon. Cross-effect: reed sentence unlocks road standing.
5. **Slice 4:** Fever Camp — isolation and medicine. Cross-effect: road beacon unlocks a clean boat at the gate.
6. **Slice 5:** Namehouse ruin — names and rites. Cross-effect: fever broken unlocks filing Ren as living.
7. **Slice 6:** Peat Fold hamlet — safe cut and share. Cross-effect: restored name unlocks kin standing on the green.
8. **Slice 7:** Lens Ruin — light path and shard. Cross-effect: fold peat credit buys lead.
9. **Slice 8:** Ropewalk — twist and taut walk. Cross-effect: set lens unlocks channel sight on the floor.
10. **Slice 9:** Salt Pans — brine, rake, weigh. Cross-effect: walked rope unlocks a rake line on the beds.
11. **Slice 10:** Smokehouse — hang, tend smoke, salt-cure. Cross-effect: raked salt unlocks a brine cure on the racks.
12. **Slice 11:** Eel Weir — set baskets, lift catch. Cross-effect: cured smoke unlocks bait on the stakes.
13. **Slice 12:** Dye Works — charge vat, dip, hang color. Cross-effect: lifted weir unlocks eel-skin mordant on the vats.
14. **Slice 13:** Toll Ferry — fare token, load, pole to far bank. Cross-effect: struck dye unlocks a dyed fare at the yard.
15. **Slice 14:** Windpump — set vanes, crank, hold the flats. Cross-effect: ferry crossed unlocks a sail brace on the tower.
16. **Slice 15:** Oyster Park — seed spat, cull beds. Cross-effect: drained flats unlock dry-bed work.
17. **Slice 16:** Counting House — mark tally, seal the day. Cross-effect: culled oysters unlock a lot credit at the desk.
18. **Slice 17:** Ice Cellar — pack ice, hold cold, bar door. Cross-effect: closed tally unlocks an ice right at the yard.
19. **Slice 18:** Wreck Chapel — wash drowned token, lay on altar. Cross-effect: held ice unlocks keeping the drowned cold.
20. **Slice 19:** Bee Skeps — smoke hive, take comb, set skep. Cross-effect: wreck laid unlocks a drowned ward on the skeps.
21. **Slice 20:** Mead House — mash must, bung, tap cask. Cross-effect: hive kept unlocks true comb pitch on the mash.
22. **Slice 21:** Cooperage — soak stave, hoop, raise barrel. Cross-effect: mead drawn unlocks a mead-cask mark on the hoop.
23. **Slice 22:** Pickle House — pack brine, lid the pickle cask. Cross-effect: barrel raised unlocks a hoop on the pickle lid.
24. **Slice 23:** Tide Forge — bank bellows, hammer bloom, quench iron. Cross-effect: pickle lidded unlocks a brine quench at the trough.
25. **Slice 24:** Decoy Pond — lay pipes, drive ducks, bag fowl. Cross-effect: iron quenched unlocks a taking hook in the tunnel.
26. **Slice 25:** Rushlight House — peel pith, tallow, bind lights. Cross-effect: fowl taken unlocks fowl tallow at the bind.
27. **Slice 26:** Caulk Yard — pick oakum, melt pitch, caulk seam. Cross-effect: lights bound unlocks a rushlight on the dark seam.
28. **Slice 27:** Net Loft — rig mesh, mend, tar the net. Cross-effect: seam caulked unlocks hull pitch on the mesh.
29. **Slice 28:** Sail Loft — cut canvas, stitch, hoist sail. Cross-effect: net tarred unlocks tarred twine on the hoist.
30. **Slice 29:** Sounding Stage — coil line, mark fathom, cast lead. Cross-effect: sail hoisted unlocks sounding under way.
31. **Slice 30:** Chart House — lay ruler, ink rutter, seal book. Cross-effect: lead cast unlocks a fathom prick on the chart.
32. **Slice 31:** Buoy Yard — stuff cage, lash spar, drop buoy. Cross-effect: sealed rutter unlocks placing the buoy by the book.
33. **Slice 32:** Kelp Shore — cut wrack, dry stones, burn kelp ash. Cross-effect: set buoy unlocks the outer wrack bank.
34. **Slice 33:** Soap House — leach ash, boil soap, cut cakes. Cross-effect: burned kelp unlocks soda charge on the leach.
35. **Slice 34:** Fulling Mill — wet web, walk stocks, hang tenters. Cross-effect: cut soap unlocks soaping the web.
36. **Slice 35:** Charcoal Clamp — cut coppice, stack clamp, draw coal. Cross-effect: fulled cloth unlocks covering the clamp.
37. **Slice 36:** Lime Kiln — break shell, charge fire, slake lime. Cross-effect: drawn coal unlocks firing the charge.
38. **Slice 37:** Mason Yard — mix mortar, lay course, point joint. Cross-effect: slaked lime unlocks tempering the mix.
39. **Slice 38:** Thatch Croft — cut thatch, bind yealm, set roof. Cross-effect: pointed wall unlocks setting the roof on stone.
40. **Slice 39:** Rain Cistern — hang gutter, set tun, dip pail. Cross-effect: set roof unlocks hanging the gutter under the thatch.
41. **Slice 40:** Wash House — soak cloth, beat wash, hang line. Cross-effect: filled cistern unlocks filling the wash pan.
42. **Slice 41:** Rag Mill — stamp rag, couch sheet, pack post. Cross-effect: hung wash unlocks sorting white rags at the stamp.
43. **Slice 42:** Osier Holt — cut holt, brake rod, weave frail. Cross-effect: laid paper unlocks wrapping the holt.
44. **Slice 43:** Bakehouse — set leaven, heat oven, draw batch. Cross-effect: woven frail unlocks proofing the sponge.
45. **Slice 44:** Dairy — set curd, wrap curd, salt wheel. Cross-effect: drawn loaf unlocks scalding the milk.
46. **Slice 45:** Loom Shed — warp beam, throw shuttle, shear web. Cross-effect: salted wheel unlocks wrapping the warp.
47. **Slice 46:** Horn Lantern — scrape horn, set pane, hang lantern. Cross-effect: sheared web unlocks wicking the horn.
48. **Slice 47:** Gall House — crush gall, mix ink, cut nib. Cross-effect: hung lantern unlocks lighting the crush.
49. **Slice 48:** Cobble Shop — last sole, awl upper, peg heel. Cross-effect: cut nib unlocks marking the last.
50. **Slice 49:** Cider House — mill fruit, wrap pomace, bung keeve. Cross-effect: pegged heel unlocks leathering the hopper.
51. **Slice 50:** Mustard Mill — mill seed, wet paste, pot mustard. Cross-effect: bunged cider unlocks cidering the quern.
52. **Slice 51:** Sausage House — chop forcemeat, fill skin, tie links. Cross-effect: potted mustard unlocks seasoning the chop.
53. **Slice 52:** Pie House — roll crust, fill pie, crimp lid. Cross-effect: linked sausage unlocks larding the crust.
54. **Slice 53:** Jam House — boil pulp, skim foam, jar jam. Cross-effect: crimped pie unlocks glazing the pulp.
55. **Slice 54:** Crock Yard — throw clay, fire biscuit, glaze crock. Cross-effect: jarred jam unlocks fluxing the clay.
56. **Slice 55:** Tannery — flesh hide, bate skin, tan hide. Cross-effect: glazed crock unlocks rinsing the hide.
57. **Slice 56:** Flax House — ret flax, heckle tow, spin line. Cross-effect: tanned hide unlocks gloving the rett.
58. **Slice 57:** Nailery — snip rod, head nail, point shank. Cross-effect: spun flax unlocks wrapping the snip grip.
59. **Slice 58:** Wheelwright — dish hub, set spoke, tyre felloe. Cross-effect: pointed nails unlock boxing the hub.
60. **Slice 59:** Malt House — steep barley, turn piece, oast malt. Cross-effect: tyred wain unlocks filling the steep.
61. **Slice 60:** Brew House — charge grist, hop wort, rack gyle. Cross-effect: oasted malt unlocks charging the hopper.
62. **Slice 61:** Vinegar House — pitch mother, sour ale, cork cruet. Cross-effect: racked gyle unlocks pitching ale into the mother.
63. **Slice 62:** Glue House — trim paring, seethe size, cake glue. Cross-effect: corked vinegar unlocks acetting the paring.
64. **Slice 63:** Bindery — gather quire, sew band, nip board. Cross-effect: caked glue unlocks sizing the quire.
65. **Slice 64:** Gilder's Loft — bole ground, lay leaf, burnish plate. Cross-effect: bound book unlocks setting the bole.
66. **Slice 65:** Jeweler — beat foil, seat gem, close collet. Cross-effect: burnished plate unlocks gilting the foil.
67. **Slice 66:** Glazier — score quarry, groze edge, came pane. Cross-effect: closed collet unlocks gemming the score.
68. **Slice 67:** Sash House — rebate stile, tenon rail, pin sash. Cross-effect: camed pane unlocks setting the rebate.
69. **Slice 68:** Putty House — whip putty, knife bed, dust light. Cross-effect: pinned sash unlocks bedding the frame.
70. **Slice 69:** Paint House — mull colour, mix oil, brush coat. Cross-effect: dusted light unlocks priming the coat.
71. **Slice 70:** Varnish House — cook resin, strain gum, flow coat. Cross-effect: brushed coat unlocks priming the gum.
72. **Slice 71:** Latch House — file keep, fit catch, throw latch. Cross-effect: flowed varnish unlocks setting the keep.
73. **Slice 72:** Hinge House — form knuckle, drift pintle, ship gudgeon. Cross-effect: thrown latch unlocks setting the knuckle.
74. **Slice 73:** Stay House — slot bar, rivet arm, peg stay. Cross-effect: shipped gudgeon unlocks hinging the slot.
75. **Slice 74:** Sill House — bed sill, kerf drip, seat stool. Cross-effect: stayed casement unlocks setting the sill.
76. **Slice 75:** Casing House — mitre head, scribe jamb, tack return. Cross-effect: seated stool unlocks setting the mitre.
77. **Slice 76:** Skirting House — cope inside, plane base, fix plinth. Cross-effect: tacked casing unlocks setting the cope.
78. **Slice 77:** Dado House — plough dado, house panel, cap rail. Cross-effect: fixed plinth unlocks setting the dado.
79. **Slice 78:** Picture Rail — snap line, plug brick, spring mould. Cross-effect: capped dado unlocks setting the chalk.
80. **Slice 79:** Cornice House — run cove, key scratch, float cornice. Cross-effect: sprung rail unlocks setting the cove.
81. **Slice 80:** Stair House — gauge string, saw housing, wedge riser. Cross-effect: floated cornice unlocks setting the string.
82. **Slice 81:** Newel House — turn blank, mortise newel, dowel finial. Cross-effect: wedged riser unlocks setting the blank.
83. **Slice 82:** Handrail House — stick mould, scarf joint, wreath ramp. Cross-effect: dowelled finial unlocks setting the stick.
84. **Slice 83:** Baluster House — rip square, flute shaft, shoulder neck. Cross-effect: wreathed ramp unlocks setting the square.
85. **Slice 84:** Tread House — mark going, nosing edge, return end. Cross-effect: shouldered neck unlocks setting the going.
86. **Slice 85:** Floorboard House — shoot edge, tongue groove, secret nail. Cross-effect: returned end unlocks setting the shot.
87. **Slice 86:** Joist House — space joist, notch trimmer, crown camber. Cross-effect: secreted nail unlocks boarding the span.
88. **Slice 87:** Lath House — rive lath, prick bay, hair coat. Cross-effect: crowned camber unlocks setting the rive.
89. **Slice 88:** Chimney House — bed flag, set hob, lime breast. Cross-effect: haired coat unlocks setting the flag.
90. **Slice 89:** Mantel House — bed lintel, set corbel, pin mantel. Cross-effect: limed breast unlocks setting the lintel.
91. **Slice 90:** Flue House — parge flue, wad throat, hang cowl. Cross-effect: pinned mantel unlocks setting the parge.
92. **Slice 91:** Fireback House — sand mould, pour plate, bed back. Cross-effect: hung cowl unlocks setting the mould.
93. **Slice 92:** Grate House — swage bar, rivet basket, register slide. Cross-effect: bedded back unlocks setting the swage.
94. **Slice 93:** Brick Yard — pug clay, strike green, set hack. Cross-effect: registered slide unlocks setting the pug.
95. **Slice 94:** Tile House — drape horse, pallet green, nick arris. Cross-effect: set hack unlocks setting the horse.
96. **Slice 95:** Slate Yard — scapple face, punch hole, lap slate. Cross-effect: nicked arris unlocks setting the face.
97. **Slice 96:** Flashing House — roll sheet, boss welt, dress flash. Cross-effect: lapped slate unlocks setting the sheet.
98. **Slice 97:** Block Loft — bore cheek, score sheave, strop block. Cross-effect: dressed flash unlocks setting the cheek.
99. **Slice 98:** Oar Loft — round shaft, spoon blade, bind grip. Cross-effect: stropped block unlocks setting the shaft.
100. **Slice 99:** Launch Ways — grease ways, set poppet, trip trigger. Cross-effect: bound grip unlocks setting the grease.
101. **Slice 100:** Clinker Shed — steam strake, clench land, fair garboard. Cross-effect: launched hull unlocks setting the steam.
102. **Slice 101:** Windlass House — ship bars, drop pawl, heave round. Cross-effect: faired garboard unlocks setting the bars.
103. **Slice 102:** Mould Loft — loft grid, spile plank, bevel station. Cross-effect: heaved round unlocks setting the grid.
104. **Slice 103:** Treenail House — shave billet, auger hole, drive trunnel. Cross-effect: bevelled station unlocks setting the billet.
105. **Slice 104:** Deadwood Yard — dub timber, cut rabbet, bolt hog. Cross-effect: driven trunnel unlocks setting the dub.
106. **Slice 105:** Mast Pond — sink pole, range mast, hoop partner. Cross-effect: bolted hog unlocks setting the sink.
107. **Slice 106:** Stem House — hew stem, cut gripe, hang knee. Cross-effect: hooped partner unlocks setting the hew.
108. **Slice 107:** Fid House — turn fid, ream eye, seize eye. Cross-effect: hung knee unlocks setting the turn.
109. **Slice 108:** Cleat House — saw cleat, gouge horn, bolt base. Cross-effect: seized eye unlocks setting the saw.
110. **Slice 109:** Hawse House — bore hawse, seat pipe, pay collar. Cross-effect: bolted base unlocks setting the bore.
111. **Slice 110:** Deadeye Loft — score deadeye, reeve strop, seize lanyard. Cross-effect: paid collar unlocks setting the rim.
112. **Slice 111:** Parrel House — groove truck, thread rib, truss parrel. Cross-effect: seized lanyard unlocks setting the truck.
113. **Slice 112:** Bitts House — step bitts, cross thwart, belay cable. Cross-effect: trussed parrel unlocks setting the step.
114. **Slice 113:** Gammoning House — woold bowsprit, ride turns, frap gammon. Cross-effect: belayed cable unlocks setting the woold.
115. **Slice 114:** Tiller House — shape tiller, fit helm, yoke tiller. Cross-effect: frapped gammon unlocks setting the shape.
116. **Slice 115:** Cathead House — adze bill, bush roller, fish fluke. Cross-effect: yoked tiller unlocks setting the bill.
117. **Slice 116:** Transom House — scribe wing, fit fashion, spike stern. Cross-effect: fished fluke unlocks setting the wing.
118. **Slice 117:** Scupper House — broach scupper, chase drain, plug mouth. Cross-effect: spiked stern unlocks setting the broach.
119. **Slice 118:** Binnacle House — true hood, fill lamp, lock card. Cross-effect: plugged mouth unlocks setting the hood.
120. **Slice 119:** Futtock House — cant futtock, scarph butt, clench belly. Cross-effect: locked card unlocks setting the cant.
121. **Slice 120:** Crosstree House — square crosstree, spread hounds, seize bolster. Cross-effect: clenched belly unlocks setting the tree.
122. **Slice 121:** Waterway House — snipe waterway, dowel margin, pay waterway. Cross-effect: seized bolster unlocks setting the snipe.
123. **Slice 122:** Coaming House — joggle coaming, lodge end, coak coaming. Cross-effect: paid waterway unlocks setting the joggle.
124. **Slice 123:** Gunwale House — snape covering, hance rail, dump bolt. Cross-effect: coaked coaming unlocks setting the covering.
125. **Slice 124:** Davit House — sweep davit, band crane, ship davit. Cross-effect: dumped bolt unlocks setting the sweep.
126. **Slice 125:** Boomkin House — steeve boomkin, bee iron, seize guy. Cross-effect: shipped davit unlocks setting the steeve.
127. **Slice 126:** Channel House — score channel, bolt plate, set strap. Cross-effect: seized guy unlocks setting the face.
128. **Slice 127:** Kevel House — chamfer kevel, mortise jaw, clench kevel. Cross-effect: set strap unlocks setting the chamfer.
129. **Slice 128:** Knighthead House — score knight, box bit, lash knight. Cross-effect: clenched kevel unlocks setting the knight.
130. **Slice 129:** Carling House — notch carling, lodge ledge, spike carling. Cross-effect: lashed knight unlocks setting the notch.
131. **Slice 130:** Tabernacle House — score tabernacle, mortise gate, pin keeper. Cross-effect: spiked carling unlocks setting the socket.
132. **Slice 131:** Planksheer House — score sheer, plane plank, dump edge. Cross-effect: pinned keeper unlocks setting the sheer.
133. **Slice 132:** Spirketting House — score spirket, plane strake, clench spirket. Cross-effect: dumped edge unlocks setting the spirket.
134. **Slice 133:** Trestle-tree House — score trestle, tenon rest, seize bib. Cross-effect: clenched spirket unlocks setting the trestle.
135. **Slice 134:** Breast-hook House — score crook, bolt palm, fay hook. Cross-effect: seized bib unlocks setting the crook.
136. **Slice 135:** Lodging-knee House — scribe lodging, bolt chock, nick lodging. Cross-effect: fayed hook unlocks setting the lodging.
137. **Slice 136:** Dagger-knee House — fair dagger, side siding, mark sirmark. Cross-effect: nicked lodging unlocks setting the dagger.
138. **Slice 137:** Rider House — wring rider, seat filling, dump wring. Cross-effect: marked sirmark unlocks setting the rider.
139. **Slice 138:** Keelson House — scarph keelson, pack stopwater, bolt sister. Cross-effect: dumped wring unlocks setting the keelson.
140. **Slice 139:** Crutch House — adze crutch, fit counter, spike crotch. Cross-effect: bolted sister unlocks setting the crutch.
141. **Slice 140:** Pointer House — bevel pointer, bed inner, dump compound. Cross-effect: spiked crotch unlocks setting the pointer.
142. **Slice 141:** Stanchion House — true stanchion, wedge prop, spike foot. Cross-effect: dumped compound unlocks setting the stanchion.
143. **Slice 142:** Pillar House — hew pillar, square king, shore queen. Cross-effect: spiked foot unlocks setting the pillar.
144. **Slice 143+:** More authored pockets. Crawler hunts *sameness* and rejects reskins.
55. **Scale rule:** stop counting a cell when a sameness crawler cannot tell it from another cell by verbs + inhabitants + effects.

The factory may generate substrate. Authored depth is what we claim.

---

## How to run

```text
python3 -m adventure_forge play --preset marsh_scout --seed 1
python3 -m adventure_forge play --preset marsh_scout --seed 1 --commands-file traces/marsh_harbor_compact.json
python3 -m adventure_forge verify
```

Play does not read traces as solutions except when a builder explicitly asks it to execute a command file. The play module does not import orchestrator evidence or verify internals.

---

## Non-goals (this scored revision)

- Copying Skyrim or Baldur’s Gate 3 plots, factions, IP, 3D, shouts, or Larian combat.
- Play-time LLM improvisation of rooms, rulings, or outcomes.
- A 3D or Larian GUI. A thin Vercel HTTP adapter of the CLI player is in scope.
- Treating commit count, test count, or agent volume as success.
- Keeping the four original briefs as live law.
