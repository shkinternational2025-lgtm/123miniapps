/* ============================================
 123MiniApps.online v2.0
 File: vendor/qr-encoder.js
 Purpose: A self-contained QR Code (ISO/IEC 18004)
 encoder, byte mode, versions 1-10,
 error correction levels L/M/Q/H.

 Written in-house rather than pulled from a CDN so
 the site keeps its "no external requests, works
 offline" property. ~9KB unminified.

 Public API:
 QREncoder.encode(text, { ecl, minVersion })
 → { size, modules: boolean[][], version, ecl }
 ============================================ */

const QREncoder = (() => {
 'use strict';

 /* ============================================
 GF(256) arithmetic for Reed-Solomon
 Field generator polynomial: x^8 + x^4 + x^3 + x^2 + 1 (0x11D)
 ============================================ */
 const EXP = new Uint8Array(512);
 const LOG = new Uint8Array(256);

 (function buildTables() {
 let x = 1;
 for (let i = 0; i < 255; i++) {
 EXP[i] = x;
 LOG[x] = i;
 x <<= 1;
 if (x & 0x100) x ^= 0x11d;
 }
 for (let i = 255; i < 512; i++) EXP[i] = EXP[i - 255];
 })();

 /** Multiply two GF(256) elements. */
 function gfMul(a, b) {
 if (a === 0 || b === 0) return 0;
 return EXP[LOG[a] + LOG[b]];
 }

 /**
 * Build the Reed-Solomon generator polynomial of a given degree.
 * @param {number} degree
 * @returns {Uint8Array} coefficients, highest term omitted
 */
 function rsGeneratorPoly(degree) {
 let poly = new Uint8Array([1]);

 for (let i = 0; i < degree; i++) {
 const next = new Uint8Array(poly.length + 1);
 for (let j = 0; j < poly.length; j++) {
 next[j] ^= poly[j];
 next[j + 1] ^= gfMul(poly[j], EXP[i]);
 }
 poly = next;
 }

 return poly.slice(1);
 }

 /**
 * Compute EC codewords for one block.
 * @param {Uint8Array} data
 * @param {number} ecLen
 * @returns {Uint8Array}
 */
 function rsEncode(data, ecLen) {
 const gen = rsGeneratorPoly(ecLen);
 const result = new Uint8Array(ecLen);

 for (const byte of data) {
 const factor = byte ^ result[0];
 result.copyWithin(0, 1);
 result[ecLen - 1] = 0;
 for (let i = 0; i < ecLen; i++) {
 result[i] ^= gfMul(gen[i], factor);
 }
 }

 return result;
 }

 /* ============================================
 Version tables (1-10)
 ============================================ */

 /** Total codewords (data + EC) per version. */
 const TOTAL_CODEWORDS = [0, 26, 44, 70, 100, 134, 172, 196, 242, 292, 346];

 /**
 * Block structure per version and EC level:
 * [ecCodewordsPerBlock, blocksInGroup1, dataPerBlock1, blocksInGroup2, dataPerBlock2]
 */
 const ECB = {
 L: [
 null,
 [7, 1, 19, 0, 0], [10, 1, 34, 0, 0], [15, 1, 55, 0, 0], [20, 1, 80, 0, 0], [26, 1, 108, 0, 0],
 [18, 2, 68, 0, 0], [20, 2, 78, 0, 0], [24, 2, 97, 0, 0], [30, 2, 116, 0, 0], [18, 2, 68, 2, 69]
 ],
 M: [
 null,
 [10, 1, 16, 0, 0], [16, 1, 28, 0, 0], [26, 1, 44, 0, 0], [18, 2, 32, 0, 0], [24, 2, 43, 0, 0],
 [16, 4, 27, 0, 0], [18, 4, 31, 0, 0], [22, 2, 38, 2, 39], [22, 3, 36, 2, 37], [26, 4, 43, 1, 44]
 ],
 Q: [
 null,
 [13, 1, 13, 0, 0], [22, 1, 22, 0, 0], [18, 2, 17, 0, 0], [26, 2, 24, 0, 0], [18, 2, 15, 2, 16],
 [24, 4, 19, 0, 0], [18, 2, 14, 4, 15], [22, 4, 18, 2, 19], [20, 4, 16, 4, 17], [24, 6, 19, 2, 20]
 ],
 H: [
 null,
 [17, 1, 9, 0, 0], [28, 1, 16, 0, 0], [22, 2, 13, 0, 0], [16, 4, 9, 0, 0], [22, 2, 11, 2, 12],
 [28, 4, 15, 0, 0], [26, 4, 13, 1, 14], [26, 4, 14, 2, 15], [24, 4, 12, 4, 13], [28, 6, 15, 2, 16]
 ]
 };

 /** Alignment pattern centre coordinates per version. */
 const ALIGNMENT = [
 [], [], [6, 18], [6, 22], [6, 26], [6, 30], [6, 34],
 [6, 22, 38], [6, 24, 42], [6, 26, 46], [6, 28, 50]
 ];

 const ECL_BITS = { L: 1, M: 0, Q: 3, H: 2 };
 const MAX_VERSION = 10;

 /** Data codeword capacity for a version + EC level. */
 function dataCapacity(version, ecl) {
 const [ecLen, b1, d1, b2, d2] = ECB[ecl][version];
 void ecLen;
 return b1 * d1 + b2 * d2;
 }

 /* ============================================
 Bit buffer
 ============================================ */
 class BitBuffer {
 constructor() {
 this.bits = [];
 }

 /** @param {number} value @param {number} length */
 put(value, length) {
 for (let i = length - 1; i >= 0; i--) {
 this.bits.push((value >>> i) & 1);
 }
 }

 get length() {
 return this.bits.length;
 }

 /** @returns {Uint8Array} */
 toBytes() {
 const bytes = new Uint8Array(Math.ceil(this.bits.length / 8));
 this.bits.forEach((bit, i) => {
 if (bit) bytes[i >>> 3] |= 0x80 >>> (i & 7);
 });
 return bytes;
 }
 }

 /* ============================================
 Data encoding
 ============================================ */

 /**
 * Encode text as byte-mode data codewords for the chosen version.
 * @param {Uint8Array} bytes - UTF-8 bytes of the payload
 * @param {number} version
 * @param {string} ecl
 * @returns {Uint8Array} data codewords, padded to capacity
 */
 function buildDataCodewords(bytes, version, ecl) {
 const capacity = dataCapacity(version, ecl);
 const buffer = new BitBuffer();

 // Mode indicator: 0100 = byte mode
 buffer.put(0b0100, 4);

 // Character count: 8 bits for versions 1-9, 16 bits for 10-26
 buffer.put(bytes.length, version <= 9 ? 8 : 16);

 for (const byte of bytes) buffer.put(byte, 8);

 // Terminator: up to four zero bits, if there's room
 const capacityBits = capacity * 8;
 const terminator = Math.min(4, capacityBits - buffer.length);
 buffer.put(0, terminator);

 // Pad to a byte boundary
 if (buffer.length % 8 !== 0) buffer.put(0, 8 - (buffer.length % 8));

 const data = new Uint8Array(capacity);
 data.set(buffer.toBytes());

 // Fill any remaining codewords with the specified alternating pad bytes
 const used = buffer.length / 8;
 for (let i = used, alt = 0; i < capacity; i++, alt++) {
 data[i] = alt % 2 === 0 ? 0xec : 0x11;
 }

 return data;
 }

 /**
 * Split into blocks, add error correction, and interleave per spec.
 * @returns {Uint8Array} the final codeword sequence
 */
 function interleave(data, version, ecl) {
 const [ecLen, b1, d1, b2, d2] = ECB[ecl][version];
 const totalBlocks = b1 + b2;

 const dataBlocks = [];
 const ecBlocks = [];
 let offset = 0;

 for (let i = 0; i < totalBlocks; i++) {
 const size = i < b1 ? d1 : d2;
 const block = data.slice(offset, offset + size);
 offset += size;
 dataBlocks.push(block);
 ecBlocks.push(rsEncode(block, ecLen));
 }

 const result = new Uint8Array(TOTAL_CODEWORDS[version]);
 let pos = 0;

 // Interleave data codewords column-wise across blocks
 const maxData = Math.max(d1, d2);
 for (let i = 0; i < maxData; i++) {
 for (const block of dataBlocks) {
 if (i < block.length) result[pos++] = block[i];
 }
 }

 // Then interleave EC codewords the same way
 for (let i = 0; i < ecLen; i++) {
 for (const block of ecBlocks) {
 result[pos++] = block[i];
 }
 }

 return result;
 }

 /* ============================================
 Matrix construction
 ============================================ */

 class Matrix {
 constructor(version) {
 this.version = version;
 this.size = version * 4 + 17;
 this.modules = Array.from({ length: this.size }, () => new Array(this.size).fill(false));
 this.reserved = Array.from({ length: this.size }, () => new Array(this.size).fill(false));
 }

 set(x, y, dark, isFunction = true) {
 this.modules[y][x] = dark;
 if (isFunction) this.reserved[y][x] = true;
 }

 /** Draw all patterns that are fixed by the spec. */
 drawFunctionPatterns() {
 const n = this.size;

 // Finder patterns + separators
 this.drawFinder(0, 0);
 this.drawFinder(n - 7, 0);
 this.drawFinder(0, n - 7);

 // Timing patterns
 for (let i = 8; i < n - 8; i++) {
 this.set(i, 6, i % 2 === 0);
 this.set(6, i, i % 2 === 0);
 }

 // Alignment patterns, skipping those that collide with finders
 const centres = ALIGNMENT[this.version];
 for (const cy of centres) {
 for (const cx of centres) {
 const nearFinder =
 (cx === 6 && cy === 6) ||
 (cx === 6 && cy === n - 7) ||
 (cx === n - 7 && cy === 6);
 if (!nearFinder) this.drawAlignment(cx, cy);
 }
 }

 // Reserve the format information areas
 for (let i = 0; i < 9; i++) {
 if (i !== 6) {
 this.set(i, 8, false);
 this.set(8, i, false);
 }
 }
 for (let i = 0; i < 8; i++) {
 this.set(n - 1 - i, 8, false);
 this.set(8, n - 1 - i, false);
 }

 // Permanent dark module
 this.set(8, n - 8, true);

 // Version information blocks, versions 7 and up
 if (this.version >= 7) this.drawVersionInfo();
 }

 drawFinder(x0, y0) {
 // 7x7 pattern plus a one-module separator on the inner sides
 for (let dy = -1; dy <= 7; dy++) {
 for (let dx = -1; dx <= 7; dx++) {
 const x = x0 + dx;
 const y = y0 + dy;
 if (x < 0 || x >= this.size || y < 0 || y >= this.size) continue;

 const inRing = dx >= 0 && dx <= 6 && dy >= 0 && dy <= 6;
 const outerRing = inRing && (dx === 0 || dx === 6 || dy === 0 || dy === 6);
 const innerBlock = dx >= 2 && dx <= 4 && dy >= 2 && dy <= 4;

 this.set(x, y, outerRing || innerBlock);
 }
 }
 }

 drawAlignment(cx, cy) {
 for (let dy = -2; dy <= 2; dy++) {
 for (let dx = -2; dx <= 2; dx++) {
 const dark = Math.max(Math.abs(dx), Math.abs(dy)) !== 1;
 this.set(cx + dx, cy + dy, dark);
 }
 }
 }

 drawVersionInfo() {
 // BCH(18,6) with generator 0x1F25
 let rem = this.version;
 for (let i = 0; i < 12; i++) {
 rem = (rem << 1) ^ ((rem >>> 11) * 0x1f25);
 }
 const bits = (this.version << 12) | rem;

 for (let i = 0; i < 18; i++) {
 const dark = ((bits >>> i) & 1) === 1;
 const a = this.size - 11 + (i % 3);
 const b = Math.floor(i / 3);
 this.set(a, b, dark);
 this.set(b, a, dark);
 }
 }

 /**
 * Format info: 5 data bits (EC level + mask) protected by
 * BCH(15,5), then XORed with 0x5412 so it's never all zeros.
 */
 drawFormatInfo(ecl, mask) {
 const data = (ECL_BITS[ecl] << 3) | mask;
 let rem = data;
 for (let i = 0; i < 10; i++) {
 rem = (rem << 1) ^ ((rem >>> 9) * 0x537);
 }
 const bits = ((data << 10) | rem) ^ 0x5412;

 const n = this.size;

 // Copy 1, around the top-left finder
 for (let i = 0; i <= 5; i++) this.set(8, i, ((bits >>> i) & 1) === 1);
 this.set(8, 7, ((bits >>> 6) & 1) === 1);
 this.set(8, 8, ((bits >>> 7) & 1) === 1);
 this.set(7, 8, ((bits >>> 8) & 1) === 1);
 for (let i = 9; i < 15; i++) this.set(14 - i, 8, ((bits >>> i) & 1) === 1);

 // Copy 2, split between the other two finders
 for (let i = 0; i < 8; i++) this.set(n - 1 - i, 8, ((bits >>> i) & 1) === 1);
 for (let i = 8; i < 15; i++) this.set(8, n - 15 + i, ((bits >>> i) & 1) === 1);
 }

 /**
 * Lay the codewords into the matrix in the spec's zigzag order:
 * two-module-wide columns, right to left, alternating direction,
 * skipping the vertical timing pattern at column 6.
 */
 placeCodewords(codewords) {
 let bitIndex = 0;
 const totalBits = codewords.length * 8;

 for (let right = this.size - 1; right >= 1; right -= 2) {
 // Column 6 is the timing pattern, shift the pair left past it
 if (right === 6) right = 5;

 for (let vert = 0; vert < this.size; vert++) {
 for (let j = 0; j < 2; j++) {
 const x = right - j;
 const upward = ((right + 1) & 2) === 0;
 const y = upward ? this.size - 1 - vert : vert;

 if (this.reserved[y][x]) continue;
 if (bitIndex >= totalBits) continue; // remainder bits stay light

 const bit = (codewords[bitIndex >>> 3] >>> (7 - (bitIndex & 7))) & 1;
 this.modules[y][x] = bit === 1;
 bitIndex++;
 }
 }
 }
 }

 /** Apply one of the eight data masks to non-function modules. */
 applyMask(mask) {
 const rules = [
 (x, y) => (x + y) % 2 === 0,
 (x, y) => y % 2 === 0,
 (x) => x % 3 === 0,
 (x, y) => (x + y) % 3 === 0,
 (x, y) => (Math.floor(y / 2) + Math.floor(x / 3)) % 2 === 0,
 (x, y) => ((x * y) % 2) + ((x * y) % 3) === 0,
 (x, y) => (((x * y) % 2) + ((x * y) % 3)) % 2 === 0,
 (x, y) => (((x + y) % 2) + ((x * y) % 3)) % 2 === 0
 ];

 const rule = rules[mask];

 for (let y = 0; y < this.size; y++) {
 for (let x = 0; x < this.size; x++) {
 if (!this.reserved[y][x] && rule(x, y)) {
 this.modules[y][x] = !this.modules[y][x];
 }
 }
 }
 }

 /**
 * The spec's four penalty rules. Lower is better; the encoder
 * tries all eight masks and keeps the lowest-scoring one.
 * @returns {number}
 */
 penalty() {
 const n = this.size;
 let score = 0;

 // Rule 1, runs of five or more same-colour modules in a line
 const scanLine = (get) => {
 for (let a = 0; a < n; a++) {
 let runColor = get(a, 0);
 let runLength = 1;
 for (let b = 1; b < n; b++) {
 const color = get(a, b);
 if (color === runColor) {
 runLength++;
 } else {
 if (runLength >= 5) score += runLength - 2;
 runColor = color;
 runLength = 1;
 }
 }
 if (runLength >= 5) score += runLength - 2;
 }
 };

 scanLine((y, x) => this.modules[y][x]);
 scanLine((x, y) => this.modules[y][x]);

 // Rule 2, 2x2 blocks of a single colour
 for (let y = 0; y < n - 1; y++) {
 for (let x = 0; x < n - 1; x++) {
 const c = this.modules[y][x];
 if (
 c === this.modules[y][x + 1] &&
 c === this.modules[y + 1][x] &&
 c === this.modules[y + 1][x + 1]
 ) {
 score += 3;
 }
 }
 }

 // Rule 3, finder-like 1:1:3:1:1 patterns with four light modules
 const PATTERN_A = [true, false, true, true, true, false, true, false, false, false, false];
 const PATTERN_B = [false, false, false, false, true, false, true, true, true, false, true];

 const matchesAt = (get, a, b, pattern) => {
 for (let k = 0; k < 11; k++) {
 if (get(a, b + k) !== pattern[k]) return false;
 }
 return true;
 };

 for (let a = 0; a < n; a++) {
 for (let b = 0; b <= n - 11; b++) {
 const row = (i, j) => this.modules[i][j];
 const col = (i, j) => this.modules[j][i];
 if (matchesAt(row, a, b, PATTERN_A) || matchesAt(row, a, b, PATTERN_B)) score += 40;
 if (matchesAt(col, a, b, PATTERN_A) || matchesAt(col, a, b, PATTERN_B)) score += 40;
 }
 }

 // Rule 4, deviation from a 50/50 light/dark balance
 let dark = 0;
 for (let y = 0; y < n; y++) {
 for (let x = 0; x < n; x++) {
 if (this.modules[y][x]) dark++;
 }
 }
 const percent = (dark * 100) / (n * n);
 score += Math.floor(Math.abs(percent - 50) / 5) * 10;

 return score;
 }
 }

 /* ============================================
 Public API
 ============================================ */

 /**
 * Encode text into a QR matrix.
 * @param {string} text
 * @param {{ecl?: 'L'|'M'|'Q'|'H', minVersion?: number, mask?: number}} [options]
 * `mask` forces a specific 0-7 data mask instead of letting the
 * penalty rules choose. Used by the test suite to compare output
 * against a reference encoder; leave it unset in production.
 * @returns {{size: number, modules: boolean[][], version: number, ecl: string, mask: number}}
 * @throws {Error} if the payload exceeds version 10 capacity
 */
 function encode(text, options = {}) {
 const ecl = options.ecl && ECL_BITS[options.ecl] !== undefined ? options.ecl : 'M';
 const minVersion = options.minVersion || 1;

 if (!text) throw new Error('Nothing to encode.');

 const bytes = new TextEncoder().encode(text);

 // Pick the smallest version that fits, accounting for the
 // character-count field widening at version 10.
 let version = 0;
 for (let v = minVersion; v <= MAX_VERSION; v++) {
 const headerBits = 4 + (v <= 9 ? 8 : 16);
 const neededBytes = Math.ceil((headerBits + bytes.length * 8) / 8);
 if (neededBytes <= dataCapacity(v, ecl)) {
 version = v;
 break;
 }
 }

 if (!version) {
 throw new Error(
 `Too much data for error correction level ${ecl}. ` +
 `Shorten the text or choose a lower correction level.`
 );
 }

 const data = buildDataCodewords(bytes, version, ecl);
 const codewords = interleave(data, version, ecl);

 /** Build the matrix for one specific mask. */
 const buildFor = (mask) => {
 const matrix = new Matrix(version);
 matrix.drawFunctionPatterns();
 matrix.placeCodewords(codewords);
 matrix.drawFormatInfo(ecl, mask);
 matrix.applyMask(mask);
 return matrix;
 };

 let best;
 let bestMask;

 if (Number.isInteger(options.mask) && options.mask >= 0 && options.mask <= 7) {
 bestMask = options.mask;
 best = buildFor(bestMask);
 } else {
 // Try every mask, keep the one the spec's penalty rules prefer.
 let bestScore = Infinity;
 for (let mask = 0; mask < 8; mask++) {
 const matrix = buildFor(mask);
 const score = matrix.penalty();
 if (score < bestScore) {
 bestScore = score;
 best = matrix;
 bestMask = mask;
 }
 }
 }

 return {
 size: best.size,
 modules: best.modules,
 version,
 ecl,
 mask: bestMask
 };
 }

 return { encode, MAX_VERSION };
})();

if (typeof window !== 'undefined') window.QREncoder = QREncoder;
if (typeof module !== 'undefined' && module.exports) module.exports = QREncoder;
