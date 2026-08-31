#!/usr/bin/env python3
# ============================================
# 123MiniApps.online v2.0
# File: tools_calculator.py
# Purpose: The 10 Calculators (ids 55-64).
#
# NOTE: every financial tool here carries an explicit
# "this is an estimate, not advice" line in its info
# panel. That is deliberate and should stay.
# ============================================

from toolkit import (
 tool, ws, info, row, text_input, number_input, select, switch, slider,
 output, status_line, buttons, HR, html_block,
)

PAGES = []

# ---------------------------------------------------------------
# 55. Percentage Calculator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="percentage-calculator", name="Percentage Calculator", icon="％", cat="calculator",
 title="Percentage Calculator: Increase, Decrease and Difference",
 description="Work out percentages five ways: of a number, increase, decrease, what percent one number is of another, and reverse percentages.",
 tagline="Five percentage calculations, each with the working shown.",
 workspace=ws(
 select("mode", "What do you want to work out?", [
 ("of", "What is X% of Y?"),
 ("what", "X is what percent of Y?"),
 ("change", "Percentage change from X to Y"),
 ("increase", "Increase X by Y%"),
 ("decrease", "Decrease X by Y%"),
 ("reverse", "X is Y% of what number?"),
 ], selected="of"),
 row(
 number_input("a", "First value", "25", "25"),
 number_input("b", "Second value", "200", "200"),
 ),
 status_line("status", "Enter two values."),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result result--primary"><span class="result__value" id="r-main">, </span><span class="result__label" id="r-label">Result</span></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Working</span></span>
 <div class="output" id="working">The calculation will be shown here.</div>
 </div>"""),
 buttons(("copy", "Copy result", "primary"), ("swap", "Swap values"), ("share", "Share tool", "ghost")),
 label="Percentage calculator",
 ),
 info_block=info(
 features=[
 "Six calculation modes covering every common case",
 "Step-by-step working shown for each result",
 "Handles negatives and decimals",
 "Reverse percentages for working back from a total",
 "Distinguishes percentage change from percentage points",
 ],
 howto=[
 "Choose which calculation you need.",
 "Enter the two values.",
 "Read the result and the working below it.",
 "Copy the answer when you are done.",
 ],
 background_title="Percentage change and percentage points",
 background_paragraphs=[
 "The most common percentage mistake is treating an increase and its matching decrease as symmetrical. They are not. A price rising from 100 to 150 is a 50% increase, but falling from 150 back to 100 is a 33.3% decrease, because the base changed. Percentage change is always relative to the starting value, so the direction matters.",
 "Compounding decreases catches people the same way. Two successive 50% discounts do not make the item free; they make it 25% of the original price, since the second discount applies to the already-reduced amount. A 20% rise followed by a 20% fall leaves you at 96% of where you started, not 100%.",
 "Percentage points are a separate unit and confusing them is a genuine error, not just imprecision. If an interest rate moves from 4% to 6%, that is a rise of 2 percentage points, but a 50% increase in the rate. News reports that conflate the two can overstate or understate a change by a large factor. When the quantity being measured is itself a percentage, always say which you mean.",
 ],
 ),
 script=r""" const MODES = {
 of: {
 labels: ['Percentage (%)', 'Of what number'],
 result: 'Result',
 calc: (a, b) => (a / 100) * b,
 show: (a, b, r) => `${a}% of ${T.fmt(b)}\n= (${a} ÷ 100) × ${T.fmt(b)}\n= ${T.fmt(a / 100, 4)} × ${T.fmt(b)}\n= ${T.fmt(r)}`
 },
 what: {
 labels: ['This number', 'Is what percent of'],
 result: 'Percentage',
 calc: (a, b) => (a / b) * 100,
 suffix: '%',
 show: (a, b, r) => `${T.fmt(a)} as a percentage of ${T.fmt(b)}\n= (${T.fmt(a)} ÷ ${T.fmt(b)}) × 100\n= ${T.fmt(r, 4)}%`
 },
 change: {
 labels: ['From (original)', 'To (new)'],
 result: 'Change',
 calc: (a, b) => ((b - a) / Math.abs(a)) * 100,
 suffix: '%',
 show: (a, b, r) => {
 const dir = r >= 0 ? 'increase' : 'decrease';
 return `Change from ${T.fmt(a)} to ${T.fmt(b)}\n` +
 `= ((${T.fmt(b)} − ${T.fmt(a)}) ÷ ${T.fmt(Math.abs(a))}) × 100\n` +
 `= (${T.fmt(b - a)} ÷ ${T.fmt(Math.abs(a))}) × 100\n` +
 `= ${T.fmt(Math.abs(r), 4)}% ${dir}`;
 }
 },
 increase: {
 labels: ['Starting value', 'Increase by (%)'],
 result: 'New value',
 calc: (a, b) => a * (1 + b / 100),
 show: (a, b, r) => `${T.fmt(a)} increased by ${b}%\n= ${T.fmt(a)} × (1 + ${b} ÷ 100)\n= ${T.fmt(a)} × ${T.fmt(1 + b / 100, 4)}\n= ${T.fmt(r)}\n\nAmount added: ${T.fmt(r - a)}`
 },
 decrease: {
 labels: ['Starting value', 'Decrease by (%)'],
 result: 'New value',
 calc: (a, b) => a * (1 - b / 100),
 show: (a, b, r) => `${T.fmt(a)} decreased by ${b}%\n= ${T.fmt(a)} × (1 − ${b} ÷ 100)\n= ${T.fmt(a)} × ${T.fmt(1 - b / 100, 4)}\n= ${T.fmt(r)}\n\nAmount removed: ${T.fmt(a - r)}`
 },
 reverse: {
 labels: ['This number', 'Is this percent (%)'],
 result: 'Original number',
 calc: (a, b) => (a / b) * 100,
 show: (a, b, r) => `If ${T.fmt(a)} is ${b}% of a number\n= (${T.fmt(a)} ÷ ${b}) × 100\n= ${T.fmt(r)}\n\nCheck: ${b}% of ${T.fmt(r)} = ${T.fmt((b / 100) * r)}`
 }
 };

 let lastResult = '';

 function syncLabels() {
 const mode = MODES[T.$('mode').value];
 T.$('a').closest('.field').querySelector('span').textContent = mode.labels[0];
 T.$('b').closest('.field').querySelector('span').textContent = mode.labels[1];
 T.$('r-label').textContent = mode.result;
 calculate();
 }

 function calculate() {
 const a = T.num(T.$('a').value);
 const b = T.num(T.$('b').value);
 const mode = MODES[T.$('mode').value];

 if (isNaN(a) || isNaN(b)) {
 T.$('r-main').textContent = ', ';
 T.setOutput('working', '', 'The calculation will be shown here.');
 T.status('status', 'Enter two values.', 'muted');
 return;
 }

 if (b === 0 && ['what', 'reverse'].includes(T.$('mode').value)) {
 T.status('status', 'Cannot divide by zero.', 'error');
 T.$('r-main').textContent = ', ';
 return;
 }

 if (a === 0 && T.$('mode').value === 'change') {
 T.status('status', 'Percentage change from zero is undefined.', 'error');
 T.$('r-main').textContent = ', ';
 return;
 }

 const result = mode.calc(a, b);
 const suffix = mode.suffix || '';

 lastResult = T.fmt(result, Math.abs(result) < 1 ? 4 : 2) + suffix;
 T.$('r-main').textContent = lastResult;
 T.setOutput('working', mode.show(a, b, result));
 T.status('status', `${mode.result}: ${lastResult}`, 'ok');
 }

 T.on(['a', 'b'], calculate);
 T.$('mode').addEventListener('change', syncLabels);

 T.$('swap').addEventListener('click', () => {
 const a = T.$('a').value;
 T.$('a').value = T.$('b').value;
 T.$('b').value = a;
 calculate();
 });

 T.$('copy').addEventListener('click', () => copyToClipboard(lastResult, 'Result copied'));
 T.$('share').addEventListener('click', () => shareLink({ title: 'Percentage Calculator | 123MiniApps' }));

 syncLabels();
 if (window.Analytics) Analytics.trackToolUse('percentage-calculator');""",
))

# ---------------------------------------------------------------
# 56. Loan Calculator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="loan-calculator", name="Loan Calculator", icon="🏦", cat="calculator",
 title="Loan Calculator: Monthly Payment and Amortization Schedule",
 description="Estimate monthly loan payments, total interest and see a full amortization schedule. Model extra payments to see how much interest they save.",
 tagline="Estimate monthly payments and total interest, with a full amortization schedule.",
 workspace=ws(
 row(
 number_input("principal", "Loan amount", "250000", "250000"),
 number_input("rate", "Annual interest rate (%)", "5.5", "5.5"),
 number_input("years", "Term (years)", "25", "25"),
 ),
 row(
 number_input("extra", "Extra monthly payment", "0", "0"),
 select("frequency", "Payment frequency", [
 ("12", "Monthly"), ("26", "Fortnightly"), ("52", "Weekly"),
 ], selected="12"),
 ),
 status_line("status", "Enter your loan details."),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result result--primary"><span class="result__value" id="r-payment">, </span><span class="result__label">Payment</span></div>
 <div class="result"><span class="result__value" id="r-total">, </span><span class="result__label">Total repaid</span></div>
 <div class="result"><span class="result__value" id="r-interest">, </span><span class="result__label">Total interest</span></div>
 <div class="result"><span class="result__value" id="r-payoff">, </span><span class="result__label">Paid off in</span></div>
 </div>"""),
 html_block(""" <div id="savings" class="field" hidden>
 <div class="result result--primary" style="text-align:left;padding:var(--space-5)">
 <span id="savings-text"></span>
 </div>
 </div>"""),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Amortization schedule</span><span class="field__hint">Yearly summary</span></span>
 <div class="table-scroll"><div id="schedule"></div></div>
 </div>"""),
 buttons(("copy", "Copy summary", "primary"), ("download", "Download schedule (CSV)"), ("share", "Share tool", "ghost")),
 label="Loan calculator",
 ),
 info_block=info(
 features=[
 "Monthly, fortnightly or weekly payment schedules",
 "Full amortization table summarised by year",
 "Extra-payment modelling with interest saved",
 "Total repaid and total interest breakdown",
 "Exports the schedule as CSV",
 ],
 howto=[
 "Enter the loan amount, rate and term.",
 "Add an extra payment amount to see its effect.",
 "Read the payment and total interest above.",
 "Download the schedule if you need it in a spreadsheet.",
 ],
 background_title="How amortization actually works",
 background_paragraphs=[
 "An amortizing loan uses a fixed payment split between interest and principal, but the split shifts over time. Interest is charged on the outstanding balance, so early payments are mostly interest and barely dent the principal. On a 25-year mortgage at 5.5%, roughly 70% of the first payment is interest; by the final year that has fallen below 5%. This is why a loan's balance drops slowly at first and then accelerates.",
 "It is also why extra payments are disproportionately effective early on. Any additional amount goes entirely to principal, which removes all the future interest that balance would have generated. Paying an extra 10% each month on a typical 25-year mortgage often cuts four to five years off the term and saves a substantial multiple of what you actually paid in.",
 "Two caveats on the numbers here. This calculates a straightforward amortizing loan and does not include property taxes, insurance, arrangement fees or mortgage insurance, all of which can add materially to what you actually pay each month. And it assumes a fixed rate for the whole term, a variable or tracker rate will diverge from these figures as soon as the rate moves.",
 ],
 ),
 script=r""" let schedule = [];
 let summary = '';

 /**
 * Build the full payment schedule.
 * @returns {{payments: Object[], totalInterest: number, periods: number}}
 */
 function amortize(principal, annualRate, years, perYear, extra) {
 const periodRate = annualRate / 100 / perYear;
 const totalPeriods = Math.round(years * perYear);

 // Standard amortization formula; the zero-rate case degenerates to
 // simple division, which the formula cannot express.
 const payment = periodRate === 0
 ? principal / totalPeriods
 : (principal * periodRate) / (1 - Math.pow(1 + periodRate, -totalPeriods));

 const payments = [];
 let balance = principal;
 let totalInterest = 0;
 let period = 0;

 // Cap the loop so a pathological input cannot hang the tab
 const MAX_PERIODS = totalPeriods * 2 + 1200;

 while (balance > 0.005 && period < MAX_PERIODS) {
 period++;
 const interest = balance * periodRate;
 let principalPart = payment + extra - interest;

 // Final payment: never overshoot the remaining balance
 if (principalPart > balance) principalPart = balance;

 balance -= principalPart;
 totalInterest += interest;

 payments.push({
 period,
 payment: principalPart + interest,
 interest,
 principal: principalPart,
 balance: Math.max(0, balance)
 });
 }

 return { payment, payments, totalInterest, periods: period };
 }

 function describeTerm(periods, perYear) {
 const years = Math.floor(periods / perYear);
 const rem = Math.round(periods % perYear);
 const unit = perYear === 12 ? 'month' : perYear === 26 ? 'fortnight' : 'week';
 return `${years} yr${rem ? ` ${rem} ${unit}${rem === 1 ? '' : 's'}` : ''}`;
 }

 function calculate() {
 const principal = T.num(T.$('principal').value);
 const rate = T.num(T.$('rate').value);
 const years = T.num(T.$('years').value);
 const extra = T.num(T.$('extra').value) || 0;
 const perYear = Number(T.$('frequency').value);

 if (isNaN(principal) || isNaN(rate) || isNaN(years) || principal <= 0 || years <= 0) {
 T.status('status', 'Enter a loan amount, rate and term.', 'muted');
 return;
 }

 if (rate < 0 || rate > 100) {
 T.status('status', 'Enter an interest rate between 0 and 100.', 'error');
 return;
 }

 const result = amortize(principal, rate, years, perYear, extra);
 schedule = result.payments;

 const totalPaid = principal + result.totalInterest;

 T.$('r-payment').textContent = T.money(result.payment + extra);
 T.$('r-total').textContent = T.money(totalPaid);
 T.$('r-interest').textContent = T.money(result.totalInterest);
 T.$('r-payoff').textContent = describeTerm(result.periods, perYear);

 // Compare against the no-extra-payment baseline
 if (extra > 0) {
 const base = amortize(principal, rate, years, perYear, 0);
 const saved = base.totalInterest - result.totalInterest;
 const periodsSaved = base.periods - result.periods;

 T.$('savings').hidden = false;
 T.$('savings-text').innerHTML =
 `Paying an extra <strong>${T.esc(T.money(extra))}</strong> each period saves ` +
 `<strong>${T.esc(T.money(saved))}</strong> in interest and clears the loan ` +
 `<strong>${T.esc(describeTerm(periodsSaved, perYear))}</strong> earlier.`;
 } else {
 T.$('savings').hidden = true;
 }

 renderSchedule(perYear);

 summary = [
 `Loan amount: ${T.money(principal)}`,
 `Interest rate: ${rate}%`,
 `Term: ${years} years`,
 `Payment: ${T.money(result.payment + extra)}`,
 `Total repaid: ${T.money(totalPaid)}`,
 `Total interest: ${T.money(result.totalInterest)}`,
 `Paid off in: ${describeTerm(result.periods, perYear)}`
 ].join('\n');

 const ratio = (result.totalInterest / principal) * 100;
 T.status('status',
 `Interest costs ${T.fmt(ratio, 1)}% of the amount borrowed.`,
 ratio > 60 ? 'warn' : 'ok');
 }

 function renderSchedule(perYear) {
 const mount = T.$('schedule');
 mount.innerHTML = '';
 if (!schedule.length) return;

 // Roll periods up into years so the table stays readable
 const rows = [];
 for (let start = 0; start < schedule.length; start += perYear) {
 const chunk = schedule.slice(start, start + perYear);
 const year = Math.floor(start / perYear) + 1;
 rows.push([
 'Year ' + year,
 T.money(chunk.reduce((n, p) => n + p.payment, 0)),
 T.money(chunk.reduce((n, p) => n + p.principal, 0)),
 T.money(chunk.reduce((n, p) => n + p.interest, 0)),
 T.money(chunk[chunk.length - 1].balance)
 ]);
 }

 mount.append(T.table(['Period', 'Paid', 'Principal', 'Interest', 'Balance'], rows));
 }

 T.on(['principal', 'rate', 'years', 'extra'], debounce(calculate, 200));
 T.on(['frequency'], calculate, 'change');

 T.$('copy').addEventListener('click', () => copyToClipboard(summary, 'Summary copied'));

 T.$('download').addEventListener('click', () => {
 if (!schedule.length) {
 toast({ type: 'warning', title: 'Nothing to download' });
 return;
 }
 const csv = ['Period,Payment,Principal,Interest,Balance']
 .concat(schedule.map((p) =>
 [p.period, p.payment.toFixed(2), p.principal.toFixed(2), p.interest.toFixed(2), p.balance.toFixed(2)].join(',')))
 .join('\n');
 downloadFile(csv, 'amortization-schedule.csv', 'text/csv');
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Loan Calculator | 123MiniApps' }));

 calculate();
 if (window.Analytics) Analytics.trackToolUse('loan-calculator');""",
))

# ---------------------------------------------------------------
# 57. BMI Calculator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="bmi-calculator", name="BMI Calculator", icon="⚖️", cat="calculator",
 title="BMI Calculator: Metric and Imperial with WHO Categories",
 description="Calculate body mass index in metric or imperial units, with WHO category ranges and the healthy weight range for your height.",
 tagline="Calculate BMI in metric or imperial, with the healthy weight range for your height.",
 workspace=ws(
 select("units", "Units", [("metric", "Metric, cm and kg"), ("imperial", "Imperial, ft/in and lb")], selected="metric"),
 html_block(""" <div class="workspace__row" id="metric-fields">
 <div class="field">
 <label class="field__label" for="height-cm"><span>Height (cm)</span></label>
 <input class="input" id="height-cm" type="number" value="175" step="any" inputmode="decimal">
 </div>
 <div class="field">
 <label class="field__label" for="weight-kg"><span>Weight (kg)</span></label>
 <input class="input" id="weight-kg" type="number" value="70" step="any" inputmode="decimal">
 </div>
 </div>"""),
 html_block(""" <div class="workspace__row" id="imperial-fields" hidden>
 <div class="field">
 <label class="field__label" for="height-ft"><span>Height (feet)</span></label>
 <input class="input" id="height-ft" type="number" value="5" step="1" inputmode="numeric">
 </div>
 <div class="field">
 <label class="field__label" for="height-in"><span>Height (inches)</span></label>
 <input class="input" id="height-in" type="number" value="9" step="any" inputmode="decimal">
 </div>
 <div class="field">
 <label class="field__label" for="weight-lb"><span>Weight (pounds)</span></label>
 <input class="input" id="weight-lb" type="number" value="154" step="any" inputmode="decimal">
 </div>
 </div>"""),
 status_line("status", "Enter your height and weight."),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result result--primary"><span class="result__value" id="r-bmi">, </span><span class="result__label">Body mass index</span></div>
 <div class="result"><span class="result__value" id="r-category" style="font-size:var(--text-xl)">, </span><span class="result__label">WHO category</span></div>
 <div class="result"><span class="result__value" id="r-healthy" style="font-size:var(--text-xl)">, </span><span class="result__label">Healthy weight range</span></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>WHO categories</span></span>
 <div class="table-scroll"><div id="categories"></div></div>
 </div>"""),
 buttons(("copy", "Copy result", "primary"), ("share", "Share tool", "ghost")),
 label="BMI calculator",
 ),
 info_block=info(
 features=[
 "Metric and imperial input",
 "WHO category classification",
 "Healthy weight range calculated for your height",
 "Full category table with your position marked",
 "Nothing is stored or transmitted",
 ],
 howto=[
 "Choose metric or imperial units.",
 "Enter your height and weight.",
 "Read your BMI and category.",
 "The healthy range shows target weights for your height.",
 ],
 background_title="What BMI does and does not tell you",
 background_paragraphs=[
 "BMI is weight in kilograms divided by height in metres squared. It was devised in the 1830s by Adolphe Quetelet as a way of describing populations, not individuals, and that origin explains most of its limitations. It is a cheap, reproducible screening measure that correlates reasonably with body fat across large groups.",
 "For any specific person it can be quite wrong, because it cannot distinguish muscle from fat or account for where fat is distributed. Muscular athletes routinely score in the overweight or obese range while carrying very little body fat. Older adults may lose muscle while gaining fat and keep the same BMI throughout. The thresholds were derived largely from European populations, and health risks rise at lower BMI values for people of South Asian, Chinese and other ancestries, several health bodies use a lower overweight threshold of 23 for these groups.",
 "BMI also tells you nothing about visceral fat, which is the type most strongly linked to metabolic risk. Waist circumference and waist-to-height ratio are better single predictors of cardiovascular risk than BMI. Treat the number here as one rough data point among several, and speak to a doctor rather than drawing conclusions from it, this tool is informational and is not medical advice.",
 ],
 ),
 script=r""" const CATEGORIES = [
 ['Underweight (severe)', 0, 16, 'var(--danger)'],
 ['Underweight (moderate)', 16, 17, 'var(--warning)'],
 ['Underweight (mild)', 17, 18.5, 'var(--warning)'],
 ['Healthy weight', 18.5, 25, 'var(--success)'],
 ['Overweight', 25, 30, 'var(--warning)'],
 ['Obese (class I)', 30, 35, 'var(--danger)'],
 ['Obese (class II)', 35, 40, 'var(--danger)'],
 ['Obese (class III)', 40, Infinity, 'var(--danger)']
 ];

 let lastResult = '';

 function syncUnits() {
 const metric = T.$('units').value === 'metric';
 T.$('metric-fields').hidden = !metric;
 T.$('imperial-fields').hidden = metric;
 calculate();
 }

 /** @returns {{heightM: number, weightKg: number}|null} */
 function readInputs() {
 if (T.$('units').value === 'metric') {
 const cm = T.num(T.$('height-cm').value);
 const kg = T.num(T.$('weight-kg').value);
 if (isNaN(cm) || isNaN(kg)) return null;
 return { heightM: cm / 100, weightKg: kg };
 }

 const ft = T.num(T.$('height-ft').value) || 0;
 const inch = T.num(T.$('height-in').value) || 0;
 const lb = T.num(T.$('weight-lb').value);
 if (isNaN(lb) || (ft === 0 && inch === 0)) return null;

 return {
 heightM: (ft * 12 + inch) * 0.0254,
 weightKg: lb * 0.45359237
 };
 }

 function categoryFor(bmi) {
 return CATEGORIES.find(([, lo, hi]) => bmi >= lo && bmi < hi) || CATEGORIES[CATEGORIES.length - 1];
 }

 function calculate() {
 const inputs = readInputs();

 if (!inputs) {
 T.$('r-bmi').textContent = ', ';
 T.status('status', 'Enter your height and weight.', 'muted');
 return;
 }

 const { heightM, weightKg } = inputs;

 if (heightM <= 0.5 || heightM > 2.7 || weightKg <= 2 || weightKg > 650) {
 T.status('status', 'Those measurements look out of range, please check them.', 'error');
 T.$('r-bmi').textContent = ', ';
 return;
 }

 const bmi = weightKg / (heightM * heightM);
 const [name,, colour] = categoryFor(bmi);

 T.$('r-bmi').textContent = T.fmt(bmi, 1);
 T.$('r-category').textContent = name;
 T.$('r-category').style.color = colour;

 // Healthy range = BMI 18.5 to 24.9 at this height
 const lowKg = 18.5 * heightM * heightM;
 const highKg = 24.9 * heightM * heightM;
 const metric = T.$('units').value === 'metric';

 T.$('r-healthy').textContent = metric
 ? `${T.fmt(lowKg, 1)}–${T.fmt(highKg, 1)} kg`
 : `${T.fmt(lowKg / 0.45359237, 0)}–${T.fmt(highKg / 0.45359237, 0)} lb`;

 renderCategories(bmi);

 lastResult = `BMI ${T.fmt(bmi, 1)}, ${name}. Healthy range for this height: ${T.$('r-healthy').textContent}.`;
 T.status('status', lastResult, 'ok');
 }

 function renderCategories(bmi) {
 const mount = T.$('categories');
 mount.innerHTML = '';

 const rows = CATEGORIES.map(([name, lo, hi]) => [
 name,
 hi === Infinity ? `${lo} and above` : `${lo} – ${hi}`,
 bmi >= lo && bmi < hi ? '← you are here' : ''
 ]);

 const table = T.table(['Category', 'BMI range', ''], rows);

 [...table.querySelectorAll('tbody tr')].forEach((tr, i) => {
 const [, lo, hi] = CATEGORIES[i];
 if (bmi >= lo && bmi < hi) {
 tr.style.background = 'color-mix(in srgb, var(--accent-primary) 14%, transparent)';
 tr.style.fontWeight = 'var(--weight-semibold)';
 }
 });

 mount.append(table);
 }

 T.$('units').addEventListener('change', syncUnits);
 T.on(['height-cm', 'weight-kg', 'height-ft', 'height-in', 'weight-lb'], calculate);

 T.$('copy').addEventListener('click', () => copyToClipboard(lastResult, 'Result copied'));
 T.$('share').addEventListener('click', () => shareLink({ title: 'BMI Calculator | 123MiniApps' }));

 syncUnits();
 if (window.Analytics) Analytics.trackToolUse('bmi-calculator');""",
))

# ---------------------------------------------------------------
# 58. Tip Calculator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="tip-calculator", name="Tip Calculator", icon="💵", cat="calculator",
 title="Tip Calculator: Split a Bill and Work Out the Gratuity",
 description="Calculate the tip and split a bill between any number of people. Adjustable percentage, tax handling and round-up options.",
 tagline="Work out the tip and split the bill, with tax handled the way you choose.",
 workspace=ws(
 row(
 number_input("bill", "Bill amount", "84.50", "84.50"),
 slider("tip", "Tip percentage", 0, 40, 18, 1, unit="%"),
 number_input("people", "Split between", "2", "2", step="1", min=1),
 ),
 row(
 number_input("tax", "Tax already included in bill (%)", "0", "0"),
 switch("tip-pretax", "Tip on the pre-tax amount", False),
 select("rounding", "Rounding", [
 ("none", "No rounding"), ("up", "Round total up to whole"),
 ("perperson", "Round each share up to whole"),
 ], selected="none"),
 ),
 status_line("status", "Enter the bill amount."),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result result--primary"><span class="result__value" id="r-each">, </span><span class="result__label">Each person pays</span></div>
 <div class="result"><span class="result__value" id="r-tip">, </span><span class="result__label">Tip amount</span></div>
 <div class="result"><span class="result__value" id="r-total">, </span><span class="result__label">Total to pay</span></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Quick tip amounts</span></span>
 <div class="chip-grid" id="presets"></div>
 </div>"""),
 buttons(("copy", "Copy breakdown", "primary"), ("share", "Share tool", "ghost")),
 label="Tip calculator",
 ),
 info_block=info(
 features=[
 "Adjustable tip from 0% to 40%",
 "Split between any number of people",
 "Tip on pre-tax or post-tax amount",
 "Round the total or each share up",
 "Quick comparison at common tip percentages",
 ],
 howto=[
 "Enter the bill total.",
 "Slide to your tip percentage.",
 "Set how many people are splitting it.",
 "Read what each person owes.",
 ],
 background_title="Tipping conventions vary enormously",
 background_paragraphs=[
 "In the United States, tipping is effectively part of the wage. Federal law allows a tipped minimum wage well below the standard one on the assumption that tips make up the difference, so 18% to 20% at a sit-down restaurant is the working norm rather than a bonus for exceptional service. Leaving nothing has a direct effect on the server's income.",
 "Most of Europe works differently. Service is generally included by law and staff are paid a full wage, so rounding up or leaving 5% to 10% is generous rather than expected. In Japan and South Korea, tipping is not customary at all and can be actively unwelcome, leaving money on the table may result in a server chasing you down the street to return it.",
 "Two practical details. Whether to tip on the pre-tax or post-tax total is genuinely disputed; tipping pre-tax is defensible since tax is not part of the service, and the difference on a typical bill is small. More significant is checking for an automatic service charge, common for larger groups and increasingly on individual bills, if one has already been added, an additional tip is entirely optional and you are not being rude to skip it.",
 ],
 ),
 script=r""" let breakdown = '';

 function calculate() {
 const bill = T.num(T.$('bill').value);
 const tipPct = Number(T.$('tip').value);
 const people = Math.max(1, Math.floor(T.num(T.$('people').value) || 1));
 const taxPct = T.num(T.$('tax').value) || 0;

 T.$('tip-value').textContent = tipPct;

 if (isNaN(bill) || bill < 0) {
 T.$('r-each').textContent = ', ';
 T.$('r-tip').textContent = ', ';
 T.$('r-total').textContent = ', ';
 T.status('status', 'Enter the bill amount.', 'muted');
 return;
 }

 // If tipping pre-tax, strip the tax out of the bill first
 const tipBase = T.$('tip-pretax').checked && taxPct > 0
 ? bill / (1 + taxPct / 100)
 : bill;

 let tip = tipBase * (tipPct / 100);
 let total = bill + tip;
 let each = total / people;

 const rounding = T.$('rounding').value;
 if (rounding === 'up') {
 total = Math.ceil(total);
 tip = total - bill;
 each = total / people;
 } else if (rounding === 'perperson') {
 each = Math.ceil(each);
 total = each * people;
 tip = total - bill;
 }

 T.$('r-each').textContent = T.money(each);
 T.$('r-tip').textContent = T.money(tip);
 T.$('r-total').textContent = T.money(total);

 renderPresets(bill, tipBase, people);

 breakdown = [
 `Bill: ${T.money(bill)}`,
 `Tip (${tipPct}%): ${T.money(tip)}`,
 `Total: ${T.money(total)}`,
 `Split between ${people}: ${T.money(each)} each`
 ].join('\n');

 T.status('status',
 people > 1
 ? `${T.money(each)} each, including ${T.money(tip / people)} of tip.`
 : `Tip of ${T.money(tip)} on a ${T.money(bill)} bill.`,
 'ok');
 }

 function renderPresets(bill, tipBase, people) {
 const mount = T.$('presets');
 mount.innerHTML = '';

 [10, 15, 18, 20, 25].forEach((pct) => {
 const tip = tipBase * (pct / 100);
 const each = (bill + tip) / people;

 const chip = el('button', {
 className: 'chip',
 attrs: { type: 'button' },
 text: `${pct}% → ${T.money(each)} each`
 });

 chip.addEventListener('click', () => {
 T.$('tip').value = String(pct);
 calculate();
 });

 if (pct === Number(T.$('tip').value)) {
 chip.style.borderColor = 'var(--accent-primary)';
 chip.style.color = 'var(--accent-primary)';
 }

 mount.append(chip);
 });
 }

 T.on(['bill', 'people', 'tax', 'tip'], calculate);
 T.on(['tip-pretax', 'rounding'], calculate, 'change');

 T.$('copy').addEventListener('click', () => copyToClipboard(breakdown, 'Breakdown copied'));
 T.$('share').addEventListener('click', () => shareLink({ title: 'Tip Calculator | 123MiniApps' }));

 calculate();
 if (window.Analytics) Analytics.trackToolUse('tip-calculator');""",
))

# ---------------------------------------------------------------
# 59. Age Calculator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="age-calculator", name="Age Calculator", icon="🎂", cat="calculator",
 title="Age Calculator: Exact Age in Years, Months and Days",
 description="Find an exact age in years, months and days, plus total days lived, the day of the week you were born and a countdown to your next birthday.",
 tagline="Exact age in years, months and days, plus a countdown to the next birthday.",
 workspace=ws(
 row(
 text_input("dob", "Date of birth", "", "1990-06-15", "date"),
 text_input("asof", "Calculate age as of", "", "", "date"),
 ),
 status_line("status", "Pick a date of birth."),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result result--primary"><span class="result__value" id="r-age">, </span><span class="result__label">Age</span></div>
 <div class="result"><span class="result__value" id="r-next" style="font-size:var(--text-xl)">, </span><span class="result__label">Next birthday</span></div>
 <div class="result"><span class="result__value" id="r-born" style="font-size:var(--text-xl)">, </span><span class="result__label">Born on a</span></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Time lived, measured differently</span></span>
 <div class="table-scroll"><div id="units"></div></div>
 </div>"""),
 buttons(("today", "Use today", "primary"), ("copy", "Copy summary"), ("share", "Share tool", "ghost")),
 label="Age calculator",
 ),
 info_block=info(
 features=[
 "Exact age in years, months and days",
 "Total days, weeks, hours and minutes lived",
 "Day of the week you were born",
 "Countdown to the next birthday",
 "Calculate age as of any date, not just today",
 ],
 howto=[
 "Enter the date of birth.",
 "Leave the second date as today, or set another date.",
 "Read the exact age above.",
 "The table shows the same span in other units.",
 ],
 background_title="Why calendar age is harder than subtracting dates",
 background_paragraphs=[
 "Calendar months have different lengths, so “one month later” has no fixed duration. Age is conventionally calculated by counting whole years first, then whole months, then remaining days, which is why someone born on 31 January is a month old on 28 February in a non-leap year, but the arithmetic has to handle that month boundary explicitly rather than dividing by an average month length.",
 "Leap years add their own complications. People born on 29 February have a birthday only once every four years, and different jurisdictions take different views on when they legally turn 18 in non-leap years, some say 28 February, others 1 March. This calculator treats 1 March as the birthday in non-leap years, which is the more common convention but not universal.",
 "There is also a cultural dimension worth knowing. The East Asian age reckoning system, still in informal use in parts of the region, counts a newborn as one year old and adds a year at each lunar new year rather than on the birthday, making someone up to two years older than their international age. South Korea officially moved to international age in 2023, but you will still encounter both.",
 ],
 ),
 script=r""" let summary = '';

 /**
 * Exact calendar difference, counting whole years then months
 * then days, the conventional way age is expressed.
 */
 function exactDiff(from, to) {
 let years = to.getFullYear() - from.getFullYear();
 let months = to.getMonth() - from.getMonth();
 let days = to.getDate() - from.getDate();

 if (days < 0) {
 months--;
 // Borrow from the month preceding `to`. The anchor day must be
 // clamped to that month's length, otherwise a start date of the
 // 31st borrowed against February produces a negative day count.
 const prevMonthDays = new Date(to.getFullYear(), to.getMonth(), 0).getDate();
 const anchorDay = Math.min(from.getDate(), prevMonthDays);
 days = to.getDate() + (prevMonthDays - anchorDay);
 }
 if (months < 0) {
 years--;
 months += 12;
 }

 return { years, months, days };
 }

 function nextBirthday(dob, from) {
 const year = from.getFullYear();
 let next = new Date(year, dob.getMonth(), dob.getDate());

 // 29 February in a non-leap year falls back to 1 March
 if (dob.getMonth() === 1 && dob.getDate() === 29 && next.getMonth() !== 1) {
 next = new Date(year, 2, 1);
 }

 if (next < from) {
 next = new Date(year + 1, dob.getMonth(), dob.getDate());
 if (dob.getMonth() === 1 && dob.getDate() === 29 && next.getMonth() !== 1) {
 next = new Date(year + 1, 2, 1);
 }
 }

 return next;
 }

 function calculate() {
 const dobRaw = T.$('dob').value;
 const asOfRaw = T.$('asof').value;

 if (!dobRaw) {
 T.status('status', 'Pick a date of birth.', 'muted');
 T.$('r-age').textContent = ', ';
 return;
 }

 const dob = new Date(dobRaw + 'T00:00:00');
 const asOf = asOfRaw ? new Date(asOfRaw + 'T00:00:00') : new Date();

 if (isNaN(dob)) {
 T.status('status', 'That date of birth is not valid.', 'error');
 return;
 }

 if (dob > asOf) {
 T.status('status', 'The date of birth is after the comparison date.', 'error');
 T.$('r-age').textContent = ', ';
 return;
 }

 const { years, months, days } = exactDiff(dob, asOf);
 T.$('r-age').textContent = `${years}y ${months}m ${days}d`;

 T.$('r-born').textContent = dob.toLocaleDateString(undefined, { weekday: 'long' });

 const next = nextBirthday(dob, asOf);
 const daysToNext = Math.ceil((next - asOf) / 86400000);
 T.$('r-next').textContent = daysToNext === 0
 ? 'Today! 🎂'
 : `${daysToNext} day${daysToNext === 1 ? '' : 's'}`;

 const ms = asOf - dob;
 const totalDays = Math.floor(ms / 86400000);

 const mount = T.$('units');
 mount.innerHTML = '';
 mount.append(T.table(['Unit', 'Amount'], [
 ['Years', T.fmt(ms / 31557600000, 2)],
 ['Months (average)', T.fmt(ms / 2629800000, 1)],
 ['Weeks', T.fmt(totalDays / 7, 1)],
 ['Days', totalDays.toLocaleString()],
 ['Hours', Math.floor(ms / 3600000).toLocaleString()],
 ['Minutes', Math.floor(ms / 60000).toLocaleString()],
 ['Heartbeats (approx, at 70 bpm)', Math.floor(ms / 60000 * 70).toLocaleString()]
 ]));

 summary = `Age: ${years} years, ${months} months, ${days} days\n` +
 `Total days: ${totalDays.toLocaleString()}\n` +
 `Born on a ${dob.toLocaleDateString(undefined, { weekday: 'long' })}\n` +
 `Next birthday: ${next.toLocaleDateString()} (${daysToNext} days)`;

 T.status('status', `${years} years, ${months} months and ${days} days old.`, 'ok');
 }

 T.on(['dob', 'asof'], calculate);

 T.$('today').addEventListener('click', () => {
 T.$('asof').value = new Date().toISOString().slice(0, 10);
 calculate();
 });

 T.$('copy').addEventListener('click', () => copyToClipboard(summary, 'Summary copied'));
 T.$('share').addEventListener('click', () => shareLink({ title: 'Age Calculator | 123MiniApps' }));

 T.$('asof').value = new Date().toISOString().slice(0, 10);
 T.$('dob').value = '1990-06-15';
 calculate();
 if (window.Analytics) Analytics.trackToolUse('age-calculator');""",
))

# ---------------------------------------------------------------
# 60. Date Difference Calculator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="date-difference-calculator", name="Date Difference Calculator", icon="📅", cat="calculator",
 title="Date Difference Calculator: Days Between Two Dates",
 description="Count the days, weeks and months between two dates, with an optional business-day mode that excludes weekends and holidays you specify.",
 tagline="Count days between two dates, calendar days or business days only.",
 workspace=ws(
 row(
 text_input("start", "Start date", "", "", "date"),
 text_input("end", "End date", "", "", "date"),
 ),
 row(
 switch("inclusive", "Include the end date in the count", False),
 switch("business", "Business days only (exclude weekends)", False),
 ),
 status_line("status", "Pick two dates."),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result result--primary"><span class="result__value" id="r-days">, </span><span class="result__label">Days</span></div>
 <div class="result"><span class="result__value" id="r-weeks">, </span><span class="result__label">Weeks</span></div>
 <div class="result"><span class="result__value" id="r-months">, </span><span class="result__label">Months</span></div>
 <div class="result"><span class="result__value" id="r-exact" style="font-size:var(--text-xl)">, </span><span class="result__label">Exact difference</span></div>
 </div>"""),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Add or subtract from the start date</span></span>
 </div>"""),
 row(
 number_input("offset", "Amount", "30", "30", step="1"),
 select("offset-unit", "Unit", [("days", "Days"), ("weeks", "Weeks"), ("months", "Months"), ("years", "Years"), ("business", "Business days")], selected="days"),
 ),
 html_block(""" <div class="result-grid">
 <div class="result"><span class="result__value" id="r-plus" style="font-size:var(--text-xl)">, </span><span class="result__label">Start date plus that</span></div>
 <div class="result"><span class="result__value" id="r-minus" style="font-size:var(--text-xl)">, </span><span class="result__label">Start date minus that</span></div>
 </div>"""),
 buttons(("today", "Start from today", "primary"), ("copy", "Copy summary"), ("share", "Share tool", "ghost")),
 label="Date difference calculator",
 ),
 info_block=info(
 features=[
 "Calendar days, weeks and months between dates",
 "Business-day mode excluding weekends",
 "Inclusive or exclusive end date",
 "Add or subtract any span from a date",
 "Exact difference in years, months and days",
 ],
 howto=[
 "Pick a start and end date.",
 "Toggle business days if weekends should not count.",
 "Read the totals above.",
 "Use the lower section to project forwards or backwards.",
 ],
 background_title="Inclusive counting and why deadlines slip",
 background_paragraphs=[
 "The commonest source of off-by-one errors in date arithmetic is whether the end date counts. Subtracting 1 March from 5 March gives 4, but a hotel booking for those dates is 4 nights and 5 days, and a project running “from the 1st to the 5th” usually means 5 working days. Contracts and statutes are frequently explicit about this for exactly that reason, using phrases like “within 30 days of” versus “no later than the 30th day after”.",
 "Business-day counting has its own subtleties. This tool excludes Saturday and Sunday, which covers most Western commercial contexts but not all, the working week runs Sunday to Thursday in much of the Middle East, and public holidays vary by country and often by region within a country. Since holidays cannot be inferred reliably from a date alone, they are not deducted here; check the result against the relevant calendar for anything contractual.",
 "Adding months is genuinely ambiguous rather than merely fiddly. What is one month after 31 January? Most systems, including this one, clamp to the last valid day and give 28 or 29 February, but some roll over into 3 March instead. That means adding a month twice does not always equal adding two months, so for recurring schedules it is safer to calculate each date from the original anchor rather than from the previous result.",
 ],
 ),
 script=r""" let summary = '';

 const DAY_MS = 86400000;

 /** Count weekdays between two dates, excluding weekends. */
 function businessDaysBetween(start, end) {
 let count = 0;
 const cursor = new Date(start);
 while (cursor < end) {
 const day = cursor.getDay();
 if (day !== 0 && day !== 6) count++;
 cursor.setDate(cursor.getDate() + 1);
 }
 return count;
 }

 /** Add n business days to a date. */
 function addBusinessDays(date, n) {
 const out = new Date(date);
 const step = n >= 0 ? 1 : -1;
 let remaining = Math.abs(n);
 while (remaining > 0) {
 out.setDate(out.getDate() + step);
 const day = out.getDay();
 if (day !== 0 && day !== 6) remaining--;
 }
 return out;
 }

 function exactDiff(from, to) {
 let years = to.getFullYear() - from.getFullYear();
 let months = to.getMonth() - from.getMonth();
 let days = to.getDate() - from.getDate();

 if (days < 0) {
 months--;
 // Clamp the anchor day to the borrowed month's length, see the
 // age calculator for why an unclamped borrow can go negative.
 const prevMonthDays = new Date(to.getFullYear(), to.getMonth(), 0).getDate();
 days = to.getDate() + (prevMonthDays - Math.min(from.getDate(), prevMonthDays));
 }
 if (months < 0) { years--; months += 12; }

 return { years, months, days };
 }

 function calculate() {
 const startRaw = T.$('start').value;
 const endRaw = T.$('end').value;

 if (!startRaw || !endRaw) {
 T.status('status', 'Pick two dates.', 'muted');
 return;
 }

 let start = new Date(startRaw + 'T00:00:00');
 let end = new Date(endRaw + 'T00:00:00');

 if (isNaN(start) || isNaN(end)) {
 T.status('status', 'One of those dates is not valid.', 'error');
 return;
 }

 const reversed = end < start;
 if (reversed) [start, end] = [end, start];

 const inclusive = T.$('inclusive').checked;
 const effectiveEnd = inclusive ? new Date(end.getTime() + DAY_MS) : end;

 const days = T.$('business').checked
 ? businessDaysBetween(start, effectiveEnd)
 : Math.round((effectiveEnd - start) / DAY_MS);

 const { years, months, days: d } = exactDiff(start, end);

 T.$('r-days').textContent = days.toLocaleString();
 T.$('r-weeks').textContent = T.fmt(days / (T.$('business').checked ? 5 : 7), 1);
 T.$('r-months').textContent = T.fmt(years * 12 + months + d / 30, 1);
 T.$('r-exact').textContent = `${years}y ${months}m ${d}d`;

 calculateOffset();

 summary = [
 `From ${start.toLocaleDateString()} to ${end.toLocaleDateString()}`,
 `${days.toLocaleString()} ${T.$('business').checked ? 'business ' : ''}days`,
 `Exact: ${years} years, ${months} months, ${d} days`
 ].join('\n');

 T.status('status',
 `${days.toLocaleString()} ${T.$('business').checked ? 'business ' : ''}day(s)` +
 (reversed ? ' (dates were swapped, the end date came first)' : ''),
 reversed ? 'warn' : 'ok');
 }

 function calculateOffset() {
 const startRaw = T.$('start').value;
 if (!startRaw) return;

 const start = new Date(startRaw + 'T00:00:00');
 const n = Math.round(T.num(T.$('offset').value) || 0);
 const unit = T.$('offset-unit').value;

 const shift = (base, amount) => {
 const out = new Date(base);
 if (unit === 'days') out.setDate(out.getDate() + amount);
 else if (unit === 'weeks') out.setDate(out.getDate() + amount * 7);
 else if (unit === 'months') out.setMonth(out.getMonth() + amount);
 else if (unit === 'years') out.setFullYear(out.getFullYear() + amount);
 else return addBusinessDays(base, amount);
 return out;
 };

 T.$('r-plus').textContent = shift(start, n).toLocaleDateString();
 T.$('r-minus').textContent = shift(start, -n).toLocaleDateString();
 }

 T.on(['start', 'end', 'offset'], calculate);
 T.on(['inclusive', 'business', 'offset-unit'], calculate, 'change');

 T.$('today').addEventListener('click', () => {
 T.$('start').value = new Date().toISOString().slice(0, 10);
 calculate();
 });

 T.$('copy').addEventListener('click', () => copyToClipboard(summary, 'Summary copied'));
 T.$('share').addEventListener('click', () => shareLink({ title: 'Date Difference Calculator | 123MiniApps' }));

 const today = new Date();
 const later = new Date(today.getTime() + 30 * DAY_MS);
 T.$('start').value = today.toISOString().slice(0, 10);
 T.$('end').value = later.toISOString().slice(0, 10);
 calculate();
 if (window.Analytics) Analytics.trackToolUse('date-difference-calculator');""",
))

# ---------------------------------------------------------------
# 61. Scientific Calculator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="scientific-calculator", name="Scientific Calculator", icon="🔬", cat="calculator",
 title="Scientific Calculator: Trig, Logs, Powers and Memory",
 description="A full scientific calculator with trigonometry, logarithms, powers, roots, constants and memory registers. Keyboard input supported throughout.",
 tagline="Trigonometry, logarithms, powers and memory, with full keyboard support.",
 workspace=ws(
 html_block(""" <div class="field">
 <label class="field__label" for="expr">
 <span>Expression</span>
 <span class="field__hint" id="mem-indicator"></span>
 </label>
 <input class="input font-mono" id="expr" type="text" value="" placeholder="e.g. sin(pi/4) * sqrt(2)"
 autocomplete="off" spellcheck="false" style="font-size:var(--text-lg);height:60px">
 </div>"""),
 html_block(""" <div class="display" style="padding:var(--space-6)">
 <span class="display__value" id="result" style="font-size:clamp(1.75rem,1rem+4vw,3rem)">0</span>
 <span class="display__label" id="status">Type an expression and press Enter.</span>
 </div>"""),
 row(
 select("angle", "Angle mode", [("rad", "Radians"), ("deg", "Degrees")], selected="rad"),
 select("precision", "Decimal places", [("auto", "Automatic"), ("2", "2"), ("4", "4"), ("6", "6"), ("10", "10")], selected="auto"),
 ),
 html_block(""" <div class="field">
 <span class="field__label"><span>Functions</span><span class="field__hint">Click to insert</span></span>
 <div class="chip-grid" id="functions"></div>
 </div>"""),
 buttons(("evaluate", "Calculate", "primary"), ("mem-store", "M+"), ("mem-recall", "MR"), ("mem-clear", "MC"), ("clear", "Clear", "ghost"), ("copy", "Copy result"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>History</span><span class="field__hint">Click any entry to reuse it</span></span>
 <div id="history" class="chip-grid"></div>
 </div>"""),
 label="Scientific calculator",
 ),
 info_block=info(
 features=[
 "Trigonometric, inverse trig and hyperbolic functions",
 "Natural and base-10 logarithms, powers and roots",
 "Radian and degree modes",
 "Memory registers and a reusable history",
 "Safe expression parser, no eval()",
 ],
 howto=[
 "Type an expression such as sin(pi/4) * sqrt(2).",
 "Press Enter or Calculate.",
 "Switch to degrees if your angles are in degrees.",
 "Click any history entry to reuse it.",
 ],
 background_title="How this evaluates expressions safely",
 background_paragraphs=[
 "The obvious way to build a calculator in JavaScript is to hand the user's input to <code>eval()</code>. That works, and it is also a security hole: eval executes arbitrary code, so anything typed into the box, or injected into it via a crafted link, runs with the page's full privileges. Plenty of online calculators do exactly this.",
 "This one implements a proper recursive-descent parser instead. The expression is tokenised into numbers, operators, parentheses and function names, then parsed according to precedence rules, parentheses first, then functions and unary minus, then exponentiation, then multiplication and division, then addition and subtraction. Anything the grammar does not recognise is rejected with an error rather than executed.",
 "One detail that surprises people: exponentiation is right-associative, so <code>2^3^2</code> means 2^(3^2) = 512, not (2^3)^2 = 64. That matches mathematical convention and most scientific calculators, though some spreadsheet software gets it wrong. Unary minus binds looser than exponentiation too, so <code>-2^2</code> is −4 rather than 4.",
 ],
 ),
 script=r""" let memory = 0;
 let history = T.store.get('calc-history', []);
 let lastValue = 0;

 const CONSTANTS = { pi: Math.PI, e: Math.E, tau: Math.PI * 2, phi: (1 + Math.sqrt(5)) / 2 };

 /** Functions available in expressions. Angle-aware where relevant. */
 function functions() {
 const deg = T.$('angle').value === 'deg';
 const toRad = (x) => (deg ? (x * Math.PI) / 180 : x);
 const fromRad = (x) => (deg ? (x * 180) / Math.PI : x);

 return {
 sin: (x) => Math.sin(toRad(x)), cos: (x) => Math.cos(toRad(x)), tan: (x) => Math.tan(toRad(x)),
 asin: (x) => fromRad(Math.asin(x)), acos: (x) => fromRad(Math.acos(x)), atan: (x) => fromRad(Math.atan(x)),
 sinh: Math.sinh, cosh: Math.cosh, tanh: Math.tanh,
 ln: Math.log, log: Math.log10, log2: Math.log2,
 sqrt: Math.sqrt, cbrt: Math.cbrt, abs: Math.abs,
 exp: Math.exp, floor: Math.floor, ceil: Math.ceil, round: Math.round,
 sign: Math.sign, fact: factorial
 };
 }

 function factorial(n) {
 if (n < 0 || n !== Math.floor(n)) throw new Error('Factorial needs a non-negative whole number');
 if (n > 170) return Infinity; // beyond double precision
 let out = 1;
 for (let i = 2; i <= n; i++) out *= i;
 return out;
 }

 /**
 * Recursive-descent parser. Deliberately not eval(), this only
 * ever evaluates arithmetic, never arbitrary JavaScript.
 * @param {string} input
 * @returns {number}
 */
 function evaluate(input) {
 const fns = functions();
 let pos = 0;
 const src = input.replace(/\s+/g, '');

 const peek = () => src[pos];
 const eof = () => pos >= src.length;

 function parseExpression() {
 let left = parseTerm();
 while (!eof() && (peek() === '+' || peek() === '-')) {
 const op = src[pos++];
 const right = parseTerm();
 left = op === '+' ? left + right : left - right;
 }
 return left;
 }

 function parseTerm() {
 let left = parseUnary();
 while (!eof() && (peek() === '*' || peek() === '/' || peek() === '%')) {
 const op = src[pos++];
 const right = parseUnary();
 if (op === '*') left *= right;
 else if (op === '/') {
 if (right === 0) throw new Error('Division by zero');
 left /= right;
 } else left %= right;
 }
 return left;
 }

 function parseUnary() {
 if (peek() === '-') { pos++; return -parseUnary(); }
 if (peek() === '+') { pos++; return parseUnary(); }
 return parsePower();
 }

 function parsePower() {
 const base = parsePostfix();
 if (!eof() && (peek() === '^')) {
 pos++;
 // Right-associative: 2^3^2 = 2^(3^2)
 return Math.pow(base, parseUnary());
 }
 return base;
 }

 function parsePostfix() {
 let value = parsePrimary();
 while (!eof() && peek() === '!') { pos++; value = factorial(value); }
 return value;
 }

 function parsePrimary() {
 if (eof()) throw new Error('Unexpected end of expression');

 if (peek() === '(') {
 pos++;
 const value = parseExpression();
 if (peek() !== ')') throw new Error('Missing closing bracket');
 pos++;
 return value;
 }

 // Number, including scientific notation
 const numMatch = /^\d*\.?\d+(e[+-]?\d+)?/i.exec(src.slice(pos));
 if (numMatch) { pos += numMatch[0].length; return Number(numMatch[0]); }

 // Identifier, function call or constant
 const idMatch = /^[a-z_][a-z0-9_]*/i.exec(src.slice(pos));
 if (idMatch) {
 const name = idMatch[0].toLowerCase();
 pos += idMatch[0].length;

 if (peek() === '(') {
 pos++;
 const arg = parseExpression();
 if (peek() !== ')') throw new Error(`Missing closing bracket after ${name}()`);
 pos++;
 const fn = fns[name];
 if (!fn) throw new Error(`Unknown function “${name}”`);
 return fn(arg);
 }

 if (name in CONSTANTS) return CONSTANTS[name];
 if (name === 'ans') return lastValue;
 if (name === 'mem') return memory;
 throw new Error(`Unknown name “${name}”`);
 }

 throw new Error(`Unexpected character “${peek()}”`);
 }

 const value = parseExpression();
 if (!eof()) throw new Error(`Unexpected character “${peek()}”`);
 return value;
 }

 function format(n) {
 if (!isFinite(n)) return n > 0 ? '∞' : (isNaN(n) ? 'Not a number' : '−∞');
 const p = T.$('precision').value;
 if (p !== 'auto') return n.toFixed(Number(p));
 if (Number.isInteger(n) && Math.abs(n) < 1e15) return n.toLocaleString();
 if (Math.abs(n) < 1e-7 || Math.abs(n) >= 1e15) return n.toExponential(8);
 return Number(n.toPrecision(12)).toString();
 }

 function run() {
 const input = T.$('expr').value.trim();
 if (!input) return;

 try {
 const value = evaluate(input);
 lastValue = value;
 T.$('result').textContent = format(value);
 T.status('status', 'Use “ans” to reference this result.', 'ok');

 history.unshift({ expr: input, result: format(value) });
 history = history.slice(0, 10);
 T.store.set('calc-history', history);
 renderHistory();
 } catch (err) {
 T.$('result').textContent = 'Error';
 T.status('status', err.message, 'error');
 }
 }

 function renderHistory() {
 const mount = T.$('history');
 mount.innerHTML = '';

 if (!history.length) {
 mount.append(el('span', { className: 'text-xs text-muted', text: 'Nothing yet.' }));
 return;
 }

 history.forEach((h) => {
 const chip = el('button', {
 className: 'chip font-mono',
 attrs: { type: 'button' },
 text: `${h.expr} = ${h.result}`
 });
 chip.addEventListener('click', () => {
 T.$('expr').value = h.expr;
 run();
 });
 mount.append(chip);
 });
 }

 function renderFunctions() {
 const mount = T.$('functions');
 const items = ['sin(', 'cos(', 'tan(', 'asin(', 'acos(', 'atan(',
 'ln(', 'log(', 'sqrt(', 'cbrt(', 'abs(', 'exp(', 'fact(',
 'pi', 'e', 'ans', '^', '!', '%'];

 items.forEach((item) => {
 const chip = el('button', { className: 'chip font-mono', attrs: { type: 'button' }, text: item });
 chip.addEventListener('click', () => {
 const input = T.$('expr');
 const at = input.selectionStart ?? input.value.length;
 input.value = input.value.slice(0, at) + item + input.value.slice(at);
 input.focus();
 input.setSelectionRange(at + item.length, at + item.length);
 });
 mount.append(chip);
 });
 }

 function updateMemoryIndicator() {
 T.$('mem-indicator').textContent = memory !== 0 ? `M = ${format(memory)}` : '';
 }

 T.$('expr').addEventListener('keydown', (e) => {
 if (e.key === 'Enter') { e.preventDefault(); run(); }
 });

 T.$('evaluate').addEventListener('click', run);
 T.on(['angle', 'precision'], run, 'change');

 T.$('mem-store').addEventListener('click', () => {
 memory += lastValue;
 updateMemoryIndicator();
 toast({ type: 'success', title: 'Added to memory', message: format(memory) });
 });

 T.$('mem-recall').addEventListener('click', () => {
 const input = T.$('expr');
 input.value += format(memory).replace(/,/g, '');
 input.focus();
 });

 T.$('mem-clear').addEventListener('click', () => {
 memory = 0;
 updateMemoryIndicator();
 toast({ type: 'success', title: 'Memory cleared' });
 });

 T.$('clear').addEventListener('click', () => {
 T.$('expr').value = '';
 T.$('result').textContent = '0';
 T.status('status', 'Type an expression and press Enter.', 'muted');
 T.$('expr').focus();
 });

 T.$('copy').addEventListener('click', () =>
 copyToClipboard(T.$('result').textContent, 'Result copied'));
 T.$('share').addEventListener('click', () => shareLink({ title: 'Scientific Calculator | 123MiniApps' }));

 renderFunctions();
 renderHistory();
 updateMemoryIndicator();
 if (window.Analytics) Analytics.trackToolUse('scientific-calculator');""",
))

# ---------------------------------------------------------------
# 62. Discount Calculator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="discount-calculator", name="Discount Calculator", icon="🏷️", cat="calculator",
 title="Discount Calculator: Sale Price, Savings and Stacked Discounts",
 description="Find the sale price and savings on any discount, including stacked discounts, and work backwards from a sale price to the original.",
 tagline="Work out sale prices and savings, including what stacked discounts really total.",
 workspace=ws(
 select("mode", "What do you want to work out?", [
 ("sale", "Sale price from a discount"),
 ("stacked", "Stacked discounts (one after another)"),
 ("original", "Original price from a sale price"),
 ("percent", "What discount was applied?"),
 ], selected="sale"),
 row(
 number_input("price", "Original price", "199.99", "199.99"),
 number_input("discount", "Discount (%)", "25", "25"),
 number_input("discount2", "Second discount (%)", "10", "10"),
 ),
 row(
 number_input("saleprice", "Sale price", "149.99", "149.99"),
 number_input("tax", "Add tax afterwards (%)", "0", "0"),
 ),
 status_line("status", "Enter a price and a discount."),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result result--primary"><span class="result__value" id="r-final">, </span><span class="result__label">You pay</span></div>
 <div class="result"><span class="result__value" id="r-saved">, </span><span class="result__label">You save</span></div>
 <div class="result"><span class="result__value" id="r-effective">, </span><span class="result__label">Effective discount</span></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Breakdown</span></span>
 <div class="output" id="working">The calculation will appear here.</div>
 </div>"""),
 buttons(("copy", "Copy result", "primary"), ("share", "Share tool", "ghost")),
 label="Discount calculator",
 ),
 info_block=info(
 features=[
 "Sale price, savings and effective discount",
 "Stacked discounts calculated correctly",
 "Reverse calculation to find the original price",
 "Optional tax applied after the discount",
 "Step-by-step breakdown of every calculation",
 ],
 howto=[
 "Pick which calculation you need.",
 "Enter the price and discount percentages.",
 "Read the final price and savings.",
 "Check the breakdown to see the working.",
 ],
 background_title="Why stacked discounts never add up",
 background_paragraphs=[
 "A 20% discount followed by another 20% is not 40% off. The second discount applies to the already-reduced price, so you pay 80% of 80%, which is 64% of the original, an effective discount of 36%, not 40%. The gap widens as the discounts grow: two 50% discounts leave you at 25% of the original rather than free.",
 "The order does not matter mathematically, multiplication is commutative, so 20% then 10% gives the same result as 10% then 20%. It can matter legally and practically, though. Some retailers apply percentage discounts before fixed-amount vouchers, others after, and the difference is real money. Tax is normally calculated on the discounted price, which is what this tool does.",
 "The pricing tactic worth being aware of is the reference price. A discount is only meaningful relative to a price the item actually sold at, and “was £200, now £100” tells you nothing if it never sold at £200. Several jurisdictions regulate this, EU rules require the displayed prior price to be the lowest price charged in the preceding 30 days, and similar rules exist in the UK and Australia. Comparing against what competitors charge is a better guide than the percentage on the label.",
 ],
 ),
 script=r""" let lastResult = '';

 function syncFields() {
 const mode = T.$('mode').value;
 const show = (id, visible) => {
 const field = T.$(id).closest('.field');
 if (field) field.style.display = visible ? '' : 'none';
 };

 show('price', mode !== 'original');
 show('discount', mode === 'sale' || mode === 'stacked');
 show('discount2', mode === 'stacked');
 show('saleprice', mode === 'original' || mode === 'percent');

 calculate();
 }

 function calculate() {
 const mode = T.$('mode').value;
 const price = T.num(T.$('price').value);
 const d1 = T.num(T.$('discount').value);
 const d2 = T.num(T.$('discount2').value);
 const sale = T.num(T.$('saleprice').value);
 const taxPct = T.num(T.$('tax').value) || 0;

 let final, saved, effective, working;

 try {
 if (mode === 'sale') {
 if (isNaN(price) || isNaN(d1)) throw new Error('need');
 final = price * (1 - d1 / 100);
 saved = price - final;
 effective = d1;
 working = `Original: ${T.money(price)}\n` +
 `Discount: ${d1}% → −${T.money(saved)}\n` +
 `Sale price: ${T.money(final)}`;
 } else if (mode === 'stacked') {
 if (isNaN(price) || isNaN(d1) || isNaN(d2)) throw new Error('need');
 const after1 = price * (1 - d1 / 100);
 final = after1 * (1 - d2 / 100);
 saved = price - final;
 effective = (saved / price) * 100;
 working = `Original: ${T.money(price)}\n` +
 `First discount ${d1}%: ${T.money(price)} × ${T.fmt(1 - d1 / 100, 3)} = ${T.money(after1)}\n` +
 `Second discount ${d2}%: ${T.money(after1)} × ${T.fmt(1 - d2 / 100, 3)} = ${T.money(final)}\n\n` +
 `Naively adding the discounts suggests ${T.fmt(d1 + d2, 1)}% off.\n` +
 `The real effective discount is ${T.fmt(effective, 2)}%, a difference of ${T.money((d1 + d2 - effective) / 100 * price)}.`;
 } else if (mode === 'original') {
 if (isNaN(sale) || isNaN(d1)) throw new Error('need');
 if (d1 >= 100) throw new Error('A 100% discount cannot be reversed.');
 const original = sale / (1 - d1 / 100);
 final = sale;
 saved = original - sale;
 effective = d1;
 working = `Sale price: ${T.money(sale)}\n` +
 `Was ${d1}% off\n` +
 `Original: ${T.money(sale)} ÷ ${T.fmt(1 - d1 / 100, 3)} = ${T.money(original)}\n` +
 `Saving: ${T.money(saved)}`;
 } else {
 if (isNaN(price) || isNaN(sale)) throw new Error('need');
 if (price === 0) throw new Error('The original price cannot be zero.');
 final = sale;
 saved = price - sale;
 effective = (saved / price) * 100;
 working = `Original: ${T.money(price)}\n` +
 `Sale price: ${T.money(sale)}\n` +
 `Saving: ${T.money(saved)}\n` +
 `Discount: (${T.money(saved)} ÷ ${T.money(price)}) × 100 = ${T.fmt(effective, 2)}%`;
 }
 } catch (err) {
 if (err.message === 'need') {
 T.status('status', 'Enter a price and a discount.', 'muted');
 ['r-final', 'r-saved', 'r-effective'].forEach((id) => { T.$(id).textContent = ', '; });
 } else {
 T.status('status', err.message, 'error');
 }
 return;
 }

 if (taxPct > 0) {
 const withTax = final * (1 + taxPct / 100);
 working += `\n\nTax at ${taxPct}%: +${T.money(withTax - final)}\nTotal to pay: ${T.money(withTax)}`;
 final = withTax;
 }

 T.$('r-final').textContent = T.money(final);
 T.$('r-saved').textContent = T.money(saved);
 T.$('r-effective').textContent = T.fmt(effective, 1) + '%';

 T.setOutput('working', working);

 lastResult = `You pay ${T.money(final)}, saving ${T.money(saved)} (${T.fmt(effective, 1)}% off).`;
 T.status('status', lastResult, 'ok');
 }

 T.on(['price', 'discount', 'discount2', 'saleprice', 'tax'], calculate);
 T.$('mode').addEventListener('change', syncFields);

 T.$('copy').addEventListener('click', () => copyToClipboard(lastResult, 'Result copied'));
 T.$('share').addEventListener('click', () => shareLink({ title: 'Discount Calculator | 123MiniApps' }));

 syncFields();
 if (window.Analytics) Analytics.trackToolUse('discount-calculator');""",
))

# ---------------------------------------------------------------
# 63. Compound Interest Calculator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="compound-interest-calculator", name="Compound Interest Calculator", icon="📈", cat="calculator",
 title="Compound Interest Calculator: Projected Growth Year by Year",
 description="Project how savings grow with compound interest and regular contributions. Any compounding frequency, with a year-by-year breakdown table.",
 tagline="Project savings growth with compounding and regular contributions.",
 workspace=ws(
 row(
 number_input("principal", "Starting amount", "10000", "10000"),
 number_input("rate", "Annual return (%)", "7", "7"),
 number_input("years", "Years", "20", "20"),
 ),
 row(
 number_input("contribution", "Regular contribution", "250", "250"),
 select("contrib-freq", "Contribution frequency", [
 ("12", "Monthly"), ("4", "Quarterly"), ("1", "Yearly"), ("0", "None"),
 ], selected="12"),
 select("compound", "Compounding frequency", [
 ("365", "Daily"), ("12", "Monthly"), ("4", "Quarterly"), ("1", "Annually"),
 ], selected="12"),
 ),
 number_input("inflation", "Adjust for inflation (%)", "0", "0"),
 status_line("status", "Enter your starting amount and rate."),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result result--primary"><span class="result__value" id="r-final">, </span><span class="result__label">Final balance</span></div>
 <div class="result"><span class="result__value" id="r-contributed">, </span><span class="result__label">Total contributed</span></div>
 <div class="result"><span class="result__value" id="r-growth">, </span><span class="result__label">Growth</span></div>
 <div class="result"><span class="result__value" id="r-real">, </span><span class="result__label">In today's money</span></div>
 </div>"""),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Year by year</span></span>
 <div class="table-scroll"><div id="schedule"></div></div>
 </div>"""),
 buttons(("copy", "Copy summary", "primary"), ("download", "Download (CSV)"), ("share", "Share tool", "ghost")),
 label="Compound interest calculator",
 ),
 info_block=info(
 features=[
 "Any compounding frequency from daily to annual",
 "Regular contributions at your chosen interval",
 "Inflation adjustment showing real purchasing power",
 "Year-by-year table of balance, contributions and growth",
 "CSV export of the full projection",
 ],
 howto=[
 "Enter your starting amount, expected return and time horizon.",
 "Add a regular contribution if you save monthly.",
 "Set an inflation rate to see the result in today's money.",
 "Read the year-by-year table for the full picture.",
 ],
 background_title="Compounding, and the assumptions behind these numbers",
 background_paragraphs=[
 "Compound interest means returns earn returns. £10,000 at 7% earns £700 in year one, but £749 in year two because the £700 is now also invested. Over long periods this dominates: the same £10,000 left for 30 years at 7% becomes roughly £76,000, of which £66,000 is growth rather than principal. Time in the market matters far more than the amount, which is why starting a decade earlier typically beats contributing more later.",
 "Compounding frequency matters much less than people expect. Moving from annual to daily compounding at 7% raises the effective annual rate only from 7% to about 7.25%. The contribution amount and the number of years dominate the outcome; frequency is a rounding detail by comparison.",
 "The assumptions here deserve scepticism. A fixed annual return is a modelling convenience, not a description of how markets behave, real returns are volatile, and the order in which good and bad years arrive materially changes the outcome when you are contributing or withdrawing. This model also ignores fees, which compound against you exactly as returns compound for you, and ignores tax on gains. Treat the output as an illustration of the mechanism, not a forecast. It is not financial advice, and a qualified adviser is the right person to consult before making decisions.",
 ],
 ),
 script=r""" let rows = [];
 let summary = '';

 function calculate() {
 const principal = T.num(T.$('principal').value);
 const rate = T.num(T.$('rate').value);
 const years = T.num(T.$('years').value);
 const contribution = T.num(T.$('contribution').value) || 0;
 const contribFreq = Number(T.$('contrib-freq').value);
 const compoundFreq = Number(T.$('compound').value);
 const inflation = T.num(T.$('inflation').value) || 0;

 if (isNaN(principal) || isNaN(rate) || isNaN(years) || years <= 0) {
 T.status('status', 'Enter your starting amount and rate.', 'muted');
 return;
 }

 if (years > 100) {
 T.status('status', 'Please use a horizon of 100 years or less.', 'error');
 return;
 }

 // Simulate period by period at the compounding frequency.
 // Contributions are added on their own schedule.
 const periodsPerYear = compoundFreq;
 const periodRate = rate / 100 / periodsPerYear;
 const totalPeriods = Math.round(years * periodsPerYear);

 let balance = principal;
 let contributed = principal;
 rows = [];

 let yearOpening = balance;
 let yearContributed = 0;

 for (let p = 1; p <= totalPeriods; p++) {
 balance *= 1 + periodRate;

 // Add a contribution when this period lands on the contribution schedule
 if (contribFreq > 0) {
 const contributionsPerPeriod = contribFreq / periodsPerYear;
 const due = contributionsPerPeriod >= 1
 ? Math.round(contributionsPerPeriod)
 : (p % Math.round(periodsPerYear / contribFreq) === 0 ? 1 : 0);

 if (due > 0) {
 const amount = contribution * due;
 balance += amount;
 contributed += amount;
 yearContributed += amount;
 }
 }

 if (p % periodsPerYear === 0 || p === totalPeriods) {
 const year = Math.ceil(p / periodsPerYear);
 rows.push({
 year,
 opening: yearOpening,
 contributed: yearContributed,
 growth: balance - yearOpening - yearContributed,
 balance
 });
 yearOpening = balance;
 yearContributed = 0;
 }
 }

 const growth = balance - contributed;
 const realValue = inflation > 0 ? balance / Math.pow(1 + inflation / 100, years) : balance;

 T.$('r-final').textContent = T.money(balance);
 T.$('r-contributed').textContent = T.money(contributed);
 T.$('r-growth').textContent = T.money(growth);
 T.$('r-real').textContent = inflation > 0 ? T.money(realValue) : ', ';

 renderSchedule();

 summary = [
 `Starting amount: ${T.money(principal)}`,
 `Annual return: ${rate}%`,
 `Period: ${years} years`,
 contribFreq ? `Contribution: ${T.money(contribution)} ${T.$('contrib-freq').selectedOptions[0].textContent.toLowerCase()}` : 'No regular contributions',
 `Final balance: ${T.money(balance)}`,
 `Total contributed: ${T.money(contributed)}`,
 `Growth: ${T.money(growth)}`,
 inflation > 0 ? `In today's money: ${T.money(realValue)}` : ''
 ].filter(Boolean).join('\n');

 const multiple = contributed > 0 ? balance / contributed : 0;
 T.status('status',
 `Growth accounts for ${T.fmt((growth / balance) * 100, 1)}% of the final balance, ` +
 `${T.fmt(multiple, 2)}× what you put in.`, 'ok');
 }

 function renderSchedule() {
 const mount = T.$('schedule');
 mount.innerHTML = '';
 if (!rows.length) return;

 mount.append(T.table(
 ['Year', 'Opening', 'Contributed', 'Growth', 'Closing'],
 rows.map((r) => [
 r.year, T.money(r.opening), T.money(r.contributed), T.money(r.growth), T.money(r.balance)
 ])
 ));
 }

 T.on(['principal', 'rate', 'years', 'contribution', 'inflation'], debounce(calculate, 200));
 T.on(['contrib-freq', 'compound'], calculate, 'change');

 T.$('copy').addEventListener('click', () => copyToClipboard(summary, 'Summary copied'));

 T.$('download').addEventListener('click', () => {
 if (!rows.length) { toast({ type: 'warning', title: 'Nothing to download' }); return; }
 const csv = ['Year,Opening,Contributed,Growth,Closing']
 .concat(rows.map((r) =>
 [r.year, r.opening.toFixed(2), r.contributed.toFixed(2), r.growth.toFixed(2), r.balance.toFixed(2)].join(',')))
 .join('\n');
 downloadFile(csv, 'compound-interest-projection.csv', 'text/csv');
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Compound Interest Calculator | 123MiniApps' }));

 calculate();
 if (window.Analytics) Analytics.trackToolUse('compound-interest-calculator');""",
))

# ---------------------------------------------------------------
# 64. Fuel Cost Calculator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="fuel-cost-calculator", name="Fuel Cost Calculator", icon="⛽", cat="calculator",
 title="Fuel Cost Calculator: Trip Cost from Distance and Efficiency",
 description="Estimate the fuel cost of any journey from distance, vehicle efficiency and fuel price. Supports MPG and L/100km, round trips and cost splitting.",
 tagline="Estimate what a journey costs in fuel, and what it costs per passenger.",
 workspace=ws(
 row(
 number_input("distance", "Distance", "250", "250"),
 select("dist-unit", "Distance unit", [("km", "Kilometres"), ("mi", "Miles")], selected="km"),
 switch("roundtrip", "Round trip (double the distance)", False),
 ),
 row(
 number_input("efficiency", "Fuel efficiency", "7.5", "7.5"),
 select("eff-unit", "Efficiency measured in", [
 ("l100km", "L/100km, lower is better"),
 ("kmpl", "km per litre"),
 ("mpg-uk", "MPG (imperial / UK)"),
 ("mpg-us", "MPG (US)"),
 ], selected="l100km"),
 ),
 row(
 number_input("price", "Fuel price", "1.65", "1.65"),
 select("price-unit", "Price per", [("litre", "Litre"), ("gallon-uk", "Gallon (UK)"), ("gallon-us", "Gallon (US)")], selected="litre"),
 number_input("passengers", "Split between", "1", "1", step="1", min=1),
 ),
 status_line("status", "Enter your trip details."),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result result--primary"><span class="result__value" id="r-cost">, </span><span class="result__label">Total fuel cost</span></div>
 <div class="result"><span class="result__value" id="r-fuel">, </span><span class="result__label">Fuel needed</span></div>
 <div class="result"><span class="result__value" id="r-each">, </span><span class="result__label">Per passenger</span></div>
 <div class="result"><span class="result__value" id="r-perdist">, </span><span class="result__label">Cost per unit distance</span></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Breakdown</span></span>
 <div class="output" id="working">The calculation will appear here.</div>
 </div>"""),
 buttons(("copy", "Copy result", "primary"), ("share", "Share tool", "ghost")),
 label="Fuel cost calculator",
 ),
 info_block=info(
 features=[
 "Metric and imperial distances",
 "Four efficiency formats including both MPG variants",
 "Round-trip toggle",
 "Cost per passenger for shared journeys",
 "Shows the working so you can check it",
 ],
 howto=[
 "Enter the distance and pick its unit.",
 "Enter your vehicle's efficiency in whichever format you know.",
 "Enter the current fuel price.",
 "Read the total and per-passenger cost.",
 ],
 background_title="Efficiency figures and why yours will be worse",
 background_paragraphs=[
 "Two things routinely trip people up. First, UK and US gallons differ, a UK gallon is 4.546 litres and a US gallon 3.785. A car rated at 40 MPG in the UK would be rated around 33 MPG in the US for identical real-world consumption, so comparing figures across the two systems without converting is meaningless. Second, L/100km and MPG run in opposite directions: lower is better for L/100km, higher is better for MPG, and the relationship between them is reciprocal rather than linear.",
 "Manufacturer efficiency figures are obtained under standardised laboratory conditions. Europe's WLTP cycle replaced the older and notoriously optimistic NEDC in 2018 and is closer to reality, but real-world consumption still typically runs 10% to 20% worse. Short journeys are much worse than that, because an engine running below operating temperature can consume 50% more fuel over the first few kilometres.",
 "The variables under your control are larger than most people assume. Aerodynamic drag rises with the square of speed, so cruising at 110 km/h instead of 130 cuts consumption noticeably on a long trip. A roof box can add 10% to 25%. Under-inflated tyres, aggressive acceleration and running the air conditioning at low speeds all add measurably. For a genuinely accurate figure, divide the fuel you actually put in by the distance you actually covered over several tanks.",
 ],
 ),
 script=r""" let lastResult = '';

 const KM_PER_MILE = 1.609344;
 const L_PER_UK_GAL = 4.54609;
 const L_PER_US_GAL = 3.785411784;

 /** Convert whatever efficiency format was entered into L/100km. */
 function toL100km(value, unit) {
 if (value <= 0) return NaN;
 switch (unit) {
 case 'l100km': return value;
 case 'kmpl': return 100 / value;
 case 'mpg-uk': return (100 * L_PER_UK_GAL) / (value * KM_PER_MILE);
 case 'mpg-us': return (100 * L_PER_US_GAL) / (value * KM_PER_MILE);
 default: return NaN;
 }
 }

 /** Convert the entered price into a price per litre. */
 function toPerLitre(price, unit) {
 if (unit === 'gallon-uk') return price / L_PER_UK_GAL;
 if (unit === 'gallon-us') return price / L_PER_US_GAL;
 return price;
 }

 function calculate() {
 let distance = T.num(T.$('distance').value);
 const efficiency = T.num(T.$('efficiency').value);
 const price = T.num(T.$('price').value);
 const passengers = Math.max(1, Math.floor(T.num(T.$('passengers').value) || 1));

 if (isNaN(distance) || isNaN(efficiency) || isNaN(price) || distance <= 0) {
 ['r-cost', 'r-fuel', 'r-each', 'r-perdist'].forEach((id) => { T.$(id).textContent = ', '; });
 T.status('status', 'Enter your trip details.', 'muted');
 return;
 }

 if (efficiency <= 0 || price < 0) {
 T.status('status', 'Efficiency must be above zero and price cannot be negative.', 'error');
 return;
 }

 if (T.$('roundtrip').checked) distance *= 2;

 const distanceKm = T.$('dist-unit').value === 'mi' ? distance * KM_PER_MILE : distance;
 const l100 = toL100km(efficiency, T.$('eff-unit').value);
 const pricePerLitre = toPerLitre(price, T.$('price-unit').value);

 if (!isFinite(l100)) {
 T.status('status', 'That efficiency value does not make sense.', 'error');
 return;
 }

 const litres = (distanceKm / 100) * l100;
 const cost = litres * pricePerLitre;

 T.$('r-cost').textContent = T.money(cost);
 T.$('r-fuel').textContent = T.fmt(litres, 1) + ' L';
 T.$('r-each').textContent = T.money(cost / passengers);

 const unit = T.$('dist-unit').value;
 const perUnit = cost / distance;
 T.$('r-perdist').textContent = T.money(perUnit) + '/' + unit;

 T.setOutput('working', [
 `Distance: ${T.fmt(distance, 1)} ${unit}${T.$('roundtrip').checked ? ' (round trip)' : ''}`,
 ` = ${T.fmt(distanceKm, 1)} km`,
 `Efficiency: ${efficiency} ${T.$('eff-unit').selectedOptions[0].textContent}`,
 ` = ${T.fmt(l100, 2)} L/100km`,
 `Fuel needed: (${T.fmt(distanceKm, 1)} ÷ 100) × ${T.fmt(l100, 2)} = ${T.fmt(litres, 2)} L`,
 `Price: ${T.money(pricePerLitre)} per litre`,
 `Cost: ${T.fmt(litres, 2)} × ${T.money(pricePerLitre)} = ${T.money(cost)}`,
 passengers > 1 ? `Split ${passengers} ways: ${T.money(cost / passengers)} each` : ''
 ].filter(Boolean).join('\n'));

 lastResult = `${T.fmt(distance, 0)} ${unit} costs ${T.money(cost)} in fuel (${T.fmt(litres, 1)} L).`;
 T.status('status', lastResult, 'ok');
 }

 T.on(['distance', 'efficiency', 'price', 'passengers'], calculate);
 T.on(['dist-unit', 'eff-unit', 'price-unit', 'roundtrip'], calculate, 'change');

 T.$('copy').addEventListener('click', () => copyToClipboard(lastResult, 'Result copied'));
 T.$('share').addEventListener('click', () => shareLink({ title: 'Fuel Cost Calculator | 123MiniApps' }));

 calculate();
 if (window.Analytics) Analytics.trackToolUse('fuel-cost-calculator');""",
))
