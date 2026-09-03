from __future__ import annotations

from dataclasses import dataclass

from adventure_forge.kernel.content import Content
from adventure_forge.kernel.effects import apply_effects
from adventure_forge.kernel.legal import enumerate_legal
from adventure_forge.kernel.seed import SeedCursor
from adventure_forge.kernel.state import GameState


@dataclass(frozen=True)
class StepResult:
    state: GameState
    cursor: SeedCursor
    accepted: bool
    action_id: str


def _unlock_outcomes(state: GameState, content: Content) -> None:
    for oid in content.outcomes:
        if oid in state.outcomes:
            continue
        if content.outcome_ready(oid, state):
            state.outcomes.append(oid)


def step(
    state: GameState,
    action_id: str,
    content: Content,
    cursor: SeedCursor,
) -> StepResult:
    """Pure transition. Does not mutate inputs. No clock, network, or ambient RNG."""
    nxt = state.clone()
    cur = cursor.clone()
    legal = {a.id: a for a in enumerate_legal(nxt, content)}
    if action_id not in legal:
        # Identity: illegal ids do not move the world or the cursor.
        return StepResult(state=state.clone(), cursor=cur, accepted=False, action_id=action_id)

    action = legal[action_id]
    text = apply_effects(action.effects, nxt, cur, content)
    nxt.last_text = text
    nxt.turn += 1
    nxt.log.append(
        {
            "turn": nxt.turn,
            "action": action_id,
            "accepted": True,
            "location": nxt.location,
        }
    )
    _unlock_outcomes(nxt, content)
    return StepResult(state=nxt, cursor=cur, accepted=True, action_id=action_id)
