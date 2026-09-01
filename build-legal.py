#!/usr/bin/env python3
# ============================================
# 123MiniApps.online v2.0
# File: build-legal.py
# Purpose: Generate the AdSense-recommended legal pages
#          (Disclaimer, Cookie Policy, DMCA) using the same
#          shared chrome as the other pages/ documents so
#          nav, footer, theme switcher and search all match.
# ============================================

import os

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(HERE, "pages")

SHELL = """<!DOCTYPE html>
<html lang="en" data-theme="indigo-nova">
<head>
<!-- ============================================
     123MiniApps.online v2.0
     File: pages/{slug}.html
     Purpose: {purpose}
     ============================================ -->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} | 123MiniApps</title>
<meta name="description" content="{description}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://www.123miniapps.online/pages/{slug}.html">
<meta property="og:type" content="website">
<meta property="og:title" content="{title} | 123MiniApps">
<meta property="og:description" content="{description}">
<meta property="og:url" content="https://www.123miniapps.online/pages/{slug}.html">
<meta property="og:image" content="https://www.123miniapps.online/assets/images/social/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0B1120">
<link rel="icon" href="../assets/images/logo.svg" type="image/svg+xml">
<link rel="manifest" href="../manifest.json">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap"></noscript>
<style>html{{background:#0B1120}}body{{margin:0;background:#0B1120;color:#fff;font-family:Inter,-apple-system,sans-serif}}</style>
<link rel="stylesheet" href="../assets/css/main.min.css?v=2.8.2">
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
      <a class="nav__link" href="../blog/index.html">Blog</a>
      <a class="nav__link" href="about.html">About</a>
      <a class="nav__link" href="contact.html">Contact</a>
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
    <a class="nav__link" href="../blog/index.html">Blog</a>
    <a class="nav__link" href="about.html">About</a>
    <a class="nav__link" href="privacy.html">Privacy</a>
    <a class="nav__link" href="terms.html">Terms</a>
    <a class="nav__link" href="contact.html">Contact</a>
  </nav>
</header>

<main class="tool-page" id="main">
  <div class="container container--narrow">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../index.html">Home</a>
      <span aria-hidden="true">/</span>
      <span aria-current="page">{title}</span>
    </nav>

    <h1 class="mb-4">{title}</h1>
    <p class="lead mb-12">{lead}</p>

    <div class="prose">
      <p class="text-muted"><strong>Last updated:</strong> <span id="policy-date">2026</span>. This document applies to www.123miniapps.online.</p>
{body}
      <p class="mt-8"><a href="../index.html">← Back to all 95 tools</a></p>
    </div>
  </div>
</main>

<footer class="footer">
  <div class="container">
    <div class="footer__bottom">
      <p>© <span id="copyright-year">2026</span> 123MiniApps.online</p>
      <p>
        <a class="footer__link" href="about.html">About</a> ·
        <a class="footer__link" href="contact.html">Contact</a> ·
        <a class="footer__link" href="privacy.html">Privacy</a> ·
        <a class="footer__link" href="terms.html">Terms</a> ·
        <a class="footer__link" href="disclaimer.html">Disclaimer</a> ·
        <a class="footer__link" href="cookies.html">Cookies</a> ·
        <a class="footer__link" href="dmca.html">DMCA</a>
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
<script src="../assets/js/search-engine.js?v=2.8.2" defer></script>
<script src="../assets/js/animations.js?v=2.8.2" defer></script>
<script src="../assets/js/pwa.js?v=2.8.2" defer></script>
<script src="../assets/js/analytics.js?v=2.8.2" defer></script>
<script src="../assets/js/consent.js?v=2.8.2" defer></script>
<script src="../assets/js/ads.js?v=2.8.2" defer></script>
<script src="../assets/js/main.js?v=2.8.2" defer></script>
<script defer>document.addEventListener('DOMContentLoaded',()=>{{document.getElementById('copyright-year').textContent=new Date().getFullYear();}});</script>
</body>
</html>
"""

PAGES = [
    {
        "slug": "disclaimer",
        "purpose": "General disclaimer of warranties and liability.",
        "title": "Disclaimer",
        "description": "Disclaimer for 123MiniApps: the free browser-based tools are provided as-is, for general use, with no warranty of accuracy or fitness for professional, legal, medical or financial decisions.",
        "lead": "The tools on this site are provided free, as-is, for general use. Read this before relying on any result for something that matters.",
        "body": """
      <h2>1. General information only</h2>
      <p>
        123MiniApps provides free online utilities for convenience and general use. The results a
        tool produces are for informational purposes only. We make no warranty, express or implied,
        that any output is accurate, complete, current, or fit for a particular purpose.
      </p>

      <h2>2. Not professional advice</h2>
      <p>
        Several tools touch areas where professional judgment matters: the calculators (loan, tax,
        BMI, percentage), the security tools (password strength, hashing) and the developer utilities.
        Nothing on this site is financial, legal, medical, tax or security advice. Do not make a
        professional, legal, medical or financial decision solely on the basis of a result from a
        free web tool. Consult a qualified professional for advice specific to your situation.
      </p>

      <h2>3. Accuracy and your own verification</h2>
      <p>
        We work to keep the tools correct and test them extensively, but software can contain errors,
        and browsers differ. You are responsible for verifying any result before you rely on it. If a
        calculation, conversion or generated value will be used for anything consequential, check it
        against an independent source.
      </p>

      <h2>4. Limitation of liability</h2>
      <p>
        To the fullest extent permitted by law, 123MiniApps and its operators are not liable for any
        loss or damage, including direct, indirect, incidental, consequential or punitive damages,
        arising from your use of, or inability to use, this site or any tool on it. You use the site
        at your own risk.
      </p>

      <h2>5. External links</h2>
      <p>
        The site and its blog may link to third-party websites for reference. We do not control those
        sites and are not responsible for their content, accuracy or practices. A link is not an
        endorsement.
      </p>

      <h2>6. Advertising</h2>
      <p>
        This site may display advertising served by third-party networks. Advertisers are solely
        responsible for the content of their ads and for the products or services they promote. We do
        not endorse advertised products and are not responsible for transactions between you and any
        advertiser.
      </p>

      <h2>7. Contact</h2>
      <p>
        Questions about this disclaimer can be sent through the <a href="contact.html">contact page</a>.
      </p>
""",
    },
    {
        "slug": "cookies",
        "purpose": "Cookie and local-storage policy.",
        "title": "Cookie Policy",
        "description": "Cookie policy for 123MiniApps: the site itself sets no tracking cookies and uses only local storage for preferences. Explains what changes if advertising is enabled.",
        "lead": "The site itself sets no tracking cookies. It uses your browser's local storage for a few preferences. Here is exactly what is stored and why.",
        "body": """
      <h2>1. What a cookie is</h2>
      <p>
        A cookie is a small text file a website asks your browser to store, which is sent back to that
        website on later visits. Related technologies, <code>localStorage</code> and
        <code>sessionStorage</code>, also store small amounts of data in your browser, but are read
        only by code running on the page and are not automatically transmitted anywhere.
      </p>

      <h2>2. What 123MiniApps stores</h2>
      <p>
        The site does not set tracking or advertising cookies of its own. It uses your browser's
        <code>localStorage</code> for a small set of preferences that stay on your device and are never
        sent to us:
      </p>
      <ul>
        <li><strong>Theme choice</strong>: which of the ten color themes you selected.</li>
        <li><strong>Favorites</strong>: the tools you have starred.</li>
        <li><strong>Recent searches</strong>: your last few search terms, for convenience.</li>
        <li><strong>Cookie-notice state</strong>: so any notice does not reappear on every visit.</li>
        <li><strong>Tool preferences</strong>: settings some tools remember between visits.</li>
      </ul>
      <p>
        You can delete all of it at any time by clearing your browser's site data for this domain.
        None of it identifies you, and none of it leaves your device.
      </p>

      <h2>3. Third-party fonts</h2>
      <p>
        The site loads its typefaces from Google Fonts. That request exposes your IP address and user
        agent to Google, as any request to any server does, but Google Fonts does not set advertising
        cookies through this mechanism. You can avoid it entirely by self-hosting the fonts.
      </p>

      <h2>4. If advertising is enabled</h2>
      <p>
        This site may display advertising from third-party networks such as
        <a href="https://adsterra.com/" rel="nofollow noopener" target="_blank">Adsterra</a> or Google AdSense.
        When advertising is active, those networks may set their own cookies or similar identifiers to
        measure and personalise the ads you see. That behaviour is controlled by the ad network, not by
        us, and it is separate from the tools themselves: your tool data (the text, files and inputs you
        work on) is never shared with advertisers because it never leaves your device. Where required by
        law, a consent banner will let you accept or reject non-essential cookies before any are set. You
        can also manage ad personalisation through Google's
        <a href="https://www.google.com/settings/ads" rel="nofollow noopener" target="_blank">Ads Settings</a>
        and opt-out tools such as <a href="https://www.aboutads.info/choices/" rel="nofollow noopener" target="_blank">aboutads.info</a>.
      </p>

      <h2>5. Managing cookies in your browser</h2>
      <p>
        Every major browser lets you view and delete cookies and local storage, and block them per
        site. Blocking storage for this domain will reset your theme and favorites on each visit but
        will not otherwise break the tools, since they run without needing stored data.
      </p>

      <h2>6. Contact</h2>
      <p>
        Questions about this cookie policy can be sent through the <a href="contact.html">contact page</a>.
      </p>
""",
    },
    {
        "slug": "dmca",
        "purpose": "DMCA / copyright takedown policy and procedure.",
        "title": "DMCA & Copyright Policy",
        "description": "DMCA copyright policy for 123MiniApps: how to submit a takedown notice, what a valid notice must contain, and the counter-notice process.",
        "lead": "We respect copyright. If you believe content on this site infringes yours, here is how to file a takedown notice and what it must include.",
        "body": """
      <h2>1. Our position</h2>
      <p>
        123MiniApps respects the intellectual property of others and expects its users to do the same.
        The tools and articles on this site are original work. If you believe material published here
        infringes a copyright you own or control, you may submit a notice under the U.S. Digital
        Millennium Copyright Act (DMCA), and we will respond promptly.
      </p>

      <h2>2. Filing a takedown notice</h2>
      <p>
        Send a written notice through the <a href="contact.html">contact page</a> (or the email address
        listed there) with the subject line "DMCA Takedown". To be valid, your notice must include:
      </p>
      <ul>
        <li>Your physical or electronic signature.</li>
        <li>Identification of the copyrighted work you claim has been infringed.</li>
        <li>The exact URL(s) on this site where the material appears, specific enough for us to locate it.</li>
        <li>Your name, address, telephone number and email address.</li>
        <li>A statement that you have a good-faith belief the use is not authorised by the copyright owner, its agent, or the law.</li>
        <li>A statement, under penalty of perjury, that the information in your notice is accurate and that you are the copyright owner or authorised to act on the owner's behalf.</li>
      </ul>

      <h2>3. What happens next</h2>
      <p>
        On receiving a valid notice, we will remove or disable access to the material in question
        within a reasonable time and, where possible, notify anyone who posted it. Incomplete notices
        may delay our response, so please include everything listed above.
      </p>

      <h2>4. Counter-notice</h2>
      <p>
        If you believe your material was removed by mistake or misidentification, you may send a
        counter-notice through the same channel, including your signature, identification of the
        removed material and its former location, a statement under penalty of perjury that you have a
        good-faith belief it was removed in error, and your contact information and consent to
        jurisdiction. We may restore the material unless the original complainant pursues a court order.
      </p>

      <h2>5. Repeat infringers</h2>
      <p>
        In appropriate circumstances we will act against parties who are repeat infringers.
      </p>

      <h2>6. Good faith</h2>
      <p>
        Please note that under Section 512(f) of the DMCA, anyone who knowingly materially
        misrepresents that material is infringing may be liable for damages. File notices in good faith.
      </p>
""",
    },
]


def build():
    for page in PAGES:
        html = SHELL.format(**page)
        path = os.path.join(PAGES_DIR, page["slug"] + ".html")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        print("wrote", path)


if __name__ == "__main__":
    build()
    print(f"\n{len(PAGES)} legal pages built.")
