# 02 · Built-in dialer — notes

Cast (My Hero Academia names only): Izuku Midoriya (agent), Shoto Todoroki, Ochaco Uraraka (agents, in the
transfer list), Tenya Iida (team lead, in the transfer list), Eijiro Kirishima, Momo Yaoyorozu, Denki Kaminari
(customers). Company chip "U.A. Supply" is invented demo data. All phone numbers are 555 numbers.

## Scenes
- **A (blue)** — Izuku's dialer (header: Ready switch; rail: Phone / Messages / Customer / History). Cursor clicks
  *Dial Now* on Eijiro → "Calling…" → call card (company chip, Outbound, timer, Connected, Mute / Hold / Keypad /
  Transfer / Take payment / End call). "Encrypted call" and "Recording" chips land on the spoken words.
- **B (light)** — Line → IVR (1 · Sales) → Sales queue; incoming-call card "From the Sales queue · Line …", ringing
  counter, Answer clicked → connected timer. Business-hours card: "Closed · to voicemail".
- **C (blue)** — Transfer dialog (Transfer / Add to call tabs, Teams and people list, "Note for Shoto Todoroki
  (optional)"), note typed, *Transfer to Shoto Todoroki* clicked → Shoto's incoming card with the
  "Transferred by Izuku Midoriya" note; Izuku moves to "Wrap-up".

## Claims shown + evidence
| Claim | Evidence |
|---|---|
| Dial from the browser (softphone, click-to-call) | FE `src/dialer/components/ActiveCallCard.tsx`, `src/components/Customers/Customer/IdentityRail.tsx:245-253` ("Dial Now"); BE `src/components/calls/services/originate.ts` |
| Calls encrypted (SRTP) | BE `src/components/calls/services/originate.ts:81,153` (`rtp_secure_media` = `mandatory`) |
| Recorded automatically | BE `src/components/telephony/services/destination/get-outbound-destination.ts` (customer calls return `record: true`), `get-inbound-destination.ts:292,426,517…` (`record: true`). Internal extension-to-extension calls are not recorded (`record: false`) — the film only shows customer calls. |
| Call card controls + labels | FE `src/dialer/components/ActiveCallCard.tsx` (Mute, Hold, Keypad, Transfer, Take payment, End call; "Connected"/"Connecting…"; `formatClock` mm:ss in `src/utils/callTimer.ts`) |
| Ready / Not ready status | FE `src/dialer/agentStatus.ts` (`STATE_LABELS`, `NOT_READY_REASONS`), `CompanyCard.tsx:275-276` |
| Rail items Phone / Messages / Customer / History | FE `src/dialer/components/DialerNav.tsx:9-14` |
| Inbound from a queue | FE `src/dialer/components/IncomingCallCard.tsx` ("Incoming call", "From the {queue} queue · Line …", "ringing Ns", "Last order …", Decline / Answer); BE routes `/v1/telephony/ring-groups*` in `src/components/telephony/routes.ts` |
| IVR | BE `src/components/telephony/routes.ts:362-382` (`/v1/telephony/ivr-menus`) |
| After hours → voicemail | BE `get-inbound-destination.ts:386-430` (closed business hours divert to voicemail, `record: true`); routes `/v1/telephony/business-hours*` |
| Transfer with a note, seen before answering | FE `src/dialer/components/TransferDialog.tsx:410-440, 617-645` ("Transfer"/"Add to call", "The caller goes straight to them and you move to wrap-up.", "Note for {name} (optional)", "They see it before they answer…", "Transfer to {name}"); `IncomingCallCard.tsx` ("Transferred by {agent}" + note); "Wrap-up" from `agentStatus.ts` `STATE_LABELS` |

## Honesty notes
- The dialer is an add-on (`organizations.dialer_enabled`, BE `src/lib/db/models/organizations.ts:36`). The chapter
  title says "Built-in dialer" and nothing mentions plans; the add-on wording is left to the lead if wanted.
- Not claimed: predictive/power dialing, answering-machine detection (the AMD flag exists but defaults off).
- "Encrypted call" and "Recording" are on-screen annotations, not literal UI labels (the real card says "Connected").
  "Connected · Recording" on the inbound card is the same kind of annotation.
- Business hours "Mon–Fri · 9:00 AM – 6:00 PM" is example configuration.
