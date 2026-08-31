/* ============================================
   123MiniApps.online v2.0
   File: test/run.js
   Purpose: Test runner.

   Usage:
     node test/run.js            run every suite
     node test/run.js text       run one suite
     node test/run.js text calc  run several
   ============================================ */

const fs = require('fs');
const path = require('path');

const SUITES = [
  'text', 'converter', 'calculator', 'generator', 'developer',
  'security', 'design', 'content', 'productivity', 'fun', 'image',
  'core'
];

async function main() {
  const requested = process.argv.slice(2);
  const names = requested.length ? requested : SUITES;

  let totalPass = 0;
  let totalFail = 0;
  const failures = [];

  for (const name of names) {
    const file = path.join(__dirname, `phase-${name}.js`);
    if (!fs.existsSync(file)) continue;

    const suite = await require(file)();

    console.log(`\n━━ ${suite.name} ━━`);
    for (const r of suite.results) {
      if (r.ok) {
        console.log('  ✓ ' + r.label);
      } else {
        console.log('  ✗ ' + r.label + (r.detail ? '   → ' + r.detail : ''));
        failures.push(`${suite.name}: ${r.label}${r.detail ? ' — ' + r.detail : ''}`);
      }
    }
    console.log(`  ${suite.passed} passed, ${suite.failed} failed`);

    totalPass += suite.passed;
    totalFail += suite.failed;
  }

  console.log('\n' + '═'.repeat(52));
  console.log(`TOTAL  ${totalPass} passed, ${totalFail} failed`);

  if (failures.length) {
    console.log('\nFailures:');
    failures.forEach((f) => console.log('  - ' + f));
  }

  process.exit(totalFail ? 1 : 0);
}

main().catch((e) => {
  console.error('runner crashed:', e);
  process.exit(2);
});
