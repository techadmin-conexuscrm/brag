# ConexusCRM — Verified Features (for marketing)

Checked against the code on 2026-10-31: backend `conexuscrm-be` @ `b16c432` (main),
frontend `ConexusCRM-FE` (master). Only claims in the **Safe to say** column go on screen.

| Area | Status | Safe to say | Don't say (yet) |
|---|---|---|---|
| AI call QA | ✅ when QA is switched on | "AI scores every recorded agent call over a minute against **your** scorecard — with reasons and a summary." "Not a 2% sample." | "100% of calls" (calls under 60s are auto-approved, not scored; QA is off until enabled) · "AI coaching" |
| QA enforcement | ✅ | "A critical violation locks the agent out and alerts admins instantly." "Sales tied to a call only close when the call passes QA." | — |
| QA review queue | ✅ | "Approve, reject or re-analyze from one queue, filtered by agent, score and flag." | A fixed "QA manager" role (it's a custom role) |
| Leaderboard | ✅ | "Live revenue leaderboard with gold/silver/bronze, top performer, most improved, needs attention." | Order-count column (broken) · coaching notes (mock) |
| Spiffs | ✅ | "Spiffs credit automatically when a sale completes. Every agent has a running balance and a full ledger." Six types: per-sale flat/%, accumulated, deadline, first-to-target. | Commissions · payroll export · "mark as paid" · "raffle" as a random draw |
| Softphone / dialer | ✅ (dialer is an add-on) | "Dial from the browser — encrypted calls, IVR, queues, business hours, voicemail, transfers with notes, number purchase." Calls recorded automatically. | Predictive / power dialing · answering-machine detection |
| Supervisor tools | ✅ (whisper/barge need dialer add-on) | "Listen, whisper or barge into live calls." "Live wallboard and agent activity log." | — |
| Calling-hours protection | ✅ (strict on dialer orgs) | "Calls are blocked outside 8am–9pm in the customer's local time, max 3 attempts per day, blocked numbers never dialed — enforced by the server." | National DNC registry scrubbing · "TCPA compliant" |
| Team chat | ✅ | "Built-in team chat — channels, DMs, @mentions, reactions, pins, file sharing — inside the CRM and the dialer." | "Replaces Slack" as a hard claim (fine as a tone line: "no more switching to Slack") |
| Team chat in the dialer | ✅ (dialer add-on) | "Message the floor without leaving the call." The dialer's Messages tab works during a live call (`DialerNav.tsx`). | — |
| GIFs in team chat | ⏳ shipping week of 2026-11-02 (not in code yet) | Only once live in production. | Anything about GIFs before it ships |
| Customer SMS | ❌ | — | Any texting customers |
| Conexus Sheets / Docs | ❌ not in code | — | Shared spreadsheets / docs / co-editing |
| Email customers | ⚠️ automated only | "Automatic emails on order events (completed, tracking, payment link, refund, failed payment), logged on the customer timeline." | Writing a one-off email from the CRM |
| Client CS portal sync | ⚠️ API webhooks only | "Signed webhooks for ~60 events (calls, notes, emails, orders, transactions) to keep your systems in sync." | A built-in connector to a client's CS portal · one-click setup |
| Customer portal | ✅ basic | "Customers see their orders and fix a failed payment themselves." | Tickets / messaging in the portal |
| Payments | ✅ | "Take payments, refunds and voids inside the CRM — NMI, Authorize.net, Stripe, Revolv3. Payment links. Checkout from the dialer." "Only a token and last 4 are stored — never the full card number." | "Card data never touches our servers" · secure keypad payment (not live yet) |
| Order intake | ✅ | Shopify (incl. abandoned carts), WooCommerce, ClickBank, Konnektive, SamCart, CartPanda, BuyGoods, Digistore24, Calendly … | Zoom (removed) |
| Roles & permissions | ✅ | "Custom roles with fine-grained permissions." | — |
| Reports | ✅ | "10 built-in reports — revenue, transactions, refunds, contact center, member status." | — |
| Tasks | ✅ | "Tasks with priorities, checklists, multiple assignees, linked to orders and customers." | — |
| Call scripts | ✅ | "Versioned call scripts with merge fields." | — |
| AI assistant "Nexa" | ✅ internal | "Nexa answers your team's questions from your own docs and looks up customers and orders." | Customer-facing chatbot |
| Security | ⚠️ | Encrypted calls (SRTP), argon2 passwords, role-based access, agent activity log. | MFA/2FA · SSO beyond Google · encryption at rest · PII redaction · recording consent |

## Corrections found while building the overview film (2026-11-01)

| Area | Finding | Evidence | Say instead |
|---|---|---|---|
| Spiff ledger | Ledger rows are recorded, but no API route or screen shows them. Only the running spiff balance is visible. | BE `spiffs/services/get-balance-ledger.ts` (exported, unused by routes); no FE usage | "Every credit is recorded" — don't show a ledger screen until one ships |
| Billing descriptors | The gateway descriptor is NOT sent as the card-statement descriptor (NMI: commented out; Stripe: description only; Authorize.net: order description; Revolv3: invoice ref). | `nmi/index.ts:41-42`, `stripe/checkout-session.ts:129-133` | "Agents can look up the gateway and its billing descriptor" — never "it's what's on the statement" |
| Blocking agent charges | `blockAgentInitiatedCharges` exists but isn't enforced on main (`isAgentChargeBlocked()` returns false) and has no settings toggle. | `agent-charge-policy.ts:4-24`, `CallingRulesCard.tsx:179` | Don't mention |
| Charging a saved card | Saved cards are only created by secure keypad entry (not live), so charging a saved card isn't available in practice. | `tokenize-from-telephony.ts:195-207` | Don't mention until the keypad ships |
| Void | Exists in the API, but the order's Transactions menu only offers Retry and Refund. | `transactions/routes.ts`, FE `Orders/Order/Transactions.tsx` | Say "refund", not "void" |
| QA reject | Rejecting a call cancels the order but doesn't refund or void a payment already taken. | `reject-call.ts:52-64` | Never "no charge" |
| QA settings copy | The product's own toggle subtitle says it scores "all call recordings" — calls under 60 s and voicemails are skipped. | FE `QASettings` | Product copy fix for the dev team |
| Calling-hours caps | Manual dials can exceed the 3-a-day cap with a reason (admins notified); auto-dial can't. | `calls/services/calling-hours-policy.ts` | Show the block; don't call the cap absolute |
