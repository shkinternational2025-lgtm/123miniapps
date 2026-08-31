/* ============================================
   123MiniApps.online v2.0
   File: test/phase-productivity.js
   Purpose: Behavioural tests for the 6 productivity tools.

   These tools are stateful, so each suite clears
   localStorage before it runs.
   ============================================ */

const { boot, Suite, set, click, text, val, wait } = require('./harness');

const num = (s) => Number(String(s).replace(/[^0-9.-]/g, ''));

module.exports = async function run() {
  const s = new Suite('Productivity tools');

  /* ---------- Pomodoro ---------- */
  {
    const { window: w, errors } = await boot('tools/pomodoro-timer.html');
    w.localStorage.clear();

    s.eq('pomodoro: starts at 25:00', text(w, 'time'), '25:00');
    s.match('pomodoro: shows ready state', text(w, 'phase'), /ready|focus/i);

    // Changing the duration updates the display while stopped
    set(w, 'work', '45');
    await wait(150);
    s.eq('pomodoro: duration change reflected', text(w, 'time'), '45:00');

    set(w, 'work', '25');
    await wait(150);

    click(w, 'start');
    await wait(400);
    s.match('pomodoro: running status', text(w, 'status'), /running/i);
    s.match('pomodoro: title shows countdown', w.document.title, /\d+:\d+ ·/);

    // The display rounds up to whole seconds, so it legitimately shows
    // 25:00 for the first second. Wait past that before asserting.
    await wait(1100);
    const shown = text(w, 'time');
    s.check('pomodoro: counted down from 25:00', shown !== '25:00', shown);

    click(w, 'pause');
    await wait(200);
    s.match('pomodoro: paused status', text(w, 'status'), /paused/i);
    const paused = text(w, 'time');
    await wait(500);
    s.eq('pomodoro: stays put while paused', text(w, 'time'), paused);
    s.eq('pomodoro: title restored on pause', w.document.title.includes('·'), false);

    click(w, 'skip');
    await wait(200);
    s.match('pomodoro: skip moves to break', text(w, 'phase'), /break/i);

    click(w, 'reset');
    await wait(200);
    s.eq('pomodoro: reset returns to 25:00', text(w, 'time'), '25:00');
    s.match('pomodoro: reset phase', text(w, 'phase'), /focus|ready/i);

    s.eq('pomodoro: four progress segments',
      w.document.querySelectorAll('#progress .meter__seg').length, 4);
    s.noErrors(errors);
  }

  /* ---------- Todo List ---------- */
  {
    const { window: w, errors } = await boot('tools/todo-list.html');
    w.localStorage.clear();

    set(w, 'new-task', 'Write the tests');
    click(w, 'add');
    await wait(200);
    s.eq('todo: task added', w.document.querySelectorAll('#list .info-panel').length, 1);
    s.includes('todo: task text shown', w.document.getElementById('list').textContent, 'Write the tests');
    s.eq('todo: input cleared after adding', val(w, 'new-task'), '');

    set(w, 'new-task', 'High priority thing');
    set(w, 'priority', 'high', 'change');
    click(w, 'add');
    await wait(200);
    s.eq('todo: two tasks', w.document.querySelectorAll('#list .info-panel').length, 2);
    s.includes('todo: priority badge shown', w.document.getElementById('list').textContent, 'high');

    // Empty input is rejected
    set(w, 'new-task', '   ');
    click(w, 'add');
    await wait(200);
    s.eq('todo: blank task rejected', w.document.querySelectorAll('#list .info-panel').length, 2);

    // Completing a task
    const checkbox = w.document.querySelector('#list input[type="checkbox"]');
    checkbox.checked = true;
    checkbox.dispatchEvent(new w.Event('change', { bubbles: true }));
    await wait(200);
    s.includes('todo: counts update', text(w, 'counts'), '1 done');

    // Filtering
    set(w, 'filter', 'active', 'change');
    await wait(200);
    s.eq('todo: active filter hides done', w.document.querySelectorAll('#list .info-panel').length, 1);

    set(w, 'filter', 'done', 'change');
    await wait(200);
    s.eq('todo: done filter shows completed', w.document.querySelectorAll('#list .info-panel').length, 1);

    set(w, 'filter', 'all', 'change');
    set(w, 'search', 'priority');
    await wait(300);
    s.eq('todo: search filters', w.document.querySelectorAll('#list .info-panel').length, 1);

    set(w, 'search', '');
    await wait(300);
    click(w, 'clear-done');
    await wait(200);
    s.eq('todo: clear completed removes done tasks',
      w.document.querySelectorAll('#list .info-panel').length, 1);

    // Persistence
    s.check('todo: persisted to storage',
      (w.localStorage.getItem('123ma:todo-tasks') || '').includes('High priority'));

    click(w, 'clear-all');
    await wait(200);
    s.check('todo: empty state shown', w.document.querySelector('#list .empty-state') !== null);
    s.noErrors(errors);
  }

  /* ---------- Notepad ---------- */
  {
    const { window: w, errors } = await boot('tools/notepad.html');
    w.localStorage.clear();

    set(w, 'content', 'Hello world, this is a test note.');
    await wait(700);
    s.match('notepad: word count', text(w, 'r-words'), /^7$/);
    s.match('notepad: saved confirmation', text(w, 'status'), /saved/i);
    s.match('notepad: timestamp shown', text(w, 'r-saved'), /\d/);

    set(w, 'note-title', 'My First Note');
    await wait(700);
    s.check('notepad: title persisted',
      (w.localStorage.getItem('123ma:notepad-notes') || '').includes('My First Note'));

    click(w, 'new');
    await wait(400);
    s.eq('notepad: new note is empty', val(w, 'content'), '');
    s.eq('notepad: two notes now', text(w, 'r-notes'), '2');

    set(w, 'content', 'Second note content here.');
    await wait(700);

    click(w, 'duplicate');
    await wait(400);
    s.eq('notepad: three notes after duplicate', text(w, 'r-notes'), '3');
    s.includes('notepad: duplicate is marked', val(w, 'note-title'), '(copy)');
    s.eq('notepad: duplicate keeps content', val(w, 'content'), 'Second note content here.');

    click(w, 'delete');
    await wait(400);
    s.eq('notepad: back to two notes', text(w, 'r-notes'), '2');

    // Deleting the last note must leave one blank note, not zero
    click(w, 'delete');
    await wait(400);
    click(w, 'delete');
    await wait(400);
    s.eq('notepad: always keeps one note', text(w, 'r-notes'), '1');
    s.noErrors(errors);
  }

  /* ---------- Countdown ---------- */
  {
    const { window: w, errors } = await boot('tools/countdown-timer.html');

    set(w, 'mode', 'duration', 'change');
    set(w, 'hours', '0');
    set(w, 'minutes', '10');
    set(w, 'seconds', '0');
    await wait(200);
    s.eq('countdown: shows 10 minutes', text(w, 'time'), '00:10:00');

    click(w, 'start');
    await wait(1300);
    s.match('countdown: running', text(w, 'status'), /counting down/i);
    s.check('countdown: time decreasing', text(w, 'time') !== '00:10:00', text(w, 'time'));
    s.match('countdown: title shows countdown', w.document.title, /\d+:\d+/);

    click(w, 'pause');
    await wait(200);
    const held = text(w, 'time');
    await wait(500);
    s.eq('countdown: paused holds value', text(w, 'time'), held);

    click(w, 'reset');
    await wait(200);
    s.eq('countdown: reset restores duration', text(w, 'time'), '00:10:00');

    // Past dates are rejected
    set(w, 'mode', 'date', 'change');
    set(w, 'target-date', '2020-01-01T00:00');
    await wait(200);
    click(w, 'start');
    await wait(200);
    s.match('countdown: past date rejected', text(w, 'status'), /already passed/i);

    // Future dates work. A datetime-local input holds LOCAL wall-clock
    // time, so the offset must be applied before formatting — feeding it
    // a raw UTC string lands in the past in any zone ahead of UTC.
    const future = new Date(Date.now() + 3600000);
    const localFuture = new Date(future.getTime() - future.getTimezoneOffset() * 60000)
      .toISOString().slice(0, 16);
    set(w, 'target-date', localFuture);
    await wait(200);
    click(w, 'start');
    await wait(300);
    s.match('countdown: future date accepted', text(w, 'status'), /counting down/i);
    click(w, 'pause');

    s.check('countdown: presets rendered',
      w.document.querySelectorAll('#presets .chip').length === 9);
    s.noErrors(errors);
  }

  /* ---------- Habit Tracker ---------- */
  {
    const { window: w, errors } = await boot('tools/habit-tracker.html');
    w.localStorage.clear();

    s.check('habits: empty state initially',
      w.document.querySelector('#habits .empty-state') !== null);

    set(w, 'new-habit', 'Read for 20 minutes');
    click(w, 'add');
    await wait(250);
    s.eq('habits: habit added', w.document.querySelectorAll('#habits .info-panel').length, 1);
    s.includes('habits: name shown', w.document.getElementById('habits').textContent, 'Read for 20 minutes');

    // 30-day view by default
    let squares = w.document.querySelectorAll('#habits button[aria-pressed]');
    s.eq('habits: 30 squares for 30 days', squares.length, 30);

    // Toggle today (the last square)
    squares[29].click();
    await wait(250);
    s.eq('habits: square toggled on',
      w.document.querySelectorAll('#habits button[aria-pressed="true"]').length, 1);
    s.includes('habits: streak counted',
      w.document.getElementById('habits').textContent, '1 day streak');

    squares = w.document.querySelectorAll('#habits button[aria-pressed]');
    squares[29].click();
    await wait(250);
    s.eq('habits: square toggled off',
      w.document.querySelectorAll('#habits button[aria-pressed="true"]').length, 0);

    // Range switching
    set(w, 'range', '90', 'change');
    await wait(250);
    s.eq('habits: 90-day view', w.document.querySelectorAll('#habits button[aria-pressed]').length, 90);

    set(w, 'new-habit', 'Exercise');
    click(w, 'add');
    await wait(250);
    s.eq('habits: two habits', w.document.querySelectorAll('#habits .info-panel').length, 2);

    s.check('habits: persisted',
      (w.localStorage.getItem('123ma:habit-tracker') || '').includes('Exercise'));

    click(w, 'clear');
    await wait(250);
    s.check('habits: cleared', w.document.querySelector('#habits .empty-state') !== null);
    s.noErrors(errors);
  }

  /* ---------- Meeting Cost ---------- */
  {
    const { window: w, errors } = await boot('tools/meeting-cost-calculator.html');

    // 6 people, £65,000, 1800 h/yr, 1.3 overhead
    // hourly per person = 65000 * 1.3 / 1800 = 46.94
    // room per minute = 46.94 * 6 / 60 = 4.69
    set(w, 'attendees', '6');
    set(w, 'salary', '65000');
    set(w, 'hours-per-year', '1800');
    set(w, 'overhead', '1.3');
    set(w, 'duration', '60');
    set(w, 'currency', 'GBP', 'change');
    await wait(250);

    s.near('meeting: cost per minute', num(text(w, 'r-rate')), 4.69, 0.05);
    s.near('meeting: 60-minute cost', num(text(w, 'r-scheduled')), 281.67, 1);
    s.near('meeting: weekly for a year', num(text(w, 'r-weekly')), 14646, 60);

    // Doubling attendees doubles the cost
    set(w, 'attendees', '12');
    await wait(250);
    s.near('meeting: doubling attendees doubles cost', num(text(w, 'r-scheduled')), 563.33, 2);

    // Overhead multiplier has effect
    set(w, 'attendees', '6');
    set(w, 'overhead', '1');
    await wait(250);
    s.near('meeting: overhead 1.0 lowers cost', num(text(w, 'r-rate')), 3.61, 0.05);

    s.check('meeting: comparison table renders',
      w.document.querySelector('#comparison table') !== null);
    s.eq('meeting: six comparison rows',
      w.document.querySelectorAll('#comparison tbody tr').length, 6);

    click(w, 'start');
    await wait(400);
    s.match('meeting: running', text(w, 'status'), /counting/i);
    s.match('meeting: elapsed shown', text(w, 'elapsed'), /\d\d:\d\d:\d\d elapsed/);

    click(w, 'pause');
    await wait(200);
    s.match('meeting: paused', text(w, 'status'), /paused at/i);

    click(w, 'reset');
    await wait(200);
    s.match('meeting: reset', text(w, 'elapsed'), /press start/i);

    // Currency switching
    set(w, 'currency', 'USD', 'change');
    await wait(250);
    s.match('meeting: currency applied', text(w, 'r-rate'), /\$/);
    s.noErrors(errors);
  }

  return s;
};
