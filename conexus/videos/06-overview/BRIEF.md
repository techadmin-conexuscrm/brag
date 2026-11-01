# Conexus overview film — chapter brief (read fully before starting)

We are making ONE narrated vertical film (1080×1920, 30fps) that walks a client through every
Conexus feature, plus a clearly labelled "Coming soon" section. It is built from short chapters
(14–22 s each) that are rendered separately and stitched together by the lead with one continuous
music bed. Each agent owns specific chapters (see `chapters.json` → `owner`).

**Repo:** `/home/user/brag` (branch `video-marketing`). This folder: `conexus/videos/06-overview/`.
**Product code (read-only, for verifying claims and copying real UI details):**
frontend `/home/user/ConexusCRM-FE/src`, backend `/home/user/conexuscrm-be/src`.

## How a chapter works

```
chapters/NN-name/
  script.json   narration lines (+ sound effects)        ← you write
  index.html    scenes + window.renderChapter(t)        ← you write
  notes.md      claims you show + code evidence + cast  ← you write
  out/          build output (git-ignored)
```

Copy `chapters/01-intro/` as your starting point — it is the working reference.

- `shared/base.css` — all shared styles (backgrounds, headline, eyebrow, cards, chips, buttons,
  captions, cursor, rings, `.chtag`, `.soon`). Add chapter-only CSS in a `<style>` in index.html.
- `shared/runtime.js` — scene fades, captions, and helpers: `$`, `enter(el,t,start,dur,dy,scale)`,
  `wt(lineId, word)` (time a word is spoken), `prog`, `easeOut`, `easeInOut`, `backOut`, `money`,
  `rings`, `cursor(el,t,[[t,x,y],...],[clickTimes])`, `typed(text,t,start,dur)`, `SC` (scene times).
- `shared/gifs.js` — original animated stickers (only for the Coming-soon chapter's GIF demo).
- Scenes are `<section class="scene bg-blue|bg-light|bg-dark" id="A">`, `B`, `C`… matching
  `"scene"` in script.json. Scene cuts are placed automatically in the pauses between lines.
  Build any dynamic markup INSIDE an element in the scene (e.g. `$('Ctiles').innerHTML = …`), never by
  appending to the `<section>` itself.
- Every frame must be a pure function of `t`: no CSS transitions/animations, no `Date.now()`,
  no unseeded randomness. Anchor actions to the narration with `wt('l2','refund')`.

### Build & review loop

```bash
cd /home/user/brag/conexus/videos/06-overview
shared/build_chapter.sh chapters/NN-name stills 1.0,4.0,8.0,12.0   # fast: contact sheet at out/stills.png
shared/build_chapter.sh chapters/NN-name                           # full: out/video.mp4, out/preview.mp4, out/sheet.png
```

The first run generates the voice (Kokoro `af_heart`, ~5 s per line); later runs only regenerate
lines whose `say` changed. Look at `out/stills.png` / `out/sheet.png` with the Read tool and fix
overflow, overlaps, text wrapping onto 3 lines, low contrast, empty frames, or UI that looks fake.
Iterate until every settled frame is postable. Then do the full build and check `out/sheet.png`.

## Style rules (match `chapters/01-intro` and `../05-team-chat`)

- Layout: chapter tag at top 200 (`<div class="chtag light|dark">NN · Title</div>` on the FIRST
  scene of your chapter), eyebrow 300, headline 345 (2 lines max; 118px fits ~13 characters per
  line, `.headline.sm` = 100px fits ~16), product UI from y≈700 to y≈1500. **Keep y 1540–1720 clear —
  captions live there.** Body text ≥ 22px; key numbers/labels ≥ 30px.
- Headline: line 1 white on blue / navy on light; line 2 navy on blue / accent (`var(--accent)`) on light.
- Alternate backgrounds across scenes (blue ↔ light; `bg-dark` sparingly for a "problem" beat).
- Show the product working: cards that land on the spoken word, a cursor that clicks, counters,
  status chips changing, toasts. Make it feel like a guided, interactive demo.
- Real UI details beat invented ones: read the FE component for the feature and copy its labels,
  columns, statuses and wording.
- Money/IDs in `.mono`. Amounts must add up on screen.

## Narration rules

- 3–5 lines, 14–22 s total. Plain, confident, specific (brand voice: clear over clever, no buzzwords).
- `text` is what the captions show; `say` is what the voice reads (spell out for TTS:
  "D Ms", "try conexus dot com", "Q A"). Keep the same words in both apart from such spellings.
- Full natural sentences. **Never a one-word sentence** like "Conexus." — it sounds choppy.
- `emph`: 1–2 words per line (exact tokens from `text`, punctuation included) shown in cyan.
- `gap` after each line: 0.15 within a scene, 0.35 before a new scene, ~0.6 on the last line.

## Claims (strict)

- Only claim what `../FEATURES.md` lists as safe AND what you confirm in the code. Put each claim
  with its evidence (`file:line`) in your `notes.md`. If the code says something is behind a flag,
  an add-on (dialer), or opt-in (QA), word it honestly ("when QA is on", "with the dialer add-on"),
  or leave it out.
- Never claim: "100% of calls", "TCPA compliant", "card data never touches our servers", payroll
  export, commissions, MFA/SSO, encryption at rest, PII redaction, recording consent, predictive
  dialing, Zoom.
- **Coming-soon chapter only:** every scene shows a `.soon` "Coming soon" badge, narration says it's
  coming, and nothing is shown as already live.
- Compliance line, exact wording if used:
  `PCI DSS (self-assessed) · HIPAA-ready · GDPR-aligned · SOC 2 Type I & ISO 27001 in progress`.

## Demo data

People and companies use **anime character names only** (no artwork, logos or likenesses). Use the
cast assigned to you; never real customer data.

## Don'ts

- Don't edit `shared/`, `chapters.json`, other agents' chapters, or anything outside your chapters
  (ask the lead in your final report if shared code needs a change).
- Don't `git commit` / push, and don't run `shared/assemble.py` — the lead does that.
- Don't install anything.

## Report back (final message)

For each chapter: duration, scene list (one line each), the claims shown with evidence paths, the
cast used, anything you couldn't verify or left out, and confirmation that `out/video.mp4` exists
and you reviewed `out/sheet.png`.
