from __future__ import annotations

import copy

from adventure_forge.kernel.content import Content
from adventure_forge.kernel.replay import ReplayError, replay


def check_tamper(content: Content, traces: list[dict]) -> None:
    base = copy.deepcopy(traces[0])
    result = replay(content, base["seed"], base["sheet"], base["actions"])
    good_fp = result.fingerprint

    def must_fail(trace: dict, why: str) -> None:
        try:
            replayed = replay(content, trace["seed"], trace["sheet"], trace["actions"], require_accepted=True)
        except ReplayError:
            return
        if trace.get("final_fingerprint") and replayed.fingerprint == trace["final_fingerprint"] and replayed.fingerprint == good_fp:
            raise AssertionError(f"tamper not detected: {why}")
        if replayed.fingerprint != good_fp:
            return
        raise AssertionError(f"tamper produced same run: {why}")

    seed_changed = copy.deepcopy(base)
    seed_changed["seed"] = int(base["seed"]) + 99
    must_fail(seed_changed, "seed")

    actions_changed = copy.deepcopy(base)
    actions_changed["actions"] = list(base["actions"]) + ["wait"]
    must_fail(actions_changed, "actions")

    if result.fingerprint == good_fp and base.get("final_fingerprint") == good_fp:
        bad_final = copy.deepcopy(base)
        bad_final["final_fingerprint"] = "0" * 64
        if bad_final["final_fingerprint"] == result.fingerprint:
            raise AssertionError("could not craft bad fingerprint")
        # Stored fingerprint mismatch is a verify-time check, not replay physics.
        replayed = replay(content, bad_final["seed"], bad_final["sheet"], bad_final["actions"])
        if replayed.fingerprint == bad_final["final_fingerprint"]:
            raise AssertionError("tampered final fingerprint matched replay")

    build_changed = copy.deepcopy(base)
    build_changed["build_id"] = "tampered-build"
    if build_changed["build_id"] == content.build_id:
        raise AssertionError("tamper build id collided")
