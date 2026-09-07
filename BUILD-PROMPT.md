# The finalised build prompt

A single, self-contained prompt. Paste it into any capable model or site
builder and it should reproduce this site — brand, structure, content and
accessibility rules — without needing the deck or this repository.

---

## PROMPT — Sinaa Partners website

You are an expert brand designer and marketing strategist. Build a premium,
fully responsive, accessible marketing website for **Sinaa Partners**, a
growth partner for ambitious management teams and the investors who back
them. Output static HTML and CSS with a small amount of vanilla JavaScript —
no frameworks, no build step, no external dependencies beyond web fonts.

### 1. Positioning

Tagline: **Strategy. Technology. Capital.**
Promise: **One partner across the entire growth journey.**

Sinaa Partners diagnoses what is really happening inside a business, builds
the technology and operating capability to fix it, and — when the moment is
right — takes the story to market to raise the capital that funds the next
stage. Three offers that stand alone or combine into one continuous
engagement.

The strategic argument the whole site must carry: growth stalls in the
**hand-offs**. The strategy house writes the plan and leaves; the build
partner ships something that does not match it; the adviser arrives at the
raise with a deck the operating numbers cannot support. Holding all three
removes the two most expensive transfers in the growth journey. Every page
should ladder back to that.

Two audiences, both first-class: **management teams** (professionalize, scale,
become fundable) and **capital partners** (find where value can actually be
created). Frame the business as a venture opportunity — an operating partner
across a hold period, not a vendor.

### 2. Voice

Confident, specific, unhurried. Institutional rather than startup. Short
declarative headlines; body copy that earns them with a concrete mechanism.
State what the firm will *not* do — it is more persuasive than another
superlative. No stock-consultancy filler ("synergies", "world-class",
"bespoke solutions"), no exclamation marks, no invented statistics, no client
logos or case studies unless supplied.

### 3. Brand system

**Palette** (five brand swatches plus text-safe siblings):

```
--ink        #04101F   hero and footer grounds
--navy       #0A1B2E   headings, dark buttons, wordmark
--navy-2     #12293F   raised surfaces on dark
--gold       #A9761D   fills, rules, borders, bullets — NOT text on light
--gold-text  #8C5F14   gold for text on light grounds
--gold-lt    #C9932F   gold for text on dark grounds
--slate      #6D85AC   graphics only — NOT text on light
--slate-text #4A628A   slate for text on light
--cream      #F2E6D2   warm section ground
--cream-2    #FAF4EA   subtle warm ground
--text-body  #33445C   body copy on light
--muted-dark #B9C6D8   body copy on dark
```

**Hard accessibility rules, non-negotiable:**

- Every text pairing must clear **WCAG 2.1 AA**: 4.5:1 normal, 3:1 for large
  text (≥24px, or ≥18.66px bold). Verify computationally, do not eyeball it.
- `#A9761D` is **3.97:1 on white** and `#6D85AC` is **3.75:1** — neither may
  carry body text on a light ground. Use `--gold-text` / `--slate-text`.
- A gold-filled button carries **ink** text (4.82:1). White on gold is
  3.97:1 and is forbidden.
- Gold as a *boundary* (card top rules, menu edge, focus ring) is fine at
  3.97:1 — that clears the 3:1 of WCAG 1.4.11.
- Watch specificity: a blanket `.on-dark a { color: gold }` will silently
  override a button's label colour and put gold text on a gold fill.

**Type:** Sora (display, UI, eyebrows) + Inter (body), Google Fonts with a
system fallback stack. Fluid `clamp()` scale; body never below 16px,
supporting text never below 14px; measure capped at ~68ch; headings
`letter-spacing: -0.02em` and `text-wrap: balance`.

**Logo:** a broken gold ring around a navy S-curve, with a slate diamond
upper-right and a slate leaf lower-left; wordmark "SINAA" over "PARTNERS",
letterspaced, navy over slate. Draw it as inline SVG from one shared
constant so header, footer and hero all update together. The rotated gold
diamond doubles as the list bullet throughout.

**Visual language:** dark navy hero with a large, low-opacity ring motif
bleeding off the right edge; cream sections to break the rhythm; hairline
rules; numbered pillar cards with a 3px gold top border; generous vertical
section rhythm (`clamp(4rem, 2rem + 7vw, 7.5rem)`); restrained motion —
scroll reveal and a 1px hover lift, both disabled under
`prefers-reduced-motion`.

### 4. Information architecture

Primary nav: **Solutions** (mega menu) · Sectors · Approach · For Investors ·
Why Sinaa · Insights, with a persistent dark "Start a conversation" button.
Below 1040px it collapses to a disclosure drawer. The mega menu lists the
four solution pages plus Engagement models and the Growth Readiness Scan.

Fourteen pages:

1. **Home** — hero; the hand-off argument; three pillar cards; the flywheel;
   eight sector tiles; four differentiators; a pointer to the readiness scan;
   closing CTA.
2. **Solutions** — pillar hub, plus a table mapping "if this sounds like you"
   → which pillar → typical engagement shape.
3. **Strategy & Consultancy (Pillar 01)** — full diagnostic deep-dive into
   operations, financials, organization and market position; root-cause
   analysis of performance gaps; strategic roadmap with prioritized
   initiatives; target operating model and organization design; board- and
   investor-ready recommendations. Process: **Discover → Diagnose → Design →
   Roadmap**. Close on the fact that the same team can execute the roadmap.
4. **Services & Technology (Pillar 02, build)** — product and platform
   strategy; architecture and solution design; build, integration and
   deployment; ongoing support and continuous improvement. Three specialist
   verticals: **Clinical**, **Compliance**, **Automation**.
5. **Managed Operations / BPO (Pillar 02, run)** — fully managed or
   co-sourced across **Finance** (accounting, reporting, FP&A), **HR**
   (recruiting, payroll, people ops), **Marketing** (content, campaigns,
   brand), **Sales** (pipeline, outreach, deal support), **Admin**
   (scheduling, data and document admin). Argue that clean operations are
   diligence evidence.
6. **Capital (Pillar 03)** — investment-readiness assessment; equity story
   and narrative; financial model and data room; investor targeting and
   outreach; process management to close. Process: **Readiness → Story &
   materials → Go to market → Diligence to close**. The differentiator: the
   raise is grounded in a diagnostic, not just a deck.
7. **Sectors** — Health Care (clinical systems, regulated care), Fintech
   (platforms, payments), PropTech, EduTech, E-commerce, Services
   (professional and business), Automation & AI, Compliance. A paragraph
   each. The common thread: regulated, operationally intricate, mid-transition.
8. **Approach** — the flywheel (Strategy → Build & Run → Capital → and the
   capital raised funds the next cycle), why each pillar makes the next one
   cheaper, and the three-step start.
9. **Engagement models** — Advisory Retainer; Project-Based Build; Managed
   Service (BPO); Capital Raise Engagement (retainer plus success fee tied to
   a completed raise). Plus how they combine, and an explicit "nothing is
   bundled".
10. **For Investors** — the venture surface. Pre-deal commercial and
    operational diligence; day 1–100 value-creation planning; portfolio build
    and run capacity through the hold; exit readiness. Three contracting
    modes: deal-by-deal, portfolio framework, fund-level operating partner.
11. **Why Sinaa** — one partner and no hand-offs; built by the team that
    designed it; comfortable with complexity; capital grounded in operating
    reality. Then a section on what that rules out.
12. **Perspectives** — six positions written out in full (not an index of
    links): diagnosis is where turnarounds fail; the hand-off is where value
    leaks; outsourcing is a control decision before a cost decision; automate
    the process you have already fixed; fundability is an operating condition,
    not a document; in regulated businesses compliance is the architecture.
    Each ends on the pillar it argues for.
13. **Growth Readiness Scan** — six questions (understanding of performance
    drivers; reliability of management information; whether the technology
    estate supports the plan; delivery capacity; senior time lost to the back
    office; funding readiness), four options each scored 0–3. Score
    client-side; under 45% → start with Strategy, 45–75% → start with
    Services & Technology, above 75% → start with Capital. Nothing is
    transmitted anywhere; say so on the page.
14. **Contact** — Intro call → Scoping proposal → Kick off. A form (name,
    work email, company, role, area of interest, the situation) that, absent
    a backend, composes a `mailto:`. Leave `[Name]`, `[title]` and `[phone]`
    as visible placeholders rather than inventing them.

### 5. Engineering requirements

- Generate the pages from **one script with a shared layout** so the header,
  mega menu and footer are identical everywhere. Do not hand-maintain
  fourteen copies of the nav.
- Semantics: skip link, one `<main>` and one `<h1>` per page, `<nav>`
  elements labelled, `<table>` with `<caption>` and `scope`, real `<button>`
  for the menu with `aria-expanded` / `aria-controls`, Escape closing it and
  returning focus to the trigger.
- Every page must work with JavaScript disabled and at 320px wide. Wide
  content scrolls inside its own container; the page body never scrolls
  horizontally.
- Visible `:focus-visible` rings on every interactive element, gold-light on
  dark grounds.
- Per-page `<title>`, meta description and Open Graph tags.
- Before you finish: run an automated contrast audit that walks every text
  node on every page, resolves the nearest opaque ancestor background, and
  asserts 4.5:1 (3:1 for large text). Fix anything it reports. Report the
  result.

### 6. Do not

- Invent client names, logos, testimonials, metrics, team members, office
  addresses or founding dates. Where proof would normally sit, offer
  references and an anonymised walkthrough under NDA instead.
- Use lorem ipsum.
- Ship a colour pairing you have not measured.
