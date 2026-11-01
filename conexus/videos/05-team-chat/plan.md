# Video 5 — Team chat (ICP: GM of a call center floor)

Same style and pipeline as `../04-spiffs-v2` (see its `plan.md` for build steps). 9:16, 30fps, ~30.6s,
Kokoro `af_heart` narration, -14 LUFS.

> **Hold until GIFs ship.** GIFs are not in the code yet (Eric: shipping the week of 2026-11-02).
> Before posting: confirm GIFs are live in production, then match the picker in the video to the real
> one (search box, grid, any required provider attribution such as "Powered by GIPHY").

## Script

| Scene | Narration | On screen |
|---|---|---|
| A | Your agents bounce between Slack, a softphone, spreadsheets and the CRM. | "Five tabs. One sale." Browser tabs pop in as each tool is named, then flip frantically |
| B | Every switch is a customer on hold. | Dark scene, "Every switch, a customer waits." Hold timer counting up |
| C | Conexus puts your team chat inside the CRM. | Logo reveal + "Team chat, built in." |
| D | Channels, DMs and mentions, all in real time. Pin the plays that matter. React in a click. | "Your floor, in one place." #closers channel: @all spiff announcement gets pinned, close gets 🔥 reactions |
| E | And now, GIFs. Because every close deserves a celebration. | "Celebrate every close." GIF picker, search "sold", SOLD! sticker posts, 🎉 reactions |
| F | Agents can message the floor without ever leaving the call. | "Chat without leaving the call." Dialer mid-call (timer running), floor lead's message, agent replies |
| G | Conexus. Built for call center GMs. Book a demo at tryconexus.com | Logo, ICP line, icons, Book a demo |

GIF stickers (SOLD!, DING! bell, PAYDAY money rain, LET'S GO!, trophy, TO THE MOON) are original
animations drawn in `src/gifs.js`, not third-party GIFs. Slack is named once in the narration as a
comparison; no Slack logo or branding is shown.

Cast: Attack on Titan (see `../../brand/CLAIMS.md` → Demo data).
