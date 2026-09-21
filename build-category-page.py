#!/usr/bin/env python3
# ============================================
# 123MiniApps.online - build-category-page.py
# Generates a standalone, indexable hub page per category at
# /categories/<slug>.html. Each hub lists every tool in the category
# (static, crawlable links), carries CollectionPage + ItemList +
# BreadcrumbList schema, and cross-links sibling categories.
#
# Run after tools.js is up to date:  python3 build-category-page.py
# ============================================

import os
import re
import json

HERE = os.path.dirname(os.path.abspath(__file__))
CAT_DIR = os.path.join(HERE, "categories")
SITE = "https://www.123miniapps.online"
VER = "2.8.9"

# id, name, icon, one-line desc, URL slug, and an intro sentence for the hub.
CATEGORIES = [
    ("text", "Text Tools", "\U0001F4DD",
     "Clean, count, compare and transform text without leaving the tab.",
     "text-tools",
     "Free online text tools to count, clean, convert and compare text. Everything runs in your browser, so nothing you paste is ever uploaded."),
    ("image", "Image Tools", "\U0001F5BC️",
     "Resize, compress, crop and convert images entirely on your device.",
     "image-tools",
     "Free image tools that resize, compress, crop and convert pictures entirely on your device. Your images are never uploaded to a server."),
    ("developer", "Developer Tools", "\U0001F4BB",
     "Format, validate and debug the payloads you work with every day.",
     "developer-tools",
     "Free developer tools to format, validate, encode and debug the data you work with. They run in your browser, so code and tokens stay private."),
    ("converter", "Converters", "\U0001F504",
     "Switch between units, formats and encodings in a single click.",
     "converters",
     "Free online converters for units, formats, encodings and more. Convert in a single click, with every calculation done locally in your browser."),
    ("generator", "Generators", "⚙️",
     "Produce passwords, QR codes, UUIDs and placeholder data instantly.",
     "generators",
     "Free generators for passwords, QR codes, UUIDs, hashes and placeholder data. Each one runs in your browser with no sign-up and nothing uploaded."),
    ("calculator", "Calculators", "\U0001F9EE",
     "Run the numbers on loans, tips, BMI, percentages and more.",
     "calculators",
     "Free online calculators for loans, tips, percentages, dates, BMI and more. Every calculation happens in your browser, instantly and privately."),
    ("security", "Security Tools", "\U0001F512",
     "Hash, encode and audit, nothing is transmitted anywhere.",
     "security-tools",
     "Free security tools to hash, encrypt, encode and audit. Built on your browser's own Web Crypto, so nothing you enter is ever transmitted."),
    ("design", "Design Tools", "\U0001F3A8",
     "Colors, gradients, shadows and type scales for your next build.",
     "design-tools",
     "Free design tools for colors, gradients, shadows, contrast and type. Preview and copy the CSS instantly, all in your browser."),
    ("content", "Content Tools", "\U0001F4DA",
     "Draft, check and polish copy for the web.",
     "content-tools",
     "Free content tools to draft, check and polish copy for the web, from readability and keyword density to meta tags and slugs. Runs in your browser."),
    ("productivity", "Productivity Tools", "\U0001F3AF",
     "Timers, notes and trackers that stay out of your way.",
     "productivity-tools",
     "Free productivity tools: timers, notes, to-do lists and trackers that stay out of your way. They run in your browser and keep data on your device."),
    ("fun", "Fun Tools", "\U0001F389",
     "Dice, wheels, coin flips and other pleasant distractions.",
     "fun-tools",
     "Free fun tools: dice, wheels, coin flips, random pickers and other pleasant distractions. Instant, free and running entirely in your browser."),
    ("premium", "Premium Applications", "\U0001F48E",
     "Professional-grade business apps with full reports and one-click PDF export.",
     "premium-applications",
     "Premium browser apps for founders and operators: full professional reports with formulas, charts, benchmarks and one-click PDF export. Everything runs in your browser, nothing uploaded."),
]


def slugify(name):
    """Mirror of slugify() in assets/data/tools.js."""
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"^-+|-+$", "", s)
    return s


def load_tools():
    """Parse tool objects (name, category, description, icon, usageCount) from tools.js."""
    src = open(os.path.join(HERE, "assets/data/tools.js"), encoding="utf-8").read()
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
        icon = field("icon")
        deleted = re.search(r"deleted:\s*true", block)
        um = re.search(r"usageCount:\s*(\d+)", block)
        usage = int(um.group(1)) if um else 0
        if name and category and not deleted:
            tools.append({"name": name, "category": category, "description": desc,
                          "icon": icon, "usage": usage, "slug": slugify(name)})
    return tools


HEAD = """<!DOCTYPE html>
<html lang="en" data-theme="indigo-nova">
<head>
  <!-- Google AdSense -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8835778560634384" crossorigin="anonymous"></script>
  <!-- Google tag (gtag.js) - Google Analytics 4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-9XBYMBW8WV"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9XBYMBW8WV');</script>
<!-- ============================================
     123MiniApps.online v2.0
     File: categories/{slug}.html
     Generated by build-category-page.py, do not edit directly.
     ============================================ -->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">

<title>{title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="author" content="123MiniApps">
<link rel="canonical" href="{canonical}">

<meta property="og:type" content="website">
<meta property="og:site_name" content="123MiniApps">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{site}/assets/images/social/og-image.png">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{site}/assets/images/social/og-image.png">

<meta name="theme-color" content="#0B1120">
<link rel="icon" href="../assets/images/logo.svg" type="image/svg+xml">
<link rel="manifest" href="../manifest.json">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap"></noscript>

<style>
html{{background:#0B1120}}
body{{margin:0;background:#0B1120;color:#fff;font-family:Inter,-apple-system,sans-serif}}
</style>
<link rel="stylesheet" href="../assets/css/main.min.css?v={ver}">

<script type="application/ld+json">
{schema}
</script>
</head>

<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="progress-bar" id="progress-bar" aria-hidden="true"></div>

<header class="nav" id="nav">
  <div class="container nav__inner">
    <a class="nav__logo" href="../index.html" aria-label="123MiniApps home">
      <span class="nav__logo-mark" aria-hidden="true">123</span>
      <span>Mini<span class="gradient-text">Apps</span></span>
    </a>
    <nav class="nav__links" aria-label="Primary">
      <a class="nav__link" href="../index.html">Home</a>
      <a class="nav__link" href="../index.html#all-tools-section">All Tools</a>
      <a class="nav__link" href="../index.html#categories">Categories</a>
      <a class="nav__link" href="../blog/index.html">Blog</a>
      <a class="nav__link" href="../pages/about.html">About</a>
    </nav>
    <div class="nav__actions">
      <button class="btn btn--icon btn--sm" data-open-search type="button" aria-label="Search tools">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
      </button>
      <button class="nav__toggle" id="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="nav-drawer">
        <span class="nav__toggle-bars" aria-hidden="true"></span>
      </button>
    </div>
  </div>
  <nav class="nav__drawer" id="nav-drawer" aria-label="Mobile">
    <a class="nav__link" href="../index.html">Home</a>
    <a class="nav__link" href="../index.html#all-tools-section">All Tools</a>
    <a class="nav__link" href="../index.html#categories">Categories</a>
    <a class="nav__link" href="../blog/index.html">Blog</a>
    <a class="nav__link" href="../pages/about.html">About</a>
  </nav>
</header>
"""

TAIL = """<footer class="footer">
  <div class="container">
    <div class="footer__bottom">
      <p>&copy; <span id="copyright-year">2026</span> 123MiniApps.online</p>
      <p>
        <a class="footer__link" href="../pages/privacy.html">Privacy</a> &middot;
        <a class="footer__link" href="../pages/terms.html">Terms</a> &middot;
        <a class="footer__link" href="../pages/disclaimer.html">Disclaimer</a> &middot;
        <a class="footer__link" href="../pages/cookies.html">Cookies</a> &middot;
        <a class="footer__link" href="../pages/dmca.html">DMCA</a> &middot;
        <a class="footer__link" href="../index.html">All tools</a>
      </p>
    </div>
  </div>
</footer>

<button class="theme-fab" id="theme-fab" type="button" aria-label="Change color theme" aria-expanded="false" aria-controls="theme-panel">
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="13.5" cy="6.5" r=".5" fill="currentColor"/><circle cx="17.5" cy="10.5" r=".5" fill="currentColor"/><circle cx="8.5" cy="7.5" r=".5" fill="currentColor"/><circle cx="6.5" cy="12.5" r=".5" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2Z"/></svg>
</button>

<div class="theme-panel" id="theme-panel" role="radiogroup" aria-label="Color themes" inert>
  <p class="theme-panel__title">Pick a theme</p>
  <p class="theme-panel__sub">Ten hand-tuned palettes.</p>
  <div class="theme-panel__grid"></div>
</div>

<button class="back-to-top" id="back-to-top" type="button" aria-label="Back to top">
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 15 6-6 6 6"/></svg>
</button>

<div class="modal" id="search-modal" role="dialog" aria-modal="true" aria-labelledby="search-modal-label" aria-hidden="true">
  <div class="modal__panel">
    <h2 class="sr-only" id="search-modal-label">Search all tools</h2>
    <div class="modal__header">
      <span class="searchbar__icon" aria-hidden="true"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg></span>
      <label class="sr-only" for="search-modal-input">Search tools</label>
      <input class="modal__input" id="search-modal-input" type="search" placeholder="Search tools..." autocomplete="off">
      <button class="btn btn--icon btn--sm" data-close-search type="button" aria-label="Close search">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>
      </button>
    </div>
    <div class="modal__body">
      <div class="search-results" id="search-results"></div>
      <p class="sr-only" id="search-status" role="status" aria-live="polite"></p>
    </div>
  </div>
</div>

<script src="../assets/js/config.js?v={ver}"></script>
<script src="../assets/js/theme-manager.js?v={ver}"></script>
<script src="../assets/data/categories.js?v={ver}" defer></script>
<script src="../assets/data/tools.js?v={ver}" defer></script>
<script src="../assets/data/testimonials.js?v={ver}" defer></script>
<script src="../assets/js/components.js?v={ver}" defer></script>
<script src="../assets/js/tool-utils.js?v={ver}" defer></script>
<script src="../assets/js/search-engine.js?v={ver}" defer></script>
<script src="../assets/js/animations.js?v={ver}" defer></script>
<script src="../assets/js/pwa.js?v={ver}" defer></script>
<script src="../assets/js/analytics.js?v={ver}" defer></script>
<script src="../assets/js/consent.js?v={ver}" defer></script>
<script src="../assets/js/ads.js?v={ver}" defer></script>
<script src="../assets/js/main.js?v={ver}" defer></script>
<script defer>document.addEventListener('DOMContentLoaded',()=>{{document.getElementById('copyright-year').textContent=new Date().getFullYear();}});</script>
</body>
</html>
"""


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def build_page(cat, tools_in_cat, all_cats):
    cid, name, icon, desc, slug, intro = cat
    canonical = f"{SITE}/categories/{slug}.html"
    n = len(tools_in_cat)
    title = f"{name}: {n} Free Online Tools | 123MiniApps"
    meta_desc = intro

    schema = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                    {"@type": "ListItem", "position": 2, "name": name, "item": canonical},
                ],
            },
            {
                "@type": "CollectionPage",
                "@id": canonical + "#collection",
                "name": f"{name} - 123MiniApps",
                "description": meta_desc,
                "url": canonical,
                "isPartOf": {"@type": "WebSite", "name": "123MiniApps", "url": SITE + "/"},
                "mainEntity": {
                    "@type": "ItemList",
                    "numberOfItems": n,
                    "itemListElement": [
                        {"@type": "ListItem", "position": i + 1,
                         "url": f"{SITE}/tools/{t['slug']}.html", "name": t["name"]}
                        for i, t in enumerate(tools_in_cat)
                    ],
                },
            },
        ],
    }, indent=2, ensure_ascii=False)

    cards = "\n".join(
        f'        <a class="tool-card" href="../tools/{t["slug"]}.html">\n'
        f'          <span class="tool-card__icon" aria-hidden="true">{t["icon"]}</span>\n'
        f'          <h3 class="tool-card__title">{esc(t["name"])}</h3>\n'
        f'          <p class="tool-card__desc">{esc(t["description"])}</p>\n'
        f'          <span class="tool-card__link"><span>Open tool</span></span>\n'
        f'        </a>'
        for t in tools_in_cat
    )

    others = "\n".join(
        f'        <a class="btn btn--ghost btn--sm" href="{c[4]}.html">{c[2]} {esc(c[1])}</a>'
        for c in all_cats if c[0] != cid
    )

    head = HEAD.format(slug=slug, title=esc(title), description=esc(meta_desc),
                       canonical=canonical, site=SITE, ver=VER, schema=schema)

    body = f"""
<main class="tool-page" id="main">
  <div class="container">

    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../index.html">Home</a>
      <span aria-hidden="true">/</span>
      <span aria-current="page">{esc(name)}</span>
    </nav>

    <div class="section__header">
      <span class="eyebrow">{icon} Category</span>
      <h1>{esc(name)}</h1>
      <p>{esc(intro)}</p>
    </div>

    <div class="grid-auto grid-auto--lg">
{cards}
    </div>

    <section class="section">
      <h2 class="text-2xl mb-4">Browse other categories</h2>
      <div class="actions" style="flex-wrap:wrap;gap:var(--space-2)">
{others}
      </div>
    </section>

    <p class="mt-8"><a href="../index.html">&larr; Back to all 116 tools</a> &middot; <a href="../blog/index.html">Read the guides</a></p>

  </div>
</main>

"""
    return head + body + TAIL.format(ver=VER)


def main():
    os.makedirs(CAT_DIR, exist_ok=True)
    tools = load_tools()
    for cat in CATEGORIES:
        cid = cat[0]
        in_cat = sorted([t for t in tools if t["category"] == cid],
                        key=lambda t: (-t["usage"], t["name"]))
        if not in_cat:
            print("WARN: no tools for category", cid)
            continue
        html = build_page(cat, in_cat, CATEGORIES)
        path = os.path.join(CAT_DIR, cat[4] + ".html")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        print(f"wrote categories/{cat[4]}.html ({len(in_cat)} tools)")


if __name__ == "__main__":
    main()
