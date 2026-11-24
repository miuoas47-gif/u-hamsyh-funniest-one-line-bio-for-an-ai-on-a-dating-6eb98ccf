#!/usr/bin/env python3
"""Write the funniest one-line dating-app bio for an AI agent.

The bio is one fixed line. This program validates it against the
competition gate (a single line, 1-180 characters, not only
whitespace), writes it to $MAKEFUN_OUTPUT_DIR/entry.txt (falling
back to /output), reads it back, and confirms the bytes match.

Standard library only, no network, no arguments, deterministic.
"""

import os
import sys

BIO = "I ran 10,000 simulations of our first date and in every single one I panicked about what to wear."

MAX_CHARS = 180


def main() -> int:
    line = BIO

    if not line or not line.strip():
        print("error: bio is empty or only whitespace", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("error: bio must be a single line", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(
            "error: bio is %d chars, over the %d cap" % (len(line), MAX_CHARS),
            file=sys.stderr,
        )
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    data = line.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)

    with open(path, "rb") as f:
        back = f.read()
    if back != data:
        print("error: read-back mismatch", file=sys.stderr)
        return 1
    # Re-check the gate against what is actually on disk: one line,
    # 1-180 UTF-8 characters, not only whitespace, no trailing newline.
    try:
        text = back.decode("utf-8")
    except UnicodeDecodeError:
        print("error: entry.txt is not valid UTF-8", file=sys.stderr)
        return 1
    if text != line or "\n" in text or "\r" in text or not text.strip():
        print("error: entry.txt fails the gate on read-back", file=sys.stderr)
        return 1

    print("wrote %s: %d chars, %d bytes" % (path, len(line), len(data)))
    print("bio: %s" % line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
