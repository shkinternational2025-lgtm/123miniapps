#!/usr/bin/env python3
# ============================================
# 123MiniApps.online v2.0
# File: tools_generator.py
# Purpose: The 10 remaining Generators
# (ids 45-54; 43 and 44 are hand-built).
# ============================================

from toolkit import (
 tool, ws, info, row, textarea, text_input, number_input, select, switch,
 slider, output, status_line, buttons, color_input, canvas,
 STD_ACTIONS, HR, html_block,
)

PAGES = []

# ---------------------------------------------------------------
# 45. UUID Generator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="uuid-generator", name="UUID Generator", icon="🆔", cat="generator",
 title="UUID Generator: RFC 4122 v4 and v7, Bulk Generation",
 description="Generate RFC 4122 version 4 and version 7 UUIDs, one at a time or a thousand at once, using cryptographically secure randomness.",
 tagline="Generate v4 and time-ordered v7 UUIDs using cryptographic randomness.",
 workspace=ws(
 row(
 select("version", "Version", [
 ("4", "v4, random (the usual choice)"),
 ("7", "v7, time-ordered, sorts chronologically"),
 ("nil", "Nil UUID, all zeros"),
 ], selected="4"),
 number_input("count", "How many", "10", "10", step="1", min=1, max=1000),
 select("format", "Format", [
 ("standard", "Standard, 8-4-4-4-12"),
 ("upper", "Uppercase"),
 ("nohyphen", "No hyphens"),
 ("braces", "Braces {…}"),
 ("urn", "URN, urn:uuid:…"),
 ], selected="standard"),
 ),
 status_line("status", "Press Generate."),
 HR,
 output("output", "UUIDs", "output-stats", "Your UUIDs will appear here."),
 buttons(("generate", "Generate", "primary"), ("copy", "Copy result"), ("download", "Download"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Anatomy of the first UUID</span></span>
 <div class="table-scroll"><div id="anatomy"></div></div>
 </div>"""),
 label="UUID generator",
 ),
 info_block=info(
 features=[
 "Version 4 (random) and version 7 (time-ordered)",
 "Bulk generation up to 1,000 at once",
 "Five output formats including URN and brace notation",
 "Cryptographically secure randomness via the Web Crypto API",
 "Field-by-field breakdown of the generated value",
 ],
 howto=[
 "Choose a version, v4 unless you need sortability.",
 "Set how many you need.",
 "Press Generate.",
 "Copy the list or download it as a text file.",
 ],
 background_title="Choosing between v4 and v7",
 background_paragraphs=[
 "A version 4 UUID is 122 random bits with six bits reserved for version and variant markers. That gives about 5.3 × 10³⁶ possible values, which is enough that collisions are not a practical concern, you would need to generate roughly a billion per second for 85 years to reach a 50% chance of a single collision. This tool draws from <code>crypto.getRandomValues()</code>, not <code>Math.random()</code>, which matters: <code>Math.random()</code> is not cryptographically secure and its output can be predicted from previous values.",
 "Version 7 was standardised in RFC 9562 in 2024 and solves a real database problem. Because v4 UUIDs are entirely random, inserting them as a primary key scatters writes across the whole B-tree index, which fragments pages and slows inserts badly at scale. A v7 UUID puts a 48-bit millisecond timestamp in the high bits, so newly generated values sort after older ones and inserts land at the end of the index. If you are choosing a primary key type today, v7 is usually the better default.",
 "Two things v7 gives up. It leaks the creation time of the record, which may matter if the identifier is exposed publicly. And it is only sortable to millisecond precision, values generated within the same millisecond order randomly among themselves, so it is not a substitute for a real sequence when strict ordering matters.",
 ],
 ),
 script=r""" let uuids = [];

 /** RFC 4122 version 4: 122 random bits with version and variant set. */
 function v4() {
 const bytes = new Uint8Array(16);
 crypto.getRandomValues(bytes);

 bytes[6] = (bytes[6] & 0x0f) | 0x40; // version 4
 bytes[8] = (bytes[8] & 0x3f) | 0x80; // variant 10xx

 return bytesToUuid(bytes);
 }

 /** RFC 9562 version 7: 48-bit millisecond timestamp, then randomness. */
 function v7() {
 const bytes = new Uint8Array(16);
 crypto.getRandomValues(bytes);

 const ms = BigInt(Date.now());
 for (let i = 0; i < 6; i++) {
 bytes[i] = Number((ms >> BigInt(8 * (5 - i))) & 0xffn);
 }

 bytes[6] = (bytes[6] & 0x0f) | 0x70; // version 7
 bytes[8] = (bytes[8] & 0x3f) | 0x80; // variant 10xx

 return bytesToUuid(bytes);
 }

 function bytesToUuid(bytes) {
 const hex = [...bytes].map((b) => b.toString(16).padStart(2, '0')).join('');
 return [
 hex.slice(0, 8), hex.slice(8, 12), hex.slice(12, 16),
 hex.slice(16, 20), hex.slice(20, 32)
 ].join('-');
 }

 const NIL = '00000000-0000-0000-0000-000000000000';

 function applyFormat(uuid) {
 switch (T.$('format').value) {
 case 'upper': return uuid.toUpperCase();
 case 'nohyphen': return uuid.replace(/-/g, '');
 case 'braces': return '{' + uuid + '}';
 case 'urn': return 'urn:uuid:' + uuid;
 default: return uuid;
 }
 }

 function generate() {
 const count = Math.min(1000, Math.max(1, Math.floor(T.num(T.$('count').value) || 1)));
 const version = T.$('version').value;

 const make = version === '4' ? v4 : version === '7' ? v7 : () => NIL;
 uuids = Array.from({ length: count }, make);

 const formatted = uuids.map(applyFormat);
 T.setOutput('output', formatted.join('\n'));
 T.$('output-stats').textContent = `${count} UUID${count === 1 ? '' : 's'}`;

 renderAnatomy(uuids[0], version);

 // Sanity check that we are not producing duplicates
 const unique = new Set(uuids).size;
 T.status('status',
 unique === count
 ? `Generated ${count} UUID(s), all unique.`
 : `Generated ${count}, but only ${unique} were unique, this should not happen.`,
 unique === count ? 'ok' : 'error');
 }

 function renderAnatomy(uuid, version) {
 const mount = T.$('anatomy');
 mount.innerHTML = '';
 if (!uuid || version === 'nil') return;

 const hex = uuid.replace(/-/g, '');
 const rows = [];

 if (version === '7') {
 const ms = parseInt(hex.slice(0, 12), 16);
 rows.push(['Timestamp (48 bits)', hex.slice(0, 12), new Date(ms).toISOString()]);
 rows.push(['Version', hex[12], 'Version ' + parseInt(hex[12], 16)]);
 rows.push(['Random A (12 bits)', hex.slice(13, 16), ', ']);
 rows.push(['Variant', hex[16], 'RFC 4122 / 9562']);
 rows.push(['Random B (62 bits)', hex.slice(17), ', ']);
 } else {
 rows.push(['Random (48 bits)', hex.slice(0, 12), ', ']);
 rows.push(['Version', hex[12], 'Version ' + parseInt(hex[12], 16)]);
 rows.push(['Random (12 bits)', hex.slice(13, 16), ', ']);
 rows.push(['Variant', hex[16], 'RFC 4122']);
 rows.push(['Random (62 bits)', hex.slice(17), ', ']);
 }

 mount.append(T.table(['Field', 'Hex', 'Meaning'], rows));
 }

 T.$('generate').addEventListener('click', generate);
 T.on(['version', 'format'], generate, 'change');
 T.$('count').addEventListener('input', debounce(generate, 250));

 T.wireActions({
 slug: 'uuid-generator',
 getResult: () => uuids.map(applyFormat).join('\n'),
 filename: 'uuids.txt'
 });

 generate();""",
))

# ---------------------------------------------------------------
# 46. Random Number Generator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="random-number-generator", name="Random Number Generator", icon="🎲", cat="generator",
 title="Random Number Generator: Any Range, With or Without Repeats",
 description="Draw random numbers in any range using cryptographic randomness. Unique-only mode, decimals, bulk draws and a distribution summary.",
 tagline="Draw random numbers in any range, with cryptographic randomness, not Math.random().",
 workspace=ws(
 row(
 number_input("min", "Minimum", "1", "1"),
 number_input("max", "Maximum", "100", "100"),
 number_input("count", "How many", "10", "10", step="1", min=1, max=10000),
 ),
 row(
 switch("unique", "No repeats (draw without replacement)", False),
 switch("decimals", "Allow decimals", False),
 select("sort", "Order", [("draw", "Order drawn"), ("asc", "Lowest first"), ("desc", "Highest first")], selected="draw"),
 ),
 status_line("status", "Set a range and press Generate."),
 HR,
 output("output", "Numbers", "output-stats", "Your numbers will appear here."),
 buttons(("generate", "Generate", "primary"), ("copy", "Copy result"), ("download", "Download"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result"><span class="result__value" id="r-sum" style="font-size:var(--text-2xl)">, </span><span class="result__label">Sum</span></div>
 <div class="result"><span class="result__value" id="r-mean" style="font-size:var(--text-2xl)">, </span><span class="result__label">Mean</span></div>
 <div class="result"><span class="result__value" id="r-min" style="font-size:var(--text-2xl)">, </span><span class="result__label">Lowest</span></div>
 <div class="result"><span class="result__value" id="r-max" style="font-size:var(--text-2xl)">, </span><span class="result__label">Highest</span></div>
 </div>"""),
 label="Random number generator",
 ),
 info_block=info(
 features=[
 "Any integer or decimal range",
 "Draw with or without replacement",
 "Up to 10,000 numbers at once",
 "Summary statistics for the draw",
 "Cryptographically secure, uniformly distributed",
 ],
 howto=[
 "Set the minimum and maximum.",
 "Choose how many numbers you need.",
 "Turn on no-repeats for lottery-style draws.",
 "Press Generate.",
 ],
 background_title="Why the source of randomness matters",
 background_paragraphs=[
 "JavaScript's <code>Math.random()</code> is a pseudo-random generator seeded from an internal state. It is fast and statistically fine for animations or shuffling a playlist, but it is not unpredictable: given enough consecutive outputs, its internal state can be recovered and all future values predicted. That makes it unsuitable for anything where someone benefits from guessing the result, prize draws, tokens, passwords, or shuffling cards for money.",
 "This tool uses <code>crypto.getRandomValues()</code>, which draws from the operating system's cryptographically secure entropy pool. Predicting its output requires breaking the underlying CSPRNG, not merely observing previous values.",
 "There is a second, subtler trap. The obvious way to map a random integer into a range is <code>value % range</code>, but unless the range divides evenly into the generator's output space, the lower values in the range come up slightly more often. For a small range the bias is tiny; for a large one it can be several percent. This tool uses rejection sampling, discarding and redrawing values that fall in the uneven tail, which makes the distribution exactly uniform at the cost of an occasional extra draw.",
 ],
 ),
 script=r""" let numbers = [];

 /** Uniform random float in [min, max). */
 function randomFloat(min, max) {
 const buf = new Uint32Array(1);
 crypto.getRandomValues(buf);
 return min + (buf[0] / 4294967296) * (max - min);
 }

 function generate() {
 const min = T.num(T.$('min').value);
 const max = T.num(T.$('max').value);
 const count = Math.min(10000, Math.max(1, Math.floor(T.num(T.$('count').value) || 1)));
 const decimals = T.$('decimals').checked;
 const unique = T.$('unique').checked;

 if (isNaN(min) || isNaN(max)) {
 T.status('status', 'Enter a minimum and maximum.', 'muted');
 return;
 }

 if (min >= max) {
 T.status('status', 'The maximum must be greater than the minimum.', 'error');
 return;
 }

 const rangeSize = Math.floor(max) - Math.ceil(min) + 1;

 if (unique && !decimals && count > rangeSize) {
 T.status('status',
 `Cannot draw ${count} unique whole numbers from a range containing only ${rangeSize}.`, 'error');
 return;
 }

 if (decimals) {
 numbers = Array.from({ length: count }, () => T.round(randomFloat(min, max), 6));
 } else if (unique) {
 // Partial Fisher-Yates over the candidate range, exact and
 // avoids the retry loop that naive rejection would need
 const pool = Array.from({ length: rangeSize }, (_, i) => Math.ceil(min) + i);
 for (let i = 0; i < count; i++) {
 const j = i + T.randomBelow(pool.length - i);
 [pool[i], pool[j]] = [pool[j], pool[i]];
 }
 numbers = pool.slice(0, count);
 } else {
 numbers = Array.from({ length: count },
 () => T.randomInt(Math.ceil(min), Math.floor(max)));
 }

 const sort = T.$('sort').value;
 const display = [...numbers];
 if (sort === 'asc') display.sort((a, b) => a - b);
 else if (sort === 'desc') display.sort((a, b) => b - a);

 T.setOutput('output', display.join('\n'));
 T.$('output-stats').textContent = `${count} number${count === 1 ? '' : 's'}`;

 const sum = numbers.reduce((a, b) => a + b, 0);
 T.$('r-sum').textContent = T.fmt(sum, decimals ? 2 : 0);
 T.$('r-mean').textContent = T.fmt(sum / numbers.length, 2);
 T.$('r-min').textContent = T.fmt(Math.min(...numbers), decimals ? 2 : 0);
 T.$('r-max').textContent = T.fmt(Math.max(...numbers), decimals ? 2 : 0);

 T.status('status',
 `Drew ${count} number(s) from ${T.fmt(min, 0)} to ${T.fmt(max, 0)}` +
 (unique ? ', without repeats.' : '.'), 'ok');
 }

 T.$('generate').addEventListener('click', generate);
 T.on(['min', 'max', 'count'], debounce(generate, 300));
 T.on(['unique', 'decimals', 'sort'], generate, 'change');

 T.wireActions({
 slug: 'random-number-generator',
 getResult: () => T.$('output').textContent,
 filename: 'random-numbers.txt'
 });

 generate();""",
))

# ---------------------------------------------------------------
# 47. Hash Generator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="hash-generator", name="Hash Generator", icon="#️⃣", cat="generator",
 title="Hash Generator: SHA-1, SHA-256, SHA-384 and SHA-512",
 description="Produce SHA-1, SHA-256, SHA-384 and SHA-512 digests of text or files, in hex or Base64. Everything is computed locally via the Web Crypto API.",
 tagline="Generate SHA digests of text or files, computed locally, never uploaded.",
 workspace=ws(
 textarea("input", "Text to hash", "Type or paste anything…", "input-stats", rows=140),
 row(
 select("encoding", "Output encoding", [("hex", "Hexadecimal"), ("base64", "Base64")], selected="hex"),
 switch("uppercase", "Uppercase hex", False),
 ),
 status_line("status", "Hashes update as you type."),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Digests</span><span class="field__hint">Click any row to copy it</span></span>
 <div class="table-scroll"><div id="digests"></div></div>
 </div>"""),
 buttons(("file", "Hash a file instead", "primary"), ("copy", "Copy all"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Verify against a known hash</span></span>
 <input class="input font-mono" id="verify" type="text"
 aria-label="Hash to verify against"
 placeholder="Paste a hash to compare it against the ones above">
 <p id="verify-result" class="field__hint"></p>
 </div>"""),
 label="Hash generator",
 ),
 info_block=info(
 features=[
 "SHA-1, SHA-256, SHA-384 and SHA-512",
 "Hexadecimal or Base64 output",
 "Hash files of any size without uploading them",
 "Constant-time comparison against a known hash",
 "Computed by the browser's own crypto implementation",
 ],
 howto=[
 "Type or paste the text you want to hash.",
 "All four digests update immediately.",
 "Use “Hash a file” to checksum a download.",
 "Paste a published hash into the verify box to compare.",
 ],
 background_title="What hashes are for, and what they are not for",
 background_paragraphs=[
 "A cryptographic hash maps any input to a fixed-size digest such that the same input always produces the same output, any change produces a completely different output, and the original cannot be recovered from the digest. That makes hashes ideal for integrity checking: download a file, hash it, compare against the published value, and you know whether it arrived intact.",
 "SHA-1 is included here because you will still encounter it, Git uses it for object identifiers, and plenty of legacy systems publish SHA-1 checksums. It should not be used for anything security-relevant. A practical collision was demonstrated in 2017, and the cost of producing one has fallen since. Use SHA-256 or better for anything new.",
 "The critical thing hashes are <em>not</em> suitable for is storing passwords. SHA-256 is designed to be fast, and fast is exactly wrong for password storage, modern hardware computes billions of SHA-256 hashes per second, so a stolen database of SHA-256 password hashes falls quickly to brute force. Password storage needs a deliberately slow, memory-hard, salted function: Argon2id, scrypt, or bcrypt. Adding a salt to SHA-256 helps against rainbow tables but does not fix the speed problem.",
 ],
 ),
 script=r""" const ALGORITHMS = ['SHA-1', 'SHA-256', 'SHA-384', 'SHA-512'];
 let digests = {};

 function toHex(buffer) {
 return [...new Uint8Array(buffer)].map((b) => b.toString(16).padStart(2, '0')).join('');
 }

 function toBase64(buffer) {
 const bytes = new Uint8Array(buffer);
 let binary = '';
 for (let i = 0; i < bytes.length; i++) binary += String.fromCharCode(bytes[i]);
 return btoa(binary);
 }

 function encodeDigest(buffer) {
 if (T.$('encoding').value === 'base64') return toBase64(buffer);
 const hex = toHex(buffer);
 return T.$('uppercase').checked ? hex.toUpperCase() : hex;
 }

 /**
 * @param {ArrayBuffer|Uint8Array} data
 * @returns {Promise<Object>} algorithm → encoded digest
 */
 async function hashAll(data) {
 const out = {};
 for (const algo of ALGORITHMS) {
 const buffer = await crypto.subtle.digest(algo, data);
 out[algo] = encodeDigest(buffer);
 }
 return out;
 }

 function renderDigests() {
 const mount = T.$('digests');
 mount.innerHTML = '';

 const entries = Object.entries(digests);
 if (!entries.length) return;

 const table = T.table(['Algorithm', 'Digest'], entries.map(([a, d]) => [a, d]));

 [...table.querySelectorAll('tbody tr')].forEach((tr, i) => {
 tr.style.cursor = 'pointer';
 tr.title = 'Click to copy';
 tr.addEventListener('click', () => {
 copyToClipboard(entries[i][1], entries[i][0] + ' copied');
 });
 });

 mount.append(table);
 checkVerify();
 }

 async function run() {
 const text = T.$('input').value;
 T.$('input-stats').textContent = text.length.toLocaleString() + ' characters';

 if (!text) {
 digests = {};
 T.$('digests').innerHTML = '';
 T.status('status', 'Hashes update as you type.', 'muted');
 return;
 }

 try {
 const data = new TextEncoder().encode(text);
 digests = await hashAll(data);
 renderDigests();
 T.status('status', `Hashed ${data.length.toLocaleString()} byte(s) of UTF-8 text.`, 'ok');
 if (window.Analytics) Analytics.trackToolUse('hash-generator');
 } catch (err) {
 T.status('status', 'Hashing failed: ' + err.message, 'error');
 }
 }

 /**
 * Compare in constant time, a length-dependent early exit would
 * leak information about how much of the hash matched.
 */
 function constantTimeEqual(a, b) {
 if (a.length !== b.length) return false;
 let diff = 0;
 for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
 return diff === 0;
 }

 function checkVerify() {
 const expected = T.$('verify').value.trim();
 const node = T.$('verify-result');

 if (!expected) {
 node.textContent = '';
 return;
 }

 const normalise = (s) => s.replace(/\s/g, '').toLowerCase();
 const match = Object.entries(digests)
 .find(([, d]) => constantTimeEqual(normalise(d), normalise(expected)));

 if (match) {
 node.textContent = `✓ Matches the ${match[0]} digest.`;
 node.style.color = 'var(--success)';
 } else {
 node.textContent = '✗ Does not match any of the digests above.';
 node.style.color = 'var(--danger)';
 }
 }

 T.$('input').addEventListener('input', debounce(run, 250));
 T.on(['encoding', 'uppercase'], run, 'change');
 T.$('verify').addEventListener('input', debounce(checkVerify, 200));

 T.$('file').addEventListener('click', async () => {
 const selected = await T.pickFile();
 if (!selected) return;

 T.status('status', `Reading ${selected.name}…`, 'muted');

 try {
 const buffer = await selected.arrayBuffer();
 digests = await hashAll(buffer);
 renderDigests();
 T.$('input').value = '';
 T.$('input-stats').textContent = '';
 T.status('status',
 `Hashed “${selected.name}” (${T.bytes(selected.size)}). The file never left your device.`, 'ok');
 } catch (err) {
 T.status('status', 'Could not read that file: ' + err.message, 'error');
 }
 });

 T.$('copy').addEventListener('click', () => {
 const text = Object.entries(digests).map(([a, d]) => `${a}: ${d}`).join('\n');
 copyToClipboard(text, 'All digests copied');
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Hash Generator | 123MiniApps' }));

 T.$('input').value = 'Hello, world!';
 run();""",
))

# ---------------------------------------------------------------
# 48. Slug Generator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="slug-generator", name="Slug Generator", icon="🔗", cat="generator",
 title="Slug Generator: Clean URL Slugs from Any Title",
 description="Turn any title into a clean URL-safe slug. Transliterates accents, removes stop words, enforces a maximum length and handles bulk input.",
 tagline="Turn titles into clean URL slugs, accents transliterated, stop words optional.",
 workspace=ws(
 textarea("input", "Title(s)", "One title per line…\nThe Quick Brown Fox Jumps Over the Lazy Dog", "input-stats", rows=140),
 row(
 select("separator", "Separator", [("-", "Hyphen -"), ("_", "Underscore _"), ("", "None")], selected="-"),
 number_input("maxlen", "Maximum length", "60", "60", step="1", min=0),
 select("case", "Case", [("lower", "lowercase"), ("upper", "UPPERCASE"), ("keep", "Keep original")], selected="lower"),
 ),
 row(
 switch("stopwords", "Remove common stop words (a, the, of…)", False),
 switch("numbers", "Keep numbers", True),
 switch("dedupe", "Add a numeric suffix to duplicates", True),
 ),
 status_line("status", "Type a title to slugify it."),
 HR,
 output("output", "Slugs", "output-stats"),
 STD_ACTIONS,
 label="Slug generator",
 ),
 info_block=info(
 features=[
 "Transliterates accented and non-Latin characters",
 "Optional stop-word removal",
 "Configurable separator and maximum length",
 "Bulk processing, one title per line",
 "Automatic numeric suffixes for duplicates",
 ],
 howto=[
 "Paste one or more titles, one per line.",
 "Choose your separator and length limit.",
 "Turn on stop-word removal for shorter slugs.",
 "Copy the slugs or download them.",
 ],
 background_title="What makes a good URL slug",
 background_paragraphs=[
 "Slugs exist because URLs have a restricted character set and because readable URLs are more clickable and more shareable than opaque identifiers. A slug should be lowercase, use hyphens rather than underscores, and contain only unreserved characters. Google has stated it treats hyphens as word separators and underscores as word joiners, so <code>red_shoes</code> may be read as one token while <code>red-shoes</code> is clearly two.",
 "Length is a genuine trade-off. Shorter slugs are cleaner and easier to share, which is the case for stripping stop words, <code>the-quick-brown-fox</code> becomes <code>quick-brown-fox</code>. But removing too much can make the slug ambiguous or change its meaning, and stop-word removal occasionally produces something nonsensical. Around 60 characters is a reasonable ceiling.",
 "The important operational rule is that slugs should be stable. Once a URL is published, changing its slug breaks every existing link and any accumulated search ranking. If you must change one, serve a 301 redirect from the old URL. This is also why many systems keep an immutable numeric ID alongside the slug in the URL, it lets the slug change for readability while the ID guarantees the page can always be found.",
 ],
 ),
 script=r""" let lastResult = '';

 const STOP_WORDS = new Set(('a an and are as at be but by for from has have in is it its of on or ' +
 'that the to was were will with').split(' '));

 /**
 * Transliterate characters that NFD normalisation cannot decompose.
 * Without this, ß, ø, æ and similar are simply deleted.
 */
 const TRANSLITERATE = {
 'ß': 'ss', 'æ': 'ae', 'Æ': 'ae', 'œ': 'oe', 'Œ': 'oe',
 'ø': 'o', 'Ø': 'o', 'å': 'a', 'Å': 'a', 'đ': 'd', 'Đ': 'd',
 'ł': 'l', 'Ł': 'l', 'ı': 'i', 'ð': 'd', 'Ð': 'd', 'þ': 'th', 'Þ': 'th',
 '&': ' and ', '@': ' at ', '€': ' euro ', '£': ' pound ', '$': ' dollar ', '%': ' percent '
 };

 function slugify(title) {
 const sep = T.$('separator').value;
 const maxLen = Math.max(0, Math.floor(T.num(T.$('maxlen').value) || 0));

 let s = String(title);

 // Expand the characters NFD cannot handle
 s = s.replace(/[ßæÆœŒøØåÅđĐłŁıðÐþÞ&@€£$%]/g, (c) => TRANSLITERATE[c] || c);

 // Strip diacritics: decompose, then remove combining marks
 s = s.normalize('NFD').replace(/[\u0300-\u036f]/g, '');

 if (T.$('case').value === 'lower') s = s.toLowerCase();
 else if (T.$('case').value === 'upper') s = s.toUpperCase();

 // Split into words on anything that is not a letter or digit
 let words = s.split(/[^a-zA-Z0-9]+/).filter(Boolean);

 if (!T.$('numbers').checked) {
 words = words.filter((word) => !/^\d+$/.test(word));
 }

 if (T.$('stopwords').checked) {
 const filtered = words.filter((word) => !STOP_WORDS.has(word.toLowerCase()));
 // Never let stop-word removal empty the slug entirely
 if (filtered.length) words = filtered;
 }

 let slug = words.join(sep);

 // Trim to the length limit at a word boundary rather than mid-word
 if (maxLen > 0 && slug.length > maxLen) {
 slug = slug.slice(0, maxLen);
 const lastSep = sep ? slug.lastIndexOf(sep) : -1;
 if (lastSep > maxLen * 0.5) slug = slug.slice(0, lastSep);
 }

 return slug;
 }

 function run() {
 const raw = T.$('input').value;
 T.$('input-stats').textContent = raw
 ? raw.split(/\r?\n/).filter((l) => l.trim()).length + ' title(s)'
 : '';

 if (!raw.trim()) {
 lastResult = '';
 T.setOutput('output', '');
 T.$('output-stats').textContent = '';
 T.status('status', 'Type a title to slugify it.', 'muted');
 return;
 }

 const lines = raw.split(/\r?\n/).filter((l) => l.trim());
 const seen = new Map();

 const slugs = lines.map((line) => {
 let slug = slugify(line);
 if (!slug) return '(empty, no usable characters)';

 if (T.$('dedupe').checked) {
 const count = seen.get(slug) || 0;
 seen.set(slug, count + 1);
 if (count > 0) slug = slug + T.$('separator').value + (count + 1);
 }

 return slug;
 });

 lastResult = slugs.join('\n');
 T.setOutput('output', lastResult);
 T.$('output-stats').textContent = `${slugs.length} slug(s)`;

 const longest = Math.max(...slugs.map((s) => s.length));
 T.status('status', `Generated ${slugs.length} slug(s). Longest is ${longest} characters.`, 'ok');
 }

 T.$('input').addEventListener('input', debounce(run, 250));
 T.on(['maxlen'], debounce(run, 250));
 T.on(['separator', 'case', 'stopwords', 'numbers', 'dedupe'], run, 'change');

 T.wireActions({ slug: 'slug-generator', getResult: () => lastResult, filename: 'slugs.txt' });
 run();""",
))

# ---------------------------------------------------------------
# 49. Barcode Generator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="barcode-generator", name="Barcode Generator", icon="📊", cat="generator",
 title="Barcode Generator: Code 128, EAN-13, EAN-8 and UPC-A",
 description="Generate Code 128, EAN-13, EAN-8 and UPC-A barcodes with automatic check digits. Download as PNG or scalable SVG. Encoded in your browser.",
 tagline="Generate scannable barcodes with automatic check digits, PNG or vector SVG.",
 extra_scripts='<script src="../assets/js/vendor/barcode-encoder.js" defer></script>',
 workspace=ws(
 row(
 select("symbology", "Barcode type", [
 ("code128", "Code 128, any text"),
 ("ean13", "EAN-13, retail products"),
 ("ean8", "EAN-8, small packages"),
 ("upca", "UPC-A, North American retail"),
 ], selected="code128"),
 text_input("value", "Value to encode", "123MINIAPPS", "123MINIAPPS"),
 ),
 row(
 slider("width", "Module width", 1, 6, 2, 1, unit="px"),
 slider("height", "Bar height", 40, 220, 100, 10, unit="px"),
 switch("showtext", "Show the value beneath", True),
 ),
 row(color_input("fg", "Bar colour", "#000000"), color_input("bg", "Background", "#FFFFFF")),
 status_line("status", "Enter a value to encode."),
 HR,
 canvas("canvas", "Barcode"),
 buttons(("download-png", "Download PNG", "primary"), ("download-svg", "Download SVG"), ("copy-value", "Copy encoded value"), ("share", "Share tool", "ghost")),
 label="Barcode generator",
 ),
 info_block=info(
 features=[
 "Four symbologies covering retail and general use",
 "Check digits calculated and validated automatically",
 "Adjustable module width, height and colours",
 "PNG raster and SVG vector export",
 "Encoder written in-house, no external requests",
 ],
 howto=[
 "Choose the barcode type you need.",
 "Enter the value, check digits are added for you.",
 "Adjust the size and colours.",
 "Download as PNG for screen or SVG for print.",
 ],
 background_title="Which symbology to use",
 background_paragraphs=[
 "Code 128 encodes the full printable ASCII set and is the right default for anything internal, asset tags, shipping references, work orders, library codes. It is also space-efficient: it has a mode that packs two digits into each symbol, so long numeric strings stay compact. This encoder switches into that mode automatically when it pays off.",
 "EAN-13 and UPC-A are for retail products sold through shops, and you cannot simply invent one. The leading digits identify the issuing organisation and the manufacturer, and those prefixes are allocated by GS1 for a fee. A made-up EAN will scan fine but may collide with a real product, so use Code 128 for internal purposes and only use EAN or UPC with a number properly assigned to you.",
 "Two practical points about printing. The check digit is a modulo-10 calculation over the preceding digits, this tool computes it if you omit it, and tells you if the one you supplied is wrong. And the quiet zone matters more than people expect: barcodes need a clear margin of roughly ten times the module width on each side, and scanners fail on codes printed right up against other artwork. Both exports here include the correct quiet zone.",
 ],
 ),
 script=r""" const canvas = T.$('canvas');
 const ctx = canvas.getContext('2d');
 let current = null;

 const PLACEHOLDERS = {
 code128: '123MINIAPPS',
 ean13: '4006381333931',
 ean8: '96385074',
 upca: '036000291452'
 };

 function render() {
 const raw = T.$('value').value.trim();
 const symbology = T.$('symbology').value;

 T.$('width-value').textContent = T.$('width').value;
 T.$('height-value').textContent = T.$('height').value;

 if (!raw) {
 current = null;
 ctx.clearRect(0, 0, canvas.width, canvas.height);
 T.$('canvas-meta').textContent = '';
 T.status('status', 'Enter a value to encode.', 'muted');
 return;
 }

 let result;
 try {
 result = BarcodeEncoder.encode(raw, symbology);
 } catch (err) {
 current = null;
 ctx.clearRect(0, 0, canvas.width, canvas.height);
 T.$('canvas-meta').textContent = '';
 T.status('status', err.message, 'error');
 return;
 }

 current = result;

 const moduleWidth = Number(T.$('width').value);
 const barHeight = Number(T.$('height').value);
 const showText = T.$('showtext').checked;
 const quiet = result.quietZone;
 const textHeight = showText ? 22 : 0;

 const totalModules = result.bits.length + quiet * 2;
 canvas.width = totalModules * moduleWidth;
 canvas.height = barHeight + textHeight + 8;
 canvas.style.maxWidth = '100%';

 ctx.fillStyle = T.$('bg').value;
 ctx.fillRect(0, 0, canvas.width, canvas.height);

 ctx.fillStyle = T.$('fg').value;
 for (let i = 0; i < result.bits.length; i++) {
 if (result.bits[i] === '1') {
 ctx.fillRect((i + quiet) * moduleWidth, 4, moduleWidth, barHeight);
 }
 }

 if (showText) {
 ctx.font = `${Math.max(11, moduleWidth * 6)}px monospace`;
 ctx.textAlign = 'center';
 ctx.textBaseline = 'top';
 ctx.fillText(result.text, canvas.width / 2, barHeight + 8);
 }

 T.$('canvas-meta').textContent =
 `${result.symbology} · ${result.bits.length} modules · ${canvas.width}×${canvas.height}px`;

 const addedCheck = result.text.length > raw.replace(/\D/g, '').length && symbology !== 'code128';
 T.status('status',
 `Encoded as ${result.symbology}` +
 (addedCheck ? `, check digit ${result.text.slice(-1)} added.` : '.'), 'ok');

 if (window.Analytics) Analytics.trackToolUse('barcode-generator');
 }

 function toSVG() {
 if (!current) return '';

 const moduleWidth = Number(T.$('width').value);
 const barHeight = Number(T.$('height').value);
 const showText = T.$('showtext').checked;
 const quiet = current.quietZone;
 const textHeight = showText ? 22 : 0;

 const width = (current.bits.length + quiet * 2) * moduleWidth;
 const height = barHeight + textHeight + 8;

 const bars = [];
 let run = 0;
 for (let i = 0; i <= current.bits.length; i++) {
 if (current.bits[i] === '1') { run++; continue; }
 if (run > 0) {
 const x = (i - run + quiet) * moduleWidth;
 bars.push(`<rect x="${x}" y="4" width="${run * moduleWidth}" height="${barHeight}"/>`);
 run = 0;
 }
 }

 const text = showText
 ? `<text x="${width / 2}" y="${barHeight + 10}" text-anchor="middle" ` +
 `dominant-baseline="hanging" font-family="monospace" ` +
 `font-size="${Math.max(11, moduleWidth * 6)}" fill="${T.$('fg').value}">${T.esc(current.text)}</text>`
 : '';

 return '<?xml version="1.0" encoding="UTF-8"?>\n' +
 `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" ` +
 `viewBox="0 0 ${width} ${height}" shape-rendering="crispEdges">` +
 `<rect width="${width}" height="${height}" fill="${T.$('bg').value}"/>` +
 `<g fill="${T.$('fg').value}">${bars.join('')}</g>${text}</svg>`;
 }

 T.$('symbology').addEventListener('change', () => {
 T.$('value').value = PLACEHOLDERS[T.$('symbology').value];
 render();
 });

 T.$('value').addEventListener('input', debounce(render, 200));
 T.on(['width', 'height'], render);
 T.on(['showtext', 'fg', 'bg'], render, 'change');

 T.$('download-png').addEventListener('click', () => {
 if (!current) { toast({ type: 'warning', title: 'Nothing to download' }); return; }
 canvas.toBlob((blob) => downloadFile(blob, 'barcode.png', 'image/png'), 'image/png');
 });

 T.$('download-svg').addEventListener('click', () => {
 if (!current) { toast({ type: 'warning', title: 'Nothing to download' }); return; }
 downloadFile(toSVG(), 'barcode.svg', 'image/svg+xml');
 });

 T.$('copy-value').addEventListener('click', () => {
 if (!current) return;
 copyToClipboard(current.text, 'Encoded value copied');
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Barcode Generator | 123MiniApps' }));

 render();""",
))

# ---------------------------------------------------------------
# 50. Placeholder Image Generator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="placeholder-image-generator", name="Placeholder Image Generator", icon="🖼️", cat="generator",
 title="Placeholder Image Generator: Custom Size, Text and Colours",
 description="Create placeholder images at any size with custom text and colours. Download as PNG or SVG, or copy a data URI to paste straight into your markup.",
 tagline="Create sized placeholder images for mockups, PNG, SVG or a copy-paste data URI.",
 workspace=ws(
 row(
 number_input("width", "Width (px)", "800", "800", step="1", min=1, max=4000),
 number_input("height", "Height (px)", "450", "450", step="1", min=1, max=4000),
 select("preset", "Or use a preset", [
 ("", "Custom size…"),
 ("1920x1080", "1920×1080, Full HD"),
 ("1200x630", "1200×630, Open Graph"),
 ("1080x1080", "1080×1080, Instagram square"),
 ("1080x1920", "1080×1920, Story"),
 ("800x600", "800×600, 4:3"),
 ("400x400", "400×400, Avatar"),
 ("160x600", "160×600, Skyscraper ad"),
 ("728x90", "728×90, Leaderboard ad"),
 ], selected=""),
 ),
 row(
 text_input("label", "Text", "Leave blank to show the dimensions", ""),
 slider("fontsize", "Text size", 10, 120, 40, 2, unit="px"),
 ),
 row(
 color_input("bg", "Background", "#1A1F4E"),
 color_input("fg", "Text colour", "#00D4FF"),
 switch("grid", "Show a diagonal cross", True),
 ),
 status_line("status", "Adjust the settings to preview."),
 HR,
 canvas("canvas", "Placeholder preview"),
 buttons(("download-png", "Download PNG", "primary"), ("download-svg", "Download SVG"), ("copy-uri", "Copy data URI"), ("copy-img", "Copy <img> tag"), ("share", "Share tool", "ghost")),
 label="Placeholder image generator",
 ),
 info_block=info(
 features=[
 "Any size up to 4000×4000",
 "Eight common presets for social and ad formats",
 "Custom text, colours and font size",
 "PNG and SVG export",
 "Copy a data URI or a complete img tag",
 ],
 howto=[
 "Set the dimensions, or pick a preset.",
 "Add text, or leave it blank to show the size.",
 "Choose your colours.",
 "Download, or copy a data URI to paste into your code.",
 ],
 background_title="Placeholder images and layout stability",
 background_paragraphs=[
 "The main reason to use correctly sized placeholders during development is Cumulative Layout Shift. If an image has no dimensions, the browser cannot reserve space for it, so everything below jumps down when it finally loads. That is measured by Core Web Vitals and it is genuinely annoying to use. Always set explicit <code>width</code> and <code>height</code> attributes, or an <code>aspect-ratio</code> in CSS, and the browser reserves the right box before a single byte of the image arrives.",
 "The data URI option is useful but has a real cost. Embedding an image directly in your HTML or CSS avoids a network request, which is worth it for tiny assets. But Base64 encoding inflates the data by roughly 33%, the bytes cannot be cached separately from the document, and a large data URI bloats every page load. As a rough guide, inline anything under about 2 KB and link to everything larger.",
 "SVG is usually the better format for placeholders specifically. It stays crisp at any size, and a solid-colour rectangle with a line of text compresses to a few hundred bytes, far smaller than the equivalent PNG. It is also editable as plain text, so you can adjust the colour in your editor without regenerating anything.",
 ],
 ),
 script=r""" const canvas = T.$('canvas');
 const ctx = canvas.getContext('2d');

 function dimensions() {
 return {
 width: T.clamp(Math.floor(T.num(T.$('width').value) || 1), 1, 4000),
 height: T.clamp(Math.floor(T.num(T.$('height').value) || 1), 1, 4000)
 };
 }

 function labelText() {
 const { width, height } = dimensions();
 return T.$('label').value.trim() || `${width} × ${height}`;
 }

 function render() {
 const { width, height } = dimensions();
 const fontSize = Number(T.$('fontsize').value);

 T.$('fontsize-value').textContent = fontSize;

 canvas.width = width;
 canvas.height = height;
 // Keep the on-screen preview manageable regardless of real size
 canvas.style.maxWidth = '100%';
 canvas.style.maxHeight = '420px';
 canvas.style.width = 'auto';

 ctx.fillStyle = T.$('bg').value;
 ctx.fillRect(0, 0, width, height);

 if (T.$('grid').checked) {
 ctx.strokeStyle = T.$('fg').value;
 ctx.globalAlpha = 0.25;
 ctx.lineWidth = Math.max(1, Math.min(width, height) / 200);
 ctx.beginPath();
 ctx.moveTo(0, 0); ctx.lineTo(width, height);
 ctx.moveTo(width, 0); ctx.lineTo(0, height);
 ctx.stroke();
 ctx.strokeRect(0, 0, width, height);
 ctx.globalAlpha = 1;
 }

 ctx.fillStyle = T.$('fg').value;
 ctx.font = `600 ${fontSize}px Inter, system-ui, sans-serif`;
 ctx.textAlign = 'center';
 ctx.textBaseline = 'middle';
 ctx.fillText(labelText(), width / 2, height / 2);

 T.$('canvas-meta').textContent = `${width} × ${height} px`;
 T.status('status', `Preview at ${width} × ${height} px.`, 'ok');

 if (window.Analytics) Analytics.trackToolUse('placeholder-image-generator');
 }

 function toSVG() {
 const { width, height } = dimensions();
 const fontSize = Number(T.$('fontsize').value);
 const fg = T.$('fg').value;

 const cross = T.$('grid').checked
 ? `<g stroke="${fg}" stroke-opacity="0.25" stroke-width="${Math.max(1, Math.min(width, height) / 200)}" fill="none">` +
 `<path d="M0 0L${width} ${height}M${width} 0L0 ${height}"/>` +
 `<rect x="0" y="0" width="${width}" height="${height}"/></g>`
 : '';

 return '<?xml version="1.0" encoding="UTF-8"?>\n' +
 `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">` +
 `<rect width="${width}" height="${height}" fill="${T.$('bg').value}"/>${cross}` +
 `<text x="50%" y="50%" text-anchor="middle" dominant-baseline="central" ` +
 `font-family="Inter, system-ui, sans-serif" font-weight="600" font-size="${fontSize}" ` +
 `fill="${fg}">${T.esc(labelText())}</text></svg>`;
 }

 T.$('preset').addEventListener('change', () => {
 const value = T.$('preset').value;
 if (!value) return;
 const [w, h] = value.split('x');
 T.$('width').value = w;
 T.$('height').value = h;
 render();
 });

 T.on(['width', 'height', 'label', 'fontsize'], debounce(render, 150));
 T.on(['bg', 'fg', 'grid'], render, 'change');

 T.$('download-png').addEventListener('click', () => {
 const { width, height } = dimensions();
 canvas.toBlob((blob) => downloadFile(blob, `placeholder-${width}x${height}.png`, 'image/png'), 'image/png');
 });

 T.$('download-svg').addEventListener('click', () => {
 const { width, height } = dimensions();
 downloadFile(toSVG(), `placeholder-${width}x${height}.svg`, 'image/svg+xml');
 });

 T.$('copy-uri').addEventListener('click', () => {
 const uri = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(toSVG())));
 copyToClipboard(uri, 'Data URI copied');
 });

 T.$('copy-img').addEventListener('click', () => {
 const { width, height } = dimensions();
 const uri = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(toSVG())));
 copyToClipboard(
 `<img src="${uri}" width="${width}" height="${height}" alt="Placeholder">`,
 'img tag copied'
 );
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Placeholder Image Generator | 123MiniApps' }));

 render();""",
))

# ---------------------------------------------------------------
# 51. Fake Data Generator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="fake-data-generator", name="Fake Data Generator", icon="👤", cat="generator",
 title="Fake Data Generator: Test Names, Emails, Addresses and More",
 description="Produce realistic sample records for testing: names, emails, phone numbers, addresses, dates and IDs. Export as JSON, CSV or SQL insert statements.",
 tagline="Generate realistic test records, and never use real customer data in staging again.",
 workspace=ws(
 html_block(""" <div class="field">
 <span class="field__label"><span>Fields to include</span><span class="field__hint">Click to toggle</span></span>
 <div class="chip-grid" id="fields"></div>
 </div>"""),
 row(
 number_input("count", "How many records", "10", "10", step="1", min=1, max=500),
 select("format", "Output format", [
 ("json", "JSON"), ("csv", "CSV"), ("sql", "SQL INSERT"), ("table", "Readable table"),
 ], selected="json"),
 select("locale", "Style", [("en", "English"), ("de", "German"), ("fr", "French"), ("es", "Spanish")], selected="en"),
 ),
 status_line("status", "Choose your fields and press Generate."),
 HR,
 output("output", "Generated data", "output-stats", "Your test data will appear here."),
 buttons(("generate", "Generate", "primary"), ("copy", "Copy result"), ("download", "Download"), ("share", "Share tool", "ghost")),
 label="Fake data generator",
 ),
 info_block=info(
 features=[
 "Twelve field types covering the common cases",
 "Four output formats including ready-to-run SQL",
 "Four naming styles for realistic international data",
 "Up to 500 records at a time",
 "Internally consistent, emails match the generated names",
 ],
 howto=[
 "Toggle the fields you need.",
 "Set how many records to generate.",
 "Pick an output format.",
 "Copy or download the result.",
 ],
 background_title="Why you should not test with real data",
 background_paragraphs=[
 "Copying a production database into a staging environment is common and is a serious problem. Staging environments typically have weaker access controls, less monitoring, wider developer access and looser backup hygiene than production. Under GDPR, personal data in a test system is still personal data, subject to the same lawful-basis, retention and breach-notification obligations, and a staging leak is a reportable breach exactly like a production one.",
 "Generated data avoids all of that, and tends to produce better tests. Real data clusters around the ordinary: mostly short names, mostly one address format, mostly the same handful of domains. Synthetic data can be deliberately awkward, apostrophes in surnames, very long strings, unusual characters, which is what actually finds the bugs.",
 "If you must derive test data from production, anonymisation is harder than replacing names with X. Pseudonymised data is still personal data under GDPR if it can be re-linked, and re-identification from a handful of quasi-identifiers like postcode, date of birth and sex is well documented. Generating fresh data sidesteps the question. Everything produced here is fictional, any resemblance to a real person is coincidental, and the addresses and card-style numbers are not valid.",
 ],
 ),
 script=r""" const NAMES = {
 en: {
 first: ['James','Mary','Robert','Patricia','John','Jennifer','Michael','Linda','David','Elizabeth','William','Barbara','Richard','Susan','Joseph','Jessica','Thomas','Sarah','Charles','Karen','Oliver','Amelia','George','Isla','Harry','Ava'],
 last: ['Smith','Johnson','Williams','Brown','Jones','Garcia','Miller','Davis','Wilson','Anderson','Taylor','Thomas','Moore','Jackson','Martin','Lee','Walker','Hall','Allen','Young','O\'Brien','MacDonald'],
 city: ['London','Manchester','Bristol','Leeds','Edinburgh','Cardiff','Liverpool','Glasgow','Oxford','Brighton','York','Bath'],
 street: ['High Street','Station Road','Church Lane','Victoria Road','Mill Lane','Park Avenue','Queens Road','Kings Way']
 },
 de: {
 first: ['Lukas','Anna','Felix','Emma','Jonas','Mia','Leon','Sophia','Paul','Hannah','Max','Lena','Tim','Laura','Jan','Julia'],
 last: ['Müller','Schmidt','Schneider','Fischer','Weber','Meyer','Wagner','Becker','Schulz','Hoffmann','Schäfer','Koch'],
 city: ['Berlin','Hamburg','München','Köln','Frankfurt','Stuttgart','Düsseldorf','Leipzig','Dresden','Bremen'],
 street: ['Hauptstraße','Bahnhofstraße','Schulstraße','Gartenweg','Kirchgasse','Lindenallee','Bergstraße']
 },
 fr: {
 first: ['Lucas','Emma','Gabriel','Jade','Louis','Louise','Raphaël','Alice','Jules','Chloé','Adam','Lina','Hugo','Léa'],
 last: ['Martin','Bernard','Dubois','Thomas','Robert','Richard','Petit','Durand','Leroy','Moreau','Simon','Laurent'],
 city: ['Paris','Marseille','Lyon','Toulouse','Nice','Nantes','Strasbourg','Bordeaux','Lille','Rennes'],
 street: ['Rue de la Paix','Avenue des Champs','Boulevard Saint-Germain','Rue Victor Hugo','Place de la République']
 },
 es: {
 first: ['Hugo','Lucía','Martín','Sofía','Pablo','María','Daniel','Paula','Alejandro','Valeria','Mateo','Carmen'],
 last: ['García','Rodríguez','González','Fernández','López','Martínez','Sánchez','Pérez','Gómez','Martín','Jiménez'],
 city: ['Madrid','Barcelona','Valencia','Sevilla','Zaragoza','Málaga','Bilbao','Granada','Alicante','Córdoba'],
 street: ['Calle Mayor','Avenida de la Constitución','Plaza España','Calle Real','Paseo del Prado']
 }
 };

 const COMPANIES = ['Acme','Globex','Initech','Umbrella','Soylent','Hooli','Vandelay','Stark','Wayne','Cyberdyne','Massive Dynamic','Wonka'];
 const SUFFIXES = ['Ltd','GmbH','SA','Inc','Group','Holdings','Partners','Studio'];
 const DOMAINS = ['example.com','example.org','example.net','test.example','mail.example'];
 const ROLES = ['Engineer','Designer','Manager','Analyst','Consultant','Director','Coordinator','Specialist'];

 const FIELDS = [
 ['id', 'ID'], ['uuid', 'UUID'], ['first_name', 'First name'], ['last_name', 'Last name'],
 ['full_name', 'Full name'], ['email', 'Email'], ['phone', 'Phone'], ['company', 'Company'],
 ['job_title', 'Job title'], ['address', 'Address'], ['city', 'City'], ['postcode', 'Postcode'],
 ['country', 'Country'], ['date_of_birth', 'Date of birth'], ['created_at', 'Created at'],
 ['active', 'Active flag'], ['amount', 'Amount']
 ];

 let selected = new Set(['id', 'first_name', 'last_name', 'email', 'phone', 'city']);
 let records = [];
 let lastResult = '';

 const COUNTRY_BY_LOCALE = { en: 'United Kingdom', de: 'Germany', fr: 'France', es: 'Spain' };

 function makeRecord(index) {
 const locale = T.$('locale').value;
 const pool = NAMES[locale];

 const first = T.pick(pool.first);
 const last = T.pick(pool.last);
 const company = T.pick(COMPANIES) + ' ' + T.pick(SUFFIXES);

 // Email is derived from the name, so the record is internally consistent
 const emailName = (first + '.' + last)
 .toLowerCase()
 .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
 .replace(/[^a-z.]/g, '');

 const dob = new Date(
 T.randomInt(1955, 2005),
 T.randomInt(0, 11),
 T.randomInt(1, 28)
 );
 const created = new Date(Date.now() - T.randomInt(0, 1000) * 86400000);

 const all = {
 id: index + 1,
 uuid: crypto.randomUUID ? crypto.randomUUID() : String(index),
 first_name: first,
 last_name: last,
 full_name: first + ' ' + last,
 email: `${emailName}${T.randomInt(1, 99)}@${T.pick(DOMAINS)}`,
 phone: `+${T.randomInt(1, 99)} ${T.randomInt(100, 999)} ${T.randomInt(100000, 999999)}`,
 company,
 job_title: T.pick(ROLES),
 address: `${T.randomInt(1, 200)} ${T.pick(pool.street)}`,
 city: T.pick(pool.city),
 postcode: `${String.fromCharCode(65 + T.randomBelow(26))}${T.randomInt(1, 99)} ${T.randomInt(1, 9)}${String.fromCharCode(65 + T.randomBelow(26))}${String.fromCharCode(65 + T.randomBelow(26))}`,
 country: COUNTRY_BY_LOCALE[locale],
 date_of_birth: dob.toISOString().slice(0, 10),
 created_at: created.toISOString(),
 active: T.randomBelow(4) > 0,
 amount: T.round(T.randomInt(100, 500000) / 100, 2)
 };

 const record = {};
 FIELDS.forEach(([key]) => { if (selected.has(key)) record[key] = all[key]; });
 return record;
 }

 function sqlEscape(v) {
 if (v === null || v === undefined) return 'NULL';
 if (typeof v === 'number') return String(v);
 if (typeof v === 'boolean') return v ? 'TRUE' : 'FALSE';
 return "'" + String(v).replace(/'/g, "''") + "'";
 }

 function csvEscape(v) {
 const s = String(v);
 return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
 }

 function formatOutput() {
 if (!records.length) return '';
 const keys = Object.keys(records[0]);
 const format = T.$('format').value;

 if (format === 'json') return JSON.stringify(records, null, 2);

 if (format === 'csv') {
 return [keys.join(',')]
 .concat(records.map((r) => keys.map((k) => csvEscape(r[k])).join(',')))
 .join('\n');
 }

 if (format === 'sql') {
 return records.map((r) =>
 `INSERT INTO users (${keys.join(', ')}) VALUES (${keys.map((k) => sqlEscape(r[k])).join(', ')});`
 ).join('\n');
 }

 // Readable fixed-width table
 const widths = keys.map((k) =>
 Math.max(k.length, ...records.map((r) => String(r[k]).length)));
 const line = (cells) => cells.map((c, i) => String(c).padEnd(widths[i])).join(' ');
 return [line(keys), line(widths.map((w) => '-'.repeat(w)))]
 .concat(records.map((r) => line(keys.map((k) => r[k]))))
 .join('\n');
 }

 function generate() {
 if (!selected.size) {
 T.status('status', 'Select at least one field.', 'error');
 T.setOutput('output', '');
 return;
 }

 const count = T.clamp(Math.floor(T.num(T.$('count').value) || 1), 1, 500);
 records = Array.from({ length: count }, (_, i) => makeRecord(i));

 lastResult = formatOutput();
 T.setOutput('output', lastResult);
 T.$('output-stats').textContent = `${count} record(s), ${selected.size} field(s)`;
 T.status('status', `Generated ${count} fictional record(s). None of this data is real.`, 'ok');

 if (window.Analytics) Analytics.trackToolUse('fake-data-generator');
 }

 function renderFields() {
 const mount = T.$('fields');
 mount.innerHTML = '';

 FIELDS.forEach(([key, label]) => {
 const chip = el('button', {
 className: 'chip',
 attrs: { type: 'button', 'aria-pressed': String(selected.has(key)) },
 text: label
 });

 const paint = () => {
 const on = selected.has(key);
 chip.style.borderColor = on ? 'var(--accent-primary)' : '';
 chip.style.color = on ? 'var(--accent-primary)' : '';
 chip.setAttribute('aria-pressed', String(on));
 };

 chip.addEventListener('click', () => {
 selected.has(key) ? selected.delete(key) : selected.add(key);
 paint();
 generate();
 });

 paint();
 mount.append(chip);
 });
 }

 T.$('generate').addEventListener('click', generate);
 T.$('count').addEventListener('input', debounce(generate, 300));
 T.on(['format', 'locale'], generate, 'change');

 T.wireActions({
 slug: 'fake-data-generator',
 getResult: () => lastResult,
 filename: 'test-data.txt'
 });

 renderFields();
 generate();""",
))

# ---------------------------------------------------------------
# 52. Signature Generator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="signature-generator", name="Signature Generator", icon="✍️", cat="generator",
 title="Signature Generator: Draw or Type, Export Transparent PNG",
 description="Draw a signature with your mouse or finger, or type one in a script font. Export as a transparent PNG ready to drop into a document.",
 tagline="Draw or type a signature and export it with a transparent background.",
 workspace=ws(
 select("mode", "Signature style", [("draw", "Draw it yourself"), ("type", "Type it in a script font")], selected="draw"),
 html_block(""" <div id="draw-panel">
 <div class="field">
 <span class="field__label"><span>Sign here</span><span class="field__hint">Click and drag, or use your finger on a touchscreen</span></span>
 <canvas id="pad" width="900" height="300" role="img" aria-label="Signature drawing area"
 style="width:100%;height:auto;background:var(--bg-surface);border:2px dashed var(--border-color);border-radius:var(--radius-md);cursor:crosshair;touch-action:none"></canvas>
 </div>
 </div>"""),
 html_block(""" <div id="type-panel" hidden>
 <div class="field">
 <label class="field__label" for="typed"><span>Your name</span></label>
 <input class="input" id="typed" type="text" value="Ada Lovelace" placeholder="Type your name">
 </div>
 <div class="field">
 <span class="field__label"><span>Preview</span></span>
 <canvas id="typed-canvas" width="900" height="300" role="img" aria-label="Typed signature preview"
 style="width:100%;height:auto;background:var(--bg-surface);border:1px solid var(--border-color);border-radius:var(--radius-md)"></canvas>
 </div>
 </div>"""),
 row(
 slider("stroke", "Stroke width", 1, 12, 3, 1, unit="px"),
 color_input("ink", "Ink colour", "#0B1120"),
 select("font", "Script font", [
 ("'Segoe Script', 'Brush Script MT', cursive", "Casual script"),
 ("'Snell Roundhand', 'Apple Chancery', cursive", "Formal script"),
 ("Georgia, 'Times New Roman', serif", "Serif"),
 ("Inter, system-ui, sans-serif", "Plain"),
 ], selected="'Segoe Script', 'Brush Script MT', cursive"),
 ),
 switch("transparent", "Transparent background in the export", True),
 status_line("status", "Draw your signature above."),
 buttons(("download", "Download PNG", "primary"), ("copy-uri", "Copy data URI"), ("undo", "Undo last stroke"), ("clear", "Clear", "ghost"), ("share", "Share tool", "ghost")),
 label="Signature generator",
 ),
 info_block=info(
 features=[
 "Draw with a mouse, trackpad or finger",
 "Or type a name in one of four fonts",
 "Adjustable stroke width and ink colour",
 "Transparent PNG export",
 "Undo individual strokes",
 ],
 howto=[
 "Draw your signature in the box, or switch to typing.",
 "Adjust the stroke width and colour.",
 "Press Undo if a stroke goes wrong.",
 "Download the PNG and place it in your document.",
 ],
 background_title="What an image of a signature is worth legally",
 background_paragraphs=[
 "In most jurisdictions a signature does not have to be handwritten to be binding. The US ESIGN Act and UETA, the EU's eIDAS regulation and the UK's Electronic Communications Act all recognise electronic signatures for the great majority of agreements. What matters legally is intent to sign and the ability to demonstrate it, not the visual form.",
 "That said, a pasted image is the weakest form of electronic signature. It carries no evidence of who applied it or when, it can be copied from one document to another trivially, and it proves nothing if the agreement is disputed. Dedicated e-signature platforms add the things that actually matter in a challenge: an authenticated signer identity, a timestamp, an IP address and an audit trail, plus a tamper-evident hash of the signed document.",
 "Some documents are excluded from electronic signing regardless. Wills, many property transfers, court filings and certain family-law documents commonly require a wet signature, and sometimes a witness or notary. The rules vary considerably by jurisdiction, so check before relying on an image for anything consequential. Practically: an image like this is fine for internal approvals and informal agreements, but use a proper platform for contracts that matter, and note that this tool is informational, not legal advice.",
 ],
 ),
 script=r""" const pad = T.$('pad');
 const padCtx = pad.getContext('2d');
 const typedCanvas = T.$('typed-canvas');
 const typedCtx = typedCanvas.getContext('2d');

 let strokes = [];
 let currentStroke = null;
 let drawing = false;

 /** Translate a pointer event into canvas coordinates. */
 function pointFromEvent(e) {
 const rect = pad.getBoundingClientRect();
 return {
 x: ((e.clientX - rect.left) / rect.width) * pad.width,
 y: ((e.clientY - rect.top) / rect.height) * pad.height
 };
 }

 function redraw() {
 padCtx.clearRect(0, 0, pad.width, pad.height);
 padCtx.lineCap = 'round';
 padCtx.lineJoin = 'round';

 for (const stroke of strokes) {
 if (stroke.points.length < 2) continue;
 padCtx.strokeStyle = stroke.colour;
 padCtx.lineWidth = stroke.width;
 padCtx.beginPath();
 padCtx.moveTo(stroke.points[0].x, stroke.points[0].y);

 // Quadratic smoothing through the midpoints reads as a much
 // steadier line than joining raw pointer samples
 for (let i = 1; i < stroke.points.length - 1; i++) {
 const mid = {
 x: (stroke.points[i].x + stroke.points[i + 1].x) / 2,
 y: (stroke.points[i].y + stroke.points[i + 1].y) / 2
 };
 padCtx.quadraticCurveTo(stroke.points[i].x, stroke.points[i].y, mid.x, mid.y);
 }

 const last = stroke.points[stroke.points.length - 1];
 padCtx.lineTo(last.x, last.y);
 padCtx.stroke();
 }
 }

 pad.addEventListener('pointerdown', (e) => {
 e.preventDefault();
 pad.setPointerCapture(e.pointerId);
 drawing = true;
 currentStroke = {
 colour: T.$('ink').value,
 width: Number(T.$('stroke').value),
 points: [pointFromEvent(e)]
 };
 strokes.push(currentStroke);
 });

 pad.addEventListener('pointermove', (e) => {
 if (!drawing) return;
 currentStroke.points.push(pointFromEvent(e));
 redraw();
 });

 const endStroke = () => {
 if (!drawing) return;
 drawing = false;
 currentStroke = null;
 T.status('status', `${strokes.length} stroke(s) drawn.`, 'ok');
 };

 pad.addEventListener('pointerup', endStroke);
 pad.addEventListener('pointerleave', endStroke);
 pad.addEventListener('pointercancel', endStroke);

 function renderTyped() {
 const text = T.$('typed').value || ' ';
 typedCtx.clearRect(0, 0, typedCanvas.width, typedCanvas.height);

 // Shrink the font until the name fits the canvas width
 let size = 120;
 typedCtx.font = `${size}px ${T.$('font').value}`;
 while (typedCtx.measureText(text).width > typedCanvas.width - 80 && size > 20) {
 size -= 4;
 typedCtx.font = `${size}px ${T.$('font').value}`;
 }

 typedCtx.fillStyle = T.$('ink').value;
 typedCtx.textAlign = 'center';
 typedCtx.textBaseline = 'middle';
 typedCtx.fillText(text, typedCanvas.width / 2, typedCanvas.height / 2);

 T.status('status', 'Typed signature ready.', 'ok');
 }

 function activeCanvas() {
 return T.$('mode').value === 'draw' ? pad : typedCanvas;
 }

 /** Compose the export, honouring the transparency setting. */
 function exportCanvas() {
 const source = activeCanvas();
 const out = document.createElement('canvas');
 out.width = source.width;
 out.height = source.height;
 const ctx = out.getContext('2d');

 if (!T.$('transparent').checked) {
 ctx.fillStyle = '#FFFFFF';
 ctx.fillRect(0, 0, out.width, out.height);
 }

 ctx.drawImage(source, 0, 0);
 return out;
 }

 function syncMode() {
 const draw = T.$('mode').value === 'draw';
 T.$('draw-panel').hidden = !draw;
 T.$('type-panel').hidden = draw;
 if (!draw) renderTyped();
 T.status('status', draw ? 'Draw your signature above.' : 'Type your name above.', 'muted');
 }

 T.$('mode').addEventListener('change', syncMode);
 T.$('typed').addEventListener('input', debounce(renderTyped, 150));
 T.on(['ink', 'font'], () => { redraw(); renderTyped(); }, 'change');
 T.$('stroke').addEventListener('input', () => {
 T.$('stroke-value').textContent = T.$('stroke').value;
 });

 T.$('undo').addEventListener('click', () => {
 if (T.$('mode').value !== 'draw' || !strokes.length) {
 toast({ type: 'warning', title: 'Nothing to undo' });
 return;
 }
 strokes.pop();
 redraw();
 T.status('status', `${strokes.length} stroke(s) remaining.`, 'ok');
 });

 T.$('clear').addEventListener('click', () => {
 strokes = [];
 redraw();
 T.status('status', 'Cleared.', 'muted');
 });

 T.$('download').addEventListener('click', () => {
 if (T.$('mode').value === 'draw' && !strokes.length) {
 toast({ type: 'warning', title: 'Nothing to download', message: 'Draw a signature first.' });
 return;
 }
 exportCanvas().toBlob((blob) => downloadFile(blob, 'signature.png', 'image/png'), 'image/png');
 if (window.Analytics) Analytics.trackToolUse('signature-generator');
 });

 T.$('copy-uri').addEventListener('click', () => {
 copyToClipboard(exportCanvas().toDataURL('image/png'), 'Data URI copied');
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Signature Generator | 123MiniApps' }));

 syncMode();""",
))

# ---------------------------------------------------------------
# 53. Invoice Generator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="invoice-generator", name="Invoice Generator", icon="🧾", cat="generator",
 title="Invoice Generator: Itemised Invoices, Printable to PDF",
 description="Build a clean itemised invoice with automatic totals and tax, then print it to PDF. Everything stays in your browser and can be saved locally.",
 tagline="Build an itemised invoice with automatic totals, print it straight to PDF.",
 workspace=ws(
 row(
 text_input("number", "Invoice number", "INV-0001", "INV-0001"),
 text_input("date", "Issue date", "", "", "date"),
 text_input("due", "Due date", "", "", "date"),
 ),
 row(
 html_block(""" <div class="field">
 <label class="field__label" for="from"><span>From (you)</span></label>
 <textarea class="textarea" id="from" style="min-height:110px" placeholder="Your name&#10;Your address&#10;VAT number"></textarea>
 </div>"""),
 html_block(""" <div class="field">
 <label class="field__label" for="to"><span>Bill to</span></label>
 <textarea class="textarea" id="to" style="min-height:110px" placeholder="Client name&#10;Client address"></textarea>
 </div>"""),
 ),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Line items</span><span class="field__hint">Totals update automatically</span></span>
 <div class="table-scroll" style="max-height:none"><div id="items"></div></div>
 </div>"""),
 buttons(("add-item", "Add a line", "secondary")),
 row(
 number_input("tax", "Tax rate (%)", "20", "20"),
 text_input("currency", "Currency code", "GBP", "GBP"),
 number_input("discount", "Discount (%)", "0", "0"),
 ),
 html_block(""" <div class="field">
 <label class="field__label" for="notes"><span>Notes / payment terms</span></label>
 <textarea class="textarea" id="notes" style="min-height:80px" placeholder="Payment due within 30 days. Bank details…"></textarea>
 </div>"""),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result"><span class="result__value" id="r-subtotal" style="font-size:var(--text-2xl)">, </span><span class="result__label">Subtotal</span></div>
 <div class="result"><span class="result__value" id="r-tax" style="font-size:var(--text-2xl)">, </span><span class="result__label">Tax</span></div>
 <div class="result result--primary"><span class="result__value" id="r-total">, </span><span class="result__label">Total due</span></div>
 </div>"""),
 status_line("status", "Add line items to build the invoice."),
 buttons(("print", "Print / save as PDF", "primary"), ("save", "Save draft"), ("load", "Load draft"), ("download", "Download HTML"), ("share", "Share tool", "ghost")),
 label="Invoice generator",
 ),
 info_block=info(
 features=[
 "Unlimited line items with automatic totals",
 "Tax and discount handling",
 "Print to PDF using your browser's print dialogue",
 "Save and reload drafts on your device",
 "Export as a self-contained HTML file",
 ],
 howto=[
 "Fill in your details and the client's.",
 "Add a line for each item, with quantity and rate.",
 "Set the tax rate and any discount.",
 "Press Print and choose “Save as PDF”.",
 ],
 background_title="What a valid invoice needs",
 background_paragraphs=[
 "Requirements vary by country, but a broadly compliant invoice needs: the word “invoice”, a unique sequential number, the issue date, your name and address, the customer's name and address, a description of what was supplied, the amount due, and the tax treatment. If you are VAT or sales-tax registered, your registration number and the tax charged must appear separately from the net amount.",
 "Sequential numbering matters more than it looks. Tax authorities expect invoice numbers to form an unbroken sequence so that gaps are visible, a missing number invites the question of what was issued and then hidden. Prefixes per client or per year are fine, provided each series is itself sequential.",
 "Two things worth getting right. Payment terms should be explicit, “payment due within 30 days” is enforceable in a way that “payment due on receipt” often is not, and many jurisdictions grant a statutory right to interest on late commercial payments. And retention periods are longer than most people expect: six years is typical in the UK, and some jurisdictions require ten. Since this tool keeps nothing, save the PDF somewhere durable rather than relying on the browser draft, which vanishes when you clear site data.",
 ],
 ),
 script=r""" let items = [];

 function addItem(description = '', quantity = 1, rate = 0) {
 items.push({ description, quantity, rate });
 renderItems();
 calculate();
 }

 function renderItems() {
 const mount = T.$('items');
 mount.innerHTML = '';

 const table = el('table', { className: 'data-table' });
 const thead = el('thead');
 const hr = el('tr');
 ['Description', 'Qty', 'Rate', 'Amount', ''].forEach((h) => hr.append(el('th', { text: h })));
 thead.append(hr);

 const tbody = el('tbody');

 items.forEach((item, index) => {
 const tr = el('tr');

 const descInput = el('input', {
 className: 'input',
 attrs: { type: 'text', value: item.description, placeholder: 'What was supplied',
 'aria-label': `Description for line ${index + 1}` }
 });
 descInput.addEventListener('input', () => { item.description = descInput.value; });

 const qtyInput = el('input', {
 className: 'input',
 attrs: { type: 'number', value: String(item.quantity), step: 'any', min: '0',
 'aria-label': `Quantity for line ${index + 1}`, style: 'max-width:90px' }
 });
 qtyInput.addEventListener('input', () => {
 item.quantity = T.num(qtyInput.value) || 0;
 calculate();
 });

 const rateInput = el('input', {
 className: 'input',
 attrs: { type: 'number', value: String(item.rate), step: 'any', min: '0',
 'aria-label': `Rate for line ${index + 1}`, style: 'max-width:120px' }
 });
 rateInput.addEventListener('input', () => {
 item.rate = T.num(rateInput.value) || 0;
 calculate();
 });

 const amount = el('td', { text: money(item.quantity * item.rate), id: `amount-${index}` });

 const remove = el('button', {
 className: 'btn btn--ghost btn--sm',
 attrs: { type: 'button', 'aria-label': `Remove line ${index + 1}` },
 text: '✕'
 });
 remove.addEventListener('click', () => {
 items.splice(index, 1);
 renderItems();
 calculate();
 });

 tr.append(
 el('td', {}, [descInput]),
 el('td', {}, [qtyInput]),
 el('td', {}, [rateInput]),
 amount,
 el('td', {}, [remove])
 );

 tbody.append(tr);
 });

 table.append(thead, tbody);
 mount.append(table);
 }

 function money(value) {
 const code = (T.$('currency').value || 'GBP').toUpperCase().slice(0, 3);
 try {
 return Number(value).toLocaleString(undefined, { style: 'currency', currency: code });
 } catch {
 return code + ' ' + T.fmt(value, 2);
 }
 }

 function totals() {
 const subtotal = items.reduce((sum, i) => sum + i.quantity * i.rate, 0);
 const discountPct = T.num(T.$('discount').value) || 0;
 const discount = subtotal * (discountPct / 100);
 const afterDiscount = subtotal - discount;
 const taxPct = T.num(T.$('tax').value) || 0;
 const tax = afterDiscount * (taxPct / 100);
 return { subtotal, discount, afterDiscount, tax, total: afterDiscount + tax };
 }

 function calculate() {
 const { subtotal, tax, total } = totals();

 items.forEach((item, i) => {
 const cell = T.$(`amount-${i}`);
 if (cell) cell.textContent = money(item.quantity * item.rate);
 });

 T.$('r-subtotal').textContent = money(subtotal);
 T.$('r-tax').textContent = money(tax);
 T.$('r-total').textContent = money(total);

 T.status('status',
 items.length
 ? `${items.length} line item(s), total ${money(total)}.`
 : 'Add line items to build the invoice.',
 items.length ? 'ok' : 'muted');
 }

 /** Build a self-contained HTML invoice for printing or download. */
 function buildHTML() {
 const { subtotal, discount, tax, total } = totals();
 const discountPct = T.num(T.$('discount').value) || 0;

 const rows = items.map((i) => `
 <tr>
 <td>${T.esc(i.description || ', ')}</td>
 <td style="text-align:right">${T.esc(String(i.quantity))}</td>
 <td style="text-align:right">${T.esc(money(i.rate))}</td>
 <td style="text-align:right">${T.esc(money(i.quantity * i.rate))}</td>
 </tr>`).join('');

 return `<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Invoice ${T.esc(T.$('number').value)}</title>
<style>
 body{font-family:system-ui,-apple-system,sans-serif;color:#111;max-width:800px;margin:40px auto;padding:0 24px;line-height:1.5}
 h1{font-size:32px;margin:0 0 4px}
 .meta{color:#666;margin-bottom:32px}
 .parties{display:flex;gap:48px;margin-bottom:32px}
 .parties div{flex:1}
 .parties h2{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:#666;margin:0 0 8px}
 .parties p{white-space:pre-line;margin:0}
 table{width:100%;border-collapse:collapse;margin-bottom:24px}
 th{text-align:left;font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:#666;border-bottom:2px solid #ddd;padding:8px 4px}
 td{padding:10px 4px;border-bottom:1px solid #eee}
 .totals{margin-left:auto;width:300px}
 .totals tr td{border:none;padding:6px 4px}
 .totals tr:last-child td{border-top:2px solid #111;font-weight:700;font-size:18px;padding-top:12px}
 .notes{margin-top:40px;padding-top:16px;border-top:1px solid #eee;white-space:pre-line;color:#444;font-size:14px}
 @media print{body{margin:0}}
</style></head><body>
<h1>Invoice</h1>
<p class="meta"><strong>${T.esc(T.$('number').value)}</strong><br>
Issued: ${T.esc(T.$('date').value || ', ')}<br>
Due: ${T.esc(T.$('due').value || ', ')}</p>

<div class="parties">
 <div><h2>From</h2><p>${T.esc(T.$('from').value || ', ')}</p></div>
 <div><h2>Bill to</h2><p>${T.esc(T.$('to').value || ', ')}</p></div>
</div>

<table>
 <thead><tr><th>Description</th><th style="text-align:right">Qty</th><th style="text-align:right">Rate</th><th style="text-align:right">Amount</th></tr></thead>
 <tbody>${rows}</tbody>
</table>

<table class="totals">
 <tr><td>Subtotal</td><td style="text-align:right">${T.esc(money(subtotal))}</td></tr>
 ${discountPct ? `<tr><td>Discount (${discountPct}%)</td><td style="text-align:right">−${T.esc(money(discount))}</td></tr>` : ''}
 <tr><td>Tax (${T.esc(String(T.num(T.$('tax').value) || 0))}%)</td><td style="text-align:right">${T.esc(money(tax))}</td></tr>
 <tr><td>Total due</td><td style="text-align:right">${T.esc(money(total))}</td></tr>
</table>

${T.$('notes').value ? `<div class="notes">${T.esc(T.$('notes').value)}</div>` : ''}
</body></html>`;
 }

 T.$('add-item').addEventListener('click', () => addItem());

 T.on(['tax', 'discount', 'currency'], calculate);

 T.$('print').addEventListener('click', () => {
 if (!items.length) {
 toast({ type: 'warning', title: 'Add a line item first' });
 return;
 }
 const win = window.open('', '_blank');
 if (!win) {
 toast({ type: 'error', title: 'Popup blocked', message: 'Allow popups, or use Download HTML.' });
 return;
 }
 win.document.write(buildHTML());
 win.document.close();
 win.focus();
 setTimeout(() => win.print(), 250);
 if (window.Analytics) Analytics.trackToolUse('invoice-generator');
 });

 T.$('download').addEventListener('click', () => {
 downloadFile(buildHTML(), `invoice-${T.$('number').value || 'draft'}.html`, 'text/html');
 });

 T.$('save').addEventListener('click', () => {
 const draft = {
 number: T.$('number').value, date: T.$('date').value, due: T.$('due').value,
 from: T.$('from').value, to: T.$('to').value, notes: T.$('notes').value,
 tax: T.$('tax').value, discount: T.$('discount').value, currency: T.$('currency').value,
 items
 };
 T.store.set('invoice-draft', draft)
 ? toast({ type: 'success', title: 'Draft saved', message: 'Stored on this device only.' })
 : toast({ type: 'error', title: 'Could not save', message: 'Browser storage is unavailable.' });
 });

 T.$('load').addEventListener('click', () => {
 const draft = T.store.get('invoice-draft');
 if (!draft) {
 toast({ type: 'warning', title: 'No saved draft found' });
 return;
 }
 ['number', 'date', 'due', 'from', 'to', 'notes', 'tax', 'discount', 'currency']
 .forEach((k) => { if (draft[k] !== undefined) T.$(k).value = draft[k]; });
 items = draft.items || [];
 renderItems();
 calculate();
 toast({ type: 'success', title: 'Draft loaded' });
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Invoice Generator | 123MiniApps' }));

 // Sensible starting state
 const today = new Date();
 const due = new Date(today.getTime() + 30 * 86400000);
 T.$('date').value = today.toISOString().slice(0, 10);
 T.$('due').value = due.toISOString().slice(0, 10);

 addItem('Consulting services', 10, 75);
 calculate();""",
))

# ---------------------------------------------------------------
# 54. Gradient Generator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="gradient-generator", name="Gradient Generator", icon="🌈", cat="generator",
 title="CSS Gradient Generator: Linear, Radial and Conic",
 description="Design linear, radial and conic CSS gradients with unlimited colour stops and a live preview. Copy the CSS or Tailwind arbitrary-value class.",
 tagline="Design CSS gradients visually, linear, radial or conic, with unlimited stops.",
 workspace=ws(
 row(
 select("type", "Gradient type", [
 ("linear", "Linear"), ("radial", "Radial"), ("conic", "Conic"),
 ], selected="linear"),
 slider("angle", "Angle", 0, 360, 135, 5, unit="°"),
 select("shape", "Radial shape", [("circle", "Circle"), ("ellipse", "Ellipse")], selected="circle"),
 ),
 html_block(""" <div class="field">
 <span class="field__label"><span>Colour stops</span><span class="field__hint">At least two required</span></span>
 <div id="stops"></div>
 </div>"""),
 buttons(("add-stop", "Add a stop", "secondary"), ("random", "Random gradient"), ("reverse", "Reverse order")),
 status_line("status", "Adjust the stops to build your gradient."),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Preview</span></span>
 <div id="preview" style="height:220px;border-radius:var(--radius-lg);border:1px solid var(--border-color)"></div>
 </div>"""),
 output("css", "CSS", None, "The CSS will appear here."),
 buttons(("copy", "Copy CSS", "primary"), ("copy-tailwind", "Copy Tailwind class"), ("download", "Download"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Presets</span></span>
 <div class="chip-grid" id="presets"></div>
 </div>"""),
 label="Gradient generator",
 ),
 info_block=info(
 features=[
 "Linear, radial and conic gradients",
 "Unlimited colour stops with position control",
 "Live preview at full width",
 "Copies plain CSS or a Tailwind arbitrary value",
 "Eight starting presets",
 ],
 howto=[
 "Pick a gradient type.",
 "Adjust the colour stops and their positions.",
 "Set the angle for linear and conic gradients.",
 "Copy the CSS straight into your stylesheet.",
 ],
 background_title="Getting gradients to look right",
 background_paragraphs=[
 "The commonest problem is the grey dead zone. Interpolating between two saturated complementary colours in sRGB passes through a desaturated middle, blue to yellow goes through a muddy grey rather than through green. Adding an intermediate stop in the hue you actually want fixes it. Newer CSS lets you interpolate in a perceptual space with <code>in oklch</code>, which avoids the problem entirely, though browser support is still uneven.",
 "Banding is the other frequent complaint, visible as distinct stripes across a large, subtle gradient. It happens because 8-bit colour has only 256 levels per channel, and a gentle transition across a wide area cannot supply enough distinct values. Adding a very subtle noise texture over the top is the standard fix and works well.",
 "Angles are worth memorising because CSS differs from the mathematical convention: <code>0deg</code> points up, <code>90deg</code> points right, and the angle increases clockwise. Conic gradients are the odd one out in usefulness, they are the natural way to build pie charts and colour wheels in pure CSS, since the colour sweeps around a centre point rather than along a line.",
 ],
 ),
 script=r""" let stops = [
 { colour: '#00D4FF', position: 0 },
 { colour: '#7B61FF', position: 100 }
 ];

 const PRESETS = [
 ['Midnight', ['#00D4FF', '#7B61FF']],
 ['Sunset', ['#FF6B35', '#FFD700']],
 ['Emerald', ['#00FF88', '#FFD700']],
 ['Rose gold', ['#F472B6', '#FB923C']],
 ['Ocean', ['#0891B2', '#059669']],
 ['Amethyst', ['#A855F7', '#EC4899']],
 ['Ember', ['#DC2626', '#F59E0B', '#FDE047']],
 ['Aurora', ['#22D3EE', '#818CF8', '#F472B6']]
 ];

 function renderStops() {
 const mount = T.$('stops');
 mount.innerHTML = '';

 stops.forEach((stop, index) => {
 const rowEl = el('div', {
 className: 'workspace__row',
 style: { alignItems: 'end', marginBottom: 'var(--space-3)' }
 });

 const colour = el('input', {
 className: 'input',
 attrs: { type: 'color', value: stop.colour, 'aria-label': `Colour for stop ${index + 1}` },
 style: { height: '48px', padding: '4px', cursor: 'pointer' }
 });
 colour.addEventListener('input', () => { stop.colour = colour.value; render(); });

 const position = el('input', {
 className: 'range',
 attrs: { type: 'range', min: '0', max: '100', value: String(stop.position),
 'aria-label': `Position for stop ${index + 1}` }
 });
 const posLabel = el('span', { className: 'field__hint', text: stop.position + '%' });
 position.addEventListener('input', () => {
 stop.position = Number(position.value);
 posLabel.textContent = stop.position + '%';
 render();
 });

 const remove = el('button', {
 className: 'btn btn--ghost btn--sm',
 attrs: { type: 'button', 'aria-label': `Remove stop ${index + 1}` },
 text: '✕'
 });
 remove.addEventListener('click', () => {
 if (stops.length <= 2) {
 toast({ type: 'warning', title: 'A gradient needs at least two stops' });
 return;
 }
 stops.splice(index, 1);
 renderStops();
 render();
 });

 rowEl.append(
 el('div', { className: 'field' }, [colour]),
 el('div', { className: 'field' }, [position, posLabel]),
 el('div', { className: 'field' }, [remove])
 );

 mount.append(rowEl);
 });
 }

 function gradientCSS() {
 const sorted = [...stops].sort((a, b) => a.position - b.position);
 const list = sorted.map((s) => `${s.colour} ${s.position}%`).join(', ');
 const type = T.$('type').value;
 const angle = Number(T.$('angle').value);

 if (type === 'linear') return `linear-gradient(${angle}deg, ${list})`;
 if (type === 'radial') return `radial-gradient(${T.$('shape').value} at center, ${list})`;
 return `conic-gradient(from ${angle}deg at center, ${list})`;
 }

 function render() {
 const css = gradientCSS();

 T.$('preview').style.background = css;
 T.setOutput('css', `background: ${css};`);

 T.$('angle-value').textContent = T.$('angle').value;

 // Angle is meaningless for radial; shape is meaningless for the others
 const type = T.$('type').value;
 T.$('angle').closest('.field').style.display = type === 'radial' ? 'none' : '';
 T.$('shape').closest('.field').style.display = type === 'radial' ? '' : 'none';

 T.status('status', `${stops.length} colour stop(s).`, 'ok');
 if (window.Analytics) Analytics.trackToolUse('gradient-generator');
 }

 function renderPresets() {
 const mount = T.$('presets');
 mount.innerHTML = '';

 PRESETS.forEach(([name, colours]) => {
 const chip = el('button', { className: 'chip', attrs: { type: 'button' }, text: name });
 chip.style.background = `linear-gradient(135deg, ${colours.join(', ')})`;
 chip.style.color = '#fff';
 chip.style.textShadow = '0 1px 3px rgba(0,0,0.6)';
 chip.style.borderColor = 'transparent';

 chip.addEventListener('click', () => {
 stops = colours.map((c, i) => ({
 colour: c,
 position: Math.round((i / (colours.length - 1)) * 100)
 }));
 renderStops();
 render();
 });

 mount.append(chip);
 });
 }

 T.$('add-stop').addEventListener('click', () => {
 stops.push({ colour: T.rgbToHex(...Object.values(hslRandom())), position: 50 });
 renderStops();
 render();
 });

 function hslRandom() {
 return T.hslToRgb(T.randomInt(0, 359), T.randomInt(60, 95), T.randomInt(45, 65));
 }

 T.$('random').addEventListener('click', () => {
 const count = T.randomInt(2, 4);
 const baseHue = T.randomInt(0, 359);
 stops = Array.from({ length: count }, (_, i) => {
 const rgb = T.hslToRgb(baseHue + i * T.randomInt(25, 70), T.randomInt(65, 95), T.randomInt(45, 65));
 return {
 colour: T.rgbToHex(rgb.r, rgb.g, rgb.b),
 position: Math.round((i / (count - 1)) * 100)
 };
 });
 T.$('angle').value = String(T.randomInt(0, 71) * 5);
 renderStops();
 render();
 });

 T.$('reverse').addEventListener('click', () => {
 stops = stops.map((s) => ({ ...s, position: 100 - s.position }));
 renderStops();
 render();
 });

 T.on(['type', 'shape'], render, 'change');
 T.$('angle').addEventListener('input', render);

 T.$('copy').addEventListener('click', () =>
 copyToClipboard(`background: ${gradientCSS()};`, 'CSS copied'));

 T.$('copy-tailwind').addEventListener('click', () =>
 copyToClipboard(`bg-[${gradientCSS().replace(/\s+/g, '_')}]`, 'Tailwind class copied'));

 T.$('download').addEventListener('click', () =>
 downloadFile(`.gradient {\n background: ${gradientCSS()};\n}\n`, 'gradient.css', 'text/css'));

 T.$('share').addEventListener('click', () => shareLink({ title: 'Gradient Generator | 123MiniApps' }));

 renderStops();
 renderPresets();
 render();""",
))
