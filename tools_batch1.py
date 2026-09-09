#!/usr/bin/env python3
# ============================================
# 123MiniApps.online, Phase 1 Batch 1
# File: tools_batch1.py
# Purpose: 5 high-search premium utilities:
#   Binary Code Translator, Morse Code Translator,
#   Online Stopwatch, GPA Calculator, Sales Tax Calculator.
# ============================================

from toolkit import (
    tool, ws, info, row, text_input, number_input, select, switch,
    textarea, status_line, buttons, HR, html_block, readonly,
)

PAGES = []

# ---------------------------------------------------------------
# Binary Code Translator
# ---------------------------------------------------------------
PAGES.append(tool(
    slug="binary-code-translator", name="Binary Code Translator", icon="🔢", cat="developer",
    title="Binary Code Translator",
    description="Translate text to binary and binary back to text, with full UTF-8 support plus decimal and hexadecimal output. Everything runs in your browser.",
    tagline="Convert text to binary and back, with UTF-8, decimal and hex, all in your browser.",
    workspace=ws(
        textarea("text", "Text", "Type or paste text here", rows=120),
        row(
            select("delim", "Binary spacing", [("space", "Space between bytes"), ("none", "No spaces")], "space"),
            select("enc", "Encoding", [("utf8", "UTF-8 (recommended)"), ("ascii", "ASCII / Latin-1")], "utf8"),
        ),
        textarea("binary", "Binary", "01001000 01101001", rows=120),
        status_line("status", "Type in either box and the other updates instantly."),
        row(
            readonly("decimal", "Decimal (byte values)"),
            readonly("hex", "Hexadecimal"),
        ),
        buttons(("copybin", "Copy binary", "primary"), ("copytext", "Copy text", "ghost"),
                ("clear", "Clear", "ghost"), ("share", "Share tool", "ghost")),
        label="Binary code translator",
    ),
    info_block=info(
        features=[
            "Two-way: text to binary and binary to text",
            "Full UTF-8 support, not just plain ASCII",
            "Also shows decimal and hexadecimal byte values",
            "Choose spaced bytes or a continuous bit stream",
            "One-click copy, everything stays in your browser",
        ],
        howto=[
            "Type or paste text into the top box to see its binary.",
            "Or paste binary into the lower box to decode it to text.",
            "Pick UTF-8 for emoji and accented characters.",
            "Copy the binary or the decoded text with one click.",
        ],
        background_title="How text becomes binary",
        background_paragraphs=[
            "Every character you type is stored as a number, and that number is stored as bits, the ones and zeros a computer actually works in. A binary translator makes that hidden layer visible: it looks up the numeric code for each character and writes it out as an 8-bit byte. The capital letter A is code 65, which is 01000001 in binary; a lowercase a is 97, or 01100001.",
            "Plain ASCII only covers the first 128 codes, enough for English letters, digits and common punctuation. Anything beyond that, an accented e, a currency symbol, an emoji, needs UTF-8, which represents those characters as two, three or four bytes. That is why this tool defaults to UTF-8: switch to ASCII only if you specifically need the classic 7-bit behaviour and are working with English text.",
            "Decoding is the same process in reverse. The tool groups the bits into bytes, reads each byte back to its number, and maps the number to a character. Because binary is just a notation, converting text to binary and back is lossless: what you put in is exactly what you get out.",
        ],
    ),
    faqs=[
        ("Is this binary translator free?", "Yes, with no limits, no account and no sign-up."),
        ("Does it support emoji and accented characters?", "Yes. With UTF-8 encoding selected, characters beyond plain ASCII, including emoji and accents, are encoded as multiple bytes and decode back correctly."),
        ("Why must binary be a multiple of 8 bits?", "Each character byte is 8 bits, so a valid binary string decodes in 8-bit groups. If the total number of 0s and 1s is not divisible by 8, a byte is incomplete and the tool asks you to check the input."),
        ("Is my text sent anywhere?", "No. The translation runs as JavaScript in your browser, so nothing you type is uploaded to a server."),
    ],
    script=r""" let updating = false;

    function textToBinary(text, enc, delim) {
      let bytes;
      if (enc === 'ascii') {
        bytes = [];
        for (const ch of text) bytes.push(ch.charCodeAt(0) & 0xFF);
      } else {
        bytes = Array.from(new TextEncoder().encode(text));
      }
      const sep = delim === 'none' ? '' : ' ';
      return { bin: bytes.map((b) => b.toString(2).padStart(8, '0')).join(sep), bytes };
    }

    function binaryToText(bin, enc) {
      const clean = bin.replace(/[^01]/g, '');
      if (clean.length === 0) return { text: '', bytes: [] };
      if (clean.length % 8 !== 0) return null;
      const bytes = [];
      for (let i = 0; i < clean.length; i += 8) bytes.push(parseInt(clean.slice(i, i + 8), 2));
      let text;
      if (enc === 'ascii') text = bytes.map((b) => String.fromCharCode(b)).join('');
      else text = new TextDecoder().decode(new Uint8Array(bytes));
      return { text, bytes };
    }

    function updateExtras(bytes) {
      T.$('decimal').value = bytes.join(' ');
      T.$('hex').value = bytes.map((b) => b.toString(16).padStart(2, '0').toUpperCase()).join(' ');
    }

    function fromText() {
      if (updating) return;
      updating = true;
      const { bin, bytes } = textToBinary(T.$('text').value, T.$('enc').value, T.$('delim').value);
      T.$('binary').value = bin;
      updateExtras(bytes);
      T.status('status', bytes.length + ' byte(s).', 'ok');
      updating = false;
    }

    function fromBinary() {
      if (updating) return;
      updating = true;
      const res = binaryToText(T.$('binary').value, T.$('enc').value);
      if (res === null) {
        T.status('status', 'Binary length must be a multiple of 8 bits.', 'error');
        updating = false;
        return;
      }
      T.$('text').value = res.text;
      updateExtras(res.bytes);
      T.status('status', res.bytes.length + ' byte(s).', 'ok');
      updating = false;
    }

    T.$('text').addEventListener('input', fromText);
    T.$('binary').addEventListener('input', fromBinary);
    T.$('delim').addEventListener('change', fromText);
    T.$('enc').addEventListener('change', () => { if (T.$('text').value) fromText(); else fromBinary(); });
    T.$('copybin').addEventListener('click', () => copyToClipboard(T.$('binary').value, 'Binary copied'));
    T.$('copytext').addEventListener('click', () => copyToClipboard(T.$('text').value, 'Text copied'));
    T.$('clear').addEventListener('click', () => {
      updating = true;
      ['text', 'binary', 'decimal', 'hex'].forEach((id) => { T.$(id).value = ''; });
      updating = false;
      T.status('status', 'Type in either box and the other updates instantly.', 'muted');
    });
    T.$('share').addEventListener('click', () => shareLink({ title: 'Binary Code Translator | 123MiniApps' }));

    T.$('text').value = 'Hi';
    fromText();
    if (window.Analytics) Analytics.trackToolUse('binary-code-translator');""",
))

# ---------------------------------------------------------------
# Morse Code Translator
# ---------------------------------------------------------------
PAGES.append(tool(
    slug="morse-code-translator", name="Morse Code Translator", icon="📡", cat="fun",
    title="Morse Code Translator",
    description="Translate text to Morse code and back, then play it as sound or a flashing light with adjustable speed. Runs entirely in your browser.",
    tagline="Translate text to Morse and back, with audio playback and a flashing light.",
    workspace=ws(
        textarea("text", "Text", "Type text to convert to Morse", rows=110),
        textarea("morse", "Morse code", ".... .. / - .... . .-. .", rows=110),
        status_line("status", "Type in either box. Use / between words in Morse."),
        row(
            html_block(""" <div class="field">
      <label class="field__label" for="wpm"><span>Playback speed</span><span class="field__hint"><strong id="wpm-value">15</strong> WPM</span></label>
      <input class="range" id="wpm" type="range" min="5" max="35" value="15" step="1">
    </div>"""),
            html_block(""" <div class="field">
      <label class="field__label"><span>Light</span></label>
      <div id="lamp" style="height:52px;border-radius:var(--radius-md);border:1px solid var(--glass-border);background:#111;transition:background .05s"></div>
    </div>"""),
        ),
        buttons(("play", "Play sound", "primary"), ("stop", "Stop", "ghost"),
                ("copymorse", "Copy Morse", "ghost"), ("clear", "Clear", "ghost"), ("share", "Share tool", "ghost")),
        label="Morse code translator",
    ),
    info_block=info(
        features=[
            "Two-way: text to Morse and Morse to text",
            "Audible playback with adjustable words-per-minute",
            "Flashing-light visual mode alongside the sound",
            "Handles letters, numbers and common punctuation",
            "Copy either side, everything runs in your browser",
        ],
        howto=[
            "Type text to see its Morse code instantly.",
            "Or paste Morse (dots, dashes, / between words) to decode it.",
            "Press Play sound to hear it and watch the light flash.",
            "Drag the speed slider to set the words-per-minute.",
        ],
        background_title="How Morse code works",
        background_paragraphs=[
            "Morse code represents each letter and number as a short sequence of dots and dashes, a dot being one unit of time and a dash three. The gap between symbols in a letter is one unit, the gap between letters is three, and the gap between words is seven, which is why spacing carries as much meaning as the marks themselves. The famous distress signal SOS is three dots, three dashes, three dots, chosen because it is unmistakable even to an untrained ear.",
            "Timing is measured in words per minute. The reference word PARIS is exactly 50 units long, so a speed of 15 WPM means 750 units per minute, and each unit is 80 milliseconds. This tool uses that standard, so raising the slider shortens every dot, dash and gap proportionally, exactly as a real operator would key faster.",
            "Because Morse is just a mapping, decoding is the reverse lookup: split the incoming code on spaces to find letters and on a slash to find word breaks, then translate each dot-dash pattern back to its character. The audio and the flashing light are two views of the same signal, one for the ear and one for the eye.",
        ],
    ),
    faqs=[
        ("Is this Morse code translator free?", "Yes, with no limits, no account and no sign-up."),
        ("Can it play Morse as sound?", "Yes. Press Play sound and the tool keys the code with correctly timed tones using your browser's audio, and flashes the on-screen light in time with it."),
        ("How do I write word breaks in Morse?", "Separate letters with a single space and words with a forward slash surrounded by spaces, for example .... .. / - .... . .-. . for HI THERE."),
        ("Is my text sent anywhere?", "No. The translation and audio run entirely in your browser, so nothing you type leaves your device."),
    ],
    script=r""" const MAP = {
      A: '.-', B: '-...', C: '-.-.', D: '-..', E: '.', F: '..-.', G: '--.', H: '....',
      I: '..', J: '.---', K: '-.-', L: '.-..', M: '--', N: '-.', O: '---', P: '.--.',
      Q: '--.-', R: '.-.', S: '...', T: '-', U: '..-', V: '...-', W: '.--', X: '-..-',
      Y: '-.--', Z: '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--',
      '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
      '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--',
      '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...',
      ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
      '"': '.-..-.', '$': '...-..-', '@': '.--.-.'
    };
    const REV = {};
    Object.keys(MAP).forEach((k) => { REV[MAP[k]] = k; });
    let updating = false;

    function textToMorse(text) {
      return text.toUpperCase().split('').map((ch) => {
        if (ch === ' ') return '/';
        return MAP[ch] !== undefined ? MAP[ch] : '';
      }).filter((x) => x !== '').join(' ').replace(/\s*\/\s*/g, ' / ');
    }

    function morseToText(code) {
      return code.trim().split(/\s+/).map((tok) => {
        if (tok === '/') return ' ';
        return REV[tok] !== undefined ? REV[tok] : '';
      }).join('').replace(/\s+/g, ' ').trim();
    }

    function fromText() { if (updating) return; updating = true; T.$('morse').value = textToMorse(T.$('text').value); T.status('status', 'Converted to Morse.', 'ok'); updating = false; }
    function fromMorse() { if (updating) return; updating = true; T.$('text').value = morseToText(T.$('morse').value); T.status('status', 'Decoded to text.', 'ok'); updating = false; }

    T.$('text').addEventListener('input', fromText);
    T.$('morse').addEventListener('input', fromMorse);
    T.$('wpm').addEventListener('input', () => { T.$('wpm-value').textContent = T.$('wpm').value; });

    let audioCtx = null;
    let playToken = 0;

    function playMorse() {
      const code = T.$('morse').value.trim();
      if (!code) { T.status('status', 'Nothing to play, type some text first.', 'muted'); return; }
      audioCtx = audioCtx || new (window.AudioContext || window.webkitAudioContext)();
      const wpm = Number(T.$('wpm').value);
      const unit = 1.2 / wpm;
      const token = ++playToken;
      let t = audioCtx.currentTime + 0.05;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'sine'; osc.frequency.value = 600;
      gain.gain.value = 0; osc.connect(gain); gain.connect(audioCtx.destination); osc.start();
      const flashes = [];
      const on = (start, dur) => { gain.gain.setValueAtTime(0.25, start); gain.gain.setValueAtTime(0, start + dur); flashes.push([start, dur]); };
      for (const ch of code) {
        if (ch === '.') { on(t, unit); t += unit + unit; }
        else if (ch === '-') { on(t, unit * 3); t += unit * 3 + unit; }
        else if (ch === ' ') { t += unit * 2; }
        else if (ch === '/') { t += unit * 4; }
      }
      osc.stop(t + unit);
      T.status('status', 'Playing...', 'ok');
      const startClock = performance.now();
      const base = audioCtx.currentTime;
      function tickLamp() {
        if (token !== playToken) return;
        const now = audioCtx.currentTime;
        const lit = flashes.some(([s, d]) => now >= s && now < s + d);
        T.$('lamp').style.background = lit ? '#facc15' : '#111';
        if (now < t + unit) requestAnimationFrame(tickLamp);
        else { T.$('lamp').style.background = '#111'; T.status('status', 'Done.', 'muted'); }
      }
      requestAnimationFrame(tickLamp);
    }

    T.$('play').addEventListener('click', playMorse);
    T.$('stop').addEventListener('click', () => { playToken++; if (audioCtx) { audioCtx.close(); audioCtx = null; } T.$('lamp').style.background = '#111'; T.status('status', 'Stopped.', 'muted'); });
    T.$('copymorse').addEventListener('click', () => copyToClipboard(T.$('morse').value, 'Morse copied'));
    T.$('clear').addEventListener('click', () => { updating = true; T.$('text').value = ''; T.$('morse').value = ''; updating = false; T.status('status', 'Type in either box. Use / between words in Morse.', 'muted'); });
    T.$('share').addEventListener('click', () => shareLink({ title: 'Morse Code Translator | 123MiniApps' }));

    T.$('text').value = 'SOS';
    fromText();
    if (window.Analytics) Analytics.trackToolUse('morse-code-translator');""",
))

# ---------------------------------------------------------------
# Online Stopwatch
# ---------------------------------------------------------------
PAGES.append(tool(
    slug="online-stopwatch", name="Online Stopwatch", icon="⏱️", cat="productivity",
    title="Online Stopwatch",
    description="A precise online stopwatch with lap and split times, keyboard shortcuts and CSV export of your laps. Runs entirely in your browser, no sign-up.",
    tagline="A precise stopwatch with laps, splits, keyboard control and CSV export.",
    workspace=ws(
        html_block(""" <div style="text-align:center;padding:var(--space-4) 0">
      <div id="display" style="font-family:var(--font-mono);font-size:clamp(2.5rem,10vw,4.5rem);font-weight:700;letter-spacing:1px">00:00.00</div>
    </div>"""),
        status_line("status", "Press Start, or hit the space bar. Press L to record a lap."),
        buttons(("startstop", "Start", "primary"), ("lap", "Lap", "ghost"),
                ("reset", "Reset", "ghost"), ("export", "Export laps (CSV)", "ghost"), ("share", "Share tool", "ghost")),
        HR,
        html_block(""" <div id="laps-wrap" hidden>
      <h3 class="text-lg mb-2">Laps</h3>
      <div style="overflow-x:auto"><table class="data-table" id="laps-table"><thead><tr><th>#</th><th>Lap time</th><th>Total time</th></tr></thead><tbody id="laps-body"></tbody></table></div>
    </div>"""),
        label="Online stopwatch",
    ),
    info_block=info(
        features=[
            "Precise to a hundredth of a second",
            "Lap and split times in a running table",
            "Keyboard control: space to start/stop, L for a lap",
            "Export all your laps to a CSV file",
            "Runs in your browser, keeps counting in the background",
        ],
        howto=[
            "Press Start, or tap the space bar, to begin timing.",
            "Press Lap (or the L key) to record a split without stopping.",
            "Press Start/Stop again to pause, and Reset to clear.",
            "Export laps to CSV to keep or analyse them.",
        ],
        background_title="Lap time versus split time",
        background_paragraphs=[
            "A stopwatch measures elapsed time, but the useful detail is often in the laps. This tool records two numbers each time you press Lap: the lap time, which is how long that individual segment took, and the total time, which is the running clock since you started. A runner doing repeats cares about the lap time; someone timing stages of a longer process cares about the total. Having both side by side means you never have to subtract in your head.",
            "Accuracy comes from measuring against the browser's high-resolution clock rather than counting ticks, so pausing and resuming does not drift. The display updates many times a second for a smooth readout, while the underlying time is tracked precisely, which is why the hundredths never stutter even if the tab is busy.",
            "Because everything is kept locally, you can export your laps to a CSV file and open them in a spreadsheet to chart pace or spot the slowest segment. Nothing is uploaded, so timing a workout, a presentation rehearsal or a cooking step stays entirely on your device.",
        ],
    ),
    faqs=[
        ("Is this online stopwatch free?", "Yes, with no limits, no account and no sign-up."),
        ("What is the difference between a lap and a split?", "The lap time is how long one segment took; the total (split) is the running time since you started. This stopwatch shows both for every lap you record."),
        ("Can I control it with the keyboard?", "Yes. The space bar starts and stops the stopwatch, and the L key records a lap, so you can time hands-free."),
        ("Does it keep running if I switch tabs?", "Yes. Timing is based on the system clock, so the elapsed time stays accurate even if the tab is in the background."),
    ],
    script=r""" let running = false, startTime = 0, elapsed = 0, raf = null;
    let laps = [], lastLap = 0;

    function fmt(ms) {
      const cs = Math.floor(ms / 10) % 100;
      const s = Math.floor(ms / 1000) % 60;
      const m = Math.floor(ms / 60000) % 60;
      const h = Math.floor(ms / 3600000);
      const p = (n) => String(n).padStart(2, '0');
      return (h > 0 ? p(h) + ':' : '') + p(m) + ':' + p(s) + '.' + p(cs);
    }

    function render() {
      const now = performance.now();
      T.$('display').textContent = fmt(elapsed + (running ? now - startTime : 0));
      if (running) raf = requestAnimationFrame(render);
    }

    function startStop() {
      if (running) {
        elapsed += performance.now() - startTime;
        running = false;
        cancelAnimationFrame(raf);
        T.$('startstop').textContent = 'Start';
        T.status('status', 'Paused.', 'muted');
      } else {
        startTime = performance.now();
        running = true;
        T.$('startstop').textContent = 'Stop';
        T.status('status', 'Running...', 'ok');
        render();
      }
    }

    function currentMs() { return elapsed + (running ? performance.now() - startTime : 0); }

    function lap() {
      const total = currentMs();
      if (total === 0) return;
      const lapTime = total - lastLap;
      lastLap = total;
      laps.push({ lapTime, total });
      const tr = document.createElement('tr');
      tr.innerHTML = '<td>' + laps.length + '</td><td>' + fmt(lapTime) + '</td><td>' + fmt(total) + '</td>';
      T.$('laps-body').prepend(tr);
      T.$('laps-wrap').hidden = false;
    }

    function reset() {
      running = false;
      cancelAnimationFrame(raf);
      elapsed = 0; lastLap = 0; laps = [];
      T.$('display').textContent = '00:00.00';
      T.$('startstop').textContent = 'Start';
      T.$('laps-body').innerHTML = '';
      T.$('laps-wrap').hidden = true;
      T.status('status', 'Reset. Press Start, or hit the space bar.', 'muted');
    }

    T.$('startstop').addEventListener('click', startStop);
    T.$('lap').addEventListener('click', lap);
    T.$('reset').addEventListener('click', reset);
    T.$('export').addEventListener('click', () => {
      if (!laps.length) { T.status('status', 'No laps to export yet.', 'muted'); return; }
      let csv = 'Lap,Lap time,Total time\n';
      laps.forEach((l, i) => { csv += (i + 1) + ',' + fmt(l.lapTime) + ',' + fmt(l.total) + '\n'; });
      const blob = new Blob([csv], { type: 'text/csv' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob); a.download = 'stopwatch-laps.csv';
      document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(a.href);
    });
    T.$('share').addEventListener('click', () => shareLink({ title: 'Online Stopwatch | 123MiniApps' }));

    document.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      if (e.code === 'Space') { e.preventDefault(); startStop(); }
      else if (e.key === 'l' || e.key === 'L') { e.preventDefault(); lap(); }
    });

    if (window.Analytics) Analytics.trackToolUse('online-stopwatch');""",
))

# ---------------------------------------------------------------
# GPA Calculator
# ---------------------------------------------------------------
PAGES.append(tool(
    slug="gpa-calculator", name="GPA Calculator", icon="🎓", cat="calculator",
    title="GPA Calculator",
    description="Calculate your GPA from letter grades and credit hours on the 4.0, 4.3 or 5.0 scale. Add unlimited courses and see your weighted grade point average.",
    tagline="Work out your weighted GPA from grades and credits on any common scale.",
    workspace=ws(
        row(
            select("scale", "Grading scale", [("4.0", "4.0 scale (standard US)"), ("4.3", "4.3 scale (A+ = 4.3)"), ("5.0", "5.0 weighted scale")], "4.0"),
            html_block(""" <div class="field"><label class="field__label"><span>&nbsp;</span></label><button class="btn btn--secondary" id="add" type="button">+ Add course</button></div>"""),
        ),
        html_block(""" <div id="courses"></div>"""),
        status_line("status", "Add your courses, pick a grade and enter the credit hours."),
        HR,
        html_block(""" <div class="result-grid">
      <div class="result"><span class="result__value" id="r-gpa" style="font-size:var(--text-3xl)">0.00</span><span class="result__label">Grade point average</span></div>
      <div class="result"><span class="result__value" id="r-credits" style="font-size:var(--text-2xl)">0</span><span class="result__label">Total credits</span></div>
      <div class="result"><span class="result__value" id="r-points" style="font-size:var(--text-2xl)">0.0</span><span class="result__label">Total grade points</span></div>
    </div>"""),
        buttons(("copy", "Copy result", "primary"), ("reset", "Reset", "ghost"), ("share", "Share tool", "ghost")),
        label="GPA calculator",
    ),
    info_block=info(
        features=[
            "Weighted GPA from letter grades and credit hours",
            "Standard 4.0, 4.3 and 5.0 scales",
            "Add or remove as many courses as you need",
            "Live total credits and grade points",
            "Runs in your browser, nothing is saved online",
        ],
        howto=[
            "Choose your grading scale at the top.",
            "Add a row for each course, pick its letter grade and credits.",
            "Your GPA updates instantly as you edit.",
            "Copy the result or reset to start over.",
        ],
        background_title="How GPA is actually calculated",
        background_paragraphs=[
            "A grade point average is a weighted average, not a simple one. Each letter grade maps to a number of points, an A is 4.0, a B is 3.0, and so on, and each course is weighted by its credit hours. To find your GPA you multiply each course's grade points by its credits, add those up across every course, and divide by the total number of credits. A run of A grades in one-credit electives moves your average far less than a single grade in a four-credit core course, which is exactly why weighting matters.",
            "Scales differ between institutions. The standard US scale caps at 4.0 and treats A and A+ alike; a 4.3 scale rewards an A+ with 4.3 points; and weighted 5.0 scales, common in high schools, add a point for honours or AP classes. This calculator lets you pick the scale so the numbers match your transcript rather than a generic default.",
            "Cumulative GPA works the same way across semesters: keep adding courses and the running total of credits and grade points gives your overall average. Because the maths is transparent, you can also use the tool to plan, entering the grades you expect next term to see where your GPA would land.",
        ],
    ),
    faqs=[
        ("Is this GPA calculator free?", "Yes, with no limits, no account and no sign-up."),
        ("How is GPA calculated?", "GPA is the sum of each course's grade points times its credit hours, divided by the total credit hours. This tool does that weighting automatically as you add courses."),
        ("Which grading scales are supported?", "The standard 4.0 scale, a 4.3 scale where an A+ is worth 4.3, and a weighted 5.0 scale used for honours and AP courses. Pick the one your school uses."),
        ("Is my data saved or uploaded?", "No. Everything is calculated in your browser and nothing is stored online, so your grades stay private."),
    ],
    script=r""" const SCALES = {
      '4.0': { 'A+': 4.0, 'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'D-': 0.7, 'F': 0.0 },
      '4.3': { 'A+': 4.3, 'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'D-': 0.7, 'F': 0.0 },
      '5.0': { 'A+': 5.0, 'A': 5.0, 'A-': 4.7, 'B+': 4.3, 'B': 4.0, 'B-': 3.7, 'C+': 3.3, 'C': 3.0, 'C-': 2.7, 'D+': 2.3, 'D': 2.0, 'D-': 1.7, 'F': 0.0 }
    };

    function gradeOptions() {
      return Object.keys(SCALES['4.0']).map((g) => '<option value="' + g + '">' + g + '</option>').join('');
    }

    function addRow(name, grade, credits) {
      const div = document.createElement('div');
      div.className = 'workspace__row course-row';
      div.innerHTML =
        '<div class="field"><input class="input" type="text" placeholder="Course name (optional)" value="' + (name || '') + '"></div>' +
        '<div class="field"><select class="input course-grade">' + gradeOptions() + '</select></div>' +
        '<div class="field"><input class="input course-credits" type="number" min="0" step="0.5" placeholder="Credits" value="' + (credits || '') + '"></div>' +
        '<div class="field"><button class="btn btn--ghost btn--sm course-del" type="button" aria-label="Remove course">Remove</button></div>';
      T.$('courses').appendChild(div);
      if (grade) div.querySelector('.course-grade').value = grade;
      div.querySelector('.course-grade').addEventListener('change', calc);
      div.querySelector('.course-credits').addEventListener('input', calc);
      div.querySelector('.course-del').addEventListener('click', () => { div.remove(); calc(); });
      calc();
    }

    function calc() {
      const scale = SCALES[T.$('scale').value];
      let totalCredits = 0, totalPoints = 0;
      document.querySelectorAll('.course-row').forEach((r) => {
        const grade = r.querySelector('.course-grade').value;
        const credits = parseFloat(r.querySelector('.course-credits').value);
        if (!isNaN(credits) && credits > 0) {
          totalCredits += credits;
          totalPoints += scale[grade] * credits;
        }
      });
      const gpa = totalCredits > 0 ? totalPoints / totalCredits : 0;
      T.$('r-gpa').textContent = gpa.toFixed(2);
      T.$('r-credits').textContent = String(totalCredits);
      T.$('r-points').textContent = totalPoints.toFixed(1);
      T.status('status', totalCredits > 0 ? 'GPA across ' + totalCredits + ' credit(s).' : 'Enter credit hours to calculate.', totalCredits > 0 ? 'ok' : 'muted');
    }

    T.$('add').addEventListener('click', () => addRow('', 'A', ''));
    T.$('scale').addEventListener('change', calc);
    T.$('copy').addEventListener('click', () => copyToClipboard('GPA: ' + T.$('r-gpa').textContent + ' over ' + T.$('r-credits').textContent + ' credits', 'Result copied'));
    T.$('reset').addEventListener('click', () => { T.$('courses').innerHTML = ''; addRow('', 'A', '3'); addRow('', 'B+', '3'); addRow('', 'A-', '4'); });
    T.$('share').addEventListener('click', () => shareLink({ title: 'GPA Calculator | 123MiniApps' }));

    addRow('', 'A', '3');
    addRow('', 'B+', '3');
    addRow('', 'A-', '4');
    if (window.Analytics) Analytics.trackToolUse('gpa-calculator');""",
))

# ---------------------------------------------------------------
# Sales Tax / VAT Calculator
# ---------------------------------------------------------------
PAGES.append(tool(
    slug="sales-tax-calculator", name="Sales Tax Calculator", icon="🧾", cat="calculator",
    title="Sales Tax Calculator",
    description="Add sales tax or VAT to a price, or work backwards to strip tax out of a total. Enter any rate and see the net, tax and gross amounts instantly.",
    tagline="Add sales tax or VAT to a price, or extract the tax back out of a total.",
    workspace=ws(
        row(
            number_input("amount", "Amount", value="100", placeholder="0.00", step="0.01", min=0),
            number_input("rate", "Tax rate (%)", value="8.5", placeholder="0", step="0.01", min=0),
        ),
        html_block(""" <div class="field">
      <label class="field__label"><span>Mode</span></label>
      <div style="display:flex;gap:8px;flex-wrap:wrap" role="radiogroup" aria-label="Mode">
        <button class="btn btn--primary" id="mode-add" type="button" role="radio" aria-checked="true">Add tax to a net price</button>
        <button class="btn btn--ghost" id="mode-extract" type="button" role="radio" aria-checked="false">Remove tax from a gross total</button>
      </div>
    </div>"""),
        status_line("status", "Enter an amount and a rate to see the breakdown."),
        HR,
        html_block(""" <div class="result-grid">
      <div class="result"><span class="result__value" id="r-net" style="font-size:var(--text-2xl)">100.00</span><span class="result__label">Net (before tax)</span></div>
      <div class="result"><span class="result__value" id="r-tax" style="font-size:var(--text-2xl)">8.50</span><span class="result__label">Tax</span></div>
      <div class="result"><span class="result__value" id="r-gross" style="font-size:var(--text-3xl)">108.50</span><span class="result__label">Gross (with tax)</span></div>
    </div>"""),
        buttons(("copy", "Copy breakdown", "primary"), ("share", "Share tool", "ghost")),
        label="Sales tax calculator",
    ),
    info_block=info(
        features=[
            "Add tax to a price, or remove tax from a total",
            "Works for any sales tax or VAT rate",
            "Shows net, tax and gross amounts at once",
            "Reverse mode extracts the tax already included",
            "Runs in your browser, nothing is uploaded",
        ],
        howto=[
            "Enter the amount and the tax rate as a percentage.",
            "Choose add tax (for a net price) or remove tax (for a gross total).",
            "Read off the net, tax and gross figures instantly.",
            "Copy the full breakdown with one click.",
        ],
        background_title="Adding tax versus extracting it",
        background_paragraphs=[
            "There are two everyday tax questions and they are not the same calculation. The first is forward: you have a net price and want to add tax, so you multiply the price by the rate and add it on. A 100 item at 8.5 percent becomes 108.50. The second is backward: you have a gross total that already includes tax and want to know how much of it is tax, which many people get wrong by simply subtracting the rate.",
            "Extracting tax correctly means dividing, not subtracting. If a total of 108.50 includes 8.5 percent tax, the net is 108.50 divided by 1.085, which is 100, and the tax is the difference, 8.50. Subtracting 8.5 percent of 108.50 would give the wrong answer, because the percentage was applied to the smaller net figure, not the gross. This calculator's remove-tax mode does the division for you.",
            "The same maths covers US sales tax and European or global VAT, since both are a percentage added to a price. The only difference is convention: sales tax is usually shown added at the register, while VAT is typically already included in the displayed price, which is exactly when the reverse calculation is useful.",
        ],
    ),
    faqs=[
        ("Is this sales tax calculator free?", "Yes, with no limits, no account and no sign-up."),
        ("How do I remove tax from a total?", "Switch to remove-tax mode and enter the gross total. The tool divides by one plus the rate to find the net price, then shows the tax that was included."),
        ("Does it work for VAT as well as sales tax?", "Yes. VAT and sales tax are both a percentage of a price, so enter your VAT rate and use remove-tax mode when the price already includes VAT."),
        ("Are my numbers sent anywhere?", "No. The calculation runs entirely in your browser, so nothing you enter leaves your device."),
    ],
    script=r""" let mode = 'add';

    function calc() {
      const amount = parseFloat(T.$('amount').value);
      const rate = parseFloat(T.$('rate').value);
      if (isNaN(amount) || isNaN(rate)) { T.status('status', 'Enter an amount and a rate.', 'muted'); return; }
      const r = rate / 100;
      let net, tax, gross;
      if (mode === 'add') { net = amount; tax = amount * r; gross = amount + tax; }
      else { gross = amount; net = amount / (1 + r); tax = gross - net; }
      T.$('r-net').textContent = net.toFixed(2);
      T.$('r-tax').textContent = tax.toFixed(2);
      T.$('r-gross').textContent = gross.toFixed(2);
      T.status('status', (mode === 'add' ? 'Tax added at ' : 'Tax extracted at ') + rate + '%.', 'ok');
    }

    function setMode(m) {
      mode = m;
      T.$('mode-add').className = 'btn ' + (m === 'add' ? 'btn--primary' : 'btn--ghost');
      T.$('mode-extract').className = 'btn ' + (m === 'extract' ? 'btn--primary' : 'btn--ghost');
      T.$('mode-add').setAttribute('aria-checked', String(m === 'add'));
      T.$('mode-extract').setAttribute('aria-checked', String(m === 'extract'));
      calc();
    }

    T.$('amount').addEventListener('input', calc);
    T.$('rate').addEventListener('input', calc);
    T.$('mode-add').addEventListener('click', () => setMode('add'));
    T.$('mode-extract').addEventListener('click', () => setMode('extract'));
    T.$('copy').addEventListener('click', () => copyToClipboard('Net: ' + T.$('r-net').textContent + '  Tax: ' + T.$('r-tax').textContent + '  Gross: ' + T.$('r-gross').textContent, 'Breakdown copied'));
    T.$('share').addEventListener('click', () => shareLink({ title: 'Sales Tax Calculator | 123MiniApps' }));

    calc();
    if (window.Analytics) Analytics.trackToolUse('sales-tax-calculator');""",
))
