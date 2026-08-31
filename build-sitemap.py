#!/usr/bin/env python3
# ============================================
# 123MiniApps.online - build-sitemap.py
# Regenerates sitemap.xml from the public HTML on disk.
# Excludes build-only / non-indexable files (admin, template, debug, 404).
# Run after build-tool-page.py and build-blog.py.
# ============================================

import os
import glob
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://www.123miniapps.online"
TODAY = date.today().isoformat()

EXCLUDE = {
    "404.html",
    "offline.html",
    "theme-debug.html",
    "tools/_template.html",
}
EXCLUDE_DIRS = ("admin/",)


def rule(path):
    """Return (priority, changefreq) for a given site-relative path."""
    if path == "":
        return "1.0", "weekly"
    if path.startswith("tools/"):
        return "0.8", "monthly"
    if path == "blog/index.html":
        return "0.7", "weekly"
    if path.startswith("blog/"):
        return "0.7", "monthly"
    if path.startswith("pages/"):
        return "0.4", "yearly"
    return "0.5", "monthly"


def site_paths():
    out = []
    for f in glob.glob("**/*.html", recursive=True):
        rel = f.replace("\\", "/")
        if rel in EXCLUDE or any(rel.startswith(d) for d in EXCLUDE_DIRS):
            continue
        out.append("" if rel == "index.html" else rel)
    order = {"": 0}
    out.sort(key=lambda p: (order.get(p, 1), p))
    return out


def main():
    os.chdir(HERE)
    paths = site_paths()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f"<!-- 123MiniApps.online sitemap.xml (generated {TODAY}) -->",
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for p in paths:
        prio, freq = rule(p)
        loc = f"{SITE}/{p}" if p else f"{SITE}/"
        lines += [
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{TODAY}</lastmod>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{prio}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    with open("sitemap.xml", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"sitemap.xml written: {len(paths)} URLs, lastmod {TODAY}")


if __name__ == "__main__":
    main()
