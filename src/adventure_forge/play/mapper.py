"""Map plain language onto a legal action id.

I3: free text is sugar. It resolves to an id the engine already offered, or the
world does not move. Nothing here invents an action, widens the legal set, or
consults anything but the ids and labels the engine just enumerated.

Matching is token-based rather than substring-based, because a player writes
"talk to the dock boss" for a verb labelled "Talk to Dock boss" and a strict
substring match rejects it over the word "the".
"""

from __future__ import annotations

from adventure_forge.kernel.legal import LegalAction

UI_COMMANDS = frozenset({"more", "all", "help", "look", "inv", "inventory", "quit", "exit"})

# Function words carry no choice. Dropped from both sides, so they cancel.
STOPWORDS = frozenset(
    {
        "a", "an", "the", "to", "at", "in", "into", "on", "onto", "of", "off",
        "up", "down", "over", "with", "and", "for", "from", "my", "your", "some",
        "please", "then", "there", "here", "it", "its", "this", "that", "go",
        "about", "around",
        # Fillers and quantifiers. They pad a line without naming a choice, so
        # "wait a moment" is "wait" and "take everything" is "take".
        "moment", "while", "now", "again", "bit", "everything", "anything",
        "something", "stuff", "things", "thing",
    }
)

# A verb the player types implies the group they meant. This narrows the field;
# it never adds an action. `go` is also a stopword so that "go to market" and
# "market" resolve identically.
VERB_GROUPS: dict[str, str] = {
    "go": "go", "walk": "go", "head": "go", "move": "go", "enter": "go",
    "travel": "go", "visit": "go", "leave": "go", "exit": "go", "climb": "go",
    "take": "take", "get": "take", "grab": "take", "pick": "take",
    "collect": "take", "pocket": "take", "loot": "take",
    "drop": "drop", "put": "drop", "leave_behind": "drop",
    "talk": "talk", "speak": "talk", "ask": "talk", "say": "talk",
    "tell": "talk", "greet": "talk", "chat": "talk", "buy": "talk",
    "wait": "time", "rest": "time", "pause": "time",
}


def _norm(text: str) -> str:
    return " ".join(text.strip().lower().split())


def _tokens(text: str) -> list[str]:
    """Lowercase word tokens. Punctuation and separators are not choices."""
    out: list[str] = []
    word: list[str] = []
    for ch in text.lower():
        if ch.isalnum():
            word.append(ch)
        else:
            if word:
                out.append("".join(word))
                word = []
    if word:
        out.append("".join(word))
    return out


def _candidate_tokens(action: LegalAction) -> frozenset[str]:
    """Every word the player could reasonably have read off this action."""
    words = _tokens(action.label) + _tokens(action.id)
    return frozenset(w for w in words if w not in STOPWORDS)


def _best_unique(scored: list[tuple[int, str]]) -> str | None:
    """Highest score wins, but only if nothing ties it. A tie is ambiguous, and
    an ambiguous line must not move the world."""
    if not scored:
        return None
    best = max(score for score, _ in scored)
    winners = [aid for score, aid in scored if score == best]
    if len(winners) == 1:
        return winners[0]
    return None


def map_text(text: str, legal: list[LegalAction]) -> str | None:
    """Map plain language onto a legal id. Ambiguous or failed mapping returns None."""
    raw = text.strip()
    if not raw:
        return None
    lowered = _norm(raw)

    # 1. The id itself, or the label verbatim.
    by_id = {a.id: a for a in legal}
    if raw in by_id:
        return raw
    if lowered in by_id:
        return lowered

    by_label: dict[str, list[str]] = {}
    for action in legal:
        by_label.setdefault(_norm(action.label), []).append(action.id)
    if lowered in by_label and len(by_label[lowered]) == 1:
        return by_label[lowered][0]

    # 2. Token match. Iterate `legal` in its given order throughout — never a
    #    set — so the result cannot depend on hash ordering (I1).
    typed = _tokens(raw)
    if not typed:
        return None

    implied_group: str | None = None
    for token in typed:
        if token in VERB_GROUPS:
            implied_group = VERB_GROUPS[token]
            break

    content = [t for t in typed if t not in STOPWORDS and t not in VERB_GROUPS]

    def score_against(group: str | None, treat_verbs_as_content: bool) -> list[tuple[int, str]]:
        wanted = content if not treat_verbs_as_content else [t for t in typed if t not in STOPWORDS]
        if not wanted and group is None:
            # Everything typed was a function word. That names no action, and a
            # line that names no action does not move the world.
            return []
        scored: list[tuple[int, str]] = []
        for action in legal:
            if group is not None and action.group != group:
                continue
            cand = _candidate_tokens(action)
            matched = sum(1 for t in wanted if t in cand)
            if group is not None:
                # The group is already a real signal. Bare "wait" or "take"
                # names its group and nothing else, so an empty content list is
                # a guess; a content word that matches nothing is not.
                if wanted and matched == 0:
                    continue
            else:
                # With nothing but words, the first word is the verb the player
                # reached for. If the action does not contain it, they did not
                # name this action: "kill the dock boss" is not "Talk to Dock
                # boss" merely because both mention a dock boss.
                if wanted[0] not in cand:
                    continue
                # And a majority of what was typed must land, so one shared word
                # in a long line stays a coincidence rather than a command.
                if matched == 0 or matched * 2 <= len(wanted):
                    continue
            scored.append((matched, action.id))
        return scored

    if implied_group is not None:
        hit = _best_unique(score_against(implied_group, False))
        if hit is not None:
            return hit

    # No group, or the implied group held nothing: match on every word typed.
    return _best_unique(score_against(None, True))


def is_ui_command(text: str) -> bool:
    lowered = _norm(text)
    if lowered in UI_COMMANDS:
        return True
    if lowered.startswith("filter ") or lowered.startswith("page "):
        return True
    if lowered.isdigit():
        return True
    return False
