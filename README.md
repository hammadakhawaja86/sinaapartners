# Sinaa Partners — marketing site

A fourteen-page static site built from the offer deck
(`7Rise_offer_deck_13072026.pptx`), carrying the **Sinaa Partners** identity:
the supplied logo, the five-swatch navy / gold / cream palette, and a
typography system verified against WCAG 2.1 AA.

```
python3 site/build.py     # regenerates every .html file
```

No dependencies, no build toolchain, no server. Open `index.html`, or serve
the folder with `python3 -m http.server`.

## Naming

The deck reads "7Rise"; the supplied logo reads "SINAA PARTNERS". Confirmed
with the client: **the logo wins** — this site is Sinaa Partners, and the
7Rise name does not appear anywhere in it.

## Information architecture

Every claim, list and process step below is lifted from the deck unless
marked **ADDED**.

| Page | Deck source | Role in the funnel |
| --- | --- | --- |
| `index.html` | slides 1, 2, 3, 4, 9, 11, 12 | Positioning, the three pillars, the loop, proof, CTA |
| `solutions.html` | slide 3 | Pillar hub + a "where to start" decision table (ADDED) |
| `strategy.html` | slide 5 | Pillar 01 — diagnostics, Discover→Diagnose→Design→Roadmap |
| `technology.html` | slide 6 | Pillar 02 — build, plus the clinical / compliance / automation verticals |
| `managed-operations.html` | slide 7 | Pillar 02 — BPO across finance, HR, marketing, sales, admin |
| `capital.html` | slide 8 | Pillar 03 — readiness through to close |
| `sectors.html` | slide 4 | The eight sectors, expanded to a paragraph each |
| `approach.html` | slides 9, 12 | The flywheel and the three-step start |
| `engagement.html` | slide 10 | The four commercial models |
| `why-sinaa.html` | slide 11 | The four differentiators, plus what they rule out |
| `investors.html` | — | **ADDED** |
| `readiness.html` | — | **ADDED** |
| `insights.html` | — | **ADDED** |
| `contact.html` | slide 12 | Intro call → scoping proposal → kick off |

### The three added flows, and why

The deck names capital partners as an audience twice but gives them no route
through the material, has no self-serve entry point between "read the offer"
and "book a call", and offers nothing that builds credibility before the
first conversation. Three flows close those gaps:

1. **`investors.html` — For Investors.** The venture-opportunity surface. The
   same three pillars, re-framed across a hold period: commercial and
   operational diligence pre-deal, value-creation planning in the first
   hundred days, portfolio build-and-run capacity during the hold, exit
   readiness at the end. Plus three ways a fund can contract (deal-by-deal,
   portfolio framework, operating partner).
2. **`readiness.html` — Growth Readiness Scan.** Six questions, scored
   client-side, returning which pillar to start with. It qualifies the lead
   *and* teaches the pillar model in two minutes. Nothing is transmitted; the
   answers never leave the browser.
3. **`insights.html` — Perspectives.** Six positions written out in full
   rather than an index of links that do not exist yet. Each one ends on the
   pillar it argues for.

Two smaller additions: the decision table on `solutions.html`, and the
"combining models" section on `engagement.html`.

## Brand

### Colour

Tokens live in `assets/brand.css`. The five supplied swatches map to:

| Token | Hex | Use |
| --- | --- | --- |
| `--ink` | `#04101F` | Hero and footer grounds |
| `--navy` | `#0A1B2E` | Headings, dark buttons, the wordmark |
| `--navy-2` | `#12293F` | Raised surfaces on dark |
| `--gold` | `#A9761D` | The ring. Fills, rules, borders, the diamond bullet |
| `--slate` | `#6D85AC` | From the mark. Fills and rules only |
| `--cream` / `--cream-2` | `#F2E6D2` / `#FAF4EA` | Warm section grounds |

Three of those cannot carry text at their supplied values, so the palette
carries text-safe siblings and the stylesheet uses those instead:

| Pairing | Ratio | Verdict |
| --- | --- | --- |
| `--gold` `#A9761D` on white | **3.97:1** | Fails AA for text. Fills, borders and large display only. |
| `--gold-text` `#8C5F14` on white | 5.58:1 | Text on white ✓ |
| `--gold-text` on `--cream` | 4.53:1 | Text on the warm ground ✓ |
| `--gold-lt` `#C9932F` on `--ink` | 7.00:1 | Accent text on dark ✓ |
| `--slate` `#6D85AC` on white | **3.75:1** | Fails AA for text. Graphics only. |
| `--slate-text` `#4A628A` on white | 6.17:1 | Text on white ✓ |
| `--text-body` `#33445C` on white | 9.90:1 | Body ✓ |
| `--text-body` on `--cream` | 8.02:1 | Body on warm ✓ |
| `--navy` on white | 17.37:1 | Headings ✓ |
| `--text-muted-dark` `#B9C6D8` on `--ink` | 11.04:1 | Body on dark ✓ |
| `--ink` on `--gold` | 4.82:1 | **Primary button label** ✓ |
| white on `--gold` | 3.97:1 | Rejected — this is why gold buttons carry ink text |

`--gold` at 3.97:1 on white also satisfies WCAG 1.4.11 (3:1) where it is used
as a component boundary — card top rules, the mega-menu edge, focus rings.

Every page is checked programmatically: the audit walks every text node,
resolves the nearest opaque ancestor background, and asserts 4.5:1 (or 3:1
for large text). It passes on all fourteen pages.

### Type

**Sora** for display and UI, **Inter** for body — both loaded from Google
Fonts with a system fallback stack. Sora's wide geometric forms echo the
logotype; Inter carries the reading load. The scale is fluid
(`clamp()`), body text never drops below 16px, and no supporting text below
14px. Line length is capped at 68ch.

### The mark

`MARK` in `build.py` is a **vector recreation** of the Sinaa Partners symbol —
the broken gold ring, the navy S-curve, the slate diamond and leaf. Geometry
and colours are matched to the supplied artwork, but it is a redraw. Swap in
the official SVG when it is available; the header, footer and hero all read
from that one constant.

The gold diamond used as a list bullet is the mark's diamond, rotated 45°.

## Accessibility

- Skip link, one `<main>` and one `<h1>` per page, landmark `<nav>` elements
  with `aria-label` / `aria-labelledby`.
- The Solutions menu is a real `<button>` with `aria-expanded` /
  `aria-controls`, closes on Escape (returning focus to the trigger), on
  outside click, and on focus leaving the panel.
- Visible focus rings everywhere, gold-light on dark grounds.
- `prefers-reduced-motion` disables scroll reveal, smooth scrolling, and the
  hover lifts.
- Every page works with JavaScript disabled. The reveal animation starts at
  full opacity for the no-JS case only when the observer is unavailable, and
  the readiness scan degrades to a plain (unscored) form.
- Wide content — the decision table — scrolls inside its own container; no
  page scrolls horizontally.

## Content that still needs the client

Placeholders carried straight from the deck's final slide, left visible on
purpose rather than invented:

- `contact.html` — `[Name]`, `[title]`, `[phone]`
- `hello@sinaapartners.com` throughout — confirm or replace
- No client names, logos, case studies or performance figures appear
  anywhere. `investors.html` offers references and an anonymised walkthrough
  under NDA instead, which is the honest version until real proof points are
  cleared for publication.

## Relationship to the rest of this repository

None. This is a self-contained brand and does not consume the 31G design
system tokens in `tokens/` — different client, different palette. Nothing
here changes anything above `site/`.
