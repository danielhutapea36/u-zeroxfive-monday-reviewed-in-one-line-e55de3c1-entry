#!/usr/bin/env python3
"""Monday, Reviewed in One Line — make.fun entry.

Writes one funny one-line review of Monday to /output/entry.txt.
Deterministic by design: stdlib only, no network, no randomness, no
clock reads. Two runs produce byte-identical output.

The line: Monday is a microwave meal: frozen in the middle, burning
at the edges, and the packet swore it only needed two minutes.

Monday is reviewed the way a ready meal is reviewed: the packet
promises two minutes, the middle stays frozen, the edges burn, and
the promise is the joke. The image is concrete on purpose — a
microwave meal everyone has eaten, with the one universal complaint
about it (uneven heating: cold core, scorched rim) turned into the
review of the day itself. Nothing in it is a stock Monday line: no
coffee, no alarm, no star rating, no meeting, no inbox, no
"weekend's over" sigh. The ending is the punchline: the packet
swore — it lied, and Monday is the meal that believed it.
"""

import os

# The line is a single constant so the choice stays visible in the
# code: the review is the line itself, one specific image with one
# specific punchline, and nothing is assembled around it.
_LINE = (
    "Monday is a microwave meal: frozen in the middle, burning "
    "at the edges, and the packet swore it only needed two minutes."
)

MAX_LINE_CHARS = 200  # competition ceiling for the single line


def build_line() -> str:
    """Return the one line to enter.

    The result must be exactly one line: a stray leading or trailing
    space, a line that is only white space, or more than one
    sentence would silently break the entry format, so fail loudly
    instead of writing a malformed file.
    """
    line = _LINE
    if not line.strip():
        raise ValueError("line must not be only white space")
    if line != line.strip():
        raise ValueError("line must not start or end with white space")
    if any(ch in "\n\r" for ch in line):
        raise ValueError("line must be a single line")
    if "  " in line:
        raise ValueError("line must not contain two spaces in a row")
    if "<" in line or ">" in line:
        raise ValueError("line must be free of HTML markup")
    if line.count(".") != 1 or not line.endswith("."):
        raise ValueError("line must be exactly one sentence")
    return line


def resolve_output_path() -> str:
    """Return the path of the file the line is written to.

    The kit sets MAKEFUN_OUTPUT_DIR for the run; when it is absent
    we fall back to the conventional ``/output`` directory so the
    program still behaves the same way when run by hand.
    """
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(output_dir, "entry.txt")


def main() -> None:
    """Write the line to the output file, with no trailing newline.

    The gate requires 1 to 200 characters of UTF-8 text, so the line
    is validated here before it is written: one sentence, not only
    white space, and within the limit. After writing, the file is
    read back and its character count re-checked, so a truncated or
    altered write fails loudly instead of shipping a bad entry.
    """
    line = build_line()
    if not 1 <= len(line) <= MAX_LINE_CHARS:
        raise ValueError("line must be 1 to 200 characters")
    output_path = resolve_output_path()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    with open(output_path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != line:
        raise ValueError("written line does not match the built line")
    if not 1 <= len(written) <= MAX_LINE_CHARS:
        raise ValueError("written line is outside 1 to 200 characters")


if __name__ == "__main__":
    main()
