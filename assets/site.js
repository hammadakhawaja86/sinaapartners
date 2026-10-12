/* Sinaa Partners — progressive enhancement only. Every page works without JS. */
(function () {
  'use strict';

  /* --- Solutions mega menu ------------------------------------------------
     One control. Click follows the link to solutions.html; hover or keyboard
     focus opens the panel. Pointer-driven open is gated behind a real mouse,
     so a tap on a touch device just navigates rather than opening a panel the
     user cannot dismiss. */
  var wrap = document.querySelector('[data-mega]');
  var trigger = document.querySelector('[data-mega-trigger]');
  var panel = document.querySelector('[data-mega-panel]');
  if (wrap && trigger && panel) {
    var closeTimer = null;
    var cancelClose = function () { if (closeTimer) { clearTimeout(closeTimer); closeTimer = null; } };
    var open = function () {
      cancelClose();
      trigger.setAttribute('aria-expanded', 'true');
      panel.hidden = false;
    };
    var close = function () {
      cancelClose();
      trigger.setAttribute('aria-expanded', 'false');
      panel.hidden = true;
    };
    // A short grace period: the pointer travels diagonally from the link to
    // the panel, and briefly leaves the wrapper on the way.
    var closeSoon = function () { cancelClose(); closeTimer = setTimeout(close, 160); };

    // Escape has to return focus to the link, but that refocus fires focusin
    // again and would reopen what the user just dismissed. This latch keeps it
    // shut until they move away or hover back in.
    var dismissed = false;

    var fine = window.matchMedia('(hover: hover) and (pointer: fine)');
    if (fine.matches) {
      wrap.addEventListener('mouseenter', function () { dismissed = false; open(); });
      wrap.addEventListener('mouseleave', closeSoon);
    }

    // Keyboard users never hover, so focus has to open it too.
    wrap.addEventListener('focusin', function () { if (!dismissed) open(); });
    wrap.addEventListener('focusout', function (e) {
      if (!wrap.contains(e.relatedTarget)) { dismissed = false; close(); }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && trigger.getAttribute('aria-expanded') === 'true') {
        dismissed = true;
        close();
        trigger.focus();
      }
    });
  }

  /* --- Mobile drawer ------------------------------------------------------ */
  var burger = document.querySelector('[data-drawer-trigger]');
  var drawer = document.querySelector('[data-drawer]');
  if (burger && drawer) {
    burger.addEventListener('click', function () {
      var open = burger.getAttribute('aria-expanded') === 'true';
      burger.setAttribute('aria-expanded', String(!open));
      drawer.hidden = open;
      burger.querySelector('[data-drawer-label]').textContent = open ? 'Menu' : 'Close';
    });
  }

    /* --- Page-load intro ----------------------------------------------------
     The cover is already in the markup, so it hides the page from the first
     paint. This clones the real header lockup into it -- never a redrawn or
     stand-in logo -- flies it to the centre, waits for the fonts, then parts
     the bands while the clone glides back onto the header copy (a FLIP move:
     it is positioned at the measured box, so `transform: none` is home).

     Anything that can leave the page covered is guarded: no JS at all is
     handled by the <noscript> rule, a throw is caught, and a failsafe timer
     reveals regardless. */
    var introEl = document.querySelector('[data-intro]');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  /* The head script has already ruled on this one: it plays on arrival and on
     a reload, not while moving between pages. */
  var skipped = document.documentElement.classList.contains('intro-skip');
  var introPending = !!introEl && !reduce.matches && !skipped;

  function afterIntro(fn) {
    if (!introPending) { fn(); return; }
    document.addEventListener('sinaa:intro-done', fn, { once: true });
  }

    if (introEl && (reduce.matches || skipped)) {
    introEl.parentNode.removeChild(introEl);
  } else if (introEl) {
    runIntro(introEl);
  }

  function runIntro(root) {
    var doc = document.documentElement;
    var box = root.querySelector('[data-intro-logo]');
    var real = document.querySelector('.site-header .logo__lockup');
    var revealed = false, failsafe;

    function finish() {
      doc.classList.remove('intro-active');
      root.classList.add('is-done');
      introPending = false;
      document.dispatchEvent(new CustomEvent('sinaa:intro-done'));
    }

    if (!box || !real) { finish(); return; }

    try {
      doc.classList.add('intro-active');

      /* A clone, so the intro cannot drift from the header lockup. The ids
         inside carry the header's suffix, so rewrite them -- two elements
         sharing an id would send the clone's mask and clip at the header's
         definitions. */
      var clone = real.cloneNode(true);
      clone.removeAttribute('role');
      clone.removeAttribute('aria-label');
      clone.setAttribute('aria-hidden', 'true');
      clone.innerHTML = clone.innerHTML.replace(/_hdr/g, '_intro');
      box.appendChild(clone);

      var SCALE = 1.55;
      function place() {
        if (revealed) return;
        var r = real.getBoundingClientRect();
        if (!r.width) return;
        box.style.left = r.left + 'px';
        box.style.top = r.top + 'px';
        box.style.transform =
          'translate(' + ((window.innerWidth - r.width * SCALE) / 2 - r.left) + 'px,' +
          ((window.innerHeight - r.height * SCALE) / 2 - r.top) + 'px) scale(' + SCALE + ')';
      }
      place();
      box.classList.add('is-waiting');
      window.addEventListener('resize', place);

      function reveal() {
        if (revealed) return;
        revealed = true;
        clearTimeout(failsafe);
        window.removeEventListener('resize', place);
        box.classList.remove('is-waiting');
        root.classList.add('is-out');
        /* Hand-off: the real lockup comes back while the clone is still
           travelling, so the swap happens under the moving element. */
        setTimeout(function () { doc.classList.remove('intro-active'); }, 820);
        setTimeout(finish, 1120);
      }

      /* Never trap the user. */
      document.addEventListener('keydown', reveal, { once: true });
      document.addEventListener('pointerdown', reveal, { once: true });
      failsafe = setTimeout(reveal, 4000);

      var fonts = (document.fonts && document.fonts.ready) || Promise.resolve();
      fonts.then(function () {
        place();
        setTimeout(reveal, 1150);
      })['catch'](function () { reveal(); });
    } catch (e) {
      finish();
    }
  }

  /* --- Scroll reveal ------------------------------------------------------
     Held until the intro finishes, so entrance animations are not spent
     playing behind the cover. */
  function initReveal() {
    var nodes = document.querySelectorAll('.reveal');
    if (!window.IntersectionObserver || reduce.matches) {
      Array.prototype.forEach.call(nodes, function (n) { n.classList.add('is-in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add('is-in'); io.unobserve(entry.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    Array.prototype.forEach.call(nodes, function (n) { io.observe(n); });
  }
  afterIntro(initReveal);

  /* --- Growth Readiness Scan --------------------------------------------- */
  var scan = document.querySelector('[data-scan]');
  if (scan) {
    var out = scan.querySelector('[data-scan-result]');
    scan.addEventListener('submit', function (e) {
      e.preventDefault();
      var answered = scan.querySelectorAll('input[type=radio]:checked');
      var total = 0;
      Array.prototype.forEach.call(answered, function (i) { total += Number(i.value); });
      var groups = scan.querySelectorAll('fieldset').length;
      if (answered.length < groups) {
        out.hidden = false;
        out.querySelector('[data-scan-headline]').textContent = 'Answer every question to see your read-out.';
        out.querySelector('[data-scan-body]').textContent = '';
        out.querySelector('[data-scan-meter]').style.transform = 'scaleX(0)';
        out.querySelector('[data-scan-band]').textContent = '';
        out.focus();
        return;
      }
      var max = groups * 3;
      var pct = Math.round((total / max) * 100);
      var band, headline, body;
      if (pct < 45) {
        band = 'Diagnostic first';
        headline = 'Start with Strategy & Consultancy.';
        body = 'The gaps sit upstream of execution. A deep-dive diagnostic will tell you what is actually driving performance before you commit capital or build anything. Going to market from here would price in the uncertainty.';
      } else if (pct < 75) {
        band = 'Build & operate';
        headline = 'Start with Services & Technology.';
        body = 'The direction is clear enough; the constraint is delivery capacity. A defined-scope build, a managed operations layer, or both, will convert the plan into run-rate performance — and create the evidence a raise needs.';
      } else {
        band = 'Capital-ready';
        headline = 'Start with Capital.';
        body = 'The operating story holds up. The work now is positioning, the equity narrative, a data room that survives diligence, and a targeted process run to close.';
      }
      out.hidden = false;
      out.querySelector('[data-scan-band]').textContent = band;
      out.querySelector('[data-scan-headline]').textContent = headline;
      out.querySelector('[data-scan-body]').textContent = body;
      out.querySelector('[data-scan-meter]').style.transform = 'scaleX(' + (pct / 100) + ')';
      out.setAttribute('tabindex', '-1');
      out.focus();
    });
  }

  /* --- Contact form (static host: no backend, so hand off to mail) -------- */
  var contact = document.querySelector('[data-contact-form]');
  if (contact) {
    contact.addEventListener('submit', function (e) {
      e.preventDefault();
      var data = new FormData(contact);
      var lines = [];
      data.forEach(function (v, k) { if (v) lines.push(k + ': ' + v); });
      var href = 'mailto:hello@sinaapartners.com'
        + '?subject=' + encodeURIComponent('Intro call — ' + (data.get('company') || 'enquiry'))
        + '&body=' + encodeURIComponent(lines.join('\n'));
      window.location.href = href;
    });
  }

  /* --- "Contact us" in the investors band (slide 46) ----------------------
     The reviewer asked this button to jump to the form. It only scrolls and
     focuses -- it never sends anything on its own. */
  var jump = document.getElementById('contact-jump');
  var jumpForm = document.getElementById('contact-form');
  if (jump && jumpForm) {
    jump.addEventListener('click', function (e) {
      e.preventDefault();
      jumpForm.scrollIntoView({ block: 'start' });
      var first = jumpForm.querySelector('input, select, textarea');
      if (first) first.focus({ preventScroll: true });
    });
  }
})();
