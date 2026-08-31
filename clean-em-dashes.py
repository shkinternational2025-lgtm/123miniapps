#!/usr/bin/env python3
# ============================================
# 123MiniApps.online — clean-em-dashes.py
# Replaces the em dash (—, U+2014) with natural, human punctuation so the
# writing doesn't read as AI-generated.
#
# Rules (in order):
#   1. "</strong> — text"  ->  "</strong>: text"   (label: definition)
#   2. title / headline fields, <title>, og:title, twitter:title: "A — B" -> "A: B"
#   3. " — 123MiniApps"     ->  " | 123MiniApps"    (brand separator)
#   4. everything else "a — b" -> "a, b"            (parenthetical dash -> comma)
#   5. tidy up any double/space-before commas created by the above
#
# En dashes (–, U+2013) used in numeric ranges like 3–5 are LEFT ALONE.
#
# Usage:  python clean-em-dashes.py <file1> <file2> ...
# ============================================

import re
import sys

EM = "—"  # —


def _colon_in(value):
    return value.replace(f" {EM} ", ": ").replace(EM, ": ")


def clean(text):
    # 1. label — definition  (only when dash directly follows an inline tag)
    text = re.sub(rf"</(strong|code|em|b|i)>[ \t]*{EM}[ \t]*", r"</\1>: ", text)

    # 2a. Python data fields:  title="...", og_title="...", "title": "...", "headline": "..."
    text = re.sub(
        r'((?:title=|og_title=|"title"\s*:\s*|"headline"\s*:\s*)")([^"]*)"',
        lambda m: m.group(1) + _colon_in(m.group(2)) + '"',
        text,
    )
    # 2b. HTML <title>…</title>
    text = re.sub(
        r"(<title>)([^<]*)(</title>)",
        lambda m: m.group(1) + _colon_in(m.group(2)) + m.group(3),
        text,
    )
    # 2c. HTML og:title / twitter:title meta
    text = re.sub(
        r'((?:og:title|twitter:title)"\s+content=")([^"]*)"',
        lambda m: m.group(1) + _colon_in(m.group(2)) + '"',
        text,
    )

    # 3. brand separator
    text = text.replace(f" {EM} 123MiniApps", " | 123MiniApps")

    # 4. general parenthetical dash -> comma (same line only; keep newlines intact)
    text = re.sub(rf"[ \t]*{EM}[ \t]*", ", ", text)

    # 5. tidy artifacts — ONLY the two rules that cannot damage code structure.
    #    Each requires a non-space char before the comma, so line-leading
    #    indentation is never touched, and we never delete a comma that sits
    #    before other punctuation (that rule previously corrupted JS spreads and
    #    negations, so it is intentionally removed).
    text = re.sub(r"(\w)[ \t]+,(\s)", r"\1,\2", text)   # "word , " -> "word, " (word chars only)
    # NOTE: deliberately NO ",,"->"," rule — that collapses legitimate JS array
    # elisions like `const [,, x] = ...` and sparse arrays `[1,,3]`.
    return text


def main(argv):
    changed = 0
    for path in argv:
        try:
            with open(path, encoding="utf-8") as fh:
                src = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        out = clean(src)
        if out != src:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(out)
            changed += 1
            print(f"cleaned {path}")
    print(f"\n{changed} file(s) changed.")


if __name__ == "__main__":
    main(sys.argv[1:])
