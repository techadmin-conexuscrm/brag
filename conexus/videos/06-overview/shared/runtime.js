// Shared runtime for overview chapters. Load AFTER timeline.js and BEFORE the chapter script.
// The chapter defines window.renderChapter(t) and uses these helpers. Every frame must be a
// pure function of t (no Date.now, no CSS transitions/animations, no randomness without a seed).
(function () {
  const $ = id => { const el = document.getElementById(id); if (!el) throw new Error('missing #' + id); return el; };
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const easeOut = p => 1 - Math.pow(1 - p, 3);
  const easeInOut = p => p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
  const backOut = p => { const c1 = 1.5, c3 = c1 + 1; return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2); };
  const prog = (t, s, d) => clamp((t - s) / d);
  const SC = Object.fromEntries(TL.scenes.map(s => [s.id, s]));
  const LINE = Object.fromEntries(TL.lines.map(l => [l.id, l]));
  const WORDS = TL.captions.flatMap(c => c.words);
  // time (s) when `word` (prefix match, case/punctuation-insensitive) is spoken in line `line`
  const wt = (line, word) => {
    const w = WORDS.find(x => x.line === line && x.w.replace(/[^\w$']/g, '').toLowerCase().startsWith(word.toLowerCase()));
    if (!w) throw new Error('wt: no word "' + word + '" in ' + line);
    return w.s;
  };
  // fade + rise (+ optional springy scale) entrance
  function enter(el, t, start, dur = 0.45, dy = 50, scale = 0) {
    const p = easeOut(prog(t, start, dur));
    el.style.opacity = p;
    const s = scale ? (1 - scale * (1 - backOut(prog(t, start, dur)))) : 1;
    el.style.transform = `translateY(${(1 - p) * dy}px) scale(${s})`;
  }
  function money(v, d = 2) { return '$' + v.toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d }); }
  // the standard logo-reveal rings
  function rings(t, ids, start) {
    ids.forEach((r, i) => { const p = prog(t, start + 0.1 + i * 0.15, 1.2); const el = $(r); el.style.opacity = 0.9 * easeOut(p); el.style.transform = `translate(-50%,-50%) scale(${0.85 + 0.15 * easeOut(p) + 0.02 * Math.sin(t * 2 + i)})`; });
  }
  // a cursor that glides between waypoints [[t,x,y],...] and "clicks" at times in `clicks`
  function cursor(el, t, path, clicks = []) {
    if (t < path[0][0] - 0.2) { el.style.opacity = 0; return; }
    let x = path[0][1], y = path[0][2];
    for (let i = 1; i < path.length; i++) {
      const [t0, x0, y0] = path[i - 1], [t1, x1, y1] = path[i];
      if (t >= t0) { const p = easeInOut(prog(t, t0, Math.max(0.05, t1 - t0))); x = x0 + (x1 - x0) * p; y = y0 + (y1 - y0) * p; }
    }
    el.style.left = x + 'px'; el.style.top = y + 'px';
    el.style.opacity = easeOut(prog(t, path[0][0] - 0.2, 0.2));
    const pressed = clicks.some(c => t >= c && t < c + 0.15);
    el.style.transform = `scale(${pressed ? 0.85 : 1})`;
  }
  // typewriter: returns the visible prefix of `text` typed from `start` over `dur`
  function typed(text, t, start, dur) { const ch = [...text]; return ch.slice(0, Math.floor(clamp((t - start) / dur) * ch.length)).join(''); }

  // wrap each scene's children so backgrounds stay solid while content fades
  document.querySelectorAll('.scene').forEach(sec => {
    const c = document.createElement('div'); c.className = 'content'; c.style.cssText = 'position:absolute;inset:0';
    while (sec.firstChild) c.appendChild(sec.firstChild); sec.appendChild(c);
  });
  const ids = TL.scenes.map(s => s.id);
  const lastId = ids[ids.length - 1];
  function sceneOpacity(id, t) {
    const s = SC[id];
    if (t < s.s || (id !== lastId && t >= s.e + 0.3)) return 0;
    return s.s === 0 ? 1 : easeOut(prog(t, s.s, 0.3));
  }
  function contentOpacity(id, t) {
    const s = SC[id]; let o = 1;
    if (s.s === 0) o *= easeOut(prog(t, 0, 0.3));                         // chapter opens: content fades in
    if (id !== lastId || !window.CHAPTER_IS_FINAL) o *= 1 - easeInOut(prog(t, s.e - 0.25, 0.25));  // scene/chapter ends
    return o;
  }

  let capKey = '';
  function renderCaption(t) {
    const c = TL.captions.find(c => t >= c.s - 0.05 && t < c.e);
    const box = document.getElementById('cap');
    if (!c) { box.innerHTML = ''; capKey = ''; return; }
    if (capKey !== c.s) { box.innerHTML = '<div class="pill">' + c.words.map(w => `<span class="w${w.em ? ' em' : ''}">${w.w}</span>`).join('') + '</div>'; capKey = c.s; }
    const pill = box.firstChild; const pin = easeOut(prog(t, c.s - 0.05, 0.18));
    pill.style.opacity = pin; pill.style.transform = `translateY(${(1 - pin) * 16}px) scale(${0.96 + 0.04 * pin})`;
    [...pill.children].forEach((el, i) => { const w = c.words[i]; const p = easeOut(prog(t, w.s - 0.04, 0.16)); el.style.opacity = 0.18 + 0.82 * p; el.style.transform = `translateY(${(1 - p) * 8}px)`; });
  }

  window.renderAt = function (t) {
    for (const id of ids) {
      const el = $(id); const o = sceneOpacity(id, t);
      el.style.opacity = o; el.style.display = o > 0 ? 'block' : 'none';
      el.querySelector('.content').style.opacity = contentOpacity(id, t);
    }
    renderCaption(t);
    window.renderChapter(t);
  };
  Object.assign(window, { $, clamp, easeOut, easeInOut, backOut, prog, SC, LINE, WORDS, wt, enter, money, rings, cursor, typed });
})();
