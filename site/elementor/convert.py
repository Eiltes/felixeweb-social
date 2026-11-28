"""Convert a built FelixeWeb page (site/pages/out/<slug>.html) into native Elementor data.

Sections/cards/rows -> Elementor containers (same tag, classes, id).
Text leaves (headings, paragraphs, lists, images, links) -> Text Editor widgets holding the exact original element.
Interactive pieces (data-* attributes, onclick, video, forms, carousels, scripts) -> HTML widgets.
Header/footer are placed with the [fw_part] shortcode (one shared Elementor template each).
"""
import json, re, secrets, sys
from bs4 import BeautifulSoup, NavigableString, Tag

CONTAINER_TAGS = {'div', 'section', 'header', 'footer', 'article', 'aside', 'nav', 'main', 'a'}
BLOCK_TAGS = {'div', 'section', 'header', 'footer', 'article', 'aside', 'nav', 'main', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
              'ul', 'ol', 'li', 'figure', 'blockquote', 'details', 'form', 'table', 'video', 'iframe', 'img', 'picture', 'button',
              'svg', 'canvas', 'dl', 'hr', 'a', 'figcaption', 'small', 'span', 'label', 'input', 'select', 'textarea'}
# whole components that must stay exactly as coded (JS-driven or structural)
COMPONENT_CLASSES = {'car', 'marquee', 'tm-split', 'tm-grid', 'faq', 'qlist', 'grain', 'bg-grid', 'orb'}
COMPONENT_IDS = {'tmSplit', 'tmGrid'}

used = set()
def nid():
    while True:
        i = secrets.token_hex(4)[:7]
        if i not in used:
            used.add(i); return i

def is_interactive(t):
    if not isinstance(t, Tag): return False
    if t.name in ('script', 'video', 'iframe', 'form', 'canvas', 'input', 'select', 'textarea', 'svg', 'button', 'details'): return True
    if any(a.startswith('data-') or a.startswith('on') for a in t.attrs): return True
    if set(t.get('class') or []) & COMPONENT_CLASSES or t.get('id') in COMPONENT_IDS: return True
    return False

def has_interactive_inside(t):
    return any(is_interactive(d) for d in t.find_all(True))

def block_children(t):
    return [c for c in t.children if isinstance(c, Tag)]

def has_loose_text(t):
    return any(isinstance(c, NavigableString) and c.strip() for c in t.children)

def is_container_candidate(t):
    if t.name not in CONTAINER_TAGS: return False
    if is_interactive(t): return False
    kids = block_children(t)
    if not kids or has_loose_text(t): return False
    # only split when at least one child is block-level (a card, a heading, a paragraph...)
    if not any(k.name in BLOCK_TAGS - {'span', 'small', 'label', 'a'} or (k.name == 'a' and is_container_candidate(k)) or (k.name in ('span',) and block_children(k) and any(x.name in ('div','p','h3','h4') for x in block_children(k))) for k in kids):
        return False
    if t.name == 'a':
        # anchor cards become linked containers only if every child is itself convertible
        return all(k.name in CONTAINER_TAGS | {'p','h1','h2','h3','h4','h5','h6','ul','ol','figure','img','span','small','b','strong','i','em'} for k in kids)
    return True

page_css = []  # inline styles moved to a page-level CSS block

def widget(kind, html, extra=None):
    w = {'id': nid(), 'elType': 'widget', 'isInner': False, 'elements': []}
    if kind == 'text':
        w.update(widgetType='text-editor', settings={'editor': html})
    else:
        w.update(widgetType='html', settings={'html': html})
    if extra: w['settings'].update(extra)
    return w

ZERO = {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True}

def container(t, depth, computed):
    cls = ' '.join(t.get('class') or [])
    s = {'content_width': 'full', 'padding': ZERO, 'margin': ZERO,
         'flex_gap': {'unit': 'px', 'size': 0, 'column': '0', 'row': '0', 'isLinked': True},
         'html_tag': t.name if t.name in CONTAINER_TAGS else 'div'}
    if cls: s['css_classes'] = cls
    if t.get('id'): s['_element_id'] = t['id']
    if t.get('style'):
        eid = t.get('id') or ('fw' + nid())
        s['_element_id'] = eid
        page_css.append(f'#{eid}{{{t["style"]}}}')
    for a in ('aria-label', 'role'):
        if t.get(a): pass  # free Elementor has no custom attributes; labels are kept on the leaves
    if t.name == 'a':
        s['link'] = {'url': t.get('href', ''), 'is_external': 'on' if t.get('target') == '_blank' else '', 'nofollow': 'on' if 'nofollow' in (t.get('rel') or []) else '', 'custom_attributes': ''}
    c = computed.get(path_of(t), {})
    if c.get('display') in ('flex', 'inline-flex'):
        s['flex_direction'] = c.get('fd', 'row')
        if c.get('fw') == 'wrap': s['flex_wrap'] = 'wrap'
    else:
        s['flex_direction'] = 'column'
    node = {'id': nid(), 'elType': 'container', 'isInner': depth > 0, 'settings': s, 'elements': []}
    for k in t.children:
        if isinstance(k, NavigableString):
            continue
        node['elements'].append(convert(k, depth + 1, computed))
    return node

def path_of(t):
    p = []
    while t is not None and t.name and t.name != '[document]':
        sib = [x for x in (t.parent.find_all(t.name, recursive=False) if t.parent else [])]
        p.append(f'{t.name}{sib.index(t) if t in sib else 0}')
        t = t.parent
    return '/'.join(reversed(p))

def convert(t, depth, computed):
    if is_container_candidate(t) and not has_only_interactive(t):
        return container(t, depth, computed)
    html = str(t)
    if is_interactive(t) or has_interactive_inside(t):
        return widget('html', html)
    return widget('text', html)

def has_only_interactive(t):
    return False

SAFE = re.compile(r'^[A-Za-z0-9_-]*$')
def data_to_classes(soup):
    # simple data-* attributes become fwd-<name>--<value> classes (restored by native.js), so cards stay editable
    for el in soup.find_all(True):
        for a in list(el.attrs):
            if a.startswith('data-') and a not in ('data-car', 'data-src') and SAFE.match(str(el[a])) and SAFE.match(a[5:]):
                el['class'] = (el.get('class') or []) + [f'fwd-{a[5:]}--{el[a] or "_"}']
                del el[a]

def build(html, computed, header_shortcode='[fw_part name="header"]', footer_shortcode='[fw_part name="footer"]'):
    soup = BeautifulSoup(html, 'html.parser')
    data_to_classes(soup)
    main = soup.find('main')
    ld = [str(x) for x in soup.find_all('script', type='application/ld+json')]
    top = []
    # header slot
    top.append({'id': nid(), 'elType': 'container', 'isInner': False, 'elements': [
        {'id': nid(), 'elType': 'widget', 'widgetType': 'shortcode', 'isInner': False, 'elements': [], 'settings': {'shortcode': header_shortcode}}],
        'settings': {'content_width': 'full', 'padding': ZERO, 'css_classes': 'fw-slot fw-slot-header'}})
    top.append(container(main, 0, computed))
    foot = [{'id': nid(), 'elType': 'widget', 'widgetType': 'shortcode', 'isInner': False, 'elements': [], 'settings': {'shortcode': footer_shortcode}}]
    extra = ''.join(ld)
    if page_css: extra += '<style id="fw-page-css">' + ''.join(page_css) + '</style>'
    if extra: foot.append(widget('html', extra))
    top.append({'id': nid(), 'elType': 'container', 'isInner': False, 'elements': foot,
                'settings': {'content_width': 'full', 'padding': ZERO, 'css_classes': 'fw-slot fw-slot-footer'}})
    return top

def stats(nodes):
    c = {'container': 0, 'text-editor': 0, 'html': 0, 'shortcode': 0}
    def walk(n):
        for x in n:
            if x['elType'] == 'container': c['container'] += 1
            else: c[x['widgetType']] += 1
            walk(x['elements'])
    walk(nodes)
    return c

if __name__ == '__main__':
    src, comp, out = sys.argv[1], sys.argv[2], sys.argv[3]
    computed = json.load(open(comp)) if comp != '-' else {}
    data = build(open(src).read(), computed)
    json.dump(data, open(out, 'w'))
    print(stats(data), 'page_css:', len(page_css))
