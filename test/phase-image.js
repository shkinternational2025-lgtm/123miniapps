/* ============================================
   123MiniApps.online v2.0
   File: test/phase-image.js
   Purpose: Behavioural tests for the 10 image tools.

   jsdom cannot decode images, so the harness stubs
   Image and FileReader. That means these tests verify
   control flow, geometry maths and generated output —
   not pixel results, which need a real browser.
   ============================================ */

const { boot, Suite, set, click, text, val, wait } = require('./harness');

/** Feed a fake image file into a tool's dropzone. */
async function dropImage(w, zoneId = 'dropzone', name = 'photo.png', size = 120000) {
  const file = new w.File(['x'.repeat(64)], name, { type: 'image/png' });
  Object.defineProperty(file, 'size', { value: size });

  const zone = w.document.getElementById(zoneId);
  const event = new w.Event('drop', { bubbles: true, cancelable: true });
  event.dataTransfer = { files: [file] };
  zone.dispatchEvent(event);

  await wait(250);
  return file;
}

module.exports = async function run() {
  const s = new Suite('Image tools');

  /* ---------- Image Compressor ---------- */
  {
    const { window: w, errors } = await boot('tools/image-compressor.html');
    w.__testImageSize = { width: 2000, height: 1500 };

    await dropImage(w, 'dropzone', 'photo.jpg', 500000);
    await wait(300);

    s.check('compressor: dropzone marked', w.document.getElementById('dropzone').classList.contains('has-file'));
    s.includes('compressor: filename shown', w.document.getElementById('dropzone').textContent, 'photo.jpg');
    s.match('compressor: original size shown', text(w, 'r-before'), /KB|MB/);
    s.match('compressor: dimensions reported', text(w, 'r-dims'), /\d+ × \d+/);

    // The width limit should default to the image's own width
    s.eq('compressor: width limit defaults to image width', val(w, 'max-width'), '2000');

    // Halving the width should be reflected in the output dimensions
    set(w, 'max-width', '1000');
    await wait(350);
    s.includes('compressor: honours width limit', text(w, 'r-dims'), '1000 × 750');

    // Never upscale
    set(w, 'max-width', '4000');
    await wait(350);
    s.includes('compressor: does not upscale past source', text(w, 'r-dims'), '2000 × 1500');

    set(w, 'format', 'image/webp', 'change');
    await wait(350);
    s.check('compressor: still reports a size', text(w, 'r-after') !== '—');
    s.noErrors(errors);
  }

  /* ---------- Image Resizer ---------- */
  {
    const { window: w, errors } = await boot('tools/image-resizer.html');
    w.__testImageSize = { width: 1600, height: 900 };

    await dropImage(w);
    await wait(300);

    s.eq('resizer: width prefilled', val(w, 'width'), '1600');
    s.eq('resizer: height prefilled', val(w, 'height'), '900');
    s.includes('resizer: original reported', text(w, 'r-original'), '1600 × 900');

    // Aspect ratio locking
    set(w, 'lock', true, 'change');
    set(w, 'width', '800');
    await wait(350);
    s.eq('resizer: locked ratio updates height', val(w, 'height'), '450');

    set(w, 'height', '300');
    await wait(350);
    s.eq('resizer: locked ratio updates width', val(w, 'width'), '533');

    // Unlocked allows independent values
    set(w, 'lock', false, 'change');
    set(w, 'width', '1000');
    await wait(350);
    s.eq('resizer: unlocked leaves height alone', val(w, 'height'), '300');

    // Presets
    set(w, 'preset', '1200x630', 'change');
    await wait(350);
    s.eq('resizer: preset width', val(w, 'width'), '1200');
    s.eq('resizer: preset height', val(w, 'height'), '630');
    s.includes('resizer: new size reported', text(w, 'r-new'), '1200 × 630');

    // Percentage mode
    set(w, 'mode', 'percent', 'change');
    set(w, 'percent', '50');
    await wait(350);
    s.includes('resizer: 50% of 1600x900', text(w, 'r-new'), '800 × 450');

    // Upscaling warns
    set(w, 'percent', '150');
    await wait(350);
    s.match('resizer: warns about upscaling', text(w, 'status'), /upscaled/i);
    s.noErrors(errors);
  }

  /* ---------- Image to Base64 ---------- */
  {
    const { window: w, errors } = await boot('tools/image-to-base64.html');

    // A small file should be recommended for inlining
    await dropImage(w, 'dropzone', 'icon.png', 1200);
    await wait(300);

    s.match('base64: verdict recommends inlining', text(w, 'r-verdict'), /yes/i);
    // Sign depends on the data: real images encode ~33% larger, but the
    // harness's stub data URI is tiny, so accept either direction.
    s.match('base64: overhead shown', text(w, 'r-overhead'), /^[+\u2212]\d+%$/);
    s.includes('base64: data URI produced', text(w, 'output'), 'data:image/png;base64,');

    // Snippet formats
    set(w, 'snippet', 'css', 'change');
    await wait(250);
    s.includes('base64: CSS snippet', text(w, 'output'), 'background-image: url("data:');

    set(w, 'snippet', 'html', 'change');
    await wait(250);
    s.includes('base64: HTML snippet', text(w, 'output'), '<img src="data:');

    set(w, 'snippet', 'markdown', 'change');
    await wait(250);
    s.match('base64: Markdown snippet', text(w, 'output'), /^!\[icon\]\(data:/);

    set(w, 'snippet', 'base64', 'change');
    await wait(250);
    s.check('base64: raw base64 has no prefix', !text(w, 'output').startsWith('data:'));

    // A large file should be discouraged
    await dropImage(w, 'dropzone', 'huge.png', 500000);
    await wait(300);
    s.match('base64: large file discouraged', text(w, 'r-verdict'), /no/i);
    s.match('base64: explains why', text(w, 'status'), /too large to inline/i);
    s.noErrors(errors);
  }

  /* ---------- Image Cropper ---------- */
  {
    const { window: w, errors } = await boot('tools/image-cropper.html');
    w.__testImageSize = { width: 1000, height: 800 };

    await dropImage(w);
    await wait(300);

    // Default crop is 80% centred
    s.eq('cropper: default crop width', val(w, 'crop-w'), '800');
    s.eq('cropper: default crop height', val(w, 'crop-h'), '640');
    s.eq('cropper: default crop centred x', val(w, 'crop-x'), '100');

    // Ratio enforcement
    set(w, 'ratio', '1:1', 'change');
    await wait(350);
    s.eq('cropper: square ratio enforced', val(w, 'crop-w'), val(w, 'crop-h'));

    set(w, 'ratio', '16:9', 'change');
    set(w, 'crop-w', '640');
    await wait(350);
    s.eq('cropper: 16:9 height derived', val(w, 'crop-h'), '360');

    // Maximise for the ratio
    click(w, 'maximise');
    await wait(350);
    // 1000x800 at 16:9 → width limited: 1000 wide, 562 high
    s.eq('cropper: maximise fills width', val(w, 'crop-w'), '1000');
    s.eq('cropper: maximise derives height', val(w, 'crop-h'), '563');

    // Out-of-bounds values are clamped, not accepted
    set(w, 'crop-x', '99999');
    await wait(350);
    s.check('cropper: x clamped inside image', Number(val(w, 'crop-x')) <= 1000);

    set(w, 'ratio', 'free', 'change');
    click(w, 'maximise');
    await wait(350);
    s.eq('cropper: freeform maximise takes whole image', val(w, 'crop-w'), '1000');

    click(w, 'centre');
    await wait(350);
    s.eq('cropper: centring a full crop leaves x at 0', val(w, 'crop-x'), '0');
    s.noErrors(errors);
  }

  /* ---------- Image Format Converter ---------- */
  {
    const { window: w, errors } = await boot('tools/image-format-converter.html');
    w.__testImageSize = { width: 400, height: 400 };

    await dropImage(w, 'dropzone', 'logo.png', 40000);
    await wait(500);

    s.check('converter: comparison table rendered',
      w.document.querySelector('#comparison table') !== null);
    s.eq('converter: four formats compared',
      w.document.querySelectorAll('#comparison tbody tr').length, 4);
    s.includes('converter: lists PNG', w.document.getElementById('comparison').textContent, 'PNG');
    s.includes('converter: lists WebP', w.document.getElementById('comparison').textContent, 'WebP');

    // Transparency column
    s.includes('converter: transparency noted',
      w.document.getElementById('comparison').textContent, 'Yes');

    set(w, 'format', 'image/jpeg', 'change');
    await wait(400);
    s.match('converter: reports conversion', text(w, 'status'), /converted to JPEG/i);
    s.includes('converter: preview meta updated', text(w, 'preview-meta'), 'JPEG');
    s.noErrors(errors);
  }

  /* ---------- Colour Picker from Image ---------- */
  {
    const { window: w, errors } = await boot('tools/color-picker-from-image.html');
    w.__testImageSize = { width: 600, height: 400 };

    await dropImage(w);
    await wait(400);

    s.match('imagecolour: prompts to click', text(w, 'status'), /click anywhere/i);
    s.includes('imagecolour: dimensions shown', text(w, 'canvas-meta'), '600 × 400');
    s.check('imagecolour: canvas is keyboard reachable',
      w.document.getElementById('canvas').getAttribute('tabindex') === '0');

    // The stub canvas returns zeroed pixel data, so sampling yields #000000 —
    // what matters is that the flow completes and all formats populate
    const canvas = w.document.getElementById('canvas');
    canvas.getBoundingClientRect = () => ({ left: 0, top: 0, width: 600, height: 400 });
    canvas.dispatchEvent(new w.MouseEvent('click', { bubbles: true, clientX: 100, clientY: 100 }));
    await wait(250);

    s.match('imagecolour: hex populated', val(w, 'hex'), /^#[0-9A-F]{6}$/);
    s.match('imagecolour: rgb populated', val(w, 'rgb'), /^rgb\(\d+, \d+, \d+\)$/);
    s.match('imagecolour: hsl populated', val(w, 'hsl'), /^hsl\(\d+, \d+%, \d+%\)$/);
    s.check('imagecolour: recent swatch added',
      w.document.querySelectorAll('#recent .swatch').length > 0);
    s.noErrors(errors);
  }

  /* ---------- Image Filters ---------- */
  {
    const { window: w, errors } = await boot('tools/image-filters.html');

    await wait(250);
    s.eq('filters: no filters initially', text(w, 'css'), 'filter: none;');
    s.check('filters: presets rendered',
      w.document.querySelectorAll('#presets .chip').length === 9);

    set(w, 'grayscale', '100');
    await wait(250);
    s.includes('filters: grayscale in CSS', text(w, 'css'), 'grayscale(100%)');

    set(w, 'blur', '5');
    await wait(250);
    s.includes('filters: blur in CSS', text(w, 'css'), 'blur(5px)');

    set(w, 'contrast', '150');
    await wait(250);
    s.includes('filters: contrast in CSS', text(w, 'css'), 'contrast(150%)');

    // Preset application
    const presets = w.document.querySelectorAll('#presets .chip');
    const bw = [...presets].find((c) => c.textContent.includes('Black'));
    bw.click();
    await wait(250);
    s.includes('filters: preset applies grayscale', text(w, 'css'), 'grayscale(100%)');
    s.check('filters: preset clears blur', !text(w, 'css').includes('blur'));

    click(w, 'reset-filters');
    await wait(250);
    s.eq('filters: reset clears everything', text(w, 'css'), 'filter: none;');

    // With an image loaded, it should report a size
    w.__testImageSize = { width: 500, height: 500 };
    await dropImage(w);
    await wait(350);
    s.match('filters: reports state with image', text(w, 'status'), /original image|filter/i);
    s.noErrors(errors);
  }

  /* ---------- Favicon Generator ---------- */
  {
    const { window: w, errors } = await boot('tools/favicon-generator.html');
    w.__testImageSize = { width: 512, height: 512 };

    // Code is generated even before an image is chosen
    await wait(250);
    s.includes('favicon: HTML includes apple touch icon', text(w, 'html-out'), 'apple-touch-icon');
    s.includes('favicon: HTML includes manifest', text(w, 'html-out'), 'rel="manifest"');
    s.includes('favicon: HTML includes SVG icon', text(w, 'html-out'), 'image/svg+xml');

    const manifest = JSON.parse(text(w, 'manifest-out'));
    s.eq('favicon: manifest has three icons', manifest.icons.length, 3);
    s.check('favicon: manifest includes maskable',
      manifest.icons.some((i) => i.purpose === 'maskable'));

    await dropImage(w, 'dropzone', 'logo.png', 30000);
    await wait(500);

    s.eq('favicon: seven icons generated',
      w.document.querySelectorAll('#icons .swatch').length, 7);
    s.match('favicon: reports generation', text(w, 'status'), /generated 7 icons/i);

    // A small source should warn about upscaling
    w.__testImageSize = { width: 64, height: 64 };
    await dropImage(w, 'dropzone', 'small.png', 2000);
    await wait(400);
    s.match('favicon: warns about small source', text(w, 'status'), /look soft|512px or more/i);
    s.noErrors(errors);
  }

  /* ---------- Meme Generator ---------- */
  {
    const { window: w, errors, canvasOps } = await boot('tools/meme-generator.html');
    w.__testImageSize = { width: 800, height: 600 };

    await dropImage(w);
    await wait(350);

    set(w, 'top', 'ONE DOES NOT SIMPLY');
    set(w, 'bottom', 'WRITE TESTS FOR A MEME GENERATOR');
    await wait(400);

    const drawnText = canvasOps.filter((o) => o[0] === 'fillText').map((o) => o[1]);
    s.check('meme: top caption drawn', drawnText.some((t) => String(t).includes('ONE DOES NOT')));
    s.check('meme: bottom caption drawn', drawnText.some((t) => String(t).includes('WRITE TESTS')));
    s.match('meme: reports ready', text(w, 'status'), /ready/i);

    // Uppercase forcing
    set(w, 'uppercase', true, 'change');
    set(w, 'top', 'lower case input');
    await wait(400);
    const upper = canvasOps.filter((o) => o[0] === 'fillText').map((o) => String(o[1]));
    s.check('meme: forces uppercase', upper.some((t) => t.includes('LOWER CASE')));

    set(w, 'uppercase', false, 'change');
    await wait(400);
    const mixed = canvasOps.filter((o) => o[0] === 'fillText').map((o) => String(o[1]));
    s.check('meme: respects lowercase when off', mixed.some((t) => t.includes('lower case')));

    s.includes('meme: dimensions reported', text(w, 'canvas-meta'), '800 × 600');
    s.noErrors(errors);
  }

  /* ---------- Image Watermark ---------- */
  {
    const { window: w, errors, canvasOps } = await boot('tools/image-watermark.html');
    w.__testImageSize = { width: 1000, height: 1000 };

    await dropImage(w);
    await wait(350);

    set(w, 'type', 'text', 'change');
    set(w, 'text', '© Test 2026');
    set(w, 'position', 'bottom-right', 'change');
    await wait(400);

    const drawn = canvasOps.filter((o) => o[0] === 'fillText').map((o) => String(o[1]));
    s.check('watermark: text drawn', drawn.some((t) => t.includes('© Test 2026')));
    s.match('watermark: reports applied', text(w, 'status'), /watermark applied/i);

    // Tiling should draw the mark many times
    const before = canvasOps.filter((o) => o[0] === 'fillText').length;
    set(w, 'position', 'tile', 'change');
    await wait(400);
    const after = canvasOps.filter((o) => o[0] === 'fillText').length;
    s.check('watermark: tiling draws many instances', after - before > 5, `${after - before} draws`);
    s.match('watermark: notes tiling is harder to remove', text(w, 'status'), /harder to remove/i);

    // Logo mode reveals the logo dropzone
    set(w, 'type', 'image', 'change');
    await wait(300);
    s.check('watermark: logo dropzone shown',
      w.document.getElementById('logo-field').hidden === false);

    s.includes('watermark: dimensions reported', text(w, 'canvas-meta'), '1000 × 1000');
    s.noErrors(errors);
  }

  return s;
};
