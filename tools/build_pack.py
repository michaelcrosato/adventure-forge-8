#!/usr/bin/env python3
"""Compile Ashfen Coast pack.json from authored data plus the salvage catalog."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "ashfen" / "pack.json"

ADJS = [
    "bent",
    "rusted",
    "salt",
    "tarred",
    "cracked",
    "braided",
    "pitted",
    "pale",
    "hooked",
    "knotted",
]
NOUNS = [
    "hook",
    "spike",
    "buckle",
    "shackle",
    "needle",
    "clasp",
    "ring",
    "wedge",
    "plate",
    "peg",
]


def salvage_catalog() -> tuple[dict[str, dict], list[str]]:
    items: dict[str, dict] = {}
    order: list[str] = []
    n = 0
    for adj in ADJS:
        for noun in NOUNS:
            item_id = f"salvage_{n:03d}"
            items[item_id] = {"name": f"{adj} {noun}", "kind": "salvage"}
            order.append(item_id)
            n += 1
    return items, order


def action(
    aid: str,
    label: str,
    group: str,
    when: dict,
    text: str,
    effects: list | None = None,
) -> dict:
    spec = {
        "id": aid,
        "label": label,
        "group": group,
        "when": when,
        "text": text,
        "effects": effects or [],
    }
    return spec


def build() -> dict:
    salvage_items, salvage_ids = salvage_catalog()
    items = {
        "frayed_rope": {"name": "frayed rope", "kind": "gear"},
        "compact_tablet": {"name": "compact tablet", "kind": "key"},
        "city_papers": {"name": "city papers", "kind": "key"},
        "ash_relic": {"name": "ash relic", "kind": "relic"},
        "brass_key": {"name": "brass key", "kind": "key"},
        "grain_sack": {"name": "grain sack", "kind": "goods"},
        "bone_name": {"name": "bone name", "kind": "rite"},
        "peat_brick": {"name": "peat brick", "kind": "goods"},
        "lens_shard": {"name": "lens shard", "kind": "glass"},
        "hemp_hank": {"name": "hemp hank", "kind": "goods"},
        "salt_cake": {"name": "salt cake", "kind": "goods"},
        "wet_fish": {"name": "wet fish", "kind": "goods"},
        "cured_fish": {"name": "cured fish", "kind": "goods"},
        "weir_basket": {"name": "weir basket", "kind": "gear"},
        "eel_catch": {"name": "eel catch", "kind": "goods"},
        "undyed_cloth": {"name": "undyed cloth", "kind": "goods"},
        "dyed_cloth": {"name": "dyed cloth", "kind": "goods"},
        "toll_token": {"name": "toll token", "kind": "key"},
        "vane_pin": {"name": "vane pin", "kind": "gear"},
        "spat_bag": {"name": "spat bag", "kind": "goods"},
        "oyster_lot": {"name": "oyster lot", "kind": "goods"},
        "tally_slate": {"name": "tally slate", "kind": "key"},
        "ice_block": {"name": "ice block", "kind": "goods"},
        "drowned_token": {"name": "drowned token", "kind": "rite"},
        "comb_cake": {"name": "comb cake", "kind": "goods"},
        "cask_bung": {"name": "cask bung", "kind": "goods"},
        **salvage_items,
    }

    locations = {
        "saltfen.dock": {
            "region": "saltfen",
            "name": "Saltfen Dock",
            "situation": "Wet planks shift under the tide. Nets hang from tarred posts.",
            "situation_if": [
                {
                    "when": {"has_flag": "compact_restored"},
                    "text": "The dock crew move with a shared list.",
                },
                {
                    "when": {"sheet": ["origin", "marshborn"]},
                    "text": "The mud smell feels like home.",
                },
                {
                    "when": {"sheet": ["origin", "cityward"]},
                    "text": "Salt and tar sting your city nose.",
                },
            ],
            "exits": [
                {"to": "saltfen.market", "label": "Go to market"},
                {"to": "saltfen.tidegate", "label": "Go to tide gate"},
            ],
            "ground": ["frayed_rope"],
            "actors": ["dock_boss"],
        },
        "saltfen.market": {
            "region": "saltfen",
            "name": "Saltfen Market",
            "situation": "Stalls crowd the wet stone. Eel smoke hangs low.",
            "situation_if": [
                {
                    "when": {"has_flag": "marsh_friend"},
                    "text": "The eel-seller leaves a space at his board.",
                },
                {
                    "when": {"has_flag": "watch_trust"},
                    "text": "A watch pair nod as you pass.",
                },
            ],
            "exits": [
                {"to": "saltfen.dock", "label": "Go to dock"},
                {"to": "saltfen.watchhouse", "label": "Go to watch-house"},
                {"to": "saltfen.inn", "label": "Go to inn"},
                {"to": "saltfen.salvage", "label": "Go to salvage yard"},
                {"to": "saltfen.tidegate", "label": "Go to tide gate"},
                {"to": "ashfen.causeway", "label": "Go to causeway"},
                {
                    "to": "saltfen.warehouse",
                    "label": "Enter warehouse",
                    "when": {"has_flag": "warehouse_open"},
                },
            ],
            "ground": [],
            "actors": ["eel_seller"],
        },
        "saltfen.watchhouse": {
            "region": "saltfen",
            "name": "Watch-house",
            "situation": "A low stone room. A ledger sits open by the door.",
            "exits": [{"to": "saltfen.market", "label": "Go to market"}],
            "ground": [],
            "actors": ["watch_sergeant"],
        },
        "saltfen.inn": {
            "region": "saltfen",
            "name": "Saltfen Inn",
            "situation": "A cramped room. Stew ticks on a black stove.",
            "exits": [{"to": "saltfen.market", "label": "Go to market"}],
            "ground": [],
            "actors": ["innkeep"],
        },
        "saltfen.warehouse": {
            "region": "saltfen",
            "name": "Harbor Warehouse",
            "situation": "Dust and salt crust the crates. One chest sits unlatched.",
            "exits": [{"to": "saltfen.market", "label": "Go to market"}],
            "ground": ["compact_tablet"],
            "actors": [],
        },
        "saltfen.tidegate": {
            "region": "saltfen",
            "name": "Tide Gate",
            "situation": "A stone arch meets the mudflat. Water writes the hour.",
            "show_tide": True,
            "exits": [
                {"to": "saltfen.dock", "label": "Go to dock"},
                {"to": "saltfen.market", "label": "Go to market"},
            ],
            "ground": [],
            "actors": [],
        },
        "saltfen.salvage": {
            "region": "saltfen",
            "name": "Salvage Yard",
            "situation": "Heaps of ship iron and rope fill the lot. Each piece has a tag.",
            "exits": [{"to": "saltfen.market", "label": "Go to market"}],
            "ground": list(salvage_ids),
            "actors": [],
        },
        "ashfen.causeway": {
            "region": "saltfen",
            "name": "Ashfen Causeway",
            "situation": "A raised track of packed shell. The stacks rise inland.",
            "exits": [
                {"to": "saltfen.market", "label": "Go to market"},
                {"to": "stacks.base", "label": "Go to stack base"},
                {"to": "mill.lane", "label": "Go to mill lane"},
                {"to": "court.gate", "label": "Go to reed court"},
                {"to": "road.ford", "label": "Go to drowned road"},
                {"to": "camp.gate", "label": "Go to fever camp"},
                {"to": "name.path", "label": "Go to namehouse"},
                {"to": "fold.lane", "label": "Go to peat fold"},
                {"to": "glass.path", "label": "Go to lens ruin"},
                {"to": "rope.path", "label": "Go to ropewalk"},
                {"to": "pans.path", "label": "Go to salt pans"},
                {"to": "smoke.path", "label": "Go to smokehouse"},
                {"to": "weir.path", "label": "Go to eel weir"},
                {"to": "dye.path", "label": "Go to dye works"},
                {"to": "ferry.path", "label": "Go to toll ferry"},
                {"to": "pump.path", "label": "Go to windpump"},
                {"to": "oyster.path", "label": "Go to oyster park"},
                {"to": "count.path", "label": "Go to counting house"},
                {"to": "ice.path", "label": "Go to ice cellar"},
                {"to": "wreck.path", "label": "Go to wreck chapel"},
                {"to": "hive.path", "label": "Go to bee skeps"},
                {"to": "mead.path", "label": "Go to mead house"},
            ],
            "ground": [],
            "actors": ["wounded_runner"],
        },
        "stacks.base": {
            "region": "hollow_stacks",
            "name": "Stack Base",
            "situation": "Broken towers lean over scree. Ropes hang from the first ledge.",
            "situation_if": [
                {
                    "when": {"has_flag": "thief_jailed"},
                    "text": "Climbers watch you like a snare.",
                }
            ],
            "exits": [{"to": "ashfen.causeway", "label": "Go to causeway"}],
            "ground": [],
            "actors": ["mira"],
        },
        "stacks.switchback": {
            "region": "hollow_stacks",
            "name": "Switchback",
            "situation": "A narrow path cuts the outer wall. Wind tugs your shirt.",
            "exits": [{"to": "stacks.base", "label": "Climb down to base"}],
            "ground": [],
            "actors": [],
        },
        "stacks.midledge": {
            "region": "hollow_stacks",
            "name": "Mid Ledge",
            "situation": "A wide shelf of old floor. Birds nest in the beam holes.",
            "exits": [{"to": "stacks.switchback", "label": "Climb down the switchback"}],
            "ground": [],
            "actors": [],
        },
        "stacks.windbridge": {
            "region": "hollow_stacks",
            "name": "Wind Bridge",
            "situation": "Planks span a gap. A guyline hums in the wind.",
            "exits": [{"to": "stacks.midledge", "label": "Go back to the ledge"}],
            "ground": [],
            "actors": [],
        },
        "stacks.relic": {
            "region": "hollow_stacks",
            "name": "Relic Chamber",
            "situation": "A round room. Ash cakes a stone bowl in the center.",
            "exits": [{"to": "stacks.windbridge", "label": "Go back to the bridge"}],
            "ground": ["ash_relic"],
            "actors": [],
        },
        "stacks.undercroft": {
            "region": "hollow_stacks",
            "name": "Undercroft",
            "situation": "A low vault under the bridge. Beams creak when you touch them.",
            "exits": [{"to": "stacks.windbridge", "label": "Climb back to the bridge"}],
            "ground": [],
            "actors": [],
        },
        "mill.lane": {
            "region": "kiln_mill",
            "name": "Mill Lane",
            "situation": "Clay ruts climb from the shell road. Kiln smoke hangs inland.",
            "exits": [
                {"to": "ashfen.causeway", "label": "Go to causeway"},
                {"to": "mill.yard", "label": "Go to mill yard"},
                {"to": "court.gate", "label": "Go to reed court"},
            ],
            "ground": [],
            "actors": [],
        },
        "mill.yard": {
            "region": "kiln_mill",
            "name": "Mill Yard",
            "situation": "Sacks lean on a debt board. The mill wheel knocks slow.",
            "situation_if": [
                {
                    "when": {"has_flag": "compact_restored"},
                    "text": "The miller names dock rates.",
                },
                {
                    "when": {"has_flag": "kiln_pact_sealed"},
                    "text": "The debt board is blank.",
                },
                {
                    "when": {"sheet": ["origin", "marshborn"]},
                    "text": "Reed chaff on the sacks smells like home.",
                },
            ],
            "exits": [
                {"to": "mill.lane", "label": "Go to mill lane"},
                {"to": "mill.kiln", "label": "Go to kiln"},
                {"to": "mill.loft", "label": "Go to loft"},
                {"to": "mill.sluice", "label": "Go to sluice"},
            ],
            "ground": [],
            "actors": ["miller"],
        },
        "mill.kiln": {
            "region": "kiln_mill",
            "name": "Kiln",
            "situation": "A brick kiln holds the heat. Ash cakes the damper bar.",
            "situation_if": [
                {
                    "when": {"has_flag": "kiln_hot"},
                    "text": "The mouth runs white.",
                },
                {
                    "when": {"has_flag": "kiln_lit"},
                    "text": "A low fire ticks in the grate.",
                },
            ],
            "exits": [{"to": "mill.yard", "label": "Go to mill yard"}],
            "ground": [],
            "actors": ["pell"],
        },
        "mill.loft": {
            "region": "kiln_mill",
            "name": "Grain Loft",
            "situation": "Dust hangs between the beams. Rats tick in the sacks.",
            "exits": [{"to": "mill.yard", "label": "Go to mill yard"}],
            "ground": ["grain_sack"],
            "actors": ["sila"],
        },
        "mill.sluice": {
            "region": "kiln_mill",
            "name": "Mill Sluice",
            "situation": "Dark water turns the wheel. One stone sits off true.",
            "exits": [{"to": "mill.yard", "label": "Go to mill yard"}],
            "ground": [],
            "actors": [],
        },
        "court.gate": {
            "region": "reed_court",
            "name": "Reed Court Gate",
            "situation": "Reed screens a low stone gate. A bailiff bars the path.",
            "situation_if": [
                {
                    "when": {"has_flag": "reed_sentence_passed"},
                    "text": "The gate stands open after the sentence.",
                }
            ],
            "exits": [
                {"to": "ashfen.causeway", "label": "Go to causeway"},
                {"to": "mill.lane", "label": "Go to mill lane"},
                {"to": "court.yard", "label": "Go to court yard"},
            ],
            "ground": [],
            "actors": ["bailiff"],
        },
        "court.yard": {
            "region": "reed_court",
            "name": "Court Yard",
            "situation": "Wet flags hold a quiet crowd. Reeds hiss along the wall.",
            "exits": [
                {"to": "court.gate", "label": "Go to court gate"},
                {"to": "court.hall", "label": "Go to hall"},
                {"to": "court.cell", "label": "Go to cell"},
            ],
            "ground": [],
            "actors": [],
        },
        "court.hall": {
            "region": "reed_court",
            "name": "Reed Hall",
            "situation": "A round hall. The magistrate sits on a reed mat.",
            "situation_if": [
                {
                    "when": {"has_flag": "kiln_pact_sealed"},
                    "text": "Orin has heard of the mill pact.",
                },
                {
                    "when": {"has_flag": "reed_sentence_passed"},
                    "text": "The hall is still after the sentence.",
                },
            ],
            "exits": [
                {"to": "court.yard", "label": "Go to court yard"},
                {"to": "court.archive", "label": "Go to archive"},
            ],
            "ground": [],
            "actors": ["magistrate"],
        },
        "court.cell": {
            "region": "reed_court",
            "name": "Holding Cell",
            "situation": "A damp cell. Tam sits on a board and waits.",
            "exits": [{"to": "court.yard", "label": "Go to court yard"}],
            "ground": [],
            "actors": ["tam"],
        },
        "court.archive": {
            "region": "reed_court",
            "name": "Reed Archive",
            "situation": "Shelves of wet-ink rolls. The air smells of reed glue.",
            "exits": [{"to": "court.hall", "label": "Go to hall"}],
            "ground": [],
            "actors": ["nia"],
        },
        "road.ford": {
            "region": "drowned_road",
            "name": "Drowned Ford",
            "situation": "A shell track sinks into the flats. Poles mark the old road.",
            "show_weather": True,
            "exits": [
                {"to": "ashfen.causeway", "label": "Go to causeway"},
                {"to": "road.dike", "label": "Go to dike"},
                {"to": "camp.gate", "label": "Go to fever camp"},
            ],
            "ground": [],
            "actors": [],
        },
        "road.dike": {
            "region": "drowned_road",
            "name": "Sea Dike",
            "situation": "A low dike cuts the flats. Water works the far side.",
            "show_weather": True,
            "exits": [
                {"to": "road.ford", "label": "Go to ford"},
                {"to": "road.hut", "label": "Go to hut"},
                {"to": "road.drownway", "label": "Go to drownway"},
            ],
            "ground": [],
            "actors": ["rell"],
        },
        "road.hut": {
            "region": "drowned_road",
            "name": "Dike Hut",
            "situation": "A tarred hut leans on the dike. A lamp sits unlit.",
            "situation_if": [
                {
                    "when": {"has_flag": "reed_sentence_passed"},
                    "text": "Cal has heard the reed sentence.",
                }
            ],
            "exits": [
                {"to": "road.dike", "label": "Go to dike"},
                {"to": "road.beacon", "label": "Go to beacon"},
            ],
            "ground": [],
            "actors": ["cal"],
        },
        "road.drownway": {
            "region": "drowned_road",
            "name": "Drownway",
            "situation": "The old road is a wet cut. Poles vanish in the flats.",
            "show_weather": True,
            "exits": [
                {"to": "road.dike", "label": "Go to dike"},
                {"to": "road.beacon", "label": "Go to beacon"},
            ],
            "ground": [],
            "actors": [],
        },
        "road.beacon": {
            "region": "drowned_road",
            "name": "Road Beacon",
            "situation": "A stone post holds a dark pan. The flats wait for a light.",
            "situation_if": [
                {
                    "when": {"has_flag": "beacon_lit"},
                    "text": "The pan burns and the road holds.",
                }
            ],
            "exits": [
                {"to": "road.hut", "label": "Go to hut"},
                {"to": "road.drownway", "label": "Go to drownway"},
            ],
            "ground": [],
            "actors": [],
        },
        "camp.gate": {
            "region": "fever_camp",
            "name": "Fever Camp Gate",
            "situation": "Lime marks a rope line. A lamp burns with a sour wick.",
            "situation_if": [
                {
                    "when": {"has_flag": "beacon_lit"},
                    "text": "A clean boat could see the road fire.",
                },
                {
                    "when": {"has_flag": "fever_broken"},
                    "text": "The rope line hangs slack.",
                },
            ],
            "exits": [
                {"to": "ashfen.causeway", "label": "Go to causeway"},
                {"to": "road.ford", "label": "Go to ford"},
                {"to": "camp.yard", "label": "Go to camp yard"},
                {"to": "name.path", "label": "Go to namehouse"},
            ],
            "ground": [],
            "actors": [],
        },
        "camp.yard": {
            "region": "fever_camp",
            "name": "Camp Yard",
            "situation": "Pallets sit in two rows. Joss keeps the sick from the well.",
            "exits": [
                {"to": "camp.gate", "label": "Go to camp gate"},
                {"to": "camp.ward", "label": "Go to ward"},
                {"to": "camp.still", "label": "Go to still"},
                {"to": "camp.pits", "label": "Go to pits"},
            ],
            "ground": [],
            "actors": ["joss"],
        },
        "camp.ward": {
            "region": "fever_camp",
            "name": "Sick Ward",
            "situation": "Low cots fill the tent. Ren breathes in short hits.",
            "situation_if": [
                {
                    "when": {"has_flag": "fever_broken"},
                    "text": "Ren sleeps cool.",
                }
            ],
            "exits": [{"to": "camp.yard", "label": "Go to camp yard"}],
            "ground": [],
            "actors": ["ren"],
        },
        "camp.still": {
            "region": "fever_camp",
            "name": "Herb Still",
            "situation": "A clay still ticks. Bitter steam beads on the lid.",
            "exits": [{"to": "camp.yard", "label": "Go to camp yard"}],
            "ground": [],
            "actors": ["oat"],
        },
        "camp.pits": {
            "region": "fever_camp",
            "name": "Lime Pits",
            "situation": "Open pits hold lime and rags. The air bites the nose.",
            "exits": [{"to": "camp.yard", "label": "Go to camp yard"}],
            "ground": [],
            "actors": [],
        },
        "name.path": {
            "region": "namehouse",
            "name": "Namehouse Path",
            "situation": "A cut of white stone sinks toward a low door. Wind names no one.",
            "exits": [
                {"to": "ashfen.causeway", "label": "Go to causeway"},
                {"to": "camp.gate", "label": "Go to fever camp"},
                {"to": "name.yard", "label": "Go to name yard"},
                {"to": "fold.lane", "label": "Go to peat fold"},
            ],
            "ground": [],
            "actors": [],
        },
        "name.yard": {
            "region": "namehouse",
            "name": "Name Yard",
            "situation": "Bone tags hang on a dry line. Ila watches the door.",
            "exits": [
                {"to": "name.path", "label": "Go to namehouse path"},
                {"to": "name.hall", "label": "Go to name hall"},
                {"to": "name.crypt", "label": "Go to crypt"},
                {"to": "name.script", "label": "Go to script room"},
            ],
            "ground": [],
            "actors": ["ila"],
        },
        "name.hall": {
            "region": "namehouse",
            "name": "Name Hall",
            "situation": "A wall of small niches. Most tags are gone.",
            "situation_if": [
                {
                    "when": {"has_flag": "fever_broken"},
                    "text": "Venn has heard a living name from the camp.",
                },
                {
                    "when": {"has_flag": "name_restored"},
                    "text": "One niche holds a bone name again.",
                },
            ],
            "exits": [{"to": "name.yard", "label": "Go to name yard"}],
            "ground": [],
            "actors": ["venn"],
        },
        "name.crypt": {
            "region": "namehouse",
            "name": "Name Crypt",
            "situation": "A cold shelf. One tag lies in the dust.",
            "exits": [{"to": "name.yard", "label": "Go to name yard"}],
            "ground": ["bone_name"],
            "actors": [],
        },
        "name.script": {
            "region": "namehouse",
            "name": "Script Room",
            "situation": "A desk of scraped bone. Ink sits in a shell.",
            "exits": [{"to": "name.yard", "label": "Go to name yard"}],
            "ground": [],
            "actors": ["sarn"],
        },
        "fold.lane": {
            "region": "peat_fold",
            "name": "Fold Lane",
            "situation": "Black turf banks the track. Smoke from a peat fire hangs low.",
            "exits": [
                {"to": "ashfen.causeway", "label": "Go to causeway"},
                {"to": "name.path", "label": "Go to namehouse"},
                {"to": "fold.green", "label": "Go to the green"},
                {"to": "glass.path", "label": "Go to lens ruin"},
            ],
            "ground": [],
            "actors": [],
        },
        "fold.green": {
            "region": "peat_fold",
            "name": "Fold Green",
            "situation": "A wet common holds a share board. Brin stands by the list.",
            "situation_if": [
                {
                    "when": {"has_flag": "name_restored"},
                    "text": "Brin has heard a fold name come home.",
                },
                {
                    "when": {"has_flag": "fold_held"},
                    "text": "The share board is marked even.",
                },
            ],
            "exits": [
                {"to": "fold.lane", "label": "Go to fold lane"},
                {"to": "fold.cut", "label": "Go to the cut"},
                {"to": "fold.shed", "label": "Go to the shed"},
                {"to": "fold.ditch", "label": "Go to the ditch"},
            ],
            "ground": [],
            "actors": ["brin"],
        },
        "fold.cut": {
            "region": "peat_fold",
            "name": "Peat Cut",
            "situation": "A black face of peat. Water seeps at the toe.",
            "situation_if": [
                {
                    "when": {"has_flag": "fold_flooded"},
                    "text": "The cut stands in water.",
                }
            ],
            "exits": [{"to": "fold.green", "label": "Go to the green"}],
            "ground": [],
            "actors": ["jase"],
        },
        "fold.shed": {
            "region": "peat_fold",
            "name": "Share Shed",
            "situation": "Dry bricks stack by a chalk board. Willa counts in pairs.",
            "exits": [{"to": "fold.green", "label": "Go to the green"}],
            "ground": [],
            "actors": ["willa"],
        },
        "fold.ditch": {
            "region": "peat_fold",
            "name": "Fold Ditch",
            "situation": "A narrow ditch takes the seepage. Reeds clog the mouth.",
            "exits": [{"to": "fold.green", "label": "Go to the green"}],
            "ground": [],
            "actors": [],
        },
        "glass.path": {
            "region": "lens_ruin",
            "name": "Lens Path",
            "situation": "Broken glass winks in the turf. A low ruin shows a round hole.",
            "exits": [
                {"to": "ashfen.causeway", "label": "Go to causeway"},
                {"to": "fold.lane", "label": "Go to peat fold"},
                {"to": "glass.yard", "label": "Go to glass yard"},
                {"to": "rope.path", "label": "Go to ropewalk"},
            ],
            "ground": [],
            "actors": [],
        },
        "glass.yard": {
            "region": "lens_ruin",
            "name": "Glass Yard",
            "situation": "Lead strips lie in a crate. The nave wall is open to the sky.",
            "situation_if": [
                {
                    "when": {"has_flag": "fold_held"},
                    "text": "Rook will take peat credit for lead.",
                }
            ],
            "exits": [
                {"to": "glass.path", "label": "Go to lens path"},
                {"to": "glass.nave", "label": "Go to the nave"},
                {"to": "glass.pit", "label": "Go to the pit"},
            ],
            "ground": [],
            "actors": [],
        },
        "glass.nave": {
            "region": "lens_ruin",
            "name": "Glass Nave",
            "situation": "A round frame holds empty lead. Light falls on the floor.",
            "situation_if": [
                {
                    "when": {"has_flag": "lens_set"},
                    "text": "The shard throws a line on the stone.",
                }
            ],
            "exits": [
                {"to": "glass.yard", "label": "Go to glass yard"},
                {"to": "glass.loft", "label": "Go to the loft"},
            ],
            "ground": [],
            "actors": ["rook"],
        },
        "glass.loft": {
            "region": "lens_ruin",
            "name": "Lens Loft",
            "situation": "A narrow walk sits behind the frame. A peg waits for a shard.",
            "exits": [{"to": "glass.nave", "label": "Go to the nave"}],
            "ground": [],
            "actors": ["lise"],
        },
        "glass.pit": {
            "region": "lens_ruin",
            "name": "Shard Pit",
            "situation": "A pit of broken panes. One shard still takes the light.",
            "exits": [{"to": "glass.yard", "label": "Go to glass yard"}],
            "ground": ["lens_shard"],
            "actors": ["nim"],
        },
        "rope.path": {
            "region": "ropewalk",
            "name": "Ropewalk Path",
            "situation": "A long shed shows at the end of a shell track. Hemp dust hangs.",
            "exits": [
                {"to": "ashfen.causeway", "label": "Go to causeway"},
                {"to": "glass.path", "label": "Go to lens ruin"},
                {"to": "rope.yard", "label": "Go to rope yard"},
                {"to": "pans.path", "label": "Go to salt pans"},
            ],
            "ground": [],
            "actors": [],
        },
        "rope.yard": {
            "region": "ropewalk",
            "name": "Rope Yard",
            "situation": "Hooks and hooks of unused strand. Tess waits by the door.",
            "exits": [
                {"to": "rope.path", "label": "Go to ropewalk path"},
                {"to": "rope.walk", "label": "Go to the walk"},
                {"to": "rope.loft", "label": "Go to the loft"},
            ],
            "ground": [],
            "actors": ["tess"],
        },
        "rope.walk": {
            "region": "ropewalk",
            "name": "The Walk",
            "situation": "A long floor runs the shed. Pegs wait for a taut line.",
            "situation_if": [
                {
                    "when": {"has_flag": "lens_set"},
                    "text": "A line of light from the ruin cuts the floor.",
                },
                {
                    "when": {"has_flag": "rope_walked"},
                    "text": "The new rope lies taut on the pegs.",
                },
            ],
            "exits": [
                {"to": "rope.yard", "label": "Go to rope yard"},
                {"to": "rope.end", "label": "Go to the far end"},
            ],
            "ground": [],
            "actors": [],
        },
        "rope.loft": {
            "region": "ropewalk",
            "name": "Hemp Loft",
            "situation": "Dry hanks hang from the beams. Bram sits on a crate.",
            "exits": [{"to": "rope.yard", "label": "Go to rope yard"}],
            "ground": ["hemp_hank"],
            "actors": ["bram"],
        },
        "rope.end": {
            "region": "ropewalk",
            "name": "Walk End",
            "situation": "The shed opens on a small landing. Kite waits with a purse.",
            "exits": [{"to": "rope.walk", "label": "Go to the walk"}],
            "ground": [],
            "actors": ["kite"],
        },
        "pans.path": {
            "region": "salt_pans",
            "name": "Pans Path",
            "situation": "White crust edges the track. The pans flash in the flats.",
            "exits": [
                {"to": "ashfen.causeway", "label": "Go to causeway"},
                {"to": "rope.path", "label": "Go to ropewalk"},
                {"to": "pans.yard", "label": "Go to pans yard"},
                {"to": "smoke.path", "label": "Go to smokehouse"},
            ],
            "ground": [],
            "actors": [],
        },
        "pans.yard": {
            "region": "salt_pans",
            "name": "Pans Yard",
            "situation": "Rakes lean on a low wall. Dorr waits by a list of pans.",
            "exits": [
                {"to": "pans.path", "label": "Go to pans path"},
                {"to": "pans.beds", "label": "Go to the beds"},
                {"to": "pans.well", "label": "Go to the brine well"},
                {"to": "pans.shed", "label": "Go to the weigh shed"},
            ],
            "ground": [],
            "actors": ["dorr"],
        },
        "pans.beds": {
            "region": "salt_pans",
            "name": "Salt Beds",
            "situation": "Shallow beds hold brine. A crust forms at the rims.",
            "situation_if": [
                {
                    "when": {"has_flag": "rope_walked"},
                    "text": "A taut line could rake the beds even.",
                },
                {
                    "when": {"has_flag": "salt_raked"},
                    "text": "One bed is scraped clean.",
                },
            ],
            "exits": [{"to": "pans.yard", "label": "Go to pans yard"}],
            "ground": [],
            "actors": [],
        },
        "pans.well": {
            "region": "salt_pans",
            "name": "Brine Well",
            "situation": "A stone well tastes of salt. Nell keeps the bucket.",
            "exits": [{"to": "pans.yard", "label": "Go to pans yard"}],
            "ground": [],
            "actors": ["nell"],
        },
        "pans.shed": {
            "region": "salt_pans",
            "name": "Weigh Shed",
            "situation": "A beam scale sits on a crate. Pim waits with chalk.",
            "exits": [{"to": "pans.yard", "label": "Go to pans yard"}],
            "ground": [],
            "actors": ["pim"],
        },
        "smoke.path": {
            "region": "smokehouse",
            "name": "Smoke Path",
            "situation": "A shed leaks a thin haze. Fish skins hang on the fence.",
            "exits": [
                {"to": "ashfen.causeway", "label": "Go to causeway"},
                {"to": "pans.path", "label": "Go to salt pans"},
                {"to": "smoke.yard", "label": "Go to smoke yard"},
                {"to": "weir.path", "label": "Go to eel weir"},
            ],
            "ground": [],
            "actors": [],
        },
        "smoke.yard": {
            "region": "smokehouse",
            "name": "Smoke Yard",
            "situation": "Racks stand under a low roof. Hal waits by a cure mark.",
            "exits": [
                {"to": "smoke.path", "label": "Go to smoke path"},
                {"to": "smoke.racks", "label": "Go to the fish racks"},
                {"to": "smoke.hearth", "label": "Go to the smoke hearth"},
                {"to": "smoke.loft", "label": "Go to the cure loft"},
            ],
            "ground": [],
            "actors": ["hal"],
        },
        "smoke.racks": {
            "region": "smokehouse",
            "name": "Fish Racks",
            "situation": "Poles hold wet fish. Drip ticks on the boards.",
            "situation_if": [
                {
                    "when": {"has_flag": "salt_raked"},
                    "text": "A brine cake would set the cure.",
                },
                {
                    "when": {"has_flag": "smoke_cured"},
                    "text": "The rack is empty and dry.",
                },
            ],
            "exits": [{"to": "smoke.yard", "label": "Go to smoke yard"}],
            "ground": ["wet_fish"],
            "actors": [],
        },
        "smoke.hearth": {
            "region": "smokehouse",
            "name": "Smoke Hearth",
            "situation": "A low hearth feeds the racks. Bea watches the draw.",
            "exits": [{"to": "smoke.yard", "label": "Go to smoke yard"}],
            "ground": [],
            "actors": ["bea"],
        },
        "smoke.loft": {
            "region": "smokehouse",
            "name": "Cure Loft",
            "situation": "Dry fish hang from pegs. Wren waits with a tally stick.",
            "exits": [{"to": "smoke.yard", "label": "Go to smoke yard"}],
            "ground": [],
            "actors": ["wren"],
        },
        "weir.path": {
            "region": "eel_weir",
            "name": "Weir Path",
            "situation": "A stake line cuts the creek. Eel slime shines on the posts.",
            "exits": [
                {"to": "ashfen.causeway", "label": "Go to causeway"},
                {"to": "smoke.path", "label": "Go to smokehouse"},
                {"to": "weir.yard", "label": "Go to weir yard"},
                {"to": "dye.path", "label": "Go to dye works"},
            ],
            "ground": [],
            "actors": [],
        },
        "weir.yard": {
            "region": "eel_weir",
            "name": "Weir Yard",
            "situation": "Wicker mouths lean on a rail. Cess waits by a run mark.",
            "exits": [
                {"to": "weir.path", "label": "Go to weir path"},
                {"to": "weir.stakes", "label": "Go to the stakes"},
                {"to": "weir.pool", "label": "Go to the eel pool"},
                {"to": "weir.hut", "label": "Go to the weir hut"},
            ],
            "ground": [],
            "actors": ["cess"],
        },
        "weir.stakes": {
            "region": "eel_weir",
            "name": "Weir Stakes",
            "situation": "Baskets sit empty on the posts. The creek pulls past.",
            "situation_if": [
                {
                    "when": {"has_flag": "smoke_cured"},
                    "text": "A strip of cure would bait the mouths.",
                },
                {
                    "when": {"has_flag": "weir_lifted"},
                    "text": "The baskets sit empty and wet.",
                },
            ],
            "exits": [{"to": "weir.yard", "label": "Go to weir yard"}],
            "ground": [],
            "actors": [],
        },
        "weir.pool": {
            "region": "eel_weir",
            "name": "Eel Pool",
            "situation": "Dark water holds. Noll crouches at the lip.",
            "exits": [{"to": "weir.yard", "label": "Go to weir yard"}],
            "ground": [],
            "actors": ["noll"],
        },
        "weir.hut": {
            "region": "eel_weir",
            "name": "Weir Hut",
            "situation": "Dry baskets hang. Meg waits with a count board.",
            "exits": [{"to": "weir.yard", "label": "Go to weir yard"}],
            "ground": ["weir_basket"],
            "actors": ["meg"],
        },
        "dye.path": {
            "region": "dye_works",
            "name": "Dye Path",
            "situation": "Vat steam hangs over a clay track. Stained rags mark the way.",
            "exits": [
                {"to": "ashfen.causeway", "label": "Go to causeway"},
                {"to": "weir.path", "label": "Go to eel weir"},
                {"to": "dye.yard", "label": "Go to dye yard"},
                {"to": "ferry.path", "label": "Go to toll ferry"},
            ],
            "ground": [],
            "actors": [],
        },
        "dye.yard": {
            "region": "dye_works",
            "name": "Dye Yard",
            "situation": "Pots of stain sit by a list. Quill waits with wet hands.",
            "exits": [
                {"to": "dye.path", "label": "Go to dye path"},
                {"to": "dye.vats", "label": "Go to the vats"},
                {"to": "dye.loft", "label": "Go to the dye loft"},
                {"to": "dye.store", "label": "Go to the cloth store"},
            ],
            "ground": [],
            "actors": ["quill"],
        },
        "dye.vats": {
            "region": "dye_works",
            "name": "Dye Vats",
            "situation": "Three vats hold still liquor. Fen stirs with a long stick.",
            "situation_if": [
                {
                    "when": {"has_flag": "weir_lifted"},
                    "text": "Eel skin would bite the vat dark.",
                },
                {
                    "when": {"has_flag": "dye_struck"},
                    "text": "One vat sits spent and cool.",
                },
            ],
            "exits": [{"to": "dye.yard", "label": "Go to dye yard"}],
            "ground": [],
            "actors": ["fen"],
        },
        "dye.loft": {
            "region": "dye_works",
            "name": "Dye Loft",
            "situation": "Poles wait for wet cloth. Moss keeps a dry line clear.",
            "exits": [{"to": "dye.yard", "label": "Go to dye yard"}],
            "ground": [],
            "actors": ["moss"],
        },
        "dye.store": {
            "region": "dye_works",
            "name": "Cloth Store",
            "situation": "White cloth sits in a dry chest. The air smells of lye.",
            "exits": [{"to": "dye.yard", "label": "Go to dye yard"}],
            "ground": ["undyed_cloth"],
            "actors": [],
        },
        "ferry.path": {
            "region": "toll_ferry",
            "name": "Ferry Path",
            "situation": "A wide creek cuts the shell track. A hull waits at a post.",
            "exits": [
                {"to": "ashfen.causeway", "label": "Go to causeway"},
                {"to": "dye.path", "label": "Go to dye works"},
                {"to": "ferry.yard", "label": "Go to ferry yard"},
            ],
            "ground": [],
            "actors": [],
        },
        "ferry.yard": {
            "region": "toll_ferry",
            "name": "Ferry Yard",
            "situation": "A board lists fares. Bex waits with a token box.",
            "exits": [
                {"to": "ferry.path", "label": "Go to ferry path"},
                {"to": "ferry.slip", "label": "Go to the slip"},
            ],
            "ground": ["toll_token"],
            "actors": ["bex"],
        },
        "ferry.slip": {
            "region": "toll_ferry",
            "name": "Ferry Slip",
            "situation": "The hull knocks the posts. Ivo holds the line.",
            "exits": [
                {"to": "ferry.yard", "label": "Go to ferry yard"},
                {
                    "to": "ferry.boat",
                    "label": "Board the boat",
                    "when": {"has_flag": "boat_loaded"},
                },
            ],
            "ground": [],
            "actors": ["ivo"],
        },
        "ferry.boat": {
            "region": "toll_ferry",
            "name": "Ferry Boat",
            "situation": "Wet boards lift on the pull. The far bank is a pale line.",
            "situation_if": [
                {
                    "when": {"has_flag": "dye_struck"},
                    "text": "A dyed cloth would pass as fare.",
                },
                {
                    "when": {"has_flag": "ferry_crossed"},
                    "text": "The hull has already made the far bank.",
                },
            ],
            "exits": [{"to": "ferry.slip", "label": "Go to the slip"}],
            "ground": [],
            "actors": [],
        },
        "ferry.far": {
            "region": "toll_ferry",
            "name": "Far Landing",
            "situation": "Shell and reed mark the far landing. Ama waits with a stamp.",
            "situation_if": [
                {
                    "when": {"has_flag": "ferry_crossed"},
                    "text": "The stamp is wet on the board.",
                }
            ],
            "exits": [
                {"to": "ferry.boat", "label": "Board the near boat"},
                {"to": "pump.path", "label": "Go to windpump"},
            ],
            "ground": [],
            "actors": ["ama"],
        },
        "pump.path": {
            "region": "windpump",
            "name": "Pump Path",
            "situation": "A ring of sails stands on the leat. The flats shine wet.",
            "exits": [
                {"to": "ashfen.causeway", "label": "Go to causeway"},
                {"to": "ferry.far", "label": "Go to far landing"},
                {"to": "pump.yard", "label": "Go to pump yard"},
                {"to": "oyster.path", "label": "Go to oyster park"},
            ],
            "ground": [],
            "actors": [],
        },
        "pump.yard": {
            "region": "windpump",
            "name": "Pump Yard",
            "situation": "Od waits by a mark on the post. The vanes tick above.",
            "exits": [
                {"to": "pump.path", "label": "Go to pump path"},
                {"to": "pump.tower", "label": "Go to the vane tower"},
                {"to": "pump.crank", "label": "Go to the crank"},
                {"to": "pump.sump", "label": "Go to the sump"},
            ],
            "ground": [],
            "actors": ["od"],
        },
        "pump.tower": {
            "region": "windpump",
            "name": "Vane Tower",
            "situation": "Loose vanes slap. A pin lies in the dust.",
            "situation_if": [
                {
                    "when": {"has_flag": "ferry_crossed"},
                    "text": "A hull line would brace the sail.",
                },
                {
                    "when": {"has_flag": "flats_drained"},
                    "text": "The ring holds still and true.",
                },
            ],
            "exits": [{"to": "pump.yard", "label": "Go to pump yard"}],
            "ground": ["vane_pin"],
            "actors": ["rusk"],
        },
        "pump.crank": {
            "region": "windpump",
            "name": "Pump Crank",
            "situation": "A long crank waits. The well mouth is still.",
            "exits": [{"to": "pump.yard", "label": "Go to pump yard"}],
            "ground": [],
            "actors": [],
        },
        "pump.sump": {
            "region": "windpump",
            "name": "Pump Sump",
            "situation": "Water pools in a clay cut. Hobb waits with a board.",
            "situation_if": [
                {
                    "when": {"has_flag": "flats_drained"},
                    "text": "The cut sits dry and firm.",
                }
            ],
            "exits": [{"to": "pump.yard", "label": "Go to pump yard"}],
            "ground": [],
            "actors": ["hobb"],
        },
        "oyster.path": {
            "region": "oyster_park",
            "name": "Oyster Path",
            "situation": "Shell heaps edge the leat. The beds lie in the wet.",
            "exits": [
                {"to": "ashfen.causeway", "label": "Go to causeway"},
                {"to": "pump.path", "label": "Go to windpump"},
                {"to": "oyster.yard", "label": "Go to oyster yard"},
                {"to": "count.path", "label": "Go to counting house"},
            ],
            "ground": [],
            "actors": [],
        },
        "oyster.yard": {
            "region": "oyster_park",
            "name": "Oyster Yard",
            "situation": "Wex waits by a list of beds. Spat dust hangs.",
            "exits": [
                {"to": "oyster.path", "label": "Go to oyster path"},
                {"to": "oyster.beds", "label": "Go to the oyster beds"},
                {"to": "oyster.spat", "label": "Go to the spat house"},
                {"to": "oyster.shed", "label": "Go to the cull shed"},
            ],
            "ground": [],
            "actors": ["wex"],
        },
        "oyster.beds": {
            "region": "oyster_park",
            "name": "Oyster Beds",
            "situation": "Stakes mark the park. Empty shells click underfoot.",
            "situation_if": [
                {
                    "when": {"has_flag": "flats_drained"},
                    "text": "The dry flats would let you work the beds.",
                },
                {
                    "when": {"has_flag": "oyster_culled"},
                    "text": "The stakes sit empty and picked.",
                },
            ],
            "exits": [{"to": "oyster.yard", "label": "Go to oyster yard"}],
            "ground": [],
            "actors": [],
        },
        "oyster.spat": {
            "region": "oyster_park",
            "name": "Spat House",
            "situation": "Trays of young spat sit in shade. Pip keeps the lid.",
            "exits": [{"to": "oyster.yard", "label": "Go to oyster yard"}],
            "ground": ["spat_bag"],
            "actors": ["pip"],
        },
        "oyster.shed": {
            "region": "oyster_park",
            "name": "Cull Shed",
            "situation": "A cull board waits. Gell holds a knife and a tally.",
            "exits": [{"to": "oyster.yard", "label": "Go to oyster yard"}],
            "ground": [],
            "actors": ["gell"],
        },
        "count.path": {
            "region": "counting_house",
            "name": "Count Path",
            "situation": "A low stone house sits inland. Chalk dust hangs in the door.",
            "exits": [
                {"to": "ashfen.causeway", "label": "Go to causeway"},
                {"to": "oyster.path", "label": "Go to oyster park"},
                {"to": "count.yard", "label": "Go to count yard"},
                {"to": "ice.path", "label": "Go to ice cellar"},
            ],
            "ground": [],
            "actors": [],
        },
        "count.yard": {
            "region": "counting_house",
            "name": "Count Yard",
            "situation": "Voss waits by a slate board. The day's count is still open.",
            "exits": [
                {"to": "count.path", "label": "Go to count path"},
                {"to": "count.desk", "label": "Go to the tally desk"},
                {"to": "count.loft", "label": "Go to the tally loft"},
                {"to": "count.vault", "label": "Go to the count vault"},
            ],
            "ground": [],
            "actors": ["voss"],
        },
        "count.desk": {
            "region": "counting_house",
            "name": "Tally Desk",
            "situation": "Rhee keeps a dry quill. The tally roll lies blank.",
            "situation_if": [
                {
                    "when": {"has_flag": "oyster_culled"},
                    "text": "An oyster lot would close a gap in the roll.",
                },
                {
                    "when": {"has_flag": "tally_closed"},
                    "text": "The roll is shut for the day.",
                },
            ],
            "exits": [{"to": "count.yard", "label": "Go to count yard"}],
            "ground": [],
            "actors": ["rhee"],
        },
        "count.loft": {
            "region": "counting_house",
            "name": "Tally Loft",
            "situation": "Blank slates lean on a rack. Dust sits on the top edge.",
            "exits": [{"to": "count.yard", "label": "Go to count yard"}],
            "ground": ["tally_slate"],
            "actors": [],
        },
        "count.vault": {
            "region": "counting_house",
            "name": "Count Vault",
            "situation": "An iron door stands shut. Orm waits with a seal.",
            "situation_if": [
                {
                    "when": {"has_flag": "tally_closed"},
                    "text": "The seal is set and the door is shut.",
                }
            ],
            "exits": [{"to": "count.yard", "label": "Go to count yard"}],
            "ground": [],
            "actors": ["orm"],
        },
        "ice.path": {
            "region": "ice_cellar",
            "name": "Ice Path",
            "situation": "A cut in the bank holds shade. Cold air leaks from a door.",
            "exits": [
                {"to": "ashfen.causeway", "label": "Go to causeway"},
                {"to": "count.path", "label": "Go to counting house"},
                {"to": "ice.yard", "label": "Go to ice yard"},
                {"to": "wreck.path", "label": "Go to wreck chapel"},
            ],
            "ground": [],
            "actors": [],
        },
        "ice.yard": {
            "region": "ice_cellar",
            "name": "Ice Yard",
            "situation": "Yul waits by a cold mark. Straw wraps a block of ice.",
            "situation_if": [
                {
                    "when": {"has_flag": "tally_closed"},
                    "text": "A closed tally would buy the ice right.",
                }
            ],
            "exits": [
                {"to": "ice.path", "label": "Go to ice path"},
                {"to": "ice.pit", "label": "Go to the ice pit"},
                {"to": "ice.hold", "label": "Go to the ice hold"},
                {"to": "ice.door", "label": "Go to the ice door"},
            ],
            "ground": [],
            "actors": ["yul"],
        },
        "ice.pit": {
            "region": "ice_cellar",
            "name": "Ice Pit",
            "situation": "Sawdust covers a pit of ice. Saff keeps a saw.",
            "exits": [{"to": "ice.yard", "label": "Go to ice yard"}],
            "ground": ["ice_block"],
            "actors": ["saff"],
        },
        "ice.hold": {
            "region": "ice_cellar",
            "name": "Ice Hold",
            "situation": "Straw and straw line a dark room. The air bites.",
            "situation_if": [
                {
                    "when": {"has_flag": "ice_held"},
                    "text": "The hold sits packed and still.",
                }
            ],
            "exits": [{"to": "ice.yard", "label": "Go to ice yard"}],
            "ground": [],
            "actors": [],
        },
        "ice.door": {
            "region": "ice_cellar",
            "name": "Ice Door",
            "situation": "A thick door leans on a bar. Kest waits.",
            "exits": [{"to": "ice.yard", "label": "Go to ice yard"}],
            "ground": [],
            "actors": ["kest"],
        },
        "wreck.path": {
            "region": "wreck_chapel",
            "name": "Wreck Path",
            "situation": "Ribs of a wreck rise from the mud. A chapel sits in the hull.",
            "exits": [
                {"to": "ashfen.causeway", "label": "Go to causeway"},
                {"to": "ice.path", "label": "Go to ice cellar"},
                {"to": "wreck.yard", "label": "Go to wreck yard"},
                {"to": "hive.path", "label": "Go to bee skeps"},
            ],
            "ground": [],
            "actors": [],
        },
        "wreck.yard": {
            "region": "wreck_chapel",
            "name": "Wreck Yard",
            "situation": "Luth waits by a wreck list. Salt crusts the door.",
            "exits": [
                {"to": "wreck.path", "label": "Go to wreck path"},
                {"to": "wreck.hull", "label": "Go to the wreck hull"},
                {"to": "wreck.wash", "label": "Go to the wreck wash"},
                {"to": "wreck.altar", "label": "Go to the wreck altar"},
            ],
            "ground": [],
            "actors": ["luth"],
        },
        "wreck.hull": {
            "region": "wreck_chapel",
            "name": "Wreck Hull",
            "situation": "Dark water sits in the hold. A token lies in the silt.",
            "situation_if": [
                {
                    "when": {"has_flag": "ice_held"},
                    "text": "Held ice would keep the drowned token cold.",
                },
                {
                    "when": {"has_flag": "wreck_laid"},
                    "text": "The silt sits empty where the token lay.",
                },
            ],
            "exits": [{"to": "wreck.yard", "label": "Go to wreck yard"}],
            "ground": ["drowned_token"],
            "actors": ["kade"],
        },
        "wreck.wash": {
            "region": "wreck_chapel",
            "name": "Wreck Wash",
            "situation": "A stone bowl holds brine. The token must be washed.",
            "exits": [{"to": "wreck.yard", "label": "Go to wreck yard"}],
            "ground": [],
            "actors": [],
        },
        "wreck.altar": {
            "region": "wreck_chapel",
            "name": "Wreck Altar",
            "situation": "A low altar faces the broken prow. Efa waits.",
            "exits": [{"to": "wreck.yard", "label": "Go to wreck yard"}],
            "ground": [],
            "actors": ["efa"],
        },
        "hive.path": {
            "region": "bee_skeps",
            "name": "Hive Path",
            "situation": "Skeps sit on a dry bank. Bees hang in a low cloud.",
            "exits": [
                {"to": "ashfen.causeway", "label": "Go to causeway"},
                {"to": "wreck.path", "label": "Go to wreck chapel"},
                {"to": "hive.yard", "label": "Go to hive yard"},
                {"to": "mead.path", "label": "Go to mead house"},
            ],
            "ground": [],
            "actors": [],
        },
        "hive.yard": {
            "region": "bee_skeps",
            "name": "Hive Yard",
            "situation": "Sol waits by a hive mark. The hum is even.",
            "exits": [
                {"to": "hive.path", "label": "Go to hive path"},
                {"to": "hive.skeps", "label": "Go to the skeps"},
                {"to": "hive.comb", "label": "Go to the comb house"},
                {"to": "hive.shed", "label": "Go to the hive shed"},
            ],
            "ground": [],
            "actors": ["sol"],
        },
        "hive.skeps": {
            "region": "bee_skeps",
            "name": "Skep Row",
            "situation": "Straw skeps sit in a row. Tansy keeps a rag of smoke.",
            "situation_if": [
                {
                    "when": {"has_flag": "wreck_laid"},
                    "text": "A drowned ward would bless the hive.",
                },
                {
                    "when": {"has_flag": "hive_kept"},
                    "text": "The row sits still and even.",
                },
            ],
            "exits": [{"to": "hive.yard", "label": "Go to hive yard"}],
            "ground": [],
            "actors": ["tansy"],
        },
        "hive.comb": {
            "region": "bee_skeps",
            "name": "Comb House",
            "situation": "Open comb drips on a board. The air is sweet.",
            "exits": [{"to": "hive.yard", "label": "Go to hive yard"}],
            "ground": ["comb_cake"],
            "actors": [],
        },
        "hive.shed": {
            "region": "bee_skeps",
            "name": "Hive Shed",
            "situation": "Wick waits with a spare skep. Straw lies in a heap.",
            "exits": [{"to": "hive.yard", "label": "Go to hive yard"}],
            "ground": [],
            "actors": ["wick"],
        },
        "mead.path": {
            "region": "mead_house",
            "name": "Mead Path",
            "situation": "A mash house sits on the bank. Sweet steam hangs low.",
            "exits": [
                {"to": "ashfen.causeway", "label": "Go to causeway"},
                {"to": "hive.path", "label": "Go to bee skeps"},
                {"to": "mead.yard", "label": "Go to mead yard"},
            ],
            "ground": [],
            "actors": [],
        },
        "mead.yard": {
            "region": "mead_house",
            "name": "Mead Yard",
            "situation": "Hop waits by a cask mark. The mash smell is sharp.",
            "exits": [
                {"to": "mead.path", "label": "Go to mead path"},
                {"to": "mead.mash", "label": "Go to the mash"},
                {"to": "mead.crock", "label": "Go to the crock"},
                {"to": "mead.tap", "label": "Go to the tap"},
            ],
            "ground": [],
            "actors": ["hop"],
        },
        "mead.mash": {
            "region": "mead_house",
            "name": "Mash Tun",
            "situation": "Mal keeps a mash paddle. Comb lies in a tub.",
            "situation_if": [
                {
                    "when": {"has_flag": "hive_kept"},
                    "text": "True comb would pitch this mash.",
                },
                {
                    "when": {"has_flag": "mead_drawn"},
                    "text": "The mash sits still and even.",
                },
            ],
            "exits": [{"to": "mead.yard", "label": "Go to mead yard"}],
            "ground": [],
            "actors": ["mal"],
        },
        "mead.crock": {
            "region": "mead_house",
            "name": "Crock Row",
            "situation": "Open crocks sit on a board. A bung lies ready.",
            "exits": [{"to": "mead.yard", "label": "Go to mead yard"}],
            "ground": ["cask_bung"],
            "actors": [],
        },
        "mead.tap": {
            "region": "mead_house",
            "name": "Tap Bench",
            "situation": "Sera waits by a cask. A tap peg hangs.",
            "exits": [{"to": "mead.yard", "label": "Go to mead yard"}],
            "ground": [],
            "actors": ["sera"],
        },
    }

    actors = {
        "dock_boss": {
            "name": "Dock boss",
            "idle": "He counts barrels and does not look up.",
        },
        "eel_seller": {
            "name": "Eel-seller",
            "idle": "He turns eels on the board and waits.",
        },
        "watch_sergeant": {
            "name": "Watch sergeant",
            "idle": "She keeps a finger on the ledger.",
        },
        "innkeep": {
            "name": "Innkeep",
            "idle": "He wipes a cup and watches the door.",
        },
        "wounded_runner": {
            "name": "Wounded runner",
            "idle": "She sits on the shell track and binds a knee.",
        },
        "mira": {
            "name": "Mira",
            "idle": "She coils rope and eyes the first ledge.",
        },
        "miller": {
            "name": "Miller Brann",
            "idle": "He keeps a thumb on the debt board.",
        },
        "pell": {
            "name": "Pell",
            "idle": "She watches the kiln mouth and waits.",
        },
        "sila": {
            "name": "Sila",
            "idle": "She counts sacks and does not smile.",
        },
        "bailiff": {
            "name": "Bailiff Kesh",
            "idle": "He holds a staff across the gate.",
        },
        "magistrate": {
            "name": "Magistrate Orin",
            "idle": "She waits with both palms on her knees.",
        },
        "tam": {
            "name": "Tam",
            "idle": "He looks at the floor and does not speak first.",
        },
        "nia": {
            "name": "Clerk Nia",
            "idle": "She keeps a dry roll under her arm.",
        },
        "rell": {
            "name": "Rell",
            "idle": "He watches the dike and the weather.",
        },
        "cal": {
            "name": "Cal",
            "idle": "She keeps one hand on the unlit lamp.",
        },
        "joss": {
            "name": "Nurse Joss",
            "idle": "She stands between the well and the cots.",
        },
        "ren": {
            "name": "Ren",
            "idle": "He lies still and watches the tent peak.",
        },
        "oat": {
            "name": "Oat",
            "idle": "He tends the still and does not taste the steam.",
        },
        "venn": {
            "name": "Keeper Venn",
            "idle": "He keeps his palm on an empty niche.",
        },
        "ila": {
            "name": "Ila",
            "idle": "She sorts tags and does not speak.",
        },
        "sarn": {
            "name": "Sarn",
            "idle": "He scrapes a bone strip for ink.",
        },
        "brin": {
            "name": "Headwoman Brin",
            "idle": "She keeps a thumb on the share list.",
        },
        "jase": {
            "name": "Jase",
            "idle": "He tests the peat face with a spade.",
        },
        "willa": {
            "name": "Willa",
            "idle": "She counts bricks and does not stack uneven.",
        },
        "rook": {
            "name": "Rook",
            "idle": "He squints at the empty frame.",
        },
        "nim": {
            "name": "Nim",
            "idle": "She sorts shards and keeps her gloves on.",
        },
        "lise": {
            "name": "Lise",
            "idle": "She holds a sun chart to the hole.",
        },
        "tess": {
            "name": "Tess",
            "idle": "She keeps a hook in her belt and waits.",
        },
        "bram": {
            "name": "Bram",
            "idle": "He spins a short strand and does not look up.",
        },
        "kite": {
            "name": "Kite",
            "idle": "He weighs a purse and watches the far pegs.",
        },
        "dorr": {
            "name": "Dorr",
            "idle": "He leans on a rake and watches the beds.",
        },
        "nell": {
            "name": "Nell",
            "idle": "She keeps the brine bucket from the well lip.",
        },
        "pim": {
            "name": "Pim",
            "idle": "He taps the scale and waits for a cake.",
        },
        "hal": {
            "name": "Hal",
            "idle": "He rubs salt from his palms and waits.",
        },
        "bea": {
            "name": "Bea",
            "idle": "She feeds chips to the hearth and watches the haze.",
        },
        "wren": {
            "name": "Wren",
            "idle": "She taps a tally stick and eyes the pegs.",
        },
        "cess": {
            "name": "Cess",
            "idle": "She mends a mouth of wicker and waits.",
        },
        "noll": {
            "name": "Noll",
            "idle": "He watches the pool and does not splash.",
        },
        "meg": {
            "name": "Meg",
            "idle": "She keeps a tally stick by the door.",
        },
        "quill": {
            "name": "Quill",
            "idle": "He rubs stain from his wrists and waits.",
        },
        "fen": {
            "name": "Fen",
            "idle": "She stirs a vat and does not splash.",
        },
        "moss": {
            "name": "Moss",
            "idle": "She holds a dry line and watches the poles.",
        },
        "bex": {
            "name": "Bex",
            "idle": "He keeps a token box shut and waits.",
        },
        "ivo": {
            "name": "Ivo",
            "idle": "He holds the line and watches the hull.",
        },
        "ama": {
            "name": "Ama",
            "idle": "She holds a stamp and does not smile.",
        },
        "od": {
            "name": "Od",
            "idle": "He watches the vanes and does not speak first.",
        },
        "rusk": {
            "name": "Rusk",
            "idle": "She holds a pin and eyes the loose sails.",
        },
        "hobb": {
            "name": "Hobb",
            "idle": "He tests the clay lip with a board.",
        },
        "wex": {
            "name": "Wex",
            "idle": "He keeps a thumb on the bed list.",
        },
        "pip": {
            "name": "Pip",
            "idle": "She fans the spat trays and waits.",
        },
        "gell": {
            "name": "Gell",
            "idle": "He tests a shell and does not smile.",
        },
        "voss": {
            "name": "Voss",
            "idle": "He keeps a thumb on the open roll.",
        },
        "rhee": {
            "name": "Rhee",
            "idle": "She taps the quill and waits.",
        },
        "orm": {
            "name": "Orm",
            "idle": "He holds a seal and does not speak first.",
        },
        "yul": {
            "name": "Yul",
            "idle": "He wraps straw around a block and waits.",
        },
        "saff": {
            "name": "Saff",
            "idle": "She tests the ice face with a saw.",
        },
        "kest": {
            "name": "Kest",
            "idle": "He keeps one hand on the bar.",
        },
        "luth": {
            "name": "Luth",
            "idle": "He keeps a wreck list under his arm.",
        },
        "kade": {
            "name": "Kade",
            "idle": "She watches the silt and does not wade yet.",
        },
        "efa": {
            "name": "Efa",
            "idle": "She keeps both palms on the altar rim.",
        },
        "sol": {
            "name": "Sol",
            "idle": "He listens to the hive and does not speak first.",
        },
        "tansy": {
            "name": "Tansy",
            "idle": "She keeps a rag of smoke and waits.",
        },
        "wick": {
            "name": "Wick",
            "idle": "He mends a straw skep and does not look up.",
        },
        "hop": {
            "name": "Hop",
            "idle": "He sniffs the mash and does not speak first.",
        },
        "mal": {
            "name": "Mal",
            "idle": "She turns the mash and waits.",
        },
        "sera": {
            "name": "Sera",
            "idle": "He keeps a tap peg and does not look up.",
        },
    }

    actions = [
        action(
            "use_marsh_cant",
            "Use marsh cant",
            "talk",
            {"all": [{"at": "saltfen.market"}, {"sheet": ["tongue", "cant"]}]},
            "You speak low marsh cant. The eel-seller nods.",
            [
                {"op": "set_flag", "flag": "marsh_friend"},
                {"op": "remember", "actor": "eel_seller", "fact": "spoke_cant"},
                {"op": "add_rep", "faction": "dockers", "n": 1},
            ],
        ),
        action(
            "show_city_papers",
            "Show city papers",
            "talk",
            {"all": [{"at": "saltfen.market"}, {"has_item": "city_papers"}]},
            "You show city papers. A watch pair eases back.",
            [
                {"op": "set_flag", "flag": "watch_trust"},
                {"op": "remember", "actor": "eel_seller", "fact": "saw_papers"},
                {"op": "add_rep", "faction": "watch", "n": 1},
            ],
        ),
        action(
            "call_the_watch",
            "Call the watch",
            "talk",
            {
                "all": [
                    {"at": "saltfen.market"},
                    {
                        "any": [
                            {"sheet": ["creed", "oathbound"]},
                            {"sheet": ["origin", "cityward"]},
                        ]
                    },
                ]
            },
            "You call the watch. They drag a cutpurse off the stalls.",
            [
                {"op": "set_flag", "flag": "thief_jailed"},
                {"op": "add_rep", "faction": "watch", "n": 1},
                {"op": "add_rep", "faction": "stackers", "n": -2},
            ],
        ),
        action(
            "slip_behind_stall",
            "Slip behind the stall",
            "do",
            {
                "all": [
                    {"at": "saltfen.market"},
                    {
                        "any": [
                            {"sheet": ["body", "agile"]},
                            {"sheet": ["skill", "hunt"]},
                        ]
                    },
                ]
            },
            "You slide into the stall gap. You hear talk of a warehouse chest.",
            [{"op": "set_flag", "flag": "heard_tablet"}],
        ),
        action(
            "threaten_seller",
            "Threaten the seller",
            "talk",
            {"all": [{"at": "saltfen.market"}, {"sheet": ["body", "might"]}]},
            "You crowd the board. He talks fast about a tablet in the warehouse.",
            [
                {"op": "set_flag", "flag": "heard_tablet"},
                {"op": "add_rep", "faction": "dockers", "n": -1},
            ],
        ),
        action(
            "buy_eels",
            "Buy smoked eels",
            "talk",
            {"at": "saltfen.market"},
            "You buy smoked eels. Salt stings your lips.",
            [{"op": "set_flag", "flag": "ate_eels"}],
        ),
        action(
            "ask_about_tablet",
            "Ask about the tablet",
            "talk",
            {
                "all": [
                    {"at": "saltfen.market"},
                    {
                        "any": [
                            {"has_flag": "marsh_friend"},
                            {"has_flag": "watch_trust"},
                            {"has_flag": "heard_tablet"},
                        ]
                    },
                ]
            },
            "He says the old compact tablet sits in the warehouse chest.",
            [{"op": "set_flag", "flag": "heard_tablet"}],
        ),
        action(
            "slip_inside",
            "Slip inside the warehouse",
            "do",
            {
                "all": [
                    {"at": "saltfen.market"},
                    {"not_flag": "warehouse_open"},
                    {
                        "any": [
                            {"sheet": ["body", "agile"]},
                            {"sheet": ["skill", "hunt"]},
                        ]
                    },
                ]
            },
            "You slip the side latch. The warehouse takes you in.",
            [
                {"op": "set_flag", "flag": "warehouse_open"},
                {"op": "move", "to": "saltfen.warehouse"},
            ],
        ),
        action(
            "force_the_door",
            "Force the warehouse door",
            "do",
            {
                "all": [
                    {"at": "saltfen.market"},
                    {"not_flag": "warehouse_open"},
                    {"sheet": ["body", "might"]},
                ]
            },
            "You force the bar. The door jumps. A watch horn sounds far off.",
            [
                {"op": "set_flag", "flag": "warehouse_open"},
                {"op": "move", "to": "saltfen.warehouse"},
                {"op": "add_rep", "faction": "watch", "n": -1},
            ],
        ),
        action(
            "show_seal_at_door",
            "Show seal at the warehouse",
            "do",
            {
                "all": [
                    {"at": "saltfen.market"},
                    {"not_flag": "warehouse_open"},
                    {"sheet": ["origin", "cityward"]},
                ]
            },
            "You show the city seal. The ware-hand opens the door.",
            [
                {"op": "set_flag", "flag": "warehouse_open"},
                {"op": "move", "to": "saltfen.warehouse"},
                {"op": "add_rep", "faction": "watch", "n": 1},
            ],
        ),
        action(
            "give_tablet",
            "Give tablet to the boss",
            "talk",
            {"all": [{"at": "saltfen.dock"}, {"has_item": "compact_tablet"}]},
            "You set the tablet on his crate. He reads and lets out a breath.",
            [
                {"op": "remove_item", "item": "compact_tablet"},
                {"op": "set_flag", "flag": "tablet_given"},
                {"op": "add_rep", "faction": "dockers", "n": 2},
            ],
        ),
        action(
            "sign_the_compact",
            "Sign the dock compact",
            "talk",
            {
                "all": [
                    {"at": "saltfen.dock"},
                    {"has_flag": "tablet_given"},
                    {
                        "any": [
                            {"rep_gte": ["dockers", 1]},
                            {"sheet": ["creed", "oathbound"]},
                        ]
                    },
                    {"not_flag": "compact_restored"},
                ]
            },
            "You sign. The crew repeat the compact in one voice.",
            [{"op": "set_flag", "flag": "compact_restored"}],
        ),
        action(
            "ask_boss_for_work",
            "Ask the boss for work",
            "talk",
            {"at": "saltfen.dock"},
            "He says the compact tablet is gone. Find it and the dock will hold.",
            [{"op": "set_flag", "flag": "heard_tablet"}],
        ),
        action(
            "report_thief",
            "Report the cutpurse",
            "talk",
            {
                "all": [
                    {"at": "saltfen.watchhouse"},
                    {"has_flag": "thief_jailed"},
                ]
            },
            "The sergeant logs the arrest. She says the stacks will hear of it.",
            [{"op": "add_rep", "faction": "watch", "n": 1}],
        ),
        action(
            "ask_watch_about_tablet",
            "Ask the watch about the tablet",
            "talk",
            {
                "all": [
                    {"at": "saltfen.watchhouse"},
                    {
                        "any": [
                            {"sheet": ["tongue", "court"]},
                            {"sheet": ["origin", "cityward"]},
                            {"has_flag": "watch_trust"},
                        ]
                    },
                ]
            },
            "She says the tablet is in the warehouse. Papers will open the door.",
            [{"op": "set_flag", "flag": "heard_tablet"}],
        ),
        action(
            "buy_stew",
            "Buy stew",
            "talk",
            {"at": "saltfen.inn"},
            "You eat hot stew. Your hands steady.",
            [{"op": "heal", "n": 1}],
        ),
        action(
            "rent_cot",
            "Rent a cot",
            "do",
            {"at": "saltfen.inn"},
            "You lie down. The room ticks and you rise clearer.",
            [{"op": "heal", "n": 2}],
        ),
        action(
            "hear_gossip",
            "Hear gossip",
            "talk",
            {"at": "saltfen.inn"},
            "A climber says the wind bridge needs a crawl, not a dash.",
            [{"op": "set_flag", "flag": "heard_bridge"}],
        ),
        action(
            "wade_mudflat",
            "Wade the mudflat",
            "do",
            {
                "all": [
                    {"at": "saltfen.tidegate"},
                    {"tide": "low"},
                    {"not_flag": "found_brass_key"},
                ]
            },
            "You wade the low mud. A brass key sits in a drowned boot.",
            [
                {"op": "add_item", "item": "brass_key"},
                {"op": "set_flag", "flag": "found_brass_key"},
            ],
        ),
        action(
            "sort_the_heap",
            "Sort the heap",
            "do",
            {
                "all": [
                    {"at": "saltfen.salvage"},
                    {"sheet": ["skill", "craft"]},
                    {"not_flag": "found_brass_key"},
                ]
            },
            "You sort tags by metal. A brass key hides under a plate.",
            [
                {"op": "add_item", "item": "brass_key"},
                {"op": "set_flag", "flag": "found_brass_key"},
            ],
        ),
        action(
            "open_warehouse_chest",
            "Open the side chest",
            "do",
            {
                "all": [
                    {"at": "saltfen.warehouse"},
                    {"has_item": "brass_key"},
                    {"not_flag": "chest_open"},
                ]
            },
            "The brass key turns. Extra rope sits in the chest.",
            [
                {"op": "set_flag", "flag": "chest_open"},
                {"op": "add_item", "item": "frayed_rope"},
            ],
        ),
        action(
            "help_runner",
            "Help the runner",
            "talk",
            {
                "all": [
                    {"at": "ashfen.causeway"},
                    {"not_flag": "runner_helped"},
                    {"not_flag": "runner_robbed"},
                ]
            },
            "You bind her knee. She says Mira at the stacks will mark you kind.",
            [
                {"op": "set_flag", "flag": "runner_helped"},
                {"op": "add_rep", "faction": "stackers", "n": 1},
                {"op": "remember", "actor": "wounded_runner", "fact": "helped"},
            ],
        ),
        action(
            "rob_runner",
            "Rob the runner",
            "do",
            {
                "all": [
                    {"at": "ashfen.causeway"},
                    {"not_flag": "runner_helped"},
                    {"not_flag": "runner_robbed"},
                    {
                        "any": [
                            {"sheet": ["creed", "freehand"]},
                            {"sheet": ["mark", "branded"]},
                        ]
                    },
                ]
            },
            "You take her coil. She swears the stacks will hear.",
            [
                {"op": "set_flag", "flag": "runner_robbed"},
                {"op": "add_item", "item": "frayed_rope"},
                {"op": "add_rep", "faction": "stackers", "n": -2},
            ],
        ),
        action(
            "climb_switchback",
            "Climb the switchback",
            "do",
            {
                "all": [
                    {"at": "stacks.base"},
                    {
                        "any": [
                            {"sheet": ["body", "agile"]},
                            {"has_item": "frayed_rope"},
                        ]
                    },
                ]
            },
            "You take the outer path. The first ledge holds.",
            [{"op": "move", "to": "stacks.switchback"}],
        ),
        action(
            "force_climb",
            "Force a climb",
            "do",
            {
                "all": [
                    {"at": "stacks.base"},
                    {"sheet": ["body", "might"]},
                ]
            },
            "You haul on stone and rope. The wall gives you a hold.",
            [{"op": "move", "to": "stacks.switchback"}],
        ),
        action(
            "ask_mira_for_tip",
            "Ask Mira for a tip",
            "talk",
            {
                "all": [
                    {"at": "stacks.base"},
                    {"rep_gte": ["stackers", 0]},
                    {"not_flag": "thief_jailed"},
                ]
            },
            "Mira says crawl the wind bridge. Dashing drops fools.",
            [{"op": "set_flag", "flag": "heard_bridge"}],
        ),
        action(
            "share_marsh_path",
            "Share marsh path with Mira",
            "talk",
            {
                "all": [
                    {"at": "stacks.base"},
                    {"has_flag": "marsh_friend"},
                ]
            },
            "You share the marsh path. Mira marks a hidden flue.",
            [
                {"op": "set_flag", "flag": "mira_marsh_tip"},
                {"op": "remember", "actor": "mira", "fact": "marsh_path"},
            ],
        ),
        action(
            "climb_to_mid",
            "Climb to the mid ledge",
            "do",
            {"at": "stacks.switchback"},
            "You work up the inner stair. The mid ledge opens.",
            [{"op": "move", "to": "stacks.midledge"}],
        ),
        action(
            "rest_on_ledge",
            "Rest on the ledge",
            "do",
            {"at": "stacks.midledge"},
            "You sit out of the wind. Your breath comes back.",
            [{"op": "heal", "n": 1}],
        ),
        action(
            "climb_to_bridge",
            "Climb to the wind bridge",
            "do",
            {"at": "stacks.midledge"},
            "You take the last stair. Planks wait over the gap.",
            [{"op": "move", "to": "stacks.windbridge"}],
        ),
        action(
            "crawl_across",
            "Crawl across the bridge",
            "do",
            {"at": "stacks.windbridge"},
            "You crawl the planks. The relic room is close.",
            [{"op": "move", "to": "stacks.relic"}],
        ),
        action(
            "dash_across",
            "Dash across the bridge",
            "do",
            {"all": [{"at": "stacks.windbridge"}, {"sheet": ["body", "agile"]}]},
            "You dash. The planks hold for your light step.",
            [{"op": "move", "to": "stacks.relic"}],
        ),
        action(
            "brace_planks",
            "Brace the planks",
            "do",
            {"all": [{"at": "stacks.windbridge"}, {"sheet": ["body", "hardy"]}]},
            "You brace the worst plank and cross slow.",
            [{"op": "move", "to": "stacks.relic"}],
        ),
        action(
            "cut_guyline",
            "Cut the guyline",
            "do",
            {
                "all": [
                    {"at": "stacks.windbridge"},
                    {"sheet": ["creed", "freehand"]},
                    {"not_flag": "guyline_cut"},
                ]
            },
            "You cut the guyline. The span sags toward the undercroft.",
            [
                {"op": "set_flag", "flag": "guyline_cut"},
                {"op": "add_rep", "faction": "stackers", "n": -1},
            ],
        ),
        action(
            "drop_to_undercroft",
            "Drop to the undercroft",
            "do",
            {"all": [{"at": "stacks.windbridge"}, {"has_flag": "guyline_cut"}]},
            "You drop into the vault. Beams groan above.",
            [{"op": "move", "to": "stacks.undercroft"}],
        ),
        action(
            "squeeze_to_relic",
            "Squeeze up to the relic",
            "do",
            {
                "all": [
                    {"at": "stacks.undercroft"},
                    {
                        "any": [
                            {"sheet": ["body", "agile"]},
                            {"sheet": ["skill", "craft"]},
                        ]
                    },
                ]
            },
            "You squeeze a cracked flue. The relic room opens above.",
            [{"op": "move", "to": "stacks.relic"}],
        ),
        action(
            "shore_the_beam",
            "Shore the beam",
            "do",
            {
                "all": [
                    {"at": "stacks.undercroft"},
                    {
                        "any": [
                            {"sheet": ["body", "might"]},
                            {"sheet": ["skill", "craft"]},
                        ]
                    },
                    {"not_flag": "beam_shored"},
                ]
            },
            "You shore the beam. The vault stops its grind.",
            [{"op": "set_flag", "flag": "beam_shored"}],
        ),
        action(
            "copy_inscription",
            "Copy the inscription",
            "do",
            {
                "all": [
                    {"at": "stacks.relic"},
                    {"sheet": ["skill", "letters"]},
                    {"not_flag": "copied_inscription"},
                ]
            },
            "You copy the bowl script. The lines name the compact as a later law.",
            [{"op": "set_flag", "flag": "copied_inscription"}],
        ),
        action(
            "leave_offering",
            "Leave an offering",
            "do",
            {
                "all": [
                    {"at": "stacks.relic"},
                    {"sheet": ["creed", "oathbound"]},
                    {"not_flag": "left_offering"},
                ]
            },
            "You leave a strip of cloth. The bowl stays still.",
            [{"op": "set_flag", "flag": "left_offering"}],
        ),
        action(
            "offer_reed_grain",
            "Offer reed grain",
            "talk",
            {
                "all": [
                    {"at": "mill.yard"},
                    {"sheet": ["origin", "marshborn"]},
                    {"not_flag": "mill_trust"},
                ]
            },
            "You offer reed grain. Brann marks your name kind.",
            [
                {"op": "set_flag", "flag": "mill_trust"},
                {"op": "remember", "actor": "miller", "fact": "reed_grain"},
                {"op": "add_rep", "faction": "millers", "n": 1},
            ],
        ),
        action(
            "read_debt_ledger",
            "Read the debt ledger",
            "talk",
            {
                "all": [
                    {"at": "mill.yard"},
                    {"sheet": ["skill", "letters"]},
                    {"not_flag": "mill_ledger_read"},
                ]
            },
            "You read the board. The mill holds the valley grain as debt.",
            [
                {"op": "set_flag", "flag": "mill_ledger_read"},
                {"op": "remember", "actor": "miller", "fact": "saw_ledger"},
            ],
        ),
        action(
            "show_mill_papers",
            "Show city papers",
            "talk",
            {
                "all": [
                    {"at": "mill.yard"},
                    {"has_item": "city_papers"},
                    {"not_flag": "mill_saw_papers"},
                ]
            },
            "You show city papers. Sila's cousin at the board goes still.",
            [
                {"op": "set_flag", "flag": "mill_saw_papers"},
                {"op": "add_rep", "faction": "millers", "n": -1},
            ],
        ),
        action(
            "cite_dock_compact",
            "Cite the dock compact",
            "talk",
            {
                "all": [
                    {"at": "mill.yard"},
                    {"has_flag": "compact_restored"},
                    {"not_flag": "mill_honors_compact"},
                ]
            },
            "You cite the dock compact. Brann drops the extra grain tax.",
            [
                {"op": "set_flag", "flag": "mill_honors_compact"},
                {"op": "set_flag", "flag": "mill_trust"},
                {"op": "remember", "actor": "miller", "fact": "dock_rates"},
                {"op": "add_rep", "faction": "millers", "n": 1},
            ],
        ),
        action(
            "swear_mill_oath",
            "Swear the mill oath",
            "talk",
            {
                "all": [
                    {"at": "mill.yard"},
                    {"has_flag": "mill_ledger_read"},
                    {"sheet": ["creed", "oathbound"]},
                    {"not_flag": "mill_trust"},
                ]
            },
            "You swear on the board. Brann takes the oath as bond.",
            [
                {"op": "set_flag", "flag": "mill_trust"},
                {"op": "remember", "actor": "miller", "fact": "oath"},
            ],
        ),
        action(
            "pay_with_grain",
            "Pay with a grain sack",
            "talk",
            {
                "all": [
                    {"at": "mill.yard"},
                    {"has_item": "grain_sack"},
                    {"not_flag": "mill_trust"},
                ]
            },
            "You set a sack on the board. Brann cuts your name from debt.",
            [
                {"op": "remove_item", "item": "grain_sack"},
                {"op": "set_flag", "flag": "mill_trust"},
                {"op": "add_rep", "faction": "millers", "n": 1},
            ],
        ),
        action(
            "kindle_kiln",
            "Kindle the kiln",
            "do",
            {
                "all": [
                    {"at": "mill.kiln"},
                    {"not_flag": "kiln_lit"},
                    {"not_flag": "kiln_hot"},
                ]
            },
            "You kindle the kiln. Heat crawls up the brick.",
            [{"op": "set_flag", "flag": "kiln_lit"}],
        ),
        action(
            "stoke_kiln",
            "Stoke the kiln",
            "do",
            {
                "all": [
                    {"at": "mill.kiln"},
                    {"has_flag": "kiln_lit"},
                    {"not_flag": "kiln_hot"},
                ]
            },
            "You stoke until the kiln runs white.",
            [
                {"op": "clear_flag", "flag": "kiln_lit"},
                {"op": "set_flag", "flag": "kiln_hot"},
            ],
        ),
        action(
            "damp_kiln",
            "Damp the kiln",
            "do",
            {"all": [{"at": "mill.kiln"}, {"has_flag": "kiln_hot"}]},
            "You damp the mouth. The white heat falls back.",
            [
                {"op": "clear_flag", "flag": "kiln_hot"},
                {"op": "set_flag", "flag": "kiln_lit"},
            ],
        ),
        action(
            "set_damper",
            "Set the damper",
            "do",
            {
                "all": [
                    {"at": "mill.kiln"},
                    {"sheet": ["skill", "craft"]},
                    {"not_flag": "damper_set"},
                ]
            },
            "You set the damper. Pell nods at the even draw.",
            [
                {"op": "set_flag", "flag": "damper_set"},
                {"op": "remember", "actor": "pell", "fact": "damper"},
            ],
        ),
        action(
            "ask_pell_heat",
            "Ask Pell about heat",
            "talk",
            {"all": [{"at": "mill.kiln"}, {"has_flag": "mill_trust"}]},
            "Pell says fire the pact only when the mouth runs white.",
            [{"op": "set_flag", "flag": "heard_kiln"}],
        ),
        action(
            "fire_the_pact",
            "Fire the grain pact",
            "do",
            {
                "all": [
                    {"at": "mill.kiln"},
                    {"has_flag": "kiln_hot"},
                    {"has_flag": "mill_trust"},
                    {"not_flag": "kiln_pact_sealed"},
                ]
            },
            "You press the debt strip into the kiln. Brann names the pact sealed.",
            [{"op": "set_flag", "flag": "kiln_pact_sealed"}],
        ),
        action(
            "force_the_sluice",
            "Force the sluice stone",
            "do",
            {
                "all": [
                    {"at": "mill.sluice"},
                    {"sheet": ["body", "might"]},
                    {"not_flag": "sluice_true"},
                ]
            },
            "You force the stone true. The wheel runs even.",
            [
                {"op": "set_flag", "flag": "sluice_true"},
                {"op": "add_rep", "faction": "millers", "n": 1},
            ],
        ),
        action(
            "ask_sila_debt",
            "Ask Sila about debt",
            "talk",
            {"at": "mill.loft"},
            "Sila says the kiln pact is the only clean write-off.",
            [{"op": "set_flag", "flag": "heard_kiln"}],
        ),
        action(
            "speak_reed_custom",
            "Speak reed custom",
            "talk",
            {
                "all": [
                    {"at": "court.hall"},
                    {
                        "any": [
                            {"sheet": ["origin", "marshborn"]},
                            {"sheet": ["tongue", "cant"]},
                        ]
                    },
                    {"not_flag": "court_standing"},
                ]
            },
            "You speak reed custom. Orin grants you standing.",
            [
                {"op": "set_flag", "flag": "court_standing"},
                {"op": "remember", "actor": "magistrate", "fact": "reed_custom"},
                {"op": "add_rep", "faction": "court", "n": 1},
            ],
        ),
        action(
            "cite_city_law",
            "Cite city law",
            "talk",
            {
                "all": [
                    {"at": "court.hall"},
                    {
                        "any": [
                            {"sheet": ["origin", "cityward"]},
                            {"sheet": ["tongue", "court"]},
                        ]
                    },
                    {"not_flag": "court_standing"},
                ]
            },
            "You cite city law. Orin grants you standing.",
            [
                {"op": "set_flag", "flag": "court_standing"},
                {"op": "remember", "actor": "magistrate", "fact": "city_law"},
                {"op": "add_rep", "faction": "court", "n": 1},
            ],
        ),
        action(
            "name_mill_pact",
            "Name the mill pact",
            "talk",
            {
                "all": [
                    {"at": "court.hall"},
                    {"has_flag": "kiln_pact_sealed"},
                    {"not_flag": "court_named_mill"},
                ]
            },
            "You name the mill pact. Orin takes it as clean proof.",
            [
                {"op": "set_flag", "flag": "court_named_mill"},
                {"op": "set_flag", "flag": "court_standing"},
                {"op": "remember", "actor": "magistrate", "fact": "mill_pact"},
            ],
        ),
        action(
            "hear_tam_witness",
            "Hear Tam as witness",
            "talk",
            {
                "all": [
                    {"at": "court.cell"},
                    {"not_flag": "witness_heard"},
                ]
            },
            "Tam names the grain theft. He saw the cut at dusk.",
            [
                {"op": "set_flag", "flag": "witness_heard"},
                {"op": "remember", "actor": "tam", "fact": "spoke"},
            ],
        ),
        action(
            "swear_true_witness",
            "Swear true witness",
            "talk",
            {
                "all": [
                    {"at": "court.hall"},
                    {"has_flag": "witness_heard"},
                    {"sheet": ["creed", "oathbound"]},
                    {"not_flag": "swore_witness"},
                ]
            },
            "You swear Tam spoke true. Orin records the oath.",
            [
                {"op": "set_flag", "flag": "swore_witness"},
                {"op": "add_rep", "faction": "court", "n": 1},
            ],
        ),
        action(
            "read_reed_charter",
            "Read the reed charter",
            "do",
            {
                "all": [
                    {"at": "court.archive"},
                    {"sheet": ["skill", "letters"]},
                    {"not_flag": "read_charter"},
                ]
            },
            "You read the charter. Sentence needs a heard witness.",
            [{"op": "set_flag", "flag": "read_charter"}],
        ),
        action(
            "pass_reed_sentence",
            "Pass the reed sentence",
            "talk",
            {
                "all": [
                    {"at": "court.hall"},
                    {"has_flag": "court_standing"},
                    {"has_flag": "witness_heard"},
                    {"not_flag": "reed_sentence_passed"},
                ]
            },
            "You pass sentence. Orin strikes the mat once.",
            [
                {"op": "set_flag", "flag": "reed_sentence_passed"},
                {"op": "add_rep", "faction": "court", "n": 2},
            ],
        ),
        action(
            "ask_kesh_rule",
            "Ask Kesh the rule",
            "talk",
            {"at": "court.gate"},
            "Kesh says standing first, then a witness, then a sentence.",
            [{"op": "set_flag", "flag": "heard_court_rule"}],
        ),
        action(
            "ask_nia_rolls",
            "Ask Nia for a roll",
            "talk",
            {"at": "court.archive"},
            "Nia says the charter is short. Witness, then sentence.",
            [{"op": "set_flag", "flag": "heard_court_rule"}],
        ),
        action(
            "track_drowned_prints",
            "Track drowned prints",
            "do",
            {
                "all": [
                    {"at": "road.hut"},
                    {"sheet": ["skill", "hunt"]},
                    {"not_flag": "road_trust"},
                ]
            },
            "You track wet prints to the beacon path. Cal nods.",
            [
                {"op": "set_flag", "flag": "road_trust"},
                {"op": "remember", "actor": "cal", "fact": "tracks"},
            ],
        ),
        action(
            "force_hut_latch",
            "Force the hut latch",
            "do",
            {
                "all": [
                    {"at": "road.hut"},
                    {"sheet": ["body", "might"]},
                    {"not_flag": "road_trust"},
                ]
            },
            "You force the latch. Cal lets you take the lamp oil.",
            [
                {"op": "set_flag", "flag": "road_trust"},
                {"op": "remember", "actor": "cal", "fact": "forced"},
            ],
        ),
        action(
            "name_the_sentence",
            "Name the reed sentence",
            "talk",
            {
                "all": [
                    {"at": "road.hut"},
                    {"has_flag": "reed_sentence_passed"},
                    {"not_flag": "road_named_sentence"},
                ]
            },
            "You name the reed sentence. Cal grants the road as owed.",
            [
                {"op": "set_flag", "flag": "road_named_sentence"},
                {"op": "set_flag", "flag": "road_trust"},
                {"op": "remember", "actor": "cal", "fact": "sentence"},
            ],
        ),
        action(
            "walk_the_flood_berm",
            "Walk the flood berm",
            "do",
            {
                "all": [
                    {"at": "road.dike"},
                    {"weather": "rain"},
                    {"not_flag": "walked_berm"},
                ]
            },
            "Rain lifts the berm path. You mark a dry line to the beacon.",
            [
                {"op": "set_flag", "flag": "walked_berm"},
                {"op": "set_flag", "flag": "road_trust"},
            ],
        ),
        action(
            "follow_the_bell",
            "Follow the fog bell",
            "do",
            {
                "all": [
                    {"at": "road.dike"},
                    {"weather": "fog"},
                    {"not_flag": "followed_bell"},
                ]
            },
            "You follow the bell through fog. The beacon post shows.",
            [{"op": "set_flag", "flag": "followed_bell"}],
        ),
        action(
            "ask_rell_weather",
            "Ask Rell the weather",
            "talk",
            {"at": "road.dike"},
            "Rell says rain opens the berm. Fog hides the bell path.",
            [{"op": "set_flag", "flag": "heard_weather"}],
        ),
        action(
            "light_the_beacon",
            "Light the road beacon",
            "do",
            {
                "all": [
                    {"at": "road.beacon"},
                    {"has_flag": "road_trust"},
                    {"not_flag": "beacon_lit"},
                ]
            },
            "You light the pan. The drowned road holds a line of fire.",
            [{"op": "set_flag", "flag": "beacon_lit"}],
        ),
        action(
            "wade_drownway_rain",
            "Wade the drownway",
            "do",
            {
                "all": [
                    {"at": "road.drownway"},
                    {"weather": "rain"},
                    {"not_flag": "waded_drownway"},
                ]
            },
            "You wade the rain cut. Poles lead you true.",
            [{"op": "set_flag", "flag": "waded_drownway"}],
        ),
        action(
            "cut_reed_herb",
            "Cut reed herb",
            "do",
            {
                "all": [
                    {"at": "camp.yard"},
                    {
                        "any": [
                            {"sheet": ["origin", "marshborn"]},
                            {"sheet": ["skill", "hunt"]},
                        ]
                    },
                    {"not_flag": "herb_found"},
                ]
            },
            "You cut reed herb. Joss lets you pass the still.",
            [
                {"op": "set_flag", "flag": "herb_found"},
                {"op": "remember", "actor": "joss", "fact": "herb"},
            ],
        ),
        action(
            "read_isolation_order",
            "Read the isolation order",
            "do",
            {
                "all": [
                    {"at": "camp.yard"},
                    {"sheet": ["skill", "letters"]},
                    {"not_flag": "recipe_known"},
                ]
            },
            "You read the isolation order. It names the still recipe.",
            [
                {"op": "set_flag", "flag": "recipe_known"},
                {"op": "remember", "actor": "joss", "fact": "order"},
            ],
        ),
        action(
            "hail_clean_boat",
            "Hail the clean boat",
            "do",
            {
                "all": [
                    {"at": "camp.gate"},
                    {"has_flag": "beacon_lit"},
                    {"not_flag": "camp_boat"},
                ]
            },
            "You hail a clean boat. Cloth and oil come ashore.",
            [
                {"op": "set_flag", "flag": "camp_boat"},
                {"op": "set_flag", "flag": "fever_trust"},
                {"op": "remember", "actor": "joss", "fact": "boat"},
            ],
        ),
        action(
            "brew_fever_broth",
            "Brew fever broth",
            "do",
            {
                "all": [
                    {"at": "camp.still"},
                    {
                        "any": [
                            {"has_flag": "herb_found"},
                            {"has_flag": "recipe_known"},
                        ]
                    },
                    {"not_flag": "broth_made"},
                ]
            },
            "You brew a bitter broth. The steam turns green.",
            [
                {"op": "set_flag", "flag": "broth_made"},
                {"op": "remember", "actor": "oat", "fact": "brewed"},
            ],
        ),
        action(
            "give_broth_to_ren",
            "Give Ren the broth",
            "talk",
            {
                "all": [
                    {"at": "camp.ward"},
                    {"has_flag": "broth_made"},
                    {"not_flag": "fever_broken"},
                ]
            },
            "You give Ren the broth. His breath lengthens.",
            [
                {"op": "set_flag", "flag": "fever_broken"},
                {"op": "remember", "actor": "ren", "fact": "drank"},
            ],
        ),
        action(
            "lime_the_pits",
            "Lime the pits",
            "do",
            {
                "all": [
                    {"at": "camp.pits"},
                    {
                        "any": [
                            {"sheet": ["skill", "craft"]},
                            {"sheet": ["body", "hardy"]},
                        ]
                    },
                    {"not_flag": "pits_limed"},
                ]
            },
            "You lime the pits. The air hurts less.",
            [{"op": "set_flag", "flag": "pits_limed"}],
        ),
        action(
            "ask_joss_rule",
            "Ask Joss the rule",
            "talk",
            {"at": "camp.yard"},
            "Joss says brew first. Then the ward can rest.",
            [{"op": "set_flag", "flag": "heard_fever_rule"}],
        ),
        action(
            "ask_oat_still",
            "Ask Oat the still",
            "talk",
            {"at": "camp.still"},
            "Oat says the still needs herb or the written order.",
            [{"op": "set_flag", "flag": "heard_fever_rule"}],
        ),
        action(
            "speak_the_old_name",
            "Speak the old name",
            "talk",
            {
                "all": [
                    {"at": "name.hall"},
                    {
                        "any": [
                            {"sheet": ["origin", "marshborn"]},
                            {"sheet": ["tongue", "cant"]},
                        ]
                    },
                    {"not_flag": "name_standing"},
                ]
            },
            "You speak the old name. Venn grants you the wall.",
            [
                {"op": "set_flag", "flag": "name_standing"},
                {"op": "remember", "actor": "venn", "fact": "old_name"},
            ],
        ),
        action(
            "copy_the_bone_name",
            "Copy the bone name",
            "do",
            {
                "all": [
                    {"at": "name.hall"},
                    {"sheet": ["skill", "letters"]},
                    {"not_flag": "name_standing"},
                ]
            },
            "You copy the missing name. Venn grants you the wall.",
            [
                {"op": "set_flag", "flag": "name_standing"},
                {"op": "remember", "actor": "venn", "fact": "copied"},
            ],
        ),
        action(
            "file_ren_living",
            "File Ren as living",
            "talk",
            {
                "all": [
                    {"at": "name.hall"},
                    {"has_flag": "fever_broken"},
                    {"not_flag": "ren_filed"},
                ]
            },
            "You file Ren as living. Venn marks the wall for the living.",
            [
                {"op": "set_flag", "flag": "ren_filed"},
                {"op": "set_flag", "flag": "name_standing"},
                {"op": "remember", "actor": "venn", "fact": "ren_live"},
            ],
        ),
        action(
            "restore_the_name",
            "Restore the name",
            "do",
            {
                "all": [
                    {"at": "name.hall"},
                    {"has_item": "bone_name"},
                    {"has_flag": "name_standing"},
                    {"not_flag": "name_restored"},
                ]
            },
            "You set the bone name in the niche. The wall holds.",
            [
                {"op": "remove_item", "item": "bone_name"},
                {"op": "set_flag", "flag": "name_restored"},
            ],
        ),
        action(
            "ask_venn_rule",
            "Ask Venn the rule",
            "talk",
            {"at": "name.hall"},
            "Venn says speak or copy. Then set the stolen name back.",
            [{"op": "set_flag", "flag": "heard_name_rule"}],
        ),
        action(
            "ask_ila_tags",
            "Ask Ila about tags",
            "talk",
            {"at": "name.yard"},
            "Ila points at the crypt. The stolen tag lies there.",
            [{"op": "set_flag", "flag": "heard_name_rule"}],
        ),
        action(
            "ask_sarn_ink",
            "Ask Sarn for ink",
            "talk",
            {"at": "name.script"},
            "Sarn says letters can copy a name the mouth cannot hold.",
            [{"op": "set_flag", "flag": "heard_name_rule"}],
        ),
        action(
            "know_the_soft_cut",
            "Know the soft cut",
            "talk",
            {
                "all": [
                    {"at": "fold.green"},
                    {
                        "any": [
                            {"sheet": ["origin", "marshborn"]},
                            {"sheet": ["skill", "hunt"]},
                        ]
                    },
                    {"not_flag": "fold_trust"},
                ]
            },
            "You name the soft seam. Brin lets you cut for the share.",
            [
                {"op": "set_flag", "flag": "fold_trust"},
                {"op": "remember", "actor": "brin", "fact": "soft_cut"},
            ],
        ),
        action(
            "read_the_share_board",
            "Read the share board",
            "do",
            {
                "all": [
                    {"at": "fold.green"},
                    {"sheet": ["skill", "letters"]},
                    {"not_flag": "fold_trust"},
                ]
            },
            "You read the share board. Brin lets you cut by the list.",
            [
                {"op": "set_flag", "flag": "fold_trust"},
                {"op": "remember", "actor": "brin", "fact": "board"},
            ],
        ),
        action(
            "cite_the_restored_name",
            "Cite the restored name",
            "talk",
            {
                "all": [
                    {"at": "fold.green"},
                    {"has_flag": "name_restored"},
                    {"not_flag": "fold_cited_name"},
                ]
            },
            "You cite the restored name. Brin counts you as kin of the fold.",
            [
                {"op": "set_flag", "flag": "fold_cited_name"},
                {"op": "set_flag", "flag": "fold_trust"},
                {"op": "remember", "actor": "brin", "fact": "named_kin"},
            ],
        ),
        action(
            "cut_safe_peat",
            "Cut a safe brick",
            "do",
            {
                "all": [
                    {"at": "fold.cut"},
                    {"has_flag": "fold_trust"},
                    {"not_flag": "fold_flooded"},
                    {"not": {"has_item": "peat_brick"}},
                ]
            },
            "You cut a shallow brick. The face holds.",
            [{"op": "add_item", "item": "peat_brick"}],
        ),
        action(
            "force_a_deep_cut",
            "Force a deep cut",
            "do",
            {
                "all": [
                    {"at": "fold.cut"},
                    {"sheet": ["body", "might"]},
                    {"not_flag": "fold_flooded"},
                ]
            },
            "You force a deep cut. Water fills the toe.",
            [
                {"op": "set_flag", "flag": "fold_flooded"},
                {"op": "add_item", "item": "peat_brick"},
            ],
        ),
        action(
            "set_the_share",
            "Set the peat share",
            "talk",
            {
                "all": [
                    {"at": "fold.shed"},
                    {"has_item": "peat_brick"},
                    {"has_flag": "fold_trust"},
                    {"not_flag": "fold_held"},
                ]
            },
            "You set the brick on the board. Willa marks the share even.",
            [
                {"op": "remove_item", "item": "peat_brick"},
                {"op": "set_flag", "flag": "fold_held"},
            ],
        ),
        action(
            "bail_the_ditch",
            "Bail the ditch",
            "do",
            {
                "all": [
                    {"at": "fold.ditch"},
                    {"has_flag": "fold_flooded"},
                    {"not_flag": "ditch_bailed"},
                ]
            },
            "You bail the ditch. The cut face shows again.",
            [
                {"op": "set_flag", "flag": "ditch_bailed"},
                {"op": "clear_flag", "flag": "fold_flooded"},
            ],
        ),
        action(
            "ask_brin_rule",
            "Ask Brin the rule",
            "talk",
            {"at": "fold.green"},
            "Brin says cut shallow. Then the brick goes on the board.",
            [{"op": "set_flag", "flag": "heard_fold_rule"}],
        ),
        action(
            "ask_jase_face",
            "Ask Jase the face",
            "talk",
            {"at": "fold.cut"},
            "Jase says a deep cut drinks the ditch.",
            [{"op": "set_flag", "flag": "heard_fold_rule"}],
        ),
        action(
            "ask_willa_count",
            "Ask Willa the count",
            "talk",
            {"at": "fold.shed"},
            "Willa says a brick on the board holds the fold.",
            [{"op": "set_flag", "flag": "heard_fold_rule"}],
        ),
        action(
            "know_the_low_sun",
            "Know the low sun",
            "talk",
            {
                "all": [
                    {"at": "glass.nave"},
                    {
                        "any": [
                            {"sheet": ["origin", "marshborn"]},
                            {"sheet": ["skill", "hunt"]},
                        ]
                    },
                    {"not_flag": "glass_trust"},
                ]
            },
            "You name the low sun line. Rook lets you set a shard.",
            [
                {"op": "set_flag", "flag": "glass_trust"},
                {"op": "remember", "actor": "rook", "fact": "low_sun"},
            ],
        ),
        action(
            "read_the_sun_chart",
            "Read the sun chart",
            "do",
            {
                "all": [
                    {"at": "glass.nave"},
                    {"sheet": ["skill", "letters"]},
                    {"not_flag": "glass_trust"},
                ]
            },
            "You read the sun chart. Rook lets you set a shard.",
            [
                {"op": "set_flag", "flag": "glass_trust"},
                {"op": "remember", "actor": "rook", "fact": "chart"},
            ],
        ),
        action(
            "trade_peat_for_lead",
            "Trade peat credit for lead",
            "talk",
            {
                "all": [
                    {"at": "glass.yard"},
                    {"has_flag": "fold_held"},
                    {"not_flag": "glass_lead_trade"},
                ]
            },
            "You trade peat credit. Rook hands over a strip of lead.",
            [
                {"op": "set_flag", "flag": "glass_lead_trade"},
                {"op": "set_flag", "flag": "glass_trust"},
                {"op": "remember", "actor": "rook", "fact": "peat_pay"},
            ],
        ),
        action(
            "set_the_lens",
            "Set the lens shard",
            "do",
            {
                "all": [
                    {"at": "glass.loft"},
                    {"has_item": "lens_shard"},
                    {"has_flag": "glass_trust"},
                    {"not_flag": "lens_set"},
                ]
            },
            "You set the shard in the peg. A line of light marks the channel.",
            [
                {"op": "remove_item", "item": "lens_shard"},
                {"op": "set_flag", "flag": "lens_set"},
            ],
        ),
        action(
            "ask_rook_rule",
            "Ask Rook the rule",
            "talk",
            {"at": "glass.nave"},
            "Rook says know the sun. Then set the shard in the loft.",
            [{"op": "set_flag", "flag": "heard_glass_rule"}],
        ),
        action(
            "ask_nim_shard",
            "Ask Nim for a shard",
            "talk",
            {"at": "glass.pit"},
            "Nim points at the bright shard in the pit.",
            [{"op": "set_flag", "flag": "heard_glass_rule"}],
        ),
        action(
            "ask_lise_peg",
            "Ask Lise the peg",
            "talk",
            {"at": "glass.loft"},
            "Lise says the peg takes one shard and no more.",
            [{"op": "set_flag", "flag": "heard_glass_rule"}],
        ),
        action(
            "know_the_hemp_twist",
            "Know the hemp twist",
            "talk",
            {
                "all": [
                    {"at": "rope.yard"},
                    {
                        "any": [
                            {"sheet": ["origin", "marshborn"]},
                            {"sheet": ["skill", "hunt"]},
                        ]
                    },
                    {"not_flag": "rope_trust"},
                ]
            },
            "You name the right twist. Tess lets you walk a hank.",
            [
                {"op": "set_flag", "flag": "rope_trust"},
                {"op": "remember", "actor": "tess", "fact": "twist"},
            ],
        ),
        action(
            "read_the_walk_mark",
            "Read the walk mark",
            "do",
            {
                "all": [
                    {"at": "rope.yard"},
                    {"sheet": ["skill", "letters"]},
                    {"not_flag": "rope_trust"},
                ]
            },
            "You read the walk mark. Tess lets you walk a hank.",
            [
                {"op": "set_flag", "flag": "rope_trust"},
                {"op": "remember", "actor": "tess", "fact": "mark"},
            ],
        ),
        action(
            "sight_the_channel",
            "Sight the channel line",
            "do",
            {
                "all": [
                    {"at": "rope.walk"},
                    {"has_flag": "lens_set"},
                    {"not_flag": "rope_sighted"},
                ]
            },
            "You sight the channel line on the floor. The walk holds true.",
            [
                {"op": "set_flag", "flag": "rope_sighted"},
                {"op": "set_flag", "flag": "rope_trust"},
                {"op": "remember", "actor": "tess", "fact": "channel"},
            ],
        ),
        action(
            "walk_the_rope",
            "Walk the rope taut",
            "do",
            {
                "all": [
                    {"at": "rope.walk"},
                    {"has_item": "hemp_hank"},
                    {"has_flag": "rope_trust"},
                    {"not_flag": "rope_walked"},
                ]
            },
            "You walk the hank taut. Tess marks the pegs done.",
            [
                {"op": "remove_item", "item": "hemp_hank"},
                {"op": "set_flag", "flag": "rope_walked"},
            ],
        ),
        action(
            "haul_the_slack",
            "Haul the slack",
            "do",
            {
                "all": [
                    {"at": "rope.walk"},
                    {"sheet": ["body", "might"]},
                    {"not_flag": "rope_hauled"},
                ]
            },
            "You haul the slack by force. The line jumps and holds.",
            [{"op": "set_flag", "flag": "rope_hauled"}],
        ),
        action(
            "ask_tess_rule",
            "Ask Tess the rule",
            "talk",
            {"at": "rope.yard"},
            "Tess says know the twist. Then walk a hank taut.",
            [{"op": "set_flag", "flag": "heard_rope_rule"}],
        ),
        action(
            "ask_bram_hank",
            "Ask Bram for a hank",
            "talk",
            {"at": "rope.loft"},
            "Bram points at the dry hank on the beam.",
            [{"op": "set_flag", "flag": "heard_rope_rule"}],
        ),
        action(
            "ask_kite_price",
            "Ask Kite the price",
            "talk",
            {"at": "rope.end"},
            "Kite pays only for a rope that lies taut.",
            [{"op": "set_flag", "flag": "heard_rope_rule"}],
        ),
        action(
            "know_the_brine_cut",
            "Know the brine cut",
            "talk",
            {
                "all": [
                    {"at": "pans.yard"},
                    {
                        "any": [
                            {"sheet": ["origin", "marshborn"]},
                            {"sheet": ["skill", "hunt"]},
                        ]
                    },
                    {"not_flag": "salt_trust"},
                ]
            },
            "You name the brine cut. Dorr lets you draw and rake.",
            [
                {"op": "set_flag", "flag": "salt_trust"},
                {"op": "remember", "actor": "dorr", "fact": "brine_cut"},
            ],
        ),
        action(
            "read_the_pan_list",
            "Read the pan list",
            "do",
            {
                "all": [
                    {"at": "pans.yard"},
                    {"sheet": ["skill", "letters"]},
                    {"not_flag": "salt_trust"},
                ]
            },
            "You read the pan list. Dorr lets you draw and rake.",
            [
                {"op": "set_flag", "flag": "salt_trust"},
                {"op": "remember", "actor": "dorr", "fact": "list"},
            ],
        ),
        action(
            "rig_the_rake_line",
            "Rig the rake line",
            "do",
            {
                "all": [
                    {"at": "pans.beds"},
                    {"has_flag": "rope_walked"},
                    {"not_flag": "rake_rigged"},
                ]
            },
            "You rig a taut rake line. The beds can be scraped even.",
            [
                {"op": "set_flag", "flag": "rake_rigged"},
                {"op": "set_flag", "flag": "salt_trust"},
                {"op": "remember", "actor": "dorr", "fact": "rake_line"},
            ],
        ),
        action(
            "draw_the_brine",
            "Draw the brine",
            "do",
            {
                "all": [
                    {"at": "pans.well"},
                    {"has_flag": "salt_trust"},
                    {"not_flag": "brine_drawn"},
                ]
            },
            "You draw brine. Nell nods at the full bucket.",
            [{"op": "set_flag", "flag": "brine_drawn"}],
        ),
        action(
            "rake_the_cake",
            "Rake a salt cake",
            "do",
            {
                "all": [
                    {"at": "pans.beds"},
                    {"has_flag": "salt_trust"},
                    {"has_flag": "brine_drawn"},
                    {"not": {"has_item": "salt_cake"}},
                    {"not_flag": "salt_raked"},
                ]
            },
            "You rake a white cake. The bed shows clean stone.",
            [{"op": "add_item", "item": "salt_cake"}],
        ),
        action(
            "weigh_the_cake",
            "Weigh the salt cake",
            "talk",
            {
                "all": [
                    {"at": "pans.shed"},
                    {"has_item": "salt_cake"},
                    {"has_flag": "salt_trust"},
                    {"not_flag": "salt_raked"},
                ]
            },
            "You weigh the cake. Pim chalks the mark and the rake is done.",
            [
                {"op": "remove_item", "item": "salt_cake"},
                {"op": "set_flag", "flag": "salt_raked"},
            ],
        ),
        action(
            "ask_dorr_rule",
            "Ask Dorr the rule",
            "talk",
            {"at": "pans.yard"},
            "Dorr says draw brine. Then rake a cake and weigh it.",
            [{"op": "set_flag", "flag": "heard_salt_rule"}],
        ),
        action(
            "ask_nell_well",
            "Ask Nell the well",
            "talk",
            {"at": "pans.well"},
            "Nell says the well is brine, not drink.",
            [{"op": "set_flag", "flag": "heard_salt_rule"}],
        ),
        action(
            "ask_pim_scale",
            "Ask Pim the scale",
            "talk",
            {"at": "pans.shed"},
            "Pim says a cake on the scale closes the rake.",
            [{"op": "set_flag", "flag": "heard_salt_rule"}],
        ),
        action(
            "know_the_wet_fish",
            "Know the wet fish",
            "talk",
            {
                "all": [
                    {"at": "smoke.yard"},
                    {
                        "any": [
                            {"sheet": ["origin", "marshborn"]},
                            {"sheet": ["skill", "hunt"]},
                        ]
                    },
                    {"not_flag": "smoke_trust"},
                ]
            },
            "You name the wet fish. Hal lets you hang and tend.",
            [
                {"op": "set_flag", "flag": "smoke_trust"},
                {"op": "remember", "actor": "hal", "fact": "wet_fish"},
            ],
        ),
        action(
            "read_the_cure_mark",
            "Read the cure mark",
            "do",
            {
                "all": [
                    {"at": "smoke.yard"},
                    {"sheet": ["skill", "letters"]},
                    {"not_flag": "smoke_trust"},
                ]
            },
            "You read the cure mark. Hal lets you hang and tend.",
            [
                {"op": "set_flag", "flag": "smoke_trust"},
                {"op": "remember", "actor": "hal", "fact": "mark"},
            ],
        ),
        action(
            "salt_the_racks",
            "Salt the racks",
            "do",
            {
                "all": [
                    {"at": "smoke.racks"},
                    {"has_flag": "salt_raked"},
                    {"not_flag": "brine_cure"},
                ]
            },
            "You salt the racks. The brine sets the cure.",
            [
                {"op": "set_flag", "flag": "brine_cure"},
                {"op": "set_flag", "flag": "smoke_trust"},
                {"op": "remember", "actor": "hal", "fact": "brine"},
            ],
        ),
        action(
            "hang_the_fish",
            "Hang the wet fish",
            "do",
            {
                "all": [
                    {"at": "smoke.racks"},
                    {"has_flag": "smoke_trust"},
                    {"has_item": "wet_fish"},
                    {"not_flag": "fish_hung"},
                    {"not_flag": "smoke_cured"},
                ]
            },
            "You hang the wet fish. The racks take the drip.",
            [
                {"op": "remove_item", "item": "wet_fish"},
                {"op": "set_flag", "flag": "fish_hung"},
            ],
        ),
        action(
            "tend_the_smoke",
            "Tend the smoke",
            "do",
            {
                "all": [
                    {"at": "smoke.hearth"},
                    {"has_flag": "fish_hung"},
                    {"not_flag": "smoke_tended"},
                    {"not_flag": "smoke_cured"},
                ]
            },
            "You tend the smoke. The racks take an even haze.",
            [{"op": "set_flag", "flag": "smoke_tended"}],
        ),
        action(
            "take_the_cure",
            "Take down the cure",
            "talk",
            {
                "all": [
                    {"at": "smoke.loft"},
                    {"has_flag": "smoke_trust"},
                    {"has_flag": "smoke_tended"},
                    {"not_flag": "smoke_cured"},
                ]
            },
            "You take down the cure. Wren marks the rack empty.",
            [
                {"op": "add_item", "item": "cured_fish"},
                {"op": "set_flag", "flag": "smoke_cured"},
            ],
        ),
        action(
            "ask_hal_rule",
            "Ask Hal the rule",
            "talk",
            {"at": "smoke.yard"},
            "Hal says hang wet fish. Then tend the smoke and take it down.",
            [{"op": "set_flag", "flag": "heard_smoke_rule"}],
        ),
        action(
            "ask_bea_hearth",
            "Ask Bea the hearth",
            "talk",
            {"at": "smoke.hearth"},
            "Bea says even smoke, not a kiln white.",
            [{"op": "set_flag", "flag": "heard_smoke_rule"}],
        ),
        action(
            "ask_wren_tally",
            "Ask Wren the tally",
            "talk",
            {"at": "smoke.loft"},
            "Wren pays only when a rack comes down dry.",
            [{"op": "set_flag", "flag": "heard_smoke_rule"}],
        ),
        action(
            "know_the_eel_run",
            "Know the eel run",
            "talk",
            {
                "all": [
                    {"at": "weir.yard"},
                    {
                        "any": [
                            {"sheet": ["origin", "marshborn"]},
                            {"sheet": ["skill", "hunt"]},
                        ]
                    },
                    {"not_flag": "weir_trust"},
                ]
            },
            "You name the eel run. Cess lets you set and lift.",
            [
                {"op": "set_flag", "flag": "weir_trust"},
                {"op": "remember", "actor": "cess", "fact": "eel_run"},
            ],
        ),
        action(
            "read_the_weir_right",
            "Read the weir right",
            "do",
            {
                "all": [
                    {"at": "weir.yard"},
                    {"sheet": ["skill", "letters"]},
                    {"not_flag": "weir_trust"},
                ]
            },
            "You read the weir right. Cess lets you set and lift.",
            [
                {"op": "set_flag", "flag": "weir_trust"},
                {"op": "remember", "actor": "cess", "fact": "right"},
            ],
        ),
        action(
            "bait_the_weir",
            "Bait the weir",
            "do",
            {
                "all": [
                    {"at": "weir.stakes"},
                    {"has_flag": "smoke_cured"},
                    {"not_flag": "weir_baited"},
                ]
            },
            "You bait the stakes. Smoke draws the run in.",
            [
                {"op": "set_flag", "flag": "weir_baited"},
                {"op": "set_flag", "flag": "weir_trust"},
                {"op": "remember", "actor": "cess", "fact": "bait"},
            ],
        ),
        action(
            "set_the_baskets",
            "Set the baskets",
            "do",
            {
                "all": [
                    {"at": "weir.stakes"},
                    {"has_flag": "weir_trust"},
                    {"has_item": "weir_basket"},
                    {"not_flag": "baskets_set"},
                    {"not_flag": "weir_lifted"},
                ]
            },
            "You set the baskets. The stakes hold the mouths.",
            [
                {"op": "remove_item", "item": "weir_basket"},
                {"op": "set_flag", "flag": "baskets_set"},
            ],
        ),
        action(
            "lift_the_weir",
            "Lift the weir",
            "do",
            {
                "all": [
                    {"at": "weir.stakes"},
                    {"has_flag": "weir_trust"},
                    {"has_flag": "baskets_set"},
                    {"not_flag": "weir_lifted"},
                ]
            },
            "You lift the weir. Eels twist in the wet wicker.",
            [
                {"op": "add_item", "item": "eel_catch"},
                {"op": "set_flag", "flag": "weir_lifted"},
            ],
        ),
        action(
            "ask_cess_rule",
            "Ask Cess the rule",
            "talk",
            {"at": "weir.yard"},
            "Cess says set the baskets. Then lift the catch.",
            [{"op": "set_flag", "flag": "heard_weir_rule"}],
        ),
        action(
            "ask_noll_run",
            "Ask Noll the run",
            "talk",
            {"at": "weir.pool"},
            "Noll says the eels hug the posts at the turn.",
            [{"op": "set_flag", "flag": "heard_weir_rule"}],
        ),
        action(
            "ask_meg_count",
            "Ask Meg the count",
            "talk",
            {"at": "weir.hut"},
            "Meg counts only a lift that comes in wet.",
            [{"op": "set_flag", "flag": "heard_weir_rule"}],
        ),
        action(
            "know_the_reed_mordant",
            "Know the reed mordant",
            "talk",
            {
                "all": [
                    {"at": "dye.yard"},
                    {
                        "any": [
                            {"sheet": ["origin", "marshborn"]},
                            {"sheet": ["skill", "hunt"]},
                        ]
                    },
                    {"not_flag": "dye_trust"},
                ]
            },
            "You name the reed mordant. Quill lets you charge and dip.",
            [
                {"op": "set_flag", "flag": "dye_trust"},
                {"op": "remember", "actor": "quill", "fact": "reed"},
            ],
        ),
        action(
            "read_the_vat_list",
            "Read the vat list",
            "do",
            {
                "all": [
                    {"at": "dye.yard"},
                    {"sheet": ["skill", "letters"]},
                    {"not_flag": "dye_trust"},
                ]
            },
            "You read the vat list. Quill lets you charge and dip.",
            [
                {"op": "set_flag", "flag": "dye_trust"},
                {"op": "remember", "actor": "quill", "fact": "list"},
            ],
        ),
        action(
            "bind_eel_skin",
            "Bind eel skin",
            "do",
            {
                "all": [
                    {"at": "dye.vats"},
                    {"has_flag": "weir_lifted"},
                    {"not_flag": "eel_mordant"},
                ]
            },
            "You bind eel skin. The vat takes a dark bite.",
            [
                {"op": "set_flag", "flag": "eel_mordant"},
                {"op": "set_flag", "flag": "dye_trust"},
                {"op": "remember", "actor": "quill", "fact": "eel_skin"},
            ],
        ),
        action(
            "charge_the_vat",
            "Charge the vat",
            "do",
            {
                "all": [
                    {"at": "dye.vats"},
                    {"has_flag": "dye_trust"},
                    {"not_flag": "vat_charged"},
                    {"not_flag": "dye_struck"},
                ]
            },
            "You charge the vat. The liquor takes a reed stain.",
            [{"op": "set_flag", "flag": "vat_charged"}],
        ),
        action(
            "dip_the_cloth",
            "Dip the cloth",
            "do",
            {
                "all": [
                    {"at": "dye.vats"},
                    {"has_flag": "dye_trust"},
                    {"has_flag": "vat_charged"},
                    {"has_item": "undyed_cloth"},
                    {"not_flag": "cloth_dipped"},
                    {"not_flag": "dye_struck"},
                ]
            },
            "You dip the cloth. The vat drinks the white.",
            [
                {"op": "remove_item", "item": "undyed_cloth"},
                {"op": "set_flag", "flag": "cloth_dipped"},
            ],
        ),
        action(
            "hang_the_color",
            "Hang the color",
            "do",
            {
                "all": [
                    {"at": "dye.loft"},
                    {"has_flag": "dye_trust"},
                    {"has_flag": "cloth_dipped"},
                    {"not_flag": "dye_struck"},
                ]
            },
            "You hang the color. Moss marks the loft dry.",
            [
                {"op": "add_item", "item": "dyed_cloth"},
                {"op": "set_flag", "flag": "dye_struck"},
            ],
        ),
        action(
            "ask_quill_rule",
            "Ask Quill the rule",
            "talk",
            {"at": "dye.yard"},
            "Quill says charge the vat. Then dip and hang dry.",
            [{"op": "set_flag", "flag": "heard_dye_rule"}],
        ),
        action(
            "ask_fen_vat",
            "Ask Fen the vat",
            "talk",
            {"at": "dye.vats"},
            "Fen says stir slow. A boil will ruin the cloth.",
            [{"op": "set_flag", "flag": "heard_dye_rule"}],
        ),
        action(
            "ask_moss_line",
            "Ask Moss the line",
            "talk",
            {"at": "dye.loft"},
            "Moss pays only when a pole holds dry color.",
            [{"op": "set_flag", "flag": "heard_dye_rule"}],
        ),
        action(
            "know_the_channel_cut",
            "Know the channel cut",
            "talk",
            {
                "all": [
                    {"at": "ferry.yard"},
                    {
                        "any": [
                            {"sheet": ["origin", "marshborn"]},
                            {"sheet": ["skill", "hunt"]},
                        ]
                    },
                    {"not_flag": "ferry_trust"},
                ]
            },
            "You name the channel cut. Bex lets you load and pole.",
            [
                {"op": "set_flag", "flag": "ferry_trust"},
                {"op": "remember", "actor": "bex", "fact": "channel"},
            ],
        ),
        action(
            "read_the_toll_board",
            "Read the toll board",
            "do",
            {
                "all": [
                    {"at": "ferry.yard"},
                    {"sheet": ["skill", "letters"]},
                    {"not_flag": "ferry_trust"},
                ]
            },
            "You read the toll board. Bex lets you load and pole.",
            [
                {"op": "set_flag", "flag": "ferry_trust"},
                {"op": "remember", "actor": "bex", "fact": "board"},
            ],
        ),
        action(
            "show_the_dyed_fare",
            "Show the dyed fare",
            "do",
            {
                "all": [
                    {"at": "ferry.yard"},
                    {"has_flag": "dye_struck"},
                    {"not_flag": "dyed_fare"},
                ]
            },
            "You show the dyed fare. Bex lets you load and pole.",
            [
                {"op": "set_flag", "flag": "dyed_fare"},
                {"op": "set_flag", "flag": "ferry_trust"},
                {"op": "remember", "actor": "bex", "fact": "dyed"},
            ],
        ),
        action(
            "load_the_boat",
            "Load the boat",
            "do",
            {
                "all": [
                    {"at": "ferry.slip"},
                    {"has_flag": "ferry_trust"},
                    {"has_item": "toll_token"},
                    {"not_flag": "boat_loaded"},
                    {"not_flag": "ferry_crossed"},
                ]
            },
            "You load the boat. Ivo takes the token and the line.",
            [
                {"op": "remove_item", "item": "toll_token"},
                {"op": "set_flag", "flag": "boat_loaded"},
                {"op": "remember", "actor": "ivo", "fact": "loaded"},
            ],
        ),
        action(
            "pole_the_crossing",
            "Pole the crossing",
            "do",
            {
                "all": [
                    {"at": "ferry.boat"},
                    {"has_flag": "boat_loaded"},
                    {"not_flag": "boat_poled"},
                    {"not_flag": "ferry_crossed"},
                ]
            },
            "You pole the crossing. The far bank takes the hull.",
            [
                {"op": "set_flag", "flag": "boat_poled"},
                {"op": "move", "to": "ferry.far"},
            ],
        ),
        action(
            "claim_the_landing",
            "Claim the landing",
            "talk",
            {
                "all": [
                    {"at": "ferry.far"},
                    {"has_flag": "boat_poled"},
                    {"not_flag": "ferry_crossed"},
                ]
            },
            "You claim the landing. Ama stamps the fare paid.",
            [
                {"op": "set_flag", "flag": "ferry_crossed"},
                {"op": "remember", "actor": "ama", "fact": "stamp"},
            ],
        ),
        action(
            "ask_bex_rule",
            "Ask Bex the rule",
            "talk",
            {"at": "ferry.yard"},
            "Bex says pay a token. Then load and pole across.",
            [{"op": "set_flag", "flag": "heard_ferry_rule"}],
        ),
        action(
            "ask_ivo_line",
            "Ask Ivo the line",
            "talk",
            {"at": "ferry.slip"},
            "Ivo says a loaded hull is the only crossing.",
            [{"op": "set_flag", "flag": "heard_ferry_rule"}],
        ),
        action(
            "ask_ama_stamp",
            "Ask Ama the stamp",
            "talk",
            {"at": "ferry.far"},
            "Ama stamps only a hull that poled from the near bank.",
            [{"op": "set_flag", "flag": "heard_ferry_rule"}],
        ),
        action(
            "know_the_wind_cut",
            "Know the wind cut",
            "talk",
            {
                "all": [
                    {"at": "pump.yard"},
                    {
                        "any": [
                            {"sheet": ["origin", "marshborn"]},
                            {"sheet": ["skill", "hunt"]},
                        ]
                    },
                    {"not_flag": "pump_trust"},
                ]
            },
            "You name the wind cut. Od lets you set and crank.",
            [
                {"op": "set_flag", "flag": "pump_trust"},
                {"op": "remember", "actor": "od", "fact": "wind_cut"},
            ],
        ),
        action(
            "read_the_pump_mark",
            "Read the pump mark",
            "do",
            {
                "all": [
                    {"at": "pump.yard"},
                    {"sheet": ["skill", "letters"]},
                    {"not_flag": "pump_trust"},
                ]
            },
            "You read the pump mark. Od lets you set and crank.",
            [
                {"op": "set_flag", "flag": "pump_trust"},
                {"op": "remember", "actor": "od", "fact": "mark"},
            ],
        ),
        action(
            "brace_the_sail",
            "Brace the sail",
            "do",
            {
                "all": [
                    {"at": "pump.tower"},
                    {"has_flag": "ferry_crossed"},
                    {"not_flag": "sail_braced"},
                ]
            },
            "You brace the sail. The vanes hold to the wind.",
            [
                {"op": "set_flag", "flag": "sail_braced"},
                {"op": "set_flag", "flag": "pump_trust"},
                {"op": "remember", "actor": "rusk", "fact": "brace"},
            ],
        ),
        action(
            "set_the_vanes",
            "Set the vanes",
            "do",
            {
                "all": [
                    {"at": "pump.tower"},
                    {"has_flag": "pump_trust"},
                    {"has_item": "vane_pin"},
                    {"not_flag": "vanes_set"},
                    {"not_flag": "flats_drained"},
                ]
            },
            "You set the vanes. The ring takes the wind.",
            [
                {"op": "remove_item", "item": "vane_pin"},
                {"op": "set_flag", "flag": "vanes_set"},
            ],
        ),
        action(
            "crank_the_pump",
            "Crank the pump",
            "do",
            {
                "all": [
                    {"at": "pump.crank"},
                    {"has_flag": "pump_trust"},
                    {"has_flag": "vanes_set"},
                    {"not_flag": "pump_cranked"},
                    {"not_flag": "flats_drained"},
                ]
            },
            "You crank the pump. Water climbs the well.",
            [{"op": "set_flag", "flag": "pump_cranked"}],
        ),
        action(
            "hold_the_draw",
            "Hold the draw",
            "do",
            {
                "all": [
                    {"at": "pump.sump"},
                    {"has_flag": "pump_trust"},
                    {"has_flag": "pump_cranked"},
                    {"not_flag": "flats_drained"},
                ]
            },
            "You hold the draw. The flats sit dry.",
            [
                {"op": "set_flag", "flag": "flats_drained"},
                {"op": "remember", "actor": "hobb", "fact": "held"},
            ],
        ),
        action(
            "ask_od_rule",
            "Ask Od the rule",
            "talk",
            {"at": "pump.yard"},
            "Od says set the vanes. Then crank and hold the draw.",
            [{"op": "set_flag", "flag": "heard_pump_rule"}],
        ),
        action(
            "ask_rusk_pin",
            "Ask Rusk the pin",
            "talk",
            {"at": "pump.tower"},
            "Rusk says a pin holds the ring true.",
            [{"op": "set_flag", "flag": "heard_pump_rule"}],
        ),
        action(
            "ask_hobb_cut",
            "Ask Hobb the cut",
            "talk",
            {"at": "pump.sump"},
            "Hobb says a firm board keeps the cut dry.",
            [{"op": "set_flag", "flag": "heard_pump_rule"}],
        ),
        action(
            "know_the_spat_set",
            "Know the spat set",
            "talk",
            {
                "all": [
                    {"at": "oyster.yard"},
                    {
                        "any": [
                            {"sheet": ["origin", "marshborn"]},
                            {"sheet": ["skill", "hunt"]},
                        ]
                    },
                    {"not_flag": "oyster_trust"},
                ]
            },
            "You name the spat set. Wex lets you seed and cull.",
            [
                {"op": "set_flag", "flag": "oyster_trust"},
                {"op": "remember", "actor": "wex", "fact": "spat"},
            ],
        ),
        action(
            "read_the_bed_list",
            "Read the bed list",
            "do",
            {
                "all": [
                    {"at": "oyster.yard"},
                    {"sheet": ["skill", "letters"]},
                    {"not_flag": "oyster_trust"},
                ]
            },
            "You read the bed list. Wex lets you seed and cull.",
            [
                {"op": "set_flag", "flag": "oyster_trust"},
                {"op": "remember", "actor": "wex", "fact": "list"},
            ],
        ),
        action(
            "work_the_dry_beds",
            "Work the dry beds",
            "do",
            {
                "all": [
                    {"at": "oyster.beds"},
                    {"has_flag": "flats_drained"},
                    {"not_flag": "dry_beds"},
                ]
            },
            "You work the dry beds. The stakes sit firm.",
            [
                {"op": "set_flag", "flag": "dry_beds"},
                {"op": "set_flag", "flag": "oyster_trust"},
                {"op": "remember", "actor": "wex", "fact": "dry"},
            ],
        ),
        action(
            "seed_the_beds",
            "Seed the beds",
            "do",
            {
                "all": [
                    {"at": "oyster.beds"},
                    {"has_flag": "oyster_trust"},
                    {"has_item": "spat_bag"},
                    {"not_flag": "beds_seeded"},
                    {"not_flag": "oyster_culled"},
                ]
            },
            "You seed the beds. The spat takes the mud.",
            [
                {"op": "remove_item", "item": "spat_bag"},
                {"op": "set_flag", "flag": "beds_seeded"},
            ],
        ),
        action(
            "cull_the_beds",
            "Cull the beds",
            "do",
            {
                "all": [
                    {"at": "oyster.shed"},
                    {"has_flag": "oyster_trust"},
                    {"has_flag": "beds_seeded"},
                    {"not_flag": "oyster_culled"},
                ]
            },
            "You cull the beds. Gell marks the take even.",
            [
                {"op": "add_item", "item": "oyster_lot"},
                {"op": "set_flag", "flag": "oyster_culled"},
                {"op": "remember", "actor": "gell", "fact": "cull"},
            ],
        ),
        action(
            "ask_wex_rule",
            "Ask Wex the rule",
            "talk",
            {"at": "oyster.yard"},
            "Wex says seed the beds. Then cull the take.",
            [{"op": "set_flag", "flag": "heard_oyster_rule"}],
        ),
        action(
            "ask_pip_spat",
            "Ask Pip the spat",
            "talk",
            {"at": "oyster.spat"},
            "Pip says keep the spat wet and cool.",
            [{"op": "set_flag", "flag": "heard_oyster_rule"}],
        ),
        action(
            "ask_gell_cull",
            "Ask Gell the cull",
            "talk",
            {"at": "oyster.shed"},
            "Gell pays only for a cull that comes in even.",
            [{"op": "set_flag", "flag": "heard_oyster_rule"}],
        ),
        action(
            "know_the_shell_count",
            "Know the shell count",
            "talk",
            {
                "all": [
                    {"at": "count.yard"},
                    {
                        "any": [
                            {"sheet": ["origin", "marshborn"]},
                            {"sheet": ["skill", "hunt"]},
                        ]
                    },
                    {"not_flag": "count_trust"},
                ]
            },
            "You name the shell count. Voss lets you mark and seal.",
            [
                {"op": "set_flag", "flag": "count_trust"},
                {"op": "remember", "actor": "voss", "fact": "shell"},
            ],
        ),
        action(
            "read_the_tally_roll",
            "Read the tally roll",
            "do",
            {
                "all": [
                    {"at": "count.yard"},
                    {"sheet": ["skill", "letters"]},
                    {"not_flag": "count_trust"},
                ]
            },
            "You read the tally roll. Voss lets you mark and seal.",
            [
                {"op": "set_flag", "flag": "count_trust"},
                {"op": "remember", "actor": "voss", "fact": "roll"},
            ],
        ),
        action(
            "lay_the_oyster_lot",
            "Lay the oyster lot",
            "do",
            {
                "all": [
                    {"at": "count.desk"},
                    {"has_flag": "oyster_culled"},
                    {"not_flag": "oyster_laid"},
                ]
            },
            "You lay the oyster lot. The roll takes the credit.",
            [
                {"op": "set_flag", "flag": "oyster_laid"},
                {"op": "set_flag", "flag": "count_trust"},
                {"op": "remember", "actor": "rhee", "fact": "lot"},
            ],
        ),
        action(
            "mark_the_tally",
            "Mark the tally",
            "do",
            {
                "all": [
                    {"at": "count.desk"},
                    {"has_flag": "count_trust"},
                    {"has_item": "tally_slate"},
                    {"not_flag": "tally_marked"},
                    {"not_flag": "tally_closed"},
                ]
            },
            "You mark the tally. Rhee nods at the even line.",
            [
                {"op": "remove_item", "item": "tally_slate"},
                {"op": "set_flag", "flag": "tally_marked"},
            ],
        ),
        action(
            "seal_the_count",
            "Seal the count",
            "do",
            {
                "all": [
                    {"at": "count.vault"},
                    {"has_flag": "count_trust"},
                    {"has_flag": "tally_marked"},
                    {"not_flag": "tally_closed"},
                ]
            },
            "You seal the count. Orm shuts the vault on the day.",
            [
                {"op": "set_flag", "flag": "tally_closed"},
                {"op": "remember", "actor": "orm", "fact": "seal"},
            ],
        ),
        action(
            "ask_voss_rule",
            "Ask Voss the rule",
            "talk",
            {"at": "count.yard"},
            "Voss says mark the tally. Then seal the day.",
            [{"op": "set_flag", "flag": "heard_count_rule"}],
        ),
        action(
            "ask_rhee_roll",
            "Ask Rhee the roll",
            "talk",
            {"at": "count.desk"},
            "Rhee says the roll must close even.",
            [{"op": "set_flag", "flag": "heard_count_rule"}],
        ),
        action(
            "ask_orm_seal",
            "Ask Orm the seal",
            "talk",
            {"at": "count.vault"},
            "Orm seals only a tally that has been marked.",
            [{"op": "set_flag", "flag": "heard_count_rule"}],
        ),
        action(
            "know_the_ice_cut",
            "Know the ice cut",
            "talk",
            {
                "all": [
                    {"at": "ice.yard"},
                    {
                        "any": [
                            {"sheet": ["origin", "marshborn"]},
                            {"sheet": ["skill", "hunt"]},
                        ]
                    },
                    {"not_flag": "ice_trust"},
                ]
            },
            "You name the ice cut. Yul lets you pack and bar.",
            [
                {"op": "set_flag", "flag": "ice_trust"},
                {"op": "remember", "actor": "yul", "fact": "ice_cut"},
            ],
        ),
        action(
            "read_the_cold_mark",
            "Read the cold mark",
            "do",
            {
                "all": [
                    {"at": "ice.yard"},
                    {"sheet": ["skill", "letters"]},
                    {"not_flag": "ice_trust"},
                ]
            },
            "You read the cold mark. Yul lets you pack and bar.",
            [
                {"op": "set_flag", "flag": "ice_trust"},
                {"op": "remember", "actor": "yul", "fact": "mark"},
            ],
        ),
        action(
            "cite_the_ice_right",
            "Cite the ice right",
            "do",
            {
                "all": [
                    {"at": "ice.yard"},
                    {"has_flag": "tally_closed"},
                    {"not_flag": "ice_right"},
                ]
            },
            "You cite the ice right. Yul lets you pack and bar.",
            [
                {"op": "set_flag", "flag": "ice_right"},
                {"op": "set_flag", "flag": "ice_trust"},
                {"op": "remember", "actor": "yul", "fact": "right"},
            ],
        ),
        action(
            "pack_the_ice",
            "Pack the ice",
            "do",
            {
                "all": [
                    {"at": "ice.hold"},
                    {"has_flag": "ice_trust"},
                    {"has_item": "ice_block"},
                    {"not_flag": "ice_packed"},
                    {"not_flag": "ice_held"},
                ]
            },
            "You pack the ice. Straw takes the cold.",
            [
                {"op": "remove_item", "item": "ice_block"},
                {"op": "set_flag", "flag": "ice_packed"},
            ],
        ),
        action(
            "bar_the_door",
            "Bar the door",
            "do",
            {
                "all": [
                    {"at": "ice.door"},
                    {"has_flag": "ice_trust"},
                    {"has_flag": "ice_packed"},
                    {"not_flag": "ice_held"},
                ]
            },
            "You bar the door. The hold keeps the cold.",
            [
                {"op": "set_flag", "flag": "ice_held"},
                {"op": "remember", "actor": "kest", "fact": "bar"},
            ],
        ),
        action(
            "ask_yul_rule",
            "Ask Yul the rule",
            "talk",
            {"at": "ice.yard"},
            "Yul says pack the ice. Then bar the door.",
            [{"op": "set_flag", "flag": "heard_ice_rule"}],
        ),
        action(
            "ask_saff_pit",
            "Ask Saff the pit",
            "talk",
            {"at": "ice.pit"},
            "Saff says cut only from the hard face.",
            [{"op": "set_flag", "flag": "heard_ice_rule"}],
        ),
        action(
            "ask_kest_bar",
            "Ask Kest the bar",
            "talk",
            {"at": "ice.door"},
            "Kest bars only a hold that is packed.",
            [{"op": "set_flag", "flag": "heard_ice_rule"}],
        ),
        action(
            "know_the_drowned_mark",
            "Know the drowned mark",
            "talk",
            {
                "all": [
                    {"at": "wreck.yard"},
                    {
                        "any": [
                            {"sheet": ["origin", "marshborn"]},
                            {"sheet": ["skill", "hunt"]},
                        ]
                    },
                    {"not_flag": "wreck_trust"},
                ]
            },
            "You name the drowned mark. Luth lets you wash and lay.",
            [
                {"op": "set_flag", "flag": "wreck_trust"},
                {"op": "remember", "actor": "luth", "fact": "drowned"},
            ],
        ),
        action(
            "read_the_wreck_list",
            "Read the wreck list",
            "do",
            {
                "all": [
                    {"at": "wreck.yard"},
                    {"sheet": ["skill", "letters"]},
                    {"not_flag": "wreck_trust"},
                ]
            },
            "You read the wreck list. Luth lets you wash and lay.",
            [
                {"op": "set_flag", "flag": "wreck_trust"},
                {"op": "remember", "actor": "luth", "fact": "list"},
            ],
        ),
        action(
            "keep_the_drowned_cold",
            "Keep the drowned cold",
            "do",
            {
                "all": [
                    {"at": "wreck.hull"},
                    {"has_flag": "ice_held"},
                    {"not_flag": "drowned_cold"},
                ]
            },
            "You keep the drowned cold. The token holds.",
            [
                {"op": "set_flag", "flag": "drowned_cold"},
                {"op": "set_flag", "flag": "wreck_trust"},
                {"op": "remember", "actor": "kade", "fact": "cold"},
            ],
        ),
        action(
            "wash_the_token",
            "Wash the token",
            "do",
            {
                "all": [
                    {"at": "wreck.wash"},
                    {"has_flag": "wreck_trust"},
                    {"has_item": "drowned_token"},
                    {"not_flag": "token_washed"},
                    {"not_flag": "wreck_laid"},
                ]
            },
            "You wash the token. Brine takes the silt.",
            [
                {"op": "remove_item", "item": "drowned_token"},
                {"op": "set_flag", "flag": "token_washed"},
            ],
        ),
        action(
            "lay_the_token",
            "Lay the token",
            "do",
            {
                "all": [
                    {"at": "wreck.altar"},
                    {"has_flag": "wreck_trust"},
                    {"has_flag": "token_washed"},
                    {"not_flag": "wreck_laid"},
                ]
            },
            "You lay the token. Efa marks the wreck rite done.",
            [
                {"op": "set_flag", "flag": "wreck_laid"},
                {"op": "remember", "actor": "efa", "fact": "laid"},
            ],
        ),
        action(
            "ask_luth_rule",
            "Ask Luth the rule",
            "talk",
            {"at": "wreck.yard"},
            "Luth says wash the token. Then lay it on the altar.",
            [{"op": "set_flag", "flag": "heard_wreck_rule"}],
        ),
        action(
            "ask_kade_silt",
            "Ask Kade the silt",
            "talk",
            {"at": "wreck.hull"},
            "Kade says the token lies in the silt.",
            [{"op": "set_flag", "flag": "heard_wreck_rule"}],
        ),
        action(
            "ask_efa_altar",
            "Ask Efa the altar",
            "talk",
            {"at": "wreck.altar"},
            "Efa lays only a token that has been washed.",
            [{"op": "set_flag", "flag": "heard_wreck_rule"}],
        ),
        action(
            "know_the_hive_hum",
            "Know the hive hum",
            "talk",
            {
                "all": [
                    {"at": "hive.yard"},
                    {
                        "any": [
                            {"sheet": ["origin", "marshborn"]},
                            {"sheet": ["skill", "hunt"]},
                        ]
                    },
                    {"not_flag": "hive_trust"},
                ]
            },
            "You name the hive hum. Sol lets you smoke and set.",
            [
                {"op": "set_flag", "flag": "hive_trust"},
                {"op": "remember", "actor": "sol", "fact": "hum"},
            ],
        ),
        action(
            "read_the_skep_mark",
            "Read the skep mark",
            "do",
            {
                "all": [
                    {"at": "hive.yard"},
                    {"sheet": ["skill", "letters"]},
                    {"not_flag": "hive_trust"},
                ]
            },
            "You read the skep mark. Sol lets you smoke and set.",
            [
                {"op": "set_flag", "flag": "hive_trust"},
                {"op": "remember", "actor": "sol", "fact": "mark"},
            ],
        ),
        action(
            "bless_the_skep",
            "Bless the skep",
            "do",
            {
                "all": [
                    {"at": "hive.skeps"},
                    {"has_flag": "wreck_laid"},
                    {"not_flag": "hive_blessed"},
                ]
            },
            "You bless the skep. The hive takes the drowned ward.",
            [
                {"op": "set_flag", "flag": "hive_blessed"},
                {"op": "set_flag", "flag": "hive_trust"},
                {"op": "remember", "actor": "tansy", "fact": "bless"},
            ],
        ),
        action(
            "smoke_the_hive",
            "Smoke the hive",
            "do",
            {
                "all": [
                    {"at": "hive.skeps"},
                    {"has_flag": "hive_trust"},
                    {"not_flag": "hive_smoked"},
                    {"not_flag": "hive_kept"},
                ]
            },
            "You smoke the hive. The bees drop and still.",
            [{"op": "set_flag", "flag": "hive_smoked"}],
        ),
        action(
            "set_the_skep",
            "Set the skep",
            "do",
            {
                "all": [
                    {"at": "hive.shed"},
                    {"has_flag": "hive_trust"},
                    {"has_flag": "hive_smoked"},
                    {"has_item": "comb_cake"},
                    {"not_flag": "hive_kept"},
                ]
            },
            "You set the skep. Wick marks the hive kept.",
            [
                {"op": "remove_item", "item": "comb_cake"},
                {"op": "set_flag", "flag": "hive_kept"},
                {"op": "remember", "actor": "wick", "fact": "set"},
            ],
        ),
        action(
            "ask_sol_rule",
            "Ask Sol the rule",
            "talk",
            {"at": "hive.yard"},
            "Sol says smoke the hive. Then take comb and set.",
            [{"op": "set_flag", "flag": "heard_hive_rule"}],
        ),
        action(
            "ask_tansy_smoke",
            "Ask Tansy the smoke",
            "talk",
            {"at": "hive.skeps"},
            "Tansy says a light smoke calms the hive.",
            [{"op": "set_flag", "flag": "heard_hive_rule"}],
        ),
        action(
            "ask_wick_skep",
            "Ask Wick the skep",
            "talk",
            {"at": "hive.shed"},
            "Wick sets only a hive that has been smoked.",
            [{"op": "set_flag", "flag": "heard_hive_rule"}],
        ),
        action(
            "know_the_wild_must",
            "Know the wild must",
            "talk",
            {
                "all": [
                    {"at": "mead.yard"},
                    {
                        "any": [
                            {"sheet": ["origin", "marshborn"]},
                            {"sheet": ["skill", "hunt"]},
                        ]
                    },
                    {"not_flag": "mead_trust"},
                ]
            },
            "You name the wild must. Hop lets you mash and tap.",
            [
                {"op": "set_flag", "flag": "mead_trust"},
                {"op": "remember", "actor": "hop", "fact": "must"},
            ],
        ),
        action(
            "read_the_cask_mark",
            "Read the cask mark",
            "do",
            {
                "all": [
                    {"at": "mead.yard"},
                    {"sheet": ["skill", "letters"]},
                    {"not_flag": "mead_trust"},
                ]
            },
            "You read the cask mark. Hop lets you mash and tap.",
            [
                {"op": "set_flag", "flag": "mead_trust"},
                {"op": "remember", "actor": "hop", "fact": "mark"},
            ],
        ),
        action(
            "pitch_true_comb",
            "Pitch true comb",
            "do",
            {
                "all": [
                    {"at": "mead.mash"},
                    {"has_flag": "hive_kept"},
                    {"not_flag": "mead_pitched"},
                ]
            },
            "You pitch true comb. The mash takes the hive wax.",
            [
                {"op": "set_flag", "flag": "mead_pitched"},
                {"op": "set_flag", "flag": "mead_trust"},
                {"op": "remember", "actor": "mal", "fact": "pitch"},
            ],
        ),
        action(
            "mash_the_must",
            "Mash the must",
            "do",
            {
                "all": [
                    {"at": "mead.mash"},
                    {"has_flag": "mead_trust"},
                    {"not_flag": "mead_mashed"},
                    {"not_flag": "mead_drawn"},
                ]
            },
            "You mash the must. The crock takes the sweet.",
            [{"op": "set_flag", "flag": "mead_mashed"}],
        ),
        action(
            "tap_the_cask",
            "Tap the cask",
            "do",
            {
                "all": [
                    {"at": "mead.tap"},
                    {"has_flag": "mead_trust"},
                    {"has_flag": "mead_mashed"},
                    {"has_item": "cask_bung"},
                    {"not_flag": "mead_drawn"},
                ]
            },
            "You tap the cask. Sera marks the mead drawn.",
            [
                {"op": "remove_item", "item": "cask_bung"},
                {"op": "set_flag", "flag": "mead_drawn"},
                {"op": "remember", "actor": "sera", "fact": "tap"},
            ],
        ),
        action(
            "ask_hop_rule",
            "Ask Hop the rule",
            "talk",
            {"at": "mead.yard"},
            "Hop says mash the must. Then bung and tap.",
            [{"op": "set_flag", "flag": "heard_mead_rule"}],
        ),
        action(
            "ask_mal_mash",
            "Ask Mal the mash",
            "talk",
            {"at": "mead.mash"},
            "Mal says mash until the comb breaks.",
            [{"op": "set_flag", "flag": "heard_mead_rule"}],
        ),
        action(
            "ask_sera_tap",
            "Ask Sera the tap",
            "talk",
            {"at": "mead.tap"},
            "Sera taps only a bunged mash.",
            [{"op": "set_flag", "flag": "heard_mead_rule"}],
        ),
    ]

    pack = {
        "id": "ashfen-coast",
        "version": "1",
        "regions": {
            "saltfen": {
                "name": "Saltfen Harbor",
                "mechanic": "law-trade-tides",
            },
            "hollow_stacks": {
                "name": "Hollow Stacks",
                "mechanic": "climb-collapse-vertical",
            },
            "kiln_mill": {
                "name": "Kiln Mill",
                "mechanic": "heat-craft-grain-debt",
            },
            "reed_court": {
                "name": "Reed Court",
                "mechanic": "law-witness-sentence",
            },
            "drowned_road": {
                "name": "Drowned Road",
                "mechanic": "weather-turn-encounters",
            },
            "fever_camp": {
                "name": "Fever Camp",
                "mechanic": "isolation-medicine",
            },
            "namehouse": {
                "name": "Namehouse",
                "mechanic": "names-rites-memory",
            },
            "peat_fold": {
                "name": "Peat Fold",
                "mechanic": "peat-cut-share",
            },
            "lens_ruin": {
                "name": "Lens Ruin",
                "mechanic": "light-lens-channel",
            },
            "ropewalk": {
                "name": "Ropewalk",
                "mechanic": "twist-tension-cordage",
            },
            "salt_pans": {
                "name": "Salt Pans",
                "mechanic": "brine-rake-weigh",
            },
            "smokehouse": {
                "name": "Smokehouse",
                "mechanic": "hang-tend-salt-cure",
            },
            "eel_weir": {
                "name": "Eel Weir",
                "mechanic": "set-baskets-lift-catch",
            },
            "dye_works": {
                "name": "Dye Works",
                "mechanic": "charge-dip-hang-color",
            },
            "toll_ferry": {
                "name": "Toll Ferry",
                "mechanic": "fare-load-pole-crossing",
            },
            "windpump": {
                "name": "Windpump",
                "mechanic": "vanes-crank-hold-flats",
            },
            "oyster_park": {
                "name": "Oyster Park",
                "mechanic": "spat-seed-cull",
            },
            "counting_house": {
                "name": "Counting House",
                "mechanic": "mark-tally-seal-day",
            },
            "ice_cellar": {
                "name": "Ice Cellar",
                "mechanic": "pack-ice-hold-cold",
            },
            "wreck_chapel": {
                "name": "Wreck Chapel",
                "mechanic": "wash-token-lay-altar",
            },
            "bee_skeps": {
                "name": "Bee Skeps",
                "mechanic": "smoke-hive-set-skep",
            },
            "mead_house": {
                "name": "Mead House",
                "mechanic": "mash-must-tap-cask",
            },
        },
        "locations": locations,
        "actors": actors,
        "items": items,
        "actions": actions,
        "outcomes": {
            "harbor_compact": {
                "name": "Harbor Compact",
                "when": {"has_flag": "compact_restored"},
            },
            "stack_relic": {
                "name": "Stack Relic",
                "when": {"has_item": "ash_relic"},
            },
            "kiln_pact": {
                "name": "Kiln Pact",
                "when": {"has_flag": "kiln_pact_sealed"},
            },
            "reed_sentence": {
                "name": "Reed Sentence",
                "when": {"has_flag": "reed_sentence_passed"},
            },
            "road_beacon": {
                "name": "Road Beacon",
                "when": {"has_flag": "beacon_lit"},
            },
            "fever_broken": {
                "name": "Fever Broken",
                "when": {"has_flag": "fever_broken"},
            },
            "name_restored": {
                "name": "Name Restored",
                "when": {"has_flag": "name_restored"},
            },
            "fold_held": {
                "name": "Fold Held",
                "when": {"has_flag": "fold_held"},
            },
            "lens_set": {
                "name": "Lens Set",
                "when": {"has_flag": "lens_set"},
            },
            "rope_walked": {
                "name": "Rope Walked",
                "when": {"has_flag": "rope_walked"},
            },
            "salt_raked": {
                "name": "Salt Raked",
                "when": {"has_flag": "salt_raked"},
            },
            "smoke_cured": {
                "name": "Smoke Cured",
                "when": {"has_flag": "smoke_cured"},
            },
            "weir_lifted": {
                "name": "Weir Lifted",
                "when": {"has_flag": "weir_lifted"},
            },
            "dye_struck": {
                "name": "Dye Struck",
                "when": {"has_flag": "dye_struck"},
            },
            "ferry_crossed": {
                "name": "Ferry Crossed",
                "when": {"has_flag": "ferry_crossed"},
            },
            "flats_drained": {
                "name": "Flats Drained",
                "when": {"has_flag": "flats_drained"},
            },
            "oyster_culled": {
                "name": "Oyster Culled",
                "when": {"has_flag": "oyster_culled"},
            },
            "tally_closed": {
                "name": "Tally Closed",
                "when": {"has_flag": "tally_closed"},
            },
            "ice_held": {
                "name": "Ice Held",
                "when": {"has_flag": "ice_held"},
            },
            "wreck_laid": {
                "name": "Wreck Laid",
                "when": {"has_flag": "wreck_laid"},
            },
            "hive_kept": {
                "name": "Hive Kept",
                "when": {"has_flag": "hive_kept"},
            },
            "mead_drawn": {
                "name": "Mead Drawn",
                "when": {"has_flag": "mead_drawn"},
            },
        },
        "start": {
            "location": "saltfen.dock",
            "hp": 6,
            "rep": {"watch": 0, "dockers": 0, "stackers": 0, "millers": 0, "court": 0, "road": 0, "camp": 0, "names": 0, "fold": 0, "glass": 0, "rope": 0, "salt": 0, "smoke": 0, "weir": 0, "dye": 0, "ferry": 0, "pump": 0, "oyster": 0, "count": 0, "ice": 0, "wreck": 0, "hive": 0, "mead": 0},
            "inventory": [],
            "flags": {},
        },
        "sheets": {
            "marsh_scout": {
                "origin": "marshborn",
                "body": "agile",
                "skill": "hunt",
                "creed": "freehand",
                "mark": "scarred",
                "tongue": "cant",
            },
            "city_oath": {
                "origin": "cityward",
                "body": "might",
                "skill": "letters",
                "creed": "oathbound",
                "mark": "clean",
                "tongue": "court",
            },
        },
    }
    return pack


def main() -> int:
    pack = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(pack, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUT} locations={len(pack['locations'])} actions={len(pack['actions'])} items={len(pack['items'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
