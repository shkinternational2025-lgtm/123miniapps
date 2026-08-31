#!/usr/bin/env python3
# ============================================
# 123MiniApps.online v2.0
# File: tools_image.py
# Purpose: The 10 Image Tools (ids 11-20).
#
# Every one of these decodes the image with the File
# API and processes it on a canvas. No image is ever
# uploaded, which is the whole point of the category.
# ============================================

from toolkit import (
 tool, ws, info, row, text_input, number_input, select, switch, slider,
 color_input, output, status_line, buttons, dropzone, canvas, HR, html_block,
)

PAGES = []

# Shared preamble: the privacy note that belongs on every image tool.
PRIVACY_NOTE = """ <p class="field__hint">
 The image is decoded and processed by your own browser. It is never uploaded, and no copy of it
 exists anywhere but this tab, you can confirm that in the DevTools Network tab while you work.
 </p>"""


# ---------------------------------------------------------------
# 11. Image Compressor
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="image-compressor", name="Image Compressor", icon="🗜️", cat="image",
 title="Image Compressor: Shrink JPG, PNG and WebP Locally",
 description="Shrink JPG, PNG and WebP files without a visible quality drop. Adjustable quality, before-and-after comparison, and nothing is ever uploaded.",
 tagline="Shrink images without a visible quality drop, processed entirely in your browser.",
 workspace=ws(
 dropzone("dropzone", "Drop an image here, or click to browse",
 "JPG, PNG, WebP or GIF, processed on your device"),
 html_block(PRIVACY_NOTE),
 row(
 slider("quality", "Quality", 10, 100, 80, 5, unit="%"),
 select("format", "Output format", [
 ("image/jpeg", "JPEG, best for photos"),
 ("image/webp", "WebP, smaller, modern"),
 ("image/png", "PNG, lossless, keeps transparency"),
 ], selected="image/jpeg"),
 slider("max-width", "Limit width to", 200, 4000, 4000, 100, unit="px"),
 ),
 status_line("status", "Choose an image to begin."),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result"><span class="result__value" id="r-before" style="font-size:var(--text-2xl)">, </span><span class="result__label">Original</span></div>
 <div class="result result--primary"><span class="result__value" id="r-after" style="font-size:var(--text-2xl)">, </span><span class="result__label">Compressed</span></div>
 <div class="result"><span class="result__value" id="r-saved" style="font-size:var(--text-2xl)">, </span><span class="result__label">Saved</span></div>
 <div class="result"><span class="result__value" id="r-dims" style="font-size:var(--text-lg)">, </span><span class="result__label">Dimensions</span></div>
 </div>"""),
 html_block(""" <div class="workspace__row">
 <div class="field">
 <span class="field__label"><span>Original</span></span>
 <div class="output output--center" style="padding:var(--space-4)">
 <img id="preview-before" alt="Original image preview" style="max-width:100%;max-height:320px;border-radius:var(--radius-sm)">
 </div>
 </div>
 <div class="field">
 <span class="field__label"><span>Compressed</span></span>
 <div class="output output--center" style="padding:var(--space-4)">
 <img id="preview-after" alt="Compressed image preview" style="max-width:100%;max-height:320px;border-radius:var(--radius-sm)">
 </div>
 </div>
 </div>"""),
 buttons(("download", "Download compressed", "primary"), ("reset", "Choose another image", "ghost"), ("share", "Share tool", "ghost")),
 label="Image compressor",
 ),
 info_block=info(
 features=[
 "JPEG, WebP and PNG output",
 "Adjustable quality with a live size readout",
 "Optional maximum width, which usually saves more than quality does",
 "Side-by-side before and after preview",
 "Nothing is uploaded",
 ],
 howto=[
 "Drop an image, or click to browse.",
 "Adjust the quality slider and watch the size change.",
 "Limit the width if the image is larger than it needs to be.",
 "Download when you are happy with the result.",
 ],
 background_title="Where the savings actually come from",
 background_paragraphs=[
 "Resizing usually beats quality reduction. File size scales with pixel count, so halving an image's width quarters its pixels and typically cuts the file to around a quarter of its original size, with no visible loss at all if the image was larger than its display size. A 4000-pixel-wide photo displayed in a 800-pixel column is carrying 25 times more data than the screen can use. Check the width limit before reaching for aggressive quality settings.",
 "JPEG quality is not a percentage of anything meaningful. It is an index into quantisation tables, and the relationship to file size is steeply non-linear: dropping from 100 to 85 often halves the file with no perceptible difference, while dropping from 50 to 35 saves comparatively little and looks noticeably worse. Somewhere between 75 and 85 is the sweet spot for most photographs.",
 "Format matters more than either. WebP is typically 25% to 35% smaller than JPEG at equivalent visual quality and is now supported by every current browser. It also supports transparency, which JPEG does not. The one case for PNG is images with sharp edges and flat colour, screenshots, logos, diagrams, where JPEG's block-based compression produces visible artefacts around text. Never re-compress a JPEG repeatedly, since each pass discards more information permanently.",
 ],
 ),
 script=r""" let sourceImage = null;
 let sourceFile = null;
 let outputBlob = null;

 async function load(file) {
 sourceFile = file;

 try {
 const dataUrl = await T.readAsDataURL(file);
 sourceImage = await T.loadImage(dataUrl);

 T.$('preview-before').src = dataUrl;
 T.$('r-before').textContent = T.bytes(file.size);

 // Default the width limit to the image's own width
 const widthInput = T.$('max-width');
 widthInput.max = String(Math.max(200, sourceImage.width));
 widthInput.value = String(Math.min(Number(widthInput.max), sourceImage.width));
 T.$('max-width-value').textContent = widthInput.value;

 markDropzone(file);
 compress();
 } catch (err) {
 T.status('status', err.message, 'error');
 }
 }

 function markDropzone(file) {
 const zone = T.$('dropzone');
 zone.classList.add('has-file');
 zone.querySelector('.dropzone__label').textContent = file.name;
 zone.querySelector('.dropzone__hint').textContent =
 `${T.bytes(file.size)} · ${sourceImage.width}×${sourceImage.height}, click to choose another`;
 }

 function compress() {
 if (!sourceImage) return;

 const quality = Number(T.$('quality').value) / 100;
 const format = T.$('format').value;
 const maxWidth = Number(T.$('max-width').value);

 T.$('quality-value').textContent = T.$('quality').value;
 T.$('max-width-value').textContent = String(maxWidth);

 // Scale down only, never upscale, which adds bytes without detail
 const scale = Math.min(1, maxWidth / sourceImage.width);
 const width = Math.round(sourceImage.width * scale);
 const height = Math.round(sourceImage.height * scale);

 const canvas = document.createElement('canvas');
 canvas.width = width;
 canvas.height = height;

 const ctx = canvas.getContext('2d');
 ctx.imageSmoothingEnabled = true;
 ctx.imageSmoothingQuality = 'high';

 // JPEG has no alpha channel, so composite onto white rather than
 // letting transparent pixels turn black
 if (format === 'image/jpeg') {
 ctx.fillStyle = '#FFFFFF';
 ctx.fillRect(0, 0, width, height);
 }

 ctx.drawImage(sourceImage, 0, 0, width, height);

 canvas.toBlob((blob) => {
 if (!blob) {
 T.status('status', 'Could not encode the image in that format.', 'error');
 return;
 }

 outputBlob = blob;
 T.$('preview-after').src = URL.createObjectURL(blob);

 T.$('r-after').textContent = T.bytes(blob.size);
 T.$('r-dims').textContent = `${width} × ${height}`;

 const saved = sourceFile.size - blob.size;
 const percentage = (saved / sourceFile.size) * 100;

 T.$('r-saved').textContent = saved > 0 ? percentage.toFixed(0) + '%' : ', ';
 T.$('r-saved').style.color = saved > 0 ? 'var(--success)' : 'var(--warning)';

 if (saved > 0) {
 T.status('status',
 `Saved ${T.bytes(saved)}, ${percentage.toFixed(1)}% smaller.` +
 (scale < 1 ? ` Resized to ${width}px wide.` : ''), 'ok');
 } else {
 T.status('status',
 'The compressed file is larger than the original. Try a lower quality, ' +
 'a smaller width, or WebP, some images are already well optimised.', 'warn');
 }

 if (window.Analytics) Analytics.trackToolUse('image-compressor');
 }, format, format === 'image/png' ? undefined : quality);
 }

 T.dropzone('dropzone', load);
 T.on(['quality', 'max-width'], debounce(compress, 150));
 T.on(['format'], compress, 'change');

 T.$('download').addEventListener('click', () => {
 if (!outputBlob) {
 toast({ type: 'warning', title: 'Choose an image first' });
 return;
 }
 const extension = { 'image/jpeg': 'jpg', 'image/webp': 'webp', 'image/png': 'png' }[T.$('format').value];
 const base = (sourceFile.name || 'image').replace(/\.[^.]+$/, '');
 downloadFile(outputBlob, `${base}-compressed.${extension}`, T.$('format').value);
 });

 T.$('reset').addEventListener('click', async () => {
 const file = await T.pickFile('image/*');
 if (file) load(file);
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Image Compressor | 123MiniApps' }));""",
))

# ---------------------------------------------------------------
# 12. Image Resizer
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="image-resizer", name="Image Resizer", icon="📐", cat="image",
 title="Image Resizer: Exact Pixels or Percentage Scaling",
 description="Resize images to exact pixel dimensions or a percentage scale, with aspect ratio locking and presets for common social and web sizes.",
 tagline="Resize to exact pixels or a percentage, with aspect ratio locked by default.",
 workspace=ws(
 dropzone("dropzone", "Drop an image here, or click to browse",
 "Resized on your device, never uploaded"),
 html_block(PRIVACY_NOTE),
 row(
 select("mode", "Resize by", [("pixels", "Exact pixels"), ("percent", "Percentage")], selected="pixels"),
 switch("lock", "Lock aspect ratio", True),
 select("fit", "When the ratio differs", [
 ("stretch", "Stretch to fit"), ("contain", "Fit inside, pad the rest"), ("cover", "Fill and crop"),
 ], selected="contain"),
 ),
 html_block(""" <div class="workspace__row" id="pixel-fields">
 <div class="field">
 <label class="field__label" for="width"><span>Width (px)</span></label>
 <input class="input" id="width" type="number" min="1" max="10000" step="1" inputmode="numeric">
 </div>
 <div class="field">
 <label class="field__label" for="height"><span>Height (px)</span></label>
 <input class="input" id="height" type="number" min="1" max="10000" step="1" inputmode="numeric">
 </div>
 </div>"""),
 html_block(""" <div class="field" id="percent-field" hidden>
 <label class="field__label" for="percent"><span>Scale</span><span class="field__hint"><strong id="percent-value">50</strong>%</span></label>
 <input class="range" id="percent" type="range" min="5" max="200" value="50" step="5">
 </div>"""),
 row(
 select("preset", "Or use a preset", [
 ("", "Custom…"),
 ("1920x1080", "1920×1080, Full HD"),
 ("1280x720", "1280×720, HD"),
 ("1200x630", "1200×630, Open Graph / link preview"),
 ("1080x1080", "1080×1080, Instagram square"),
 ("1080x1920", "1080×1920, Story / Reel"),
 ("800x600", "800×600, 4:3"),
 ("512x512", "512×512, App icon"),
 ("256x256", "256×256, Avatar"),
 ("64x64", "64×64, Small icon"),
 ], selected=""),
 color_input("pad", "Padding colour", "#FFFFFF"),
 select("format", "Output format", [
 ("image/png", "PNG"), ("image/jpeg", "JPEG"), ("image/webp", "WebP"),
 ], selected="image/png"),
 ),
 status_line("status", "Choose an image to begin."),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result"><span class="result__value" id="r-original" style="font-size:var(--text-lg)">, </span><span class="result__label">Original</span></div>
 <div class="result result--primary"><span class="result__value" id="r-new" style="font-size:var(--text-lg)">, </span><span class="result__label">New size</span></div>
 <div class="result"><span class="result__value" id="r-filesize" style="font-size:var(--text-lg)">, </span><span class="result__label">File size</span></div>
 </div>"""),
 canvas("canvas", "Resized preview"),
 buttons(("download", "Download", "primary"), ("reset", "Choose another image", "ghost"), ("share", "Share tool", "ghost")),
 label="Image resizer",
 ),
 info_block=info(
 features=[
 "Exact pixel dimensions or percentage scaling",
 "Aspect ratio locking",
 "Contain, cover and stretch fitting modes",
 "Nine presets for common web and social sizes",
 "PNG, JPEG and WebP output",
 ],
 howto=[
 "Drop an image in.",
 "Enter a width, the height follows automatically.",
 "Or pick a preset for a standard size.",
 "Download the result.",
 ],
 background_title="Upscaling, downscaling and the resampling problem",
 background_paragraphs=[
 "Downscaling discards information and generally looks fine. Upscaling invents it and generally does not, enlarging a 200-pixel image to 800 pixels cannot recover detail that was never captured, so the browser interpolates between existing pixels and the result looks soft. Machine-learning upscalers do better by hallucinating plausible detail, but that is a fundamentally different operation from what a canvas can do. If you need a larger image, start from a larger original.",
 "The three fitting modes solve different problems when the target ratio differs from the source. <em>Contain</em> fits the whole image inside the target box and pads the remainder, so nothing is lost but you get bars. <em>Cover</em> fills the box completely and crops the overflow, which is what you want for a thumbnail or hero image. <em>Stretch</em> distorts the image to fit exactly, which is almost never what anyone actually wants, it is included because occasionally you genuinely need exact dimensions and do not care.",
 "One quality note: the browser's default image smoothing is bilinear, which is fine for modest reductions but produces visible aliasing when shrinking dramatically, reducing to under a third of the original in one step tends to look rough. Doing it in two or three successive halvings gives a noticeably cleaner result. This tool sets <code>imageSmoothingQuality</code> to high, which mitigates but does not eliminate the effect.",
 ],
 ),
 script=r""" let sourceImage = null;
 let sourceFile = null;
 let outputBlob = null;

 const canvas = T.$('canvas');
 const ctx = canvas.getContext('2d');

 async function load(file) {
 sourceFile = file;

 try {
 const dataUrl = await T.readAsDataURL(file);
 sourceImage = await T.loadImage(dataUrl);

 T.$('width').value = String(sourceImage.width);
 T.$('height').value = String(sourceImage.height);
 T.$('r-original').textContent = `${sourceImage.width} × ${sourceImage.height}`;

 const zone = T.$('dropzone');
 zone.classList.add('has-file');
 zone.querySelector('.dropzone__label').textContent = file.name;
 zone.querySelector('.dropzone__hint').textContent =
 `${T.bytes(file.size)} · ${sourceImage.width}×${sourceImage.height}`;

 render();
 } catch (err) {
 T.status('status', err.message, 'error');
 }
 }

 function targetSize() {
 if (!sourceImage) return { width: 0, height: 0 };

 if (T.$('mode').value === 'percent') {
 const scale = Number(T.$('percent').value) / 100;
 return {
 width: Math.max(1, Math.round(sourceImage.width * scale)),
 height: Math.max(1, Math.round(sourceImage.height * scale))
 };
 }

 return {
 width: T.clamp(Math.round(T.num(T.$('width').value) || 1), 1, 10000),
 height: T.clamp(Math.round(T.num(T.$('height').value) || 1), 1, 10000)
 };
 }

 function render() {
 if (!sourceImage) return;

 const { width, height } = targetSize();

 canvas.width = width;
 canvas.height = height;
 canvas.style.maxWidth = '100%';
 canvas.style.maxHeight = '400px';
 canvas.style.height = 'auto';

 ctx.clearRect(0, 0, width, height);
 ctx.imageSmoothingEnabled = true;
 ctx.imageSmoothingQuality = 'high';

 const format = T.$('format').value;
 const fit = T.$('fit').value;

 // JPEG has no alpha, and contain mode needs a backdrop anyway
 if (format === 'image/jpeg' || fit === 'contain') {
 ctx.fillStyle = T.$('pad').value;
 ctx.fillRect(0, 0, width, height);
 }

 const sourceRatio = sourceImage.width / sourceImage.height;
 const targetRatio = width / height;

 if (fit === 'stretch') {
 ctx.drawImage(sourceImage, 0, 0, width, height);
 } else if (fit === 'contain') {
 const scale = sourceRatio > targetRatio ? width / sourceImage.width : height / sourceImage.height;
 const drawWidth = sourceImage.width * scale;
 const drawHeight = sourceImage.height * scale;
 ctx.drawImage(sourceImage, (width - drawWidth) / 2, (height - drawHeight) / 2, drawWidth, drawHeight);
 } else {
 // cover: scale up to fill, then centre-crop the overflow
 const scale = sourceRatio > targetRatio ? height / sourceImage.height : width / sourceImage.width;
 const drawWidth = sourceImage.width * scale;
 const drawHeight = sourceImage.height * scale;
 ctx.drawImage(sourceImage, (width - drawWidth) / 2, (height - drawHeight) / 2, drawWidth, drawHeight);
 }

 T.$('r-new').textContent = `${width} × ${height}`;
 T.$('canvas-meta').textContent = `${width} × ${height} px`;

 canvas.toBlob((blob) => {
 if (!blob) return;
 outputBlob = blob;
 T.$('r-filesize').textContent = T.bytes(blob.size);

 const ratio = (width * height) / (sourceImage.width * sourceImage.height);
 T.status('status',
 ratio > 1
 ? `Upscaled to ${(ratio * 100).toFixed(0)}% of the original pixel count, expect softness.`
 : `Resized to ${(ratio * 100).toFixed(0)}% of the original pixel count.`,
 ratio > 1 ? 'warn' : 'ok');
 }, format, 0.92);

 if (window.Analytics) Analytics.trackToolUse('image-resizer');
 }

 /** Keep the other dimension in step when the ratio is locked. */
 function syncDimension(changed) {
 if (!sourceImage || !T.$('lock').checked) { render(); return; }

 const ratio = sourceImage.width / sourceImage.height;

 if (changed === 'width') {
 const width = T.num(T.$('width').value);
 if (width > 0) T.$('height').value = String(Math.round(width / ratio));
 } else {
 const height = T.num(T.$('height').value);
 if (height > 0) T.$('width').value = String(Math.round(height * ratio));
 }

 render();
 }

 function syncMode() {
 const percent = T.$('mode').value === 'percent';
 T.$('pixel-fields').hidden = percent;
 T.$('percent-field').hidden = !percent;
 render();
 }

 T.dropzone('dropzone', load);

 T.$('width').addEventListener('input', debounce(() => syncDimension('width'), 200));
 T.$('height').addEventListener('input', debounce(() => syncDimension('height'), 200));
 T.$('percent').addEventListener('input', () => {
 T.$('percent-value').textContent = T.$('percent').value;
 render();
 });

 T.on(['mode'], syncMode, 'change');
 T.on(['fit', 'format', 'lock'], render, 'change');
 T.on(['pad'], render, 'input');

 T.$('preset').addEventListener('change', () => {
 const value = T.$('preset').value;
 if (!value) return;
 const [w, h] = value.split('x');
 T.$('mode').value = 'pixels';
 syncMode();
 T.$('width').value = w;
 T.$('height').value = h;
 render();
 });

 T.$('download').addEventListener('click', () => {
 if (!outputBlob) { toast({ type: 'warning', title: 'Choose an image first' }); return; }
 const extension = { 'image/png': 'png', 'image/jpeg': 'jpg', 'image/webp': 'webp' }[T.$('format').value];
 const { width, height } = targetSize();
 const base = (sourceFile.name || 'image').replace(/\.[^.]+$/, '');
 downloadFile(outputBlob, `${base}-${width}x${height}.${extension}`, T.$('format').value);
 });

 T.$('reset').addEventListener('click', async () => {
 const file = await T.pickFile('image/*');
 if (file) load(file);
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Image Resizer | 123MiniApps' }));

 syncMode();""",
))

# ---------------------------------------------------------------
# 13. Image to Base64
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="image-to-base64", name="Image to Base64", icon="🔗", cat="image",
 title="Image to Base64: Data URI for CSS and HTML",
 description="Convert an image into a Base64 data URI ready to paste into CSS, HTML or JSON, with a size warning and ready-made code snippets.",
 tagline="Turn an image into a data URI you can paste straight into CSS or HTML.",
 workspace=ws(
 dropzone("dropzone", "Drop an image here, or click to browse",
 "Encoded on your device, never uploaded"),
 html_block(PRIVACY_NOTE),
 select("snippet", "Output as", [
 ("uri", "Raw data URI"),
 ("css", "CSS background-image"),
 ("html", "HTML img tag"),
 ("json", "JSON value"),
 ("markdown", "Markdown image"),
 ("base64", "Base64 only, no prefix"),
 ], selected="uri"),
 status_line("status", "Choose an image to encode."),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result"><span class="result__value" id="r-original" style="font-size:var(--text-2xl)">, </span><span class="result__label">Original file</span></div>
 <div class="result result--primary"><span class="result__value" id="r-encoded" style="font-size:var(--text-2xl)">, </span><span class="result__label">Encoded size</span></div>
 <div class="result"><span class="result__value" id="r-overhead" style="font-size:var(--text-2xl)">, </span><span class="result__label">Overhead</span></div>
 <div class="result"><span class="result__value" id="r-verdict" style="font-size:var(--text-base)">, </span><span class="result__label">Worth inlining?</span></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Preview</span></span>
 <div class="output output--center" style="padding:var(--space-4)">
 <img id="preview" alt="Encoded image preview" style="max-width:100%;max-height:280px;border-radius:var(--radius-sm)">
 </div>
 </div>"""),
 output("output", "Output", "output-stats", "The data URI will appear here."),
 buttons(("copy", "Copy result", "primary"), ("download", "Download as text"), ("reset", "Choose another image", "ghost"), ("share", "Share tool", "ghost")),
 label="Image to Base64 converter",
 ),
 info_block=info(
 features=[
 "Six output formats including CSS and Markdown",
 "Size comparison showing the encoding overhead",
 "A clear verdict on whether inlining is worthwhile",
 "Live preview of the encoded result",
 "Works with any image format your browser can read",
 ],
 howto=[
 "Drop in the image you want to encode.",
 "Choose the snippet format you need.",
 "Check the verdict, small images are worth inlining, large ones are not.",
 "Copy the result into your code.",
 ],
 background_title="When inlining an image is worth it",
 background_paragraphs=[
 "Base64 encoding represents binary data using 64 printable characters, storing 6 bits per character instead of 8. That means the encoded output is always about 33% larger than the original, plus a few bytes of padding. Nothing is compressed, you are trading size for the ability to embed the image directly in text.",
 "The trade is worthwhile when the request overhead exceeds the size penalty. Each HTTP request carries latency, and on a high-latency connection a round trip can cost 100 milliseconds or more regardless of how small the file is. For an icon of a few hundred bytes, inlining removes that entirely. The usual guidance is to inline anything under roughly 2 to 4 KB.",
 "Above that, inlining actively hurts. An inlined image cannot be cached separately from the document, so it is re-downloaded on every page load rather than served from cache. It bloats your HTML or CSS, which are typically render-blocking, delaying first paint. And it cannot be lazy-loaded or served in a different format to different browsers. HTTP/2 and HTTP/3 multiplex requests over a single connection, which has substantially reduced the cost of extra requests and correspondingly reduced the case for inlining at all.",
 ],
 ),
 script=r""" let dataUri = '';
 let sourceFile = null;

 async function load(file) {
 sourceFile = file;
 T.status('status', 'Encoding…', 'muted');

 try {
 dataUri = await T.readAsDataURL(file);
 T.$('preview').src = dataUri;

 const zone = T.$('dropzone');
 zone.classList.add('has-file');
 zone.querySelector('.dropzone__label').textContent = file.name;
 zone.querySelector('.dropzone__hint').textContent = T.bytes(file.size);

 render();
 } catch (err) {
 T.status('status', err.message, 'error');
 }
 }

 function base64Only() {
 const comma = dataUri.indexOf(',');
 return comma === -1 ? dataUri : dataUri.slice(comma + 1);
 }

 function render() {
 if (!dataUri || !sourceFile) return;

 const name = (sourceFile.name || 'image').replace(/\.[^.]+$/, '');
 let output;

 switch (T.$('snippet').value) {
 case 'css':
 output = `.element {\n background-image: url("${dataUri}");\n background-size: cover;\n}`;
 break;
 case 'html':
 output = `<img src="${dataUri}" alt="${T.esc(name)}">`;
 break;
 case 'json':
 output = JSON.stringify({ [name]: dataUri }, null, 2);
 break;
 case 'markdown':
 output = `![${name}](${dataUri})`;
 break;
 case 'base64':
 output = base64Only();
 break;
 default:
 output = dataUri;
 }

 T.setOutput('output', output);
 T.$('output-stats').textContent = output.length.toLocaleString() + ' characters';

 const encodedBytes = new Blob([dataUri]).size;
 const overhead = ((encodedBytes / sourceFile.size - 1) * 100);

 T.$('r-original').textContent = T.bytes(sourceFile.size);
 T.$('r-encoded').textContent = T.bytes(encodedBytes);
 // Format the sign explicitly, a bare '+' prefix produced "+-98%"
 // whenever the encoded form came out smaller than the source.
 T.$('r-overhead').textContent =
 (overhead >= 0 ? '+' : '\u2212') + Math.abs(overhead).toFixed(0) + '%';

 // The practical guidance: inline small assets, link large ones
 let verdict, colour, note;
 if (sourceFile.size <= 2048) {
 verdict = 'Yes, good candidate';
 colour = 'var(--success)';
 note = 'Under 2 KB. Inlining avoids a request that would cost more than the size penalty.';
 } else if (sourceFile.size <= 8192) {
 verdict = 'Borderline';
 colour = 'var(--warning)';
 note = 'Between 2 and 8 KB. Worth inlining only if it is needed for first paint.';
 } else {
 verdict = 'No, link to it instead';
 colour = 'var(--danger)';
 note = `At ${T.bytes(sourceFile.size)} this is too large to inline. It would bloat your ` +
 'HTML or CSS and could not be cached separately.';
 }

 T.$('r-verdict').textContent = verdict;
 T.$('r-verdict').style.color = colour;
 T.status('status', note, sourceFile.size <= 2048 ? 'ok' : sourceFile.size <= 8192 ? 'warn' : 'error');

 if (window.Analytics) Analytics.trackToolUse('image-to-base64');
 }

 T.dropzone('dropzone', load);
 T.on(['snippet'], render, 'change');

 T.$('copy').addEventListener('click', () => {
 if (!dataUri) { toast({ type: 'warning', title: 'Choose an image first' }); return; }
 copyToClipboard(T.$('output').textContent, 'Copied to clipboard');
 });

 T.$('download').addEventListener('click', () => {
 if (!dataUri) { toast({ type: 'warning', title: 'Choose an image first' }); return; }
 downloadFile(T.$('output').textContent, 'image-base64.txt');
 });

 T.$('reset').addEventListener('click', async () => {
 const file = await T.pickFile('image/*');
 if (file) load(file);
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Image to Base64 | 123MiniApps' }));""",
))

# ---------------------------------------------------------------
# 14. Image Cropper
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="image-cropper", name="Image Cropper", icon="✂️", cat="image",
 title="Image Cropper: Precise Cropping With Ratio Presets",
 description="Crop images with numeric precision and common aspect-ratio presets, with a live preview of exactly what will be exported.",
 tagline="Crop with pixel precision and ratio presets, nothing leaves your device.",
 workspace=ws(
 dropzone("dropzone", "Drop an image here, or click to browse",
 "Cropped on your device, never uploaded"),
 html_block(PRIVACY_NOTE),
 select("ratio", "Aspect ratio", [
 ("free", "Freeform"), ("1:1", "1:1, Square"), ("4:3", "4:3, Classic"),
 ("3:2", "3:2, Photo"), ("16:9", "16:9, Widescreen"), ("9:16", "9:16, Portrait / Story"),
 ("3:1", "3:1, Banner"),
 ], selected="free"),
 html_block(""" <div class="workspace__row">
 <div class="field">
 <label class="field__label" for="crop-x"><span>Left (px)</span></label>
 <input class="input" id="crop-x" type="number" min="0" step="1" value="0" inputmode="numeric">
 </div>
 <div class="field">
 <label class="field__label" for="crop-y"><span>Top (px)</span></label>
 <input class="input" id="crop-y" type="number" min="0" step="1" value="0" inputmode="numeric">
 </div>
 <div class="field">
 <label class="field__label" for="crop-w"><span>Width (px)</span></label>
 <input class="input" id="crop-w" type="number" min="1" step="1" value="100" inputmode="numeric">
 </div>
 <div class="field">
 <label class="field__label" for="crop-h"><span>Height (px)</span></label>
 <input class="input" id="crop-h" type="number" min="1" step="1" value="100" inputmode="numeric">
 </div>
 </div>"""),
 row(
 select("format", "Output format", [("image/png", "PNG"), ("image/jpeg", "JPEG"), ("image/webp", "WebP")], selected="image/png"),
 html_block(""" <div class="field"><span class="field__label"><span>&nbsp;</span></span>
 <button class="btn btn--secondary" id="centre" type="button">Centre the crop</button>
 </div>"""),
 html_block(""" <div class="field"><span class="field__label"><span>&nbsp;</span></span>
 <button class="btn btn--secondary" id="maximise" type="button">Maximise for ratio</button>
 </div>"""),
 ),
 status_line("status", "Choose an image to begin."),
 HR,
 html_block(""" <div class="workspace__row">
 <div class="field">
 <span class="field__label"><span>Source with crop region</span></span>
 <div class="output output--center" style="padding:var(--space-4)">
 <canvas id="source-canvas" role="img" aria-label="Source image with the crop region marked" style="max-width:100%;height:auto"></canvas>
 </div>
 </div>
 <div class="field">
 <span class="field__label"><span>Result</span><span class="field__hint" id="result-meta"></span></span>
 <div class="output output--center" style="padding:var(--space-4)">
 <canvas id="canvas" role="img" aria-label="Cropped result" style="max-width:100%;height:auto"></canvas>
 </div>
 </div>
 </div>"""),
 buttons(("download", "Download crop", "primary"), ("reset", "Choose another image", "ghost"), ("share", "Share tool", "ghost")),
 label="Image cropper",
 ),
 info_block=info(
 features=[
 "Numeric crop region for exact control",
 "Seven aspect ratio presets",
 "Live overlay showing the crop region on the source",
 "Centre and maximise helpers",
 "PNG, JPEG and WebP output",
 ],
 howto=[
 "Drop in an image.",
 "Pick an aspect ratio, or leave it freeform.",
 "Set the crop position and size, or press Maximise.",
 "Download the cropped result.",
 ],
 background_title="Cropping, composition and the ratios that matter",
 background_paragraphs=[
 "Cropping is lossless in the sense that it discards pixels rather than degrading the ones it keeps, but those pixels are gone. Always crop from the original rather than from a previous crop, and keep the original file, because you cannot uncrop.",
 "The ratio presets exist because platforms enforce them. Instagram displays square and 4:5; stories and Reels are 9:16; YouTube thumbnails and most video are 16:9; link previews on Facebook, LinkedIn and Slack all crop toward 1.91:1, which is why 1200×630 is the standard Open Graph size. Uploading the wrong ratio means the platform crops it for you, usually badly and usually from the centre.",
 "One compositional rule survives most scrutiny: leave headroom but not too much. The rule of thirds, placing the subject a third of the way across the frame rather than dead centre, is a useful default rather than a law, and centred composition works well for symmetry and portraits. What consistently looks wrong is cropping through a joint in a person's body: crop mid-thigh or mid-forearm rather than exactly at the knee, ankle or wrist.",
 ],
 ),
 script=r""" let sourceImage = null;
 let sourceFile = null;
 let outputBlob = null;

 const sourceCanvas = T.$('source-canvas');
 const sourceCtx = sourceCanvas.getContext('2d');
 const canvas = T.$('canvas');
 const ctx = canvas.getContext('2d');

 async function load(file) {
 sourceFile = file;

 try {
 const dataUrl = await T.readAsDataURL(file);
 sourceImage = await T.loadImage(dataUrl);

 // Start with a centred crop covering 80% of the image
 const width = Math.round(sourceImage.width * 0.8);
 const height = Math.round(sourceImage.height * 0.8);

 T.$('crop-x').value = String(Math.round((sourceImage.width - width) / 2));
 T.$('crop-y').value = String(Math.round((sourceImage.height - height) / 2));
 T.$('crop-w').value = String(width);
 T.$('crop-h').value = String(height);

 const zone = T.$('dropzone');
 zone.classList.add('has-file');
 zone.querySelector('.dropzone__label').textContent = file.name;
 zone.querySelector('.dropzone__hint').textContent =
 `${T.bytes(file.size)} · ${sourceImage.width}×${sourceImage.height}`;

 render();
 } catch (err) {
 T.status('status', err.message, 'error');
 }
 }

 function ratioValue() {
 const raw = T.$('ratio').value;
 if (raw === 'free') return null;
 const [w, h] = raw.split(':').map(Number);
 return w / h;
 }

 /** Read the crop region, clamped to the image bounds. */
 function cropRegion() {
 if (!sourceImage) return { x: 0, y: 0, width: 1, height: 1 };

 let width = T.clamp(Math.round(T.num(T.$('crop-w').value) || 1), 1, sourceImage.width);
 let height = T.clamp(Math.round(T.num(T.$('crop-h').value) || 1), 1, sourceImage.height);

 const ratio = ratioValue();
 if (ratio) {
 // Honour the ratio by adjusting height to match width
 height = T.clamp(Math.round(width / ratio), 1, sourceImage.height);
 if (height === sourceImage.height) width = Math.round(height * ratio);
 }

 const x = T.clamp(Math.round(T.num(T.$('crop-x').value) || 0), 0, sourceImage.width - width);
 const y = T.clamp(Math.round(T.num(T.$('crop-y').value) || 0), 0, sourceImage.height - height);

 return { x, y, width, height };
 }

 function render() {
 if (!sourceImage) return;

 const region = cropRegion();

 // Write the clamped values back so the fields never show something impossible
 T.$('crop-x').value = String(region.x);
 T.$('crop-y').value = String(region.y);
 T.$('crop-w').value = String(region.width);
 T.$('crop-h').value = String(region.height);

 // Source preview with the crop region marked
 const previewMax = 420;
 const scale = Math.min(1, previewMax / sourceImage.width);
 sourceCanvas.width = Math.round(sourceImage.width * scale);
 sourceCanvas.height = Math.round(sourceImage.height * scale);

 sourceCtx.clearRect(0, 0, sourceCanvas.width, sourceCanvas.height);
 sourceCtx.drawImage(sourceImage, 0, 0, sourceCanvas.width, sourceCanvas.height);

 // Dim everything outside the crop
 sourceCtx.fillStyle = 'rgba(0, 0, 0, 0.55)';
 sourceCtx.fillRect(0, 0, sourceCanvas.width, sourceCanvas.height);

 sourceCtx.save();
 sourceCtx.beginPath();
 sourceCtx.rect(region.x * scale, region.y * scale, region.width * scale, region.height * scale);
 sourceCtx.clip();
 sourceCtx.drawImage(sourceImage, 0, 0, sourceCanvas.width, sourceCanvas.height);
 sourceCtx.restore();

 sourceCtx.strokeStyle = '#00D4FF';
 sourceCtx.lineWidth = 2;
 sourceCtx.strokeRect(region.x * scale, region.y * scale, region.width * scale, region.height * scale);

 // The actual crop, at full resolution
 canvas.width = region.width;
 canvas.height = region.height;
 ctx.clearRect(0, 0, region.width, region.height);

 if (T.$('format').value === 'image/jpeg') {
 ctx.fillStyle = '#FFFFFF';
 ctx.fillRect(0, 0, region.width, region.height);
 }

 ctx.drawImage(
 sourceImage,
 region.x, region.y, region.width, region.height,
 0, 0, region.width, region.height
 );

 canvas.style.maxHeight = '320px';

 // This tool renders its own preview markup, so it has #result-meta
 // rather than the #canvas-meta the shared canvas() helper provides.
 T.$('result-meta').textContent = `${region.width} × ${region.height}`;

 canvas.toBlob((blob) => {
 if (!blob) return;
 outputBlob = blob;

 const kept = (region.width * region.height) / (sourceImage.width * sourceImage.height);
 T.status('status',
 `Cropped to ${region.width}×${region.height}, keeping ${(kept * 100).toFixed(0)}% of the original pixels. ` +
 T.bytes(blob.size) + '.', 'ok');
 }, T.$('format').value, 0.92);

 if (window.Analytics) Analytics.trackToolUse('image-cropper');
 }

 T.dropzone('dropzone', load);
 T.on(['crop-x', 'crop-y', 'crop-w', 'crop-h'], debounce(render, 200));
 T.on(['ratio', 'format'], render, 'change');

 T.$('centre').addEventListener('click', () => {
 if (!sourceImage) return;
 const region = cropRegion();
 T.$('crop-x').value = String(Math.round((sourceImage.width - region.width) / 2));
 T.$('crop-y').value = String(Math.round((sourceImage.height - region.height) / 2));
 render();
 });

 T.$('maximise').addEventListener('click', () => {
 if (!sourceImage) return;
 const ratio = ratioValue();

 if (!ratio) {
 T.$('crop-x').value = '0';
 T.$('crop-y').value = '0';
 T.$('crop-w').value = String(sourceImage.width);
 T.$('crop-h').value = String(sourceImage.height);
 } else {
 // Largest rectangle of this ratio that fits inside the image
 const sourceRatio = sourceImage.width / sourceImage.height;
 let width, height;

 if (sourceRatio > ratio) {
 height = sourceImage.height;
 width = Math.round(height * ratio);
 } else {
 width = sourceImage.width;
 height = Math.round(width / ratio);
 }

 T.$('crop-w').value = String(width);
 T.$('crop-h').value = String(height);
 T.$('crop-x').value = String(Math.round((sourceImage.width - width) / 2));
 T.$('crop-y').value = String(Math.round((sourceImage.height - height) / 2));
 }

 render();
 });

 T.$('download').addEventListener('click', () => {
 if (!outputBlob) { toast({ type: 'warning', title: 'Choose an image first' }); return; }
 const extension = { 'image/png': 'png', 'image/jpeg': 'jpg', 'image/webp': 'webp' }[T.$('format').value];
 const base = (sourceFile.name || 'image').replace(/\.[^.]+$/, '');
 downloadFile(outputBlob, `${base}-cropped.${extension}`, T.$('format').value);
 });

 T.$('reset').addEventListener('click', async () => {
 const file = await T.pickFile('image/*');
 if (file) load(file);
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Image Cropper | 123MiniApps' }));""",
))

# ---------------------------------------------------------------
# 15. Image Format Converter
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="image-format-converter", name="Image Format Converter", icon="🔄", cat="image",
 title="Image Format Converter: PNG, JPG, WebP and BMP",
 description="Convert between PNG, JPEG, WebP and BMP in your browser, with transparency handling and a size comparison across every format.",
 tagline="Convert between image formats locally, and see which one is actually smallest.",
 workspace=ws(
 dropzone("dropzone", "Drop an image here, or click to browse",
 "Converted on your device, never uploaded"),
 html_block(PRIVACY_NOTE),
 row(
 select("format", "Convert to", [
 ("image/png", "PNG, lossless, supports transparency"),
 ("image/jpeg", "JPEG, smaller, no transparency"),
 ("image/webp", "WebP, smallest, supports transparency"),
 ("image/bmp", "BMP, uncompressed"),
 ], selected="image/webp"),
 slider("quality", "Quality", 10, 100, 90, 5, unit="%"),
 color_input("matte", "Background for transparency", "#FFFFFF"),
 ),
 status_line("status", "Choose an image to convert."),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Size in every format</span><span class="field__hint">Click a row to switch to that format</span></span>
 <div class="table-scroll"><div id="comparison"></div></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Preview</span><span class="field__hint" id="preview-meta"></span></span>
 <div class="output output--center" style="padding:var(--space-4)">
 <img id="preview" alt="Converted image preview" style="max-width:100%;max-height:320px;border-radius:var(--radius-sm)">
 </div>
 </div>"""),
 buttons(("download", "Download converted", "primary"), ("reset", "Choose another image", "ghost"), ("share", "Share tool", "ghost")),
 label="Image format converter",
 ),
 info_block=info(
 features=[
 "PNG, JPEG, WebP and BMP output",
 "Size comparison across every supported format",
 "Transparency detection with a configurable matte colour",
 "Quality control for lossy formats",
 "Nothing is uploaded",
 ],
 howto=[
 "Drop in the image you want to convert.",
 "Check the comparison table to see which format is smallest.",
 "Pick a format and adjust quality if it is lossy.",
 "Download the converted file.",
 ],
 background_title="Choosing a format",
 background_paragraphs=[
 "The old rule was PNG for graphics, JPEG for photographs. WebP has largely superseded both: it does lossy and lossless compression, supports transparency and animation, and is typically 25% to 35% smaller than JPEG at equivalent quality. Every current browser supports it. AVIF is smaller still, often another 20% below WebP, though encoding is slower and browser support, while now broad, is not universal.",
 "The important thing to understand is that converting a lossy image to a lossless one does not restore quality. Converting a JPEG to PNG produces a larger file containing exactly the same visible artefacts, because the information JPEG discarded is permanently gone. The PNG is faithfully reproducing a degraded image. Only convert to a lossless format if you started from one.",
 "Transparency is the other trap. JPEG has no alpha channel, so any transparent pixel must be composited against something, this tool uses the matte colour you choose, defaulting to white. Without that step transparent areas typically turn black, which is a common and jarring surprise. BMP is included mainly for completeness: it is essentially uncompressed, so files are enormous, and it is only worth using for legacy systems that require it.",
 ],
 ),
 script=r""" let sourceImage = null;
 let sourceFile = null;
 let outputBlob = null;
 let hasTransparency = false;

 const FORMATS = [
 ['image/png', 'PNG'], ['image/jpeg', 'JPEG'],
 ['image/webp', 'WebP'], ['image/bmp', 'BMP']
 ];

 async function load(file) {
 sourceFile = file;
 T.status('status', 'Reading image…', 'muted');

 try {
 const dataUrl = await T.readAsDataURL(file);
 sourceImage = await T.loadImage(dataUrl);
 hasTransparency = detectTransparency(sourceImage);

 const zone = T.$('dropzone');
 zone.classList.add('has-file');
 zone.querySelector('.dropzone__label').textContent = file.name;
 zone.querySelector('.dropzone__hint').textContent =
 `${T.bytes(file.size)} · ${sourceImage.width}×${sourceImage.height}` +
 (hasTransparency ? ' · has transparency' : '');

 await compare();
 convert();
 } catch (err) {
 T.status('status', err.message, 'error');
 }
 }

 /** Sample the alpha channel to see whether the image uses transparency. */
 function detectTransparency(image) {
 try {
 const canvas = document.createElement('canvas');
 // Sampling at reduced size keeps this fast on large images
 const size = 64;
 canvas.width = size;
 canvas.height = size;

 const ctx = canvas.getContext('2d');
 ctx.drawImage(image, 0, 0, size, size);

 const { data } = ctx.getImageData(0, 0, size, size);
 for (let i = 3; i < data.length; i += 4) {
 if (data[i] < 250) return true;
 }
 return false;
 } catch {
 return false;
 }
 }

 /** Render the image to a canvas in the given format. */
 function encode(format) {
 const canvas = document.createElement('canvas');
 canvas.width = sourceImage.width;
 canvas.height = sourceImage.height;

 const ctx = canvas.getContext('2d');

 // Formats without an alpha channel need a matte, or transparent
 // pixels come out black
 if (format === 'image/jpeg' || format === 'image/bmp') {
 ctx.fillStyle = T.$('matte').value;
 ctx.fillRect(0, 0, canvas.width, canvas.height);
 }

 ctx.drawImage(sourceImage, 0, 0);

 const quality = Number(T.$('quality').value) / 100;
 return new Promise((resolve) => {
 canvas.toBlob(
 (blob) => resolve(blob),
 format,
 format === 'image/png' || format === 'image/bmp' ? undefined : quality
 );
 });
 }

 async function compare() {
 const mount = T.$('comparison');
 mount.innerHTML = '';

 const results = [];
 for (const [mime, label] of FORMATS) {
 const blob = await encode(mime);
 // A browser that cannot encode a format returns a PNG instead;
 // detect that by checking the reported type
 const supported = blob && (blob.type === mime || mime === 'image/bmp');
 results.push({ mime, label, blob, supported, size: blob ? blob.size : 0 });
 }

 const smallest = results
 .filter((r) => r.supported && r.size)
 .sort((a, b) => a.size - b.size)[0];

 const table = T.table(
 ['Format', 'Size', 'Versus original', 'Transparency'],
 results.map((r) => [
 r.label + (smallest && r.mime === smallest.mime ? ', smallest' : ''),
 r.supported ? T.bytes(r.size) : 'not supported here',
 r.supported && sourceFile
 ? ((r.size / sourceFile.size - 1) * 100).toFixed(0) + '%'
 : ', ',
 ['image/png', 'image/webp'].includes(r.mime) ? 'Yes' : 'No'
 ])
 );

 [...table.querySelectorAll('tbody tr')].forEach((tr, i) => {
 const result = results[i];
 if (!result.supported) return;

 tr.style.cursor = 'pointer';
 tr.title = 'Click to convert to ' + result.label;
 tr.addEventListener('click', () => {
 T.$('format').value = result.mime;
 convert();
 });

 if (smallest && result.mime === smallest.mime) {
 tr.style.background = 'color-mix(in srgb, var(--success) 12%, transparent)';
 }
 });

 mount.append(table);
 }

 async function convert() {
 if (!sourceImage) return;

 const format = T.$('format').value;
 T.$('quality-value').textContent = T.$('quality').value;

 // Quality only applies to lossy formats
 const lossy = format === 'image/jpeg' || format === 'image/webp';
 T.$('quality').closest('.field').style.opacity = lossy ? '1' : '0.45';
 T.$('matte').closest('.field').style.opacity =
 (format === 'image/jpeg' || format === 'image/bmp') ? '1' : '0.45';

 const blob = await encode(format);
 if (!blob) {
 T.status('status', 'Your browser cannot encode that format.', 'error');
 return;
 }

 outputBlob = blob;
 T.$('preview').src = URL.createObjectURL(blob);

 const label = (FORMATS.find(([m]) => m === format) || [, format])[1];
 T.$('preview-meta').textContent = `${label} · ${T.bytes(blob.size)}`;

 const delta = ((blob.size / sourceFile.size - 1) * 100);
 const warning = hasTransparency && (format === 'image/jpeg' || format === 'image/bmp')
 ? ` Transparency has been flattened onto ${T.$('matte').value}.`
 : '';

 T.status('status',
 `Converted to ${label}, ${T.bytes(blob.size)}, ` +
 `${delta >= 0 ? '+' : ''}${delta.toFixed(0)}% versus the original.` + warning,
 delta < 0 ? 'ok' : 'warn');

 if (window.Analytics) Analytics.trackToolUse('image-format-converter');
 }

 T.dropzone('dropzone', load);
 T.on(['format'], convert, 'change');
 T.$('quality').addEventListener('input', debounce(async () => {
 await convert();
 await compare();
 }, 250));
 T.on(['matte'], convert, 'input');

 T.$('download').addEventListener('click', () => {
 if (!outputBlob) { toast({ type: 'warning', title: 'Choose an image first' }); return; }
 const extension = { 'image/png': 'png', 'image/jpeg': 'jpg', 'image/webp': 'webp', 'image/bmp': 'bmp' }[T.$('format').value];
 const base = (sourceFile.name || 'image').replace(/\.[^.]+$/, '');
 downloadFile(outputBlob, `${base}.${extension}`, T.$('format').value);
 });

 T.$('reset').addEventListener('click', async () => {
 const file = await T.pickFile('image/*');
 if (file) load(file);
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Image Format Converter | 123MiniApps' }));""",
))

# ---------------------------------------------------------------
# 16. Color Picker from Image
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="color-picker-from-image", name="Color Picker from Image", icon="🎨", cat="image",
 title="Colour Picker from Image: Sample Any Pixel",
 description="Pick any colour out of an uploaded image and copy its hex value, with automatic palette extraction from the image's dominant colours.",
 tagline="Sample any pixel from an image, and extract its dominant palette automatically.",
 workspace=ws(
 dropzone("dropzone", "Drop an image here, or click to browse",
 "Read on your device, never uploaded"),
 html_block(PRIVACY_NOTE),
 html_block(""" <div class="field">
 <span class="field__label"><span>Click anywhere on the image to sample</span><span class="field__hint" id="canvas-meta"></span></span>
 <div class="output output--center" style="padding:var(--space-4)">
 <canvas id="canvas" role="img" aria-label="Click to sample a colour" style="max-width:100%;height:auto;cursor:crosshair"></canvas>
 </div>
 </div>"""),
 status_line("status", "Choose an image to begin."),
 HR,
 html_block(""" <div class="workspace__row">
 <div class="field">
 <span class="field__label"><span>Sampled colour</span></span>
 <div id="swatch" style="height:88px;border-radius:var(--radius-md);border:1px solid var(--border-color);background:var(--bg-surface)"></div>
 </div>
 <div class="field">
 <label class="field__label" for="hex"><span>HEX</span></label>
 <input class="input font-mono" id="hex" type="text" readonly>
 <label class="field__label mt-2" for="rgb"><span>RGB</span></label>
 <input class="input font-mono" id="rgb" type="text" readonly>
 <label class="field__label mt-2" for="hsl"><span>HSL</span></label>
 <input class="input font-mono" id="hsl" type="text" readonly>
 </div>
 </div>"""),
 buttons(("copy-hex", "Copy HEX", "primary"), ("copy-rgb", "Copy RGB"), ("extract", "Extract palette"), ("reset", "Choose another image", "ghost"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Dominant colours</span><span class="field__hint">Click a swatch to copy</span></span>
 <div class="swatch-grid" id="palette"></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Recently sampled</span></span>
 <div class="swatch-grid" id="recent"></div>
 </div>"""),
 label="Colour picker from image",
 ),
 info_block=info(
 features=[
 "Click any pixel to sample its colour",
 "HEX, RGB and HSL output",
 "Automatic dominant-colour extraction",
 "History of recently sampled colours",
 "The image never leaves your device",
 ],
 howto=[
 "Drop in an image.",
 "Click anywhere on it to sample that pixel.",
 "Press Extract palette for the dominant colours.",
 "Click any swatch to copy its hex value.",
 ],
 background_title="How the palette is extracted",
 background_paragraphs=[
 "The dominant colours are found by colour quantisation. Every pixel is sorted into a bucket by rounding its red, green and blue channels to a coarser resolution, this tool uses 32 levels per channel, and the buckets with the most pixels win. It is a simple approach compared to k-means clustering or the median-cut algorithm that GIF encoders use, but it is fast, runs on any image size, and produces sensible results for the purpose.",
 "One deliberate refinement: very dark and very desaturated pixels are down-weighted. Photographs frequently have large areas of near-black shadow or near-white sky that dominate a naive pixel count while telling you nothing useful about the image's character. Filtering them out surfaces the colours a designer would actually pick out.",
 "A caveat about accuracy. What you sample is the pixel value after the browser has decoded the image and applied any colour management. If the file carries an embedded ICC profile, common in photographs from a decent camera, the value you get here may differ slightly from what a colour-managed application like Photoshop reports. For web work the browser's value is the right one, since that is what visitors will see. For print work, sample in software that respects the profile.",
 ],
 ),
 script=r""" let sourceImage = null;
 let recent = [];

 const canvas = T.$('canvas');
 const ctx = canvas.getContext('2d', { willReadFrequently: true });

 async function load(file) {
 try {
 const dataUrl = await T.readAsDataURL(file);
 sourceImage = await T.loadImage(dataUrl);

 // Cap the canvas so very large images stay responsive
 const maxWidth = 720;
 const scale = Math.min(1, maxWidth / sourceImage.width);
 canvas.width = Math.round(sourceImage.width * scale);
 canvas.height = Math.round(sourceImage.height * scale);

 ctx.drawImage(sourceImage, 0, 0, canvas.width, canvas.height);

 const zone = T.$('dropzone');
 zone.classList.add('has-file');
 zone.querySelector('.dropzone__label').textContent = file.name;
 zone.querySelector('.dropzone__hint').textContent =
 `${T.bytes(file.size)} · ${sourceImage.width}×${sourceImage.height}`;

 T.$('canvas-meta').textContent = `${sourceImage.width} × ${sourceImage.height} px`;
 T.status('status', 'Click anywhere on the image to sample a colour.', 'ok');

 extractPalette();
 } catch (err) {
 T.status('status', err.message, 'error');
 }
 }

 function sampleAt(clientX, clientY) {
 if (!sourceImage) return;

 const rect = canvas.getBoundingClientRect();
 const x = Math.floor(((clientX - rect.left) / rect.width) * canvas.width);
 const y = Math.floor(((clientY - rect.top) / rect.height) * canvas.height);

 if (x < 0 || y < 0 || x >= canvas.width || y >= canvas.height) return;

 const [r, g, b] = ctx.getImageData(x, y, 1, 1).data;
 setColour(T.rgbToHex(r, g, b));
 }

 function setColour(hex) {
 const rgb = T.hexToRgb(hex);
 if (!rgb) return;

 const hsl = T.rgbToHsl(rgb.r, rgb.g, rgb.b);

 T.$('swatch').style.background = hex;
 T.$('hex').value = hex;
 T.$('rgb').value = `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`;
 T.$('hsl').value = `hsl(${hsl.h}, ${hsl.s}%, ${hsl.l}%)`;

 recent = [hex, ...recent.filter((c) => c !== hex)].slice(0, 12);
 renderRecent();

 T.status('status', `Sampled ${hex}.`, 'ok');
 if (window.Analytics) Analytics.trackToolUse('color-picker-from-image');
 }

 /**
 * Quantise pixels into coarse buckets and rank by frequency.
 * Very dark and very desaturated pixels are down-weighted, since
 * shadows and sky otherwise dominate the count without being
 * characteristic of the image.
 */
 function extractPalette() {
 if (!sourceImage) return;

 const sampleCanvas = document.createElement('canvas');
 const size = 120;
 sampleCanvas.width = size;
 sampleCanvas.height = size;

 const sampleCtx = sampleCanvas.getContext('2d', { willReadFrequently: true });
 sampleCtx.drawImage(sourceImage, 0, 0, size, size);

 const { data } = sampleCtx.getImageData(0, 0, size, size);
 const buckets = new Map();

 for (let i = 0; i < data.length; i += 4) {
 const alpha = data[i + 3];
 if (alpha < 200) continue;

 const r = data[i], g = data[i + 1], b = data[i + 2];

 const max = Math.max(r, g, b);
 const min = Math.min(r, g, b);
 const lightness = (max + min) / 2;
 const saturation = max === min ? 0 : (max - min) / (255 - Math.abs(max + min - 255));

 // Weight down near-black, near-white and grey pixels
 let weight = 1;
 if (lightness < 25 || lightness > 240) weight = 0.15;
 if (saturation < 0.1) weight *= 0.4;

 // Round to 32 levels per channel
 const key = `${r >> 3},${g >> 3},${b >> 3}`;
 const entry = buckets.get(key) || { count: 0, r: 0, g: 0, b: 0 };
 entry.count += weight;
 entry.r += r; entry.g += g; entry.b += b;
 buckets.set(key, entry);
 }

 const top = [...buckets.entries()]
 .sort((a, b) => b[1].count - a[1].count)
 .slice(0, 8)
 .map(([, entry]) => {
 // Average the actual pixel values in the bucket rather than
 // using the rounded bucket centre
 const n = Math.max(1, Math.round(entry.count));
 void n;
 const divisor = Math.max(1, Math.round(entry.count));
 return T.rgbToHex(entry.r / divisor / 1, entry.g / divisor / 1, entry.b / divisor / 1);
 });

 renderPalette(top);
 }

 function swatchFor(hex, label) {
 const swatch = el('div', { className: 'swatch' });

 const chip = el('button', {
 className: 'swatch__chip',
 attrs: { type: 'button', 'aria-label': `Copy ${hex}` },
 style: { background: hex, width: '100%', border: 'none', cursor: 'pointer' }
 });

 chip.addEventListener('click', () => {
 setColour(hex);
 copyToClipboard(hex, hex + ' copied');
 });

 swatch.append(chip, el('span', { className: 'swatch__hex', text: label || hex }));
 return swatch;
 }

 function renderPalette(colours) {
 const mount = T.$('palette');
 mount.innerHTML = '';
 colours.forEach((hex) => mount.append(swatchFor(hex)));
 }

 function renderRecent() {
 const mount = T.$('recent');
 mount.innerHTML = '';
 recent.forEach((hex) => mount.append(swatchFor(hex)));
 }

 canvas.addEventListener('click', (e) => sampleAt(e.clientX, e.clientY));

 // Keyboard accessibility: allow sampling the centre pixel
 canvas.setAttribute('tabindex', '0');
 canvas.addEventListener('keydown', (e) => {
 if (e.key !== 'Enter' && e.key !== ' ') return;
 e.preventDefault();
 const rect = canvas.getBoundingClientRect();
 sampleAt(rect.left + rect.width / 2, rect.top + rect.height / 2);
 });

 T.dropzone('dropzone', load);

 T.$('extract').addEventListener('click', extractPalette);
 T.$('copy-hex').addEventListener('click', () => copyToClipboard(T.$('hex').value, 'HEX copied'));
 T.$('copy-rgb').addEventListener('click', () => copyToClipboard(T.$('rgb').value, 'RGB copied'));

 T.$('reset').addEventListener('click', async () => {
 const file = await T.pickFile('image/*');
 if (file) load(file);
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Colour Picker from Image | 123MiniApps' }));""",
))

# ---------------------------------------------------------------
# 17. Image Filters
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="image-filters", name="Image Filters", icon="🌈", cat="image",
 title="Image Filters: Grayscale, Sepia, Blur and More",
 description="Apply grayscale, sepia, blur, brightness, contrast, saturation and hue adjustments with a live preview. Stackable, reversible and entirely local.",
 tagline="Apply stackable image filters with a live preview, nothing is uploaded.",
 workspace=ws(
 dropzone("dropzone", "Drop an image here, or click to browse",
 "Filtered on your device, never uploaded"),
 html_block(PRIVACY_NOTE),
 html_block(""" <div class="field">
 <span class="field__label"><span>Presets</span></span>
 <div class="chip-grid" id="presets"></div>
 </div>"""),
 row(
 slider("brightness", "Brightness", 0, 200, 100, 5, unit="%"),
 slider("contrast", "Contrast", 0, 200, 100, 5, unit="%"),
 slider("saturate", "Saturation", 0, 300, 100, 10, unit="%"),
 ),
 row(
 slider("grayscale", "Grayscale", 0, 100, 0, 5, unit="%"),
 slider("sepia", "Sepia", 0, 100, 0, 5, unit="%"),
 slider("invert", "Invert", 0, 100, 0, 5, unit="%"),
 ),
 row(
 slider("blur", "Blur", 0, 20, 0, 1, unit="px"),
 slider("hue", "Hue rotate", 0, 360, 0, 5, unit="°"),
 slider("opacity", "Opacity", 10, 100, 100, 5, unit="%"),
 ),
 status_line("status", "Choose an image to begin."),
 HR,
 canvas("canvas", "Filtered preview"),
 output("css", "Equivalent CSS filter", None, "The CSS will appear here."),
 buttons(("download", "Download filtered", "primary"), ("copy-css", "Copy CSS"), ("reset-filters", "Reset filters"), ("reset", "Choose another image", "ghost"), ("share", "Share tool", "ghost")),
 label="Image filters",
 ),
 info_block=info(
 features=[
 "Nine stackable adjustments",
 "Eight one-click presets",
 "Live preview at full resolution",
 "Exports the equivalent CSS filter string",
 "Fully reversible, the original is never modified",
 ],
 howto=[
 "Drop in an image.",
 "Try a preset, or adjust the sliders individually.",
 "Copy the CSS if you want the effect in a stylesheet instead.",
 "Download the filtered image when you are happy.",
 ],
 background_title="Canvas filters and the CSS equivalent",
 background_paragraphs=[
 "These adjustments use the canvas <code>filter</code> property, which accepts the same syntax as the CSS <code>filter</code> property. That is genuinely useful: the string this tool generates can be pasted straight into a stylesheet to apply the identical effect to a live element, without producing a modified image file at all. For a hover effect or a theme variation, that is almost always the better approach, no extra download, and it can be animated.",
 "Filters apply in the order written, and the order changes the result. Blurring then increasing contrast produces a different image from increasing contrast then blurring, because each operation acts on the output of the previous one. This tool applies them in a fixed, sensible order; if you need a different order, edit the generated CSS string by hand.",
 "One performance note if you use the CSS version: blur is expensive. It forces the browser to sample a wide neighbourhood of pixels for every output pixel, and animating a blur radius will drop frames on modest hardware. Animating <code>opacity</code> on a pre-blurred layer is far cheaper. Grayscale, sepia and hue-rotate are simple per-pixel matrix operations and are essentially free by comparison.",
 ],
 ),
 script=r""" let sourceImage = null;
 let sourceFile = null;
 let outputBlob = null;

 const canvas = T.$('canvas');
 const ctx = canvas.getContext('2d');

 const CONTROLS = ['brightness', 'contrast', 'saturate', 'grayscale',
 'sepia', 'invert', 'blur', 'hue', 'opacity'];

 const DEFAULTS = {
 brightness: 100, contrast: 100, saturate: 100, grayscale: 0,
 sepia: 0, invert: 0, blur: 0, hue: 0, opacity: 100
 };

 const PRESETS = {
 'Original': { ...DEFAULTS },
 'Black & white': { ...DEFAULTS, grayscale: 100, contrast: 110 },
 'Vintage': { ...DEFAULTS, sepia: 60, contrast: 110, brightness: 105, saturate: 85 },
 'Vivid': { ...DEFAULTS, saturate: 160, contrast: 115 },
 'Faded': { ...DEFAULTS, saturate: 65, brightness: 110, contrast: 88 },
 'Cool': { ...DEFAULTS, hue: 200, saturate: 120 },
 'Warm': { ...DEFAULTS, hue: 20, saturate: 125, brightness: 105 },
 'Dramatic': { ...DEFAULTS, contrast: 155, saturate: 120, brightness: 95 },
 'Soft focus': { ...DEFAULTS, blur: 2, brightness: 108, saturate: 92 }
 };

 async function load(file) {
 sourceFile = file;

 try {
 const dataUrl = await T.readAsDataURL(file);
 sourceImage = await T.loadImage(dataUrl);

 const zone = T.$('dropzone');
 zone.classList.add('has-file');
 zone.querySelector('.dropzone__label').textContent = file.name;
 zone.querySelector('.dropzone__hint').textContent =
 `${T.bytes(file.size)} · ${sourceImage.width}×${sourceImage.height}`;

 render();
 } catch (err) {
 T.status('status', err.message, 'error');
 }
 }

 function filterString() {
 const value = (id) => Number(T.$(id).value);

 const parts = [];
 if (value('brightness') !== 100) parts.push(`brightness(${value('brightness')}%)`);
 if (value('contrast') !== 100) parts.push(`contrast(${value('contrast')}%)`);
 if (value('saturate') !== 100) parts.push(`saturate(${value('saturate')}%)`);
 if (value('grayscale') > 0) parts.push(`grayscale(${value('grayscale')}%)`);
 if (value('sepia') > 0) parts.push(`sepia(${value('sepia')}%)`);
 if (value('invert') > 0) parts.push(`invert(${value('invert')}%)`);
 if (value('hue') > 0) parts.push(`hue-rotate(${value('hue')}deg)`);
 if (value('blur') > 0) parts.push(`blur(${value('blur')}px)`);
 if (value('opacity') !== 100) parts.push(`opacity(${value('opacity')}%)`);

 return parts.length ? parts.join(' ') : 'none';
 }

 function render() {
 CONTROLS.forEach((id) => {
 const label = T.$(id + '-value');
 if (label) label.textContent = T.$(id).value;
 });

 const filter = filterString();
 T.setOutput('css', `filter: ${filter};`);

 if (!sourceImage) {
 T.status('status', 'Choose an image to begin.', 'muted');
 return;
 }

 canvas.width = sourceImage.width;
 canvas.height = sourceImage.height;
 canvas.style.maxWidth = '100%';
 canvas.style.maxHeight = '420px';
 canvas.style.height = 'auto';

 ctx.clearRect(0, 0, canvas.width, canvas.height);
 ctx.filter = filter;
 ctx.drawImage(sourceImage, 0, 0);
 ctx.filter = 'none';

 T.$('canvas-meta').textContent = `${canvas.width} × ${canvas.height} px`;

 canvas.toBlob((blob) => {
 if (!blob) return;
 outputBlob = blob;

 const active = filter === 'none' ? 0 : filter.split(' ').length;
 T.status('status',
 active
 ? `${active} filter(s) applied · ${T.bytes(blob.size)}.`
 : 'No filters applied, this is the original image.',
 'ok');
 }, 'image/png');

 if (window.Analytics) Analytics.trackToolUse('image-filters');
 }

 function applyPreset(name) {
 const preset = PRESETS[name];
 if (!preset) return;

 Object.entries(preset).forEach(([key, value]) => {
 const input = T.$(key);
 if (input) input.value = String(value);
 });

 render();
 T.status('status', `Applied the “${name}” preset.`, 'ok');
 }

 T.dropzone('dropzone', load);
 T.on(CONTROLS, debounce(render, 80));

 T.$('reset-filters').addEventListener('click', () => applyPreset('Original'));

 T.$('download').addEventListener('click', () => {
 if (!outputBlob) { toast({ type: 'warning', title: 'Choose an image first' }); return; }
 const base = (sourceFile.name || 'image').replace(/\.[^.]+$/, '');
 downloadFile(outputBlob, `${base}-filtered.png`, 'image/png');
 });

 T.$('copy-css').addEventListener('click', () =>
 copyToClipboard(`filter: ${filterString()};`, 'CSS copied'));

 T.$('reset').addEventListener('click', async () => {
 const file = await T.pickFile('image/*');
 if (file) load(file);
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Image Filters | 123MiniApps' }));

 const presetMount = T.$('presets');
 Object.keys(PRESETS).forEach((name) => {
 const chip = el('button', { className: 'chip', attrs: { type: 'button' }, text: name });
 chip.addEventListener('click', () => applyPreset(name));
 presetMount.append(chip);
 });

 render();""",
))

# ---------------------------------------------------------------
# 18. Favicon Generator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="favicon-generator", name="Favicon Generator", icon="⭐", cat="image",
 title="Favicon Generator: Complete Icon Set With HTML",
 description="Turn any square image into a complete favicon set including Apple touch icon and PWA sizes, with the HTML snippet ready to paste.",
 tagline="Generate a full favicon set from one image, with the HTML ready to paste.",
 workspace=ws(
 dropzone("dropzone", "Drop a square image here, or click to browse",
 "512×512 or larger works best, generated on your device"),
 html_block(PRIVACY_NOTE),
 row(
 color_input("background", "Background for padded icons", "#0B1120"),
 slider("padding", "Padding", 0, 30, 0, 2, unit="%"),
 select("shape", "Shape", [("square", "Square"), ("rounded", "Rounded corners"), ("circle", "Circle")], selected="square"),
 ),
 status_line("status", "Choose an image to begin."),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Generated sizes</span><span class="field__hint">Click any icon to download it</span></span>
 <div id="icons" style="display:flex;flex-wrap:wrap;gap:var(--space-5);align-items:flex-end"></div>
 </div>"""),
 output("html-out", "HTML for your <head>", None, "The HTML will appear here."),
 output("manifest-out", "Web app manifest entries", None, "The manifest JSON will appear here."),
 buttons(("download-all", "Download all as separate files", "primary"), ("copy-html", "Copy HTML"), ("copy-manifest", "Copy manifest"), ("reset", "Choose another image", "ghost"), ("share", "Share tool", "ghost")),
 label="Favicon generator",
 ),
 info_block=info(
 features=[
 "Seven sizes covering browsers, iOS and PWA",
 "Optional padding, rounded corners or circular crop",
 "Ready-to-paste HTML head snippet",
 "Web app manifest icon entries",
 "Individual or bulk download",
 ],
 howto=[
 "Drop in a square image, ideally 512 pixels or larger.",
 "Add padding if your logo needs breathing room.",
 "Click any generated icon to download it individually.",
 "Copy the HTML into your page's head.",
 ],
 background_title="What a modern favicon set actually needs",
 background_paragraphs=[
 "The sprawling favicon sets of a few years ago, thirty files covering every Windows tile size and legacy iOS version, are no longer necessary. A modern site needs surprisingly little: an SVG favicon for browsers that support it, a 32×32 PNG fallback, a 180×180 Apple touch icon for iOS home screens, and 192×192 plus 512×512 PNGs referenced from the web app manifest for Android and PWA installs.",
 "An SVG favicon is worth using where you can. It scales perfectly to any display density, is usually smaller than the PNG equivalent, and can respond to the user's colour scheme with a <code>prefers-color-scheme</code> media query inside the SVG itself, so your icon can invert automatically in dark mode. Browsers that do not support it fall back to the PNG, so there is no downside.",
 "Two practical points. Favicons render at 16 pixels in a browser tab, which is genuinely tiny, a detailed logo becomes an unreadable smudge. Most well-designed favicons are a single letter, a simple mark, or a heavily simplified version of the full logo. And maskable icons for Android need their content inside a safe zone covering the central 80%, because the launcher may crop the icon to a circle, squircle or rounded square depending on the device. The padding control here exists for exactly that.",
 ],
 ),
 script=r""" let sourceImage = null;
 const generated = new Map();

 const SIZES = [
 [16, 'favicon-16.png', 'Browser tab'],
 [32, 'favicon-32.png', 'Browser tab, retina'],
 [48, 'favicon-48.png', 'Windows site icon'],
 [180, 'apple-touch-icon.png', 'iOS home screen'],
 [192, 'icon-192.png', 'Android / PWA'],
 [512, 'icon-512.png', 'PWA splash screen'],
 [512, 'icon-maskable-512.png', 'Android maskable']
 ];

 async function load(file) {
 try {
 const dataUrl = await T.readAsDataURL(file);
 sourceImage = await T.loadImage(dataUrl);

 const zone = T.$('dropzone');
 zone.classList.add('has-file');
 zone.querySelector('.dropzone__label').textContent = file.name;

 const square = sourceImage.width === sourceImage.height;
 zone.querySelector('.dropzone__hint').textContent =
 `${sourceImage.width}×${sourceImage.height}` +
 (square ? '' : ', not square, so it will be centre-cropped');

 render();

 // Warn AFTER rendering, render() writes its own success message,
 // so warning first meant the caution was immediately overwritten.
 if (sourceImage.width < 180) {
 T.status('status',
 `That image is only ${sourceImage.width}px wide. Larger icons will be upscaled and look soft, 512px or more is best.`,
 'warn');
 }
 } catch (err) {
 T.status('status', err.message, 'error');
 }
 }

 /** Render one icon at the given size. */
 function renderIcon(size, maskable) {
 const canvas = document.createElement('canvas');
 canvas.width = size;
 canvas.height = size;
 const ctx = canvas.getContext('2d');

 const shape = T.$('shape').value;
 // Maskable icons need their content inside the central 80% safe zone
 const padding = (maskable ? 20 : Number(T.$('padding').value)) / 100 * size;

 // Background, unless a transparent square with no padding is wanted
 if (padding > 0 || shape !== 'square' || maskable) {
 ctx.fillStyle = T.$('background').value;

 if (shape === 'circle' && !maskable) {
 ctx.beginPath();
 ctx.arc(size / 2, size / 2, size / 2, 0, Math.PI * 2);
 ctx.fill();
 } else if (shape === 'rounded' && !maskable) {
 const radius = size * 0.22;
 ctx.beginPath();
 ctx.roundRect ? ctx.roundRect(0, 0, size, size, radius)
 : ctx.rect(0, 0, size, size);
 ctx.fill();
 } else {
 ctx.fillRect(0, 0, size, size);
 }
 }

 // Clip the artwork to the chosen shape
 if ((shape === 'circle' || shape === 'rounded') && !maskable) {
 ctx.save();
 ctx.beginPath();
 if (shape === 'circle') {
 ctx.arc(size / 2, size / 2, size / 2, 0, Math.PI * 2);
 } else if (ctx.roundRect) {
 ctx.roundRect(0, 0, size, size, size * 0.22);
 } else {
 ctx.rect(0, 0, size, size);
 }
 ctx.clip();
 }

 // Centre-crop the source to a square, then draw it inside the padding
 const side = Math.min(sourceImage.width, sourceImage.height);
 const sourceX = (sourceImage.width - side) / 2;
 const sourceY = (sourceImage.height - side) / 2;
 const target = size - padding * 2;

 ctx.imageSmoothingEnabled = true;
 ctx.imageSmoothingQuality = 'high';
 ctx.drawImage(sourceImage, sourceX, sourceY, side, side, padding, padding, target, target);

 if ((shape === 'circle' || shape === 'rounded') && !maskable) ctx.restore();

 return canvas;
 }

 function render() {
 if (!sourceImage) return;

 const mount = T.$('icons');
 mount.innerHTML = '';
 generated.clear();

 SIZES.forEach(([size, filename, description]) => {
 const maskable = filename.includes('maskable');
 const canvas = renderIcon(size, maskable);

 canvas.toBlob((blob) => generated.set(filename, blob), 'image/png');

 const display = Math.min(size, 96);
 const preview = el('img', {
 attrs: {
 src: canvas.toDataURL('image/png'),
 alt: `${size} by ${size} icon, ${description}`,
 width: String(display),
 height: String(display)
 },
 style: {
 width: display + 'px', height: display + 'px',
 borderRadius: 'var(--radius-xs)', border: '1px solid var(--border-color)',
 imageRendering: size <= 48 ? 'pixelated' : 'auto'
 }
 });

 const wrapper = el('button', {
 className: 'swatch',
 attrs: { type: 'button', 'aria-label': `Download ${filename}` },
 style: { width: 'auto', cursor: 'pointer', alignItems: 'center' }
 }, [
 preview,
 el('span', { className: 'swatch__hex', text: `${size}×${size}` }),
 el('span', { className: 'swatch__hex', text: description, style: { fontSize: '10px' } })
 ]);

 wrapper.addEventListener('click', () => {
 const blob = generated.get(filename);
 if (blob) downloadFile(blob, filename, 'image/png');
 });

 mount.append(wrapper);
 });

 generateCode();
 T.status('status', `Generated ${SIZES.length} icons. Click any of them to download.`, 'ok');

 if (window.Analytics) Analytics.trackToolUse('favicon-generator');
 }

 function generateCode() {
 T.setOutput('html-out',
 '<!-- Favicons -->\n' +
 '<link rel="icon" href="/favicon.ico" sizes="32x32">\n' +
 '<link rel="icon" href="/icon.svg" type="image/svg+xml">\n' +
 '<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">\n' +
 '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n' +
 '<link rel="manifest" href="/manifest.json">');

 T.setOutput('manifest-out', JSON.stringify({
 icons: [
 { src: '/icon-192.png', sizes: '192x192', type: 'image/png', purpose: 'any' },
 { src: '/icon-512.png', sizes: '512x512', type: 'image/png', purpose: 'any' },
 { src: '/icon-maskable-512.png', sizes: '512x512', type: 'image/png', purpose: 'maskable' }
 ]
 }, null, 2));
 }

 T.dropzone('dropzone', load);
 T.on(['background'], render, 'input');
 T.on(['shape'], render, 'change');
 T.$('padding').addEventListener('input', () => {
 T.$('padding-value').textContent = T.$('padding').value;
 render();
 });

 T.$('download-all').addEventListener('click', () => {
 if (!generated.size) { toast({ type: 'warning', title: 'Choose an image first' }); return; }

 // Downloading several files needs a small stagger, or browsers
 // suppress everything after the first
 let delay = 0;
 generated.forEach((blob, filename) => {
 setTimeout(() => downloadFile(blob, filename, 'image/png'), delay);
 delay += 400;
 });

 toast({
 type: 'success',
 title: `Downloading ${generated.size} files`,
 message: 'Your browser may ask permission for multiple downloads.'
 });
 });

 T.$('copy-html').addEventListener('click', () =>
 copyToClipboard(T.$('html-out').textContent, 'HTML copied'));
 T.$('copy-manifest').addEventListener('click', () =>
 copyToClipboard(T.$('manifest-out').textContent, 'Manifest copied'));

 T.$('reset').addEventListener('click', async () => {
 const file = await T.pickFile('image/*');
 if (file) load(file);
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Favicon Generator | 123MiniApps' }));

 generateCode();""",
))

# ---------------------------------------------------------------
# 19. Meme Generator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="meme-generator", name="Meme Generator", icon="😂", cat="image",
 title="Meme Generator: Classic Top and Bottom Captions",
 description="Add classic top and bottom captions to any image with the traditional outlined Impact styling, adjustable size and position.",
 tagline="Add captions to any image, classic outlined styling, all done locally.",
 workspace=ws(
 dropzone("dropzone", "Drop an image here, or click to browse",
 "Captioned on your device, never uploaded"),
 html_block(PRIVACY_NOTE),
 row(
 text_input("top", "Top caption", "TOP TEXT"),
 text_input("bottom", "Bottom caption", "BOTTOM TEXT"),
 ),
 row(
 slider("size", "Text size", 4, 20, 10, 1, unit="%"),
 slider("outline", "Outline thickness", 0, 12, 6, 1, unit=""),
 slider("margin", "Edge margin", 0, 15, 4, 1, unit="%"),
 ),
 row(
 select("font", "Font", [
 ("Impact, 'Arial Black', sans-serif", "Impact, the classic"),
 ("'Arial Black', Arial, sans-serif", "Arial Black"),
 ("Georgia, serif", "Georgia"),
 ("Inter, system-ui, sans-serif", "Inter"),
 ], selected="Impact, 'Arial Black', sans-serif"),
 color_input("fill", "Text colour", "#FFFFFF"),
 color_input("stroke", "Outline colour", "#000000"),
 ),
 switch("uppercase", "Force uppercase", True),
 status_line("status", "Choose an image to begin."),
 HR,
 canvas("canvas", "Meme preview"),
 buttons(("download", "Download meme", "primary"), ("reset", "Choose another image", "ghost"), ("share", "Share tool", "ghost")),
 label="Meme generator",
 ),
 info_block=info(
 features=[
 "Classic outlined caption styling",
 "Automatic word wrapping and shrink-to-fit",
 "Adjustable size, outline and margin",
 "Four fonts including Impact",
 "Nothing is uploaded",
 ],
 howto=[
 "Drop in your image.",
 "Type the top and bottom captions.",
 "Adjust the size until it looks right.",
 "Download the finished image.",
 ],
 background_title="Why Impact, and how the outline works",
 background_paragraphs=[
 "Impact became the meme typeface largely by accident. It shipped with Windows 95 and was one of the few genuinely heavy condensed fonts available by default, which made it the obvious choice when image macros emerged in the early 2000s on sites like 4chan and Something Awful. Its extreme weight and tight letterspacing let a caption stay legible at small sizes over a busy photograph, which is exactly the constraint.",
 "The white fill with a black outline solves the same problem. A photograph has unpredictable brightness, so plain white text vanishes over a bright sky and plain black text vanishes over shadow. Outlining guarantees contrast against whatever is behind it, this is the same reason subtitles and sports graphics use it. Technically it is a stroke drawn behind the fill, which is why the outline thickness control here affects legibility more than aesthetics.",
 "A practical note on rendering: canvas has no automatic text wrapping, so this tool measures each word and breaks lines manually, then shrinks the font if the caption still will not fit. It also draws the stroke first and the fill second, the reverse order puts the outline on top and eats into the letterforms, which is a common mistake and looks noticeably worse at small sizes.",
 ],
 ),
 script=r""" let sourceImage = null;
 let sourceFile = null;
 let outputBlob = null;

 const canvas = T.$('canvas');
 const ctx = canvas.getContext('2d');

 async function load(file) {
 sourceFile = file;

 try {
 const dataUrl = await T.readAsDataURL(file);
 sourceImage = await T.loadImage(dataUrl);

 const zone = T.$('dropzone');
 zone.classList.add('has-file');
 zone.querySelector('.dropzone__label').textContent = file.name;
 zone.querySelector('.dropzone__hint').textContent =
 `${T.bytes(file.size)} · ${sourceImage.width}×${sourceImage.height}`;

 render();
 } catch (err) {
 T.status('status', err.message, 'error');
 }
 }

 /**
 * Wrap text to the available width, shrinking the font if it still
 * will not fit in a reasonable number of lines. Canvas has no
 * automatic wrapping, so this has to be done by measurement.
 */
 function layout(text, maxWidth, startSize, maxLines = 3) {
 let fontSize = startSize;

 for (let attempt = 0; attempt < 30; attempt++) {
 ctx.font = `${fontSize}px ${T.$('font').value}`;

 const words = text.split(/\s+/).filter(Boolean);
 const lines = [];
 let current = '';

 for (const word of words) {
 const candidate = current ? current + ' ' + word : word;
 if (ctx.measureText(candidate).width <= maxWidth || !current) {
 current = candidate;
 } else {
 lines.push(current);
 current = word;
 }
 }
 if (current) lines.push(current);

 const tooWide = lines.some((line) => ctx.measureText(line).width > maxWidth);

 if (lines.length <= maxLines && !tooWide) {
 return { lines, fontSize };
 }

 fontSize *= 0.92;
 }

 ctx.font = `${fontSize}px ${T.$('font').value}`;
 return { lines: [text], fontSize };
 }

 function drawCaption(text, position) {
 if (!text.trim()) return;

 const content = T.$('uppercase').checked ? text.toUpperCase() : text;
 const margin = (Number(T.$('margin').value) / 100) * canvas.height;
 const maxWidth = canvas.width * 0.92;
 const startSize = (Number(T.$('size').value) / 100) * canvas.height;

 const { lines, fontSize } = layout(content, maxWidth, startSize);

 ctx.font = `${fontSize}px ${T.$('font').value}`;
 ctx.textAlign = 'center';
 ctx.lineJoin = 'round'; // avoids spiky artefacts on thick strokes
 ctx.miterLimit = 2;

 ctx.strokeStyle = T.$('stroke').value;
 ctx.fillStyle = T.$('fill').value;
 ctx.lineWidth = (Number(T.$('outline').value) / 100) * fontSize * 2;

 const lineHeight = fontSize * 1.1;
 const x = canvas.width / 2;

 lines.forEach((line, index) => {
 let y;
 if (position === 'top') {
 ctx.textBaseline = 'top';
 y = margin + index * lineHeight;
 } else {
 ctx.textBaseline = 'bottom';
 y = canvas.height - margin - (lines.length - 1 - index) * lineHeight;
 }

 // Stroke first, then fill, the reverse puts the outline on top
 // and visibly eats into the letterforms
 if (ctx.lineWidth > 0) ctx.strokeText(line, x, y);
 ctx.fillText(line, x, y);
 });
 }

 function render() {
 ['size', 'outline', 'margin'].forEach((id) => {
 T.$(id + '-value').textContent = T.$(id).value;
 });

 if (!sourceImage) return;

 canvas.width = sourceImage.width;
 canvas.height = sourceImage.height;
 canvas.style.maxWidth = '100%';
 canvas.style.maxHeight = '460px';
 canvas.style.height = 'auto';

 ctx.clearRect(0, 0, canvas.width, canvas.height);
 ctx.drawImage(sourceImage, 0, 0);

 drawCaption(T.$('top').value, 'top');
 drawCaption(T.$('bottom').value, 'bottom');

 T.$('canvas-meta').textContent = `${canvas.width} × ${canvas.height} px`;

 canvas.toBlob((blob) => {
 if (!blob) return;
 outputBlob = blob;
 T.status('status', `Ready, ${T.bytes(blob.size)}.`, 'ok');
 }, 'image/png');

 if (window.Analytics) Analytics.trackToolUse('meme-generator');
 }

 T.dropzone('dropzone', load);
 T.on(['top', 'bottom'], debounce(render, 200));
 T.on(['size', 'outline', 'margin'], debounce(render, 80));
 T.on(['font', 'uppercase'], render, 'change');
 T.on(['fill', 'stroke'], render, 'input');

 T.$('download').addEventListener('click', () => {
 if (!outputBlob) { toast({ type: 'warning', title: 'Choose an image first' }); return; }
 const base = (sourceFile.name || 'meme').replace(/\.[^.]+$/, '');
 downloadFile(outputBlob, `${base}-meme.png`, 'image/png');
 });

 T.$('reset').addEventListener('click', async () => {
 const file = await T.pickFile('image/*');
 if (file) load(file);
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Meme Generator | 123MiniApps' }));

 render();""",
))

# ---------------------------------------------------------------
# 20. Image Watermark
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="image-watermark", name="Image Watermark", icon="💧", cat="image",
 title="Image Watermark: Text or Logo, Tiled or Placed",
 description="Stamp a text or logo watermark across your images before sharing them. Adjustable opacity, rotation, tiling and nine placement positions.",
 tagline="Add a text or logo watermark before sharing, placed or tiled, all done locally.",
 workspace=ws(
 dropzone("dropzone", "Drop the image to watermark", "Processed on your device, never uploaded"),
 html_block(PRIVACY_NOTE),
 row(
 select("type", "Watermark type", [("text", "Text"), ("image", "Logo image")], selected="text"),
 text_input("text", "Watermark text", "© Your Name 2026", "© Your Name 2026"),
 ),
 html_block(""" <div class="field" id="logo-field" hidden>
 <div class="dropzone" id="logo-dropzone" role="button" tabindex="0"
 aria-label="Choose a logo image" style="min-height:120px">
 <span class="dropzone__icon" aria-hidden="true">🖼️</span>
 <span class="dropzone__label">Drop your logo here</span>
 <span class="dropzone__hint">A transparent PNG works best</span>
 </div>
 </div>"""),
 row(
 select("position", "Position", [
 ("tile", "Tiled across the whole image"),
 ("bottom-right", "Bottom right"), ("bottom-left", "Bottom left"),
 ("top-right", "Top right"), ("top-left", "Top left"),
 ("center", "Centre"), ("bottom-center", "Bottom centre"),
 ], selected="bottom-right"),
 slider("opacity", "Opacity", 5, 100, 40, 5, unit="%"),
 slider("scale", "Size", 2, 30, 6, 1, unit="%"),
 ),
 row(
 slider("rotation", "Rotation", -90, 90, 0, 5, unit="°"),
 slider("spacing", "Tile spacing", 100, 400, 200, 20, unit="%"),
 color_input("colour", "Text colour", "#FFFFFF"),
 ),
 switch("shadow", "Add a shadow for legibility", True),
 status_line("status", "Choose an image to begin."),
 HR,
 canvas("canvas", "Watermarked preview"),
 buttons(("download", "Download watermarked", "primary"), ("reset", "Choose another image", "ghost"), ("share", "Share tool", "ghost")),
 label="Image watermark",
 ),
 info_block=info(
 features=[
 "Text or logo image watermarks",
 "Seven placements plus full tiling",
 "Adjustable opacity, size and rotation",
 "Optional shadow for legibility over busy images",
 "Nothing is uploaded",
 ],
 howto=[
 "Drop in the image you want to watermark.",
 "Type your text, or switch to logo mode and add a PNG.",
 "Choose a position, tiled is hardest to remove.",
 "Download the watermarked image.",
 ],
 background_title="What a watermark can and cannot do",
 background_paragraphs=[
 "A watermark deters casual copying and makes attribution travel with the image when it gets reposted. That is genuinely useful, and it is the realistic goal. What it does not do is prevent theft, a corner watermark can be cropped out in seconds, and content-aware fill in Photoshop or any of the numerous automated watermark removers will clear a semi-transparent overlay with reasonable results.",
 "The trade-off is visibility against intrusiveness. A tiled watermark across the whole image is far harder to remove cleanly, because reconstructing the image underneath requires inpainting every affected region rather than cropping one corner. It is also considerably more intrusive to look at. Photographers often use a light tiled watermark on preview images and supply clean files on purchase, which gets both properties.",
 "Two things worth knowing. Watermarks are not a substitute for copyright registration, in a dispute, registration and the original raw file with its EXIF metadata carry far more weight than a visible mark. And be aware that many platforms strip EXIF data on upload, so if metadata is part of your provenance strategy, keep the originals yourself rather than relying on what the platform preserves.",
 ],
 ),
 script=r""" let sourceImage = null;
 let sourceFile = null;
 let logoImage = null;
 let outputBlob = null;

 const canvas = T.$('canvas');
 const ctx = canvas.getContext('2d');

 async function loadSource(file) {
 sourceFile = file;

 try {
 const dataUrl = await T.readAsDataURL(file);
 sourceImage = await T.loadImage(dataUrl);

 const zone = T.$('dropzone');
 zone.classList.add('has-file');
 zone.querySelector('.dropzone__label').textContent = file.name;
 zone.querySelector('.dropzone__hint').textContent =
 `${T.bytes(file.size)} · ${sourceImage.width}×${sourceImage.height}`;

 render();
 } catch (err) {
 T.status('status', err.message, 'error');
 }
 }

 async function loadLogo(file) {
 try {
 const dataUrl = await T.readAsDataURL(file);
 logoImage = await T.loadImage(dataUrl);

 const zone = T.$('logo-dropzone');
 zone.classList.add('has-file');
 zone.querySelector('.dropzone__label').textContent = file.name;
 zone.querySelector('.dropzone__hint').textContent =
 `${logoImage.width}×${logoImage.height}`;

 render();
 } catch (err) {
 T.status('status', err.message, 'error');
 }
 }

 /** Draw one watermark instance centred at the given point. */
 function drawMark(centreX, centreY) {
 const scale = Number(T.$('scale').value) / 100;
 const rotation = (Number(T.$('rotation').value) * Math.PI) / 180;

 ctx.save();
 ctx.translate(centreX, centreY);
 ctx.rotate(rotation);

 if (T.$('shadow').checked) {
 ctx.shadowColor = 'rgba(0, 0, 0, 0.55)';
 ctx.shadowBlur = Math.max(2, canvas.width * 0.004);
 ctx.shadowOffsetX = 1;
 ctx.shadowOffsetY = 1;
 }

 if (T.$('type').value === 'image' && logoImage) {
 const width = canvas.width * scale * 3;
 const height = width * (logoImage.height / logoImage.width);
 ctx.drawImage(logoImage, -width / 2, -height / 2, width, height);
 } else {
 const fontSize = canvas.width * scale;
 ctx.font = `600 ${fontSize}px Inter, system-ui, sans-serif`;
 ctx.fillStyle = T.$('colour').value;
 ctx.textAlign = 'center';
 ctx.textBaseline = 'middle';
 ctx.fillText(T.$('text').value || '© Watermark', 0, 0);
 }

 ctx.restore();
 }

 function render() {
 ['opacity', 'scale', 'rotation', 'spacing'].forEach((id) => {
 T.$(id + '-value').textContent = T.$(id).value;
 });

 if (!sourceImage) return;

 canvas.width = sourceImage.width;
 canvas.height = sourceImage.height;
 canvas.style.maxWidth = '100%';
 canvas.style.maxHeight = '460px';
 canvas.style.height = 'auto';

 ctx.clearRect(0, 0, canvas.width, canvas.height);
 ctx.drawImage(sourceImage, 0, 0);

 ctx.globalAlpha = Number(T.$('opacity').value) / 100;

 const position = T.$('position').value;
 const inset = canvas.width * 0.05;

 if (position === 'tile') {
 // Measure one instance so the tiling grid can be spaced sensibly
 const scale = Number(T.$('scale').value) / 100;
 let markWidth;

 if (T.$('type').value === 'image' && logoImage) {
 markWidth = canvas.width * scale * 3;
 } else {
 ctx.font = `600 ${canvas.width * scale}px Inter, system-ui, sans-serif`;
 markWidth = ctx.measureText(T.$('text').value || '© Watermark').width;
 }

 const step = Math.max(40, markWidth * (Number(T.$('spacing').value) / 100));

 // Overshoot the bounds so rotated marks still cover the corners
 for (let y = -step; y < canvas.height + step; y += step) {
 for (let x = -step; x < canvas.width + step; x += step) {
 drawMark(x, y);
 }
 }
 } else {
 const positions = {
 'bottom-right': [canvas.width - inset, canvas.height - inset],
 'bottom-left': [inset, canvas.height - inset],
 'top-right': [canvas.width - inset, inset],
 'top-left': [inset, inset],
 'center': [canvas.width / 2, canvas.height / 2],
 'bottom-center': [canvas.width / 2, canvas.height - inset]
 };

 let [x, y] = positions[position] || positions['bottom-right'];

 // Nudge inward so an edge-anchored mark is not clipped
 if (T.$('type').value !== 'image') {
 ctx.font = `600 ${canvas.width * (Number(T.$('scale').value) / 100)}px Inter, system-ui, sans-serif`;
 const halfWidth = ctx.measureText(T.$('text').value || '© Watermark').width / 2;
 if (position.includes('right')) x -= halfWidth;
 if (position.includes('left')) x += halfWidth;
 }

 drawMark(x, y);
 }

 ctx.globalAlpha = 1;
 T.$('canvas-meta').textContent = `${canvas.width} × ${canvas.height} px`;

 canvas.toBlob((blob) => {
 if (!blob) return;
 outputBlob = blob;
 T.status('status',
 position === 'tile'
 ? `Tiled watermark applied, harder to remove than a corner mark. ${T.bytes(blob.size)}.`
 : `Watermark applied. ${T.bytes(blob.size)}.`,
 'ok');
 }, 'image/png');

 if (window.Analytics) Analytics.trackToolUse('image-watermark');
 }

 function syncType() {
 const isImage = T.$('type').value === 'image';
 T.$('logo-field').hidden = !isImage;
 T.$('text').closest('.field').style.display = isImage ? 'none' : '';
 T.$('colour').closest('.field').style.opacity = isImage ? '0.45' : '1';
 render();
 }

 T.dropzone('dropzone', loadSource);
 T.dropzone('logo-dropzone', loadLogo);

 T.$('text').addEventListener('input', debounce(render, 200));
 T.on(['opacity', 'scale', 'rotation', 'spacing'], debounce(render, 80));
 T.on(['position', 'shadow'], render, 'change');
 T.on(['colour'], render, 'input');
 T.$('type').addEventListener('change', syncType);

 T.$('download').addEventListener('click', () => {
 if (!outputBlob) { toast({ type: 'warning', title: 'Choose an image first' }); return; }
 const base = (sourceFile.name || 'image').replace(/\.[^.]+$/, '');
 downloadFile(outputBlob, `${base}-watermarked.png`, 'image/png');
 });

 T.$('reset').addEventListener('click', async () => {
 const file = await T.pickFile('image/*');
 if (file) loadSource(file);
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Image Watermark | 123MiniApps' }));

 syncType();""",
))
