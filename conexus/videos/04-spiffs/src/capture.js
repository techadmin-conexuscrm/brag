// Usage: node capture.js <outDir> [fps] [duration] [t1,t2,...]  — renders frames as PNG
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [outDir, fpsArg, durArg, stills] = process.argv.slice(2);
  const fps = Number(fpsArg || 30), dur = Number(durArg || 22);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(__dirname, 'index.html'));
  await page.evaluate(async () => { await Promise.all(['600 72px Geist','400 40px Geist','500 40px Geist','600 40px "Geist Mono"','500 40px "Geist Mono"'].map(f => document.fonts.load(f))); await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode())); });
  const ok = await page.evaluate(() => [document.fonts.check('600 72px Geist'), document.fonts.check('600 40px "Geist Mono"')]);
  if (!ok.every(Boolean)) { console.error('Fonts not loaded', ok); process.exit(1); }
  const times = stills ? stills.split(',').map(Number) : Array.from({ length: Math.round(fps * dur) }, (_, i) => i / fps);
  for (let i = 0; i < times.length; i++) {
    await page.evaluate(t => window.renderAt(t), times[i]);
    const name = stills ? `still_${times[i].toFixed(2)}.png` : `f${String(i).padStart(4, '0')}.png`;
    await page.screenshot({ path: path.join(outDir, name) });
  }
  await browser.close();
  console.log('rendered', times.length);
})();
