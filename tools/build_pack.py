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
        },
        "start": {
            "location": "saltfen.dock",
            "hp": 6,
            "rep": {"watch": 0, "dockers": 0, "stackers": 0},
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
