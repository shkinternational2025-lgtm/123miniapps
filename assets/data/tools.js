/* ============================================
 123MiniApps.online v2.0
 File: tools.js
 Purpose: The complete tools database (95 tools).

 ADDING A TOOL, three steps, nothing else:
 1. Append an object to RAW_TOOLS below.
 2. Create tools/<slug>.html from tools/_template.html.
 3. Add the URL to sitemap.xml.
 `url`, `tags` and `slug` are derived automatically by
 normalize() so they can never drift out of sync with
 the tool's name.
 ============================================ */

/**
 * @typedef {Object} Tool
 * @property {number} id Stable identifier
 * @property {string} name Display name
 * @property {string} slug URL-safe name (derived)
 * @property {string} category Category id from categories.js
 * @property {string} icon Emoji
 * @property {string} description One-line summary
 * @property {boolean} premium Shows the "Premium" badge
 * @property {string[]} features 3-4 key capabilities
 * @property {number} usageCount Simulated popularity counter
 * @property {number} rating 1-5
 * @property {boolean} live true = real page exists, false = coming soon
 * @property {string} url Path to the tool page (derived)
 * @property {string[]} tags Search index terms (derived + explicit)
 */

/**
 * Source data. Fields omitted here are filled in by normalize().
 * `keywords` are extra search terms that aren't in the name/description.
 */
const RAW_TOOLS = [
 /* ---------- 📝 TEXT TOOLS (1-10) ---------- */
 { id: 1, name: 'Word Counter', category: 'text', icon: '🔢', premium: false, rating: 4.8, usageCount: 184200,
 description: 'Count words, characters, sentences and reading time as you type.',
 features: ['Live word & character count', 'Reading + speaking time', 'Keyword density', 'Paragraph breakdown'],
 keywords: ['characters', 'letters', 'essay', 'length'] },
 { id: 2, name: 'Case Converter', category: 'text', icon: '🔠', premium: false, rating: 4.7, usageCount: 142800,
 description: 'Switch text between upper, lower, title, sentence, camel and snake case.',
 features: ['9 case styles', 'One-click copy', 'Preserves punctuation', 'Bulk paste support'],
 keywords: ['uppercase', 'lowercase', 'titlecase', 'camelcase', 'snake'] },
 { id: 3, name: 'Text Diff Checker', category: 'text', icon: '🔍', premium: true, rating: 4.9, usageCount: 96400,
 description: 'Compare two blocks of text and highlight every addition and deletion.',
 features: ['Word-level diffing', 'Side-by-side view', 'Ignore whitespace option', 'Copy unified diff'],
 keywords: ['compare', 'difference', 'merge', 'changes'] },
 { id: 4, name: 'Lorem Ipsum Generator', category: 'text', icon: '📄', premium: false, rating: 4.6, usageCount: 118900,
 description: 'Generate placeholder paragraphs, sentences or words for mockups.',
 features: ['Paragraphs / sentences / words', 'Classic or modern variants', 'HTML tag wrapping', 'Instant copy'],
 keywords: ['placeholder', 'dummy text', 'filler', 'mockup'] },
 { id: 5, name: 'Text Reverser', category: 'text', icon: '↔️', premium: false, rating: 4.4, usageCount: 54300,
 description: 'Reverse text by characters, words or lines in a single click.',
 features: ['Character reverse', 'Word reverse', 'Line reverse', 'Palindrome check'],
 keywords: ['backwards', 'flip', 'mirror', 'palindrome'] },
 { id: 6, name: 'Remove Duplicate Lines', category: 'text', icon: '🧹', premium: false, rating: 4.7, usageCount: 87600,
 description: 'Strip repeated lines from any list while keeping the original order.',
 features: ['Case-sensitive toggle', 'Trim whitespace', 'Sort output', 'Duplicate count report'],
 keywords: ['dedupe', 'unique', 'list cleaner', 'repeated'] },
 { id: 7, name: 'Find and Replace', category: 'text', icon: '🔁', premium: false, rating: 4.6, usageCount: 71200,
 description: 'Bulk find-and-replace across large text with optional regex.',
 features: ['Regex mode', 'Match highlighting', 'Replace all or step through', 'Undo history'],
 keywords: ['substitute', 'swap', 'regex', 'bulk edit'] },
 { id: 8, name: 'Text to Speech', category: 'text', icon: '🔊', premium: true, rating: 4.5, usageCount: 63400,
 description: 'Read any text aloud using the voices already installed on your device.',
 features: ['Multiple system voices', 'Rate & pitch control', 'Pause and resume', 'No audio leaves the device'],
 keywords: ['tts', 'read aloud', 'voice', 'speech synthesis'] },
 { id: 9, name: 'Character Counter', category: 'text', icon: '🔤', premium: false, rating: 4.5, usageCount: 92100,
 description: 'Track character limits for tweets, meta descriptions and SMS.',
 features: ['Platform limit presets', 'Live remaining count', 'With/without spaces', 'Over-limit warning'],
 keywords: ['limit', 'twitter', 'sms', 'meta description'] },
 { id: 10, name: 'Text Formatter', category: 'text', icon: '✨', premium: false, rating: 4.6, usageCount: 68700,
 description: 'Tidy messy text: fix spacing, line breaks, indentation and smart quotes.',
 features: ['Collapse extra spaces', 'Normalize line endings', 'Smart quote conversion', 'Trim every line'],
 keywords: ['clean', 'tidy', 'whitespace', 'beautify'] },

 /* ---------- 🖼️ IMAGE TOOLS (11-20) ---------- */
 { id: 11, name: 'Image Compressor', category: 'image', icon: '🗜️', premium: true, rating: 4.9, usageCount: 213500,
 description: 'Shrink JPG, PNG and WebP files without a visible quality drop.',
 features: ['Adjustable quality slider', 'Before/after preview', 'Batch compression', 'Files never uploaded'],
 keywords: ['optimize', 'reduce size', 'shrink', 'jpg', 'png', 'webp'] },
 { id: 12, name: 'Image Resizer', category: 'image', icon: '📐', premium: false, rating: 4.8, usageCount: 176300,
 description: 'Resize images to exact pixel dimensions or a percentage scale.',
 features: ['Lock aspect ratio', 'Preset social sizes', 'Percentage scaling', 'High-quality resampling'],
 keywords: ['scale', 'dimensions', 'resize', 'pixels'] },
 { id: 13, name: 'Image to Base64', category: 'image', icon: '🔗', premium: false, rating: 4.6, usageCount: 88200,
 description: 'Convert an image into a Base64 data URI ready to paste into CSS or HTML.',
 features: ['Data URI output', 'CSS / HTML / JSON snippets', 'Size warning for large files', 'One-click copy'],
 keywords: ['data uri', 'encode', 'inline image', 'css'] },
 { id: 14, name: 'Image Cropper', category: 'image', icon: '✂️', premium: true, rating: 4.8, usageCount: 134900,
 description: 'Crop images with a draggable frame and common aspect-ratio presets.',
 features: ['Freeform or locked ratios', 'Preset 1:1, 16:9, 4:3', 'Pixel-precise nudging', 'Export PNG or JPG'],
 keywords: ['trim', 'cut', 'aspect ratio', 'thumbnail'] },
 { id: 15, name: 'Image Format Converter', category: 'image', icon: '🔄', premium: false, rating: 4.7, usageCount: 121700,
 description: 'Convert between PNG, JPG, WebP and BMP right in the browser.',
 features: ['4 output formats', 'Quality control for lossy formats', 'Transparency handling', 'Batch convert'],
 keywords: ['png to jpg', 'webp', 'bmp', 'convert image'] },
 { id: 16, name: 'Color Picker from Image', category: 'image', icon: '🎨', premium: false, rating: 4.7, usageCount: 79400,
 description: 'Pick any color out of an uploaded image and copy its hex value.',
 features: ['Magnified eyedropper', 'HEX / RGB / HSL output', 'Recent color history', 'Auto palette extraction'],
 keywords: ['eyedropper', 'hex', 'sample color', 'palette'] },
 { id: 17, name: 'Image Filters', category: 'image', icon: '🌈', premium: true, rating: 4.6, usageCount: 67800,
 description: 'Apply grayscale, sepia, blur, contrast and saturation adjustments.',
 features: ['10 live filters', 'Stackable adjustments', 'Reset to original', 'Export edited image'],
 keywords: ['grayscale', 'sepia', 'blur', 'effects', 'edit'] },
 { id: 18, name: 'Favicon Generator', category: 'image', icon: '⭐', premium: false, rating: 4.7, usageCount: 94600,
 description: 'Turn any square image into a complete favicon set with HTML snippet.',
 features: ['16/32/48/180/512px output', 'Apple touch icon', 'Ready-to-paste HTML', 'ZIP download'],
 keywords: ['icon', 'apple touch', 'site icon', 'browser tab'] },
 { id: 19, name: 'Meme Generator', category: 'image', icon: '😂', premium: false, rating: 4.5, usageCount: 108300,
 description: 'Add classic top and bottom captions to any image.',
 features: ['Impact-style caption text', 'Drag to reposition', 'Font size & outline control', 'Download as PNG'],
 keywords: ['caption', 'funny', 'top text', 'bottom text'] },
 { id: 20, name: 'Image Watermark', category: 'image', icon: '💧', premium: true, rating: 4.6, usageCount: 58100,
 description: 'Stamp text or a logo watermark across your images before sharing.',
 features: ['Text or image watermark', 'Opacity & rotation', 'Tiled or single placement', 'Batch apply'],
 keywords: ['copyright', 'brand', 'stamp', 'protect'] },

 /* ---------- 💻 DEVELOPER TOOLS (21-32) ---------- */
 { id: 21, name: 'JSON Formatter', category: 'developer', icon: '{ }', premium: true, rating: 4.9, usageCount: 298400,
 description: 'Beautify, minify and validate JSON with precise error locations.',
 features: ['Pretty print with 2/4-space indent', 'Minify to one line', 'Error line & column', 'Collapsible tree view'],
 keywords: ['beautify', 'prettify', 'validate', 'minify', 'parse'] },
 { id: 22, name: 'Regex Tester', category: 'developer', icon: '🎯', premium: true, rating: 4.8, usageCount: 187600,
 description: 'Test regular expressions against sample text with live match highlighting.',
 features: ['Live match highlighting', 'Capture group inspector', 'All standard flags', 'Common pattern library'],
 keywords: ['regular expression', 'pattern', 'match', 'regexp'] },
 { id: 23, name: 'Base64 Encoder / Decoder', category: 'developer', icon: '🔐', premium: false, rating: 4.8, usageCount: 205300,
 description: 'Encode text to Base64 or decode it back, with full Unicode support.',
 features: ['Encode and decode', 'URL-safe variant', 'Unicode / emoji safe', 'File-to-Base64 mode'],
 keywords: ['btoa', 'atob', 'encode', 'decode', 'base 64'] },
 { id: 24, name: 'URL Encoder / Decoder', category: 'developer', icon: '🌐', premium: false, rating: 4.7, usageCount: 143200,
 description: 'Percent-encode or decode URLs and query string components.',
 features: ['Full URI vs component modes', 'Query parameter breakdown', 'Batch line-by-line', 'Copy result'],
 keywords: ['percent encoding', 'uri', 'querystring', 'escape'] },
 { id: 25, name: 'JWT Decoder', category: 'developer', icon: '🎫', premium: true, rating: 4.8, usageCount: 112700,
 description: 'Inspect the header, payload and expiry of any JSON Web Token.',
 features: ['Header & payload decode', 'Expiry countdown', 'Algorithm display', 'Decoding is local only'],
 keywords: ['token', 'jwt', 'auth', 'bearer', 'claims'] },
 { id: 26, name: 'HTML Formatter', category: 'developer', icon: '📋', premium: false, rating: 4.6, usageCount: 89300,
 description: 'Indent and tidy messy HTML, or minify it for production.',
 features: ['Configurable indent', 'Minify mode', 'Attribute wrapping', 'Syntax highlighting'],
 keywords: ['beautify', 'indent', 'minify', 'markup'] },
 { id: 27, name: 'CSS Minifier', category: 'developer', icon: '🎨', premium: false, rating: 4.6, usageCount: 76500,
 description: 'Strip comments and whitespace from CSS and report the bytes saved.',
 features: ['Comment removal', 'Whitespace collapse', 'Savings percentage', 'Beautify mode too'],
 keywords: ['compress', 'stylesheet', 'optimize', 'minify css'] },
 { id: 28, name: 'JavaScript Minifier', category: 'developer', icon: '⚡', premium: true, rating: 4.5, usageCount: 71900,
 description: 'Reduce JavaScript file size by removing comments and dead whitespace.',
 features: ['Safe whitespace stripping', 'Comment removal', 'Before/after size', 'Copy or download'],
 keywords: ['uglify', 'compress js', 'bundle', 'minify'] },
 { id: 29, name: 'SQL Formatter', category: 'developer', icon: '🗄️', premium: false, rating: 4.6, usageCount: 82400,
 description: 'Format SQL queries with consistent keyword casing and indentation.',
 features: ['Keyword uppercasing', 'Clause-aware indentation', 'Multiple SQL dialects', 'Compact mode'],
 keywords: ['query', 'database', 'beautify sql', 'postgres', 'mysql'] },
 { id: 30, name: 'Markdown Preview', category: 'developer', icon: '📝', premium: false, rating: 4.7, usageCount: 97800,
 description: 'Write Markdown on the left and see rendered HTML update live on the right.',
 features: ['Live split preview', 'GitHub-flavoured syntax', 'Export HTML', 'Synced scrolling'],
 keywords: ['md', 'readme', 'preview', 'github'] },
 { id: 31, name: 'Cron Expression Builder', category: 'developer', icon: '⏰', premium: true, rating: 4.7, usageCount: 64200,
 description: 'Build and read cron schedules with a plain-English explanation.',
 features: ['Visual field builder', 'Human-readable summary', 'Next 5 run times', 'Common presets'],
 keywords: ['schedule', 'crontab', 'job', 'timer'] },
 { id: 32, name: 'HTTP Status Codes', category: 'developer', icon: '📡', premium: false, rating: 4.5, usageCount: 55600,
 description: 'Searchable reference for every HTTP status code and what it means.',
 features: ['All 1xx-5xx codes', 'Instant filter', 'When-to-use guidance', 'RFC references'],
 keywords: ['404', '500', 'response', 'api', 'rest'] },

 /* ---------- 🔄 CONVERTERS (33-42) ---------- */
 { id: 33, name: 'Unit Converter', category: 'converter', icon: '📏', premium: false, rating: 4.8, usageCount: 167400,
 description: 'Convert length, weight, volume, area, speed and temperature.',
 features: ['8 measurement families', 'Metric & imperial', 'Live bidirectional conversion', 'High precision'],
 keywords: ['metric', 'imperial', 'inches', 'kg', 'miles'] },
 { id: 34, name: 'Temperature Converter', category: 'converter', icon: '🌡️', premium: false, rating: 4.6, usageCount: 98200,
 description: 'Switch between Celsius, Fahrenheit and Kelvin instantly.',
 features: ['3-way live conversion', 'Negative value support', 'Rounding control', 'Reference points'],
 keywords: ['celsius', 'fahrenheit', 'kelvin', 'degrees'] },
 { id: 35, name: 'CSV to JSON', category: 'converter', icon: '📊', premium: true, rating: 4.8, usageCount: 124600,
 description: 'Turn CSV data into structured JSON, and convert back again.',
 features: ['Header row detection', 'Custom delimiters', 'JSON to CSV reverse', 'Download result'],
 keywords: ['spreadsheet', 'excel', 'tabular', 'parse csv'] },
 { id: 36, name: 'Timestamp Converter', category: 'converter', icon: '🕐', premium: false, rating: 4.7, usageCount: 139800,
 description: 'Convert Unix timestamps to readable dates across any timezone.',
 features: ['Seconds & milliseconds', 'Timezone selector', 'ISO 8601 output', 'Live current timestamp'],
 keywords: ['unix', 'epoch', 'date', 'time', 'iso'] },
 { id: 37, name: 'Number Base Converter', category: 'converter', icon: '🔢', premium: false, rating: 4.6, usageCount: 71300,
 description: 'Convert between binary, octal, decimal and hexadecimal.',
 features: ['Base 2/8/10/16', 'Arbitrary base 2-36', 'Bit-length display', 'Live sync across fields'],
 keywords: ['binary', 'hex', 'octal', 'decimal', 'radix'] },
 { id: 38, name: 'Roman Numeral Converter', category: 'converter', icon: '🏛️', premium: false, rating: 4.4, usageCount: 44700,
 description: 'Convert numbers to Roman numerals and back, up to 3,999,999.',
 features: ['Both directions', 'Validation of malformed numerals', 'Extended overline notation', 'Copy result'],
 keywords: ['roman', 'numerals', 'latin', 'mmxxv'] },
 { id: 39, name: 'Currency Converter', category: 'converter', icon: '💱', premium: true, rating: 4.5, usageCount: 156200,
 description: 'Convert between currencies using rates you enter or paste in.',
 features: ['Offline rate table', 'Custom rate entry', 'Multi-currency comparison', 'No tracking'],
 keywords: ['exchange rate', 'usd', 'eur', 'money', 'forex'] },
 { id: 40, name: 'Time Zone Converter', category: 'converter', icon: '🌍', premium: false, rating: 4.7, usageCount: 87900,
 description: 'Compare a moment in time across several time zones at once.',
 features: ['Multi-zone board', 'DST-aware', 'Meeting-time finder', 'Shareable link'],
 keywords: ['timezone', 'utc', 'gmt', 'meeting', 'dst'] },
 { id: 41, name: 'File Size Converter', category: 'converter', icon: '💾', premium: false, rating: 4.4, usageCount: 39800,
 description: 'Convert between bytes, KB, MB, GB and TB, binary or decimal.',
 features: ['Binary (1024) & decimal (1000)', 'All units to TB', 'Transfer time estimate', 'Copy value'],
 keywords: ['bytes', 'kilobytes', 'megabytes', 'gigabytes', 'storage'] },
 { id: 42, name: 'Text to ASCII', category: 'converter', icon: '🔡', premium: false, rating: 4.3, usageCount: 36500,
 description: 'Convert text to ASCII or Unicode code points and back.',
 features: ['Decimal & hex code points', 'Reverse decoding', 'Unicode escape output', 'Per-character table'],
 keywords: ['ascii', 'unicode', 'charcode', 'codepoint'] },

 /* ---------- ⚙️ GENERATORS (43-54) ---------- */
 { id: 43, name: 'Password Generator', category: 'generator', icon: '🔑', premium: true, rating: 4.9, usageCount: 342800,
 description: 'Create cryptographically strong passwords with full character control.',
 features: ['crypto.getRandomValues entropy', 'Length 4-128', 'Exclude ambiguous characters', 'Live strength meter'],
 keywords: ['secure', 'random', 'passphrase', 'strong password'] },
 { id: 44, name: 'QR Code Generator', category: 'generator', icon: '📱', premium: true, rating: 4.9, usageCount: 276300,
 description: 'Turn links, text, Wi-Fi credentials or contact cards into a QR code.',
 features: ['URL / text / Wi-Fi / vCard', '4 error-correction levels', 'Custom size & colors', 'PNG & SVG download'],
 keywords: ['qr', 'barcode', 'scan', 'wifi', 'vcard'] },
 { id: 45, name: 'UUID Generator', category: 'generator', icon: '🆔', premium: false, rating: 4.7, usageCount: 128400,
 description: 'Generate RFC-4122 v4 UUIDs one at a time or a thousand at once.',
 features: ['Bulk generation up to 1000', 'Uppercase & no-hyphen variants', 'Cryptographic randomness', 'Copy all'],
 keywords: ['guid', 'unique id', 'v4', 'identifier'] },
 { id: 46, name: 'Random Number Generator', category: 'generator', icon: '🎲', premium: false, rating: 4.6, usageCount: 94200,
 description: 'Draw random numbers in any range, with or without repeats.',
 features: ['Custom min/max', 'Unique-only mode', 'Bulk draws', 'Integer or decimal'],
 keywords: ['rng', 'random', 'draw', 'pick number'] },
 { id: 47, name: 'Hash Generator', category: 'generator', icon: '#️⃣', premium: true, rating: 4.8, usageCount: 118700,
 description: 'Produce SHA-1, SHA-256, SHA-384 and SHA-512 digests of any text.',
 features: ['4 SHA variants via Web Crypto', 'Hex & Base64 output', 'File hashing', 'Compare two hashes'],
 keywords: ['sha256', 'sha1', 'digest', 'checksum', 'md5'] },
 { id: 48, name: 'Slug Generator', category: 'generator', icon: '🔗', premium: false, rating: 4.5, usageCount: 62800,
 description: 'Turn any title into a clean, URL-safe slug.',
 features: ['Accent transliteration', 'Custom separator', 'Stop-word removal', 'Max length trimming'],
 keywords: ['url slug', 'permalink', 'seo', 'kebab case'] },
 { id: 49, name: 'Barcode Generator', category: 'generator', icon: '📊', premium: true, rating: 4.6, usageCount: 73400,
 description: 'Generate Code128, EAN-13 and UPC-A barcodes as downloadable images.',
 features: ['3 barcode symbologies', 'Checksum validation', 'Adjustable bar width', 'PNG & SVG export'],
 keywords: ['ean', 'upc', 'code128', 'scan', 'retail'] },
 { id: 50, name: 'Placeholder Image Generator', category: 'generator', icon: '🖼️', premium: false, rating: 4.4, usageCount: 51600,
 description: 'Create sized placeholder images with custom text and colors.',
 features: ['Any dimensions', 'Custom label text', 'Background & text colors', 'Download PNG'],
 keywords: ['dummy image', 'mockup', 'wireframe', 'placeholder'] },
 { id: 51, name: 'Fake Data Generator', category: 'generator', icon: '👤', premium: true, rating: 4.7, usageCount: 88100,
 description: 'Produce realistic sample names, emails, addresses and phone numbers.',
 features: ['9 field types', 'JSON / CSV export', 'Row count up to 500', 'Locale selection'],
 keywords: ['mock data', 'test data', 'seed', 'faker', 'sample'] },
 { id: 52, name: 'Signature Generator', category: 'generator', icon: '✍️', premium: false, rating: 4.5, usageCount: 67300,
 description: 'Draw or type a signature and export it with a transparent background.',
 features: ['Draw with mouse or touch', 'Typed script fonts', 'Transparent PNG export', 'Adjustable stroke'],
 keywords: ['sign', 'esign', 'autograph', 'transparent png'] },
 { id: 53, name: 'Invoice Generator', category: 'generator', icon: '🧾', premium: true, rating: 4.6, usageCount: 79500,
 description: 'Build a clean itemized invoice and export it as a printable PDF.',
 features: ['Line items with tax', 'Auto totals & subtotals', 'Company logo upload', 'Print-ready PDF'],
 keywords: ['bill', 'receipt', 'freelance', 'pdf invoice'] },
 { id: 54, name: 'Gradient Generator', category: 'generator', icon: '🌈', premium: false, rating: 4.7, usageCount: 102400,
 description: 'Design linear and radial CSS gradients with a live preview.',
 features: ['Unlimited color stops', 'Linear / radial / conic', 'Angle control', 'Copy CSS or Tailwind'],
 keywords: ['css gradient', 'linear-gradient', 'radial', 'background'] },

 /* ---------- 🧮 CALCULATORS (55-64) ---------- */
 { id: 55, name: 'Percentage Calculator', category: 'calculator', icon: '％', premium: false, rating: 4.7, usageCount: 152900,
 description: 'Work out percentages, increases, decreases and percentage differences.',
 features: ['5 calculation modes', 'Step-by-step working', 'Percentage change', 'Reverse percentage'],
 keywords: ['percent', 'increase', 'decrease', 'discount'] },
 { id: 56, name: 'Loan Calculator', category: 'calculator', icon: '🏦', premium: true, rating: 4.8, usageCount: 134700,
 description: 'Estimate monthly payments, total interest and see a full amortization table.',
 features: ['Monthly payment estimate', 'Amortization schedule', 'Total interest breakdown', 'Extra-payment modelling'],
 keywords: ['mortgage', 'emi', 'interest', 'amortization', 'repayment'] },
 { id: 57, name: 'BMI Calculator', category: 'calculator', icon: '⚖️', premium: false, rating: 4.6, usageCount: 118300,
 description: 'Calculate body mass index in metric or imperial units.',
 features: ['Metric & imperial input', 'WHO category ranges', 'Healthy weight range', 'Result explanation'],
 keywords: ['body mass index', 'weight', 'height', 'health'] },
 { id: 58, name: 'Tip Calculator', category: 'calculator', icon: '💵', premium: false, rating: 4.5, usageCount: 96700,
 description: 'Split a bill and work out the tip per person in seconds.',
 features: ['Adjustable tip percentage', 'Split between N people', 'Round-up option', 'Tax handling'],
 keywords: ['gratuity', 'bill split', 'restaurant', 'service charge'] },
 { id: 59, name: 'Age Calculator', category: 'calculator', icon: '🎂', premium: false, rating: 4.6, usageCount: 108200,
 description: 'Find an exact age in years, months, days, plus the next birthday countdown.',
 features: ['Years / months / days', 'Total days lived', 'Next birthday countdown', 'Day-of-week born'],
 keywords: ['birthday', 'date of birth', 'how old', 'dob'] },
 { id: 60, name: 'Date Difference Calculator', category: 'calculator', icon: '📅', premium: false, rating: 4.5, usageCount: 74600,
 description: 'Count the days, weeks and months between any two dates.',
 features: ['Business-day mode', 'Include/exclude end date', 'Weeks & months breakdown', 'Add/subtract days'],
 keywords: ['days between', 'duration', 'business days', 'countdown'] },
 { id: 61, name: 'Scientific Calculator', category: 'calculator', icon: '🔬', premium: true, rating: 4.7, usageCount: 127400,
 description: 'A full scientific calculator with trig, logs, powers and memory.',
 features: ['Trig & inverse trig', 'Log / ln / exponentials', 'Memory registers', 'Keyboard input'],
 keywords: ['sin', 'cos', 'log', 'sqrt', 'math'] },
 { id: 62, name: 'Discount Calculator', category: 'calculator', icon: '🏷️', premium: false, rating: 4.5, usageCount: 83900,
 description: 'Find the sale price, savings and effective discount on any purchase.',
 features: ['Single & stacked discounts', 'Savings amount', 'Reverse: find original price', 'Tax inclusion'],
 keywords: ['sale', 'off', 'markdown', 'savings', 'price'] },
 { id: 63, name: 'Compound Interest Calculator', category: 'calculator', icon: '📈', premium: true, rating: 4.7, usageCount: 91200,
 description: 'Project how savings grow with compounding and regular contributions.',
 features: ['Any compounding frequency', 'Regular contributions', 'Year-by-year table', 'Growth chart'],
 keywords: ['savings', 'investment', 'apy', 'growth', 'returns'] },
 { id: 64, name: 'Fuel Cost Calculator', category: 'calculator', icon: '⛽', premium: false, rating: 4.4, usageCount: 47800,
 description: 'Estimate the fuel cost of a trip from distance, efficiency and price.',
 features: ['MPG or L/100km', 'Round-trip toggle', 'Cost per passenger', 'Multi-leg journeys'],
 keywords: ['gas', 'petrol', 'mpg', 'road trip', 'mileage'] },

 /* ---------- 🔒 SECURITY TOOLS (65-69) ---------- */
 { id: 65, name: 'Password Strength Checker', category: 'security', icon: '🛡️', premium: true, rating: 4.8, usageCount: 143600,
 description: 'Score a password on entropy and estimate how long it would take to crack.',
 features: ['Entropy in bits', 'Crack-time estimate', 'Common-pattern detection', 'Never leaves your browser'],
 keywords: ['entropy', 'crack time', 'secure', 'audit password'] },
 { id: 66, name: 'Encryption Tool', category: 'security', icon: '🔐', premium: true, rating: 4.7, usageCount: 86400,
 description: 'Encrypt and decrypt text with AES-GCM using a passphrase you choose.',
 features: ['AES-256-GCM via Web Crypto', 'PBKDF2 key derivation', 'Copyable ciphertext', 'Fully client-side'],
 keywords: ['aes', 'decrypt', 'cipher', 'secret', 'encrypt text'] },
 { id: 67, name: 'Hash Comparison', category: 'security', icon: '🔍', premium: false, rating: 4.5, usageCount: 52300,
 description: 'Compare two hashes or verify a file checksum against a known value.',
 features: ['Constant-time comparison', 'File checksum verify', 'SHA-256 / SHA-512', 'Clear match indicator'],
 keywords: ['checksum', 'verify', 'integrity', 'compare hash'] },
 { id: 68, name: 'Random Key Generator', category: 'security', icon: '🗝️', premium: false, rating: 4.6, usageCount: 68900,
 description: 'Generate API keys, secrets and tokens at any length or encoding.',
 features: ['Hex / Base64 / Base64URL', 'Length 16-512 bits', 'Prefix support', 'Crypto-grade randomness'],
 keywords: ['api key', 'secret', 'token', 'nonce', 'salt'] },
 { id: 69, name: 'Privacy Checker', category: 'security', icon: '👁️', premium: false, rating: 4.4, usageCount: 41700,
 description: 'See what your browser reveals about you, and what to do about it.',
 features: ['Fingerprint surface report', 'Cookie & storage audit', 'Do Not Track status', 'Hardening tips'],
 keywords: ['fingerprint', 'tracking', 'browser privacy', 'cookies'] },

 /* ---------- 🎨 DESIGN TOOLS (70-77) ---------- */
 { id: 70, name: 'Color Picker', category: 'design', icon: '🎨', premium: false, rating: 4.8, usageCount: 189400,
 description: 'Pick a color and get HEX, RGB, HSL and a full tint/shade ramp.',
 features: ['HEX / RGB / HSL / HSV', 'Tint & shade ramp', 'Contrast checker', 'Copy any format'],
 keywords: ['hex', 'rgb', 'hsl', 'colour', 'swatch'] },
 { id: 71, name: 'Color Palette Generator', category: 'design', icon: '🖌️', premium: true, rating: 4.8, usageCount: 156700,
 description: 'Build harmonious palettes from a base color using color theory.',
 features: ['Complementary / triadic / analogous', 'Lock individual swatches', 'Export CSS variables', 'Accessibility check'],
 keywords: ['palette', 'scheme', 'harmony', 'brand colors'] },
 { id: 72, name: 'Contrast Checker', category: 'design', icon: '◐', premium: false, rating: 4.7, usageCount: 97300,
 description: 'Verify text/background contrast ratios against WCAG AA and AAA.',
 features: ['WCAG AA & AAA verdicts', 'Large-text thresholds', 'Live preview', 'Suggested fixes'],
 keywords: ['wcag', 'accessibility', 'a11y', 'ratio', 'legibility'] },
 { id: 73, name: 'Box Shadow Generator', category: 'design', icon: '🌑', premium: false, rating: 4.6, usageCount: 84200,
 description: 'Compose CSS box-shadows visually, including layered and inset shadows.',
 features: ['Multiple stacked shadows', 'Inset toggle', 'Live preview surface', 'Copy CSS'],
 keywords: ['css shadow', 'drop shadow', 'elevation', 'inset'] },
 { id: 74, name: 'Border Radius Generator', category: 'design', icon: '⬜', premium: false, rating: 4.5, usageCount: 61800,
 description: 'Dial in per-corner border radii, including elliptical blob shapes.',
 features: ['Independent corner control', 'Elliptical radii', 'Live preview', 'Copy shorthand CSS'],
 keywords: ['rounded corners', 'css radius', 'blob', 'squircle'] },
 { id: 75, name: 'Font Pairing Tool', category: 'design', icon: '🔤', premium: true, rating: 4.7, usageCount: 73600,
 description: 'Browse curated heading/body font pairings with live specimen text.',
 features: ['40 curated pairings', 'Live specimen preview', 'Google Fonts embed code', 'Size & weight controls'],
 keywords: ['typography', 'google fonts', 'typeface', 'heading font'] },
 { id: 76, name: 'CSS Grid Generator', category: 'design', icon: '⚏', premium: true, rating: 4.7, usageCount: 88900,
 description: 'Lay out a CSS grid visually and copy the generated rules.',
 features: ['Drag to define areas', 'Row/column sizing', 'Gap control', 'Copy grid-template CSS'],
 keywords: ['grid layout', 'css grid', 'template areas', 'flexbox'] },
 { id: 77, name: 'Glassmorphism Generator', category: 'design', icon: '🪟', premium: false, rating: 4.6, usageCount: 69400,
 description: 'Generate frosted-glass CSS with blur, transparency and border tuning.',
 features: ['Blur & saturation control', 'Transparency slider', 'Border & shadow presets', 'Copy CSS'],
 keywords: ['frosted glass', 'backdrop filter', 'blur', 'glass effect'] },

 /* ---------- 📚 CONTENT TOOLS (78-83) ---------- */
 { id: 78, name: 'Readability Checker', category: 'content', icon: '📖', premium: true, rating: 4.7, usageCount: 78500,
 description: 'Score your writing with Flesch-Kincaid and spot hard-to-read sentences.',
 features: ['Flesch reading ease', 'Grade level estimate', 'Long-sentence highlighting', 'Passive voice flags'],
 keywords: ['flesch', 'grade level', 'readability', 'plain english'] },
 { id: 79, name: 'Meta Tag Generator', category: 'content', icon: '🏷️', premium: false, rating: 4.6, usageCount: 92100,
 description: 'Produce complete SEO, Open Graph and Twitter Card meta tags.',
 features: ['SEO + OG + Twitter tags', 'Live SERP preview', 'Character-limit warnings', 'Copy full <head> block'],
 keywords: ['seo', 'open graph', 'twitter card', 'head tags'] },
 { id: 80, name: 'Keyword Density Checker', category: 'content', icon: '📊', premium: false, rating: 4.5, usageCount: 61300,
 description: 'Find your most-used words and phrases and their density percentages.',
 features: ['1/2/3-word phrases', 'Stop-word filtering', 'Density percentages', 'Over-optimization warning'],
 keywords: ['seo', 'keywords', 'frequency', 'phrase count'] },
 { id: 81, name: 'Citation Generator', category: 'content', icon: '📚', premium: true, rating: 4.6, usageCount: 84700,
 description: 'Format references in APA, MLA, Chicago and Harvard styles.',
 features: ['4 citation styles', 'Book / article / website types', 'Bibliography builder', 'Copy formatted entry'],
 keywords: ['apa', 'mla', 'chicago', 'harvard', 'bibliography', 'reference'] },
 { id: 82, name: 'Blog Title Generator', category: 'content', icon: '✏️', premium: false, rating: 4.4, usageCount: 57900,
 description: 'Spin a topic into dozens of headline variations across proven formats.',
 features: ['10 headline formulas', 'Power-word suggestions', 'Length scoring', 'Copy any variant'],
 keywords: ['headline', 'title ideas', 'copywriting', 'blog post'] },
 { id: 83, name: 'Text Summarizer', category: 'content', icon: '📄', premium: true, rating: 4.5, usageCount: 96800,
 description: 'Condense long text to its key sentences using extractive scoring.',
 features: ['Adjustable summary length', 'Key sentence ranking', 'Keyword extraction', 'Runs entirely offline'],
 keywords: ['summary', 'tldr', 'condense', 'abstract', 'shorten'] },

 /* ---------- 🎯 PRODUCTIVITY TOOLS (84-89) ---------- */
 { id: 84, name: 'Pomodoro Timer', category: 'productivity', icon: '🍅', premium: false, rating: 4.8, usageCount: 168200,
 description: 'Run focused 25-minute work blocks with automatic break cycles.',
 features: ['Custom work/break lengths', 'Audio & title-bar alerts', 'Session counter', 'Runs in a background tab'],
 keywords: ['focus', 'timer', 'productivity', 'study', 'tomato'] },
 { id: 85, name: 'Todo List', category: 'productivity', icon: '✅', premium: false, rating: 4.7, usageCount: 142900,
 description: 'A fast checklist that saves to your browser and needs no account.',
 features: ['Drag to reorder', 'Priority levels', 'Saved locally', 'Export as text'],
 keywords: ['tasks', 'checklist', 'reminder', 'todos'] },
 { id: 86, name: 'Notepad', category: 'productivity', icon: '📓', premium: false, rating: 4.6, usageCount: 121400,
 description: 'A distraction-free scratchpad that autosaves as you type.',
 features: ['Autosave to local storage', 'Word count', 'Multiple notes', 'Download as .txt'],
 keywords: ['notes', 'scratchpad', 'write', 'memo'] },
 { id: 87, name: 'Countdown Timer', category: 'productivity', icon: '⏱️', premium: false, rating: 4.6, usageCount: 98300,
 description: 'Count down to a date or duration with a full-screen display.',
 features: ['Date or duration mode', 'Full-screen display', 'Audio alert', 'Shareable countdown link'],
 keywords: ['stopwatch', 'countdown', 'event', 'deadline'] },
 { id: 88, name: 'Habit Tracker', category: 'productivity', icon: '📈', premium: true, rating: 4.7, usageCount: 87600,
 description: 'Track daily habits on a streak grid stored only on your device.',
 features: ['Streak calendar grid', 'Multiple habits', 'Completion percentage', 'Data stays local'],
 keywords: ['streak', 'daily', 'routine', 'consistency'] },
 { id: 89, name: 'Meeting Cost Calculator', category: 'productivity', icon: '💼', premium: false, rating: 4.5, usageCount: 54200,
 description: 'Watch what a meeting costs in real time based on attendee salaries.',
 features: ['Live ticking cost', 'Per-attendee rates', 'Annualized projection', 'Shareable summary'],
 keywords: ['meeting', 'salary', 'cost', 'burn rate', 'roi'] },

 /* ---------- 🎉 FUN TOOLS (90-95) ---------- */
 { id: 90, name: 'Random Picker', category: 'fun', icon: '🎯', premium: false, rating: 4.6, usageCount: 112700,
 description: 'Drop in a list and let it pick a winner, with an animated reveal.',
 features: ['Paste any list', 'Remove-after-pick mode', 'Animated draw', 'Pick multiple winners'],
 keywords: ['raffle', 'giveaway', 'choose', 'random name'] },
 { id: 91, name: 'Dice Roller', category: 'fun', icon: '🎲', premium: false, rating: 4.5, usageCount: 87400,
 description: 'Roll any dice notation, d4 through d100, with modifiers.',
 features: ['Full dice notation (3d6+2)', 'Roll history', 'Advantage/disadvantage', 'Animated roll'],
 keywords: ['d20', 'rpg', 'tabletop', 'dnd', 'roll'] },
 { id: 92, name: 'Coin Flip', category: 'fun', icon: '🪙', premium: false, rating: 4.4, usageCount: 76200,
 description: 'Flip a coin with a 3D animation, or flip a hundred at once.',
 features: ['3D flip animation', 'Bulk flip mode', 'Running heads/tails tally', 'Fair randomness'],
 keywords: ['heads', 'tails', 'decide', 'toss'] },
 { id: 93, name: 'Spin the Wheel', category: 'fun', icon: '🎡', premium: true, rating: 4.7, usageCount: 134800,
 description: 'Build a custom spinning wheel for decisions, giveaways or classrooms.',
 features: ['Unlimited custom segments', 'Weighted odds', 'Sound effects', 'Shareable wheel link'],
 keywords: ['wheel of names', 'spinner', 'raffle', 'decision'] },
 { id: 94, name: 'Password Game', category: 'fun', icon: '🎮', premium: false, rating: 4.3, usageCount: 62900,
 description: 'A playful challenge that teaches what actually makes a password strong.',
 features: ['Escalating rules', 'Score tracking', 'Educational hints', 'No data collected'],
 keywords: ['game', 'challenge', 'puzzle', 'security game'] },
 { id: 95, name: 'Emoji Picker', category: 'fun', icon: '😀', premium: false, rating: 4.5, usageCount: 103500,
 description: 'Search thousands of emoji by name and copy them with one click.',
 features: ['Search by name or keyword', 'Category browsing', 'Recently used', 'Copy on click'],
 keywords: ['emoji', 'smiley', 'unicode', 'symbols', 'copy emoji'] }
];

/**
 * Every tool now has a real, shipped page. LIVE_TOOL_IDS is kept as a
 * mechanism rather than deleted: if a future tool is added to RAW_TOOLS
 * before its page exists, remove its id here and the card will show a
 * "Soon" badge instead of linking to a 404.
 * @type {Set<number>}
 */
const LIVE_TOOL_IDS = new Set(RAW_TOOLS.map((t) => t.id));

/**
 * Convert a display name into a URL slug.
 * @param {string} name
 * @returns {string}
 */
function slugify(name) {
 return name
 .toLowerCase()
 .normalize('NFD')
 .replace(/[\u0300-\u036f]/g, '')
 .replace(/[^a-z0-9]+/g, '-')
 .replace(/^-+|-+$/g, '');
}

/**
 * Fill in derived fields so the raw data above stays terse and
 * impossible to desynchronize.
 * @param {Object} raw
 * @returns {Tool}
 */
function normalize(raw) {
 const slug = slugify(raw.name);
 const words = (raw.name + ' ' + raw.description).toLowerCase().match(/[a-z0-9]+/g) || [];

 return {
 id: raw.id,
 name: raw.name,
 slug,
 category: raw.category,
 icon: raw.icon,
 description: raw.description,
 premium: Boolean(raw.premium),
 features: raw.features,
 usageCount: raw.usageCount,
 rating: raw.rating,
 live: LIVE_TOOL_IDS.has(raw.id),
 url: `tools/${slug}.html`,
 tags: Array.from(new Set([...words, ...(raw.keywords || []), raw.category]))
 };
}

/** @type {Tool[]} */
const TOOLS = RAW_TOOLS.map(normalize);

window.TOOLS = TOOLS;

/* ---------- Query helpers ---------- */

/** @returns {Tool[]} Tools belonging to a category. */
window.getToolsByCategory = (categoryId) =>
 TOOLS.filter((t) => t.category === categoryId);

/** @returns {Tool|undefined} */
window.getToolById = (id) => TOOLS.find((t) => t.id === Number(id));

/** @returns {Tool|undefined} */
window.getToolBySlug = (slug) => TOOLS.find((t) => t.slug === slug);

/** @returns {Tool[]} The N most-used tools. */
window.getPopularTools = (n = 6) =>
 [...TOOLS].sort((a, b) => b.usageCount - a.usageCount).slice(0, n);

/** @returns {Tool[]} Tools in the same category, excluding the given one. */
window.getRelatedTools = (tool, n = 4) =>
 TOOLS.filter((t) => t.category === tool.category && t.id !== tool.id).slice(0, n);

/** @returns {number} Count of tools per category id. */
window.getCategoryCount = (categoryId) =>
 TOOLS.reduce((n, t) => n + (t.category === categoryId ? 1 : 0), 0);
