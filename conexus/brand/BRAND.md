# Conexus — Brand Kit for Video

Source of truth: [`Conexus_Brand_Book.html`](Conexus_Brand_Book.html) — *Conexus Brand Book v1.0*
(2026-10-31). Open it in a browser for the full visual book. Colors match the live product
(`ConexusCRM-FE/src/index.css`). Every Conexus video made with `/brag` follows this file.

**Tagline:** Customer relationships, connected.

## The brand

- **Name:** Con·nect + nexus — the point where connections converge. Conexus is where
  customer relationships come together and move.
- **What it is:** A multi-tenant CRM platform that unifies calls, messages, orders and
  pipeline for modern teams — one connected place to run customer relationships end to end.
- **Attributes:** Connected · Capable · Clear · Trustworthy · Modern
- **The mark:** The letter **E** is built from three stacked banners reading forward —
  the signal-flag "E" at the heart of con**E**xus. It signals communication and momentum.
  Good motion idea: the three banners sliding in, left to right, to build the E.

## Voice & tone

Clear over clever · Confident, not loud · Human · Concise

| We say | We don't say |
|---|---|
| "Your payment went through. Receipt sent." | "Your transaction has been successfully processed." |
| "3 leads need follow-up today." | "You have outstanding action items in your queue." |
| "Connect your gateway to start taking orders." | "Leverage our platform to unlock synergies." |

Short, plain sentences. Concrete numbers and outcomes. No buzzwords, no hype.

## Logo

Files in `logos/` (transparent PNGs; full logos are 1524×224, marks 184×224):

| File | Variation | Use on |
|---|---|---|
| `logo-full-color.png` | Full color — Navy wordmark, Signal Blue + black flag E | Light backgrounds |
| `logo-dark-bg.png` | Light-blue — Bright Blue wordmark, Cyan + white flag E | Dark backgrounds |
| `logo-reversed-white.png` | Reversed white | Navy / brand-blue / dark backgrounds |
| `logo-mono-black.png` | Mono black (Ink `#0F172A`) | One-color, light backgrounds |
| `mark-full-color.png` | The mark (flag E), full color | Light — tight spaces, avatars |
| `mark-dark-bg.png` | The mark, light-blue | Dark backgrounds |
| `mark-white.png` | The mark, white | App-icon tiles on Navy or Conexus Blue |
| `favicon.svg` | Favicon (black mark in a white circle) | Browser tabs |
| `logo.svg` | Current shipped logo.svg (embeds a raster image) | Reference only |

There is no true vector logo yet. The 1524px PNGs are sharp up to ~1500px wide on screen,
which covers 1080p video; for 4K or very large scale-ups we need a real SVG export.

**Rules**
- Clear space: at least ½× the logo height on all sides.
- Minimum size: full logo 150px wide; mark 24px. In tiny spaces use the mark.
- Never stretch, recolor, rotate or add effects (glow, shadow, bevel) to the logo.
- Never put the dark-background logo on a light background, or any logo on a
  low-contrast background.
- The wordmark is custom lettering — never retype "Conexus" in Geist as a logo.
  Animate the supplied files (fade, slide, mask reveal); don't rebuild them.

## Color

**Navy anchors the brand; blue leads action in-product.**

Logo colors — light backgrounds
| Name | Hex | Role |
|---|---|---|
| Conexus Navy | `#0F2288` | Wordmark (light bg) |
| Signal Blue | `#0962C0` | Logo flag (light bg) |
| Logo Black | `#000000` | Lower flags |

Logo colors — dark backgrounds
| Name | Hex | Role |
|---|---|---|
| Bright Blue | `#1D8FFF` | Wordmark (dark bg) |
| Cyan | `#00CFFF` | Logo flag (dark bg) |

Brand / product blues
| Name | Hex | Role |
|---|---|---|
| Conexus Blue | `#2563EB` | Product UI — primary, links, CTAs |
| Blue Deep | `#1D4ED8` | Hover / pressed |
| Blue 500 | `#3B82F6` | Dark-mode primary |
| Blue 400 | `#60A5FA` | Highlights |
| Blue Soft | `#EFF6FF` | Tints, selected |

Neutrals & ink
| Name | Hex | Role |
|---|---|---|
| Ink | `#0F172A` | Primary text |
| Slate 700 | `#334155` | Secondary text |
| Slate 500 | `#64748B` | Muted text |
| Border | `#E5E7EB` | Borders |
| Muted | `#F1F5F9` | Muted surfaces |
| Surface | `#F8FAFC` | App background |
| White | `#FFFFFF` | Cards |

Status & semantic — use only for meaning
| Success `#059669` — confirmed, paid | Warning `#B45309` — pending, overdue | Info / Violet `#7C3AED` — informational | Destructive `#DC2626` — errors, delete |
|---|---|---|---|

Data / chart palette, in order: `#2563EB`, `#7C3AED`, `#059669`, `#B45309`, `#334155`

**Balance:** Neutral 70% · Ink 22% · Blue 8%. Blue is the accent, not the canvas —
except for full-bleed Navy title / end cards. Conexus Navy and Conexus Blue on white both
pass AA. On dark backgrounds use the Bright Blue / Cyan logo (or reversed white).

Dark canvas for video (product dark mode): `#080C16`.

## Typography

- **Geist** — primary typeface for product UI and marketing: all headlines, captions and
  on-screen copy. Display 700 · Heading 1–3 600 · Body 400.
- **Geist Mono** (500) — numbers, money, IDs, code: `$1,240.00` · `#INV-4821` · `+12.4%`.
  Tabular figures keep columns aligned and stop counting-up numbers from jittering.
- Both are free (SIL OFL): https://vercel.com/font
- The logo wordmark is custom lettering and a fixed asset — never reset it in Geist.

## UI look (for product shots and mock screens)

- Corner radius: sm 4 · md 6 · **lg 8 (default)** · xl 12 · 2xl 14 px
- Clean white cards on `#F8FAFC`, 1px `#E5E7EB` borders, soft low elevation (3 levels).
- Buttons: Primary (Conexus Blue), Secondary, Outline.
- Example stat card: label "Revenue", value `$48,250` in Geist Mono, delta `+12.4%` in Success green.
- Prefer real screenshots / recordings of the ConexusCRM app over invented UI.

## Video defaults

- Open or close on the logo with clear space; end card = logo + tagline
  "Customer relationships, connected." (+ URL / CTA when we have one).
- Navy (`#0F2288`) title and end cards with the reversed-white logo, or the dark canvas
  with the light-blue logo.
- Light, airy product scenes with Conexus Blue as the only accent.
- Motion: confident and smooth, forward (left → right) like the flag E. No glitch,
  shake or neon effects.
- Copy on screen follows the voice rules above: one idea per card, few words.
