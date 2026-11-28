"""Builds the shared CSS/JS for native Elementor pages and the header/footer HTML."""
import re, json, sys
from bs4 import BeautifulSoup
src = open('../pages/out/home.html').read()
s = BeautifulSoup(src, 'html.parser')
css = ''.join(x.string or '' for x in s.find_all('style', recursive=False))
# the old single-widget pages force every Elementor container to padding 0 !important; native pages need containers to take their own padding
css = css.replace('.elementor-section.elementor-section-boxed>.elementor-container,.e-con,.e-con-inner,.elementor-column-gap-default>.elementor-column>.elementor-element-populated{max-width:100%!important;padding:0!important;margin:0!important}', '')
assert '.e-con,.e-con-inner' not in css
import tinycss2
def boost_sel(sel):
    out=[]
    for part in sel.split(','):
        q=part.strip()
        if not q: continue
        if q.startswith(('html',':root','*','::')) or q.startswith('body'):
            q = q.replace('body', 'body.fwn', 1) if q.startswith('body') and not q.startswith('body.fwn') else q
            out.append(q)
        elif q.startswith(('.ready', '.menu-open')):
            out.append('body.fwn' + q)  # state classes the script puts on <body>
        else:
            out.append('body.fwn ' + q)
    return ','.join(out)
def boost(rules):
    res=''
    for r in rules:
        if r.type=='qualified-rule':
            sel=tinycss2.serialize(r.prelude).strip()
            res+=boost_sel(sel)+'{'+tinycss2.serialize(r.content)+'}'
        elif r.type=='at-rule':
            kw=r.at_keyword.lower()
            pre=tinycss2.serialize(r.prelude)
            if kw in ('media','supports') and r.content is not None:
                res+='@'+r.at_keyword+pre+'{'+boost(tinycss2.parse_rule_list(r.content, skip_whitespace=True, skip_comments=True))+'}'
            else:
                res+='@'+r.at_keyword+pre+('{'+tinycss2.serialize(r.content)+'}' if r.content is not None else ';')
    return res
css = boost(tinycss2.parse_stylesheet(css, skip_whitespace=True, skip_comments=True))
compat = '''
/* ---- FelixeWeb native Elementor compatibility ---- */
body.fwn{margin:0}
body.fwn .e-con{--padding-top:0px;--padding-right:0px;--padding-bottom:0px;--padding-left:0px;--margin-top:0px;--margin-right:0px;--margin-bottom:0px;--margin-left:0px;--gap:0px;--row-gap:0px;--column-gap:0px;--width:auto;--min-height:0px;--container-max-width:none;--content-width:100%;--border-radius:0;--flex-wrap:nowrap;max-width:none}
body.fwn .fwb{display:block}
body.fwn .e-con{min-width:auto}
body.fwn .e-con.e-flex>.elementor-widget,body.fwn .e-con>.elementor-widget{max-width:none;margin:0}
body.fwn .elementor-widget{--kit-widget-spacing:0px}
body.fwn:not(.elementor-editor-active) .elementor-widget-text-editor,
body.fwn:not(.elementor-editor-active) .elementor-widget-html,
body.fwn:not(.elementor-editor-active) .elementor-widget-shortcode,
body.fwn:not(.elementor-editor-active) .elementor-widget-container,
body.fwn:not(.elementor-editor-active) .elementor-shortcode,
body.fwn:not(.elementor-editor-active) .fw-slot,
body.fwn:not(.elementor-editor-active) .fw-part,
body.fwn:not(.elementor-editor-active) .fw-part>.elementor,
body.fwn:not(.elementor-editor-active) .fw-part .elementor-element.e-con.fw-part-root{display:contents}
.elementor-editor-active .rv{opacity:1!important;transform:none!important}
.elementor-editor-active #loader{display:none!important}
'''
open('native.css', 'w').write(compat + css)
js = [x.string or '' for x in s.find_all('script', recursive=False) if x.get('type') != 'application/ld+json']
shim = r'''(function(){
 // data-* attributes travel as classes (fwd-<name>--<value>) so the elements stay editable in Elementor
 document.querySelectorAll('[class*="fwd-"]').forEach(function(el){[].slice.call(el.classList).forEach(function(c){var m=/^fwd-([a-z0-9]+)--(.*)$/.exec(c);if(m){el.setAttribute('data-'+m[1],m[2]==='_'?'':m[2]);}})});
 // highlight the menu link for this page
 var p=location.pathname.replace(/\/+$/,'/')||'/';
 document.querySelectorAll('header a[href], #mobile-menu a[href]').forEach(function(a){a.classList.remove('on');var h=a.getAttribute('href');if(h===p)a.classList.add('on')});
})();
'''
open('native.js', 'w').write(shim + '\n'.join(js))
links = [str(l) for l in s.find_all('link', recursive=False)]
json.dump({'links': links}, open('native_links.json', 'w'))
# shared header (header + mobile menu + loader + cursor + grain) and footer
hdr = ''.join(str(x) for x in [s.find('div', id='loader'), s.find('div', id='cur'), s.find('svg', class_='grain'), s.find('header'), s.find('nav', id='mobile-menu')] if x)
hdr = re.sub(r' class="(m )?on"', lambda m: ' class="m"' if m.group(1) else '', hdr)
open('header.html', 'w').write(hdr)
open('footer.html', 'w').write(str(s.find('footer')))
print(len(compat + css), len(shim) + sum(map(len, js)), len(hdr), len(str(s.find('footer'))), links)
