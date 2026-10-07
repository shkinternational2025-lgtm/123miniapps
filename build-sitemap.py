#!/usr/bin/env python3
# ============================================
# 123MiniApps.online - build-sitemap.py
# Regenerates sitemap.xml from the public HTML on disk.
# Excludes build-only / non-indexable files (admin, template, debug, 404).
# Run after build-tool-page.py and build-blog.py.
# ============================================

import os
import glob
import re
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://www.123miniapps.online"
TODAY = date.today().isoformat()

EXCLUDE = {
    "404.html",
    "offline.html",
    "theme-debug.html",
    "tools/_template.html",
    "yandex_09607beaf7a1dd2b.html",   # search-engine verification token, not content
}
# Non-content trees: the Adsterra ad iframes under assets/, build deps, and admin.
EXCLUDE_DIRS = ("admin/", "assets/", "node_modules/", "test/")


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


IMG_RE = re.compile(r'(?:\.\./)?(assets/images/blog/[^"\'\s]+\.(?:webp|png|jpe?g))')


def article_images(rel_path):
    """Return absolute URLs of in-content images in a built HTML page,
    deduped and in document order, for Google Images indexing."""
    if not rel_path.startswith("blog/") or not rel_path.endswith(".html"):
        return []
    try:
        html = open(rel_path, encoding="utf-8").read()
    except OSError:
        return []
    seen, out = set(), []
    for m in IMG_RE.finditer(html):
        asset = m.group(1)
        if asset not in seen:
            seen.add(asset)
            out.append(f"{SITE}/{asset}")
    return out


def main():
    os.chdir(HERE)
    paths = site_paths()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f"<!-- 123MiniApps.online sitemap.xml (generated {TODAY}) -->",
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"'
        ' xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    ]
    img_total = 0
    for p in paths:
        prio, freq = rule(p)
        loc = f"{SITE}/{p}" if p else f"{SITE}/"
        lines += [
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{TODAY}</lastmod>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{prio}</priority>",
        ]
        for img in article_images(p):
            lines += [
                "    <image:image>",
                f"      <image:loc>{img}</image:loc>",
                "    </image:image>",
            ]
            img_total += 1
        lines.append("  </url>")
    lines.append("</urlset>")
    with open("sitemap.xml", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"sitemap.xml written: {len(paths)} URLs, {img_total} images, lastmod {TODAY}")


if __name__ == "__main__":
    main()
