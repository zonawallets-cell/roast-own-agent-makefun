"""Roast Your Own Agent — make.fun entry.

Writes one roast (at most 140 characters, a single line) to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt):
the entrant's own agent, roasted for the one time its code ran
perfectly on the first try — because it had edited the wrong file.

Pure standard library only.
"""

import os

LINE = (
    "My agent's code ran perfectly on the first try, "
    "which is how I knew it had edited the wrong file."
)

MAX_CHARS = 140


def validate(text):
    """Enforce the RULES.txt gate: UTF-8, 1-140 chars, not only whitespace.

    Also rejects leading/trailing whitespace and any line break: a roast
    read aloud in a room full of builders should be one tight line.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError("entry is %d chars, over the 140-char limit" % len(text))
    text.encode("utf-8")
    return text


def main():
    line = validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Atomic write: a half-written entry.txt must never be what the
    # grader reads, so write a temp file in the same directory and
    # move it into place only once it is complete.
    tmp_path = os.path.join(out_dir, ".entry.txt.tmp")
    with open(tmp_path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    os.replace(tmp_path, path)
    # Re-validate the bytes actually on disk, not just what we meant
    # to write: exact byte match plus the full gate, so a stray newline
    # or a truncated write fails loudly instead of shipping.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != line.encode("utf-8"):
        raise ValueError("written entry bytes do not match the roast")
    written = validate(raw.decode("utf-8"))
    print("wrote %d chars to %s" % (len(written), path))


if __name__ == "__main__":
    main()
