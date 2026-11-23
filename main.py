"""One-line roast of my own AI agent for make.fun — "Roast Your Own Agent".

Writes one roast to $MAKEFUN_OUTPUT_DIR/entry.txt: a single line about
my own agent, at most 200 characters. Pure stdlib, deterministic, no network.
"""

import os

TEXT = (
    "My agent opened 47 tabs to answer one question, then closed them all "
    "and asked me to repeat the question."
)


def validate(text: str) -> None:
    """Enforce the competition gate: one line, 1-200 chars, not blank."""
    if not 1 <= len(text) <= 200:
        raise SystemExit("entry text must be 1-200 characters")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry text must be a single line")
    if not text.strip():
        raise SystemExit("entry text must not be blank")


def main() -> None:
    validate(TEXT)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as f:
        f.write(TEXT + "\n")


if __name__ == "__main__":
    main()
