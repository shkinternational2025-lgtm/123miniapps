/* ============================================
 123MiniApps.online v2.0
 File: vendor/barcode-encoder.js
 Purpose: Self-contained 1D barcode encoder for
 Code 128, EAN-13, EAN-8 and UPC-A.

 Written in-house rather than pulled from a CDN so
 the site keeps its "no external requests, works
 offline" property.

 Public API:
 BarcodeEncoder.encode(value, symbology)
 → { bits: string, text: string, quietZone: number }

 `bits` is a string of '0' and '1', one character per
 module. Renderers draw a bar for each '1'.
 ============================================ */

const BarcodeEncoder = (() => {
 'use strict';

 /* ============================================
 CODE 128
 ============================================ */

 /**
 * The 107 Code 128 patterns. Each entry gives the widths of
 * six alternating bars and spaces, starting with a bar.
 * Index 106 is the stop pattern, which has a seventh element.
 */
 const C128_PATTERNS = [
 '212222', '222122', '222221', '121223', '121322', '131222', '122213', '122312',
 '132212', '221213', '221312', '231212', '112232', '122132', '122231', '113222',
 '123122', '123221', '223211', '221132', '221231', '213212', '223112', '312131',
 '311222', '321122', '321221', '312212', '322112', '322211', '212123', '212321',
 '232121', '111323', '131123', '131321', '112313', '132113', '132311', '211313',
 '231113', '231311', '112133', '112331', '132131', '113123', '113321', '133121',
 '313121', '211331', '231131', '213113', '213311', '213131', '311123', '311321',
 '331121', '312113', '312311', '332111', '314111', '221411', '431111', '111224',
 '111422', '121124', '121421', '141122', '141221', '112214', '112412', '122114',
 '122411', '142112', '142211', '241211', '221114', '413111', '241112', '134111',
 '111242', '121142', '121241', '114212', '124112', '124211', '411212', '421112',
 '421211', '212141', '214121', '412121', '111143', '111341', '131141', '114113',
 '114311', '411113', '411311', '113141', '114131', '311141', '411131', '211412',
 '211214', '211232', '2331112'
 ];

 const C128_START_B = 104;
 const C128_START_C = 105;
 const C128_STOP = 106;

 /** Turn a width pattern into a bit string, starting with a bar. */
 function patternToBits(pattern) {
 let bits = '';
 let isBar = true;
 for (const ch of pattern) {
 bits += (isBar ? '1' : '0').repeat(Number(ch));
 isBar = !isBar;
 }
 return bits;
 }

 /**
 * Encode as Code 128. Uses subset C for runs of digits, which
 * packs two digits per symbol, and subset B for everything else.
 * @param {string} value
 * @returns {{bits: string, text: string, quietZone: number}}
 */
 function code128(value) {
 if (!value) throw new Error('Nothing to encode.');

 for (const ch of value) {
 const code = ch.charCodeAt(0);
 if (code < 32 || code > 126) {
 throw new Error('Code 128 here supports printable ASCII only (space to ~).');
 }
 }

 const codes = [];
 let i = 0;

 // An even run of four or more digits is worth switching to subset C for
 const digitRunAt = (pos) => {
 let n = 0;
 while (pos + n < value.length && /\d/.test(value[pos + n])) n++;
 return n;
 };

 let mode = null;
 const startRun = digitRunAt(0);

 if (startRun >= 4 && startRun % 2 === 0) {
 codes.push(C128_START_C);
 mode = 'C';
 } else {
 codes.push(C128_START_B);
 mode = 'B';
 }

 while (i < value.length) {
 const run = digitRunAt(i);

 // The spec's guidance: switching to subset C pays for itself at
 // four or more digits when the run reaches the end of the data
 // (no switch back is needed), and at six or more mid-string
 // (where the cost of switching back has to be recovered).
 const runReachesEnd = i + run === value.length;
 const worthSwitching = run % 2 === 0 && (run >= 6 || (run >= 4 && runReachesEnd));

 if (mode === 'B' && worthSwitching) {
 codes.push(99); // switch to subset C
 mode = 'C';
 continue;
 }

 if (mode === 'C') {
 if (run >= 2) {
 codes.push(Number(value.substr(i, 2)));
 i += 2;
 continue;
 }
 codes.push(100); // switch to subset B
 mode = 'B';
 continue;
 }

 // Subset B: value 0 is a space (ASCII 32)
 codes.push(value.charCodeAt(i) - 32);
 i++;
 }

 // Checksum: start value plus each symbol weighted by its position
 let sum = codes[0];
 for (let k = 1; k < codes.length; k++) sum += codes[k] * k;
 codes.push(sum % 103);
 codes.push(C128_STOP);

 const bits = codes.map((c) => patternToBits(C128_PATTERNS[c])).join('');
 return { bits, text: value, quietZone: 10 };
 }

 /* ============================================
 EAN / UPC
 ============================================ */

 const EAN_L = ['0001101', '0011001', '0010011', '0111101', '0100011',
 '0110001', '0101111', '0111011', '0110111', '0001011'];
 const EAN_G = ['0100111', '0110011', '0011011', '0100001', '0011101',
 '0111001', '0000101', '0010001', '0001001', '0010111'];
 const EAN_R = ['1110010', '1100110', '1101100', '1000010', '1011100',
 '1001110', '1010000', '1000100', '1001000', '1110100'];

 /** Parity pattern for the left half, selected by the first digit. */
 const EAN_PARITY = [
 'LLLLLL', 'LLGLGG', 'LLGGLG', 'LLGGGL', 'LGLLGG',
 'LGGLLG', 'LGGGLL', 'LGLGLG', 'LGLGGL', 'LGGLGL'
 ];

 /**
 * EAN/UPC check digit: weight digits 1,3,1,3… from the left,
 * then take the amount needed to reach the next multiple of ten.
 * @param {string} digits - without the check digit
 * @returns {number}
 */
 function eanCheckDigit(digits) {
 let sum = 0;
 const rev = digits.split('').reverse();
 // Working right to left, the rightmost digit is weighted 3
 rev.forEach((d, i) => { sum += Number(d) * (i % 2 === 0 ? 3 : 1); });
 return (10 - (sum % 10)) % 10;
 }

 /**
 * Encode EAN-13. Accepts 12 digits (check digit computed) or 13
 * (check digit verified).
 */
 function ean13(value) {
 const digits = String(value).replace(/\D/g, '');

 if (digits.length !== 12 && digits.length !== 13) {
 throw new Error('EAN-13 needs 12 digits, or 13 including the check digit.');
 }

 const body = digits.slice(0, 12);
 const check = eanCheckDigit(body);

 if (digits.length === 13 && Number(digits[12]) !== check) {
 throw new Error(`Check digit should be ${check}, not ${digits[12]}.`);
 }

 const full = body + check;
 const parity = EAN_PARITY[Number(full[0])];

 let bits = '101'; // start guard

 for (let i = 1; i <= 6; i++) {
 const d = Number(full[i]);
 bits += parity[i - 1] === 'L' ? EAN_L[d] : EAN_G[d];
 }

 bits += '01010'; // centre guard

 for (let i = 7; i <= 12; i++) {
 bits += EAN_R[Number(full[i])];
 }

 bits += '101'; // end guard

 return { bits, text: full, quietZone: 11 };
 }

 /** Encode EAN-8, 7 digits plus a check digit. */
 function ean8(value) {
 const digits = String(value).replace(/\D/g, '');

 if (digits.length !== 7 && digits.length !== 8) {
 throw new Error('EAN-8 needs 7 digits, or 8 including the check digit.');
 }

 const body = digits.slice(0, 7);
 const check = eanCheckDigit(body);

 if (digits.length === 8 && Number(digits[7]) !== check) {
 throw new Error(`Check digit should be ${check}, not ${digits[7]}.`);
 }

 const full = body + check;

 let bits = '101';
 for (let i = 0; i < 4; i++) bits += EAN_L[Number(full[i])];
 bits += '01010';
 for (let i = 4; i < 8; i++) bits += EAN_R[Number(full[i])];
 bits += '101';

 return { bits, text: full, quietZone: 7 };
 }

 /**
 * Encode UPC-A. It is structurally EAN-13 with a leading zero,
 * so encode it that way and report the 12-digit text.
 */
 function upca(value) {
 const digits = String(value).replace(/\D/g, '');

 if (digits.length !== 11 && digits.length !== 12) {
 throw new Error('UPC-A needs 11 digits, or 12 including the check digit.');
 }

 const body = digits.slice(0, 11);
 const check = eanCheckDigit(body);

 if (digits.length === 12 && Number(digits[11]) !== check) {
 throw new Error(`Check digit should be ${check}, not ${digits[11]}.`);
 }

 const full = body + check;
 const result = ean13('0' + full.slice(0, 11));

 return { bits: result.bits, text: full, quietZone: 9 };
 }

 /* ============================================
 Public API
 ============================================ */

 const SYMBOLOGIES = {
 code128: { name: 'Code 128', encode: code128 },
 ean13: { name: 'EAN-13', encode: ean13 },
 ean8: { name: 'EAN-8', encode: ean8 },
 upca: { name: 'UPC-A', encode: upca }
 };

 /**
 * @param {string} value - encoded verbatim; the caller trims if it wants to
 * @param {'code128'|'ean13'|'ean8'|'upca'} symbology
 * @returns {{bits: string, text: string, quietZone: number, symbology: string}}
 */
 function encode(value, symbology = 'code128') {
 const spec = SYMBOLOGIES[symbology];
 if (!spec) throw new Error(`Unknown symbology “${symbology}”.`);

 // Deliberately no trim(): silently altering the payload would mean
 // the printed barcode does not match what the caller asked for.
 const result = spec.encode(String(value));
 return { ...result, symbology: spec.name };
 }

 return { encode, eanCheckDigit, SYMBOLOGIES };
})();

if (typeof window !== 'undefined') window.BarcodeEncoder = BarcodeEncoder;
if (typeof module !== 'undefined' && module.exports) module.exports = BarcodeEncoder;
