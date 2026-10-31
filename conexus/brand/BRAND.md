# Conexus — Brand Kit for Video

Source: *Conexus Brand Book v1.0* (2026-10-31). Colors were confirmed against the
live product (`ConexusCRM-FE/src/index.css`) and sampled from the shipped logo files.
Every Conexus video made with `/brag` follows this file.

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

Files in `logos/`:

| File | Use |
|---|---|
| `logo-full-color.png` | Full logo on light backgrounds (navy wordmark, blue + black flag E) |
| `logo-dark-bg.png` | Full logo on dark / navy backgrounds (bright blue + cyan + white) |
| `mark-full-color.png` | Mark only, light backgrounds — tight spaces, avatars |
| `mark-dark-bg.png` | Mark only, dark backgrounds |
| `favicon.svg` | Favicon |
| `logo.svg` | Current shipped logo.svg (embeds a raster image) |

Still needed from the brand pack: mono black, reversed white, light-blue variants and
high-res (1200px) exports — see `conexus-logo-pack.zip`.

**Rules**
- Clear space: at least ½× the logo height on all sides.
- Minimum size: full logo 150px wide; mark 24px. In tiny spaces use the mark.
- Never stretch, recolor, rotate or add effects (glow, shadow, bevel) to the logo.
- Never put the dark-background logo on a light background, or either logo on a
  low-contrast background.
- The wordmark is custom lettering — never retype "Conexus" in Geist as a logo.
  Animate the supplied file (fade, slide, mask reveal), don't rebuild it.

## Color

**Navy anchors the brand; blue leads action.**

Logo colors
| Name | Hex | Where |
|---|---|---|
| Conexus Navy | `#0F2288` | Wordmark on light |
| Flag Blue | `#0962C0` | Top banner of the E on light |
| Ink Black | `#000000` | Lower banners of the E on light |
| Bright Blue | `#1E90FF` | Wordmark on dark |
| Cyan | `#00CFFF` | Top banner of the E on dark |
| White | `#FFFFFF` | Lower banners of the E on dark |

Product colors
| Name | Hex | Use |
|---|---|---|
| Conexus Blue | `#2563EB` | Primary action, highlights, CTAs |
| Blue Hover | `#1D4ED8` | Pressed / emphasis |
| Blue Soft | `#EFF6FF` | Tinted panels |
| Ink | `#0F172A` | Headline / body text on light |
| Slate | `#334155` | Secondary text |
| Muted | `#64748B` | Captions, labels |
| Background | `#F8FAFC` | Light canvas |
| Border | `#E5E7EB` | Dividers, card outlines |
| Dark canvas | `#080C16` (`hsl(222 47% 6%)`) | Dark-mode background |

Status (use only for meaning)
| Success `#059669` | Warning `#B45309` | Info `#7C3AED` | Destructive `#DC2626` |
|---|---|---|---|

Data / chart palette, in order: `#2563EB`, `#7C3AED`, `#059669`, `#B45309`, `#334155`

**Balance:** roughly 70% neutral, 22% ink, 8% blue. Blue is the accent, not the canvas —
except for full-bleed navy title / end cards. Navy and Conexus Blue on white both pass AA.

## Typography

- **Geist** — all headlines, captions and on-screen copy.
  Display 700 · Headings 600 · Body 400.
- **Geist Mono** (500) — numbers, money, IDs, code: `$48,250` · `#INV-4821` · `+12.4%`.
  Use tabular figures so counting-up numbers don't jitter.
- Both are free (SIL OFL): https://vercel.com/font

## UI look (for product shots and mock screens)

- Corner radius: 4 / 6 / **8 (default)** / 12 / 14 px
- Clean white cards on `#F8FAFC`, 1px `#E5E7EB` borders, soft low elevation.
- Example stat card: label "Revenue", value `$48,250` in Geist Mono, delta `+12.4%` in success green.
- Prefer real screenshots / recordings of the ConexusCRM app over invented UI.

## Video defaults

- Open or close on the logo with clear space; end card = logo + tagline
  "Customer relationships, connected." (+ URL / CTA when we have one).
- Navy (`#0F2288`) or dark canvas for title and end cards, using the dark-background logo.
- Light, airy product scenes with Conexus Blue as the only accent.
- Motion: confident and smooth, forward (left → right) like the flag E. No glitch,
  shake or neon effects.
- Copy on screen follows the voice rules above: one idea per card, few words.
