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
