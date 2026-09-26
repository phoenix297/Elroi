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

  // ---------- Scroll progress bar + pinned journey (world route chart) ----------
  var progressBar = $('.scroll-progress');
  var journey = $('#journey');
  var SVGNS = 'http://www.w3.org/2000/svg';
  function svgEl(tag, attrs, parent) {
    var el = d.createElementNS(SVGNS, tag);
    for (var k in attrs) el.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(el);
    return el;
  }
  // chart units: x = (lon + 180) * 10, y = (90 - lat) * 10
  function toXY(ll) { return [(ll[0] + 180) * 10, (90 - ll[1]) * 10]; }
  function clamp01(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function seg(p, a, b) { return clamp01((p - a) / (b - a)); }
  function ease(t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }
  function lerp(a, b, t) { return a + (b - a) * t; }

  // smooth curve through waypoints (Catmull-Rom), sampled into a polyline
  function spline(way, per) {
    var P = way.map(toXY), out = [];
    for (var i = 0; i < P.length - 1; i++) {
      var p0 = P[i - 1] || P[i], p1 = P[i], p2 = P[i + 1], p3 = P[i + 2] || P[i + 1];
      for (var j = 0; j < per; j++) {
        var t = j / per, t2 = t * t, t3 = t2 * t;
        out.push([0, 1].map(function (k) {
          return 0.5 * (2 * p1[k] + (-p0[k] + p2[k]) * t + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t2 + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t3);
        }));
      }
    }
    out.push(P[P.length - 1]);
    return out;
  }
  function curve(a, b, bend, n) {
    var A = toXY(a), B = toXY(b);
    var mx = (A[0] + B[0]) / 2, my = (A[1] + B[1]) / 2;
    var nx = -(B[1] - A[1]) * bend, ny = (B[0] - A[0]) * bend;
    var out = [];
    for (var i = 0; i <= n; i++) {
      var t = i / n, u = 1 - t;
      out.push([u * u * A[0] + 2 * u * t * (mx + nx) + t * t * B[0], u * u * A[1] + 2 * u * t * (my + ny) + t * t * B[1]]);
    }
    return out;
  }
  function Line(pts, parent, cls) {
    this.pts = pts;
    this.cum = [0];
    for (var i = 1; i < pts.length; i++) {
      this.cum.push(this.cum[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
    }
    this.len = this.cum[this.cum.length - 1];
    var all = pts.map(function (q) { return q[0].toFixed(1) + ',' + q[1].toFixed(1); }).join(' ');
    svgEl('polyline', { points: all, 'class': 'jm-route ' + (cls || ''), 'vector-effect': 'non-scaling-stroke' }, parent);
    this.gold = svgEl('polyline', { points: '', 'class': 'jm-gold', 'vector-effect': 'non-scaling-stroke' }, parent);
  }
  // draw the first `f` of the line; returns the head point and heading (degrees)
  Line.prototype.draw = function (f) {
    var target = f * this.len, pts = this.pts, cum = this.cum, out = [], i = 1;
    out.push(pts[0][0].toFixed(1) + ',' + pts[0][1].toFixed(1));
    while (i < pts.length && cum[i] <= target) { out.push(pts[i][0].toFixed(1) + ',' + pts[i][1].toFixed(1)); i++; }
    var head = pts[Math.min(i, pts.length - 1)], prev = pts[Math.max(0, i - 1)];
    if (i < pts.length) {
      var k = (target - cum[i - 1]) / ((cum[i] - cum[i - 1]) || 1);
      head = [lerp(pts[i - 1][0], pts[i][0], k), lerp(pts[i - 1][1], pts[i][1], k)];
      out.push(head[0].toFixed(1) + ',' + head[1].toFixed(1));
    } else { prev = pts[pts.length - 2]; }
    this.gold.setAttribute('points', f > 0 ? out.join(' ') : '');
    var a = pts[Math.min(i, pts.length - 1)];
    var dx = a[0] - prev[0], dy = a[1] - prev[1];
    return { x: head[0], y: head[1], ang: Math.atan2(dy, dx) * 180 / Math.PI };
  };

  var TRUCK_SVG = '<g transform="translate(0 -9)"><rect x="-24" y="-15" width="28" height="17" rx="2" fill="#0B1F35"/><rect x="-22" y="-13" width="24" height="3" fill="#C9A227"/><path d="M5 -11 H14 L21 -4 V2 H5 Z" fill="#0B1F35"/><path d="M9 -9 H13 L17 -5 H9 Z" fill="#8FB0D1"/><circle cx="-16" cy="4" r="3.6" fill="#0B1F35" stroke="#F6F4EE" stroke-width="1.5"/><circle cx="-7" cy="4" r="3.6" fill="#0B1F35" stroke="#F6F4EE" stroke-width="1.5"/><circle cx="13" cy="4" r="3.6" fill="#0B1F35" stroke="#F6F4EE" stroke-width="1.5"/></g>';
  var SHIP_SVG = '<g transform="translate(0 -6)"><path d="M-28 0 H26 L19 11 H-21 Z" fill="#0B1F35"/><path d="M-21 11 H19" stroke="#C9A227" stroke-width="1.5"/><rect x="-20" y="-8" width="8" height="8" fill="#C9A227"/><rect x="-11" y="-8" width="8" height="8" fill="#3E6D9C"/><rect x="-2" y="-8" width="8" height="8" fill="#C9A227"/><rect x="-15" y="-16" width="8" height="8" fill="#3E6D9C"/><rect x="-6" y="-16" width="8" height="8" fill="#E0C468"/><rect x="12" y="-15" width="8" height="15" fill="#0B1F35"/><rect x="14" y="-12" width="4" height="3" fill="#8FB0D1"/></g>';

  var jr = null;
  if (journey && $('#jr-svg')) {
    var ESSEN = [7.01, 51.46], PORT = [4.40, 51.22];
    var CHANNEL = [[4.4, 51.22], [3.2, 51.5], [1.6, 51.05], [-1.5, 50.2], [-5.5, 49.3], [-8.5, 47.5]];
    var ATL = CHANNEL.concat([[-12, 40], [-17, 30], [-19, 20], [-18, 11]]);
    var MED = CHANNEL.concat([[-10.2, 43], [-10, 38], [-6.5, 36], [-3, 36.1], [5, 37.8], [11, 37.6], [15, 35.8], [22, 34.6], [29, 32.2], [32.3, 31.3], [32.6, 29.8], [34, 27.5], [37, 23], [40, 18], [42.6, 14.2], [43.4, 12.6], [46, 12.2], [51.5, 13.5]]);
    var LANES = [
      { label: 'Americas', pos: 'below', way: CHANNEL.concat([[-20, 45.5], [-40, 43.5], [-60, 41], [-74, 40.5]]) },
      { label: 'South America', pos: 'below', way: ATL.concat([[-27, 5], [-33, -6], [-38, -14], [-41, -23.5], [-46.3, -24]]) },
      { label: 'Lagos', pos: 'right', way: ATL.concat([[-12, 5], [-4, 4], [3.4, 6.3]]) },
      { label: 'Southern Africa', pos: 'right', way: ATL.concat([[-10, 0], [0, -15], [10, -28], [18.4, -35.3], [25, -35.5], [31, -30]]) },
      { label: 'Middle East', pos: 'above', way: MED.concat([[58, 17.5], [60, 22.3], [57.5, 25.5], [56.3, 26.4], [55, 25.1]]) },
      { label: 'Asia', pos: 'left', way: MED.concat([[62, 11], [73, 8], [80.5, 5.5], [88, 5.8], [94.5, 6.5], [97.5, 5.8], [100, 3.5], [102.5, 1.8], [104, 1.2], [107, 5], [110, 11], [114, 19], [118.5, 23.5], [122, 27.5], [122, 31]]) }
    ];
    var EUROPE = [
      { label: 'Holland', at: [4.48, 51.92], pos: 'above', bend: 0.18 },
      { label: 'Belgium', at: [4.35, 50.85], pos: 'below', bend: -0.18 },
      { label: 'Austria', at: [16.37, 48.21], pos: 'below', bend: 0.12 }
    ];

    var svg = $('#jr-svg'), lines = $('#jr-lines'), marks = $('#jr-marks'), grid = $('#jr-grid');
    var gd = '';
    for (var glon = -180; glon <= 180; glon += 15) gd += 'M' + ((glon + 180) * 10) + ' 0V1800';
    for (var glat = -75; glat <= 75; glat += 15) gd += 'M0 ' + ((90 - glat) * 10) + 'H3600';
    svgEl('path', { d: gd, 'class': 'jm-grid', 'vector-effect': 'non-scaling-stroke' }, grid);

    var marker = function (ll, cls, label, pos) {
      var xy = toXY(ll);
      var g = svgEl('g', { 'class': 'jm-mark ' + cls }, marks);
      g.innerHTML = (cls.indexOf('hub') > -1 ? '<circle class="jm-ring" r="7"/>' : '') + '<circle class="jm-dot" r="' + (cls.indexOf('hub') > -1 ? 6 : 4.5) + '"/>' +
        (label ? '<text class="jm-label" ' + ({ above: 'x="0" y="-14" text-anchor="middle"', topfar: 'x="0" y="-32" text-anchor="middle"', below: 'x="0" y="24" text-anchor="middle"', left: 'x="-12" y="5" text-anchor="end"', right: 'x="12" y="5"' }[pos || 'right']) + '>' + label + '</text>' : '');
      return { g: g, x: xy[0], y: xy[1] };
    };

    var euroLines = EUROPE.map(function (e) { return new Line(curve(ESSEN, e.at, e.bend, 24), lines, 'jm-road'); });
    var truckLine = new Line(curve(ESSEN, PORT, -0.25, 24), lines, 'jm-road');
    var laneLines = LANES.map(function (l) { return new Line(spline(l.way, 6), lines, 'jm-sea'); });

    var euroMarks = EUROPE.map(function (e) { return marker(e.at, 'jm-eu', e.label, e.pos); });
    var laneMarks = LANES.map(function (l) { return marker(l.way[l.way.length - 1], 'jm-dest', l.label, l.pos); });
    var portMark = marker(PORT, 'jm-port', null);
    var hubMark = marker(ESSEN, 'jm-hub', 'Essen', 'topfar');
    var truck = svgEl('g', { 'class': 'jm-vehicle jm-truck' }, marks);
    truck.innerHTML = TRUCK_SVG;
    var ships = LANES.map(function () { var g = svgEl('g', { 'class': 'jm-vehicle jm-ship' }, marks); g.innerHTML = SHIP_SVG; return g; });

    jr = {
      map: $('#jr-map'), svg: svg, sticky: $('.journey-sticky', journey),
      steps: $$('.journey-step', journey), dots: $$('.journey-dots i', journey),
      status: $('#jr-status', journey), sub: $('#jr-sub', journey),
      euroLines: euroLines, truckLine: truckLine, laneLines: laneLines,
      euroMarks: euroMarks, laneMarks: laneMarks, fixed: [portMark, hubMark],
      truck: truck, ships: ships, last: -1
    };
  }

  var STATUS = ['Quote requested', 'Estimate confirmed', 'Loaded and shipped', 'Delivered worldwide'];
  var SUBS = ['Essen, Germany', 'Major routes: Belgium, Holland, Austria', 'Sea freight to any part of the world', 'Europe · Americas · Africa · Middle East · Asia'];
  var STEP_AT = [0, 0.25, 0.5, 0.8, 1];

  function placeMark(m, k, opacity) {
    m.g.setAttribute('transform', 'translate(' + m.x.toFixed(1) + ' ' + m.y.toFixed(1) + ') scale(' + k.toFixed(4) + ')');
    if (opacity !== undefined) m.g.style.opacity = opacity.toFixed(3);
  }
  function placeVehicle(g, h, k, scale, opacity) {
    var a = h.ang, rot;
    if (Math.cos(a * Math.PI / 180) >= 0) rot = 'rotate(' + Math.max(-35, Math.min(35, a)).toFixed(1) + ')';
    else {
      var t = a - 180;
      while (t < -180) t += 360;
      while (t > 180) t -= 360;
      rot = 'rotate(' + Math.max(-35, Math.min(35, t)).toFixed(1) + ') scale(-1 1)';
    }
    g.setAttribute('transform', 'translate(' + h.x.toFixed(1) + ' ' + h.y.toFixed(1) + ') scale(' + (k * scale).toFixed(4) + ') ' + rot);
    g.style.opacity = opacity.toFixed(3);
  }

  function renderJourney(p) {
    // camera: close on Europe, then pull back to the whole world
    var boxW = jr.map.clientWidth || 1, boxH = jr.map.clientHeight || 1, aspect = boxW / boxH;
    var W0 = Math.max(170, 60 * aspect), W1 = Math.max(aspect < 1.6 ? 2500 : 2950, 960 * aspect);
    var z = ease(seg(p, 0.5, 0.64));
    var W = Math.exp(lerp(Math.log(W0), Math.log(W1), z)), H = W / aspect;
    var cx = lerp(1900, 2020, z), cy = lerp(398, 820, z);
    jr.svg.setAttribute('viewBox', (cx - W / 2).toFixed(1) + ' ' + (cy - H / 2).toFixed(1) + ' ' + W.toFixed(1) + ' ' + H.toFixed(1));
    var k = W / boxW; // chart units per screen pixel: keeps markers a constant on-screen size
    var small = boxW < 600 ? 0.8 : 1;

    var fe = ease(seg(p, 0.2, 0.4));
    jr.euroLines.forEach(function (l) { l.draw(fe); });
    var th = jr.truckLine.draw(ease(seg(p, 0.28, 0.47)));
    placeVehicle(jr.truck, th, k, small, 1 - seg(p, 0.5, 0.55));

    var fs = ease(seg(p, 0.56, 0.9));
    var shipOn = seg(p, 0.5, 0.56) * (1 - seg(p, 0.9, 0.96)); // ships fade once they arrive
    jr.laneLines.forEach(function (l, i) { placeVehicle(jr.ships[i], l.draw(fs), k, 0.7 * small, shipOn); });

    var euroOp = 1 - seg(p, 0.52, 0.6);
    jr.euroMarks.forEach(function (m) { placeMark(m, k, euroOp); });
    var destOp = seg(p, 0.84, 0.92);
    jr.laneMarks.forEach(function (m) { placeMark(m, k, destOp); });
    placeMark(jr.fixed[0], k, 1 - seg(p, 0.55, 0.62));
    placeMark(jr.fixed[1], k);

    var step = p < STEP_AT[1] ? 0 : p < STEP_AT[2] ? 1 : p < STEP_AT[3] ? 2 : 3;
    jr.steps.forEach(function (el, i) {
      el.classList.toggle('is-active', i === step);
      el.classList.toggle('is-done', i < step);
      el.style.setProperty('--fill', i < step ? 1 : i > step ? 0 : seg(p, STEP_AT[i], STEP_AT[i + 1]).toFixed(3));
    });
    jr.dots.forEach(function (el, i) { el.classList.toggle('on', i <= step); });
    if (step !== jr.last) {
      jr.status.textContent = STATUS[step];
      jr.sub.textContent = SUBS[step];
      jr.last = step;
    }
  }

  var journeyP = 0;
  var scrollTicking = false;
  function onScrollFrame() {
    scrollTicking = false;
    var doc = d.documentElement;
    var max = doc.scrollHeight - window.innerHeight;
    if (progressBar) progressBar.style.setProperty('--scroll', max > 0 ? (window.scrollY / max).toFixed(4) : 0);
    if (jr) {
      if (reduceMotion) journeyP = 1;
      else {
        var rect = journey.getBoundingClientRect();
        var headerH = header ? header.offsetHeight : 0;
        var travel = journey.offsetHeight - jr.sticky.offsetHeight;
        journeyP = travel > 0 ? clamp01((headerH - rect.top) / travel) : 1;
      }
      renderJourney(journeyP);
    }
  }
  function requestScrollFrame() {
    if (!scrollTicking) { scrollTicking = true; requestAnimationFrame(onScrollFrame); }
  }
  if (progressBar || jr) {
    window.addEventListener('scroll', requestScrollFrame, { passive: true });
    window.addEventListener('resize', requestScrollFrame);
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

  // ---------- Scroll reveal: fade in on enter, fade out on leave (both directions) ----------
  if (hasIO) {
    var revealIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) { entry.target.classList.toggle('in', entry.isIntersecting); });
    }, { threshold: 0, rootMargin: '-6% 0px -8% 0px' });
    $$('[data-reveal], .process-item').forEach(function (el) { revealIO.observe(el); });
  } else {
    d.documentElement.classList.add('no-io');
    $$('[data-reveal], .process-item').forEach(function (el) { el.classList.add('in'); });
  }

  // ---------- Headline word reveal (replays when scrolled back to) ----------
  if (hasIO && !reduceMotion) {
    var splitWords = function (el) {
      var walker = d.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
      var texts = [];
      while (walker.nextNode()) texts.push(walker.currentNode);
      var n = 0;
      texts.forEach(function (tn) {
        var frag = d.createDocumentFragment();
        tn.nodeValue.split(/(\s+)/).forEach(function (part) {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.appendChild(d.createTextNode(part)); return; }
          var w = d.createElement('span');
          w.className = 'w';
          var wi = d.createElement('span');
          wi.className = 'wi';
          wi.textContent = part;
          wi.style.setProperty('--wi', n++);
          w.appendChild(wi);
          frag.appendChild(w);
        });
        tn.parentNode.replaceChild(frag, tn);
      });
      el.classList.add('wsplit');
    };
    var wordIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) { entry.target.classList.toggle('words-in', entry.isIntersecting); });
    }, { threshold: 0.15 });
    $$('.section-head h2, .why-sticky h2, .cta h2, .journey-head h2, .coverage-grid h2, .split > div > h2, .page-hero h1, .statement blockquote, .values').forEach(function (el) {
      if (el.closest('.hero')) return;
      splitWords(el);
      wordIO.observe(el);
    });
  }

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

  // ---------- Office maps (Essen / Lagos tabs; one or more per page) ----------
  $$('[data-map-block]').forEach(function (block) {
    var frame = $('.map-frame iframe', block);
    var link = $('.map-link', block);
    var tabs = $$('.map-tabs button', block);
    tabs.forEach(function (btn) {
      btn.addEventListener('click', function () {
        tabs.forEach(function (b) {
          b.classList.toggle('active', b === btn);
          b.setAttribute('aria-pressed', String(b === btn));
        });
        frame.src = btn.getAttribute('data-map');
        frame.title = btn.getAttribute('data-title');
        if (link) link.href = btn.getAttribute('data-link');
      });
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
    if (params.get('weight') && $('#q-weight')) $('#q-weight').value = params.get('weight');
    if (params.get('estimate')) $('#q-notes').value = 'Calculator estimate: ' + params.get('estimate');
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
