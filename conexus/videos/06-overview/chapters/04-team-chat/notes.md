# 04 · Team chat — notes

**Duration:** 18.33 s · 2 scenes · voice `af_heart`
**Source:** adapted from `../../05-team-chat/src/` (scenes D and F). The GIF scene (E) is deliberately left out: GIFs are not shipped (they belong to 14-coming-soon).

## Scenes
| Scene | Narration | On screen |
|---|---|---|
| A (light) | "Your team chat lives right inside Conexus, with channels, DMs and mentions." / "Pin the announcement everyone needs, and react to a big close in one click." | `04 · Team chat` tag, "Your floor, in one place." CRM Messages: drawer with Channels / Direct Messages (each section lights up when named), #closers with Messages · Pins · Files · Links tabs. Armin's @Mikasa mention lands on "mentions". The cursor hovers Levi's @all message, clicks the pin: "Pinned by Levi Ackerman" label, yellow tint, Pins tab goes 0 → 1. The cursor taps 🔥 and the count climbs from 1 to 6. "Sasha Braus is typing…" |
| B (blue) | "With the dialer add-on, agents can message the floor without leaving the call." / "The floor lead sends the play, and the customer never waits." | "Never leave the call." Dialer Phone screen: live call with Jean Kirstein (Survey Corps · Inbound, timer running, Connected, Mute/Hold/Keypad/Transfer/New order/End call). The Messages tab gets an unread badge, the cursor taps it, and #closers opens while the Phone tab keeps its green in-call dot. Levi's play (@Mikasa) arrives, Mikasa types "On it 👍 adding it now" and it sends on "customer". The "On call · Jean Kirstein · 2:xx" pill keeps counting. |

## Claims → evidence
| Claim | Evidence |
|---|---|
| Team chat inside the CRM: channels and DMs | FE `src/components/Messages/MessageDrawer/index.tsx:253` (Channels), `:347` (Direct Messages) |
| @mentions (including @all) | FE `src/components/Messages/MentionSuggestion.tsx:12-19` (`{ _type: "all" }` + members) |
| Pins, with a "Pinned by …" label and a tinted row | FE `src/components/Messages/Message/index.tsx:159` (`bg-[#F2C7441A]`), `:205` (`Pinned by {pinnedBy}`); `src/components/Messages/Chat/PinnedMessages.tsx` |
| Chat tabs Messages / Pins / Files / Links, "N online" | FE `src/components/Messages/Chat/index.tsx:46-61`, `:194` |
| Emoji reactions with counts | FE `src/components/Messages/Message/MessageReactions.tsx:32-41` (grouped by emoji, count++) |
| Composer placeholder "Type a message...", attachments | FE `src/components/Messages/MessageInput.tsx:300`, `:36` |
| Messages works in the dialer during a call (dialer add-on) | FE `src/dialer/components/DialerNav.tsx:11` (Messages tab), `:31-35` (unread badge visible "on every screen, including during a call"), `:92` (green dot on Phone while on a call); `src/dialer/DialerApp.tsx:166` (MessagesScreen) |
| Dialer call card labels | FE `src/dialer/components/ActiveCallCard.tsx:298` (Connected), `:374/383/393/409` (Keypad, Transfer, New order, End call); `PhoneStatus.tsx:121` (Phone ready) |
| FEATURES.md rows | "Team chat ✅" and "Team chat in the dialer ✅ (dialer add-on)": narration says "With the dialer add-on" |

## Not shown / honest wording
- No GIFs, GIF button or GIF picker anywhere in this chapter.
- No "replaces Slack" claim; Slack isn't named.
- The white "On call · Jean Kirstein · 2:xx" pill above the dialer is a film annotation, not dialer UI. In the real dialer the in-call signal on the Messages screen is the Phone tab's green dot, which is also shown.
- File sharing appears only as the real "Files" tab and the paperclip in the composer. It isn't narrated.

## Cast (Attack on Titan)
Mikasa Ackerman (agent), Levi Ackerman (floor lead), Armin Arlert, Sasha Braus, Connie Springer; customer Jean Kirstein; company chip "Survey Corps". Phone number (555) 014-2290 is fictional.
