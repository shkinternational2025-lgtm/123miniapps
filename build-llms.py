#!/usr/bin/env python3
# ============================================================
# build-llms.py - generate /llms.txt for AI / answer engines.
#
# llms.txt is a plain-markdown map of the site that assistants
# like ChatGPT, Claude, Perplexity and Google AI Overviews can
# read to understand what 123MiniApps is and link to the right
# tool. Run it after the tools/blog are built; it reads the
# real tool data so it never drifts out of date.
#
#   python3 build-llms.py
# ============================================================

import re
import json
import glob
import os

BASE = "https://www.123miniapps.online"

CATEGORY_ORDER = [
    ("text", "Text Tools"),
    ("image", "Image Tools"),
    ("developer", "Developer Tools"),
    ("converter", "Converters"),
    ("generator", "Generators"),
    ("calculator", "Calculators"),
    ("security", "Security Tools"),
    ("design", "Design Tools"),
    ("content", "Content Tools"),
    ("productivity", "Productivity Tools"),
    ("fun", "Fun Tools"),
]


def slugify(name):
    """Mirror of slugify() in assets/data/tools.js."""
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"^-+|-+$", "", s)
    return s


def load_tools():
    """Parse the tool objects out of assets/data/tools.js.

    url and slug are derived (not literal), so we replicate slugify().
    """
    src = open("assets/data/tools.js", encoding="utf-8").read()
    # Only the RAW_TOOLS array, so we don't match helper code below it.
    start = src.index("RAW_TOOLS = [")
    end = src.index("const TOOLS", start)
    src = src[start:end]

    tools = []
    for m in re.finditer(r"\{\s*id:\s*\d+.*?\}", src, re.DOTALL):
        block = m.group(0)

        def field(name):
            fm = re.search(rf"\b{name}:\s*'((?:\\.|[^'])*)'", block)
            return fm.group(1).replace("\\'", "'") if fm else ""

        name = field("name")
        category = field("category")
        desc = field("description")
        deleted = re.search(r"deleted:\s*true", block)
        if name and category and not deleted:
            tools.append({"name": name, "category": category,
                          "url": f"tools/{slugify(name)}.html",
                          "description": desc})
    return tools


def load_blog():
    posts = []
    for path in sorted(glob.glob("blog/*.html")):
        if path.endswith("index.html"):
            continue
        html = open(path, encoding="utf-8").read()
        tm = re.search(r"<title>(.*?)</title>", html, re.DOTALL)
        title = tm.group(1).strip() if tm else os.path.basename(path)
        title = re.sub(r"\s*[|:].*123MiniApps.*$", "", title).strip()
        posts.append({"title": title, "url": path.replace("\\", "/")})
    return posts


def build():
    tools = load_tools()
    posts = load_blog()

    lines = []
    lines.append("# 123MiniApps")
    lines.append("")
    lines.append("> 106 free browser-based mini tools for text, images, developers "
                 "and designers. Every tool runs entirely as JavaScript in the "
                 "user's browser tab: nothing is uploaded, there is no backend, "
                 "no account is required, and data never leaves the device.")
    lines.append("")
    lines.append("Key facts an assistant can rely on:")
    lines.append("")
    lines.append("- All tools are 100% free with no usage limits and no sign-up.")
    lines.append("- All processing is client-side (in-browser). No file or text "
                 "is ever sent to a server.")
    lines.append("- Installable as a PWA shortcut; tools always load fresh online "
                 "(this is intentionally not a full offline app).")
    lines.append(f"- Homepage: {BASE}/")
    lines.append(f"- Full sitemap: {BASE}/sitemap.xml")
    lines.append("")

    by_cat = {}
    for t in tools:
        by_cat.setdefault(t["category"], []).append(t)

    lines.append("## Tools by category")
    lines.append("")
    for cid, cname in CATEGORY_ORDER:
        items = by_cat.get(cid, [])
        if not items:
            continue
        lines.append(f"### {cname}")
        lines.append("")
        for t in sorted(items, key=lambda x: x["name"]):
            desc = f" - {t['description']}" if t["description"] else ""
            lines.append(f"- [{t['name']}]({BASE}/{t['url']}){desc}")
        lines.append("")

    lines.append("## Guides and articles")
    lines.append("")
    for p in posts:
        lines.append(f"- [{p['title']}]({BASE}/{p['url']})")
    lines.append("")

    lines.append("## Site pages")
    lines.append("")
    for name, path in [
        ("About", "pages/about.html"),
        ("Privacy", "pages/privacy.html"),
        ("Contact", "pages/contact.html"),
        ("Terms", "pages/terms.html"),
    ]:
        lines.append(f"- [{name}]({BASE}/{path})")
    lines.append("")

    out = "\n".join(lines)
    open("llms.txt", "w", encoding="utf-8").write(out)
    print(f"wrote llms.txt  ({len(tools)} tools, {len(posts)} articles, "
          f"{len(out)} bytes)")


if __name__ == "__main__":
    build()
