"""I4 acceptor binds traces to the current pack. Tamper must fail that acceptor."""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from adventure_forge.kernel.content import load_pack
from adventure_forge.verify.i4 import TraceReject, accept_trace, check_i4
from adventure_forge.verify.tamper import check_tamper


def _load_traces() -> list[dict]:
    traces = []
    for path in sorted((ROOT / "traces").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        data.setdefault("id", path.stem)
        traces.append(data)
    return traces


class I4AcceptorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.content = load_pack()
        cls.traces = _load_traces()

    def test_honest_traces_accept(self) -> None:
        for trace in self.traces:
            result = accept_trace(self.content, trace)
            self.assertEqual(result.fingerprint, trace["final_fingerprint"])
            self.assertEqual(trace["build_id"], self.content.build_id)

    def test_tampered_build_id_rejected_by_acceptor(self) -> None:
        trace = copy.deepcopy(self.traces[0])
        trace["build_id"] = "tampered-build"
        with self.assertRaises(TraceReject) as ctx:
            accept_trace(self.content, trace)
        self.assertIn("build_id", str(ctx.exception))

    def test_stale_build_id_rejected_even_if_fingerprint_would_match(self) -> None:
        trace = copy.deepcopy(next(t for t in self.traces if t["id"] == "marsh_harbor_compact"))
        honest = accept_trace(self.content, copy.deepcopy(trace))
        trace["build_id"] = "stale-pack"
        trace["final_fingerprint"] = honest.fingerprint
        with self.assertRaises(TraceReject):
            accept_trace(self.content, trace)

    def test_tampered_seed_rejected_by_acceptor(self) -> None:
        trace = copy.deepcopy(self.traces[0])
        trace["seed"] = int(trace["seed"]) + 99
        with self.assertRaises(TraceReject):
            accept_trace(self.content, trace)

    def test_tampered_actions_rejected_by_acceptor(self) -> None:
        trace = copy.deepcopy(self.traces[0])
        trace["actions"] = list(trace["actions"]) + ["wait"]
        with self.assertRaises(TraceReject):
            accept_trace(self.content, trace)

    def test_tampered_final_fingerprint_rejected_by_acceptor(self) -> None:
        trace = copy.deepcopy(self.traces[0])
        trace["final_fingerprint"] = "0" * 64
        with self.assertRaises(TraceReject):
            accept_trace(self.content, trace)

    def test_check_i4_fails_when_a_witness_build_id_is_wrong(self) -> None:
        traces = copy.deepcopy(self.traces)
        target = next(t for t in traces if t["id"] == "marsh_harbor_compact")
        target["build_id"] = "tampered-build"
        with self.assertRaises(TraceReject):
            check_i4(self.content, traces)

    def test_check_tamper_detects_all_four_on_shipped_traces(self) -> None:
        check_tamper(self.content, self.traces)

    def test_check_tamper_drives_build_through_acceptor(self) -> None:
        src = Path(check_tamper.__code__.co_filename).read_text(encoding="utf-8")
        self.assertIn("accept_trace", src)
        self.assertIn('must_fail(build_changed, "build")', src)
        self.assertIn('must_fail(seed_changed, "seed")', src)
        self.assertIn('must_fail(actions_changed, "actions")', src)
        self.assertIn('must_fail(bad_final, "final")', src)


if __name__ == "__main__":
    unittest.main()
