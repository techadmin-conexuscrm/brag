# 03 · Calling-hours protection — notes

Cast (My Hero Academia names only): Izuku Midoriya (agent), Eijiro Kirishima (Chicago, late call),
Momo Yaoyorozu (attempt cap), Denki Kaminari (blocked). 555 numbers only.

## Scenes
- **A (dark, night)** — Eijiro's card, cursor clicks *Dial Now* → "Checking…". Calling-window track (8 AM – 9 PM
  their time) with a red pin at "Now in Chicago 9:42 PM". The real block dialog lands: "Cannot call Eijiro
  Kirishima" + "Outside calling hours (8:00-21:00 customer local time). Local hour: 21, Timezone: America/Chicago",
  with a "Refused by the server" chip.
- **B (light)** — Momo: "Calls · last 24 h" counter fills 1 → 3 / 3, three outbound rows, then "This would be call
  #4 to this customer today / 3 outbound calls to this customer in the last 24 hours (limit 3)." Denki: Blocked
  chip, disabled Dial Now clicked → "This customer is blocked from calls: Asked not to be called".
- **C (blue)** — The org's "Calling rules" card: Calling window 8 AM – 9 PM, No address on file 11 AM – 9 PM (ET),
  Enforce calling hours on, Attempts per customer per day 3.

## Claims shown + evidence
| Claim | Evidence |
|---|---|
| 8 AM – 9 PM customer local time | BE `src/lib/timezone/calling-window.ts:2-3`; `src/components/calls/services/calling-hours-policy.ts` (`evaluateStrictCallingHours`, `clampGuardrails`) |
| Fallback 11 AM – 9 PM Eastern when location unknown | BE `calling-window.ts:4-12`; `src/lib/db/models/telephony.ts:833-840` |
| Max 3 attempts per rolling 24 h | BE `calling-window.ts:13-17`; `telephony.ts:842-845`; `calling-hours-policy.ts` attempt-cap block |
| Enforced by the server (both click-to-call and softphone) | BE `src/components/telephony/services/destination/get-outbound-destination.ts:~170-190` (`assertStrictCallingHours`) |
| Blocked customers never dialed | BE `get-outbound-destination.ts:~158-168` ("This customer is blocked from calls: {reason}"); `src/components/calls/services/dial-customer.ts:17-19` |
| Strict mode = dialer orgs (and auto-dial) | BE `calling-hours-policy.ts` `strictGuardrailsFor`; `telephony.ts:822` (`strictCallingHours` default true). Narration says "With the dialer, the server blocks it." |
| Dialog wording | FE `src/components/Table/CallButton.tsx` ("Cannot call {name}", clock icon, Close); BE message format in `calling-hours-policy.ts` (`Outside calling hours (8:00-21:00 customer local time). Local hour: …, Timezone: …`) |
| Attempt-cap wording | FE `src/components/Telephony/CallingHoursBlockDialog.tsx` ("This would be call #N to this customer today"); BE attempt_cap message in `calling-hours-policy.ts` |
| Calling rules card | FE `src/components/Telephony/CallingRulesCard.tsx` (title, description, "Calling window", "In the customer's local time. Outside it, the dialer refuses the call.", "No address means no timezone, so these are called on Eastern time.", "Enforce calling hours", "On, a call outside the window is refused.", "Attempts per customer per day"). The row label "No address on file" is shortened from "Customers with no address on file"; "From (ET)" from "From (Eastern)". |

## Honesty notes
- Never says "TCPA compliant"; closing line is "built to keep your whole floor inside calling-hours rules".
- No national DNC registry scrubbing is claimed — "blocked" means a customer the org blocked (block reason is free
  text; "Asked not to be called" is example data).
- On manual dialing an agent can go past the attempt cap with a reason (admins are notified, logged) and can confirm
  local time for an unknown location; auto-dial can never override, and a known location outside hours is never
  overridable (`calling-hours-policy.ts` `assertStrictCallingHours`). The film shows the block, not the override, and
  does not claim the cap can never be overridden.
- Admins can switch strict enforcement off for manual dialing ("Enforce calling hours"); shown switched on.
- "Refused by the server" is an on-screen annotation chip, not a UI label. The "Calls · last 24 h" counter is an
  illustrative visual (the count is real server logic; the widget is not a product screen).
