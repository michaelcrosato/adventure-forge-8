"""Guards against the regression this repo already shipped once.

119 structurally identical regions landed in a single commit under a green bar,
because nothing in `verify` could tell one region from another. These tests do
not check that the world is good. They check that the bar can still *notice*
when it gets worse — that the sameness ratchet, the web trust boundary, and the
mapper's refusal to invent actions all actually fire.

A test here failing means a guard stopped guarding.
"""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from adventure_forge.kernel.content import Content, load_pack
from adventure_forge.kernel.legal import enumerate_legal
from adventure_forge.kernel.replay import new_game
from adventure_forge.play.mapper import map_text
from adventure_forge.play.session import MAX_CLIENT_ACTIONS, PlaySession
from adventure_forge.verify.sameness import (
    SamenessFail,
    check_sameness,
    clone_classes,
    measure,
    wallpaper_locations,
)
from adventure_forge.verify.web_surface import WebSurfaceFail, check_web_surface
from adventure_forge.web import play_turn


def _mutable(content: Content) -> dict:
    return copy.deepcopy(content.raw)


def _as_content(raw: dict) -> Content:
    return Content(raw=raw, build_id="test-build")


class SamenessRatchetTests(unittest.TestCase):
    """The check that would have caught the 119-region commit."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.content = load_pack()

    def test_baseline_file_exists_and_matches_shape(self) -> None:
        path = ROOT / "sameness-baseline.json"
        self.assertTrue(path.exists(), "the ratchet has no baseline")
        doc = json.loads(path.read_text(encoding="utf-8"))
        for key in ("limits", "targets", "notes"):
            self.assertIn(key, doc)
        now = measure(self.content)
        for metric in doc["limits"]:
            self.assertIn(metric, now, f"baseline records {metric}, which is no longer measured")

    def test_live_pack_largest_clone_class_is_at_most_three(self) -> None:
        """Shipped pack via the real loader and real `measure`.

        The 118-region vocabulary-swap class must not return. Same-kind shops
        may still share a fingerprint; that class is capped at the G4 target.
        """
        now = measure(self.content)
        self.assertLessEqual(now["largest_clone_class"], 3)
        classes = clone_classes(self.content)
        self.assertTrue(
            any(len(members) == 1 for members in classes.values()),
            "unique coast regions disappeared with the clones",
        )

    def test_current_pack_passes_its_own_ratchet(self) -> None:
        check_sameness(self.content)

    def test_adding_a_clone_region_fails(self) -> None:
        """Ship region 145 as a copy of an existing one: the bar must refuse."""
        raw = _mutable(self.content)
        classes = clone_classes(self.content)
        biggest = max(classes.values(), key=len)
        source = biggest[0]

        raw["regions"]["clone_probe"] = {"name": "Clone Probe", "mechanic": "probe-probe-probe"}
        mapping: dict[str, str] = {}
        for lid, loc in list(raw["locations"].items()):
            if loc.get("region") != source:
                continue
            new_id = f"probe.{lid.split('.')[-1]}"
            mapping[lid] = new_id
            clone = copy.deepcopy(loc)
            clone["region"] = "clone_probe"
            raw["locations"][new_id] = clone
        for old_id, new_id in mapping.items():
            for spec in raw["locations"][new_id].get("exits", []):
                spec["to"] = mapping.get(str(spec["to"]), str(spec["to"]))
        for action in list(raw["actions"]):
            text = json.dumps(action)
            if not any(f'"{old}"' in text for old in mapping):
                continue
            clone = json.loads(text)
            clone["id"] = f"probe_{clone['id']}"
            for old_id, new_id in mapping.items():
                clone = json.loads(json.dumps(clone).replace(f'"{old_id}"', f'"{new_id}"'))
            raw["actions"].append(clone)

        mutated = _as_content(raw)
        after = measure(mutated)
        self.assertGreater(
            after["largest_clone_class"],
            measure(self.content)["largest_clone_class"],
            "cloning a region did not grow a clone class — the fingerprint is too coarse",
        )
        with self.assertRaises(SamenessFail):
            check_sameness(mutated)

    def test_adding_a_room_with_no_verbs_fails(self) -> None:
        raw = _mutable(self.content)
        raw["locations"]["probe.empty"] = {
            "name": "Empty Probe",
            "region": "saltfen",
            "situation": "Nothing here asks anything of you.",
            "exits": [],
            "actors": [],
            "ground": [],
        }
        mutated = _as_content(raw)
        self.assertIn("probe.empty", wallpaper_locations(mutated))
        with self.assertRaises(SamenessFail):
            check_sameness(mutated)

    def test_letting_a_live_op_go_dark_fails(self) -> None:
        """`heal` is used three times. Losing it must not pass silently."""
        raw = _mutable(self.content)
        for action in raw["actions"]:
            action["effects"] = [e for e in action.get("effects", []) if e.get("op") != "heal"]
        mutated = _as_content(raw)
        self.assertIn("heal", measure(mutated)["unused_effect_ops"])
        with self.assertRaises(SamenessFail):
            check_sameness(mutated)

    def test_every_ratcheted_metric_actually_fires(self) -> None:
        """Each direction in RATCHET must be enforced, not just declared.

        Tested against the live measurement with a tightened baseline, so a
        metric silently dropped from the comparison shows up here.
        """
        from adventure_forge.verify import sameness as mod

        now = measure(self.content)
        real = mod.load_baseline
        for metric, worse in mod.RATCHET.items():
            limits = dict(real()["limits"])
            # Move the limit just past the current value, in the failing direction.
            if worse == "up":
                limits[metric] = now[metric] - 1
            else:
                limits[metric] = now[metric] + 1
            mod.load_baseline = lambda limits=limits: {"limits": limits}
            try:
                with self.assertRaises(SamenessFail, msg=f"{metric} is not enforced"):
                    check_sameness(self.content)
            finally:
                mod.load_baseline = real

    def test_a_missing_limit_is_refused(self) -> None:
        """A baseline that quietly drops a metric must not read as a pass."""
        from adventure_forge.verify import sameness as mod

        real = mod.load_baseline
        limits = dict(real()["limits"])
        limits.pop("largest_clone_class")
        mod.load_baseline = lambda: {"limits": limits}
        try:
            with self.assertRaises(SamenessFail):
                check_sameness(self.content)
        finally:
            mod.load_baseline = real


class WebTrustBoundaryTests(unittest.TestCase):
    """The hole that awarded 139 of 144 outcomes in one POST."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.content = load_pack()

    def test_surface_passes_its_own_check(self) -> None:
        check_web_surface(self.content)

    def test_forged_state_is_refused(self) -> None:
        player = PlaySession.start(self.content, 1, "marsh_scout")
        forged = json.loads(json.dumps(player.dump()))
        forged["state"]["flags"] = {flag: True for flag in self.content.outcomes}
        with self.assertRaises(ValueError):
            play_turn(session=forged, line="wait")

    def test_forged_cursor_alone_is_refused(self) -> None:
        payload = {
            "build_id": self.content.build_id,
            "seed": 1,
            "sheet": "marsh_scout",
            "cursor": {"seed": 1, "n": 0},
        }
        with self.assertRaises(ValueError):
            play_turn(session=payload)

    def test_unbounded_history_is_refused(self) -> None:
        payload = {
            "build_id": self.content.build_id,
            "seed": 1,
            "sheet": "marsh_scout",
            "actions": ["wait"] * (MAX_CLIENT_ACTIONS + 1),
        }
        with self.assertRaises(ValueError):
            play_turn(session=payload)

    def test_local_save_still_restores_exactly(self) -> None:
        """The trusted path is a real feature and must keep working."""
        import tempfile

        live = PlaySession.start(self.content, 1, "marsh_scout")
        live.apply_line("go:saltfen.market")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "save.json"
            live.save(path)
            back = PlaySession.load(self.content, path)
        self.assertEqual(back.fingerprint(), live.fingerprint())

    def test_reopening_the_hole_is_caught(self) -> None:
        """If someone drops `trusted=False`, the bar must go red.

        This is the test that makes the others matter: it proves the check
        fails when the guard is removed, rather than passing for its own
        unrelated reasons.
        """
        original = PlaySession.from_dump

        def permissive(content, payload, *, trusted=True):
            return original(content, payload, trusted=True)

        PlaySession.from_dump = permissive  # type: ignore[method-assign]
        try:
            with self.assertRaises(WebSurfaceFail):
                check_web_surface(self.content)
        finally:
            PlaySession.from_dump = original  # type: ignore[method-assign]


class MapperTests(unittest.TestCase):
    """Plain language must reach the verb, and nothing else may move the world."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.content = load_pack()

    def _legal_at_start(self):
        state, _ = new_game(self.content, 1, "marsh_scout")
        return enumerate_legal(state, self.content)

    def test_natural_phrasings_resolve(self) -> None:
        legal = self._legal_at_start()
        cases = {
            "go to the market": "go:saltfen.market",
            "head to market": "go:saltfen.market",
            "walk to market": "go:saltfen.market",
            "enter the market": "go:saltfen.market",
            "talk to the dock boss": "talk:dock_boss",
            "speak with the dock boss": "talk:dock_boss",
            "ask boss for work": "ask_boss_for_work",
            "take the frayed rope": "take:frayed_rope",
            "pick up the rope": "take:frayed_rope",
            "grab rope": "take:frayed_rope",
            "wait a moment": "wait",
        }
        for line, expected in cases.items():
            with self.subTest(line=line):
                self.assertEqual(map_text(line, legal), expected)

    def test_nonsense_never_maps(self) -> None:
        legal = self._legal_at_start()
        for line in (
            "summon a star from the sea",
            "xyzzy",
            "dance wildly",
            "become king",
            "burn down the dock",
            "kill the dock boss",
            "steal every rope in town",
            "go to nowhere",
            "sing a song about rope",
        ):
            with self.subTest(line=line):
                self.assertIsNone(map_text(line, legal), f"{line!r} should not map")

    def test_ambiguity_does_not_move_the_world(self) -> None:
        """Two verbs mention the boss, so "boss" alone is a question, not a move."""
        legal = self._legal_at_start()
        self.assertIsNone(map_text("boss", legal))

    def test_mapping_never_leaves_the_legal_set(self) -> None:
        legal = self._legal_at_start()
        ids = {a.id for a in legal}
        for line in ("market", "rope", "boss", "wait", "take", "go", "talk to someone"):
            mapped = map_text(line, legal)
            if mapped is not None:
                self.assertIn(mapped, ids, f"{line!r} mapped outside the legal set")

    def test_unmapped_text_leaves_the_fingerprint_alone(self) -> None:
        session = PlaySession.start(self.content, 1, "marsh_scout")
        before = session.fingerprint()
        result = session.apply_line("conjure a bridge of salt")
        self.assertFalse(result.accepted)
        self.assertEqual(session.fingerprint(), before)


if __name__ == "__main__":
    unittest.main()
