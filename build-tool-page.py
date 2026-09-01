#!/usr/bin/env python3
# ============================================
# 123MiniApps.online v2.0
# File: build-tool-page.py
# Purpose: Scaffold a tool page from the shared shell
#          so every page carries identical nav, footer,
#          theme switcher, search modal and script tags.
#
# Usage: python build-tool-page.py
#        (edit PAGES below, then re-run)
#
# This is a build-time dev utility, not something the
# site ships. It exists so that a change to the shared
# chrome can be rolled out to all 95 pages by editing
# one file instead of 95.
# ============================================

import os

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(HERE, "tools")

SHELL = """<!DOCTYPE html>
<html lang="en" data-theme="indigo-nova">
<head>
<!-- ============================================
     123MiniApps.online v2.0
     File: tools/{slug}.html
     Purpose: {purpose}
     ============================================ -->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">

<title>{title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="author" content="123MiniApps">
<link rel="canonical" href="https://www.123miniapps.online/tools/{slug}.html">

<meta property="og:type" content="website">
<meta property="og:site_name" content="123MiniApps">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="https://www.123miniapps.online/tools/{slug}.html">
<meta property="og:image" content="https://www.123miniapps.online/assets/images/social/og-image.png">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="https://www.123miniapps.online/assets/images/social/og-image.png">

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
<link rel="stylesheet" href="../assets/css/main.min.css?v=2.8.2">

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.123miniapps.online/" }},
        {{ "@type": "ListItem", "position": 2, "name": "{category_name}", "item": "https://www.123miniapps.online/#category-{category_id}" }},
        {{ "@type": "ListItem", "position": 3, "name": "{tool_name}", "item": "https://www.123miniapps.online/tools/{slug}.html" }}
      ]
    }},
    {{
      "@type": "SoftwareApplication",
      "name": "{tool_name}",
      "applicationCategory": "{schema_category}",
      "operatingSystem": "Any modern web browser",
      "offers": {{ "@type": "Offer", "price": "0", "priceCurrency": "USD" }},
      "isAccessibleForFree": true,
      "inLanguage": "en",
      "browserRequirements": "Requires JavaScript. Runs entirely in the browser; no data is uploaded.",
      "description": "{description}"
    }}{extra_schema}
  ]
}}
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

<main class="tool-page" id="main">
  <div class="container">

    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../index.html">Home</a>
      <span aria-hidden="true">/</span>
      <a href="../index.html#category-{category_id}">{category_name}</a>
      <span aria-hidden="true">/</span>
      <span aria-current="page">{tool_name}</span>
    </nav>

    <div class="tool-header">
      <div class="tool-header__icon" aria-hidden="true">{icon}</div>
      <div>
        <h1>{tool_name}</h1>
        <p>{tagline}</p>
      </div>
    </div>

{workspace}

{info}

    <section class="section">
      <h2 class="text-2xl mb-4">Related tools</h2>
      <div class="related-strip" id="related"></div>
    </section>
{further_reading}

    <div class="feedback" id="feedback">
      <span class="text-sm">Was this tool useful?</span>
      <button class="feedback__btn" type="button" data-value="good" aria-pressed="false" aria-label="Useful">😍</button>
      <button class="feedback__btn" type="button" data-value="ok" aria-pressed="false" aria-label="Okay">😐</button>
      <button class="feedback__btn" type="button" data-value="bad" aria-pressed="false" aria-label="Not useful">😞</button>
    </div>

  </div>
</main>

<footer class="footer">
  <div class="container">
    <div class="footer__bottom">
      <p>© <span id="copyright-year">2026</span> 123MiniApps.online</p>
      <p>
        <a class="footer__link" href="../pages/about.html">About</a> ·
        <a class="footer__link" href="../pages/contact.html">Contact</a> ·
        <a class="footer__link" href="../pages/privacy.html">Privacy</a> ·
        <a class="footer__link" href="../pages/terms.html">Terms</a> ·
        <a class="footer__link" href="../pages/disclaimer.html">Disclaimer</a> ·
        <a class="footer__link" href="../pages/cookies.html">Cookies</a> ·
        <a class="footer__link" href="../pages/dmca.html">DMCA</a>
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

<script src="../assets/js/config.js?v=2.8.2"></script>
<script src="../assets/js/theme-manager.js?v=2.8.2"></script>
<script src="../assets/data/categories.js?v=2.8.2" defer></script>
<script src="../assets/data/tools.js?v=2.8.2" defer></script>
<script src="../assets/data/testimonials.js?v=2.8.2" defer></script>
<script src="../assets/js/components.js?v=2.8.2" defer></script>
<script src="../assets/js/tool-utils.js?v=2.8.2" defer></script>
<script src="../assets/js/search-engine.js?v=2.8.2" defer></script>
<script src="../assets/js/animations.js?v=2.8.2" defer></script>
<script src="../assets/js/pwa.js?v=2.8.2" defer></script>
<script src="../assets/js/analytics.js?v=2.8.2" defer></script>
<script src="../assets/js/consent.js?v=2.8.2" defer></script>
<script src="../assets/js/ads.js?v=2.8.2" defer></script>
<script src="../assets/js/main.js?v=2.8.2" defer></script>
{extra_scripts}
<!-- ============================================
     TOOL LOGIC
     ============================================ -->
<script defer>
document.addEventListener('DOMContentLoaded', () => {{
  document.getElementById('copyright-year').textContent = new Date().getFullYear();
  const $ = (id) => document.getElementById(id);

{script}

  /* ---- Related tools ---- */
  const related = document.getElementById('related');
  const thisTool = window.getToolBySlug('{slug}');
  if (related && thisTool) {{
    window.getRelatedTools(thisTool, 4).forEach((tool) => {{
      related.append(createToolCard({{ tool, base: '../' }}));
    }});
  }}
}});
</script>
</body>
</html>
"""


DEFAULTS = {"extra_scripts": "", "extra_schema": "", "further_reading": ""}

# Tool slug -> the blog article that explains the concept behind it.
# This is the second half of the internal link graph: the blog already
# links out to tools; here each tool links back to the article a curious
# reader would want. Internal links spread whatever ranking authority the
# site earns across all its pages and keep visitors on-site longer.
FURTHER_READING = {
    "word-counter": ("how-many-words-is-that-word-count-guide", "How Many Words Is That? A Practical Guide to Word Count"),
    "case-converter": ("convert-text-case-without-retyping", "Uppercase, lowercase, Title Case: Convert Text Case Without Retyping"),
    "text-diff-checker": ("compare-two-texts-find-differences", "How to Compare Two Texts and Spot Every Difference"),
    "lorem-ipsum-generator": ("what-is-lorem-ipsum-placeholder-text", "What Is Lorem Ipsum and Why Designers Still Use Placeholder Text"),
    "text-reverser": ("how-to-reverse-text-words-lines", "How to Reverse Text, Words, or Lines (and Why You'd Want To)"),
    "remove-duplicate-lines": ("remove-duplicate-lines-from-a-list", "How to Remove Duplicate Lines from a List Instantly"),
    "find-and-replace": ("find-and-replace-online-bulk-edit-text", "Find and Replace Online: Bulk-Edit Text Without Opening an Editor"),
    "text-to-speech": ("text-to-speech-in-your-browser", "Turn Text into Natural Speech in Your Browser, Free"),
    "character-counter": ("character-count-tweets-meta-sms", "Character Count for Tweets, Meta Descriptions & SMS: Why Limits Matter"),
    "text-formatter": ("clean-up-messy-text-formatting", "Clean Up Messy Text: Fix Spacing, Line Breaks and Formatting Fast"),
    "image-compressor": ("webp-vs-jpeg-vs-png", "WebP, JPEG or PNG: which should you actually use?"),
    "image-resizer": ("resize-image-to-exact-dimensions", "How to Resize an Image to Exact Dimensions Without Stretching It"),
    "image-to-base64": ("what-is-a-base64-image-data-uri", "What Is a Base64 Image and When Should You Inline One?"),
    "image-cropper": ("crop-image-to-right-aspect-ratio", "How to Crop an Image to the Right Aspect Ratio"),
    "image-format-converter": ("convert-between-image-formats-png-jpg-webp", "PNG, JPG, WebP: How to Convert Between Image Formats"),
    "color-picker-from-image": ("get-hex-color-from-any-image", "How to Get the Exact Hex Color from Any Image"),
    "image-filters": ("apply-photo-filters-in-your-browser", "Apply Filters to Photos in Your Browser: Brightness, Contrast, Blur and More"),
    "favicon-generator": ("make-a-favicon-for-every-browser", "How to Make a Favicon That Looks Right in Every Browser Tab"),
    "meme-generator": ("how-to-make-a-meme", "How to Make a Meme: Top and Bottom Text Done Right"),
    "image-watermark": ("watermark-images-to-protect-your-work", "How to Watermark Images to Protect Your Work"),
    "json-formatter": ("why-is-my-json-invalid", "Why is my JSON invalid when it looks perfectly fine?"),
    "regex-tester": ("how-to-test-regular-expressions", "How to Test Regular Expressions Without Breaking Them"),
    "base64-encoder-decoder": ("base64-encoding-explained-for-developers", "Base64 Encoding Explained: What It Is and When to Use It"),
    "url-encoder-decoder": ("url-encoding-percent-encoding-explained", "URL Encoding Explained: Why Spaces Become %20"),
    "jwt-decoder": ("how-to-decode-a-jwt-safely", "How to Decode a JWT (and Why You Should Never Paste One Online)"),
    "html-formatter": ("why-format-your-html", "Why You Should Format Your HTML (and What a Formatter Actually Does)"),
    "css-minifier": ("css-minification-explained", "CSS Minification: How Removing Whitespace Speeds Up Your Site"),
    "javascript-minifier": ("javascript-minification-and-performance", "JavaScript Minification: Smaller Bundles, Faster Load Times"),
    "sql-formatter": ("why-format-your-sql", "Why Formatting Your SQL Makes Queries Easier to Read and Debug"),
    "markdown-preview": ("markdown-explained-for-beginners", "Markdown Explained: Write Formatted Text Without a Word Processor"),
    "cron-expression-builder": ("cron-day-of-week-trap", "The cron mistake that runs your job far more often than you intended"),
    "http-status-codes": ("http-status-codes-explained", "HTTP Status Codes Explained: What 404, 301 and 500 Really Mean"),
    "unit-converter": ("metric-to-imperial-unit-conversion-explained", "Metric to Imperial: How Unit Conversion Actually Works"),
    "temperature-converter": ("celsius-fahrenheit-kelvin-temperature-conversion", "Celsius, Fahrenheit and Kelvin: How to Convert Temperature"),
    "csv-to-json": ("how-to-convert-csv-to-json", "How to Convert CSV to JSON (and Why the Structure Changes)"),
    "timestamp-converter": ("unix-timestamps-epoch-time-explained", "Unix Timestamps Explained: Converting Epoch Time to a Date"),
    "number-base-converter": ("binary-decimal-hex-number-bases-explained", "Binary, Decimal, Hex: How to Convert Between Number Bases"),
    "roman-numeral-converter": ("how-roman-numerals-work", "How Roman Numerals Work and How to Convert Them"),
    "currency-converter": ("how-currency-conversion-works", "How Currency Conversion Works (and Why Rates Keep Moving)"),
    "time-zone-converter": ("time-zones-explained-converting-times", "Time Zones Explained: Converting Times Across the World"),
    "file-size-converter": ("why-1tb-drive-shows-931gb", "Why does my 1TB hard drive only show 931GB?"),
    "text-to-ascii": ("what-is-ascii-text-to-character-codes", "What Is ASCII? Converting Text to Character Codes"),
    "password-generator": ("how-long-should-a-password-be", "How long should a password actually be?"),
    "qr-code-generator": ("how-qr-codes-work-and-how-to-make-one", "How QR Codes Work and How to Make One"),
    "uuid-generator": ("what-is-a-uuid-and-when-you-need-one", "What Is a UUID and When Do You Need One?"),
    "random-number-generator": ("how-to-generate-truly-random-numbers", "How to Generate Truly Random Numbers (and Why Math.random Isn't Enough)"),
    "hash-generator": ("what-is-a-hash-md5-sha256-explained", "What Is a Hash? MD5, SHA-256 and How Hashing Works"),
    "slug-generator": ("what-is-a-url-slug-seo-friendly", "What Is a URL Slug and How to Create SEO-Friendly Ones"),
    "barcode-generator": ("barcodes-explained-how-to-generate-one", "Barcodes Explained: How to Generate One That Scans"),
    "placeholder-image-generator": ("placeholder-images-why-and-how", "Placeholder Images: Why Designers Use Them and How to Generate One"),
    "fake-data-generator": ("why-you-need-fake-data-for-testing", "Why You Need Fake Data for Testing (and How to Generate It)"),
    "signature-generator": ("create-a-digital-signature-online", "How to Create a Signature for Documents Online"),
    "invoice-generator": ("how-to-make-a-professional-invoice", "How to Make a Professional Invoice (Free, No Software)"),
    "gradient-generator": ("css-gradients-explained", "CSS Gradients Explained: How to Create Beautiful Backgrounds"),
    "percentage-calculator": ("how-to-calculate-percentages", "How to Calculate Percentages: Increase, Decrease and \"Of\""),
    "loan-calculator": ("how-loan-repayments-work-amortization", "How Loan Repayments Work: Understanding Amortization"),
    "bmi-calculator": ("what-bmi-measures-and-what-it-doesnt", "What BMI Actually Measures (and What It Doesn't)"),
    "tip-calculator": ("how-much-to-tip-and-split-the-bill", "How Much to Tip: A Practical Guide to Splitting the Bill"),
    "age-calculator": ("how-to-calculate-exact-age", "How to Calculate Exact Age in Years, Months and Days"),
    "date-difference-calculator": ("how-to-calculate-days-between-dates", "How to Calculate the Number of Days Between Two Dates"),
    "scientific-calculator": ("scientific-calculator-functions-explained", "Scientific Calculator Functions Explained"),
    "discount-calculator": ("why-stacked-discounts-never-add-up", "Why 20% off plus another 20% off is not 40% off"),
    "compound-interest-calculator": ("compound-interest-explained", "Compound Interest Explained: Why It's So Powerful Over Time"),
    "fuel-cost-calculator": ("how-to-calculate-fuel-cost-of-a-trip", "How to Calculate the Fuel Cost of a Trip"),
    "password-strength-checker": ("how-password-strength-is-measured", "How Password Strength Is Actually Measured"),
    "encryption-tool": ("how-encryption-works-keeping-text-private", "How Encryption Works: Keeping Text Truly Private"),
    "hash-comparison": ("what-a-checksum-actually-proves", "What does a matching checksum actually prove?"),
    "random-key-generator": ("what-makes-a-strong-key-or-secret", "Generating Secure Keys and Secrets: What Makes a Key Strong"),
    "privacy-checker": ("what-a-website-knows-about-you", "How to Check What a Website Can Learn About You"),
    "color-picker": ("understanding-color-hex-rgb-hsl", "Understanding Color on the Web: Hex, RGB and HSL"),
    "color-palette-generator": ("how-to-build-a-color-palette", "How to Build a Color Palette That Actually Works"),
    "contrast-checker": ("color-contrast-and-accessibility", "Color Contrast and Accessibility: Meeting WCAG"),
    "box-shadow-generator": ("css-box-shadow-explained", "CSS Box Shadow Explained: Adding Depth and Elevation"),
    "border-radius-generator": ("css-border-radius-rounded-corners", "CSS Border Radius: Rounded Corners Done Right"),
    "font-pairing-tool": ("how-to-pair-fonts-that-work", "How to Pair Fonts That Work Together"),
    "css-grid-generator": ("css-grid-explained-visual-layouts", "CSS Grid Explained: Building Layouts the Modern Way"),
    "glassmorphism-generator": ("glassmorphism-frosted-glass-effect", "Glassmorphism: The Frosted-Glass UI Effect Explained"),
    "readability-checker": ("how-to-make-writing-easier-to-read", "How to Make Your Writing Easier to Read (Readability Scores Explained)"),
    "meta-tag-generator": ("meta-tags-explained-title-description-open-graph", "Meta Tags Explained: Title, Description and Open Graph"),
    "keyword-density-checker": ("keyword-density-and-why-stuffing-backfires", "Keyword Density: What It Is and Why Stuffing Backfires"),
    "citation-generator": ("how-to-cite-sources-apa-mla-chicago", "How to Cite Sources: APA, MLA and Chicago Explained"),
    "blog-title-generator": ("how-to-write-blog-titles-that-get-clicks", "How to Write Blog Titles That Get Clicks"),
    "text-summarizer": ("how-text-summarizers-work", "How Text Summarizers Work and When to Use One"),
    "pomodoro-timer": ("the-pomodoro-technique-explained", "The Pomodoro Technique: Why Working in 25-Minute Sprints Works"),
    "todo-list": ("why-writing-a-to-do-list-works", "Why Writing a To-Do List Works (and How to Write a Better One)"),
    "notepad": ("digital-notepad-quick-notes-in-browser", "The Case for a Quick Digital Notepad in Your Browser"),
    "countdown-timer": ("how-to-use-a-countdown-timer", "How a Countdown Timer Sharpens Focus and Beats Procrastination"),
    "habit-tracker": ("how-habit-tracking-builds-consistency", "How Habit Tracking Builds Consistency (and Why the Streak Works)"),
    "meeting-cost-calculator": ("the-real-cost-of-meetings", "The Real Cost of Meetings (and How to Calculate It)"),
    "random-picker": ("how-to-pick-a-random-winner-fairly", "How to Pick a Random Winner Fairly (Raffles, Giveaways and Names)"),
    "dice-roller": ("dice-notation-explained", "What does 4d6kh3 mean? Dice notation explained"),
    "coin-flip": ("is-a-coin-flip-really-fair", "Is a Coin Flip Really 50/50? The Surprising Truth"),
    "spin-the-wheel": ("spin-the-wheel-for-fair-random-choices", "Spin the Wheel: Making Random Choices Fun and Fair"),
    "password-game": ("why-password-rules-are-so-frustrating", "Why Password Rules Are So Frustrating (and What Good Ones Look Like)"),
    "emoji-picker": ("how-emoji-work-and-how-to-use-them", "How Emoji Actually Work (and How to Use Them Well)"),
}


def further_reading_html(slug):
    """Build the 'Further reading' block for a tool, or '' if none maps."""
    entry = FURTHER_READING.get(slug)
    if not entry:
        return ""
    art_slug, art_title = entry
    return (
        '\n    <section class="section" aria-labelledby="further-reading-h">'
        '\n      <h2 class="text-2xl mb-4" id="further-reading-h">Further reading</h2>'
        '\n      <div class="info-panel" style="border-left:3px solid var(--accent-primary)">'
        '\n        <strong class="text-sm">\U0001F4D6 <a href="../blog/' + art_slug + '.html">' + art_title + '</a></strong>'
        '\n        <p class="text-sm text-muted mt-2">Read the full guide on the 123MiniApps blog.</p>'
        '\n      </div>'
        '\n    </section>'
    )


def enrich(page):
    """
    The five originally hand-built tools carry their info markup as raw
    HTML rather than going through toolkit.info(), so they have no
    structured data to generate schema from. Where such a page supplies
    `faqs` and `howto` keys, build the visible FAQ section and matching
    FAQPage / HowTo schema the same way toolkit.tool() does.
    """
    if page.get("extra_schema") or "faqs" not in page:
        return page

    import json
    from toolkit import faq_section

    url = f"https://www.123miniapps.online/tools/{page['slug']}.html"
    faqs = page["faqs"]

    entries = [{
        "@type": "FAQPage",
        "@id": url + "#faq",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }]

    if page.get("howto"):
        entries.append({
            "@type": "HowTo",
            "@id": url + "#howto",
            "name": f"How to use {page['tool_name']}",
            "description": page["tagline"],
            "totalTime": "PT1M",
            "tool": [{"@type": "HowToTool", "name": "A web browser"}],
            "step": [
                {"@type": "HowToStep", "position": i + 1, "name": step.rstrip("."),
                 "text": step, "url": f"{url}#step{i + 1}"}
                for i, step in enumerate(page["howto"])
            ],
        })

    page = dict(page)
    page["info"] = page["info"] + "\n\n" + faq_section(faqs)
    page["extra_schema"] = ",\n    " + ",\n    ".join(
        json.dumps(e, ensure_ascii=False, indent=6)[1:-1].strip().join("{}")
        for e in entries
    )
    return page


def build(page):
    """Render one tool page from the shared shell."""
    page = enrich(page)
    page = {**page, "further_reading": page.get("further_reading") or further_reading_html(page["slug"])}
    html = SHELL.format(**{**DEFAULTS, **page})
    path = os.path.join(TOOLS_DIR, page["slug"] + ".html")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("wrote", path)


# Every module that contributes tool pages. Adding a category means
# adding one module here, nothing else in the build changes.
TOOL_MODULES = [
    "pages_data",       # the original five hand-built tools
    "tools_text",
    "tools_converter",
    "tools_calculator",
    "tools_generator",
    "tools_developer",
    "tools_security",
    "tools_design",
    "tools_content",
    "tools_productivity",
    "tools_fun",
    "tools_image",
]


def collect():
    """Import every tool module that exists and gather its PAGES."""
    import importlib

    pages = []
    for name in TOOL_MODULES:
        try:
            mod = importlib.import_module(name)
        except ModuleNotFoundError:
            continue  # phase not built yet
        pages.extend(getattr(mod, "PAGES", []))
    return pages


if __name__ == "__main__":
    all_pages = collect()

    slugs = [p["slug"] for p in all_pages]
    dupes = {s for s in slugs if slugs.count(s) > 1}
    if dupes:
        raise SystemExit(f"duplicate slugs: {sorted(dupes)}")

    for page in all_pages:
        build(page)

    print(f"\n{len(all_pages)} tool pages built.")
