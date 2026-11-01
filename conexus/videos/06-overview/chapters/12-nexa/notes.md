# 12 · Nexa AI & call scripts — notes

Duration 17.1 s · 3 scenes · cast (Frieren: Beyond Journey's End): Fern (new-hire agent), Himmel (admin), customer Heiter. Company in UI: "Aura Wellness" (Frieren character name).

## Scenes
- **A (blue)** "Just ask Nexa." — knowledge-base files (Refund Policy.pdf, Product Guide.docx, Pricing.xlsx) land; Fern types a question, Nexa types an answer citing "Refund Policy.pdf", then looks up Heiter's last order (#20417, Starter Kit, $129.00, Shipped). Header chip "Only what Fern can see".
- **B (light)** "Every call, on script." — Welcome call.docx dropped into "Upload a script" → "4 steps imported"; the agent script panel's merge fields (`{{customer.first_name}}` etc.) fill in with Heiter / Fern / Aura Wellness / #20417 / $129.00 / Lisbon.
- **C (blue)** "Roll back in a click." — cursor clicks "Publish changes" (v3 goes Live), then "Roll back to this" on v2 → v4 Live "rolled back to v2"; Fern's dialer shows "An admin just published version 4. You're seeing it now."

## Claims → evidence
| Claim | Evidence |
|---|---|
| Assistant is called "Nexa" (internal, staff-facing) | FE `src/dialer/useNexaScope.ts:35` (`label: "Nexa"`), FE `src/components/Chatbot/FloatingChatbot.tsx` |
| "Answers from <company>" header, "Type your message..." input, h:mm:ss timestamps | FE `src/components/Chatbot/ChatbotInterface.tsx:259,362,332` |
| Answers from your own uploaded docs (PDF/DOCX/XLSX…), cites document title | BE `chatbot/routes.ts` upload (PDF, TXT, CSV, DOCX, XLSX, XML); `chatbot/jobs/process-document.ts:105-129`; system prompt in `chatbot/services/process-message.ts` ("cite the document title"); FE `src/pages/admin/KnowledgeBase.tsx:212` accept list |
| Looks up customers/orders/products only where the user has read permission | BE `chatbot/tools/index.ts:30` (`hasPermission(user, tool.requiredPermission, orgId)`), `search-orders.ts:79` (`read#order`), `search-customers.ts:58` (`read#customer`), `search-products.ts:48` |
| Upload .docx/.pdf/.txt/.md into a draft | BE `call-scripts/routes.ts:75`, `services/upload/detect-file-type.ts:10`; FE `ScriptEditor.tsx:266` "Upload a script" |
| Merge fields | BE `call-scripts/services/format/merge-fields.ts:12-28` (customer.first_name, agent.first_name, company.name, order.id, order.total, customer.city) |
| Draft → publish creates a new version; rollback re-publishes an older one as N+1 | BE `call-scripts/routes.ts:117`, `services/publish-script.ts` header comment |
| UI wording: "Published versions", "Live", "Roll back to this", "Publish changes", "Save draft", publish/rollback messages, "An admin just published version N. You're seeing it now." | FE `dialer/scripts/ScriptVersions.tsx:40,57,74`, `ScriptEditor.tsx:165,402,412,422`, `ScriptPanel.tsx:218` |
| Script step UI ("Step 2 of 4 ·", progress bars, checklist, Back/Next, "Script for the campaign of this call's order.") | FE `dialer/scripts/ScriptPanel.tsx:31,231-290` |

## Caveats / left out
- Scripts are edited and shown in the dialer (`src/dialer/scripts/`), i.e. the dialer add-on. Narration doesn't say "with the dialer add-on"; FEATURES.md lists "Versioned call scripts with merge fields" as safe without a caveat. Lead may want to add "in the dialer".
- The real chat UI doesn't render tool calls, so none are shown; the answer text and the order table are illustrative (Nexa's replies are model-written markdown).
- Not claimed: customer-facing chatbot, Nexa listening to calls.
