#!/usr/bin/env python3
"""Builds the German site (/de/) from the generated English pages."""
import glob, html, json, os, re, sys
from bs4 import BeautifulSoup, NavigableString, Comment

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from de_dict import DE, SAME
from extract import units, ATTRS, SKIP

OUT = os.path.dirname(HERE)  # the site root (parent of _build/)
SITE_URL = 'https://elroishipping.de/'
SVG_RE = re.compile(r'<svg.*?</svg>', re.S)


def norm(s):
    s = SVG_RE.sub('§', s)
    return html.unescape(re.sub(r'\s+', ' ', s).strip())


TABLE = {norm(k): v for k, v in DE.items()}
for k in SAME:
    TABLE.setdefault(norm(k), None)
MISSES = {}


def tr_plain(s, where):
    k = norm(s)
    if not k:
        return s
    if k in TABLE:
        return s if TABLE[k] is None else TABLE[k]
    if re.fullmatch(r'[\d\s.,:+~()\-–—%/€]*', k):
        return s
    MISSES.setdefault(k, where)
    return s


def escape_amp(v):
    return re.sub(r'&(?!#?\w+;)', '&amp;', v)


def localize_href(v):
    if not v or v.startswith(('http', 'mailto:', 'tel:', '#', 'data:', '//')):
        return v
    if v.startswith('de/'):
        return v[3:]
    if v.startswith('assets/') or v.startswith('guide-') or v in ('sitemap.xml',):
        return '../' + v
    return v


def build_page(path):
    name = os.path.basename(path)
    page = '' if name == 'index.html' else name
    soup = BeautifulSoup(open(path).read(), 'html.parser')
    soup.html['lang'] = 'de'

    # text units
    for el in units(soup):
        src = el.decode_contents()
        k = norm(src)
        if not k:
            continue
        val = TABLE.get(k, 'MISS') if k in TABLE else 'MISS'
        tail = ''
        if val == 'MISS':
            mt = re.match(r'(.*?)(<span[^>]*></span>)$', k)
            if mt and mt.group(1).strip() in TABLE and TABLE[mt.group(1).strip()] is not None:
                val, tail = TABLE[mt.group(1).strip()], mt.group(2)
        if val == 'MISS':
            if not re.fullmatch(r'[\d\s.,:+~()\-–—%/€]*', k):
                MISSES.setdefault(k, name)
            continue
        if val is None:
            continue
        svgs = SVG_RE.findall(src)
        out = escape_amp(val) + tail
        for sv in svgs:
            out = out.replace('§', sv, 1)
        el.clear()
        frag = BeautifulSoup(out, 'html.parser')
        for node in list(frag.contents):
            el.append(node)

    # attributes
    for el in soup.find_all(True):
        if el.name in SKIP:
            continue
        for a in ATTRS:
            if el.get(a):
                el[a] = tr_plain(el[a], name + '@' + a)
    for m in soup.find_all('meta'):
        if m.get('name') == 'description' or m.get('property') in ('og:title', 'og:description', 'og:image:alt'):
            m['content'] = tr_plain(m['content'], name + '@meta')
        if m.get('property') == 'og:url':
            m['content'] = SITE_URL + 'de/' + page
    og = soup.new_tag('meta'); og['property'] = 'og:locale'; og['content'] = 'de_DE'
    soup.head.append(og)
    for b in soup.find_all('base'):
        b['href'] = '/de/'
    for l in soup.find_all('link', rel='canonical'):
        l['href'] = SITE_URL + 'de/' + page

    # structured data
    for s in soup.find_all('script', type='application/ld+json'):
        data = json.loads(s.string)

        def walk(o):
            if isinstance(o, dict):
                for kk, v in list(o.items()):
                    if kk in ('name', 'description', 'text', 'slogan', 'contactType') and isinstance(v, str):
                        o[kk] = html.unescape(re.sub('<[^>]+>', '', tr_plain(v, name + '@ld')))
                    elif kk == 'item' and isinstance(v, str) and v.startswith(SITE_URL) and '/guide-' not in v:
                        o[kk] = SITE_URL + 'de/' + v[len(SITE_URL):]
                    else:
                        walk(v)
                if o.get('@type') == 'LocalBusiness' and 'availableLanguage' not in json.dumps(o):
                    pass
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(data)
        if data.get('@type') == 'LocalBusiness':
            data['url'] = SITE_URL + 'de/'
        s.string = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

    # links and asset paths
    for el in soup.find_all(True):
        for a in ('href', 'src'):
            if el.get(a):
                el[a] = localize_href(el[a])
        if el.get('style') and "url('assets/" in el['style']:
            el['style'] = el['style'].replace("url('assets/", "url('../assets/")
    # language switch
    for sw in soup.select('.lang-switch'):
        for a in sw.find_all('a'):
            if a.get('data-lang') == 'en':
                a['href'] = '../' + name
                a['class'] = []
            else:
                a['href'] = name
                a['class'] = ['on']

    os.makedirs(os.path.join(OUT, 'de'), exist_ok=True)
    out = str(soup)
    if not out.lstrip().lower().startswith('<!doctype'):
        out = '<!DOCTYPE html>\n' + out
    open(os.path.join(OUT, 'de', name), 'w').write(out)
    return page


def main():
    pages = [p for p in sorted(glob.glob(os.path.join(OUT, '*.html'))) if not os.path.basename(p).startswith('guide-')]
    done = [build_page(p) for p in pages]
    # sitemap: add German URLs with hreflang alternates
    sm = open(os.path.join(OUT, 'sitemap.xml')).read()
    locs = re.findall(r'<url><loc>(.*?)</loc><lastmod>(.*?)</lastmod><priority>(.*?)</priority></url>', sm)
    rows = []
    for loc, mod, pri in locs:
        page = loc[len(SITE_URL):]
        if page.startswith('guide-'):
            rows.append(f'  <url><loc>{loc}</loc><lastmod>{mod}</lastmod><priority>{pri}</priority></url>')
            continue
        alt = (f'<xhtml:link rel="alternate" hreflang="en" href="{SITE_URL}{page}"/>'
               f'<xhtml:link rel="alternate" hreflang="de" href="{SITE_URL}de/{page}"/>'
               f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE_URL}{page}"/>')
        rows.append(f'  <url><loc>{loc}</loc><lastmod>{mod}</lastmod><priority>{pri}</priority>{alt}</url>')
        rows.append(f'  <url><loc>{SITE_URL}de/{page}</loc><lastmod>{mod}</lastmod><priority>{pri}</priority>{alt}</url>')
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + '\n'.join(rows) + '\n</urlset>\n')
    print('German pages:', len(done), '| sitemap URLs:', len(rows))
    if MISSES:
        print('UNTRANSLATED (%d):' % len(MISSES))
        for k, w in MISSES.items():
            print('  ', w, '|', k[:160])


if __name__ == '__main__':
    main()
