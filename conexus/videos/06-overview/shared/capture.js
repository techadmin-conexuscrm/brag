// Render a chapter's frames.  node capture.js <chapterDir> <outDir> [fps] [t1,t2,...]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [chDir, outDir, fpsArg, stills] = process.argv.slice(2);
  const fps = Number(fpsArg || 30);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto('file://' + path.resolve(chDir, 'index.html'));
  await page.evaluate(async () => {
    await Promise.all(['800 118px Poppins','700 54px Poppins','600 30px Poppins','500 30px Poppins','400 36px Poppins','600 40px "Geist Mono"','500 40px "Geist Mono"'].map(f => document.fonts.load(f)));
    await document.fonts.ready;
    await Promise.all([...document.images].map(i => i.decode().catch(() => {})));
  });
  const ok = await page.evaluate(() => [document.fonts.check('800 118px Poppins'), document.fonts.check('600 40px "Geist Mono"'), typeof window.renderAt === 'function']);
  if (!ok.every(Boolean)) { console.error('not ready (fonts/renderAt):', ok, errors); process.exit(1); }
  const total = await page.evaluate(() => TL.total);
  const times = stills ? stills.split(',').map(Number) : Array.from({ length: Math.round(fps * total) }, (_, i) => i / fps);
  for (let i = 0; i < times.length; i++) {
    await page.evaluate(t => window.renderAt(t), times[i]);
    if (errors.length) { console.error('page error at t=' + times[i] + ':', errors); process.exit(1); }
    const name = stills ? `still_${times[i].toFixed(2)}.png` : `f${String(i).padStart(4, '0')}.png`;
    await page.screenshot({ path: path.join(outDir, name) });
  }
  await browser.close();
  console.log('rendered', times.length, 'frames, total', total, 's');
})();
