#!/usr/bin/env python3
# ============================================
# 123MiniApps.online v2.0
# File: tools_productivity.py
# Purpose: The 6 Productivity Tools (ids 84-89).
#
# These are the stateful tools, timers, lists and
# trackers. All state lives in localStorage via
# T.store, so nothing is transmitted.
# ============================================

from toolkit import (
 tool, ws, info, row, textarea, text_input, number_input, select, switch,
 slider, output, status_line, buttons, HR, html_block,
)

PAGES = []

# ---------------------------------------------------------------
# 84. Pomodoro Timer
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="pomodoro-timer", name="Pomodoro Timer", icon="🍅", cat="productivity",
 title="Pomodoro Timer: Focused Work Blocks with Automatic Breaks",
 description="Run focused work blocks with automatic break cycles. Custom durations, audio alerts, session counting and a title-bar countdown that survives tab switching.",
 tagline="Focused work blocks with automatic breaks, accurate even in a background tab.",
 workspace=ws(
 html_block(""" <div class="display" id="display">
 <span class="display__value" id="time">25:00</span>
 <span class="display__label" id="phase">Ready to focus</span>
 </div>"""),
 html_block(""" <div class="meter" id="progress" role="img" aria-label="Session progress" style="margin-top:var(--space-4)">
 <span class="meter__seg"></span><span class="meter__seg"></span>
 <span class="meter__seg"></span><span class="meter__seg"></span>
 </div>"""),
 buttons(("start", "Start", "primary"), ("pause", "Pause"), ("reset", "Reset"), ("skip", "Skip phase", "ghost")),
 HR,
 row(
 slider("work", "Work block", 5, 60, 25, 5, unit="min"),
 slider("short-break", "Short break", 1, 20, 5, 1, unit="min"),
 slider("long-break", "Long break", 5, 45, 15, 5, unit="min"),
 ),
 row(
 slider("cycles", "Blocks before a long break", 2, 8, 4, 1, unit=""),
 switch("auto", "Start the next phase automatically", True),
 switch("sound", "Play a sound when a phase ends", True),
 ),
 text_input("task", "What are you working on?", "Optional, shown during the session"),
 status_line("status", "Set your durations and press Start."),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result result--primary"><span class="result__value" id="r-completed" style="font-size:var(--text-3xl)">0</span><span class="result__label">Blocks completed today</span></div>
 <div class="result"><span class="result__value" id="r-focus-time" style="font-size:var(--text-2xl)">0m</span><span class="result__label">Focus time today</span></div>
 <div class="result"><span class="result__value" id="r-streak" style="font-size:var(--text-2xl)">0</span><span class="result__label">Current cycle</span></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Session log</span><span class="field__hint">Stored on this device only</span></span>
 <div class="table-scroll"><div id="log"></div></div>
 </div>"""),
 buttons(("clear-log", "Clear today's log", "ghost"), ("share", "Share tool", "ghost")),
 label="Pomodoro timer",
 ),
 info_block=info(
 features=[
 "Custom work, short break and long break durations",
 "Automatic cycling with a long break every N blocks",
 "Countdown in the browser tab title",
 "Audio alert generated in the browser, no file needed",
 "Daily session log kept on your device",
 ],
 howto=[
 "Set your work and break durations.",
 "Optionally name what you are working on.",
 "Press Start and leave the tab in the background.",
 "The title bar shows the countdown while you work.",
 ],
 background_title="The technique, and why the timer is accurate",
 background_paragraphs=[
 "Francesco Cirillo developed the Pomodoro Technique as a university student in the late 1980s, naming it after a tomato-shaped kitchen timer. The structure is deliberately rigid: work for one block, take a short break, and after four blocks take a longer one. The rigidity is the point, the fixed commitment makes starting easier, and the enforced break prevents the diminishing returns of grinding through fatigue.",
 "Twenty-five minutes is a starting point rather than a rule. Deep technical work often benefits from 45 or 50-minute blocks, because the overhead of reloading context makes short blocks inefficient. Shallower work, email, admin, review, suits shorter blocks. The durations here are adjustable for that reason.",
 "One technical detail worth explaining: browsers throttle <code>setInterval</code> in background tabs, often to once per minute, so a naive timer built by counting ticks drifts badly and can finish minutes late. This timer records the target end time when you press Start and computes the remaining time from the system clock on each tick. That means it stays accurate whether or not the tab is visible, and it recovers correctly if your machine sleeps mid-session.",
 ],
 ),
 script=r""" const PHASES = { work: 'Focus', short: 'Short break', long: 'Long break' };

 let phase = 'work';
 let endTime = null; // absolute timestamp, not a tick count
 let remaining = 0; // milliseconds, used while paused
 let running = false;
 let completedInCycle = 0;
 let ticker = null;
 const originalTitle = document.title;

 function durationFor(which) {
 const minutes = {
 work: Number(T.$('work').value),
 short: Number(T.$('short-break').value),
 long: Number(T.$('long-break').value)
 }[which];
 return minutes * 60000;
 }

 function todayKey() {
 return 'pomodoro-' + new Date().toISOString().slice(0, 10);
 }

 function loadLog() {
 return T.store.get(todayKey(), []);
 }

 function saveSession(entry) {
 const log = loadLog();
 log.push(entry);
 T.store.set(todayKey(), log);
 renderLog();
 }

 function renderLog() {
 const log = loadLog();
 const mount = T.$('log');
 mount.innerHTML = '';

 const workSessions = log.filter((e) => e.phase === 'work');
 const focusMinutes = workSessions.reduce((sum, e) => sum + e.minutes, 0);

 T.$('r-completed').textContent = String(workSessions.length);
 T.$('r-focus-time').textContent = focusMinutes >= 60
 ? `${Math.floor(focusMinutes / 60)}h ${focusMinutes % 60}m`
 : `${focusMinutes}m`;
 T.$('r-streak').textContent = `${completedInCycle} / ${T.$('cycles').value}`;

 if (!log.length) return;

 mount.append(T.table(
 ['Time', 'Phase', 'Length', 'Task'],
 log.slice().reverse().slice(0, 20).map((e) => [
 new Date(e.at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
 PHASES[e.phase],
 e.minutes + ' min',
 e.task || ', '
 ])
 ));
 }

 function updateDisplay() {
 const ms = running ? Math.max(0, endTime - Date.now()) : remaining;
 const totalSeconds = Math.ceil(ms / 1000);
 const minutes = Math.floor(totalSeconds / 60);
 const seconds = totalSeconds % 60;
 const label = `${T.pad2(minutes)}:${T.pad2(seconds)}`;

 T.$('time').textContent = label;

 const task = T.$('task').value.trim();
 T.$('phase').textContent = phase === 'work' && task
 ? `${PHASES[phase]}, ${task}`
 : PHASES[phase];

 // Keep the countdown visible when the tab is in the background
 document.title = running ? `${label} · ${PHASES[phase]}` : originalTitle;

 // Progress meter fills as the phase elapses
 const total = durationFor(phase);
 const elapsed = 1 - ms / total;
 const lit = Math.ceil(T.clamp(elapsed, 0, 1) * 4);
 const key = phase === 'work' ? 'strong' : 'good';
 T.$$('#progress .meter__seg').forEach((seg, i) => {
 seg.className = 'meter__seg' + (i < lit ? ` is-on-${key}` : '');
 });

 if (running && ms <= 0) finishPhase();
 }

 /** A short two-tone chime, synthesised so no audio file is needed. */
 function playChime() {
 if (!T.$('sound').checked) return;

 try {
 const Ctx = window.AudioContext || window.webkitAudioContext;
 if (!Ctx) return;

 const ctx = new Ctx();
 const now = ctx.currentTime;

 [880, 1320].forEach((frequency, index) => {
 const osc = ctx.createOscillator();
 const gain = ctx.createGain();

 osc.type = 'sine';
 osc.frequency.value = frequency;

 const start = now + index * 0.18;
 gain.gain.setValueAtTime(0, start);
 gain.gain.linearRampToValueAtTime(0.25, start + 0.02);
 gain.gain.exponentialRampToValueAtTime(0.001, start + 0.35);

 osc.connect(gain).connect(ctx.destination);
 osc.start(start);
 osc.stop(start + 0.4);
 });

 setTimeout(() => ctx.close(), 1200);
 } catch {
 /* Audio is a nicety, never let it break the timer */
 }
 }

 function finishPhase() {
 running = false;
 clearInterval(ticker);
 playChime();

 saveSession({
 at: Date.now(),
 phase,
 minutes: Math.round(durationFor(phase) / 60000),
 task: T.$('task').value.trim()
 });

 if (phase === 'work') {
 completedInCycle++;
 const cycles = Number(T.$('cycles').value);
 phase = completedInCycle >= cycles ? 'long' : 'short';
 if (phase === 'long') completedInCycle = 0;
 } else {
 phase = 'work';
 }

 remaining = durationFor(phase);
 updateDisplay();

 T.status('status', `${PHASES[phase]} is next.`, 'ok');
 toast({
 type: 'success',
 title: 'Phase complete',
 message: `Time for a ${PHASES[phase].toLowerCase()}.`,
 duration: 8000
 });

 if (T.$('auto').checked) start();
 else renderLog();
 }

 function start() {
 if (running) return;

 if (remaining <= 0) remaining = durationFor(phase);
 endTime = Date.now() + remaining;
 running = true;

 clearInterval(ticker);
 // A 250ms tick keeps the display smooth; accuracy comes from
 // comparing against endTime, not from counting ticks
 ticker = setInterval(updateDisplay, 250);
 updateDisplay();

 T.status('status', `${PHASES[phase]} running.`, 'ok');
 if (window.Analytics) Analytics.trackToolUse('pomodoro-timer');
 }

 function pause() {
 if (!running) return;
 remaining = Math.max(0, endTime - Date.now());
 running = false;
 clearInterval(ticker);
 updateDisplay();
 T.status('status', 'Paused.', 'warn');
 }

 function reset() {
 running = false;
 clearInterval(ticker);
 phase = 'work';
 completedInCycle = 0;
 remaining = durationFor('work');
 updateDisplay();
 renderLog();
 T.status('status', 'Reset. Set your durations and press Start.', 'muted');
 }

 function skip() {
 if (running) { running = false; clearInterval(ticker); }
 phase = phase === 'work' ? 'short' : 'work';
 remaining = durationFor(phase);
 updateDisplay();
 T.status('status', `Skipped to ${PHASES[phase].toLowerCase()}.`, 'muted');
 }

 T.$('start').addEventListener('click', start);
 T.$('pause').addEventListener('click', pause);
 T.$('reset').addEventListener('click', reset);
 T.$('skip').addEventListener('click', skip);

 ['work', 'short-break', 'long-break', 'cycles'].forEach((id) => {
 T.$(id).addEventListener('input', () => {
 T.$(id + '-value').textContent = T.$(id).value;
 if (!running) {
 remaining = durationFor(phase);
 updateDisplay();
 }
 renderLog();
 });
 });

 T.$('task').addEventListener('input', updateDisplay);

 T.$('clear-log').addEventListener('click', () => {
 T.store.remove(todayKey());
 completedInCycle = 0;
 renderLog();
 toast({ type: 'success', title: 'Log cleared' });
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Pomodoro Timer | 123MiniApps' }));

 // Restore the title if the user navigates away mid-session
 window.addEventListener('beforeunload', () => { document.title = originalTitle; });

 remaining = durationFor('work');
 updateDisplay();
 renderLog();""",
))

# ---------------------------------------------------------------
# 85. Todo List
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="todo-list", name="Todo List", icon="✅", cat="productivity",
 title="Todo List: Fast Checklist With No Account Required",
 description="A fast checklist that saves to your browser and needs no account. Priorities, due dates, filtering and drag-free reordering, stored only on your device.",
 tagline="A checklist that saves to your browser, no account, no sync, no tracking.",
 workspace=ws(
 html_block(""" <div class="field">
 <label class="field__label" for="new-task"><span>Add a task</span><span class="field__hint">Press Enter to add</span></label>
 <div style="display:flex;gap:var(--space-3)">
 <input class="input" id="new-task" type="text" placeholder="What needs doing?" autocomplete="off" style="flex:1">
 <button class="btn btn--primary" id="add" type="button">Add</button>
 </div>
 </div>"""),
 row(
 select("priority", "Priority", [("normal", "Normal"), ("high", "High"), ("low", "Low")], selected="normal"),
 text_input("due", "Due date (optional)", "", "", "date"),
 text_input("tag", "Tag (optional)", "e.g. work"),
 ),
 HR,
 row(
 select("filter", "Show", [
 ("all", "Everything"), ("active", "Not done"), ("done", "Done"),
 ("today", "Due today or overdue"), ("high", "High priority"),
 ], selected="all"),
 select("sort", "Sort by", [
 ("added", "When added"), ("priority", "Priority"),
 ("due", "Due date"), ("alpha", "Alphabetically"),
 ], selected="added"),
 text_input("search", "Search", "Filter by text"),
 ),
 status_line("status", "Add your first task."),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Tasks</span><span class="field__hint" id="counts"></span></span>
 <div id="list"></div>
 </div>"""),
 buttons(("clear-done", "Clear completed", "secondary"), ("export", "Export as text"), ("copy", "Copy list"), ("clear-all", "Delete everything", "ghost"), ("share", "Share tool", "ghost")),
 label="Todo list",
 ),
 info_block=info(
 features=[
 "Priorities, due dates and tags",
 "Filter by status, priority or due date",
 "Move tasks up and down without dragging",
 "Search across all tasks",
 "Saved on your device, no account, no sync",
 ],
 howto=[
 "Type a task and press Enter.",
 "Set a priority or due date before adding if you want one.",
 "Click a task to mark it done.",
 "Use the filters to focus on what matters now.",
 ],
 background_title="Where your tasks live, and what that means",
 background_paragraphs=[
 "Everything here is stored in your browser's localStorage. That has real advantages: it works offline, it loads instantly, nobody can read it, and there is no account to create or subscription to cancel. It also has a real limitation you should understand before relying on it, the data lives in one browser on one device. It will not appear on your phone, it does not survive clearing site data, and private browsing windows discard it when closed.",
 "Use the export button if a list matters. A quick copy into a note or document takes seconds and protects you from the one failure mode this design has.",
 "On the productivity side, the most useful discipline is keeping the list short. A list of eighty items is a source of anxiety rather than a plan, because scanning it costs more attention than it saves. Most systems that work, whether that is a daily top-three, a kanban work-in-progress limit, or simply deleting anything untouched for a month, do the same underlying thing: they reduce the number of open decisions. The filters here exist to support that, not to help you manage a longer list.",
 ],
 ),
 script=r""" let tasks = T.store.get('todo-tasks', []);

 const PRIORITY_ORDER = { high: 0, normal: 1, low: 2 };
 const PRIORITY_COLOUR = { high: 'var(--danger)', normal: 'var(--text-muted)', low: 'var(--info)' };

 function save() {
 T.store.set('todo-tasks', tasks);
 }

 function addTask() {
 const textValue = T.$('new-task').value.trim();
 if (!textValue) {
 T.status('status', 'Type something first.', 'warn');
 return;
 }

 tasks.push({
 id: Date.now() + Math.random(),
 text: textValue,
 done: false,
 priority: T.$('priority').value,
 due: T.$('due').value || null,
 tag: T.$('tag').value.trim() || null,
 added: Date.now()
 });

 save();
 T.$('new-task').value = '';
 T.$('due').value = '';
 render();
 T.$('new-task').focus();

 if (window.Analytics) Analytics.trackToolUse('todo-list');
 }

 function visibleTasks() {
 const filter = T.$('filter').value;
 const search = T.$('search').value.trim().toLowerCase();
 const today = new Date().toISOString().slice(0, 10);

 let list = tasks.filter((task) => {
 if (search && !task.text.toLowerCase().includes(search) &&
 !(task.tag || '').toLowerCase().includes(search)) return false;

 if (filter === 'active') return !task.done;
 if (filter === 'done') return task.done;
 if (filter === 'high') return task.priority === 'high' && !task.done;
 if (filter === 'today') return !task.done && task.due && task.due <= today;
 return true;
 });

 const sort = T.$('sort').value;
 if (sort === 'priority') {
 list = [...list].sort((a, b) => PRIORITY_ORDER[a.priority] - PRIORITY_ORDER[b.priority]);
 } else if (sort === 'due') {
 // Tasks with no due date sort last
 list = [...list].sort((a, b) => (a.due || '9999').localeCompare(b.due || '9999'));
 } else if (sort === 'alpha') {
 list = [...list].sort((a, b) => a.text.localeCompare(b.text));
 }

 return list;
 }

 function dueLabel(due) {
 if (!due) return null;
 const today = new Date().toISOString().slice(0, 10);
 const date = new Date(due + 'T00:00:00');
 const days = Math.round((date - new Date(today + 'T00:00:00')) / 86400000);

 if (days < 0) return { text: `${Math.abs(days)} day(s) overdue`, colour: 'var(--danger)' };
 if (days === 0) return { text: 'Due today', colour: 'var(--warning)' };
 if (days === 1) return { text: 'Due tomorrow', colour: 'var(--warning)' };
 return { text: `Due in ${days} days`, colour: 'var(--text-muted)' };
 }

 function render() {
 const mount = T.$('list');
 mount.innerHTML = '';

 const list = visibleTasks();
 const done = tasks.filter((t) => t.done).length;

 T.$('counts').textContent = tasks.length
 ? `${tasks.length - done} open · ${done} done`
 : '';

 if (!list.length) {
 mount.append(el('div', { className: 'empty-state' }, [
 el('div', { className: 'empty-state__icon', text: tasks.length ? '🔍' : '📝',
 attrs: { 'aria-hidden': 'true' } }),
 el('p', { text: tasks.length
 ? 'No tasks match the current filter.'
 : 'Nothing here yet. Add your first task above.' })
 ]));
 T.status('status', tasks.length ? 'No matches.' : 'Add your first task.', 'muted');
 return;
 }

 list.forEach((task) => {
 const index = tasks.indexOf(task);

 const rowEl = el('div', {
 className: 'info-panel mb-2',
 style: {
 display: 'flex', alignItems: 'center', gap: 'var(--space-4)',
 opacity: task.done ? '0.55' : '1',
 borderLeftWidth: '3px',
 borderLeftColor: task.done ? 'var(--success)' : PRIORITY_COLOUR[task.priority]
 }
 });

 const checkbox = el('input', {
 attrs: {
 type: 'checkbox',
 'aria-label': `Mark “${task.text}” as ${task.done ? 'not done' : 'done'}`
 },
 style: { width: '20px', height: '20px', flexShrink: '0', cursor: 'pointer' }
 });
 checkbox.checked = task.done;
 checkbox.addEventListener('change', () => {
 task.done = checkbox.checked;
 save();
 render();
 });

 const body = el('div', { style: { flex: '1', minWidth: '0' } });
 body.append(el('div', {
 text: task.text,
 style: {
 textDecoration: task.done ? 'line-through' : 'none',
 color: 'var(--text-primary)',
 overflowWrap: 'anywhere'
 }
 }));

 const meta = el('div', { className: 'flex flex-wrap gap-2 mt-2' });

 if (task.priority !== 'normal') {
 meta.append(el('span', {
 className: 'badge',
 text: task.priority,
 style: { color: PRIORITY_COLOUR[task.priority], borderColor: PRIORITY_COLOUR[task.priority] }
 }));
 }

 if (task.tag) meta.append(el('span', { className: 'badge badge--muted', text: task.tag }));

 const due = dueLabel(task.due);
 if (due && !task.done) {
 meta.append(el('span', {
 className: 'badge',
 text: due.text,
 style: { color: due.colour, borderColor: due.colour }
 }));
 }

 if (meta.children.length) body.append(meta);
 rowEl.append(checkbox, body);

 // Reordering without drag-and-drop, which is fiddly on touch
 const controls = el('div', { className: 'flex gap-1', style: { flexShrink: '0' } });

 const move = (direction, label) => {
 const button = el('button', {
 className: 'btn btn--ghost btn--sm',
 attrs: { type: 'button', 'aria-label': `Move “${task.text}” ${label}` },
 text: direction < 0 ? '↑' : '↓'
 });
 button.addEventListener('click', () => {
 const target = index + direction;
 if (target < 0 || target >= tasks.length) return;
 [tasks[index], tasks[target]] = [tasks[target], tasks[index]];
 save();
 render();
 });
 return button;
 };

 const remove = el('button', {
 className: 'btn btn--ghost btn--sm',
 attrs: { type: 'button', 'aria-label': `Delete “${task.text}”` },
 text: '✕'
 });
 remove.addEventListener('click', () => {
 tasks.splice(index, 1);
 save();
 render();
 });

 controls.append(move(-1, 'up'), move(1, 'down'), remove);
 rowEl.append(controls);
 mount.append(rowEl);
 });

 const overdue = tasks.filter((t) => !t.done && t.due && t.due < new Date().toISOString().slice(0, 10)).length;
 T.status('status',
 overdue ? `${overdue} task(s) overdue.` : `${tasks.length - done} task(s) remaining.`,
 overdue ? 'warn' : 'ok');
 }

 function asText() {
 return tasks.map((task) =>
 `${task.done ? '[x]' : '[ ]'} ${task.text}` +
 (task.priority !== 'normal' ? ` (${task.priority})` : '') +
 (task.due ? `, due ${task.due}` : '') +
 (task.tag ? ` #${task.tag}` : '')
 ).join('\n');
 }

 T.$('add').addEventListener('click', addTask);
 T.$('new-task').addEventListener('keydown', (e) => {
 if (e.key === 'Enter') { e.preventDefault(); addTask(); }
 });

 T.on(['filter', 'sort'], render, 'change');
 T.$('search').addEventListener('input', debounce(render, 200));

 T.$('clear-done').addEventListener('click', () => {
 const before = tasks.length;
 tasks = tasks.filter((t) => !t.done);
 save();
 render();
 toast({ type: 'success', title: `Cleared ${before - tasks.length} completed task(s)` });
 });

 T.$('clear-all').addEventListener('click', () => {
 if (!tasks.length) return;
 tasks = [];
 save();
 render();
 toast({ type: 'success', title: 'All tasks deleted', message: 'This cannot be undone.' });
 });

 T.$('copy').addEventListener('click', () => copyToClipboard(asText(), 'List copied'));
 T.$('export').addEventListener('click', () => {
 if (!tasks.length) { toast({ type: 'warning', title: 'Nothing to export' }); return; }
 downloadFile(asText(), 'todo-list.txt');
 });
 T.$('share').addEventListener('click', () => shareLink({ title: 'Todo List | 123MiniApps' }));

 render();""",
))

# ---------------------------------------------------------------
# 86. Notepad
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="notepad", name="Notepad", icon="📓", cat="productivity",
 title="Notepad: Distraction-Free Scratchpad That Autosaves",
 description="A distraction-free scratchpad that autosaves as you type. Multiple notes, word count, full-screen focus mode and text export, all stored locally.",
 tagline="A scratchpad that autosaves to your browser, multiple notes, no account.",
 workspace=ws(
 row(
 select("note-select", "Note", []),
 text_input("note-title", "Title", "Untitled note"),
 ),
 html_block(""" <div class="field">
 <label class="field__label" for="content">
 <span>Content</span>
 <span class="field__hint" id="content-stats"></span>
 </label>
 <textarea class="textarea" id="content" style="min-height:420px;font-family:var(--font-body);font-size:var(--text-base)"
 placeholder="Start typing. Everything saves automatically to this browser."></textarea>
 </div>"""),
 status_line("status", "Autosaves as you type."),
 buttons(("new", "New note", "primary"), ("duplicate", "Duplicate"), ("delete", "Delete note"), ("focus", "Focus mode"), ("copy", "Copy"), ("download", "Download"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result"><span class="result__value" id="r-words" style="font-size:var(--text-2xl)">0</span><span class="result__label">Words</span></div>
 <div class="result"><span class="result__value" id="r-chars" style="font-size:var(--text-2xl)">0</span><span class="result__label">Characters</span></div>
 <div class="result"><span class="result__value" id="r-notes" style="font-size:var(--text-2xl)">0</span><span class="result__label">Notes saved</span></div>
 <div class="result"><span class="result__value" id="r-saved" style="font-size:var(--text-lg)">, </span><span class="result__label">Last saved</span></div>
 </div>"""),
 label="Notepad",
 ),
 info_block=info(
 features=[
 "Autosaves as you type, no save button",
 "Multiple named notes",
 "Full-screen focus mode",
 "Live word and character count",
 "Export any note as a text file",
 ],
 howto=[
 "Start typing, the note saves itself.",
 "Use New note to start another.",
 "Switch between notes with the dropdown.",
 "Download anything you want to keep permanently.",
 ],
 background_title="Autosave, and the limits of browser storage",
 background_paragraphs=[
 "Typing triggers a debounced save half a second after you stop, rather than on every keystroke, writing to localStorage is synchronous and blocks the main thread, so saving on every character would make typing feel sluggish in a long note. The note also saves when you switch away from the tab or close it, which covers the case where you type and immediately navigate away.",
 "localStorage gives roughly 5 to 10 MB per origin depending on the browser, which is a great deal of plain text, several hundred thousand words. You are far more likely to lose notes to clearing browser data than to hitting the limit. Private browsing windows are the main hazard: they discard storage entirely when the last window closes, usually without warning.",
 "The honest framing is that this is a scratchpad, not a notes application. It is genuinely good for the thing it is for, somewhere to paste text, draft a message, or think something through without opening an app or creating an account. For anything you would be upset to lose, download it or paste it somewhere durable. The export button exists precisely because this storage is convenient rather than reliable.",
 ],
 ),
 script=r""" let notes = T.store.get('notepad-notes', []);
 let currentId = T.store.get('notepad-current', null);
 let saveTimer = null;

 function ensureNote() {
 if (!notes.length) {
 notes = [{ id: Date.now(), title: 'Untitled note', content: '', updated: Date.now() }];
 currentId = notes[0].id;
 persist();
 }
 if (!notes.some((n) => n.id === currentId)) currentId = notes[0].id;
 }

 function current() {
 return notes.find((n) => n.id === currentId);
 }

 function persist() {
 T.store.set('notepad-notes', notes);
 T.store.set('notepad-current', currentId);
 }

 function populateSelect() {
 const select = T.$('note-select');
 select.innerHTML = '';

 // Most recently edited first
 [...notes].sort((a, b) => b.updated - a.updated).forEach((note) => {
 const option = document.createElement('option');
 option.value = String(note.id);
 const preview = note.content.trim().split('\n')[0].slice(0, 30);
 option.textContent = note.title + (preview ? `, ${preview}…` : '');
 if (note.id === currentId) option.selected = true;
 select.append(option);
 });

 T.$('r-notes').textContent = String(notes.length);
 }

 function loadCurrent() {
 const note = current();
 if (!note) return;

 T.$('note-title').value = note.title;
 T.$('content').value = note.content;
 updateStats();

 T.$('r-saved').textContent = note.updated
 ? new Date(note.updated).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
 : ', ';
 }

 function updateStats() {
 const content = T.$('content').value;
 const words = T.words(content).length;

 T.$('r-words').textContent = words.toLocaleString();
 T.$('r-chars').textContent = content.length.toLocaleString();
 T.$('content-stats').textContent =
 `${words.toLocaleString()} words · ${content.length.toLocaleString()} characters`;
 }

 function saveNow() {
 const note = current();
 if (!note) return;

 note.title = T.$('note-title').value.trim() || 'Untitled note';
 note.content = T.$('content').value;
 note.updated = Date.now();

 const ok = T.store.set('notepad-notes', notes);
 T.store.set('notepad-current', currentId);

 T.$('r-saved').textContent = new Date(note.updated)
 .toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

 populateSelect();

 T.status('status',
 ok ? 'Saved to this browser.' : 'Could not save, browser storage may be full or disabled.',
 ok ? 'ok' : 'error');
 }

 /** Debounced so typing stays smooth, localStorage writes are synchronous. */
 function scheduleSave() {
 updateStats();
 T.status('status', 'Saving…', 'muted');
 clearTimeout(saveTimer);
 saveTimer = setTimeout(saveNow, 500);
 }

 T.$('content').addEventListener('input', scheduleSave);
 T.$('note-title').addEventListener('input', scheduleSave);

 T.$('note-select').addEventListener('change', () => {
 saveNow();
 currentId = Number(T.$('note-select').value);
 persist();
 loadCurrent();
 });

 T.$('new').addEventListener('click', () => {
 saveNow();
 const note = { id: Date.now(), title: 'Untitled note', content: '', updated: Date.now() };
 notes.push(note);
 currentId = note.id;
 persist();
 populateSelect();
 loadCurrent();
 T.$('content').focus();
 toast({ type: 'success', title: 'New note created' });
 });

 T.$('duplicate').addEventListener('click', () => {
 saveNow();
 const source = current();
 if (!source) return;
 const copy = {
 id: Date.now(),
 title: source.title + ' (copy)',
 content: source.content,
 updated: Date.now()
 };
 notes.push(copy);
 currentId = copy.id;
 persist();
 populateSelect();
 loadCurrent();
 });

 T.$('delete').addEventListener('click', () => {
 if (notes.length === 1) {
 // Keep at least one note rather than leaving an empty state
 notes[0] = { id: Date.now(), title: 'Untitled note', content: '', updated: Date.now() };
 currentId = notes[0].id;
 } else {
 notes = notes.filter((n) => n.id !== currentId);
 currentId = notes[0].id;
 }
 persist();
 populateSelect();
 loadCurrent();
 toast({ type: 'success', title: 'Note deleted' });
 });

 T.$('focus').addEventListener('click', () => {
 const textarea = T.$('content');
 if (document.fullscreenElement) {
 document.exitFullscreen();
 return;
 }
 const wrapper = textarea.closest('.field');
 if (wrapper && wrapper.requestFullscreen) {
 wrapper.requestFullscreen().then(() => textarea.focus()).catch(() => {
 toast({ type: 'warning', title: 'Full screen unavailable' });
 });
 }
 });

 T.$('copy').addEventListener('click', () =>
 copyToClipboard(T.$('content').value, 'Note copied'));

 T.$('download').addEventListener('click', () => {
 const note = current();
 if (!note || !note.content.trim()) {
 toast({ type: 'warning', title: 'This note is empty' });
 return;
 }
 downloadFile(note.content, T.slugify(note.title || 'note') + '.txt');
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Notepad | 123MiniApps' }));

 // Save when leaving, so a quick type-and-navigate is not lost
 window.addEventListener('beforeunload', saveNow);
 document.addEventListener('visibilitychange', () => {
 if (document.hidden) saveNow();
 });

 ensureNote();
 populateSelect();
 loadCurrent();
 if (window.Analytics) Analytics.trackToolUse('notepad');""",
))

# ---------------------------------------------------------------
# 87. Countdown Timer
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="countdown-timer", name="Countdown Timer", icon="⏱️", cat="productivity",
 title="Countdown Timer: Count Down to a Date or Duration",
 description="Count down to a date or run a simple duration timer, with a full-screen display, audio alert and a shareable link that carries the target time.",
 tagline="Count down to a date or a duration, with a shareable link and full-screen display.",
 workspace=ws(
 select("mode", "Countdown to", [
 ("duration", "A duration from now"), ("date", "A specific date and time"),
 ], selected="duration"),
 html_block(""" <div class="workspace__row" id="duration-panel">
 <div class="field">
 <label class="field__label" for="hours"><span>Hours</span></label>
 <input class="input" id="hours" type="number" value="0" min="0" max="99" step="1" inputmode="numeric">
 </div>
 <div class="field">
 <label class="field__label" for="minutes"><span>Minutes</span></label>
 <input class="input" id="minutes" type="number" value="10" min="0" max="59" step="1" inputmode="numeric">
 </div>
 <div class="field">
 <label class="field__label" for="seconds"><span>Seconds</span></label>
 <input class="input" id="seconds" type="number" value="0" min="0" max="59" step="1" inputmode="numeric">
 </div>
 </div>"""),
 html_block(""" <div class="field" id="date-panel" hidden>
 <label class="field__label" for="target-date"><span>Target date and time</span></label>
 <input class="input" id="target-date" type="datetime-local">
 </div>"""),
 text_input("label", "Label (optional)", "What is this counting down to?"),
 html_block(""" <div class="display" id="display">
 <span class="display__value" id="time">00:10:00</span>
 <span class="display__label" id="caption">Ready</span>
 </div>"""),
 status_line("status", "Set a duration and press Start."),
 buttons(("start", "Start", "primary"), ("pause", "Pause"), ("reset", "Reset"), ("fullscreen", "Full screen"), ("copy-link", "Copy shareable link"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Quick presets</span></span>
 <div class="chip-grid" id="presets"></div>
 </div>"""),
 label="Countdown timer",
 ),
 info_block=info(
 features=[
 "Duration mode or a specific target date",
 "Full-screen display for presentations",
 "Audio alert generated in the browser",
 "Shareable link carrying the target time",
 "Accurate in background tabs",
 ],
 howto=[
 "Choose duration or date mode.",
 "Set the time and press Start.",
 "Use Full screen for a room-visible display.",
 "Copy the shareable link to send the same countdown to someone else.",
 ],
 background_title="Why background tabs break naive timers",
 background_paragraphs=[
 "Browsers aggressively throttle timers in tabs that are not visible, typically to once per second, and often to once per minute after a few minutes of inactivity. A countdown built by decrementing a counter on each tick therefore runs slow, and a ten-minute timer left in a background tab can finish several minutes late.",
 "This timer avoids the problem by storing an absolute target timestamp when you press Start, then computing the remaining time from the system clock on every tick. The tick rate only affects how smoothly the display updates, never the accuracy. It also means the timer recovers correctly if your machine sleeps: on waking it immediately shows the correct remaining time, or fires straight away if the moment has passed.",
 "The shareable link encodes the target as a Unix timestamp in the URL fragment. Because it is a fragment rather than a query parameter, it is never sent to the server, the countdown is reconstructed entirely in the recipient's browser. That keeps the tool consistent with the rest of the site: nothing about what you are counting down to leaves your device.",
 ],
 ),
 script=r""" let endTime = null;
 let remaining = 0;
 let running = false;
 let ticker = null;
 const originalTitle = document.title;

 const PRESETS = [
 ['1 minute', 60], ['3 minutes', 180], ['5 minutes', 300],
 ['10 minutes', 600], ['15 minutes', 900], ['20 minutes', 1200],
 ['30 minutes', 1800], ['45 minutes', 2700], ['1 hour', 3600]
 ];

 function durationSeconds() {
 return (T.num(T.$('hours').value) || 0) * 3600 +
 (T.num(T.$('minutes').value) || 0) * 60 +
 (T.num(T.$('seconds').value) || 0);
 }

 function targetFromInputs() {
 if (T.$('mode').value === 'date') {
 const value = T.$('target-date').value;
 if (!value) return null;
 const ms = new Date(value).getTime();
 return isFinite(ms) ? ms : null;
 }
 return Date.now() + durationSeconds() * 1000;
 }

 function formatRemaining(ms) {
 const total = Math.max(0, Math.ceil(ms / 1000));
 const days = Math.floor(total / 86400);
 const hours = Math.floor((total % 86400) / 3600);
 const minutes = Math.floor((total % 3600) / 60);
 const seconds = total % 60;

 if (days > 0) return `${days}d ${T.pad2(hours)}:${T.pad2(minutes)}:${T.pad2(seconds)}`;
 return `${T.pad2(hours)}:${T.pad2(minutes)}:${T.pad2(seconds)}`;
 }

 function update() {
 // Always derive from the clock, never from a tick counter
 const ms = running ? Math.max(0, endTime - Date.now()) : remaining;
 const label = formatRemaining(ms);

 T.$('time').textContent = label;

 const caption = T.$('label').value.trim();
 T.$('caption').textContent = running
 ? (caption || 'Counting down')
 : (ms <= 0 ? 'Finished' : 'Ready');

 document.title = running ? `${label}, ${caption || 'Countdown'}` : originalTitle;

 // Turn red in the final minute
 T.$('time').style.color = running && ms < 60000 ? 'var(--danger)' : '';

 if (running && ms <= 0) finish();
 }

 function finish() {
 running = false;
 clearInterval(ticker);
 remaining = 0;
 document.title = originalTitle;

 T.$('time').textContent = '00:00:00';
 T.$('caption').textContent = 'Time is up';
 T.status('status', 'Countdown finished.', 'ok');

 playAlarm();
 toast({ type: 'success', title: 'Time is up', message: T.$('label').value.trim() || '', duration: 10000 });
 }

 /** Three short beeps, synthesised, no audio file required. */
 function playAlarm() {
 try {
 const Ctx = window.AudioContext || window.webkitAudioContext;
 if (!Ctx) return;

 const ctx = new Ctx();
 const now = ctx.currentTime;

 for (let i = 0; i < 3; i++) {
 const osc = ctx.createOscillator();
 const gain = ctx.createGain();
 osc.type = 'square';
 osc.frequency.value = 880;

 const start = now + i * 0.32;
 gain.gain.setValueAtTime(0, start);
 gain.gain.linearRampToValueAtTime(0.18, start + 0.02);
 gain.gain.exponentialRampToValueAtTime(0.001, start + 0.25);

 osc.connect(gain).connect(ctx.destination);
 osc.start(start);
 osc.stop(start + 0.3);
 }

 setTimeout(() => ctx.close(), 1500);
 } catch {
 /* audio is optional */
 }
 }

 function start() {
 if (running) return;

 if (remaining > 0) {
 endTime = Date.now() + remaining;
 } else {
 const target = targetFromInputs();
 if (target === null) {
 T.status('status', 'Set a target date first.', 'error');
 return;
 }
 if (target <= Date.now()) {
 T.status('status', 'That time has already passed.', 'error');
 return;
 }
 endTime = target;
 }

 running = true;
 clearInterval(ticker);
 ticker = setInterval(update, 200);
 update();

 T.status('status', 'Counting down.', 'ok');
 if (window.Analytics) Analytics.trackToolUse('countdown-timer');
 }

 function pause() {
 if (!running) return;
 remaining = Math.max(0, endTime - Date.now());
 running = false;
 clearInterval(ticker);
 update();
 T.status('status', 'Paused.', 'warn');
 }

 function reset() {
 running = false;
 clearInterval(ticker);
 remaining = 0;
 document.title = originalTitle;

 const target = targetFromInputs();
 T.$('time').textContent = formatRemaining(
 T.$('mode').value === 'date' && target ? target - Date.now() : durationSeconds() * 1000
 );
 T.$('caption').textContent = 'Ready';
 T.$('time').style.color = '';
 T.status('status', 'Reset.', 'muted');
 }

 function syncMode() {
 const isDate = T.$('mode').value === 'date';
 T.$('duration-panel').hidden = isDate;
 T.$('date-panel').hidden = !isDate;
 reset();
 }

 T.$('start').addEventListener('click', start);
 T.$('pause').addEventListener('click', pause);
 T.$('reset').addEventListener('click', reset);
 T.$('mode').addEventListener('change', syncMode);

 T.on(['hours', 'minutes', 'seconds', 'target-date'], () => { if (!running) reset(); });
 T.$('label').addEventListener('input', update);

 T.$('fullscreen').addEventListener('click', () => {
 const display = T.$('display');
 if (document.fullscreenElement) {
 document.exitFullscreen();
 } else if (display.requestFullscreen) {
 display.requestFullscreen().catch(() =>
 toast({ type: 'warning', title: 'Full screen unavailable' }));
 }
 });

 T.$('copy-link').addEventListener('click', () => {
 const target = running ? endTime : targetFromInputs();
 if (!target) {
 toast({ type: 'warning', title: 'Set a time first' });
 return;
 }
 // The fragment is never sent to the server, so the target stays private
 const url = `${location.origin}${location.pathname}#t=${Math.floor(target / 1000)}` +
 (T.$('label').value.trim() ? `&l=${encodeURIComponent(T.$('label').value.trim())}` : '');
 copyToClipboard(url, 'Shareable link copied');
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Countdown Timer | 123MiniApps' }));

 // Presets
 const presetMount = T.$('presets');
 PRESETS.forEach(([name, seconds]) => {
 const chip = el('button', { className: 'chip', attrs: { type: 'button' }, text: name });
 chip.addEventListener('click', () => {
 T.$('mode').value = 'duration';
 syncMode();
 T.$('hours').value = String(Math.floor(seconds / 3600));
 T.$('minutes').value = String(Math.floor((seconds % 3600) / 60));
 T.$('seconds').value = String(seconds % 60);
 reset();
 start();
 });
 presetMount.append(chip);
 });

 // Restore a shared countdown from the URL fragment
 (function restoreFromHash() {
 const match = location.hash.match(/t=(\d+)/);
 if (!match) return;

 const target = Number(match[1]) * 1000;
 const labelMatch = location.hash.match(/l=([^&]+)/);
 if (labelMatch) T.$('label').value = decodeURIComponent(labelMatch[1]);

 if (target > Date.now()) {
 T.$('mode').value = 'date';
 syncMode();
 T.$('target-date').value = new Date(target - new Date().getTimezoneOffset() * 60000)
 .toISOString().slice(0, 16);
 start();
 T.status('status', 'Restored a shared countdown from the link.', 'ok');
 }
 })();

 window.addEventListener('beforeunload', () => { document.title = originalTitle; });

 syncMode();""",
))

# ---------------------------------------------------------------
# 88. Habit Tracker
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="habit-tracker", name="Habit Tracker", icon="📈", cat="productivity",
 title="Habit Tracker: Streak Grid Stored on Your Device",
 description="Track daily habits on a streak grid stored only on your device. Multiple habits, current and longest streaks, and completion percentages.",
 tagline="Track daily habits on a streak grid, stored on your device, never uploaded.",
 workspace=ws(
 html_block(""" <div class="field">
 <label class="field__label" for="new-habit"><span>Add a habit</span></label>
 <div style="display:flex;gap:var(--space-3)">
 <input class="input" id="new-habit" type="text" placeholder="e.g. Read for 20 minutes" autocomplete="off" style="flex:1">
 <button class="btn btn--primary" id="add" type="button">Add</button>
 </div>
 </div>"""),
 row(
 select("range", "Show", [("30", "Last 30 days"), ("60", "Last 60 days"), ("90", "Last 90 days")], selected="30"),
 switch("weekends", "Highlight weekends", True),
 ),
 status_line("status", "Add a habit to start tracking."),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Your habits</span><span class="field__hint">Click any square to toggle that day</span></span>
 <div id="habits"></div>
 </div>"""),
 buttons(("export", "Export data", "secondary"), ("clear", "Delete all habits", "ghost"), ("share", "Share tool", "ghost")),
 label="Habit tracker",
 ),
 info_block=info(
 features=[
 "Unlimited habits with a streak grid each",
 "Current streak and longest streak",
 "Completion percentage over the visible period",
 "30, 60 or 90-day views",
 "Data stays on your device",
 ],
 howto=[
 "Add a habit you want to build.",
 "Click today's square when you complete it.",
 "Watch the streak build across the grid.",
 "Export the data if you want to keep it.",
 ],
 background_title="What the research actually says about habits",
 background_paragraphs=[
 "The widely repeated claim that habits take 21 days comes from a misreading of a 1960 book by a plastic surgeon, who observed that patients took about 21 days to adjust to a changed appearance. The actual research is less tidy: a 2009 study by Phillippa Lally at UCL found habits took a median of 66 days to become automatic, with a range from 18 to 254 days depending on the person and the complexity of the behaviour.",
 "The same study found something more useful than the number. Missing a single day had no measurable effect on eventual automaticity. The all-or-nothing framing that a broken streak ruins everything is not supported by evidence, and it is actively counterproductive if it causes people to abandon a habit after one lapse. The grid here shows longest streak alongside current streak partly for this reason.",
 "What does reliably help is making the behaviour easy to start and tying it to an existing routine. Implementation intentions, deciding in advance exactly when and where you will do something, roughly double follow-through in controlled studies. Tracking itself helps too, but mostly through attention rather than motivation: a visible record makes the gap between intention and behaviour hard to ignore.",
 ],
 ),
 script=r""" let habits = T.store.get('habit-tracker', []);

 const COLOURS = ['#00D4FF', '#00FF88', '#FF6B35', '#A855F7', '#F472B6', '#FFD700'];

 function save() {
 T.store.set('habit-tracker', habits);
 }

 function dateKey(offsetDays = 0) {
 const date = new Date();
 date.setHours(12, 0, 0, 0); // midday avoids DST edge cases
 date.setDate(date.getDate() - offsetDays);
 return date.toISOString().slice(0, 10);
 }

 function lastNDays(n) {
 return Array.from({ length: n }, (_, i) => dateKey(n - 1 - i));
 }

 /** Current streak, counting back from today. */
 function currentStreak(habit) {
 let streak = 0;
 for (let i = 0; i < 400; i++) {
 const key = dateKey(i);
 if (habit.days[key]) streak++;
 else if (i > 0) break; // today not yet ticked is not a broken streak
 else if (i === 0) continue;
 }
 return streak;
 }

 function longestStreak(habit) {
 const days = Object.keys(habit.days).filter((k) => habit.days[k]).sort();
 if (!days.length) return 0;

 let best = 1;
 let run = 1;

 for (let i = 1; i < days.length; i++) {
 const previous = new Date(days[i - 1] + 'T12:00:00');
 const current = new Date(days[i] + 'T12:00:00');
 const gap = Math.round((current - previous) / 86400000);

 if (gap === 1) { run++; best = Math.max(best, run); }
 else run = 1;
 }

 return best;
 }

 function render() {
 const mount = T.$('habits');
 mount.innerHTML = '';

 if (!habits.length) {
 mount.append(el('div', { className: 'empty-state' }, [
 el('div', { className: 'empty-state__icon', text: '📈', attrs: { 'aria-hidden': 'true' } }),
 el('p', { text: 'No habits yet. Add one above to start tracking.' })
 ]));
 T.status('status', 'Add a habit to start tracking.', 'muted');
 return;
 }

 const days = lastNDays(Number(T.$('range').value));
 const today = dateKey(0);

 habits.forEach((habit, index) => {
 const colour = COLOURS[index % COLOURS.length];
 const panel = el('div', { className: 'info-panel mb-4' });

 const completed = days.filter((d) => habit.days[d]).length;
 const percentage = Math.round((completed / days.length) * 100);

 const head = el('div', { className: 'flex items-center justify-between gap-4 mb-4 flex-wrap' }, [
 el('div', {}, [
 el('strong', { text: habit.name, style: { fontSize: 'var(--text-lg)', color: colour } }),
 el('div', { className: 'text-xs text-muted mt-1',
 text: `${currentStreak(habit)} day streak · longest ${longestStreak(habit)} · ${percentage}% over ${days.length} days` })
 ])
 ]);

 const remove = el('button', {
 className: 'btn btn--ghost btn--sm',
 attrs: { type: 'button', 'aria-label': `Delete habit “${habit.name}”` },
 text: '✕'
 });
 remove.addEventListener('click', () => {
 habits.splice(index, 1);
 save();
 render();
 });
 head.append(remove);
 panel.append(head);

 // The grid itself
 const grid = el('div', {
 style: {
 display: 'grid',
 gridTemplateColumns: `repeat(auto-fill, minmax(18px, 1fr))`,
 gap: '4px'
 }
 });

 days.forEach((day) => {
 const done = Boolean(habit.days[day]);
 const date = new Date(day + 'T12:00:00');
 const isWeekend = [0, 6].includes(date.getDay());
 const isToday = day === today;

 const square = el('button', {
 attrs: {
 type: 'button',
 'aria-pressed': String(done),
 'aria-label': `${habit.name} on ${date.toLocaleDateString()}: ${done ? 'done' : 'not done'}`,
 title: date.toLocaleDateString(undefined, { weekday: 'short', day: 'numeric', month: 'short' })
 },
 style: {
 aspectRatio: '1',
 minHeight: '18px',
 borderRadius: '4px',
 cursor: 'pointer',
 border: isToday ? `2px solid ${colour}` : '1px solid var(--border-color)',
 background: done
 ? colour
 : (isWeekend && T.$('weekends').checked
 ? 'color-mix(in srgb, var(--text-muted) 12%, transparent)'
 : 'var(--bg-surface)'),
 padding: '0'
 }
 });

 square.addEventListener('click', () => {
 if (habit.days[day]) delete habit.days[day];
 else habit.days[day] = true;
 save();
 render();
 });

 grid.append(square);
 });

 panel.append(grid);
 mount.append(panel);
 });

 const doneToday = habits.filter((h) => h.days[today]).length;
 T.status('status',
 `${doneToday} of ${habits.length} habit(s) done today.`,
 doneToday === habits.length ? 'ok' : 'muted');
 }

 function addHabit() {
 const name = T.$('new-habit').value.trim();
 if (!name) {
 T.status('status', 'Give the habit a name first.', 'warn');
 return;
 }

 habits.push({ id: Date.now(), name, days: {}, created: dateKey(0) });
 save();
 T.$('new-habit').value = '';
 render();
 T.$('new-habit').focus();

 if (window.Analytics) Analytics.trackToolUse('habit-tracker');
 }

 T.$('add').addEventListener('click', addHabit);
 T.$('new-habit').addEventListener('keydown', (e) => {
 if (e.key === 'Enter') { e.preventDefault(); addHabit(); }
 });

 T.on(['range', 'weekends'], render, 'change');

 T.$('export').addEventListener('click', () => {
 if (!habits.length) { toast({ type: 'warning', title: 'Nothing to export' }); return; }
 downloadFile(JSON.stringify(habits, null, 2), 'habits.json', 'application/json');
 });

 T.$('clear').addEventListener('click', () => {
 if (!habits.length) return;
 habits = [];
 save();
 render();
 toast({ type: 'success', title: 'All habits deleted' });
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Habit Tracker | 123MiniApps' }));

 render();""",
))

# ---------------------------------------------------------------
# 89. Meeting Cost Calculator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="meeting-cost-calculator", name="Meeting Cost Calculator", icon="💼", cat="productivity",
 title="Meeting Cost Calculator: Live Cost While You Sit There",
 description="Watch what a meeting costs in real time based on attendee salaries, with an annualised projection for recurring meetings.",
 tagline="Watch a meeting's cost tick upward in real time, and see what the recurring version costs annually.",
 workspace=ws(
 row(
 number_input("attendees", "Attendees", "6", "6", step="1", min=1, max=500),
 number_input("salary", "Average annual salary", "65000", "65000"),
 select("currency", "Currency", [
 ("GBP", "GBP £"), ("USD", "USD $"), ("EUR", "EUR €"),
 ("AUD", "AUD $"), ("CAD", "CAD $"), ("INR", "INR ₹"),
 ], selected="GBP"),
 ),
 row(
 number_input("hours-per-year", "Working hours per year", "1800", "1800"),
 number_input("overhead", "Overhead multiplier", "1.3", "1.3"),
 number_input("duration", "Scheduled duration (minutes)", "60", "60", step="5"),
 ),
 html_block(""" <div class="display">
 <span class="display__value" id="cost">, </span>
 <span class="display__label" id="elapsed">Press Start when the meeting begins</span>
 </div>"""),
 buttons(("start", "Start", "primary"), ("pause", "Pause"), ("reset", "Reset"), ("share", "Share tool", "ghost")),
 status_line("status", "Enter the attendee count and average salary."),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result"><span class="result__value" id="r-rate" style="font-size:var(--text-2xl)">, </span><span class="result__label">Cost per minute</span></div>
 <div class="result"><span class="result__value" id="r-scheduled" style="font-size:var(--text-2xl)">, </span><span class="result__label">Scheduled cost</span></div>
 <div class="result"><span class="result__value" id="r-weekly" style="font-size:var(--text-2xl)">, </span><span class="result__label">If weekly, per year</span></div>
 <div class="result"><span class="result__value" id="r-hours" style="font-size:var(--text-2xl)">, </span><span class="result__label">Person-hours consumed</span></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Comparison</span></span>
 <div class="table-scroll"><div id="comparison"></div></div>
 </div>"""),
 label="Meeting cost calculator",
 ),
 info_block=info(
 features=[
 "Live cost ticking upward during the meeting",
 "Overhead multiplier for true employment cost",
 "Annualised projection for recurring meetings",
 "Six currencies",
 "Comparison against the scheduled duration",
 ],
 howto=[
 "Enter how many people are attending and their average salary.",
 "Press Start when the meeting actually begins.",
 "Watch the cost accumulate.",
 "Check the annual figure if this meeting recurs.",
 ],
 background_title="Reading these numbers honestly",
 background_paragraphs=[
 "Salary alone understates what an employee costs. Employer pension contributions, national insurance or payroll taxes, equipment, software licences, office space and benefits typically add 25% to 40% on top, which is what the overhead multiplier accounts for. The default of 1.3 is a reasonable middle estimate for a knowledge worker; check your own finance team's figure if you have access to it.",
 "The annualised number is usually the one that changes behaviour. A weekly hour-long meeting with eight people is not an hour, it is over 400 person-hours a year, which is a quarter of a full-time role. That framing tends to prompt better questions than the per-meeting figure: does everyone need to be there, could it be fortnightly, could the status update be a written summary?",
 "One caveat worth stating plainly. Cost is not the same as value, and a tool like this can encourage a false precision. Meetings that build alignment, surface a problem early or resolve something that would otherwise take a week of asynchronous back-and-forth are often worth far more than they cost. The useful application is spotting the recurring meeting nobody can justify, not treating every conversation as an expense to be minimised.",
 ],
 ),
 script=r""" let startedAt = null;
 let accumulated = 0; // milliseconds of elapsed meeting time
 let running = false;
 let ticker = null;

 function currency() { return T.$('currency').value; }

 function money(value) {
 try {
 return Number(value).toLocaleString(undefined, {
 style: 'currency', currency: currency(), maximumFractionDigits: 2
 });
 } catch {
 return T.fmt(value, 2);
 }
 }

 /** Fully-loaded cost per minute for the whole room. */
 function costPerMinute() {
 const attendees = Math.max(1, Math.floor(T.num(T.$('attendees').value) || 1));
 const salary = T.num(T.$('salary').value) || 0;
 const hoursPerYear = Math.max(1, T.num(T.$('hours-per-year').value) || 1800);
 const overhead = T.num(T.$('overhead').value) || 1;

 const hourlyPerPerson = (salary * overhead) / hoursPerYear;
 return (hourlyPerPerson * attendees) / 60;
 }

 function elapsedMs() {
 return running ? accumulated + (Date.now() - startedAt) : accumulated;
 }

 function update() {
 const perMinute = costPerMinute();
 const ms = elapsedMs();
 const minutes = ms / 60000;

 T.$('cost').textContent = money(perMinute * minutes);

 const seconds = Math.floor(ms / 1000);
 T.$('elapsed').textContent = running || ms > 0
 ? `${T.pad2(Math.floor(seconds / 3600))}:${T.pad2(Math.floor((seconds % 3600) / 60))}:${T.pad2(seconds % 60)} elapsed`
 : 'Press Start when the meeting begins';

 T.$('r-rate').textContent = money(perMinute);

 const scheduled = T.num(T.$('duration').value) || 0;
 T.$('r-scheduled').textContent = money(perMinute * scheduled);
 T.$('r-weekly').textContent = money(perMinute * scheduled * 52);

 const attendees = Math.max(1, Math.floor(T.num(T.$('attendees').value) || 1));
 T.$('r-hours').textContent = T.fmt((minutes * attendees) / 60, 1);

 // Flag when the meeting overruns
 if (running && scheduled > 0 && minutes > scheduled) {
 const over = minutes - scheduled;
 T.status('status',
 `Running ${Math.round(over)} minute(s) over, that overrun alone has cost ${money(perMinute * over)}.`,
 'warn');
 T.$('cost').style.color = 'var(--danger)';
 } else if (running) {
 T.$('cost').style.color = '';
 }

 renderComparison(perMinute, scheduled, attendees);
 }

 function renderComparison(perMinute, scheduled, attendees) {
 const mount = T.$('comparison');
 mount.innerHTML = '';

 const rows = [
 ['This meeting, as scheduled', `${scheduled} min`, money(perMinute * scheduled)],
 ['If it runs 15 minutes over', `${scheduled + 15} min`, money(perMinute * (scheduled + 15))],
 ['If you cut it to 30 minutes', '30 min', money(perMinute * 30)],
 ['If two people skip it', `${scheduled} min`,
 money((perMinute / attendees) * Math.max(1, attendees - 2) * scheduled)],
 ['Weekly for a year', `${scheduled * 52} min`, money(perMinute * scheduled * 52)],
 ['Daily for a year (250 days)', `${scheduled * 250} min`, money(perMinute * scheduled * 250)]
 ];

 mount.append(T.table(['Scenario', 'Duration', 'Cost'], rows));
 }

 function start() {
 if (running) return;
 startedAt = Date.now();
 running = true;
 clearInterval(ticker);
 ticker = setInterval(update, 200);
 update();
 T.status('status', 'Counting. The cost updates every fifth of a second.', 'ok');
 if (window.Analytics) Analytics.trackToolUse('meeting-cost-calculator');
 }

 function pause() {
 if (!running) return;
 accumulated += Date.now() - startedAt;
 running = false;
 clearInterval(ticker);
 update();
 T.status('status', `Paused at ${money(costPerMinute() * (accumulated / 60000))}.`, 'warn');
 }

 function reset() {
 running = false;
 clearInterval(ticker);
 accumulated = 0;
 startedAt = null;
 T.$('cost').style.color = '';
 update();
 T.status('status', 'Reset.', 'muted');
 }

 T.$('start').addEventListener('click', start);
 T.$('pause').addEventListener('click', pause);
 T.$('reset').addEventListener('click', reset);

 T.on(['attendees', 'salary', 'hours-per-year', 'overhead', 'duration'], update);
 T.on(['currency'], update, 'change');

 T.$('share').addEventListener('click', () => shareLink({ title: 'Meeting Cost Calculator | 123MiniApps' }));

 update();""",
))
