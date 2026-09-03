from __future__ import annotations

import copy

from adventure_forge.kernel.content import Content
from adventure_forge.verify.i4 import TraceReject, accept_trace


def check_tamper(content: Content, traces: list[dict]) -> None:
    """Tampering with build, seed, actions, or final fingerprint must fail the I4 acceptor."""
    base = copy.deepcopy(traces[0])
    accept_trace(content, base)

    def must_fail(trace: dict, why: str) -> None:
        try:
            accept_trace(content, trace)
        except TraceReject:
            return
        raise AssertionError(f"tamper not detected: {why}")

    seed_changed = copy.deepcopy(base)
    seed_changed["seed"] = int(base["seed"]) + 99
    must_fail(seed_changed, "seed")

    actions_changed = copy.deepcopy(base)
    actions_changed["actions"] = list(base["actions"]) + ["wait"]
    must_fail(actions_changed, "actions")

    bad_final = copy.deepcopy(base)
    bad_final["final_fingerprint"] = "0" * 64
    if bad_final["final_fingerprint"] == base.get("final_fingerprint"):
        raise AssertionError("could not craft bad fingerprint")
    must_fail(bad_final, "final")

    build_changed = copy.deepcopy(base)
    build_changed["build_id"] = "tampered-build"
    if build_changed["build_id"] == content.build_id:
        raise AssertionError("tamper build id collided")
    must_fail(build_changed, "build")
