/* ============================================
   123MiniApps.online v2.0
   File: test/phase-calculator.js
   Purpose: Behavioural tests for the 10 calculators.

   Financial maths is checked against independently
   derived expected values, not against the
   implementation's own output.
   ============================================ */

const { boot, Suite, set, click, text, val, wait } = require('./harness');

const num = (s) => Number(String(s).replace(/[^0-9.-]/g, ''));

module.exports = async function run() {
  const s = new Suite('Calculators');

  /* ---------- Percentage ---------- */
  {
    const { window: w, errors } = await boot('tools/percentage-calculator.html');

    set(w, 'mode', 'of', 'change');
    set(w, 'a', '25'); set(w, 'b', '200');
    await wait(80);
    s.eq('pct: 25% of 200 = 50', num(text(w, 'r-main')), 50);

    set(w, 'mode', 'what', 'change');
    set(w, 'a', '50'); set(w, 'b', '200');
    await wait(80);
    s.eq('pct: 50 is 25% of 200', num(text(w, 'r-main')), 25);

    // Increase and decrease are not symmetrical
    set(w, 'mode', 'change', 'change');
    set(w, 'a', '100'); set(w, 'b', '150');
    await wait(80);
    s.eq('pct: 100→150 is +50%', num(text(w, 'r-main')), 50);
    set(w, 'a', '150'); set(w, 'b', '100');
    await wait(80);
    s.near('pct: 150→100 is -33.33%', num(text(w, 'r-main')), -33.3333, 0.01);

    set(w, 'mode', 'increase', 'change');
    set(w, 'a', '80'); set(w, 'b', '25');
    await wait(80);
    s.eq('pct: 80 +25% = 100', num(text(w, 'r-main')), 100);

    set(w, 'mode', 'decrease', 'change');
    set(w, 'a', '100'); set(w, 'b', '20');
    await wait(80);
    s.eq('pct: 100 -20% = 80', num(text(w, 'r-main')), 80);

    set(w, 'mode', 'reverse', 'change');
    set(w, 'a', '50'); set(w, 'b', '25');
    await wait(80);
    s.eq('pct: 50 is 25% of 200', num(text(w, 'r-main')), 200);

    // Division by zero
    set(w, 'mode', 'what', 'change');
    set(w, 'a', '5'); set(w, 'b', '0');
    await wait(80);
    s.match('pct: divide by zero rejected', text(w, 'status'), /divide by zero/i);
    s.noErrors(errors);
  }

  /* ---------- Loan ---------- */
  {
    const { window: w, errors } = await boot('tools/loan-calculator.html');

    // £200,000 at 6% over 30 years → monthly payment $1,199.10
    // (standard amortization formula, verified independently)
    set(w, 'principal', '200000');
    set(w, 'rate', '6');
    set(w, 'years', '30');
    set(w, 'extra', '0');
    await wait(350);
    s.near('loan: 200k @ 6% /30yr = 1199.10/mo', num(text(w, 'r-payment')), 1199.10, 0.5);
    s.near('loan: total interest ≈ 231,676', num(text(w, 'r-interest')), 231676, 200);

    // Zero interest degenerates to simple division
    set(w, 'rate', '0');
    set(w, 'years', '10');
    set(w, 'principal', '120000');
    await wait(350);
    s.near('loan: 0% → principal/months', num(text(w, 'r-payment')), 1000, 0.5);
    s.near('loan: 0% → no interest', num(text(w, 'r-interest')), 0, 0.01);

    // Extra payments shorten the term
    set(w, 'rate', '6');
    set(w, 'principal', '200000');
    set(w, 'years', '30');
    await wait(350);
    const baseTerm = text(w, 'r-payoff');
    set(w, 'extra', '200');
    await wait(350);
    s.check('loan: extra payment shortens term', text(w, 'r-payoff') !== baseTerm, `${baseTerm} → ${text(w, 'r-payoff')}`);
    s.check('loan: savings panel appears', w.document.getElementById('savings').hidden === false);
    s.match('loan: savings text mentions interest', text(w, 'savings-text'), /saves/i);

    s.check('loan: schedule table renders', w.document.querySelector('#schedule table') !== null);
    s.noErrors(errors);
  }

  /* ---------- BMI ---------- */
  {
    const { window: w, errors } = await boot('tools/bmi-calculator.html');

    // 70 kg at 1.75 m → 70 / 3.0625 = 22.86
    set(w, 'units', 'metric', 'change');
    set(w, 'height-cm', '175');
    set(w, 'weight-kg', '70');
    await wait(80);
    s.near('bmi: 70kg/175cm = 22.9', num(text(w, 'r-bmi')), 22.9, 0.05);
    s.eq('bmi: category healthy', text(w, 'r-category'), 'Healthy weight');

    set(w, 'weight-kg', '95');
    await wait(80);
    s.near('bmi: 95kg/175cm = 31.0', num(text(w, 'r-bmi')), 31.0, 0.05);
    s.match('bmi: category obese', text(w, 'r-category'), /obese/i);

    set(w, 'weight-kg', '50');
    await wait(80);
    s.match('bmi: category underweight', text(w, 'r-category'), /underweight/i);

    // Imperial: 5'9" 154 lb ≈ same as 175cm/70kg
    set(w, 'units', 'imperial', 'change');
    set(w, 'height-ft', '5');
    set(w, 'height-in', '9');
    set(w, 'weight-lb', '154');
    await wait(80);
    s.near('bmi: imperial matches metric', num(text(w, 'r-bmi')), 22.7, 0.3);

    set(w, 'units', 'metric', 'change');
    set(w, 'height-cm', '175');
    set(w, 'weight-kg', '70');
    await wait(80);
    s.match('bmi: healthy range shown', text(w, 'r-healthy'), /5[0-9](\.\d)?–7[0-9](\.\d)? kg/);

    set(w, 'height-cm', '400');
    await wait(80);
    s.match('bmi: absurd height rejected', text(w, 'status'), /out of range/i);
    s.noErrors(errors);
  }

  /* ---------- Tip ---------- */
  {
    const { window: w, errors } = await boot('tools/tip-calculator.html');

    set(w, 'bill', '100');
    set(w, 'tip', '20');
    set(w, 'people', '1');
    set(w, 'tax', '0');
    await wait(80);
    s.eq('tip: 20% of 100 = 20', num(text(w, 'r-tip')), 20);
    s.eq('tip: total 120', num(text(w, 'r-total')), 120);

    set(w, 'people', '4');
    await wait(80);
    s.eq('tip: split 4 ways = 30', num(text(w, 'r-each')), 30);

    // Tipping pre-tax on a bill that includes 10% tax
    set(w, 'people', '1');
    set(w, 'tax', '10');
    set(w, 'tip-pretax', true, 'change');
    await wait(80);
    // pre-tax base = 100/1.1 = 90.91; 20% = 18.18
    s.near('tip: pre-tax tip is lower', num(text(w, 'r-tip')), 18.18, 0.02);

    set(w, 'tip-pretax', false, 'change');
    set(w, 'tax', '0');
    set(w, 'bill', '84.50');
    set(w, 'tip', '18');
    set(w, 'rounding', 'up', 'change');
    await wait(80);
    s.check('tip: round up gives whole total', Number.isInteger(num(text(w, 'r-total'))));

    s.check('tip: preset chips render', w.document.querySelectorAll('#presets .chip').length === 5);
    s.noErrors(errors);
  }

  /* ---------- Age ---------- */
  {
    const { window: w, errors } = await boot('tools/age-calculator.html');

    set(w, 'dob', '1990-06-15');
    set(w, 'asof', '2025-06-15');
    await wait(80);
    s.eq('age: exactly 35 years', text(w, 'r-age'), '35y 0m 0d');

    set(w, 'asof', '2025-06-14');
    await wait(80);
    s.eq('age: day before 35th birthday', text(w, 'r-age'), '34y 11m 30d');

    set(w, 'dob', '2000-01-31');
    set(w, 'asof', '2000-03-01');
    await wait(80);
    s.match('age: month-end handled', text(w, 'r-age'), /^0y 1m \d+d$/);

    // Born on a known weekday: 15 June 1990 was a Friday
    set(w, 'dob', '1990-06-15');
    set(w, 'asof', '2025-01-01');
    await wait(80);
    s.eq('age: 15 June 1990 was a Friday', text(w, 'r-born'), 'Friday');

    set(w, 'dob', '2030-01-01');
    set(w, 'asof', '2025-01-01');
    await wait(80);
    s.match('age: future DOB rejected', text(w, 'status'), /after the comparison/i);
    s.noErrors(errors);
  }

  /* ---------- Date Difference ---------- */
  {
    const { window: w, errors } = await boot('tools/date-difference-calculator.html');

    set(w, 'start', '2025-01-01');
    set(w, 'end', '2025-01-31');
    set(w, 'inclusive', false, 'change');
    set(w, 'business', false, 'change');
    await wait(80);
    s.eq('datediff: 1-31 Jan exclusive = 30', num(text(w, 'r-days')), 30);

    set(w, 'inclusive', true, 'change');
    await wait(80);
    s.eq('datediff: inclusive = 31', num(text(w, 'r-days')), 31);

    // Jan 2025: 1st is a Wednesday; 1-31 Jan has 23 weekdays
    set(w, 'inclusive', true, 'change');
    set(w, 'business', true, 'change');
    await wait(80);
    s.eq('datediff: business days in Jan 2025 = 23', num(text(w, 'r-days')), 23);

    // Leap year: 2024 has 366 days
    set(w, 'business', false, 'change');
    set(w, 'inclusive', false, 'change');
    set(w, 'start', '2024-01-01');
    set(w, 'end', '2025-01-01');
    await wait(80);
    s.eq('datediff: 2024 is a leap year (366)', num(text(w, 'r-days')), 366);

    // Reversed dates are handled, with a warning
    set(w, 'start', '2025-06-01');
    set(w, 'end', '2025-01-01');
    await wait(80);
    s.match('datediff: reversed dates warned', text(w, 'status'), /swapped/i);

    // Date offset
    set(w, 'start', '2025-01-01');
    set(w, 'end', '2025-02-01');
    set(w, 'offset', '30');
    set(w, 'offset-unit', 'days', 'change');
    await wait(80);
    s.includes('datediff: +30 days from 1 Jan', text(w, 'r-plus'), '31');
    s.noErrors(errors);
  }

  /* ---------- Scientific Calculator ---------- */
  {
    const { window: w, errors } = await boot('tools/scientific-calculator.html');

    const calc = async (expr) => {
      set(w, 'expr', expr);
      click(w, 'evaluate');
      await wait(60);
      return text(w, 'result');
    };

    s.eq('calc: 2+3*4 respects precedence', num(await calc('2+3*4')), 14);
    s.eq('calc: (2+3)*4 respects brackets', num(await calc('(2+3)*4')), 20);
    s.eq('calc: 2^10', num(await calc('2^10')), 1024);
    // Right-associative exponentiation
    s.eq('calc: 2^3^2 = 512 not 64', num(await calc('2^3^2')), 512);
    s.eq('calc: -2^2 = -4', num(await calc('-2^2')), -4);
    s.eq('calc: sqrt(144)', num(await calc('sqrt(144)')), 12);
    s.eq('calc: fact(5)', num(await calc('fact(5)')), 120);
    s.eq('calc: 5!', num(await calc('5!')), 120);
    s.near('calc: pi', num(await calc('pi')), 3.14159, 0.001);
    s.near('calc: ln(e)', num(await calc('ln(e)')), 1, 1e-9);
    s.eq('calc: log(1000)', num(await calc('log(1000)')), 3);
    s.near('calc: sin(pi/2) radians', num(await calc('sin(pi/2)')), 1, 1e-9);

    set(w, 'angle', 'deg', 'change');
    await wait(60);
    s.near('calc: sin(90) degrees', num(await calc('sin(90)')), 1, 1e-9);
    s.near('calc: cos(180) degrees', num(await calc('cos(180)')), -1, 1e-9);
    set(w, 'angle', 'rad', 'change');

    // ans references the previous result
    await calc('10');
    s.eq('calc: ans reuses last result', num(await calc('ans*5')), 50);

    // Error handling — and crucially, no eval()
    await calc('1/0');
    s.match('calc: division by zero', text(w, 'status'), /division by zero/i);
    await calc('(1+2');
    s.match('calc: unbalanced bracket', text(w, 'status'), /missing closing/i);
    await calc('nosuchfn(2)');
    s.match('calc: unknown function', text(w, 'status'), /unknown function/i);

    // The security-relevant assertion: arbitrary JS must not execute
    w.__pwned = false;
    await calc('__pwned=true');
    s.check('calc: does not execute arbitrary JS', w.__pwned === false);
    s.eq('calc: rejects assignment expression', text(w, 'result'), 'Error');

    s.check('calc: history renders', w.document.querySelectorAll('#history .chip').length > 0);
    s.noErrors(errors);
  }

  /* ---------- Discount ---------- */
  {
    const { window: w, errors } = await boot('tools/discount-calculator.html');

    set(w, 'mode', 'sale', 'change');
    set(w, 'price', '200'); set(w, 'discount', '25'); set(w, 'tax', '0');
    await wait(80);
    s.eq('discount: 200 -25% = 150', num(text(w, 'r-final')), 150);
    s.eq('discount: saved 50', num(text(w, 'r-saved')), 50);

    // The headline case: stacked discounts do not add
    set(w, 'mode', 'stacked', 'change');
    set(w, 'price', '100'); set(w, 'discount', '20'); set(w, 'discount2', '20');
    await wait(80);
    s.eq('discount: 20%+20% leaves 64', num(text(w, 'r-final')), 64);
    s.eq('discount: effective is 36% not 40%', num(text(w, 'r-effective')), 36);
    s.includes('discount: explains the difference', text(w, 'working'), '40.0%');

    set(w, 'mode', 'original', 'change');
    set(w, 'saleprice', '150'); set(w, 'discount', '25');
    await wait(80);
    s.eq('discount: reverse to 200', num(text(w, 'r-saved')), 50);

    set(w, 'mode', 'percent', 'change');
    set(w, 'price', '200'); set(w, 'saleprice', '150');
    await wait(80);
    s.eq('discount: 200→150 is 25% off', num(text(w, 'r-effective')), 25);

    // Tax applied after discount
    set(w, 'mode', 'sale', 'change');
    set(w, 'price', '100'); set(w, 'discount', '50'); set(w, 'tax', '20');
    await wait(80);
    s.eq('discount: 100 -50% +20% tax = 60', num(text(w, 'r-final')), 60);
    s.noErrors(errors);
  }

  /* ---------- Compound Interest ---------- */
  {
    const { window: w, errors } = await boot('tools/compound-interest-calculator.html');

    // 10,000 at 7% annually for 10 years, no contributions
    // = 10000 * 1.07^10 = 19,671.51
    set(w, 'principal', '10000');
    set(w, 'rate', '7');
    set(w, 'years', '10');
    set(w, 'contribution', '0');
    set(w, 'contrib-freq', '0', 'change');
    set(w, 'compound', '1', 'change');
    set(w, 'inflation', '0');
    await wait(350);
    s.near('compound: 10k @7% 10yr annual = 19671', num(text(w, 'r-final')), 19671.51, 1);
    s.near('compound: contributed stays 10k', num(text(w, 'r-contributed')), 10000, 0.5);
    s.near('compound: growth 9671', num(text(w, 'r-growth')), 9671.51, 1);

    // Monthly compounding beats annual, but not by much
    set(w, 'compound', '12', 'change');
    await wait(350);
    const monthly = num(text(w, 'r-final'));
    s.check('compound: monthly > annual', monthly > 19671.51);
    s.check('compound: but only slightly', monthly < 20200);

    // Zero rate means no growth
    set(w, 'rate', '0');
    await wait(350);
    s.near('compound: 0% → no growth', num(text(w, 'r-growth')), 0, 0.01);

    // Inflation adjustment
    set(w, 'rate', '7');
    set(w, 'inflation', '3');
    await wait(350);
    s.check('compound: real value below nominal',
      num(text(w, 'r-real')) < num(text(w, 'r-final')));

    s.check('compound: schedule renders', w.document.querySelector('#schedule table') !== null);
    s.noErrors(errors);
  }

  /* ---------- Fuel Cost ---------- */
  {
    const { window: w, errors } = await boot('tools/fuel-cost-calculator.html');

    // 100 km at 10 L/100km = 10 L; at 1.50/L = 15.00
    set(w, 'distance', '100');
    set(w, 'dist-unit', 'km', 'change');
    set(w, 'efficiency', '10');
    set(w, 'eff-unit', 'l100km', 'change');
    set(w, 'price', '1.50');
    set(w, 'price-unit', 'litre', 'change');
    set(w, 'passengers', '1');
    set(w, 'roundtrip', false, 'change');
    await wait(80);
    s.eq('fuel: 100km @10L/100km = 15.00', num(text(w, 'r-cost')), 15);
    s.near('fuel: 10 litres needed', num(text(w, 'r-fuel')), 10, 0.05);

    set(w, 'roundtrip', true, 'change');
    await wait(80);
    s.eq('fuel: round trip doubles cost', num(text(w, 'r-cost')), 30);

    set(w, 'roundtrip', false, 'change');
    set(w, 'passengers', '4');
    await wait(80);
    s.eq('fuel: split 4 ways', num(text(w, 'r-each')), 3.75);

    // UK and US MPG must give different answers for the same number
    set(w, 'passengers', '1');
    set(w, 'eff-unit', 'mpg-uk', 'change');
    set(w, 'efficiency', '40');
    await wait(80);
    const ukCost = num(text(w, 'r-cost'));
    set(w, 'eff-unit', 'mpg-us', 'change');
    await wait(80);
    const usCost = num(text(w, 'r-cost'));
    s.check('fuel: UK vs US MPG differ', Math.abs(ukCost - usCost) > 0.5, `${ukCost} vs ${usCost}`);
    // 40 MPG measured in the smaller US gallon is better efficiency
    // than 40 MPG imperial, so the same journey costs less.
    s.check('fuel: 40 US MPG is more efficient than 40 UK MPG', usCost < ukCost);

    set(w, 'efficiency', '0');
    await wait(80);
    s.match('fuel: zero efficiency rejected', text(w, 'status'), /above zero/i);
    s.noErrors(errors);
  }

  return s;
};
