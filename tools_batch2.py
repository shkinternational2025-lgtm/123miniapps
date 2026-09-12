#!/usr/bin/env python3
# ============================================
# 123MiniApps.online, Phase 1 Batch 2
# File: tools_batch2.py
# Purpose: 5 high-search premium utilities:
#   Fancy Text Generator, JSON to CSV, Aspect Ratio
#   Calculator, Time Duration Calculator, Word Cloud Generator.
# ============================================

from toolkit import (
    tool, ws, info, row, text_input, number_input, select, switch,
    textarea, status_line, buttons, HR, html_block, readonly,
)

PAGES = []

# ---------------------------------------------------------------
# Fancy Text Generator
# ---------------------------------------------------------------
PAGES.append(tool(
    slug="fancy-text-generator", name="Fancy Text Generator", icon="✨", cat="text",
    title="Fancy Text Generator",
    description="Turn plain text into dozens of fancy Unicode font styles for bios, usernames and posts: bold, italic, script, bubble, upside down and more.",
    tagline="Turn plain text into dozens of copy-paste Unicode font styles.",
    workspace=ws(
        textarea("input", "Your text", "Type something...", rows=90, value="Fancy Text"),
        status_line("status", "Every style below updates as you type. Click one to copy it."),
        html_block(""" <div id="styles"></div>"""),
        buttons(("clear", "Clear", "ghost"), ("share", "Share tool", "ghost")),
        label="Fancy text generator",
    ),
    info_block=info(
        features=[
            "Dozens of Unicode styles from one box of text",
            "Bold, italic, script, fraktur, monospace and more",
            "Fun styles: bubble, squared, upside down, strikethrough",
            "Click any result to copy it instantly",
            "Works in bios, usernames, posts, everything runs in your browser",
        ],
        howto=[
            "Type or paste your text in the box.",
            "Scroll the styles, each one updates live.",
            "Click a style to copy it to your clipboard.",
            "Paste it into your bio, username or post.",
        ],
        background_title="How fancy text actually works",
        background_paragraphs=[
            "Fancy text is not a font in the usual sense. A font changes how normal letters are drawn; fancy text instead swaps your ordinary letters for entirely different Unicode characters that happen to look like styled versions of them. When you paste a bold-looking name into Instagram or a game, you are not sending a formatting instruction, you are sending real characters from the Mathematical Alphanumeric Symbols block and similar ranges that already look bold, italic or script.",
            "That is why fancy text survives copy and paste into places that normally strip formatting: the style is baked into the characters themselves. It also explains the occasional gap you might see, some styles do not include every letter in Unicode, so a rare character falls back to plain, and a few platforms render certain symbols differently or not at all.",
            "Because these are standard Unicode characters, they are read aloud oddly by screen readers and are not ideal for anything that needs to be searched or indexed. They are perfect for a decorative username or a one-off post, and best avoided in body text you want people, or search engines, to read normally.",
        ],
    ),
    faqs=[
        ("Is this fancy text generator free?", "Yes, with no limits, no account and no sign-up. Generate and copy as many styles as you like."),
        ("Will fancy text work on Instagram, TikTok and games?", "Yes. Because the styles are real Unicode characters rather than formatting, they paste into most bios, usernames, captions and chat boxes. A few platforms block certain symbols, so if one style does not show, try another."),
        ("Why do some letters look plain in a style?", "Some Unicode styles do not include every character, so any letter without a styled version falls back to normal. Styles like bold and monospace are the most complete."),
        ("Is my text sent anywhere?", "No. The conversion runs entirely in your browser, so nothing you type is uploaded."),
    ],
    script=r""" function mapRange(baseUpper, baseLower, baseDigit, exceptions) {
      return (ch) => {
        if (exceptions && exceptions[ch] !== undefined) return exceptions[ch];
        const c = ch.codePointAt(0);
        if (c >= 65 && c <= 90 && baseUpper) return String.fromCodePoint(baseUpper + (c - 65));
        if (c >= 97 && c <= 122 && baseLower) return String.fromCodePoint(baseLower + (c - 97));
        if (c >= 48 && c <= 57 && baseDigit) return String.fromCodePoint(baseDigit + (c - 48));
        return ch;
      };
    }
    function lookup(mapObj) { return (ch) => mapObj[ch] !== undefined ? mapObj[ch] : ch; }
    function combine(mark) { return (ch) => ch === ' ' ? ch : ch + mark; }

    const scriptEx = { B: 'ℬ', E: 'ℰ', F: 'ℱ', H: 'ℋ', I: 'ℐ', L: 'ℒ', M: 'ℳ', R: 'ℛ', e: 'ℯ', g: 'ℊ', o: 'ℴ' };
    const frakEx = { C: 'ℭ', H: 'ℌ', I: 'ℑ', R: 'ℜ', Z: 'ℨ' };
    const dsEx = { C: 'ℂ', H: 'ℍ', N: 'ℕ', P: 'ℙ', Q: 'ℚ', R: 'ℝ', Z: 'ℤ' };
    const circleDigits = { '0': '⓪', '1': '①', '2': '②', '3': '③', '4': '④', '5': '⑤', '6': '⑥', '7': '⑦', '8': '⑧', '9': '⑨' };
    const flip = { a: 'ɐ', b: 'q', c: 'ɔ', d: 'p', e: 'ǝ', f: 'ɟ', g: 'ƃ', h: 'ɥ', i: 'ᴉ', j: 'ɾ', k: 'ʞ', l: 'l', m: 'ɯ', n: 'u', o: 'o', p: 'd', q: 'b', r: 'ɹ', s: 's', t: 'ʇ', u: 'n', v: 'ʌ', w: 'ʍ', x: 'x', y: 'ʎ', z: 'z', '.': '˙', ',': "'", '?': '¿', '!': '¡', "'": ',', '(': ')', ')': '(', '&': '⅋', '_': '‾' };
    const smallcaps = { a: 'ᴀ', b: 'ʙ', c: 'ᴄ', d: 'ᴅ', e: 'ᴇ', f: 'ꜰ', g: 'ɢ', h: 'ʜ', i: 'ɪ', j: 'ᴊ', k: 'ᴋ', l: 'ʟ', m: 'ᴍ', n: 'ɴ', o: 'ᴏ', p: 'ᴘ', q: 'q', r: 'ʀ', s: 's', t: 'ᴛ', u: 'ᴜ', v: 'ᴠ', w: 'ᴡ', x: 'x', y: 'ʏ', z: 'ᴢ' };

    const STYLES = [
      ['Bold', mapRange(0x1D400, 0x1D41A, 0x1D7CE)],
      ['Italic', mapRange(0x1D434, 0x1D44E, null, { h: 'ℎ' })],
      ['Bold Italic', mapRange(0x1D468, 0x1D482, null)],
      ['Script', mapRange(0x1D49C, 0x1D4B6, null, scriptEx)],
      ['Bold Script', mapRange(0x1D4D0, 0x1D4EA, null)],
      ['Fraktur', mapRange(0x1D504, 0x1D51E, null, frakEx)],
      ['Double-struck', mapRange(0x1D538, 0x1D552, 0x1D7D8, dsEx)],
      ['Monospace', mapRange(0x1D670, 0x1D68A, 0x1D7F6)],
      ['Sans-serif', mapRange(0x1D5A0, 0x1D5BA, 0x1D7E2)],
      ['Sans Bold', mapRange(0x1D5D4, 0x1D5EE, 0x1D7EC)],
      ['Small Caps', lookup(smallcaps)],
      ['Circled', (ch) => { const c = ch.codePointAt(0); if (c >= 65 && c <= 90) return String.fromCodePoint(0x24B6 + c - 65); if (c >= 97 && c <= 122) return String.fromCodePoint(0x24D0 + c - 97); return circleDigits[ch] !== undefined ? circleDigits[ch] : ch; }],
      ['Squared', (ch) => { const u = ch.toUpperCase(); const c = u.codePointAt(0); return (c >= 65 && c <= 90) ? String.fromCodePoint(0x1F130 + c - 65) : ch; }],
      ['Fullwidth', (ch) => { const c = ch.codePointAt(0); if (c === 32) return '　'; return (c >= 33 && c <= 126) ? String.fromCodePoint(0xFF01 + c - 33) : ch; }],
      ['Upside down', lookup(flip)],
      ['Strikethrough', combine('̶')],
      ['Underline', combine('̲')],
    ];

    function styleText(text, fn, flipIt) {
      const chars = Array.from(text).map(fn);
      if (flipIt) chars.reverse();
      return chars.join('');
    }

    function render() {
      const text = T.$('input').value || '';
      const frag = document.createDocumentFragment();
      STYLES.forEach(([name, fn]) => {
        const out = styleText(text, fn, name === 'Upside down');
        const card = document.createElement('button');
        card.type = 'button';
        card.className = 'info-panel';
        card.style.cssText = 'display:block;width:100%;text-align:left;margin-bottom:var(--space-3);cursor:pointer';
        card.innerHTML = '<span class="text-sm text-muted">' + name + '</span><div style="font-size:var(--text-lg);word-break:break-word;margin-top:4px">' + (out || '&nbsp;') + '</div>';
        card.addEventListener('click', () => copyToClipboard(out, name + ' copied'));
        frag.appendChild(card);
      });
      T.$('styles').innerHTML = '';
      T.$('styles').appendChild(frag);
    }

    T.$('input').addEventListener('input', render);
    T.$('clear').addEventListener('click', () => { T.$('input').value = ''; render(); });
    T.$('share').addEventListener('click', () => shareLink({ title: 'Fancy Text Generator | 123MiniApps' }));
    render();
    if (window.Analytics) Analytics.trackToolUse('fancy-text-generator');""",
))

# ---------------------------------------------------------------
# JSON to CSV
# ---------------------------------------------------------------
PAGES.append(tool(
    slug="json-to-csv", name="JSON to CSV", icon="🔄", cat="developer",
    title="JSON to CSV",
    description="Convert a JSON array of objects into clean CSV, flattening nested fields and handling commas and quotes correctly. Download the file, all in your browser.",
    tagline="Turn a JSON array of objects into clean, spreadsheet-ready CSV.",
    workspace=ws(
        textarea("input", "JSON (array of objects)", '[{"name":"Ada","role":"Engineer"},{"name":"Alan","role":"Mathematician"}]', rows=140),
        row(
            select("delim", "Delimiter", [("comma", "Comma (,)"), ("semicolon", "Semicolon (;)"), ("tab", "Tab")], "comma"),
            select("flatten", "Nested objects", [("flatten", "Flatten with dot keys"), ("stringify", "Keep as JSON text")], "flatten"),
        ),
        status_line("status", "Paste a JSON array of objects and it converts as you type."),
        textarea("output", "CSV", "", rows=140),
        buttons(("copy", "Copy CSV", "primary"), ("download", "Download .csv", "ghost"), ("clear", "Clear", "ghost"), ("share", "Share tool", "ghost")),
        label="JSON to CSV converter",
    ),
    info_block=info(
        features=[
            "Converts a JSON array of objects to CSV",
            "Flattens nested objects into dot-notation columns",
            "Escapes commas, quotes and line breaks correctly",
            "Comma, semicolon or tab delimiter",
            "Copy or download the file, nothing is uploaded",
        ],
        howto=[
            "Paste a JSON array of objects into the top box.",
            "Choose your delimiter and how to handle nested objects.",
            "The CSV appears below, ready to copy.",
            "Download it and open in Excel, Sheets or Numbers.",
        ],
        background_title="Why the structure changes",
        background_paragraphs=[
            "JSON and CSV describe data in fundamentally different shapes, and understanding that is the key to a clean conversion. JSON is a tree: objects can nest inside objects, and arrays can hold anything. CSV is a flat grid: rows and columns, nothing deeper. Converting from one to the other therefore means projecting a tree onto a table, and the natural unit for a row is one object in a top-level array.",
            "That is why this tool expects an array of objects. Each object becomes a row, and every key that appears anywhere in the data becomes a column, so records with different fields still line up. When a value is itself an object, flattening turns it into dot-notation columns, so an address object with a city field becomes an address.city column. Arrays and awkward values can instead be kept as JSON text in a single cell if you prefer to preserve them intact.",
            "The other half of a correct converter is escaping. A CSV field that contains the delimiter, a quote or a line break must be wrapped in double quotes, and any quotes inside it doubled, or the file will break when a spreadsheet reads it. Getting this right by hand is fiddly and easy to botch, which is exactly why doing it in a tool saves you from silently corrupted exports.",
        ],
    ),
    faqs=[
        ("Is this JSON to CSV converter free?", "Yes, with no limits, no account and no sign-up."),
        ("What JSON shape does it expect?", "A top-level array of objects, where each object becomes a row. If your JSON is a single object, wrap it in square brackets to make it an array of one."),
        ("How are nested objects handled?", "By default they are flattened into dot-notation columns, so a nested address.city becomes its own column. You can instead keep nested values as JSON text in one cell."),
        ("Is my data uploaded?", "No. The conversion runs entirely in your browser, so your JSON never leaves your device."),
    ],
    script=r""" function flatten(obj, prefix, out) {
      for (const k in obj) {
        if (!Object.prototype.hasOwnProperty.call(obj, k)) continue;
        const key = prefix ? prefix + '.' + k : k;
        const v = obj[k];
        if (v && typeof v === 'object' && !Array.isArray(v)) flatten(v, key, out);
        else out[key] = v;
      }
      return out;
    }

    function toCell(v) {
      if (v === null || v === undefined) return '';
      if (typeof v === 'object') return JSON.stringify(v);
      return String(v);
    }

    function esc(cell, sep) {
      if (cell.includes(sep) || cell.includes('"') || cell.includes('\n')) {
        return '"' + cell.replace(/"/g, '""') + '"';
      }
      return cell;
    }

    function convert() {
      const raw = T.$('input').value.trim();
      if (!raw) { T.$('output').value = ''; T.status('status', 'Paste a JSON array of objects.', 'muted'); return; }
      let data;
      try { data = JSON.parse(raw); } catch (e) { T.status('status', 'Invalid JSON: ' + e.message, 'error'); return; }
      if (!Array.isArray(data)) { if (data && typeof data === 'object') data = [data]; else { T.status('status', 'JSON must be an array of objects.', 'error'); return; } }
      const sep = T.$('delim').value === 'semicolon' ? ';' : (T.$('delim').value === 'tab' ? '\t' : ',');
      const doFlatten = T.$('flatten').value === 'flatten';
      const rows = data.map((r) => (r && typeof r === 'object' && !Array.isArray(r)) ? (doFlatten ? flatten(r, '', {}) : r) : { value: r });
      const cols = [];
      rows.forEach((r) => Object.keys(r).forEach((k) => { if (!cols.includes(k)) cols.push(k); }));
      const lines = [cols.map((c) => esc(c, sep)).join(sep)];
      rows.forEach((r) => { lines.push(cols.map((c) => esc(toCell(r[c]), sep)).join(sep)); });
      T.$('output').value = lines.join('\n');
      T.status('status', rows.length + ' row(s), ' + cols.length + ' column(s).', 'ok');
    }

    T.$('input').addEventListener('input', convert);
    T.$('delim').addEventListener('change', convert);
    T.$('flatten').addEventListener('change', convert);
    T.$('copy').addEventListener('click', () => copyToClipboard(T.$('output').value, 'CSV copied'));
    T.$('download').addEventListener('click', () => {
      if (!T.$('output').value) return;
      const blob = new Blob([T.$('output').value], { type: 'text/csv' });
      const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'data.csv';
      document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(a.href);
    });
    T.$('clear').addEventListener('click', () => { T.$('input').value = ''; convert(); });
    T.$('share').addEventListener('click', () => shareLink({ title: 'JSON to CSV | 123MiniApps' }));
    convert();
    if (window.Analytics) Analytics.trackToolUse('json-to-csv');""",
))

# ---------------------------------------------------------------
# Aspect Ratio Calculator
# ---------------------------------------------------------------
PAGES.append(tool(
    slug="aspect-ratio-calculator", name="Aspect Ratio Calculator", icon="📐", cat="calculator",
    title="Aspect Ratio Calculator",
    description="Work out a new width or height that keeps the same aspect ratio, or find the ratio of any size. Presets for 16:9, 4:3, 1:1 and more, in your browser.",
    tagline="Resize without distortion: keep the aspect ratio, or find it from any size.",
    workspace=ws(
        row(
            number_input("ow", "Original width", value="1920", step="1", min=1),
            number_input("oh", "Original height", value="1080", step="1", min=1),
        ),
        html_block(""" <div class="field"><label class="field__label"><span>Common ratios</span></label>
      <div id="presets" style="display:flex;gap:8px;flex-wrap:wrap"></div></div>"""),
        HR,
        row(
            number_input("nw", "New width", value="1280", step="1", min=1),
            number_input("nh", "New height", value="", placeholder="auto", step="1", min=1),
        ),
        status_line("status", "Enter a new width to get the matching height, or the reverse."),
        html_block(""" <div class="result-grid">
      <div class="result"><span class="result__value" id="r-ratio" style="font-size:var(--text-2xl)">16:9</span><span class="result__label">Aspect ratio</span></div>
      <div class="result"><span class="result__value" id="r-decimal" style="font-size:var(--text-2xl)">1.778</span><span class="result__label">Ratio (decimal)</span></div>
    </div>"""),
        buttons(("copy", "Copy result", "primary"), ("share", "Share tool", "ghost")),
        label="Aspect ratio calculator",
    ),
    info_block=info(
        features=[
            "Find a new width or height that keeps the ratio",
            "One-click presets: 16:9, 4:3, 3:2, 1:1, 21:9 and more",
            "Shows the simplified ratio and its decimal value",
            "Works for images, video, screens and print",
            "Runs entirely in your browser",
        ],
        howto=[
            "Enter your original width and height, or pick a preset.",
            "Type the new width you want.",
            "The matching height that avoids distortion appears instantly.",
            "Or enter a new height to get the matching width.",
        ],
        background_title="What an aspect ratio really is",
        background_paragraphs=[
            "An aspect ratio is simply the relationship between width and height, written as two numbers like 16:9. It does not fix a size, only a shape: 1280 by 720, 1920 by 1080 and 3840 by 2160 are all 16:9, which is why a video scales cleanly between them. Distortion happens when you change width and height by different amounts, stretching circles into ovals and faces into funhouse mirrors. Keeping the ratio constant is what keeps everything looking right.",
            "To resize without distortion you scale both dimensions by the same factor. If a 1920 by 1080 image needs to be 1280 wide, the factor is 1280 divided by 1920, and multiplying the height by that same factor gives 720. That is the whole calculation, and doing it the other way, fixing a height and solving for width, works identically. The tool simply does the arithmetic and rounds to whole pixels.",
            "The simplified ratio comes from dividing both numbers by their greatest common divisor. 1920 and 1080 share a divisor of 120, which reduces them to 16 and 9, hence 16:9. Common shapes have names worth knowing: 16:9 is standard widescreen video, 4:3 is older screens and many photos, 1:1 is square social posts, 3:2 is classic 35mm photography, and 21:9 is ultrawide cinema.",
        ],
    ),
    faqs=[
        ("Is this aspect ratio calculator free?", "Yes, with no limits, no account and no sign-up."),
        ("How do I resize an image without stretching it?", "Keep the aspect ratio: enter the original dimensions, then type either the new width or the new height and the tool fills in the other so both scale by the same factor."),
        ("What is the 16:9 aspect ratio in pixels?", "16:9 is a shape, not a fixed size. Common 16:9 resolutions are 1280x720, 1920x1080 and 3840x2160; all share the same ratio."),
        ("Are my numbers uploaded?", "No. The calculation runs entirely in your browser."),
    ],
    script=r""" const PRESETS = [['16:9', 16, 9], ['4:3', 4, 3], ['3:2', 3, 2], ['1:1', 1, 1], ['21:9', 21, 9], ['9:16', 9, 16], ['2:1', 2, 1], ['5:4', 5, 4]];
    function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a || 1; }
    let lastEdited = 'nw';

    function updateRatio() {
      const ow = parseFloat(T.$('ow').value), oh = parseFloat(T.$('oh').value);
      if (!(ow > 0 && oh > 0)) return;
      const g = gcd(Math.round(ow), Math.round(oh));
      T.$('r-ratio').textContent = Math.round(ow / g) + ':' + Math.round(oh / g);
      T.$('r-decimal').textContent = (ow / oh).toFixed(3);
    }

    function recompute() {
      const ow = parseFloat(T.$('ow').value), oh = parseFloat(T.$('oh').value);
      if (!(ow > 0 && oh > 0)) { T.status('status', 'Enter the original width and height.', 'muted'); return; }
      updateRatio();
      if (lastEdited === 'nw') {
        const nw = parseFloat(T.$('nw').value);
        if (nw > 0) { T.$('nh').value = Math.round(nw * oh / ow); T.status('status', 'Height set to keep the ratio.', 'ok'); }
      } else {
        const nh = parseFloat(T.$('nh').value);
        if (nh > 0) { T.$('nw').value = Math.round(nh * ow / oh); T.status('status', 'Width set to keep the ratio.', 'ok'); }
      }
    }

    ['ow', 'oh'].forEach((id) => T.$(id).addEventListener('input', recompute));
    T.$('nw').addEventListener('input', () => { lastEdited = 'nw'; recompute(); });
    T.$('nh').addEventListener('input', () => { lastEdited = 'nh'; recompute(); });

    const presetWrap = T.$('presets');
    PRESETS.forEach(([label, w, h]) => {
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'btn btn--ghost btn--sm'; b.textContent = label;
      b.addEventListener('click', () => { T.$('ow').value = w * 120; T.$('oh').value = h * 120; lastEdited = 'nw'; recompute(); });
      presetWrap.appendChild(b);
    });

    T.$('copy').addEventListener('click', () => copyToClipboard(T.$('nw').value + ' x ' + T.$('nh').value + ' (' + T.$('r-ratio').textContent + ')', 'Result copied'));
    T.$('share').addEventListener('click', () => shareLink({ title: 'Aspect Ratio Calculator | 123MiniApps' }));
    recompute();
    if (window.Analytics) Analytics.trackToolUse('aspect-ratio-calculator');""",
))

# ---------------------------------------------------------------
# Time Duration Calculator
# ---------------------------------------------------------------
PAGES.append(tool(
    slug="time-duration-calculator", name="Time Duration Calculator", icon="⌛", cat="calculator",
    title="Time Duration Calculator",
    description="Find the exact time between two times, with optional dates and an overnight option. See the duration in hours and minutes and in total minutes.",
    tagline="Work out the exact duration between two times, across midnight if needed.",
    workspace=ws(
        row(
            html_block(""" <div class="field"><label class="field__label" for="start"><span>Start time</span></label><input class="input" id="start" type="time" value="09:00" step="60"></div>"""),
            html_block(""" <div class="field"><label class="field__label" for="end"><span>End time</span></label><input class="input" id="end" type="time" value="17:30" step="60"></div>"""),
        ),
        switch("overnight", "End time is on the next day (overnight)"),
        number_input("break", "Break to subtract (minutes)", value="0", step="1", min=0),
        status_line("status", "Enter a start and end time to see the duration."),
        HR,
        html_block(""" <div class="result-grid">
      <div class="result"><span class="result__value" id="r-hm" style="font-size:var(--text-3xl)">8h 30m</span><span class="result__label">Duration</span></div>
      <div class="result"><span class="result__value" id="r-dec" style="font-size:var(--text-2xl)">8.50</span><span class="result__label">Decimal hours</span></div>
      <div class="result"><span class="result__value" id="r-min" style="font-size:var(--text-2xl)">510</span><span class="result__label">Total minutes</span></div>
    </div>"""),
        buttons(("copy", "Copy result", "primary"), ("share", "Share tool", "ghost")),
        label="Time duration calculator",
    ),
    info_block=info(
        features=[
            "Exact duration between two clock times",
            "Overnight option for shifts that cross midnight",
            "Subtract an unpaid break in minutes",
            "Shows hours and minutes, decimal hours and total minutes",
            "Runs entirely in your browser",
        ],
        howto=[
            "Enter the start time and end time.",
            "Tick overnight if the end time is on the next day.",
            "Optionally subtract a break in minutes.",
            "Read the duration in whichever format you need.",
        ],
        background_title="Why time subtraction trips people up",
        background_paragraphs=[
            "Subtracting times feels like it should be as easy as subtracting numbers, but clock time is base 60, not base 10, which is exactly where mistakes creep in. From 9:45 to 10:30 is not 0.85 of an hour just because 30 minus 45 looks negative; it is 45 minutes, because you borrow a full 60-minute hour. The reliable method is to convert both times to minutes since midnight, subtract, and then convert back. 10:30 is 630 minutes, 9:45 is 585 minutes, the difference is 45 minutes.",
            "Overnight shifts add the second trap. If someone clocks in at 22:00 and out at 06:00, a plain subtraction gives a nonsensical negative sixteen hours. The fix is to recognise the end time falls on the next day and add 24 hours' worth of minutes before subtracting, giving the correct eight hours. That is what the overnight option does for you.",
            "Decimal hours matter for anyone billing or being paid by time, because payroll and invoices usually work in decimals rather than hours and minutes. Thirty minutes is 0.5 hours, fifteen is 0.25, and twenty is 0.333, so eight hours and thirty minutes is 8.5, not 8.30. Showing the duration in hours-and-minutes, decimal and total-minutes at once means you never have to convert by hand for a timesheet.",
        ],
    ),
    faqs=[
        ("Is this time duration calculator free?", "Yes, with no limits, no account and no sign-up."),
        ("How do I calculate hours for an overnight shift?", "Enter the start and end times and tick the overnight box. The tool treats the end time as the next day, so a 22:00 to 06:00 shift correctly returns 8 hours."),
        ("How do I convert minutes to decimal hours?", "Divide the minutes by 60. So 30 minutes is 0.5 hours and 45 minutes is 0.75. The calculator shows decimal hours automatically for timesheets."),
        ("Are my times uploaded?", "No. The calculation runs entirely in your browser."),
    ],
    script=r""" function toMin(v) { if (!v) return null; const [h, m] = v.split(':').map(Number); return h * 60 + m; }

    function calc() {
      let s = toMin(T.$('start').value), e = toMin(T.$('end').value);
      if (s === null || e === null) { T.status('status', 'Enter a start and end time.', 'muted'); return; }
      if (T.$('overnight').checked) e += 24 * 60;
      let diff = e - s;
      const brk = parseInt(T.$('break').value, 10) || 0;
      diff -= brk;
      if (diff < 0) { T.status('status', 'End is before start, tick overnight if it crosses midnight.', 'error'); return; }
      const h = Math.floor(diff / 60), m = diff % 60;
      T.$('r-hm').textContent = h + 'h ' + m + 'm';
      T.$('r-dec').textContent = (diff / 60).toFixed(2);
      T.$('r-min').textContent = String(diff);
      T.status('status', 'Duration calculated' + (brk ? ' (break subtracted).' : '.'), 'ok');
    }

    ['start', 'end', 'break'].forEach((id) => T.$(id).addEventListener('input', calc));
    T.$('overnight').addEventListener('change', calc);
    T.$('copy').addEventListener('click', () => copyToClipboard(T.$('r-hm').textContent + ' (' + T.$('r-dec').textContent + ' hours)', 'Result copied'));
    T.$('share').addEventListener('click', () => shareLink({ title: 'Time Duration Calculator | 123MiniApps' }));
    calc();
    if (window.Analytics) Analytics.trackToolUse('time-duration-calculator');""",
))

# ---------------------------------------------------------------
# Word Cloud Generator
# ---------------------------------------------------------------
PAGES.append(tool(
    slug="word-cloud-generator", name="Word Cloud Generator", icon="☁️", cat="content",
    title="Word Cloud Generator",
    description="Paste any text and get a word cloud where the most frequent words appear largest, with common stop words filtered out. Download it as an image, in your browser.",
    tagline="Turn any text into a word cloud sized by how often each word appears.",
    workspace=ws(
        textarea("input", "Paste your text", "Paste an article, feedback, notes or any text to see its most frequent words as a cloud.", rows=120),
        row(
            switch("stop", "Remove common words (the, and, of...)", checked=True),
            number_input("max", "Max words", value="60", step="1", min=5, max=200),
        ),
        status_line("status", "Paste text above to build the cloud."),
        HR,
        html_block(""" <div id="cloud" style="min-height:180px;padding:var(--space-5);border:1px solid var(--glass-border);border-radius:var(--radius-md);line-height:2;text-align:center"></div>"""),
        buttons(("download", "Download image", "primary"), ("recolor", "Recolor", "ghost"), ("clear", "Clear", "ghost"), ("share", "Share tool", "ghost")),
        label="Word cloud generator",
    ),
    info_block=info(
        features=[
            "Sizes each word by how often it appears",
            "Filters out common stop words so themes stand out",
            "Adjustable maximum number of words",
            "Recolour and download the cloud as a PNG image",
            "Runs entirely in your browser, nothing is uploaded",
        ],
        howto=[
            "Paste any block of text into the box.",
            "Keep stop-word removal on to surface the meaningful words.",
            "The cloud builds instantly, largest words are most frequent.",
            "Download it as an image to drop into a slide or report.",
        ],
        background_title="What a word cloud does and does not show",
        background_paragraphs=[
            "A word cloud is a frequency picture: the more often a word appears in your text, the larger it is drawn. That makes it a fast way to see what a piece of writing is mostly about, which is why they turn up in survey analysis, meeting notes, product reviews and presentation slides. Feed in a hundred pieces of customer feedback and the biggest words tell you, at a glance, what people keep mentioning.",
            "The single most important step is removing stop words. Words like the, and, of and to are the most frequent in almost any English text, so without filtering them a word cloud just shows you the plumbing of the language rather than its meaning. Stripping them out lets the words that actually carry the topic rise to the top, which is why this tool removes them by default and lets you keep them only if you specifically want to.",
            "It is worth knowing the limits, too. A word cloud shows frequency, not importance or sentiment: a word can be common without being positive, and a crucial idea mentioned once will look tiny. Two words that always appear together are shown separately, so context is lost. Treat a cloud as a quick overview that points you toward what to read more closely, not as analysis on its own.",
        ],
    ),
    faqs=[
        ("Is this word cloud generator free?", "Yes, with no limits, no account and no sign-up."),
        ("Can I download the word cloud as an image?", "Yes. Once the cloud is built, download it as a PNG to drop into a slide, document or report."),
        ("What are stop words and why remove them?", "Stop words are extremely common words like the, and and of. They dominate any frequency count, so removing them lets the meaningful words in your text stand out. You can turn the filter off if you prefer."),
        ("Is my text uploaded?", "No. The text is analysed entirely in your browser and never leaves your device."),
    ],
    script=r""" const STOP = new Set('a an and are as at be but by for from has have he her his i in is it its of on or that the their they this to was were will with you your we our us not no so if then than there here what which who when how all can just get got out up down about into over after before your are'.split(' '));
    const PALETTES = [['#6366f1', '#8b5cf6', '#3b82f6', '#06b6d4', '#10b981'], ['#f59e0b', '#ef4444', '#ec4899', '#8b5cf6', '#f97316'], ['#14b8a6', '#0ea5e9', '#6366f1', '#22c55e', '#eab308']];
    let palette = 0;

    function counts() {
      const text = T.$('input').value.toLowerCase();
      const words = text.match(/[a-z0-9']+/g) || [];
      const useStop = T.$('stop').checked;
      const freq = {};
      words.forEach((w) => { if (w.length < 2) return; if (useStop && STOP.has(w)) return; freq[w] = (freq[w] || 0) + 1; });
      const max = parseInt(T.$('max').value, 10) || 60;
      return Object.entries(freq).sort((a, b) => b[1] - a[1]).slice(0, max);
    }

    function build() {
      const list = counts();
      if (!list.length) { T.$('cloud').innerHTML = '<span class="text-muted">No words yet, paste some text.</span>'; T.status('status', 'Paste text above to build the cloud.', 'muted'); return; }
      const hi = list[0][1], lo = list[list.length - 1][1];
      const colors = PALETTES[palette % PALETTES.length];
      T.$('cloud').innerHTML = list.map(([w, n], i) => {
        const size = 0.9 + (hi === lo ? 1 : (n - lo) / (hi - lo)) * 2.4;
        const c = colors[i % colors.length];
        return '<span style="font-size:' + size.toFixed(2) + 'rem;color:' + c + ';font-weight:700;margin:0 8px;display:inline-block">' + w + '</span>';
      }).join('');
      T.status('status', list.length + ' words shown, largest is most frequent.', 'ok');
    }

    function download() {
      const list = counts();
      if (!list.length) return;
      const W = 1200, H = 630;
      const cv = document.createElement('canvas'); cv.width = W; cv.height = H;
      const ctx = cv.getContext('2d');
      ctx.fillStyle = '#0B1120'; ctx.fillRect(0, 0, W, H);
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      const hi = list[0][1], lo = list[list.length - 1][1];
      const colors = PALETTES[palette % PALETTES.length];
      let x = 40, y = 90;
      list.forEach(([w, n], i) => {
        const size = 16 + (hi === lo ? 1 : (n - lo) / (hi - lo)) * 60;
        ctx.font = '700 ' + size + 'px Inter, sans-serif';
        ctx.fillStyle = colors[i % colors.length];
        const width = ctx.measureText(w).width + 24;
        if (x + width > W - 40) { x = 40; y += 80; }
        if (y > H - 40) return;
        ctx.fillText(w, x + width / 2, y);
        x += width;
      });
      const a = document.createElement('a'); a.href = cv.toDataURL('image/png'); a.download = 'word-cloud.png';
      document.body.appendChild(a); a.click(); a.remove();
    }

    T.$('input').addEventListener('input', build);
    T.$('stop').addEventListener('change', build);
    T.$('max').addEventListener('input', build);
    T.$('recolor').addEventListener('click', () => { palette++; build(); });
    T.$('download').addEventListener('click', download);
    T.$('clear').addEventListener('click', () => { T.$('input').value = ''; build(); });
    T.$('share').addEventListener('click', () => shareLink({ title: 'Word Cloud Generator | 123MiniApps' }));
    build();
    if (window.Analytics) Analytics.trackToolUse('word-cloud-generator');""",
))
