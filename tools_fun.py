#!/usr/bin/env python3
# ============================================
# 123MiniApps.online v2.0
# File: tools_fun.py
# Purpose: The 6 Fun Tools (ids 90-95).
#
# All randomness here goes through T.randomBelow,
# which is CSPRNG-backed and rejection-sampled, if
# someone runs a giveaway with these, the draw should
# actually be fair.
# ============================================

from toolkit import (
 tool, ws, info, row, textarea, text_input, number_input, select, switch,
 slider, output, status_line, buttons, canvas, HR, html_block,
)

PAGES = []

# ---------------------------------------------------------------
# 90. Random Picker
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="random-picker", name="Random Picker", icon="🎯", cat="fun",
 title="Random Picker: Fair Draws From Any List",
 description="Drop in a list and pick a winner fairly, with an animated reveal. Remove-after-pick mode, multiple winners and cryptographic randomness.",
 tagline="Pick a winner from any list, fairly, with cryptographic randomness.",
 workspace=ws(
 textarea("input", "Your list", "One entry per line…", "input-stats", rows=180,
 value="Alice\nBob\nCharlie\nDiana\nEli\nFatima\nGeorge\nHannah"),
 row(
 number_input("winners", "How many to pick", "1", "1", step="1", min=1),
 switch("remove", "Remove winners from the list after picking", False),
 switch("animate", "Animated reveal", True),
 ),
 html_block(""" <div class="display" id="display">
 <span class="display__value" id="result" style="font-size:clamp(1.75rem,1rem+4vw,3.5rem)">, </span>
 <span class="display__label" id="caption">Press Pick to draw</span>
 </div>"""),
 status_line("status", "Paste a list and press Pick."),
 buttons(("pick", "Pick", "primary"), ("shuffle", "Shuffle the whole list"), ("reset", "Restore removed"), ("copy", "Copy winners"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Draw history</span><span class="field__hint">This session only</span></span>
 <div class="table-scroll"><div id="history"></div></div>
 </div>"""),
 label="Random picker",
 ),
 info_block=info(
 features=[
 "Pick one winner or several at once",
 "Remove-after-pick for multi-round draws",
 "Animated reveal that cycles through entries",
 "Shuffle the entire list into random order",
 "Cryptographically secure and provably unbiased",
 ],
 howto=[
 "Paste your entries, one per line.",
 "Choose how many winners to draw.",
 "Press Pick.",
 "Turn on remove-after-pick for multi-round draws.",
 ],
 background_title="What makes a draw actually fair",
 background_paragraphs=[
 "Two things can quietly break a random draw, and both are common. The first is the randomness source: <code>Math.random()</code> is a predictable pseudo-random generator, and given a handful of previous outputs its internal state can be recovered and future values predicted. For a prize draw that matters. This tool uses <code>crypto.getRandomValues()</code>, which draws from the operating system's cryptographic entropy pool.",
 "The second is modulo bias. Mapping a random 32-bit number into a range of, say, 7 entries by taking the remainder gives the first few entries a very slightly higher chance, because 2³² is not divisible by 7. The bias is small but it is real and it is systematic, the same entries are favoured every time. This tool uses rejection sampling, discarding values that fall in the uneven tail, which makes every entry exactly equally likely.",
 "For multiple winners the tool uses a partial Fisher-Yates shuffle rather than picking repeatedly and discarding duplicates. That guarantees distinct winners in a single pass and, unlike the naive approach, produces every possible combination with equal probability. If you are running a draw where the outcome matters to people, it is worth being able to say all of this.",
 ],
 ),
 script=r""" let removed = [];
 let history = [];
 let animating = false;

 function entries() {
 return T.$('input').value
 .split(/\r?\n/)
 .map((line) => line.trim())
 .filter(Boolean);
 }

 function updateStats() {
 const count = entries().length;
 T.$('input-stats').textContent = count ? `${count} entr${count === 1 ? 'y' : 'ies'}` : '';
 }

 function pick() {
 if (animating) return;

 const list = entries();
 const wanted = Math.max(1, Math.floor(T.num(T.$('winners').value) || 1));

 if (!list.length) {
 T.status('status', 'Add some entries first.', 'error');
 return;
 }

 if (wanted > list.length) {
 T.status('status',
 `You asked for ${wanted} winners but there are only ${list.length} entries.`, 'error');
 return;
 }

 // Partial Fisher-Yates: guarantees distinct winners in one pass and
 // gives every combination equal probability
 const pool = [...list];
 const winners = [];
 for (let i = 0; i < wanted; i++) {
 const j = i + T.randomBelow(pool.length - i);
 [pool[i], pool[j]] = [pool[j], pool[i]];
 winners.push(pool[i]);
 }

 if (T.$('animate').checked) {
 animateReveal(list, winners);
 } else {
 reveal(winners, list.length);
 }
 }

 /** Cycle through entries with a decelerating interval, then settle. */
 function animateReveal(list, winners) {
 animating = true;
 T.$('pick').disabled = true;
 T.$('caption').textContent = 'Drawing…';

 let step = 0;
 const steps = 22;

 const tick = () => {
 if (step >= steps) {
 animating = false;
 T.$('pick').disabled = false;
 reveal(winners, list.length);
 return;
 }

 T.$('result').textContent = T.pick(list);
 step++;

 // Ease out: start fast, slow toward the end
 const delay = 40 + Math.pow(step / steps, 3) * 220;
 setTimeout(tick, delay);
 };

 tick();
 }

 function reveal(winners, poolSize) {
 T.$('result').textContent = winners.join(', ');
 T.$('caption').textContent = winners.length === 1
 ? `Drawn from ${poolSize} entries`
 : `${winners.length} winners from ${poolSize} entries`;

 history.unshift({ at: Date.now(), winners: winners.join(', '), poolSize });
 history = history.slice(0, 20);
 renderHistory();

 if (T.$('remove').checked) {
 const remaining = entries().filter((entry) => !winners.includes(entry));
 removed.push(...winners);
 T.$('input').value = remaining.join('\n');
 updateStats();
 T.status('status',
 `Picked ${winners.join(', ')}. ${remaining.length} entr${remaining.length === 1 ? 'y' : 'ies'} left.`,
 'ok');
 } else {
 T.status('status', `Picked ${winners.join(', ')} from ${poolSize} entries.`, 'ok');
 }

 if (window.Analytics) Analytics.trackToolUse('random-picker');
 }

 function renderHistory() {
 const mount = T.$('history');
 mount.innerHTML = '';
 if (!history.length) return;

 mount.append(T.table(
 ['Time', 'Winner(s)', 'Pool size'],
 history.map((h) => [
 new Date(h.at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
 h.winners,
 h.poolSize
 ])
 ));
 }

 T.$('pick').addEventListener('click', pick);

 T.$('shuffle').addEventListener('click', () => {
 const list = entries();
 if (list.length < 2) {
 T.status('status', 'Need at least two entries to shuffle.', 'warn');
 return;
 }
 T.$('input').value = T.shuffle([...list]).join('\n');
 T.status('status', `Shuffled ${list.length} entries into a random order.`, 'ok');
 });

 T.$('reset').addEventListener('click', () => {
 if (!removed.length) {
 T.status('status', 'Nothing has been removed.', 'muted');
 return;
 }
 T.$('input').value = entries().concat(removed).join('\n');
 T.status('status', `Restored ${removed.length} removed entr${removed.length === 1 ? 'y' : 'ies'}.`, 'ok');
 removed = [];
 updateStats();
 });

 T.$('copy').addEventListener('click', () => {
 if (!history.length) { toast({ type: 'warning', title: 'No draws yet' }); return; }
 copyToClipboard(history.map((h) => h.winners).join('\n'), 'Winners copied');
 });

 T.$('input').addEventListener('input', debounce(updateStats, 200));
 T.$('share').addEventListener('click', () => shareLink({ title: 'Random Picker | 123MiniApps' }));

 updateStats();""",
))

# ---------------------------------------------------------------
# 91. Dice Roller
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="dice-roller", name="Dice Roller", icon="🎲", cat="fun",
 title="Dice Roller: Full Dice Notation with Modifiers",
 description="Roll any dice notation from d4 to d100 with modifiers, advantage and disadvantage, exploding dice and a running roll history.",
 tagline="Roll full dice notation, 3d6+2, advantage, exploding dice and all.",
 workspace=ws(
 html_block(""" <div class="field">
 <label class="field__label" for="notation">
 <span>Dice notation</span>
 <span class="field__hint">e.g. 3d6+2, 2d20, 4d6kh3</span>
 </label>
 <input class="input font-mono" id="notation" type="text" value="1d20"
 style="font-size:var(--text-xl);height:60px" autocomplete="off" spellcheck="false">
 </div>"""),
 row(
 select("mode", "Roll mode", [
 ("normal", "Normal"),
 ("advantage", "Advantage, roll twice, keep highest"),
 ("disadvantage", "Disadvantage, roll twice, keep lowest"),
 ], selected="normal"),
 switch("explode", "Exploding dice, max roll rolls again", False),
 ),
 html_block(""" <div class="display" id="display">
 <span class="display__value" id="total">, </span>
 <span class="display__label" id="breakdown">Press Roll</span>
 </div>"""),
 status_line("status", "Enter dice notation and press Roll."),
 buttons(("roll", "Roll", "primary"), ("reroll", "Roll again"), ("clear", "Clear history", "ghost"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Common dice</span></span>
 <div class="chip-grid" id="presets"></div>
 </div>"""),
 html_block(""" <div class="result-grid">
 <div class="result"><span class="result__value" id="r-rolls" style="font-size:var(--text-2xl)">0</span><span class="result__label">Rolls this session</span></div>
 <div class="result"><span class="result__value" id="r-average" style="font-size:var(--text-2xl)">, </span><span class="result__label">Average total</span></div>
 <div class="result"><span class="result__value" id="r-highest" style="font-size:var(--text-2xl)">, </span><span class="result__label">Highest</span></div>
 <div class="result"><span class="result__value" id="r-lowest" style="font-size:var(--text-2xl)">, </span><span class="result__label">Lowest</span></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Roll history</span></span>
 <div class="table-scroll"><div id="history"></div></div>
 </div>"""),
 label="Dice roller",
 ),
 info_block=info(
 features=[
 "Full dice notation including keep-highest and keep-lowest",
 "Advantage and disadvantage",
 "Exploding dice",
 "Session statistics and roll history",
 "Cryptographic randomness, not Math.random",
 ],
 howto=[
 "Type notation such as 3d6+2, or tap a preset.",
 "Choose advantage or disadvantage if you need it.",
 "Press Roll.",
 "Individual die results are shown beneath the total.",
 ],
 background_title="Reading dice notation",
 background_paragraphs=[
 "The basic form is <code>NdS</code>: N dice with S sides each. <code>3d6</code> rolls three six-sided dice and sums them. Modifiers are added after: <code>3d6+2</code> adds two to the total, <code>1d20-1</code> subtracts one. This is the notation Dungeons &amp; Dragons popularised and it is now near-universal across tabletop games.",
 "The keep notation handles the common case of rolling extra dice and discarding some. <code>4d6kh3</code> rolls four six-sided dice and keeps the highest three, the standard method for generating D&amp;D ability scores, because discarding the lowest die shifts the average from 10.5 up to about 12.24. <code>2d20kl1</code> keeps the lowest of two, which is what disadvantage does.",
 "Multiple dice produce a bell curve, and this matters more than people expect. A single d20 is flat: every result from 1 to 20 is equally likely. Three d6 sum to between 3 and 18 but cluster heavily around 10 and 11, with a 1-in-216 chance of either extreme. Games that use 3d6 instead of 1d20 are choosing predictability, the average outcome dominates and dramatic swings are rare.",
 ],
 ),
 script=r""" let history = [];

 const PRESETS = ['1d4', '1d6', '1d8', '1d10', '1d12', '1d20', '1d100',
 '2d6', '3d6', '4d6kh3', '2d20kh1', '1d20+5'];

 /**
 * Parse dice notation into a structured roll.
 * Supports NdS, +/- modifiers, and khN / klN keep clauses.
 * @returns {{count: number, sides: number, modifier: number, keep: ?{mode: string, n: number}}|null}
 */
 function parse(notation) {
 const cleaned = String(notation).trim().toLowerCase().replace(/\s+/g, '');
 const match = cleaned.match(/^(\d*)d(\d+)((?:kh|kl)\d+)?([+-]\d+)?$/);
 if (!match) return null;

 const count = match[1] ? Number(match[1]) : 1;
 const sides = Number(match[2]);
 const modifier = match[4] ? Number(match[4]) : 0;

 let keep = null;
 if (match[3]) {
 keep = { mode: match[3].slice(0, 2), n: Number(match[3].slice(2)) };
 if (keep.n > count || keep.n < 1) return null;
 }

 if (count < 1 || count > 200) return null;
 // d1 is degenerate but valid notation and common parsers accept it,
 // so allow anything from 1 upward rather than rejecting it.
 if (sides < 1 || sides > 1000) return null;

 return { count, sides, modifier, keep };
 }

 /** Roll one die, exploding on a maximum result if enabled. */
 function rollDie(sides) {
 let total = T.randomInt(1, sides);
 const parts = [total];

 if (T.$('explode').checked) {
 let guard = 0;
 while (parts[parts.length - 1] === sides && guard < 20) {
 const extra = T.randomInt(1, sides);
 parts.push(extra);
 total += extra;
 guard++;
 }
 }

 return { total, parts };
 }

 function rollOnce(spec) {
 const dice = Array.from({ length: spec.count }, () => rollDie(spec.sides));
 let values = dice.map((d) => d.total);
 let kept = [...values];
 let dropped = [];

 if (spec.keep) {
 const sorted = [...values].sort((a, b) => spec.keep.mode === 'kh' ? b - a : a - b);
 kept = sorted.slice(0, spec.keep.n);
 dropped = sorted.slice(spec.keep.n);
 }

 const total = kept.reduce((sum, v) => sum + v, 0) + spec.modifier;
 return { total, values, kept, dropped, dice };
 }

 function roll() {
 const notation = T.$('notation').value;
 const spec = parse(notation);

 if (!spec) {
 T.status('status',
 'Could not read that notation. Try something like 3d6+2 or 4d6kh3.', 'error');
 return;
 }

 const mode = T.$('mode').value;
 let result;
 let modeNote = '';

 if (mode === 'normal') {
 result = rollOnce(spec);
 } else {
 // Advantage and disadvantage roll the whole expression twice
 const a = rollOnce(spec);
 const b = rollOnce(spec);
 const takeHigher = mode === 'advantage';
 result = (takeHigher ? a.total >= b.total : a.total <= b.total) ? a : b;
 modeNote = ` (${mode}: ${a.total} vs ${b.total})`;
 }

 T.$('total').textContent = String(result.total);

 const parts = [];
 parts.push(`Dice: [${result.values.join(', ')}]`);
 if (result.dropped.length) parts.push(`dropped [${result.dropped.join(', ')}]`);
 if (spec.modifier) parts.push(`${spec.modifier > 0 ? '+' : ''}${spec.modifier}`);

 T.$('breakdown').textContent = parts.join(' · ') + modeNote;

 // Highlight natural maximum and minimum on a single die
 if (spec.count === 1 && !spec.keep) {
 if (result.values[0] === spec.sides) {
 T.$('total').style.color = 'var(--success)';
 T.$('breakdown').textContent += ', natural maximum!';
 } else if (result.values[0] === 1) {
 T.$('total').style.color = 'var(--danger)';
 T.$('breakdown').textContent += ', natural 1.';
 } else {
 T.$('total').style.color = '';
 }
 } else {
 T.$('total').style.color = '';
 }

 history.unshift({
 at: Date.now(),
 notation: notation.trim(),
 total: result.total,
 detail: `[${result.values.join(', ')}]${spec.modifier ? ` ${spec.modifier > 0 ? '+' : ''}${spec.modifier}` : ''}`
 });
 history = history.slice(0, 30);

 renderHistory();
 renderStats(spec);

 T.status('status', `Rolled ${notation.trim()} for ${result.total}.`, 'ok');
 if (window.Analytics) Analytics.trackToolUse('dice-roller');
 }

 function renderStats(spec) {
 const totals = history.map((h) => h.total);

 T.$('r-rolls').textContent = String(history.length);
 T.$('r-average').textContent = totals.length
 ? T.fmt(totals.reduce((a, b) => a + b, 0) / totals.length, 1)
 : ', ';
 T.$('r-highest').textContent = totals.length ? String(Math.max(...totals)) : ', ';
 T.$('r-lowest').textContent = totals.length ? String(Math.min(...totals)) : ', ';
 void spec;
 }

 function renderHistory() {
 const mount = T.$('history');
 mount.innerHTML = '';
 if (!history.length) return;

 mount.append(T.table(
 ['Time', 'Notation', 'Result', 'Detail'],
 history.map((h) => [
 new Date(h.at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
 h.notation,
 h.total,
 h.detail
 ])
 ));
 }

 T.$('roll').addEventListener('click', roll);
 T.$('reroll').addEventListener('click', roll);

 T.$('notation').addEventListener('keydown', (e) => {
 if (e.key === 'Enter') { e.preventDefault(); roll(); }
 });

 T.$('clear').addEventListener('click', () => {
 history = [];
 renderHistory();
 renderStats();
 T.status('status', 'History cleared.', 'muted');
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Dice Roller | 123MiniApps' }));

 const presetMount = T.$('presets');
 PRESETS.forEach((notation) => {
 const chip = el('button', { className: 'chip font-mono', attrs: { type: 'button' }, text: notation });
 chip.addEventListener('click', () => {
 T.$('notation').value = notation;
 roll();
 });
 presetMount.append(chip);
 });""",
))

# ---------------------------------------------------------------
# 92. Coin Flip
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="coin-flip", name="Coin Flip", icon="🪙", cat="fun",
 title="Coin Flip: One Toss or a Thousand",
 description="Flip a coin with an animated reveal, or flip hundreds at once and watch the running tally converge on fifty-fifty.",
 tagline="Flip one coin, or a thousand, and watch the tally converge on fifty-fifty.",
 workspace=ws(
 html_block(""" <div class="display" id="display">
 <span class="display__value" id="result" style="font-size:clamp(3rem,2rem+6vw,6rem)">🪙</span>
 <span class="display__label" id="caption">Press Flip</span>
 </div>"""),
 row(
 number_input("count", "How many to flip", "1", "1", step="1", min=1, max=10000),
 text_input("heads-label", "Call heads", "Heads", "Heads"),
 text_input("tails-label", "Call tails", "Tails", "Tails"),
 ),
 switch("animate", "Animate a single flip", True),
 status_line("status", "Press Flip to toss."),
 buttons(("flip", "Flip", "primary"), ("flip-100", "Flip 100"), ("reset", "Reset tally", "ghost"), ("copy", "Copy results"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result result--primary"><span class="result__value" id="r-total" style="font-size:var(--text-3xl)">0</span><span class="result__label">Total flips</span></div>
 <div class="result"><span class="result__value" id="r-heads" style="font-size:var(--text-3xl)">0</span><span class="result__label" id="l-heads">Heads</span></div>
 <div class="result"><span class="result__value" id="r-tails" style="font-size:var(--text-3xl)">0</span><span class="result__label" id="l-tails">Tails</span></div>
 <div class="result"><span class="result__value" id="r-split" style="font-size:var(--text-2xl)">, </span><span class="result__label">Split</span></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Distribution</span></span>
 <div id="bar" style="display:flex;height:44px;border-radius:var(--radius-sm);overflow:hidden;border:1px solid var(--border-color)">
 <div id="bar-heads" style="background:var(--accent-primary);display:grid;place-items:center;font-size:var(--text-sm);font-weight:600;color:var(--on-accent);transition:width .3s"></div>
 <div id="bar-tails" style="background:var(--accent-secondary);display:grid;place-items:center;font-size:var(--text-sm);font-weight:600;color:var(--on-accent);transition:width .3s"></div>
 </div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Recent flips</span><span class="field__hint">Newest first</span></span>
 <div id="recent" class="chip-grid"></div>
 </div>"""),
 label="Coin flip",
 ),
 info_block=info(
 features=[
 "Single animated flip or bulk flipping",
 "Custom labels instead of heads and tails",
 "Running tally with a visual distribution bar",
 "Up to 10,000 flips at once",
 "Cryptographically fair",
 ],
 howto=[
 "Press Flip for a single toss.",
 "Set a count and flip many at once.",
 "Rename the sides if you are deciding between two options.",
 "Watch the split converge as the count rises.",
 ],
 background_title="Why a real coin is not quite fifty-fifty",
 background_paragraphs=[
 "A physical coin toss is not perfectly fair, and the deviation has been measured. Persi Diaconis and colleagues at Stanford showed that a coin caught in the hand lands the same way it started about 51% of the time, because the coin precesses about an axis rather than flipping cleanly. A 2023 study with 350,757 recorded flips confirmed the effect at almost exactly the predicted rate. A coin allowed to bounce on a surface behaves differently again, since the bounce introduces chaotic dynamics.",
 "This simulation has no such bias. Each flip draws from the operating system's cryptographic entropy pool with rejection sampling, so the two outcomes are exactly equally likely and each flip is independent of the last.",
 "That independence is the thing people find hardest to accept. After eight heads in a row, the ninth flip is still exactly fifty-fifty, the coin has no memory. The gambler's fallacy is the belief that a run must be corrected; the equally wrong hot-hand version is the belief that a run will continue. What actually happens is that the <em>proportion</em> converges toward 50% as the count grows, while the absolute difference between heads and tails typically drifts further from zero. Flip a thousand times here and you will usually see something close to 50% alongside a gap of twenty or thirty flips.",
 ],
 ),
 script=r""" let heads = 0;
 let tails = 0;
 let recent = [];
 let flipping = false;

 function labels() {
 return {
 heads: T.$('heads-label').value.trim() || 'Heads',
 tails: T.$('tails-label').value.trim() || 'Tails'
 };
 }

 /** One fair flip. randomBelow is rejection-sampled, so exactly 50/50. */
 function flipOnce() {
 return T.randomBelow(2) === 0 ? 'heads' : 'tails';
 }

 function doFlip(count) {
 if (flipping) return;

 const total = T.clamp(Math.floor(count), 1, 10000);
 const results = Array.from({ length: total }, flipOnce);

 if (total === 1 && T.$('animate').checked) {
 animateSingle(results[0]);
 } else {
 applyResults(results);
 }
 }

 /** Spin through faces with a decelerating interval before settling. */
 function animateSingle(outcome) {
 flipping = true;
 T.$('flip').disabled = true;
 T.$('caption').textContent = 'Flipping…';

 const faces = ['🪙', '⚪', '🪙', '⚫'];
 let step = 0;
 const steps = 16;

 const tick = () => {
 if (step >= steps) {
 flipping = false;
 T.$('flip').disabled = false;
 applyResults([outcome]);
 return;
 }

 T.$('result').textContent = faces[step % faces.length];
 step++;
 setTimeout(tick, 40 + Math.pow(step / steps, 3) * 200);
 };

 tick();
 }

 function applyResults(results) {
 const names = labels();

 results.forEach((outcome) => {
 if (outcome === 'heads') heads++; else tails++;
 });

 recent = results.slice(-40).reverse().concat(recent).slice(0, 40);

 if (results.length === 1) {
 const outcome = results[0];
 T.$('result').textContent = outcome === 'heads' ? '👑' : '🌙';
 T.$('caption').textContent = outcome === 'heads' ? names.heads : names.tails;
 T.status('status', `${outcome === 'heads' ? names.heads : names.tails}.`, 'ok');
 } else {
 const h = results.filter((r) => r === 'heads').length;
 T.$('result').textContent = `${h} / ${results.length - h}`;
 T.$('caption').textContent = `${names.heads} / ${names.tails} in this batch`;
 T.status('status',
 `Flipped ${results.length} times: ${h} ${names.heads.toLowerCase()}, ` +
 `${results.length - h} ${names.tails.toLowerCase()}.`, 'ok');
 }

 render();
 if (window.Analytics) Analytics.trackToolUse('coin-flip');
 }

 function render() {
 const names = labels();
 const total = heads + tails;

 T.$('r-total').textContent = total.toLocaleString();
 T.$('r-heads').textContent = heads.toLocaleString();
 T.$('r-tails').textContent = tails.toLocaleString();
 T.$('l-heads').textContent = names.heads;
 T.$('l-tails').textContent = names.tails;

 if (total) {
 const headsPct = (heads / total) * 100;
 T.$('r-split').textContent = `${headsPct.toFixed(1)}% / ${(100 - headsPct).toFixed(1)}%`;

 T.$('bar-heads').style.width = headsPct + '%';
 T.$('bar-tails').style.width = (100 - headsPct) + '%';
 T.$('bar-heads').textContent = headsPct > 12 ? `${heads}` : '';
 T.$('bar-tails').textContent = headsPct < 88 ? `${tails}` : '';
 } else {
 T.$('r-split').textContent = ', ';
 T.$('bar-heads').style.width = '50%';
 T.$('bar-tails').style.width = '50%';
 T.$('bar-heads').textContent = '';
 T.$('bar-tails').textContent = '';
 }

 const mount = T.$('recent');
 mount.innerHTML = '';
 recent.slice(0, 40).forEach((outcome) => {
 mount.append(el('span', {
 className: 'chip',
 text: outcome === 'heads' ? 'H' : 'T',
 style: {
 minWidth: '32px', textAlign: 'center', padding: 'var(--space-1) var(--space-2)',
 color: outcome === 'heads' ? 'var(--accent-primary)' : 'var(--accent-secondary)'
 }
 }));
 });
 }

 T.$('flip').addEventListener('click', () => doFlip(T.num(T.$('count').value) || 1));
 T.$('flip-100').addEventListener('click', () => doFlip(100));

 T.$('reset').addEventListener('click', () => {
 heads = 0; tails = 0; recent = [];
 T.$('result').textContent = '🪙';
 T.$('caption').textContent = 'Press Flip';
 render();
 T.status('status', 'Tally reset.', 'muted');
 });

 T.$('copy').addEventListener('click', () => {
 const names = labels();
 copyToClipboard(
 `${names.heads}: ${heads}\n${names.tails}: ${tails}\nTotal: ${heads + tails}`,
 'Results copied');
 });

 T.on(['heads-label', 'tails-label'], debounce(render, 200));
 T.$('share').addEventListener('click', () => shareLink({ title: 'Coin Flip | 123MiniApps' }));

 render();""",
))

# ---------------------------------------------------------------
# 93. Spin the Wheel
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="spin-the-wheel", name="Spin the Wheel", icon="🎡", cat="fun",
 title="Spin the Wheel: Custom Decision Wheel",
 description="Build a custom spinning wheel for decisions, giveaways or classrooms. Weighted odds, remove-after-spin and a shareable link carrying your entries.",
 tagline="Build a spinning wheel for decisions or giveaways, with weighted odds if you need them.",
 workspace=ws(
 textarea("input", "Wheel entries", "One per line. Add :2 to double an entry's odds.",
 "input-stats", rows=150,
 value="Pizza\nSushi\nCurry\nTacos\nRamen\nBurgers"),
 row(
 switch("weighted", "Enable weights (name:number)", False),
 switch("remove", "Remove the winner after each spin", False),
 slider("duration", "Spin length", 2, 8, 4, 1, unit="s"),
 ),
 canvas("canvas", "The wheel"),
 html_block(""" <div class="display" style="padding:var(--space-6)">
 <span class="display__value" id="result" style="font-size:clamp(1.5rem,1rem+3vw,2.5rem)">, </span>
 <span class="display__label" id="caption">Press Spin</span>
 </div>"""),
 status_line("status", "Add entries and press Spin."),
 buttons(("spin", "Spin", "primary"), ("shuffle", "Shuffle entries"), ("reset", "Restore removed"), ("copy-link", "Copy shareable link"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Results so far</span></span>
 <div class="table-scroll"><div id="history"></div></div>
 </div>"""),
 label="Spin the wheel",
 ),
 info_block=info(
 features=[
 "Unlimited custom segments",
 "Optional weighted odds per entry",
 "Remove-after-spin for elimination draws",
 "Shareable link carrying your entries",
 "Adjustable spin duration",
 ],
 howto=[
 "Type your options, one per line.",
 "Press Spin.",
 "Turn on weights and write “Pizza:3” to triple its odds.",
 "Copy the shareable link to send the same wheel to someone else.",
 ],
 background_title="How the winner is chosen",
 background_paragraphs=[
 "The winner is decided before the animation starts, not by where the wheel happens to stop. The tool draws a cryptographically random index, then calculates the exact rotation needed to land that segment under the pointer and animates to it. This is how essentially every digital wheel works, and it is the honest approach, animating a physical simulation and reading off the result would introduce subtle biases from the easing function and frame timing.",
 "Weighted mode changes the segment sizes proportionally and the selection weights to match, so the visual and the odds always agree. Writing <code>Pizza:3</code> gives Pizza three times the arc and three times the chance. This matters for fairness perception: a wheel where one option is visibly larger but selected uniformly would be actively misleading.",
 "The shareable link encodes your entries in the URL fragment rather than a query string, which means they are never transmitted to any server, the fragment is stripped by the browser before the request is sent. Someone opening your link reconstructs the wheel entirely locally. For long entry lists the URL gets unwieldy, but for a typical decision wheel it stays comfortably within limits.",
 ],
 ),
 script=r""" const canvas = T.$('canvas');
 const ctx = canvas.getContext('2d');

 const COLOURS = ['#00D4FF', '#7B61FF', '#00FF88', '#FF6B35', '#F472B6',
 '#FFD700', '#A855F7', '#06B6D4', '#FB923C', '#34D399'];

 let rotation = 0;
 let spinning = false;
 let removed = [];
 let history = [];

 /** Parse entries, honouring "name:weight" when weighting is on. */
 function segments() {
 const weighted = T.$('weighted').checked;

 return T.$('input').value
 .split(/\r?\n/)
 .map((line) => line.trim())
 .filter(Boolean)
 .map((line) => {
 if (!weighted) return { label: line, weight: 1 };
 const match = line.match(/^(.*):(\d+(?:\.\d+)?)$/);
 return match
 ? { label: match[1].trim(), weight: Math.max(0.1, Number(match[2])) }
 : { label: line, weight: 1 };
 });
 }

 function draw() {
 const list = segments();
 const size = 420;

 canvas.width = size;
 canvas.height = size;
 canvas.style.maxWidth = '100%';
 canvas.style.height = 'auto';

 ctx.clearRect(0, 0, size, size);

 if (!list.length) {
 T.$('canvas-meta').textContent = '';
 return;
 }

 const centre = size / 2;
 const radius = centre - 14;
 const totalWeight = list.reduce((sum, s) => sum + s.weight, 0);

 ctx.save();
 ctx.translate(centre, centre);
 ctx.rotate(rotation);

 let angle = -Math.PI / 2; // start at the top

 list.forEach((segment, index) => {
 const sweep = (segment.weight / totalWeight) * Math.PI * 2;

 ctx.beginPath();
 ctx.moveTo(0, 0);
 ctx.arc(0, 0, radius, angle, angle + sweep);
 ctx.closePath();
 ctx.fillStyle = COLOURS[index % COLOURS.length];
 ctx.fill();
 ctx.strokeStyle = 'rgba(0,0,0.25)';
 ctx.lineWidth = 2;
 ctx.stroke();

 // Label, rotated to sit along the radius
 ctx.save();
 ctx.rotate(angle + sweep / 2);
 ctx.textAlign = 'right';
 ctx.textBaseline = 'middle';
 ctx.fillStyle = '#0B1120';
 ctx.font = `600 ${Math.max(11, Math.min(18, 260 / list.length + 8))}px Inter, sans-serif`;

 const label = segment.label.length > 18
 ? segment.label.slice(0, 17) + '…'
 : segment.label;
 ctx.fillText(label, radius - 16, 0);
 ctx.restore();

 angle += sweep;
 });

 ctx.restore();

 // Hub and pointer, drawn unrotated
 ctx.beginPath();
 ctx.arc(centre, centre, 26, 0, Math.PI * 2);
 ctx.fillStyle = '#0B1120';
 ctx.fill();
 ctx.strokeStyle = '#fff';
 ctx.lineWidth = 3;
 ctx.stroke();

 ctx.beginPath();
 ctx.moveTo(centre - 14, 6);
 ctx.lineTo(centre + 14, 6);
 ctx.lineTo(centre, 38);
 ctx.closePath();
 ctx.fillStyle = '#fff';
 ctx.fill();
 ctx.strokeStyle = '#0B1120';
 ctx.lineWidth = 2;
 ctx.stroke();

 T.$('canvas-meta').textContent =
 `${list.length} segment${list.length === 1 ? '' : 's'}` +
 (T.$('weighted').checked ? ` · total weight ${totalWeight}` : '');
 }

 function spin() {
 if (spinning) return;

 const list = segments();
 if (list.length < 2) {
 T.status('status', 'Add at least two entries.', 'error');
 return;
 }

 // Choose the winner first, then animate to it. Reading the result
 // off the animation would introduce easing bias.
 const totalWeight = list.reduce((sum, s) => sum + s.weight, 0);
 let target = (T.randomBelow(1e9) / 1e9) * totalWeight;
 let winnerIndex = 0;
 let cumulative = 0;

 for (let i = 0; i < list.length; i++) {
 cumulative += list[i].weight;
 if (target <= cumulative) { winnerIndex = i; break; }
 }

 // Angle of the winning segment's centre
 let before = 0;
 for (let i = 0; i < winnerIndex; i++) before += list[i].weight;
 const segmentCentre = ((before + list[winnerIndex].weight / 2) / totalWeight) * Math.PI * 2;

 // Rotate so that centre ends up under the pointer at the top
 const spins = 5 + T.randomBelow(3);
 const targetRotation = spins * Math.PI * 2 - segmentCentre;

 spinning = true;
 T.$('spin').disabled = true;
 T.$('caption').textContent = 'Spinning…';

 const duration = Number(T.$('duration').value) * 1000;
 const startRotation = rotation % (Math.PI * 2);
 const startTime = performance.now();

 const animate = (now) => {
 const progress = Math.min((now - startTime) / duration, 1);
 // easeOutQuart gives a convincing slow-down
 const eased = 1 - Math.pow(1 - progress, 4);

 rotation = startRotation + (targetRotation - startRotation) * eased;
 draw();

 if (progress < 1) {
 requestAnimationFrame(animate);
 } else {
 spinning = false;
 T.$('spin').disabled = false;
 announce(list[winnerIndex].label, list.length);
 }
 };

 requestAnimationFrame(animate);
 }

 function announce(label, poolSize) {
 T.$('result').textContent = label;
 T.$('caption').textContent = `Chosen from ${poolSize} options`;

 history.unshift({ at: Date.now(), label, poolSize });
 history = history.slice(0, 20);
 renderHistory();

 if (T.$('remove').checked) {
 const remaining = T.$('input').value
 .split(/\r?\n/)
 .filter((line) => {
 const name = T.$('weighted').checked
 ? line.replace(/:(\d+(?:\.\d+)?)\s*$/, '').trim()
 : line.trim();
 return name !== label;
 });

 removed.push(label);
 T.$('input').value = remaining.join('\n');
 draw();
 updateStats();
 }

 T.status('status', `The wheel chose ${label}.`, 'ok');
 if (window.Analytics) Analytics.trackToolUse('spin-the-wheel');
 }

 function renderHistory() {
 const mount = T.$('history');
 mount.innerHTML = '';
 if (!history.length) return;

 mount.append(T.table(
 ['Time', 'Result', 'Options'],
 history.map((h) => [
 new Date(h.at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
 h.label,
 h.poolSize
 ])
 ));
 }

 function updateStats() {
 const count = segments().length;
 T.$('input-stats').textContent = count ? `${count} entries` : '';
 }

 T.$('spin').addEventListener('click', spin);

 T.$('input').addEventListener('input', debounce(() => { draw(); updateStats(); }, 250));
 T.on(['weighted', 'remove'], () => { draw(); updateStats(); }, 'change');
 T.$('duration').addEventListener('input', () => {
 T.$('duration-value').textContent = T.$('duration').value;
 });

 T.$('shuffle').addEventListener('click', () => {
 const lines = T.$('input').value.split(/\r?\n/).filter((l) => l.trim());
 T.$('input').value = T.shuffle(lines).join('\n');
 draw();
 });

 T.$('reset').addEventListener('click', () => {
 if (!removed.length) {
 T.status('status', 'Nothing has been removed.', 'muted');
 return;
 }
 T.$('input').value = (T.$('input').value.trim() + '\n' + removed.join('\n')).trim();
 removed = [];
 draw();
 updateStats();
 T.status('status', 'Restored removed entries.', 'ok');
 });

 T.$('copy-link').addEventListener('click', () => {
 const entries = segments().map((s) => s.label).join('|');
 // A fragment is never sent to the server, so entries stay private
 const url = `${location.origin}${location.pathname}#w=${encodeURIComponent(entries)}`;
 copyToClipboard(url, 'Shareable link copied');
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Spin the Wheel | 123MiniApps' }));

 // Restore a shared wheel
 (function restore() {
 const match = location.hash.match(/w=([^&]+)/);
 if (!match) return;
 const entries = decodeURIComponent(match[1]).split('|').filter(Boolean);
 if (entries.length >= 2) {
 T.$('input').value = entries.join('\n');
 T.status('status', 'Loaded a shared wheel from the link.', 'ok');
 }
 })();

 draw();
 updateStats();""",
))

# ---------------------------------------------------------------
# 94. Password Game
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="password-game", name="Password Game", icon="🎮", cat="fun",
 title="Password Game: Learn What Makes a Password Strong",
 description="A playful challenge with escalating rules that teaches what actually makes a password strong, and what security theatre looks like.",
 tagline="An escalating-rules challenge that teaches what actually makes a password strong.",
 workspace=ws(
 html_block(""" <div class="field">
 <label class="field__label" for="password">
 <span>Your password</span>
 <span class="field__hint" id="length-hint"></span>
 </label>
 <input class="input font-mono" id="password" type="text" autocomplete="off"
 spellcheck="false" placeholder="Start typing…"
 style="font-size:var(--text-lg);height:56px">
 </div>"""),
 html_block(""" <div class="result-grid">
 <div class="result result--primary"><span class="result__value" id="r-level" style="font-size:var(--text-3xl)">1</span><span class="result__label">Level reached</span></div>
 <div class="result"><span class="result__value" id="r-passed" style="font-size:var(--text-3xl)">0</span><span class="result__label">Rules satisfied</span></div>
 <div class="result"><span class="result__value" id="r-best" style="font-size:var(--text-3xl)">0</span><span class="result__label">Best level</span></div>
 </div>"""),
 status_line("status", "Start typing to reveal the first rule."),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Rules</span><span class="field__hint">A new one appears each time you satisfy them all</span></span>
 <div id="rules"></div>
 </div>"""),
 buttons(("reset", "Start over", "secondary"), ("reveal", "Show all rules"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="info-panel">
 <strong class="text-sm">The point of this game</strong>
 <p class="text-sm text-muted mt-2" id="lesson">
 Several of these rules are the kind real websites impose, and several of them make passwords
 measurably <em>weaker</em>. Watch which ones frustrate you, then read the notes below.
 </p>
 </div>"""),
 label="Password game",
 ),
 info_block=info(
 features=[
 "Twelve escalating rules",
 "Live validation as you type",
 "Best-level tracking saved on your device",
 "Explains which rules are genuinely useful",
 "Nothing is transmitted or stored beyond your best score",
 ],
 howto=[
 "Start typing to reveal the first rule.",
 "Satisfy every visible rule to unlock the next.",
 "Notice which rules make the password worse.",
 "Read the notes below when you get stuck.",
 ],
 background_title="Which of these rules are real security",
 background_paragraphs=[
 "Composition rules, requiring an uppercase letter, a digit and a symbol, are the classic example of security theatre. NIST formally recommended against them in Special Publication 800-63B, because they produce predictable results: told to add a capital and a number, people overwhelmingly produce <code>Password1!</code>. The rule adds almost no entropy while making passwords harder to remember, which pushes people toward reuse and writing them down.",
 "Length is the rule that genuinely works, and it works better than everything else combined. Each additional character multiplies the search space, so a long passphrase of common words beats a short string of symbols by an enormous margin. NIST's current guidance is to require a minimum of 8 characters, permit at least 64, allow all printable characters including spaces, and impose no composition rules at all.",
 "Two more real measures. Checking new passwords against lists of known breached credentials catches the passwords attackers actually try first, which no composition rule does. And forced periodic expiry, the 90-day rotation policy many organisations still run, was also withdrawn by NIST, because it drives predictable incrementing (<code>Spring2024</code>, then <code>Summer2024</code>) and offers no benefit unless there is evidence of compromise. If a site imposes rules like the sillier ones in this game, that tells you something about how much thought went into the rest of its security.",
 ],
 ),
 script=r""" const RULES = [
 {
 id: 1,
 text: 'Your password must be at least 8 characters long.',
 test: (p) => p.length >= 8,
 real: true,
 note: 'Genuinely useful. Length is the single biggest factor in password strength.'
 },
 {
 id: 2,
 text: 'Your password must include a number.',
 test: (p) => /\d/.test(p),
 real: false,
 note: 'Security theatre. NIST recommends against composition rules, most people just append a 1.'
 },
 {
 id: 3,
 text: 'Your password must include an uppercase letter.',
 test: (p) => /[A-Z]/.test(p),
 real: false,
 note: 'Also theatre. Almost everyone capitalises the first letter, which attackers know.'
 },
 {
 id: 4,
 text: 'Your password must include a special character.',
 test: (p) => /[^a-zA-Z0-9]/.test(p),
 real: false,
 note: 'Theatre again. The overwhelmingly common choice is a trailing exclamation mark.'
 },
 {
 id: 5,
 text: 'Your password must be at least 16 characters long.',
 test: (p) => p.length >= 16,
 real: true,
 note: 'This is the rule that actually matters. Sixteen characters is a meaningful bar.'
 },
 {
 id: 6,
 text: 'Your password must not contain the word "password".',
 test: (p) => !/pass\W*w[o0]rd/i.test(p),
 real: true,
 note: 'Reasonable. Blocking known-terrible passwords is genuinely effective.'
 },
 {
 id: 7,
 text: 'The digits in your password must add up to exactly 25.',
 test: (p) => {
 const digits = (p.match(/\d/g) || []).map(Number);
 return digits.length > 0 && digits.reduce((a, b) => a + b, 0) === 25;
 },
 real: false,
 note: 'Absurd, obviously. But it is not far from rules that ban repeated characters or sequences.'
 },
 {
 id: 8,
 text: 'Your password must contain a month of the year.',
 test: (p) => /jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec/i.test(p),
 real: false,
 note: 'Actively harmful, it forces a dictionary word into every password on the system.'
 },
 {
 id: 9,
 text: 'Your password must not contain three identical characters in a row.',
 test: (p) => !/(.)\1\1/.test(p),
 real: true,
 note: 'Mildly useful. Long runs of one character add length without adding real entropy.'
 },
 {
 id: 10,
 text: 'Your password must contain a Roman numeral.',
 test: (p) => /[IVXLCDM]/.test(p),
 real: false,
 note: 'Nonsense, and it is satisfied by any uppercase I, V, X, L, C, D or M, including the one rule 3 made you add.'
 },
 {
 id: 11,
 text: 'Your password must be at least 24 characters long.',
 test: (p) => p.length >= 24,
 real: true,
 note: 'By now you have probably given up on memorising this, which is exactly the problem.'
 },
 {
 id: 12,
 text: 'Your password must contain a space.',
 test: (p) => /\s/.test(p),
 real: true,
 note: 'Genuinely good, and many sites wrongly forbid it. NIST says all printable characters, including spaces, should be allowed.'
 }
 ];

 let unlocked = 1;
 let revealAll = false;
 let best = T.store.get('password-game-best', 0);

 function evaluate() {
 const password = T.$('password').value;
 T.$('length-hint').textContent = password ? `${password.length} characters` : '';

 if (!password) {
 unlocked = 1;
 render(password);
 T.status('status', 'Start typing to reveal the first rule.', 'muted');
 return;
 }

 // Unlock the next rule once everything visible passes
 const visible = revealAll ? RULES.length : unlocked;
 const allPass = RULES.slice(0, visible).every((rule) => rule.test(password));

 if (allPass && unlocked < RULES.length && !revealAll) {
 unlocked++;
 toast({
 type: 'success',
 title: `Level ${unlocked}`,
 message: 'A new rule has appeared.',
 duration: 2500
 });
 }

 if (unlocked > best) {
 best = unlocked;
 T.store.set('password-game-best', best);
 }

 render(password);
 }

 function render(password) {
 const visible = revealAll ? RULES.length : unlocked;
 const shown = RULES.slice(0, visible);
 const passed = shown.filter((rule) => rule.test(password)).length;

 T.$('r-level').textContent = String(unlocked);
 T.$('r-passed').textContent = `${passed} / ${shown.length}`;
 T.$('r-best').textContent = String(best);

 const mount = T.$('rules');
 mount.innerHTML = '';

 // Newest rule first, it is the one the player is working on
 [...shown].reverse().forEach((rule) => {
 const ok = rule.test(password);

 const panel = el('div', {
 className: 'info-panel mb-2',
 style: {
 borderLeftWidth: '3px',
 borderLeftColor: ok ? 'var(--success)' : 'var(--danger)'
 }
 }, [
 el('div', { className: 'flex items-start gap-3' }, [
 el('span', {
 text: ok ? '✓' : '✗',
 style: {
 color: ok ? 'var(--success)' : 'var(--danger)',
 fontWeight: '700',
 fontSize: 'var(--text-lg)',
 flexShrink: '0'
 }
 }),
 el('div', {}, [
 el('div', { className: 'text-sm', text: `Rule ${rule.id}: ${rule.text}` }),
 ok ? el('div', {
 className: 'text-xs text-muted mt-2',
 text: (rule.real ? '✔ Real security: ' : '✘ Security theatre: ') + rule.note
 }) : null
 ])
 ])
 ]);

 mount.append(panel);
 });

 if (passed === RULES.length) {
 T.status('status',
 'You satisfied all twelve. Note how little of that difficulty made the password stronger.',
 'ok');
 T.$('lesson').innerHTML =
 'You made it. Of the twelve rules, only five (1, 5, 6, 9, 11 and 12) reflect real security ' +
 'guidance, and the ones that mattered were almost entirely about <strong>length</strong>. ' +
 'The rest are the kind of composition requirements NIST explicitly recommends against, ' +
 'because they make passwords harder to remember without making them meaningfully harder to guess.';
 } else if (password) {
 T.status('status', `${passed} of ${shown.length} rules satisfied.`, passed === shown.length ? 'ok' : 'warn');
 }

 if (window.Analytics) Analytics.trackToolUse('password-game');
 }

 T.$('password').addEventListener('input', debounce(evaluate, 150));

 T.$('reset').addEventListener('click', () => {
 T.$('password').value = '';
 unlocked = 1;
 revealAll = false;
 evaluate();
 T.$('password').focus();
 });

 T.$('reveal').addEventListener('click', () => {
 revealAll = !revealAll;
 T.$('reveal').textContent = revealAll ? 'Hide later rules' : 'Show all rules';
 render(T.$('password').value);
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Password Game | 123MiniApps' }));

 evaluate();""",
))

# ---------------------------------------------------------------
# 95. Emoji Picker
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="emoji-picker", name="Emoji Picker", icon="😀", cat="fun",
 title="Emoji Picker: Search and Copy Emoji by Name",
 description="Search hundreds of emoji by name or keyword, browse by category, and copy with one click. Recently used emoji are remembered on your device.",
 tagline="Search emoji by name and copy with one click, recents remembered locally.",
 workspace=ws(
 html_block(""" <div class="searchbar" style="max-width:none;margin-bottom:var(--space-5)">
 <label class="sr-only" for="search">Search emoji</label>
 <div class="searchbar__field">
 <span class="searchbar__icon" aria-hidden="true">
 <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
 </span>
 <input class="searchbar__input" id="search" type="search"
 placeholder="Search by name, try heart, cat, party or thumbs" autocomplete="off">
 </div>
 </div>"""),
 html_block(""" <div class="chip-grid" id="categories" style="margin-bottom:var(--space-5)"></div>"""),
 html_block(""" <div class="field" id="recent-field" hidden>
 <span class="field__label"><span>Recently used</span><span class="field__hint">Stored on this device</span></span>
 <div id="recent" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(52px,1fr));gap:var(--space-2)"></div>
 </div>"""),
 status_line("status", ""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Emoji</span><span class="field__hint">Click to copy</span></span>
 <div id="grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(52px,1fr));gap:var(--space-2)"></div>
 </div>"""),
 html_block(""" <div class="field">
 <label class="field__label" for="basket"><span>Collected emoji</span><span class="field__hint">Shift-click any emoji to add it here</span></label>
 <input class="input" id="basket" type="text" readonly style="font-size:var(--text-xl);height:56px">
 </div>"""),
 buttons(("copy-basket", "Copy collected", "primary"), ("clear-basket", "Clear collected"), ("clear-recent", "Clear recents", "ghost"), ("share", "Share tool", "ghost")),
 label="Emoji picker",
 ),
 info_block=info(
 features=[
 "Search by name and keyword",
 "Eight categories",
 "Recently used emoji remembered on your device",
 "Shift-click to collect several at once",
 "One-click copy",
 ],
 howto=[
 "Type a word to search, or pick a category.",
 "Click an emoji to copy it.",
 "Shift-click to collect several, then copy them together.",
 "Recents build up as you use it.",
 ],
 background_title="How emoji actually work",
 background_paragraphs=[
 "Emoji are Unicode characters, not images, which is why they can be typed, searched and copied like any other text. Each has a code point, the grinning face is U+1F600, and it is the font on your device that decides what it looks like. That is why the same emoji appears different on iOS, Android and Windows, and why an emoji occasionally shows as a hollow box: your system has the character but no glyph for it.",
 "Many emoji are not single characters at all. Skin-tone variants combine a base emoji with a modifier; the family emoji are sequences of person emoji joined by zero-width joiners; flags are pairs of regional indicator letters. This is why deleting one emoji sometimes takes several backspaces, and why naive string handling can tear a family emoji into its component people.",
 "Support depends on the Unicode version your device has. New emoji are approved annually and take months to reach devices, so a recently added one may render on your phone but not on a colleague's older laptop. The set here sticks to widely supported emoji from established Unicode versions for that reason. If something shows as a box, it is your font, not the page.",
 ],
 ),
 script=r""" const EMOJI = {
 'Smileys': [
 ['😀', 'grinning face happy smile'], ['😃', 'grinning big eyes happy'],
 ['😄', 'grinning smiling eyes laugh'], ['😁', 'beaming grin smile'],
 ['😆', 'laughing squinting haha'], ['😅', 'sweat smile nervous laugh'],
 ['🤣', 'rolling floor laughing rofl'], ['😂', 'tears of joy crying laughing'],
 ['🙂', 'slightly smiling face'], ['🙃', 'upside down sarcasm'],
 ['😉', 'winking wink'], ['😊', 'smiling blush happy'],
 ['😇', 'halo angel innocent'], ['🥰', 'smiling hearts love adore'],
 ['😍', 'heart eyes love'], ['🤩', 'star struck excited amazed'],
 ['😘', 'blowing kiss love'], ['😗', 'kissing'],
 ['😋', 'savouring delicious yum tongue'], ['😛', 'tongue out playful'],
 ['🤪', 'zany crazy silly'], ['🤔', 'thinking hmm consider'],
 ['🤨', 'raised eyebrow sceptical doubt'], ['😐', 'neutral face blank'],
 ['😑', 'expressionless unimpressed'], ['🙄', 'rolling eyes annoyed'],
 ['😏', 'smirking smug'], ['😴', 'sleeping zzz tired'],
 ['🤤', 'drooling'], ['😪', 'sleepy tired'],
 ['😵', 'dizzy knocked out'], ['🤐', 'zipper mouth quiet secret'],
 ['🥴', 'woozy drunk'], ['🤢', 'nauseated sick'],
 ['🤧', 'sneezing ill'], ['😷', 'medical mask sick'],
 ['🤒', 'thermometer ill fever'], ['😎', 'sunglasses cool'],
 ['🤓', 'nerd glasses geek'], ['🧐', 'monocle inspect'],
 ['😕', 'confused unsure'], ['😟', 'worried concerned'],
 ['🙁', 'frowning sad'], ['😯', 'hushed surprised'],
 ['😲', 'astonished shocked'], ['😳', 'flushed embarrassed'],
 ['🥺', 'pleading begging puppy eyes'], ['😢', 'crying sad tear'],
 ['😭', 'sobbing crying loudly'], ['😱', 'screaming fear scared'],
 ['😖', 'confounded frustrated'], ['😣', 'persevering struggling'],
 ['😞', 'disappointed sad'], ['😤', 'triumph steam angry'],
 ['😠', 'angry mad'], ['😡', 'pouting rage furious'],
 ['🤬', 'cursing swearing symbols'], ['😈', 'smiling devil mischief'],
 ['💀', 'skull dead'], ['👻', 'ghost boo halloween'],
 ['👽', 'alien extraterrestrial'], ['🤖', 'robot bot'],
 ['🎃', 'jack o lantern pumpkin halloween'], ['😺', 'grinning cat'],
 ['😻', 'heart eyes cat love'], ['🙈', 'see no evil monkey'],
 ['🙉', 'hear no evil monkey'], ['🙊', 'speak no evil monkey']
 ],
 'Gestures': [
 ['👋', 'waving hand hello bye'], ['🤚', 'raised back of hand'],
 ['✋', 'raised hand stop'], ['🖖', 'vulcan salute spock'],
 ['👌', 'ok hand perfect'], ['🤌', 'pinched fingers italian'],
 ['✌️', 'victory peace'], ['🤞', 'crossed fingers luck hope'],
 ['🤟', 'love you gesture'], ['🤘', 'horns rock metal'],
 ['👈', 'pointing left'], ['👉', 'pointing right'],
 ['👆', 'pointing up'], ['👇', 'pointing down'],
 ['☝️', 'index up one'], ['👍', 'thumbs up like yes good approve'],
 ['👎', 'thumbs down dislike no bad'], ['✊', 'raised fist power'],
 ['👊', 'fist bump punch'], ['👏', 'clapping applause bravo'],
 ['🙌', 'raising hands celebration praise'], ['🤝', 'handshake deal agreement'],
 ['🙏', 'folded hands please thanks pray'], ['💪', 'flexed biceps strong muscle'],
 ['✍️', 'writing hand'], ['🤳', 'selfie']
 ],
 'People': [
 ['👶', 'baby infant'], ['🧒', 'child'], ['👦', 'boy'], ['👧', 'girl'],
 ['🧑', 'person adult'], ['👨', 'man'], ['👩', 'woman'],
 ['🧔', 'person beard'], ['👴', 'old man elderly'], ['👵', 'old woman elderly'],
 ['👮', 'police officer'], ['👷', 'construction worker'],
 ['💂', 'guard'], ['🕵️', 'detective spy investigate'],
 ['👨‍⚕️', 'doctor health'], ['👩‍🏫', 'teacher school'],
 ['👨‍💻', 'technologist developer programmer'], ['👩‍🔬', 'scientist research'],
 ['👨‍🍳', 'cook chef'], ['🧑‍🚀', 'astronaut space'],
 ['🤵', 'person in tuxedo'], ['👰', 'person with veil wedding'],
 ['🤰', 'pregnant'], ['🎅', 'santa christmas'],
 ['🧙', 'mage wizard'], ['🧚', 'fairy'], ['🦸', 'superhero'], ['🦹', 'supervillain']
 ],
 'Animals': [
 ['🐶', 'dog puppy'], ['🐱', 'cat kitten'], ['🐭', 'mouse'],
 ['🐹', 'hamster'], ['🐰', 'rabbit bunny'], ['🦊', 'fox'],
 ['🐻', 'bear'], ['🐼', 'panda'], ['🐨', 'koala'],
 ['🐯', 'tiger'], ['🦁', 'lion'], ['🐮', 'cow'],
 ['🐷', 'pig'], ['🐸', 'frog'], ['🐵', 'monkey'],
 ['🐔', 'chicken'], ['🐧', 'penguin'], ['🐦', 'bird'],
 ['🦆', 'duck'], ['🦅', 'eagle'], ['🦉', 'owl'],
 ['🦇', 'bat'], ['🐺', 'wolf'], ['🐗', 'boar'],
 ['🐴', 'horse'], ['🦄', 'unicorn'], ['🐝', 'bee honeybee'],
 ['🐛', 'bug caterpillar'], ['🦋', 'butterfly'], ['🐌', 'snail'],
 ['🐞', 'ladybird beetle'], ['🐜', 'ant'], ['🕷️', 'spider'],
 ['🐢', 'turtle tortoise'], ['🐍', 'snake'], ['🦎', 'lizard'],
 ['🐙', 'octopus'], ['🦑', 'squid'], ['🦐', 'shrimp'],
 ['🐠', 'tropical fish'], ['🐟', 'fish'], ['🐬', 'dolphin'],
 ['🐳', 'whale'], ['🦈', 'shark'], ['🐊', 'crocodile'],
 ['🐘', 'elephant'], ['🦒', 'giraffe'], ['🦓', 'zebra']
 ],
 'Food': [
 ['🍏', 'green apple'], ['🍎', 'red apple'], ['🍐', 'pear'],
 ['🍊', 'orange tangerine'], ['🍋', 'lemon'], ['🍌', 'banana'],
 ['🍉', 'watermelon'], ['🍇', 'grapes'], ['🍓', 'strawberry'],
 ['🫐', 'blueberries'], ['🍒', 'cherries'], ['🍑', 'peach'],
 ['🥭', 'mango'], ['🍍', 'pineapple'], ['🥥', 'coconut'],
 ['🥝', 'kiwi'], ['🍅', 'tomato'], ['🥑', 'avocado'],
 ['🥦', 'broccoli'], ['🥕', 'carrot'], ['🌽', 'corn'],
 ['🥔', 'potato'], ['🍞', 'bread'], ['🥐', 'croissant'],
 ['🧀', 'cheese'], ['🥚', 'egg'], ['🥓', 'bacon'],
 ['🍔', 'hamburger burger'], ['🍟', 'chips fries'], ['🍕', 'pizza'],
 ['🌭', 'hot dog'], ['🌮', 'taco'], ['🌯', 'burrito'],
 ['🥗', 'salad'], ['🍝', 'spaghetti pasta'], ['🍜', 'ramen noodles'],
 ['🍣', 'sushi'], ['🍤', 'fried shrimp tempura'], ['🍚', 'rice'],
 ['🍦', 'ice cream'], ['🍰', 'cake slice'], ['🎂', 'birthday cake'],
 ['🍪', 'cookie biscuit'], ['🍫', 'chocolate'], ['🍬', 'sweet candy'],
 ['☕', 'coffee hot drink tea'], ['🍵', 'green tea'], ['🍺', 'beer'],
 ['🍷', 'wine'], ['🥂', 'clinking glasses cheers'], ['🍾', 'champagne celebrate']
 ],
 'Objects': [
 ['⌚', 'watch time'], ['📱', 'mobile phone'], ['💻', 'laptop computer'],
 ['⌨️', 'keyboard'], ['🖥️', 'desktop computer'], ['🖨️', 'printer'],
 ['🖱️', 'mouse computer'], ['💾', 'floppy disk save'], ['💿', 'cd disc'],
 ['📷', 'camera photo'], ['📹', 'video camera'], ['🎥', 'movie camera film'],
 ['📞', 'telephone call'], ['📺', 'television tv'], ['📻', 'radio'],
 ['🎙️', 'microphone podcast'], ['⏰', 'alarm clock'], ['⏳', 'hourglass time'],
 ['🔋', 'battery'], ['🔌', 'plug electric'], ['💡', 'light bulb idea'],
 ['🔦', 'torch flashlight'], ['📚', 'books'], ['📖', 'open book'],
 ['📝', 'memo note writing'], ['📌', 'pushpin'], ['📎', 'paperclip'],
 ['✂️', 'scissors cut'], ['🔒', 'locked secure'], ['🔓', 'unlocked'],
 ['🔑', 'key'], ['🔨', 'hammer'], ['🔧', 'wrench spanner'],
 ['⚙️', 'gear settings cog'], ['🧲', 'magnet'], ['💊', 'pill medicine'],
 ['🩺', 'stethoscope'], ['💰', 'money bag'], ['💳', 'credit card'],
 ['📦', 'package box parcel'], ['✉️', 'envelope email'], ['📮', 'postbox']
 ],
 'Symbols': [
 ['❤️', 'red heart love'], ['🧡', 'orange heart'], ['💛', 'yellow heart'],
 ['💚', 'green heart'], ['💙', 'blue heart'], ['💜', 'purple heart'],
 ['🖤', 'black heart'], ['🤍', 'white heart'], ['💔', 'broken heart'],
 ['💕', 'two hearts'], ['💖', 'sparkling heart'], ['💯', 'hundred points perfect'],
 ['💢', 'anger symbol'], ['💥', 'collision boom'], ['💫', 'dizzy star'],
 ['💦', 'sweat droplets water'], ['🔥', 'fire lit hot'], ['⭐', 'star'],
 ['🌟', 'glowing star'], ['✨', 'sparkles'], ['⚡', 'high voltage lightning'],
 ['☀️', 'sun sunny'], ['🌙', 'crescent moon night'], ['☁️', 'cloud'],
 ['🌈', 'rainbow'], ['❄️', 'snowflake cold'], ['✅', 'check mark tick done'],
 ['❌', 'cross mark no wrong'], ['⚠️', 'warning caution'], ['❓', 'question mark'],
 ['❗', 'exclamation mark'], ['♻️', 'recycling'], ['🔔', 'bell notification'],
 ['🔕', 'muted bell'], ['🎵', 'musical note'], ['🚫', 'prohibited no entry']
 ],
 'Activities': [
 ['⚽', 'football soccer'], ['🏀', 'basketball'], ['🏈', 'american football'],
 ['⚾', 'baseball'], ['🎾', 'tennis'], ['🏐', 'volleyball'],
 ['🏉', 'rugby'], ['🎱', 'pool billiards eight ball'], ['🏓', 'table tennis ping pong'],
 ['🏸', 'badminton'], ['🥊', 'boxing glove'], ['⛳', 'golf'],
 ['🎣', 'fishing'], ['🎿', 'ski'], ['🏂', 'snowboard'],
 ['🏊', 'swimming'], ['🚴', 'cycling bike'], ['🏃', 'running'],
 ['🎯', 'target bullseye dart'], ['🎮', 'video game controller'], ['🕹️', 'joystick'],
 ['🎲', 'dice game'], ['🧩', 'jigsaw puzzle'], ['🎨', 'artist palette art'],
 ['🎭', 'performing arts theatre'], ['🎪', 'circus tent'], ['🎬', 'clapper board film'],
 ['🎤', 'microphone singing karaoke'], ['🎧', 'headphones music'], ['🎸', 'guitar'],
 ['🎹', 'piano keyboard'], ['🥁', 'drum'], ['🏆', 'trophy winner'],
 ['🥇', 'gold medal first'], ['🎉', 'party popper celebration'], ['🎊', 'confetti ball']
 ]
 };

 const ALL = Object.entries(EMOJI).flatMap(([category, list]) =>
 list.map(([emoji, keywords]) => ({ emoji, keywords, category })));

 let activeCategory = 'all';
 let recent = T.store.get('emoji-recent', []);
 let basket = [];

 function visible() {
 const query = T.$('search').value.trim().toLowerCase();

 return ALL.filter((item) => {
 if (activeCategory !== 'all' && item.category !== activeCategory) return false;
 if (!query) return true;
 return item.keywords.includes(query) || item.emoji === query;
 });
 }

 function emojiButton(emoji, keywords) {
 const button = el('button', {
 attrs: {
 type: 'button',
 title: keywords || emoji,
 'aria-label': `Copy ${keywords || emoji}`
 },
 text: emoji,
 style: {
 fontSize: '28px', lineHeight: '1', padding: 'var(--space-2)',
 background: 'var(--bg-surface)', border: '1px solid var(--border-color)',
 borderRadius: 'var(--radius-sm)', cursor: 'pointer', aspectRatio: '1'
 }
 });

 button.addEventListener('click', (e) => {
 if (e.shiftKey) {
 basket.push(emoji);
 T.$('basket').value = basket.join('');
 T.status('status', `${basket.length} emoji collected.`, 'ok');
 } else {
 copyToClipboard(emoji, `${emoji} copied`);
 }

 recent = [emoji, ...recent.filter((r) => r !== emoji)].slice(0, 24);
 T.store.set('emoji-recent', recent);
 renderRecent();

 if (window.Analytics) Analytics.trackToolUse('emoji-picker');
 });

 return button;
 }

 function render() {
 const mount = T.$('grid');
 mount.innerHTML = '';

 const list = visible();

 if (!list.length) {
 mount.innerHTML = '';
 mount.append(el('div', {
 className: 'empty-state',
 style: { gridColumn: '1 / -1' }
 }, [
 el('div', { className: 'empty-state__icon', text: '🔍', attrs: { 'aria-hidden': 'true' } }),
 el('p', { text: 'No emoji match that search.' })
 ]));
 T.status('status', 'No matches.', 'warn');
 return;
 }

 list.forEach((item) => mount.append(emojiButton(item.emoji, item.keywords)));
 T.status('status', `Showing ${list.length} of ${ALL.length} emoji.`, 'ok');
 }

 function renderRecent() {
 const field = T.$('recent-field');
 const mount = T.$('recent');
 mount.innerHTML = '';

 if (!recent.length) {
 field.hidden = true;
 return;
 }

 field.hidden = false;
 recent.forEach((emoji) => {
 const found = ALL.find((item) => item.emoji === emoji);
 mount.append(emojiButton(emoji, found ? found.keywords : ''));
 });
 }

 function renderCategories() {
 const mount = T.$('categories');
 mount.innerHTML = '';

 [['all', 'All'], ...Object.keys(EMOJI).map((c) => [c, c])].forEach(([key, label]) => {
 const chip = el('button', { className: 'chip', attrs: { type: 'button' }, text: label });

 if (key === activeCategory) {
 chip.style.borderColor = 'var(--accent-primary)';
 chip.style.color = 'var(--accent-primary)';
 }

 chip.addEventListener('click', () => {
 activeCategory = key;
 renderCategories();
 render();
 });

 mount.append(chip);
 });
 }

 T.$('search').addEventListener('input', debounce(render, 150));

 T.$('copy-basket').addEventListener('click', () => {
 if (!basket.length) { toast({ type: 'warning', title: 'Nothing collected yet', message: 'Shift-click emoji to collect them.' }); return; }
 copyToClipboard(basket.join(''), 'Collected emoji copied');
 });

 T.$('clear-basket').addEventListener('click', () => {
 basket = [];
 T.$('basket').value = '';
 T.status('status', 'Collection cleared.', 'muted');
 });

 T.$('clear-recent').addEventListener('click', () => {
 recent = [];
 T.store.set('emoji-recent', recent);
 renderRecent();
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Emoji Picker | 123MiniApps' }));

 renderCategories();
 renderRecent();
 render();""",
))
