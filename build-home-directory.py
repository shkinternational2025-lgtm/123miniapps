#!/usr/bin/env python3
# ============================================
# build-home-directory.py
# Injects a static, crawlable "all tools by category" directory into
# index.html between <!-- TOOL-DIRECTORY:start --> / :end markers (added
# before </main> on first run). Gives Google real, static links to every
# tool + category page instead of only JS-rendered ones.
#
# Run after tools.js changes:  python3 build-home-directory.py
# ============================================

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

# Category id -> (display name, hub slug), in display order.
CATS = [
    ("text", "Text Tools", "text-tools"),
    ("image", "Image Tools", "image-tools"),
    ("developer", "Developer Tools", "developer-tools"),
    ("converter", "Converters", "converters"),
    ("generator", "Generators", "generators"),
    ("calculator", "Calculators", "calculators"),
    ("security", "Security Tools", "security-tools"),
    ("design", "Design Tools", "design-tools"),
    ("content", "Content Tools", "content-tools"),
    ("productivity", "Productivity Tools", "productivity-tools"),
    ("fun", "Fun Tools", "fun-tools"),
]

START = "<!-- TOOL-DIRECTORY:start -->"
END = "<!-- TOOL-DIRECTORY:end -->"


def slugify(name):
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"^-+|-+$", "", s)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def load_tools():
    src = open(os.path.join(HERE, "assets/data/tools.js"), encoding="utf-8").read()
    seg = src[src.index("RAW_TOOLS = ["):src.index("const TOOLS")]
    tools = []
    for m in re.finditer(r"\{\s*id:\s*\d+.*?\}", seg, re.DOTALL):
        block = m.group(0)
        nm = re.search(r"\bname:\s*'((?:\\.|[^'])*)'", block)
        cm = re.search(r"\bcategory:\s*'([^']*)'", block)
        if nm and cm and not re.search(r"deleted:\s*true", block):
            name = nm.group(1).replace("\\'", "'")
            tools.append((name, cm.group(1), slugify(name)))
    return tools


def build_block(tools):
    total = len(tools)
    groups = []
    for cid, cname, cslug in CATS:
        items = sorted([t for t in tools if t[1] == cid], key=lambda t: t[0].lower())
        if not items:
            continue
        links = "\n".join(
            f'          <li><a class="dir-list__link" href="tools/{slug}.html">{esc(name)}</a></li>'
            for name, _, slug in items
        )
        groups.append(
            f'      <div class="dir-group">\n'
            f'        <h3 class="dir-group__title"><a href="categories/{cslug}.html">{esc(cname)}</a></h3>\n'
            f'        <ul class="dir-list">\n{links}\n        </ul>\n'
            f'      </div>'
        )
    body = "\n".join(groups)
    return f"""{START}
  <section class="section section--divided" id="tool-directory" aria-labelledby="tool-directory-heading">
    <div class="container">
      <div class="section__header">
        <span class="eyebrow">Full directory</span>
        <h2 id="tool-directory-heading">All {total} tools, by category</h2>
        <p>Every tool on 123MiniApps, grouped by category. Pick a category to explore, or jump straight to a tool.</p>
      </div>
      <div class="dir-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:var(--space-6)">
{body}
      </div>
    </div>
  </section>
  {END}"""


def main():
    tools = load_tools()
    block = build_block(tools)
    path = os.path.join(HERE, "index.html")
    html = open(path, encoding="utf-8").read()
    if START in html and END in html:
        html = re.sub(re.escape(START) + r".*?" + re.escape(END), block, html, flags=re.DOTALL)
    else:
        # Insert just before the closing </main>
        html = html.replace("</main>", block + "\n\n</main>", 1)
    open(path, "w", encoding="utf-8").write(html)
    print(f"injected static directory: {len(tools)} tools across {len(CATS)} categories")


if __name__ == "__main__":
    main()
