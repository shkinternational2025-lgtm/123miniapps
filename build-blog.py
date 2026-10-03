#!/usr/bin/env python3
# ============================================
# 123MiniApps.online v2.0
# File: build-blog.py
# Purpose: Generate the blog index and article pages
#          from blog_posts.py.
#
# WHY A BLOG EXISTS ON A TOOL SITE
# --------------------------------
# Tool pages compete for head terms ("password
# generator") that established sites already own.
# Articles compete for long-tail questions ("why does
# my 1TB drive show 931GB") that nobody has properly
# answered, far lower difficulty, and the reader who
# arrives is already one click from the tool that
# solves their problem.
#
# It also addresses the AdSense thin-content problem:
# a reviewer sees substantial editorial writing rather
# than 95 near-identical utility pages.
#
# Usage: python3 build-blog.py
# ============================================

import os
import re
import json
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(HERE, "blog")
SITE = "https://www.123miniapps.online"

# Freshness signal: articles were reviewed/updated on this date. Bump when the
# content is meaningfully revised so Google/answer-engines see recent maintenance.
LAST_REVIEWED = "2026-09-01"

NAV = """  <div class="container nav__inner">
    <a class="nav__logo" href="{root}index.html" aria-label="123MiniApps home">
      <span class="nav__logo-mark" aria-hidden="true">123</span>
      <span>Mini<span class="gradient-text">Apps</span></span>
    </a>
    <nav class="nav__links" aria-label="Primary">
      <a class="nav__link" href="{root}index.html">Home</a>
      <a class="nav__link" href="{root}index.html#all-tools-section">All Tools</a>
      <a class="nav__link" href="{root}blog/index.html">Blog</a>
      <a class="nav__link" href="{root}pages/about.html">About</a>
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
    <a class="nav__link" href="{root}index.html">Home</a>
    <a class="nav__link" href="{root}index.html#all-tools-section">All Tools</a>
    <a class="nav__link" href="{root}blog/index.html">Blog</a>
    <a class="nav__link" href="{root}pages/about.html">About</a>
  </nav>"""

CHROME_TAIL = """<footer class="footer">
  <div class="container">
    <div class="footer__bottom">
      <p>© <span id="copyright-year">2026</span> 123MiniApps.online</p>
      <p>
        <a class="footer__link" href="{root}pages/privacy.html">Privacy</a> ·
        <a class="footer__link" href="{root}pages/terms.html">Terms</a> ·
        <a class="footer__link" href="{root}pages/disclaimer.html">Disclaimer</a> ·
        <a class="footer__link" href="{root}pages/cookies.html">Cookies</a> ·
        <a class="footer__link" href="{root}pages/dmca.html">DMCA</a> ·
        <a class="footer__link" href="{root}index.html">All tools</a>
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
      <input class="modal__input" id="search-modal-input" type="search" placeholder="Search tools…" autocomplete="off">
      <button class="btn btn--icon btn--sm" data-close-search type="button" aria-label="Close search">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>
      </button>
    </div>
    <div class="modal__body">
      <div class="search-results" id="search-results"></div>
      <p class="sr-only" id="search-status" role="status" aria-live="polite"></p>
    </div>
    <div class="modal__footer">
      <span class="modal__hint"><kbd>↑</kbd><kbd>↓</kbd> navigate</span>
      <span class="modal__hint"><kbd>↵</kbd> open</span>
      <span class="modal__hint"><kbd>Esc</kbd> close</span>
    </div>
  </div>
</div>

<script src="{root}assets/js/config.js?v=2.9.0"></script>
<script src="{root}assets/js/theme-manager.js?v=2.9.0"></script>
<script src="{root}assets/data/categories.js?v=2.9.0" defer></script>
<script src="{root}assets/data/tools.js?v=2.9.0" defer></script>
<script src="{root}assets/data/testimonials.js?v=2.9.0" defer></script>
<script src="{root}assets/js/components.js?v=2.9.0" defer></script>
<script src="{root}assets/js/tool-utils.js?v=2.9.0" defer></script>
<script src="{root}assets/js/search-engine.js?v=2.9.0" defer></script>
<script src="{root}assets/js/animations.js?v=2.9.0" defer></script>
<script src="{root}assets/js/pwa.js?v=2.9.0" defer></script>
<script src="{root}assets/js/analytics.js?v=2.9.0" defer></script>
<script src="{root}assets/js/consent.js?v=2.9.0" defer></script>
<script src="{root}assets/js/ads.js?v=2.9.0" defer></script>
<script src="{root}assets/js/main.js?v=2.9.0" defer></script>
<script defer>document.addEventListener('DOMContentLoaded',()=>{{document.getElementById('copyright-year').textContent=new Date().getFullYear();}});</script>
</body>
</html>
"""

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
     File: {file}
     Generated by build-blog.py, do not edit directly.
     ============================================ -->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">

<title>{title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="author" content="123MiniApps">
<link rel="canonical" href="{canonical}">

<meta property="og:type" content="{og_type}">
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
{extra_meta}
<meta name="theme-color" content="#0B1120">
<link rel="icon" href="{root}assets/images/logo.svg" type="image/svg+xml">
<link rel="manifest" href="{root}manifest.json">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap"></noscript>

<style>
html{{background:#0B1120}}
body{{margin:0;background:#0B1120;color:#fff;font-family:Inter,-apple-system,sans-serif}}
</style>
<link rel="stylesheet" href="{root}assets/css/main.min.css?v=2.9.0">

<script type="application/ld+json">
{schema}
</script>
</head>

<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="progress-bar" id="progress-bar" aria-hidden="true"></div>

<header class="nav" id="nav">
{nav}
</header>
"""


def render_body(markdownish):
    """
    Turn the lightweight article format into HTML.

    Deliberately minimal, the articles are authored as structured
    Python, so this only needs to handle headings, paragraphs, lists,
    blockquotes and callouts.
    """
    html = []
    for block in markdownish:
        kind = block[0]
        if kind == "h2":
            html.append(f'      <h2 id="{slugify(block[1])}">{block[1]}</h2>')
        elif kind == "h3":
            html.append(f"      <h3>{block[1]}</h3>")
        elif kind == "p":
            html.append(f"      <p>{block[1]}</p>")
        elif kind == "ul":
            items = "\n".join(f"        <li>{i}</li>" for i in block[1])
            html.append(f"      <ul>\n{items}\n      </ul>")
        elif kind == "ol":
            items = "\n".join(f"        <li>{i}</li>" for i in block[1])
            html.append(f"      <ol>\n{items}\n      </ol>")
        elif kind == "quote":
            html.append(
                f'      <blockquote style="border-left:3px solid var(--accent-primary);'
                f'padding-left:var(--space-5);margin:var(--space-6) 0;color:var(--text-secondary)">'
                f"{block[1]}</blockquote>"
            )
        elif kind == "callout":
            html.append(
                f'      <div class="info-panel" style="margin:var(--space-6) 0">'
                f'<strong class="text-sm">{block[1]}</strong>'
                f'<p class="text-sm text-muted mt-2">{block[2]}</p></div>'
            )
        elif kind == "table":
            headers = "".join(f"<th>{h}</th>" for h in block[1])
            rows = "".join(
                "<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in block[2]
            )
            html.append(
                f'      <div class="table-scroll" style="margin:var(--space-6) 0">'
                f'<table class="data-table"><thead><tr>{headers}</tr></thead>'
                f"<tbody>{rows}</tbody></table></div>"
            )
        elif kind == "tool":
            slug, name, blurb = block[1], block[2], block[3]
            html.append(
                f'      <div class="info-panel" style="margin:var(--space-6) 0;'
                f'border-left:3px solid var(--accent-primary)">'
                f'<strong class="text-sm">Try it: <a href="../tools/{slug}.html">{name}</a></strong>'
                f'<p class="text-sm text-muted mt-2">{blurb}</p></div>'
            )
        elif kind == "img":
            # ("img", src, alt[, caption]) - src is repo-root-relative, e.g.
            # assets/images/blog/<slug>/<slug>-2.webp ; served from /blog/ via ../
            src, alt = block[1], block[2]
            cap = block[3] if len(block) > 3 else ""
            figcap = (
                f'<figcaption class="text-sm text-muted mt-2" style="text-align:center">{cap}</figcaption>'
                if cap else ""
            )
            html.append(
                f'      <figure style="margin:var(--space-6) 0;text-align:center">'
                f'<img src="../{src}" alt="{alt}" width="1280" height="720" loading="lazy" decoding="async" '
                f'style="max-width:100%;height:auto;border-radius:var(--radius-lg)">{figcap}</figure>'
            )
    return "\n\n".join(html)


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", text).lower()).strip("-")


def word_count(blocks):
    text = []
    for b in blocks:
        for part in b[1:]:
            if isinstance(part, str):
                text.append(re.sub(r"<[^>]+>", " ", part))
            elif isinstance(part, (list, tuple)):
                for item in part:
                    if isinstance(item, str):
                        text.append(re.sub(r"<[^>]+>", " ", item))
                    elif isinstance(item, (list, tuple)):
                        text.extend(re.sub(r"<[^>]+>", " ", str(i)) for i in item)
    return len(" ".join(text).split())


def compute_related(posts, n=3):
    """Attach up to n related articles to each post, by keyword overlap.
    Deepens the internal link graph (good for SEO and time-on-site)."""
    for p in posts:
        pk = set(p.get("keywords", []))
        scored = []
        for other in posts:
            if other["slug"] == p["slug"]:
                continue
            overlap = len(pk & set(other.get("keywords", [])))
            scored.append((overlap, other))
        # Highest overlap first; stable fallback keeps output deterministic.
        scored.sort(key=lambda t: (-t[0], t[1]["slug"]))
        p["_related"] = [(o["slug"], o["nav_title"]) for _, o in scored[:n]]


def build_article(post):
    canonical = f"{SITE}/blog/{post['slug']}.html"
    words = word_count(post["body"])
    modified = post.get("modified", LAST_REVIEWED)

    # Hero image (optional): ("assets/images/blog/<slug>/<slug>-1-hero.webp", "alt text").
    # Used as the article's schema/OG image when present; otherwise the site OG image.
    hero = post.get("hero")
    hero_img_url = (SITE + "/" + hero[0]) if hero else (SITE + "/assets/images/social/og-image.png")

    graph = [
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/index.html"},
                {"@type": "ListItem", "position": 3, "name": post["title"], "item": canonical},
            ],
        },
        {
            "@type": "BlogPosting",
            "@id": canonical + "#article",
            "headline": post["headline"],
            "description": post["description"],
            "datePublished": post["published"],
            "dateModified": modified,
            "author": {
                "@type": "Organization",
                "name": "123MiniApps",
                "url": SITE + "/",
                "logo": {"@type": "ImageObject", "url": SITE + "/assets/images/logo.svg"},
            },
            "publisher": {
                "@type": "Organization",
                "name": "123MiniApps",
                "url": SITE + "/",
                "logo": {"@type": "ImageObject", "url": SITE + "/assets/images/logo.svg"},
            },
            "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
            "image": hero_img_url,
            "wordCount": words,
            "keywords": ", ".join(post["keywords"]),
            "inLanguage": "en",
            "isAccessibleForFree": True,
            "isFamilyFriendly": True,
            # Answer/voice engines: read the H1 and the Quick-answer summary aloud.
            "speakable": {
                "@type": "SpeakableSpecification",
                "cssSelector": ["h1", "#quick-answer"],
            },
        },
    ]

    # FAQ (optional): post["faq"] = [(question, answer_html), ...].
    # Renders both a visible FAQ section and FAQPage structured data.
    faq = post.get("faq", [])
    if faq:
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": re.sub(r"<[^>]+>", "", q).strip(),
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": re.sub(r"<[^>]+>", "", a).strip(),
                    },
                }
                for q, a in faq
            ],
        })

    schema = json.dumps({
        "@context": "https://schema.org",
        "@graph": graph,
    }, indent=2, ensure_ascii=False)

    extra_meta = (
        f'<meta property="article:published_time" content="{post["published"]}">\n'
        f'<meta property="article:modified_time" content="{modified}">\n'
        f'<meta property="article:section" content="{post.get("section", "Guides")}">\n'
        f'<meta property="article:tag" content="{", ".join(post["keywords"])}">'
    )

    head = HEAD.format(
        file=f"blog/{post['slug']}.html",
        title=post["title"],
        description=post["description"],
        canonical=canonical,
        og_type="article",
        site=SITE,
        root="../",
        schema=schema,
        nav=NAV.format(root="../"),
        extra_meta=extra_meta,
    )

    related = "\n".join(
        f'          <li><a href="../tools/{slug}.html">{name}</a></li>'
        for slug, name in post["related_tools"]
    )

    related_articles = post.get("_related", [])
    read_more = ""
    if related_articles:
        cards = "\n".join(
            f'        <a class="tool-card" href="{a_slug}.html">'
            f'<h3 class="tool-card__title">{a_title}</h3>'
            f'<span class="tool-card__link"><span>Read the guide</span></span></a>'
            for a_slug, a_title in related_articles
        )
        read_more = f"""
    <section class="section">
      <h2 class="text-2xl mb-4">Continue reading</h2>
      <div class="grid-auto grid-auto--lg">
{cards}
      </div>
    </section>
"""

    hero_html = ""
    if hero:
        hero_html = (
            f'\n      <figure style="margin:0 0 var(--space-7)">'
            f'<img src="../{hero[0]}" alt="{hero[1]}" width="1280" height="720" '
            f'fetchpriority="high" decoding="async" style="max-width:100%;height:auto;border-radius:var(--radius-lg)">'
            f'</figure>'
        )

    faq_html = ""
    if faq:
        faq_items = "\n".join(
            f'        <div class="info-panel mb-3">'
            f'<strong class="text-sm">{q}</strong>'
            f'<p class="text-sm text-muted mt-2" style="margin-bottom:0">{a}</p></div>'
            for q, a in faq
        )
        faq_html = f"""
    <section class="section" id="faq">
      <h2 class="text-2xl mb-4">Frequently asked questions</h2>
{faq_items}
    </section>
"""

    body = f"""
<main class="tool-page" id="main">
  <div class="container container--narrow">

    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../index.html">Home</a>
      <span aria-hidden="true">/</span>
      <a href="index.html">Blog</a>
      <span aria-hidden="true">/</span>
      <span aria-current="page">{post['nav_title']}</span>
    </nav>

    <article>
      <header class="mb-8">
        <h1>{post['headline']}</h1>
        <div class="info-panel" id="quick-answer" style="margin-top:var(--space-5);border-left:3px solid var(--accent-primary)">
          <strong class="eyebrow" style="color:var(--accent-primary)">Quick answer</strong>
          <p class="lead mt-2" style="margin-bottom:0">{post['standfirst']}</p>
        </div>
        <p class="text-sm text-muted mt-4">
          By 123MiniApps · Published {post['published']} · Updated {modified} ·
          {words} words · about {max(1, round(words / 225))} minute read
        </p>
      </header>
{hero_html}
      <div class="prose">
{render_body(post['body'])}
      </div>
    </article>

    <div class="ad-slot" hidden></div>
{faq_html}
    <section class="section">
      <h2 class="text-2xl mb-4">Tools mentioned in this article</h2>
      <div class="info-panel">
        <ul class="stack-sm">
{related}
        </ul>
      </div>
    </section>
{read_more}
    <p class="mt-8"><a href="index.html">← More articles</a> · <a href="../index.html">Browse all 116 tools</a></p>

  </div>
</main>

"""
    return head + body + CHROME_TAIL.format(root="../")


def build_index(posts):
    canonical = f"{SITE}/blog/index.html"

    schema = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Blog",
                "@id": canonical + "#blog",
                "name": "123MiniApps Blog",
                "description": "Practical explanations of the things our tools do, file sizes, "
                               "password strength, image formats, character encoding and more.",
                "url": canonical,
                "publisher": {"@type": "Organization", "name": "123MiniApps", "url": SITE + "/"},
                "blogPost": [
                    {
                        "@type": "BlogPosting",
                        "headline": p["headline"],
                        "description": p["description"],
                        "datePublished": p["published"],
                        "url": f"{SITE}/blog/{p['slug']}.html",
                    }
                    for p in posts
                ],
            }
        ],
    }, indent=2, ensure_ascii=False)

    head = HEAD.format(
        file="blog/index.html",
        title="Blog: Practical Explanations | 123MiniApps",
        description="Clear answers to the questions behind our tools: why a 1TB drive shows 931GB, "
                    "how long a password should be, which image format to use, and more.",
        canonical=canonical,
        og_type="website",
        site=SITE,
        root="../",
        schema=schema,
        nav=NAV.format(root="../"),
        extra_meta="",
    )

    cards = []
    for p in posts:
        words = word_count(p["body"])
        cards.append(f"""        <article class="tool-card">
          <a class="tool-card__overlay-link" href="{p['slug']}.html" aria-label="Read {p['nav_title']}"></a>
          <div class="tool-card__top">
            <span class="tool-card__icon" aria-hidden="true">{p['icon']}</span>
            <span class="badge badge--muted">{max(1, round(words / 225))} min</span>
          </div>
          <h2 class="tool-card__title">{p['headline']}</h2>
          <p class="tool-card__desc">{p['standfirst']}</p>
          <div class="tool-card__meta">
            <span>{p['published']}</span>
            <span class="tool-card__link"><span>Read</span></span>
          </div>
        </article>""")

    body = f"""
<main class="tool-page" id="main">
  <div class="container">

    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../index.html">Home</a>
      <span aria-hidden="true">/</span>
      <span aria-current="page">Blog</span>
    </nav>

    <div class="section__header">
      <span class="eyebrow">Articles</span>
      <h1>Practical explanations</h1>
      <p>
        The questions behind the tools, answered properly. No filler, no listicles,
        just the explanation you were actually looking for when you searched.
      </p>
    </div>

    <div class="grid-auto grid-auto--lg">
{chr(10).join(cards)}
    </div>

    <p class="mt-12 text-center"><a href="../index.html">Browse all 116 tools →</a></p>

  </div>
</main>

"""
    return head + body + CHROME_TAIL.format(root="../")


# Article modules, collected in order. Add a module name here and its POSTS
# list is included automatically, same pattern as build-tool-page's TOOL_MODULES.
POST_MODULES = [
    "blog_posts",            # original 8 general explainers
    "blog_posts_text",       # one dedicated article per Text tool
    "blog_posts_image",
    "blog_posts_developer",
    "blog_posts_converter",
    "blog_posts_generator",
    "blog_posts_calculator",
    "blog_posts_security",
    "blog_posts_design",
    "blog_posts_content",
    "blog_posts_productivity",
    "blog_posts_fun",
    "blog_posts_extra",
    "blog_posts_batch1",
    "blog_posts_batch2",
    "blog_posts_batch3",
    "blog_posts_batch4",
    "blog_posts_premium",   # premium-app long-form guides
]


def collect_posts():
    import importlib
    posts = []
    seen = set()
    for name in POST_MODULES:
        try:
            mod = importlib.import_module(name)
        except ModuleNotFoundError:
            continue  # batch not written yet
        for p in getattr(mod, "POSTS", []):
            if p["slug"] in seen:
                raise SystemExit(f"duplicate article slug: {p['slug']}")
            seen.add(p["slug"])
            posts.append(p)
    return posts


def apply_upgrades(posts):
    """Merge SEO/AEO upgrades from blog_upgrades.py onto existing posts.

    Lets us enrich published articles (keywords, hero image, in-body images,
    FAQ, refined quick-answer) without rewriting each source module. The URL
    and primary content stay put; we only add. Silent no-op if the file is
    absent.
    """
    try:
        from blog_upgrades import UPGRADES
    except Exception:
        return
    by_slug = {p["slug"]: p for p in posts}
    for slug, up in UPGRADES.items():
        p = by_slug.get(slug)
        if not p:
            continue
        # Only apply an upgrade once its images are physically present. This
        # gates each batch on its images being dropped in: an article is
        # upgraded (hero, FAQ, in-body images, extra sections) the moment its
        # hero WebP exists on disk, and stays untouched until then. Prevents
        # shipping broken image references for a batch whose art is not ready.
        hero = up.get("hero")
        hero_rel = hero[0] if hero else None
        if not hero_rel or not os.path.exists(os.path.join(HERE, hero_rel)):
            continue
        for key in ("keywords", "hero", "faq", "modified", "standfirst"):
            if key in up:
                p[key] = up[key]
        # Extra same-intent sections: list of body tuples, added before FAQ.
        for sec in up.get("append_sections", []):
            p["body"].append(sec)
        # In-body images: insert the first after the paragraph following the
        # first H2, the second after the paragraph following the last H2.
        imgs = up.get("images", [])
        if imgs:
            body = p["body"]
            h2_idx = [i for i, b in enumerate(body) if b[0] == "h2"]

            def after_para(h2_i):
                j = h2_i + 1
                while j < len(body) and body[j][0] != "p":
                    j += 1
                return (j + 1) if j < len(body) else (h2_i + 1)

            # Spread up to 3 in-body images across the article: after the
            # first H2, a middle H2, and the last H2 (deduped, in order).
            points = []
            if h2_idx:
                n = len(imgs)
                picks = [h2_idx[0]]
                if n >= 3 and len(h2_idx) >= 3:
                    picks.append(h2_idx[len(h2_idx) // 2])
                if n >= 2:
                    picks.append(h2_idx[-1])
                seen = set()
                for h in picks:
                    pos = after_para(h)
                    if pos not in seen:
                        points.append(pos)
                        seen.add(pos)
            # Insert positioned images from the bottom up so indices stay valid.
            for img, pos in sorted(zip(imgs, points), key=lambda t: -t[1]):
                body.insert(pos, img)
            # Any images beyond the available anchor points go at the end.
            for img in imgs[len(points):]:
                body.append(img)


if __name__ == "__main__":
    os.makedirs(BLOG_DIR, exist_ok=True)
    posts = collect_posts()
    apply_upgrades(posts)
    compute_related(posts)

    for post in posts:
        path = os.path.join(BLOG_DIR, post["slug"] + ".html")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(build_article(post))
        print(f"  {post['slug']:38} {word_count(post['body']):5} words")

    with open(os.path.join(BLOG_DIR, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(build_index(posts))

    total = sum(word_count(p["body"]) for p in posts)
    print(f"\n  {len(posts)} articles + index, {total:,} words total")
    print(f"  average {total // len(posts):,} words per article")
