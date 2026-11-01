# 06 · AI call QA — notes

Duration 18.8 s · scenes A (blue) → B (light) → C (dark).

## Scenes
- **A** "No more sampling." — 12 call tiles; while "small sample" is said only 2 get a "Reviewed" stamp and the rest dim. The cursor flips **Enable QA System** on at "QA on", then a score lands on every tile (green ≥8, amber ≥6, red <6, as in CallsTable). All durations ≥ 1:00 and they flash on "over a minute".
- **B** "Your rules, with reasons." — Transcription card (AGENT / CUSTOMER lines), then the QA Score Summary counts up to 9.3/10 · Approved · Pass Threshold 7.0/10, plus a summary and Criteria Evaluation rows (boolean Pass, scaled 8/10, boolean Pass), each with its reasoning. Score maths: (10 + 8 + 10) / 3 = 9.3.
- **C** "Critical flag, agent paused." — Issues Detected card (critical flag criterion + reasoning). Nobara's state goes from "On a call" to "Not ready · Paused by QA" on "pauses". An email card "User Access Blocked - Nobara Kugisaki in Jujutsu High" lands on "emails". Then the cursor clicks "Generate unflag code", which shows a 6-digit code, "Works once, for 24 hours".

## Claims → evidence (BE = conexuscrm-be/src, FE = ConexusCRM-FE/src)
| Claim | Evidence |
|---|---|
| Only when QA is on | BE `components/telephony/services/handle-call-recording.ts:201` (queue only if `qaEnabled`); `lib/db/models/organizations.ts:49` default false; `analyze-call.ts:129-136` |
| Voicemails skipped | BE `components/calls/jobs/process-call-recording.ts:39-40` |
| Scored only if ≥ 60 s (shorter ones are auto-approved, not scored) | `process-call-recording.ts:94-112` |
| Transcribed, agent and customer separated | `transcribe-call.ts:57-60`; `components/ai/transacription/aws-transcribe.ts:302-317` (channel labels Agent/Customer when the direction is known) |
| Your own criteria: boolean, scaled 1–10, flags with warning/critical | `lib/db/models/calls.ts:177-199`; FE `components/Calls/QASettings/criterion-form.tsx:97-99,119` |
| Score 0–10 = average of boolean (10/0) and scaled answers | `analyze-call.ts:93-121` |
| Summary + per-criterion reasoning | `analyze-call.ts:14-31,56-57,233-236`; FE `score-summary.tsx:75,128`, `criteria-breakdown.tsx:39` |
| Pass threshold (default 7.0) | `process-call-recording.ts:132`; FE `qa-settings-card.tsx:106` |
| A critical flag pauses the agent in that company | `handle-call-analyzed-event.ts:15-32` (`organizationMembers.flagged = true` for that org) |
| Admins are emailed | `handle-call-analyzed-event.ts:58-68` + `lib/email/templates/user-blocked.ts` (subject "User Access Blocked - {{userName}} in {{organizationName}}") |
| One-time unflag code (6 digits, 24 h, used once) | `lib/db/models/flagged-user-codes.ts:14-28`; `organizations/services/unflag-code.ts:28`; FE `dialer/supervisor/QaUnlock.tsx:219,241`, `activityLabels.ts:176` |
| UI labels | "Enable QA System" `qa-settings-card.tsx:83`; "Issues Detected" `score-summary.tsx:116`; "Not ready · Paused by QA" `dialer/agentStatus.ts:44` + `supervisor/shared.tsx:78-79`; "Review Required"/"Approved" `components/Table/StatusCell.tsx` |

Narration never says "100%" or "every call". It says "every recorded call over a minute", "with QA on".

## Cast
Agents Yuji Itadori, Megumi Fushiguro, Nobara Kugisaki (flagged), Maki Zenin; admin Yuta Okkotsu; customers Toge Inumaki, Aoi Todo, Kasumi Miwa. Company "Jujutsu High".

## Liberties / not shown
- The subtitle under the toggle ("Score threshold 7.0/10 · your own criteria") is my copy. The real subtitle reads "Automatically analyze and score all call recordings", which overstates the case, so I left it out.
- The email card is a summary (recipient line + real subject), not the HTML email itself.
- The transcript is shown as two lines with AGENT/CUSTOMER chips. The real transcript panel is plain text with channel labels.
- The FE badge shows the type in lowercase ("boolean", "scaled"); I used uppercase chips.
