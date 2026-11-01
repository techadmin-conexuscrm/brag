# 11 · Abandoned carts become calls — notes

Checked against BE `conexuscrm-be` @ `b16c432` (main) and FE `ConexusCRM-FE` @ `f7c9f07` (master).

## Cast (Spy x Family, names only)
Yor Forger (agent); customers Sylvia Sherwood (cart), Damian Desmond, Becky Blackbell, Henry Henderson
(incoming orders). "Eden Academy Supply Co." is fictional. No third-party logos — store and fulfillment
names are plain text chips.

## Scenes
- **A (blue) — "Left at checkout?"** Shopify checkout card (Sylvia Sherwood: Stella Star Planner $24.00 +
  Fountain Pen Set $31.00 = $55.00), chip "Checkout started 2:05 PM" → "No order after 60 min"; the cart dims
  and lands in Orders as O-048236, status **Abandoned**; pill "Checked every 15 minutes"; Assigned User
  Yor Forger; cursor clicks the row's call button → "Calling Sylvia Sherwood".
- **B (light) — "Your stores, one CRM."** "Orders in" chips: Shopify, WooCommerce, ClickBank, Konnektive,
  SamCart, CartPanda, BuyGoods, Digistore24 → Conexus hub with orders arriving (WooCommerce, ClickBank,
  SamCart) → "Fulfillment out" chips: ShipStation, ShipOffers, JetPack, PBS Fulfillment → "Tracking number back".

## Claims → evidence
| Claim | Evidence |
|---|---|
| Shopify abandoned checkouts become abandoned orders; checked every 15 minutes | BE `plugins/plugins/shopify/index.ts:22-30` (`*/15 * * * *`), `:54-131` (`status: "abandoned"`, `importSource: "shopify"`); checkouts tracked by webhook `shopify/webhook.ts:250-252` |
| "No order after 60 min" (store's timeout, default 60, 1–1440) | BE `shopify/config.ts:9-13`; `shopify/index.ts:39-43` |
| Imported orders are assigned round-robin to an agent | BE `orders/services/record-incoming-order.ts:129-131,176-179` (`isImported: true`); `orders/services/create-order.ts:167-169`; `orders/services/get-next-user-to-assign.ts` |
| Orders list: Order ID / Customer / Phone (call button) / Status / Assigned User; "Abandoned" status | FE `components/Orders/OrdersColumnDef.tsx:27,38-152`; `components/Orders/filters.ts:49` |
| Order sources: Shopify, WooCommerce, ClickBank, Konnektive, SamCart, CartPanda, BuyGoods, Digistore24 | BE `plugins/plugins/{shopify,woocommerce,clickbank,konnektive,samcart,cartpanda,buygoods,digistore24}/index.ts` (all `type: "data"`); FE import-source labels `components/Orders/filters.ts:37-44` |
| Fulfillment out: ShipStation, ShipOffers, JetPack, PBS Fulfillment | BE `plugins/plugins/{shipstation,shipoffers,jetpack,pbsfulfillment}/index.ts` (`type: "fulfillment"`) |
| Tracking comes back | BE `shipstation/poll-status-of-fulfillments.ts:64-106`; also `shipoffers/`, `jetpack/`, `pbsfulfillment/poll-status-of-fulfillments.ts` (every 30 min) |

## Not claimed
- Zoom (removed) — not mentioned. Calendly is an intake plugin for customers, not orders — not shown.
- No claim about calling instantly/automatically: the agent clicks call. Round-robin only assigns to members
  set to auto-assign and on shift (`get-next-user-to-assign.ts`); narration says "assigned to an agent".
- FE spells "JetPack" in its config description (`jetpack/config.ts`); "PBS Fulfillment" is my display name for
  the `pbsfulfillment` plugin.
