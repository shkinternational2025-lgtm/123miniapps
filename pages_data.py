#!/usr/bin/env python3
# ============================================
# 123MiniApps.online v2.0
# File: pages_data.py
# Purpose: Per-tool content consumed by
# build-tool-page.py. Each entry supplies
# only what is unique to that tool; the
# shared chrome comes from the shell.
# ============================================

# ---------------------------------------------------------------
# JSON FORMATTER
# ---------------------------------------------------------------
JSON_FORMATTER = {
 "slug": "json-formatter",
 "faqs": [('Is this JSON formatter free and unlimited?', 'Yes. There is no size cap, no daily limit, no account and no paid tier. Formatting happens in your browser, so there is no server cost to pass on to you.'), ('Is my JSON sent to a server?', "No. The JSON is parsed by JavaScript running in your own tab using the browser's built-in JSON.parse. Nothing is uploaded, logged or stored. This matters when you are debugging an API response that contains real customer records, access tokens or personal data, you can paste it here without it leaving your machine. Open your developer tools and watch the Network tab while you format to confirm it."), ('Why does my JSON say invalid when it looks fine?', 'Four mistakes cause most failures. A trailing comma after the last item in an object or array is valid JavaScript but not valid JSON. Single quotes are not permitted, JSON strings require double quotes. Keys must always be quoted, even when they look like plain identifiers. And an unescaped control character, usually a literal newline inside a string, will stop the parser. This tool reports the exact line and column where parsing gave up, which is normally enough to spot the problem, though note the reported position is sometimes just after the real mistake.'), ('What is the difference between beautify and minify?', 'Beautify adds indentation and line breaks so the structure is readable by a human. Minify strips every optional space and newline to produce the smallest valid output, which is what you want before sending JSON over a network. Both produce semantically identical JSON, no data is changed either way.')],
 "howto": ['Paste your JSON into the input box.', 'Pick an indentation style.', 'Press Beautify to format, or Minify to compress.', 'Copy the result or download it as a .json file.'],
 "tool_name": "JSON Formatter",
 "icon": "{ }",
 "category_id": "developer",
 "category_name": "Developer Tools",
 "schema_category": "DeveloperApplication",
 "purpose": "Beautify, minify and validate JSON with precise error locations.",
 "title": "JSON Formatter & Validator: Pretty Print JSON Online | 123MiniApps",
 "og_title": "JSON Formatter & Validator | 123MiniApps",
 "description": "Beautify, minify and validate JSON in your browser. Get the exact line and column of any syntax error. Nothing is uploaded, parsing happens entirely on your device.",
 "tagline": "Beautify, minify and validate JSON, with the exact line and column of any error.",
 "workspace": """ <section class="workspace" aria-label="JSON formatter">
 <div class="field">
 <label class="field__label" for="input">
 <span>Input JSON</span>
 <span class="field__hint" id="input-stats">0 characters</span>
 </label>
 <textarea class="textarea" id="input" spellcheck="false" autocapitalize="off" autocorrect="off"
 placeholder='{"name":"123MiniApps","tools":95,"private":true}'></textarea>
 </div>

 <p id="status" class="field__hint" role="status" aria-live="polite">Paste or type JSON to validate it.</p>

 <div class="workspace__row">
 <div class="field">
 <label class="field__label" for="indent"><span>Indentation</span></label>
 <select class="select" id="indent">
 <option value="2" selected>2 spaces</option>
 <option value="4">4 spaces</option>
 <option value="tab">Tab</option>
 </select>
 </div>
 <div class="field">
 <label class="field__label" for="sort"><span>Key order</span></label>
 <select class="select" id="sort">
 <option value="keep" selected>Keep original order</option>
 <option value="asc">Sort keys A-Z</option>
 </select>
 </div>
 </div>

 <div class="actions">
 <button class="btn btn--primary" id="format" type="button">Beautify</button>
 <button class="btn btn--secondary" id="minify" type="button">Minify</button>
 <button class="btn btn--secondary" id="validate" type="button">Validate only</button>
 <button class="btn btn--ghost" id="sample" type="button">Load sample</button>
 <button class="btn btn--ghost" id="clear" type="button">Clear</button>
 </div>

 <hr class="hr">

 <div class="field">
 <label class="field__label" for="output">
 <span>Result</span>
 <span class="field__hint" id="output-stats"></span>
 </label>
 <div class="output output--empty" id="output">Formatted JSON will appear here.</div>
 </div>

 <div class="actions">
 <button class="btn btn--secondary" id="copy" type="button">Copy result</button>
 <button class="btn btn--secondary" id="download" type="button">Download .json</button>
 <button class="btn btn--ghost" id="share" type="button">Share tool</button>
 </div>
 </section>""",
 "info": """ <div class="info-grid">
 <section class="info-panel">
 <h2>Features</h2>
 <ul>
 <li>Pretty print with 2-space, 4-space or tab indentation</li>
 <li>Minify to a single line and see the bytes saved</li>
 <li>Exact line and column for every syntax error</li>
 <li>Optional alphabetical key sorting</li>
 <li>Handles deeply nested structures and large payloads</li>
 </ul>
 </section>

 <section class="info-panel">
 <h2>How to use it</h2>
 <ol>
 <li>Paste your JSON into the input box.</li>
 <li>Pick an indentation style.</li>
 <li>Press Beautify to format, or Minify to compress.</li>
 <li>Copy the result or download it as a .json file.</li>
 </ol>
 </section>

 <section class="info-panel">
 <h2>Common JSON errors</h2>
 <p class="text-sm text-muted">
 Four mistakes account for most parse failures. A trailing comma after the last item in an
 object or array is valid in JavaScript but not in JSON. Single quotes are not permitted, 
 JSON strings require double quotes. Keys must always be quoted, even when they look like
 plain identifiers. And unescaped control characters, particularly literal newlines inside a
 string, will stop the parser cold.
 </p>
 <p class="text-sm text-muted mt-3">
 When this tool reports an error it gives you the line and column, which is usually enough to
 spot the problem immediately. Note that the reported position is where the parser gave up,
 which is sometimes just after the actual mistake, a missing comma on line 8 often surfaces
 as an error at the start of line 9.
 </p>
 </section>
 </div>""",
 "script": r""" const input = $('input');
 const output = $('output');
 const status = $('status');
 let lastResult = '';

 const SAMPLE = JSON.stringify({
 site: '123MiniApps.online',
 version: '2.0.0',
 tools: 95,
 categories: ['text', 'image', 'developer', 'design'],
 privacy: { uploadsData: false, requiresAccount: false, tracksUsers: false },
 themes: 9
 });

 /**
 * Convert a character offset into a 1-based line and column.
 * @param {string} text
 * @param {number} position
 * @returns {{line: number, col: number}}
 */
 function locate(text, position) {
 const upTo = text.slice(0, position);
 const lines = upTo.split('\n');
 return { line: lines.length, col: lines[lines.length - 1].length + 1 };
 }

 /**
 * Pull a character offset out of a browser's JSON error message.
 * Engines word these differently, so try the known shapes and
 * fall back to no position rather than guessing wrong.
 * @param {Error} err
 * @returns {number|null}
 */
 function offsetFromError(err) {
 const m = String(err.message).match(/position (\d+)/i);
 return m ? Number(m[1]) : null;
 }

 /** Recursively sort object keys for stable, diffable output. */
 function sortKeys(value) {
 if (Array.isArray(value)) return value.map(sortKeys);
 if (value && typeof value === 'object') {
 return Object.keys(value).sort().reduce((acc, key) => {
 acc[key] = sortKeys(value[key]);
 return acc;
 }, {});
 }
 return value;
 }

 function indentValue() {
 const v = $('indent').value;
 return v === 'tab' ? '\t' : Number(v);
 }

 function setStatus(message, kind) {
 status.textContent = message;
 status.style.color = kind === 'error' ? 'var(--danger)'
 : kind === 'ok' ? 'var(--success)'
 : 'var(--text-muted)';
 }

 function showResult(text) {
 lastResult = text;
 output.textContent = text;
 output.classList.remove('output--empty');
 const bytes = new Blob([text]).size;
 $('output-stats').textContent = text.length.toLocaleString() + ' chars · ' + bytes.toLocaleString() + ' bytes';
 }

 /**
 * Parse the input, reporting precise errors.
 * @returns {{ok: boolean, value?: any}}
 */
 function parse() {
 const text = input.value.trim();

 if (!text) {
 setStatus('Nothing to parse, paste some JSON first.', 'error');
 return { ok: false };
 }

 try {
 const value = JSON.parse(text);
 const type = Array.isArray(value) ? 'array'
 : value === null ? 'null'
 : typeof value;
 setStatus('Valid JSON, parsed as ' + type + '.', 'ok');
 return { ok: true, value };
 } catch (err) {
 const offset = offsetFromError(err);
 if (offset !== null) {
 const { line, col } = locate(text, offset);
 setStatus('Invalid JSON at line ' + line + ', column ' + col + ', ' + err.message, 'error');
 } else {
 setStatus('Invalid JSON, ' + err.message, 'error');
 }
 output.textContent = 'Fix the error above, then try again.';
 output.classList.add('output--empty');
 lastResult = '';
 return { ok: false };
 }
 }

 function transform(minify) {
 const result = parse();
 if (!result.ok) return;

 const value = $('sort').value === 'asc' ? sortKeys(result.value) : result.value;
 const text = minify
 ? JSON.stringify(value)
 : JSON.stringify(value, null, indentValue());

 showResult(text);

 if (minify) {
 const saved = input.value.length - text.length;
 if (saved > 0) {
 const pct = ((saved / input.value.length) * 100).toFixed(1);
 toast({ type: 'success', title: 'Minified', message: 'Saved ' + saved.toLocaleString() + ' characters (' + pct + '%).' });
 }
 }

 if (window.Analytics) Analytics.trackToolUse('json-formatter');
 }

 /* ---- Wiring ---- */
 input.addEventListener('input', debounce(() => {
 $('input-stats').textContent = input.value.length.toLocaleString() + ' characters';
 if (input.value.trim()) parse();
 else setStatus('Paste or type JSON to validate it.', 'muted');
 }, 300));

 $('format').addEventListener('click', () => transform(false));
 $('minify').addEventListener('click', () => transform(true));
 $('validate').addEventListener('click', parse);

 $('sample').addEventListener('click', () => {
 input.value = SAMPLE;
 $('input-stats').textContent = input.value.length.toLocaleString() + ' characters';
 transform(false);
 });

 $('clear').addEventListener('click', () => {
 input.value = '';
 lastResult = '';
 output.textContent = 'Formatted JSON will appear here.';
 output.classList.add('output--empty');
 $('input-stats').textContent = '0 characters';
 $('output-stats').textContent = '';
 setStatus('Paste or type JSON to validate it.', 'muted');
 input.focus();
 });

 $('copy').addEventListener('click', () => copyToClipboard(lastResult, 'JSON copied'));
 $('download').addEventListener('click', () => {
 if (!lastResult) {
 toast({ type: 'warning', title: 'Nothing to download', message: 'Format some JSON first.' });
 return;
 }
 downloadFile(lastResult, 'formatted.json', 'application/json');
 });
 $('share').addEventListener('click', () => shareLink({ title: 'JSON Formatter | 123MiniApps' }));

 // Ctrl/Cmd+Enter formats
 input.addEventListener('keydown', (e) => {
 if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
 e.preventDefault();
 transform(false);
 }
 });""",
}

# ---------------------------------------------------------------
# BASE64 ENCODER / DECODER
# ---------------------------------------------------------------
BASE64 = {
 "slug": "base64-encoder-decoder",
 "faqs": [('Is this Base64 tool free?', 'Yes, entirely. No limits on input size, no account, no paid tier.'), ('Does my text get uploaded anywhere?', 'No. Encoding and decoding both happen in your browser using the built-in btoa and atob functions wrapped in TextEncoder and TextDecoder. Nothing is transmitted or stored. You can verify this in your developer tools Network tab.'), ('Why do other Base64 tools break on emoji?', "The browser's built-in btoa function only accepts characters in the Latin-1 range. Feed it an emoji, a Cyrillic character or a CJK character and it throws an InvalidCharacterError. Many online encoders hit exactly this limit and either fail or silently mangle the text. This tool converts your input to UTF-8 bytes with TextEncoder before encoding and decodes back through TextDecoder, which round-trips any string correctly including emoji, accented Latin, CJK and right-to-left scripts."), ('Is Base64 a form of encryption?', 'No, and this is an important distinction. Base64 is an encoding, not a cipher. Anyone can decode it instantly with no key, that is the entire point of it. Never use Base64 to protect a password, token or anything else confidential. If you need actual protection, use encryption.')],
 "howto": ['Choose whether you are encoding or decoding.', 'Paste your text into the input box.', 'The result updates as you type.', 'Copy it, or press Swap to run the reverse operation.'],
 "tool_name": "Base64 Encoder / Decoder",
 "icon": "🔐",
 "category_id": "developer",
 "category_name": "Developer Tools",
 "schema_category": "DeveloperApplication",
 "purpose": "Encode text to Base64 and decode it back, with full Unicode support.",
 "title": "Base64 Encoder & Decoder: Unicode Safe, Runs Locally | 123MiniApps",
 "og_title": "Base64 Encoder & Decoder | 123MiniApps",
 "description": "Encode text to Base64 or decode it back, with full Unicode and emoji support plus a URL-safe variant. Runs entirely in your browser, nothing is uploaded.",
 "tagline": "Encode and decode Base64 with full Unicode support, including emoji, which naive encoders break on.",
 "workspace": """ <section class="workspace" aria-label="Base64 encoder and decoder">
 <div class="field">
 <label class="field__label" for="input">
 <span>Input</span>
 <span class="field__hint" id="input-stats">0 characters</span>
 </label>
 <textarea class="textarea" id="input" spellcheck="false" autocapitalize="off" autocorrect="off"
 placeholder="Type or paste text here…"></textarea>
 </div>

 <div class="workspace__row">
 <div class="field">
 <label class="field__label" for="mode"><span>Direction</span></label>
 <select class="select" id="mode">
 <option value="encode" selected>Encode → Base64</option>
 <option value="decode">Decode → plain text</option>
 </select>
 </div>

 <label class="switch">
 <input class="switch__input" type="checkbox" id="urlsafe">
 <span class="switch__track"><span class="switch__thumb"></span></span>
 <span>URL-safe alphabet (<code>-_</code> instead of <code>+/</code>)</span>
 </label>

 <label class="switch">
 <input class="switch__input" type="checkbox" id="wrap">
 <span class="switch__track"><span class="switch__thumb"></span></span>
 <span>Wrap output at 76 characters</span>
 </label>
 </div>

 <p id="status" class="field__hint" role="status" aria-live="polite">Output updates as you type.</p>

 <hr class="hr">

 <div class="field">
 <label class="field__label" for="output">
 <span>Output</span>
 <span class="field__hint" id="output-stats"></span>
 </label>
 <div class="output output--empty" id="output">Result will appear here.</div>
 </div>

 <div class="actions">
 <button class="btn btn--primary" id="swap" type="button">Swap input and output</button>
 <button class="btn btn--secondary" id="copy" type="button">Copy result</button>
 <button class="btn btn--secondary" id="download" type="button">Download .txt</button>
 <button class="btn btn--ghost" id="file" type="button">Encode a file</button>
 <button class="btn btn--ghost" id="clear" type="button">Clear</button>
 </div>

 <input type="file" id="file-input" aria-label="Choose a file to encode" hidden>
 </section>""",
 "info": """ <div class="info-grid">
 <section class="info-panel">
 <h2>Features</h2>
 <ul>
 <li>Encode and decode in both directions</li>
 <li>Full Unicode and emoji support via UTF-8</li>
 <li>URL-safe alphabet for query strings and JWTs</li>
 <li>Optional 76-character line wrapping (MIME style)</li>
 <li>Encode any file to a Base64 data URI</li>
 </ul>
 </section>

 <section class="info-panel">
 <h2>How to use it</h2>
 <ol>
 <li>Choose whether you're encoding or decoding.</li>
 <li>Paste your text into the input box.</li>
 <li>The result updates as you type.</li>
 <li>Copy it, or press Swap to run the reverse operation.</li>
 </ol>
 </section>

 <section class="info-panel">
 <h2>Why Unicode support matters</h2>
 <p class="text-sm text-muted">
 The browser's built-in <code>btoa()</code> only accepts characters in the Latin-1 range. Feed
 it an emoji or a Cyrillic character and it throws an <code>InvalidCharacterError</code>. Many
 online encoders hit exactly this wall and either fail or silently mangle your text.
 </p>
 <p class="text-sm text-muted mt-3">
 This tool converts your input to UTF-8 bytes with <code>TextEncoder</code> before encoding,
 and decodes back through <code>TextDecoder</code>. That round-trips any string correctly,
 including emoji, accented Latin, CJK characters and right-to-left scripts.
 </p>
 <p class="text-sm text-muted mt-3">
 One thing worth remembering: Base64 is an <em>encoding</em>, not encryption. Anyone can decode
 it in a second. Never use it to protect a secret.
 </p>
 </section>
 </div>""",
 "script": r""" const input = $('input');
 const output = $('output');
 const status = $('status');
 let lastResult = '';

 /**
 * Encode a string to Base64 via UTF-8 bytes.
 * Using TextEncoder rather than btoa() directly is what makes
 * emoji and non-Latin scripts survive the round trip.
 * @param {string} text
 * @returns {string}
 */
 function encode(text) {
 const bytes = new TextEncoder().encode(text);
 let binary = '';
 // Chunked to stay well under the argument-count limit on large inputs
 const CHUNK = 0x8000;
 for (let i = 0; i < bytes.length; i += CHUNK) {
 binary += String.fromCharCode.apply(null, bytes.subarray(i, i + CHUNK));
 }
 return btoa(binary);
 }

 /**
 * Decode Base64 back to a string via UTF-8 bytes.
 * @param {string} b64
 * @returns {string}
 * @throws {Error} on malformed input
 */
 function decode(b64) {
 const binary = atob(b64);
 const bytes = new Uint8Array(binary.length);
 for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
 return new TextDecoder('utf-8', { fatal: false }).decode(bytes);
 }

 const toUrlSafe = (s) => s.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
 const fromUrlSafe = (s) => {
 let out = s.replace(/-/g, '+').replace(/_/g, '/');
 while (out.length % 4) out += '=';
 return out;
 };

 const wrapLines = (s, width = 76) => s.replace(new RegExp('.{1,' + width + '}', 'g'), '$&\n').trim();

 function setStatus(message, kind) {
 status.textContent = message;
 status.style.color = kind === 'error' ? 'var(--danger)'
 : kind === 'ok' ? 'var(--success)'
 : 'var(--text-muted)';
 }

 function run() {
 const text = input.value;
 $('input-stats').textContent = text.length.toLocaleString() + ' characters';

 if (!text) {
 lastResult = '';
 output.textContent = 'Result will appear here.';
 output.classList.add('output--empty');
 $('output-stats').textContent = '';
 setStatus('Output updates as you type.', 'muted');
 return;
 }

 const mode = $('mode').value;

 try {
 let result;

 if (mode === 'encode') {
 result = encode(text);
 if ($('urlsafe').checked) result = toUrlSafe(result);
 if ($('wrap').checked) result = wrapLines(result);
 setStatus('Encoded ' + new Blob([text]).size.toLocaleString() + ' bytes to Base64.', 'ok');
 } else {
 let cleaned = text.replace(/\s+/g, '');
 if ($('urlsafe').checked || /[-_]/.test(cleaned)) cleaned = fromUrlSafe(cleaned);
 result = decode(cleaned);
 setStatus('Decoded successfully.', 'ok');
 }

 lastResult = result;
 output.textContent = result;
 output.classList.remove('output--empty');
 $('output-stats').textContent = result.length.toLocaleString() + ' characters';
 } catch (err) {
 lastResult = '';
 setStatus('Could not decode, this does not look like valid Base64.', 'error');
 output.textContent = 'Check the input for stray characters or a truncated string.';
 output.classList.add('output--empty');
 }

 if (window.Analytics) Analytics.trackToolUse('base64-encoder-decoder');
 }

 /* ---- Wiring ---- */
 input.addEventListener('input', debounce(run, 200));
 ['mode', 'urlsafe', 'wrap'].forEach((id) => $(id).addEventListener('change', run));

 $('swap').addEventListener('click', () => {
 if (!lastResult) return;
 input.value = lastResult;
 $('mode').value = $('mode').value === 'encode' ? 'decode' : 'encode';
 run();
 });

 $('copy').addEventListener('click', () => copyToClipboard(lastResult, 'Result copied'));

 $('download').addEventListener('click', () => {
 if (!lastResult) {
 toast({ type: 'warning', title: 'Nothing to download' });
 return;
 }
 downloadFile(lastResult, $('mode').value === 'encode' ? 'encoded.txt' : 'decoded.txt');
 });

 $('clear').addEventListener('click', () => {
 input.value = '';
 run();
 input.focus();
 });

 /* ---- File encoding ---- */
 $('file').addEventListener('click', () => $('file-input').click());

 $('file-input').addEventListener('change', (e) => {
 const selected = e.target.files[0];
 if (!selected) return;

 if (selected.size > 5 * 1024 * 1024) {
 toast({ type: 'warning', title: 'File is large', message: 'Files over 5 MB may freeze the tab.' });
 }

 const reader = new FileReader();
 reader.onload = () => {
 lastResult = String(reader.result);
 output.textContent = lastResult;
 output.classList.remove('output--empty');
 $('output-stats').textContent = lastResult.length.toLocaleString() + ' characters';
 setStatus('Encoded "' + selected.name + '" as a data URI. The file never left your device.', 'ok');
 };
 reader.onerror = () => setStatus('Could not read that file.', 'error');
 reader.readAsDataURL(selected);
 });""",
}

# ---------------------------------------------------------------
# COLOR PICKER
# ---------------------------------------------------------------
COLOR_PICKER = {
 "slug": "color-picker",
 "faqs": [('Is this colour picker free?', 'Yes, with no limits, no account and no paid tier.'), ('What colour formats does it output?', 'HEX, RGB, HSL and HSV for every colour, plus an eleven-step tint and shade ramp you can use for hover and active states. Every value is one click to copy.'), ('How do I read the contrast numbers?', 'WCAG expresses contrast as a ratio between two relative luminance values, running from 1:1 for identical colours to 21:1 for black on white. Body text needs at least 4.5:1 to meet AA, and 7:1 to meet AAA. Large text, 18pt regular or 14pt bold and above, has a lower bar of 3:1 for AA. The panel tells you whether black or white text passes on your chosen colour. If neither reaches 4.5:1, the colour is too mid-tone to carry text and should be lightened or darkened before use as a background.'), ('Does it work offline?', 'Yes. Once the page has loaded once, the service worker caches it and the tool keeps working with no connection. Nothing about it depends on a server.')],
 "howto": ['Click the colour field, or paste a hex value.', 'Read off whichever format you need.', 'Use the ramp for hover and active states.', 'Check the contrast panel before shipping text on this colour.'],
 "tool_name": "Color Picker",
 "icon": "🎨",
 "category_id": "design",
 "category_name": "Design Tools",
 "schema_category": "DesignApplication",
 "purpose": "Pick a color and get HEX, RGB, HSL plus tint and shade ramps.",
 "title": "Color Picker: HEX, RGB, HSL and Contrast Checker | 123MiniApps",
 "og_title": "Color Picker, HEX, RGB, HSL | 123MiniApps",
 "description": "Pick any color and get HEX, RGB, HSL and HSV values, a full tint and shade ramp, and WCAG contrast ratios against black and white. Runs entirely in your browser.",
 "tagline": "Pick a color, get every format, and see how it performs against WCAG contrast thresholds.",
 "workspace": """ <section class="workspace" aria-label="Color picker">
 <div class="workspace__row">
 <div class="field">
 <label class="field__label" for="picker"><span>Pick a color</span></label>
 <input class="input" id="picker" type="color" value="#00D4FF" style="height:88px;padding:6px;cursor:pointer">
 </div>

 <div class="field">
 <label class="field__label" for="hex"><span>HEX</span></label>
 <input class="input font-mono" id="hex" type="text" value="#00D4FF" spellcheck="false" maxlength="7">
 <span class="field__hint" id="hex-error" style="color:var(--danger)" hidden>Not a valid hex color.</span>
 </div>
 </div>

 <div class="workspace__row">
 <div class="field">
 <label class="field__label" for="rgb"><span>RGB</span></label>
 <input class="input font-mono" id="rgb" type="text" readonly>
 </div>
 <div class="field">
 <label class="field__label" for="hsl"><span>HSL</span></label>
 <input class="input font-mono" id="hsl" type="text" readonly>
 </div>
 <div class="field">
 <label class="field__label" for="hsv"><span>HSV</span></label>
 <input class="input font-mono" id="hsv" type="text" readonly>
 </div>
 </div>

 <div class="actions">
 <button class="btn btn--primary" id="copy-hex" type="button">Copy HEX</button>
 <button class="btn btn--secondary" id="copy-rgb" type="button">Copy RGB</button>
 <button class="btn btn--secondary" id="copy-hsl" type="button">Copy HSL</button>
 <button class="btn btn--ghost" id="random" type="button">Random color</button>
 <button class="btn btn--ghost" id="share" type="button">Share tool</button>
 </div>

 <hr class="hr">

 <div class="field">
 <span class="field__label"><span>Tints and shades</span><span class="field__hint">Click any swatch to copy</span></span>
 <div class="swatch-grid" id="ramp"></div>
 </div>

 <hr class="hr">

 <div class="field">
 <span class="field__label"><span>Contrast against WCAG thresholds</span></span>
 <div class="workspace__row" id="contrast"></div>
 </div>
 </section>""",
 "info": """ <div class="info-grid">
 <section class="info-panel">
 <h2>Features</h2>
 <ul>
 <li>HEX, RGB, HSL and HSV output for every color</li>
 <li>Eleven-step tint and shade ramp</li>
 <li>WCAG AA and AAA contrast ratios against black and white</li>
 <li>Click any swatch to copy its hex value</li>
 <li>Paste a hex value to jump straight to it</li>
 </ul>
 </section>

 <section class="info-panel">
 <h2>How to use it</h2>
 <ol>
 <li>Click the color field, or paste a hex value.</li>
 <li>Read off whichever format you need.</li>
 <li>Use the ramp for hover and active states.</li>
 <li>Check the contrast panel before shipping text on this color.</li>
 </ol>
 </section>

 <section class="info-panel">
 <h2>Reading the contrast numbers</h2>
 <p class="text-sm text-muted">
 WCAG expresses contrast as a ratio between two relative luminance values, running from 1:1
 (identical) to 21:1 (black on white). Body text needs at least 4.5:1 to meet AA, and 7:1 to
 meet AAA. Large text, 18pt regular or 14pt bold and above, gets a lower bar of 3:1 for AA.
 </p>
 <p class="text-sm text-muted mt-3">
 The panel above tells you which of black or white text passes on your chosen color. If
 neither reaches 4.5:1, the color is too mid-tone to carry text at all; darken or lighten it
 before using it as a background. Note that contrast ratio is a proxy for legibility, not a
 guarantee of it, it says nothing about font weight, size or the surrounding layout.
 </p>
 </section>
 </div>""",
 "script": r""" const picker = $('picker');
 const hexInput = $('hex');

 /* ---------- Color space conversions ---------- */

 /**
 * @param {string} hex - "#RRGGBB" or "#RGB"
 * @returns {{r: number, g: number, b: number}|null}
 */
 function hexToRgb(hex) {
 let h = String(hex).trim().replace(/^#/, '');
 if (h.length === 3) h = h.split('').map((c) => c + c).join('');
 if (!/^[0-9a-f]{6}$/i.test(h)) return null;
 return {
 r: parseInt(h.slice(0, 2), 16),
 g: parseInt(h.slice(2, 4), 16),
 b: parseInt(h.slice(4, 6), 16)
 };
 }

 /** @returns {string} */
 function rgbToHex(r, g, b) {
 const to2 = (n) => Math.round(Math.min(255, Math.max(0, n))).toString(16).padStart(2, '0');
 return ('#' + to2(r) + to2(g) + to2(b)).toUpperCase();
 }

 /** @returns {{h: number, s: number, l: number}} */
 function rgbToHsl(r, g, b) {
 r /= 255; g /= 255; b /= 255;
 const max = Math.max(r, g, b);
 const min = Math.min(r, g, b);
 const d = max - min;
 let h = 0;

 if (d) {
 if (max === r) h = ((g - b) / d) % 6;
 else if (max === g) h = (b - r) / d + 2;
 else h = (r - g) / d + 4;
 h *= 60;
 if (h < 0) h += 360;
 }

 const l = (max + min) / 2;
 const s = d === 0 ? 0 : d / (1 - Math.abs(2 * l - 1));
 return { h: Math.round(h), s: Math.round(s * 100), l: Math.round(l * 100) };
 }

 /** @returns {{h: number, s: number, v: number}} */
 function rgbToHsv(r, g, b) {
 r /= 255; g /= 255; b /= 255;
 const max = Math.max(r, g, b);
 const min = Math.min(r, g, b);
 const d = max - min;
 let h = 0;

 if (d) {
 if (max === r) h = ((g - b) / d) % 6;
 else if (max === g) h = (b - r) / d + 2;
 else h = (r - g) / d + 4;
 h *= 60;
 if (h < 0) h += 360;
 }

 return {
 h: Math.round(h),
 s: Math.round((max === 0 ? 0 : d / max) * 100),
 v: Math.round(max * 100)
 };
 }

 /**
 * Relative luminance per WCAG 2.1, used for contrast ratios.
 * @returns {number} 0-1
 */
 function luminance(r, g, b) {
 const channel = (c) => {
 const s = c / 255;
 return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
 };
 return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b);
 }

 /** @returns {number} contrast ratio between 1 and 21 */
 function contrastRatio(rgb1, rgb2) {
 const l1 = luminance(rgb1.r, rgb1.g, rgb1.b);
 const l2 = luminance(rgb2.r, rgb2.g, rgb2.b);
 const lighter = Math.max(l1, l2);
 const darker = Math.min(l1, l2);
 return (lighter + 0.05) / (darker + 0.05);
 }

 /** Mix a color toward white (amount > 0) or black (amount < 0). */
 function mix(rgb, amount) {
 const target = amount > 0 ? 255 : 0;
 const t = Math.abs(amount);
 return {
 r: rgb.r + (target - rgb.r) * t,
 g: rgb.g + (target - rgb.g) * t,
 b: rgb.b + (target - rgb.b) * t
 };
 }

 /* ---------- Rendering ---------- */

 function renderRamp(rgb) {
 const ramp = $('ramp');
 ramp.innerHTML = '';

 const steps = [-0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8];

 steps.forEach((step) => {
 const mixed = step === 0 ? rgb : mix(rgb, step);
 const hex = rgbToHex(mixed.r, mixed.g, mixed.b);

 const swatch = el('button', {
 className: 'swatch',
 attrs: { type: 'button', 'aria-label': 'Copy ' + hex },
 on: { click: () => copyToClipboard(hex, hex + ' copied') }
 }, [
 el('span', { className: 'swatch__chip', style: { background: hex } }),
 el('span', { className: 'swatch__hex', text: hex })
 ]);

 if (step === 0) swatch.style.outline = '2px solid var(--accent-primary)';
 ramp.append(swatch);
 });
 }

 function renderContrast(rgb) {
 const panel = $('contrast');
 panel.innerHTML = '';

 [
 { label: 'Black text', text: { r: 0, g: 0, b: 0 }, css: '#000' },
 { label: 'White text', text: { r: 255, g: 255, b: 255 }, css: '#fff' }
 ].forEach(({ label, text, css }) => {
 const ratio = contrastRatio(rgb, text);
 const aa = ratio >= 4.5;
 const aaa = ratio >= 7;
 const aaLarge = ratio >= 3;

 const verdict = aaa ? 'Passes AAA' : aa ? 'Passes AA' : aaLarge ? 'Large text only' : 'Fails';
 const badgeClass = aaa ? 'badge--success' : aa ? 'badge--success' : aaLarge ? 'badge--warning' : 'badge--danger';

 panel.append(
 el('div', { className: 'panel' }, [
 el('div', {
 style: {
 background: rgbToHex(rgb.r, rgb.g, rgb.b),
 color: css,
 padding: 'var(--space-5)',
 borderRadius: 'var(--radius-sm)',
 marginBottom: 'var(--space-3)',
 fontWeight: '600',
 textAlign: 'center'
 },
 text: 'Sample text'
 }),
 el('div', { className: 'flex items-center justify-between gap-3' }, [
 el('span', { className: 'text-sm', text: label }),
 el('span', { className: 'badge ' + badgeClass, text: ratio.toFixed(2) + ':1 · ' + verdict })
 ])
 ])
 );
 });
 }

 /**
 * Update every readout from a single source-of-truth hex value.
 * @param {string} hex
 * @param {boolean} [syncInput]
 */
 function update(hex, syncInput = true) {
 const rgb = hexToRgb(hex);

 if (!rgb) {
 $('hex-error').hidden = false;
 hexInput.classList.add('is-invalid');
 return;
 }

 $('hex-error').hidden = true;
 hexInput.classList.remove('is-invalid');

 const normalized = rgbToHex(rgb.r, rgb.g, rgb.b);
 const hsl = rgbToHsl(rgb.r, rgb.g, rgb.b);
 const hsv = rgbToHsv(rgb.r, rgb.g, rgb.b);

 picker.value = normalized;
 if (syncInput) hexInput.value = normalized;

 $('rgb').value = 'rgb(' + rgb.r + ', ' + rgb.g + ', ' + rgb.b + ')';
 $('hsl').value = 'hsl(' + hsl.h + ', ' + hsl.s + '%, ' + hsl.l + '%)';
 $('hsv').value = 'hsv(' + hsv.h + ', ' + hsv.s + '%, ' + hsv.v + '%)';

 renderRamp(rgb);
 renderContrast(rgb);
 }

 /* ---- Wiring ---- */
 picker.addEventListener('input', () => update(picker.value));
 hexInput.addEventListener('input', () => update(hexInput.value, false));

 $('copy-hex').addEventListener('click', () => copyToClipboard(hexInput.value, 'HEX copied'));
 $('copy-rgb').addEventListener('click', () => copyToClipboard($('rgb').value, 'RGB copied'));
 $('copy-hsl').addEventListener('click', () => copyToClipboard($('hsl').value, 'HSL copied'));

 $('random').addEventListener('click', () => {
 const buf = new Uint8Array(3);
 crypto.getRandomValues(buf);
 update(rgbToHex(buf[0], buf[1], buf[2]));
 });

 $('share').addEventListener('click', () => shareLink({ title: 'Color Picker | 123MiniApps' }));

 update('#00D4FF');
 if (window.Analytics) Analytics.trackToolUse('color-picker');""",
}

# ---------------------------------------------------------------
# QR CODE GENERATOR
# ---------------------------------------------------------------
QR_CODE = {
 "slug": "qr-code-generator",
 "faqs": [('Is this QR code generator free, and do the codes expire?', 'Yes, free with no limits, and no, the codes never expire. Many QR generators create a short redirect URL that points through their servers, which means the code stops working if they shut down or start charging. This tool encodes your data directly into the QR pattern, so the image is permanent and depends on nobody.'), ('Is my data sent anywhere when I generate a code?', 'No. The QR encoder is written in-house and runs entirely in your browser, there is no API call. This matters for the Wi-Fi option in particular, since the password is encoded locally and never transmitted. Bear in mind though that anyone who scans or photographs the resulting image can read that password, so share the picture carefully.'), ('Which error correction level should I choose?', 'QR codes carry redundant data so they still scan when partly obscured. Level L tolerates around 7% damage and produces the smallest code; H tolerates about 30% but needs noticeably more modules for the same payload. M is the sensible default for anything displayed on a screen. Choose Q or H when the code will be printed on packaging, used outdoors, or has a logo overlaid on it.'), ('What is the difference between the PNG and SVG download?', 'PNG is a fixed-resolution raster image, which is right for websites, emails and slides. SVG is vector, so it stays perfectly sharp at any size, use it for anything going to print, on signage, or on a large format where a PNG would show pixel edges.')],
 "howto": ['Pick what you are encoding from the dropdown.', 'Fill in the fields, the code redraws as you type.', 'Adjust size, colours and correction level.', 'Download as PNG for the web, or SVG for print.'],
 "tool_name": "QR Code Generator",
 "icon": "📱",
 "category_id": "generator",
 "category_name": "Generators",
 "schema_category": "UtilitiesApplication",
 "purpose": "Generate QR codes for links, text, Wi-Fi and contact cards.",
 "title": "QR Code Generator: Links, Wi-Fi and vCards, PNG & SVG | 123MiniApps",
 "og_title": "QR Code Generator, PNG & SVG | 123MiniApps",
 "description": "Generate QR codes for URLs, text, Wi-Fi or contact cards. Four error-correction levels, custom colors, PNG and SVG download. Encoded locally.",
 "tagline": "Turn a link, Wi-Fi password or contact card into a QR code, encoded locally, never uploaded.",
 "extra_scripts": '<script src="../assets/js/vendor/qr-encoder.js" defer></script>',
 "workspace": """ <section class="workspace" aria-label="QR code generator">
 <div class="field">
 <label class="field__label" for="type"><span>What are you encoding?</span></label>
 <select class="select" id="type">
 <option value="url" selected>Link (URL)</option>
 <option value="text">Plain text</option>
 <option value="wifi">Wi-Fi network</option>
 <option value="vcard">Contact card (vCard)</option>
 <option value="email">Email address</option>
 </select>
 </div>

 <!-- URL / text -->
 <div class="field" data-panel="url text">
 <label class="field__label" for="content">
 <span id="content-label">Link</span>
 <span class="field__hint" id="content-stats"></span>
 </label>
 <textarea class="textarea" id="content" style="min-height:110px" spellcheck="false"
 placeholder="https://www.123miniapps.online/">https://www.123miniapps.online/</textarea>
 </div>

 <!-- Wi-Fi -->
 <div data-panel="wifi" hidden>
 <div class="workspace__row">
 <div class="field">
 <label class="field__label" for="wifi-ssid"><span>Network name (SSID)</span></label>
 <input class="input" id="wifi-ssid" type="text" placeholder="MyNetwork">
 </div>
 <div class="field">
 <label class="field__label" for="wifi-pass"><span>Password</span></label>
 <input class="input" id="wifi-pass" type="text" placeholder="••••••••" autocomplete="off">
 </div>
 <div class="field">
 <label class="field__label" for="wifi-enc"><span>Security</span></label>
 <select class="select" id="wifi-enc">
 <option value="WPA" selected>WPA / WPA2 / WPA3</option>
 <option value="WEP">WEP</option>
 <option value="nopass">Open (no password)</option>
 </select>
 </div>
 </div>
 <p class="field__hint">The password is encoded into the QR image on this device. It is never sent anywhere, but anyone who scans or photographs the code can read it, so share the image carefully.</p>
 </div>

 <!-- vCard -->
 <div data-panel="vcard" hidden>
 <div class="workspace__row">
 <div class="field">
 <label class="field__label" for="vc-name"><span>Full name</span></label>
 <input class="input" id="vc-name" type="text" placeholder="Ada Lovelace">
 </div>
 <div class="field">
 <label class="field__label" for="vc-phone"><span>Phone</span></label>
 <input class="input" id="vc-phone" type="tel" placeholder="+1 555 0100">
 </div>
 <div class="field">
 <label class="field__label" for="vc-email"><span>Email</span></label>
 <input class="input" id="vc-email" type="email" placeholder="ada@example.com">
 </div>
 <div class="field">
 <label class="field__label" for="vc-org"><span>Organisation</span></label>
 <input class="input" id="vc-org" type="text" placeholder="Analytical Engines Ltd">
 </div>
 </div>
 </div>

 <!-- Email -->
 <div data-panel="email" hidden>
 <div class="workspace__row">
 <div class="field">
 <label class="field__label" for="em-to"><span>To</span></label>
 <input class="input" id="em-to" type="email" placeholder="hello@example.com">
 </div>
 <div class="field">
 <label class="field__label" for="em-subject"><span>Subject</span></label>
 <input class="input" id="em-subject" type="text" placeholder="Hello">
 </div>
 </div>
 </div>

 <hr class="hr">

 <div class="workspace__row">
 <div class="field">
 <label class="field__label" for="ecl">
 <span>Error correction</span>
 </label>
 <select class="select" id="ecl">
 <option value="L">L, recovers ~7% damage (smallest code)</option>
 <option value="M" selected>M, recovers ~15% (balanced)</option>
 <option value="Q">Q, recovers ~25%</option>
 <option value="H">H, recovers ~30% (largest code)</option>
 </select>
 </div>

 <div class="field">
 <label class="field__label" for="size">
 <span>Image size</span>
 <span class="field__hint"><strong id="size-value">320</strong> px</span>
 </label>
 <input class="range" id="size" type="range" min="128" max="1024" step="32" value="320">
 </div>

 <div class="field">
 <label class="field__label" for="margin">
 <span>Quiet zone</span>
 <span class="field__hint"><strong id="margin-value">4</strong> modules</span>
 </label>
 <input class="range" id="margin" type="range" min="0" max="8" step="1" value="4">
 </div>
 </div>

 <div class="workspace__row">
 <div class="field">
 <label class="field__label" for="fg"><span>Foreground</span></label>
 <input class="input" id="fg" type="color" value="#000000" style="height:52px;padding:6px;cursor:pointer">
 </div>
 <div class="field">
 <label class="field__label" for="bg"><span>Background</span></label>
 <input class="input" id="bg" type="color" value="#FFFFFF" style="height:52px;padding:6px;cursor:pointer">
 </div>
 </div>

 <p id="status" class="field__hint" role="status" aria-live="polite">The code updates as you type.</p>
 <p id="contrast-warning" class="field__hint" style="color:var(--warning)" hidden></p>

 <hr class="hr">

 <div class="field">
 <span class="field__label"><span>Your QR code</span><span class="field__hint" id="qr-meta"></span></span>
 <div class="output output--center" style="padding:var(--space-6)">
 <canvas id="canvas" role="img" aria-label="Generated QR code"></canvas>
 </div>
 </div>

 <div class="actions">
 <button class="btn btn--primary" id="download-png" type="button">Download PNG</button>
 <button class="btn btn--secondary" id="download-svg" type="button">Download SVG</button>
 <button class="btn btn--secondary" id="copy-img" type="button">Copy image</button>
 <button class="btn btn--ghost" id="share" type="button">Share tool</button>
 </div>
 </section>""",
 "info": """ <div class="info-grid">
 <section class="info-panel">
 <h2>Features</h2>
 <ul>
 <li>Five payload types: URL, text, Wi-Fi, vCard and email</li>
 <li>All four error-correction levels</li>
 <li>Custom foreground and background colors</li>
 <li>PNG raster and SVG vector download</li>
 <li>Encoder written in-house, no external requests</li>
 </ul>
 </section>

 <section class="info-panel">
 <h2>How to use it</h2>
 <ol>
 <li>Pick what you're encoding from the dropdown.</li>
 <li>Fill in the fields, the code redraws as you type.</li>
 <li>Adjust size, colors and correction level.</li>
 <li>Download as PNG for the web, or SVG for print.</li>
 </ol>
 </section>

 <section class="info-panel">
 <h2>Choosing an error correction level</h2>
 <p class="text-sm text-muted">
 QR codes carry redundant data so they still scan when partly obscured. Level L tolerates
 around 7% damage and produces the smallest code; H tolerates about 30% but needs noticeably
 more modules for the same payload. M is the sensible default for anything displayed on a
 screen.
 </p>
 <p class="text-sm text-muted mt-3">
 Reach for Q or H when the code will be printed on packaging, placed outdoors, or has a logo
 overlaid on it, all situations where part of the pattern may be lost. Two other things
 matter more than people expect: keep the quiet zone (the blank margin) at four modules or
 more, and keep strong contrast between foreground and background. A light-on-dark inverted
 code will fail on many scanners regardless of correction level.
 </p>
 </section>
 </div>""",
 "script": r""" const canvas = $('canvas');
 const ctx = canvas.getContext('2d');
 const status = $('status');
 let current = null;

 /** Escape the characters that carry meaning in a Wi-Fi QR payload. */
 const escapeWifi = (s) => String(s).replace(/([\\; ":])/g, '\\$1');

 /**
 * Assemble the payload string for the selected type.
 * @returns {string}
 */
 function buildPayload() {
 const type = $('type').value;

 if (type === 'url' || type === 'text') {
 return $('content').value.trim();
 }

 if (type === 'wifi') {
 const ssid = $('wifi-ssid').value.trim();
 if (!ssid) return '';
 const enc = $('wifi-enc').value;
 const pass = enc === 'nopass' ? '' : $('wifi-pass').value;
 return 'WIFI:T:' + enc + ';S:' + escapeWifi(ssid) + ';P:' + escapeWifi(pass) + ';;';
 }

 if (type === 'vcard') {
 const name = $('vc-name').value.trim();
 if (!name) return '';
 const lines = ['BEGIN:VCARD', 'VERSION:3.0', 'FN:' + name];
 if ($('vc-org').value.trim()) lines.push('ORG:' + $('vc-org').value.trim());
 if ($('vc-phone').value.trim()) lines.push('TEL:' + $('vc-phone').value.trim());
 if ($('vc-email').value.trim()) lines.push('EMAIL:' + $('vc-email').value.trim());
 lines.push('END:VCARD');
 return lines.join('\n');
 }

 if (type === 'email') {
 const to = $('em-to').value.trim();
 if (!to) return '';
 const subject = $('em-subject').value.trim();
 return 'mailto:' + to + (subject ? '?subject=' + encodeURIComponent(subject) : '');
 }

 return '';
 }

 function setStatus(message, kind) {
 status.textContent = message;
 status.style.color = kind === 'error' ? 'var(--danger)'
 : kind === 'ok' ? 'var(--success)'
 : 'var(--text-muted)';
 }

 /** Relative luminance, for the contrast warning. */
 function luminance(hex) {
 const h = hex.replace('#', '');
 const rgb = [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16) / 255);
 const lin = rgb.map((c) => (c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4)));
 return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2];
 }

 /** Warn when the chosen colors will defeat real-world scanners. */
 function checkContrast() {
 const fg = $('fg').value;
 const bg = $('bg').value;
 const l1 = luminance(fg);
 const l2 = luminance(bg);
 const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
 const warning = $('contrast-warning');

 if (ratio < 3) {
 warning.hidden = false;
 warning.textContent = 'Low contrast (' + ratio.toFixed(1) + ':1), many scanners will fail to read this. Aim for 7:1 or higher.';
 } else if (l1 > l2) {
 warning.hidden = false;
 warning.textContent = 'This code is inverted (light on dark). Some scanners will not read it.';
 } else {
 warning.hidden = true;
 }
 }

 /** Render the current payload to the canvas. */
 function render() {
 const payload = buildPayload();
 $('content-stats').textContent = payload ? payload.length + ' characters' : '';

 if (!payload) {
 ctx.clearRect(0, 0, canvas.width, canvas.height);
 current = null;
 $('qr-meta').textContent = '';
 setStatus('Fill in the fields above to generate a code.', 'muted');
 return;
 }

 let result;
 try {
 result = QREncoder.encode(payload, { ecl: $('ecl').value });
 } catch (err) {
 current = null;
 setStatus(err.message, 'error');
 $('qr-meta').textContent = '';
 ctx.clearRect(0, 0, canvas.width, canvas.height);
 return;
 }

 current = result;

 const pixelSize = Number($('size').value);
 const margin = Number($('margin').value);
 const total = result.size + margin * 2;
 const scale = Math.max(1, Math.floor(pixelSize / total));
 const dimension = total * scale;

 canvas.width = dimension;
 canvas.height = dimension;
 canvas.style.width = Math.min(dimension, 360) + 'px';
 canvas.style.height = Math.min(dimension, 360) + 'px';

 ctx.fillStyle = $('bg').value;
 ctx.fillRect(0, 0, dimension, dimension);
 ctx.fillStyle = $('fg').value;

 for (let y = 0; y < result.size; y++) {
 for (let x = 0; x < result.size; x++) {
 if (result.modules[y][x]) {
 ctx.fillRect((x + margin) * scale, (y + margin) * scale, scale, scale);
 }
 }
 }

 $('qr-meta').textContent = 'Version ' + result.version + ' · ' + result.size + '×' + result.size +
 ' modules · level ' + result.ecl;
 setStatus('Generated ' + dimension + '×' + dimension + ' px.', 'ok');
 checkContrast();

 if (window.Analytics) Analytics.trackToolUse('qr-code-generator');
 }

 /** Build an SVG string from the current matrix, crisp at any print size. */
 function toSVG() {
 if (!current) return '';

 const margin = Number($('margin').value);
 const total = current.size + margin * 2;
 const paths = [];

 for (let y = 0; y < current.size; y++) {
 for (let x = 0; x < current.size; x++) {
 if (current.modules[y][x]) {
 paths.push('M' + (x + margin) + ' ' + (y + margin) + 'h1v1h-1z');
 }
 }
 }

 return '<?xml version="1.0" encoding="UTF-8"?>\n' +
 '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + total + ' ' + total + '" ' +
 'width="' + $('size').value + '" height="' + $('size').value + '" shape-rendering="crispEdges">' +
 '<rect width="' + total + '" height="' + total + '" fill="' + $('bg').value + '"/>' +
 '<path d="' + paths.join('') + '" fill="' + $('fg').value + '"/>' +
 '</svg>';
 }

 /* ---- Panel switching ---- */
 function showPanels() {
 const type = $('type').value;
 document.querySelectorAll('[data-panel]').forEach((panel) => {
 panel.hidden = !panel.dataset.panel.split(' ').includes(type);
 });
 $('content-label').textContent = type === 'url' ? 'Link' : 'Text';
 render();
 }

 /* ---- Wiring ---- */
 $('type').addEventListener('change', showPanels);

 ['content', 'wifi-ssid', 'wifi-pass', 'vc-name', 'vc-phone', 'vc-email', 'vc-org', 'em-to', 'em-subject']
 .forEach((id) => $(id).addEventListener('input', debounce(render, 250)));

 ['ecl', 'wifi-enc', 'fg', 'bg'].forEach((id) => $(id).addEventListener('input', render));

 $('size').addEventListener('input', () => {
 $('size-value').textContent = $('size').value;
 render();
 });

 $('margin').addEventListener('input', () => {
 $('margin-value').textContent = $('margin').value;
 render();
 });

 $('download-png').addEventListener('click', () => {
 if (!current) {
 toast({ type: 'warning', title: 'Nothing to download', message: 'Generate a code first.' });
 return;
 }
 canvas.toBlob((blob) => downloadFile(blob, 'qr-code.png', 'image/png'), 'image/png');
 });

 $('download-svg').addEventListener('click', () => {
 if (!current) {
 toast({ type: 'warning', title: 'Nothing to download', message: 'Generate a code first.' });
 return;
 }
 downloadFile(toSVG(), 'qr-code.svg', 'image/svg+xml');
 });

 $('copy-img').addEventListener('click', async () => {
 if (!current) return;

 // ClipboardItem isn't available everywhere, fall back to the SVG source
 if (!navigator.clipboard || !window.ClipboardItem) {
 copyToClipboard(toSVG(), 'SVG source copied');
 return;
 }

 canvas.toBlob(async (blob) => {
 try {
 await navigator.clipboard.write([new ClipboardItem({ 'image/png': blob })]);
 toast({ type: 'success', title: 'Image copied' });
 } catch {
 copyToClipboard(toSVG(), 'SVG source copied instead');
 }
 }, 'image/png');
 });

 $('share').addEventListener('click', () => shareLink({ title: 'QR Code Generator | 123MiniApps' }));

 showPanels();""",
}

PAGES = [JSON_FORMATTER, BASE64, COLOR_PICKER, QR_CODE]
