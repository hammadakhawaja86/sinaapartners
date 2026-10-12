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
# file. Inlined, not referenced as <img>: inside the header's backdrop-filter
# layer the browser rasterised the file once at its 993px intrinsic width and
# then resampled it down 5.8x to a fractional 171.63px box, which is what made
# the lockup look soft. Inline SVG is drawn as vectors at device resolution
# every time, so it is sharp at any zoom and any DPR.
#
# The light and dark artworks are byte-identical apart from the ink colour, so
# one template serves both: the ink is currentColor and .logo sets it. The
# viewBox is the measured ink box, not the artboard, so no invisible padding
# eats into the rendered height.
#
# Standalone copies of both variants stay in assets/ for favicon and social use.
# --------------------------------------------------------------------------
LOCKUP = "assets/sinaa-lockup.svg"
LOCKUP_ON_DARK = "assets/sinaa-lockup-on-dark.svg"

LOCKUP_SVG = """<svg class="logo__lockup" viewBox="16 9.5 993 277" fill="none" role="img" aria-label="Sinaa Partners" focusable="false" xmlns="http://www.w3.org/2000/svg">
<path d="M937.962 73.7698L898.807 174.682H909.314L944.405 83.1869H962.744L997.835 174.682H1008.34L969.187 73.7698H937.962Z" fill="currentColor"/>
<path d="M772.617 73.7698L733.462 174.682H743.969L779.061 83.1869H797.399L832.49 174.682H842.998L803.842 73.7698H772.617Z" fill="currentColor"/>
<path d="M570 178.746V73.7695H580.706L661.991 165.264V73.7695H672.102V178.746H660.9L580.111 88.5395V178.746H570Z" fill="currentColor"/>
<path d="M492.879 178.746V73.7695H502.99V178.746H492.879Z" fill="currentColor"/>
<path d="M393.455 184.99C385.392 184.99 377.297 183.834 369.168 181.521C361.04 179.142 354.431 176.499 349.343 173.591L353.209 165.561C357.967 168.205 364.014 170.617 371.349 172.798C378.685 174.979 385.921 176.069 393.058 176.069C403.037 176.069 410.901 174.153 416.65 170.32C422.4 166.487 425.275 160.77 425.275 153.171C425.275 146.232 422.499 141.143 416.948 137.905C411.397 134.601 402.938 132.089 391.571 130.371C386.945 129.644 382.947 128.917 379.577 128.19C376.206 127.463 372.373 126.307 368.078 124.721C363.849 123.135 360.379 121.285 357.67 119.17C354.96 117.055 352.647 114.246 350.731 110.744C348.88 107.241 347.955 103.243 347.955 98.7495C347.955 89.1011 351.689 81.6665 359.156 76.4458C366.624 71.159 377.165 68.5156 390.778 68.5156C405.119 68.5156 417.576 71.4895 428.149 77.4371L423.689 85.3673C414.635 80.0805 403.731 77.4371 390.976 77.4371C368.772 77.4371 357.67 84.4752 357.67 98.5513C357.67 100.864 358.099 103.012 358.958 104.995C359.817 106.911 360.842 108.563 362.031 109.951C363.287 111.339 364.972 112.627 367.087 113.817C369.267 115.006 371.25 115.965 373.034 116.692C374.885 117.352 377.198 118.046 379.973 118.773C382.815 119.434 385.095 119.93 386.813 120.26C388.597 120.591 390.877 120.987 393.653 121.45C398.279 122.177 402.343 122.97 405.846 123.829C409.414 124.688 413.115 125.944 416.948 127.596C420.781 129.248 423.92 131.164 426.365 133.345C428.876 135.526 430.925 138.334 432.511 141.771C434.163 145.141 434.989 149.007 434.989 153.369C434.989 163.149 431.222 170.881 423.689 176.565C416.221 182.182 406.143 184.99 393.455 184.99Z" fill="currentColor"/>
<rect x="938.946" y="160.053" width="20.6886" height="20.6886" transform="rotate(-45 938.946 160.053)" fill="#D39000"/>
<path d="M444.64 249.715V206.078H460.194C463.589 206.078 466.402 206.696 468.632 207.932C470.862 209.168 472.531 210.858 473.639 213.003C474.747 215.134 475.301 217.534 475.301 220.205C475.301 222.89 474.74 225.304 473.617 227.449C472.51 229.58 470.833 231.27 468.589 232.52C466.359 233.756 463.554 234.374 460.173 234.374H449.477V228.792H459.576C461.721 228.792 463.461 228.422 464.796 227.684C466.132 226.931 467.112 225.908 467.737 224.615C468.362 223.323 468.674 221.853 468.674 220.205C468.674 218.557 468.362 217.094 467.737 215.816C467.112 214.537 466.125 213.536 464.775 212.811C463.44 212.087 461.679 211.725 459.491 211.725H451.224V249.715H444.64ZM506.076 249.715H499.088L514.791 206.078H522.397L538.1 249.715H531.112L518.775 214.005H518.434L506.076 249.715ZM507.248 232.627H529.919V238.167H507.248V232.627ZM568.402 249.715V206.078H583.956C587.337 206.078 590.142 206.661 592.372 207.826C594.616 208.99 596.293 210.603 597.401 212.662C598.508 214.708 599.062 217.073 599.062 219.757C599.062 222.428 598.501 224.779 597.379 226.81C596.271 228.827 594.595 230.397 592.351 231.519C590.121 232.641 587.315 233.202 583.935 233.202H572.152V227.534H583.338C585.469 227.534 587.202 227.229 588.537 226.618C589.886 226.007 590.874 225.12 591.499 223.955C592.124 222.79 592.436 221.391 592.436 219.757C592.436 218.11 592.116 216.682 591.477 215.475C590.852 214.267 589.865 213.344 588.516 212.705C587.18 212.051 585.426 211.725 583.253 211.725H574.986V249.715H568.402ZM589.943 230.027L600.724 249.715H593.224L582.656 230.027H589.943ZM628.922 211.746V206.078H662.693V211.746H649.078V249.715H642.516V211.746H628.922ZM729.376 206.078V249.715H723.325L701.144 217.712H700.74V249.715H694.156V206.078H700.25L722.451 238.124H722.856V206.078H729.376ZM762.98 249.715V206.078H790.338V211.746H769.564V225.042H788.91V230.688H769.564V244.047H790.594V249.715H762.98ZM823.132 249.715V206.078H838.686C842.067 206.078 844.872 206.661 847.103 207.826C849.347 208.99 851.023 210.603 852.131 212.662C853.239 214.708 853.793 217.073 853.793 219.757C853.793 222.428 853.232 224.779 852.11 226.81C851.002 228.827 849.326 230.397 847.081 231.519C844.851 232.641 842.046 233.202 838.665 233.202H826.882V227.534H838.068C840.199 227.534 841.932 227.229 843.267 226.618C844.617 226.007 845.604 225.12 846.229 223.955C846.854 222.79 847.167 221.391 847.167 219.757C847.167 218.11 846.847 216.682 846.208 215.475C845.583 214.267 844.595 213.344 843.246 212.705C841.911 212.051 840.157 211.725 837.983 211.725H829.716V249.715H823.132ZM844.674 230.027L855.455 249.715H847.955L837.387 230.027H844.674ZM909.604 217.542C909.377 215.525 908.439 213.962 906.792 212.854C905.144 211.732 903.07 211.171 900.57 211.171C898.78 211.171 897.232 211.455 895.925 212.023C894.618 212.577 893.603 213.344 892.878 214.324C892.168 215.29 891.813 216.391 891.813 217.627C891.813 218.664 892.054 219.559 892.537 220.311C893.034 221.064 893.681 221.696 894.476 222.208C895.286 222.705 896.152 223.124 897.076 223.465C897.999 223.792 898.887 224.061 899.739 224.275L904 225.382C905.392 225.723 906.82 226.185 908.283 226.767C909.746 227.35 911.103 228.117 912.353 229.069C913.603 230.02 914.611 231.199 915.378 232.605C916.159 234.012 916.55 235.695 916.55 237.655C916.55 240.127 915.911 242.321 914.632 244.239C913.368 246.157 911.529 247.669 909.114 248.777C906.713 249.885 903.809 250.439 900.399 250.439C897.132 250.439 894.306 249.921 891.919 248.884C889.533 247.847 887.665 246.377 886.316 244.473C884.966 242.556 884.22 240.283 884.078 237.655H890.684C890.811 239.232 891.323 240.546 892.218 241.597C893.127 242.634 894.284 243.408 895.691 243.919C897.111 244.417 898.667 244.665 900.357 244.665C902.218 244.665 903.872 244.374 905.321 243.792C906.784 243.195 907.935 242.371 908.773 241.32C909.611 240.255 910.03 239.012 910.03 237.591C910.03 236.299 909.661 235.24 908.922 234.417C908.198 233.593 907.211 232.911 905.961 232.371C904.725 231.831 903.326 231.355 901.763 230.944L896.607 229.537C893.113 228.586 890.343 227.186 888.297 225.34C886.266 223.493 885.25 221.05 885.25 218.01C885.25 215.496 885.932 213.301 887.296 211.426C888.659 209.551 890.506 208.096 892.836 207.059C895.165 206.007 897.793 205.482 900.719 205.482C903.674 205.482 906.28 206 908.539 207.037C910.811 208.074 912.601 209.502 913.908 211.32C915.215 213.124 915.897 215.198 915.953 217.542H909.604Z" fill="#D39000"/>
<mask id="mask0_{uid}" style="mask-type:alpha" maskUnits="userSpaceOnUse" x="0" y="-1" width="265" height="307">
<path d="M264.62 305.452H105.157L239.305 298.092L135.083 17.4255L100.114 27.2175L105.157 305.452H0V-0.000282288H264.62V305.452Z" fill="#D9D9D9"/>
</mask>
<g mask="url(#mask0_{uid})">
<path d="M194.06 250.131C227.665 227.449 247.416 186.989 241.622 144.089C234.846 93.9058 195.252 56.2123 147.396 49.7196M92.3656 261.335C56.4133 247.211 28.9756 214.55 23.4393 173.553C16.7679 124.149 43.9719 77.9814 87.1999 58.4744" stroke="#D39000" stroke-width="12.9614" stroke-linecap="square"/>
</g>
<g clip-path="url(#clip0_{uid})">
<path d="M126.771 285.398C126.354 285.777 126.001 285.698 125.805 285.594C125.479 285.424 125.348 284.862 125.648 284.51L136.292 272.169C145.146 260.611 151.675 248.101 151.519 233.187C151.362 218.274 144.845 205.658 134.685 195.015L118.44 177.973L95.0768 153.839L90.0229 148.511C85.4913 143.732 81.3385 138.795 78.0606 133.062C72.3276 123.059 70.7214 111.593 73.6727 100.401C76.0626 91.3382 80.5811 83.0978 87.0323 76.294L108.123 54.0542L144.153 18.063L152.367 10.0316L152.563 10.1883L148.058 15.6079L128.234 38.5137C124.525 42.8102 121.025 46.8977 117.578 51.3901C105.224 67.4921 98.6419 88.3215 106.83 107.741C109.546 114.192 113.229 119.964 118.061 125.07L149.494 158.306C156.194 165.384 162.867 172.188 169.031 179.697C172.936 184.463 176.135 189.53 178.225 195.315C180.314 201.101 181.476 207.474 181.059 213.912C180.366 224.673 175.978 234.415 169.031 242.564C163.533 249.015 157.761 254.918 151.832 261.029C143.683 269.426 135.547 277.575 126.784 285.398H126.771Z" fill="currentColor"/>
<path d="M113.163 243.516L106.83 237.143L97.0615 227.649L90.5972 221.433L85.7131 216.783L74.234 205.331C71.3088 202.418 69.1018 199.14 67.0515 195.588C60.0126 183.443 59.7383 168.726 68.8014 157.495L73.3199 162.405L83.8978 173.766L118.152 209.967C121.835 213.858 125.139 217.802 127.333 222.738C132.334 233.969 130.859 245.109 124.421 255.465L113.203 243.503L113.163 243.516Z" fill="#667D9E"/>
<path d="M187.195 142.79L176.944 153.199L156.376 132.448L151.113 127.08L157.799 120.146L164.668 113.016L171.015 106.421L176.957 100.27L183.278 106.812L188.449 112.219L193.986 118.03L199.536 123.842L202.697 127.119L187.195 142.79Z" fill="#667D9E"/>
</g>
<defs>
<clipPath id="clip0_{uid}">
<rect width="140.843" height="275.654" fill="white" transform="translate(61.8535 10.0319)"/>
</clipPath>
</defs>
</svg>"""

SOLUTIONS = [
    ("strategy.html", "01", "Strategy &amp; Consultancy",
     "Find out what is actually happening inside the business, then what to do."),
    ("technology.html", "02", "Technology &amp; Services: Tech",
     "Strategy through architecture, build and integration, into deployment."),
    ("managed-operations.html", "02", "Technology &amp; Services: Services",
     "We deliver the enabling functions, so you can focus on the things that matter."),
    ("capital.html", "03", "Capital",
     "Go-to-market to raise capital, grounded in fundamentals, not just a deck."),
]

NAV = [
    ("Solutions", "solutions.html", True),
    ("Sectors", "sectors.html", False),
    ("Approach", "approach.html", False),
    ("For Investors", "investors.html", False),
    ("Why Sinaa", "why-sinaa.html", False),
    ("Insights", "insights.html", False),
]


def logo(tag="a", href="index.html", on_dark=False, uid="hdr"):
    """Render the lockup inline.

    `uid` suffixes the mask and clipPath ids. The artwork carries both and
    appears twice per document, so without a distinct uid the footer copy
    would reference the header copy's definitions.

    A single <defs> plus two <use> references would carry the paths once and
    save ~2.3KB gzipped per page, but <use> combined with a mask has a patchy
    history in Safari, and the mask is not decorative here -- removing it
    changes 2.7% of the artwork's ink pixels. For the one element that has to
    render correctly everywhere, the duplicated markup is the cheaper risk.

    `on_dark` only adds a class. The ink is currentColor, so the colour comes
    from CSS; the two supplied files are byte-identical apart from that ink.
    """
    cls = "logo logo--on-dark" if on_dark else "logo"
    return (
        '<{t} class="{c}" href="{h}">{svg}</{t}>'
    ).format(t=tag, c=cls, h=href, svg=LOCKUP_SVG.format(uid=uid))


def header(current):
    items = []
    for label, href, mega in NAV:
        cur = ' aria-current="page"' if href == current or (
            mega and current in [s[0] for s in SOLUTIONS]) else ""
        if mega:
            panel = (
                '<a class="mega__item" href="solutions.html">'
                '<span class="mega__num">OVERVIEW</span>'
                '<span class="mega__title">All solutions</span>'
                '<span class="mega__desc">Deep-dive diagnostics, end-to-end technology, and the capital raise.</span></a>'
            )
            panel += "".join(
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
                '<span class="mega__desc">Retainer, project based, service fees or contingent based.</span></a>'
                '<a class="mega__item" href="readiness.html">'
                '<span class="mega__num">TOOL</span>'
                '<span class="mega__title">Growth Readiness Scan</span>'
                '<span class="mega__desc">Six questions, two minutes. No email required.</span></a>'
            )
            # One control: the link navigates on click, and opens the panel
            # on hover or keyboard focus. Not a button -- a button cannot
            # navigate, and that was the bug the reviewer reported.
            items.append(
                '<div class="nav__item nav__item--mega" data-mega>'
                '<a class="nav__link nav__link--mega" href="{h}" data-mega-trigger '
                'aria-expanded="false" aria-controls="mega-solutions"{c}>Solutions'
                '<svg class="nav__caret" viewBox="0 0 10 10" aria-hidden="true" focusable="false">'
                '<path d="M1 3l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6" '
                'stroke-linecap="round" stroke-linejoin="round"/></svg></a>'
                '<div class="mega" id="mega-solutions" data-mega-panel hidden>{p}</div>'
                '</div>'.format(h=href, c=cur, p=panel)
            )
        else:
            items.append(
                '<div class="nav__item"><a class="nav__link" href="{h}"{c}>{l}</a></div>'.format(
                    h=href, c=cur, l=label))

    drawer_links = '<a href="solutions.html">All solutions</a>' + "".join(
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
</header>""".format(logo=logo(uid="hdr"), items="".join(items), dl=drawer_links, dm=drawer_more)


FOOTER = """<footer class="site-footer on-dark">
  <div class="shell">
    <div class="footer__grid">
      <div>
        {logo}
        <p style="margin-top:1.25rem;max-width:32ch;font-size:var(--t-small)">
          One partner across the entire growth journey.</p>
      </div>
      <nav aria-labelledby="f-sol">
        <h2 id="f-sol">Solutions</h2>
        <ul class="footer__nav">
          <li><a href="strategy.html">Strategy &amp; Consultancy</a></li>
          <li><a href="technology.html">Technology &amp; Services: Tech</a></li>
          <li><a href="managed-operations.html">Technology &amp; Services: Services</a></li>
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
      <p style="margin:0">&copy; 2026 Sinaa Partners Ltd. All rights reserved.</p>
      <p style="margin:0"><a href="mailto:{email}">{email}</a></p>
    </div>
  </div>
</footer>""".format(logo=logo(on_dark=True, uid="ftr"), email=EMAIL)


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
<link rel="preload" href="assets/fonts/aptos-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/aptos-display-700.woff2" as="font" type="font/woff2" crossorigin>
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


# --------------------------------------------------------------------------
# Sector tiles. Icons are 24-unit outline glyphs drawn to one spec -- 1.8
# stroke, round caps and joins, no fills -- so they read as one set rather
# than eight borrowed pictures. Decorative: each sits beside its own label,
# so it is hidden from assistive tech.
# --------------------------------------------------------------------------
SECTOR_ICONS = {
    "health": '<circle cx="12" cy="12" r="8.5"/><path d="M7 12h2.2l1.4-3.4L13.2 15l1.4-3H17"/>',
    "card": '<rect x="2.8" y="5.8" width="18.4" height="12.4" rx="2.2"/><path d="M2.8 10h18.4"/>',
    "house": '<path d="M3.6 10.4 12 4l8.4 6.4"/><path d="M6 9.2V20h12V9.2"/><path d="M10.2 20v-4.4h3.6V20"/>',
    "cap": '<path d="M12 4.6 2.6 9.2 12 13.8l9.4-4.6L12 4.6Z"/>'
           '<path d="M6.4 11.3v4.4c0 1.3 2.5 2.4 5.6 2.4s5.6-1.1 5.6-2.4v-4.4"/>',
    "cart": '<path d="M2.6 3.8h2.2l2.3 10.3a1.7 1.7 0 0 0 1.7 1.3h7.9a1.7 1.7 0 0 0 1.6-1.2L20 7.1H6.2"/>'
            '<circle cx="9.6" cy="19.2" r="1.3"/><circle cx="16.6" cy="19.2" r="1.3"/>',
    "case": '<rect x="2.6" y="6.8" width="18.8" height="12.6" rx="2.2"/>'
            '<path d="M8.8 6.8V5.4A1.6 1.6 0 0 1 10.4 3.8h3.2a1.6 1.6 0 0 1 1.6 1.6v1.4"/>',
    "chip": '<rect x="6.8" y="6.8" width="10.4" height="10.4" rx="1.8"/>'
            '<rect x="10.2" y="10.2" width="3.6" height="3.6" rx="0.6"/>'
            '<path d="M9.8 3.6v3.2M14.2 3.6v3.2M9.8 17.2v3.2M14.2 17.2v3.2'
            'M3.6 9.8h3.2M3.6 14.2h3.2M17.2 9.8h3.2M17.2 14.2h3.2"/>',
    "shield": '<path d="M12 3.4 5.2 5.9v6.2c0 4.1 2.9 7.2 6.8 8.5 3.9-1.3 6.8-4.4 6.8-8.5V5.9L12 3.4Z"/>'
              '<path d="M9.1 12.1 11.3 14.3 15.2 10"/>',
}

HOME_SECTORS = [
    ("Health Care", "Clinical systems &amp; regulated care delivery", "health"),
    ("Fintech", "Investment and finance platforms &amp; payments", "card"),
    ("PropTech", "Property &amp; real estate technology", "house"),
    ("EduTech", "Learning platforms &amp; education delivery", "cap"),
    ("E-commerce", "Retail, marketplace &amp; digital commerce", "cart"),
    ("Services", "Professional &amp; business services", "case"),
    ("Automation &amp; AI", "Workflow automation &amp; applied AI", "chip"),
    ("Compliance", "Regulatory &amp; risk-driven builds", "shield"),
]


def sector_tiles():
    out = []
    for title, body, icon in HOME_SECTORS:
        out.append(
            '<div class="tile">'
            '<div class="tile__top"><h3>{t}</h3>'
            '<svg class="tile__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true" focusable="false">{i}</svg></div>'
            '<p>{b}</p></div>'.format(t=title, b=body, i=SECTOR_ICONS[icon]))
    return "\n      ".join(out)


# --------------------------------------------------------------------------
# Managed-operations function cards. Same icon spec as the sector tiles --
# 24-unit box, 1.8 stroke, round caps, no fills -- so the two sets read as one
# family. Decorative: each sits beside its own heading.
# --------------------------------------------------------------------------
FUNCTION_ICONS = {
    "chart": '<path d="M3.6 20.2h16.8"/><rect x="5.4" y="12.4" width="3.4" height="6"/>'
             '<rect x="10.3" y="8.6" width="3.4" height="9.8"/>'
             '<rect x="15.2" y="4.8" width="3.4" height="13.6"/>',
    "people": '<circle cx="9.2" cy="8.4" r="3.2"/>'
              '<path d="M3.4 19.6a5.8 5.8 0 0 1 11.6 0"/>'
              '<path d="M15.6 5.6a3.2 3.2 0 0 1 0 5.9"/><path d="M17 15.1a5.8 5.8 0 0 1 3.6 4.5"/>',
    "megaphone": '<path d="M4.4 10.2v3.6a1.8 1.8 0 0 0 1.8 1.8h1.6l7.6 4V4.4l-7.6 4H6.2a1.8 1.8 0 0 0-1.8 1.8Z"/>'
                 '<path d="M18.4 9.4a3.6 3.6 0 0 1 0 5.2"/><path d="M7.8 15.6v3.1a1.4 1.4 0 0 0 2.8 0v-2.1"/>',
    "funnel": '<path d="M3.6 4.6h16.8l-6.5 7.6v6.4l-3.8 2.2v-8.6L3.6 4.6Z"/>',
    "calendar": '<rect x="3.6" y="5.6" width="16.8" height="14.8" rx="2"/>'
                '<path d="M3.6 10h16.8M8.4 3.6v4M15.6 3.6v4"/>'
                '<path d="M7.6 13.6h2M11 13.6h2M14.4 13.6h2M7.6 16.8h2M11 16.8h2"/>',
    "layers": '<path d="M12 3.4 3.4 7.8 12 12.2l8.6-4.4L12 3.4Z"/>'
              '<path d="M3.4 12.2 12 16.6l8.6-4.4"/><path d="M3.4 16.4 12 20.8l8.6-4.4"/>',
}

FUNCTIONS = [
    ("Finance", "Accounting, reporting, FP&amp;A: a clean monthly close and MI that the board can rely on.", "chart"),
    ("HR", "Recruitment, payroll and people management: all run to process rather than whoever has time.", "people"),
    ("Marketing", "Content, campaigns and brand: consistent output without need for an in-house team.", "megaphone"),
    ("Sales", "Pipeline, outreach and deal support: keeps the top of the funnel growing.", "funnel"),
    ("Admin", "Scheduling, data and document admin: the work that quietly absorbs senior resource time.", "calendar"),
    ("Or a blend", "Choose a combination of services that will turn the needle for you.", "layers"),
]


def function_cards():
    out = []
    for title, body, icon in FUNCTIONS:
        out.append(
            '<div class="card">'
            '<div class="card__top"><div class="card__rule"></div>'
            '<svg class="card__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true" focusable="false">{i}</svg></div>'
            '<h3>{t}</h3><p>{b}</p></div>'.format(t=title, b=body, i=FUNCTION_ICONS[icon]))
    return "\n      ".join(out)



# --------------------------------------------------------------------------
# "Why us" cards (offer deck slide 12). The deck names its four icons link /
# blueprint / layers / scales and sets them in the top-right of a rounded box
# with the number top-left; this redraws them to the same 24-unit, 1.8-stroke,
# no-fill spec as the sector and function icons so the three sets read as one
# family. "layers" is already in FUNCTION_ICONS, so it is reused rather than
# drawn twice.
# --------------------------------------------------------------------------
WHY_ICONS = {
    # two interlocking links -- one partner, no hand-offs
    "link": '<rect x="2.3" y="8.4" width="11.1" height="7.2" rx="3.6"/>'
            '<rect x="10.6" y="8.4" width="11.1" height="7.2" rx="3.6"/>',
        # a wireframe frame -- built by the team that designed it. The header rule
    # and the column divider deliberately overshoot the frame with round caps,
    # which is the detail that makes the deck's drawing read as a blueprint.
    "blueprint": '<rect x="3.2" y="4.5" width="18" height="15.1" rx="1.6"/>'
                 '<path d="M2.6 8.7h19.2"/><path d="M9.1 8.3v11.8"/>'
                 '<path d="M11.5 12.9h7M11.5 15.9h7"/>',
        # balance scales -- a raise grounded in reality. Each pan is a closed
    # triangle sitting above its own bowl arc, as the deck draws it, rather
    # than one triangle with a curved base.
    "scales": '<path d="M12 3.7v16.2"/><path d="M3.7 7.7h16.6"/><path d="M4.5 19.9h15"/>'
              '<path d="M4.1 7.9 2.2 11.7h3.8L4.1 7.9Z"/>'
              '<path d="M1 11.7a3.1 3.1 0 0 0 6.2 0"/>'
              '<path d="M19.9 7.9 18 11.7h3.8L19.9 7.9Z"/>'
              '<path d="M16.8 11.7a3.1 3.1 0 0 0 6.2 0"/>',
}

WHY_US = [
    ("01", "One partner, no hand-offs", "link",
     "Strategy, execution and capital raise under one roof, not three vendors passing "
     "a file. Nobody blames the previous firm, because there is no previous firm."),
    ("02", "Built by the team that designed it", "blueprint",
     "The people who write the strategy also build and run the technology. What we "
     "conclude is what we deliver."),
    ("03", "Comfortable with complexity", "layers",
     "Experience across clinical, compliance-heavy and operationally intricate "
     "businesses, where regulation and workflows shape the outcome."),
    ("04", "Capital raise process grounded in reality", "scales",
     "Our end-to-end approach means the diligence process confirms the investor story "
     "rather than unpicks it."),
]


ICON_ATTRS = ('viewBox="0 0 24 24" fill="none" stroke="currentColor" '
              'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
              'aria-hidden="true" focusable="false"')


def why_cards(tag="h3", variant="compact"):
    """The four Why-us boxes.

    `compact` is the home teaser: number, title and icon share one row, so the
    box stays short. `full` is the Why Sinaa page, where these are the whole
    section rather than a teaser -- it keeps the larger .card scale and the
    number / rule / heading rhythm, and hangs the icon in the top-right corner
    as the deck does.
    """
    out = []
    for num, title, icon, body in WHY_US:
        glyph = WHY_ICONS.get(icon) or FUNCTION_ICONS[icon]
        if variant == "full":
            out.append(
                '<div class="card">'
                '<div class="card__top"><span class="card__num">{n}</span>'
                '<svg class="card__icon" {a}>{i}</svg></div>'
                '<div class="card__rule"></div>'
                '<{g}>{t}</{g}><p>{b}</p></div>'.format(
                    n=num, t=title, g=tag, b=body, i=glyph, a=ICON_ATTRS))
        else:
            out.append(
                '<div class="wcard">'
                '<div class="wcard__top">'
                '<span class="wcard__num">{n}</span>'
                '<{g}>{t}</{g}>'
                '<svg class="wcard__icon" {a}>{i}</svg>'
                '</div><p>{b}</p></div>'.format(
                    n=num, t=title, g=tag, b=body, i=glyph, a=ICON_ATTRS))
    return "\n        ".join(out)


# --------------------------------------------------------------------------
# Sectors page cards. Same eight sectors as the home tiles, so they reuse
# SECTOR_ICONS rather than carrying a second drawing of the same thing.
# --------------------------------------------------------------------------
SECTOR_DETAIL = [
    ("Health Care", "Clinical systems and regulated care delivery. Safety, information governance "
     "and clinical workflow are design constraints from the first sprint, not a "
     "compliance review at the end.", "health"),
    ("Fintech", "Investment &amp; finance platforms and payments. Where reconciliation, resilience "
     "and the regulatory perimeter configures the output.", "card"),
    ("PropTech", "Property and real estate technology. Transaction-heavy workflows joining "
     "fragmented data across parties who do not share systems.", "house"),
    ("EduTech", "Learning platforms and education delivery. Built for outcomes and engagement.", "cap"),
    ("E-commerce", "Retail, marketplace and digital commerce, where unit economics and "
     "operational throughput matter more than the storefront.", "cart"),
    ("Services", "Professional and business services. People-led businesses that need to "
     "productise, systematise and scale without losing margin.", "case"),
    ("Automation &amp; AI", "Workflow automation and applied AI, deployed where it removes measurable "
     "cost or cycle time.", "chip"),
    ("Compliance", "Regulatory and risk-driven builds. Where the control environment is part of the "
     "product.", "shield"),
]


def sector_cards():
    out = []
    for i, (title, body, icon) in enumerate(SECTOR_DETAIL, 1):
        out.append(
            '<div class="card">'
            '<div class="card__top"><span class="card__num">{n:02d}</span>'
            '<svg class="card__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true" focusable="false">{i}</svg></div>'
            '<h2>{t}</h2><p>{b}</p></div>'.format(n=i, t=title, b=body, i=SECTOR_ICONS[icon]))
    return "\n      ".join(out)


def cta(heading, body, primary=("contact.html", "Book an intro call"),
        secondary=("readiness.html", "Take the readiness scan")):
    # A secondary entry may carry a third element: an id, used when the button
    # has to do something on the page rather than navigate away.
    sid = ' id="{}"'.format(secondary[2]) if len(secondary) > 2 else ""
    return """<section class="section cta-band on-dark">
  <div class="shell center reveal" style="max-width:760px">
    <h2>{h}</h2>
    <p class="lead">{b}</p>
    <div class="btn-row" style="margin-top:2rem">
      <a class="btn btn--primary" href="{p0}">{p1}</a>
      <a class="btn btn--ghost" href="{s0}"{sid}>{s1}</a>
    </div>
  </div>
</section>""".format(h=heading, b=body, p0=primary[0], p1=primary[1],
                     s0=secondary[0], s1=secondary[1], sid=sid)


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
    <svg viewBox="0 0 100 100" fill="none" aria-hidden="true" focusable="false">
      <path d="M37 14.3 A38 38 0 0 0 37 85.7" stroke="#A9761D" stroke-width="1.2" stroke-linecap="round" opacity="0.32"/>
      <path d="M63 14.3 A38 38 0 0 1 63 85.7" stroke="#A9761D" stroke-width="1.2" stroke-linecap="round" opacity="0.32"/>
      <path d="M46 6 C30 26 62 40 58 54 C54 70 34 78 40 94 C30 74 52 62 48 48 C44 34 34 24 46 6 Z" fill="#12293F" opacity="0.5"/>
      <path d="M72 29 L83 40 L72 51 L61 40 Z" fill="#6D85AC" opacity="0.18"/>
    </svg>
  </div>
  <div class="shell hero__inner">
    <p class="eyebrow">Strategy | Technology | Capital</p>
    <h1>One partner across the entire growth journey.</h1>
    <p class="lead">We work alongside founders, ambitious management teams and the
      investors who back them. We diagnose what is really happening inside the business,
      build the technology and deliver the operating capability to fix it and, when the
      time is right, take the story to market to raise the capital.</p>
    <div class="btn-row" style="margin-top:2.5rem">
      <a class="btn btn--primary" href="contact.html">Start a conversation</a>
      <a class="btn btn--ghost" href="solutions.html">Explore the three pillars</a>
    </div>
    <dl class="hero__meta">
      <div><dt>For management teams</dt><dd>Professionalise, scale, and become fundable.</dd></div>
      <div><dt>For capital partners</dt><dd>Identify the areas for value creation</dd></div>
      <div><dt>Engagement</dt><dd>Standalone pillars or one continuous mandate.</dd></div>
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
        <p class="lead">Most businesses have stalled in their growth journey due to the
          gap between the three pillars. The strategy house writes the plan and leaves.
          The tech partner builds something that doesn&rsquo;t quite match the plan. The
          financial adviser concludes the numbers don&rsquo;t support the pitch.</p>
        <p class="lead">Sound familiar&hellip;?</p>
        <p>Sinaa Partners closes the gap by delivering across the three pillars, for
          those wanting to scale efficiently.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--warm">
  <div class="shell">
    <div class="center reveal" style="max-width:640px;margin-bottom:3.5rem">
      <p class="eyebrow">Our offer</p>
      <h2>Three pillars</h2>
      <p>Each pillar is a complete engagement in its own right. Together, they form a
        single continuous growth journey.</p>
    </div>
    <div class="grid grid--3 reveal">
      <a class="card card--pillar" href="strategy.html">
        <span class="card__num">PILLAR 01</span>
        <h3>Strategy &amp; Consultancy</h3>
        <ul class="ticks" style="gap:.6rem;font-size:var(--t-small);margin-top:.5rem">
          <li>Deep-dive business diagnostics</li>
          <li>Root-cause analysis of gaps</li>
          <li>Strategic roadmap &amp; priorities</li>
          <li>Board-ready recommendations</li>
        </ul>
        <span class="link-arrow">Explore the pillar</span>
      </a>
      <a class="card card--pillar" href="technology.html">
        <span class="card__num">PILLAR 02</span>
        <h3>Technology &amp; Services: Tech</h3>
        <ul class="ticks" style="gap:.6rem;font-size:var(--t-small);margin-top:.5rem">
          <li>Tech build, start to finish</li>
          <li>Clinical, compliance &amp; automation</li>
          <li>Managed BPO across the business</li>
          <li>Ongoing support &amp; improvement</li>
        </ul>
        <span class="link-arrow">Explore the pillar</span>
      </a>
      <a class="card card--pillar" href="capital.html">
        <span class="card__num">PILLAR 03</span>
        <h3>Capital</h3>
        <ul class="ticks" style="gap:.6rem;font-size:var(--t-small);margin-top:.5rem">
          <li>Investor appeal positioning</li>
          <li>Go-to-market for the raise</li>
          <li>Data room &amp; narrative support</li>
          <li>Process management to close</li>
        </ul>
        <span class="link-arrow">Explore the pillar</span>
      </a>
    </div>
    <div class="center" style="margin-top:3rem">
      <a class="link-arrow" href="approach.html">How the three fit together</a>
    </div>
  </div>
</section>

<section class="section section--dark on-dark">
  <div class="shell">
    <div class="split reveal">
      <div class="sticky">
        <p class="eyebrow">How it fits together</p>
        <h2>Three pillars, one growth journey.</h2>
        <p>Each offer stands alone delivering clear outcomes. Together they compound to
          deliver your growth ambition.</p>
        <p style="margin-top:1.5rem"><a class="link-arrow" href="approach.html">See the full approach</a></p>
      </div>
      <div>
        <div class="loop">
          <div class="card card--dark">
            <span class="card__num">01</span>
            <h3>Strategy &amp; Consultancy</h3>
            <p>Discover, diagnose &amp; plan</p>
          </div>
          <div class="loop__arrow" aria-hidden="true">→</div>
          <div class="card card--dark">
            <span class="card__num">02</span>
            <h3>Technology &amp; Services</h3>
            <p>Build &amp; run</p>
          </div>
          <div class="loop__arrow" aria-hidden="true">→</div>
          <div class="card card--dark">
            <span class="card__num">03</span>
            <h3>Capital</h3>
            <p>Funding to the next stage</p>
          </div>
        </div>
        <p class="loop__note">A holistic proposition delivered by one partner</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="center reveal" style="max-width:640px;margin-bottom:3rem">
      <p class="eyebrow">Sectors we know</p>
      <h2>Hands-on experience across dynamic sectors.</h2>
      <p>Regulated, operationally intricate, fast evolving industries; this is where the
        strategy, business model and operating realities become entangled.</p>
    </div>
    <div class="grid grid--4 reveal">
      """ + sector_tiles() + """
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
        <p class="eyebrow">Why us</p>
        <h2>An operating partner, not another adviser.</h2>
        <p class="lead">Four reasons, each of them a structural choice rather than a
          claim.</p>
        <p style="margin-top:1.5rem"><a class="link-arrow" href="why-sinaa.html">The full case</a></p>
      </div>
      <div class="grid grid--2 why-grid grid--hover-dark">
        """ + why_cards() + """
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
        <p>The Growth Readiness Scan asks six questions about your operating model, your
          data, your delivery capacity and your funding position. It tells you which
          pillar to start with, and why.</p>
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
        "And the capital raise to fund the next chapter.") + """
<section class="section">
  <div class="shell">
    <div class="grid grid--2 reveal" style="gap:2.5rem">
      <a class="card card--pillar" href="strategy.html">
        <span class="card__num">PILLAR 01</span>
        <h2>Strategy &amp; Consultancy</h2>
        <p>A full diagnostic deep-dive into operations, financials, organisation and
          market position, followed by a prioritised roadmap the board can act on.</p>
        <ul class="ticks" style="gap:.6rem;font-size:var(--t-small)">
          <li>Deep-dive business diagnostics</li>
          <li>Root-cause analysis of gaps</li>
          <li>Strategic roadmap &amp; priorities</li>
          <li>Board-ready and shareholder recommendations</li>
        </ul>
        <span class="link-arrow">Explore Strategy</span>
      </a>
      <a class="card card--pillar" href="technology.html">
        <span class="card__num">PILLAR 02</span>
        <h2>Technology &amp; Services: Tech</h2>
        <p>End-to-end technology delivery, from product and platform strategy through to
          architecture, build, integration and continuous improvement.</p>
        <ul class="ticks" style="gap:.6rem;font-size:var(--t-small)">
          <li>Product &amp; platform strategy</li>
          <li>Architecture &amp; solution design</li>
          <li>Build, integration &amp; deployment</li>
          <li>Ongoing support &amp; continuous improvement</li>
        </ul>
        <span class="link-arrow">Explore Technology</span>
      </a>
      <a class="card card--pillar" href="managed-operations.html">
        <span class="card__num">PILLAR 02</span>
        <h2>Technology &amp; Services: Services</h2>
        <p>Fully managed or co-sourced operations across the functions that keep a
          business, so the leadership team can focus on growth.</p>
        <ul class="ticks" style="gap:.6rem;font-size:var(--t-small)">
          <li>Finance: accounting, reporting, FP&amp;A</li>
          <li>HR: recruitment, payroll, people management</li>
          <li>Marketing and sales support</li>
          <li>Scheduling, data &amp; document admin</li>
        </ul>
        <span class="link-arrow">Explore Services</span>
      </a>
      <a class="card card--pillar" href="capital.html">
        <span class="card__num">PILLAR 03</span>
        <h2>Capital</h2>
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
      <p class="eyebrow">Where to start?</p>
      <h2>Does this sound familiar?</h2>
    </div>
    <div class="table-wrap reveal">
      <table>
        <caption class="vh">Which pillar to start with, by situation</caption>
        <thead>
          <tr><th scope="col">Scenario</th><th scope="col">Focus on</th><th scope="col">Typical scope</th></tr>
        </thead>
        <tbody>
          <tr>
            <th scope="row">Performance is drifting and the cause is contested</th>
            <td>Strategy &amp; Consultancy</td>
            <td>6&ndash;10 week diagnostic, board-ready roadmap</td>
          </tr>
          <tr>
            <th scope="row">The plan is clear but delivery capacity is the constraint</th>
            <td>Technology &amp; Services</td>
            <td>Fixed-scope build, then ongoing support</td>
          </tr>
          <tr>
            <th scope="row">The back office is consuming the leadership team</th>
            <td>Services</td>
            <td>Managed or co-sourced service, monthly</td>
          </tr>
          <tr>
            <th scope="row">The business is performing and needs funds for growth</th>
            <td>Capital</td>
            <td>Retainer plus success fee to close</td>
          </tr>
          <tr>
            <th scope="row">All of the above</th>
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
          "Let us help you work out the best place to start."),
)

# ==========================================================================
# Pillar 01 — Strategy
# ==========================================================================
PAGES["strategy.html"] = dict(
    title="Strategy & Consultancy — Sinaa Partners",
    desc="A full diagnostic deep-dive into operations, financials, organisation and "
         "market position, ending in a prioritised roadmap and board-ready recommendations.",
    main=page_hero(
        "Pillar 01",
        "Strategy &amp; Consultancy",
        "Identify the root causes of what is happening, develop the solutions and how "
        "to practically deliver them.") + """
<section class="section">
  <div class="shell">
    <div class="split reveal">
      <div class="sticky">
        <p class="eyebrow">What we do</p>
        <h2>A diagnostic, not an opinion.</h2>
        <p>We go deep into the business: the operating processes; the financials; the org
          chart as it really works; and the market position, as customers experience it.</p>
      </div>
      <ul class="ticks">
        <li>Full diagnostic: deep-dive operations, financials, organisation, market
          position</li>
        <li>Root-cause analysis of performance gaps, separating symptom from cause</li>
        <li>Strategic roadmap, sequenced by value and feasibility</li>
        <li>Target operating model and organisation design</li>
        <li>Board and shareholder-ready recommendations</li>
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
      <li><h3>Discover</h3><p>Understand the business as it runs today, across processes, systems &amp; data
        and people, not as the org chart describes it.</p></li>
      <li><h3>Diagnose</h3><p>Root-causes across all aspects of the business.</p></li>
      <li><h3>Design</h3><p>Define the target operating model and the outcomes that close the gap.</p></li>
      <li><h3>Roadmap</h3><p>Sequenced, costed, owned. Primed for stakeholders to review and approve.</p></li>
    </ol>
  </div>
</section>

<section class="section section--dark on-dark">
  <div class="shell">
    <div class="split reveal">
      <div>
        <p class="eyebrow">What happens next</p>
        <h2>The roadmap is the beginning not the end.</h2>
      </div>
      <div class="stack">
        <p class="pull">Most strategic reviews stay on the shelf because the authors cannot implement.</p>
        <p>Ours doesn&rsquo;t have to. Our team can pick up the roadmap and deliver it:
          either as a technology build; as managed operations; or both.</p>
        <div class="btn-row" style="margin-top:1.5rem">
          <a class="btn btn--primary" href="technology.html">Pillar 02 &mdash; Tech. &amp; Services</a>
          <a class="btn btn--ghost" href="capital.html">Pillar 03 — Capital</a>
        </div>
      </div>
    </div>
  </div>
</section>
""" + cta("Start with a diagnostic.",
          "We will perform a deep-dive against your priorities and deliver clarity "
          "within an agreed time frame.",
          ("contact.html", "Scope a diagnostic"),
          ("approach.html", "How the pillars connect")),
)

# ==========================================================================
# Pillar 02 — Technology build
# ==========================================================================
PAGES["technology.html"] = dict(
    title="Technology &amp; Services: Tech — Sinaa Partners",
    desc="End-to-end technology delivery: product and platform strategy, architecture, "
         "build, integration and deployment, with specialist clinical, compliance and "
         "automation practices.",
    main=page_hero(
        "Pillar 02",
        "Technology &amp; Services: Tech",
        "End-to-end technology delivery. Strategy through architecture, build and "
        "integration, into deployment and continuous improvement.") + """
<section class="section">
  <div class="shell">
    <div class="split reveal">
      <div class="sticky">
        <p class="eyebrow">End-to-end delivery</p>
        <h2>The team that designs it, is the team that ships it.</h2>
        <p>No hand-off between the people who set the direction and the people who
          write the code. One accountable team from platform strategy to run.</p>
      </div>
      <ul class="ticks ticks--drop">
        <li>Product &amp; platform strategy: what to build, for whom, in what order</li>
        <li>Architecture &amp; solution design, including integration into what exists</li>
        <li>Build, integration &amp; deployment against a defined scope</li>
        <li>Ongoing support &amp; continuous improvement post go-live</li>
      </ul>
    </div>
  </div>
</section>

<section class="section section--warm">
  <div class="shell">
    <div class="center reveal" style="max-width:620px;margin-bottom:3rem">
      <p class="eyebrow">Specialist verticals</p>
      <h2>Where the build is harder than the code.</h2>
      <p>Three specialist practices for domains where clinical risk, regulation or process
        complexity, determine success or failure.</p>
    </div>
        <div class="grid grid--3 reveal grid--hover-dark">
      <div class="card">
        <div class="card__rule"></div>
        <h3>Clinical</h3>
        <p>Clinical systems and workflow technology, built for the realities of delivering
          regulated care, where safety and auditability are non-negotiable.</p>
      </div>
      <div class="card">
        <div class="card__rule"></div>
        <h3>Compliance</h3>
        <p>Regulatory and risk-driven builds where the control environment is paramount.</p>
      </div>
      <div class="card">
        <div class="card__rule"></div>
        <h3>Automation</h3>
        <p>Workflow &amp; process automation, with applied AI to drive cost reduction.</p>
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
        <p>A platform that nobody operates is a cost line. Most of our &lsquo;build&rsquo;
          engagements continue into a &lsquo;run&rsquo; relationship, which leads to
          continuous improvement in the technology, and features managed services, to
          deliver the business processes.</p>
        <p><a class="link-arrow" href="managed-operations.html">Pillar 02 &mdash; Technology &amp; Services: Services</a></p>
      </div>
    </div>
  </div>
</section>
""" + cta("Scope a build.",
          "Bring us a roadmap, a problem, or a platform that has stalled. We will come "
          "back with a defined scope and a set of deliverables.",
          ("contact.html", "Scope a build"),
          ("sectors.html", "Sectors we know")),
)

# ==========================================================================
# Pillar 02 — Managed operations
# ==========================================================================
PAGES["managed-operations.html"] = dict(
    title="Technology &amp; Services: Services — Sinaa Partners",
    desc="Fully managed or co-sourced operations across finance, HR, marketing, sales "
         "and admin — run the back office so the leadership team can focus on growth.",
    main=page_hero(
        "Pillar 02",
        "Technology &amp; Services: Services",
        "We deliver the enabling functions, so you can focus on the things that "
        "matter.") + """
<section class="section">
  <div class="shell">
    <div class="center reveal" style="max-width:620px;margin-bottom:3rem">
      <p class="eyebrow">Functions we run</p>
      <h2>Five functions, one accountable service.</h2>
    </div>
    <div class="grid grid--3 grid--hover-dark reveal">
      """ + function_cards() + """
    </div>
  </div>
</section>

<section class="section section--warm-deep">
  <div class="shell">
    <div class="split reveal">
      <div class="sticky">
        <p class="eyebrow">Two models</p>
        <h2>Fully managed, or co-sourced.</h2>
        <p>The choice is about control, not cost. We help you decide which is more effective.</p>
      </div>
      <div class="grid grid--2">
        <div class="card">
          <h3>Fully managed</h3>
          <p>We own the function end-to-end and deliver against agreed service levels. Best
            where it is a distraction, not a differentiator.</p>
        </div>
        <div class="card">
          <h3>Co-sourced</h3>
          <p>Your team keeps ownership and management: we supply capacity; processes; and
            the tooling underneath. Best where domain knowledge needs to stay in-house.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--dark on-dark">
  <div class="shell">
    <div class="split reveal">
      <div>
        <p class="eyebrow">Why it matters</p>
        <h2>Clean operations stand up to diligence</h2>
      </div>
      <div class="stack">
        <p class="pull">A reliable monthly close is worth more in a data room than any
          slide about operational excellence.</p>
        <p>Running the support functions properly should not be a cost story. It leads to
          operating discipline and the outputs that underpin a successful capital raise.</p>
        <p><a class="link-arrow" href="capital.html">Pillar 03 — Capital</a></p>
      </div>
    </div>
  </div>
</section>
""" + cta("Hand over the work that is not yours to do.",
          "We will map the functions, the current cost and service levels, followed by "
          "proposing a solution.",
          ("contact.html", "Scope the services"),
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
        "Go-to-market to raise capital, grounded in fundamentals, not just a deck.") + """
<section class="section">
  <div class="shell">
    <div class="split reveal">
      <div class="sticky">
        <p class="eyebrow">What we do</p>
        <h2>From readiness to close.</h2>
        <p>We run a focused process, not just introductions.</p>
      </div>
      <ul class="ticks">
        <li>Investment-readiness assessment, an honest read on whether you are ready</li>
        <li>Curate the equity story &amp; narrative, built on the operating facts</li>
        <li>Financial model &amp; data room that is diligence ready</li>
        <li>Investor outreach, the right investors, with the right messaging</li>
        <li>Process management through to close</li>
      </ul>
    </div>
  </div>
</section>

<section class="section section--warm">
  <div class="shell">
    <div class="split reveal">
      <div>
        <p class="eyebrow">The difference</p>
        <h2>The raise is grounded in fundamentals, not just a deck.</h2>
      </div>
      <div class="stack">
        <p class="lead">Raising capital is not a standalone exercise. The equity story for investors is
          built from clarity in the strategic review phase which comes to life through
          technology and operational implementation.</p>
        <p>The data room will populate itself with the work preceding the capital raise.
          When potential investors diligence the numbers, the answer is not a follow-up
          email, it is a coherent narrative rooted in the diagnostic.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="center reveal" style="max-width:600px;margin-bottom:3rem">
      <p class="eyebrow">The process</p>
      <h2>How we engage</h2>
    </div>
    <ol class="steps steps--row reveal">
      <li><h3>Readiness</h3><p>Assess fundability, close the gaps that would stall a
        process before it starts.</p></li>
      <li><h3>Story &amp; materials</h3><p>Equity narrative, model and a data room built to anticipate the questions.</p></li>
      <li><h3>Go to market</h3><p>Targeted outreach to a mapped investor set.</p></li>
      <li><h3>Diligence to close</h3><p>Coordinate the process, hold the timetable and get to signature.</p></li>
    </ol>
  </div>
</section>


""" + cta("Find out if you are fundable today.",
          "A readiness assessment gives you a straight answer and a list of what would "
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
        "Hands-on experience across complex and fast evolving industries.",
        "We don’t claim every sector. Complexity is a common denominator where we "
        "have delivered.") + """
<section class="section">
  <div class="shell">
    <div class="grid grid--2 grid--hover-dark reveal" style="gap:2rem">
      """ + sector_cards() + """
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
          the business model, the operating reality and the regulatory environment are entangled, so a plan that ignores any one of the three fails.</p>
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
        "Three pillars, one growth journey.",
        "Each offer stands alone delivering clear outcomes. Together they compound to "
        "deliver your growth ambition.") + """
<section class="section">
  <div class="shell">
    <div class="loop reveal">
      <div class="card card--pillar">
        <span class="card__num">01</span><h2>Strategy &amp; Consultancy</h2>
        <p>Discover, diagnose &amp; plan. Understand the business as it operates today,
          identify the root cause of issues and sequence the fix.</p>
        <a class="link-arrow" href="strategy.html">Pillar 01</a>
      </div>
      <div class="loop__arrow" aria-hidden="true">→</div>
      <div class="card card--pillar">
        <span class="card__num">02</span><h2>Technology &amp; Services</h2>
        <p>Build and run. Deliver the platform and operate the functions that turn a plan
          into performance.</p>
        <a class="link-arrow" href="technology.html">Pillar 02</a>
      </div>
      <div class="loop__arrow" aria-hidden="true">→</div>
      <div class="card card--pillar">
        <span class="card__num">03</span><h2>Capital</h2>
        <p>Funding to the next stage. Take a real operating story to a mapped investor set
          and manage to close.</p>
        <a class="link-arrow" href="capital.html">Pillar 03</a>
      </div>
    </div>
    <p class="loop__note reveal" style="color:var(--gold-text);border-color:var(--rule-strong)">
      ↻ Capital raised funds the next cycle of strategy and growth</p>
  </div>
</section>

<section class="section section--warm">
  <div class="shell">
    <div class="split reveal">
      <div class="sticky">
        <p class="eyebrow">Why it compounds</p>
        <h2>Each pillar makes the next one efficient.</h2>
      </div>
      <div>
        <ul class="facts">
          <li><b>Diagnostic → Build</b><span>Grounded in a deep diagnostic exercise, the
            scope is already defined for the build phase. No duplication of discovery
            phase and total clarity on what stakeholders want to achieve.</span></li>
          <li><b>Build → Operations</b><span>The team that built the platform runs the
            processes on top of it, so the technology and operating model stay in
            sync.</span></li>
          <li><b>Operations → Capital</b><span>Clean reporting and an audit trail of
            activities populate the data room. Diligence questions are answered from
            source and not having to be retro-constructed.</span></li>
          <li><b>Capital → Strategy</b><span>Funds raised delivers the plan and takes
            the business through to the next phase of growth.</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>


""" + cta("One partner, from diagnosis to close.",
          "Take one pillar or take the journey. The entry point is the same."),
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
        "Four commercial models, designed to match the work rather than the other way round.") + """
<section class="section">
  <div class="shell">
    <div class="grid grid--2 reveal" style="gap:2rem">
      <div class="card card--pillar">
        <span class="card__num">MODEL 01</span>
        <h2>Advisory Retainer</h2>
        <p>Ongoing strategic advisory access, for co-founders and management teams
          navigating an active growth phase.</p>
        <ul class="ticks" style="gap:.6rem;font-size:var(--t-small)">
          <li>Monthly fee, defined access and cadence</li>
          <li>Board and leadership support</li>
          <li>Rolling term, reviewed quarterly</li>
        </ul>
      </div>
      <div class="card card--pillar">
        <span class="card__num">MODEL 02</span>
        <h2>Project-Based Build</h2>
        <p>Defined-scope technology or transformation build, delivered start to finish
          against a fixed plan with clear deliverables.</p>
        <ul class="ticks" style="gap:.6rem;font-size:var(--t-small)">
          <li>Fixed scope, timeline and price</li>
          <li>Named delivery team</li>
          <li>Optional ongoing support and continuous improvement after handover</li>
        </ul>
      </div>
      <div class="card card--pillar">
        <span class="card__num">MODEL 03</span>
        <h2>Managed Service (BPO)</h2>
        <p>Ongoing outsourced or co-sourced operations across finance, HR, marketing, sales
          or admin, that operate to agreed service levels.</p>
        <ul class="ticks" style="gap:.6rem;font-size:var(--t-small)">
          <li>Monthly service fee by function and volume</li>
          <li>Fully managed or co-sourced</li>
          <li>Scales up and down with the business</li>
        </ul>
      </div>
      <div class="card card--pillar">
        <span class="card__num">MODEL 04</span>
        <h2>Capital Raise Engagement</h2>
        <p>Retainer plus success fee contingent on a completed raise.</p>
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
        <p>Each step is a separate decision with its own commercials. Nothing is bundled to
          force the next one.</p>
        <p><a class="link-arrow" href="approach.html">See how the pillars connect</a></p>
      </div>
    </div>
  </div>
</section>
""" + cta("Which model fits your situation?",
          "Tell us the problem and the timeline. We will propose the commercial shape "
          "that suits."),
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
        "For capital providers",
        "An operating partner, not another adviser.",
        "You assess where value can be created: before the deal and every quarter "
        "after it. We work the same three pillars from your side of the table.") + """
<section class="section">
  <div class="shell">
    <div class="split reveal">
      <div class="sticky">
        <p class="eyebrow">The problem we solve</p>
        <h2>The value-creation plan and the people who can execute it are rarely the same firm.</h2>
      </div>
      <div class="stack">
        <p class="lead">A strategy house hands you a plan. A systems integrator hands you a quote.
          Neither is accountable for whether their deliverables fulfil the objective:
          we are.</p>
        <p>The team that writes the strategy and operational thesis is the team that can be
          deployed into the portfolio company to deliver it: as a build; as a managed
          operations layer; or as an interim capability while a permanent team is hired.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--warm">
  <div class="shell">
    <div class="center reveal" style="max-width:620px;margin-bottom:3rem">
      <p class="eyebrow">Across the investment cycle</p>
      <h2>Where we plug in</h2>
    </div>
    <div class="grid grid--4 reveal">
      <div class="card"><span class="card__num">PRE-DEAL</span><div class="card__rule"></div>
        <h3>Commercial &amp; operational diligence</h3>
        <p>An operator&rsquo;s read on the target: whether the operating model can deliver
          the plan, what the technology estate should really cost, and where the
          execution risk sits.</p></div>
      <div class="card"><span class="card__num">DAY 1&ndash;100</span><div class="card__rule"></div>
        <h3>Value-creation planning</h3>
        <p>A diagnostic converted into a sequenced, costed and owned roadmap, underpinned
          by a target operating model.</p></div>
      <div class="card"><span class="card__num">HOLD</span><div class="card__rule"></div>
        <h3>Build &amp; operate</h3>
        <p>Delivery capacity for platform builds, integrations after a bolt-on and managed
          back-office operations, across a portfolio rather than one asset at a time.</p></div>
      <div class="card"><span class="card__num">EXIT</span><div class="card__rule"></div>
        <h3>Exit readiness</h3>
        <p>Equity story, model and data room reflecting the operating realities we help to
          deliver. Diligence then confirms the story instead of testing it.</p></div>
    </div>
  </div>
</section>

<section class="section section--dark on-dark">
  <div class="shell">
    <div class="split reveal">
      <div>
        <p class="eyebrow">The approach</p>
        <h2>Three ways in.</h2>
      </div>
      <div>
        <ul class="facts">
          <li><b>Deal-by-deal</b><span>Scoped diligence or a single portfolio company engagement.</span></li>
          <li><b>Portfolio framework</b><span>A named team, drawn down across assets as needed.</span></li>
          <li><b>Operating partner</b><span>A retained relationship at fund level assisting with portfolio management and
          deployed where execution support is required.</span></li>
        </ul>
        <p style="margin-top:2rem"><a class="link-arrow" href="engagement.html">Engagement models in detail</a></p>
      </div>
    </div>
  </div>
</section>


""" + cta("Assessing an asset, or a portfolio?",
          "We will tell you if we have seen the situation before and where we would "
          "start.",
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
        "Four reasons, each of them a structural choice rather than a claim.") + """
<section class="section">
  <div class="shell">
        <div class="grid grid--2 reveal grid--hover-dark" style="gap:2.5rem">
      """ + why_cards("h2", "full") + """
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
          <li><b>No shelf strategy</b><span>We do not conclude a diagnostic mandate without a view on who executes the result.</span></li>
          <li><b>No raise we cannot stand behind</b><span>If the readiness assessment says the business is not fundable yet, we say so and
            propose how to change that.</span></li>
          <li><b>No sector tourism</b><span>If a situation is outside the space we know, we will say so.</span></li>
          <li><b>No bundling</b><span>Each pillar is a separate commercial decision. One
            engagement never obliges the next.</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>
""" + cta("See whether it stacks up.",
          "Let’s discuss an issue you actually have."),
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
    ("q4", "Do you have the capacity to execute?", [
        ("No, everything queues behind the same few people", 0),
        ("Some, but the roadmap is slipping", 1),
        ("Enough for the current plan", 2),
        ("Enough to accelerate if we choose to", 3)]),
    ("q5", "How much senior time goes into back-office operations?", [
        ("It dominates the leadership teams&rsquo; time", 0),
        ("More than it should", 1),
        ("Contained, mostly delegated", 2),
        ("Minimal, it runs without us", 3)]),
    ("q6", "Where are you on the funding journey?", [
        ("Not thinking about it yet", 0),
        ("We know we will need capital, nothing prepared", 1),
        ("Materials started, investors not yet identified", 2),
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
        "Six questions about your operating model, your data, your delivery capacity "
        "and your funding position. Two minutes, no email required, answers stay in "
        "your browser.") + """
<section class="section">
  <div class="shell">
    <div class="split">
      <div class="sticky reveal">
        <p class="eyebrow">How to read it</p>
        <h2>An honest starting point, not a sales qualifier.</h2>
        <p>The scan uncovers whether your constraints lie upstream (i.e. you do not know
          what is wrong), in the middle (i.e. you know, but cannot deliver it), or
          downstream (i.e. you are performing and need funding to grow).</p>
        <p>Nothing is submitted anywhere. If the read-out is useful, bring it to the intro
          call and let&rsquo;s discuss.</p>
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
""" + cta("Prefer to talk it through?",
          "A thirty-minute call covers more ground than any questionnaire.",
          ("contact.html", "Book an intro call"),
          ("solutions.html", "Explore the three pillars")),
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
        "Our views stated plainly. These insights explain our ethos and approach.") + """
<section class="section">
  <div class="shell" style="max-width:820px">
    <article class="card--flat reveal" style="margin-bottom:3.5rem;border-top:0">
      <p class="eyebrow">01 &mdash; Diagnostics</p>
      <h2>Most turnaround plans fail at the diagnosis, not the execution.</h2>
      <p>By the time a management team commissions help, there is usually already a theory
          in the room about what is wrong and the work quietly becomes an exercise in
          trying to confirm it. The result: a plan aimed at the wrong symptoms.</p>
      <p>This is why our diagnostic starts from the operating data rather than the
        leadership interview, and why root-cause analysis is a named deliverable rather
        than an implicit step.</p>
      <p><a class="link-arrow" href="strategy.html">Pillar 01 — Strategy &amp; Consultancy</a></p>
    </article>

    <article class="card--flat reveal" style="margin-bottom:3.5rem">
      <p class="eyebrow">02 &mdash; Delivery</p>
      <h2>The hand-over is where the value leaks.</h2>
      <p>Strategy firm to build partner to financial adviser: three transfers, each one a
          chance for context to be lost and for accountability to become blurred. Every
          transfer entails a discovery phase, paid for again.</p>
      <p>Delivering all three is not an upsell pitch. It prevents dropping the baton and
          avoids expensive detours in the growth journey.</p>
      <p><a class="link-arrow" href="approach.html">How the pillars connect</a></p>
    </article>

    <article class="card--flat reveal" style="margin-bottom:3.5rem">
      <p class="eyebrow">03 &mdash; Operations</p>
      <h2>Outsourcing is a control decision before it is a cost decision.</h2>
      <p>The question should never be whether a function is cheaper elsewhere. It is
          whether operating that function is a source of advantage. Where it is,
          co-source and keep control in-house. Where it is not, hand over the function
          and hold it to a service level.</p>
      <p>Getting this the wrong way around, i.e. outsourcing the control and keeping the
          admin, is a common and expensive mistake.</p>
      <p><a class="link-arrow" href="managed-operations.html">Technology &amp; Services: Services</a></p>
    </article>

    <article class="card--flat reveal" style="margin-bottom:3.5rem">
      <p class="eyebrow">04 &mdash; Applied AI</p>
      <h2>Automate the process you have already fixed.</h2>
      <p>Automation applied to a broken process produces a faster broken process and a
        new integration to maintain. Applied AI is worth deploying where the workflow is
        understood, the data is trustworthy, and the cost or cycle time being removed can
        be measured before and after.</p>
      <p>In other scenarios it is just a pilot, and pilots should be sandboxed and costed
          as such.</p>
      <p><a class="link-arrow" href="technology.html">Technology &amp; Services: Tech</a></p>
    </article>

    <article class="card--flat reveal" style="margin-bottom:3.5rem">
      <p class="eyebrow">05 &mdash; Capital</p>
      <h2>Fundability is a function of operating reality, not a deck.</h2>
      <p>The capital raise process brings external scrutiny to the operating model. No
          narrative survives a monthly close that cannot be reconciled, or a metric that
          changes definition between the deck and the data room.</p>
      <p>Our readiness assessment seeks to evaluate whether you are ready or not and what
          needs to change first.</p>
      <p><a class="link-arrow" href="capital.html">Pillar 03 — Capital</a></p>
    </article>

    <article class="card--flat reveal">
      <p class="eyebrow">06 &mdash; Regulated sectors</p>
      <h2>In regulated businesses, architecture is the compliance.</h2>
      <p>Treating the regulatory compliance as a review gate at the end of a build is the
          reliable way to discover, late, that the product cannot ship.</p>
        <p>In clinical and compliance-heavy businesses the regulatory perimeter must be
          considered a design input, alongside the user needs. It shapes the data model,
          the audit trail and the release process.</p>
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
        "Getting started",
        "Let&rsquo;s start with a conversation.",
        "Three steps from first contact to work beginning.") + """
<section class="section section--tight">
  <div class="shell">
    <ol class="steps steps--3 reveal">
      <li><h2>Intro call</h2><p>Understand where you are today and where you want to get to. No materials
        required.</p></li>
      <li><h2>Scoping proposal</h2><p>A tailored diagnostic or project scope, with clear
        deliverables, timeline and price.</p></li>
      <li><h2>Kick off</h2><p>A standalone project or the start of a journey, you
        decide.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="split reveal">
      <div class="sticky">
        <p class="eyebrow">Schedule a call</p>
        <h2>Tell us the situation.</h2>
        <p>The more details shared, the more useful the first call. If we are not the right
          partner, we will say so and try to direct you to those better placed.</p>
        <ul class="facts" style="margin-top:2rem">
          <li><b>Email</b><span><a href="mailto:{email}">{email}</a></span></li>
          <li><b>Phone</b><span>[phone]</span></li>
          <li><b>Contact</b><span>[Name], [title]</span></li>
        </ul>
      </div>

      <form id="contact-form" data-contact-form novalidate>
        <div class="field">
          <label for="name">Your name</label>
          <input id="name" name="name" type="text" autocomplete="name" required>
        </div>
        <div class="field">
          <label for="email">Email</label>
          <input id="email" name="email" type="email" autocomplete="email" required>
        </div>
        <div class="field">
          <label for="company">Company</label>
          <input id="company" name="company" type="text" autocomplete="organisation">
        </div>
        <div class="field">
          <label for="role">You are</label>
          <select id="role" name="role">
            <option>Founder / owner</option>
            <option>Investor / capital provider</option>
            <option>Board member / NED</option>
            <option>Management team</option>
            <option>Other</option>
          </select>
        </div>
        <div class="field">
          <label for="interest">What is this about?</label>
          <select id="interest" name="interest">
            <option>Strategy &amp; Consultancy</option>
            <option>Technology &amp; Services: Tech</option>
            <option>Technology &amp; Services: Services</option>
            <option>Capital</option>
            <option>Other / not sure yet</option>
          </select>
        </div>
        <div class="field">
          <label for="message">The situation</label>
          <textarea id="message" name="message" placeholder="Where are you today and what do you want to achieve going forward"></textarea>
          <p class="hint" id="message-hint">A few sentences is plenty.</p>
        </div>
        <button type="submit" class="btn btn--primary">Request an intro call</button>
      </form>
    </div>
  </div>
</section>
""".format(email=EMAIL) + cta(
        "Assessing an asset rather than running one?",
        "Capital providers evaluating an opportunity or managing an investment, "
          "please contact us with your specific needs.",
        ("investors.html", "For investors"),
        ("#contact-form", "Contact us", "contact-jump")),
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
