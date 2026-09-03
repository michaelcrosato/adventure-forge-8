from __future__ import annotations

from adventure_forge.kernel.canon import canonical_dumps, sha256_hex
from adventure_forge.kernel.seed import SeedCursor
from adventure_forge.kernel.state import GameState


def fingerprint(state: GameState, cursor: SeedCursor) -> str:
    payload = {"state": state.to_dict(), "cursor": cursor.to_dict()}
    return sha256_hex(canonical_dumps(payload))
