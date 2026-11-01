# 13 · Security & compliance — notes

Duration 21.8 s · 3 scenes · cast (Frieren: Beyond Journey's End): Stark, Fern (agents), customer Eisen. Role "Floor agent" (custom role). Company "Aura Wellness" is not shown here.

## Scenes
- **A (dark)** "Locked down by design." — padlock snaps shut on "encrypted"; three proof cards: Call audio (waveform turns green, "SRTP required", "WSS signalling"), Saved card (number masks to •••• 4242; Stored: gateway token + last 4; Never: card number or CVV), Passwords (typed into an `$argon2id$…` hash).
- **B (light)** "Right people, right data." — "Floor agent" custom role: permissions toggle on/off (Can view customers / orders on; Can delete customers / Can listen to live calls off, with their `op#resource` keys); cards "Each company's data kept separate" and "Calling hours enforced by the server"; Agent activity log ("Append-only") with Opened the dialer / Went Ready / Answered a call.
- **C (blue)** "Where we stand today." — PCI DSS (Self-assessed), HIPAA-ready, GDPR-aligned, SOC 2 Type I (In progress), ISO 27001 (In progress); footer with the exact approved line: `PCI DSS (self-assessed) · HIPAA-ready · GDPR-aligned · SOC 2 Type I & ISO 27001 in progress` ("in progress" highlighted, stays on screen to the end).

## Claims → evidence
| Claim | Evidence |
|---|---|
| Browser call audio encrypted, SRTP mandatory | BE `calls/services/originate.ts:81,153` (`rtp_secure_media=mandatory`, `media_webrtc`); `lib/esl.ts:725`; `telephony/services/queues/pickup-next.ts:60` |
| WSS signalling | FE `src/components/Telephony/telephonySession.ts:311` (`wss://…:8081`) |
| Saved cards: gateway token + last 4 only, never number/CVV | BE `lib/db/models/saved-payment-methods.ts:19,39,43` |
| argon2 password hashing | BE `users/services/login.ts:1,24`, `change-password.ts:51`, `signup-complete.ts:12` (node-argon2 defaults: argon2id, m=65536, t=3, p=4 — the hash shown is illustrative) |
| Custom roles, fine-grained `${op}#${resource}` permissions | BE `lib/permissions/index.ts:49-50`, `organizations/services/create-role.ts`; FE labels `src/config/permissions.ts` ("Can view customers", "Can listen to live calls", …) |
| Data separated per company | BE `lib/permissions/index.ts:93-118` (permissions keyed by organization id, `Object.hasOwn` at :105); every model carries `organization_id` |
| Append-only agent activity log | BE `lib/db/models/agent-activity.ts:27`; FE wording `src/dialer/supervisor/activityLabels.ts` ("Opened the dialer", "Went Ready", "Answered a call") |
| Server-enforced calling hours (8am–9pm customer local) | BE `lib/timezone/calling-window.ts:1-3`, `calls/services/calling-hours-policy.ts:64` (`call:calling_hours_blocked`) |
| Compliance line | `/home/user/brag/conexus/brand/CLAIMS.md` (exact wording) |

## Wording choices
- Narration says "Browser calls are encrypted" (SRTP covers the browser ↔ phone-system leg; the carrier leg is not claimed).
- Narration says "Agent activity lands in an append-only log" (not "every action").
- Narration abbreviates "PCI self-assessed"; the screen shows the exact approved line.
- Not claimed: MFA/2FA, SSO, encryption at rest, PII redaction, recording consent, "HIPAA compliant/certified", "SOC 2 certified", "PCI certified".
- Calling hours are on screen only (not narrated); FEATURES.md notes it's strict on dialer orgs.
