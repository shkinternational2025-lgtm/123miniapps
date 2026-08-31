/* ============================================
   123MiniApps.online v2.0
   File: test/phase-security.js
   Purpose: Behavioural tests for the 5 security tools.

   Crypto is verified by round-tripping and by
   asserting that tampering is detected — not by
   trusting the implementation's own reports.
   ============================================ */

const { boot, Suite, set, click, text, val, wait } = require('./harness');

module.exports = async function run() {
  const s = new Suite('Security tools');

  /* ---------- Password Strength ---------- */
  {
    const { window: w, errors } = await boot('tools/password-strength-checker.html');

    const num = (x) => Number(String(x).replace(/[^0-9.-]/g, ''));

    // A long random password should score highly
    set(w, 'password', 'kR7#mQ9$vX2@pL5!nD8&wZ4');
    await wait(300);
    s.check('pwstrength: strong password scores high', num(text(w, 'r-entropy')) > 100,
      text(w, 'r-entropy'));
    s.eq('pwstrength: verdict strong', text(w, 'r-verdict'), 'Strong');

    // Short password
    set(w, 'password', 'abc');
    await wait(300);
    s.check('pwstrength: short password scores low', num(text(w, 'r-entropy')) < 25);
    s.match('pwstrength: verdict very weak', text(w, 'r-verdict'), /very weak/i);
    s.includes('pwstrength: flags short length',
      w.document.getElementById('warnings').textContent, 'Shorter than 8');

    // The important case: high raw entropy but a known-bad password
    set(w, 'password', 'Password123!');
    await wait(300);
    const warnings = w.document.getElementById('warnings').textContent;
    s.includes('pwstrength: detects common password', warnings, 'password');
    s.check('pwstrength: penalised below raw entropy', num(text(w, 'r-entropy')) < 79,
      text(w, 'r-entropy'));

    // Leetspeak substitutions must not evade detection
    set(w, 'password', 'P@ssw0rd');
    await wait(300);
    s.includes('pwstrength: sees through leetspeak',
      w.document.getElementById('warnings').textContent, 'substitutions do not help');

    // Keyboard runs
    set(w, 'password', 'qwertyuiop');
    await wait(300);
    s.includes('pwstrength: detects keyboard run',
      w.document.getElementById('warnings').textContent, 'keyboard run');

    // Repetition
    set(w, 'password', 'aaaaaaaaaaaa');
    await wait(300);
    s.includes('pwstrength: detects repetition',
      w.document.getElementById('warnings').textContent, 'repeated');

    // Repeating unit
    set(w, 'password', 'abcabcabcabc');
    await wait(300);
    s.includes('pwstrength: detects repeated unit',
      w.document.getElementById('warnings').textContent, 'repeated unit');

    s.check('pwstrength: crack table renders',
      w.document.querySelector('#crack table') !== null);

    // Suggestion must itself be strong
    click(w, 'generate');
    await wait(300);
    s.check('pwstrength: suggestion is strong', num(text(w, 'r-entropy')) > 60,
      val(w, 'password'));
    s.check('pwstrength: suggestion is a passphrase', val(w, 'password').includes('-'));

    click(w, 'clear');
    await wait(300);
    s.eq('pwstrength: clear empties the field', val(w, 'password'), '');
    s.noErrors(errors);
  }

  /* ---------- Encryption ---------- */
  {
    const { window: w, errors } = await boot('tools/encryption-tool.html');

    // Use the fastest setting so the test does not take forever
    set(w, 'iterations', '100000', 'change');
    set(w, 'mode', 'encrypt', 'change');
    set(w, 'input', 'Attack at dawn 🌅');
    set(w, 'passphrase', 'correct-horse-battery-staple');
    click(w, 'run');
    await wait(2500);

    const ciphertext = text(w, 'output');
    s.check('encrypt: produced output', ciphertext.length > 40, ciphertext.slice(0, 40));
    s.match('encrypt: output is Base64', ciphertext, /^[A-Za-z0-9+/]+=*$/);
    s.check('encrypt: plaintext not visible in output', !ciphertext.includes('Attack'));
    s.match('encrypt: reports algorithm', text(w, 'status'), /AES-256-GCM/);

    // Encrypting twice must give different output (random IV and salt)
    click(w, 'run');
    await wait(2500);
    s.check('encrypt: two runs differ (random IV/salt)', text(w, 'output') !== ciphertext);
    const second = text(w, 'output');

    // Round-trip
    set(w, 'mode', 'decrypt', 'change');
    set(w, 'input', second);
    set(w, 'passphrase', 'correct-horse-battery-staple');
    click(w, 'run');
    await wait(2500);
    s.eq('decrypt: round-trips exactly', text(w, 'output'), 'Attack at dawn 🌅');

    // Wrong passphrase must fail, not return garbage
    set(w, 'input', second);
    set(w, 'passphrase', 'wrong-passphrase-entirely');
    click(w, 'run');
    await wait(2500);
    s.match('decrypt: wrong passphrase rejected', text(w, 'status'), /passphrase is wrong|altered/i);

    // Tampered ciphertext must be detected by GCM authentication
    const tampered = second.slice(0, -8) + 'AAAAAAAA';
    set(w, 'input', tampered);
    set(w, 'passphrase', 'correct-horse-battery-staple');
    click(w, 'run');
    await wait(2500);
    s.match('decrypt: tampering detected', text(w, 'status'), /wrong, or the message has been altered/i);

    // Non-tool input rejected
    set(w, 'input', btoa('hello world this is not ours at all really'));
    click(w, 'run');
    await wait(1200);
    s.match('decrypt: foreign payload rejected', text(w, 'status'), /not produced by this tool|too short/i);

    // Missing passphrase
    set(w, 'mode', 'encrypt', 'change');
    set(w, 'input', 'test');
    set(w, 'passphrase', '');
    click(w, 'run');
    await wait(300);
    s.match('encrypt: missing passphrase rejected', text(w, 'status'), /enter a passphrase/i);
    s.noErrors(errors);
  }

  /* ---------- Hash Comparison ---------- */
  {
    const { window: w, errors } = await boot('tools/hash-comparison.html');

    const H = 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad';

    set(w, 'mode', 'compare', 'change');
    set(w, 'hash-a', H);
    set(w, 'hash-b', H);
    await wait(300);
    s.match('hashcmp: identical hashes match', text(w, 'verdict'), /match/i);
    s.includes('hashcmp: identifies SHA-256', text(w, 'verdict-detail'), 'SHA-256');

    // Case and whitespace must be ignored
    set(w, 'hash-b', '  ' + H.toUpperCase() + '  ');
    await wait(300);
    s.match('hashcmp: case and space insensitive', text(w, 'verdict'), /match/i);

    // One character different
    set(w, 'hash-b', H.slice(0, -1) + 'e');
    await wait(300);
    s.match('hashcmp: single-char difference caught', text(w, 'verdict'), /no match/i);
    s.includes('hashcmp: counts differing chars', text(w, 'verdict-detail'), '1 of 64');
    s.includes('hashcmp: suggests typo', text(w, 'verdict-detail'), 'typo');

    // Different lengths
    set(w, 'hash-b', 'a9993e364706816aba3e25717850c26c9cd0d89d');
    await wait(300);
    s.match('hashcmp: length mismatch reported', text(w, 'verdict-detail'), /Lengths differ/i);

    // Algorithm identification by length
    set(w, 'hash-a', 'a'.repeat(40));
    await wait(300);
    s.includes('hashcmp: identifies SHA-1 as broken', text(w, 'a-type'), 'SHA-1');

    set(w, 'hash-a', 'a'.repeat(32));
    await wait(300);
    s.includes('hashcmp: identifies MD5 as broken', text(w, 'a-type'), 'MD5');

    set(w, 'hash-a', 'nothex!!');
    await wait(300);
    s.includes('hashcmp: rejects non-hex', text(w, 'a-type'), 'not hexadecimal');

    set(w, 'mode', 'file', 'change');
    await wait(200);
    s.check('hashcmp: file panel shown', w.document.getElementById('file-panel').hidden === false);
    s.noErrors(errors);
  }

  /* ---------- Random Key ---------- */
  {
    const { window: w, errors } = await boot('tools/random-key-generator.html');

    set(w, 'bits', '256');
    set(w, 'encoding', 'hex', 'change');
    set(w, 'count', '20');
    set(w, 'prefix', '');
    await wait(400);

    const keys = text(w, 'output').split('\n');
    s.eq('randomkey: 20 keys', keys.length, 20);
    s.check('randomkey: all unique', new Set(keys).size === 20);
    s.check('randomkey: 256-bit hex is 64 chars', keys.every((k) => k.length === 64));
    s.check('randomkey: valid hex', keys.every((k) => /^[0-9a-f]{64}$/.test(k)));

    set(w, 'encoding', 'base64url', 'change');
    await wait(400);
    const urlSafe = text(w, 'output').split('\n');
    s.check('randomkey: base64url has no + / =',
      urlSafe.every((k) => !/[+/=]/.test(k)));

    set(w, 'encoding', 'base58', 'change');
    await wait(400);
    const b58 = text(w, 'output').split('\n');
    s.check('randomkey: base58 excludes 0OIl',
      b58.every((k) => !/[0OIl]/.test(k)), b58[0]);

    set(w, 'encoding', 'hex', 'change');
    set(w, 'prefix', 'sk_live_');
    await wait(400);
    s.check('randomkey: prefix applied',
      text(w, 'output').split('\n').every((k) => k.startsWith('sk_live_')));

    // Presets
    set(w, 'preset', 'salt', 'change');
    await wait(400);
    s.eq('randomkey: salt preset is 128 bits', val(w, 'bits'), '128');
    s.eq('randomkey: salt preset uses hex', val(w, 'encoding'), 'hex');
    s.check('randomkey: 128-bit hex is 32 chars',
      text(w, 'output').split('\n')[0].length === 32);

    set(w, 'preset', 'jwt', 'change');
    await wait(400);
    s.eq('randomkey: jwt preset is 512 bits', val(w, 'bits'), '512');
    s.eq('randomkey: entropy readout', text(w, 'r-bits'), '512');
    s.noErrors(errors);
  }

  /* ---------- Privacy Checker ---------- */
  {
    const { window: w, errors } = await boot('tools/privacy-checker.html');

    await wait(400);

    s.check('privacy: report table renders', w.document.querySelector('#report table') !== null);
    s.match('privacy: score shown', text(w, 'r-score'), /\d+ of \d+/);

    const reportText = w.document.getElementById('report').textContent;
    s.includes('privacy: reports timezone', reportText, 'Timezone');
    s.includes('privacy: reports user agent', reportText, 'User agent');
    s.includes('privacy: reports screen resolution', reportText, 'Screen resolution');
    s.includes('privacy: reports canvas fingerprint', reportText, 'Canvas fingerprint');
    s.includes('privacy: reports Do Not Track', reportText, 'Do Not Track');

    s.check('privacy: advice rendered',
      w.document.querySelectorAll('#advice .info-panel').length >= 3);
    s.check('privacy: storage table rendered',
      w.document.querySelector('#storage table') !== null);

    s.match('privacy: confirms nothing was sent', text(w, 'status'), /none of this was sent/i);

    click(w, 'refresh');
    await wait(300);
    s.match('privacy: re-run works', text(w, 'r-score'), /\d+ of \d+/);
    s.noErrors(errors);
  }

  return s;
};
