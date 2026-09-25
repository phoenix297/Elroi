/* EL-ROI Shipping — interactive 3D route globe.
   Dependency-free canvas renderer: land dots (assets/globe-land.js), graticule,
   great-circle shipping arcs from Essen with travelling pulses, drag to rotate.
   Mounts on any element with [data-globe]. */
(function () {
  'use strict';

  var DEG = Math.PI / 180;
  var GOLD = '224, 196, 104';
  var GOLD_DEEP = '201, 162, 39';
  var STEEL = '143, 176, 209';
  var IVORY = '246, 244, 238';

  var HUB = { name: 'Essen', lat: 51.4556, lon: 7.0116 };
  // Major routes (Europe) in gold; worldwide destinations show "any part of the world"
  var ROUTES = [
    { name: 'Antwerp', lat: 51.2194, lon: 4.4025, kind: 'main' },
    { name: 'Rotterdam', lat: 51.9244, lon: 4.4777, kind: 'main' },
    { name: 'Vienna', lat: 48.2082, lon: 16.3738, kind: 'main', label: 'Europe' },
    { name: 'Lagos', lat: 6.4474, lon: 3.3903, kind: 'world', label: 'Lagos' },
    { name: 'New York', lat: 40.7128, lon: -74.006, kind: 'world', label: 'Americas' },
    { name: 'Santos', lat: -23.9608, lon: -46.3336, kind: 'world' },
    { name: 'Durban', lat: -29.8587, lon: 31.0218, kind: 'world', label: 'Africa' },
    { name: 'Dubai', lat: 25.0112, lon: 55.0610, kind: 'world', label: 'Middle East' },
    { name: 'Shanghai', lat: 31.2304, lon: 121.4737, kind: 'world', label: 'Asia' }
  ];
  var STYLE = {
    main: { rgb: GOLD, width: 2, alpha: 0.95, pulse: 3.2 },
    world: { rgb: STEEL, width: 1.3, alpha: 0.75, pulse: 5.5 }
  };

  function vec(lat, lon) {
    var cl = Math.cos(lat * DEG);
    return [cl * Math.sin(lon * DEG), Math.sin(lat * DEG), cl * Math.cos(lon * DEG)];
  }

  // Great-circle path between two unit vectors, lifted off the surface mid-way
  function arcPath(a, b, steps) {
    var dot = Math.max(-1, Math.min(1, a[0] * b[0] + a[1] * b[1] + a[2] * b[2]));
    var ang = Math.acos(dot);
    var sinA = Math.sin(ang) || 1e-6;
    var lift = 0.03 + 0.32 * (ang / Math.PI);
    var pts = [];
    for (var i = 0; i <= steps; i++) {
      var t = i / steps;
      var wa = Math.sin((1 - t) * ang) / sinA;
      var wb = Math.sin(t * ang) / sinA;
      var h = 1 + lift * Math.sin(Math.PI * t);
      pts.push([(a[0] * wa + b[0] * wb) * h, (a[1] * wa + b[1] * wb) * h, (a[2] * wa + b[2] * wb) * h]);
    }
    return pts;
  }

  function decodeLand() {
    var b64 = window.ELROI_LAND || '';
    var bin = atob(b64);
    var bytes = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    var ints = new Int16Array(bytes.buffer);
    var n = ints.length / 2;
    var out = new Float32Array(n * 3);
    for (var j = 0; j < n; j++) {
      var v = vec(ints[j * 2] / 100, ints[j * 2 + 1] / 100);
      out[j * 3] = v[0]; out[j * 3 + 1] = v[1]; out[j * 3 + 2] = v[2];
    }
    return out;
  }

  function graticule() {
    var lines = [];
    var lat, lon, pts;
    for (lat = -60; lat <= 60; lat += 30) {
      pts = [];
      for (lon = -180; lon <= 180; lon += 4) pts.push(vec(lat, lon));
      lines.push(pts);
    }
    for (lon = -180; lon < 180; lon += 30) {
      pts = [];
      for (lat = -80; lat <= 80; lat += 4) pts.push(vec(lat, lon));
      lines.push(pts);
    }
    return lines;
  }

  function wrap(a) {
    while (a > Math.PI) a -= 2 * Math.PI;
    while (a < -Math.PI) a += 2 * Math.PI;
    return a;
  }

  function mount(host) {
    if (host.__globe) return;
    host.__globe = true;
    var canvas = document.createElement('canvas');
    canvas.className = 'globe-canvas';
    host.appendChild(canvas);
    var ctx = canvas.getContext('2d');
    if (!ctx) return;

    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var land = decodeLand();
    var grid = graticule();
    var hubV = vec(HUB.lat, HUB.lon);
    var routes = ROUTES.map(function (r, i) {
      var v = vec(r.lat, r.lon);
      var ang = Math.acos(Math.max(-1, Math.min(1, hubV[0] * v[0] + hubV[1] * v[1] + hubV[2] * v[2])));
      return { r: r, v: v, path: arcPath(hubV, v, ang < 0.2 ? 24 : 72), delay: 0.25 + i * 0.14, phase: i * 0.29 };
    });

    var W = 0, H = 0, R = 0, cx = 0, cy = 0, dpr = 1;
    var CENTER_LON = 12 * DEG;
    var yaw = CENTER_LON - 0.9, pitch = 26 * DEG;
    var vYaw = 0, vPitch = 0;
    var dragging = false, lastX = 0, lastY = 0, lastInteract = -1e9;
    var start = performance.now();
    var running = false, visible = true, raf = 0;
    var cy2, sy2, cyaw, syaw;

    function resize() {
      var rect = host.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = Math.max(1, Math.round(rect.width));
      H = Math.max(1, Math.round(rect.height || rect.width));
      canvas.width = W * dpr;
      canvas.height = H * dpr;
      canvas.style.width = W + 'px';
      canvas.style.height = H + 'px';
      R = Math.min(W, H) * 0.4;
      cx = W / 2;
      cy = H / 2;
      if (!running) draw(performance.now());
    }

    // world vector -> [sx, sy, z, rr] (rr = squared distance from centre in sphere units)
    function project(x, y, z) {
      var x1 = x * cyaw - z * syaw;
      var z1 = x * syaw + z * cyaw;
      var y2 = y * cy2 - z1 * sy2;
      var z2 = y * sy2 + z1 * cy2;
      return [cx + x1 * R, cy - y2 * R, z2, x1 * x1 + y2 * y2];
    }
    function isVisible(p) { return p[2] >= 0 || p[3] > 1; }

    function drawSphere() {
      // atmosphere
      var glow = ctx.createRadialGradient(cx, cy, R * 0.9, cx, cy, R * 1.32);
      glow.addColorStop(0, 'rgba(62, 109, 156, 0.45)');
      glow.addColorStop(0.35, 'rgba(62, 109, 156, 0.16)');
      glow.addColorStop(1, 'rgba(62, 109, 156, 0)');
      ctx.fillStyle = glow;
      ctx.beginPath(); ctx.arc(cx, cy, R * 1.32, 0, Math.PI * 2); ctx.fill();
      // body
      var body = ctx.createRadialGradient(cx - R * 0.35, cy - R * 0.4, R * 0.1, cx, cy, R);
      body.addColorStop(0, '#1B456F');
      body.addColorStop(0.55, '#0F2C4B');
      body.addColorStop(1, '#06121F');
      ctx.fillStyle = body;
      ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2); ctx.fill();
    }

    function drawRim() {
      var rim = ctx.createLinearGradient(cx - R, cy - R, cx + R, cy + R);
      rim.addColorStop(0, 'rgba(' + GOLD + ', 0.55)');
      rim.addColorStop(0.5, 'rgba(' + STEEL + ', 0.25)');
      rim.addColorStop(1, 'rgba(' + STEEL + ', 0.05)');
      ctx.strokeStyle = rim;
      ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2); ctx.stroke();
      // soft terminator shading for depth
      var shade = ctx.createRadialGradient(cx - R * 0.3, cy - R * 0.35, R * 0.4, cx, cy, R * 1.02);
      shade.addColorStop(0, 'rgba(6, 18, 31, 0)');
      shade.addColorStop(1, 'rgba(6, 18, 31, 0.55)');
      ctx.fillStyle = shade;
      ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2); ctx.fill();
    }

    function drawGrid() {
      ctx.strokeStyle = 'rgba(' + STEEL + ', 0.09)';
      ctx.lineWidth = 1;
      for (var l = 0; l < grid.length; l++) {
        var line = grid[l], open = false;
        ctx.beginPath();
        for (var i = 0; i < line.length; i++) {
          var p = project(line[i][0], line[i][1], line[i][2]);
          if (p[2] > 0) {
            if (open) ctx.lineTo(p[0], p[1]); else { ctx.moveTo(p[0], p[1]); open = true; }
          } else open = false;
        }
        ctx.stroke();
      }
    }

    function drawLand() {
      var buckets = [[], [], [], [], []];
      var n = land.length / 3;
      for (var i = 0; i < n; i++) {
        var p = project(land[i * 3], land[i * 3 + 1], land[i * 3 + 2]);
        if (p[2] <= 0.02) continue;
        var b = Math.min(4, Math.floor(p[2] * 5));
        buckets[b].push(p[0], p[1], p[2]);
      }
      var base = Math.max(0.9, R / 190);
      for (var k = 0; k < 5; k++) {
        var arr = buckets[k];
        if (!arr.length) continue;
        var depth = (k + 0.5) / 5;
        ctx.fillStyle = 'rgba(' + (depth > 0.55 ? GOLD : STEEL) + ', ' + (0.22 + 0.7 * depth).toFixed(3) + ')';
        ctx.beginPath();
        var r = base * (0.55 + 0.45 * depth);
        for (var j = 0; j < arr.length; j += 3) {
          ctx.moveTo(arr[j] + r, arr[j + 1]);
          ctx.arc(arr[j], arr[j + 1], r, 0, Math.PI * 2);
        }
        ctx.fill();
      }
    }

    function strokePath(pts, from, to, rgb, alpha, width) {
      ctx.strokeStyle = 'rgba(' + rgb + ', ' + alpha + ')';
      ctx.lineWidth = width;
      ctx.lineCap = 'round';
      ctx.beginPath();
      var open = false;
      var n = pts.length - 1;
      var i0 = Math.max(0, Math.floor(from * n)), i1 = Math.min(n, Math.ceil(to * n));
      for (var i = i0; i <= i1; i++) {
        var p = project(pts[i][0], pts[i][1], pts[i][2]);
        if (isVisible(p)) {
          if (open) ctx.lineTo(p[0], p[1]); else { ctx.moveTo(p[0], p[1]); open = true; }
        } else open = false;
      }
      ctx.stroke();
    }

    function drawRoutes(t) {
      for (var i = 0; i < routes.length; i++) {
        var rt = routes[i], st = STYLE[rt.r.kind];
        var grow = reduce ? 1 : Math.min(1, Math.max(0, (t - rt.delay) / 1.4));
        grow = 1 - Math.pow(1 - grow, 3);
        if (grow <= 0) continue;
        strokePath(rt.path, 0, grow, st.rgb, st.alpha * 0.55, st.width);
        ctx.setLineDash([]);
        if (grow < 1 || reduce) continue;
        // travelling pulse
        var head = ((t / st.pulse) + rt.phase) % 1;
        var tail = Math.max(0, head - 0.16);
        for (var s = 0; s < 4; s++) {
          var a = tail + (head - tail) * (s / 4);
          strokePath(rt.path, a, head, st.rgb, 0.18 + 0.2 * s, st.width + 0.6 + s * 0.35);
        }
        var hp = rt.path[Math.round(head * (rt.path.length - 1))];
        var pp = project(hp[0], hp[1], hp[2]);
        if (isVisible(pp)) {
          ctx.fillStyle = 'rgba(' + st.rgb + ', 1)';
          ctx.beginPath(); ctx.arc(pp[0], pp[1], st.width + 1, 0, Math.PI * 2); ctx.fill();
        }
      }
    }

    function marker(v, rgb, size, label, t, ring, align) {
      var p = project(v[0], v[1], v[2]);
      if (p[2] <= 0) return;
      var fade = Math.min(1, p[2] * 3);
      if (ring && !reduce) {
        var k = (t % 2.4) / 2.4;
        ctx.strokeStyle = 'rgba(' + rgb + ', ' + (0.7 * (1 - k) * fade).toFixed(3) + ')';
        ctx.lineWidth = 1.2;
        ctx.beginPath(); ctx.arc(p[0], p[1], size + k * 16, 0, Math.PI * 2); ctx.stroke();
      }
      ctx.fillStyle = 'rgba(6, 18, 31, ' + fade + ')';
      ctx.beginPath(); ctx.arc(p[0], p[1], size + 2, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = 'rgba(' + rgb + ', ' + fade + ')';
      ctx.beginPath(); ctx.arc(p[0], p[1], size, 0, Math.PI * 2); ctx.fill();
      if (label) {
        ctx.font = '600 ' + Math.max(10, Math.round(R / 22)) + 'px Inter, system-ui, sans-serif';
        ctx.textBaseline = 'middle';
        ctx.textAlign = align === 'left' ? 'right' : align === 'top' ? 'center' : 'left';
        var dx = align === 'left' ? -(size + 8) : align === 'top' ? 0 : size + 8;
        var dy = align === 'top' ? -(size + 12) : 0;
        ctx.fillStyle = 'rgba(6, 18, 31, ' + (0.6 * fade) + ')';
        ctx.fillText(label.toUpperCase(), p[0] + dx + 1, p[1] + dy + 1);
        ctx.fillStyle = 'rgba(' + rgb + ', ' + fade + ')';
        ctx.fillText(label.toUpperCase(), p[0] + dx, p[1] + dy);
      }
    }

    function draw(now) {
      var t = (now - start) / 1000;
      // idle motion: a slow swing centred on Europe/Africa so the Essen hub stays in play
      if (!dragging) {
        yaw += vYaw; pitch += vPitch;
        vYaw *= 0.94; vPitch *= 0.94;
        if (!reduce && now - lastInteract > 2500) {
          var targetYaw = CENTER_LON + Math.sin(t * 0.26) * 0.95;
          yaw += wrap(targetYaw - yaw) * 0.02;
          pitch += (26 * DEG - pitch) * 0.02;
        }
      }
      pitch = Math.max(-35 * DEG, Math.min(65 * DEG, pitch));
      cyaw = Math.cos(yaw); syaw = Math.sin(yaw);
      cy2 = Math.cos(pitch); sy2 = Math.sin(pitch);

      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);
      var intro = reduce ? 1 : Math.min(1, t / 1.2);
      ctx.globalAlpha = 1 - Math.pow(1 - intro, 3);
      drawSphere();
      drawGrid();
      drawLand();
      drawRim();
      drawRoutes(t);
      for (var i = 0; i < routes.length; i++) {
        var r = routes[i].r;
        var col = r.kind === 'main' ? GOLD : STEEL;
        marker(routes[i].v, col, r.kind === 'main' ? 3.2 : 2.8, r.label, t, !!r.label, r.lon < -20 ? 'left' : 'right');
      }
      marker(hubV, GOLD, 5, HUB.name, t + 1.2, true, 'top');
      ctx.globalAlpha = 1;
    }

    function loop(now) {
      draw(now);
      raf = running ? requestAnimationFrame(loop) : 0;
    }
    function play() {
      if (running || reduce) return;
      running = true;
      raf = requestAnimationFrame(loop);
    }
    function pause() { running = false; if (raf) cancelAnimationFrame(raf); raf = 0; }
    function sync() { if (visible && !document.hidden) play(); else pause(); }

    // drag to rotate (horizontal on touch so the page can still scroll vertically)
    canvas.addEventListener('pointerdown', function (e) {
      dragging = true; lastX = e.clientX; lastY = e.clientY;
      vYaw = vPitch = 0;
      canvas.setPointerCapture(e.pointerId);
      host.classList.add('is-dragging');
    });
    canvas.addEventListener('pointermove', function (e) {
      if (!dragging) return;
      var k = 1 / (R * 1.1);
      var dx = (e.clientX - lastX) * k, dy = (e.clientY - lastY) * k;
      lastX = e.clientX; lastY = e.clientY;
      yaw -= dx; pitch += dy;
      vYaw = -dx; vPitch = dy;
      lastInteract = performance.now();
      if (!running) draw(performance.now());
    });
    function endDrag() {
      dragging = false;
      lastInteract = performance.now();
      host.classList.remove('is-dragging');
    }
    canvas.addEventListener('pointerup', endDrag);
    canvas.addEventListener('pointercancel', endDrag);

    if ('ResizeObserver' in window) new ResizeObserver(resize).observe(host);
    else window.addEventListener('resize', resize);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) { visible = entries[0].isIntersecting; sync(); }).observe(host);
    }
    document.addEventListener('visibilitychange', sync);
    resize();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { if (!running) draw(performance.now()); });
    sync();
    host.classList.add('is-ready');
  }

  function init() {
    Array.prototype.forEach.call(document.querySelectorAll('[data-globe]'), mount);
  }
  window.ElroiGlobe = { mount: mount };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
