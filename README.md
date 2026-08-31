# 123MiniApps.online v2.0

95 browser-based mini tools. Everything runs client-side — no backend, no uploads,
no accounts, no tracking.

## Status

All 95 tools are built, wired and tested. 963 behavioural tests pass.

| Category | Tools | Tests |
|---|---:|---:|
| Text | 10 | 97 |
| Converters | 10 | 104 |
| Calculators | 10 | 95 |
| Generators | 12 | 94 |
| Developer | 12 | 106 |
| Security | 5 | 64 |
| Design | 8 | 71 |
| Content | 6 | 70 |
| Productivity | 6 | 75 |
| Fun | 6 | 67 |
| Image | 10 | 91 |
| Core site (homepage, data, all 95 pages boot) | — | 33 |

## Running the tests

```bash
npm install jsdom      # the only dev dependency
node test/run.js       # every suite
node test/run.js text  # one suite
```

`test/harness.js` boots a page in jsdom with stubs for the APIs jsdom lacks
(canvas, crypto.subtle, Image, FileReader, speechSynthesis). Read the comment
at the top before changing it — the script-execution ordering is subtle and
getting it wrong silently double-fires every event handler.

## Build system

Tool pages are **generated**, not hand-edited. The shared chrome — nav, footer,
theme switcher, search modal, script tags — lives in one place so a change
propagates to all 95 pages.

```bash
python3 build-tool-page.py
```

| File | Role |
|---|---|
| `build-tool-page.py` | Page shell + build loop |
| `toolkit.py` | Markup builders (`textarea()`, `slider()`, `info()`, …) |
| `tools_<category>.py` | One module per category, holding each tool's markup and logic |
| `pages_data.py` | The five originally hand-built tools |

**Do not edit `tools/*.html` directly** — the next build overwrites it. Edit the
category module and rebuild.

### Adding a tool

1. Append to `RAW_TOOLS` in `assets/data/tools.js`.
2. Add a `tool(...)` entry to the relevant `tools_<category>.py`.
3. Run `python3 build-tool-page.py`.
4. Add tests to `test/phase-<category>.js`.
5. Regenerate `sitemap.xml`.

`url`, `slug` and `tags` are derived automatically, so they cannot drift out of
sync with the tool's name.

## Architecture

```
assets/css/     10 layers — design tokens, then reset → components
assets/js/      config, theme-manager, search-engine, components,
                tool-utils, animations, pwa, analytics, main
assets/js/vendor/  qr-encoder.js, barcode-encoder.js — written in-house
assets/data/    tools.js (95 records), categories.js, testimonials.js
tools/          95 generated pages + _template.html
pages/          about, privacy, terms, contact
test/           harness + 12 suites
```

Every visual decision is a CSS custom property in `design-tokens.css`. The nine
themes are defined entirely by swapping `[data-theme]` on the root element.

## Verified, not assumed

- **QR encoder** — 48 forced-mask matrices compared byte-for-byte against
  Python's `qrcode` library.
- **Barcode encoder** — EAN-13, EAN-8 and UPC-A verified against
  `python-barcode`; Code 128 verified by an independent round-trip decoder.
- **Hashes** — checked against published SHA-1/256/512 digests for `"abc"`.
- **Encryption** — AES-256-GCM round-trip, plus confirmation that a wrong
  passphrase and a tampered ciphertext both fail rather than returning garbage.
- **Financial maths** — loan and compound-interest figures checked against
  independently derived values, not the implementation's own output.
- **Randomness** — 800 picker draws and 1,000 coin flips both land inside
  expected distribution bounds.
- **Contrast** — all 117 colour pairs across 9 themes meet their WCAG threshold.
- **Every page** — all 95 boot in jsdom with the full shared chrome and no
  runtime errors.

## Known limitations

- **No Lighthouse run.** The architecture targets the stated scores (critical CSS
  inlined, GPU-only animations, deferred JS, cached shell) but they are
  *designed for*, not measured.
- **`main.css` uses `@import`**, which costs a round-trip per file. Concatenate
  the 10 files in cascade order before deploying.
- **Image tools are tested for control flow and geometry, not pixels.** jsdom
  cannot decode images; verify visual output in a real browser.
- **Testimonials are illustrative**, clearly labelled as such. Replace with real
  attributed quotes before launch — fabricated testimonials are an FTC problem.
- **`privacy.html` is accurate only while the site stays backend-free.** If you
  add any data collection, rewrite it rather than shipping it as-is.

## Deployment checklist

- [ ] Concatenate CSS, drop the `@import` chain
- [ ] Replace the illustrative testimonials
- [ ] Point `contact.html`'s mailto at a real address
- [ ] Have a lawyer review `privacy.html` and `terms.html` for your jurisdiction
- [ ] Run Lighthouse and fix what it actually finds
- [ ] Confirm the service worker registers over HTTPS (it skips `file://`)
