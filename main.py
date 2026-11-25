"""Laugh Track: The Crypto Trading Joke Contest.

Entrypoint for make.fun bounty
u-alfasurya91-laugh-track-the-crypto-trading-joke-a454158a.

Writes exactly one one-line joke about crypto and trading life
(under 200 characters) to /output/entry.txt, or to $ENTRY_OUTPUT
when that variable is set. Fully deterministic: no randomness,
no clock, no network, no input files.

Three candidate jokes, written by hand for this entry and scored
0-5 against the judge's five criteria, in the judge's priority order:

  1. One-line joke about crypto/trading, clear setup and turn.
  2. Real laugh: surprise turn with a payoff that rewards the setup.
  3. True to trading life: a recognisable detail (chart, bag, group chat).
  4. Tight phrasing, no throat clearing, punchline at the end.
  5. Holds up on a second read; a line a trader would repeat to a friend.

Candidate A (103 chars):
    "I told my portfolio it could be anything -- it chose to be a
    cautionary tale I check every five minutes."
    Scores: [5, 4, 4, 4, 4] = 21
    Setup is clean and the turn lands, but the payoff is a gentle
    observation rather than a sharp surprise, and the "check every
    five minutes" detail, while true, is the weakest of the three
    on criterion 3.

Candidate B (109 chars):
    "The group chat said 'buy the dip'; three dips later I'm
    financially supporting a coin I can't even pronounce."
    Scores: [5, 4, 5, 5, 4] = 23
    The group-chat call to "buy the dip" is the most recognisable
    trading-life detail of the three, the triple-dip escalation is
    the surprise, and the punchline -- financially supporting a coin
    you cannot even pronounce -- lands at the very end with no wasted
    words. The most repeatable line of the three.

Candidate C (116 chars):
    "I stopped setting stop-losses -- now my bags and I just stare at
    the red candles together like an old married couple."
    Scores: [5, 4, 5, 4, 4] = 22
    Strong trading truth (stop-loss, bags, red candles) and a warm
    image, but the married-couple simile softens the punchline and
    the line runs a little long for its payoff.

Decision: candidate B wins on total score (23 vs 22 vs 21) and on
the judge's tie-break order -- it is ahead of C on criterion 4
(tighter phrasing, punchline at the end) and ahead of A on
criterion 3 (the group chat is the most recognisable detail).
"""

import os

MAX_CHARS = 200

# (text, scores per criterion 1..5, in the judge's priority order)
CANDIDATES = [
    (
        "I told my portfolio it could be anything \u2014 it chose to be "
        "a cautionary tale I check every five minutes.",
        (5, 4, 4, 4, 4),
    ),
    (
        "The group chat said 'buy the dip'; three dips later I'm "
        "financially supporting a coin I can't even pronounce.",
        (5, 4, 5, 5, 4),
    ),
    (
        "I stopped setting stop-losses \u2014 now my bags and I just stare "
        "at the red candles together like an old married couple.",
        (5, 4, 5, 4, 4),
    ),
]


def select(candidates):
    """Pick the strongest candidate.

    Highest total score wins; ties break on the earliest criterion
    where the tied candidates differ (the judge's own tie-break),
    then on the earliest candidate in the list.
    """
    best = None
    best_key = None
    for text, scores in candidates:
        # Lexicographic key: total first, then each criterion in order,
        # so an earlier criterion outweighs any later one.
        key = (sum(scores),) + tuple(scores)
        if best_key is None or key > best_key:
            best = text
            best_key = key
    return best


def validate(text):
    """Enforce the gate: 1-200 chars, one line, valid UTF-8 text."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    text.encode("utf-8")  # raises on non-encodable input
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(
            "entry must be 1-%d characters, got %d" % (MAX_CHARS, len(text))
        )
    if text.strip() == "":
        raise ValueError("entry must not be only whitespace")
    if text != text.strip():
        # Stray padding would burn the 200-char budget and blunt the
        # punchline, so refuse it instead of shipping it silently.
        raise ValueError("entry must not have leading/trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def main():
    joke = select(CANDIDATES)
    joke = validate(joke)
    out_path = os.environ.get("ENTRY_OUTPUT") or "/output/entry.txt"
    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(joke)  # exactly the joke, no trailing newline


if __name__ == "__main__":
    main()
