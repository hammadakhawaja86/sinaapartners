#!/usr/bin/env python3
"""Generate the Sinaa Partners marketing site.

Static HTML, no dependencies: `python3 site/build.py` rewrites every page in
site/ from the content model below. The generator exists so the header, mega
menu and footer stay identical across all fourteen pages — edit here, not in
the output.

Source of content: the Sinaa Partners offer deck (Strategy / Technology /
Capital). Flows not in the deck but required for a credible venture-facing
site are marked ADDED in the page notes.
"""

import os
import re

OUT = os.path.dirname(os.path.abspath(__file__))
SITE = "Sinaa Partners"
TAGLINE = "Strategy. Technology. Capital."
EMAIL = "hello@sinaapartners.com"

# --------------------------------------------------------------------------
# Brand mark — the official lockup, exported from the Sinaa Partners Figma
# file (node 27:541). Held as two static SVGs rather than inline markup: the
# artwork appears twice per page, and inlining it would repeat 13KB of path
# data in every document instead of being fetched and cached once.
# --------------------------------------------------------------------------
LOCKUP = "assets/sinaa-lockup.svg"
LOCKUP_ON_DARK = "assets/sinaa-lockup-on-dark.svg"

SOLUTIONS = [
    ("strategy.html", "01", "Strategy &amp; Consultancy",
     "Deep-dive diagnostics and a clear roadmap for the business."),
    ("technology.html", "02", "Services &amp; Technology",
     "Build the platform, start to finish — architecture through to run."),
    ("managed-operations.html", "02", "Managed Operations (BPO)",
     "Run finance, HR, marketing, sales and admin so you can focus on growth."),
    ("capital.html", "03", "Capital",
     "Go-to-market and raise support to fund what comes next."),
]

NAV = [
    ("Solutions", "solutions.html", True),
    ("Sectors", "sectors.html", False),
    ("Approach", "approach.html", False),
    ("For Investors", "investors.html", False),
    ("Why Sinaa", "why-sinaa.html", False),
    ("Insights", "insights.html", False),
]


def logo(tag="a", href="index.html", on_dark=False):
    """Render the lockup. `on_dark` picks the inverted variant.

    Two files, not one tinted copy: in the master artwork the wordmark and
    the flame are near-black (#020C1A), which disappears on the footer's
    ink ground. Both variants clear 3:1 against their own background.

    The intrinsic width/height attributes are the artboard's, so the box is
    reserved before the SVG lands and the header does not reflow.
    """
    return (
        '<{t} class="logo" href="{h}">'
        '<img class="logo__lockup" src="{s}" alt="Sinaa Partners"'
        ' width="564" height="138" decoding="async"></{t}>'
    ).format(t=tag, h=href, s=LOCKUP_ON_DARK if on_dark else LOCKUP)


def header(current):
    items = []
    for label, href, mega in NAV:
        cur = ' aria-current="page"' if href == current or (
            mega and current in [s[0] for s in SOLUTIONS]) else ""
        if mega:
            panel = "".join(
                '<a class="mega__item" href="{h}">'
                '<span class="mega__num">PILLAR {n}</span>'
                '<span class="mega__title">{t}</span>'
                '<span class="mega__desc">{d}</span></a>'.format(h=h, n=n, t=t, d=d)
                for h, n, t, d in SOLUTIONS
            )
            panel += (
                '<a class="mega__item" href="engagement.html">'
                '<span class="mega__num">COMMERCIAL</span>'
                '<span class="mega__title">Engagement models</span>'
                '<span class="mega__desc">Retainer, project build, managed service, or raise mandate.</span></a>'
                '<a class="mega__item" href="readiness.html">'
                '<span class="mega__num">TOOL</span>'
                '<span class="mega__title">Growth Readiness Scan</span>'
                '<span class="mega__desc">Two minutes. Find out which pillar to start with.</span></a>'
            )
            items.append(
                '<div class="nav__item">'
                '<button type="button" class="nav__link" data-mega-trigger '
                'aria-expanded="false" aria-controls="mega-solutions"{c}>Solutions'
                '<svg class="nav__caret" viewBox="0 0 10 10" aria-hidden="true">'
                '<path d="M1 3l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6" '
                'stroke-linecap="round" stroke-linejoin="round"/></svg></button>'
                '<div class="mega" id="mega-solutions" data-mega-panel hidden>{p}</div>'
                '</div>'.format(c=cur, p=panel)
            )
        else:
            items.append(
                '<div class="nav__item"><a class="nav__link" href="{h}"{c}>{l}</a></div>'.format(
                    h=href, c=cur, l=label))

    drawer_links = "".join(
        '<a href="{h}">{t}</a>'.format(h=h, t=t) for h, _n, t, _d in SOLUTIONS)
    drawer_more = "".join(
        '<a href="{h}">{l}</a>'.format(h=h, l=l)
        for l, h, mega in NAV if not mega)

    return """<header class="site-header">
  <div class="shell site-header__inner">
    {logo}
    <nav class="nav" aria-label="Primary">{items}</nav>
    <a class="btn btn--dark header__cta" href="contact.html">Start a conversation</a>
    <button type="button" class="burger" data-drawer-trigger aria-expanded="false" aria-controls="drawer">
      <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M1 4h14M1 8h14M1 12h14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
      <span data-drawer-label>Menu</span>
    </button>
  </div>
  <div class="drawer" id="drawer" data-drawer hidden>
    <div class="shell">
      <div class="drawer__group">
        <p class="drawer__label">Solutions</p>
        {dl}
      </div>
      <div class="drawer__group">
        <p class="drawer__label">Company</p>
        {dm}
        <a href="engagement.html">Engagement models</a>
        <a href="readiness.html">Growth Readiness Scan</a>
      </div>
      <div class="drawer__group" style="border-bottom:0">
        <a class="btn btn--primary" href="contact.html" style="margin-top:1rem">Start a conversation</a>
      </div>
    </div>
  </div>
</header>""".format(logo=logo(), items="".join(items), dl=drawer_links, dm=drawer_more)


FOOTER = """<footer class="site-footer on-dark">
  <div class="shell">
    <div class="footer__grid">
      <div>
        {logo}
        <p style="margin-top:1.25rem;max-width:32ch;font-size:var(--t-small)">
          One partner across the entire growth journey — diagnostic, build and run,
          and the capital that funds the next stage.</p>
      </div>
      <nav aria-labelledby="f-sol">
        <h2 id="f-sol">Solutions</h2>
        <ul class="footer__nav">
          <li><a href="strategy.html">Strategy &amp; Consultancy</a></li>
          <li><a href="technology.html">Services &amp; Technology</a></li>
          <li><a href="managed-operations.html">Managed Operations</a></li>
          <li><a href="capital.html">Capital</a></li>
        </ul>
      </nav>
      <nav aria-labelledby="f-co">
        <h2 id="f-co">Company</h2>
        <ul class="footer__nav">
          <li><a href="approach.html">Approach</a></li>
          <li><a href="sectors.html">Sectors</a></li>
          <li><a href="why-sinaa.html">Why Sinaa</a></li>
          <li><a href="insights.html">Insights</a></li>
        </ul>
      </nav>
      <nav aria-labelledby="f-st">
        <h2 id="f-st">Get started</h2>
        <ul class="footer__nav">
          <li><a href="readiness.html">Growth Readiness Scan</a></li>
          <li><a href="engagement.html">Engagement models</a></li>
          <li><a href="investors.html">For investors</a></li>
          <li><a href="contact.html">Book an intro call</a></li>
        </ul>
      </nav>
    </div>
    <div class="footer__bar">
      <p style="margin:0">&copy; 2026 Sinaa Partners. All rights reserved.</p>
      <p style="margin:0"><a href="mailto:{email}">{email}</a></p>
    </div>
  </div>
</footer>""".format(logo=logo(on_dark=True), email=EMAIL)


SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#04101F">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="assets/brand.css">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header}
<main id="main">
{main}
</main>
{footer}
<script src="assets/site.js" defer></script>
</body>
</html>
"""


def cta(heading, body, primary=("contact.html", "Book an intro call"),
        secondary=("readiness.html", "Take the readiness scan")):
    return """<section class="section cta-band on-dark">
  <div class="shell center reveal" style="max-width:760px">
    <h2>{h}</h2>
    <p class="lead">{b}</p>
    <div class="btn-row" style="margin-top:2rem">
      <a class="btn btn--primary" href="{p0}">{p1}</a>
      <a class="btn btn--ghost" href="{s0}">{s1}</a>
    </div>
  </div>
</section>""".format(h=heading, b=body, p0=primary[0], p1=primary[1],
                     s0=secondary[0], s1=secondary[1])


def page_hero(eyebrow, h1, lead):
    return """<section class="page-hero on-dark">
  <div class="shell page-hero__inner">
    <p class="eyebrow">{e}</p>
    <h1>{h}</h1>
    <p class="lead">{l}</p>
  </div>
</section>""".format(e=eyebrow, h=h1, l=lead)


PAGES = {}

# ==========================================================================
# Home
# ==========================================================================
PAGES["index.html"] = dict(
    title="Sinaa Partners — Strategy. Technology. Capital.",
    desc="One partner across the entire growth journey. We diagnose what is really "
         "happening inside a business, build and run the technology behind the fix, "
         "and take the story to market to raise the capital that funds what is next.",
    main="""
<section class="hero on-dark">
  <div class="hero__bg" aria-hidden="true">
    <svg viewBox="0 0 100 100" fill="none">
      <path d="M37 14.3 A38 38 0 0 0 37 85.7" stroke="#A9761D" stroke-width="1.2" stroke-linecap="round" opacity="0.32"/>
      <path d="M63 14.3 A38 38 0 0 1 63 85.7" stroke="#A9761D" stroke-width="1.2" stroke-linecap="round" opacity="0.32"/>
      <path d="M46 6 C30 26 62 40 58 54 C54 70 34 78 40 94 C30 74 52 62 48 48 C44 34 34 24 46 6 Z" fill="#12293F" opacity="0.5"/>
      <path d="M72 29 L83 40 L72 51 L61 40 Z" fill="#6D85AC" opacity="0.18"/>
    </svg>
  </div>
  <div class="shell hero__inner">
    <p class="eyebrow">Strategy. Technology. Capital.</p>
    <h1>One partner across the entire growth journey.</h1>
    <p class="lead">We work alongside ambitious management teams and the investors who
      back them. We diagnose what is really happening inside a business, build the
      technology and operating capability to fix it, and — when the moment is right —
      take the story to market to raise the capital that funds the next stage.</p>
    <div class="btn-row" style="margin-top:2.5rem">
      <a class="btn btn--primary" href="contact.html">Start a conversation</a>
      <a class="btn btn--ghost" href="solutions.html">See the three pillars</a>
    </div>
    <dl class="hero__meta">
      <div><dt>For management teams</dt><dd>Professionalize, scale, and become fundable.</dd></div>
      <div><dt>For capital partners</dt><dd>Find where value can actually be created.</dd></div>
      <div><dt>Engagement</dt><dd>Standalone pillars, or one continuous mandate.</dd></div>
    </dl>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="split reveal">
      <div>
        <p class="eyebrow">The offer</p>
        <h2>One partner, three ways to grow.</h2>
      </div>
      <div class="stack">
        <p class="lead">Most growth stalls in the gap between the three. The strategy
          house writes the plan and leaves. The build partner ships something that does
          not match the plan. The adviser arrives at the raise with a deck that the
          operating numbers cannot support.</p>
        <p>Sinaa Partners closes that gap by holding all three. Whether you are a
          management team looking to professionalize and scale, or a capital partner
          assessing where value can be created, our three offers stand alone or work
          together as one integrated engagement.</p>
        <p><a class="link-arrow" href="approach.html">How the three fit together</a></p>
      </div>
    </div>
  </div>
</section>

<section class="section section--warm">
  <div class="shell">
    <div class="center reveal" style="max-width:640px;margin-bottom:3.5rem">
      <p class="eyebrow">Our offer</p>
      <h2>Three pillars</h2>
      <p>Each pillar is a complete engagement in its own right. Together they form a
        single continuous growth journey.</p>
    </div>
    <div class="grid grid--3 reveal">
      <a class="card card--pillar" href="strategy.html">
        <span class="card__num">PILLAR 01</span>
        <h3>Strategy &amp; Consultancy</h3>
        <ul class="ticks" style="gap:.6rem;font-size:var(--t-small);margin-top:.5rem">
          <li>Deep-dive business diagnostics</li>
          <li>Strategic roadmap &amp; priorities</li>
          <li>Board-ready recommendations</li>
        </ul>
        <span class="link-arrow">Explore the pillar</span>
      </a>
      <a class="card card--pillar" href="technology.html">
        <span class="card__num">PILLAR 02</span>
        <h3>Services &amp; Technology</h3>
        <ul class="ticks" style="gap:.6rem;font-size:var(--t-small);margin-top:.5rem">
          <li>Tech build, start to finish</li>
          <li>Clinical, compliance &amp; automation</li>
          <li>Managed BPO across the business</li>
        </ul>
        <span class="link-arrow">Explore the pillar</span>
      </a>
      <a class="card card--pillar" href="capital.html">
        <span class="card__num">PILLAR 03</span>
        <h3>Capital</h3>
        <ul class="ticks" style="gap:.6rem;font-size:var(--t-small);margin-top:.5rem">
          <li>Investor-ready positioning</li>
          <li>Go-to-market for the raise</li>
          <li>Data room &amp; narrative support</li>
        </ul>
        <span class="link-arrow">Explore the pillar</span>
      </a>
    </div>
  </div>
</section>

<section class="section section--dark on-dark">
  <div class="shell">
    <div class="split reveal">
      <div class="sticky">
        <p class="eyebrow">How it fits together</p>
        <h2>Three offers. One growth journey.</h2>
        <p>Each offer stands alone. Together, they compound — because the capital
          raised funds the next cycle of strategy and growth.</p>
        <p style="margin-top:1.5rem"><a class="link-arrow" href="approach.html">See the full approach</a></p>
      </div>
      <div>
        <div class="loop">
          <div class="card card--dark">
            <span class="card__num">01</span>
            <h3>Strategy</h3>
            <p>Diagnose &amp; plan</p>
          </div>
          <div class="loop__arrow" aria-hidden="true">→</div>
          <div class="card card--dark">
            <span class="card__num">02</span>
            <h3>Build &amp; Run</h3>
            <p>Technology &amp; operations</p>
          </div>
          <div class="loop__arrow" aria-hidden="true">→</div>
          <div class="card card--dark">
            <span class="card__num">03</span>
            <h3>Capital</h3>
            <p>Fund the next stage</p>
          </div>
        </div>
        <p class="loop__note">↻ Capital raised funds the next cycle of strategy and growth</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="center reveal" style="max-width:640px;margin-bottom:3rem">
      <p class="eyebrow">Sectors we know</p>
      <h2>Practical, hands-on experience across complex and fast-moving industries.</h2>
    </div>
    <div class="grid grid--4 reveal">
      <div class="tile"><h3>Health Care</h3><p>Clinical systems &amp; regulated care delivery</p></div>
      <div class="tile"><h3>Fintech</h3><p>Financial platforms &amp; payments</p></div>
      <div class="tile"><h3>PropTech</h3><p>Property &amp; real estate technology</p></div>
      <div class="tile"><h3>EduTech</h3><p>Learning platforms &amp; education delivery</p></div>
      <div class="tile"><h3>E-commerce</h3><p>Retail, marketplace &amp; digital commerce</p></div>
      <div class="tile"><h3>Services</h3><p>Professional &amp; business services</p></div>
      <div class="tile"><h3>Automation &amp; AI</h3><p>Workflow automation &amp; applied AI</p></div>
      <div class="tile"><h3>Compliance</h3><p>Regulatory &amp; risk-driven builds</p></div>
    </div>
    <div class="center" style="margin-top:2.5rem">
      <a class="link-arrow" href="sectors.html">Sector detail</a>
    </div>
  </div>
</section>

<section class="section section--warm-deep">
  <div class="shell">
    <div class="split reveal">
      <div>
        <p class="eyebrow">Why Sinaa</p>
        <h2>Built by the team that designed it.</h2>
        <p class="lead">The people who write the strategy also build and run the
          technology behind it — and stand behind the numbers when the raise goes out.</p>
        <p style="margin-top:1.5rem"><a class="link-arrow" href="why-sinaa.html">The full case</a></p>
      </div>
      <div class="grid grid--2">
        <div class="card--flat">
          <h3>One partner, no hand-offs</h3>
          <p>Strategy, execution and capital sit under one roof — not three vendors passing a file.</p>
        </div>
        <div class="card--flat">
          <h3>Comfortable with complexity</h3>
          <p>Experience across clinical, compliance-heavy and operationally intricate businesses.</p>
        </div>
        <div class="card--flat">
          <h3>Capital grounded in operating reality</h3>
          <p>Raise support built on a real diagnostic and data room — not just a pitch deck.</p>
        </div>
        <div class="card--flat">
          <h3>Aligned on the outcome</h3>
          <p>Raise mandates carry a success fee. We are paid when the round closes, not before.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="shell">
    <div class="split reveal">
      <div>
        <p class="eyebrow">Not sure where to start?</p>
        <h2>Two minutes to a straight answer.</h2>
      </div>
      <div class="stack">
        <p>The Growth Readiness Scan asks six questions about your operating model,
          your data, your delivery capacity and your funding position — and tells you
          which pillar to start with, and why.</p>
        <div class="btn-row">
          <a class="btn btn--dark" href="readiness.html">Take the scan</a>
          <a class="btn btn--ghost" href="engagement.html">See engagement models</a>
        </div>
      </div>
    </div>
  </div>
</section>
""" + cta(
        "Let&rsquo;s start with a conversation.",
        "An intro call to align on priorities and where you are today. If it is a fit, "
        "we come back with a tailored scoping proposal and clear deliverables.",
        ("contact.html", "Schedule a call"),
        ("solutions.html", "Explore the offer"),
    ),
)

# ==========================================================================
# Solutions overview
# ==========================================================================
PAGES["solutions.html"] = dict(
    title="Solutions — Sinaa Partners",
    desc="Three pillars: Strategy & Consultancy, Services & Technology, and Capital. "
         "Each stands alone; together they form one continuous growth engagement.",
    main=page_hero(
        "Our offer",
        "Three pillars. Take one, or take the journey.",
        "Deep-dive diagnostics. End-to-end technology and managed operations. "
        "And the go-to-market that raises the capital to fund what comes next.") + """
<section class="section">
  <div class="shell">
    <div class="grid grid--2 reveal" style="gap:2.5rem">
      <a class="card card--pillar" href="strategy.html">
        <span class="card__num">PILLAR 01</span>
        <h3>Strategy &amp; Consultancy</h3>
        <p>A full diagnostic deep-dive into operations, financials, organization and
          market position — then a prioritized roadmap the board can act on.</p>
        <ul class="ticks" style="gap:.6rem;font-size:var(--t-small)">
          <li>Deep-dive business diagnostics</li>
          <li>Root-cause analysis of performance gaps</li>
          <li>Target operating model &amp; organization design</li>
          <li>Board- and investor-ready recommendations</li>
        </ul>
        <span class="link-arrow">Explore Strategy</span>
      </a>
      <a class="card card--pillar" href="technology.html">
        <span class="card__num">PILLAR 02</span>
        <h3>Services &amp; Technology — Build</h3>
        <p>End-to-end technology delivery, from product and platform strategy through
          architecture, build, integration and ongoing improvement.</p>
        <ul class="ticks" style="gap:.6rem;font-size:var(--t-small)">
          <li>Product &amp; platform strategy</li>
          <li>Architecture &amp; solution design</li>
          <li>Build, integration &amp; deployment</li>
          <li>Clinical, compliance and automation verticals</li>
        </ul>
        <span class="link-arrow">Explore Technology</span>
      </a>
      <a class="card card--pillar" href="managed-operations.html">
        <span class="card__num">PILLAR 02</span>
        <h3>Services — Managed Operations</h3>
        <p>Fully managed or co-sourced operations across the functions that keep a
          business running, so the leadership team can focus on growth.</p>
        <ul class="ticks" style="gap:.6rem;font-size:var(--t-small)">
          <li>Finance — accounting, reporting, FP&amp;A</li>
          <li>HR — recruiting, payroll, people ops</li>
          <li>Marketing and sales support</li>
          <li>Scheduling, data &amp; document admin</li>
        </ul>
        <span class="link-arrow">Explore Managed Operations</span>
      </a>
      <a class="card card--pillar" href="capital.html">
        <span class="card__num">PILLAR 03</span>
        <h3>Capital</h3>
        <p>Investment-readiness, the equity story, the model and data room, and a
          targeted investor process run through to close.</p>
        <ul class="ticks" style="gap:.6rem;font-size:var(--t-small)">
          <li>Investment-readiness assessment</li>
          <li>Equity story &amp; narrative development</li>
          <li>Financial model &amp; data room preparation</li>
          <li>Process management through to close</li>
        </ul>
        <span class="link-arrow">Explore Capital</span>
      </a>
    </div>
  </div>
</section>

<section class="section section--warm">
  <div class="shell">
    <div class="center reveal" style="max-width:620px;margin-bottom:3rem">
      <p class="eyebrow">Choosing a starting point</p>
      <h2>Where most engagements begin</h2>
    </div>
    <div class="table-wrap reveal">
      <table>
        <caption class="vh">Which pillar to start with, by situation</caption>
        <thead>
          <tr><th scope="col">If this sounds like you</th><th scope="col">Start with</th><th scope="col">Typical shape</th></tr>
        </thead>
        <tbody>
          <tr>
            <th scope="row">Performance is drifting and the cause is contested</th>
            <td>Strategy &amp; Consultancy</td>
            <td>6&ndash;10 week diagnostic, board-ready roadmap</td>
          </tr>
          <tr>
            <th scope="row">The plan is clear but delivery capacity is the constraint</th>
            <td>Services &amp; Technology</td>
            <td>Fixed-scope build, then ongoing support</td>
          </tr>
          <tr>
            <th scope="row">The back office is consuming the leadership team</th>
            <td>Managed Operations</td>
            <td>Managed or co-sourced service, monthly</td>
          </tr>
          <tr>
            <th scope="row">The business is performing and needs to fund the next stage</th>
            <td>Capital</td>
            <td>Retainer plus success fee to close</td>
          </tr>
          <tr>
            <th scope="row">All of the above, and the clock is running</th>
            <td>Integrated mandate</td>
            <td>Diagnostic into build into raise</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="center" style="margin-top:2.5rem">
      <a class="btn btn--dark" href="readiness.html">Take the Growth Readiness Scan</a>
    </div>
  </div>
</section>
""" + cta("Tell us where you are today.",
          "One call is usually enough to work out which pillar earns its keep first."),
)

# ==========================================================================
# Pillar 01 — Strategy
# ==========================================================================
PAGES["strategy.html"] = dict(
    title="Strategy & Consultancy — Sinaa Partners",
    desc="A full diagnostic deep-dive into operations, financials, organization and "
         "market position, ending in a prioritized roadmap and board-ready recommendations.",
    main=page_hero(
        "Pillar 01",
        "Strategy &amp; Consultancy",
        "Find out what is actually happening inside the business — then decide what to "
        "do about it, in an order the board can defend.") + """
<section class="section">
  <div class="shell">
    <div class="split reveal">
      <div class="sticky">
        <p class="eyebrow">What we do</p>
        <h2>A diagnostic, not an opinion.</h2>
        <p>We go into the business rather than around it: the operating data, the
          financials, the org chart as it really works, and the market position as
          customers experience it.</p>
      </div>
      <ul class="ticks">
        <li>Full diagnostic deep-dive into the business — operations, financials,
          organization, and market position</li>
        <li>Root-cause analysis of performance gaps, separating symptom from cause</li>
        <li>Strategic roadmap with prioritized initiatives, sequenced by value and
          feasibility</li>
        <li>Target operating model and organization design</li>
        <li>Board- and investor-ready recommendations, written to survive scrutiny</li>
      </ul>
    </div>
  </div>
</section>

<section class="section section--warm">
  <div class="shell">
    <div class="center reveal" style="max-width:600px;margin-bottom:3rem">
      <p class="eyebrow">How we engage</p>
      <h2>Four steps, one deliverable that gets used.</h2>
    </div>
    <ol class="steps steps--row reveal">
      <li><h3>Discover</h3><p>Data, systems, interviews. Understand the business as it
        runs today, not as the org chart describes it.</p></li>
      <li><h3>Diagnose</h3><p>Root-cause analysis across performance, cost, capability
        and market position.</p></li>
      <li><h3>Design</h3><p>Target operating model, organization design, and the
        initiatives that close the gap.</p></li>
      <li><h3>Roadmap</h3><p>Sequenced, costed and owned — with the board pack that
        gets it approved.</p></li>
    </ol>
  </div>
</section>

<section class="section section--dark on-dark">
  <div class="shell">
    <div class="split reveal">
      <div>
        <p class="eyebrow">What happens next</p>
        <h2>The roadmap is not the end of the engagement.</h2>
      </div>
      <div class="stack">
        <p class="pull">Most strategy work dies on the shelf because the people who
          wrote it cannot build it.</p>
        <p>Ours does not have to. The same team can pick up the roadmap and deliver it
          &mdash; as a technology build, as a managed operations layer, or both. And when
          the numbers support it, the same diagnostic becomes the evidence base for a
          raise.</p>
        <div class="btn-row" style="margin-top:1.5rem">
          <a class="btn btn--primary" href="technology.html">Pillar 02 — Build &amp; Run</a>
          <a class="btn btn--ghost" href="capital.html">Pillar 03 — Capital</a>
        </div>
      </div>
    </div>
  </div>
</section>
""" + cta("Start with a diagnostic.",
          "We will scope a deep-dive against your priorities, with clear deliverables "
          "and a fixed timeline, before any work begins.",
          ("contact.html", "Scope a diagnostic"),
          ("approach.html", "How the pillars connect")),
)

# ==========================================================================
# Pillar 02 — Technology build
# ==========================================================================
PAGES["technology.html"] = dict(
    title="Services & Technology — Sinaa Partners",
    desc="End-to-end technology delivery: product and platform strategy, architecture, "
         "build, integration and deployment, with specialist clinical, compliance and "
         "automation practices.",
    main=page_hero(
        "Pillar 02",
        "Services &amp; Technology — Build",
        "End-to-end technology delivery. Strategy through architecture, build and "
        "integration, into deployment and continuous improvement.") + """
<section class="section">
  <div class="shell">
    <div class="split reveal">
      <div class="sticky">
        <p class="eyebrow">End-to-end delivery</p>
        <h2>The team that designs it is the team that ships it.</h2>
        <p>No hand-off between the people who set the direction and the people who
          write the code. One accountable team from platform strategy to run.</p>
      </div>
      <ul class="ticks">
        <li>Product &amp; platform strategy — what to build, for whom, and in what order</li>
        <li>Architecture &amp; solution design, including integration into what already exists</li>
        <li>Build, integration &amp; deployment against a defined scope and plan</li>
        <li>Ongoing support &amp; continuous improvement once it is live</li>
      </ul>
    </div>
  </div>
</section>

<section class="section section--warm">
  <div class="shell">
    <div class="center reveal" style="max-width:620px;margin-bottom:3rem">
      <p class="eyebrow">Specialist vertical offers</p>
      <h2>Where the build is harder than the code.</h2>
      <p>Three practices for domains where regulation, clinical risk or process
        complexity decide whether a platform actually lands.</p>
    </div>
    <div class="grid grid--3 reveal">
      <div class="card">
        <div class="card__rule"></div>
        <h3>Clinical</h3>
        <p>Clinical systems and workflow technology, built for the realities of
          regulated care delivery — safety, auditability, and clinicians who will not
          use a tool that slows them down.</p>
      </div>
      <div class="card">
        <div class="card__rule"></div>
        <h3>Compliance</h3>
        <p>Regulatory and risk-driven builds where the control environment is part of
          the requirement, not a document written afterwards.</p>
      </div>
      <div class="card">
        <div class="card__rule"></div>
        <h3>Automation</h3>
        <p>Workflow and process automation — including applied AI where it removes real
          cost, and not where it only adds surface area.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="split reveal">
      <div>
        <p class="eyebrow">Build, then run</p>
        <h2>Shipping is the halfway point.</h2>
      </div>
      <div class="stack">
        <p>A platform that nobody operates is a cost line. Most of our build engagements
          continue into a run relationship — support and continuous improvement on the
          technology, and often a managed operations layer around the business
          processes it serves.</p>
        <p><a class="link-arrow" href="managed-operations.html">Managed Operations (BPO)</a></p>
      </div>
    </div>
  </div>
</section>
""" + cta("Scope a build.",
          "Bring us a roadmap, a problem, or a platform that has stalled. We will come "
          "back with a defined scope, a plan and a fixed set of deliverables.",
          ("contact.html", "Scope a build"),
          ("sectors.html", "Sectors we know")),
)

# ==========================================================================
# Pillar 02 — Managed operations
# ==========================================================================
PAGES["managed-operations.html"] = dict(
    title="Managed Operations (BPO) — Sinaa Partners",
    desc="Fully managed or co-sourced operations across finance, HR, marketing, sales "
         "and admin — run the back office so the leadership team can focus on growth.",
    main=page_hero(
        "Pillar 02",
        "Managed Operations (BPO)",
        "Run the back office so you can focus on growth. Fully managed or co-sourced "
        "operations across the functions that keep a business running.") + """
<section class="section">
  <div class="shell">
    <div class="center reveal" style="max-width:620px;margin-bottom:3rem">
      <p class="eyebrow">Functions we run</p>
      <h2>Five functions, one accountable service.</h2>
    </div>
    <div class="grid grid--3 reveal">
      <div class="card"><div class="card__rule"></div><h3>Finance</h3>
        <p>Accounting, reporting, FP&amp;A — a clean monthly close and numbers a board
          can rely on.</p></div>
      <div class="card"><div class="card__rule"></div><h3>HR</h3>
        <p>Recruiting, payroll and people operations, run to process rather than to
          whoever has time.</p></div>
      <div class="card"><div class="card__rule"></div><h3>Marketing</h3>
        <p>Content, campaigns and brand — consistent output without a standing in-house
          team.</p></div>
      <div class="card"><div class="card__rule"></div><h3>Sales</h3>
        <p>Pipeline, outreach and deal support that keeps the top of the funnel moving.</p></div>
      <div class="card"><div class="card__rule"></div><h3>Admin</h3>
        <p>Scheduling, data and document administration — the work that quietly absorbs
          senior time.</p></div>
      <div class="card card--dark"><div class="card__rule"></div><h3>Or a blend</h3>
        <p>Most clients start with one function and add others as the model proves out.
          Co-sourcing keeps your team in control of what matters.</p></div>
    </div>
  </div>
</section>

<section class="section section--warm-deep">
  <div class="shell">
    <div class="split reveal">
      <div class="sticky">
        <p class="eyebrow">Two models</p>
        <h2>Fully managed, or co-sourced.</h2>
        <p>The choice is about control, not cost. We will tell you which one your
          situation calls for.</p>
      </div>
      <div class="grid grid--2">
        <div class="card">
          <h3>Fully managed</h3>
          <p>We own the function end to end against agreed service levels. Best where
            the function is a distraction rather than a differentiator.</p>
        </div>
        <div class="card">
          <h3>Co-sourced</h3>
          <p>Your team keeps ownership and judgement; we supply capacity, process and
            tooling underneath. Best where domain knowledge has to stay in-house.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--dark on-dark">
  <div class="shell">
    <div class="split reveal">
      <div>
        <p class="eyebrow">Why it matters at the raise</p>
        <h2>Clean operations are diligence evidence.</h2>
      </div>
      <div class="stack">
        <p class="pull">A reliable monthly close is worth more in a data room than any
          slide about operational excellence.</p>
        <p>Running the back office properly is not only a cost story. It produces the
          reporting discipline, the audit trail and the management information that a
          capital process depends on — which is why so many of our raise mandates start
          from an operations engagement.</p>
        <p><a class="link-arrow" href="capital.html">Pillar 03 — Capital</a></p>
      </div>
    </div>
  </div>
</section>
""" + cta("Hand over the work that is not yours to do.",
          "We will map the functions, the current cost and the service levels, then "
          "propose a managed or co-sourced model against them.",
          ("contact.html", "Discuss managed operations"),
          ("engagement.html", "Engagement models")),
)

# ==========================================================================
# Pillar 03 — Capital
# ==========================================================================
PAGES["capital.html"] = dict(
    title="Capital — Sinaa Partners",
    desc="Go-to-market to raise the capital that funds growth: investment-readiness, "
         "equity story, financial model and data room, investor targeting, and process "
         "management through to close.",
    main=page_hero(
        "Pillar 03",
        "Capital",
        "Go-to-market to raise the capital that funds growth — grounded in a diagnostic, "
        "not just a deck.") + """
<section class="section">
  <div class="shell">
    <div class="split reveal">
      <div class="sticky">
        <p class="eyebrow">What we do</p>
        <h2>From readiness to close.</h2>
        <p>We run the raise as a process with a critical path, not as a series of
          introductions.</p>
      </div>
      <ul class="ticks">
        <li>Investment-readiness assessment — an honest read on whether the business is
          fundable today, and what would make it so</li>
        <li>Equity story &amp; narrative development, built from the operating facts</li>
        <li>Financial model &amp; data room preparation that will survive diligence</li>
        <li>Investor targeting &amp; outreach strategy — the right investors, in the right
          order, with the right ask</li>
        <li>Process management through to close, including diligence coordination</li>
      </ul>
    </div>
  </div>
</section>

<section class="section section--warm">
  <div class="shell">
    <div class="split reveal">
      <div>
        <p class="eyebrow">The difference</p>
        <h2>The raise is grounded in a diagnostic, not just a deck.</h2>
      </div>
      <div class="stack">
        <p class="lead">Capital works standalone. But it follows directly from a
          Strategy &amp; Consultancy engagement — which means the equity story is built on
          work we did inside the business, and the data room is populated from
          operations we understand.</p>
        <p>That changes what happens in diligence. When an investor pushes on a number,
          the answer is not a follow-up email; it is a line we already traced to its
          source during the diagnostic.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="center reveal" style="max-width:600px;margin-bottom:3rem">
      <p class="eyebrow">The process</p>
      <h2>How a mandate runs</h2>
    </div>
    <ol class="steps steps--row reveal">
      <li><h3>Readiness</h3><p>Assess fundability, close the gaps that would stall a
        process before it starts.</p></li>
      <li><h3>Story &amp; materials</h3><p>Equity narrative, model, and a data room built
        to answer questions before they are asked.</p></li>
      <li><h3>Go to market</h3><p>Targeted outreach to a mapped investor set, managed as
        a live pipeline.</p></li>
      <li><h3>Diligence to close</h3><p>Coordinate the process, hold the timetable, and
        get to signature.</p></li>
    </ol>
  </div>
</section>

<section class="section section--dark on-dark">
  <div class="shell">
    <div class="split reveal">
      <div>
        <p class="eyebrow">Commercials</p>
        <h2>Aligned from kickoff to close.</h2>
      </div>
      <div class="stack">
        <p>Capital raise engagements are structured as a retainer plus a success fee
          tied to a completed raise. The retainer funds the work that makes a business
          fundable; the success fee means we are paid properly only when the round
          closes.</p>
        <p><a class="link-arrow" href="engagement.html">All engagement models</a></p>
      </div>
    </div>
  </div>
</section>
""" + cta("Find out if you are fundable today.",
          "A readiness assessment gives you a straight answer, and a list of what would "
          "have to change before going to market.",
          ("contact.html", "Request a readiness assessment"),
          ("investors.html", "For investors")),
)

# ==========================================================================
# Sectors
# ==========================================================================
PAGES["sectors.html"] = dict(
    title="Sectors — Sinaa Partners",
    desc="Practical, hands-on experience across health care, fintech, proptech, edutech, "
         "e-commerce, professional services, automation & AI, and compliance-driven builds.",
    main=page_hero(
        "Sectors we know",
        "Practical, hands-on experience across complex and fast-moving industries.",
        "We do not claim every sector. These are the ones where we have built, run and "
        "financed real businesses — and where the complexity is the point.") + """
<section class="section">
  <div class="shell">
    <div class="grid grid--2 reveal" style="gap:2rem">
      <div class="card"><span class="card__num">01</span><h3>Health Care</h3>
        <p>Clinical systems and regulated care delivery. Safety, information governance
          and clinical workflow are design constraints from the first sprint, not a
          compliance review at the end.</p></div>
      <div class="card"><span class="card__num">02</span><h3>Fintech</h3>
        <p>Financial platforms and payments, where reconciliation, resilience and the
          regulatory perimeter decide what can actually ship.</p></div>
      <div class="card"><span class="card__num">03</span><h3>PropTech</h3>
        <p>Property and real estate technology — transaction-heavy workflows joining
          fragmented data across parties who do not share systems.</p></div>
      <div class="card"><span class="card__num">04</span><h3>EduTech</h3>
        <p>Learning platforms and education delivery, built for outcomes and engagement
          rather than feature count.</p></div>
      <div class="card"><span class="card__num">05</span><h3>E-commerce</h3>
        <p>Retail, marketplace and digital commerce, where unit economics and
          operational throughput matter more than the storefront.</p></div>
      <div class="card"><span class="card__num">06</span><h3>Services</h3>
        <p>Professional and business services — people-led businesses that need to
          productize, systematize and scale without losing margin.</p></div>
      <div class="card"><span class="card__num">07</span><h3>Automation &amp; AI</h3>
        <p>Workflow automation and applied AI, deployed where it removes measurable
          cost or cycle time.</p></div>
      <div class="card"><span class="card__num">08</span><h3>Compliance</h3>
        <p>Regulatory and risk-driven builds where the control environment is part of
          the product.</p></div>
    </div>
  </div>
</section>

<section class="section section--warm">
  <div class="shell">
    <div class="split reveal">
      <div>
        <p class="eyebrow">The common thread</p>
        <h2>Regulated, operationally intricate, and mid-transition.</h2>
      </div>
      <div class="stack">
        <p class="lead">What these sectors share is not a technology stack. It is that
          the business model, the operating reality and the regulatory environment are
          entangled — so a plan that ignores any one of the three fails.</p>
        <p>That is the case for a partner who diagnoses, builds and finances rather
          than one who only advises.</p>
        <p><a class="link-arrow" href="why-sinaa.html">Why Sinaa</a></p>
      </div>
    </div>
  </div>
</section>
""" + cta("Working in one of these sectors?",
          "Tell us the situation. We will tell you honestly whether we are the right "
          "partner for it."),
)

# ==========================================================================
# Approach — how it fits together
# ==========================================================================
PAGES["approach.html"] = dict(
    title="Approach — Sinaa Partners",
    desc="Three offers, one growth journey. How diagnosis, build-and-run and capital "
         "compound into a single continuous engagement.",
    main=page_hero(
        "How it fits together",
        "Three offers. One growth journey.",
        "Each offer stands alone. Together, they form a single continuous engagement — "
        "and each cycle funds the next.") + """
<section class="section">
  <div class="shell">
    <div class="loop reveal">
      <div class="card card--pillar">
        <span class="card__num">01</span><h3>Strategy</h3>
        <p>Diagnose &amp; plan. Understand the business as it runs, find the root cause,
          and sequence the fix.</p>
        <a class="link-arrow" href="strategy.html">Pillar 01</a>
      </div>
      <div class="loop__arrow" aria-hidden="true">→</div>
      <div class="card card--pillar">
        <span class="card__num">02</span><h3>Build &amp; Run</h3>
        <p>Technology &amp; operations. Deliver the platform and run the functions that
          turn a plan into performance.</p>
        <a class="link-arrow" href="technology.html">Pillar 02</a>
      </div>
      <div class="loop__arrow" aria-hidden="true">→</div>
      <div class="card card--pillar">
        <span class="card__num">03</span><h3>Capital</h3>
        <p>Fund the next stage. Take a real operating story to a mapped investor set and
          run it to close.</p>
        <a class="link-arrow" href="capital.html">Pillar 03</a>
      </div>
    </div>
    <p class="loop__note reveal" style="color:var(--gold-text);border-color:var(--rule-strong)">
      ↻ Capital raised funds the next cycle of strategy and growth</p>
  </div>
</section>

<section class="section section--dark on-dark">
  <div class="shell">
    <div class="split reveal">
      <div class="sticky">
        <p class="eyebrow">Why it compounds</p>
        <h2>Each pillar makes the next one cheaper.</h2>
      </div>
      <div>
        <ul class="facts">
          <li><b>Diagnostic → build</b><span>The scope is already written. There is no
            discovery phase to pay for twice, and no argument about what the plan
            actually said.</span></li>
          <li><b>Build → operations</b><span>The team that built the platform runs the
            processes on top of it, so the operating model and the technology stay in
            step.</span></li>
          <li><b>Operations → capital</b><span>Clean reporting and a real audit trail
            populate the data room. Diligence questions get answered from the source,
            not reconstructed.</span></li>
          <li><b>Capital → strategy</b><span>The raise funds the next cycle of growth —
            and the diagnostic that shapes it.</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section section--warm">
  <div class="shell">
    <div class="center reveal" style="max-width:620px;margin-bottom:3rem">
      <p class="eyebrow">Getting started</p>
      <h2>Let&rsquo;s start with a conversation.</h2>
      <p>Three steps from first contact to work beginning. No procurement theatre.</p>
    </div>
    <ol class="steps steps--3 reveal">
      <li><h3>Intro call</h3><p>Align on priorities and where you are today. Thirty
        minutes, no materials required.</p></li>
      <li><h3>Scoping proposal</h3><p>A tailored diagnostic or project scope, with clear
        deliverables, timeline and price.</p></li>
      <li><h3>Kick off</h3><p>Begin the engagement — standalone, or across pillars as
        one mandate.</p></li>
    </ol>
    <div class="center" style="margin-top:2.5rem">
      <a class="btn btn--dark" href="contact.html">Book the intro call</a>
    </div>
  </div>
</section>
""" + cta("One partner, from diagnosis to close.",
          "Take one pillar, or take the journey. The entry point is the same conversation."),
)

# ==========================================================================
# Engagement models
# ==========================================================================
PAGES["engagement.html"] = dict(
    title="Engagement models — Sinaa Partners",
    desc="Four ways to work with Sinaa Partners: advisory retainer, project-based build, "
         "managed service, and capital raise engagement.",
    main=page_hero(
        "Engagement models",
        "Ways to work with us",
        "Four commercial shapes, chosen to match the work rather than the other way "
        "round. Most clients combine two of them.") + """
<section class="section">
  <div class="shell">
    <div class="grid grid--2 reveal" style="gap:2rem">
      <div class="card card--pillar">
        <span class="card__num">MODEL 01</span>
        <h3>Advisory Retainer</h3>
        <p>Ongoing strategic advisory access — ideal for management teams navigating an
          active growth phase, where the questions arrive faster than a project can
          answer them.</p>
        <ul class="ticks" style="gap:.6rem;font-size:var(--t-small)">
          <li>Monthly fee, defined access and cadence</li>
          <li>Board and leadership support</li>
          <li>Rolling term, reviewed quarterly</li>
        </ul>
      </div>
      <div class="card card--pillar">
        <span class="card__num">MODEL 02</span>
        <h3>Project-Based Build</h3>
        <p>Defined-scope technology or transformation build, delivered start to finish
          against a fixed plan with clear deliverables and acceptance.</p>
        <ul class="ticks" style="gap:.6rem;font-size:var(--t-small)">
          <li>Fixed scope, timeline and price</li>
          <li>Named delivery team</li>
          <li>Optional support and improvement tail</li>
        </ul>
      </div>
      <div class="card card--pillar">
        <span class="card__num">MODEL 03</span>
        <h3>Managed Service (BPO)</h3>
        <p>Ongoing outsourced or co-sourced operations across finance, HR, marketing,
          sales or admin — run against agreed service levels.</p>
        <ul class="ticks" style="gap:.6rem;font-size:var(--t-small)">
          <li>Monthly service fee by function and volume</li>
          <li>Fully managed or co-sourced</li>
          <li>Scales up and down with the business</li>
        </ul>
      </div>
      <div class="card card--pillar">
        <span class="card__num">MODEL 04</span>
        <h3>Capital Raise Engagement</h3>
        <p>Retainer plus success fee tied to a completed raise — aligned incentives from
          kickoff to close.</p>
        <ul class="ticks" style="gap:.6rem;font-size:var(--t-small)">
          <li>Retainer funds readiness and materials</li>
          <li>Success fee on completion</li>
          <li>Exclusive mandate for a defined period</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section section--warm">
  <div class="shell">
    <div class="split reveal">
      <div>
        <p class="eyebrow">Combining models</p>
        <h2>The common combination</h2>
      </div>
      <div class="stack">
        <p class="lead">A diagnostic under an advisory retainer, a project-based build
          to deliver the roadmap, a managed service to run what it produces, and a raise
          mandate when the numbers are ready to be shown.</p>
        <p>Each step is a separate decision with its own commercial. Nothing is bundled
          to force the next one.</p>
        <p><a class="link-arrow" href="approach.html">See how the pillars connect</a></p>
      </div>
    </div>
  </div>
</section>
""" + cta("Which model fits your situation?",
          "Tell us the problem and the timeline. We will propose the commercial shape "
          "that suits it, and say so if none of ours does."),
)

# ==========================================================================
# For investors  — ADDED (not in the deck; the deck names capital partners as
# an audience but gives them no route through the material)
# ==========================================================================
PAGES["investors.html"] = dict(
    title="For Investors — Sinaa Partners",
    desc="An operating partner for capital partners: commercial and operational "
         "diligence, value-creation planning, portfolio build and run capacity, and "
         "exit readiness.",
    main=page_hero(
        "For capital partners",
        "An operating partner, not another adviser.",
        "You are assessing where value can be created — before the deal, and every "
        "quarter after it. We work the same three pillars from your side of the table.") + """
<section class="section">
  <div class="shell">
    <div class="split reveal">
      <div class="sticky">
        <p class="eyebrow">The problem we solve</p>
        <h2>The value-creation plan and the people who can execute it are rarely the same firm.</h2>
      </div>
      <div class="stack">
        <p class="lead">A diligence provider hands you a thesis. A systems integrator
          hands you a quote. Neither is accountable for whether the plan survives contact
          with the asset.</p>
        <p>We are. The team that writes the operational thesis is the team that can be
          deployed into the portfolio company to deliver it — as a build, as a managed
          operations layer, or as interim capability while a permanent team is hired.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--warm">
  <div class="shell">
    <div class="center reveal" style="max-width:620px;margin-bottom:3rem">
      <p class="eyebrow">Across the hold period</p>
      <h2>Where we plug in</h2>
    </div>
    <div class="grid grid--4 reveal">
      <div class="card"><span class="card__num">PRE-DEAL</span><div class="card__rule"></div>
        <h3>Commercial &amp; operational diligence</h3>
        <p>An operator&rsquo;s read on the target: whether the operating model can carry the
          plan, what the technology estate really costs, and where the execution risk
          sits.</p></div>
      <div class="card"><span class="card__num">DAY 1&ndash;100</span><div class="card__rule"></div>
        <h3>Value-creation planning</h3>
        <p>A diagnostic converted into a sequenced, costed and owned initiative
          roadmap — with a target operating model attached to it.</p></div>
      <div class="card"><span class="card__num">HOLD</span><div class="card__rule"></div>
        <h3>Portfolio build &amp; run</h3>
        <p>Delivery capacity for platform builds, integrations after a bolt-on, and
          managed back-office operations across a portfolio rather than one asset at a
          time.</p></div>
      <div class="card"><span class="card__num">EXIT</span><div class="card__rule"></div>
        <h3>Exit readiness</h3>
        <p>Equity story, model and data room built from operating evidence we helped
          produce — so diligence confirms the story instead of testing it.</p></div>
    </div>
  </div>
</section>

<section class="section section--dark on-dark">
  <div class="shell">
    <div class="split reveal">
      <div>
        <p class="eyebrow">How we work with funds</p>
        <h2>Three ways in.</h2>
      </div>
      <div>
        <ul class="facts">
          <li><b>Deal-by-deal</b><span>Scoped diligence or a single portfolio company
            engagement, priced as a project.</span></li>
          <li><b>Portfolio framework</b><span>A standing agreement with pre-agreed rates
            and a named team, drawn down across assets as needed.</span></li>
          <li><b>Operating partner</b><span>A retained relationship at fund level —
            involved in screening, then deployed where the thesis needs execution.</span></li>
        </ul>
        <p style="margin-top:2rem"><a class="link-arrow" href="engagement.html">Engagement models in detail</a></p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="center reveal" style="max-width:640px">
      <p class="eyebrow">A note on evidence</p>
      <h2>We would rather show you the work than the logos.</h2>
      <p>Reference calls with management teams we have worked with, and a walkthrough of
        an anonymised diagnostic and data room, are available under NDA. Ask on the
        intro call.</p>
    </div>
  </div>
</section>
""" + cta("Assessing an asset, or a portfolio?",
          "We will tell you within one call whether we have seen the situation before, "
          "and what we would want to look at first.",
          ("contact.html", "Talk to us"),
          ("capital.html", "Pillar 03 — Capital")),
)

# ==========================================================================
# Why Sinaa
# ==========================================================================
PAGES["why-sinaa.html"] = dict(
    title="Why Sinaa Partners",
    desc="One partner and no hand-offs. Built by the team that designed it. Comfortable "
         "with complexity. Capital grounded in operating reality.",
    main=page_hero(
        "Why us",
        "Why Sinaa Partners",
        "Four reasons, and each of them is a structural choice rather than a claim about "
        "effort.") + """
<section class="section">
  <div class="shell">
    <div class="grid grid--2 reveal" style="gap:2.5rem">
      <div class="card"><span class="card__num">01</span><div class="card__rule"></div>
        <h3>One partner, no hand-offs</h3>
        <p>Strategy, execution and capital sit under one roof — not three vendors passing
          a file. Nobody gets to blame the previous firm&rsquo;s work, because there is no
          previous firm.</p></div>
      <div class="card"><span class="card__num">02</span><div class="card__rule"></div>
        <h3>Built by the team that designed it</h3>
        <p>The people who write the strategy also build and run the technology behind it.
          That constrains what we recommend: we do not propose what we would not want to
          deliver.</p></div>
      <div class="card"><span class="card__num">03</span><div class="card__rule"></div>
        <h3>Comfortable with complexity</h3>
        <p>Experience across clinical, compliance-heavy and operationally intricate
          businesses — where regulation and workflow decide the outcome long before the
          technology does.</p></div>
      <div class="card"><span class="card__num">04</span><div class="card__rule"></div>
        <h3>Capital grounded in operating reality</h3>
        <p>Raise support built on a real diagnostic and a real data room — not just a
          pitch deck. Diligence tends to confirm the story rather than unpick it.</p></div>
    </div>
  </div>
</section>

<section class="section section--warm-deep">
  <div class="shell">
    <div class="split reveal">
      <div>
        <p class="eyebrow">What this rules out</p>
        <h2>The things we will not do.</h2>
      </div>
      <div>
        <ul class="facts">
          <li><b>No shelf strategy</b><span>We do not take a diagnostic mandate without a
            view on who executes the result.</span></li>
          <li><b>No raise we cannot stand behind</b><span>If the readiness assessment says
            the business is not fundable yet, we say so and propose the work that would
            change it.</span></li>
          <li><b>No sector tourism</b><span>If a situation sits outside the sectors we
            know, we will say that on the first call.</span></li>
          <li><b>No bundling</b><span>Each pillar is a separate commercial decision. One
            engagement never obliges the next.</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>
""" + cta("See whether it holds up.",
          "The fastest test of any of this is a thirty-minute call about a problem you "
          "actually have."),
)

# ==========================================================================
# Growth Readiness Scan — ADDED (lead-qualification flow; the deck has no
# self-serve entry point between "read the offer" and "book a call")
# ==========================================================================
SCAN_QUESTIONS = [
    ("q1", "How well do you understand what is driving current performance?", [
        ("We are working from opinion and anecdote", 0),
        ("We have reporting, but the causes are contested", 1),
        ("We have a clear view on most of the drivers", 2),
        ("Root causes are evidenced and agreed by the board", 3)]),
    ("q2", "How reliable is your management information?", [
        ("The monthly close is late and reworked", 0),
        ("The numbers land, but nobody fully trusts them", 1),
        ("Reliable monthly reporting with some manual effort", 2),
        ("Clean, timely, and traceable to source", 3)]),
    ("q3", "Does your technology estate support the plan?", [
        ("It actively blocks us", 0),
        ("It works, but change takes months", 1),
        ("Broadly fit, with known gaps being addressed", 2),
        ("It is a genuine advantage", 3)]),
    ("q4", "Do you have the delivery capacity to execute?", [
        ("No — everything queues behind the same few people", 0),
        ("Some, but the roadmap is slipping", 1),
        ("Enough for the current plan", 2),
        ("Enough to accelerate if we chose to", 3)]),
    ("q5", "How much senior time goes into back-office operations?", [
        ("It dominates the leadership team&rsquo;s week", 0),
        ("More than it should", 1),
        ("Contained, mostly delegated", 2),
        ("Minimal — it runs without us", 3)]),
    ("q6", "Where are you on funding the next stage?", [
        ("Not thinking about it yet", 0),
        ("We know we will need capital, nothing prepared", 1),
        ("Materials started, investors not yet mapped", 2),
        ("Model, data room and target list are ready", 3)]),
]


def scan_fields():
    out = []
    for name, question, options in SCAN_QUESTIONS:
        choices = "".join(
            '<label class="choice"><input type="radio" name="{n}" value="{v}" required>'
            '<span>{l}</span></label>'.format(n=name, v=v, l=l) for l, v in options)
        out.append(
            '<fieldset><legend>{q}</legend><div class="choices">{c}</div></fieldset>'.format(
                q=question, c=choices))
    return "".join(out)


PAGES["readiness.html"] = dict(
    title="Growth Readiness Scan — Sinaa Partners",
    desc="Six questions, two minutes. Find out which of the three pillars your business "
         "should start with — diagnostic, build and run, or capital.",
    main=page_hero(
        "Growth Readiness Scan",
        "Which pillar should you start with?",
        "Six questions about your operating model, your data, your delivery capacity and "
        "your funding position. Two minutes, no email required, answer stays in your "
        "browser.") + """
<section class="section">
  <div class="shell">
    <div class="split">
      <div class="sticky reveal">
        <p class="eyebrow">How to read it</p>
        <h2>An honest starting point, not a sales qualifier.</h2>
        <p>The scan weighs whether your constraint sits upstream (you do not yet know
          what is wrong), in the middle (you know, but cannot deliver it), or downstream
          (you are performing and need to fund the next stage).</p>
        <p>Nothing is submitted anywhere. If the read-out is useful, bring it to the
          intro call and we will pressure-test it.</p>
      </div>
      <form data-scan novalidate class="reveal">
        """ + scan_fields() + """
        <button type="submit" class="btn btn--primary">Show my read-out</button>

        <div class="scan__result" data-scan-result hidden style="margin-top:2rem">
          <p class="eyebrow" data-scan-band></p>
          <h3 data-scan-headline></h3>
          <div class="meter" role="img" aria-label="Readiness indicator">
            <span class="meter__fill" data-scan-meter></span>
          </div>
          <p data-scan-body></p>
          <div class="btn-row" style="margin-top:1.5rem">
            <a class="btn btn--dark" href="contact.html">Bring this to an intro call</a>
            <a class="btn btn--ghost" href="solutions.html">Compare the pillars</a>
          </div>
        </div>
      </form>
    </div>
  </div>
</section>
""" + cta("Prefer to just talk it through?",
          "A thirty-minute call covers more ground than any questionnaire.",
          ("contact.html", "Book an intro call"),
          ("solutions.html", "See the three pillars")),
)

# ==========================================================================
# Perspectives — ADDED (credibility surface; full positions written inline
# rather than an index of links that do not exist yet)
# ==========================================================================
PAGES["insights.html"] = dict(
    title="Perspectives — Sinaa Partners",
    desc="Where Sinaa Partners stands on diagnostics, build-versus-buy, managed "
         "operations, applied AI, and what actually makes a business fundable.",
    main=page_hero(
        "Perspectives",
        "Where we stand",
        "Positions we hold, stated plainly, because they explain how an engagement with "
        "us will actually run.") + """
<section class="section">
  <div class="shell" style="max-width:820px">
    <article class="card--flat reveal" style="margin-bottom:3.5rem;border-top:0">
      <p class="eyebrow">01 &mdash; Diagnostics</p>
      <h2>Most turnaround plans fail at the diagnosis, not the execution.</h2>
      <p>By the time a management team commissions help, there is usually already a
        theory in the room about what is wrong — and the work quietly becomes an
        exercise in confirming it. The expensive failure is not a badly executed plan.
        It is a well-executed plan aimed at a symptom.</p>
      <p>This is why our diagnostic starts from the operating data rather than the
        leadership interview, and why root-cause analysis is a named deliverable rather
        than an implicit step.</p>
      <p><a class="link-arrow" href="strategy.html">Pillar 01 — Strategy &amp; Consultancy</a></p>
    </article>

    <article class="card--flat reveal" style="margin-bottom:3.5rem">
      <p class="eyebrow">02 &mdash; Delivery</p>
      <h2>The hand-off is where the value leaks.</h2>
      <p>Strategy firm to build partner to raise adviser: three transfers, each one a
        chance for context to be lost and for accountability to become negotiable. Every
        transfer also costs a discovery phase, paid for again.</p>
      <p>Holding all three is not an upsell argument. It removes the two most expensive
        moments in the growth journey.</p>
      <p><a class="link-arrow" href="approach.html">How the pillars connect</a></p>
    </article>

    <article class="card--flat reveal" style="margin-bottom:3.5rem">
      <p class="eyebrow">03 &mdash; Operations</p>
      <h2>Outsourcing is a control decision before it is a cost decision.</h2>
      <p>The question is never simply whether a function is cheaper elsewhere. It is
        whether the judgement inside that function is a source of advantage. Where it is,
        co-source and keep the judgement in-house. Where it is not, hand the whole
        function over and hold it to a service level.</p>
      <p>Getting this backwards — outsourcing the judgement and keeping the
        administration — is the common and expensive mistake.</p>
      <p><a class="link-arrow" href="managed-operations.html">Managed Operations</a></p>
    </article>

    <article class="card--flat reveal" style="margin-bottom:3.5rem">
      <p class="eyebrow">04 &mdash; Applied AI</p>
      <h2>Automate the process you have already fixed.</h2>
      <p>Automation applied to a broken process produces a faster broken process and a
        new integration to maintain. Applied AI is worth deploying where the workflow is
        understood, the data is trustworthy, and the cost or cycle time being removed can
        be measured before and after.</p>
      <p>Everywhere else it is a pilot, and pilots should be priced and timeboxed as
        such.</p>
      <p><a class="link-arrow" href="technology.html">Services &amp; Technology</a></p>
    </article>

    <article class="card--flat reveal" style="margin-bottom:3.5rem">
      <p class="eyebrow">05 &mdash; Capital</p>
      <h2>Fundability is an operating condition, not a document.</h2>
      <p>A raise process exposes the operating model to people paid to find the flaw in
        it. No narrative survives a monthly close that cannot be reconciled, or a metric
        that changes definition between the deck and the data room.</p>
      <p>Which is why our readiness assessment can conclude that a business should not go
        to market yet — and say what would have to change first.</p>
      <p><a class="link-arrow" href="capital.html">Pillar 03 — Capital</a></p>
    </article>

    <article class="card--flat reveal">
      <p class="eyebrow">06 &mdash; Regulated sectors</p>
      <h2>In regulated businesses, compliance is the architecture.</h2>
      <p>Treating the control environment as a review gate at the end of a build is the
        reliable way to discover, late, that the product cannot ship. In clinical and
        compliance-heavy work the regulatory perimeter is a design input alongside the
        user need — it shapes the data model, the audit trail and the release process.</p>
      <p><a class="link-arrow" href="sectors.html">Sectors we know</a></p>
    </article>
  </div>
</section>
""" + cta("Disagree with any of it?",
          "Good. Those conversations tend to be the useful ones.",
          ("contact.html", "Start a conversation"),
          ("why-sinaa.html", "Why Sinaa")),
)

# ==========================================================================
# Contact
# ==========================================================================
PAGES["contact.html"] = dict(
    title="Contact — Sinaa Partners",
    desc="Start with a thirty-minute intro call. Align on priorities, receive a tailored "
         "scoping proposal, then kick off — standalone or across pillars.",
    main=page_hero(
        "Get started",
        "Let&rsquo;s start with a conversation.",
        "Three steps from first contact to work beginning.") + """
<section class="section section--tight">
  <div class="shell">
    <ol class="steps steps--3 reveal">
      <li><h3>Intro call</h3><p>Align on priorities and where you are today. Thirty
        minutes, no materials required.</p></li>
      <li><h3>Scoping proposal</h3><p>A tailored diagnostic or project scope, with clear
        deliverables, timeline and price.</p></li>
      <li><h3>Kick off</h3><p>Begin the engagement — standalone or across pillars.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="split reveal">
      <div class="sticky">
        <p class="eyebrow">Schedule a call</p>
        <h2>Tell us the situation.</h2>
        <p>The more specific the problem, the more useful the first call. If we are not
          the right partner for it, we will say so and point you somewhere better.</p>
        <ul class="facts" style="margin-top:2rem">
          <li><b>Email</b><span><a href="mailto:{email}">{email}</a></span></li>
          <li><b>Phone</b><span>[phone]</span></li>
          <li><b>Contact</b><span>[Name], [title]</span></li>
        </ul>
      </div>

      <form data-contact-form novalidate>
        <div class="field">
          <label for="name">Your name</label>
          <input id="name" name="name" type="text" autocomplete="name" required>
        </div>
        <div class="field">
          <label for="email">Work email</label>
          <input id="email" name="email" type="email" autocomplete="email" required>
        </div>
        <div class="field">
          <label for="company">Company</label>
          <input id="company" name="company" type="text" autocomplete="organization">
        </div>
        <div class="field">
          <label for="role">You are</label>
          <select id="role" name="role">
            <option>Management team</option>
            <option>Founder / owner</option>
            <option>Investor or capital partner</option>
            <option>Board member / NED</option>
            <option>Other</option>
          </select>
        </div>
        <div class="field">
          <label for="interest">What is this about?</label>
          <select id="interest" name="interest">
            <option>Strategy &amp; Consultancy — diagnostic</option>
            <option>Services &amp; Technology — build</option>
            <option>Managed Operations (BPO)</option>
            <option>Capital — raise support</option>
            <option>Investor / portfolio engagement</option>
            <option>Not sure yet</option>
          </select>
        </div>
        <div class="field">
          <label for="message">The situation</label>
          <textarea id="message" name="message" placeholder="Where you are today, and what you would want to be different in twelve months."></textarea>
          <p class="hint" id="message-hint">A few sentences is plenty.</p>
        </div>
        <button type="submit" class="btn btn--primary">Request an intro call</button>
        <p class="hint" data-contact-note hidden style="margin-top:1rem">
          Opening your email client with the details filled in. If nothing happens,
          write to <a href="mailto:{email}">{email}</a>.</p>
      </form>
    </div>
  </div>
</section>
""".format(email=EMAIL) + cta(
        "Assessing an asset rather than running one?",
        "There is a separate route through this for capital partners and boards.",
        ("investors.html", "For investors"),
        ("readiness.html", "Growth Readiness Scan")),
)


# ==========================================================================
# Render
# ==========================================================================
def main():
    for filename, spec in PAGES.items():
        html = SHELL.format(
            title=spec["title"],
            desc=re.sub(r"\s+", " ", spec["desc"]).strip(),
            header=header(filename),
            main=spec["main"],
            footer=FOOTER,
        )
        with open(os.path.join(OUT, filename), "w", encoding="utf-8") as fh:
            fh.write(html)
        print("wrote", filename)
    print(len(PAGES), "pages")


if __name__ == "__main__":
    main()
