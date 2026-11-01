# 14 · Coming soon — notes

Duration 23.4 s · 3 scenes · cast (Frieren: Beyond Journey's End): Fern, Stark (agents), Frieren (team lead), Himmel (admin); customers Sein, Eisen, Übel.

Every scene has a `.soon` "★ Coming soon" badge at the top; every roadmap card/tile has its own "Coming soon" badge. The narration says "Coming soon", "are coming", "are on the way", "is coming next", "we're building", "more on the way". Nothing is shown as live; the AI-calling card is labelled "Preview · not live yet".

## Scenes
- **A (blue)** "What's coming next." — accordion roadmap; each card expands as it's named:
  1. **AI calling** — two lanes, "Fern · On a call with Sein" and "AI agent · On a call with Eisen", with waveforms. No specifics or numbers.
  2. **GIFs in team chat** — Stark: "Just closed Übel's upgrade!", picker with the original stickers from `shared/gifs.js` (sold, bell, letsgo), "SOLD!" picked, composer "Message #closers" + GIF.
  3. **Secure keypad payment** — phone keypad keys light up one at a time; agent panel "Secure entry in progress" shows only a digit count, "Agent hears: Silence", "Recording: No card digits", "Saved as: Gateway token + last 4".
- **B (light)** "Texts, sheets and docs." — cards flip in: **Customer texting (SMS)** (Fern ↔ Eisen thread) and **Conexus Sheets & Docs** (Frieren typing in a shared sheet, Himmel typing in a doc, presence avatars).
- **C (blue)** "And more on the way." — all five as "Coming soon" tiles plus a dashed "And more on the way…" tile.

## Sources
- Secure keypad: `/home/user/conexuscrm-be/docs/dialer/secure-payment-verification.md` (agent leg parked in silence, recordings masked, progress events are counts only, gateway token + brand/last four/expiry kept). The doc says it is built and unit-tested but has NOT run on live telephony, so it's shown as coming soon only. `saved_payment_methods.source = "phone_keypad"` exists in the model.
- GIFs: FEATURES.md says it ships the week of 2026-11-02 and isn't in code yet, so coming soon only. Stickers are the original canvas drawings in `shared/gifs.js`.
- SMS, Sheets & Docs, AI calling: not in code (FEATURES.md); roadmap only, as briefed.
