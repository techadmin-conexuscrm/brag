# 10 · Customer service — notes

Checked against BE `conexuscrm-be` @ `b16c432` (main) and FE `ConexusCRM-FE` @ `f7c9f07` (master).

## Cast (Spy x Family, names only)
Franky Franklin (agent), Yor Forger (agent); customers Henry Henderson, Sylvia Sherwood, Damian Desmond.
"Eden Academy Supply Co." / "Eden Supply · NMI" etc. are fictional.

## Scenes
- **A (light) — "Where's my order?"** Order O-048190 (Henry Henderson), Fulfillments tab: Status
  Pending Shipment → **Shipped**, Plugin ShipStation, Tracking Number 1Z84F2A00318462290; a stepper of the
  fulfillment statuses (Hold → Pending → Pending Shipment → Shipped → Delivered) fills to Shipped. Activities
  card: "System fulfillment status changed", "System assigned tracking number to order", "Email sent ·
  'Your order has shipped'".
- **B (blue) — "Who charged me?"** Transaction Details report filtered to Sylvia Sherwood: O-048177,
  Oct 28 2:16 PM, $59.90, Gateway "Eden Supply · NMI" (highlighted). Then the Gateways list (Name /
  Descriptor) with that gateway's descriptor `EDENSUPPLY*SHOP` highlighted, tag "Billing descriptor".
- **C (light) — "Refund it, just once."** Order O-048201 (Damian Desmond), Transactions tab (Transaction ID /
  Type / Amount / Currency / Status). Cursor: ⋯ → Refund → "Refund Transaction" dialog (Refund Amount 64.90,
  Refund Reason "Arrived damaged") → Refund Transaction → toast "Refund processed successfully", new Refund
  row 64.90 USD Completed, order chip Completed → Refunded, note "Same refund again within 2 minutes is
  refused". Then "Email sent · Your refund for O-048201" and "Refund Summary · Today": 13 → 14 refunds,
  $812.40 → $877.30 (812.40 + 64.90).

## Claims → evidence
| Claim | Evidence |
|---|---|
| Order page tabs (Order Details, Transactions, Fulfillments, Emails, Activities) | FE `src/components/Orders/OrderForm.tsx:166-174`, fulfillments tab `:1472` |
| Fulfillment columns Status / Plugin / Tracking Number; status labels | FE `src/components/Fulfillments/FulfilmentTable.tsx:87-111`; `components/Table/StatusCell.tsx:3-31` |
| Fulfillment statuses hold → pending → pending_shipment → shipped → delivered | BE `src/lib/db/models/orders.ts:217-225` |
| ShipStation sends fulfillments and polls status, carrier and tracking every 30 min; records `order.tracking_number.assigned` | BE `plugins/plugins/shipstation/index.ts:12-30`, `shipstation/poll-status-of-fulfillments.ts:64-106`; API path `orders/services/update-order-external-fulfillments.ts:33-66` |
| Tracking email goes out automatically (auto-responder on "tracking number assigned") | BE `emails/listeners/handle-email-auto-responders.ts:17-29`; FE responder label "Order Tracking Number Assigned" `components/Campaigns/Campaign/Emails/index.tsx:31` |
| Logged on the customer timeline | BE `activity/services/handle-event.ts:130` (tracking), `:183-197` (email.sent); customer Activities tab `FE components/Customers/Customer/CustomerDetails.tsx:397-405`; labels `FE utils/activityLabels.ts:12,16,27` |
| Customers can see their own orders and tracking (not shown, context only) | FE `components/CustomerPortal/Orders/OrderCard.tsx:220-237` |
| Transaction Details report has a Gateway column | FE `components/Reports/transactionDetailsColumn.tsx:55-56` |
| Each gateway has a Descriptor, set when adding it and shown in the Gateways list | FE `components/Gateways/AddGateway.tsx:403-412`, `components/Gateways/index.tsx:170-172`; BE `transactions/services/create-gateway-instance.ts:55` |
| Refund from the order's Transactions table (⋯ → Refund), dialog fields, toast text | FE `components/Orders/Order/Transactions.tsx:97-180` (columns), `:218-221` (menu), `:344` (toast); `components/Transactions/popups/RefundTxn.tsx` ("Refund Transaction", "Refund Amount", "Refund Reason") |
| A double click never refunds twice / same refund within 2 minutes refused | BE `transactions/services/refund-transaction.ts:55-57`, `:69-72` (order lock), `:116-132` (2-minute guard, used by the refund endpoint) |
| Refund email auto-responder + logged | BE `handle-email-auto-responders.ts:27`, `activity/services/handle-event.ts:120` |
| Refund Summary report (Refunds, Refund Amount, by campaign/gateway/day) | BE `reporting/reports/refund-summary/index.ts:12-25`; FE `pages/reports/refund-summary/constants.ts:13-24` |

## Wording choices / not claimed
- **Billing descriptor:** I did NOT say it is "sent with every charge" or that it is "exactly what appears on
  the statement". In the code the field is not sent as a statement descriptor by any gateway: NMI has it
  commented out (`transactions/gateways/nmi/index.ts:41-42`), Stripe deliberately sends it only as the
  payment description, not `statement_descriptor` (`gateways/stripe/checkout-session.ts:129-133`),
  Authorize.net uses it as the order description (`authorizenet/build-requests.ts:192`), Revolv3 as
  `MerchantInvoiceRefId` (`revolv3/index.ts:56`). The statement text comes from the merchant account. The
  film only says the agent "checks the billing descriptor of the gateway that took it", shown where it really
  lives: the Gateways page (needs `read#gateway`) — the order and its Transactions tab don't show the gateway;
  the Transaction Details report does.
- **Void:** not shown. The API has `POST /v1/transactions/:id/void` (`transactions/routes.ts:47-52`), but the
  order's Transactions menu only offers Retry and Refund (`Transactions.tsx:205-221`).
- The tracking email depends on the campaign having the "tracking number assigned" auto-responder set up;
  narration says it "went out on its own", which is how it works once configured.
- Carrier "UPS" appears only in the activity sub-line (BE stores `carrier`, the CRM fulfillments table does not
  show a carrier column; the customer portal does).
