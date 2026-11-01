# 08 · Listen, whisper, barge — notes

Duration 20.0 s · scenes A (blue) → B (light) → C (dark).

## Scenes
- **A** "The floor, live." with a "Dialer add-on" chip. Live wallboard with the tabs Live wallboard / Agents / Missed calls / Agent activity / QA, a "Live · Updated just now" chip, and the tiles Calls waiting / Longest wait / Service level. Below are the Queues table (Waiting, Longest wait, Answered today) and Agents with state pills whose clocks tick. Nobara's row is blue with "🔒 Collecting card". On "statuses" Megumi goes Ready → Ringing → On a call, Calls waiting drops 3 → 2 and Sales answered goes 41 → 42. The Queues and Agents sections pulse on "queue" and "agent".
- **B** "Three ways to step in." — Yuji's live call with the Listen / Whisper / Barge in buttons, each clicked on its word. A diagram (Kento Nanami → Yuji Itadori ↔ Aoi Todo) shows who hears the supervisor: Listen = nobody, Whisper = only the agent, Barge in = both.
- **C** "Card entry stays private." — The cursor clicks Listen on Nobara while she is collecting a card, and the server's refusal appears: "Listening is not available while the customer is entering card details. Try again once they have finished." Then the Agent activity log (with a Missed calls tab) fills in: "Kento Nanami whispered on their call", "Missed a call · It rang and wasn't answered", "Went Not ready · On break · Was Ready", "Answered a call".

## Claims → evidence
| Claim | Evidence |
|---|---|
| Listen / whisper (only agent hears) / barge (both hear) | BE `components/calls/services/spy-call.ts:32-38,107-112` |
| Listen needs `monitor#call`; whisper and barge need `control#call` | `spy-call.ts:84-90,101-105,215-223` |
| Whisper/barge need the dialer add-on | `spy-call.ts:225` (`assertDialerEnabled`). The Supervisor screens are dialer-only (FE `SupervisorScreen.tsx:211`), so the whole chapter is labelled "Dialer add-on" and narrated "With the dialer add-on" |
| Monitoring refused during card entry (all modes, Listen included) | `spy-call.ts:260-267`; message `controls/secure-entry.ts:115`; MODE_LABEL "Listening" `spy-call.ts:114-118` |
| Wallboard: queues + agents + states | FE `dialer/supervisor/Wallboard.tsx:328-382,412-459,498-560`; state labels `dialer/agentStatus.ts:51-58`; Collecting card `Wallboard.tsx:275-283`; buttons `Wallboard.tsx:151-154` |
| Tabs: Live wallboard, Agents, Missed calls, Agent activity, QA | `SupervisorScreen.tsx:48-52` |
| Agent activity wording | `dialer/supervisor/activityLabels.ts` (`call_monitored` :192-200, `call_missed`, `status_changed`, `call_answered`) |

## Cast
Supervisor Kento Nanami; agents Yuji Itadori, Megumi Fushiguro, Nobara Kugisaki, Maki Zenin; customer Aoi Todo. Company "Jujutsu High".

## Liberties
- The wallboard is condensed: the Abandoned, Avg handle time and Agents tiles are left out, and the Queues table drops the Service level/Abandoned/Avg handle columns. The real "Blue rows…" hint continues "You never see card details."
- Nobara's monitor buttons are hidden on the wallboard in scene A (they are shown in scene C) to keep the row on one line.
- "Missed calls" is shown as a tab next to Agent activity; I didn't draw the missed-calls table itself.
- I left out the Agents board's Required/Optional toggles.
