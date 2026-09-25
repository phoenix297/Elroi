/* EL-ROI Shipping Services — site interactions */
(function () {
  'use strict';

  var d = document;
  var WHATSAPP = '4915219521826';
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO = 'IntersectionObserver' in window;

  function $(sel, ctx) { return (ctx || d).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || d).querySelectorAll(sel)); }

  // Run a callback once, when an element scrolls into view
  function onVisible(el, cb, margin) {
    if (!hasIO) { cb(el); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { io.unobserve(entry.target); cb(entry.target); }
      });
    }, { threshold: 0, rootMargin: margin || '0px 0px -8% 0px' });
    io.observe(el);
  }

  // ---------- Toast ----------
  var toastEl = $('.toast');
  var toastTimer;
  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove('show'); }, 4200);
  }

  // ---------- Preloader ----------
  var preloader = $('#preloader');
  if (preloader) {
    var hidePre = function () { preloader.classList.add('hide'); };
    if (d.readyState === 'complete') setTimeout(hidePre, 200);
    else window.addEventListener('load', function () { setTimeout(hidePre, 250); });
    setTimeout(hidePre, 1600); // never block the page for long
  }

  // ---------- Header ----------
  var header = $('header.site');
  function onScroll() { if (header) header.classList.toggle('scrolled', window.scrollY > 8); }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // ---------- Hero: live background (drifting photo, optional video, scroll depth) ----------
  var heroMedia = $('.hero-media');
  if (heroMedia) {
    var videoSrc = heroMedia.getAttribute('data-video');
    var saveData = navigator.connection && navigator.connection.saveData;
    if (videoSrc && !reduceMotion && !saveData) {
      var hv = d.createElement('video');
      hv.className = 'hero-video';
      hv.muted = true; hv.loop = true; hv.autoplay = true; hv.playsInline = true;
      hv.setAttribute('muted', ''); hv.setAttribute('playsinline', '');
      hv.preload = 'auto';
      hv.src = videoSrc;
      hv.addEventListener('playing', function () { hv.classList.add('is-playing'); });
      heroMedia.appendChild(hv);
      var pr = hv.play();
      if (pr && pr.catch) pr.catch(function () {});
    }
    if (!reduceMotion) {
      var heroTicking = false;
      window.addEventListener('scroll', function () {
        if (heroTicking) return;
        heroTicking = true;
        requestAnimationFrame(function () {
          var y = Math.min(window.scrollY, window.innerHeight);
          heroMedia.style.setProperty('--parallax', (y * 0.12).toFixed(1) + 'px');
          heroTicking = false;
        });
      }, { passive: true });
    }
  }

  // ---------- Scroll progress bar + pinned journey animation ----------
  var progressBar = $('.scroll-progress');
  var journey = $('#journey');
  var jr = null;
  if (journey) {
    jr = {
      road: $('#jr-road', journey),
      sea: $('#jr-sea', journey),
      roadGold: $('#jr-road-gold', journey),
      seaGold: $('#jr-sea-gold', journey),
      veh: $('.jr-vehicle', journey),
      truck: $('.jr-truck', journey),
      ship: $('.jr-ship', journey),
      steps: $$('.journey-step', journey),
      dots: $$('.journey-dots i', journey),
      status: $('#jr-status', journey),
      day: $('#jr-day', journey),
      sticky: $('.journey-sticky', journey),
      map: $('.journey-map', journey),
      svg: $('.journey-map svg', journey),
      last: -1
    };
    jr.Lr = jr.road.getTotalLength();
    jr.Ls = jr.sea.getTotalLength();
    jr.roadGold.style.strokeDasharray = jr.Lr;
    jr.seaGold.style.strokeDasharray = jr.Ls;
  }
  var STATUS = ['Quote requested', 'Estimate confirmed', 'Loaded and at sea', 'Arrived in Lagos'];
  var STEP_AT = [0, 0.25, 0.5, 0.8, 1];
  var phone = window.matchMedia ? window.matchMedia('(max-width: 760px)') : { matches: false };
  function clamp01(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function seg(p, a, b) { return clamp01((p - a) / (b - a)); }
  function ease(t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }

  function renderJourney(p) {
    var roadT = ease(seg(p, 0.1, 0.42));
    var seaT = ease(seg(p, 0.52, 0.93));
    jr.roadGold.style.strokeDashoffset = (jr.Lr * (1 - roadT)).toFixed(1);
    jr.seaGold.style.strokeDashoffset = (jr.Ls * (1 - seaT)).toFixed(1);
    // truck on the road, container ship at sea (swap at the port)
    var onSea = p >= 0.47;
    var path = onSea ? jr.sea : jr.road;
    var L = onSea ? jr.Ls : jr.Lr;
    var at = (onSea ? seaT : roadT) * L;
    var pt = path.getPointAtLength(at);
    var a1 = path.getPointAtLength(Math.max(0, at - 3));
    var a2 = path.getPointAtLength(Math.min(L, at + 3));
    var ang = Math.atan2(a2.y - a1.y, a2.x - a1.x) * 180 / Math.PI;
    ang = Math.max(-26, Math.min(26, ang));
    jr.veh.setAttribute('transform', 'translate(' + pt.x.toFixed(1) + ' ' + pt.y.toFixed(1) + ') rotate(' + ang.toFixed(1) + ') scale(' + (phone.matches ? 1.25 : 1) + ')');
    // phones: pan the wide chart so the vehicle stays centred
    if (phone.matches) {
      var boxW = jr.map.clientWidth, boxH = jr.map.clientHeight;
      var k = boxH / 400, svgW = 1200 * k;
      var pan = Math.min(0, Math.max(boxW - svgW, boxW / 2 - pt.x * k));
      jr.svg.style.setProperty('--pan', pan.toFixed(1) + 'px');
    } else {
      jr.svg.style.removeProperty('--pan');
    }
    jr.truck.style.opacity = onSea ? 0 : 1;
    jr.ship.style.opacity = onSea ? 1 : 0;
    // steps, status and day counter
    var step = p < STEP_AT[1] ? 0 : p < STEP_AT[2] ? 1 : p < STEP_AT[3] ? 2 : 3;
    jr.steps.forEach(function (el, i) {
      el.classList.toggle('is-active', i === step);
      el.classList.toggle('is-done', i < step);
      el.style.setProperty('--fill', i < step ? 1 : i > step ? 0 : seg(p, STEP_AT[i], STEP_AT[i + 1]).toFixed(3));
    });
    jr.dots.forEach(function (el, i) { el.classList.toggle('on', i <= step); });
    var day = Math.round(seaT * 14);
    if (step !== jr.last) { jr.status.textContent = STATUS[step]; jr.last = step; }
    jr.day.textContent = day;
  }

  var scrollTicking = false;
  function onScrollFrame() {
    scrollTicking = false;
    var doc = d.documentElement;
    var max = doc.scrollHeight - window.innerHeight;
    if (progressBar) progressBar.style.setProperty('--scroll', max > 0 ? (window.scrollY / max).toFixed(4) : 0);
    if (jr && !reduceMotion) {
      var rect = journey.getBoundingClientRect();
      var headerH = header ? header.offsetHeight : 0;
      var travel = journey.offsetHeight - jr.sticky.offsetHeight;
      if (travel > 0) renderJourney(clamp01((headerH - rect.top) / travel));
    }
  }
  function requestScrollFrame() {
    if (!scrollTicking) { scrollTicking = true; requestAnimationFrame(onScrollFrame); }
  }
  if (progressBar || jr) {
    window.addEventListener('scroll', requestScrollFrame, { passive: true });
    window.addEventListener('resize', requestScrollFrame);
    if (jr && reduceMotion) renderJourney(1);
    onScrollFrame();
  }

  // ---------- Mobile menu ----------
  var toggle = $('.nav-toggle');
  var menu = $('#mobile-menu');
  function setMenu(open) {
    d.body.classList.toggle('menu-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    menu.setAttribute('aria-hidden', String(!open));
  }
  if (toggle && menu) {
    toggle.addEventListener('click', function () { setMenu(!d.body.classList.contains('menu-open')); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    d.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && d.body.classList.contains('menu-open')) { setMenu(false); toggle.focus(); }
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 1140 && d.body.classList.contains('menu-open')) setMenu(false);
    });
  }

  // ---------- Scroll reveal ----------
  $$('[data-reveal], .process-item').forEach(function (el) {
    onVisible(el, function (t) { t.classList.add('in'); });
  });
  if (!hasIO) d.documentElement.classList.add('no-io');

  // ---------- Year stamps & counters ----------
  var year = new Date().getFullYear();
  $$('[data-year]').forEach(function (el) { el.textContent = year; });
  $$('[data-since]').forEach(function (el) {
    var n = year - parseInt(el.getAttribute('data-since'), 10);
    el.setAttribute('data-count', n);
    el.firstChild.nodeValue = n;
  });
  $$('[data-count]').forEach(function (el) {
    var target = parseInt(el.getAttribute('data-count'), 10);
    var textNode = el.firstChild;
    if (reduceMotion || !textNode) return;
    textNode.nodeValue = '0';
    onVisible(el, function () {
      var start = null;
      var dur = 1400;
      function step(ts) {
        if (!start) start = ts;
        var p = Math.min((ts - start) / dur, 1);
        textNode.nodeValue = Math.round((1 - Math.pow(1 - p, 3)) * target);
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  });

  // ---------- Horizontal photo strip ----------
  $$('[data-strip]').forEach(function (wrap) {
    var strip = d.getElementById(wrap.getAttribute('data-strip'));
    if (!strip) return;
    $$('[data-dir]', wrap).forEach(function (btn) {
      btn.addEventListener('click', function () {
        var dir = btn.getAttribute('data-dir') === 'next' ? 1 : -1;
        strip.scrollBy({ left: dir * strip.clientWidth * 0.7, behavior: reduceMotion ? 'auto' : 'smooth' });
      });
    });
  });

  // ---------- FAQ accordion ----------
  $$('.faq-item').forEach(function (item) {
    var q = $('.faq-q', item);
    if (!q) return;
    q.addEventListener('click', function () {
      var open = !item.classList.contains('open');
      $$('.faq-item.open').forEach(function (other) {
        if (other !== item) {
          other.classList.remove('open');
          $('.faq-q', other).setAttribute('aria-expanded', 'false');
        }
      });
      item.classList.toggle('open', open);
      q.setAttribute('aria-expanded', String(open));
    });
  });

  // ---------- Gallery filter + lightbox ----------
  $$('.filters button').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var f = btn.getAttribute('data-filter');
      $$('.filters button').forEach(function (b) {
        b.classList.toggle('active', b === btn);
        b.setAttribute('aria-pressed', String(b === btn));
      });
      $$('.masonry figure').forEach(function (fig) {
        var cats = (fig.getAttribute('data-cat') || '').split(' ');
        fig.hidden = !(f === 'all' || cats.indexOf(f) > -1);
      });
    });
  });

  var lbLinks = $$('[data-lightbox]');
  if (lbLinks.length) {
    var arrow = '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="square" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"/></svg>';
    var lb = d.createElement('div');
    lb.className = 'lightbox';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    lb.setAttribute('aria-label', 'Photo viewer');
    lb.innerHTML =
      '<button class="lb-btn lb-close" aria-label="Close"><svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="square"><path d="M6 6l12 12M18 6L6 18"/></svg></button>' +
      '<button class="lb-btn lb-prev" aria-label="Previous photo">' + arrow + '</button>' +
      '<img alt="">' +
      '<button class="lb-btn lb-next" aria-label="Next photo">' + arrow + '</button>' +
      '<div class="lb-cap"></div>';
    d.body.appendChild(lb);
    var lbImg = $('img', lb);
    var lbCap = $('.lb-cap', lb);
    var current = 0;
    var lastFocus = null;

    function visibleLinks() {
      return lbLinks.filter(function (a) { var fig = a.closest('figure'); return !fig || !fig.hidden; });
    }
    function show(i) {
      var list = visibleLinks();
      if (!list.length) return;
      current = (i + list.length) % list.length;
      var a = list[current];
      var img = $('img', a);
      lbImg.src = a.getAttribute('href');
      lbImg.alt = img ? img.alt : '';
      lbCap.textContent = (a.getAttribute('data-caption') || lbImg.alt) + '  —  ' + (current + 1) + ' / ' + list.length;
    }
    function open(a) {
      lastFocus = d.activeElement;
      show(visibleLinks().indexOf(a));
      lb.classList.add('open');
      d.body.style.overflow = 'hidden';
      $('.lb-close', lb).focus();
    }
    function close() {
      lb.classList.remove('open');
      d.body.style.overflow = '';
      if (lastFocus) lastFocus.focus();
    }
    lbLinks.forEach(function (a) {
      a.addEventListener('click', function (e) { e.preventDefault(); open(a); });
    });
    $('.lb-close', lb).addEventListener('click', close);
    $('.lb-prev', lb).addEventListener('click', function () { show(current - 1); });
    $('.lb-next', lb).addEventListener('click', function () { show(current + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    d.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(current - 1);
      if (e.key === 'ArrowRight') show(current + 1);
    });
    var touchX = null;
    lb.addEventListener('touchstart', function (e) { touchX = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) {
      if (touchX === null) return;
      var dx = e.changedTouches[0].clientX - touchX;
      if (Math.abs(dx) > 50) show(current + (dx < 0 ? 1 : -1));
      touchX = null;
    });
  }

  // ---------- Office map tabs ----------
  var mapFrame = $('.map-frame iframe');
  $$('.map-tabs button').forEach(function (btn) {
    btn.addEventListener('click', function () {
      $$('.map-tabs button').forEach(function (b) {
        b.classList.toggle('active', b === btn);
        b.setAttribute('aria-pressed', String(b === btn));
      });
      mapFrame.src = btn.getAttribute('data-map');
      var mapLink = $('#map-link');
      if (mapLink) mapLink.href = btn.getAttribute('data-link');
      mapFrame.title = btn.getAttribute('data-title');
    });
  });

  // ---------- Shipping calculator (rough estimate only) ----------
  var calc = $('#calc-form');
  if (calc) {
    var baseRates = {
      'General Cargo': 4.5,
      'Containers': 3.8,
      'Vehicles': 6.2,
      'Fragile Goods': 7.0,
      'Oversized / Heavy Cargo': 8.5,
      'Machinery / Equipment': 7.8,
      'Documents': 2.0
    };
    var destMultiplier = {
      'Europe (Belgium, Austria, Holland)': 1,
      'Lagos, Nigeria': 1.6,
      'Rest of World': 2.1
    };
    var MIN_KG = 50;
    var MAX_KG = 30000;
    var weightIn = $('#calc-weight');
    var range = $('#calc-range');
    var amount = $('#calc-amount');
    var cta = $('#calc-cta');
    var bRate = $('#b-rate');
    var bWeight = $('#b-weight');
    var bRoute = $('#b-route');
    var eur = function (n, dp) { return '€' + n.toLocaleString('en-GB', { minimumFractionDigits: dp || 0, maximumFractionDigits: dp || 0 }); };

    // Log-scale slider so small and huge loads are both easy to pick
    function sliderToKg(v) { return Math.round(MIN_KG * Math.pow(MAX_KG / MIN_KG, v / 1000) / 10) * 10; }
    function kgToSlider(kg) { return Math.round(1000 * Math.log(Math.max(kg, MIN_KG) / MIN_KG) / Math.log(MAX_KG / MIN_KG)); }
    function paintRange() { range.style.setProperty('--p', (range.value / 10) + '%'); }

    function update() {
      var cargoEl = $('input[name="cargo"]:checked', calc);
      var destEl = $('input[name="dest"]:checked', calc);
      var w = parseFloat(weightIn.value) || 0;
      var chargeable = Math.max(w, MIN_KG);
      bWeight.textContent = w > 0 ? chargeable.toLocaleString('en-GB') + ' kg' + (w < MIN_KG ? ' (min.)' : '') : '—';
      bRate.textContent = cargoEl ? eur(baseRates[cargoEl.value], 2) + ' / kg' : '—';
      bRoute.textContent = destEl ? '× ' + destMultiplier[destEl.value] : '—';

      if (!cargoEl || !destEl || w <= 0) {
        amount.textContent = '€ —';
        cta.classList.add('disabled');
        cta.setAttribute('aria-disabled', 'true');
        cta.href = 'quote.html';
        return;
      }
      var estimate = chargeable * baseRates[cargoEl.value] * destMultiplier[destEl.value];
      var text = eur(Math.round(estimate));
      if (amount.textContent !== text) {
        amount.textContent = text;
        amount.classList.remove('bump');
        void amount.offsetWidth;
        amount.classList.add('bump');
      }
      cta.classList.remove('disabled');
      cta.removeAttribute('aria-disabled');
      cta.href = 'quote.html?' + [
        'cargo=' + encodeURIComponent(cargoEl.value),
        'destination=' + encodeURIComponent(destEl.value),
        'weight=' + encodeURIComponent(w),
        'estimate=' + encodeURIComponent(text)
      ].join('&');
    }

    range.addEventListener('input', function () { weightIn.value = sliderToKg(range.value); paintRange(); update(); });
    weightIn.addEventListener('input', function () { range.value = kgToSlider(parseFloat(weightIn.value) || MIN_KG); paintRange(); update(); });
    $$('[data-kg]', calc).forEach(function (b) {
      b.addEventListener('click', function () {
        weightIn.value = b.getAttribute('data-kg');
        range.value = kgToSlider(parseFloat(weightIn.value));
        paintRange();
        update();
      });
    });
    calc.addEventListener('change', update);
    calc.addEventListener('submit', function (e) { e.preventDefault(); update(); });
    range.value = kgToSlider(parseFloat(weightIn.value) || 1000);
    paintRange();
    update();
  }

  // ---------- Quote form: prefill from the calculator ----------
  var quoteForm = $('#quote-form');
  if (quoteForm && window.URLSearchParams && location.search) {
    var params = new URLSearchParams(location.search);
    var cargoSel = $('#q-cargo');
    if (params.get('cargo') && cargoSel) cargoSel.value = params.get('cargo');
    if (params.get('destination')) $('#q-destination').value = params.get('destination');
    if (params.get('weight')) {
      $('#q-notes').value = 'Approx. weight: ' + params.get('weight') + ' kg' +
        (params.get('estimate') ? '\nCalculator estimate: ' + params.get('estimate') : '');
    }
  }

  // ---------- Forms: fall back to WhatsApp until Formspree is connected ----------
  $$('form[data-wa]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      if ((form.getAttribute('action') || '').indexOf('YOUR_FORM_ID') === -1) return; // Formspree is live
      e.preventDefault();
      var lines = [form.getAttribute('data-wa'), ''];
      var hasFiles = false;
      new FormData(form).forEach(function (value, key) {
        if (typeof value === 'string') {
          if (value.trim()) lines.push('*' + key + ':* ' + value.trim());
        } else if (value && value.name) {
          hasFiles = true;
        }
      });
      if (hasFiles) lines.push('', '(I have documents to send, attaching them in this chat.)');
      window.open('https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(lines.join('\n')), '_blank', 'noopener');
      toast('Opening WhatsApp with your details. Just hit send.');
    });
  });
})();
