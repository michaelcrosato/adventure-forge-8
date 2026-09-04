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
        },
        "start": {
            "location": "saltfen.dock",
            "hp": 6,
            "rep": {"watch": 0, "dockers": 0, "stackers": 0, "millers": 0, "court": 0, "road": 0, "camp": 0, "names": 0, "fold": 0},
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
