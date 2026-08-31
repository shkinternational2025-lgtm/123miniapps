#!/usr/bin/env python3
# ============================================
# 123MiniApps.online v2.0
# File: tools_security.py
# Purpose: The 5 Security Tools (ids 65-69).
#
# NOTE: these tools handle sensitive input. Every one
# of them must stay strictly client-side, and the
# copy must be honest about what it does and does not
# protect against.
# ============================================

from toolkit import (
 tool, ws, info, row, textarea, text_input, number_input, select, switch,
 slider, output, status_line, buttons, HR, html_block,
)

PAGES = []

# ---------------------------------------------------------------
# 65. Password Strength Checker
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="password-strength-checker", name="Password Strength Checker", icon="🛡️", cat="security",
 title="Password Strength Checker: Entropy and Crack Time Estimate",
 description="Score a password on entropy in bits and estimate how long it would take to crack offline. Detects common patterns. Nothing is transmitted.",
 tagline="Measure password entropy and estimate crack time, analysed entirely in your browser.",
 workspace=ws(
 html_block(""" <p class="field__hint" style="color:var(--warning)">
 Never type a password you actually use into a website you have not verified. This page analyses
 input locally and makes no network requests, you can confirm that in the DevTools Network tab
 before typing. If in any doubt, test a password of the same shape rather than the real one.
 </p>"""),
 html_block(""" <div class="field">
 <label class="field__label" for="password">
 <span>Password to analyse</span>
 <span class="field__hint" id="length-hint"></span>
 </label>
 <input class="input font-mono" id="password" type="text" autocomplete="off"
 spellcheck="false" placeholder="Type or paste a password"
 style="font-size:var(--text-lg);height:56px">
 </div>"""),
 html_block(""" <div class="meter" id="meter" role="img" aria-label="Password strength">
 <span class="meter__seg"></span><span class="meter__seg"></span>
 <span class="meter__seg"></span><span class="meter__seg"></span>
 </div>"""),
 status_line("status", "Type a password to analyse it."),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result result--primary"><span class="result__value" id="r-entropy">, </span><span class="result__label">Entropy (bits)</span></div>
 <div class="result"><span class="result__value" id="r-verdict" style="font-size:var(--text-xl)">, </span><span class="result__label">Verdict</span></div>
 <div class="result"><span class="result__value" id="r-pool" style="font-size:var(--text-2xl)">, </span><span class="result__label">Character pool</span></div>
 </div>"""),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Estimated time to crack offline</span><span class="field__hint">Assuming the hash has leaked</span></span>
 <div class="table-scroll"><div id="crack"></div></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Weaknesses detected</span></span>
 <div id="warnings"></div>
 </div>"""),
 buttons(("generate", "Suggest a strong password", "primary"), ("clear", "Clear", "ghost"), ("share", "Share tool", "ghost")),
 label="Password strength checker",
 ),
 info_block=info(
 features=[
 "Entropy calculated in bits from the actual character pool",
 "Crack-time estimates across four attacker capabilities",
 "Detects dictionary words, keyboard runs and repetition",
 "Penalises predictable substitutions like @ for a",
 "Runs entirely in your browser",
 ],
 howto=[
 "Type or paste a password into the field.",
 "Read the entropy figure and the verdict.",
 "Check the weaknesses list for specific problems.",
 "Use the suggest button if you need a stronger one.",
 ],
 background_title="What entropy measures, and what it misses",
 background_paragraphs=[
 "Entropy in bits describes the size of the search space: each additional bit doubles the number of guesses needed. A password drawn randomly from a 95-character keyboard set carries about 6.6 bits per character, so a 12-character random password is roughly 79 bits. Below 50 bits is weak against a determined offline attack, around 70 is reasonable, and above 100 bits is beyond any foreseeable brute-force capability.",
 "The critical caveat is that this arithmetic only holds for <em>randomly generated</em> passwords. Entropy calculated from the character pool badly overstates the strength of anything a human chose. <code>Password123!</code> scores about 79 bits by that formula but appears in every cracking dictionary and falls in milliseconds. Real attackers do not brute-force blindly, they start with leaked password lists, dictionary words with common substitutions, and keyboard patterns. That is why the weaknesses panel matters more than the headline number.",
 "The crack-time figures assume the attacker has stolen a database and is attacking the hashes offline, which is the realistic threat. The rates vary enormously by hashing algorithm: a consumer GPU manages billions of SHA-256 guesses per second but only tens of thousands against properly configured bcrypt or Argon2. That difference is entirely the defender's choice, which is why how a site stores your password matters as much as how you chose it. In practice, length beats complexity, uniqueness beats both, and a password manager beats trying to remember any of it.",
 ],
 ),
 script=r""" const COMMON = new Set(('password passwd 123456 12345678 123456789 qwerty abc123 letmein monkey ' +
 'dragon baseball football superman batman trustno1 iloveyou welcome admin login master hello ' +
 'freedom whatever qazwsx sunshine princess starwars shadow michael jennifer jordan harley ranger ' +
 'hunter buster soccer hockey killer george charlie andrew michelle love secret summer').split(' '));

 const KEYBOARD_ROWS = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm', '1234567890'];

 // Guesses per second for an offline attack, by attacker capability
 const ATTACKERS = [
 ['Ordinary laptop, fast hash (SHA-256)', 1e9],
 ['Single high-end GPU, fast hash', 1e11],
 ['GPU cluster, fast hash', 1e13],
 ['Single GPU against bcrypt (cost 12)', 2e4]
 ];

 function characterPool(password) {
 let pool = 0;
 if (/[a-z]/.test(password)) pool += 26;
 if (/[A-Z]/.test(password)) pool += 26;
 if (/[0-9]/.test(password)) pool += 10;
 if (/[^a-zA-Z0-9\s]/.test(password)) pool += 33;
 if (/\s/.test(password)) pool += 1;
 return pool;
 }

 /**
 * Detect patterns that make a password far weaker than its raw
 * entropy suggests. Each returns a penalty in bits.
 * @returns {{message: string, penalty: number}[]}
 */
 function findWeaknesses(password) {
 const found = [];
 const lower = password.toLowerCase();

 if (password.length < 8) {
 found.push({ message: 'Shorter than 8 characters, trivially brute-forced.', penalty: 0 });
 }

 // Common password, possibly with leetspeak substitutions
 const deleeted = lower
 .replace(/[@4]/g, 'a').replace(/[3]/g, 'e').replace(/[1!|]/g, 'i')
 .replace(/[0]/g, 'o').replace(/[5$]/g, 's').replace(/[7]/g, 't');

 for (const word of COMMON) {
 if (deleeted.includes(word) && word.length >= 4) {
 found.push({
 message: `Contains the common password “${word}”${deleeted !== lower ? ' (character substitutions do not help)' : ''}.`,
 penalty: 25
 });
 break;
 }
 }

 // Keyboard runs
 for (const row of KEYBOARD_ROWS) {
 for (let i = 0; i <= row.length - 4; i++) {
 const run = row.slice(i, i + 4);
 if (lower.includes(run) || lower.includes([...run].reverse().join(''))) {
 found.push({ message: `Contains the keyboard run “${run}”.`, penalty: 15 });
 i = row.length;
 break;
 }
 }
 }

 // Sequential characters
 if (/(?:abc|bcd|cde|def|123|234|345|456|567|678|789|890)/.test(lower)) {
 found.push({ message: 'Contains a sequential run such as “abc” or “123”.', penalty: 12 });
 }

 // Repetition
 if (/(.)\1{2,}/.test(password)) {
 found.push({ message: 'Contains a character repeated three or more times.', penalty: 10 });
 }

 // A short repeating unit, "abcabcabc"
 for (let unit = 1; unit <= password.length / 2; unit++) {
 const chunk = password.slice(0, unit);
 if (chunk.repeat(Math.ceil(password.length / unit)).slice(0, password.length) === password
 && password.length / unit >= 3) {
 found.push({ message: `Made of the repeated unit “${chunk}”.`, penalty: 20 });
 break;
 }
 }

 // A four-digit year is a very common component
 if (/(19|20)\d{2}/.test(password)) {
 found.push({ message: 'Contains what looks like a year, commonly guessed.', penalty: 8 });
 }

 // Digits appended to the end is the single most common pattern
 if (/^[a-zA-Z]+\d{1,4}!?$/.test(password)) {
 found.push({
 message: 'Follows the “word + digits” pattern that cracking tools try first.',
 penalty: 18
 });
 }

 // Single character class
 const pool = characterPool(password);
 if (pool <= 26 && password.length > 0) {
 found.push({ message: 'Uses only one character class.', penalty: 0 });
 }

 return found;
 }

 function humanTime(seconds) {
 if (seconds < 1) return 'instantly';
 if (seconds < 60) return `${Math.round(seconds)} seconds`;
 if (seconds < 3600) return `${Math.round(seconds / 60)} minutes`;
 if (seconds < 86400) return `${Math.round(seconds / 3600)} hours`;
 if (seconds < 2592000) return `${Math.round(seconds / 86400)} days`;
 if (seconds < 31536000) return `${Math.round(seconds / 2592000)} months`;

 const years = seconds / 31536000;
 if (years < 1000) return `${Math.round(years)} years`;
 if (years < 1e6) return `${Math.round(years / 1000)} thousand years`;
 if (years < 1e9) return `${(years / 1e6).toFixed(1)} million years`;
 if (years < 1e12) return `${(years / 1e9).toFixed(1)} billion years`;
 return 'longer than the age of the universe';
 }

 function analyse() {
 const password = T.$('password').value;
 T.$('length-hint').textContent = password ? `${password.length} characters` : '';

 if (!password) {
 ['r-entropy', 'r-verdict', 'r-pool'].forEach((id) => { T.$(id).textContent = ', '; });
 T.$('crack').innerHTML = '';
 T.$('warnings').innerHTML = '';
 T.$$('#meter .meter__seg').forEach((seg) => { seg.className = 'meter__seg'; });
 T.status('status', 'Type a password to analyse it.', 'muted');
 return;
 }

 const pool = characterPool(password);
 const rawEntropy = password.length * Math.log2(pool || 1);

 const weaknesses = findWeaknesses(password);
 const penalty = weaknesses.reduce((sum, w) => sum + w.penalty, 0);
 const entropy = Math.max(0, rawEntropy - penalty);

 T.$('r-entropy').textContent = Math.round(entropy);
 T.$('r-pool').textContent = pool + ' chars';

 // Verdict bands
 let level, key, verdict;
 if (entropy < 40) { level = 1; key = 'weak'; verdict = 'Very weak'; }
 else if (entropy < 60) { level = 2; key = 'fair'; verdict = 'Weak'; }
 else if (entropy < 80) { level = 3; key = 'good'; verdict = 'Reasonable'; }
 else { level = 4; key = 'strong'; verdict = 'Strong'; }

 T.$('r-verdict').textContent = verdict;
 T.$('r-verdict').style.color =
 { weak: 'var(--danger)', fair: 'var(--warning)', good: 'var(--info)', strong: 'var(--success)' }[key];

 T.$$('#meter .meter__seg').forEach((seg, i) => {
 seg.className = 'meter__seg' + (i < level ? ` is-on-${key}` : '');
 });

 // Crack times, expected effort is half the search space
 const guesses = Math.pow(2, entropy) / 2;
 const mount = T.$('crack');
 mount.innerHTML = '';
 mount.append(T.table(
 ['Attacker', 'Guesses per second', 'Time to crack'],
 ATTACKERS.map(([name, rate]) => [name, rate.toExponential(0), humanTime(guesses / rate)])
 ));

 renderWarnings(weaknesses, penalty);

 T.status('status',
 penalty > 0
 ? `${Math.round(rawEntropy)} bits on paper, but ${Math.round(entropy)} after ${penalty} bits of pattern penalties.`
 : `${Math.round(entropy)} bits of entropy with no obvious patterns detected.`,
 key === 'strong' ? 'ok' : key === 'good' ? 'ok' : 'warn');

 if (window.Analytics) Analytics.trackToolUse('password-strength-checker');
 }

 function renderWarnings(weaknesses, penalty) {
 const mount = T.$('warnings');
 mount.innerHTML = '';

 if (!weaknesses.length) {
 mount.append(el('p', {
 className: 'text-sm',
 text: '✓ No common weaknesses detected.',
 style: { color: 'var(--success)' }
 }));
 return;
 }

 const list = el('ul', { className: 'stack-sm' });
 weaknesses.forEach((w) => {
 list.append(el('li', {
 className: 'text-sm',
 text: (w.penalty ? `− ${w.penalty} bits: ` : '• ') + w.message,
 style: { color: w.penalty >= 15 ? 'var(--danger)' : 'var(--warning)' }
 }));
 });

 mount.append(list);
 void penalty;
 }

 T.$('password').addEventListener('input', debounce(analyse, 200));

 T.$('generate').addEventListener('click', () => {
 // Four random words plus a separator and digits reads better and
 // remembers better than a random character string of equal strength
 const WORDS = ('anchor bright cactus dolphin ember falcon granite harbour ivory jasmine ' +
 'kestrel lantern marble nectar orchid pepper quartz ribbon saffron thunder umber velvet ' +
 'willow xenon yarrow zephyr copper silver meadow canyon).').split(' ');

 const picked = Array.from({ length: 4 }, () => T.pick(WORDS).replace(/[^a-z]/g, ''));
 const suggestion = picked.join('-') + '-' + T.randomInt(10, 99);

 T.$('password').value = suggestion;
 analyse();
 toast({ type: 'success', title: 'Suggested a passphrase', message: 'Generated locally, copy it before leaving.' });
 });

 T.$('clear').addEventListener('click', () => {
 T.$('password').value = '';
 analyse();
 toast({ type: 'success', title: 'Cleared', message: 'The password is gone from this page.' });
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Password Strength Checker | 123MiniApps' }));

 analyse();""",
))

# ---------------------------------------------------------------
# 66. Encryption Tool
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="encryption-tool", name="Encryption Tool", icon="🔐", cat="security",
 title="AES-256 Encryption Tool: Encrypt Text With a Passphrase",
 description="Encrypt and decrypt text with AES-256-GCM using a passphrase. Keys are derived with PBKDF2 and everything runs through the browser's Web Crypto API.",
 tagline="Encrypt text with AES-256-GCM and a passphrase, entirely in your browser.",
 workspace=ws(
 select("mode", "Mode", [("encrypt", "Encrypt"), ("decrypt", "Decrypt")], selected="encrypt"),
 textarea("input", "Message", "Type the text you want to encrypt…", "input-stats", rows=150),
 row(
 html_block(""" <div class="field">
 <label class="field__label" for="passphrase"><span>Passphrase</span></label>
 <input class="input" id="passphrase" type="password" autocomplete="new-password"
 placeholder="A long passphrase you can remember">
 </div>"""),
 select("iterations", "PBKDF2 iterations", [
 ("310000", "310,000, OWASP recommended"),
 ("600000", "600,000, stronger, slower"),
 ("100000", "100,000, faster, weaker"),
 ], selected="310000"),
 ),
 switch("show-pass", "Show the passphrase", False),
 status_line("status", "Enter a message and a passphrase."),
 HR,
 output("output", "Result", "output-stats"),
 buttons(("run", "Encrypt", "primary"), ("copy", "Copy result"), ("download", "Download"), ("swap", "Swap direction"), ("share", "Share tool", "ghost")),
 html_block(""" <p class="field__hint">
 The output bundles the salt, the initialisation vector and the ciphertext together in one
 Base64 string, so you only need to keep that and the passphrase. There is no recovery mechanism:
 lose the passphrase and the data is gone permanently.
 </p>"""),
 label="Encryption tool",
 ),
 info_block=info(
 features=[
 "AES-256-GCM authenticated encryption",
 "PBKDF2-SHA-256 key derivation with a configurable work factor",
 "Random salt and IV generated for every message",
 "Self-contained output, salt and IV travel with the ciphertext",
 "Uses the browser's audited Web Crypto implementation",
 ],
 howto=[
 "Choose Encrypt and type your message.",
 "Enter a long passphrase and press Encrypt.",
 "Copy the whole output string and store it safely.",
 "To reverse it, switch to Decrypt and supply the same passphrase.",
 ],
 background_title="How this works, and what it is not suitable for",
 background_paragraphs=[
 "AES-GCM is authenticated encryption: it provides confidentiality and integrity together. If a single bit of the ciphertext is altered, decryption fails outright rather than returning corrupted plaintext. That is why a wrong passphrase produces an error rather than garbage. A fresh 96-bit initialisation vector is generated for every message, which is essential, reusing an IV with the same key in GCM catastrophically breaks the cipher and can expose the key.",
 "Your passphrase is not the key. It is stretched into one using PBKDF2 with a random 128-bit salt and, by default, 310,000 iterations of SHA-256, the figure OWASP currently recommends. The salt means two people with identical passphrases get different keys, and the iteration count makes brute-forcing the passphrase expensive. The strength of the whole scheme still rests on the passphrase: a short one falls to a dictionary attack regardless of the iteration count.",
 "Be clear about the limits. This is a useful way to protect a note before emailing it or storing it somewhere you do not fully trust, but it is not a secure messaging system. There is no forward secrecy, no identity verification, and no safe channel here for sharing the passphrase, sending it alongside the ciphertext defeats the entire exercise. For ongoing private communication use a purpose-built tool like Signal or age, and for anything where lives or livelihoods depend on the secrecy, use software that has been formally audited.",
 ],
 ),
 script=r""" let lastResult = '';

 const encoder = new TextEncoder();
 const decoder = new TextDecoder();

 /**
 * Stretch a passphrase into a 256-bit AES key.
 * @param {string} passphrase
 * @param {Uint8Array} salt
 * @param {number} iterations
 * @returns {Promise<CryptoKey>}
 */
 async function deriveKey(passphrase, salt, iterations) {
 const material = await crypto.subtle.importKey(
 'raw', encoder.encode(passphrase), 'PBKDF2', false, ['deriveKey']
 );

 return crypto.subtle.deriveKey(
 { name: 'PBKDF2', salt, iterations, hash: 'SHA-256' },
 material,
 { name: 'AES-GCM', length: 256 },
 false,
 ['encrypt', 'decrypt']
 );
 }

 function toBase64(bytes) {
 let binary = '';
 const chunk = 0x8000;
 for (let i = 0; i < bytes.length; i += chunk) {
 binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
 }
 return btoa(binary);
 }

 function fromBase64(b64) {
 const binary = atob(b64.replace(/\s+/g, ''));
 const bytes = new Uint8Array(binary.length);
 for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
 return bytes;
 }

 /**
 * Output layout, all concatenated then Base64-encoded:
 * magic (4) | iterations (4, big-endian) | salt (16) | iv (12) | ciphertext
 * Bundling the parameters means the recipient needs only the string
 * and the passphrase.
 */
 const MAGIC = [0x31, 0x32, 0x33, 0x4d]; // "123M"

 async function encrypt(plaintext, passphrase, iterations) {
 const salt = crypto.getRandomValues(new Uint8Array(16));
 const iv = crypto.getRandomValues(new Uint8Array(12));
 const key = await deriveKey(passphrase, salt, iterations);

 const ciphertext = new Uint8Array(
 await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, encoder.encode(plaintext))
 );

 const header = new Uint8Array(8);
 header.set(MAGIC, 0);
 new DataView(header.buffer).setUint32(4, iterations, false);

 const out = new Uint8Array(header.length + salt.length + iv.length + ciphertext.length);
 out.set(header, 0);
 out.set(salt, header.length);
 out.set(iv, header.length + salt.length);
 out.set(ciphertext, header.length + salt.length + iv.length);

 return toBase64(out);
 }

 async function decrypt(payload, passphrase) {
 let bytes;
 try {
 bytes = fromBase64(payload.trim());
 } catch {
 throw new Error('That does not look like Base64, check you copied the whole string.');
 }

 if (bytes.length < 36) throw new Error('The input is too short to be a valid message.');

 const magicOk = MAGIC.every((b, i) => bytes[i] === b);
 if (!magicOk) throw new Error('This was not produced by this tool.');

 const iterations = new DataView(bytes.buffer, bytes.byteOffset).getUint32(4, false);
 const salt = bytes.slice(8, 24);
 const iv = bytes.slice(24, 36);
 const ciphertext = bytes.slice(36);

 const key = await deriveKey(passphrase, salt, iterations);

 try {
 const plain = await crypto.subtle.decrypt({ name: 'AES-GCM', iv }, key, ciphertext);
 return { text: decoder.decode(plain), iterations };
 } catch {
 // GCM authentication failure, wrong passphrase or tampering
 throw new Error('Decryption failed. The passphrase is wrong, or the message has been altered.');
 }
 }

 async function run() {
 const text = T.$('input').value;
 const passphrase = T.$('passphrase').value;
 const encrypting = T.$('mode').value === 'encrypt';

 if (!text.trim()) {
 T.status('status', 'Enter a message first.', 'error');
 return;
 }

 if (!passphrase) {
 T.status('status', 'Enter a passphrase.', 'error');
 return;
 }

 if (encrypting && passphrase.length < 8) {
 T.status('status', 'Use a passphrase of at least 8 characters, longer is much better.', 'warn');
 }

 T.$('run').classList.add('is-loading');
 T.status('status', 'Deriving key…', 'muted');

 try {
 if (encrypting) {
 const iterations = Number(T.$('iterations').value);
 lastResult = await encrypt(text, passphrase, iterations);
 T.setOutput('output', lastResult);
 T.$('output-stats').textContent = lastResult.length.toLocaleString() + ' characters';
 T.status('status',
 `Encrypted with AES-256-GCM using ${iterations.toLocaleString()} PBKDF2 iterations.`, 'ok');
 } else {
 const { text: plain, iterations } = await decrypt(text, passphrase);
 lastResult = plain;
 T.setOutput('output', lastResult);
 T.$('output-stats').textContent = lastResult.length.toLocaleString() + ' characters';
 T.status('status',
 `Decrypted successfully. The message used ${iterations.toLocaleString()} iterations.`, 'ok');
 }

 if (window.Analytics) Analytics.trackToolUse('encryption-tool');
 } catch (err) {
 lastResult = '';
 T.setOutput('output', '');
 T.status('status', err.message, 'error');
 } finally {
 T.$('run').classList.remove('is-loading');
 }
 }

 function syncMode() {
 const encrypting = T.$('mode').value === 'encrypt';
 T.$('run').querySelector('span') || null;
 T.$('run').textContent = encrypting ? 'Encrypt' : 'Decrypt';
 T.$('input').placeholder = encrypting
 ? 'Type the text you want to encrypt…'
 : 'Paste the encrypted string…';
 T.$('iterations').closest('.field').style.display = encrypting ? '' : 'none';
 }

 T.$('mode').addEventListener('change', syncMode);
 T.$('run').addEventListener('click', run);

 T.$('show-pass').addEventListener('change', () => {
 T.$('passphrase').type = T.$('show-pass').checked ? 'text' : 'password';
 });

 T.$('swap').addEventListener('click', () => {
 if (!lastResult) return;
 T.$('input').value = lastResult;
 T.$('mode').value = T.$('mode').value === 'encrypt' ? 'decrypt' : 'encrypt';
 syncMode();
 T.setOutput('output', '');
 lastResult = '';
 });

 T.$('input').addEventListener('input', debounce(() => {
 T.$('input-stats').textContent = T.$('input').value.length.toLocaleString() + ' characters';
 }, 250));

 T.wireActions({ slug: 'encryption-tool', getResult: () => lastResult, filename: 'encrypted.txt' });

 syncMode();""",
))

# ---------------------------------------------------------------
# 67. Hash Comparison
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="hash-comparison", name="Hash Comparison", icon="🔍", cat="security",
 title="Hash Comparison: Verify Checksums and Compare Digests",
 description="Compare two hashes or verify a downloaded file against a published checksum. Constant-time comparison, with automatic algorithm detection.",
 tagline="Verify a download against its published checksum, or compare two hashes safely.",
 workspace=ws(
 select("mode", "What do you want to do?", [
 ("compare", "Compare two hashes"),
 ("file", "Verify a file against a published hash"),
 ], selected="compare"),
 html_block(""" <div id="compare-panel">
 <div class="field">
 <label class="field__label" for="hash-a"><span>Hash A</span><span class="field__hint" id="a-type"></span></label>
 <input class="input font-mono" id="hash-a" type="text" placeholder="Paste the first hash" autocomplete="off" spellcheck="false">
 </div>
 <div class="field">
 <label class="field__label" for="hash-b"><span>Hash B</span><span class="field__hint" id="b-type"></span></label>
 <input class="input font-mono" id="hash-b" type="text" placeholder="Paste the second hash" autocomplete="off" spellcheck="false">
 </div>
 </div>"""),
 html_block(""" <div id="file-panel" hidden>
 <div class="dropzone" id="dropzone" role="button" tabindex="0" aria-label="Choose a file to checksum">
 <span class="dropzone__icon" aria-hidden="true">📁</span>
 <span class="dropzone__label">Drop a file here, or click to browse</span>
 <span class="dropzone__hint">Hashed on your device, the file is never uploaded</span>
 </div>
 <div class="field mt-4">
 <label class="field__label" for="expected"><span>Published checksum</span><span class="field__hint" id="expected-type"></span></label>
 <input class="input font-mono" id="expected" type="text" placeholder="Paste the checksum from the download page" autocomplete="off" spellcheck="false">
 </div>
 <div class="field">
 <span class="field__label"><span>Computed hashes</span></span>
 <div class="table-scroll"><div id="computed"></div></div>
 </div>
 </div>"""),
 status_line("status", "Paste two hashes to compare them."),
 HR,
 html_block(""" <div class="display" id="verdict-box" style="padding:var(--space-8)">
 <span class="display__value" id="verdict" style="font-size:clamp(1.5rem,1rem+3vw,2.5rem)">, </span>
 <span class="display__label" id="verdict-detail">Awaiting input</span>
 </div>"""),
 buttons(("clear", "Clear", "ghost"), ("share", "Share tool", "ghost")),
 label="Hash comparison",
 ),
 info_block=info(
 features=[
 "Compare two hashes with a clear pass or fail verdict",
 "Hash a local file and check it against a published checksum",
 "Automatic algorithm detection from digest length",
 "Constant-time comparison",
 "Ignores case and whitespace differences",
 ],
 howto=[
 "To compare two hashes, paste one into each box.",
 "To verify a download, switch mode and choose the file.",
 "Paste the checksum published on the download page.",
 "Read the verdict, it either matches or it does not.",
 ],
 background_title="What a matching checksum actually proves",
 background_paragraphs=[
 "A matching hash proves the file you have is byte-for-byte identical to the file the hash was computed from. That reliably catches truncated downloads, disk corruption and transmission errors, which is the everyday use.",
 "It proves considerably less about tampering than people assume. If an attacker can modify the file on the server, they can usually modify the checksum published alongside it too, and you would verify the bad file against the bad hash and see a match. Checksums only defend against a compromised mirror when the hash comes from a different, trusted channel: the project's signing key, a separate domain, or a signature you verify with GPG. This is why serious projects publish signed hash files rather than a bare hex string.",
 "Algorithm choice matters here. MD5 and SHA-1 are both broken for collision resistance, it is computationally feasible to construct two different files with the same digest, and this has been demonstrated with real PDFs and certificates. They remain adequate for detecting accidental corruption but must not be relied on where an adversary is involved. Prefer SHA-256 or SHA-512 for anything security-relevant.",
 ],
 ),
 script=r""" const ALGORITHMS = ['SHA-1', 'SHA-256', 'SHA-384', 'SHA-512'];

 // Digest length in hex characters → likely algorithm
 const BY_LENGTH = {
 32: 'MD5 (broken, do not rely on it)',
 40: 'SHA-1 (broken for collisions)',
 56: 'SHA-224',
 64: 'SHA-256',
 96: 'SHA-384',
 128: 'SHA-512'
 };

 let computed = {};

 const normalise = (s) => String(s).replace(/\s+/g, '').toLowerCase();

 /** Constant-time string comparison, no early exit on first mismatch. */
 function constantTimeEqual(a, b) {
 if (a.length !== b.length) return false;
 let diff = 0;
 for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
 return diff === 0;
 }

 function identify(hash) {
 const clean = normalise(hash);
 if (!clean) return '';
 if (!/^[0-9a-f]+$/.test(clean)) return 'not hexadecimal';
 return BY_LENGTH[clean.length] || `${clean.length} hex chars, unrecognised`;
 }

 function setVerdict(state, headline, detail) {
 const colours = {
 match: 'var(--success)', mismatch: 'var(--danger)',
 partial: 'var(--warning)', idle: 'var(--text-muted)'
 };
 T.$('verdict').textContent = headline;
 T.$('verdict').style.color = colours[state];
 T.$('verdict-detail').textContent = detail;
 }

 function compare() {
 const a = normalise(T.$('hash-a').value);
 const b = normalise(T.$('hash-b').value);

 T.$('a-type').textContent = identify(T.$('hash-a').value);
 T.$('b-type').textContent = identify(T.$('hash-b').value);

 if (!a || !b) {
 setVerdict('idle', ', ', 'Paste a hash into both boxes.');
 T.status('status', 'Paste two hashes to compare them.', 'muted');
 return;
 }

 if (a.length !== b.length) {
 setVerdict('mismatch', '✗ Different', `Lengths differ, ${a.length} vs ${b.length} characters, so these are different algorithms.`);
 T.status('status', 'These hashes are different lengths, so they cannot match.', 'error');
 return;
 }

 if (constantTimeEqual(a, b)) {
 setVerdict('match', '✓ Match', `Both are identical ${identify(a)} digests.`);
 T.status('status', 'The two hashes are identical.', 'ok');
 } else {
 // Show how many characters differ, which helps spot a typo
 let differing = 0;
 for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) differing++;
 setVerdict('mismatch', '✗ No match',
 `${differing} of ${a.length} characters differ.` +
 (differing <= 2 ? ' That few suggests a typo rather than a different file.' : ''));
 T.status('status', 'The hashes do not match.', 'error');
 }

 if (window.Analytics) Analytics.trackToolUse('hash-comparison');
 }

 async function hashFile(file) {
 T.status('status', `Reading ${file.name}…`, 'muted');
 setVerdict('idle', '…', 'Hashing the file');

 try {
 const buffer = await file.arrayBuffer();
 computed = {};

 for (const algo of ALGORITHMS) {
 const digest = await crypto.subtle.digest(algo, buffer);
 computed[algo] = [...new Uint8Array(digest)]
 .map((b) => b.toString(16).padStart(2, '0')).join('');
 }

 renderComputed(file);
 checkExpected();

 T.status('status',
 `Hashed “${file.name}” (${T.bytes(file.size)}). The file never left your device.`, 'ok');
 } catch (err) {
 T.status('status', 'Could not read that file: ' + err.message, 'error');
 }
 }

 function renderComputed(file) {
 const mount = T.$('computed');
 mount.innerHTML = '';

 const entries = Object.entries(computed);
 if (!entries.length) return;

 const table = T.table(['Algorithm', 'Digest'], entries);
 [...table.querySelectorAll('tbody tr')].forEach((tr, i) => {
 tr.style.cursor = 'pointer';
 tr.title = 'Click to copy';
 tr.addEventListener('click', () => copyToClipboard(entries[i][1], entries[i][0] + ' copied'));
 });

 mount.append(table);

 const zone = T.$('dropzone');
 zone.classList.add('has-file');
 zone.querySelector('.dropzone__label').textContent = file.name;
 zone.querySelector('.dropzone__hint').textContent =
 `${T.bytes(file.size)}, click to choose a different file`;
 }

 function checkExpected() {
 const expected = normalise(T.$('expected').value);
 T.$('expected-type').textContent = identify(T.$('expected').value);

 if (!Object.keys(computed).length) {
 setVerdict('idle', ', ', 'Choose a file first.');
 return;
 }

 if (!expected) {
 setVerdict('idle', ', ', 'Paste the published checksum to verify.');
 return;
 }

 const match = Object.entries(computed)
 .find(([, digest]) => constantTimeEqual(digest, expected));

 if (match) {
 setVerdict('match', '✓ Verified',
 `The file matches the published ${match[0]} checksum.`);
 T.status('status', `Verified against ${match[0]}.`, 'ok');
 } else {
 setVerdict('mismatch', '✗ Does not match',
 'The file does not match that checksum. It may be corrupt, incomplete, or a different version.');
 T.status('status', 'No algorithm produced a digest matching that checksum.', 'error');
 }
 }

 function syncMode() {
 const comparing = T.$('mode').value === 'compare';
 T.$('compare-panel').hidden = !comparing;
 T.$('file-panel').hidden = comparing;

 if (comparing) compare();
 else checkExpected();
 }

 T.$('mode').addEventListener('change', syncMode);
 T.on(['hash-a', 'hash-b'], debounce(compare, 200));
 T.$('expected').addEventListener('input', debounce(checkExpected, 200));

 T.dropzone('dropzone', hashFile, '*/*');

 T.$('clear').addEventListener('click', () => {
 ['hash-a', 'hash-b', 'expected'].forEach((id) => { T.$(id).value = ''; });
 computed = {};
 T.$('computed').innerHTML = '';
 const zone = T.$('dropzone');
 zone.classList.remove('has-file');
 zone.querySelector('.dropzone__label').textContent = 'Drop a file here, or click to browse';
 zone.querySelector('.dropzone__hint').textContent = 'Hashed on your device, the file is never uploaded';
 syncMode();
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Hash Comparison | 123MiniApps' }));

 syncMode();""",
))

# ---------------------------------------------------------------
# 68. Random Key Generator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="random-key-generator", name="Random Key Generator", icon="🗝️", cat="security",
 title="Random Key Generator: API Keys, Secrets and Tokens",
 description="Generate API keys, secrets, tokens and salts at any length in hex, Base64, Base64URL or Base58, using cryptographically secure randomness.",
 tagline="Generate API keys and secrets with cryptographic randomness, in five encodings.",
 workspace=ws(
 row(
 slider("bits", "Key strength", 64, 512, 256, 32, unit="bits"),
 select("encoding", "Encoding", [
 ("hex", "Hexadecimal"),
 ("base64", "Base64"),
 ("base64url", "Base64URL, safe in URLs"),
 ("base58", "Base58, no look-alike characters"),
 ("alnum", "Alphanumeric"),
 ], selected="hex"),
 number_input("count", "How many", "5", "5", step="1", min=1, max=100),
 ),
 row(
 text_input("prefix", "Prefix (optional)", "e.g. sk_live_"),
 select("preset", "Or use a preset", [
 ("", "Custom…"),
 ("api", "API key, 256-bit, prefixed"),
 ("session", "Session token, 256-bit Base64URL"),
 ("salt", "Password salt, 128-bit hex"),
 ("jwt", "JWT signing secret, 512-bit"),
 ("webhook", "Webhook secret, 256-bit hex"),
 ("nonce", "Nonce, 96-bit hex"),
 ], selected=""),
 ),
 status_line("status", "Press Generate."),
 HR,
 output("output", "Generated keys", "output-stats", "Your keys will appear here."),
 buttons(("generate", "Generate", "primary"), ("copy", "Copy result"), ("download", "Download"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result"><span class="result__value" id="r-bits" style="font-size:var(--text-2xl)">, </span><span class="result__label">Entropy</span></div>
 <div class="result"><span class="result__value" id="r-length" style="font-size:var(--text-2xl)">, </span><span class="result__label">Characters</span></div>
 <div class="result"><span class="result__value" id="r-space" style="font-size:var(--text-lg)">, </span><span class="result__label">Search space</span></div>
 </div>"""),
 label="Random key generator",
 ),
 info_block=info(
 features=[
 "64 to 512 bits of entropy",
 "Five encodings including Base58 and Base64URL",
 "Optional prefix for environment tagging",
 "Six presets for common uses",
 "crypto.getRandomValues, never Math.random",
 ],
 howto=[
 "Choose a strength, 256 bits suits almost everything.",
 "Pick an encoding appropriate to where the key will live.",
 "Add a prefix if you tag keys by environment.",
 "Press Generate and store the result somewhere safe.",
 ],
 background_title="Choosing a length and an encoding",
 background_paragraphs=[
 "For a secret that is never transmitted in the clear and is compared server-side, 128 bits is already beyond brute force and 256 bits is the comfortable standard. Going beyond that adds length without adding meaningful security, a 512-bit key is appropriate for an HMAC signing secret, where the recommendation is to match the hash output size, but is overkill for a session token.",
 "Encoding affects where a key can safely live. Standard Base64 uses <code>+</code> and <code>/</code>, both of which have meaning in URLs and must be escaped; Base64URL substitutes <code>-</code> and <code>_</code> so the key can be dropped into a path or query string unmodified. Base58, which Bitcoin popularised, removes the characters people misread, <code>0</code>, <code>O</code>, <code>I</code> and <code>l</code>: which matters if a key will ever be read aloud, written down or retyped.",
 "The operational advice matters more than the generation. Prefixing keys by environment (<code>sk_live_</code>, <code>sk_test_</code>) prevents the expensive mistake of running test code against production. Store only a hash of the key server-side, so a database leak does not expose working credentials, this is why well-designed services show a key exactly once. And keys generated here exist only in this tab: they are not logged, stored or transmitted, so copy them before you navigate away.",
 ],
 ),
 script=r""" const BASE58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
 const ALNUM = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

 const PRESETS = {
 api: { bits: 256, encoding: 'base64url', prefix: 'sk_live_' },
 session: { bits: 256, encoding: 'base64url', prefix: '' },
 salt: { bits: 128, encoding: 'hex', prefix: '' },
 jwt: { bits: 512, encoding: 'base64', prefix: '' },
 webhook: { bits: 256, encoding: 'hex', prefix: 'whsec_' },
 nonce: { bits: 96, encoding: 'hex', prefix: '' }
 };

 let keys = [];

 function encodeBytes(bytes, encoding) {
 if (encoding === 'hex') {
 return [...bytes].map((b) => b.toString(16).padStart(2, '0')).join('');
 }

 if (encoding === 'base64' || encoding === 'base64url') {
 let binary = '';
 for (const b of bytes) binary += String.fromCharCode(b);
 const b64 = btoa(binary);
 return encoding === 'base64url'
 ? b64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '')
 : b64;
 }

 const alphabet = encoding === 'base58' ? BASE58 : ALNUM;

 // Rejection sampling keeps the distribution uniform; a plain
 // modulo would bias toward the start of the alphabet
 const targetLength = Math.ceil((bytes.length * 8) / Math.log2(alphabet.length));
 let out = '';
 for (let i = 0; i < targetLength; i++) {
 out += alphabet[T.randomBelow(alphabet.length)];
 }
 return out;
 }

 function generate() {
 const bits = Number(T.$('bits').value);
 const encoding = T.$('encoding').value;
 const count = T.clamp(Math.floor(T.num(T.$('count').value) || 1), 1, 100);
 const prefix = T.$('prefix').value;

 T.$('bits-value').textContent = bits;

 const byteLength = Math.ceil(bits / 8);

 keys = Array.from({ length: count }, () => {
 const bytes = new Uint8Array(byteLength);
 crypto.getRandomValues(bytes);
 return prefix + encodeBytes(bytes, encoding);
 });

 T.setOutput('output', keys.join('\n'));
 T.$('output-stats').textContent = `${count} key${count === 1 ? '' : 's'}`;

 const sample = keys[0].slice(prefix.length);
 T.$('r-bits').textContent = bits;
 T.$('r-length').textContent = keys[0].length;

 // Search space, expressed in a way people can picture
 const space = Math.pow(2, bits);
 T.$('r-space').textContent = space > 1e21
 ? '2^' + bits
 : space.toExponential(1);

 const unique = new Set(keys).size;
 T.status('status',
 unique === count
 ? `Generated ${count} key(s) with ${bits} bits of entropy each. Nothing is stored, copy them now.`
 : 'Duplicate detected, which should be impossible. Please report this.',
 unique === count ? 'ok' : 'error');

 void sample;
 if (window.Analytics) Analytics.trackToolUse('random-key-generator');
 }

 T.$('preset').addEventListener('change', () => {
 const preset = PRESETS[T.$('preset').value];
 if (!preset) return;
 T.$('bits').value = String(preset.bits);
 T.$('encoding').value = preset.encoding;
 T.$('prefix').value = preset.prefix;
 generate();
 });

 T.$('generate').addEventListener('click', generate);
 T.$('bits').addEventListener('input', generate);
 T.on(['encoding'], generate, 'change');
 T.on(['count', 'prefix'], debounce(generate, 300));

 T.wireActions({
 slug: 'random-key-generator',
 getResult: () => keys.join('\n'),
 filename: 'keys.txt'
 });

 generate();""",
))

# ---------------------------------------------------------------
# 69. Privacy Checker
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="privacy-checker", name="Privacy Checker", icon="👁️", cat="security",
 title="Browser Privacy Checker: See What Your Browser Reveals",
 description="See what your browser exposes to every site you visit: fingerprinting surface, storage, tracking preferences and hardware hints, with hardening advice.",
 tagline="See what your browser reveals to every site, and what to do about it.",
 workspace=ws(
 html_block(""" <p class="field__hint">
 Everything below is read from your own browser and displayed here. None of it is transmitted,
 logged or stored, this page simply shows you what any site could read about you without
 asking permission.
 </p>"""),
 html_block(""" <div class="result-grid">
 <div class="result result--primary"><span class="result__value" id="r-score" style="font-size:var(--text-3xl)">, </span><span class="result__label">Fingerprint surface</span></div>
 <div class="result"><span class="result__value" id="r-dnt" style="font-size:var(--text-xl)">, </span><span class="result__label">Do Not Track</span></div>
 <div class="result"><span class="result__value" id="r-cookies" style="font-size:var(--text-xl)">, </span><span class="result__label">Cookies</span></div>
 </div>"""),
 status_line("status", "Reading your browser configuration…"),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>What your browser reveals</span><span class="field__hint">Readable by any site, no permission needed</span></span>
 <div class="table-scroll"><div id="report"></div></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Storage in use on this site</span></span>
 <div class="table-scroll"><div id="storage"></div></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Suggestions</span></span>
 <div id="advice"></div>
 </div>"""),
 buttons(("refresh", "Re-run the check", "primary"), ("copy", "Copy report"), ("clear-storage", "Clear this site's storage"), ("share", "Share tool", "ghost")),
 label="Privacy checker",
 ),
 info_block=info(
 features=[
 "Fingerprinting surface summary",
 "Full list of attributes readable without permission",
 "Local storage inspection for this site",
 "Do Not Track and Global Privacy Control status",
 "Practical hardening suggestions",
 ],
 howto=[
 "The check runs automatically when the page loads.",
 "Read the table to see what any site can learn about you.",
 "Check the suggestions for ways to reduce the surface.",
 "Use Clear storage to wipe what this site has stored.",
 ],
 background_title="How browser fingerprinting works",
 background_paragraphs=[
 "Fingerprinting identifies you without cookies by combining attributes that are individually unremarkable but collectively rare. Your screen resolution, timezone, language, installed fonts, GPU model and the precise way your device renders a canvas element each narrow the field. Combine twenty such values and the result is frequently unique among hundreds of millions of browsers, the Electronic Frontier Foundation's Panopticlick research demonstrated this over a decade ago and it has only become more effective since.",
 "The counter-intuitive part is that hardening can make things worse. A browser with an unusual user agent, a rare screen size and privacy extensions installed is <em>more</em> identifiable than a default one, because those choices are themselves distinguishing. This is why the Tor Browser makes every user look identical rather than making each user look random, and why it discourages resizing the window or installing extensions.",
 "Do Not Track is worth understanding for what it is not. It sends a header politely requesting that you not be tracked, and it is entirely voluntary, almost no advertiser honours it, and enabling it adds one more bit to your fingerprint. Global Privacy Control is a newer signal with actual legal weight in California and some other jurisdictions, where it counts as a valid opt-out request under CCPA. If you want meaningful protection, the effective measures are blocking third-party cookies, using a content blocker like uBlock Origin, and preferring a browser that fights fingerprinting by default.",
 ],
 ),
 script=r""" let report = [];

 /** Attributes any site can read with no permission prompt. */
 function gather() {
 const nav = window.navigator;
 const screenInfo = window.screen || {};
 const rows = [];

 const add = (category, item, value, identifying) => {
 rows.push({ category, item, value: String(value), identifying });
 };

 // Screen and window
 add('Display', 'Screen resolution', `${screenInfo.width || '?'} × ${screenInfo.height || '?'}`, true);
 add('Display', 'Available screen area', `${screenInfo.availWidth || '?'} × ${screenInfo.availHeight || '?'}`, true);
 add('Display', 'Colour depth', (screenInfo.colorDepth || '?') + ' bits', false);
 add('Display', 'Device pixel ratio', window.devicePixelRatio || '?', true);
 add('Display', 'Window size', `${window.innerWidth} × ${window.innerHeight}`, true);

 // Locale and time
 const resolved = Intl.DateTimeFormat().resolvedOptions();
 add('Locale', 'Timezone', resolved.timeZone || 'unknown', true);
 add('Locale', 'UTC offset', new Date().getTimezoneOffset() / -60 + ' hours', true);
 add('Locale', 'Language', nav.language || 'unknown', true);
 add('Locale', 'All languages', (nav.languages || []).join(', ') || 'unknown', true);
 add('Locale', 'Calendar', resolved.calendar || 'unknown', false);
 add('Locale', 'Numbering system', resolved.numberingSystem || 'unknown', false);

 // Hardware hints
 add('Hardware', 'CPU cores reported', nav.hardwareConcurrency || 'not exposed', true);
 add('Hardware', 'Device memory', nav.deviceMemory ? nav.deviceMemory + ' GB' : 'not exposed', true);
 add('Hardware', 'Max touch points', nav.maxTouchPoints ?? 'unknown', true);
 add('Hardware', 'Platform', nav.platform || 'not exposed', true);

 // Browser identity
 add('Browser', 'User agent', nav.userAgent || 'unknown', true);
 add('Browser', 'Vendor', nav.vendor || 'unknown', false);
 add('Browser', 'Cookies enabled', nav.cookieEnabled ? 'yes' : 'no', false);
 add('Browser', 'Online', nav.onLine ? 'yes' : 'no', false);
 add('Browser', 'PDF viewer', nav.pdfViewerEnabled ? 'enabled' : 'not reported', false);
 add('Browser', 'Plugins reported', (nav.plugins ? nav.plugins.length : 0) + ' entries', true);

 // Privacy signals
 const dnt = nav.doNotTrack || window.doNotTrack || nav.msDoNotTrack;
 add('Privacy signals', 'Do Not Track', dnt === '1' || dnt === 'yes' ? 'enabled' : 'not enabled', false);
 add('Privacy signals', 'Global Privacy Control', nav.globalPrivacyControl ? 'enabled' : 'not enabled', false);

 // Rendering preferences, which are also fingerprintable
 const mq = (query) => window.matchMedia && window.matchMedia(query).matches;
 add('Preferences', 'Prefers dark mode', mq('(prefers-color-scheme: dark)') ? 'yes' : 'no', false);
 add('Preferences', 'Prefers reduced motion', mq('(prefers-reduced-motion: reduce)') ? 'yes' : 'no', true);
 add('Preferences', 'Prefers contrast', mq('(prefers-contrast: more)') ? 'more' : 'default', true);

 // Capability surface
 add('Capabilities', 'Web Crypto', window.crypto && window.crypto.subtle ? 'available' : 'unavailable', false);
 add('Capabilities', 'Service workers', 'serviceWorker' in nav ? 'supported' : 'unsupported', false);
 add('Capabilities', 'WebGL', detectWebGL(), true);
 add('Capabilities', 'Canvas fingerprint', canvasFingerprint(), true);

 return rows;
 }

 /** The GPU string is one of the strongest single identifiers. */
 function detectWebGL() {
 try {
 const canvas = document.createElement('canvas');
 const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
 if (!gl) return 'unavailable';

 const ext = gl.getExtension('WEBGL_debug_renderer_info');
 if (!ext) return 'available (renderer masked)';

 return String(gl.getParameter(ext.UNMASKED_RENDERER_WEBGL)).slice(0, 60);
 } catch {
 return 'unavailable';
 }
 }

 /**
 * Render text to a canvas and hash the pixels. Tiny differences in
 * font rasterisation and anti-aliasing between devices make this
 * highly identifying, which is the point of showing it.
 */
 function canvasFingerprint() {
 try {
 const canvas = document.createElement('canvas');
 canvas.width = 240;
 canvas.height = 60;
 const ctx = canvas.getContext('2d');
 if (!ctx) return 'unavailable';

 ctx.textBaseline = 'top';
 ctx.font = '16px Arial';
 ctx.fillStyle = '#f60';
 ctx.fillRect(10, 10, 100, 30);
 ctx.fillStyle = '#069';
 ctx.fillText('123MiniApps 🔒', 12, 14);

 const data = canvas.toDataURL();
 let hash = 0;
 for (let i = 0; i < data.length; i++) {
 hash = ((hash << 5) - hash + data.charCodeAt(i)) | 0;
 }
 return (hash >>> 0).toString(16).padStart(8, '0');
 } catch {
 return 'blocked';
 }
 }

 function inspectStorage() {
 const mount = T.$('storage');
 mount.innerHTML = '';
 const rows = [];

 try {
 for (let i = 0; i < localStorage.length; i++) {
 const key = localStorage.key(i);
 const value = localStorage.getItem(key) || '';
 rows.push(['localStorage', key, T.bytes(new Blob([value]).size)]);
 }
 } catch {
 rows.push(['localStorage', 'unavailable', ', ']);
 }

 try {
 for (let i = 0; i < sessionStorage.length; i++) {
 rows.push(['sessionStorage', sessionStorage.key(i), ', ']);
 }
 } catch { /* unavailable */ }

 const cookies = document.cookie ? document.cookie.split(';').length : 0;
 rows.push(['Cookies', `${cookies} cookie(s) on this domain`, ', ']);

 if (rows.length) mount.append(T.table(['Type', 'Key', 'Size'], rows));
 }

 function renderReport(rows) {
 const mount = T.$('report');
 mount.innerHTML = '';

 const table = T.table(
 ['Category', 'Attribute', 'Value'],
 rows.map((r) => [r.category, r.item, r.value.length > 70 ? r.value.slice(0, 70) + '…' : r.value])
 );

 // Tint the rows that meaningfully narrow down who you are
 [...table.querySelectorAll('tbody tr')].forEach((tr, i) => {
 if (rows[i].identifying) {
 tr.style.background = 'color-mix(in srgb, var(--warning) 10%, transparent)';
 }
 });

 mount.append(table);
 }

 function renderAdvice(rows) {
 const mount = T.$('advice');
 mount.innerHTML = '';

 const tips = [];
 const find = (item) => (rows.find((r) => r.item === item) || {}).value || '';

 if (find('Do Not Track') !== 'enabled' && find('Global Privacy Control') !== 'enabled') {
 tips.push(['Enable Global Privacy Control', 'It carries legal weight under CCPA and similar laws, unlike Do Not Track which is voluntary and largely ignored.']);
 }

 if (find('Canvas fingerprint') !== 'blocked') {
 tips.push(['Canvas fingerprinting is readable', 'Your device produces a distinctive canvas hash. Firefox with resistFingerprinting, the Tor Browser, or Brave\'s shields all randomise or block this.']);
 }

 if (find('WebGL').includes('available') && !find('WebGL').includes('masked')) {
 tips.push(['Your GPU model is exposed', 'The unmasked WebGL renderer string is one of the most identifying values available. Browsers with fingerprint protection mask it.']);
 }

 if (find('CPU cores reported') !== 'not exposed') {
 tips.push(['Hardware details are exposed', 'Core count and device memory narrow you down considerably when combined with screen size and timezone.']);
 }

 tips.push(['Use a content blocker', 'uBlock Origin blocks the majority of tracking scripts before they run, which prevents fingerprinting scripts from executing at all.']);
 tips.push(['Block third-party cookies', 'Most browsers now offer this in settings. It breaks cross-site tracking without breaking most sites.']);
 tips.push(['Do not over-customise', 'Counter-intuitively, an unusual configuration makes you easier to identify. Blending in with a large group beats being random.']);

 const list = el('div', { className: 'stack' });
 tips.forEach(([heading, detail]) => {
 list.append(el('div', { className: 'info-panel' }, [
 el('strong', { text: heading, className: 'text-sm' }),
 el('p', { className: 'text-sm text-muted mt-2', text: detail })
 ]));
 });

 mount.append(list);
 }

 function run() {
 report = gather();
 renderReport(report);
 inspectStorage();
 renderAdvice(report);

 const identifying = report.filter((r) => r.identifying).length;
 T.$('r-score').textContent = identifying + ' of ' + report.length;

 const dnt = report.find((r) => r.item === 'Do Not Track').value;
 const gpc = report.find((r) => r.item === 'Global Privacy Control').value;
 T.$('r-dnt').textContent = dnt === 'enabled' ? 'On' : gpc === 'enabled' ? 'GPC on' : 'Off';
 T.$('r-dnt').style.color = (dnt === 'enabled' || gpc === 'enabled') ? 'var(--success)' : 'var(--warning)';

 T.$('r-cookies').textContent = navigator.cookieEnabled ? 'Enabled' : 'Blocked';

 T.status('status',
 `${identifying} of ${report.length} attributes meaningfully narrow down who you are. ` +
 'None of this was sent anywhere.', identifying > 12 ? 'warn' : 'ok');

 if (window.Analytics) Analytics.trackToolUse('privacy-checker');
 }

 T.$('refresh').addEventListener('click', run);

 T.$('copy').addEventListener('click', () => {
 const text = report.map((r) => `${r.category}, ${r.item}: ${r.value}`).join('\n');
 copyToClipboard(text, 'Report copied');
 });

 T.$('clear-storage').addEventListener('click', () => {
 try {
 localStorage.clear();
 sessionStorage.clear();
 toast({ type: 'success', title: 'Storage cleared', message: 'Your theme and favorites have been reset.' });
 } catch {
 toast({ type: 'error', title: 'Could not clear storage' });
 }
 inspectStorage();
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Privacy Checker | 123MiniApps' }));

 run();""",
))
