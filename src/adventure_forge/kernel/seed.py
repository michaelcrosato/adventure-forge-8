from __future__ import annotations

import hashlib
from dataclasses import dataclass


@dataclass
class SeedCursor:
    seed: int
    index: int = 0

    def clone(self) -> SeedCursor:
        return SeedCursor(self.seed, self.index)

    def to_dict(self) -> dict[str, int]:
        return {"seed": int(self.seed), "index": int(self.index)}

    @classmethod
    def from_dict(cls, data: dict[str, int]) -> SeedCursor:
        return cls(seed=int(data["seed"]), index=int(data["index"]))

    def draw(self, n: int) -> int:
        """Deterministic draw in [0, n). Mutates this cursor."""
        if n <= 0:
            raise ValueError("draw n must be positive")
        raw = f"{self.seed}:{self.index}".encode("utf-8")
        digest = hashlib.sha256(raw).digest()
        self.index += 1
        return int.from_bytes(digest[:8], "big") % n
