# 09 · Payments on the call — notes

Checked against BE `conexuscrm-be` @ `b16c432` (main) and FE `ConexusCRM-FE` @ `f7c9f07` (master).

## Cast (Spy x Family, names only)
Loid Forger (agent), Yor Forger (agent); customers Becky Blackbell, Damian Desmond.
Store "Eden Academy Supply Co." is fictional.

## Scenes
- **A (blue)** — "Sell it on the call." Dialer order panel on Loid's live call with Becky: 2 × Stella Star
  Planner $48.00 + 1 × Chimera Plush $19.00 = $67.00, shipping $5.95, total **$72.95**. Steps
  1 · Products → 2 · Payment → 3 · Done. "Card, you type it" → "Save order and take card" → card form →
  "Charge $72.95" → "Card taken · confirming with Stripe" → "Approved · $72.95", order O-048213.
- **B (light)** — "Send a payment link." Yor on a call with Damian: Eden Academy Tie $34.00 + shipping
  $5.90 = **$39.90**. "Send a payment link" (Email chip) → "Save order and email the link" → "Link emailed"
  done box, plus the customer's email card ("Complete your order O-048214", Payment Pending, Pay now).
- **C (blue)** — "Four gateways. Only a token." NMI / Authorize.net / Stripe / Revolv3 text chips, then
  "What Conexus keeps for a card": gateway token, brand + last 4, expiry, fingerprint; full card number
  "Never stored".

## Claims → evidence
| Claim on screen / in narration | Evidence |
|---|---|
| Orders taken in the dialer on the agent's own call (dialer add-on, company's "Orders in the dialer" switch) | BE `src/components/calls/routes.ts:298-351` (`/v1/calls/:callId/order`, `/order/stripe-session`, `/order/link`); FE `src/dialer/orders/access.ts:27-50` (needs `dialerEnabled` + `allowOrders`) |
| Panel labels: steps "Products / Payment / Done", "New order", "How is X paying?", totals rows | FE `src/dialer/orders/OrderPanel.tsx:70`, `:105-121`, `:295`, `:918` |
| "Card, you type it" — agent types the card into Stripe's own fields | FE `OrderPanel.tsx:936-945`; BE `src/components/calls/dialer-order-schema.ts:12-21`, `services/dialer-orders/order-stripe-session.ts:18-31` |
| "Save order and take card", "Charge $72.95", "Card taken · confirming with Stripe", "Approved · $72.95" | FE `OrderPanel.tsx:885`, `:1055-1061`; `src/dialer/orders/StripeStep.tsx:431` |
| Payment link by email, order waits until paid; "Save order and email the link", "Link emailed", "waiting for payment. Sent to …" | FE `OrderPanel.tsx:948-962`, `:887`, `:1064`, `:1105-1106`; BE `calls/routes.ts:343-350`; `orders/services/create-order.ts:139-155` (link needs the `order.payment_link.created` auto-responder); `emails/listeners/handle-email-auto-responders.ts:26` |
| Gateways: NMI, Authorize.net, Stripe, Revolv3 | BE `src/components/transactions/gateways/index.ts:5-10` |
| Stored for a card: gateway token, brand, last 4, expiry, fingerprint — never the full number | BE `src/lib/db/models/saved-payment-methods.ts:39-48`; transactions keep only a truncated fingerprint `src/lib/db/models/transactions.ts:40-44`; format `transactions/utils/card.ts:97-129` ("411111:1111:1230") |

## Left out on purpose / could not verify
- **Secure keypad** ("Card, on the phone keypad") — not live; not shown. Note that in the real panel the keypad
  option is listed first; the film shows only the option being used.
- **Charging a saved card** — left out. Saved cards are only ever created by secure keypad entry
  (`telephony/services/secure-payment/tokenize-from-telephony.ts:195-207`, `source: "phone_keypad"`), and the
  dialer's `/order/charge` charges "the card the customer just keyed in on this call"
  (`calls/services/dialer-orders/charge-dialer-order.ts:23-27`). Showing it would show the keypad.
  The "what we keep" card in scene C uses the saved-payment-method fields only as a description of storage.
- **`blockAgentInitiatedCharges` (admins block agent charges)** — left out. The column exists with default
  `true` (`lib/db/models/telephony.ts:853-857`, `telephony/services/automations/get-dialer-automations.ts:44`),
  but the enforcement hook `isAgentChargeBlocked()` returns `false` on main
  (`transactions/services/saved-payment-methods/agent-charge-policy.ts:4-24`, "not on main"), and the FE
  settings card skips the field when saving (`components/Telephony/CallingRulesCard.tsx:179`) with no toggle.
  Not live, so not claimed.
- In the dialer, "Card, you type it" exists only for Stripe products, and the payment-link option only for
  non-Stripe products (`OrderPanel.tsx:935`, `:947`); the two calls in A and B are different orders, so this
  is consistent. No claim that Conexus "never receives" card data was made.
- Scene A gateway labelled "Card · Stripe" (my label, not a literal FE string).
