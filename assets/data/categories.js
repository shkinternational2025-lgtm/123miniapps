/* ============================================
 123MiniApps.online v2.0
 File: categories.js
 Purpose: The 11 tool categories. `primary: true`
 categories get full cards on the homepage;
 the rest render as chips in a scroll row.
 ============================================ */

/**
 * @typedef {Object} Category
 * @property {string} id - Matches tool.category
 * @property {string} name - Display name
 * @property {string} icon - Emoji
 * @property {string} desc - One-line description
 * @property {boolean} primary - Show as a full card on the homepage
 * @property {string[]} examples - 3 example tool names
 */

/** @type {Category[]} */
const CATEGORIES = [
 {
 id: 'text',
 name: 'Text Tools',
 icon: '📝',
 desc: 'Clean, count, compare and transform text without leaving the tab.',
 primary: true,
 examples: ['Word Counter', 'Case Converter', 'Text Diff']
 },
 {
 id: 'image',
 name: 'Image Tools',
 icon: '🖼️',
 desc: 'Resize, compress, crop and convert images entirely on your device.',
 primary: true,
 examples: ['Image Compressor', 'Image Resizer', 'Image to Base64']
 },
 {
 id: 'developer',
 name: 'Developer Tools',
 icon: '💻',
 desc: 'Format, validate and debug the payloads you work with every day.',
 primary: true,
 examples: ['JSON Formatter', 'Regex Tester', 'JWT Decoder']
 },
 {
 id: 'converter',
 name: 'Converters',
 icon: '🔄',
 desc: 'Switch between units, formats and encodings in a single click.',
 primary: true,
 examples: ['Unit Converter', 'CSV to JSON', 'Timestamp Converter']
 },
 {
 id: 'generator',
 name: 'Generators',
 icon: '⚙️',
 desc: 'Produce passwords, QR codes, UUIDs and placeholder data instantly.',
 primary: true,
 examples: ['Password Generator', 'QR Code Generator', 'UUID Generator']
 },
 {
 id: 'calculator',
 name: 'Calculators',
 icon: '🧮',
 desc: 'Run the numbers on loans, tips, BMI, percentages and more.',
 primary: true,
 examples: ['Percentage Calculator', 'Loan Calculator', 'BMI Calculator']
 },
 {
 id: 'security',
 name: 'Security Tools',
 icon: '🔒',
 desc: 'Hash, encode and audit, nothing is transmitted anywhere.',
 primary: false,
 examples: ['Hash Generator', 'Password Strength', 'Encryption Tool']
 },
 {
 id: 'design',
 name: 'Design Tools',
 icon: '🎨',
 desc: 'Colors, gradients, shadows and type scales for your next build.',
 primary: false,
 examples: ['Color Picker', 'Gradient Generator', 'Palette Generator']
 },
 {
 id: 'content',
 name: 'Content Tools',
 icon: '📚',
 desc: 'Draft, check and polish copy for the web.',
 primary: false,
 examples: ['Readability Checker', 'Meta Tag Generator', 'Slug Generator']
 },
 {
 id: 'productivity',
 name: 'Productivity Tools',
 icon: '🎯',
 desc: 'Timers, notes and trackers that stay out of your way.',
 primary: false,
 examples: ['Pomodoro Timer', 'Todo List', 'Notepad']
 },
 {
 id: 'fun',
 name: 'Fun Tools',
 icon: '🎉',
 desc: 'Dice, wheels, coin flips and other pleasant distractions.',
 primary: false,
 examples: ['Random Picker', 'Dice Roller', 'Coin Flip']
 }
];

window.CATEGORIES = CATEGORIES;

/** @returns {Category|undefined} */
window.getCategory = (id) => CATEGORIES.find((c) => c.id === id);
