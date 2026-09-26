#!/usr/bin/env python3
"""Generates the static EL-ROI pages (luxury navy/gold theme) with a shared header/footer."""
import os, re

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # the site root (parent of _build/)
HERE = os.path.dirname(os.path.abspath(__file__))

PHONE = '+49 1521 9521826'
TEL = '+4915219521826'
WA = 'https://wa.me/4915219521826'
EMAIL = 'info@elroishipping.de'
FORMSPREE = 'https://formspree.io/f/YOUR_FORM_ID'
MAPS_ESSEN = 'https://www.google.com/maps/search/?api=1&amp;query=Ripshorster+Str.+379,+45357+Essen,+Germany'
MAPS_LAGOS = 'https://www.google.com/maps/search/?api=1&amp;query=Olodi+Apapa,+Lagos,+Nigeria'
EMBED_ESSEN = 'https://maps.google.com/maps?q=Ripshorster%20Str.%20379%2C%2045357%20Essen%2C%20Germany&amp;z=15&amp;output=embed'
EMBED_LAGOS = 'https://maps.google.com/maps?q=Olodi%20Apapa%2C%20Lagos%2C%20Nigeria&amp;z=14&amp;output=embed'

IMG = {
    'transporter': ('assets/img/car-transporter.webp', 'Car transporter loaded with two trucks for export', 1280, 720),
    'tractor': ('assets/img/tractor-john-deere.webp', 'Green John Deere tractor in a yard, being prepared for shipping', 1280, 720),
    'volvo': ('assets/img/truck-volvo-fh.webp', 'Rear view of a red Volvo FH tractor unit', 960, 1280),
    'chassis': ('assets/img/container-chassis-schmitz.webp', 'Blue Schmitz container chassis trailer', 1280, 960),
    'loading': ('assets/img/container-loading.webp', 'Inside a shipping container during loading', 1280, 963),
    'volvofront': ('assets/img/truck-volvo-front.webp', 'Front of a red Volvo FH tractor unit', 960, 1280),
    'chassisrear': ('assets/img/chassis-schmitz-rear.webp', 'Rear of a Schmitz tri-axle container chassis', 1280, 960),
    'deere3140': ('assets/img/tractor-john-deere-3140.webp', 'John Deere 3140 tractor with front loader', 1280, 720),
    'van': ('assets/img/van-mercedes.webp', 'Blue Mercedes-Benz van ready for export', 1280, 719),
    'msc': ('assets/img/container-msc-40ft.webp', 'Yellow 40ft shipping container on a trailer', 1280, 720),
    'loaded': ('assets/img/transporter-loaded.webp', 'Transporter loaded with a van and a truck for export', 1280, 720),
    'vanload': ('assets/img/container-van-loading.webp', 'A van loaded inside a shipping container', 1280, 719),
    'redchassis': ('assets/img/chassis-van-moer.webp', 'Red tri-axle container chassis in a yard', 1280, 960),
    'yardload': ('assets/img/container-yard-loading.webp', 'Loading cargo into an open container', 720, 1280),
    'engines': ('assets/img/container-engines-night.webp', 'Loading engines into a container at night', 719, 1280),
    'carsload': ('assets/img/container-cars-loading.webp', 'Wrapped cars strapped inside a container during loading', 719, 1280),
    'enginesclose': ('assets/img/container-engines-closeup.webp', 'Engines and parts packed tightly into a container', 719, 1280),
}

import hashlib


def ver(path):
    """Short content hash so browsers never pair a new page with a cached old asset."""
    with open(os.path.join(OUT, path), 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()[:10]


# Public address of the site: change this when the custom domain is live
SITE_URL = 'https://elroishipping.de/'
LASTMOD = '2026-09-26'
FONTS_URL = 'assets/fonts.css?v=' + ver('assets/fonts.css')
FONT_FR = next(f for f in os.listdir(os.path.join(OUT, 'assets/fonts')) if f.startswith('fraunces-normal-latin-') and '-ext-' not in f)
FONT_IN = next(f for f in os.listdir(os.path.join(OUT, 'assets/fonts')) if f.startswith('inter-normal-latin-') and '-ext-' not in f)
CSS_URL = 'assets/style.css?v=' + ver('assets/style.css')
JS_URL = 'assets/script.js?v=' + ver('assets/script.js')
GLOBE_URL = 'assets/globe.js?v=' + ver('assets/globe.js')
LAND_URL = 'assets/globe-land.js?v=' + ver('assets/globe-land.js')

WA_PATH = 'M17.6 6.32A7.85 7.85 0 0 0 12.05 4a7.94 7.94 0 0 0-6.9 11.9L4 20l4.2-1.1a7.9 7.9 0 0 0 3.85 1h0a7.94 7.94 0 0 0 7.94-7.94 7.9 7.9 0 0 0-2.4-5.64Zm-5.55 12.2h0a6.6 6.6 0 0 1-3.36-.92l-.24-.14-2.5.66.67-2.44-.16-.25a6.6 6.6 0 1 1 12.24-3.5 6.56 6.56 0 0 1-6.65 6.59Zm3.6-4.93c-.2-.1-1.17-.58-1.35-.64-.18-.07-.31-.1-.44.1-.13.19-.5.64-.62.77-.11.13-.23.14-.42.05-.2-.1-.83-.3-1.58-.97-.58-.52-.98-1.16-1.09-1.36-.11-.19 0-.3.09-.4.09-.09.2-.23.3-.35.1-.11.13-.19.2-.32.06-.13.03-.24-.02-.34-.05-.1-.44-1.06-.6-1.45-.16-.38-.32-.33-.44-.33-.11 0-.24-.01-.37-.01-.13 0-.34.05-.52.24-.18.19-.68.66-.68 1.62 0 .95.7 1.87.8 2 .1.13 1.37 2.1 3.33 2.94.46.2.83.32 1.11.41.47.15.9.13 1.23.08.38-.06 1.17-.48 1.33-.94.16-.46.16-.86.11-.94-.05-.09-.18-.14-.38-.24Z'
ARROW = '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"/></svg>'
WA_ICON = f'<svg class="wa-ico" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="{WA_PATH}"/></svg>'
PHONE_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>'
MAIL_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M3 5h18v14H3z"/><path d="M3 6l9 7 9-7"/></svg>'
LOGO_MARK = ('<svg class="logo-mark" viewBox="0 0 44 44" aria-hidden="true">'
             '<circle cx="22" cy="22" r="21" fill="none" stroke="#C9A227" stroke-width="1"/>'
             '<circle cx="22" cy="22" r="17.5" fill="none" stroke="#C9A227" stroke-width=".5" opacity=".55"/>'
             '<text x="22" y="27.2" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="15" font-style="italic" fill="#E0C468">ER</text></svg>')
LOGO = f'{LOGO_MARK}<span class="logo-text"><span class="logo-name">EL-ROI <em>Shipping</em></span><span class="logo-sub">Freight &amp; Logistics &middot; Est. 1999</span></span>'

ICONS = {
    'box': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"><path d="M3 7.5 12 3l9 4.5v9L12 21l-9-4.5z"/><path d="M3 7.5 12 12l9-4.5M12 12v9"/></svg>',
    'container': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="2.5" y="6" width="19" height="12"/><path d="M7 8.5v7M10.5 8.5v7M14 8.5v7M17.5 8.5v7"/></svg>',
    'gear': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="12" r="3.2"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M5.3 18.7l2.1-2.1M16.6 7.4l2.1-2.1"/></svg>',
    'fragile': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"><path d="M7.5 3h9l-.8 6.2a3.7 3.7 0 0 1-7.4 0z"/><path d="M12 13v7M8 21h8"/></svg>',
    'doc': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"><path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/></svg>',
}

NAV = [
    ('index.html', 'Home'),
    ('about.html', 'About'),
    ('services.html', 'Services'),
    ('routes.html', 'Routes'),
    ('gallery.html', 'Gallery'),
    ('blog.html', 'Guides'),
    ('faq.html', 'FAQ'),
    ('contact.html', 'Contact'),
]
MOBILE_NAV = NAV[:5] + [('calculator.html', 'Calculator'), ('book.html', 'Book a Shipment')] + NAV[5:] + [('quote.html', 'Get a Quote')]


def img(key, eager=False):
    src, alt, w, h = IMG[key]
    return f'<img src="{src}" alt="{alt}" width="{w}" height="{h}" loading="{"eager" if eager else "lazy"}" decoding="async">'


def head(title, desc, page='', ld='', noindex=False):
    alternates = '' if (page.startswith('guide-') or noindex) else f'\n<link rel="alternate" hreflang="en" href="{SITE_URL}{page}">\n<link rel="alternate" hreflang="de" href="{SITE_URL}de/{page}">\n<link rel="alternate" hreflang="x-default" href="{SITE_URL}{page}">'
    robots = '<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">{'<base href="/">' if noindex else ''}
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0B1F35">
{robots}
<link rel="canonical" href="{SITE_URL}{page}">{alternates}
<meta property="og:type" content="website">
<meta property="og:site_name" content="EL-ROI Shipping Services">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<meta property="og:url" content="{SITE_URL}{page}">
<meta property="og:image" content="{SITE_URL}assets/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="EL-ROI Shipping: Germany to any part of the world">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="assets/fonts/{FONT_FR}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/{FONT_IN}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{FONTS_URL}">
<link rel="stylesheet" href="{CSS_URL}">
<script>document.documentElement.className += ' js';</script>
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="scroll-progress" aria-hidden="true"></div>
'''


def header(active, name=''):
    de_href = 'de/' + (name if name and not name.startswith('guide-') else ('blog.html' if name.startswith('guide-') else 'index.html'))
    lang_switch = f'<div class="lang-switch" role="group" aria-label="Language"><a class="on" href="{name or "index.html"}" hreflang="en" lang="en" data-lang="en">EN</a><a href="{de_href}" hreflang="de" lang="de" data-lang="de">DE</a></div>'
    act = ' class="active" aria-current="page"'
    links = '\n      '.join(f'<a href="{h}"{act if h == active else ""}>{t}</a>' for h, t in NAV)
    mlinks = '\n    '.join(f'<a href="{h}"{act if h == active else ""}><span>{i + 1:02d}</span>{t}</a>' for i, (h, t) in enumerate(MOBILE_NAV))
    return f'''<div class="topbar">
  <div class="container">
    <div class="tb-left"><span>Ripshorster Str. 379, Essen</span><span>Olodi Apapa, Lagos</span></div>
    <div class="tb-right"><a href="tel:{TEL}">{PHONE}</a><a class="hide-sm" href="mailto:{EMAIL}">Email us</a><a class="tb-wa" href="{WA}" target="_blank" rel="noopener">WhatsApp</a></div>
  </div>
</div>
<header class="site">
  <div class="container nav-wrap">
    <a href="index.html" class="logo" aria-label="EL-ROI Shipping Services home">{LOGO}</a>
    <nav class="primary" aria-label="Primary">
      {links}
    </nav>
    <div class="nav-end">
      {lang_switch}
      <a href="quote.html" class="btn btn-primary btn-sm">Get a Quote</a>
      <button class="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu"><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu" aria-hidden="true">
  <nav aria-label="Mobile">
    {mlinks}
  </nav>
  <div class="mm-foot">
    {lang_switch}
    <a class="btn btn-primary btn-block" href="{WA}" target="_blank" rel="noopener">{WA_ICON} Chat on WhatsApp</a>
    <a class="btn btn-ghost btn-block" href="tel:{TEL}">Call {PHONE}</a>
    <small>Essen, Germany &middot; Lagos, Nigeria</small>
  </div>
</div>
'''


import json
SITEMAP = []
BUSINESS_LD = {
    '@context': 'https://schema.org',
    '@type': 'LocalBusiness',
    '@id': SITE_URL + '#business',
    'name': 'EL-ROI Shipping Services',
    'alternateName': 'EL-ROI Shipping',
    'description': 'Freight forwarder in Essen, Germany since 1999. Sea freight for vehicles, trucks, tractors, 20ft and 40ft containers, machinery and general cargo from Germany to any part of the world, with major routes to Belgium, Austria and Holland and an office in Lagos, Nigeria.',
    'url': SITE_URL,
    'image': SITE_URL + 'assets/og-image.jpg',
    'logo': SITE_URL + 'assets/favicon.svg',
    'telephone': '+49 1521 9521826',
    'email': EMAIL,
    'foundingDate': '1999',
    'slogan': 'Your satisfaction, our priority',
    'address': {'@type': 'PostalAddress', 'streetAddress': 'Ripshorster Str. 379', 'postalCode': '45357', 'addressLocality': 'Essen', 'addressRegion': 'Nordrhein-Westfalen', 'addressCountry': 'DE'},
    'hasMap': 'https://www.google.com/maps/search/?api=1&query=Ripshorster+Str.+379,+45357+Essen,+Germany',
    'areaServed': ['Germany', 'Belgium', 'Austria', 'Netherlands', 'Nigeria', 'Worldwide'],
    'knowsAbout': ['Sea freight', 'Container shipping', 'Vehicle shipping', 'Car export from Germany', 'Shipping to Nigeria', 'Form M', 'Heavy machinery shipping'],
    'department': [{'@type': 'LocalBusiness', 'name': 'EL-ROI Shipping Services Lagos', 'telephone': '+49 1521 9521826',
                    'address': {'@type': 'PostalAddress', 'streetAddress': 'Olodi Apapa', 'addressLocality': 'Lagos', 'addressCountry': 'NG'}}],
    'contactPoint': [{'@type': 'ContactPoint', 'telephone': '+49 1521 9521826', 'contactType': 'customer service', 'availableLanguage': ['English', 'German']}],
}
SEO = {
    'index.html': ('Shipping from Germany to Nigeria & Worldwide | EL-ROI Shipping, Essen',
                   'Freight forwarder in Essen since 1999. Sea freight for cars, trucks, tractors, containers and machinery from Germany to Europe, Lagos and any part of the world. Honest quotes.'),
    'about.html': ('About Us: Freight Forwarder in Essen since 1999 | EL-ROI Shipping',
                   'EL-ROI Shipping Services: a German freight forwarder in Essen with an office in Lagos. Over 20 years of honest estimates, fair pricing and clear communication.'),
    'services.html': ('Car, Truck, Tractor & Container Shipping from Germany | EL-ROI Shipping',
                      'Ship vehicles, trucks, tractors, 20ft and 40ft containers, machinery, fragile goods and documents by sea from Germany, with documents and Form M handled.'),
    'routes.html': ('Shipping Routes from Germany: Europe, Lagos & Worldwide | EL-ROI',
                    'Sea freight from Essen, Germany: major routes to Belgium, Austria and Holland, plus Lagos, Nigeria and any port worldwide. Around two weeks after loading.'),
    'gallery.html': ('Gallery: Vehicles, Trucks & Containers We Ship | EL-ROI Shipping',
                     'Real photos of cars, trucks, tractors, containers and engines loaded and shipped by EL-ROI Shipping Services from Germany.'),
    'blog.html': ('Shipping Guides & News | EL-ROI Shipping',
                  'Practical guides to shipping from Germany: shipping a car to Nigeria, Form M, 20ft vs 40ft containers and what to prepare before booking.'),
    'faq.html': ('Shipping FAQ: Transit Times, Form M, Customs & Documents | EL-ROI',
                 'Answers about shipping from Germany: transit times, cargo types, documents, Form M, customs duties, insurance, container sizes and our offices.'),
    'contact.html': ('Contact EL-ROI Shipping | Essen, Germany & Lagos, Nigeria',
                     'Contact EL-ROI Shipping Services: Ripshorster Str. 379, 45357 Essen, and Olodi Apapa, Lagos. Call +49 1521 9521826 or chat on WhatsApp.'),
    'quote.html': ('Get a Free Shipping Quote from Germany | EL-ROI Shipping',
                   'Request a transparent, no-pressure sea freight quote from Germany for vehicles, containers, machinery or general cargo. No hidden fees.'),
    'book.html': ('Book a Shipment from Germany | EL-ROI Shipping',
                  'Book sea freight from Germany to Europe, Lagos or anywhere in the world. Send your cargo details and we confirm availability and next steps.'),
    'calculator.html': ('Shipping Cost Calculator: Germany to Europe, Lagos & Worldwide | EL-ROI',
                        'Estimate the cost of shipping from Germany by cargo type, weight and destination. Then request a formal quote for the exact price.'),
}


def photo_bg(key, pos='center', strength='strong'):
    """Truck photo behind a navy block, tinted so text stays readable."""
    tint = {'strong': 'rgba(9,26,45,.9), rgba(11,31,53,.78) 55%, rgba(17,51,90,.9)',
            'soft': 'rgba(9,26,45,.84), rgba(11,31,53,.66) 55%, rgba(17,51,90,.84)'}[strength]
    return f'<div class="photo-bg" aria-hidden="true" style="background-image:linear-gradient(160deg, {tint}), url(\'{IMG[key][0]}\');background-position:center, {pos}"></div>'


FOOTER = f'''<footer class="site has-photo">
  {photo_bg("chassis", "center 60%")}
  <div class="container">
    <div class="footer-grid">
      <div>
        <a href="index.html" class="logo" aria-label="EL-ROI Shipping Services home">{LOGO}</a>
        <p>Direct freight forwarding from Germany to destinations worldwide. Honest estimates, fair pricing, clear communication.</p>
      </div>
      <div>
        <h5>Company</h5>
        <ul>
          <li><a href="about.html">About Us</a></li>
          <li><a href="services.html">Services</a></li>
          <li><a href="routes.html">Routes</a></li>
          <li><a href="gallery.html">Gallery</a></li>
          <li><a href="blog.html">Shipping guides</a></li>
        </ul>
      </div>
      <div>
        <h5>Shipping</h5>
        <ul>
          <li><a href="quote.html">Get a Quote</a></li>
          <li><a href="book.html">Book Shipment</a></li>
          <li><a href="calculator.html">Calculator</a></li>
          <li><a href="faq.html">FAQ</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h5>Offices</h5>
        <ul>
          <li><strong>Essen</strong><br>Ripshorster Str. 379<br>45357 Essen, Germany</li>
          <li><strong>Lagos</strong><br>Olodi Apapa, Lagos, Nigeria</li>
          <li><a href="tel:{TEL}">{PHONE}</a></li>
          <li><a class="break" href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span data-year>2026</span> EL-ROI Shipping Services. All rights reserved.</span>
      <span><a href="privacy.html">Privacy Policy</a> &nbsp;&middot;&nbsp; <a href="terms.html">Terms &amp; Conditions</a> &nbsp;&middot;&nbsp; <button type="button" class="linklike" data-consent-open>Cookie settings</button> &nbsp;&middot;&nbsp; <em>Your satisfaction, our priority.</em></span>
    </div>
  </div>
</footer>
<a class="wa-float" href="{WA}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="{WA_PATH}"/></svg></a>
<div class="toast" role="status" aria-live="polite"></div>
<div class="consent" id="consent" role="dialog" aria-labelledby="consent-title" aria-describedby="consent-text" hidden>
  <div class="consent-body">
    <strong id="consent-title">Privacy settings</strong>
    <p id="consent-text">This website sets no cookies of its own. Our office maps come from Google Maps, which can set cookies and receives your IP address. Allow the maps? You can change this any time under &ldquo;Cookie settings&rdquo; at the bottom of the page. <a href="privacy.html#cookies">Privacy Policy</a></p>
  </div>
  <div class="consent-actions">
    <button type="button" class="btn btn-ghost btn-sm" data-consent-decline>Decline</button>
    <button type="button" class="btn btn-primary btn-sm" data-consent-accept>Accept</button>
  </div>
</div>
<script src="{JS_URL}" defer></script>
</body>
</html>
'''

CHART_LAND = open(os.path.join(HERE, 'chart_land.txt')).read()

ROUTE_LINE = '<svg class="route-line" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true"><path vector-effect="non-scaling-stroke" d="M-10 72 C 260 72, 420 18, 720 30 S 1160 76, 1450 22"/></svg>'


def page_hero(crumb, eyebrow, h1, lede, bg, pos='center'):
    return f'''<section class="page-hero">
  <div class="bg" style="background-image:url('{IMG[bg][0]}');background-position:{pos}"></div>
  {ROUTE_LINE}
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">{crumb}</span></nav>
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>
'''


def map_block(extra=''):
    return f'''<div class="container map-block{extra}" data-map-block data-reveal>
    <div class="head-actions" style="margin-bottom:16px">
      <div class="map-tabs" role="group" aria-label="Choose office map" style="margin:0">
        <button class="active" aria-pressed="true" data-map="{EMBED_ESSEN}" data-link="{MAPS_ESSEN}" data-title="Map of the EL-ROI office in Essen, Germany" data-place="Ripshorster Str. 379, 45357 Essen">Essen office</button>
        <button aria-pressed="false" data-map="{EMBED_LAGOS}" data-link="{MAPS_LAGOS}" data-title="Map of the EL-ROI office in Olodi Apapa, Lagos" data-place="Olodi Apapa, Lagos, Nigeria">Lagos office</button>
      </div>
      <a class="link-arrow map-link" href="{MAPS_ESSEN}" target="_blank" rel="noopener">Open in Google Maps {ARROW}</a>
    </div>
    <div class="map-frame">
      <iframe data-src="{EMBED_ESSEN}" title="Map of the EL-ROI office in Essen, Germany" loading="lazy" referrerpolicy="no-referrer-when-downgrade" hidden></iframe>
      <div class="map-consent">
        <div class="mc-inner">
          <svg class="mc-pin" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 22s7-7.2 7-12.5A7 7 0 0 0 5 9.5C5 14.8 12 22 12 22z" fill="#C9A227"/><circle cx="12" cy="9.5" r="2.6" fill="#0B1F35"/></svg>
          <strong class="mc-place">Ripshorster Str. 379, 45357 Essen</strong>
          <p>The map is provided by Google, which can set cookies and receives your IP address. See our <a href="privacy.html#share">Privacy Policy</a>.</p>
          <button type="button" class="btn btn-primary btn-sm" data-consent-accept>Accept and show map</button>
        </div>
      </div>
    </div>
  </div>'''


CTA = f'''<section class="section-alt cta">
  <div class="container" data-reveal>
    <span class="eyebrow">Get started</span>
    <h2>Ready to move <em>your cargo?</em></h2>
    <p>Get a transparent quote, or reach us directly on WhatsApp. The estimate we give you is the price you pay.</p>
    <div class="hero-actions">
      <a href="quote.html" class="btn btn-dark">Request a Quote {ARROW}</a>
      <a href="{WA}" class="btn btn-outline" target="_blank" rel="noopener">{WA_ICON} Chat on WhatsApp</a>
    </div>
    <a class="cta-phone" href="tel:{TEL}">{PHONE}</a>
  </div>
  {map_block(' cta-map')}
</section>
'''

ROUTES_TABLE = '''<table class="route-table">
      <thead><tr><th>Destination</th><th>Method</th><th>Typical transit</th><th></th></tr></thead>
      <tbody>
        <tr><td>Europe<small>Belgium &middot; Austria &middot; Holland</small></td><td>Sea freight</td><td>~2 weeks after loading</td><td><span class="pill">Major route</span></td></tr>
        <tr><td>Worldwide<small>Africa &middot; Americas &middot; Middle East &middot; Asia</small></td><td>Sea freight</td><td>Varies by destination</td><td><span class="pill">Any port</span></td></tr>
        <tr><td>Lagos, Nigeria<small>Our second office, Olodi Apapa</small></td><td>Sea freight</td><td>Varies by schedule</td><td><span class="pill soft">Local office</span></td></tr>
      </tbody>
    </table>
    <p class="table-note">All routes depart from Essen, Germany. Transit times are estimates and depend on port schedules, customs and cargo type.</p>'''


def write(name, title, desc, active, body, preloader=False, scripts='', extra_ld=None, crumbs=None):
    pre = '<div id="preloader" aria-hidden="true"><div class="pl-mark"><span>EL-ROI <em>Shipping</em></span><span class="pl-bar"></span></div></div>\n' if preloader else ''
    if name in ('quote.html', 'book.html', 'contact.html', 'calculator.html', 'faq.html'):
        # forms and tools only fade in, so nothing fades while someone is typing
        body = body.replace(' data-reveal>', ' data-reveal="in">').replace(' data-reveal style', ' data-reveal="in" style')
    if name in SEO:
        title, desc = SEO[name]
    page = '' if name == 'index.html' else name
    blocks = [BUSINESS_LD] if name in ('index.html', 'about.html', 'contact.html') else []
    if name != 'index.html' and name != '404.html':
        blocks.append({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE_URL}] + [
            {'@type': 'ListItem', 'position': i + 2, 'name': n, 'item': SITE_URL + u} for i, (n, u) in enumerate(crumbs or [(title.split(' | ')[0].split(':')[0], name)])]})
    blocks += extra_ld or []
    ld = ''.join('<script type="application/ld+json">' + json.dumps(b, ensure_ascii=False, separators=(',', ':')) + '</script>' for b in blocks)
    if name != '404.html':
        SITEMAP.append((page, name))
    html = head(title, desc, page, ld, noindex=(name == '404.html')) + pre + header(active, name) + '<main id="main">\n' + body + '</main>\n' + FOOTER.replace('<script src="' + JS_URL + '" defer></script>', scripts + '<script src="' + JS_URL + '" defer></script>')
    with open(os.path.join(OUT, name), 'w') as f:
        f.write(html)
    print('wrote', name)


# =====================================================================
# HOME
# =====================================================================

home = f'''<section class="hero dark">
  <!-- Live background: the photo drifts slowly (Ken Burns). To use a real video instead,
       put an MP4 in assets/video/ and set data-video="assets/video/hero.mp4" below. -->
  <div class="hero-media" data-video="" aria-hidden="true">
    <img class="hero-photo" src="assets/img/transporter-loaded.webp" alt="" width="1280" height="720" fetchpriority="high">
  </div>
  <div class="hero-aurora" aria-hidden="true"></div>
  <div class="hero-sweep" aria-hidden="true"></div>
  <svg class="hero-network" viewBox="0 0 1400 700" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
    <path class="hn-line" d="M40 620 C 300 560, 500 480, 780 500 S 1200 420, 1360 340"/>
    <path class="hn-line" d="M100 120 C 320 180, 560 160, 820 220 S 1180 260, 1340 200"/>
    <path class="hn-line" d="M60 380 C 260 340, 480 400, 700 360 S 1000 320, 1320 380"/>
    <circle class="hn-dot" cx="120" cy="150" r="3"/>
    <circle class="hn-dot" cx="480" cy="240" r="2.4"/>
    <circle class="hn-dot" cx="820" cy="180" r="3"/>
    <circle class="hn-dot" cx="1100" cy="300" r="2.4"/>
    <circle class="hn-dot" cx="1320" cy="220" r="3"/>
    <circle class="hn-dot" cx="220" cy="450" r="2.4"/>
    <circle class="hn-dot" cx="640" cy="500" r="3"/>
    <circle class="hn-dot" cx="980" cy="440" r="2.4"/>
    <circle class="hn-dot" cx="1260" cy="380" r="3"/>
  </svg>
  <div class="container">
    <div class="hero-grid">
      <div class="hero-copy">
        <span class="eyebrow">Germany &rarr; Worldwide freight forwarding</span>
        <h1><span class="line">Your cargo,</span> <span class="line">moved with</span> <span class="accent">total transparency.</span></h1>
        <p class="hero-lede">EL-ROI Shipping Services has connected Germany to the world for over 20 years. Sea freight, vehicles, containers and heavy cargo, handled with honest estimates and clear communication at every step.</p>
        <div class="hero-actions">
          <a href="quote.html" class="btn btn-primary">Request a Quote {ARROW}</a>
          <a href="book.html" class="btn btn-ghost">Book a Shipment</a>
        </div>
        <a class="hero-wa" href="{WA}" target="_blank" rel="noopener" style="margin:22px 0 0">{WA_ICON} Or chat with us on WhatsApp</a>
      </div>
      <div class="hero-globe-wrap" data-reveal style="--d:2">
        <div class="hero-globe" data-globe role="img" aria-label="3D globe showing EL-ROI shipping routes from Essen, Germany to Europe and to destinations worldwide: the Americas, Africa, the Middle East and Asia"></div>
        <div class="globe-legend" aria-hidden="true"><span><i></i>Major routes: Europe</span><span><i class="eu"></i>Worldwide destinations</span></div>
        <p class="globe-hint">Drag the globe to spin it</p>
      </div>
    </div>
    <div class="hero-stats" data-reveal style="--d:4">
      <div><div class="stat-num"><span data-count="20">20</span><span class="plus">+</span></div><div class="stat-label">Years in operation</div></div>
      <div><div class="stat-num">1999</div><div class="stat-label">Established</div></div>
      <div><div class="stat-num" data-count="2">2</div><div class="stat-label">Offices: Essen &amp; Lagos</div></div>
      <div><div class="stat-num">~2<small>wks</small></div><div class="stat-label">Average transit</div></div>
    </div>
  </div>
</section>

<div class="marquee" aria-hidden="true">
  <div class="marquee-track">
    <span>Worldwide shipping</span><span>Sea freight specialists</span><span>Vehicles &amp; heavy cargo</span><span>Germany to the world</span><span>Since 1999</span>
    <span>Worldwide shipping</span><span>Sea freight specialists</span><span>Vehicles &amp; heavy cargo</span><span>Germany to the world</span><span>Since 1999</span>
  </div>
</div>

<section>
  <div class="container">
    <div class="section-head" data-reveal>
      <div>
        <span class="num-label">(01)</span>
        <span class="eyebrow">What we handle</span>
        <h2>Cargo types <em>we move</em></h2>
      </div>
      <div><p>From single documents to full oversized machinery, every shipment gets the same standard of care.</p><a class="link-arrow" href="services.html">All services {ARROW}</a></div>
    </div>
    <div class="cargo-grid">
      <a class="cargo-card" href="services.html#vehicles" data-reveal>
        <div class="cargo-img">{img('loaded')}</div>
        <span class="cargo-idx">01 &middot; Vehicles</span>
        <h3>Vehicles &amp; parts</h3>
        <p>Cars, trucks and vehicle parts shipped with full documentation support.</p>
      </a>
      <a class="cargo-card" href="services.html#tractors" data-reveal style="--d:1">
        <div class="cargo-img">{img('tractor')}</div>
        <span class="cargo-idx">02 &middot; Agriculture</span>
        <h3>Tractors &amp; farm machinery</h3>
        <p>Tractors and agricultural equipment, secured for sea freight.</p>
      </a>
      <a class="cargo-card" href="services.html#trucks" data-reveal style="--d:2">
        <div class="cargo-img">{img('volvo')}</div>
        <span class="cargo-idx">03 &middot; Trucks</span>
        <h3>Trucks &amp; tractor units</h3>
        <p>Tractor heads and commercial vehicles, exported from Germany.</p>
      </a>
      <a class="cargo-card" href="services.html#heavy" data-reveal style="--d:3">
        <div class="cargo-img">{img('chassis')}</div>
        <span class="cargo-idx">04 &middot; Heavy</span>
        <h3>Oversized &amp; machinery</h3>
        <p>Trailers, construction equipment and engines, handled with specialist care.</p>
      </a>
    </div>
    <ul class="also" data-reveal>
      <li class="also-label" style="display:inline">Also shipping</li>
      <li>General cargo</li><li>20FT / 40FT containers</li><li>Machinery &amp; engines</li><li>Fragile goods</li><li>Documents</li>
    </ul>
  </div>
</section>

<section class="dark has-photo">
  {photo_bg("msc", "center 40%")}
  <div class="container coverage-grid">
      <div class="route-card" data-reveal>
        <div class="rc-head"><span class="live">Major routes</span><span>Sea freight</span></div>
        <svg class="rc-svg" viewBox="0 0 420 130" aria-hidden="true">
          <path class="rc-arc-2" d="M40 112 H380"/>
          <path id="rc-path" class="rc-arc" d="M40 112 C 130 4, 290 4, 380 112"/>
          <circle class="rc-glow" cx="40" cy="112" r="7"/>
          <circle class="rc-node" cx="40" cy="112" r="5"/>
          <circle class="rc-glow" cx="380" cy="112" r="7" style="animation-delay:-1.2s"/>
          <circle class="rc-node" cx="380" cy="112" r="5"/>
          <circle class="rc-ship" r="4"><animateMotion dur="5s" repeatCount="indefinite" keyPoints="0;1" keyTimes="0;1" calcMode="spline" keySplines=".45 0 .25 1"><mpath href="#rc-path"/></animateMotion></circle>
        </svg>
        <div class="rc-points">
          <div><small>Origin</small><strong>Essen</strong><span>Germany</span></div>
          <div class="rc-mid">~2 weeks</div>
          <div><small>Destination</small><strong>Europe</strong><span>Belgium &middot; Austria &middot; Holland</span></div>
        </div>
        <ul class="rc-list">
          <li><span>Any part of the world</span><span>Sea freight</span></li>
          <li><span>Lagos, Nigeria</span><span>Our 2nd office</span></li>
        </ul>
      </div>
    <div data-reveal style="--d:1">
      <span class="num-label">(02)</span>
      <span class="eyebrow">Global coverage</span>
      <h2>Wherever your cargo <em>needs to go</em></h2>
      <p style="max-width:48ch;margin-bottom:36px">We ship from Germany to any part of the world, with major routes to Belgium, Austria and Holland and our own office in Lagos. Whatever the route, the same standard of care and communication applies.</p>
      {ROUTES_TABLE}
    </div>
  </div>
</section>

<section class="journey section-alt" id="journey">
  <div class="journey-sticky">
    <div class="container journey-inner">
      <div class="journey-head">
        <div>
          <span class="num-label">(03)</span>
          <span class="eyebrow">How it works</span>
          <h2>Four steps, <em>no surprises</em></h2>
        </div>
        <div class="journey-status">
          <span class="js-label">Shipment status</span>
          <strong id="jr-status">Quote requested</strong>
          <span class="js-day" id="jr-sub">Essen, Germany</span>
        </div>
      </div>
      <div class="journey-map" id="jr-map">
        <svg id="jr-svg" viewBox="637 340 2766 900" preserveAspectRatio="xMidYMid slice" role="img" aria-labelledby="jr-title">
          <title id="jr-title">World route map: pickup in Essen, Germany; major routes to Belgium, Holland and Austria; sea freight to the Americas, Africa, the Middle East and Asia</title>
          <g id="jr-grid"></g>
          <path class="jm-land" d="{CHART_LAND}"/>
          <g id="jr-lines"></g>
          <g id="jr-marks"></g>
        </svg>
      </div>
      <ol class="journey-steps">
        <li class="journey-step is-active"><span class="process-num">01</span><h4>Tell us what you're shipping</h4><p>Share your cargo details and destination through our quote or booking form.</p></li>
        <li class="journey-step"><span class="process-num">02</span><h4>Get a transparent estimate</h4><p>We confirm pricing and documentation needs before anything is booked. No hidden fees.</p></li>
        <li class="journey-step"><span class="process-num">03</span><h4>Cargo is loaded and shipped</h4><p>Your shipment moves by sea freight, with any special declarations (Form M) handled for you.</p></li>
        <li class="journey-step"><span class="process-num">04</span><h4>Arrival, typically ~2 weeks</h4><p>Delivery time varies by destination, but averages around two weeks after loading.</p></li>
      </ol>
      <div class="journey-dots" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
    </div>
  </div>
</section>

<section class="statement">
  <div class="bg" style="background-image:url('{IMG['loading'][0]}')"></div>
  <div class="container" data-reveal>
    <blockquote>Your satisfaction is <em>our priority.</em></blockquote>
    <cite>The EL-ROI promise &middot; since 1999</cite>
  </div>
</section>

<section>
  <div class="container why-grid">
    <div class="why-sticky" data-reveal>
      <span class="num-label">(04)</span>
      <span class="eyebrow">Why EL-ROI</span>
      <h2>Built on relationships, <em>not just routes</em></h2>
      <p>Five things that make the difference between a shipment that goes smoothly and one that doesn't.</p>
      <figure class="why-photo">{img('chassis')}<figcaption>Ready for the port</figcaption></figure>
    </div>
    <div>
      <div class="why-item" data-reveal><div class="why-num">01</div><div><h4>Transparent estimates</h4><p>You see the full cost before anything is booked. No hidden fees added later.</p></div></div>
      <div class="why-item" data-reveal><div class="why-num">02</div><div><h4>Documentation handled for you</h4><p>Vehicle documents, Form M declarations: we guide you through what's required.</p></div></div>
      <div class="why-item" data-reveal><div class="why-num">03</div><div><h4>Fair, honest pricing</h4><p>The estimate we give you is the price you pay, not a starting offer.</p></div></div>
      <div class="why-item" data-reveal><div class="why-num">04</div><div><h4>Direct communication</h4><p>You deal with real people who know your shipment, not a call centre queue.</p></div></div>
      <div class="why-item" data-reveal><div class="why-num">05</div><div><h4>20+ years of experience</h4><p>We've been moving cargo from Germany to the world since 1999.</p></div></div>
    </div>
  </div>
</section>

<section class="dark has-photo">
  {photo_bg("vanload", "center 45%")}
  <div class="container">
    <div class="section-head" data-reveal>
      <div>
        <span class="num-label">(05)</span>
        <span class="eyebrow">Testimonials</span>
        <h2>What <em>clients say</em></h2>
      </div>
    </div>
    <!-- Placeholder testimonials: replace the quotes and names with real client feedback. -->
    <div class="testimonials">
      <figure class="testimonial" data-reveal><p>&ldquo;Honest estimate, no surprises at the end. That's rare in freight.&rdquo;</p><cite>Client name, Company</cite></figure>
      <figure class="testimonial" data-reveal style="--d:1"><p>&ldquo;They handled our Form M paperwork without us having to chase anyone.&rdquo;</p><cite>Client name, Company</cite></figure>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head" data-reveal>
      <div>
        <span class="num-label">(06)</span>
        <span class="eyebrow">From the yard</span>
        <h2>Real cargo, <em>real photos</em></h2>
      </div>
      <div class="head-actions" data-strip="yard-strip">
        <a class="link-arrow" href="gallery.html">Full gallery {ARROW}</a>
        <div class="strip-ctrl">
          <button class="round-btn prev" data-dir="prev" aria-label="Scroll photos left">{ARROW}</button>
          <button class="round-btn" data-dir="next" aria-label="Scroll photos right">{ARROW}</button>
        </div>
      </div>
    </div>
  </div>
  <div class="strip" id="yard-strip">
    <a href="gallery.html"><div class="strip-img">{img('transporter')}</div><span class="cap">Vehicle transport</span></a>
    <a href="gallery.html"><div class="strip-img">{img('tractor')}</div><span class="cap">John Deere tractor</span></a>
    <a href="gallery.html"><div class="strip-img">{img('volvo')}</div><span class="cap">Volvo FH tractor unit</span></a>
    <a href="gallery.html"><div class="strip-img">{img('chassis')}</div><span class="cap">Container chassis</span></a>
    <a href="gallery.html"><div class="strip-img">{img('msc')}</div><span class="cap">40ft container</span></a>
    <a href="gallery.html"><div class="strip-img">{img('deere3140')}</div><span class="cap">John Deere 3140</span></a>
    <a href="gallery.html"><div class="strip-img">{img('van')}</div><span class="cap">Mercedes-Benz van</span></a>
    <a href="gallery.html"><div class="strip-img">{img('loading')}</div><span class="cap">Loading day</span></a>
  </div>
</section>

{CTA}'''

write('index.html', 'Home | EL-ROI Shipping Services',
      'EL-ROI Shipping Services: direct freight forwarding from Germany to destinations worldwide since 1999.',
      'index.html', home, preloader=True,
      scripts='<script src="' + LAND_URL + '" defer></script>\n<script src="' + GLOBE_URL + '" defer></script>\n')

# =====================================================================
# ABOUT
# =====================================================================
about = page_hero('About', 'Our story', '20+ years of <em>honest freight forwarding</em>',
                  'A German shipping company built on relationships: honest estimates, fair pricing and clear communication at every step.',
                  'engines', 'center 40%') + f'''
<section>
  <div class="container split">
    <div data-reveal>
      <span class="eyebrow">Who we are</span>
      <h2>A German shipping company <em>built on relationships</em></h2>
      <p class="lead-p">We're a German-based shipping service, in operation for over 20 years, moving cargo directly from Germany to any part of the world.</p>
      <p style="color:var(--text-2)">From global export of tractors, trucks, 40FT/20FT containers, vehicles and parts, to construction equipment and engines, we've built our name on doing the job right.</p>
      <p style="color:var(--text-2)">We believe great service starts with great relationships. That means honest estimates, fair pricing, and clear communication every step of the way.</p>
    </div>
    <div class="glance" data-reveal style="--d:2">
      <h3>At a glance</h3>
      <div class="glance-row"><span>Founded</span><div>1999</div></div>
      <div class="glance-row"><span>Headquarters</span><div>Ripshorster Str. 379, 45357 Essen, Germany</div></div>
      <div class="glance-row"><span>Second office</span><div>Olodi Apapa, Lagos, Nigeria</div></div>
      <div class="glance-row"><span>Management</span><div>Iyamah</div></div>
      <div class="glance-row"><span>Major routes</span><div>Germany to Belgium, Austria and Holland</div></div>
      <div class="glance-row"><span>Shipping</span><div>Sea freight, Germany to worldwide</div></div>
      <div class="glance-row"><span>Transit</span><div>Around two weeks after loading (average)</div></div>
    </div>
  </div>
</section>

<section class="dark has-photo" style="text-align:center">
  {photo_bg("deere3140", "center 40%")}
  <div class="container" data-reveal>
    <span class="eyebrow">Core values</span>
    <p class="values"><span>Honesty.</span><span>Fairness.</span><span>Reliability.</span><span>Easy shipment.</span></p>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="grid g-3">
      <div class="card" data-reveal><span class="card-kicker">Vision</span><h3>Your satisfaction is our priority</h3><p>We're there with you every step of the way, giving you a fast and reliable shipping experience.</p></div>
      <div class="card" data-reveal style="--d:1"><span class="card-kicker">Mission</span><h3>Total transparency</h3><p>Before any job starts, you get a detailed estimate so you can make the right decision for your shipment. No hidden fees, no pressure.</p></div>
      <div class="card" data-reveal style="--d:2"><span class="card-kicker">Core values</span><h3>Every job, every time</h3><p>Honesty, fairness, reliability and easy shipment. Every job, every time.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head" data-reveal>
      <div><span class="eyebrow">On the ground</span><h2>The work <em>speaks</em></h2></div>
      <div><a class="link-arrow" href="gallery.html">View gallery {ARROW}</a></div>
    </div>
    <div class="photo-trio" data-reveal>
      <a href="gallery.html">{img('transporter')}</a>
      <a href="gallery.html">{img('volvo')}</a>
      <a href="gallery.html">{img('chassis')}</a>
    </div>
  </div>
</section>

{CTA}'''

write('about.html', 'About Us | EL-ROI Shipping Services',
      '20+ years of honest, transparent freight forwarding from Germany to the world.',
      'about.html', about)

# =====================================================================
# SERVICES
# =====================================================================
def feature(anchor, num, key, title, text, bullets):
    lis = ''.join(f'<li>{b}</li>' for b in bullets)
    return f'''      <div class="feature" id="{anchor}" data-reveal>
        <figure class="feature-img">{img(key)}</figure>
        <div>
          <span class="feature-num">{num}</span>
          <h3>{title}</h3>
          <p>{text}</p>
          <ul class="checklist">{lis}</ul>
        </div>
      </div>'''


services = page_hero('Services', 'What we offer', 'Freight services <em>built around your cargo</em>',
                     'Sea freight from Germany for everything from documents to heavy machinery, with the paperwork handled and the price agreed up front.',
                     'loaded', 'center 55%') + f'''
<section>
  <div class="container">
    <div class="section-head" data-reveal>
      <div><span class="num-label">(01)</span><span class="eyebrow">Cargo gallery</span><h2>What <em>we move</em></h2></div>
      <div><p>From single documents to full oversized machinery, we handle it with the same standard of care.</p></div>
    </div>
    <div>
{feature('vehicles', '01', 'loaded', 'Vehicles &amp; vehicle parts', 'Cars, trucks and vehicle parts shipped with full documentation support. We make sure the vehicle papers are in order before anything is loaded. Shipping a car to Nigeria? Read our <a href="guide-ship-car-germany-to-nigeria.html" class="inline-link">step-by-step guide</a>.', ['Vehicles and spare parts', 'Vehicle documentation handled correctly', 'Form M special declarations where required'])}
{feature('tractors', '02', 'tractor', 'Tractors &amp; farm machinery', 'Tractors and agricultural equipment, prepared and secured for sea freight to any part of the world.', ['Tractors and implements', 'Secured for sea freight', 'Transparent estimate before booking'])}
{feature('trucks', '03', 'volvo', 'Trucks &amp; tractor units', 'Tractor heads, trucks and commercial vehicles exported directly from Germany.', ['Trucks and tractor units', 'Shipped direct from Germany', 'Clear communication at every step'])}
{feature('containers', '04', 'msc', 'Containers (20FT / 40FT)', 'Full container loads, packed, sealed and shipped by sea freight to destinations worldwide.', ['20FT and 40FT HC containers', 'Packed and secured for the voyage', 'Sea freight to any part of the world'])}
{feature('heavy', '05', 'redchassis', 'Oversized &amp; heavy cargo', 'Trailers, construction equipment and oversized loads, planned around real constraints.', ['Trailers and chassis', 'Construction equipment', 'Engines and industrial machinery'])}
    </div>
  </div>
</section>

<section class="section-alt" id="more">
  <div class="container">
    <div class="section-head" data-reveal>
      <div><span class="num-label">(02)</span><span class="eyebrow">Also on board</span><h2>Every cargo, <em>the same care</em></h2></div>
    </div>
    <div class="grid g-3">
      <div class="card" data-reveal><div class="card-ico">{ICONS['box']}</div><h3>General cargo</h3><p>Packed, documented and shipped with full care from pickup to port.</p></div>
      <div class="card" data-reveal style="--d:1"><div class="card-ico">{ICONS['container']}</div><h3>Containers (20FT / 40FT)</h3><p>Full and part container loads, sea freight to destinations worldwide.</p></div>
      <div class="card" data-reveal style="--d:2"><div class="card-ico">{ICONS['gear']}</div><h3>Machinery &amp; equipment</h3><p>Engines and industrial machinery shipped with proper securing and paperwork.</p></div>
      <div class="card" data-reveal><div class="card-ico">{ICONS['fragile']}</div><h3>Fragile goods</h3><p>Extra-care packaging and handling for delicate or high-value items.</p></div>
      <div class="card" data-reveal style="--d:1"><div class="card-ico">{ICONS['doc']}</div><h3>Documents</h3><p>Important papers shipped safely alongside, or independent of, your cargo.</p></div>
      <div class="card card-navy cta-card has-photo" data-reveal style="--d:2">{photo_bg("enginesclose", "center 40%", "soft")}<div><span class="card-kicker">Not listed?</span><h3>Ask us about your cargo</h3><p>Get in touch and we'll confirm whether we can move it, and what it takes.</p></div><a class="link-arrow" href="contact.html">Contact us {ARROW}</a></div>
    </div>
  </div>
</section>

<section>
  <div class="container split">
    <div data-reveal>
      <span class="num-label">(03)</span>
      <span class="eyebrow">Shipping method</span>
      <h2>Sea freight, <em>done right</em></h2>
      <p style="color:var(--text-2);max-width:46ch">All shipments move by sea freight. Delivery time depends on the destination country, but averages around two weeks after your container is loaded onto the ship.</p>
    </div>
    <div class="grid">
      <div class="card" data-reveal><span class="card-kicker">What we need from you</span><h3>Your checklist</h3>
        <ul class="checklist"><li>Name and address</li><li>Phone number</li><li>Company or private name</li><li>Vehicle documentation</li><li>Special declaration paperwork (Form M), where applicable</li></ul>
        <a class="link-arrow" href="guide-what-to-prepare-before-booking.html" style="margin-top:22px">Full checklist {ARROW}</a>
      </div>
      <div class="card" data-reveal style="--d:1"><span class="card-kicker">Restrictions</span><h3>What we don't accept</h3>
        <p>Certain cargo types are restricted for safety and regulatory reasons. Get in touch to confirm your cargo qualifies before booking.</p>
      </div>
    </div>
  </div>
</section>

{CTA}'''

write('services.html', 'Services | EL-ROI Shipping Services',
      'Freight services built around your cargo: vehicles, tractors, trucks, containers, machinery, oversized cargo, fragile goods and documents.',
      'services.html', services)

# =====================================================================
# ROUTES
# =====================================================================
route_map = '''<svg class="route-map" viewBox="0 0 800 560" role="img" aria-labelledby="map-title">
        <title id="map-title">Schematic route map: Essen, Germany to Holland, Belgium and Austria (major routes), Lagos and worldwide</title>
        <path class="ln ln-world" d="M372 150 H 560 L 640 70 H 760"/>
        <path class="ln ln-eu" d="M372 150 V 250 L 330 292 V 478 H 250"/>
        <path class="ln ln-main" d="M372 150 L 300 78 H 170"/>
        <path class="ln ln-main" d="M372 150 L 300 222 H 170"/>
        <path class="ln ln-main" d="M372 150 V 250 L 452 330 H 600"/>
        <path class="flow" d="M372 150 L 300 78 H 170"/>
        <path class="flow" d="M372 150 L 300 222 H 170"/>
        <path class="flow" d="M372 150 V 250 L 452 330 H 600"/>
        <circle class="hub-ring" cx="372" cy="150" r="20"/>
        <circle class="hub" cx="372" cy="150" r="15"/>
        <circle class="stn-main" cx="170" cy="78" r="10"/>
        <circle class="stn-main" cx="170" cy="222" r="10"/>
        <circle class="stn-main" cx="600" cy="330" r="10"/>
        <circle class="stn" cx="250" cy="478" r="10"/>
        <text x="398" y="196" class="t-gold">Essen, DE</text>
        <text x="398" y="216" class="sub">HQ &#183; ORIGIN</text>
        <text x="60" y="60">Holland</text><text x="60" y="106" class="sub">NL &#183; ~2 WKS</text>
        <text x="60" y="204">Belgium</text><text x="60" y="250" class="sub">BE &#183; ~2 WKS</text>
        <text x="620" y="326">Austria</text><text x="620" y="348" class="sub">AT &#183; ~2 WKS</text>
        <text x="60" y="470">Lagos</text><text x="60" y="498" class="sub">NG &#183; OUR 2ND OFFICE</text>
        <text x="640" y="52">World</text><text x="640" y="100" class="sub">ANY PORT &#183; SEA FREIGHT</text>
      </svg>'''

routes = page_hero('Routes', 'Where we ship', 'Germany to <em>any part of the world</em>',
                   'Major routes from our Essen headquarters to Belgium, Austria and Holland, and sea freight to any part of the world, including Lagos, home of our second office.',
                   'msc', 'center 45%') + f'''
<section>
  <div class="container">
    <div class="section-head" data-reveal>
      <div><span class="num-label">(01)</span><span class="eyebrow">Coverage</span><h2>Our <em>shipping routes</em></h2></div>
      <div><p>Every route runs by sea freight from Essen, Germany.</p></div>
    </div>
    <div data-reveal>
    {ROUTES_TABLE}
    </div>
  </div>
</section>

<section class="dark has-photo">
  {photo_bg("redchassis", "center 50%")}
  <div class="container split" style="align-items:center">
    <div data-reveal>
      <div class="map-wrap">
      {route_map}
      </div>
      <div class="map-legend"><span><i></i>Major routes: Europe</span><span><i class="eu"></i>Lagos office</span><span><i class="ww"></i>Worldwide</span></div>
    </div>
    <div data-reveal style="--d:1">
      <span class="num-label">(02)</span>
      <span class="eyebrow">The network</span>
      <h2>One hub, <em>every port</em></h2>
      <div class="lanes">
        <div class="lane"><span class="lane-code">EU</span><div><h4>Essen &rarr; Europe</h4><p>Our major routes: Belgium, Austria and Holland. Around two weeks after loading.</p></div></div>
        <div class="lane"><span class="lane-code ww">WW</span><div><h4>Essen &rarr; Any part of the world</h4><p>Sea freight to Africa, the Americas, the Middle East and Asia. Transit varies by destination, so ask us for a route-specific timeline.</p></div></div>
        <div class="lane"><span class="lane-code eu">NG</span><div><h4>Lagos office</h4><p>Our second office in Olodi Apapa, Lagos, supports shipments arriving in Nigeria.</p></div></div>
      </div>
    </div>
  </div>
</section>

<section class="section-alt cta">
  <div class="container" data-reveal>
    <h2>Not sure if we cover <em>your destination?</em></h2>
    <p>We ship from Germany to any part of the world. Reach out and we'll confirm the route for you.</p>
    <div class="hero-actions">
      <a class="btn btn-dark" href="contact.html">Contact Us {ARROW}</a>
      <a class="btn btn-outline" href="{WA}" target="_blank" rel="noopener">{WA_ICON} WhatsApp</a>
    </div>
  </div>
</section>
'''

write('routes.html', 'Routes | EL-ROI Shipping Services',
      'Sea freight from Essen, Germany: major routes to Belgium, Austria and Holland, and any destination worldwide, including Lagos, Nigeria.',
      'routes.html', routes)

# =====================================================================
# GALLERY
# =====================================================================
GALLERY = [
    ('transporter', 'vehicles', 'Vehicle transport', 'Trucks loaded for the port'),
    ('volvo', 'vehicles', 'Volvo FH tractor unit', 'Trucks'),
    ('tractor', 'machinery', 'John Deere tractor', 'Farm machinery'),
    ('chassis', 'containers', 'Blue container chassis', 'Trailers'),
    ('loading', 'containers', 'Loading day', 'Inside the container'),
    ('msc', 'containers', '40ft container', 'Ready for the port'),
    ('volvofront', 'vehicles', 'Volvo FH', 'Tractor unit'),
    ('deere3140', 'machinery', 'John Deere 3140', 'Tractor with front loader'),
    ('chassisrear', 'containers', 'Tri-axle chassis', 'Trailers'),
    ('van', 'vehicles', 'Mercedes-Benz van', 'Vans &amp; light vehicles'),
    ('loaded', 'vehicles', 'Loaded for export', 'Van and truck on a transporter'),
    ('vanload', 'containers', 'Van in a container', 'Packed for sea freight'),
    ('yardload', 'containers', 'Loading the container', 'Cargo going in'),
    ('engines', 'machinery', 'Engines', 'Loaded at night'),
    ('redchassis', 'containers', 'Red container chassis', 'Trailers'),
    ('carsload', 'vehicles', 'Cars in a container', 'Wrapped and strapped'),
    ('enginesclose', 'machinery', 'Engines &amp; parts', 'Packed to the roof'),
]
figs = '\n'.join(
    f'''      <figure data-cat="{cat}" data-reveal>
        <a href="{IMG[k][0]}" data-lightbox data-caption="{title}">{img(k)}</a>
        <figcaption><strong>{title}</strong><span>{sub}</span></figcaption>
      </figure>''' for k, cat, title, sub in GALLERY)

gallery = page_hero('Gallery', 'Gallery', 'From <em>the yard</em>',
                    'Real cargo, real photos: tractors, trucks, trailers and containers on their way from Germany.',
                    'vanload', 'center 45%') + f'''
<section>
  <div class="container">
    <div class="filters" role="group" aria-label="Filter photos">
      <button class="active" data-filter="all" aria-pressed="true">All</button>
      <button data-filter="vehicles" aria-pressed="false">Trucks &amp; vehicles</button>
      <button data-filter="machinery" aria-pressed="false">Tractors &amp; machinery</button>
      <button data-filter="containers" aria-pressed="false">Containers &amp; trailers</button>
    </div>
    <div class="masonry">
{figs}
    </div>
  </div>
</section>

<section class="section-alt cta">
  <div class="container" data-reveal>
    <h2>Have cargo to ship? <em>Send us a photo.</em></h2>
    <p>Send a photo of your cargo and its destination on WhatsApp, and we'll tell you what it takes to ship it.</p>
    <div class="hero-actions">
      <a class="btn btn-dark" href="{WA}" target="_blank" rel="noopener">{WA_ICON} Send on WhatsApp</a>
      <a class="btn btn-outline" href="quote.html">Request a Quote</a>
    </div>
  </div>
</section>
'''

write('gallery.html', 'Gallery | EL-ROI Shipping Services',
      'Photos of tractors, trucks, trailers and containers shipped by EL-ROI Shipping Services from Germany.',
      'gallery.html', gallery)

# =====================================================================
# NEWS
# =====================================================================
# =====================================================================
# SHIPPING GUIDES (SEO articles)
# =====================================================================
def tick(items):
    return '<ul class="checklist">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


GUIDES = [
 {
  'slug': 'guide-ship-car-germany-to-nigeria.html',
  'title': 'How to ship a car from Germany to Nigeria',
  'h1': 'How to ship a car from <em>Germany to Nigeria</em>',
  'seo': 'How to Ship a Car from Germany to Nigeria (Step by Step) | EL-ROI',
  'desc': 'Step-by-step guide to shipping a car from Germany to Lagos, Nigeria: documents, Form M, container shipping, transit time and customs clearance.',
  'img': 'vanload', 'pos': 'center 45%', 'badge': 'Vehicles', 'mins': 5,
  'lede': 'From paperwork in Germany to collection in Lagos: what happens at each step, and what you need to have ready.',
  'body': f"""
<p class="lead-p">Shipping a car from Germany to Nigeria is straightforward when the documents are right before the car is loaded. We have been doing it from our Essen yard since 1999, with our own office in Olodi Apapa, Lagos.</p>
<h2>1. Check the car and its papers</h2>
<p>Before anything is booked, make sure you have:</p>
{tick(['The vehicle registration documents (in Germany: Zulassungsbescheinigung Teil I and Teil II)', 'The purchase invoice or proof of ownership', 'A copy of the owner&rsquo;s ID or passport', 'The receiver&rsquo;s full name, address and phone number in Nigeria'])}
<p>If the car is still registered in Germany, it usually needs to be deregistered or put on export plates before it leaves. Ask us if you are not sure.</p>
<h2>2. Get the Form M started in Nigeria</h2>
<p>Almost every import into Nigeria needs a <strong>Form M</strong>, and it must be opened by the importer in Nigeria through their bank <em>before</em> the car is shipped. Starting it late is one of the most common causes of delays at the port. Read our <a href="guide-form-m-nigeria.html">Form M guide</a> for what it is and what the bank needs.</p>
<h2>3. Get a transparent quote</h2>
<p>Send us the make, model, year and approximate weight, plus where the car is now. We confirm the full price and any documents we need before anything is booked, with no hidden fees. You can get a rough figure first with our <a href="calculator.html">shipping calculator</a>.</p>
<h2>4. Prepare the car</h2>
{tick(['Remove personal belongings unless we have agreed to ship them with the car', 'Leave only a little fuel in the tank', 'Note any existing damage and take photos from all sides', 'Hand over all keys, including spares'])}
<h2>5. Loading and sea freight</h2>
<p>Cars are loaded into a container and secured with straps and wheel chocks. One car fits in a 20ft container, and a 40ft container can take several cars depending on their size. See <a href="guide-20ft-vs-40ft-container.html">20ft vs 40ft containers</a>. Sea freight usually takes <strong>around two weeks after the container is loaded</strong> onto the ship, depending on the shipping line and port schedules.</p>
<h2>6. Arrival and customs clearance in Lagos</h2>
<p>When the ship arrives, the car is cleared through Nigerian customs. Import duties, taxes and port charges in Nigeria are paid by the importer and are not part of the freight price unless we agree otherwise. Our Lagos office keeps you updated along the way.</p>
<div class="note"><strong>Check the current rules.</strong> Nigerian import rules for vehicles (for example duty rates and rules on vehicle age) change from time to time. Check the latest Nigeria Customs Service rules, or ask your clearing agent, before you buy a car for export.</div>
""",
  'faq': [
   ('How long does it take to ship a car from Germany to Nigeria?', 'Usually around two weeks at sea after the container is loaded, depending on the shipping line and port schedules. Add time for collection, loading and customs clearance in Lagos.'),
   ('Do I need a Form M to import a car into Nigeria?', 'Yes, imports into Nigeria generally need a Form M, opened by the importer through their bank in Nigeria before the car is shipped.'),
   ('Who pays customs duty on a car shipped to Nigeria?', 'The importer pays Nigerian import duties, taxes and port charges. They are not included in the freight price unless agreed otherwise.'),
  ],
 },
 {
  'slug': 'guide-form-m-nigeria.html',
  'title': 'What is Form M? A simple guide for shipping to Nigeria',
  'h1': 'What is <em>Form M?</em>',
  'seo': 'What Is Form M? Nigeria Import Guide for Shipping from Germany | EL-ROI',
  'desc': 'Form M explained in plain English: what it is, who completes it, when it must be done and which documents your bank in Nigeria needs before shipping.',
  'img': 'yardload', 'pos': 'center 45%', 'badge': 'Documents', 'mins': 4,
  'lede': 'The one document that most often holds up shipments to Nigeria, explained in plain English.',
  'body': f"""
<p class="lead-p">If you are shipping goods or a vehicle into Nigeria, you will hear about Form M. Here is what it is and how to avoid delays.</p>
<h2>What Form M is</h2>
<p>Form M is Nigeria&rsquo;s mandatory import declaration. It registers the planned import with the authorities before the goods are shipped, and it is processed electronically through the importer&rsquo;s bank in Nigeria.</p>
<h2>Who completes it</h2>
<p>The <strong>importer in Nigeria</strong> (the person or company receiving the goods) opens the Form M through their bank. As the shipper in Germany, we don&rsquo;t file it, but we give you the shipment details you need and add the Form M reference to the shipping documents.</p>
<h2>When it must be done</h2>
<p>Before the goods are shipped. A shipment that leaves Germany without a valid Form M can face delays, extra costs or penalties when it arrives in Nigeria, so start it as soon as you have a quote.</p>
<h2>What the bank usually asks for</h2>
{tick(['A proforma invoice from the seller, describing the goods and their value', 'A description of the goods and their customs (HS) code', 'The importer&rsquo;s registration details', 'Insurance details for the shipment, where required'])}
<p>Your bank and your clearing agent will confirm exactly what they need, because requirements can change.</p>
<h2>How we help</h2>
<p>When you book with us, we provide the cargo and shipping details for your Form M application and include your Form M reference on the documents. You can add it on our <a href="quote.html">quote</a> or <a href="book.html">booking</a> form in the &ldquo;special declaration&rdquo; field.</p>
<div class="note"><strong>General information only.</strong> This guide is not legal or customs advice. Your bank and licensed clearing agent in Nigeria confirm the current Form M requirements.</div>
""",
  'faq': [
   ('What is Form M?', 'Form M is Nigeria’s mandatory import declaration, opened by the importer through their bank in Nigeria before goods are shipped.'),
   ('Who fills in Form M?', 'The importer in Nigeria, through their bank. The shipper provides the shipment details and adds the Form M reference to the documents.'),
   ('When should Form M be done?', 'Before the goods are shipped. Starting it late is a common cause of delays at the port.'),
  ],
 },
 {
  'slug': 'guide-20ft-vs-40ft-container.html',
  'title': '20ft vs 40ft container: which size do you need?',
  'h1': '20ft vs 40ft <em>container</em>',
  'seo': '20ft vs 40ft Container: Sizes, Capacity & Which to Choose | EL-ROI',
  'desc': 'Compare 20ft, 40ft and 40ft high cube shipping containers: inside dimensions, volume and payload, how many cars fit, and which size suits your cargo.',
  'img': 'msc', 'pos': 'center 45%', 'badge': 'Containers', 'mins': 4,
  'lede': 'Inside sizes, how much fits, and how to choose the right container for your cargo.',
  'body': f"""
<p class="lead-p">Most of our sea freight moves in standard 20ft and 40ft containers. Here is how they compare.</p>
<h2>Container sizes at a glance</h2>
<div class="table-wrap"><table class="data-table">
<thead><tr><th>Type</th><th>Inside length</th><th>Inside width</th><th>Inside height</th><th>Volume</th><th>Max. cargo weight</th></tr></thead>
<tbody>
<tr><td>20ft standard</td><td>5.90 m</td><td>2.35 m</td><td>2.39 m</td><td>~33 m&sup3;</td><td>~28,000 kg</td></tr>
<tr><td>40ft standard</td><td>12.03 m</td><td>2.35 m</td><td>2.39 m</td><td>~67 m&sup3;</td><td>~26,500 kg</td></tr>
<tr><td>40ft high cube (HC)</td><td>12.03 m</td><td>2.35 m</td><td>2.69 m</td><td>~76 m&sup3;</td><td>~26,500&ndash;28,500 kg</td></tr>
</tbody></table></div>
<p class="small-note">Typical figures. Every container lists its own maximum weight and capacity on the door. The 40ft high cube in our <a href="gallery.html">gallery</a>, for example, shows 76.4 m&sup3;.</p>
<h2>What fits</h2>
{tick(['<strong>One car</strong>, plus some parts: a 20ft container', '<strong>Several cars</strong>, or a car with a lot of parts and goods: a 40ft or 40ft HC', '<strong>Tall cargo</strong> such as vans, furniture or stacked goods: a 40ft high cube, which gives an extra 30 cm of height', '<strong>Heavy, compact cargo</strong> such as engines: often a 20ft, because heavy goods reach the weight limit before the space runs out'])}
<h2>How to choose</h2>
<p>Choose by <strong>volume</strong> for light, bulky goods, and by <strong>weight</strong> for dense goods like engines and machinery. If your cargo does not fill a container, ask about shipping it together with other cargo, which can be cheaper. Oversized items such as tractors or construction equipment may need special handling, so send us the dimensions.</p>
<p>Not sure? Send us a list or a photo of your cargo on <a href="{WA}" target="_blank" rel="noopener">WhatsApp</a> and we&rsquo;ll recommend the right size in your <a href="quote.html">quote</a>.</p>
""",
  'faq': [
   ('How many cars fit in a 20ft container?', 'Usually one car, with some room for parts.'),
   ('What is the difference between a 40ft and a 40ft high cube container?', 'The same length and width, but a high cube is about 30 cm taller inside (around 2.69 m instead of 2.39 m), giving roughly 76 m³ instead of 67 m³.'),
   ('How much weight can a 20ft container carry?', 'Typically around 28,000 kg of cargo, but each container lists its own maximum on the door.'),
  ],
 },
 {
  'slug': 'guide-what-to-prepare-before-booking.html',
  'title': 'What to prepare before booking a shipment',
  'h1': 'What to prepare <em>before booking</em>',
  'seo': 'What to Prepare Before Booking a Shipment from Germany | EL-ROI',
  'desc': 'A checklist of the details and documents to have ready before booking sea freight from Germany, so your shipment moves without delays.',
  'img': 'chassisrear', 'pos': 'center 50%', 'badge': 'Checklist', 'mins': 3,
  'lede': 'Have these ready and your quote, booking and shipment all move faster.',
  'body': f"""
<p class="lead-p">Most delays happen because a detail or document arrives late. Use this checklist before you contact us.</p>
<h2>About you and the receiver</h2>
{tick(['Full name, or company name', 'Address', 'Phone number and email', 'The receiver&rsquo;s name, address and phone number at the destination'])}
<h2>About the cargo</h2>
{tick(['Pickup location and destination', 'Cargo type: vehicle, container load, machinery, fragile goods, documents or general cargo', 'Approximate weight and number of packages', 'Dimensions for anything large or oversized', 'Photos of the cargo (very helpful for a fast, accurate quote)'])}
<h2>Documents</h2>
{tick(['Vehicle documents, for cars, trucks and tractors', 'Purchase invoices', 'Any special declaration, such as the <a href="guide-form-m-nigeria.html">Form M</a> for Nigeria'])}
<h2>Good to know</h2>
<p>We ship by sea freight, usually around two weeks after the container is loaded. Payment is arranged directly with our team, never through the website. Some cargo can&rsquo;t be shipped for safety or legal reasons, so ask us if you are unsure.</p>
<p>Ready? <a href="quote.html">Request a quote</a> or <a href="book.html">book a shipment</a>.</p>
""",
  'faq': [],
 },
]


def guide_page(g):
    others = [o for o in GUIDES if o is not g][:3]
    related = ''.join(f'''<a class="rel-card" href="{o['slug']}"><div class="post-img">{img(o['img'])}</div><span class="badge">{o['badge']}</span><h3>{o['title']}</h3></a>''' for o in others)
    body = page_hero('Guides', f"{g['badge']} guide &middot; {g['mins']} min read", g['h1'], g['lede'], g['img'], g['pos']).replace(
        '<span aria-current="page">Guides</span>', '<a href="blog.html">Guides</a><span aria-hidden="true">/</span><span aria-current="page">' + g['badge'] + '</span>') + f'''
<section>
  <div class="container">
    <article class="prose">
{g['body']}
      <p class="policy-date">Published by EL-ROI Shipping Services, Essen &middot; Updated 26 September 2026</p>
    </article>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="section-head"><div><span class="eyebrow">Keep reading</span><h2>More <em>shipping guides</em></h2></div></div>
    <div class="grid g-3">{related}</div>
  </div>
</section>

{CTA}'''
    ld = [{'@context': 'https://schema.org', '@type': 'Article', 'headline': g['title'], 'description': g['desc'],
           'image': SITE_URL + IMG[g['img']][0], 'datePublished': '2026-09-26', 'dateModified': '2026-09-26',
           'author': {'@type': 'Organization', 'name': 'EL-ROI Shipping Services', 'url': SITE_URL},
           'publisher': {'@type': 'Organization', 'name': 'EL-ROI Shipping Services', 'logo': {'@type': 'ImageObject', 'url': SITE_URL + 'assets/favicon.svg'}},
           'mainEntityOfPage': SITE_URL + g['slug']}]
    if g['faq']:
        ld.append({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in g['faq']]})
    write(g['slug'], g['seo'], g['desc'], 'blog.html', body, extra_ld=ld, crumbs=[('Guides', 'blog.html'), (g['title'], g['slug'])])


for _g in GUIDES:
    guide_page(_g)


featured = GUIDES[0]
cards = ''.join(f'''<a class="post" href="{x['slug']}" data-reveal>
        <div class="post-img">{img(x['img'])}</div>
        <span class="badge">{x['badge']} &middot; {x['mins']} min read</span>
        <h3>{x['title']}</h3>
        <p>{x['desc']}</p>
      </a>''' for x in GUIDES[1:])
blog = page_hero('Guides', 'Guides &amp; news', 'Shipping guides <em>&amp; news</em>',
                 'Practical, plain-English guides to shipping from Germany, and updates from EL-ROI Shipping Services.', 'redchassis', 'center 55%') + f'''
<section>
  <div class="container">
    <div class="section-head" data-reveal><div><span class="eyebrow">Shipping guides</span><h2>Know before <em>you ship</em></h2></div></div>
    <div class="posts">
      <a class="post featured" href="{featured['slug']}" data-reveal>
        <div class="post-img">{img(featured['img'])}</div>
        <div>
          <span class="badge">{featured['badge']} &middot; {featured['mins']} min read</span>
          <h3>{featured['title']}</h3>
          <p>{featured['desc']}</p>
          <span class="link-arrow" style="margin-top:22px">Read the guide {ARROW}</span>
        </div>
      </a>
      {cards}
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="section-head" data-reveal><div><span class="eyebrow">Company news</span><h2>From <em>EL-ROI</em></h2></div></div>
    <div class="posts">
      <article class="post" data-reveal>
        <div class="post-img">{img('tractor')}</div>
        <span class="badge">Company news</span>
        <h3>Welcome to our new website</h3>
        <p>Our new online home makes it easier to request quotes, book shipments and reach our team in Essen and Lagos.</p>
      </article>
      <article class="post" data-reveal style="--d:1">
        <div class="post-img">{img('volvo')}</div>
        <span class="badge">Company news</span>
        <h3>Over 20 years of shipping, and counting</h3>
        <p>Since 1999 we have been moving vehicles, containers and heavy cargo from Germany to the world.</p>
      </article>
    </div>
  </div>
</section>

{CTA}'''

write('blog.html', 'Guides', 'Guides', 'blog.html', blog, crumbs=[('Guides', 'blog.html')])

# =====================================================================
# FAQ
# =====================================================================
FAQS = [
    ('Do you only ship to Nigeria?', 'No. We ship from Germany to any part of the world by sea freight. Our major routes are to Belgium, Austria and Holland, and we have our own office in Lagos, Nigeria.'),
    ('Can you ship a car from Germany to Nigeria?', 'Yes. Cars, vans, trucks and tractors are some of the most common things we ship. See our <a href="guide-ship-car-germany-to-nigeria.html">step-by-step guide to shipping a car to Nigeria</a>.'),
    ('What container sizes do you use?', '20ft and 40ft containers, including 40ft high cube. See <a href="guide-20ft-vs-40ft-container.html">20ft vs 40ft containers</a> to find the right size.'),
    ('How long does shipping take?', 'Delivery time depends on the destination country, but on average it takes around two weeks after your container is loaded onto the ship.'),
    ('What cargo types do you handle?', 'We handle general cargo, containers, vehicles, fragile goods, oversized and heavy cargo, machinery and equipment, and documents.'),
    ('What information do I need to book a shipment?', 'Your full name, phone number, email, pickup location, destination, cargo type, cargo weight, number of packages, and preferred shipping method.'),
    ('Do you offer shipment tracking?', 'Shipment tracking is coming soon. In the meantime, our team will keep you updated directly on your shipment status.'),
    ('What documents are needed for special declarations?', "Certain cargo, like vehicles, requires vehicle documentation and may need a Form M special declaration. We'll guide you through what's required for your shipment. See <a href=\"guide-form-m-nigeria.html\">What is Form M?</a>"),
    ('Who pays customs duties and import taxes?', 'Customs duties, import taxes and port charges at the destination are paid by the receiver or importer. They are not included in our freight price unless we agree otherwise in writing.'),
    ('Is my cargo insured?', 'Our liability is limited by law, which can be less than the value of your cargo, so we recommend cargo insurance. We can arrange it on request.'),
    ('Where are your offices?', 'Our headquarters is at Ripshorster Str. 379, 45357 Essen, Germany, and our second office is in Olodi Apapa, Lagos, Nigeria.'),
    ('Can I pay through the website?', 'Online payment is coming soon. For now, payment details are arranged directly with our team, never submitted through the website form.'),
]
faq_items = '\n'.join(
    f'''      <div class="faq-item"><button class="faq-q" aria-expanded="false" aria-controls="faq-{i}">{q}<span class="faq-icon" aria-hidden="true"></span></button><div class="faq-a" id="faq-{i}"><div><p>{a}</p></div></div></div>'''
    for i, (q, a) in enumerate(FAQS))

faq = page_hero('FAQ', 'Support', 'Frequently asked <em>questions</em>',
                'Clear answers to the questions we hear most.', 'loading') + f'''
<section>
  <div class="container faq-layout">
    <aside class="faq-aside" data-reveal>
      <div class="card card-navy has-photo">{photo_bg("volvo", "center 30%", "soft")}
        <span class="card-kicker">Still have a question?</span>
        <h3>Talk to a real person</h3>
        <p>You deal with people who know your shipment, not a call centre queue.</p>
        <div class="contact-lines">
          <a href="tel:{TEL}">{PHONE_ICON}{PHONE}</a>
          <a href="{WA}" target="_blank" rel="noopener">{WA_ICON}Chat on WhatsApp</a>
          <a href="mailto:{EMAIL}">{MAIL_ICON}Email us</a>
        </div>
      </div>
    </aside>
    <div class="faq" data-reveal style="--d:1">
{faq_items}
    </div>
  </div>
</section>

{CTA}'''

import re as _re
FAQ_LD = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
    {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': _re.sub('<[^>]+>', '', a)}} for q, a in FAQS]}
write('faq.html', 'FAQ', 'FAQ', 'faq.html', faq, extra_ld=[FAQ_LD])

# =====================================================================
# CONTACT
# =====================================================================
contact = page_hero('Contact', 'Get in touch', 'Contact <em>EL-ROI Shipping</em>',
                    'Send a message, call, or chat with us on WhatsApp.', 'tractor', 'center 55%') + f'''
<section>
  <div class="container form-layout">
    <div class="form-panel" data-reveal>
      <h2 class="form-title">Send us a message</h2>
      <p class="form-intro">We'll get back to you by email or phone.</p>
      <form action="{FORMSPREE}" method="POST" data-wa="Hello EL-ROI, message from your website:">
        <div class="form-row">
          <div class="field"><label for="c-name">Full name <b>*</b></label><input id="c-name" name="Full Name" type="text" autocomplete="name" required></div>
          <div class="field"><label for="c-email">Email address <b>*</b></label><input id="c-email" name="Email" type="email" autocomplete="email" required></div>
        </div>
        <div class="field"><label for="c-phone">Phone number</label><input id="c-phone" name="Phone" type="tel" autocomplete="tel"></div>
        <div class="field"><label for="c-message">Message <b>*</b></label><textarea id="c-message" name="Message" placeholder="What are you shipping, and where to?" required></textarea></div>
        <div class="form-foot">
          <small>Never send bank details or passwords through this form. See our <a href="privacy.html">Privacy Policy</a>. Bookings are subject to our <a href="terms.html">Terms &amp; Conditions</a>.</small>
          <button type="submit" class="btn btn-primary">Send Message {ARROW}</button>
        </div>
      </form>
    </div>
    <div class="aside-stack">
      <div class="card office" data-reveal>
        <span class="card-kicker">Headquarters</span>
        <h3>Essen, Germany</h3>
        <address>Ripshorster Str. 379<br>45357 Essen, Germany</address>
        <div class="contact-lines">
          <a href="tel:{TEL}">{PHONE_ICON}{PHONE}</a>
          <a class="break" href="mailto:{EMAIL}">{MAIL_ICON}{EMAIL}</a>
        </div>
      </div>
      <div class="card office" data-reveal style="--d:1">
        <span class="card-kicker">Nigeria office</span>
        <h3>Lagos, Nigeria</h3>
        <address>Olodi Apapa<br>Lagos, Nigeria</address>
      </div>
      <div class="card card-navy has-photo" data-reveal style="--d:2">{photo_bg("loaded", "center 50%", "soft")}
        <h3>Prefer WhatsApp?</h3>
        <p style="margin-bottom:22px">Message us with your cargo and destination.</p>
        <a class="btn btn-primary btn-block" href="{WA}" target="_blank" rel="noopener">{WA_ICON} Chat on WhatsApp</a>
      </div>
    </div>
  </div>
  {map_block()}
</section>
'''

write('contact.html', 'Contact | EL-ROI Shipping Services',
      'Contact EL-ROI Shipping Services in Essen, Germany and Lagos, Nigeria. Phone, email, WhatsApp and office map.',
      'contact.html', contact)

# =====================================================================
# QUOTE / BOOK
# =====================================================================
CARGO_OPTIONS = ['General Cargo', 'Containers', 'Vehicles', 'Fragile Goods', 'Oversized / Heavy Cargo', 'Machinery / Equipment', 'Documents']
cargo_opts = ''.join(f'<option value="{c}">{c}</option>' for c in CARGO_OPTIONS)

ASIDE_NEXT = f'''<div class="card card-navy has-photo" data-reveal>{photo_bg("yardload", "center 40%", "soft")}
        <span class="card-kicker">What happens next</span>
        <ol class="next-steps">
          <li><div><strong>We review your details</strong><span>Our team checks your cargo, route and paperwork needs.</span></div></li>
          <li><div><strong>You get a clear estimate</strong><span>The full cost up front, with no hidden fees added later.</span></div></li>
          <li><div><strong>You decide</strong><span>No pressure. Book only when you're ready.</span></div></li>
        </ol>
      </div>
      <div class="card" data-reveal style="--d:1">
        <span class="card-kicker">Prefer to talk?</span>
        <h3>Call or WhatsApp</h3>
        <div class="contact-lines">
          <a href="tel:{TEL}">{PHONE_ICON}{PHONE}</a>
          <a href="{WA}" target="_blank" rel="noopener">{WA_ICON}Chat on WhatsApp</a>
        </div>
      </div>'''

quote = page_hero('Get a Quote', 'Get a quote', 'Request a <em>shipping quotation</em>',
                  "Tell us about your cargo and we'll get back to you with a transparent, no-pressure estimate.",
                  'volvo', 'center 35%') + f'''
<section>
  <div class="container form-layout">
    <div class="form-panel" data-reveal>
      <h2 class="form-title">Your shipment</h2>
      <p class="form-intro">Fields marked <b style="color:var(--gold-deep)">*</b> are required.</p>
      <form id="quote-form" action="{FORMSPREE}" method="POST" data-wa="Hello EL-ROI, I'd like a shipping quote:">
        <div class="form-row">
          <div class="field"><label for="q-name">Full name <b>*</b></label><input id="q-name" name="Full Name" type="text" autocomplete="name" required></div>
          <div class="field"><label for="q-company">Company name</label><input id="q-company" name="Company Name" type="text" autocomplete="organization"></div>
        </div>
        <div class="form-row">
          <div class="field"><label for="q-phone">Phone number <b>*</b></label><input id="q-phone" name="Phone" type="tel" autocomplete="tel" required></div>
          <div class="field"><label for="q-email">Email address <b>*</b></label><input id="q-email" name="Email" type="email" autocomplete="email" required></div>
        </div>
        <div class="field"><label for="q-address">Address</label><input id="q-address" name="Address" type="text" autocomplete="street-address"></div>
        <div class="form-row">
          <div class="field"><label for="q-pickup">Pickup location <b>*</b></label><input id="q-pickup" name="Pickup Location" type="text" placeholder="e.g. Essen, Germany" required></div>
          <div class="field"><label for="q-destination">Destination <b>*</b></label><input id="q-destination" name="Destination" type="text" placeholder="e.g. Antwerp, Belgium" required></div>
        </div>
        <div class="form-row">
          <div class="field">
            <label for="q-cargo">Cargo type <b>*</b></label>
            <select id="q-cargo" name="Cargo Type" required><option value="">Select cargo type</option>{cargo_opts}</select>
          </div>
          <div class="field"><label for="q-weight">Cargo weight (kg)</label><input id="q-weight" name="Cargo Weight" type="number" min="0" inputmode="numeric"></div>
        </div>
        <div class="form-row">
          <div class="field"><label for="q-packages">Number of packages</label><input id="q-packages" name="Number of Packages" type="number" min="1" inputmode="numeric"></div>
          <div class="field">
            <label for="q-method">Preferred shipping method</label>
            <select id="q-method" name="Preferred Shipping Method"><option value="Sea Freight">Sea Freight</option></select>
          </div>
        </div>
        <div class="field">
          <label for="q-vehicle-doc">Vehicle document / special declaration reference (if applicable)</label>
          <input id="q-vehicle-doc" name="Vehicle Document" type="text">
          <span class="field-note">Include Form M reference if your cargo needs a special declaration.</span>
        </div>
        <div class="field"><label for="q-notes">Additional details</label><textarea id="q-notes" name="Notes" placeholder="Make and model, dimensions, weight, number of items..."></textarea></div>
        <div class="form-foot">
          <small>Want a rough figure first? Try the <a href="calculator.html">shipping calculator</a>. How we use your details: <a href="privacy.html">Privacy Policy</a>. Bookings are subject to our <a href="terms.html">Terms &amp; Conditions</a>.</small>
          <button type="submit" class="btn btn-primary">Request Quote {ARROW}</button>
        </div>
      </form>
    </div>
    <div class="aside-stack">
      {ASIDE_NEXT}
    </div>
  </div>
</section>
'''

write('quote.html', 'Get a Quote | EL-ROI Shipping Services',
      'Request a transparent, no-pressure shipping quotation from EL-ROI Shipping Services.',
      'quote.html', quote)

book = page_hero('Book a Shipment', 'Book a shipment', 'Start your <em>shipment booking</em>',
                 'Provide your shipment details below. Our team will confirm availability and next steps by phone or email.',
                 'yardload', 'center 55%') + f'''
<section>
  <div class="container form-layout">
    <div class="form-panel" data-reveal>
      <h2 class="form-title">Booking request</h2>
      <p class="form-intro">Fields marked <b style="color:var(--gold-deep)">*</b> are required.</p>
      <form action="{FORMSPREE}" method="POST" enctype="multipart/form-data" data-wa="Hello EL-ROI, I'd like to book a shipment:">
        <div class="form-row">
          <div class="field"><label for="b-name">Full name <b>*</b></label><input id="b-name" name="Full Name" type="text" autocomplete="name" required></div>
          <div class="field"><label for="b-phone">Phone number <b>*</b></label><input id="b-phone" name="Phone" type="tel" autocomplete="tel" required></div>
        </div>
        <div class="form-row">
          <div class="field"><label for="b-email">Email address <b>*</b></label><input id="b-email" name="Email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="b-company">Company or private name</label><input id="b-company" name="Company / Private Name" type="text" autocomplete="organization"></div>
        </div>
        <div class="field"><label for="b-address">Address <b>*</b></label><input id="b-address" name="Address" type="text" autocomplete="street-address" required></div>
        <div class="form-row">
          <div class="field"><label for="b-pickup">Pickup location <b>*</b></label><input id="b-pickup" name="Pickup Location" type="text" required></div>
          <div class="field"><label for="b-destination">Destination <b>*</b></label><input id="b-destination" name="Destination" type="text" required></div>
        </div>
        <div class="form-row">
          <div class="field">
            <label for="b-cargo">Cargo type <b>*</b></label>
            <select id="b-cargo" name="Cargo Type" required><option value="">Select cargo type</option>{cargo_opts}</select>
          </div>
          <div class="field"><label for="b-weight">Cargo weight (kg)</label><input id="b-weight" name="Cargo Weight" type="number" min="0" inputmode="numeric"></div>
        </div>
        <div class="form-row">
          <div class="field"><label for="b-packages">Number of packages</label><input id="b-packages" name="Number of Packages" type="number" min="1" inputmode="numeric"></div>
          <div class="field">
            <label for="b-method">Preferred shipping method</label>
            <select id="b-method" name="Preferred Method"><option value="Sea Freight">Sea Freight</option></select>
          </div>
        </div>
        <div class="field">
          <label for="b-vehicle-doc">Vehicle document / special declaration reference (if applicable)</label>
          <input id="b-vehicle-doc" name="Vehicle Document" type="text">
          <span class="field-note">Include your Form M reference if your cargo needs a special declaration.</span>
        </div>
        <div class="field">
          <label for="b-docs">Upload cargo / shipping documents (optional)</label>
          <input id="b-docs" name="Documents" type="file" multiple accept=".pdf,.jpg,.jpeg,.png">
          <span class="field-note">PDF, JPG or PNG. Never upload bank details, passwords or payment credentials here.</span>
        </div>
        <div class="form-foot">
          <small>A booking request doesn't commit you to anything. We confirm the details with you first. See our <a href="privacy.html">Privacy Policy</a>. Bookings are subject to our <a href="terms.html">Terms &amp; Conditions</a>.</small>
          <button type="submit" class="btn btn-primary">Submit Booking Request {ARROW}</button>
        </div>
      </form>
    </div>
    <div class="aside-stack">
      {ASIDE_NEXT}
    </div>
  </div>
</section>
'''

write('book.html', 'Book a Shipment | EL-ROI Shipping Services',
      'Start your shipment booking with EL-ROI Shipping Services. Sea freight from Germany to any part of the world.',
      'book.html', book)

# =====================================================================
# CALCULATOR
# =====================================================================
cargo_chips = ''.join(
    f'<label class="chip"><input type="radio" name="cargo" value="{c}"{" required" if i == 0 else ""}><span>{c}</span></label>'
    for i, c in enumerate(CARGO_OPTIONS))
DESTS = ['Europe (Belgium, Austria, Holland)', 'Lagos, Nigeria', 'Rest of World']
dest_chips = ''.join(
    f'<label class="chip"><input type="radio" name="dest" value="{c}"{" required" if i == 0 else ""}><span>{c}</span></label>'
    for i, c in enumerate(DESTS))

calculator = page_hero('Calculator', 'Estimate', 'Shipping cost <em>calculator</em>',
                       'Get a rough estimate based on cargo type, weight and destination. Final pricing is confirmed through a formal quote.',
                       'deere3140', 'center 45%') + f'''
<section>
  <div class="container calc">
    <form class="calc-panel" id="calc-form" data-reveal>
      <div class="calc-step">
        <div class="label" id="lbl-cargo"><i>01</i> Cargo type</div>
        <fieldset class="chips" aria-labelledby="lbl-cargo">{cargo_chips}</fieldset>
      </div>
      <div class="calc-step">
        <div class="label"><i>02</i> <label for="calc-weight">Estimated weight</label></div>
        <div class="weight-row">
          <input type="range" id="calc-range" min="0" max="1000" step="1" value="500" aria-label="Weight slider">
          <div class="weight-input"><input type="number" id="calc-weight" min="1" max="100000" value="1500" inputmode="numeric"><span>KG</span></div>
        </div>
        <div class="presets">
          <button type="button" data-kg="500">Pallet ~500 kg</button>
          <button type="button" data-kg="1500">Car ~1,500 kg</button>
          <button type="button" data-kg="5000">Tractor ~5,000 kg</button>
          <button type="button" data-kg="7500">Truck ~7,500 kg</button>
        </div>
      </div>
      <div class="calc-step">
        <div class="label" id="lbl-dest"><i>03</i> Destination</div>
        <fieldset class="chips" aria-labelledby="lbl-dest">{dest_chips}</fieldset>
      </div>
    </form>
    <div class="calc-result has-photo" data-reveal style="--d:1" aria-live="polite">
      {photo_bg("msc", "center 40%")}
      <div>
        <span class="eyebrow">Estimated cost</span>
        <div class="calc-amount" id="calc-amount">&euro; &mdash;</div>
      </div>
      <div class="calc-breakdown">
        <div><span>Base rate</span><strong id="b-rate">&mdash;</strong></div>
        <div><span>Chargeable weight</span><strong id="b-weight">&mdash;</strong></div>
        <div><span>Route factor</span><strong id="b-route">&mdash;</strong></div>
      </div>
      <p class="calc-caveat">This is a rough estimate only and does not reflect final pricing. Request a formal quote for accurate costs.</p>
      <a class="btn btn-primary btn-block" id="calc-cta" href="quote.html" aria-disabled="true">Request a formal quote {ARROW}</a>
    </div>
  </div>
</section>
'''

write('calculator.html', 'Shipping Calculator | EL-ROI Shipping Services',
      'Get a rough shipping cost estimate by cargo type, weight and destination. Final pricing confirmed by formal quote.',
      'calculator.html', calculator)

# =====================================================================
# PRIVACY POLICY
# =====================================================================
PRIV = [
 ('who', 'Who we are', f"""<p>This website is operated by <strong>EL-ROI Shipping Services</strong>, Ripshorster Str. 379, 45357 Essen, Germany (the &ldquo;controller&rdquo; under the EU General Data Protection Regulation, GDPR). We also have an office in Olodi Apapa, Lagos, Nigeria.</p>
<p>Questions about your data: <a href="mailto:{EMAIL}">{EMAIL}</a> or <a href="tel:{TEL}">{PHONE}</a>.</p>"""),
 ('collect', 'What we collect', """<p>We only collect what you choose to send us:</p>
<ul class="checklist"><li><strong>Quote, booking and contact forms:</strong> name, company or private name, phone number, email, address, pickup location, destination, cargo type, weight, number of packages, shipping method, vehicle document or Form M reference, and any message you write.</li>
<li><strong>Uploaded documents</strong> (booking form): cargo or shipping documents you attach.</li>
<li><strong>WhatsApp, phone and email:</strong> whatever you send us through those channels.</li></ul>
<p>We do not use analytics, advertising trackers or tracking cookies, and we never ask for bank details, passwords or payment credentials through this website.</p>"""),
 ('use', 'Why we use it', """<ul class="checklist"><li>To prepare quotes, handle bookings and answer your questions (GDPR Art. 6(1)(b): steps before and performance of a contract).</li>
<li>To arrange shipping documents and customs declarations, and to keep records required by law (Art. 6(1)(c): legal obligation).</li>
<li>To keep in touch about a shipment you asked us about (Art. 6(1)(f): our legitimate interest in running our business).</li></ul>
<p>We do not sell your data or use it for advertising.</p>"""),
 ('share', 'Who we share it with', """<p>Only where needed to run the website or move your cargo:</p>
<ul class="checklist"><li><strong>Formspree</strong> (USA): receives form submissions and forwards them to our email.</li>
<li><strong>WhatsApp / Meta</strong>: if you contact us on WhatsApp or a form opens WhatsApp for you.</li>
<li><strong>GitHub Pages</strong> (hosting): processes technical data such as your IP address to deliver the site.</li>
<li><strong>Google</strong>: the office maps (Google Maps) load from Google servers, which receive your IP address. Our website fonts are hosted on our own site, so no data goes to Google for them. The maps only load after you agree in our privacy settings (Art. 6(1)(a) GDPR and &sect; 25(1) TDDDG: consent). If you decline, you can still use the &ldquo;Open in Google Maps&rdquo; link.</li>
<li><strong>Shipping partners, ports and customs authorities</strong>: the details needed to ship your cargo.</li></ul>
<p>Some of these providers are outside the EU. Where that is the case, transfers rely on safeguards such as the EU&ndash;US Data Privacy Framework or the European Commission&rsquo;s standard contractual clauses.</p>"""),
 ('keep', 'How long we keep it', """<p>Enquiries that do not lead to a shipment are deleted within 12 months. Records of shipments and invoices are kept for as long as German commercial and tax law requires (usually 6 to 10 years), then deleted.</p>"""),
 ('rights', 'Your rights', f"""<p>You can ask us to show you, correct, delete or restrict the data we hold about you, to object to its use, or to receive it in a portable format. Where we rely on your consent, you can withdraw it at any time. Just email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<p>You can also complain to a data protection authority, for example the one responsible for us: Landesbeauftragte f&uuml;r Datenschutz und Informationsfreiheit Nordrhein-Westfalen (LDI NRW), D&uuml;sseldorf. Customers in Nigeria can contact the Nigeria Data Protection Commission (NDPC).</p>"""),
 ('cookies', 'Cookies', """<p>This website does not set cookies of its own. When you first visit, we ask whether you allow the Google Maps office maps, which can set Google cookies. Your choice is saved in your browser&rsquo;s local storage (never sent to us) so we don&rsquo;t ask again. You can change or withdraw it at any time with &ldquo;Cookie settings&rdquo; at the bottom of every page.</p>"""),
 ('changes', 'Changes', """<p>We may update this policy when our services or the law change. The date below shows the latest version.</p>"""),
]
toc = ''.join(f'<li><a href="#{k}">{t}</a></li>' for k, t, _ in PRIV)
secs = '\n'.join(f'<section class="policy-sec" id="{k}"><h2>{t}</h2>{body}</section>' for k, t, body in PRIV)
privacy = page_hero('Privacy Policy', 'Legal', 'Privacy <em>policy</em>',
                    'How EL-ROI Shipping Services collects, uses and protects your personal data.', 'loaded', 'center 55%') + f'''
<section>
  <div class="container policy">
    <aside class="policy-toc"><span class="card-kicker">On this page</span><ol>{toc}</ol></aside>
    <div class="policy-body">
{secs}
      <p class="policy-date">Last updated: 26 September 2026</p>
    </div>
  </div>
</section>
'''
write('privacy.html', 'Privacy Policy | EL-ROI Shipping Services',
      'How EL-ROI Shipping Services collects, uses and protects your personal data.', '', privacy)

# =====================================================================
# TERMS & CONDITIONS
# =====================================================================
TERMS = [
 ('scope', 'Scope', """<p>These terms apply to all quotes, bookings and freight forwarding services provided by <strong>EL-ROI Shipping Services</strong>, Ripshorster Str. 379, 45357 Essen, Germany (&ldquo;we&rdquo;, &ldquo;us&rdquo;), and to the use of this website. Anything we agree with you individually in writing takes priority over these terms.</p>
<p>Where we agree it with business customers, our services are also carried out under the German Freight Forwarders&rsquo; Standard Terms and Conditions (ADSp 2017). Mandatory law always applies, including the German Commercial Code (HGB) and international transport conventions.</p>"""),
 ('quotes', 'Quotes and estimates', """<ul class="checklist"><li>A quote is based on the information you give us (cargo type, dimensions, weight, pickup point and destination). If that information turns out to be different, the price may change, and we will tell you before going ahead.</li>
<li>The online shipping calculator gives a rough, non-binding estimate only.</li>
<li>Unless stated otherwise, quotes do not include customs duties, import taxes, port and terminal charges at destination, storage, inspections or fees charged by authorities.</li>
<li>Quotes are valid for the period stated on them, or 14 days if no period is given, because freight rates change.</li></ul>"""),
 ('booking', 'Bookings', """<p>Sending a booking or quote request through the website, WhatsApp, phone or email does not create a contract. A contract is formed only when we confirm your booking in writing (email or WhatsApp is fine) and you accept the price.</p>"""),
 ('customer', 'Your responsibilities', """<ul class="checklist"><li>Give us complete and correct details about the cargo, the sender and the receiver.</li>
<li>Provide the documents needed for export and import on time, including vehicle documents and, where required, the Form M special declaration.</li>
<li>Make sure the cargo is legal to export and import, and properly packed, secured and labelled unless we have agreed to do this.</li>
<li>Remove fuel, batteries, gas bottles and personal belongings from vehicles unless we have agreed otherwise in writing.</li>
<li>Do not hand us dangerous, illegal or restricted goods without telling us first. Ask us before booking if you are unsure whether your cargo qualifies.</li></ul>
<p>You are responsible for costs, delays, fines or damage caused by missing or incorrect information or documents.</p>"""),
 ('prices', 'Prices and payment', """<ul class="checklist"><li>Payment terms are agreed with you directly and shown on our invoice. We never ask for bank details or payment credentials through this website.</li>
<li>Unless agreed otherwise, freight charges are due before the cargo is loaded or released.</li>
<li>Customs duties, taxes and destination charges are payable by you (or the receiver), even if they arise after shipping.</li>
<li>We may hold the cargo or its documents until outstanding amounts for that shipment have been paid, as the law allows.</li></ul>"""),
 ('transit', 'Transit times', """<p>Transit times are estimates. Sea freight usually takes around two weeks after the container is loaded, but this depends on the destination, the shipping line, port congestion, weather and customs. We are not responsible for delays caused by carriers, authorities or events beyond our control, and we will keep you informed.</p>"""),
 ('liability', 'Liability and insurance', """<ul class="checklist"><li>Our liability for loss of or damage to cargo is limited to the amounts set by mandatory law (such as the HGB) and the international conventions that apply to the transport, and, where agreed, by the ADSp.</li>
<li>These limits do not apply where damage is caused intentionally or through gross negligence, or where the law does not allow a limit.</li>
<li>We are not liable for loss caused by incorrect information, poor packing by the sender, the nature of the goods, or acts of authorities.</li>
<li>Standard liability limits can be lower than the value of your cargo. We strongly recommend cargo insurance, and we can arrange it on request.</li></ul>"""),
 ('claims', 'Damage and claims', """<p>Please check the cargo on delivery. Visible loss or damage must be noted on the delivery documents and reported to us immediately. Hidden damage must be reported in writing within 7 days of delivery. Late reports can make it impossible to claim against the carrier.</p>"""),
 ('cancel', 'Cancellations', """<p>You can cancel a booking free of charge until we have made arrangements for it. After that, you pay the costs we have already incurred (for example container booking, collection, storage or documents). Once the cargo has been loaded onto the ship, the full freight charge is due.</p>"""),
 ('website', 'Using this website', """<p>The information on this website is general and may change. Photos show examples of our work. All content belongs to EL-ROI Shipping Services and may not be copied without permission. How we handle your personal data is explained in our <a href="privacy.html">Privacy Policy</a>.</p>"""),
 ('law', 'Law and jurisdiction', """<p>These terms are governed by German law. For business customers, the place of jurisdiction is Essen, Germany. Consumers keep any protections they have under the law of the country where they live. If any part of these terms is invalid, the rest remains in force.</p>"""),
]

def legal_page(items):
    toc = ''.join(f'<li><a href="#{k}">{t}</a></li>' for k, t, _ in items)
    secs = '\n'.join(f'<section class="policy-sec" id="{k}"><h2>{t}</h2>{body}</section>' for k, t, body in items)
    return f'''
<section>
  <div class="container policy">
    <aside class="policy-toc"><span class="card-kicker">On this page</span><ol>{toc}</ol></aside>
    <div class="policy-body">
{secs}
      <p class="policy-date">Questions: <a href="mailto:{EMAIL}">{EMAIL}</a> &middot; <a href="tel:{TEL}">{PHONE}</a><br>Last updated: 26 September 2026</p>
    </div>
  </div>
</section>
'''

terms = page_hero('Terms &amp; Conditions', 'Legal', 'Terms &amp; <em>conditions</em>',
                  'The terms that apply to our quotes, bookings and shipping services.', 'msc', 'center 45%') + legal_page(TERMS)
write('terms.html', 'Terms &amp; Conditions | EL-ROI Shipping Services',
      'Terms and conditions for quotes, bookings and freight forwarding services by EL-ROI Shipping Services.', '', terms)

# =====================================================================
# 404
# =====================================================================
lost = f'''<section class="lost dark has-photo">
  {photo_bg("transporter", "center 55%", "soft")}
  <div class="container">
    <span class="eyebrow">Error 404</span>
    <h1>This page has <em>gone off route.</em></h1>
    <p style="max-width:46ch;margin-bottom:32px">The page you're looking for doesn't exist or has moved.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="index.html">Back to home {ARROW}</a>
      <a class="btn btn-ghost" href="contact.html">Contact us</a>
    </div>
  </div>
</section>
'''
write('404.html', 'Page not found | EL-ROI Shipping Services', 'This page could not be found.', '', lost)


# =====================================================================
# SITEMAP + ROBOTS
# =====================================================================
PRIORITY = {'index.html': '1.0', 'services.html': '0.9', 'routes.html': '0.9', 'quote.html': '0.9', 'contact.html': '0.8', 'blog.html': '0.8', 'faq.html': '0.7', 'privacy.html': '0.2', 'terms.html': '0.2'}
urls = ''.join(f'  <url><loc>{SITE_URL}{page}</loc><lastmod>{LASTMOD}</lastmod><priority>{PRIORITY.get(name, "0.7" if name.startswith("guide-") else "0.6")}</priority></url>\n' for page, name in SITEMAP)
with open(os.path.join(OUT, 'sitemap.xml'), 'w') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')
with open(os.path.join(OUT, 'robots.txt'), 'w') as f:
    f.write('User-agent: *\nAllow: /\nDisallow: /.claude/\n\nSitemap: ' + SITE_URL + 'sitemap.xml\n')
HTACCESS = r'''# Generated by _build/build.py for Apache/LiteSpeed hosting (Hostinger)
Options -Indexes
ErrorDocument 404 /404.html

<IfModule mod_rewrite.c>
RewriteEngine On
# Build scripts, editor files and docs are not part of the site
RewriteRule ^(_build|\.claude|\.git)(/|$) - [R=404,L]
RewriteRule ^(README\.md|\.gitignore)$ - [R=404,L]
# One address: https, no www
RewriteCond %{HTTPS} off [OR]
RewriteCond %{HTTP_HOST} ^www\. [NC]
RewriteRule ^ https://elroishipping.de%{REQUEST_URI} [R=301,L]
</IfModule>

<IfModule mod_headers.c>
Header always set X-Content-Type-Options "nosniff"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set X-Frame-Options "SAMEORIGIN"
Header always set Strict-Transport-Security "max-age=31536000"
</IfModule>

# Assets carry a ?v= content hash, so they can be cached for a long time
<IfModule mod_expires.c>
ExpiresActive On
ExpiresDefault "access plus 1 hour"
ExpiresByType text/html "access plus 0 seconds"
ExpiresByType text/css "access plus 1 year"
ExpiresByType application/javascript "access plus 1 year"
ExpiresByType text/javascript "access plus 1 year"
ExpiresByType image/jpeg "access plus 1 year"
ExpiresByType image/png "access plus 1 year"
ExpiresByType image/webp "access plus 1 year"
ExpiresByType image/svg+xml "access plus 1 year"
ExpiresByType font/woff2 "access plus 1 year"
ExpiresByType application/xml "access plus 1 day"
</IfModule>

<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css application/javascript text/javascript image/svg+xml application/xml text/plain
</IfModule>
'''
with open(os.path.join(OUT, '.htaccess'), 'w') as f:
    f.write(HTACCESS)
print('wrote sitemap.xml with', len(SITEMAP), 'pages, robots.txt and .htaccess')

# German site (/de/) is generated from the English pages above
import build_de
build_de.main()
