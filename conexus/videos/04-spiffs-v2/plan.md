# Video 4 v2 — Spiffs & leaderboard (ICP: Sales Team Leader)

Restyled to match the reference promo (`conexus-promo-vertical.mp4`): 1080×1920 (9:16), 30fps, ~30.8s,
narrated with karaoke-style caption pills, Poppins ExtraBold headlines, blue gradient / light dotted-grid
scenes, navy accent dots, -14 LUFS.

- **Voice:** Kokoro `af_heart` (open-source, Apache-2.0), generated per line by `src/tts.mjs` from `src/script.json`.
- **Timeline:** `src/timeline.py` trims each line, lays them out, times every word, chunks captions and snaps scene cuts to the 120 BPM grid → `src/timeline.js`.
- **Scenes:** `src/index.html` (each frame is a pure function of time) → `src/capture.js` (Playwright) → PNG frames.
- **Sound:** `src/music.py` — Am–F–C–G bed resolving to C on the end card, effects synced to on-screen actions, ducked ~9 dB under the voice (voice ≈12 dB above music).
- **End card (ICP):** "Built for sales team leaders." + feature icons + "Book a demo" + tryconexus.com. To split-test another ICP, change line `l10` in `script.json` and `#Gt` in `index.html`, then re-run the pipeline.

## Build

```bash
# 1. voice (from a folder where kokoro-js is installed)
node tts.mjs src/script.json brag-output/work/vo
# 2. timeline + voice track
python3 src/timeline.py src/script.json brag-output/work/vo brag-output/work/vo.wav src/timeline.js
# 3. music + mix
python3 src/music.py src/timeline.js brag-output/work/vo.wav brag-output/work/mix.wav
# 4. frames
node src/capture.js brag-output/work/frames 30
# 5. encode (poster frame 96 baked in as frame 0)
ffmpeg -framerate 30 -i brag-output/work/frames/f%04d.png -i brag-output/work/mix.wav -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart out.mp4
```

## Script

| Scene | Narration | On screen |
|---|---|---|
| A | Every payday, the same question. Did my spiff count? | "Every payday. Same question." + stacked agent messages |
| B | You dig through spreadsheets and chat threads, and someone still gets missed. | "Spreadsheets. Missed spiffs." + broken spreadsheet (#REF!) |
| C | With Conexus, spiffs run themselves. | Logo reveal + "Spiffs that run themselves." |
| D | Set one up once. The moment a sale closes, it's credited to the agent, automatically. | "Credited at the close." Cursor activates spiff → order completed → balance $150 → $175 |
| E | The leaderboard updates live, so the whole floor sees who's winning. | "Everyone sees who's winning." Jordan climbs from 3rd to 2nd |
| F | Every dollar lands on the ledger. Payday math. Done. | "Payday math, done." Ledger rows → Balance owed $175.00 |
| G | Meet Conexus, the CRM built for sales team leaders. Book a demo at tryconexus.com | Logo, ICP line, feature icons, Book a demo |

People are anime characters (see `../../brand/CLAIMS.md` → Demo data); orders and amounts are made up. Claims come from `../FEATURES.md`.

## Closing-line change (2026-11-01)

"Conexus. Built for sales team leaders." sounded choppy: the voice read "Conexus." as a one-word sentence followed by a fragment.
Replaced with a full sentence: **"Meet Conexus, the CRM built for sales team leaders."** (same style as `../05-team-chat-call-teams`).
Only the closing line's voice was regenerated; all other narration audio is unchanged. The end-card text stays as it was.
