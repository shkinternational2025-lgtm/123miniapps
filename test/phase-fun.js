/* ============================================
   123MiniApps.online v2.0
   File: test/phase-fun.js
   Purpose: Behavioural tests for the 6 fun tools.

   Fairness matters here — these tools get used for
   real draws, so the distribution tests are not
   decorative.
   ============================================ */

const { boot, Suite, set, click, text, val, wait } = require('./harness');

module.exports = async function run() {
  const s = new Suite('Fun tools');

  /* ---------- Random Picker ---------- */
  {
    const { window: w, errors } = await boot('tools/random-picker.html');

    set(w, 'input', 'Alice\nBob\nCharlie\nDiana');
    set(w, 'winners', '1');
    set(w, 'animate', false, 'change');
    set(w, 'remove', false, 'change');
    await wait(300);
    s.match('picker: counts entries', text(w, 'input-stats'), /4 entries/);

    click(w, 'pick');
    await wait(200);
    s.check('picker: picked a real entry',
      ['Alice', 'Bob', 'Charlie', 'Diana'].includes(text(w, 'result')), text(w, 'result'));

    // Fairness: 800 draws over 4 entries should be roughly even
    const counts = {};
    for (let i = 0; i < 800; i++) {
      click(w, 'pick');
      const winner = text(w, 'result');
      counts[winner] = (counts[winner] || 0) + 1;
    }
    const values = Object.values(counts);
    s.eq('picker: all four entries appear', Object.keys(counts).length, 4);
    s.check('picker: distribution roughly uniform over 800 draws',
      Math.min(...values) > 140 && Math.max(...values) < 270,
      JSON.stringify(counts));

    // Multiple winners must be distinct
    set(w, 'winners', '3');
    click(w, 'pick');
    await wait(200);
    const winners = text(w, 'result').split(', ');
    s.eq('picker: three winners returned', winners.length, 3);
    s.eq('picker: winners are distinct', new Set(winners).size, 3);

    // Asking for more than available is rejected
    set(w, 'winners', '10');
    click(w, 'pick');
    await wait(200);
    s.match('picker: too many winners rejected', text(w, 'status'), /only 4 entries/i);

    // Remove-after-pick
    set(w, 'winners', '1');
    set(w, 'remove', true, 'change');
    click(w, 'pick');
    await wait(250);
    s.match('picker: entry removed', text(w, 'input-stats'), /3 entries/);

    click(w, 'reset');
    await wait(250);
    s.match('picker: restore brings it back', text(w, 'input-stats'), /4 entries/);

    // Empty list
    set(w, 'input', '');
    await wait(250);
    click(w, 'pick');
    await wait(200);
    s.match('picker: empty list rejected', text(w, 'status'), /add some entries/i);
    s.noErrors(errors);
  }

  /* ---------- Dice Roller ---------- */
  {
    const { window: w, errors } = await boot('tools/dice-roller.html');

    set(w, 'notation', '1d6');
    set(w, 'mode', 'normal', 'change');
    set(w, 'explode', false, 'change');
    await wait(200);

    // 600 rolls of 1d6 — every face should appear, roughly evenly
    const faces = {};
    for (let i = 0; i < 600; i++) {
      click(w, 'roll');
      const value = Number(text(w, 'total'));
      faces[value] = (faces[value] || 0) + 1;
    }
    s.eq('dice: d6 produces exactly six faces', Object.keys(faces).length, 6);
    s.check('dice: all results within 1-6',
      Object.keys(faces).every((v) => Number(v) >= 1 && Number(v) <= 6));
    s.check('dice: d6 roughly uniform',
      Math.min(...Object.values(faces)) > 60 && Math.max(...Object.values(faces)) < 145,
      JSON.stringify(faces));

    // Modifiers
    set(w, 'notation', '1d1+10');
    click(w, 'roll');
    await wait(150);
    s.eq('dice: modifier applied', text(w, 'total'), '11');

    // Multiple dice
    set(w, 'notation', '3d1');
    click(w, 'roll');
    await wait(150);
    s.eq('dice: 3d1 sums to 3', text(w, 'total'), '3');

    // Keep-highest
    set(w, 'notation', '4d6kh3');
    click(w, 'roll');
    await wait(150);
    const total = Number(text(w, 'total'));
    s.check('dice: 4d6kh3 within 3-18', total >= 3 && total <= 18, String(total));
    s.includes('dice: shows dropped die', text(w, 'breakdown'), 'dropped');

    // Invalid notation
    set(w, 'notation', 'not dice');
    click(w, 'roll');
    await wait(150);
    s.match('dice: invalid notation rejected', text(w, 'status'), /could not read/i);

    // Advantage rolls twice
    set(w, 'notation', '1d20');
    set(w, 'mode', 'advantage', 'change');
    click(w, 'roll');
    await wait(150);
    s.includes('dice: advantage shows both rolls', text(w, 'breakdown'), 'advantage:');

    s.check('dice: history renders', w.document.querySelector('#history table') !== null);
    s.check('dice: presets render', w.document.querySelectorAll('#presets .chip').length === 12);
    s.noErrors(errors);
  }

  /* ---------- Coin Flip ---------- */
  {
    const { window: w, errors } = await boot('tools/coin-flip.html');

    set(w, 'animate', false, 'change');
    set(w, 'count', '1000');
    await wait(200);

    click(w, 'flip');
    await wait(400);

    const total = Number(text(w, 'r-total').replace(/,/g, ''));
    const heads = Number(text(w, 'r-heads').replace(/,/g, ''));
    const tails = Number(text(w, 'r-tails').replace(/,/g, ''));

    s.eq('coin: 1000 flips recorded', total, 1000);
    s.eq('coin: heads plus tails equals total', heads + tails, 1000);

    // With 1000 fair flips, landing outside 43-57% would be extraordinary
    const headsPct = (heads / total) * 100;
    s.check('coin: roughly fifty-fifty over 1000 flips',
      headsPct > 43 && headsPct < 57, headsPct.toFixed(1) + '%');

    s.match('coin: split displayed', text(w, 'r-split'), /\d+\.\d% \/ \d+\.\d%/);

    // Custom labels
    set(w, 'heads-label', 'Pizza');
    set(w, 'tails-label', 'Curry');
    await wait(300);
    s.eq('coin: custom heads label', text(w, 'l-heads'), 'Pizza');
    s.eq('coin: custom tails label', text(w, 'l-tails'), 'Curry');

    click(w, 'reset');
    await wait(200);
    s.eq('coin: reset clears tally', text(w, 'r-total'), '0');

    click(w, 'flip-100');
    await wait(300);
    s.eq('coin: flip 100 button', text(w, 'r-total'), '100');
    s.noErrors(errors);
  }

  /* ---------- Spin the Wheel ---------- */
  {
    const { window: w, errors, canvasOps } = await boot('tools/spin-the-wheel.html');

    set(w, 'input', 'Pizza\nSushi\nCurry\nTacos');
    set(w, 'duration', '2');
    await wait(350);

    s.match('wheel: counts entries', text(w, 'input-stats'), /4 entries/);
    s.match('wheel: segment count shown', text(w, 'canvas-meta'), /4 segments/);
    s.check('wheel: canvas drawn', canvasOps.length > 0);

    // Spin and wait for the animation to complete
    click(w, 'spin');
    await wait(2600);
    s.check('wheel: picked a real entry',
      ['Pizza', 'Sushi', 'Curry', 'Tacos'].includes(text(w, 'result')), text(w, 'result'));
    s.check('wheel: history recorded', w.document.querySelector('#history table') !== null);

    // Weighted mode changes the reported total weight
    set(w, 'input', 'Pizza:3\nSushi:1');
    set(w, 'weighted', true, 'change');
    await wait(350);
    s.includes('wheel: weights totalled', text(w, 'canvas-meta'), 'total weight 4');

    set(w, 'weighted', false, 'change');
    set(w, 'input', 'OnlyOne');
    await wait(350);
    click(w, 'spin');
    await wait(300);
    s.match('wheel: needs two entries', text(w, 'status'), /at least two entries/i);

    // Shuffle preserves the set of entries
    set(w, 'input', 'A\nB\nC\nD');
    await wait(350);
    click(w, 'shuffle');
    await wait(200);
    s.eq('wheel: shuffle keeps all entries',
      val(w, 'input').split('\n').sort().join(''), 'ABCD');
    s.noErrors(errors);
  }

  /* ---------- Password Game ---------- */
  {
    const { window: w, errors } = await boot('tools/password-game.html');
    w.localStorage.clear();

    await wait(200);
    s.match('game: prompts to start', text(w, 'status'), /start typing/i);

    // Rule 1 is length >= 8
    set(w, 'password', 'short');
    await wait(300);
    s.eq('game: level 1 initially', text(w, 'r-level'), '1');
    s.includes('game: shows rule 1', w.document.getElementById('rules').textContent, '8 characters');

    // Satisfying rule 1 unlocks rule 2
    set(w, 'password', 'longenough');
    await wait(300);
    s.eq('game: level 2 unlocked', text(w, 'r-level'), '2');
    s.includes('game: rule 2 revealed', w.document.getElementById('rules').textContent, 'include a number');

    set(w, 'password', 'longenough1');
    await wait(300);
    s.eq('game: level 3 unlocked', text(w, 'r-level'), '3');

    set(w, 'password', 'Longenough1');
    await wait(300);
    s.eq('game: level 4 unlocked', text(w, 'r-level'), '4');

    set(w, 'password', 'Longenough1!');
    await wait(300);
    s.eq('game: level 5 unlocked', text(w, 'r-level'), '5');

    // Rule 6 forbids "password" — including leetspeak
    set(w, 'password', 'MyP@ssw0rdIsLong1!');
    await wait(300);
    s.includes('game: catches leetspeak password',
      w.document.getElementById('rules').textContent, 'not contain the word');

    // Reveal-all shows every rule
    click(w, 'reveal');
    await wait(300);
    s.eq('game: reveal shows all twelve',
      w.document.querySelectorAll('#rules .info-panel').length, 12);
    s.includes('game: rule 12 mentions space',
      w.document.getElementById('rules').textContent, 'contain a space');

    click(w, 'reset');
    await wait(300);
    s.eq('game: reset clears the field', val(w, 'password'), '');
    s.eq('game: best level remembered', text(w, 'r-best') !== '0', true);
    s.noErrors(errors);
  }

  /* ---------- Emoji Picker ---------- */
  {
    const { window: w, errors } = await boot('tools/emoji-picker.html');
    w.localStorage.clear();

    await wait(300);
    s.match('emoji: shows total count', text(w, 'status'), /Showing \d+ of \d+/);
    s.check('emoji: grid populated',
      w.document.querySelectorAll('#grid button').length > 50);

    set(w, 'search', 'heart');
    await wait(300);
    const results = w.document.querySelectorAll('#grid button');
    s.check('emoji: search narrows results', results.length > 0 && results.length < 30,
      String(results.length));
    s.check('emoji: heart results contain a heart',
      [...results].some((b) => b.textContent.includes('❤')));

    set(w, 'search', 'thumbs');
    await wait(300);
    s.check('emoji: finds thumbs up',
      [...w.document.querySelectorAll('#grid button')].some((b) => b.textContent === '👍'));

    set(w, 'search', 'zzzznothing');
    await wait(300);
    s.match('emoji: no matches state', text(w, 'status'), /no matches/i);

    set(w, 'search', '');
    await wait(300);

    // Category filtering
    const categories = w.document.querySelectorAll('#categories .chip');
    s.eq('emoji: nine category chips', categories.length, 9);
    categories[4].click();   // Animals
    await wait(300);
    s.check('emoji: category filter applied',
      w.document.querySelectorAll('#grid button').length < 100);

    categories[0].click();   // All
    await wait(300);

    // Shift-click collects into the basket
    const first = w.document.querySelector('#grid button');
    const emoji = first.textContent;
    const shiftClick = new w.MouseEvent('click', { bubbles: true, shiftKey: true });
    first.dispatchEvent(shiftClick);
    await wait(200);
    s.includes('emoji: shift-click collects', val(w, 'basket'), emoji);

    click(w, 'clear-basket');
    await wait(200);
    s.eq('emoji: basket cleared', val(w, 'basket'), '');

    // Recents populate after a plain click
    first.click();
    await wait(250);
    s.check('emoji: recents shown',
      w.document.getElementById('recent-field').hidden === false);
    s.noErrors(errors);
  }

  return s;
};
