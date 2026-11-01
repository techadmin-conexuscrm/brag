# 05 · Spiffs & leaderboard — notes

**Duration:** 16.80 s · 3 scenes · voice `af_heart`
**Source:** adapted from `../../04-spiffs-v2/src/` (scenes D, E, F).

## Scenes
| Scene | Narration | On screen |
|---|---|---|
| A (light) | "Set up a spiff once, and Conexus does the counting for you." / "The moment Tanjiro closes a sale, his balance is credited automatically." | `05 · Spiffs & leaderboard` tag, "Credited at the close." Create Spiff card (Name: Friday Push · Type: Flat / Per Sale · Reward amount ($): 25.00). The cursor clicks Create on "once" and the status shows "● active". Spiff Balance card (Tanjiro Kamado). "Order completed #10482 · $189.00" toast on "closes". The balance counts $150.00 → $175.00 with +$25.00 on "credited". |
| B (blue) | "The leaderboard updates live, so the whole floor sees who's winning." | "Everyone sees who's winning." Leaderboard (Name / Total Revenue, gold/silver/bronze, 1st/2nd/3rd Place). On "live", Tanjiro's revenue goes $41,980 → $42,169 (+$189) and he passes Katsuki Bakugo ($42,110) for 2nd. |
| C (light) | "Every dollar lands on his ledger, so payday math is already done." | "Payday math, done." Ledger for Tanjiro: Friday Push per sale #10482 +$25, #10477 +$25, 20 Sales by Thursday deadline target reached +$100, Manual adjustment +$25. Spiff balance **$175.00** (= 25+25+100+25; and $150 before the newest +$25). |

## Claims → evidence
| Claim | Evidence |
|---|---|
| Spiffs credit automatically when a sale completes | BE `src/components/events/listners.ts:58` (`order.completed` → `evaluateSpiffsForOrder`); `src/components/spiffs/services/evaluate-spiffs-for-order.ts:28` (completed only), `:45` (active spiffs), `:56` (per-sale processing) |
| Flat per-sale reward credited to the agent's balance + ledger row | BE `src/components/spiffs/services/process-ongoing-spiff.ts:47` (reason `Spiff payout: {name} (per sale)`); `credit-spiff-balance.ts:18` (insert `balance_ledger`), `:33` (`spiffBalance +=`) |
| Running balance | BE `src/lib/db/models/organizations.ts:101` (`spiff_balance`); FE `src/components/admin/user/index.tsx:290-291` ("Spiff Balance", "Total earned spiff rewards") |
| Ledger of every credit (payouts + manual adjustments) | BE `src/lib/db/models/spiffs.ts:39-41` (`spiff_payout`, `manual_adjustment`), `:78` (`balance_ledger`); `process-deadline-spiff.ts:136` (deadline target reached); `adjust-member-balance.ts:23` |
| New spiffs default to active | BE `src/lib/db/models/spiffs.ts:55` |
| UI labels Create Spiff / Reward amount ($) / Create / Flat / Per Sale | FE `src/components/SpiffsComponent/SpiffsFormLayout.tsx:123`, `:154`, `:253`; `spiffTableColumns.tsx:10` |
| Live revenue leaderboard with medals | FE `src/components/Leaderboard/index.tsx:43` (refetch every 60 s), `:65` (Total Revenue), `:140-144` (gold/silver/bronze, 1st/2nd/3rd Place) |

## Not shown / honest wording
- No commissions, payroll, "mark as paid" or payout-export claims. The total is labelled "Spiff balance", not "owed".
- The leaderboard "Order Count" column (`Leaderboard/index.tsx:74`, broken) is not shown. Coaching notes (mock) are not shown.
- **Ledger screen:** the ledger is real data (`balance_ledger` table + `get-balance-ledger.ts` service), but I found no route or FE screen that lists it today. The ledger card is a faithful rendering of those rows, not a copy of an existing screen. Narration says "lands on his ledger", which matches the data model.
- The Create-Spiff → "● active" morph compresses the real flow (Create in a side panel → row in the Spiffs table with status `active`).
- "Live" = the leaderboard refetches every 60 s. The narration and FEATURES.md both use "live".

## Cast
Demon Slayer: Tanjiro Kamado (agent). The leaderboard also shows Satoru Gojo, Katsuki Bakugo, Anya Forger and Shoyo Hinata, the same as the standalone video. Zenitsu, Inosuke, Nezuko and Giyu appear in the standalone's "problem" scenes, which this shortened chapter doesn't use. Orders and amounts are made up.
