import glob, json, os, re
from bs4 import BeautifulSoup, NavigableString, Comment
SKIP = {'script', 'style', 'svg'}
ATTRS = ['alt', 'title', 'placeholder', 'aria-label', 'data-caption', 'data-title', 'data-wa', 'data-place']
def units(soup):
    done = set()
    out = []
    for el in soup.find_all(True):
        if el.name in SKIP or any(p.name in SKIP for p in el.parents): continue
        if any(id(p) in done for p in el.parents): continue
        if any(isinstance(c, NavigableString) and not isinstance(c, Comment) and c.strip() for c in el.children):
            done.add(id(el)); out.append(el)
    return out
def pages():
    return [f for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '*.html'))) if not os.path.basename(f).startswith('guide-')]
if __name__ == '__main__':
    keys = {}
    for f in pages():
        soup = BeautifulSoup(open(f).read(), 'html.parser')
        for el in units(soup):
            k = el.decode_contents().strip()
            keys.setdefault(k, os.path.basename(f))
        for el in soup.find_all(True):
            for a in ATTRS:
                if el.get(a) and el.name not in SKIP: keys.setdefault(el[a].strip(), 'attr')
        for m in soup.find_all('meta'):
            if m.get('name') == 'description' or m.get('property') in ('og:title', 'og:description', 'og:image:alt'):
                keys.setdefault(m['content'], 'meta')
        for s in soup.find_all('script', type='application/ld+json'):
            def walk(o):
                if isinstance(o, dict):
                    for kk, v in o.items():
                        if kk in ('name', 'description', 'text', 'slogan', 'alternateName', 'contactType') and isinstance(v, str): keys.setdefault(v, 'ld')
                        else: walk(v)
                elif isinstance(o, list):
                    for v in o: walk(v)
            walk(json.loads(s.string))
    json.dump(keys, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'de_keys.json'), 'w'), ensure_ascii=False, indent=0)
    print(len(keys), 'unique strings;', sum(len(k) for k in keys), 'chars')
