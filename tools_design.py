#!/usr/bin/env python3
# ============================================
# 123MiniApps.online v2.0
# File: tools_design.py
# Purpose: The 7 remaining Design Tools
# (ids 71-77; 70 Color Picker is hand-built).
# ============================================

from toolkit import (
 tool, ws, info, row, text_input, number_input, select, switch, slider,
 color_input, output, status_line, buttons, HR, html_block,
)

PAGES = []

# ---------------------------------------------------------------
# 71. Color Palette Generator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="color-palette-generator", name="Color Palette Generator", icon="🖌️", cat="design",
 title="Colour Palette Generator: Harmonies from a Base Colour",
 description="Build harmonious colour palettes from a base colour using colour theory. Lock swatches, export CSS variables and check contrast automatically.",
 tagline="Generate harmonious palettes from a base colour, with contrast checked for you.",
 workspace=ws(
 row(
 color_input("base", "Base colour", "#00D4FF"),
 select("scheme", "Harmony", [
 ("complementary", "Complementary, opposite on the wheel"),
 ("analogous", "Analogous, neighbours"),
 ("triadic", "Triadic, evenly spaced three"),
 ("tetradic", "Tetradic, two complementary pairs"),
 ("split", "Split complementary"),
 ("monochromatic", "Monochromatic, one hue"),
 ("shades", "Tints and shades"),
 ], selected="analogous"),
 slider("count", "Swatches", 3, 8, 5, 1, unit=""),
 ),
 status_line("status", "Pick a base colour and a harmony."),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Palette</span><span class="field__hint">Click a swatch to copy · click the lock to keep it</span></span>
 <div class="swatch-grid" id="palette"></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Contrast against white and black</span></span>
 <div class="table-scroll"><div id="contrast"></div></div>
 </div>"""),
 output("css", "Export", None, "The palette will export here."),
 row(
 select("format", "Export format", [
 ("css", "CSS custom properties"),
 ("scss", "SCSS variables"),
 ("tailwind", "Tailwind config"),
 ("json", "JSON"),
 ("hex", "Plain hex list"),
 ], selected="css"),
 html_block(""" <div class="field"><span class="field__label"><span>&nbsp;</span></span>
 <button class="btn btn--secondary" id="randomise" type="button">Random palette</button>
 </div>"""),
 ),
 buttons(("copy", "Copy export", "primary"), ("download", "Download"), ("share", "Share tool", "ghost")),
 label="Colour palette generator",
 ),
 info_block=info(
 features=[
 "Seven harmony schemes based on colour theory",
 "Lock individual swatches while regenerating the rest",
 "WCAG contrast checked against white and black",
 "Five export formats including Tailwind config",
 "Three to eight swatches",
 ],
 howto=[
 "Choose a base colour.",
 "Pick a harmony scheme.",
 "Lock any swatch you want to keep, then randomise.",
 "Copy the export in your preferred format.",
 ],
 background_title="Colour harmony, and where the theory falls short",
 background_paragraphs=[
 "Harmony schemes come from positions on the colour wheel. Complementary colours sit opposite each other and produce maximum contrast, which is why they work for calls to action but clash in large areas. Analogous colours are neighbours and feel calm and cohesive, making them a safe choice for backgrounds. Triadic schemes take three evenly spaced hues for vibrancy without the tension of a direct complement.",
 "The traditional wheel has a real flaw, though. It is based on HSL, where a fixed lightness value does not correspond to equal perceived brightness, yellow at 50% lightness looks far brighter than blue at 50% lightness. This is why a mathematically generated palette often contains one swatch that jumps out. Perceptual colour spaces like OKLCH fix this, and modern CSS supports them, though browser support is still uneven.",
 "One practical rule beats most theory: the 60-30-10 split. Roughly 60% of a design should be a dominant neutral, 30% a secondary colour, and 10% an accent. Palettes fail more often from using every colour equally than from choosing the wrong hues. And whatever the wheel says, always verify contrast, a beautiful palette that fails WCAG AA is unusable for text, which is why the contrast table sits directly beneath the swatches here.",
 ],
 ),
 script=r""" let palette = [];
 let locked = new Set();

 function baseHsl() {
 const rgb = T.hexToRgb(T.$('base').value) || { r: 0, g: 212, b: 255 };
 return T.rgbToHsl(rgb.r, rgb.g, rgb.b);
 }

 function hexFromHsl(h, s, l) {
 const rgb = T.hslToRgb(h, T.clamp(s, 0, 100), T.clamp(l, 0, 100));
 return T.rgbToHex(rgb.r, rgb.g, rgb.b);
 }

 /**
 * Build the palette for the chosen scheme.
 * Locked swatches keep their previous value.
 */
 function build() {
 const { h, s, l } = baseHsl();
 const count = Number(T.$('count').value);
 const scheme = T.$('scheme').value;

 const offsets = {
 complementary: [0, 180],
 analogous: [-40, -20, 0, 20, 40],
 triadic: [0, 120, 240],
 tetradic: [0, 90, 180, 270],
 split: [0, 150, 210]
 }[scheme];

 const next = [];

 for (let i = 0; i < count; i++) {
 if (locked.has(i) && palette[i]) {
 next.push(palette[i]);
 continue;
 }

 if (scheme === 'monochromatic') {
 // Vary saturation and lightness, hold the hue
 next.push(hexFromHsl(h, T.clamp(s - 20 + i * 12, 15, 100), T.clamp(25 + i * (55 / count), 12, 92)));
 } else if (scheme === 'shades') {
 // Even ramp from dark to light through the base hue
 next.push(hexFromHsl(h, s, 12 + (i * 76) / (count - 1 || 1)));
 } else {
 const offset = offsets[i % offsets.length];
 // Vary lightness slightly on repeats so extra swatches differ
 const cycle = Math.floor(i / offsets.length);
 next.push(hexFromHsl(h + offset, s, T.clamp(l + cycle * 18 - 9, 18, 88)));
 }
 }

 palette = next;
 render();
 }

 function render() {
 const mount = T.$('palette');
 mount.innerHTML = '';

 palette.forEach((hex, index) => {
 const isLocked = locked.has(index);

 const swatch = el('div', { className: 'swatch' });

 const chip = el('button', {
 className: 'swatch__chip',
 attrs: { type: 'button', 'aria-label': `Copy ${hex}`, title: 'Click to copy' },
 style: { background: hex, width: '100%', border: 'none', cursor: 'pointer' }
 });
 chip.addEventListener('click', () => copyToClipboard(hex, hex + ' copied'));

 const label = el('span', { className: 'swatch__hex', text: hex });

 const lock = el('button', {
 className: 'btn btn--ghost btn--sm',
 attrs: {
 type: 'button',
 'aria-pressed': String(isLocked),
 'aria-label': `${isLocked ? 'Unlock' : 'Lock'} swatch ${index + 1}`
 },
 text: isLocked ? '🔒 Locked' : '🔓 Lock',
 style: { fontSize: '10px', padding: '2px 6px', minHeight: '0' }
 });
 lock.addEventListener('click', () => {
 locked.has(index) ? locked.delete(index) : locked.add(index);
 render();
 });

 swatch.append(chip, label, lock);
 mount.append(swatch);
 });

 renderContrast();
 renderExport();

 T.status('status',
 `${palette.length} swatch(es)${locked.size ? `, ${locked.size} locked` : ''}.`, 'ok');
 }

 function renderContrast() {
 const mount = T.$('contrast');
 mount.innerHTML = '';

 const white = { r: 255, g: 255, b: 255 };
 const black = { r: 0, g: 0, b: 0 };

 const rows = palette.map((hex) => {
 const rgb = T.hexToRgb(hex);
 const onWhite = T.contrast(rgb, white);
 const onBlack = T.contrast(rgb, black);
 const best = Math.max(onWhite, onBlack);

 return [
 hex,
 onWhite.toFixed(2) + ':1',
 onBlack.toFixed(2) + ':1',
 best >= 4.5 ? '✓ AA for text' : best >= 3 ? 'Large text only' : '✗ Decorative only'
 ];
 });

 mount.append(T.table(['Colour', 'On white', 'On black', 'Verdict'], rows));
 }

 function renderExport() {
 const format = T.$('format').value;
 let out;

 if (format === 'css') {
 out = ':root {\n' +
 palette.map((c, i) => ` --colour-${i + 1}: ${c};`).join('\n') + '\n}';
 } else if (format === 'scss') {
 out = palette.map((c, i) => `$colour-${i + 1}: ${c};`).join('\n');
 } else if (format === 'tailwind') {
 out = 'module.exports = {\n theme: {\n extend: {\n colors: {\n' +
 palette.map((c, i) => ` brand${i + 1}: '${c}',`).join('\n') +
 '\n }\n }\n }\n};';
 } else if (format === 'json') {
 out = JSON.stringify(
 Object.fromEntries(palette.map((c, i) => [`colour-${i + 1}`, c])), null, 2);
 } else {
 out = palette.join('\n');
 }

 T.setOutput('css', out);
 }

 T.on(['base'], build, 'input');
 T.on(['scheme'], build, 'change');
 T.on(['format'], renderExport, 'change');

 T.$('count').addEventListener('input', () => {
 T.$('count-value').textContent = T.$('count').value;
 // Locks beyond the new length no longer apply
 locked = new Set([...locked].filter((i) => i < Number(T.$('count').value)));
 build();
 });

 T.$('randomise').addEventListener('click', () => {
 const rgb = T.hslToRgb(T.randomInt(0, 359), T.randomInt(55, 95), T.randomInt(40, 65));
 T.$('base').value = T.rgbToHex(rgb.r, rgb.g, rgb.b);
 build();
 });

 T.wireActions({
 slug: 'color-palette-generator',
 getResult: () => T.$('css').textContent,
 filename: 'palette.css',
 mime: 'text/css'
 });

 build();""",
))

# ---------------------------------------------------------------
# 72. Contrast Checker
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="contrast-checker", name="Contrast Checker", icon="◐", cat="design",
 title="WCAG Contrast Checker: AA and AAA Compliance",
 description="Check text and background contrast ratios against WCAG AA and AAA thresholds, with a live preview and automatic suggestions when a pair fails.",
 tagline="Check colour contrast against WCAG thresholds, with fixes suggested when it fails.",
 workspace=ws(
 row(
 color_input("fg", "Text colour", "#8892B0"),
 color_input("bg", "Background colour", "#0B1120"),
 html_block(""" <div class="field">
 <span class="field__label"><span>&nbsp;</span></span>
 <button class="btn btn--secondary" id="swap" type="button">Swap colours</button>
 </div>"""),
 ),
 row(
 text_input("fg-hex", "Text hex", "#8892B0", "#8892B0"),
 text_input("bg-hex", "Background hex", "#0B1120", "#0B1120"),
 ),
 status_line("status", "Pick two colours to compare."),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result result--primary"><span class="result__value" id="r-ratio">, </span><span class="result__label">Contrast ratio</span></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Preview</span></span>
 <div id="preview" style="padding:var(--space-8);border-radius:var(--radius-md);border:1px solid var(--border-color)">
 <p id="preview-large" style="font-size:24px;font-weight:700;margin-bottom:12px">Large heading text</p>
 <p id="preview-body" style="font-size:16px;margin-bottom:12px">Body text at 16 pixels, which is the size most of your interface will actually use.</p>
 <p id="preview-small" style="font-size:12px">Small print at 12 pixels, captions, labels and legal text.</p>
 </div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>WCAG results</span></span>
 <div class="table-scroll"><div id="results"></div></div>
 </div>"""),
 html_block(""" <div class="field" id="suggestions-field" hidden>
 <span class="field__label"><span>Suggested fixes</span><span class="field__hint">Nearest passing colours, click to apply</span></span>
 <div class="swatch-grid" id="suggestions"></div>
 </div>"""),
 buttons(("copy", "Copy result", "primary"), ("share", "Share tool", "ghost")),
 label="Contrast checker",
 ),
 info_block=info(
 features=[
 "Contrast ratio to two decimal places",
 "AA and AAA verdicts for normal, large and UI elements",
 "Live preview at three text sizes",
 "Suggested nearest passing colours when a pair fails",
 "Hex entry as well as colour pickers",
 ],
 howto=[
 "Set your text and background colours.",
 "Read the ratio and the pass or fail verdicts.",
 "Check the preview at the size you will actually use.",
 "If it fails, click a suggested colour to apply it.",
 ],
 background_title="Reading the WCAG thresholds",
 background_paragraphs=[
 "WCAG 2.1 sets three thresholds. Normal body text needs 4.5:1 for AA and 7:1 for AAA. Large text, defined as 18pt regular or 14pt bold, roughly 24px and 18.66px, gets a lower bar of 3:1 for AA and 4.5:1 for AAA, because larger glyphs have thicker strokes and are easier to read at lower contrast. Non-text elements such as form borders, icons and focus indicators need 3:1 under criterion 1.4.11.",
 "The formula compares relative luminance, which weights the colour channels by human sensitivity: green contributes about 72%, red 21% and blue 7%. That is why blue text on black fails badly even when it looks distinct, blue contributes almost nothing to perceived luminance. It also means the ratio is symmetrical, so swapping foreground and background does not change it.",
 "Two things the ratio does not capture. It says nothing about colour blindness, red and green can have identical luminance and pass easily while being indistinguishable to roughly 8% of men. Never rely on colour alone to convey meaning. And WCAG 2's formula is known to be imperfect, particularly for dark themes where it can be overly permissive; APCA, developed for WCAG 3, models perception more accurately but is not yet a formal standard. Meeting 4.5:1 remains the defensible legal baseline today.",
 ],
 ),
 script=r""" let updating = false;

 function ratio() {
 const fg = T.hexToRgb(T.$('fg').value);
 const bg = T.hexToRgb(T.$('bg').value);
 if (!fg || !bg) return null;
 return T.contrast(fg, bg);
 }

 function verdictFor(value, threshold) {
 return value >= threshold
 ? { text: '✓ Pass', colour: 'var(--success)' }
 : { text: '✗ Fail', colour: 'var(--danger)' };
 }

 function update(source) {
 if (updating) return;

 // Keep the picker and the hex field in step
 updating = true;
 if (source === 'fg-hex' && T.hexToRgb(T.$('fg-hex').value)) {
 T.$('fg').value = T.rgbToHex(...Object.values(T.hexToRgb(T.$('fg-hex').value)));
 } else if (source === 'bg-hex' && T.hexToRgb(T.$('bg-hex').value)) {
 T.$('bg').value = T.rgbToHex(...Object.values(T.hexToRgb(T.$('bg-hex').value)));
 } else {
 T.$('fg-hex').value = T.$('fg').value.toUpperCase();
 T.$('bg-hex').value = T.$('bg').value.toUpperCase();
 }
 updating = false;

 const value = ratio();
 if (value === null) {
 T.status('status', 'One of those is not a valid hex colour.', 'error');
 return;
 }

 T.$('r-ratio').textContent = value.toFixed(2) + ':1';

 // Preview
 const preview = T.$('preview');
 preview.style.background = T.$('bg').value;
 ['preview-large', 'preview-body', 'preview-small'].forEach((id) => {
 T.$(id).style.color = T.$('fg').value;
 });

 // Results table
 const rows = [
 ['Normal text (AA)', '4.5:1', verdictFor(value, 4.5)],
 ['Normal text (AAA)', '7:1', verdictFor(value, 7)],
 ['Large text (AA)', '3:1', verdictFor(value, 3)],
 ['Large text (AAA)', '4.5:1', verdictFor(value, 4.5)],
 ['UI components (AA)', '3:1', verdictFor(value, 3)]
 ];

 const mount = T.$('results');
 mount.innerHTML = '';
 const table = T.table(['Requirement', 'Threshold', 'Result'],
 rows.map((r) => [r[0], r[1], r[2].text]));

 [...table.querySelectorAll('tbody tr')].forEach((tr, i) => {
 tr.lastElementChild.style.color = rows[i][2].colour;
 tr.lastElementChild.style.fontWeight = 'var(--weight-semibold)';
 });
 mount.append(table);

 // Suggestions when body text fails
 if (value < 4.5) {
 renderSuggestions();
 T.$('suggestions-field').hidden = false;
 T.status('status',
 `${value.toFixed(2)}:1, fails AA for body text. Needs 4.5:1.`, 'error');
 } else {
 T.$('suggestions-field').hidden = true;
 T.status('status',
 `${value.toFixed(2)}:1, passes AA${value >= 7 ? ' and AAA' : ''} for body text.`, 'ok');
 }

 if (window.Analytics) Analytics.trackToolUse('contrast-checker');
 }

 /**
 * Walk the foreground colour's lightness up and down until it clears
 * the AA threshold, and offer the nearest passing options.
 */
 function renderSuggestions() {
 const mount = T.$('suggestions');
 mount.innerHTML = '';

 const fgRgb = T.hexToRgb(T.$('fg').value);
 const bgRgb = T.hexToRgb(T.$('bg').value);
 if (!fgRgb || !bgRgb) return;

 const { h, s, l } = T.rgbToHsl(fgRgb.r, fgRgb.g, fgRgb.b);
 const found = [];

 for (const direction of [-1, 1]) {
 for (let step = 1; step <= 100; step++) {
 const lightness = l + direction * step;
 if (lightness < 0 || lightness > 100) break;

 const candidate = T.hslToRgb(h, s, lightness);
 if (T.contrast(candidate, bgRgb) >= 4.5) {
 found.push({
 hex: T.rgbToHex(candidate.r, candidate.g, candidate.b),
 label: direction < 0 ? 'Darker' : 'Lighter',
 ratio: T.contrast(candidate, bgRgb)
 });
 break;
 }
 }
 }

 // Also offer plain white and black as guaranteed fallbacks
 [['#FFFFFF', 'White'], ['#000000', 'Black']].forEach(([hex, label]) => {
 const rgb = T.hexToRgb(hex);
 const r = T.contrast(rgb, bgRgb);
 if (r >= 4.5) found.push({ hex, label, ratio: r });
 });

 found.forEach((item) => {
 const swatch = el('div', { className: 'swatch' });

 const chip = el('button', {
 className: 'swatch__chip',
 attrs: { type: 'button', 'aria-label': `Use ${item.hex}` },
 style: { background: item.hex, width: '100%', border: 'none', cursor: 'pointer' }
 });
 chip.addEventListener('click', () => {
 T.$('fg').value = item.hex;
 update();
 });

 swatch.append(
 chip,
 el('span', { className: 'swatch__hex', text: item.hex }),
 el('span', {
 className: 'swatch__hex',
 text: `${item.label} · ${item.ratio.toFixed(1)}:1`,
 style: { fontSize: '10px' }
 })
 );

 mount.append(swatch);
 });
 }

 T.on(['fg', 'bg'], () => update(), 'input');
 T.on(['fg-hex'], () => update('fg-hex'));
 T.on(['bg-hex'], () => update('bg-hex'));

 T.$('swap').addEventListener('click', () => {
 const fg = T.$('fg').value;
 T.$('fg').value = T.$('bg').value;
 T.$('bg').value = fg;
 update();
 });

 T.$('copy').addEventListener('click', () => {
 copyToClipboard(
 `${T.$('fg').value} on ${T.$('bg').value}, ${T.$('r-ratio').textContent}`,
 'Result copied');
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Contrast Checker | 123MiniApps' }));

 update();""",
))

# ---------------------------------------------------------------
# 73. Box Shadow Generator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="box-shadow-generator", name="Box Shadow Generator", icon="🌑", cat="design",
 title="CSS Box Shadow Generator: Layered and Inset Shadows",
 description="Compose CSS box-shadows visually with multiple stacked layers, inset support and a live preview. Copy the generated CSS or a Tailwind class.",
 tagline="Compose layered CSS box-shadows visually, with a live preview.",
 workspace=ws(
 html_block(""" <div class="field">
 <span class="field__label"><span>Shadow layers</span><span class="field__hint">Stack several for realistic depth</span></span>
 <div id="layers"></div>
 </div>"""),
 buttons(("add", "Add a layer", "secondary"), ("preset-soft", "Soft"), ("preset-material", "Material"), ("preset-hard", "Hard"), ("preset-glow", "Glow")),
 HR,
 row(
 color_input("bg", "Preview background", "#131842"),
 color_input("box", "Box colour", "#1A1F4E"),
 slider("radius", "Corner radius", 0, 60, 22, 2, unit="px"),
 ),
 html_block(""" <div class="preview-surface" id="surface">
 <div id="preview-box" style="width:180px;height:120px"></div>
 </div>"""),
 status_line("status", "Adjust the layers to build your shadow."),
 output("css", "CSS", None, "The CSS will appear here."),
 buttons(("copy", "Copy CSS", "primary"), ("copy-tailwind", "Copy Tailwind class"), ("download", "Download"), ("share", "Share tool", "ghost")),
 label="Box shadow generator",
 ),
 info_block=info(
 features=[
 "Unlimited stacked shadow layers",
 "Inset shadows for inner depth",
 "Independent colour and opacity per layer",
 "Four starting presets",
 "Copies plain CSS or a Tailwind arbitrary value",
 ],
 howto=[
 "Start from a preset, or add layers manually.",
 "Adjust offset, blur, spread and colour per layer.",
 "Watch the live preview.",
 "Copy the CSS into your stylesheet.",
 ],
 background_title="Why one shadow rarely looks right",
 background_paragraphs=[
 "A single box-shadow reads as artificial because real shadows are not uniform. Light scatters, so an object close to a surface casts a tight dark shadow while ambient light produces a much softer, wider one. Stacking two or three layers, one tight and slightly opaque, one broad and very faint, mimics that and is what every mature design system does. Material Design's elevation levels are all multi-layer for exactly this reason.",
 "The four values are offset-x, offset-y, blur and spread. Blur softens the edge and roughly doubles the visual size of the shadow; spread grows or shrinks it before blurring. A common mistake is a large blur with no vertical offset, which produces a glow rather than a shadow because it implies light coming from directly in front. Real interfaces usually assume light from above, so the vertical offset should exceed the horizontal.",
 "Two practical notes. Shadow colour should rarely be pure black at high opacity, a very dark tint of the background hue at 10% to 25% opacity looks far more natural, which is why the presets here use rgba rather than solid values. And box-shadow is expensive to animate, since it forces a repaint on every frame. If you need a shadow to change on hover, animate the <code>opacity</code> of a pseudo-element carrying the larger shadow instead, which stays on the compositor.",
 ],
 ),
 script=r""" const PRESETS = {
 soft: [
 { x: 0, y: 4, blur: 12, spread: 0, colour: '#000000', alpha: 12, inset: false },
 { x: 0, y: 12, blur: 32, spread: -8, colour: '#000000', alpha: 18, inset: false }
 ],
 material: [
 { x: 0, y: 2, blur: 4, spread: -1, colour: '#000000', alpha: 20, inset: false },
 { x: 0, y: 4, blur: 5, spread: 0, colour: '#000000', alpha: 14, inset: false },
 { x: 0, y: 1, blur: 10, spread: 0, colour: '#000000', alpha: 12, inset: false }
 ],
 hard: [
 { x: 6, y: 6, blur: 0, spread: 0, colour: '#00D4FF', alpha: 100, inset: false }
 ],
 glow: [
 { x: 0, y: 0, blur: 24, spread: 2, colour: '#00D4FF', alpha: 45, inset: false },
 { x: 0, y: 0, blur: 60, spread: 8, colour: '#7B61FF', alpha: 25, inset: false }
 ]
 };

 let layers = JSON.parse(JSON.stringify(PRESETS.soft));

 function rgba(hex, alpha) {
 const rgb = T.hexToRgb(hex) || { r: 0, g: 0, b: 0 };
 return `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${(alpha / 100).toFixed(2)})`;
 }

 function shadowCSS() {
 if (!layers.length) return 'none';
 return layers.map((l) =>
 `${l.inset ? 'inset ' : ''}${l.x}px ${l.y}px ${l.blur}px ${l.spread}px ${rgba(l.colour, l.alpha)}`
 ).join(', ');
 }

 function renderLayers() {
 const mount = T.$('layers');
 mount.innerHTML = '';

 layers.forEach((layer, index) => {
 const panel = el('div', {
 className: 'info-panel mb-3',
 style: { padding: 'var(--space-4)' }
 });

 const head = el('div', { className: 'flex items-center justify-between mb-3' }, [
 el('strong', { className: 'text-sm', text: `Layer ${index + 1}` })
 ]);

 const remove = el('button', {
 className: 'btn btn--ghost btn--sm',
 attrs: { type: 'button', 'aria-label': `Remove layer ${index + 1}` },
 text: '✕'
 });
 remove.addEventListener('click', () => {
 layers.splice(index, 1);
 renderLayers();
 render();
 });
 head.append(remove);
 panel.append(head);

 const grid = el('div', { className: 'workspace__row' });

 const slider = (key, label, min, max) => {
 const wrap = el('div', { className: 'field' });
 const value = el('span', { className: 'field__hint', text: layer[key] + 'px' });

 const input = el('input', {
 className: 'range',
 attrs: { type: 'range', min: String(min), max: String(max),
 value: String(layer[key]), 'aria-label': `${label} for layer ${index + 1}` }
 });
 input.addEventListener('input', () => {
 layer[key] = Number(input.value);
 value.textContent = layer[key] + 'px';
 render();
 });

 wrap.append(
 el('span', { className: 'field__label' }, [el('span', { text: label }), value]),
 input
 );
 return wrap;
 };

 grid.append(
 slider('x', 'Offset X', -60, 60),
 slider('y', 'Offset Y', -60, 60),
 slider('blur', 'Blur', 0, 120),
 slider('spread', 'Spread', -40, 60)
 );

 const bottom = el('div', { className: 'workspace__row' });

 const colourWrap = el('div', { className: 'field' });
 const colour = el('input', {
 className: 'input',
 attrs: { type: 'color', value: layer.colour, 'aria-label': `Colour for layer ${index + 1}` },
 style: { height: '44px', padding: '4px', cursor: 'pointer' }
 });
 colour.addEventListener('input', () => { layer.colour = colour.value; render(); });
 colourWrap.append(el('span', { className: 'field__label' }, [el('span', { text: 'Colour' })]), colour);

 const alphaWrap = el('div', { className: 'field' });
 const alphaValue = el('span', { className: 'field__hint', text: layer.alpha + '%' });
 const alpha = el('input', {
 className: 'range',
 attrs: { type: 'range', min: '0', max: '100', value: String(layer.alpha),
 'aria-label': `Opacity for layer ${index + 1}` }
 });
 alpha.addEventListener('input', () => {
 layer.alpha = Number(alpha.value);
 alphaValue.textContent = layer.alpha + '%';
 render();
 });
 alphaWrap.append(
 el('span', { className: 'field__label' }, [el('span', { text: 'Opacity' }), alphaValue]),
 alpha
 );

 const insetWrap = el('label', { className: 'switch' });
 const inset = el('input', {
 className: 'switch__input',
 attrs: { type: 'checkbox', 'aria-label': `Inset for layer ${index + 1}` }
 });
 inset.checked = layer.inset;
 inset.addEventListener('change', () => { layer.inset = inset.checked; render(); });
 insetWrap.append(
 inset,
 el('span', { className: 'switch__track' }, [el('span', { className: 'switch__thumb' })]),
 el('span', { text: 'Inset' })
 );

 bottom.append(colourWrap, alphaWrap, insetWrap);
 panel.append(grid, bottom);
 mount.append(panel);
 });
 }

 function render() {
 const css = shadowCSS();

 T.$('surface').style.background = T.$('bg').value;
 // The colour input is #box; the preview element is #preview-box.
 // Sharing one id meant the preview never picked up the colour.
 const box = T.$('preview-box');
 box.style.background = T.$('box').value;
 box.style.borderRadius = T.$('radius').value + 'px';
 box.style.boxShadow = css;

 T.$('radius-value').textContent = T.$('radius').value;
 T.setOutput('css', `box-shadow: ${css};`);

 T.status('status', `${layers.length} layer(s).`, 'ok');
 if (window.Analytics) Analytics.trackToolUse('box-shadow-generator');
 }

 T.$('add').addEventListener('click', () => {
 layers.push({ x: 0, y: 8, blur: 24, spread: 0, colour: '#000000', alpha: 20, inset: false });
 renderLayers();
 render();
 });

 Object.keys(PRESETS).forEach((name) => {
 T.$('preset-' + name).addEventListener('click', () => {
 layers = JSON.parse(JSON.stringify(PRESETS[name]));
 renderLayers();
 render();
 });
 });

 T.on(['bg', 'box'], render, 'input');
 T.$('radius').addEventListener('input', render);

 T.$('copy').addEventListener('click', () =>
 copyToClipboard(`box-shadow: ${shadowCSS()};`, 'CSS copied'));

 T.$('copy-tailwind').addEventListener('click', () =>
 copyToClipboard(`shadow-[${shadowCSS().replace(/\s+/g, '_')}]`, 'Tailwind class copied'));

 T.$('download').addEventListener('click', () =>
 downloadFile(`.shadow {\n box-shadow: ${shadowCSS()};\n}\n`, 'shadow.css', 'text/css'));

 T.$('share').addEventListener('click', () => shareLink({ title: 'Box Shadow Generator | 123MiniApps' }));

 renderLayers();
 render();""",
))

# ---------------------------------------------------------------
# 74. Border Radius Generator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="border-radius-generator", name="Border Radius Generator", icon="⬜", cat="design",
 title="CSS Border Radius Generator: Per-Corner and Blob Shapes",
 description="Dial in per-corner border radii, including elliptical values for organic blob shapes, with a live preview and copyable shorthand CSS.",
 tagline="Control every corner independently, including elliptical radii for blob shapes.",
 workspace=ws(
 switch("advanced", "Elliptical mode, separate horizontal and vertical radii", False),
 html_block(""" <div class="workspace__row" id="simple-controls"></div>"""),
 html_block(""" <div id="advanced-controls" hidden></div>"""),
 row(
 switch("linked", "Link all corners", False),
 slider("size", "Preview size", 100, 320, 200, 10, unit="px"),
 ),
 row(color_input("box", "Shape colour", "#00D4FF"), color_input("bg", "Background", "#131842")),
 status_line("status", "Adjust the corners."),
 html_block(""" <div class="preview-surface" id="surface">
 <div id="preview-box"></div>
 </div>"""),
 output("css", "CSS", None, "The CSS will appear here."),
 buttons(("copy", "Copy CSS", "primary"), ("blob", "Random blob"), ("reset", "Reset"), ("download", "Download"), ("share", "Share tool", "ghost")),
 label="Border radius generator",
 ),
 info_block=info(
 features=[
 "Independent control of all four corners",
 "Elliptical mode for organic blob shapes",
 "Link corners together for uniform rounding",
 "Live preview at adjustable size",
 "Copies the shortest valid shorthand",
 ],
 howto=[
 "Drag the sliders for each corner.",
 "Turn on elliptical mode for asymmetric curves.",
 "Press Random blob for an organic shape.",
 "Copy the CSS when you are happy.",
 ],
 background_title="Border radius syntax and the squircle problem",
 background_paragraphs=[
 "The shorthand accepts one to four values, applied clockwise from the top left: one value rounds every corner, two set top-left/bottom-right and top-right/bottom-left, and four set each corner individually. The slash syntax is the less-known part, <code>border-radius: 50% 20% / 30% 40%</code> gives horizontal radii before the slash and vertical radii after, which is what produces elliptical rather than circular corners and makes organic blob shapes possible.",
 "Percentages behave differently from pixels in a way that catches people out. A percentage is relative to the element's own dimensions, so <code>border-radius: 50%</code> turns a square into a circle and a rectangle into an ellipse. Pixel values stay fixed regardless of size, which is usually what you want for cards and buttons where the corner should look consistent across different content lengths.",
 "One thing CSS cannot currently do well is the squircle. Apple's icon shape is a superellipse with continuous curvature, where the transition from straight edge to curve is smooth rather than abrupt. A CSS border-radius is a plain quarter-ellipse, and at large radii the discontinuity is visible as a slight flattening where the curve meets the edge. Approximating a true squircle today needs an SVG path or a clip-path; the proposed <code>corner-shape</code> property would fix this but is not yet widely available.",
 ],
 ),
 script=r""" const CORNERS = [
 ['tl', 'Top left'], ['tr', 'Top right'],
 ['br', 'Bottom right'], ['bl', 'Bottom left']
 ];

 let simple = { tl: 22, tr: 22, br: 22, bl: 22 };
 let elliptical = {
 tl: [30, 70], tr: [70, 30], br: [30, 70], bl: [70, 30]
 };

 function buildSimpleControls() {
 const mount = T.$('simple-controls');
 mount.innerHTML = '';

 CORNERS.forEach(([key, label]) => {
 const wrap = el('div', { className: 'field' });
 const value = el('span', { className: 'field__hint', text: simple[key] + 'px' });

 const input = el('input', {
 className: 'range',
 attrs: { type: 'range', min: '0', max: '150', value: String(simple[key]),
 'aria-label': label + ' radius' }
 });

 input.addEventListener('input', () => {
 const v = Number(input.value);
 if (T.$('linked').checked) {
 CORNERS.forEach(([k]) => { simple[k] = v; });
 buildSimpleControls();
 } else {
 simple[key] = v;
 value.textContent = v + 'px';
 }
 render();
 });

 wrap.append(el('span', { className: 'field__label' }, [el('span', { text: label }), value]), input);
 mount.append(wrap);
 });
 }

 function buildAdvancedControls() {
 const mount = T.$('advanced-controls');
 mount.innerHTML = '';

 CORNERS.forEach(([key, label]) => {
 const rowEl = el('div', { className: 'workspace__row' });

 ['Horizontal', 'Vertical'].forEach((axis, axisIndex) => {
 const wrap = el('div', { className: 'field' });
 const value = el('span', { className: 'field__hint', text: elliptical[key][axisIndex] + '%' });

 const input = el('input', {
 className: 'range',
 attrs: { type: 'range', min: '0', max: '100', value: String(elliptical[key][axisIndex]),
 'aria-label': `${label} ${axis.toLowerCase()} radius` }
 });

 input.addEventListener('input', () => {
 elliptical[key][axisIndex] = Number(input.value);
 value.textContent = input.value + '%';
 render();
 });

 wrap.append(
 el('span', { className: 'field__label' },
 [el('span', { text: `${label}, ${axis}` }), value]),
 input
 );
 rowEl.append(wrap);
 });

 mount.append(rowEl);
 });
 }

 function radiusCSS() {
 if (T.$('advanced').checked) {
 const h = CORNERS.map(([k]) => elliptical[k][0] + '%').join(' ');
 const v = CORNERS.map(([k]) => elliptical[k][1] + '%').join(' ');
 return `${h} / ${v}`;
 }

 const { tl, tr, br, bl } = simple;

 // Emit the shortest equivalent shorthand
 if (tl === tr && tr === br && br === bl) return `${tl}px`;
 if (tl === br && tr === bl) return `${tl}px ${tr}px`;
 if (tr === bl) return `${tl}px ${tr}px ${br}px`;
 return `${tl}px ${tr}px ${br}px ${bl}px`;
 }

 function render() {
 const css = radiusCSS();
 const size = Number(T.$('size').value);

 const box = T.$('preview-box');
 box.style.width = size + 'px';
 box.style.height = size + 'px';
 box.style.background = T.$('box').value;
 box.style.borderRadius = css;

 T.$('surface').style.background = T.$('bg').value;
 T.$('size-value').textContent = size;

 T.setOutput('css', `border-radius: ${css};`);
 T.status('status', T.$('advanced').checked ? 'Elliptical mode.' : 'Simple mode.', 'ok');

 if (window.Analytics) Analytics.trackToolUse('border-radius-generator');
 }

 function syncMode() {
 const advanced = T.$('advanced').checked;
 T.$('simple-controls').hidden = advanced;
 T.$('advanced-controls').hidden = !advanced;
 T.$('linked').closest('.switch').style.display = advanced ? 'none' : '';
 render();
 }

 T.$('advanced').addEventListener('change', syncMode);
 T.$('size').addEventListener('input', render);
 T.on(['box', 'bg'], render, 'input');

 T.$('linked').addEventListener('change', () => {
 if (T.$('linked').checked) {
 const v = simple.tl;
 CORNERS.forEach(([k]) => { simple[k] = v; });
 buildSimpleControls();
 render();
 }
 });

 T.$('blob').addEventListener('click', () => {
 T.$('advanced').checked = true;
 CORNERS.forEach(([k]) => {
 elliptical[k] = [T.randomInt(20, 80), T.randomInt(20, 80)];
 });
 buildAdvancedControls();
 syncMode();
 });

 T.$('reset').addEventListener('click', () => {
 simple = { tl: 22, tr: 22, br: 22, bl: 22 };
 elliptical = { tl: [30, 70], tr: [70, 30], br: [30, 70], bl: [70, 30] };
 T.$('advanced').checked = false;
 buildSimpleControls();
 buildAdvancedControls();
 syncMode();
 });

 T.$('copy').addEventListener('click', () =>
 copyToClipboard(`border-radius: ${radiusCSS()};`, 'CSS copied'));

 T.$('download').addEventListener('click', () =>
 downloadFile(`.shape {\n border-radius: ${radiusCSS()};\n}\n`, 'radius.css', 'text/css'));

 T.$('share').addEventListener('click', () => shareLink({ title: 'Border Radius Generator | 123MiniApps' }));

 buildSimpleControls();
 buildAdvancedControls();
 syncMode();""",
))

# ---------------------------------------------------------------
# 75. Font Pairing Tool
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="font-pairing-tool", name="Font Pairing Tool", icon="🔤", cat="design",
 title="Font Pairing Tool: Curated Heading and Body Combinations",
 description="Browse curated heading and body font pairings with live specimen text, adjustable sizes and weights, and ready-to-paste embed code.",
 tagline="Browse curated font pairings with live specimen text and ready-to-paste code.",
 workspace=ws(
 row(
 select("pairing", "Curated pairing", []),
 select("category", "Filter by mood", [
 ("all", "All pairings"), ("classic", "Classic"), ("modern", "Modern"),
 ("editorial", "Editorial"), ("technical", "Technical"),
 ], selected="all"),
 ),
 row(
 slider("heading-size", "Heading size", 24, 84, 48, 2, unit="px"),
 slider("body-size", "Body size", 12, 24, 17, 1, unit="px"),
 slider("line-height", "Body line height", 12, 22, 16, 1, unit="/10"),
 ),
 row(
 text_input("sample-heading", "Heading text", "The quick brown fox", "The quick brown fox"),
 select("weight", "Heading weight", [("400", "Regular"), ("600", "Semibold"), ("700", "Bold"), ("800", "Extrabold")], selected="700"),
 ),
 status_line("status", "Pick a pairing to preview it."),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Specimen</span></span>
 <div id="specimen" style="padding:var(--space-8);background:var(--bg-surface);border:1px solid var(--border-color);border-radius:var(--radius-md)">
 <h3 id="spec-heading" style="margin-bottom:var(--space-4)">The quick brown fox</h3>
 <p id="spec-body" style="margin-bottom:var(--space-4)">Typography is the craft of arranging type to make written language legible, readable and appealing when displayed. The arrangement of type involves selecting typefaces, point sizes, line lengths, line spacing and letter spacing.</p>
 <p id="spec-small" style="font-size:0.85em;opacity:.75">A second paragraph at a smaller size, showing how the body face holds up in captions and secondary text where the line length is shorter.</p>
 </div>
 </div>"""),
 output("css", "CSS and embed code", None, "The code will appear here."),
 buttons(("copy", "Copy code", "primary"), ("random", "Random pairing"), ("download", "Download"), ("share", "Share tool", "ghost")),
 label="Font pairing tool",
 ),
 info_block=info(
 features=[
 "Twenty curated pairings across four moods",
 "Live specimen with your own text",
 "Adjustable size, weight and line height",
 "Google Fonts embed code included",
 "System-font fallbacks in every stack",
 ],
 howto=[
 "Pick a pairing, or filter by mood first.",
 "Type your own heading into the specimen.",
 "Adjust sizes until it reads well.",
 "Copy the CSS and embed code.",
 ],
 background_title="What makes two typefaces work together",
 background_paragraphs=[
 "The reliable principle is contrast with a shared quality. Two faces that are too similar look like a mistake rather than a decision, pairing two humanist sans-serifs usually reads as inconsistent rather than harmonious. Real contrast comes from pairing across categories: a serif heading with a sans body, or a geometric display face with a neutral text face. The shared quality that holds them together is usually a similar x-height or a comparable era of design.",
 "Superfamilies remove the guesswork entirely. Faces like Source Serif and Source Sans, or IBM Plex Serif and IBM Plex Sans, were designed together with matching proportions and metrics. If a pairing has to work without much typographic judgement, a superfamily is close to foolproof.",
 "Two practical constraints matter more than aesthetics. Each additional font weight and style is a separate file to download, so a page loading four weights of two families can easily add 200 KB of render-blocking requests, two weights of each is usually plenty. And <code>font-display: swap</code> should be set on every web font, otherwise the browser hides the text entirely while the font loads, producing a flash of invisible text that hurts both perceived speed and Core Web Vitals.",
 ],
 ),
 script=r""" const PAIRINGS = [
 ['Playfair Display', 'Source Sans 3', 'editorial', 'High-contrast serif headings over a clean, highly legible sans.'],
 ['Merriweather', 'Open Sans', 'classic', 'A sturdy screen serif with the most widely used humanist sans.'],
 ['Montserrat', 'Merriweather', 'classic', 'Geometric sans headings above a warm, readable serif body.'],
 ['Inter', 'Inter', 'modern', 'A single superfamily, impossible to get wrong, works at every size.'],
 ['Space Grotesk', 'Inter', 'modern', 'Quirky geometric headings grounded by a neutral body face.'],
 ['DM Serif Display', 'DM Sans', 'editorial', 'A matched superfamily with elegant display serifs.'],
 ['Libre Baskerville', 'Source Sans 3', 'classic', 'A transitional serif rooted in eighteenth-century printing.'],
 ['Oswald', 'Lato', 'modern', 'Condensed headings that save horizontal space, with a friendly body.'],
 ['Lora', 'Lato', 'editorial', 'Calligraphic serif headings with a humanist sans beneath.'],
 ['Poppins', 'Roboto', 'modern', 'Circular geometric headings with a neutral workhorse body.'],
 ['IBM Plex Serif', 'IBM Plex Sans', 'technical', 'A superfamily designed for documentation and technical writing.'],
 ['JetBrains Mono', 'Inter', 'technical', 'Monospaced headings for a deliberately technical feel.'],
 ['Bitter', 'Source Sans 3', 'technical', 'A slab serif that stays sharp at small sizes on screen.'],
 ['Raleway', 'Merriweather', 'editorial', 'Elegant thin-stroke headings over a solid reading serif.'],
 ['Work Sans', 'Work Sans', 'modern', 'One family across the whole hierarchy, varied only by weight.'],
 ['Cormorant Garamond', 'Proza Libre', 'editorial', 'Refined old-style serif for long-form editorial layouts.'],
 ['Archivo Black', 'Archivo', 'modern', 'Heavy display weight paired with its own text companion.'],
 ['Nunito', 'Nunito Sans', 'classic', 'Rounded terminals throughout, approachable and soft.'],
 ['Fira Sans', 'Fira Sans', 'technical', 'Designed for legibility on low-resolution screens.'],
 ['Rubik', 'Karla', 'modern', 'Slightly rounded geometric headings with a grotesque body.']
 ];

 const FALLBACK_SERIF = "Georgia, 'Times New Roman', serif";
 const FALLBACK_SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
 const FALLBACK_MONO = "'SF Mono', Consolas, monospace";

 function fallbackFor(name) {
 if (/mono/i.test(name)) return FALLBACK_MONO;
 if (/serif|playfair|merriweather|lora|baskerville|bitter|cormorant|garamond|georgia/i.test(name)) {
 return FALLBACK_SERIF;
 }
 return FALLBACK_SANS;
 }

 function populate() {
 const filter = T.$('category').value;
 const select = T.$('pairing');
 const previous = select.value;
 select.innerHTML = '';

 PAIRINGS.forEach(([heading, body, category], index) => {
 if (filter !== 'all' && category !== filter) return;
 const opt = document.createElement('option');
 opt.value = String(index);
 opt.textContent = heading === body ? `${heading} (superfamily)` : `${heading} + ${body}`;
 select.append(opt);
 });

 if (!select.options.length) {
 const opt = document.createElement('option');
 opt.textContent = 'No pairings in this category';
 select.append(opt);
 return;
 }

 // Keep the current selection if it survived the filter
 if ([...select.options].some((o) => o.value === previous)) select.value = previous;
 render();
 }

 function render() {
 const index = Number(T.$('pairing').value);
 const pairing = PAIRINGS[index];
 if (!pairing) return;

 const [heading, body, category, note] = pairing;

 const headingStack = `'${heading}', ${fallbackFor(heading)}`;
 const bodyStack = `'${body}', ${fallbackFor(body)}`;

 const headingSize = Number(T.$('heading-size').value);
 const bodySize = Number(T.$('body-size').value);
 const lineHeight = Number(T.$('line-height').value) / 10;
 const weight = T.$('weight').value;

 T.$('heading-size-value').textContent = headingSize;
 T.$('body-size-value').textContent = bodySize;
 T.$('line-height-value').textContent = lineHeight.toFixed(1);

 const specHeading = T.$('spec-heading');
 specHeading.style.fontFamily = headingStack;
 specHeading.style.fontSize = headingSize + 'px';
 specHeading.style.fontWeight = weight;
 specHeading.style.lineHeight = '1.15';
 specHeading.textContent = T.$('sample-heading').value || 'The quick brown fox';

 ['spec-body', 'spec-small'].forEach((id) => {
 const node = T.$(id);
 node.style.fontFamily = bodyStack;
 node.style.fontSize = bodySize + 'px';
 node.style.lineHeight = String(lineHeight);
 });

 // Load the fonts so the specimen is accurate
 loadFonts([heading, body]);

 const families = [...new Set([heading, body])]
 .map((f) => f.replace(/ /g, '+') + ':wght@400;600;700;800')
 .join('&family=');

 T.setOutput('css',
 `<!-- Add to <head> -->\n` +
 `<link rel="preconnect" href="https://fonts.googleapis.com">\n` +
 `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n` +
 `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=${families}&display=swap">\n\n` +
 `/* CSS */\n` +
 `h1, h2, h3 {\n font-family: ${headingStack};\n font-weight: ${weight};\n line-height: 1.15;\n}\n\n` +
 `body {\n font-family: ${bodyStack};\n font-size: ${bodySize}px;\n line-height: ${lineHeight};\n}`
 );

 T.status('status', note, 'ok');
 void category;

 if (window.Analytics) Analytics.trackToolUse('font-pairing-tool');
 }

 const loaded = new Set();

 /** Inject a Google Fonts stylesheet once per family. */
 function loadFonts(families) {
 families.forEach((family) => {
 if (loaded.has(family)) return;
 loaded.add(family);

 const link = document.createElement('link');
 link.rel = 'stylesheet';
 link.href = `https://fonts.googleapis.com/css2?family=${family.replace(/ /g, '+')}` +
 ':wght@400;600;700;800&display=swap';
 document.head.append(link);
 });
 }

 T.on(['pairing'], render, 'change');
 T.on(['category'], populate, 'change');
 T.on(['weight'], render, 'change');
 T.on(['heading-size', 'body-size', 'line-height'], render);
 T.$('sample-heading').addEventListener('input', debounce(render, 150));

 T.$('random').addEventListener('click', () => {
 const options = [...T.$('pairing').options];
 if (!options.length) return;
 T.$('pairing').value = T.pick(options).value;
 render();
 });

 T.wireActions({
 slug: 'font-pairing-tool',
 getResult: () => T.$('css').textContent,
 filename: 'fonts.css',
 mime: 'text/css'
 });

 populate();""",
))

# ---------------------------------------------------------------
# 76. CSS Grid Generator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="css-grid-generator", name="CSS Grid Generator", icon="⚏", cat="design",
 title="CSS Grid Generator: Build Layouts and Copy the Rules",
 description="Lay out a CSS grid visually with adjustable rows, columns and gaps, then copy the generated grid-template rules and the HTML to go with them.",
 tagline="Build a CSS grid visually and copy both the CSS and the matching HTML.",
 workspace=ws(
 row(
 slider("cols", "Columns", 1, 12, 3, 1, unit=""),
 slider("rows", "Rows", 1, 12, 3, 1, unit=""),
 slider("gap", "Gap", 0, 48, 16, 2, unit="px"),
 ),
 row(
 select("col-unit", "Column sizing", [
 ("1fr", "Equal, 1fr each"),
 ("auto", "Auto, fit content"),
 ("minmax", "Responsive, minmax(200px, 1fr)"),
 ("mixed", "Mixed, sidebar + content"),
 ], selected="1fr"),
 select("row-unit", "Row sizing", [
 ("auto", "Auto, fit content"),
 ("1fr", "Equal, 1fr each"),
 ("minmax", "Minimum height, minmax(100px, auto)"),
 ], selected="auto"),
 switch("areas", "Use named grid areas", False),
 ),
 status_line("status", "Adjust the grid."),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Preview</span><span class="field__hint">Click a cell to toggle its span</span></span>
 <div id="preview" style="padding:var(--space-4);background:var(--bg-surface);border:1px solid var(--border-color);border-radius:var(--radius-md);min-height:220px"></div>
 </div>"""),
 output("css", "CSS", None, "The CSS will appear here."),
 output("html-out", "HTML", None, "The HTML will appear here."),
 buttons(("copy", "Copy CSS", "primary"), ("copy-html", "Copy HTML"), ("reset", "Reset spans"), ("download", "Download"), ("share", "Share tool", "ghost")),
 label="CSS grid generator",
 ),
 info_block=info(
 features=[
 "1 to 12 columns and rows",
 "Four column sizing strategies including responsive minmax",
 "Click cells to make them span two columns",
 "Optional named grid areas",
 "Generates matching CSS and HTML",
 ],
 howto=[
 "Set the number of rows and columns.",
 "Choose a sizing strategy.",
 "Click any cell to toggle a two-column span.",
 "Copy the CSS and HTML into your project.",
 ],
 background_title="fr units, minmax and the auto-fit trick",
 background_paragraphs=[
 "The <code>fr</code> unit distributes leftover space after fixed-size items and gaps are accounted for. Three columns of <code>1fr</code> each are equal; <code>2fr 1fr</code> gives the first column twice the remaining space. Crucially, <code>fr</code> handles gaps correctly, which is why it is better than percentages, three columns of 33.33% plus gaps overflows the container, while three <code>1fr</code> columns never do.",
 "The single most useful grid pattern needs no media queries at all: <code>grid-template-columns: repeat(auto-fill, minmax(250px, 1fr))</code>. This fits as many columns as will hold 250 pixels each, then stretches them to fill the row, reflowing automatically as the container resizes. Using <code>auto-fit</code> instead of <code>auto-fill</code> collapses empty tracks so a single item stretches full width, which is usually what you want for a card grid.",
 "One trap worth knowing: grid items have a default <code>min-width: auto</code>, which means a track will refuse to shrink below the intrinsic width of its content. A long unbroken string or a wide image can therefore blow out your entire layout even with <code>1fr</code> columns. The fix is <code>minmax(0, 1fr)</code> rather than plain <code>1fr</code>, which lets the track shrink properly.",
 ],
 ),
 script=r""" let spans = new Set();

 function columnTemplate() {
 const cols = Number(T.$('cols').value);
 const unit = T.$('col-unit').value;

 if (unit === 'minmax') return `repeat(auto-fill, minmax(200px, 1fr))`;
 if (unit === 'auto') return `repeat(${cols}, auto)`;
 if (unit === 'mixed') {
 return cols >= 2 ? `240px repeat(${cols - 1}, minmax(0, 1fr))` : 'minmax(0, 1fr)';
 }
 return `repeat(${cols}, minmax(0, 1fr))`;
 }

 function rowTemplate() {
 const rows = Number(T.$('rows').value);
 const unit = T.$('row-unit').value;

 if (unit === 'minmax') return `repeat(${rows}, minmax(100px, auto))`;
 if (unit === '1fr') return `repeat(${rows}, minmax(0, 1fr))`;
 return `repeat(${rows}, auto)`;
 }

 function render() {
 const cols = Number(T.$('cols').value);
 const rows = Number(T.$('rows').value);
 const gap = Number(T.$('gap').value);

 T.$('cols-value').textContent = cols;
 T.$('rows-value').textContent = rows;
 T.$('gap-value').textContent = gap;

 const preview = T.$('preview');
 preview.innerHTML = '';
 preview.style.display = 'grid';
 preview.style.gridTemplateColumns = columnTemplate();
 preview.style.gridTemplateRows = rowTemplate();
 preview.style.gap = gap + 'px';

 const total = cols * rows;
 for (let i = 0; i < total; i++) {
 const spanning = spans.has(i);

 const cell = el('button', {
 className: 'chip',
 attrs: { type: 'button', 'aria-pressed': String(spanning),
 'aria-label': `Cell ${i + 1}${spanning ? ', spanning two columns' : ''}` },
 text: String(i + 1),
 style: {
 display: 'grid',
 placeItems: 'center',
 minHeight: '56px',
 background: spanning
 ? 'color-mix(in srgb, var(--accent-primary) 22%, transparent)'
 : 'var(--bg-card)',
 borderColor: spanning ? 'var(--accent-primary)' : 'var(--border-color)'
 }
 });

 if (spanning) cell.style.gridColumn = 'span 2';

 cell.addEventListener('click', () => {
 spans.has(i) ? spans.delete(i) : spans.add(i);
 render();
 });

 preview.append(cell);
 }

 generateCode(cols, rows, gap);
 T.status('status',
 `${cols} × ${rows} grid${spans.size ? `, ${spans.size} spanning cell(s)` : ''}.`, 'ok');

 if (window.Analytics) Analytics.trackToolUse('css-grid-generator');
 }

 function generateCode(cols, rows, gap) {
 const useAreas = T.$('areas').checked;

 let css = `.grid {\n display: grid;\n` +
 ` grid-template-columns: ${columnTemplate()};\n` +
 ` grid-template-rows: ${rowTemplate()};\n` +
 ` gap: ${gap}px;\n`;

 if (useAreas) {
 // Build a simple named-area map: header, sidebar, content, footer
 const names = [];
 for (let r = 0; r < rows; r++) {
 const rowNames = [];
 for (let c = 0; c < cols; c++) {
 if (r === 0) rowNames.push('header');
 else if (r === rows - 1) rowNames.push('footer');
 else rowNames.push(c === 0 ? 'sidebar' : 'content');
 }
 names.push(' "' + rowNames.join(' ') + '"');
 }
 css += ` grid-template-areas:\n${names.join('\n')};\n`;
 }

 css += '}';

 if (spans.size) {
 css += '\n\n' + [...spans].sort((a, b) => a - b)
 .map((i) => `.grid > :nth-child(${i + 1}) {\n grid-column: span 2;\n}`)
 .join('\n\n');
 }

 T.setOutput('css', css);

 const cells = Array.from({ length: cols * rows },
 (_, i) => ` <div class="cell">${i + 1}</div>`).join('\n');
 T.setOutput('html-out', `<div class="grid">\n${cells}\n</div>`);
 }

 T.on(['cols', 'rows', 'gap'], render);
 T.on(['col-unit', 'row-unit', 'areas'], render, 'change');

 T.$('reset').addEventListener('click', () => { spans.clear(); render(); });

 T.$('copy').addEventListener('click', () => copyToClipboard(T.$('css').textContent, 'CSS copied'));
 T.$('copy-html').addEventListener('click', () =>
 copyToClipboard(T.$('html-out').textContent, 'HTML copied'));

 T.$('download').addEventListener('click', () =>
 downloadFile(T.$('css').textContent, 'grid.css', 'text/css'));

 T.$('share').addEventListener('click', () => shareLink({ title: 'CSS Grid Generator | 123MiniApps' }));

 render();""",
))

# ---------------------------------------------------------------
# 77. Glassmorphism Generator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="glassmorphism-generator", name="Glassmorphism Generator", icon="🪟", cat="design",
 title="Glassmorphism Generator: Frosted Glass CSS",
 description="Generate frosted-glass CSS with adjustable blur, transparency, saturation and border tuning, previewed over a real background image.",
 tagline="Generate frosted-glass CSS, previewed over a background so you can judge it properly.",
 workspace=ws(
 row(
 slider("blur", "Blur", 0, 40, 20, 1, unit="px"),
 slider("transparency", "Transparency", 0, 100, 20, 1, unit="%"),
 slider("saturation", "Saturation", 100, 250, 160, 5, unit="%"),
 ),
 row(
 color_input("tint", "Glass tint", "#1A1F4E"),
 slider("border-alpha", "Border strength", 0, 100, 25, 1, unit="%"),
 slider("radius", "Corner radius", 0, 48, 22, 2, unit="px"),
 ),
 row(
 select("backdrop", "Preview background", [
 ("mesh", "Colourful mesh"), ("photo", "Photo-like gradient"),
 ("dark", "Dark solid"), ("light", "Light solid"),
 ], selected="mesh"),
 switch("shadow", "Add a drop shadow", True),
 switch("noise", "Add subtle noise texture", False),
 ),
 status_line("status", "Adjust the sliders."),
 HR,
 html_block(""" <div id="surface" style="padding:var(--space-12);border-radius:var(--radius-lg);display:grid;place-items:center;min-height:320px">
 <div id="glass" style="padding:var(--space-8);max-width:340px;text-align:center">
 <h3 style="margin-bottom:var(--space-2);color:#fff">Frosted glass</h3>
 <p style="color:rgba(255,255,255.85);font-size:var(--text-sm)">The blur samples whatever sits behind the element, so glass only reads as glass over something with detail.</p>
 </div>
 </div>"""),
 output("css", "CSS", None, "The CSS will appear here."),
 buttons(("copy", "Copy CSS", "primary"), ("copy-tailwind", "Copy Tailwind class"), ("download", "Download"), ("share", "Share tool", "ghost")),
 label="Glassmorphism generator",
 ),
 info_block=info(
 features=[
 "Blur, transparency and saturation control",
 "Custom tint colour and border strength",
 "Four preview backgrounds to judge against",
 "Optional drop shadow and noise texture",
 "Includes the -webkit- prefix for Safari",
 ],
 howto=[
 "Adjust the blur and transparency.",
 "Pick a background that resembles your real one.",
 "Tune the tint and border until it reads as glass.",
 "Copy the CSS, the Safari prefix is included.",
 ],
 background_title="Making glassmorphism work in practice",
 background_paragraphs=[
 "The effect depends entirely on <code>backdrop-filter</code>, which blurs whatever is painted behind the element rather than the element itself. That means it does nothing over a flat background, glass only reads as glass when there is detail behind it to distort. If your preview looks like a plain translucent box, the problem is the backdrop, not the settings.",
 "Legibility is the recurring failure. A blurred backdrop still varies in brightness, so text over glass can be perfectly readable in one scroll position and unreadable in another. The fixes are to raise the tint opacity above about 15%, add saturation to push the backdrop toward a consistent tone, and always verify contrast against the lightest and darkest points the backdrop reaches. A glass panel that passes WCAG AA over one photo may fail badly over another.",
 "There is a real performance cost too. <code>backdrop-filter</code> forces the browser to composite and blur a region on every frame, which is expensive, especially on mobile, and especially if the content behind it is animating or scrolling. Use it on a handful of elements rather than throughout an interface. Safari also still requires the <code>-webkit-</code> prefix, and Firefox only enabled it by default relatively recently, so include a solid-colour fallback inside an <code>@supports</code> query for browsers that lack it.",
 ],
 ),
 script=r""" const BACKDROPS = {
 mesh: 'radial-gradient(at 20% 25%, #00D4FF 0px, transparent 55%), ' +
 'radial-gradient(at 78% 30%, #7B61FF 0px, transparent 55%), ' +
 'radial-gradient(at 55% 85%, #F472B6 0px, transparent 55%), #0B1120',
 photo: 'linear-gradient(135deg, #667eea 0%, #764ba2 35%, #f093fb 70%, #f5576c 100%)',
 dark: '#0B1120',
 light: '#F0F4FF'
 };

 function tintRgba() {
 const rgb = T.hexToRgb(T.$('tint').value) || { r: 26, g: 31, b: 78 };
 const alpha = Number(T.$('transparency').value) / 100;
 return `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${alpha.toFixed(2)})`;
 }

 function borderRgba() {
 const alpha = Number(T.$('border-alpha').value) / 100;
 return `rgba(255, 255, 255, ${alpha.toFixed(2)})`;
 }

 function buildCSS() {
 const blur = Number(T.$('blur').value);
 const saturation = Number(T.$('saturation').value);
 const radius = Number(T.$('radius').value);

 const lines = [
 `background: ${tintRgba()};`,
 `-webkit-backdrop-filter: blur(${blur}px) saturate(${saturation}%);`,
 `backdrop-filter: blur(${blur}px) saturate(${saturation}%);`,
 `border: 1px solid ${borderRgba()};`,
 `border-radius: ${radius}px;`
 ];

 if (T.$('shadow').checked) {
 lines.push('box-shadow: 0 8px 32px rgba(0, 0, 0, 0.24);');
 }

 return lines;
 }

 function render() {
 ['blur', 'transparency', 'saturation', 'border-alpha', 'radius'].forEach((id) => {
 T.$(id + '-value').textContent = T.$(id).value;
 });

 const surface = T.$('surface');
 surface.style.background = BACKDROPS[T.$('backdrop').value];

 const glass = T.$('glass');
 const blur = Number(T.$('blur').value);
 const saturation = Number(T.$('saturation').value);

 glass.style.background = tintRgba();
 glass.style.backdropFilter = `blur(${blur}px) saturate(${saturation}%)`;
 glass.style.webkitBackdropFilter = `blur(${blur}px) saturate(${saturation}%)`;
 glass.style.border = `1px solid ${borderRgba()}`;
 glass.style.borderRadius = T.$('radius').value + 'px';
 glass.style.boxShadow = T.$('shadow').checked ? '0 8px 32px rgba(0,0,0.24)' : 'none';

 if (T.$('noise').checked) {
 // A tiny inline SVG turbulence pattern, tiled, no extra request
 const noise = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3'/%3E%3C/filter%3E%3Crect width='120' height='120' filter='url(%23n)' opacity='.06'/%3E%3C/svg%3E\")";
 glass.style.backgroundImage = noise;
 } else {
 glass.style.backgroundImage = 'none';
 }

 const lines = buildCSS();
 if (T.$('noise').checked) {
 lines.push("/* Optional noise texture, inlined so it costs no request */");
 lines.push("background-image: url(\"data:image/svg+xml...\"); /* see the copy button */");
 }

 T.setOutput('css',
 '.glass {\n ' + lines.join('\n ') + '\n}\n\n' +
 '/* Fallback for browsers without backdrop-filter */\n' +
 '@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {\n' +
 ` .glass {\n background: ${solidFallback()};\n }\n}`);

 // Warn when the effect will not be visible
 const flat = ['dark', 'light'].includes(T.$('backdrop').value);
 T.status('status',
 flat
 ? 'Over a flat background the blur has nothing to sample, glass needs detail behind it.'
 : `Blur ${blur}px at ${T.$('transparency').value}% tint opacity.`,
 flat ? 'warn' : 'ok');

 if (window.Analytics) Analytics.trackToolUse('glassmorphism-generator');
 }

 /** A solid approximation for browsers lacking backdrop-filter. */
 function solidFallback() {
 const rgb = T.hexToRgb(T.$('tint').value) || { r: 26, g: 31, b: 78 };
 const alpha = Math.min(0.95, Number(T.$('transparency').value) / 100 + 0.55);
 return `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${alpha.toFixed(2)})`;
 }

 T.on(['blur', 'transparency', 'saturation', 'border-alpha', 'radius'], render);
 T.on(['tint'], render, 'input');
 T.on(['backdrop', 'shadow', 'noise'], render, 'change');

 T.$('copy').addEventListener('click', () => copyToClipboard(T.$('css').textContent, 'CSS copied'));

 T.$('copy-tailwind').addEventListener('click', () => {
 const blur = T.$('blur').value;
 copyToClipboard(
 `backdrop-blur-[${blur}px] backdrop-saturate-[${T.$('saturation').value}%] ` +
 `bg-[${tintRgba().replace(/\s+/g, '')}] border border-[${borderRgba().replace(/\s+/g, '')}] ` +
 `rounded-[${T.$('radius').value}px]`,
 'Tailwind classes copied');
 });

 T.$('download').addEventListener('click', () =>
 downloadFile(T.$('css').textContent, 'glass.css', 'text/css'));

 T.$('share').addEventListener('click', () => shareLink({ title: 'Glassmorphism Generator | 123MiniApps' }));

 render();""",
))
