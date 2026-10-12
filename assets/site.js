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

  /* --- Scroll reveal ------------------------------------------------------ */
  var nodes = document.querySelectorAll('.reveal');
  if (!window.IntersectionObserver || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    Array.prototype.forEach.call(nodes, function (n) { n.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add('is-in'); io.unobserve(entry.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    Array.prototype.forEach.call(nodes, function (n) { io.observe(n); });
  }

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
        out.querySelector('[data-scan-meter]').style.width = '0%';
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
