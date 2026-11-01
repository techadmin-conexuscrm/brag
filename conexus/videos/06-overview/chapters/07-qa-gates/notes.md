# 07 · QA protects every sale — notes

Duration 16.7 s · scenes A (blue) → B (light) → C (blue).

## Scenes
- **A** "Pass QA, then close." — Order #20481 (Aoi Todo, sold by Yuji, $149.00) moves Awaiting Recording → Review In Progress → score 9.1 → ✓ Completed on "passes". Order #20482 (Kasumi Miwa, Megumi, $129.00) scores 5.4 on "failing" and stops at Review Required with "Flag Reason: Low Score". The pass threshold of 7.0 is shown.
- **B** "One queue, your call." — QA page with the filters Agent, Min/Max Score, Flag Reason (set to Low Score), Disposition and Min Duration (s), and the review queue (Agent / Customer / Duration / Score / QA Status). The cursor selects Megumi's row and **Manager Actions** opens. It clicks **Approve Order** on "approve": "Approving...", then the toast "Call has been approved" and the row turns ✓ Approved. Reject Order and Re-run Analysis pulse on their words.
- **C** "Catch it early." — Order #20483 (Toge Inumaki, Maki, $89.00, 6.1, Flag Reason: Both, Issues Detected). The cursor clicks **Reject Order** on "caught": the status becomes Canceled and the toast reads "Call has been rejected". On the spoken words, "Refund" and "Chargeback" pills land and are struck through ("Caught before it turns into a").

## Claims → evidence
| Claim | Evidence |
|---|---|
| A call's order waits in awaiting_recording → review_in_progress | BE `components/calls/jobs/process-call-recording.ts:66-83`; `orders/services/create-order.ts:469-478` |
| Passing (score ≥ threshold, no flags) completes the order | `process-call-recording.ts:132-155` |
| Failing sends the order to review_required (low_score / flags / both) | `process-call-recording.ts:156-173`; `analyze-call.ts:219-229` |
| Approve → order completed; Reject → order canceled | `calls/services/approve-call.ts:24-40`; `reject-call.ts:52-64` |
| Re-analyze | `calls/services/reanalyze-call.ts`; FE `manager-actions.tsx:150-158` |
| One queue filtered by agent, score, flag reason, disposition, duration | FE `pages/QAPage.tsx:93-200` (queue = `qaStatusFilter={["review_required"]}`, :204); flag reason labels :21-26 |
| Labels | "Manager Actions", "Approve Order", "Reject Order", "Re-run Analysis", "Approving...", toasts `components/Calls/manager-actions.tsx:42,57,124-158`; statuses `components/Table/StatusCell.tsx` |

Benefit line ("before they turn into refunds or chargebacks") is phrased as a benefit, with no statistic. Note for the lead: rejecting cancels the order, but the code does not void or refund a payment that was already taken (`reject-call.ts`). That is why the visual only crosses out the words and never claims "no charge".

## Cast
Agents Yuji Itadori, Megumi Fushiguro, Maki Zenin, Nobara Kugisaki; QA manager Kento Nanami (implied cursor); customers Aoi Todo, Kasumi Miwa, Toge Inumaki.

## Liberties
- The QA page is condensed: the real table has more columns (Call, Direction, Tags, From/To, Status, Disposition, Order, Recording, Call Time). Manager Actions really sits on the call detail page, not under the table.
- "Canceled" uses the CRM's fallback capitalisation of the `canceled` order status.
