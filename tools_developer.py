#!/usr/bin/env python3
# ============================================
# 123MiniApps.online v2.0
# File: tools_developer.py
# Purpose: The 10 remaining Developer Tools
# (ids 22, 24-32; 21 and 23 are hand-built).
# ============================================

from toolkit import (
 tool, ws, info, row, textarea, text_input, number_input, select, switch,
 output, status_line, buttons, STD_ACTIONS, HR, html_block,
)

PAGES = []

# ---------------------------------------------------------------
# 22. Regex Tester
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="regex-tester", name="Regex Tester", icon="🎯", cat="developer",
 title="Regex Tester: Live Match Highlighting and Capture Groups",
 description="Test regular expressions against sample text with live match highlighting, a capture group inspector, all standard flags and a common pattern library.",
 tagline="Test regular expressions with live highlighting and a capture group inspector.",
 workspace=ws(
 html_block(""" <div class="field">
 <label class="field__label" for="pattern">
 <span>Pattern</span>
 <span class="field__hint" id="pattern-status"></span>
 </label>
 <div style="display:flex;align-items:center;gap:var(--space-2)">
 <span class="font-mono text-muted">/</span>
 <input class="input font-mono" id="pattern" type="text" value="(\\w+)@(\\w+\\.\\w+)"
 placeholder="Your regular expression" autocomplete="off" spellcheck="false">
 <span class="font-mono text-muted">/</span>
 <input class="input font-mono" id="flags" type="text" value="g" placeholder="flags"
 style="max-width:90px" autocomplete="off" spellcheck="false" aria-label="Regex flags">
 </div>
 </div>"""),
 html_block(""" <div class="chip-grid" id="flag-toggles" style="margin-top:var(--space-3)"></div>"""),
 textarea("subject", "Test against", "Paste the text you want to match against…", "subject-stats", rows=170,
 value="Contact ada@example.com or alan@example.org for details."),
 status_line("status", "Enter a pattern to begin."),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Matches</span><span class="field__hint" id="match-count"></span></span>
 <div class="output output--empty" id="highlight">Matches will be highlighted here.</div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Capture groups</span></span>
 <div class="table-scroll"><div id="groups"></div></div>
 </div>"""),
 row(
 text_input("replace", "Replacement (optional)", "$1 at $2"),
 html_block(""" <div class="field">
 <span class="field__label"><span>Replacement result</span></span>
 <div class="output output--empty" id="replaced" style="min-height:52px">, </div>
 </div>"""),
 ),
 buttons(("copy", "Copy matches", "primary"), ("copy-replaced", "Copy replacement"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Common patterns</span><span class="field__hint">Click to load</span></span>
 <div class="chip-grid" id="library"></div>
 </div>"""),
 label="Regex tester",
 ),
 info_block=info(
 features=[
 "Live match highlighting as you type",
 "Numbered and named capture group inspector",
 "All standard flags with one-click toggles",
 "Replacement preview with $1 backreferences",
 "Library of twelve common patterns",
 ],
 howto=[
 "Type your pattern in the top field.",
 "Paste sample text into the box below.",
 "Matches highlight immediately; groups appear in the table.",
 "Add a replacement string to preview a substitution.",
 ],
 background_title="Flags, greediness and catastrophic backtracking",
 background_paragraphs=[
 "The flags change behaviour more than newcomers expect. Without <code>g</code>, only the first match is returned. The <code>m</code> flag makes <code>^</code> and <code>$</code> match at line boundaries rather than only at the start and end of the whole string. The <code>s</code> flag lets <code>.</code> match newlines, which it otherwise never does, the single most common reason a pattern fails on multi-line input.",
 "Quantifiers are greedy by default, meaning <code>&lt;.+&gt;</code> against <code>&lt;a&gt;&lt;b&gt;</code> matches the entire string rather than just <code>&lt;a&gt;</code>. Adding <code>?</code> makes them lazy, so <code>&lt;.+?&gt;</code> stops at the first closing bracket. Knowing which you want is usually the difference between a pattern that works and one that almost works.",
 "The genuine hazard is catastrophic backtracking. Nested quantifiers such as <code>(a+)+b</code> can take exponential time on input that nearly matches, a few dozen characters can hang the engine for minutes. This has taken down production services; Cloudflare's 2019 global outage was caused by exactly this. If a pattern will ever see untrusted input, avoid nesting quantifiers, and prefer atomic constructs or a hard input length limit. This tool caps execution to keep the tab responsive if you hit one.",
 ],
 ),
 script=r""" const FLAGS = [
 ['g', 'global, find all matches'],
 ['i', 'ignore case'],
 ['m', 'multiline, ^ and $ match line breaks'],
 ['s', 'dotall. matches newlines'],
 ['u', 'unicode'],
 ['y', 'sticky']
 ];

 const LIBRARY = [
 ['Email', "[\\w.+-]+@[\\w-]+\\.[\\w.]+", 'g'],
 ['URL', "https?://[^\\s/$.?#].[^\\s]*", 'g'],
 ['IPv4', "\\b(?:\\d{1,3}\\.){3}\\d{1,3}\\b", 'g'],
 ['Hex colour', "#(?:[0-9a-fA-F]{3}){1,2}\\b", 'g'],
 ['Date ISO', "\\d{4}-\\d{2}-\\d{2}", 'g'],
 ['UK postcode', "[A-Z]{1,2}\\d[A-Z\\d]?\\s?\\d[A-Z]{2}", 'gi'],
 ['Phone (loose)', "\\+?\\d[\\d\\s()-]{7,}\\d", 'g'],
 ['HTML tag', "<\\/?[a-zA-Z][^>]*>", 'g'],
 ['Duplicate word', "\\b(\\w+)\\s+\\1\\b", 'gi'],
 ['Whitespace runs', "\\s{2,}", 'g'],
 ['Number with decimals', "-?\\d+(?:\\.\\d+)?", 'g'],
 ['Quoted string', "\"[^\"]*\"|'[^']*'", 'g']
 ];

 let matches = [];

 function buildRegex() {
 const pattern = T.$('pattern').value;
 if (!pattern) return null;

 try {
 const re = new RegExp(pattern, T.$('flags').value);
 T.$('pattern').classList.remove('is-invalid');
 T.$('pattern-status').textContent = '';
 return re;
 } catch (err) {
 T.$('pattern').classList.add('is-invalid');
 T.$('pattern-status').textContent = 'invalid';
 T.$('pattern-status').style.color = 'var(--danger)';
 T.status('status', err.message, 'error');
 return false;
 }
 }

 function run() {
 const subject = T.$('subject').value;
 T.$('subject-stats').textContent = subject.length.toLocaleString() + ' characters';

 const re = buildRegex();

 if (re === null) {
 T.setOutput('highlight', '', 'Matches will be highlighted here.');
 T.$('groups').innerHTML = '';
 T.$('match-count').textContent = '';
 T.status('status', 'Enter a pattern to begin.', 'muted');
 return;
 }
 if (re === false) return;

 matches = [];

 // Collect matches with a hard cap and a zero-length guard, so a
 // pathological pattern cannot lock the tab up.
 const global = re.flags.includes('g');
 const scan = new RegExp(re.source, global ? re.flags : re.flags + 'g');
 const started = Date.now();

 let m;
 while ((m = scan.exec(subject)) !== null) {
 matches.push({ text: m[0], index: m.index, groups: m.slice(1), named: m.groups || null });

 if (m[0] === '') scan.lastIndex++; // zero-length match
 if (!global) break;
 if (matches.length >= 500) break;
 if (Date.now() - started > 1000) {
 T.status('status', 'Pattern took too long, stopped after 1 second. Check for nested quantifiers.', 'error');
 break;
 }
 }

 renderHighlight(subject);
 renderGroups();
 renderReplacement(subject, re);

 T.$('match-count').textContent = `${matches.length} match${matches.length === 1 ? '' : 'es'}`;

 if (matches.length) {
 T.status('status', `${matches.length} match(es) found.`, 'ok');
 } else {
 T.status('status', 'No matches in the sample text.', 'warn');
 }
 }

 function renderHighlight(subject) {
 if (!matches.length) {
 T.setOutput('highlight', '', 'No matches.');
 return;
 }

 let html = '';
 let cursor = 0;

 matches.forEach((match, i) => {
 html += T.esc(subject.slice(cursor, match.index));
 html += `<span class="${i % 2 ? 'hl--alt' : 'hl'}">${T.esc(match.text) || '∅'}</span>`;
 cursor = match.index + match.text.length;
 });

 html += T.esc(subject.slice(cursor));
 T.setOutputHTML('highlight', html);
 }

 function renderGroups() {
 const mount = T.$('groups');
 mount.innerHTML = '';

 const withGroups = matches.filter((m) => m.groups.length);
 if (!withGroups.length) return;

 const groupCount = Math.max(...withGroups.map((m) => m.groups.length));
 const headers = ['#', 'Full match', ...Array.from({ length: groupCount }, (_, i) => `Group ${i + 1}`)];

 const rows = matches.slice(0, 50).map((m, i) => [
 i + 1,
 m.text || '(empty)',
 ...Array.from({ length: groupCount }, (_, g) =>
 m.groups[g] === undefined ? ', ' : m.groups[g])
 ]);

 mount.append(T.table(headers, rows));
 }

 function renderReplacement(subject, re) {
 const replacement = T.$('replace').value;

 if (!replacement) {
 T.setOutput('replaced', '', ', ');
 return;
 }

 try {
 T.setOutput('replaced', subject.replace(re, replacement));
 } catch (err) {
 T.setOutput('replaced', '', 'Replacement failed: ' + err.message);
 }
 }

 function renderFlagToggles() {
 const mount = T.$('flag-toggles');
 mount.innerHTML = '';

 FLAGS.forEach(([flag, description]) => {
 const chip = el('button', {
 className: 'chip font-mono',
 attrs: { type: 'button', title: description },
 text: flag
 });

 const paint = () => {
 const on = T.$('flags').value.includes(flag);
 chip.style.borderColor = on ? 'var(--accent-primary)' : '';
 chip.style.color = on ? 'var(--accent-primary)' : '';
 chip.setAttribute('aria-pressed', String(on));
 };

 chip.addEventListener('click', () => {
 const current = T.$('flags').value;
 T.$('flags').value = current.includes(flag)
 ? current.replace(flag, '')
 : current + flag;
 renderFlagToggles();
 run();
 });

 paint();
 mount.append(chip);
 });
 }

 function renderLibrary() {
 const mount = T.$('library');
 mount.innerHTML = '';

 LIBRARY.forEach(([name, pattern, flags]) => {
 const chip = el('button', { className: 'chip', attrs: { type: 'button' }, text: name });
 chip.addEventListener('click', () => {
 T.$('pattern').value = pattern;
 T.$('flags').value = flags;
 renderFlagToggles();
 run();
 });
 mount.append(chip);
 });
 }

 T.on(['pattern', 'flags', 'replace'], debounce(() => { renderFlagToggles(); run(); }, 250));
 T.$('subject').addEventListener('input', debounce(run, 250));

 T.$('copy').addEventListener('click', () =>
 copyToClipboard(matches.map((m) => m.text).join('\n'), 'Matches copied'));

 T.$('copy-replaced').addEventListener('click', () =>
 copyToClipboard(T.$('replaced').textContent, 'Replacement copied'));

 T.$('share').addEventListener('click', () => shareLink({ title: 'Regex Tester | 123MiniApps' }));

 renderFlagToggles();
 renderLibrary();
 run();
 if (window.Analytics) Analytics.trackToolUse('regex-tester');""",
))

# ---------------------------------------------------------------
# 24. URL Encoder / Decoder
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="url-encoder-decoder", name="URL Encoder / Decoder", icon="🌐", cat="developer",
 title="URL Encoder & Decoder: Percent Encoding and Query Parsing",
 description="Percent-encode or decode URLs and query components, with a full breakdown of every part of a URL and its query parameters.",
 tagline="Encode and decode URLs, and break any URL into its component parts.",
 workspace=ws(
 select("mode", "Mode", [
 ("encode-component", "Encode a component (encodeURIComponent)"),
 ("encode-uri", "Encode a full URL (encodeURI)"),
 ("decode", "Decode"),
 ], selected="encode-component"),
 textarea("input", "Input", "https://example.com/search?q=hello world&lang=en", "input-stats", rows=130,
 value="https://example.com/search?q=hello world&lang=en"),
 switch("perline", "Process each line separately", False),
 status_line("status", "Output updates as you type."),
 HR,
 output("output", "Result", "output-stats"),
 buttons(("copy", "Copy result", "primary"), ("swap", "Use result as input"), ("download", "Download"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>URL breakdown</span><span class="field__hint">Parsed from the input, when it is a valid URL</span></span>
 <div class="table-scroll"><div id="parts"></div></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Query parameters</span></span>
 <div class="table-scroll"><div id="params"></div></div>
 </div>"""),
 label="URL encoder and decoder",
 ),
 info_block=info(
 features=[
 "Component and full-URL encoding modes",
 "Decoding with clear errors on malformed input",
 "Complete URL breakdown: scheme, host, path, query, fragment",
 "Query parameter table with decoded values",
 "Line-by-line batch processing",
 ],
 howto=[
 "Pick whether you are encoding a component or a whole URL.",
 "Paste your text or URL.",
 "The result and breakdown update as you type.",
 "Copy the result or feed it back in with Swap.",
 ],
 background_title="encodeURI versus encodeURIComponent",
 background_paragraphs=[
 "These two functions are not interchangeable and picking the wrong one is a routine source of bugs. <code>encodeURI</code> assumes you are handing it a complete URL, so it leaves the structural characters alone: <code>: / ? # [ ] @ ! $ &amp; ' ( ) * +; =</code> all survive. That is correct for a whole URL and wrong for a value inside one.",
 "<code>encodeURIComponent</code> escapes all of those. Use it for anything that goes <em>into</em> a URL, a query parameter value, a path segment, a fragment. If a search term contains an ampersand and you encode it with <code>encodeURI</code>, the ampersand stays literal and the server reads the rest of your term as a separate parameter. Encoded as <code>%26</code>, it arrives intact.",
 "Two details that catch people out. Neither function escapes <code>!'()*</code>, which are legal in URLs but occasionally problematic in specific contexts. And a space becomes <code>%20</code> in both, whereas in the <code>application/x-www-form-urlencoded</code> body of a form submission a space becomes <code>+</code>. When decoding form data you must convert <code>+</code> back to a space first, or <code>decodeURIComponent</code> will leave plus signs scattered through your text.",
 ],
 ),
 script=r""" let lastResult = '';

 function transform(text) {
 const mode = T.$('mode').value;

 if (mode === 'encode-component') return encodeURIComponent(text);
 if (mode === 'encode-uri') return encodeURI(text);

 // Decoding: form-encoded bodies use + for space, which
 // decodeURIComponent leaves alone.
 return decodeURIComponent(text.replace(/\+/g, ' '));
 }

 function run() {
 const raw = T.$('input').value;
 T.$('input-stats').textContent = raw.length.toLocaleString() + ' characters';

 if (!raw) {
 lastResult = '';
 T.setOutput('output', '');
 T.$('output-stats').textContent = '';
 T.$('parts').innerHTML = '';
 T.$('params').innerHTML = '';
 T.status('status', 'Output updates as you type.', 'muted');
 return;
 }

 try {
 lastResult = T.$('perline').checked
 ? raw.split(/\r?\n/).map(transform).join('\n')
 : transform(raw);

 T.setOutput('output', lastResult);
 T.$('output-stats').textContent = lastResult.length.toLocaleString() + ' characters';

 const delta = lastResult.length - raw.length;
 T.status('status',
 `Done, ${delta >= 0 ? '+' : ''}${delta} character(s).`, 'ok');
 } catch (err) {
 lastResult = '';
 T.setOutput('output', '');
 T.status('status',
 'Could not decode, the input contains a malformed percent sequence.', 'error');
 }

 analyse(raw);
 }

 /** Break the input into URL parts, when it parses as one. */
 function analyse(raw) {
 const partsMount = T.$('parts');
 const paramsMount = T.$('params');
 partsMount.innerHTML = '';
 paramsMount.innerHTML = '';

 let url;
 try {
 url = new URL(raw.trim());
 } catch {
 return; // not a URL, nothing to break down
 }

 const rows = [
 ['Scheme', url.protocol.replace(':', '')],
 ['Host', url.hostname],
 ['Port', url.port || '(default)'],
 ['Path', url.pathname],
 ['Query', url.search || '(none)'],
 ['Fragment', url.hash || '(none)'],
 ['Origin', url.origin]
 ];
 if (url.username) rows.splice(1, 0, ['Username', url.username]);

 partsMount.append(T.table(['Part', 'Value'], rows));

 const params = [...url.searchParams.entries()];
 if (params.length) {
 paramsMount.append(T.table(
 ['Parameter', 'Raw value', 'Decoded'],
 params.map(([k, v]) => [k, encodeURIComponent(v), v])
 ));
 }
 }

 T.$('input').addEventListener('input', debounce(run, 250));
 T.on(['mode', 'perline'], run, 'change');

 T.$('swap').addEventListener('click', () => {
 if (!lastResult) return;
 T.$('input').value = lastResult;
 T.$('mode').value = T.$('mode').value === 'decode' ? 'encode-component' : 'decode';
 run();
 });

 T.wireActions({ slug: 'url-encoder-decoder', getResult: () => lastResult, filename: 'url.txt' });
 run();""",
))

# ---------------------------------------------------------------
# 25. JWT Decoder
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="jwt-decoder", name="JWT Decoder", icon="🎫", cat="developer",
 title="JWT Decoder: Inspect Header, Payload and Expiry Locally",
 description="Decode a JSON Web Token to inspect its header, payload and expiry. Decoding happens entirely in your browser, the token is never transmitted.",
 tagline="Inspect a JWT's header, claims and expiry, decoded locally, never sent anywhere.",
 workspace=ws(
 html_block(""" <p class="field__hint" style="color:var(--warning)">
 A JWT often <em>is</em> a live credential. Pasting one into an online decoder that sends it to a
 server hands over whatever access it grants. This tool decodes in your browser and makes no
 network requests, you can confirm that in the Network tab. Even so, treat production tokens
 with care and revoke anything you have pasted somewhere you did not fully trust.
 </p>"""),
 textarea("input", "JSON Web Token", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9…", "input-stats", rows=130),
 status_line("status", "Paste a token to decode it."),
 HR,
 html_block(""" <div class="workspace__row">
 <div class="field">
 <span class="field__label"><span>Header</span><span class="field__hint">Algorithm and type</span></span>
 <div class="output output--empty" id="header">, </div>
 </div>
 <div class="field">
 <span class="field__label"><span>Payload</span><span class="field__hint">The claims</span></span>
 <div class="output output--empty" id="payload">, </div>
 </div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Registered claims</span></span>
 <div class="table-scroll"><div id="claims"></div></div>
 </div>"""),
 html_block(""" <div class="result-grid">
 <div class="result result--primary"><span class="result__value" id="r-status" style="font-size:var(--text-xl)">, </span><span class="result__label">Token status</span></div>
 <div class="result"><span class="result__value" id="r-alg" style="font-size:var(--text-xl)">, </span><span class="result__label">Algorithm</span></div>
 <div class="result"><span class="result__value" id="r-expires" style="font-size:var(--text-lg)">, </span><span class="result__label">Expires</span></div>
 </div>"""),
 buttons(("sample", "Load a sample token", "primary"), ("copy", "Copy payload"), ("clear", "Clear", "ghost"), ("share", "Share tool", "ghost")),
 label="JWT decoder",
 ),
 info_block=info(
 features=[
 "Decodes header and payload with formatting",
 "Registered claim reference with human-readable times",
 "Expiry status and countdown",
 "Handles Base64URL padding correctly",
 "Nothing is transmitted, decoding is local",
 ],
 howto=[
 "Paste your token into the box.",
 "The header and payload decode immediately.",
 "Check the claims table for expiry and issuer.",
 "Clear the box when you are finished.",
 ],
 background_title="What decoding a JWT does and does not prove",
 background_paragraphs=[
 "A JWT has three Base64URL-encoded parts separated by dots: header, payload and signature. The first two are merely encoded, not encrypted, anyone holding the token can read every claim in it. That is by design, and it is why you must never put anything confidential in a JWT payload. Assume the user, and anyone who intercepts the token, can read it.",
 "This tool decodes but does not verify. Verification means recomputing the signature over the header and payload using the secret or public key, and that requires the key, which you should not paste into a website. An unverified token proves nothing: an attacker can change any claim and re-encode it. Always verify server-side before trusting a single field.",
 "The classic vulnerability is the <code>alg</code> header. Early libraries would read the algorithm from the token itself, so an attacker could set <code>alg</code> to <code>none</code>, strip the signature, and have the token accepted. A related attack switches <code>RS256</code> to <code>HS256</code> so the public key gets used as an HMAC secret. Modern libraries reject both, but the lesson stands: the server must decide which algorithm is acceptable, never the token. This decoder flags <code>alg: none</code> prominently for that reason.",
 ],
 ),
 script=r""" const CLAIM_NAMES = {
 iss: 'Issuer', sub: 'Subject', aud: 'Audience', exp: 'Expiry time',
 nbf: 'Not valid before', iat: 'Issued at', jti: 'JWT ID',
 scope: 'Scope', scp: 'Scope', roles: 'Roles', email: 'Email',
 name: 'Name', azp: 'Authorised party', typ: 'Type', kid: 'Key ID'
 };

 const TIME_CLAIMS = new Set(['exp', 'nbf', 'iat', 'auth_time', 'updated_at']);

 let payloadJson = '';

 /** Decode Base64URL, restoring padding and handling UTF-8. */
 function base64UrlDecode(segment) {
 let s = segment.replace(/-/g, '+').replace(/_/g, '/');
 while (s.length % 4) s += '=';

 const binary = atob(s);
 const bytes = new Uint8Array(binary.length);
 for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
 return new TextDecoder('utf-8').decode(bytes);
 }

 function relative(seconds) {
 const diff = seconds * 1000 - Date.now();
 const abs = Math.abs(diff);
 const units = [['day', 86400000], ['hour', 3600000], ['minute', 60000], ['second', 1000]];

 for (const [name, size] of units) {
 if (abs >= size || name === 'second') {
 const n = Math.round(abs / size);
 return diff < 0 ? `${n} ${name}${n === 1 ? '' : 's'} ago` : `in ${n} ${name}${n === 1 ? '' : 's'}`;
 }
 }
 return 'now';
 }

 function run() {
 const raw = T.$('input').value.trim();
 T.$('input-stats').textContent = raw.length.toLocaleString() + ' characters';

 if (!raw) {
 T.setOutput('header', '', ', ');
 T.setOutput('payload', '', ', ');
 T.$('claims').innerHTML = '';
 ['r-status', 'r-alg', 'r-expires'].forEach((id) => { T.$(id).textContent = ', '; });
 T.status('status', 'Paste a token to decode it.', 'muted');
 return;
 }

 const parts = raw.split('.');

 if (parts.length !== 3) {
 T.status('status',
 `A JWT has three dot-separated parts; this has ${parts.length}.`, 'error');
 return;
 }

 let header, payload;

 try {
 header = JSON.parse(base64UrlDecode(parts[0]));
 } catch {
 T.status('status', 'The header is not valid Base64URL-encoded JSON.', 'error');
 return;
 }

 try {
 payload = JSON.parse(base64UrlDecode(parts[1]));
 } catch {
 T.status('status', 'The payload is not valid Base64URL-encoded JSON.', 'error');
 return;
 }

 T.setOutput('header', JSON.stringify(header, null, 2));
 payloadJson = JSON.stringify(payload, null, 2);
 T.setOutput('payload', payloadJson);

 const alg = header.alg || 'unknown';
 T.$('r-alg').textContent = alg;
 T.$('r-alg').style.color = alg.toLowerCase() === 'none' ? 'var(--danger)' : '';

 renderClaims(payload);

 // Expiry
 const now = Math.floor(Date.now() / 1000);
 let statusText = 'Decoded';
 let statusColour = 'var(--success)';

 if (payload.exp) {
 T.$('r-expires').textContent = new Date(payload.exp * 1000).toLocaleString();
 if (payload.exp < now) {
 statusText = 'Expired';
 statusColour = 'var(--danger)';
 }
 } else {
 T.$('r-expires').textContent = 'No expiry claim';
 }

 if (payload.nbf && payload.nbf > now) {
 statusText = 'Not yet valid';
 statusColour = 'var(--warning)';
 }

 T.$('r-status').textContent = statusText;
 T.$('r-status').style.color = statusColour;

 if (alg.toLowerCase() === 'none') {
 T.status('status',
 'Warning: alg is "none", meaning this token carries no signature at all.', 'error');
 } else if (statusText === 'Expired') {
 T.status('status',
 `Token expired ${relative(payload.exp)}. Decoded successfully, but not verified.`, 'warn');
 } else {
 T.status('status',
 'Decoded successfully. Note that the signature has NOT been verified.', 'ok');
 }

 if (window.Analytics) Analytics.trackToolUse('jwt-decoder');
 }

 function renderClaims(payload) {
 const mount = T.$('claims');
 mount.innerHTML = '';

 const rows = Object.entries(payload).map(([key, value]) => {
 let display;

 if (TIME_CLAIMS.has(key) && typeof value === 'number') {
 display = `${new Date(value * 1000).toLocaleString()} (${relative(value)})`;
 } else if (value !== null && typeof value === 'object') {
 display = JSON.stringify(value);
 } else {
 display = String(value);
 }

 return [key, CLAIM_NAMES[key] || ', ', display];
 });

 mount.append(T.table(['Claim', 'Meaning', 'Value'], rows));
 }

 T.$('input').addEventListener('input', debounce(run, 250));

 T.$('sample').addEventListener('click', () => {
 // A deliberately fake, already-expired demo token
 const header = { alg: 'HS256', typ: 'JWT' };
 const payload = {
 sub: '1234567890',
 name: 'Ada Lovelace',
 email: 'ada@example.com',
 roles: ['engineer', 'admin'],
 iss: 'https://auth.example.com',
 iat: Math.floor(Date.now() / 1000) - 3600,
 exp: Math.floor(Date.now() / 1000) + 3600
 };
 const enc = (obj) => btoa(JSON.stringify(obj))
 .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');

 T.$('input').value = `${enc(header)}.${enc(payload)}.not-a-real-signature`;
 run();
 });

 T.$('copy').addEventListener('click', () => copyToClipboard(payloadJson, 'Payload copied'));

 T.$('clear').addEventListener('click', () => {
 T.$('input').value = '';
 run();
 toast({ type: 'success', title: 'Cleared', message: 'The token is gone from this page.' });
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'JWT Decoder | 123MiniApps' }));

 run();""",
))

# ---------------------------------------------------------------
# 26. HTML Formatter
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="html-formatter", name="HTML Formatter", icon="📋", cat="developer",
 title="HTML Formatter: Beautify and Minify Markup",
 description="Indent and tidy messy HTML, or minify it for production. Configurable indentation, with tag statistics and a size comparison.",
 tagline="Beautify messy HTML or minify it for production, with a size comparison.",
 workspace=ws(
 textarea("input", "HTML", "<div><p>Paste your markup here</p></div>", "input-stats", rows=180),
 row(
 select("indent", "Indentation", [("2", "2 spaces"), ("4", "4 spaces"), ("tab", "Tab")], selected="2"),
 switch("preserve", "Preserve pre, code and textarea content", True),
 switch("collapse", "Collapse empty lines", True),
 ),
 status_line("status", "Paste HTML to format it."),
 HR,
 output("output", "Result", "output-stats"),
 buttons(("beautify", "Beautify", "primary"), ("minify", "Minify"), ("copy", "Copy result"), ("download", "Download"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Tag summary</span></span>
 <div class="table-scroll"><div id="tags"></div></div>
 </div>"""),
 label="HTML formatter",
 ),
 info_block=info(
 features=[
 "Beautify with 2-space, 4-space or tab indentation",
 "Minify with a before-and-after size comparison",
 "Preserves whitespace-sensitive elements",
 "Handles void elements and self-closing tags",
 "Tag frequency summary",
 ],
 howto=[
 "Paste your HTML into the input box.",
 "Choose an indentation style.",
 "Press Beautify to format, or Minify to compress.",
 "Copy or download the result.",
 ],
 background_title="Whitespace in HTML is not always insignificant",
 background_paragraphs=[
 "HTML collapses runs of whitespace to a single space when rendering, which is why you can indent markup freely. But whitespace is not universally ignorable. Inside <code>&lt;pre&gt;</code>, <code>&lt;textarea&gt;</code> and any element with <code>white-space: pre</code>, every space and newline is significant, reindenting those changes what the user sees. This formatter leaves their contents untouched when the preserve option is on.",
 "There is a subtler case that catches people out with minification. Inline elements are separated by the whitespace between them, so <code>&lt;span&gt;a&lt;/span&gt; &lt;span&gt;b&lt;/span&gt;</code> renders as “a b” while removing that single space renders “ab”. Aggressive minifiers that strip all inter-tag whitespace can visibly change layouts. This one only collapses runs of whitespace rather than eliminating them entirely, which is the safe default.",
 "Minification savings on HTML are usually modest, often 10% to 20%, and much of that overlaps with what gzip or brotli compression would achieve anyway, since repeated indentation compresses extremely well. If your server has compression enabled, the incremental benefit of minifying HTML is small. It matters far more for CSS and JavaScript, where minification also shortens identifiers.",
 ],
 ),
 script=r""" let lastResult = '';

 // Elements that never have closing tags
 const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
 'link', 'meta', 'param', 'source', 'track', 'wbr']);

 // Elements whose inner whitespace is significant
 const PRESERVE = new Set(['pre', 'code', 'textarea', 'script', 'style']);

 function indentString() {
 const v = T.$('indent').value;
 return v === 'tab' ? '\t' : ' '.repeat(Number(v));
 }

 /**
 * Tokenise into tags, comments and text runs, then re-emit with
 * indentation tracked by a depth counter.
 */
 function beautify(html) {
 const indent = indentString();
 const preserve = T.$('preserve').checked;

 // Split on tags and comments, keeping the delimiters
 const tokens = html
 .replace(/\r\n/g, '\n')
 .split(/(<!--[\s\S]*?-->|<[^>]+>)/)
 .filter((t) => t !== '');

 const out = [];
 let depth = 0;
 let preserveDepth = 0;

 for (let raw of tokens) {
 const isTag = raw.startsWith('<');

 if (!isTag) {
 if (preserveDepth > 0) { out[out.length - 1] += raw; continue; }
 const text = raw.replace(/\s+/g, ' ').trim();
 if (text) out.push(indent.repeat(depth) + text);
 continue;
 }

 const isComment = raw.startsWith('<!--');
 const isClosing = /^<\//.test(raw);
 const isDoctype = /^<!doctype/i.test(raw);
 const name = (raw.match(/^<\/?\s*([a-zA-Z0-9-]+)/) || [])[1];
 const lower = name ? name.toLowerCase() : '';
 const selfClosing = /\/>$/.test(raw) || VOID.has(lower);

 if (preserveDepth > 0) {
 out[out.length - 1] += raw;
 if (isClosing && PRESERVE.has(lower)) preserveDepth--;
 continue;
 }

 if (isClosing) depth = Math.max(0, depth - 1);

 out.push(indent.repeat(depth) + raw.replace(/\s+/g, ' '));

 if (!isClosing && !isComment && !isDoctype && !selfClosing) {
 depth++;
 if (preserve && PRESERVE.has(lower)) preserveDepth++;
 }
 }

 let result = out.join('\n');
 if (T.$('collapse').checked) result = result.replace(/\n{3,}/g, '\n\n');
 return result;
 }

 function minify(html) {
 return html
 // Strip comments, but keep conditional comments
 .replace(/<!--(?!\[if)[\s\S]*?-->/g, '')
 // Collapse whitespace runs to a single space, never remove
 // them entirely, since inline elements depend on them
 .replace(/\s{2,}/g, ' ')
 .replace(/>\s+</g, '> <')
 .replace(/\n/g, '')
 .trim();
 }

 function analyseTags(html) {
 const mount = T.$('tags');
 mount.innerHTML = '';

 const counts = new Map();
 const re = /<([a-zA-Z][a-zA-Z0-9-]*)\b/g;
 let m;
 while ((m = re.exec(html)) !== null) {
 const tag = m[1].toLowerCase();
 counts.set(tag, (counts.get(tag) || 0) + 1);
 }

 const top = [...counts.entries()].sort((a, b) => b[1] - a[1]).slice(0, 12);
 if (!top.length) return;

 mount.append(T.table(['Tag', 'Count'], top.map(([t, n]) => ['<' + t + '>', n])));
 }

 function run(mode) {
 const raw = T.$('input').value;
 T.$('input-stats').textContent = raw.length.toLocaleString() + ' characters';

 if (!raw.trim()) {
 lastResult = '';
 T.setOutput('output', '');
 T.$('output-stats').textContent = '';
 T.$('tags').innerHTML = '';
 T.status('status', 'Paste HTML to format it.', 'muted');
 return;
 }

 try {
 lastResult = mode === 'minify' ? minify(raw) : beautify(raw);
 T.setOutput('output', lastResult);

 const saved = raw.length - lastResult.length;
 const pct = raw.length ? ((saved / raw.length) * 100).toFixed(1) : '0';

 T.$('output-stats').textContent =
 `${lastResult.length.toLocaleString()} characters` +
 (mode === 'minify' && saved > 0 ? ` · ${pct}% smaller` : '');

 T.status('status',
 mode === 'minify'
 ? `Minified, saved ${saved.toLocaleString()} character(s), ${pct}% smaller.`
 : 'Formatted.', 'ok');

 analyseTags(raw);
 if (window.Analytics) Analytics.trackToolUse('html-formatter');
 } catch (err) {
 T.status('status', 'Could not process that markup: ' + err.message, 'error');
 }
 }

 // Remember which mode the user last asked for, so the debounced
 // re-run after typing does not silently clobber a minified result
 // with a beautified one (or vice versa).
 let currentMode = 'beautify';
 const setMode = (mode) => { currentMode = mode; run(mode); };

 T.$('beautify').addEventListener('click', () => setMode('beautify'));
 T.$('minify').addEventListener('click', () => setMode('minify'));
 T.$('input').addEventListener('input', debounce(() => run(currentMode), 400));
 T.on(['indent', 'preserve', 'collapse'], () => run(currentMode), 'change');

 T.wireActions({ slug: 'html-formatter', getResult: () => lastResult, filename: 'formatted.html', mime: 'text/html' });

 T.$('input').value = '<div class="card"><h2>Title</h2><p>Some <strong>bold</strong> text.</p><ul><li>One</li><li>Two</li></ul></div>';
 run('beautify');""",
))

# ---------------------------------------------------------------
# 27. CSS Minifier
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="css-minifier", name="CSS Minifier", icon="🎨", cat="developer",
 title="CSS Minifier and Beautifier: Compress Stylesheets",
 description="Strip comments and whitespace from CSS to shrink it, or expand minified CSS back into readable form. Reports exactly how many bytes were saved.",
 tagline="Compress CSS for production, or expand minified CSS back into readable form.",
 workspace=ws(
 textarea("input", "CSS", "Paste your stylesheet here…", "input-stats", rows=200),
 row(
 switch("comments", "Remove comments", True),
 switch("lastsemi", "Remove the last semicolon in each block", True),
 switch("zeros", "Shorten zero values and colours", True),
 ),
 status_line("status", "Paste CSS to minify it."),
 HR,
 output("output", "Result", "output-stats"),
 buttons(("minify", "Minify", "primary"), ("beautify", "Beautify"), ("copy", "Copy result"), ("download", "Download"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result"><span class="result__value" id="r-before" style="font-size:var(--text-2xl)">, </span><span class="result__label">Original</span></div>
 <div class="result result--primary"><span class="result__value" id="r-after" style="font-size:var(--text-2xl)">, </span><span class="result__label">Minified</span></div>
 <div class="result"><span class="result__value" id="r-saved" style="font-size:var(--text-2xl)">, </span><span class="result__label">Saved</span></div>
 <div class="result"><span class="result__value" id="r-rules" style="font-size:var(--text-2xl)">, </span><span class="result__label">Rules</span></div>
 </div>"""),
 label="CSS minifier",
 ),
 info_block=info(
 features=[
 "Comment and whitespace removal",
 "Optional zero-value and hex-colour shortening",
 "Beautify mode for reading minified CSS",
 "Byte-level savings report",
 "Preserves strings and url() contents",
 ],
 howto=[
 "Paste your CSS into the input box.",
 "Choose which optimisations to apply.",
 "Press Minify, or Beautify to expand it again.",
 "Copy or download the result.",
 ],
 background_title="What minification actually saves",
 background_paragraphs=[
 "CSS minification typically removes 20% to 35% of the raw bytes, mostly whitespace and comments. But it is worth being clear-eyed about the real benefit: if your server sends CSS with gzip or brotli compression enabled, and it should, much of that saving already happens automatically, because repeated indentation and long runs of spaces compress extremely well. Minifying before compressing usually yields a further 5% to 15%, which is worth having but is not transformative.",
 "The safe optimisations are unambiguous. <code>0px</code> can become <code>0</code> in most contexts, since the unit is meaningless at zero. <code>#ffffff</code> can become <code>#fff</code> when the pairs repeat. A leading zero in <code>0.5em</code> is optional. The final semicolon in a block is redundant. None of these change behaviour.",
 "Two caveats. Zero without units is <em>not</em> always safe, inside <code>flex-basis</code> and in some <code>calc()</code> expressions a unit is required, and stripping it breaks the rule. And minifiers must not touch the inside of strings or <code>url()</code> values, where whitespace and case can be significant. This tool protects those regions, but the general principle applies: always test a minified stylesheet before shipping it, rather than assuming byte-identical rendering.",
 ],
 ),
 script=r""" let lastResult = '';

 /**
 * Replace strings and url() contents with placeholders so later
 * transformations cannot corrupt them, then restore afterwards.
 */
 function protect(css) {
 const stash = [];
 const protectedCss = css.replace(
 /(url\([^)]*\))|("(?:\\.|[^"\\])*")|('(?:\\.|[^'\\])*')/g,
 (match) => {
 stash.push(match);
 return `\u0000${stash.length - 1}\u0000`;
 }
 );
 return { css: protectedCss, stash };
 }

 function restore(css, stash) {
 return css.replace(/\u0000(\d+)\u0000/g, (_, i) => stash[Number(i)]);
 }

 function minify(input) {
 const { css: safe, stash } = protect(input);
 let css = safe;

 if (T.$('comments').checked) {
 // Keep /*! … */ banner comments, which usually carry licences
 css = css.replace(/\/\*(?!!)[\s\S]*?\*\//g, '');
 }

 css = css
 .replace(/\s+/g, ' ')
 .replace(/\s*([{}:; >+~])\s*/g, '$1')
 .trim();

 if (T.$('lastsemi').checked) css = css.replace(/;}/g, '}');

 if (T.$('zeros').checked) {
 css = css
 // Units are meaningless at zero for length values
 .replace(/(?<![\w.])0(px|em|rem|%|in|cm|mm|pt|pc|ex|vh|vw|vmin|vmax)/g, '0')
 // Leading zero in decimals is optional
 .replace(/(?<![\w.])0\.(\d)/g, '.$1')
 // #aabbcc → #abc when the pairs repeat
 .replace(/#([0-9a-f])\1([0-9a-f])\2([0-9a-f])\3\b/gi, '#$1$2$3');
 }

 return restore(css, stash);
 }

 function beautify(input) {
 const { css: safe, stash } = protect(input);

 let out = safe
 .replace(/\s+/g, ' ')
 .replace(/\s*{\s*/g, ' {\n ')
 .replace(/;\s*/g, ';\n ')
 .replace(/\s*}\s*/g, '\n}\n\n')
 .replace(/,\s*/g, ',\n')
 .replace(/\n\s+\n/g, '\n')
 .replace(/ }/g, '}')
 .trim();

 // Tidy the stray indentation left before closing braces
 out = out.split('\n').map((line) => line.replace(/\s+$/, '')).join('\n');
 return restore(out, stash);
 }

 function run(mode) {
 const raw = T.$('input').value;
 T.$('input-stats').textContent = raw.length.toLocaleString() + ' characters';

 if (!raw.trim()) {
 lastResult = '';
 T.setOutput('output', '');
 ['r-before', 'r-after', 'r-saved', 'r-rules'].forEach((id) => { T.$(id).textContent = ', '; });
 T.status('status', 'Paste CSS to minify it.', 'muted');
 return;
 }

 lastResult = mode === 'beautify' ? beautify(raw) : minify(raw);
 T.setOutput('output', lastResult);

 const before = new Blob([raw]).size;
 const after = new Blob([lastResult]).size;
 const saved = before - after;
 const pct = before ? ((saved / before) * 100).toFixed(1) : '0';

 T.$('r-before').textContent = T.bytes(before);
 T.$('r-after').textContent = T.bytes(after);
 T.$('r-saved').textContent = saved > 0 ? pct + '%' : ', ';
 T.$('r-rules').textContent = String((raw.match(/\{/g) || []).length);

 T.$('output-stats').textContent = lastResult.length.toLocaleString() + ' characters';

 T.status('status',
 mode === 'beautify'
 ? 'Expanded into readable form.'
 : `Minified, ${saved.toLocaleString()} bytes saved (${pct}% smaller).`, 'ok');

 if (window.Analytics) Analytics.trackToolUse('css-minifier');
 }

 // See the HTML formatter: the debounced re-run must honour the mode
 // the user last chose, not a hardcoded one.
 let currentMode = 'minify';
 const setMode = (mode) => { currentMode = mode; run(mode); };

 T.$('minify').addEventListener('click', () => setMode('minify'));
 T.$('beautify').addEventListener('click', () => setMode('beautify'));
 T.$('input').addEventListener('input', debounce(() => run(currentMode), 400));
 T.on(['comments', 'lastsemi', 'zeros'], () => run(currentMode), 'change');

 T.wireActions({ slug: 'css-minifier', getResult: () => lastResult, filename: 'styles.min.css', mime: 'text/css' });

 T.$('input').value =
 '/* Card component */\n.card {\n background: #ffffff;\n padding: 0px 16px;\n margin: 0.5em;\n border-radius: 8px;\n}\n\n.card:hover {\n box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);\n}';
 run('minify');""",
))

# ---------------------------------------------------------------
# 28. JavaScript Minifier
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="javascript-minifier", name="JavaScript Minifier", icon="⚡", cat="developer",
 title="JavaScript Minifier: Safe Whitespace and Comment Removal",
 description="Reduce JavaScript file size by removing comments and redundant whitespace, preserving strings, regex literals and template literals exactly.",
 tagline="Shrink JavaScript safely, strings, regex and template literals left untouched.",
 workspace=ws(
 textarea("input", "JavaScript", "Paste your script here…", "input-stats", rows=200),
 row(
 switch("comments", "Remove comments", True),
 switch("blanklines", "Remove blank lines", True),
 switch("semicolons", "Keep all semicolons (recommended)", True),
 ),
 status_line("status", "Paste JavaScript to minify it."),
 HR,
 output("output", "Result", "output-stats"),
 buttons(("minify", "Minify", "primary"), ("copy", "Copy result"), ("download", "Download"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result"><span class="result__value" id="r-before" style="font-size:var(--text-2xl)">, </span><span class="result__label">Original</span></div>
 <div class="result result--primary"><span class="result__value" id="r-after" style="font-size:var(--text-2xl)">, </span><span class="result__label">Minified</span></div>
 <div class="result"><span class="result__value" id="r-saved" style="font-size:var(--text-2xl)">, </span><span class="result__label">Saved</span></div>
 </div>"""),
 html_block(""" <p class="field__hint">
 This performs conservative, lexer-based minification: comments and redundant whitespace are
 removed, but nothing is renamed or restructured. A production bundler such as esbuild or
 Terser will do considerably better because it can shorten local variable names and remove
 unreachable code, transformations that need a full parser and are not safe to attempt here.
 </p>"""),
 label="JavaScript minifier",
 ),
 info_block=info(
 features=[
 "Removes line and block comments",
 "Collapses redundant whitespace",
 "Preserves strings, template literals and regex literals exactly",
 "Byte savings report",
 "Never renames identifiers, so behaviour cannot change",
 ],
 howto=[
 "Paste your JavaScript into the input box.",
 "Choose which cleanups to apply.",
 "Press Minify.",
 "Copy or download the result.",
 ],
 background_title="Why naive JavaScript minification breaks code",
 background_paragraphs=[
 "Stripping comments with a regular expression is the classic mistake. The sequence <code>//</code> appears inside URLs in strings, and <code>/*</code> can appear inside a regex literal. A naive comment-stripper turns <code>const url = 'https://example.com'</code> into <code>const url = 'https:</code> and breaks the file. This minifier walks the source character by character, tracking whether it is inside a string, template literal, regex or comment, which is the only reliable way to tell them apart.",
 "Distinguishing a regex literal from a division operator is genuinely ambiguous without parsing. In <code>a / b / c</code> the slashes are division; in <code>a = /b/g</code> they delimit a regex. The lexer here uses the standard heuristic of looking at the previous significant token, after an identifier, number or closing bracket a slash is division; otherwise it starts a regex. That is correct for essentially all real code.",
 "Automatic semicolon insertion is why the keep-semicolons option defaults to on. JavaScript will insert semicolons at line breaks under certain rules, so removing newlines from code that relies on ASI changes its meaning. A line starting with <code>(</code> or <code>[</code> is the classic hazard, it gets attached to the previous line as a call or index. Keeping semicolons and only collapsing whitespace avoids the whole category of problem.",
 ],
 ),
 script=r""" let lastResult = '';

 /**
 * Character-by-character lexer. Tracks strings, template literals,
 * regex literals and comments so that content inside them is never
 * altered, which a regex-based approach cannot do safely.
 * @param {string} src
 * @returns {string}
 */
 function minify(src) {
 const stripComments = T.$('comments').checked;
 let out = '';
 let i = 0;

 // Tracks the last emitted non-whitespace character, used both for
 // whitespace decisions and for the regex-vs-division heuristic
 let prev = '';

 const isIdentChar = (c) => /[A-Za-z0-9_$]/.test(c);

 /** After these, a slash means division rather than a regex. */
 const divisionContext = () => /[A-Za-z0-9_$)\]]/.test(prev);

 while (i < src.length) {
 const c = src[i];
 const next = src[i + 1];

 // Line comment
 if (c === '/' && next === '/' && !divisionContext()) {
 const end = src.indexOf('\n', i);
 if (!stripComments) out += src.slice(i, end === -1 ? src.length : end);
 i = end === -1 ? src.length : end;
 continue;
 }

 // Block comment
 if (c === '/' && next === '*') {
 const end = src.indexOf('*/', i + 2);
 const block = src.slice(i, end === -1 ? src.length : end + 2);
 // Keep /*! … */ banners, which usually carry licence text
 if (!stripComments || block.startsWith('/*!')) out += block;
 else out += ' ';
 i = end === -1 ? src.length : end + 2;
 continue;
 }

 // String literal
 if (c === '"' || c === "'") {
 const quote = c;
 let j = i + 1;
 while (j < src.length) {
 if (src[j] === '\\') { j += 2; continue; }
 if (src[j] === quote) break;
 j++;
 }
 out += src.slice(i, j + 1);
 prev = quote;
 i = j + 1;
 continue;
 }

 // Template literal, may contain ${} expressions, but copying
 // verbatim is always safe
 if (c === '`') {
 let j = i + 1;
 let depth = 0;
 while (j < src.length) {
 if (src[j] === '\\') { j += 2; continue; }
 if (src[j] === '$' && src[j + 1] === '{') { depth++; j += 2; continue; }
 if (src[j] === '}' && depth > 0) { depth--; j++; continue; }
 if (src[j] === '`' && depth === 0) break;
 j++;
 }
 out += src.slice(i, j + 1);
 prev = '`';
 i = j + 1;
 continue;
 }

 // Regex literal
 if (c === '/' && !divisionContext()) {
 let j = i + 1;
 let inClass = false;
 while (j < src.length) {
 if (src[j] === '\\') { j += 2; continue; }
 if (src[j] === '[') inClass = true;
 else if (src[j] === ']') inClass = false;
 else if (src[j] === '/' && !inClass) break;
 else if (src[j] === '\n') break; // unterminated, bail out
 j++;
 }
 // Include trailing flags
 let k = j + 1;
 while (k < src.length && /[a-z]/.test(src[k])) k++;
 out += src.slice(i, k);
 prev = '/';
 i = k;
 continue;
 }

 // Whitespace: keep exactly one space where it separates two
 // identifier characters, otherwise drop it
 if (/\s/.test(c)) {
 let j = i;
 let sawNewline = false;
 while (j < src.length && /\s/.test(src[j])) {
 if (src[j] === '\n') sawNewline = true;
 j++;
 }

 const after = src[j];
 const needsSpace = isIdentChar(prev) && isIdentChar(after);

 if (needsSpace) { out += ' '; prev = ' '; }
 else if (sawNewline && !T.$('blanklines').checked) { out += '\n'; }

 i = j;
 continue;
 }

 out += c;
 prev = c;
 i++;
 }

 return out.trim();
 }

 function run() {
 const raw = T.$('input').value;
 T.$('input-stats').textContent = raw.length.toLocaleString() + ' characters';

 if (!raw.trim()) {
 lastResult = '';
 T.setOutput('output', '');
 ['r-before', 'r-after', 'r-saved'].forEach((id) => { T.$(id).textContent = ', '; });
 T.status('status', 'Paste JavaScript to minify it.', 'muted');
 return;
 }

 try {
 lastResult = minify(raw);
 T.setOutput('output', lastResult);

 const before = new Blob([raw]).size;
 const after = new Blob([lastResult]).size;
 const saved = before - after;
 const pct = before ? ((saved / before) * 100).toFixed(1) : '0';

 T.$('r-before').textContent = T.bytes(before);
 T.$('r-after').textContent = T.bytes(after);
 T.$('r-saved').textContent = pct + '%';
 T.$('output-stats').textContent = lastResult.length.toLocaleString() + ' characters';

 T.status('status', `Minified, ${saved.toLocaleString()} bytes saved (${pct}% smaller).`, 'ok');
 if (window.Analytics) Analytics.trackToolUse('javascript-minifier');
 } catch (err) {
 T.status('status', 'Minification failed: ' + err.message, 'error');
 }
 }

 T.$('minify').addEventListener('click', run);
 T.$('input').addEventListener('input', debounce(run, 400));
 T.on(['comments', 'blanklines', 'semicolons'], run, 'change');

 T.wireActions({ slug: 'javascript-minifier', getResult: () => lastResult, filename: 'script.min.js', mime: 'text/javascript' });

 T.$('input').value =
 "// Fetch the user record\nfunction getUser(id) {\n const url = 'https://api.example.com/users/' + id;\n const valid = /^[0-9]+$/.test(id);\n\n /* Bail out early if the id is not numeric */\n if (!valid) {\n return null;\n }\n\n return fetch(url).then(function (r) {\n return r.json();\n });\n}";
 run();""",
))

# ---------------------------------------------------------------
# 29. SQL Formatter
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="sql-formatter", name="SQL Formatter", icon="🗄️", cat="developer",
 title="SQL Formatter: Readable Queries with Consistent Keywords",
 description="Format SQL queries with consistent keyword casing and clause-aware indentation, or compact them to a single line. Handles joins and subqueries.",
 tagline="Format SQL with clause-aware indentation and consistent keyword casing.",
 workspace=ws(
 textarea("input", "SQL", "select * from users where active = 1", "input-stats", rows=180),
 row(
 select("keywords", "Keyword case", [("upper", "UPPERCASE"), ("lower", "lowercase"), ("keep", "Leave as written")], selected="upper"),
 select("indent", "Indentation", [("2", "2 spaces"), ("4", "4 spaces"), ("tab", "Tab")], selected="2"),
 switch("commas", "Put commas at the start of lines", False),
 ),
 status_line("status", "Paste a query to format it."),
 HR,
 output("output", "Formatted SQL", "output-stats"),
 buttons(("format", "Format", "primary"), ("compact", "Compact to one line"), ("copy", "Copy result"), ("download", "Download"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Query summary</span></span>
 <div class="table-scroll"><div id="summary"></div></div>
 </div>"""),
 label="SQL formatter",
 ),
 info_block=info(
 features=[
 "Clause-aware line breaks and indentation",
 "Configurable keyword casing",
 "Leading or trailing comma style",
 "Compact mode for single-line output",
 "Query summary listing tables and clauses",
 ],
 howto=[
 "Paste your SQL into the input box.",
 "Choose keyword casing and indentation.",
 "Press Format.",
 "Copy the result into your editor or migration file.",
 ],
 background_title="Formatting conventions and why they matter",
 background_paragraphs=[
 "Uppercase keywords are the long-standing convention, and the reason is practical rather than aesthetic: SQL has no visual distinction between keywords and identifiers, so uppercasing <code>SELECT</code>, <code>FROM</code> and <code>WHERE</code> lets you find the structure of a long query at a glance. Table and column names stay lowercase, which makes the two categories immediately distinguishable without syntax highlighting.",
 "Leading commas look strange at first but solve a real problem. When each line begins with a comma, commenting out a column means deleting or commenting one line without touching its neighbours. With trailing commas, removing the last column in a list leaves a dangling comma that breaks the query, a small annoyance that happens constantly while debugging.",
 "The formatting choice that matters most for reviewability is putting each JOIN and each condition on its own line. A five-table join written on one line is unreadable and hides mistakes; the same join with one table per line makes a missing ON clause or an accidental cross join immediately visible. This formatter breaks on the major clause keywords and indents JOIN conditions under their join, which is the convention most style guides converge on.",
 ],
 ),
 script=r""" let lastResult = '';

 // Clauses that begin a new line at the base indent level
 const MAJOR = ['SELECT', 'FROM', 'WHERE', 'GROUP BY', 'HAVING', 'ORDER BY',
 'LIMIT', 'OFFSET', 'UNION ALL', 'UNION', 'INSERT INTO', 'VALUES', 'UPDATE',
 'SET', 'DELETE FROM', 'CREATE TABLE', 'ALTER TABLE', 'DROP TABLE', 'WITH',
 'RETURNING', 'FETCH'];

 // Joins begin a new line but are conceptually part of FROM
 const JOINS = ['LEFT OUTER JOIN', 'RIGHT OUTER JOIN', 'FULL OUTER JOIN',
 'LEFT JOIN', 'RIGHT JOIN', 'INNER JOIN', 'CROSS JOIN', 'FULL JOIN', 'JOIN'];

 // Indented continuations
 const MINOR = ['AND', 'OR', 'ON'];

 const ALL_KEYWORDS = [...MAJOR, ...JOINS, ...MINOR, 'AS', 'ASC', 'DESC', 'IN',
 'NOT', 'NULL', 'IS', 'LIKE', 'BETWEEN', 'EXISTS', 'CASE', 'WHEN', 'THEN',
 'ELSE', 'END', 'DISTINCT', 'COUNT', 'SUM', 'AVG', 'MIN', 'MAX', 'INTO'];

 function indentString() {
 const v = T.$('indent').value;
 return v === 'tab' ? '\t' : ' '.repeat(Number(v));
 }

 /** Apply the chosen casing to recognised keywords only. */
 function applyCase(sql) {
 const mode = T.$('keywords').value;
 if (mode === 'keep') return sql;

 // Longest first, so GROUP BY is matched before GROUP
 const sorted = [...ALL_KEYWORDS].sort((a, b) => b.length - a.length);
 const pattern = sorted.map((k) => k.replace(/ /g, '\\s+')).join('|');

 return sql.replace(new RegExp(`\\b(${pattern})\\b`, 'gi'), (m) =>
 mode === 'upper' ? m.toUpperCase() : m.toLowerCase());
 }

 function format(sql) {
 const indent = indentString();

 // Normalise whitespace outside of string literals
 let out = sql.replace(/\s+/g, ' ').trim();

 // Break before major clauses
 MAJOR.forEach((kw) => {
 const re = new RegExp(`\\s+(${kw.replace(/ /g, '\\s+')})\\b`, 'gi');
 out = out.replace(re, '\n$1');
 });

 // Break before joins, at the base level
 JOINS.forEach((kw) => {
 const re = new RegExp(`\\s+(${kw.replace(/ /g, '\\s+')})\\b`, 'gi');
 out = out.replace(re, '\n$1');
 });

 // Break before AND / OR / ON, indented one level
 MINOR.forEach((kw) => {
 const re = new RegExp(`\\s+(${kw})\\b`, 'gi');
 out = out.replace(re, `\n${indent}$1`);
 });

 // Column lists: one per line, indented
 out = out.split('\n').map((line) => {
 if (!/^\s*(SELECT|SET|VALUES)\b/i.test(line)) return line;
 const leadingComma = T.$('commas').checked;
 return leadingComma
 ? line.replace(/,\s*/g, `\n${indent}, `)
 : line.replace(/,\s*/g, `,\n${indent}`);
 }).join('\n');

 // Tidy: no trailing spaces, no runs of blank lines
 out = out.split('\n')
 .map((l) => l.replace(/\s+$/, ''))
 .filter((l, i, arr) => l.trim() !== '' || (i > 0 && arr[i - 1].trim() !== ''))
 .join('\n');

 return applyCase(out).trim();
 }

 function compact(sql) {
 return applyCase(sql.replace(/\s+/g, ' ').replace(/\s*([(),])\s*/g, '$1 ').trim());
 }

 function summarise(sql) {
 const mount = T.$('summary');
 mount.innerHTML = '';

 const upper = sql.toUpperCase();
 const rows = [];

 const statement = (upper.match(/^\s*(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|WITH)/) || [])[1];
 if (statement) rows.push(['Statement type', statement]);

 const tables = [...sql.matchAll(/\b(?:FROM|JOIN|INTO|UPDATE)\s+([a-zA-Z_][\w.]*)/gi)]
 .map((m) => m[1]);
 if (tables.length) rows.push(['Tables referenced', [...new Set(tables)].join(', ')]);

 const joinCount = (upper.match(/\bJOIN\b/g) || []).length;
 if (joinCount) rows.push(['Joins', String(joinCount)]);

 const subqueries = (sql.match(/\(\s*SELECT/gi) || []).length;
 if (subqueries) rows.push(['Subqueries', String(subqueries)]);

 if (!/\bWHERE\b/i.test(sql) && /^(\s*)(SELECT|UPDATE|DELETE)/i.test(sql)) {
 rows.push(['⚠ Note', 'No WHERE clause, this affects every row.']);
 }

 if (rows.length) mount.append(T.table(['Property', 'Value'], rows));
 }

 function run(mode) {
 const raw = T.$('input').value;
 T.$('input-stats').textContent = raw.length.toLocaleString() + ' characters';

 if (!raw.trim()) {
 lastResult = '';
 T.setOutput('output', '');
 T.$('summary').innerHTML = '';
 T.status('status', 'Paste a query to format it.', 'muted');
 return;
 }

 lastResult = mode === 'compact' ? compact(raw) : format(raw);
 T.setOutput('output', lastResult);
 T.$('output-stats').textContent = lastResult.split('\n').length + ' lines';

 summarise(raw);
 T.status('status', mode === 'compact' ? 'Compacted to one line.' : 'Formatted.', 'ok');

 if (window.Analytics) Analytics.trackToolUse('sql-formatter');
 }

 // The debounced re-run keeps whichever mode was last chosen.
 let currentMode = 'format';
 const setMode = (mode) => { currentMode = mode; run(mode); };

 T.$('format').addEventListener('click', () => setMode('format'));
 T.$('compact').addEventListener('click', () => setMode('compact'));
 T.$('input').addEventListener('input', debounce(() => run(currentMode), 400));
 T.on(['keywords', 'indent', 'commas'], () => run(currentMode), 'change');

 T.wireActions({ slug: 'sql-formatter', getResult: () => lastResult, filename: 'query.sql' });

 T.$('input').value =
 'select u.id, u.name, count(o.id) as order_count from users u left join orders o on o.user_id = u.id where u.active = 1 and u.created_at > 2024-01-01 group by u.id, u.name having count(o.id) > 5 order by order_count desc limit 20';
 run('format');""",
))

# ---------------------------------------------------------------
# 30. Markdown Preview
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="markdown-preview", name="Markdown Preview", icon="📝", cat="developer",
 title="Markdown Preview: Live Rendering with HTML Export",
 description="Write Markdown and see rendered HTML update live. Supports headings, lists, tables, code blocks, links and task lists. Export the HTML.",
 tagline="Write Markdown on the left, see the rendered result on the right.",
 workspace=ws(
 html_block(""" <div class="workspace__row">
 <div class="field">
 <label class="field__label" for="input">
 <span>Markdown</span>
 <span class="field__hint" id="input-stats"></span>
 </label>
 <textarea class="textarea" id="input" style="min-height:420px" spellcheck="false"></textarea>
 </div>
 <div class="field">
 <span class="field__label"><span>Preview</span><span class="field__hint">Rendered live</span></span>
 <div class="output" id="preview" style="min-height:420px;font-family:var(--font-body);white-space:normal"></div>
 </div>
 </div>"""),
 status_line("status", "Start typing Markdown."),
 buttons(("copy-html", "Copy HTML", "primary"), ("copy-md", "Copy Markdown"), ("download", "Download HTML"), ("sample", "Load sample"), ("clear", "Clear", "ghost"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Generated HTML</span></span>
 <div class="output output--empty" id="html">The HTML will appear here.</div>
 </div>"""),
 label="Markdown preview",
 ),
 info_block=info(
 features=[
 "Live side-by-side preview",
 "Headings, emphasis, lists, tables, blockquotes and code",
 "Task lists, links and images",
 "HTML export",
 "Raw HTML in the source is escaped, not executed",
 ],
 howto=[
 "Type or paste Markdown on the left.",
 "The preview renders as you type.",
 "Copy the generated HTML, or download it as a file.",
 "Use the sample to see the supported syntax.",
 ],
 background_title="Markdown's many dialects",
 background_paragraphs=[
 "Markdown was written by John Gruber in 2004 with a deliberately loose specification, which led to incompatible implementations. CommonMark was created in 2014 to pin down the ambiguities, how many spaces a nested list needs, what happens with mismatched emphasis markers, how to handle a list item containing a blank line. Most modern renderers follow CommonMark, but not all agree on the extensions.",
 "GitHub Flavored Markdown adds the features most people now assume are standard: tables, fenced code blocks with language hints, strikethrough, task lists and automatic URL linking. None of those are in the original Markdown. This renderer implements the common subset of GFM, which covers what documentation and README files actually use.",
 "One security point worth knowing. Original Markdown deliberately passes raw HTML straight through, which is convenient and dangerous, a Markdown file from an untrusted source can contain a script tag. Renderers that accept user content must sanitise the output, and many CVEs have come from doing this incompletely. This tool escapes HTML in the source rather than passing it through, which loses a little flexibility and eliminates the entire risk category.",
 ],
 ),
 script=r""" const SAMPLE = `# Markdown Preview

A **live** renderer with *emphasis*, ~~strikethrough~~ and \`inline code\`.

## Lists

- First item
- Second item
 - Nested item
- Third item

1. Ordered one
2. Ordered two

## Task list

- [x] Write the renderer
- [ ] Add syntax highlighting

## Table

| Feature | Supported |
| --- | --- |
| Headings | Yes |
| Tables | Yes |
| Footnotes | No |

## Code

\`\`\`javascript
function greet(name) {
 return \`Hello, \${name}\`;
}
\`\`\`

> A blockquote for emphasis.

[A link](https://www.123miniapps.online/) and a horizontal rule:

---
`;

 let html = '';

 /**
 * A small CommonMark-ish renderer covering the GFM subset that
 * documentation actually uses.
 *
 * Everything is escaped first, so raw HTML in the source is shown
 * literally rather than executed.
 */
 function render(md) {
 const codeBlocks = [];

 // Stash fenced code blocks before any other processing
 let src = md.replace(/```(\w*)\n([\s\S]*?)```/g, (_, lang, code) => {
 codeBlocks.push({ lang, code });
 return `\u0000CODE${codeBlocks.length - 1}\u0000`;
 });

 src = T.esc(src);

 const lines = src.split('\n');
 const out = [];
 let inList = null; // 'ul' | 'ol' | null
 let inQuote = false;
 let inTable = false;

 const closeBlocks = () => {
 if (inList) { out.push(`</${inList}>`); inList = null; }
 if (inQuote) { out.push('</blockquote>'); inQuote = false; }
 if (inTable) { out.push('</tbody></table>'); inTable = false; }
 };

 for (let i = 0; i < lines.length; i++) {
 const line = lines[i];

 // Stashed code block
 const codeMatch = line.match(/^\u0000CODE(\d+)\u0000$/);
 if (codeMatch) {
 closeBlocks();
 const block = codeBlocks[Number(codeMatch[1])];
 out.push(`<pre><code class="language-${T.esc(block.lang)}">${T.esc(block.code)}</code></pre>`);
 continue;
 }

 // Horizontal rule
 if (/^\s*([-*_])\s*\1\s*\1[\s\-*_]*$/.test(line)) {
 closeBlocks();
 out.push('<hr>');
 continue;
 }

 // Heading
 const heading = line.match(/^(#{1,6})\s+(.*)$/);
 if (heading) {
 closeBlocks();
 const level = heading[1].length;
 out.push(`<h${level}>${inline(heading[2])}</h${level}>`);
 continue;
 }

 // Table row
 if (/^\s*\|.*\|\s*$/.test(line)) {
 const cells = line.trim().slice(1, -1).split('|').map((c) => c.trim());

 // The delimiter row that follows a header
 if (/^[\s|:-]+$/.test(line)) continue;

 if (!inTable) {
 closeBlocks();
 out.push('<table><thead><tr>' +
 cells.map((c) => `<th>${inline(c)}</th>`).join('') +
 '</tr></thead><tbody>');
 inTable = true;
 continue;
 }

 out.push('<tr>' + cells.map((c) => `<td>${inline(c)}</td>`).join('') + '</tr>');
 continue;
 }

 // Blockquote
 const quote = line.match(/^&gt;\s?(.*)$/);
 if (quote) {
 if (!inQuote) { closeBlocks(); out.push('<blockquote>'); inQuote = true; }
 out.push(`<p>${inline(quote[1])}</p>`);
 continue;
 }

 // Task list item
 const task = line.match(/^\s*[-*+]\s+\[([ xX])\]\s+(.*)$/);
 if (task) {
 if (inList !== 'ul') { closeBlocks(); out.push('<ul>'); inList = 'ul'; }
 const checked = task[1].toLowerCase() === 'x' ? ' checked' : '';
 out.push(`<li style="list-style:none;margin-left:-1.2em">` +
 `<input type="checkbox" disabled${checked}> ${inline(task[2])}</li>`);
 continue;
 }

 // Unordered list item
 const ul = line.match(/^(\s*)[-*+]\s+(.*)$/);
 if (ul) {
 if (inList !== 'ul') { closeBlocks(); out.push('<ul>'); inList = 'ul'; }
 const nested = ul[1].length >= 2;
 out.push(`<li${nested ? ' style="margin-left:1.5em"' : ''}>${inline(ul[2])}</li>`);
 continue;
 }

 // Ordered list item
 const ol = line.match(/^\s*\d+[.)]\s+(.*)$/);
 if (ol) {
 if (inList !== 'ol') { closeBlocks(); out.push('<ol>'); inList = 'ol'; }
 out.push(`<li>${inline(ol[1])}</li>`);
 continue;
 }

 // Blank line closes open blocks
 if (!line.trim()) { closeBlocks(); continue; }

 // Paragraph
 closeBlocks();
 out.push(`<p>${inline(line)}</p>`);
 }

 closeBlocks();
 return out.join('\n');
 }

 /** Inline formatting, applied to already-escaped text. */
 function inline(text) {
 return text
 .replace(/`([^`]+)`/g, '<code>$1</code>')
 .replace(/!\[([^\]]*)\]\(([^)\s]+)[^)]*\)/g,
 '<img src="$2" alt="$1" style="max-width:100%">')
 .replace(/\[([^\]]+)\]\(([^)\s]+)[^)]*\)/g,
 '<a href="$2" rel="noopener noreferrer">$1</a>')
 .replace(/\*\*\*([^*]+)\*\*\*/g, '<strong><em>$1</em></strong>')
 .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
 .replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, '<em>$1</em>')
 .replace(/__([^_]+)__/g, '<strong>$1</strong>')
 .replace(/~~([^~]+)~~/g, '<del>$1</del>');
 }

 function run() {
 const md = T.$('input').value;
 T.$('input-stats').textContent =
 `${md.split('\n').length} lines · ${T.words(md).length} words`;

 if (!md.trim()) {
 T.$('preview').innerHTML = '<p class="text-muted">Nothing to preview yet.</p>';
 T.setOutput('html', '');
 T.status('status', 'Start typing Markdown.', 'muted');
 return;
 }

 html = render(md);
 T.$('preview').innerHTML = html;
 T.setOutput('html', html);

 T.status('status', `Rendered ${md.split('\n').length} line(s).`, 'ok');
 if (window.Analytics) Analytics.trackToolUse('markdown-preview');
 }

 T.$('input').addEventListener('input', debounce(run, 200));

 T.$('sample').addEventListener('click', () => { T.$('input').value = SAMPLE; run(); });
 T.$('clear').addEventListener('click', () => { T.$('input').value = ''; run(); T.$('input').focus(); });

 T.$('copy-html').addEventListener('click', () => copyToClipboard(html, 'HTML copied'));
 T.$('copy-md').addEventListener('click', () => copyToClipboard(T.$('input').value, 'Markdown copied'));

 T.$('download').addEventListener('click', () => {
 downloadFile(
 `<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8">\n<title>Document</title>\n` +
 `<style>body{font-family:system-ui,sans-serif;max-width:70ch;margin:40px auto;padding:0 20px;line-height:1.6}` +
 `pre{background:#f4f4f4;padding:12px;overflow:auto;border-radius:6px}` +
 `code{background:#f4f4f4;padding:2px 4px;border-radius:3px}` +
 `table{border-collapse:collapse}th,td{border:1px solid #ddd;padding:6px 10px}</style>\n` +
 `</head><body>\n${html}\n</body></html>`,
 'document.html', 'text/html');
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Markdown Preview | 123MiniApps' }));

 T.$('input').value = SAMPLE;
 run();""",
))

# ---------------------------------------------------------------
# 31. Cron Expression Builder
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="cron-expression-builder", name="Cron Expression Builder", icon="⏰", cat="developer",
 title="Cron Expression Builder: Read and Write Cron Schedules",
 description="Build and read cron schedules with a plain-English explanation and the next five run times. Includes presets for common schedules.",
 tagline="Build cron schedules and read them back in plain English, with the next run times.",
 workspace=ws(
 html_block(""" <div class="field">
 <label class="field__label" for="expression">
 <span>Cron expression</span>
 <span class="field__hint">minute hour day-of-month month day-of-week</span>
 </label>
 <input class="input font-mono" id="expression" type="text" value="0 9 * * 1-5"
 style="font-size:var(--text-xl);height:60px" autocomplete="off" spellcheck="false">
 </div>"""),
 html_block(""" <div class="display" style="padding:var(--space-6)">
 <span class="display__label" style="font-size:var(--text-lg);color:var(--text-primary)" id="explanation">, </span>
 </div>"""),
 status_line("status", "Enter a cron expression."),
 HR,
 row(
 text_input("f-minute", "Minute (0-59)", "0", "0"),
 text_input("f-hour", "Hour (0-23)", "9", "9"),
 text_input("f-dom", "Day of month (1-31)", "*", "*"),
 text_input("f-month", "Month (1-12)", "*", "*"),
 text_input("f-dow", "Day of week (0-6)", "1-5", "1-5"),
 ),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Next five runs</span><span class="field__hint">In your local timezone</span></span>
 <div class="table-scroll"><div id="runs"></div></div>
 </div>"""),
 buttons(("copy", "Copy expression", "primary"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Common schedules</span></span>
 <div class="chip-grid" id="presets"></div>
 </div>"""),
 label="Cron expression builder",
 ),
 info_block=info(
 features=[
 "Two-way editing, expression or individual fields",
 "Plain-English explanation of any schedule",
 "Next five run times calculated locally",
 "Twelve common presets",
 "Validates ranges, steps and lists",
 ],
 howto=[
 "Type a cron expression, or fill in the five fields.",
 "Read the plain-English explanation.",
 "Check the next five run times look right.",
 "Copy the expression into your crontab.",
 ],
 background_title="Reading cron expressions",
 background_paragraphs=[
 "The five fields are minute, hour, day of month, month and day of week, in that order. An asterisk means every value. Lists use commas (<code>1,15</code>), ranges use hyphens (<code>1-5</code>), and steps use a slash (<code>*/15</code> means every fifteenth). So <code>0 9 * * 1-5</code> runs at nine o'clock on weekdays.",
 "The trap that catches nearly everyone is the interaction between day-of-month and day-of-week. When both are restricted, cron runs the job if <em>either</em> matches, not both, so <code>0 0 1 * 1</code> runs on the first of the month <em>and</em> every Monday, not only on Mondays that fall on the first. If you need an AND, you have to add a guard inside the job itself.",
 "Two operational points. Cron uses the server's local timezone, so a job scheduled for 02:30 may run twice or not at all on daylight-saving transition days, schedule anything critical outside the 01:00 to 03:00 window, or use UTC. And a job scheduled every minute will start again even if the previous run has not finished, so long-running jobs need a lockfile or they will pile up and exhaust the machine.",
 ],
 ),
 script=r""" const PRESETS = [
 ['Every minute', '* * * * *'],
 ['Every 5 minutes', '*/5 * * * *'],
 ['Every 15 minutes', '*/15 * * * *'],
 ['Every hour', '0 * * * *'],
 ['Every day at midnight', '0 0 * * *'],
 ['Every weekday at 9am', '0 9 * * 1-5'],
 ['Every Monday at 9am', '0 9 * * 1'],
 ['Twice a day', '0 0,12 * * *'],
 ['First of the month', '0 0 1 * *'],
 ['Every Sunday at 3am', '0 3 * * 0'],
 ['Quarterly', '0 0 1 1,4,7,10 *'],
 ['Weekends at noon', '0 12 * * 0,6']
 ];

 const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
 'July', 'August', 'September', 'October', 'November', 'December'];
 const DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

 const RANGES = {
 minute: [0, 59], hour: [0, 23], dom: [1, 31], month: [1, 12], dow: [0, 6]
 };

 let updating = false;

 /**
 * Expand one cron field into the set of values it matches.
 * @returns {number[]|null} null when the field is invalid
 */
 function expand(field, name) {
 const [lo, hi] = RANGES[name];
 const values = new Set();

 for (const part of String(field).split(',')) {
 const token = part.trim();
 if (!token) return null;

 const stepMatch = token.match(/^(.+?)\/(\d+)$/);
 const step = stepMatch ? Number(stepMatch[2]) : 1;
 const base = stepMatch ? stepMatch[1] : token;

 if (step < 1) return null;

 let start, end;

 if (base === '*') {
 start = lo; end = hi;
 } else if (/^\d+-\d+$/.test(base)) {
 [start, end] = base.split('-').map(Number);
 } else if (/^\d+$/.test(base)) {
 start = end = Number(base);
 } else {
 return null;
 }

 if (isNaN(start) || isNaN(end) || start < lo || end > hi || start > end) return null;

 for (let v = start; v <= end; v += step) values.add(v);
 }

 return values.size ? [...values].sort((a, b) => a - b) : null;
 }

 /** Describe one field in plain English. */
 function describeField(field, name) {
 const [lo, hi] = RANGES[name];
 if (field === '*') return null;

 const stepMatch = field.match(/^\*\/(\d+)$/);
 if (stepMatch) {
 const n = Number(stepMatch[1]);
 const unit = { minute: 'minute', hour: 'hour', dom: 'day', month: 'month', dow: 'day' }[name];
 return `every ${n === 1 ? '' : n + ' '}${unit}${n === 1 ? '' : 's'}`;
 }

 const values = expand(field, name);
 if (!values) return null;

 const list = (arr, fmt) => {
 const parts = arr.map(fmt);
 if (parts.length === 1) return parts[0];
 if (parts.length === 2) return parts.join(' and ');
 if (parts.length > 5) return `${parts.length} selected values`;
 return parts.slice(0, -1).join(', ') + ' and ' + parts[parts.length - 1];
 };

 if (name === 'month') return list(values, (v) => MONTHS[v - 1]);
 if (name === 'dow') return list(values, (v) => DAYS[v % 7]);
 if (name === 'dom') return list(values, (v) => 'the ' + ordinal(v));

 void lo; void hi;
 return list(values, String);
 }

 function ordinal(n) {
 const s = ['th', 'st', 'nd', 'rd'];
 const v = n % 100;
 return n + (s[(v - 20) % 10] || s[v] || s[0]);
 }

 function explain(parts) {
 const [minute, hour, dom, month, dow] = parts;

 // Time of day
 let time;
 const minutes = expand(minute, 'minute');
 const hours = expand(hour, 'hour');

 if (minute === '*' && hour === '*') {
 time = 'Every minute';
 } else if (hour === '*' && minutes && minutes.length === 1) {
 time = `At ${minutes[0]} minute(s) past every hour`;
 } else if (minute.startsWith('*/')) {
 time = `Every ${minute.slice(2)} minutes`;
 } else if (minutes && hours && minutes.length === 1 && hours.length <= 3) {
 time = 'At ' + hours.map((h) => `${T.pad2(h)}:${T.pad2(minutes[0])}`).join(' and ');
 } else {
 const m = describeField(minute, 'minute');
 const h = describeField(hour, 'hour');
 time = `At minute ${m || 'every'}${h ? `, hour ${h}` : ''}`;
 }

 const bits = [time];

 const domText = describeField(dom, 'dom');
 const dowText = describeField(dow, 'dow');
 const monthText = describeField(month, 'month');

 if (domText && dowText) {
 bits.push(`on ${domText} OR on ${dowText} (cron treats these as OR, not AND)`);
 } else if (domText) {
 bits.push(`on ${domText}`);
 } else if (dowText) {
 bits.push(`on ${dowText}`);
 }

 if (monthText) bits.push(`in ${monthText}`);

 return bits.join(' ') + '.';
 }

 /** Find the next N times the expression matches, by scanning forward. */
 function nextRuns(parts, count = 5) {
 const [minute, hour, dom, month, dow] = parts;
 const mins = expand(minute, 'minute');
 const hrs = expand(hour, 'hour');
 const doms = expand(dom, 'dom');
 const months = expand(month, 'month');
 const dows = expand(dow, 'dow');

 if (!mins || !hrs || !doms || !months || !dows) return [];

 const domRestricted = dom !== '*';
 const dowRestricted = dow !== '*';

 const runs = [];
 const cursor = new Date();
 cursor.setSeconds(0, 0);
 cursor.setMinutes(cursor.getMinutes() + 1);

 // Scan at most a year ahead, one minute at a time
 const LIMIT = 366 * 24 * 60;

 for (let i = 0; i < LIMIT && runs.length < count; i++) {
 const matchesMonth = months.includes(cursor.getMonth() + 1);
 const matchesHour = hrs.includes(cursor.getHours());
 const matchesMinute = mins.includes(cursor.getMinutes());

 // The OR rule: when both day fields are restricted, either may match
 const matchesDom = doms.includes(cursor.getDate());
 const matchesDow = dows.includes(cursor.getDay());
 const matchesDay = domRestricted && dowRestricted
 ? matchesDom || matchesDow
 : domRestricted ? matchesDom
 : dowRestricted ? matchesDow
 : true;

 if (matchesMonth && matchesDay && matchesHour && matchesMinute) {
 runs.push(new Date(cursor));
 }

 cursor.setMinutes(cursor.getMinutes() + 1);
 }

 return runs;
 }

 function parse() {
 const raw = T.$('expression').value.trim().replace(/\s+/g, ' ');
 const parts = raw.split(' ');

 if (parts.length !== 5) {
 T.status('status', `A cron expression has five fields; this has ${parts.length}.`, 'error');
 T.$('explanation').textContent = ', ';
 T.$('runs').innerHTML = '';
 return;
 }

 const names = ['minute', 'hour', 'dom', 'month', 'dow'];
 for (let i = 0; i < 5; i++) {
 if (!expand(parts[i], names[i])) {
 T.status('status', `The ${names[i]} field “${parts[i]}” is not valid.`, 'error');
 T.$('explanation').textContent = ', ';
 T.$('runs').innerHTML = '';
 return;
 }
 }

 if (!updating) {
 updating = true;
 ['f-minute', 'f-hour', 'f-dom', 'f-month', 'f-dow']
 .forEach((id, i) => { T.$(id).value = parts[i]; });
 updating = false;
 }

 T.$('explanation').textContent = explain(parts);

 const runs = nextRuns(parts);
 const mount = T.$('runs');
 mount.innerHTML = '';

 if (runs.length) {
 mount.append(T.table(
 ['Run', 'Date and time', 'In'],
 runs.map((d, i) => [
 '#' + (i + 1),
 d.toLocaleString(undefined, { weekday: 'short', year: 'numeric', month: 'short',
 day: 'numeric', hour: '2-digit', minute: '2-digit' }),
 relative(d)
 ])
 ));
 T.status('status', `Valid. Next run ${relative(runs[0])}.`, 'ok');
 } else {
 T.status('status', 'Valid, but no runs found in the next year, check the day and month fields.', 'warn');
 }

 if (window.Analytics) Analytics.trackToolUse('cron-expression-builder');
 }

 function relative(date) {
 const diff = date - Date.now();
 const mins = Math.round(diff / 60000);
 if (mins < 60) return `${mins} minute${mins === 1 ? '' : 's'}`;
 const hours = Math.round(mins / 60);
 if (hours < 48) return `${hours} hour${hours === 1 ? '' : 's'}`;
 return `${Math.round(hours / 24)} days`;
 }

 function fromFields() {
 if (updating) return;
 updating = true;
 T.$('expression').value = ['f-minute', 'f-hour', 'f-dom', 'f-month', 'f-dow']
 .map((id) => T.$(id).value.trim() || '*').join(' ');
 updating = false;
 parse();
 }

 T.$('expression').addEventListener('input', debounce(parse, 250));
 T.on(['f-minute', 'f-hour', 'f-dom', 'f-month', 'f-dow'], debounce(fromFields, 250));

 T.$('copy').addEventListener('click', () =>
 copyToClipboard(T.$('expression').value.trim(), 'Expression copied'));
 T.$('share').addEventListener('click', () => shareLink({ title: 'Cron Expression Builder | 123MiniApps' }));

 const presetMount = T.$('presets');
 PRESETS.forEach(([name, expr]) => {
 const chip = el('button', { className: 'chip', attrs: { type: 'button', title: expr }, text: name });
 chip.addEventListener('click', () => { T.$('expression').value = expr; parse(); });
 presetMount.append(chip);
 });

 parse();""",
))

# ---------------------------------------------------------------
# 32. HTTP Status Codes
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="http-status-codes", name="HTTP Status Codes", icon="📡", cat="developer",
 title="HTTP Status Codes: Searchable Reference with Guidance",
 description="A searchable reference for every HTTP status code, with what each means, when to use it, and the RFC that defines it.",
 tagline="Every HTTP status code, searchable, with guidance on when to use each one.",
 workspace=ws(
 html_block(""" <div class="searchbar" style="max-width:none;margin-bottom:var(--space-5)">
 <label class="sr-only" for="search">Search status codes</label>
 <div class="searchbar__field">
 <span class="searchbar__icon" aria-hidden="true">
 <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
 </span>
 <input class="searchbar__input" id="search" type="search" placeholder="Search by code, name or meaning, try 404, redirect, or teapot" autocomplete="off">
 </div>
 </div>"""),
 html_block(""" <div class="chip-grid" id="classes" style="margin-bottom:var(--space-5)"></div>"""),
 status_line("status", ""),
 html_block(""" <div id="results"></div>"""),
 buttons(("copy", "Copy visible codes", "primary"), ("share", "Share tool", "ghost")),
 label="HTTP status code reference",
 ),
 info_block=info(
 features=[
 "Every registered status code across all five classes",
 "Instant filtering by code, name or description",
 "Guidance on when each code is appropriate",
 "Class filters for 1xx through 5xx",
 "Works offline once the page is cached",
 ],
 howto=[
 "Type a code or a word into the search box.",
 "Or filter by class using the buttons.",
 "Read the description and the usage guidance.",
 "Copy the filtered list if you need it elsewhere.",
 ],
 background_title="Status codes people commonly get wrong",
 background_paragraphs=[
 "The 401 and 403 distinction is the most frequently muddled. <strong>401 Unauthorized</strong> actually means unauthenticated, the request lacks valid credentials, and retrying with credentials might work. <strong>403 Forbidden</strong> means the server knows who you are and you still may not have it; retrying with the same credentials will not help. A 401 response is required to include a <code>WWW-Authenticate</code> header telling the client how to authenticate.",
 "Redirects have a subtlety that breaks form submissions. <strong>301</strong> and <strong>302</strong> historically allowed clients to change a POST into a GET when following the redirect, and most browsers do exactly that. <strong>307</strong> and <strong>308</strong> were introduced to guarantee the method and body are preserved. If you are redirecting anything other than a GET, use 307 or 308.",
 "Two more worth knowing. <strong>422 Unprocessable Content</strong> is the right code when a request is syntactically valid but semantically wrong, well-formed JSON that fails validation, where many APIs incorrectly return 400. And <strong>429 Too Many Requests</strong> should always be accompanied by a <code>Retry-After</code> header; without it, clients have no way to back off sensibly and will usually just hammer you again.",
 ],
 ),
 script=r""" const CODES = [
 [100, 'Continue', '1xx', 'The client should continue with its request. Sent in response to an Expect: 100-continue header.', 'Rarely set manually, servers handle this automatically.'],
 [101, 'Switching Protocols', '1xx', 'The server is switching protocols as requested, typically to WebSocket.', 'Sent by WebSocket handshakes.'],
 [102, 'Processing', '1xx', 'The server has received the request and is working on it, but no response is available yet.', 'WebDAV. Largely superseded by 103.'],
 [103, 'Early Hints', '1xx', 'Sends preliminary headers, usually Link headers for preloading, before the final response.', 'Useful for preloading critical assets while the server prepares the page.'],

 [200, 'OK', '2xx', 'The request succeeded. The meaning of success depends on the method.', 'The default success response for GET, PUT and PATCH.'],
 [201, 'Created', '2xx', 'The request succeeded and a new resource was created.', 'Use for POST that creates a resource. Include a Location header pointing at it.'],
 [202, 'Accepted', '2xx', 'The request was accepted for processing but has not been completed.', 'Use for asynchronous jobs. Give the client a way to poll for the result.'],
 [204, 'No Content', '2xx', 'The request succeeded and there is deliberately no response body.', 'Ideal for DELETE, and for PUT where returning the resource adds nothing.'],
 [206, 'Partial Content', '2xx', 'The server is delivering part of the resource, as requested by a Range header.', 'Video streaming and resumable downloads.'],

 [301, 'Moved Permanently', '3xx', 'The resource has permanently moved to a new URL.', 'Use when changing a URL for good, search engines transfer ranking. May turn POST into GET.'],
 [302, 'Found', '3xx', 'The resource is temporarily at a different URL.', 'Temporary redirects. May turn POST into GET; prefer 307 if that matters.'],
 [303, 'See Other', '3xx', 'The response can be found at another URL, which should be fetched with GET.', 'The correct redirect after a successful POST, to prevent double submission.'],
 [304, 'Not Modified', '3xx', 'The cached version is still current, so no body is sent.', 'Sent in response to conditional requests using If-None-Match or If-Modified-Since.'],
 [307, 'Temporary Redirect', '3xx', 'Temporary redirect that preserves the request method and body.', 'Use instead of 302 when redirecting a POST, PUT or DELETE.'],
 [308, 'Permanent Redirect', '3xx', 'Permanent redirect that preserves the request method and body.', 'Use instead of 301 when redirecting a non-GET request.'],

 [400, 'Bad Request', '4xx', 'The server cannot process the request because it is malformed.', 'Use for syntax errors. If the syntax is fine but the content is invalid, 422 is more precise.'],
 [401, 'Unauthorized', '4xx', 'Authentication is required and has failed or not been provided.', 'Really means "unauthenticated". Must include a WWW-Authenticate header.'],
 [402, 'Payment Required', '4xx', 'Reserved for future use; occasionally used for quota or billing failures.', 'Some APIs use it when a subscription has lapsed.'],
 [403, 'Forbidden', '4xx', 'The server understood the request but refuses to authorise it.', 'The client is authenticated but lacks permission. Retrying will not help.'],
 [404, 'Not Found', '4xx', 'The server cannot find the requested resource.', 'Also used to hide the existence of a resource from unauthorised clients.'],
 [405, 'Method Not Allowed', '4xx', 'The method is known but not supported for this resource.', 'Must include an Allow header listing the methods that are supported.'],
 [406, 'Not Acceptable', '4xx', 'No representation matches the client’s Accept headers.', 'Rare in practice; most servers return their default format instead.'],
 [408, 'Request Timeout', '4xx', 'The server timed out waiting for the request.', 'Usually a slow or stalled client connection.'],
 [409, 'Conflict', '4xx', 'The request conflicts with the current state of the resource.', 'Edit conflicts, duplicate unique keys, or version mismatches.'],
 [410, 'Gone', '4xx', 'The resource was deliberately removed and will not return.', 'More informative than 404 when you know something was deleted permanently.'],
 [413, 'Content Too Large', '4xx', 'The request body is larger than the server will accept.', 'File upload limits. Tell the client the maximum size.'],
 [415, 'Unsupported Media Type', '4xx', 'The request body format is not supported.', 'Wrong Content-Type, for example XML sent to a JSON-only endpoint.'],
 [418, 'I’m a teapot', '4xx', 'The server refuses to brew coffee because it is, permanently, a teapot.', 'An April Fools joke from RFC 2324 that survives in many frameworks.'],
 [422, 'Unprocessable Content', '4xx', 'The request is well-formed but semantically invalid.', 'The right code for validation failures on syntactically valid JSON.'],
 [429, 'Too Many Requests', '4xx', 'The client has sent too many requests in a given period.', 'Rate limiting. Always include a Retry-After header.'],
 [451, 'Unavailable For Legal Reasons', '4xx', 'Access is denied for legal reasons such as a court order.', 'The number references Fahrenheit 451.'],

 [500, 'Internal Server Error', '5xx', 'The server hit an unexpected condition it cannot handle.', 'The catch-all for unhandled exceptions. Never leak stack traces in the body.'],
 [501, 'Not Implemented', '5xx', 'The server does not support the functionality required.', 'The method is not recognised at all.'],
 [502, 'Bad Gateway', '5xx', 'A server acting as a gateway received an invalid upstream response.', 'Usually a crashed or unreachable backend behind a proxy.'],
 [503, 'Service Unavailable', '5xx', 'The server is temporarily unable to handle the request.', 'Maintenance or overload. Include Retry-After if you know how long.'],
 [504, 'Gateway Timeout', '5xx', 'A gateway did not receive a timely upstream response.', 'The backend is too slow, or a timeout is set too low.'],
 [507, 'Insufficient Storage', '5xx', 'The server cannot store the representation needed to complete the request.', 'WebDAV, and occasionally disk-full conditions.'],
 [511, 'Network Authentication Required', '5xx', 'The client must authenticate to gain network access.', 'Captive portals on public wifi.']
 ];

 const CLASS_INFO = {
 '1xx': ['Informational', 'The request was received and the process is continuing.'],
 '2xx': ['Success', 'The request was received, understood and accepted.'],
 '3xx': ['Redirection', 'Further action is needed to complete the request.'],
 '4xx': ['Client error', 'The request contains bad syntax or cannot be fulfilled.'],
 '5xx': ['Server error', 'The server failed to fulfil a valid request.']
 };

 let activeClass = 'all';

 function visible() {
 const query = T.$('search').value.trim().toLowerCase();

 return CODES.filter(([code, name, cls, description, guidance]) => {
 if (activeClass !== 'all' && cls !== activeClass) return false;
 if (!query) return true;
 return String(code).includes(query) ||
 name.toLowerCase().includes(query) ||
 description.toLowerCase().includes(query) ||
 guidance.toLowerCase().includes(query) ||
 cls === query;
 });
 }

 function colourFor(cls) {
 return { '1xx': 'var(--info)', '2xx': 'var(--success)', '3xx': 'var(--warning)',
 '4xx': 'var(--danger)', '5xx': 'var(--danger)' }[cls];
 }

 function render() {
 const mount = T.$('results');
 mount.innerHTML = '';

 const list = visible();

 if (!list.length) {
 mount.append(el('div', { className: 'empty-state' }, [
 el('div', { className: 'empty-state__icon', text: '🔍', attrs: { 'aria-hidden': 'true' } }),
 el('p', { text: 'No status codes match that search.' })
 ]));
 T.status('status', 'No matches.', 'warn');
 return;
 }

 let currentClass = null;

 list.forEach(([code, name, cls, description, guidance]) => {
 if (cls !== currentClass) {
 currentClass = cls;
 const [label, blurb] = CLASS_INFO[cls];
 mount.append(el('h3', {
 className: 'mt-8 mb-3',
 text: `${cls}, ${label}`,
 style: { color: colourFor(cls) }
 }));
 mount.append(el('p', { className: 'text-sm text-muted mb-4', text: blurb }));
 }

 const card = el('div', { className: 'info-panel mb-3' }, [
 el('div', { className: 'flex items-center gap-3 mb-2' }, [
 el('span', {
 className: 'result__value',
 text: String(code),
 style: { fontSize: 'var(--text-2xl)', color: colourFor(cls) }
 }),
 el('strong', { text: name, style: { fontSize: 'var(--text-lg)' } })
 ]),
 el('p', { className: 'text-sm', text: description }),
 el('p', { className: 'text-sm text-muted mt-2', text: '→ ' + guidance })
 ]);

 mount.append(card);
 });

 T.status('status', `Showing ${list.length} of ${CODES.length} status codes.`, 'ok');
 }

 function renderClasses() {
 const mount = T.$('classes');
 mount.innerHTML = '';

 [['all', 'All codes'], ...Object.entries(CLASS_INFO).map(([k, v]) => [k, `${k} ${v[0]}`])]
 .forEach(([key, label]) => {
 const chip = el('button', { className: 'chip', attrs: { type: 'button' }, text: label });

 if (key === activeClass) {
 chip.style.borderColor = 'var(--accent-primary)';
 chip.style.color = 'var(--accent-primary)';
 }

 chip.addEventListener('click', () => {
 activeClass = key;
 renderClasses();
 render();
 });

 mount.append(chip);
 });
 }

 T.$('search').addEventListener('input', debounce(render, 150));

 T.$('copy').addEventListener('click', () => {
 const text = visible().map(([code, name, description]) =>
 `${code} ${name}, ${description}`).join('\n');
 copyToClipboard(text, 'Status codes copied');
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'HTTP Status Codes | 123MiniApps' }));

 renderClasses();
 render();
 if (window.Analytics) Analytics.trackToolUse('http-status-codes');""",
))
