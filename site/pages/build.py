#!/usr/bin/env python3
"""Builds the FelixeWeb multi-page site: one self-contained Elementor HTML widget per page."""
import re, os, json

BASE = open('base.html').read()
CSS = open('base.css').read()
from reviews import CSS as _WRCSS
CSS += _WRCSS
CAL = 'https://calendar.app.google/zokGimp6miS6uLni7'
FIVERR = 'https://www.fiverr.com/s/odWybEX'
IG = 'https://www.instagram.com/felixeweb/'

def sec(id_):
    i = BASE.index(f'<section id="{id_}"'); j = BASE.index('</section>', i) + 10
    return BASE[i:j]

WORK_SEC = sec('work')
CARDS = re.findall(r'(   <a class="card[^"]*"[\s\S]*?</a>)', WORK_SEC)
def card(url_part):
    for c in CARDS:
        if url_part in c: return c
    raise KeyError(url_part)
REVIEWS_VIDEO = sec('reviews')
from reviews import wr_block, HOME as WR_HOME, WEB as WR_WEB, VIDEO as WR_VIDEO, ALL as WR_ALL, CSS as WR_CSS
def reviews_sec(keys):
    i = REVIEWS_VIDEO.rindex('</div>\n</section>')
    return REVIEWS_VIDEO[:i] + '<div class="wr-wrap">' + wr_block(keys, FIVERR) + '</div>' + REVIEWS_VIDEO[i:]
REVIEWS = reviews_sec(WR_HOME)
def reviews_only(keys, title, label='Client reviews'):
    return f'<section id="reviews" aria-label="Client reviews"><div class="wrap">' + wr_block(keys, FIVERR, title, label) + '</div></section>'
CASE = sec('case-study')
PROCESS = sec('process')
SVC = sec('services')
SVC_CARDS = re.findall(r'(<div class="svc[^"]*"[^>]*>(?:<span class="badge[^"]*">[^<]*</span>)?<div class="num">\d\d</div>[\s\S]*?</div></div>)', SVC)
def svc(num):
    for c in SVC_CARDS:
        if f'<div class="num">{num}</div>' in c: return c
    raise KeyError(num)
FAQ_ALL = re.findall(r'(<div class="q[^"]*"><button[\s\S]*?</p></div></div></div>)', sec('faq'))
def faq_q(start):
    for q in FAQ_ALL:
        if start in q: return q.replace('class="q open"', 'class="q"').replace('aria-expanded="true"', 'aria-expanded="false"')
    raise KeyError(start)

EXTRA_CSS = r'''
/* ===== multi-page additions ===== */
.links{align-items:center}
.links a.on{color:var(--ivory)}.links a.on::after{width:100%}
.dd{position:relative;display:flex;align-items:center}
.dd>a{display:inline-flex;align-items:center;gap:6px}
.dd>a .car{width:7px;height:7px;border-right:1.5px solid currentColor;border-bottom:1.5px solid currentColor;transform:rotate(45deg) translateY(-2px);transition:transform .3s}
.dd:hover>a .car,.dd:focus-within>a .car{transform:rotate(225deg) translateY(-1px)}
.dd-menu{position:absolute;top:calc(100% + 18px);left:-24px;width:min(620px,80vw);display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:14px;background:rgba(14,14,14,.97);border:1px solid var(--line);border-radius:20px;box-shadow:0 40px 80px rgba(0,0,0,.6);opacity:0;visibility:hidden;transform:translateY(10px);transition:opacity .3s,transform .3s,visibility .3s;backdrop-filter:blur(14px)}
.dd::before{content:"";position:absolute;left:0;right:0;top:100%;height:20px}
.dd:hover .dd-menu,.dd:focus-within .dd-menu{opacity:1;visibility:visible;transform:none}
.links .dd-menu a{display:flex;gap:14px;align-items:flex-start;padding:14px;border-radius:14px;color:var(--ivory);transition:background .25s}
.links .dd-menu a::after{display:none}
.links .dd-menu a:hover{background:#1b1914}
.dd-menu .di{width:40px;height:40px;flex-shrink:0;border-radius:10px;border:1.5px solid var(--bronze);display:flex;align-items:center;justify-content:center;color:var(--gold)}
.dd-menu b{display:block;font-size:14px;font-weight:700}
.dd-menu small{display:block;font-size:12px;color:var(--muted);font-weight:400;margin-top:2px;line-height:1.4}
.dd-menu a.all{grid-column:1/-1;justify-content:space-between;align-items:center;border-top:1px solid var(--line);border-radius:0 0 12px 12px;margin-top:4px;padding:14px 16px;font-size:13px;font-weight:700;color:var(--gold)}
#mobile-menu{justify-content:flex-start;padding-top:110px;padding-bottom:40px;overflow-y:auto}
#mobile-menu a.m{font-size:clamp(30px,8vw,40px)}
#mobile-menu a.m.on{color:var(--gold)}
#mobile-menu .subs{display:grid;grid-template-columns:1fr 1fr;gap:4px 16px;padding:8px 0 14px 34px;border-bottom:1px solid var(--line)}
#mobile-menu .subs a{font-size:15px;font-weight:600;color:var(--soft);padding:6px 0}
#mobile-menu .subs a.on{color:var(--gold)}
/* page hero */
.phero{position:relative;overflow:hidden;padding:clamp(150px,16vw,210px) 0 clamp(70px,8vw,110px);border-bottom:1px solid var(--line)}
.phero .glow{width:1000px;height:1000px;right:-300px;top:-380px}
.phero .bigword{font-size:clamp(110px,19vw,300px);right:-1vw;bottom:-3vw;left:auto}
.phero-grid{position:relative;display:grid;grid-template-columns:1.15fr .85fr;gap:clamp(30px,5vw,70px);align-items:center}
.phero.solo .phero-grid{grid-template-columns:1fr}
.crumbs{font-size:12px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:var(--muted);display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.crumbs a:hover{color:var(--gold)}.crumbs i{font-style:normal;color:var(--bronze)}
.phero h1{font-weight:800;font-size:clamp(42px,6vw,92px);line-height:.96;letter-spacing:-.045em;margin:22px 0 26px;max-width:960px}
.phero p.lead{font-size:clamp(17px,1.45vw,20px);color:var(--soft);max-width:620px}
.phero .hero-cta{margin:34px 0 0}
.phero .chips{margin-top:26px}
/* overview tiles */
.wwd{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:18px}
.wwd a{position:relative;grid-column:span 2;display:flex;flex-direction:column;gap:14px;padding:32px 28px;border-radius:22px;background:var(--char);border:1px solid var(--line);overflow:hidden;min-height:300px;transition:transform .4s,border-color .4s}
.wwd a.big{grid-column:span 3}
.wwd a:hover{transform:translateY(-6px);border-color:var(--bronze)}
.wwd a::before{content:"";position:absolute;inset:auto -40% -60% -40%;height:70%;background:radial-gradient(circle,rgba(176,138,46,.22),transparent 65%);opacity:0;transition:opacity .5s}
.wwd a:hover::before{opacity:1}
.wwd .ic{width:54px;height:54px;border-radius:14px;border:1.5px solid var(--gold);display:flex;align-items:center;justify-content:center;color:var(--gold)}
.wwd h3{font-size:clamp(22px,2vw,28px);font-weight:700;letter-spacing:-.6px;line-height:1.1}
.wwd p{color:var(--soft);font-size:15px;max-width:440px}
.wwd .from{margin-top:auto;display:flex;justify-content:space-between;align-items:center;gap:16px;font-size:13px;color:var(--muted)}
.wwd .from b{color:var(--ivory);font-size:20px;font-weight:800;letter-spacing:-.5px}
.wwd .from span.go{width:46px;height:46px}
.wwd a:hover .go{background:var(--gold);border-color:var(--gold);color:var(--onyx);transform:rotate(-45deg)}
/* feature list */
.fgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0;border:1px solid var(--line);border-radius:24px;overflow:hidden}
.fgrid.two{grid-template-columns:repeat(2,minmax(0,1fr))}
.fi{padding:34px 30px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);background:linear-gradient(180deg,rgba(22,22,22,.55),transparent)}
.fgrid .fi:nth-child(3n){border-right:0}
.fgrid.two .fi:nth-child(3n){border-right:1px solid var(--line)}.fgrid.two .fi:nth-child(2n){border-right:0}
.fi .k{font-size:13px;font-weight:700;letter-spacing:3px;color:var(--gold)}
.fi h4{font-size:21px;font-weight:700;letter-spacing:-.4px;margin:12px 0 8px}
.fi p{font-size:15px;color:var(--muted)}
/* split */
.split{display:grid;grid-template-columns:1fr 1fr;gap:clamp(30px,6vw,90px);align-items:center}
.split h2{font-size:clamp(34px,4.4vw,62px);font-weight:800;line-height:1;letter-spacing:-.04em;margin:16px 0 22px}
.split p{color:var(--soft);font-size:17px;margin-bottom:16px}
.ticks{list-style:none;display:flex;flex-direction:column;gap:12px;margin:22px 0 30px}
.ticks li{display:flex;gap:12px;color:var(--soft);font-size:16px}
.ticks li::before{content:"";flex-shrink:0;width:20px;height:20px;margin-top:2px;border-radius:50%;background:var(--gold) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%230A0A0A' stroke-width='3.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='20 6 9 17 4 12'/%3E%3C/svg%3E") center/12px no-repeat}
/* visuals */
.vis{position:relative;border-radius:26px;border:1px solid var(--line);background:radial-gradient(ellipse at 50% 110%,rgba(176,138,46,.26),transparent 60%),var(--char);aspect-ratio:5/4;display:flex;align-items:center;justify-content:center;overflow:hidden}
.vis .browser{width:86%;margin:0;border-radius:12px;border-bottom:1px solid var(--line);box-shadow:0 40px 80px rgba(0,0,0,.6)}
.vis .shot{aspect-ratio:16/10}
.v-player{width:84%;aspect-ratio:16/9;border-radius:14px;background:#0d0d0d;border:1px solid var(--line);position:relative;overflow:hidden;box-shadow:0 40px 80px rgba(0,0,0,.6)}
.v-player .scene{position:absolute;inset:0 0 38px;background:linear-gradient(160deg,#1c1913,#0d0d0d)}
.v-player .sun{position:absolute;width:26%;aspect-ratio:1;border-radius:50%;background:var(--gold);left:14%;top:22%;animation:bob 6s ease-in-out infinite}
.v-player .hill{position:absolute;left:-10%;right:-10%;bottom:-30%;height:70%;border-radius:50%;background:#2a2318}
.v-player .hill.b{left:30%;bottom:-40%;background:#3a2f1c}
.v-player .char{position:absolute;right:20%;bottom:26%;width:12%;aspect-ratio:1/2;border-radius:40% 40% 10px 10px;background:var(--ivory);animation:bob 3.5s ease-in-out infinite}
.v-player .char::before{content:"";position:absolute;left:50%;top:-34%;width:80%;aspect-ratio:1;transform:translateX(-50%);border-radius:50%;background:var(--ivory)}
.v-player .ctrl{position:absolute;left:0;right:0;bottom:0;height:38px;display:flex;align-items:center;gap:12px;padding:0 14px;background:#111;border-top:1px solid var(--line)}
.v-player .ctrl i{width:0;height:0;border-style:solid;border-width:6px 0 6px 10px;border-color:transparent transparent transparent var(--gold)}
.v-player .bar2{flex:1;height:4px;border-radius:4px;background:#2a2a2a;position:relative;overflow:hidden}
.v-player .bar2 b{position:absolute;inset:0 auto 0 0;width:40%;background:var(--gold);animation:prog 8s linear infinite}
@keyframes prog{from{width:0}to{width:100%}}
.v-player .ctrl small{font-size:11px;color:var(--muted)}
.frames{position:absolute;left:8%;right:8%;bottom:7%;display:flex;gap:8px}
.frames span{flex:1;aspect-ratio:16/10;border-radius:8px;border:1px solid var(--line);background:#121212;box-shadow:0 10px 30px rgba(0,0,0,.5)}
.frames span:nth-child(2){border-color:var(--gold)}
.v-book{width:72%;aspect-ratio:3/2;display:grid;grid-template-columns:1fr 1fr;background:#F3EEE4;border-radius:8px;box-shadow:0 40px 80px rgba(0,0,0,.6);position:relative;transform:rotate(-2deg)}
.v-book::after{content:"";position:absolute;left:50%;top:0;bottom:0;width:2px;background:rgba(10,10,10,.14)}
.v-book .pg{padding:9% 10%;display:flex;flex-direction:column;gap:7px;color:#0A0A0A}
.v-book .ck{font-size:clamp(7px,.7vw,10px);font-weight:800;letter-spacing:2px;color:#7A5C1C}
.v-book .ct{font-family:Georgia,serif;font-size:clamp(14px,1.8vw,26px);font-weight:700;line-height:1.05;margin-bottom:6px}
.v-book .ln{height:2px;background:rgba(10,10,10,.16)}
.v-book .ln.s{width:70%}
.v-book .dc{font-family:Georgia,serif;font-size:clamp(22px,3vw,44px);line-height:.8;color:#7A5C1C;float:left;margin-right:6px}
.v-book .pn{margin-top:auto;text-align:center;font-size:10px;color:rgba(10,10,10,.45)}
.v-flow{width:86%;display:flex;flex-direction:column;gap:16px}
.node{display:flex;align-items:center;gap:14px;padding:16px 18px;border-radius:16px;background:#121212;border:1px solid var(--line);box-shadow:0 20px 40px rgba(0,0,0,.45);position:relative}
.node .ni{width:40px;height:40px;flex-shrink:0;border-radius:10px;border:1.5px solid var(--gold);display:flex;align-items:center;justify-content:center;color:var(--gold)}
.node b{display:block;font-size:15px}.node small{color:var(--muted);font-size:12px}
.node.on{border-color:var(--gold)}
.node:not(:last-child)::after{content:"";position:absolute;left:37px;top:100%;height:16px;width:2px;background:repeating-linear-gradient(var(--gold) 0 4px,transparent 4px 8px);background-size:2px 8px;animation:flow 1s linear infinite}
@keyframes flow{to{background-position:0 8px}}
.node:nth-child(2){margin-left:8%}.node:nth-child(3){margin-left:16%}.node:nth-child(4){margin-left:8%}
.v-phone{width:42%;aspect-ratio:9/19;border-radius:34px;border:8px solid #1d1d1d;background:#0d0d0d;box-shadow:0 40px 80px rgba(0,0,0,.6);padding:12% 8% 8%;display:flex;flex-direction:column;gap:8%;position:relative}
.v-phone::before{content:"";position:absolute;top:8px;left:50%;transform:translateX(-50%);width:34%;height:14px;border-radius:10px;background:#1d1d1d}
.v-phone .t{font-size:clamp(10px,1vw,15px);font-weight:800}
.v-phone .kp{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.v-phone .kp span{aspect-ratio:1;border-radius:12px;background:#171717;border:1px solid var(--line)}
.v-phone .kp span.g{background:var(--gold);border-color:var(--gold)}
.v-phone .row2{height:14%;border-radius:12px;background:#171717;border:1px solid var(--line)}
.v-phone .btn2{margin-top:auto;height:10%;border-radius:10px;background:var(--gold)}
.v-phone.b2{position:absolute;width:30%;right:8%;bottom:-10%;transform:rotate(8deg);opacity:.9}
.price-row{display:flex;gap:18px;flex-wrap:wrap;align-items:stretch}
.price-row .svc{flex:1 1 280px;min-height:0}
/* contact */
.contact-grid{display:grid;grid-template-columns:1.2fr .8fr;gap:clamp(24px,4vw,56px);align-items:start}
.form{background:var(--char);border:1px solid var(--line);border-radius:26px;padding:clamp(24px,3.4vw,44px);display:grid;grid-template-columns:1fr 1fr;gap:16px}
.form .full{grid-column:1/-1}
.form label{display:flex;flex-direction:column;gap:8px;font-size:13px;font-weight:600;color:var(--soft)}
.form input,.form select,.form textarea{font:inherit;font-size:15px;color:var(--ivory);background:#0f0f0f;border:1px solid var(--line);border-radius:12px;padding:14px 16px;outline:none;transition:border-color .3s;width:100%}
.form textarea{min-height:150px;resize:vertical}
.elementor-widget-html .form input,.elementor-widget-html .form select{height:52px!important;min-height:52px;line-height:1.3!important;padding:0 16px!important}
.elementor-widget-html .form select{padding-right:40px!important}
.form input:focus,.form select:focus,.form textarea:focus{border-color:var(--gold)}
.form select{appearance:none;background-image:linear-gradient(45deg,transparent 50%,var(--gold) 50%),linear-gradient(135deg,var(--gold) 50%,transparent 50%);background-position:calc(100% - 22px) 52%,calc(100% - 16px) 52%;background-size:6px 6px;background-repeat:no-repeat}
.form .hp{position:absolute;left:-9999px}
.form button.btn{border:0;cursor:pointer;justify-self:start;font-family:inherit}
.form .note{font-size:13px;color:var(--muted);align-self:center}
.form .msg{grid-column:1/-1;padding:14px 16px;border-radius:12px;font-size:15px;display:none}
.form .msg.ok{display:block;background:rgba(63,191,110,.1);border:1px solid rgba(63,191,110,.4);color:#9be3b6}
.form .msg.err{display:block;background:rgba(224,112,95,.1);border:1px solid rgba(224,112,95,.4);color:#f0b3a8}
.ways{display:flex;flex-direction:column;gap:14px}
.way{display:flex;gap:16px;align-items:center;padding:22px;border-radius:20px;background:var(--char);border:1px solid var(--line);transition:border-color .3s,transform .3s}
.way:hover{border-color:var(--bronze);transform:translateX(4px)}
.way .ni{width:48px;height:48px;flex-shrink:0;border-radius:12px;border:1.5px solid var(--gold);display:flex;align-items:center;justify-content:center;color:var(--gold)}
.way b{display:block;font-size:16px}.way small{color:var(--muted);font-size:13px}
.way.gold{background:var(--gold);border-color:var(--gold);color:var(--onyx)}.way.gold .ni{border-color:var(--onyx);color:var(--onyx)}.way.gold small{color:#3a2c0c}
/* values */
.vals{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}
.val{padding:30px 26px;border-radius:22px;background:var(--char);border:1px solid var(--line)}
.val .k{font-size:40px;font-weight:300;color:var(--gold);line-height:1}
.val h4{font-size:19px;font-weight:700;margin:14px 0 8px}.val p{color:var(--muted);font-size:14px}
.morelink{display:flex;justify-content:center;margin-top:40px}
/* ===== blog ===== */
.post-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}
.pcard2{display:flex;flex-direction:column;border-radius:22px;overflow:hidden;background:var(--char);border:1px solid var(--line);transition:transform .4s,border-color .4s;color:var(--ivory)}
.pcard2:hover{transform:translateY(-6px);border-color:var(--bronze)}
.pcard2 .pimg{aspect-ratio:16/9;background:radial-gradient(ellipse at 30% 120%,rgba(176,138,46,.45),transparent 60%),#121110;position:relative;overflow:hidden}
.pcard2 .pimg img{width:100%;height:100%;object-fit:cover;transition:transform .8s}
.pcard2:hover .pimg img{transform:scale(1.04)}
.pcard2 .pimg .pw{position:absolute;left:22px;bottom:16px;font-size:44px;font-weight:800;letter-spacing:-2px;color:transparent;-webkit-text-stroke:1px rgba(176,138,46,.55);line-height:1}
.pcard2 .pb{padding:22px 24px 26px;display:flex;flex-direction:column;gap:10px;flex:1}
.pcard2 .pc{font-size:11px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:var(--gold)}
.pcard2 h3{font-size:20px;font-weight:700;line-height:1.25;letter-spacing:-.4px}
.pcard2 p{font-size:14px;color:var(--muted)}
.pcard2 .pm{margin-top:auto;font-size:12px;color:var(--muted);display:flex;justify-content:space-between}
.post-grid .pcard2.lead{grid-column:span 3;display:grid;grid-template-columns:1.2fr 1fr}
.post-grid .pcard2.lead .pimg{aspect-ratio:auto;min-height:320px}
.post-grid .pcard2.lead h3{font-size:clamp(24px,2.6vw,36px)}
.pager{display:flex;gap:8px;justify-content:center;margin-top:46px}
.pager a,.pager span{min-width:44px;height:44px;padding:0 14px;border-radius:22px;border:1px solid var(--line);display:inline-flex;align-items:center;justify-content:center;font-size:14px;font-weight:600;color:var(--soft)}
.pager .cur{background:var(--gold);border-color:var(--gold);color:var(--onyx)}
.cats{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:34px}
.cats a{padding:8px 16px;border-radius:20px;border:1px solid var(--line);font-size:13px;font-weight:600;color:var(--soft)}
.cats a.on,.cats a:hover{border-color:var(--gold);color:var(--gold)}
.post-head{padding:clamp(150px,15vw,200px) 0 clamp(40px,5vw,60px);position:relative;overflow:hidden}
.post-head .glow{width:900px;height:900px;right:-300px;top:-400px}
.post-head .wrap{max-width:900px}
.post-head h1{font-weight:800;font-size:clamp(36px,5vw,68px);line-height:1.02;letter-spacing:-.04em;margin:20px 0 22px}
.post-head .meta{display:flex;gap:16px;flex-wrap:wrap;align-items:center;font-size:14px;color:var(--muted)}
.post-head .meta .by{display:flex;gap:10px;align-items:center;color:var(--soft)}
.post-head .meta img{width:36px;height:36px;border-radius:50%;object-fit:cover;object-position:top;border:1px solid var(--bronze)}
.post-feat{max-width:1100px;margin:0 auto clamp(30px,4vw,50px);padding:0 24px}
.post-feat img{width:100%;border-radius:24px;border:1px solid var(--line)}
.prose{max-width:760px;margin:0 auto;padding:0 24px clamp(60px,7vw,90px);font-size:18px;line-height:1.75;color:var(--soft)}
.prose>*+*{margin-top:1.15em}
.prose h2{font-size:clamp(26px,2.8vw,36px);line-height:1.15;letter-spacing:-.03em;color:var(--ivory);margin-top:1.9em;font-weight:800}
.prose h3{font-size:22px;line-height:1.25;color:var(--ivory);margin-top:1.6em;font-weight:700}
.prose strong{color:var(--ivory)}
.prose a{color:var(--gold);text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:1px}
.prose a:hover{color:#d4ad4f}
.prose ul,.prose ol{padding-left:1.3em}.prose li+li{margin-top:.45em}
.prose ul li::marker{color:var(--gold)}
.prose blockquote{border-left:3px solid var(--gold);padding:6px 0 6px 22px;color:var(--ivory);font-style:italic}
.prose img{border-radius:16px;border:1px solid var(--line)}
.prose table{width:100%;border-collapse:collapse;font-size:15px;display:block;overflow-x:auto}
.prose th,.prose td{border:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top}
.prose th{background:#151412;color:var(--ivory)}
.prose code{background:#1a1916;border:1px solid var(--line);border-radius:6px;padding:1px 6px;font-size:.88em}
.prose hr{border:0;border-top:1px solid var(--line);margin:2.4em 0}
.prose .box,.disclosure{background:var(--char);border:1px solid var(--line);border-radius:16px;padding:18px 20px;font-size:15px}
.disclosure{border-left:3px solid var(--gold);color:var(--muted);margin-bottom:1.6em!important}
.post-cta{max-width:760px;margin:0 auto 40px;padding:0 24px}
.post-cta .in{border-radius:24px;padding:32px;background:radial-gradient(ellipse at 80% 120%,rgba(176,138,46,.3),transparent 60%),var(--char);border:1px solid var(--line)}
.post-cta h3{font-size:clamp(24px,2.6vw,32px);font-weight:800;letter-spacing:-.03em;line-height:1.1}
.post-cta p{color:var(--soft);margin:10px 0 20px}
.post-cta .row{display:flex;gap:12px;flex-wrap:wrap}
.share{max-width:760px;margin:0 auto 60px;padding:0 24px;display:flex;gap:10px;flex-wrap:wrap;align-items:center;font-size:13px;color:var(--muted)}
.share a{padding:8px 14px;border:1px solid var(--line);border-radius:20px;color:var(--soft)}
.share a:hover{border-color:var(--gold);color:var(--gold)}
@media (max-width:1000px){.post-grid{grid-template-columns:1fr 1fr}.post-grid .pcard2.lead{grid-column:span 2;grid-template-columns:1fr}.post-grid .pcard2.lead .pimg{min-height:0;aspect-ratio:16/9}}
@media (max-width:640px){.post-grid{grid-template-columns:1fr}.post-grid .pcard2.lead{grid-column:auto}.prose{font-size:17px}}

@media (max-width:1100px){.wwd a,.wwd a.big{grid-column:span 3}.vals{grid-template-columns:repeat(2,minmax(0,1fr))}.fgrid{grid-template-columns:repeat(2,minmax(0,1fr))}.fgrid .fi:nth-child(3n){border-right:1px solid var(--line)}.fgrid .fi:nth-child(2n){border-right:0}}
@media (max-width:900px){.phero-grid,.split,.contact-grid{grid-template-columns:1fr}.vis{aspect-ratio:4/3}.split .vis{order:-1}}
@media (max-width:640px){.wwd{grid-template-columns:1fr}.wwd a,.wwd a.big{grid-column:auto;min-height:0}.fgrid,.fgrid.two{grid-template-columns:1fr}.fi{border-right:0!important}.vals{grid-template-columns:1fr}.form{grid-template-columns:1fr}.phero h1{font-size:clamp(40px,11.5vw,60px)}#mobile-menu .subs{grid-template-columns:1fr;padding-left:20px}.v-phone{width:52%}}
'''

ICONS = {
 'web': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M2 9h20M6 6.5h.01M9 6.5h.01"/></svg>',
 'app': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M11 18h2"/></svg>',
 'video': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="5" width="14" height="14" rx="2"/><path d="M16 10l6-3v10l-6-3"/></svg>',
 'book': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 5c3-1.5 7-1.5 10 1 3-2.5 7-2.5 10-1v14c-3-1.5-7-1.5-10 1-3-2.5-7-2.5-10-1z"/><path d="M12 6v14"/></svg>',
 'auto': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="5" cy="6" r="2.5"/><circle cx="19" cy="6" r="2.5"/><circle cx="12" cy="18" r="2.5"/><path d="M7.5 6h9M6.3 8.2l4.4 7.6M17.7 8.2l-4.4 7.6"/></svg>',
 'mail': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/></svg>',
 'cal': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>',
 'ig': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/></svg>',
 'star': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/></svg>',
 'cart': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>',
 'bolt': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2L3 14h9l-1 8 10-12h-9z"/></svg>',
 'crm': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.8-3.6 3.4-5.5 6.5-5.5s5.7 1.9 6.5 5.5M16 4.5a3.5 3.5 0 010 7"/></svg>',
 'bell': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8a6 6 0 00-12 0c0 7-3 9-3 9h18s-3-2-3-9M13.7 21a2 2 0 01-3.4 0"/></svg>',
}

SERVICES = [
 ('web-design', 'Websites &amp; stores', 'WordPress, WooCommerce and research peptide stores', 'web'),
 ('app-development', 'Apps &amp; digital products', 'Mobile apps, web apps and interactive invitations', 'app'),
 ('video', '2D &amp; 3D AI video', 'Explainers, 3D animation and video editing', 'video'),
 ('book-formatting', 'Book formatting', 'Kindle, ebook and paperback files ready for KDP', 'book'),
 ('ai-automation', 'AI automation', 'Workflows, AI assistants and WordPress integrations', 'auto'),
]

def header(active):
    dd = ''.join(f'<a href="/{s}/"{" class=\"on\"" if active==s else ""}><span class="di">{ICONS[i]}</span><span><b>{t}</b><small>{d}</small></span></a>' for s,t,d,i in SERVICES)
    dd += '<a class="all" href="/services/">All services &amp; prices <span>→</span></a>'
    svc_on = active in ('services',) + tuple(s for s,_,_,_ in SERVICES)
    def L(slug, label):
        return f'<a href="/{slug}/"{" class=\"on\"" if active==slug else ""}>{label}</a>'
    subs = ''.join(f'<a href="/{s}/"{" class=\"on\"" if active==s else ""}>{t}</a>' for s,t,d,i in SERVICES)
    return f'''<div id="loader" aria-hidden="true"><div class="coin"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><b class="cf">F<span>W</span></b><b class="cf cb">F<span>W</span></b></div></div>
<div id="cur" aria-hidden="true"></div>
<svg class="grain" aria-hidden="true" width="100%" height="100%"><filter id="gr"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/></filter><rect width="100%" height="100%" filter="url(#gr)"/></svg>

<header id="top">
 <div class="wrap nav">
  <a href="/" class="brand" aria-label="FelixeWeb home"><div class="fw">F<span>W</span></div><b>FELIXE<span>WEB</span></b></a>
  <nav class="links" aria-label="Main">
   <div class="dd"><a href="/services/"{' class="on"' if svc_on else ''}>Services <span class="car"></span></a><div class="dd-menu">{dd}</div></div>
   {L('work','Work')}{L('about','About')}{L('blog','Blog')}{L('contact','Contact')}
  </nav>
  <div class="nav-right">
   <span class="avail"><i class="dot"></i>TAKING NEW PROJECTS</span>
   <a class="btn btn-gold mag" href="{CAL}" target="_blank" rel="noopener">Book a free call <span class="arr">→</span></a>
   <button class="burger" aria-label="Open menu" aria-expanded="false" id="burger"><i></i></button>
  </div>
 </div>
</header>
<nav id="mobile-menu" aria-label="Mobile">
 <a class="m{' on' if active=='home' else ''}" href="/"><em>01</em>Home</a>
 <a class="m{' on' if active=='services' else ''}" href="/services/"><em>02</em>Services</a>
 <div class="subs">{subs}</div>
 <a class="m{' on' if active=='work' else ''}" href="/work/"><em>03</em>Work</a>
 <a class="m{' on' if active=='about' else ''}" href="/about/"><em>04</em>About &amp; team</a>
 <a class="m{' on' if active=='blog' else ''}" href="/blog/"><em>05</em>Blog</a>
 <a class="m{' on' if active=='contact' else ''}" href="/contact/"><em>06</em>Contact</a>
 <a class="btn btn-gold" style="margin-top:30px;align-self:flex-start" href="{CAL}" target="_blank" rel="noopener">Book a free 30-min call →</a>
</nav>
'''

FOOTER = f'''<footer>
 <div class="wrap">
  <div class="foot">
   <div><a href="/" class="brand"><div class="fw">F<span>W</span></div><b>FELIXE<span>WEB</span></b></a><p>A web and video studio founded by Felix. Stores that sell, live in 7–10 days, plus apps, 2D &amp; 3D AI video, book formatting and AI automation.</p></div>
   <div class="fcols">
    <div><h5>SERVICES</h5><ul>{''.join(f'<li><a href="/{s}/">{t}</a></li>' for s,t,d,i in SERVICES)}<li><a href="/services/">All prices</a></li></ul></div>
    <div><h5>STUDIO</h5><ul><li><a href="/work/">Work</a></li><li><a href="/about/">About &amp; team</a></li><li><a href="/blog/">Blog</a></li><li><a href="/contact/">Contact</a></li><li><a href="/contact/#faq">FAQ</a></li></ul></div>
    <div><h5>FOLLOW</h5><ul><li><a href="{IG}" target="_blank" rel="noopener">Instagram</a></li><li><a href="https://www.threads.com/@felixeweb" target="_blank" rel="noopener">Threads</a></li><li><a href="https://www.behance.net/felixeweb" target="_blank" rel="noopener">Behance</a></li><li><a href="{FIVERR}" target="_blank" rel="noopener">Fiverr (65+ reviews)</a></li></ul></div>
    <div><h5>CONTACT</h5><ul><li><a href="mailto:hello@felixeweb.com">hello@felixeweb.com</a></li><li><a href="{CAL}" target="_blank" rel="noopener">Book a free call</a></li><li><a href="/contact/">Start a project</a></li></ul></div>
   </div>
  </div>
  <div class="mega" aria-hidden="true">FELIXE<span>WEB</span></div>
  <div class="legal"><span>© 2026 FelixeWeb. All rights reserved.</span><a href="#top">Back to top ↑</a></div>
 </div>
</footer>
'''

JS = r'''<script>
(function(){
 var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
 function $(s){return document.querySelector(s)}function $$(s){return document.querySelectorAll(s)}
 function ready(){var l=$('#loader');if(l)l.classList.add('done');document.body.classList.add('ready')}
 window.addEventListener('load',function(){setTimeout(ready,reduce?0:450)});setTimeout(ready,2200);
 var hd=$('#top');function onScroll(){if(hd)hd.classList.toggle('scrolled',window.scrollY>30)}
 window.addEventListener('scroll',onScroll,{passive:true});onScroll();
 var bg=$('#burger');if(bg){bg.addEventListener('click',function(){var o=document.body.classList.toggle('menu-open');bg.setAttribute('aria-expanded',o)});
 $$('#mobile-menu a').forEach(function(a){a.addEventListener('click',function(){document.body.classList.remove('menu-open');bg.setAttribute('aria-expanded',false)})})}
 var tr=$('#track');if(tr)tr.innerHTML+=tr.innerHTML;
 var els=$$('.rv,#proc');
 if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -40px 0px'});els.forEach(function(el){io.observe(el)})}else els.forEach(function(el){el.classList.add('in')});
 $$('.filters button').forEach(function(b){b.addEventListener('click',function(){
  $$('.filters button').forEach(function(x){x.classList.remove('on')});b.classList.add('on');
  var f=b.dataset.f;$$('#grid .card').forEach(function(c){var show=f==='all'||c.dataset.c===f;c.classList.toggle('hide',!show);c.classList.toggle('wide',show&&c.hasAttribute('data-wide')&&(f==='all'||f==='digital'))});
 })});
 $$('.q button').forEach(function(b){b.addEventListener('click',function(){var q=b.parentElement,o=q.classList.toggle('open');b.setAttribute('aria-expanded',o)})});
 // video testimonials
 (function(){var fr=document.querySelectorAll('.vt-frame');fr.forEach(function(f){var v=f.querySelector('video');f.addEventListener('click',function(e){if(f.classList.contains('playing')&&e.target===v)return;fr.forEach(function(o){if(o!==f){var ov=o.querySelector('video');ov.pause();}});v.controls=true;v.muted=false;v.play();f.classList.add('playing')});v.addEventListener('pause',function(){if(v.ended||v.currentTime===0)f.classList.remove('playing')});v.addEventListener('ended',function(){f.classList.remove('playing');v.controls=false;v.load()})})})();
 // team
 var g=$('#tmGrid');if(g&&window.fetch){fetch('/wp-json/fwcrm/v1/team').then(function(r){return r.json()}).then(function(list){
  if(!Array.isArray(list)||!list.length)return;g.innerHTML='';
  list.forEach(function(m){var c=document.createElement('div');c.className='tm';var ph=document.createElement('div');ph.className='tm-ph';
   if(m.photo){var i=document.createElement('img');i.src=m.photo;i.alt=m.name+', '+m.title+' at FelixeWeb';i.loading='lazy';ph.appendChild(i)}else{var n=document.createElement('div');n.className='ini';n.textContent=(m.name||'?').charAt(0);ph.appendChild(n)}
   var b=document.createElement('div');b.className='tm-b';var h=document.createElement('h3');h.textContent=m.name;var s=document.createElement('span');s.textContent=m.title;b.appendChild(h);b.appendChild(s);
   if(m.bio){var p=document.createElement('p');p.textContent=m.bio;b.appendChild(p)}c.appendChild(ph);c.appendChild(b);g.appendChild(c)})}).catch(function(){})}

 // home team: founder large, team 2x2
 var sp=$('#tmSplit');if(sp&&window.fetch){fetch('/wp-json/fwcrm/v1/team').then(function(r){return r.json()}).then(function(list){
  if(!Array.isArray(list)||!list.length)return;var four=sp.querySelector('.tm-four'),lead=sp.querySelector('.tm-lead');
  var fi=0;list.forEach(function(m,i){if(/founder/i.test(m.title||''))fi=i});
  function fill(card,m){var ph=card.querySelector('.tm-ph');ph.innerHTML='';if(m.photo){var i=document.createElement('img');i.src=m.photo;i.alt=m.name+', '+m.title+' at FelixeWeb';i.loading='lazy';ph.appendChild(i)}else{var n=document.createElement('div');n.className='ini';n.textContent=(m.name||'?').charAt(0);ph.appendChild(n)}
   var b=card.querySelector('.tm-b');b.innerHTML='';var h=document.createElement('h3');h.textContent=m.name;var s=document.createElement('span');s.textContent=m.title;b.appendChild(h);b.appendChild(s);if(m.bio){var p=document.createElement('p');p.textContent=m.bio;b.appendChild(p)}}
  fill(lead,list[fi]);four.innerHTML='';list.forEach(function(m,i){if(i===fi)return;var c=document.createElement('div');c.className='tm';c.innerHTML='<div class="tm-ph"></div><div class="tm-b"></div>';fill(c,m);four.appendChild(c)});
  sp.classList.toggle('odd',(list.length-1)%2===1)}).catch(function(){})}
 // carousels (reviews, team)
 function carInit(c){var t=c.querySelector('.car-track'),pv=c.querySelector('.prev'),nx=c.querySelector('.next'),dots=c.querySelector('.car-dots'),auto=null,hold=false;
  function step(){var k=t.children[0];return k?k.getBoundingClientRect().width+parseFloat(getComputedStyle(t).columnGap||getComputedStyle(t).gap||20):t.clientWidth}
  function pages(){return Math.max(1,Math.round((t.scrollWidth-t.clientWidth)/step())+1)}
  function idx(){return Math.round(t.scrollLeft/step())}
  function draw(){var n=pages();if(dots.children.length!==n){dots.innerHTML='';for(var i=0;i<n;i++){var b=document.createElement('button');b.type='button';b.setAttribute('aria-label','Go to '+(i+1));(function(i){b.addEventListener('click',function(){go(i)})})(i);dots.appendChild(b)}}
   var i=idx();[].forEach.call(dots.children,function(b,j){b.classList.toggle('on',j===i)});pv.disabled=t.scrollLeft<4;nx.disabled=t.scrollLeft>=t.scrollWidth-t.clientWidth-4;c.classList.toggle('car-off',n<2)}
  function go(i){t.scrollTo({left:i*step(),behavior:'smooth'})}
  pv.addEventListener('click',function(){go(Math.max(0,idx()-1));pause()});nx.addEventListener('click',function(){go(idx()+1);pause()});
  var st;t.addEventListener('scroll',function(){clearTimeout(st);st=setTimeout(draw,60)},{passive:true});
  // drag with mouse
  var down=false,sx=0,sl=0,moved=false;t.addEventListener('pointerdown',function(e){if(e.pointerType!=='mouse')return;down=true;moved=false;sx=e.clientX;sl=t.scrollLeft});
  window.addEventListener('pointermove',function(e){if(!down)return;var dx=e.clientX-sx;if(Math.abs(dx)>5){moved=true;t.classList.add('drag')}if(moved)t.scrollLeft=sl-dx});
  window.addEventListener('pointerup',function(){if(!down)return;down=false;if(moved){t.classList.remove('drag');go(idx());pause()}});
  t.addEventListener('click',function(e){if(moved){e.preventDefault();e.stopPropagation();moved=false}},true);
  // gentle autoplay, stops when people interact
  function pause(){hold=true;clearInterval(auto)}
  if(!reduce){auto=setInterval(function(){if(hold||document.hidden)return;var r=c.getBoundingClientRect();if(r.bottom<0||r.top>innerHeight)return;if(t.scrollLeft>=t.scrollWidth-t.clientWidth-4)go(0);else go(idx()+1)},6000)}
  c.addEventListener('mouseenter',function(){hold=true});c.addEventListener('mouseleave',function(){if(auto)hold=false});t.addEventListener('touchstart',pause,{passive:true});c.addEventListener('focusin',pause);
  window.addEventListener('resize',draw);if(window.MutationObserver)new MutationObserver(function(){setTimeout(draw,50)}).observe(t,{childList:true});draw();setTimeout(draw,800)}
 $$('[data-car]').forEach(carInit);
 // enquiry form
 var fm=$('#enq');if(fm){var t0=Date.now();var pre=(location.search.match(/[?&]service=([a-z0-9]+)/)||[])[1];if(pre&&fm.service)fm.service.value=pre;
  fm.addEventListener('submit',function(e){e.preventDefault();var m=fm.querySelector('.msg'),btn=fm.querySelector('button');m.className='msg';btn.disabled=true;btn.style.opacity=.6;
   var d={t:t0};['name','email','company','website','service','budget','message','company_url'].forEach(function(k){if(fm[k])d[k]=fm[k].value});
   fetch('/wp-json/fwcrm/v1/enquiry',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)}).then(function(r){return r.json()}).then(function(j){
    if(j&&j.ok){m.className='msg ok';m.textContent='Thank you. Your message is in. Felix will reply within one working day.';fm.reset()}else{m.className='msg err';m.textContent=(j&&j.msg)||'Something went wrong. Please email hello@felixeweb.com.'}
   }).catch(function(){m.className='msg err';m.textContent='Something went wrong. Please email hello@felixeweb.com.'}).finally(function(){btn.disabled=false;btn.style.opacity=1})})}
 if(reduce)return;
 var cur=$('#cur'),mx=0,my=0,cx=0,cy=0;
 if(cur){window.addEventListener('mousemove',function(e){mx=e.clientX;my=e.clientY});
 (function loop(){cx+=(mx-cx)*.2;cy+=(my-cy)*.2;cur.style.transform='translate('+cx+'px,'+cy+'px) translate(-50%,-50%)';requestAnimationFrame(loop)})();
 $$('a,button').forEach(function(el){el.addEventListener('mouseenter',function(){cur.classList.add(el.classList.contains('card')?'view':'big')});el.addEventListener('mouseleave',function(){cur.classList.remove('big','view')})})}
 $$('.mag').forEach(function(b){b.addEventListener('mousemove',function(e){var r=b.getBoundingClientRect();b.style.transform='translate('+((e.clientX-r.left-r.width/2)*.25)+'px,'+((e.clientY-r.top-r.height/2)*.35)+'px)'});b.addEventListener('mouseleave',function(){b.style.transform=''})});
 var gl=$('#heroGlow'),hs=$('.hero');if(gl&&hs)hs.addEventListener('mousemove',function(e){var x=(e.clientX/window.innerWidth-.5)*80,y=(e.clientY/window.innerHeight-.5)*80;gl.style.transform='translate('+x+'px,calc(-50% + '+y+'px))'});
 $$('.card').forEach(function(c){c.addEventListener('mousemove',function(e){var r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.transform='perspective(1200px) rotateY('+(x*4)+'deg) rotateX('+(-y*4)+'deg)'});c.addEventListener('mouseleave',function(){c.style.transform=''})});
 var bws=$$('.hero .bigword,.phero .bigword');window.addEventListener('scroll',function(){var y=window.scrollY;bws.forEach(function(b){b.style.transform='translateX('+(-y*.25)+'px)'})},{passive:true});
})();
</script>'''

HEAD = '''<!-- FelixeWeb · {name} page · paste into ONE Elementor "HTML" widget (page template: Elementor Canvas). Built by build.py -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,300;1,400&display=swap" rel="stylesheet">
<style>
'''

def page(name, active, body, schema=None):
    out = HEAD.format(name=name) + CSS + EXTRA_CSS + '</style>\n' + header(active) + '\n<main id="home">\n' + body + '\n</main>\n\n' + FOOTER + '\n' + JS
    if schema: out += '\n<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False) + '</script>'
    return out

def phero(crumb, h1, lead, word, visual='', chips=None, ctas=None):
    ctas = ctas or f'<a class="btn btn-gold mag" href="{CAL}" target="_blank" rel="noopener">Book a free 30-min call <span class="arr">→</span></a><a class="btn btn-ghost mag" href="/contact/">Start a project</a>'
    ch = '<div class="chips rv d4">' + ''.join(f'<span class="chip">{c}</span>' for c in chips) + '</div>' if chips else ''
    cr = '<div class="crumbs rv"><a href="/">Home</a>' + ''.join(f'<i>/</i>{c}' for c in crumb) + '</div>'
    vis = f'<div class="rv d2">{visual}</div>' if visual else ''
    return f'''<section class="phero{'' if visual else ' solo'}">
 <div class="glow"></div>
 <div class="bigword" aria-hidden="true">{word}</div>
 <div class="wrap phero-grid">
  <div>{cr}<h1 class="rv d1">{h1}</h1><p class="lead rv d2">{lead}</p><div class="hero-cta rv d3">{ctas}</div>{ch}</div>
  {vis}
 </div>
</section>
'''

def cta(h, p, word='LAUNCH', label='Ready when you are'):
    return f'''<section id="contact-cta">
 <div class="cta rv">
  <div class="glow"></div>
  <div class="bigword" aria-hidden="true">{word}</div>
  <div class="label" style="position:relative">{label}</div>
  <h2>{h}</h2>
  <p>{p}</p>
  <div class="row">
   <a class="btn btn-gold mag" href="{CAL}" target="_blank" rel="noopener">Book a free call <span class="arr">→</span></a>
   <a class="btn btn-ghost mag" href="/contact/">Send a message</a>
   <a class="btn btn-ghost mag" href="{FIVERR}" target="_blank" rel="noopener">Hire us on Fiverr</a>
  </div>
  <div class="contact-line">Or email <a href="mailto:hello@felixeweb.com">hello@felixeweb.com</a></div>
 </div>
</section>'''

def head(label, h2, p='', id_=''):
    return f'<div class="sec-head"><div><div class="label rv">{label}</div><h2 class="rv d1">{h2}</h2></div>{f"<p class=\"rv d2\">{p}</p>" if p else ""}</div>'

def faqs(items, title='Questions, <em>answered</em>.'):
    qs = ''
    for i,(q,a) in enumerate(items):
        qs += f'<div class="q{" open" if i==0 else ""}"><button aria-expanded="{"true" if i==0 else "false"}">{q}<i></i></button><div class="a"><div><p>{a}</p></div></div></div>\n'
    return f'<section id="faq" style="padding-top:0"><div class="wrap">{head("FAQ", title)}<div class="faq rv d2">{qs}</div></div></section>'

def fgrid(items, two=False):
    return f'<div class="fgrid{" two" if two else ""} rv">' + ''.join(f'<div class="fi"><div class="k">{k}</div><h4>{t}</h4><p>{p}</p></div>' for k,t,p in items) + '</div>'

def steps(items, id_='proc'):
    st = ''.join(f'<div class="step"><span class="pt"></span><div class="d">{d}</div><h4>{t}</h4><p>{p}</p></div>' for d,t,p in items)
    return f'<div class="process" id="{id_}"><div class="pline"><b></b></div>{st}</div>'

def team_split():
    lead = ('<div class="tm tm-lead"><div class="tm-ph"><img src="/wp-content/uploads/2026/11/felix.webp" alt="Felix, founder of FelixeWeb" loading="lazy"></div>'
            '<div class="tm-b"><h3>Felix</h3><span>Founder</span><p>Founder of FelixeWeb. Felix designs and launches WordPress and WooCommerce stores and leads every project, from the first call to launch day.</p></div></div>')
    return f'<div class="tm-split rv" id="tmSplit">{lead}<div class="tm-four"></div></div>'

def team_grid(car=False):
    g = team_grid_html()
    if not car: return g
    from reviews import carousel
    return carousel(g.replace('class="tm-grid"', 'class="tm-grid car-track"', 1), 'The team')

def team_grid_html():
    return '<div class="tm-grid" id="tmGrid"><div class="tm"><div class="tm-ph"><img src="/wp-content/uploads/2026/11/felix.webp" alt="Felix, founder of FelixeWeb" loading="lazy"></div><div class="tm-b"><h3>Felix</h3><span>Founder</span><p>Founder of FelixeWeb. Felix designs and launches WordPress and WooCommerce stores and leads every project, from the first call to launch day.</p></div></div></div>'

def wwd():
    items = [
     ('web-design','web','Websites &amp; stores','WordPress websites, WooCommerce stores and research peptide stores, live in 7–10 days.','From','$150','big'),
     ('video','video','2D &amp; 3D AI video','Explainer videos, 3D product and character animation, and AI video editing.','From','$100','big'),
     ('app-development','app','Apps &amp; digital products','iOS, Android and web apps, plus interactive event invitations.','Quoted','Custom',''),
     ('book-formatting','book','Book formatting','Kindle, ebook and paperback interiors, formatted and ready for KDP.','Quoted','Custom',''),
     ('ai-automation','auto','AI automation','Forms, leads, emails and tools connected so routine work runs itself.','Quoted','Custom',''),
    ]
    out = '<div class="wwd">'
    for i,(slug,ic,t,p,lab,price,cls) in enumerate(items):
        out += f'<a class="rv d{i%3}{" "+cls if cls else ""}" href="/{slug}/"><span class="ic">{ICONS[ic]}</span><h3>{t}</h3><p>{p}</p><div class="from"><span>{lab}<br><b>{price}</b></span><span class="go" aria-hidden="true">↗</span></div></a>'
    return out + '</div>'

ORG = {"@context":"https://schema.org","@type":"ProfessionalService","name":"FelixeWeb","url":"https://felixeweb.com/","email":"hello@felixeweb.com","founder":{"@type":"Person","name":"Felix"},"description":"A web and video studio: WordPress and WooCommerce stores in 7–10 days, apps, 2D and 3D AI video, book formatting and AI automation.","sameAs":["https://www.instagram.com/felixeweb/","https://www.behance.net/felixeweb","https://www.threads.com/@felixeweb"],"areaServed":"Worldwide"}

def faq_schema(items):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":re.sub('<[^>]+>','',q).replace('&amp;','&'),"acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',a).replace('&amp;','&')}} for q,a in items]}

pages = {}

# ---------------- HOME ----------------
hero_i = BASE.index('<section class="hero">'); hero_j = BASE.index('</section>', hero_i) + 10
hero = BASE[hero_i:hero_j].replace('href="#work">See our work', 'href="/work/">See our work').replace('href="#work" aria-label="Scroll to work"', 'href="#what" aria-label="Scroll to services"')
mq_i = BASE.index('<div class="marquee"'); mq_j = BASE.index('</div></div>', mq_i) + 12
marquee = BASE[mq_i:mq_j]
st_i = BASE.index('<section style="padding-bottom:0;padding-top:clamp(50px,6vw,80px)">'); st_j = BASE.index('</section>', st_i) + 10
stats = BASE[st_i:st_j]
summary = sec('summary')
home_work = f'''<section id="work">
 <div class="wrap">
  {head('Selected work · 2025–2026', 'Stores &amp; sites we’ve <em>launched</em>.', 'A few recent builds. See the full portfolio, with filters and a case study, on the Work page.')}
  <div class="work-grid" id="grid">
{card('medwellplus.com')}
{card('renovasynergy.com')}
{card('zentraxwellness.com')}
{card('velvetlenz.com')}
{card('invite.sixandbloomco.com')}
  </div>
  <div class="morelink rv"><a class="btn btn-ghost mag" href="/work/">See all work <span class="arr">→</span></a></div>
 </div>
</section>'''
home_team = f'''<section id="team" style="padding-top:0">
 <div class="wrap">
  {head('The team', 'The people behind <em>FelixeWeb</em>.', 'Felix leads every project, with a small team of 2D and 3D AI video creators, a book formatter and a WordPress &amp; AI automation developer.')}
  {team_split()}
  <div class="morelink rv"><a class="btn btn-ghost mag" href="/about/">About the studio <span class="arr">→</span></a></div>
 </div>
</section>'''
home_proc = PROCESS
home_faq_items = [
 ('How long does it take to build my store?', 'Most stores go live in 7–10 days: free call on day 1, design on days 2–3, build on days 4–7, testing on days 8–9 and launch on day 10. Bigger catalogues or custom features can take a little longer, and we’ll tell you on the call.'),
 ('How much does a website cost?', 'WordPress websites start from $300, WooCommerce stores from $450, research peptide stores from $600, and landing pages or redesigns from $150. You get a fixed quote after the free call. See every price on the <a href="/services/" style="color:var(--gold)">Services page</a>.'),
 ('Do you make videos?', 'Yes. Our video team makes 2D explainer videos from $200, 3D animations from $300 and AI video editing from $100, usually delivered in about a week.'),
 ('Do you offer book formatting and AI automation?', 'Yes. Our book formatter prepares Kindle, ebook and paperback files ready for KDP, and our WordPress &amp; AI automation developer connects your forms, emails and tools. Both are quoted per project.'),
 ('Can I hire you on Fiverr?', f'Yes. Felix has 65+ client reviews on <a href="{FIVERR}" target="_blank" rel="noopener" style="color:var(--gold)">Fiverr</a>. You can order there, or book a free 30-minute call and work with us directly.'),
]
home_body = hero + '\n' + marquee + '\n' + stats + '\n' + summary + f'''
<section id="what">
 <div class="wrap">
  {head('What we do', 'One studio, <em>five</em> ways to grow.', 'Pick what you need. Every service has its own page with what’s included, prices and how it works.')}
  {wwd()}
 </div>
</section>
''' + home_work + '\n' + REVIEWS + '\n' + home_proc + '\n' + home_team + '\n' + faqs(home_faq_items).replace('</div></div></section>', '<div class="morelink" style="justify-content:flex-start"><a class="btn btn-ghost mag" href="/contact/#faq">More questions <span class="arr">→</span></a></div></div></div></section>', 1) + '\n' + cta('Let’s get your store <em>live</em>.', 'Book a free 30-minute call. We’ll look at your products, goals and timeline, and you’ll leave with a clear plan.')
pages['home'] = page('Home', 'home', home_body, [ORG, faq_schema(home_faq_items)])

# ---------------- SERVICES ----------------
def svc_group(label, title, p, nums, link):
    return f'''<section style="padding-top:0">
 <div class="wrap">
  {head(label, title, p)}
  <div class="svc-grid">{''.join(svc(n) for n in nums)}</div>
  <div class="morelink" style="justify-content:flex-start"><a class="btn btn-ghost mag" href="{link}">See details <span class="arr">→</span></a></div>
 </div>
</section>'''
services_body = phero(['Services'], 'Everything you need to <em>launch</em> and grow.', 'Websites, online stores, apps, video, book formatting and AI automation, all from one studio. Starting prices are below; your fixed quote comes after a free call.', 'SERVICES', chips=['Fixed quotes', 'Mobile-first', 'Fast delivery', 'Worldwide clients']) + f'''
<section style="padding-bottom:clamp(60px,8vw,100px)"><div class="wrap">{wwd()}</div></section>
''' + svc_group('Websites &amp; stores', 'Stores &amp; sites that <em>sell</em>.', 'WordPress and WooCommerce builds, live in 7–10 days.', ['01','02','03','04'], '/web-design/').replace('<div class="svc-grid">', '<div class="svc-grid" style="grid-template-columns:repeat(auto-fit,minmax(260px,1fr))">') \
 + svc_group('Apps &amp; digital products', 'Apps and <em>interactive</em> products.', 'Quoted per project after a free call.', ['05','06'], '/app-development/').replace('<div class="svc-grid">', '<div class="svc-grid" style="grid-template-columns:repeat(auto-fit,minmax(280px,1fr))">') \
 + svc_group('2D &amp; 3D AI video', 'Video that <em>explains</em> and sells.', 'Usually delivered in about a week.', ['07','08','09'], '/video/') \
 + svc_group('Books &amp; automation', 'Books formatted, work <em>automated</em>.', 'Both quoted per project after a free call.', ['10','11'], '/book-formatting/').replace('<div class="svc-grid">', '<div class="svc-grid" style="grid-template-columns:repeat(auto-fit,minmax(280px,1fr))">').replace('href="/book-formatting/">See details', 'href="/book-formatting/">Book formatting details <span class="arr">→</span></a><a class="btn btn-ghost mag" style="margin-left:12px" href="/ai-automation/">AI automation details') \
 + '\n' + cta('Not sure what you <em>need</em>?', 'Tell us about your business on a free 30-minute call and we’ll recommend the right mix, with a fixed quote.', 'START')
pages['services'] = page('Services', 'services', services_body, [ORG])

# ---------------- WEB DESIGN ----------------
web_vis = '<div class="vis"><div class="browser"><div class="bar"><i></i><i></i><i></i><u>yourstore.com</u></div><div class="shot"><img src="/wp-content/uploads/2026/11/renova.webp" alt="A research peptide WooCommerce store built by FelixeWeb" loading="lazy"></div></div><div class="float f1" style="left:4%;bottom:10%"><div class="ic">' + ICONS['cart'] + '</div><div><b>New order</b><small>Your store · just now</small></div></div></div>'
web_faq = [
 ('How long does it take to build my store?', 'Most stores go live in 7–10 days: free call on day 1, design on days 2–3, build on days 4–7, testing on days 8–9 and launch on day 10. Bigger catalogues or custom features can take a little longer.'),
 ('How much does a website cost?', 'WordPress websites start from $300, WooCommerce stores from $450, research peptide stores from $600, and landing pages or redesigns from $150. You get a fixed quote after the free call.'),
 ('Do you build research peptide websites?', 'Yes. They include a COA page for every batch, an age gate, “research use only” notices, clear product specs and a payment setup suited to the niche.'),
 ('WooCommerce or Shopify: which should I choose?', 'WooCommerce gives you full ownership of your site and data, no platform fee per sale, full design freedom, and it works for niches some platforms restrict. Shopify is quick to start but adds monthly plan and app costs.'),
 ('What do I need to prepare?', 'Product photos, product details (names, prices, variants, descriptions), an approved payment account, and your shipping and returns policy. Don’t have them all yet? We’ll plan around it on the call.'),
]
web_body = phero(['<a href="/services/">Services</a>', 'Websites &amp; stores'], 'Stores that sell, live in <em>7–10 days</em>.', 'Custom WordPress and WooCommerce builds, designed for your brand and tested on every screen before launch. No templates, no months of back-and-forth.', 'STORES', web_vis, ['WordPress', 'WooCommerce', 'Elementor', 'Research peptide stores']) + f'''
<section>
 <div class="wrap">
  {head('Packages', 'Pick your <em>starting</em> point.', 'Final price depends on pages and features. We agree it on the free call.')}
  <div class="svc-grid" style="grid-template-columns:repeat(auto-fit,minmax(260px,1fr))">{svc('01')}{svc('02')}{svc('03')}{svc('04')}</div>
 </div>
</section>
<section style="padding-top:0">
 <div class="wrap">
  {head('Every build includes', 'Built to <em>sell</em> from day one.')}
  {fgrid([('01','Custom design','A look made for your brand, not a recycled template.'),('02','Mobile-first','Designed for phones first, then tablets and desktops.'),('03','Fast loading','Image optimisation, caching and clean code for speed.'),('04','Payments &amp; shipping','Checkout, payment methods and shipping rules set up and tested.'),('05','Basic SEO','Titles, descriptions and structure that search engines understand.'),('06','Handover','A walkthrough so you can add products and edit pages yourself.')])}
 </div>
</section>
<section style="padding-top:0">
 <div class="wrap split">
  <div class="vis"><div class="browser"><div class="bar"><i></i><i></i><i></i><u>researchstore.com</u></div><div class="shot"><img src="/wp-content/uploads/2026/11/zentrax.webp" alt="Research peptide store with a public COA for every batch" loading="lazy"></div></div></div>
  <div>
   <div class="label rv">Specialty</div>
   <h2 class="rv d1">Research peptide stores, <em>done right</em>.</h2>
   <p class="rv d2">Felix has built stores for research peptide brands in the US and Europe. These stores need more than a nice design, and every one gets:</p>
   <ul class="ticks rv d3"><li>A COA page for every batch, easy to search</li><li>Age gate and “research use only” notices</li><li>Clear specs layout on every product</li><li>A payment setup that works for the niche, including manual-payment checkout</li></ul>
   <a class="btn btn-gold mag rv d4" href="{CAL}" target="_blank" rel="noopener">Talk about your store <span class="arr">→</span></a>
  </div>
 </div>
</section>
''' + CASE + PROCESS + f'''
<section style="padding-top:0">
 <div class="wrap">
  {head('Recent stores', 'See them <em>live</em>.')}
  <div class="work-grid" id="grid">{card('medwellresearchlabs.com')}{card('shopcitadellabs.com')}{card('elevatelabs.shop')}{card('dermyslabs.fr')}</div>
  <div class="morelink rv"><a class="btn btn-ghost mag" href="/work/">See all work <span class="arr">→</span></a></div>
 </div>
</section>
''' + reviews_only(WR_WEB, 'Store owners, in their <em>own</em> words.') + '\n' + faqs(web_faq) + '\n' + cta('Let’s get your store <em>live</em>.', 'Book a free 30-minute call. We’ll look at your products, goals and timeline, and you’ll leave with a clear plan.')
pages['web-design'] = page('Websites & stores', 'web-design', web_body, [ORG, faq_schema(web_faq)])

# ---------------- APPS ----------------
app_vis = '<div class="vis"><div class="v-phone"><div class="t">Your app</div><div class="row2"></div><div class="kp"><span class="g"></span><span></span><span></span><span></span></div><div class="row2"></div><div class="btn2"></div></div><div class="v-phone b2"><div class="row2"></div><div class="row2"></div><div class="btn2"></div></div></div>'
app_faq = [
 ('Do you build mobile and web apps?', 'Yes. We build mobile apps for iOS and Android and web apps, from calculators and booking tools to customer dashboards. Apps are quoted per project after a free call.'),
 ('I started an app with an AI app builder and got stuck. Can you help?', 'Yes. We can fix it, finish it and help you launch it on the App Store and Google Play.'),
 ('What are digital invitations?', 'Interactive event invitations guests open from a link: a tap-to-open envelope, event details, RSVP, map and optional music.'),
 ('How much does an app cost?', 'Every app is different, so apps are quoted per project. Book a free call and you’ll get a clear scope and a fixed quote.'),
]
app_body = phero(['<a href="/services/">Services</a>', 'Apps &amp; digital products'], 'Apps people <em>actually</em> use.', 'Mobile apps for iOS and Android, web apps and dashboards, and interactive digital products. We also fix and finish apps started with AI app builders.', 'APPS', app_vis, ['iOS &amp; Android', 'React Native', 'Expo', 'Web apps']) + f'''
<section>
 <div class="wrap">
  {head('What we build', 'From idea to <em>App Store</em>.')}
  <div class="svc-grid" style="grid-template-columns:repeat(auto-fit,minmax(300px,1fr))">{svc('05')}{svc('06')}</div>
 </div>
</section>
<section style="padding-top:0">
 <div class="wrap">
  {head('Good fits', 'Apps that solve <em>one</em> job well.')}
  {fgrid([('01','Calculators &amp; tools','Simple apps that do one useful job for your customers.'),('02','Booking &amp; ordering','Let customers book, order or reserve from their phone.'),('03','Dashboards','Web apps for your team or customers to see their data.'),('04','Fix &amp; finish','Apps started with AI builders, cleaned up and launched.'),('05','Store launch','App Store and Google Play listings and submission.'),('06','Digital invitations','Tap-to-open event invitations with RSVP and maps.')])}
 </div>
</section>
''' + f'''<section style="padding-top:0">
 <div class="wrap">
  {head('Digital products', 'See one <em>live</em>.')}
  <div class="work-grid" id="grid">{card('invite.sixandbloomco.com').replace('class="card rv"','class="card wide rv"')}</div>
 </div>
</section>
''' + faqs(app_faq) + '\n' + cta('Got an app <em>idea</em>?', 'Tell us what it should do on a free 30-minute call. You’ll leave with a clear scope and next steps.', 'BUILD')
pages['app-development'] = page('Apps & digital products', 'app-development', app_body, [ORG, faq_schema(app_faq)])

# ---------------- VIDEO ----------------
vid_vis = '<div class="vis"><div class="v-player"><div class="scene"><div class="sun"></div><div class="hill"></div><div class="hill b"></div><div class="char"></div></div><div class="ctrl"><i></i><div class="bar2"><b></b></div><small>0:45</small></div></div></div>'
vid_faq = [
 ('How much does a video cost?', '2D explainer videos start from $200, 3D animations from $300 and AI video editing from $100. Longer videos, extra revisions or extra versions cost more. You get a fixed quote before we start.'),
 ('How long does a video take?', 'Most videos are delivered in about a week once the script is approved. Editing jobs can be faster.'),
 ('Do you write the script?', 'We can. Send us what you want the video to say, and we’ll help shape it into a short script and storyboard for you to approve.'),
 ('Who are explainer videos good for?', 'Anyone who needs to show how something works: clinics explaining a treatment, apps showing a feature, stores showing a product, and service businesses explaining their process.'),
 ('Can I see examples?', 'Yes. Ask on the free call or by email and we’ll share samples close to what you need.'),
]
vid_body = phero(['<a href="/services/">Services</a>', '2D &amp; 3D AI video'], 'Video that explains, <em>then sells</em>.', '2D explainer videos, 3D product and character animation, and AI video editing from the FelixeWeb video team. Usually delivered in about a week.', 'VIDEO', vid_vis, ['2D explainers', '3D animation', 'AI video editing', 'About 1 week']) + f'''
<section>
 <div class="wrap">
  {head('Video services', 'Three ways to <em>show</em> it.', 'Starting prices. Your fixed quote comes after a short brief.')}
  <div class="svc-grid">{svc('07')}{svc('08')}{svc('09')}</div>
 </div>
</section>
<section style="padding-top:0">
 <div class="wrap split">
  <div class="vis"><div class="v-player" style="width:80%"><div class="scene"><div class="sun" style="left:60%"></div><div class="hill"></div><div class="char" style="right:auto;left:22%"></div></div><div class="ctrl"><i></i><div class="bar2"><b></b></div><small>1:00</small></div></div><div class="frames"><span></span><span></span><span></span><span></span></div></div>
  <div>
   <div class="label rv">Where it works</div>
   <h2 class="rv d1">One video, <em>everywhere</em> you sell.</h2>
   <p class="rv d2">A short video can explain in a minute what a page of text can’t. Use it on your:</p>
   <ul class="ticks rv d3"><li>Homepage and product or service pages</li><li>Instagram, TikTok, YouTube and ads</li><li>Booking pages and email campaigns</li><li>Waiting-room and in-store screens</li></ul>
  </div>
 </div>
</section>
<section style="padding-top:0">
 <div class="wrap">
  {head('How it works', 'From brief to video in about <em>a week</em>.')}
  {steps([('STEP 1','Brief','Tell us what the video is for, who it’s for and where it will be used.'),('STEP 2','Script','A short script for you to approve, or polish of yours.'),('STEP 3','Storyboard','Key frames and style, approved before animation starts.'),('STEP 4','Animation','Animation, voiceover and music come together.'),('STEP 5','Delivery','Final video in the sizes you need, after your revisions.')])}
 </div>
</section>
<section style="padding-top:0">
 <div class="wrap">
  {head('Good fits', 'Who we make videos <em>for</em>.')}
  {fgrid([('01','Clinics &amp; healthcare','Explain a treatment or service so patients understand and book.'),('02','Apps &amp; software','Show what your product does in under a minute.'),('03','Online stores','Product animations and ads for launches and social.'),('04','Service businesses','Walk customers through how you work.'),('05','Authors','Book trailers and promo videos.'),('06','Your own footage','Edits, captions, music and colour for reels and YouTube.')])}
 </div>
</section>
''' + reviews_only(WR_VIDEO, 'Clients on their <em>videos</em>.') + '\n' + faqs(vid_faq) + '\n' + cta('Let’s make your <em>video</em>.', 'Book a free 30-minute call or send a short brief. We’ll suggest the right style and give you a fixed quote.', 'ACTION')
pages['video'] = page('2D & 3D AI video', 'video', vid_body, [ORG, faq_schema(vid_faq)])

# ---------------- BOOK FORMATTING ----------------
book_vis = '<div class="vis"><div class="v-book"><div class="pg"><div class="ck">CHAPTER ONE</div><div class="ct">The Beginning</div><div><span class="dc">I</span><div class="ln"></div></div><div class="ln"></div><div class="ln"></div><div class="ln s"></div><div class="ln"></div><div class="ln"></div><div class="pn">1</div></div><div class="pg"><div class="ln"></div><div class="ln"></div><div class="ln s"></div><div class="ln"></div><div class="ln"></div><div class="ln"></div><div class="ln s"></div><div class="ln"></div><div class="pn">2</div></div></div></div>'
book_faq = [
 ('What formats do you deliver?', 'Kindle (KDP) ebook files, EPUB for other ebook stores, and a print-ready paperback interior PDF sized to your trim.'),
 ('Will my files pass KDP review?', 'Files are prepared to KDP’s formatting guidelines and checked in the previewer before delivery. If KDP flags a formatting issue, we fix it.'),
 ('What do I need to send?', 'Your final edited manuscript in Word or Google Docs, your trim size if you have one, and any images, front matter and back matter you want included.'),
 ('Do you edit or proofread?', 'Formatting is about layout, not editing. Send your final, edited text so the formatted book matches what you approved.'),
 ('How much does book formatting cost?', 'It depends on length, images and formats, so book formatting is quoted per book. Send your manuscript details for a fixed quote.'),
]
book_body = phero(['<a href="/services/">Services</a>', 'Book formatting'], 'Books formatted to <em>publish</em>.', 'Kindle, ebook and paperback interiors, laid out cleanly and prepared for Amazon KDP. Send your final manuscript; get files ready to upload.', 'BOOKS', book_vis, ['Kindle', 'Ebook', 'Paperback', 'KDP-ready']) + f'''
<section>
 <div class="wrap">
  {head('What you get', 'A book that reads <em>beautifully</em>.')}
  {fgrid([('01','Kindle &amp; ebook','Reflowable files with a clickable table of contents.'),('02','Paperback interior','A print-ready PDF sized to your trim, with proper margins.'),('03','Chapter styling','Chapter openings, headers, page numbers and scene breaks.'),('04','Front &amp; back matter','Title page, copyright, dedication, about the author and more.'),('05','Images &amp; tables','Placed and sized so they look right on every device.'),('06','KDP-ready','Prepared for Amazon KDP and checked before delivery.')])}
 </div>
</section>
<section style="padding-top:0">
 <div class="wrap split">
  <div>
   <div class="label rv">Pricing</div>
   <h2 class="rv d1">Quoted per <em>book</em>.</h2>
   <p class="rv d2">Every manuscript is different. Tell us the word count, number of images and the formats you need, and you’ll get a fixed quote before we start.</p>
   <ul class="ticks rv d3"><li>Fiction, non-fiction, workbooks and journals</li><li>Ebook, paperback or both</li><li>Revisions until the layout is right</li></ul>
   <a class="btn btn-gold mag rv d4" href="/contact/?service=book">Get a quote <span class="arr">→</span></a>
  </div>
  <div class="price-row rv d2">{svc('10')}</div>
 </div>
</section>
<section style="padding-top:0">
 <div class="wrap">
  {head('How it works', 'Manuscript in, <em>book</em> out.')}
  {steps([('STEP 1','Send your manuscript','Word or Google Docs, plus images and your trim size.'),('STEP 2','Fixed quote','A clear price and delivery date for your book.'),('STEP 3','Formatting','Layout, styling, front and back matter.'),('STEP 4','Review','You check the proofs and ask for changes.'),('STEP 5','Ready to publish','Final files, ready to upload to KDP.')])}
 </div>
</section>
''' + faqs(book_faq) + '\n' + cta('Ready to <em>publish</em>?', 'Send your manuscript details and we’ll reply with a fixed quote and delivery date.', 'PUBLISH', 'For authors')
pages['book-formatting'] = page('Book formatting', 'book-formatting', book_body, [ORG, faq_schema(book_faq)])

# ---------------- AI AUTOMATION ----------------
auto_vis = '<div class="vis"><div class="v-flow"><div class="node"><span class="ni">' + ICONS['mail'] + '</span><div><b>New enquiry</b><small>Website form or email</small></div></div><div class="node on"><span class="ni">' + ICONS['crm'] + '</span><div><b>Saved to your CRM</b><small>Tagged and scored</small></div></div><div class="node"><span class="ni">' + ICONS['bolt'] + '</span><div><b>Instant reply sent</b><small>Personal, on-brand</small></div></div><div class="node"><span class="ni">' + ICONS['bell'] + '</span><div><b>You get an alert</b><small>With a follow-up task</small></div></div></div></div>'
auto_faq = [
 ('What can you automate?', 'Repeated tasks that follow the same steps: capturing leads, replying to enquiries, sending follow-ups, creating tasks, updating spreadsheets or a CRM, and notifying you when something needs attention.'),
 ('Do I need to change the tools I use?', 'Usually not. We connect the tools you already have, such as your website, email, forms and spreadsheets, wherever they support it.'),
 ('Can you add an AI assistant to my website?', 'Yes. We can add an assistant that answers common questions from your own content and hands off to you when a person is needed.'),
 ('How much does automation cost?', 'It depends on the tools and steps involved, so automation is quoted per project after a free call.'),
]
auto_body = phero(['<a href="/services/">Services</a>', 'AI automation'], 'Let the routine work <em>run itself</em>.', 'We connect your website, forms, email and tools, and add AI where it helps, so leads get answered, tasks get created and nothing slips through.', 'AUTOMATE', auto_vis, ['Workflows', 'AI assistants', 'WordPress', 'CRM &amp; email']) + f'''
<section>
 <div class="wrap">
  {head('What we automate', 'Less copy-paste, <em>more</em> selling.')}
  {fgrid([('01','Lead capture','Website forms and emails saved straight into your CRM or sheet.'),('02','Instant replies','A friendly first reply goes out while you’re busy.'),('03','Follow-ups','Polite follow-ups sent on schedule, stopped when they reply.'),('04','Orders &amp; alerts','Order, stock and payment alerts to your phone or email.'),('05','AI assistants','Answer common questions from your own content, day and night.'),('06','WordPress integrations','Your WordPress or WooCommerce site connected to the tools you use.')])}
 </div>
</section>
<section style="padding-top:0">
 <div class="wrap split">
  <div>
   <div class="label rv">Pricing</div>
   <h2 class="rv d1">Quoted per <em>project</em>.</h2>
   <p class="rv d2">On a free call we map the jobs that eat your time, pick the ones worth automating first, and give you a fixed quote.</p>
   <ul class="ticks rv d3"><li>Built around the tools you already use</li><li>Tested end to end before handover</li><li>A short guide so you know what runs and when</li></ul>
   <a class="btn btn-gold mag rv d4" href="/contact/?service=automation">Get a quote <span class="arr">→</span></a>
  </div>
  <div class="price-row rv d2">{svc('11')}</div>
 </div>
</section>
<section style="padding-top:0">
 <div class="wrap">
  {head('How it works', 'From busywork to <em>workflow</em>.')}
  {steps([('STEP 1','Map','We list the tasks you repeat every week.'),('STEP 2','Plan','Pick what to automate first and agree a fixed quote.'),('STEP 3','Build','Connect the tools and set up the workflow.'),('STEP 4','Test','Run real examples end to end and fix the edges.'),('STEP 5','Handover','A short guide and support while it settles in.')])}
 </div>
</section>
''' + faqs(auto_faq) + '\n' + cta('What would you <em>automate</em> first?', 'Book a free 30-minute call. We’ll find the tasks worth automating and show you how.', 'FLOW')
pages['ai-automation'] = page('AI automation', 'ai-automation', auto_body, [ORG, faq_schema(auto_faq)])

# ---------------- WORK ----------------
work_full = WORK_SEC.replace('Stores, sites &amp; products I’ve <em>launched</em>.', 'Every <em>project</em>, live.').replace('<section id="work">', '<section id="work" style="padding-top:clamp(60px,7vw,100px)">')
work_body = phero(['Work'], 'Stores, sites &amp; products we’ve <em>launched</em>.', 'Real client projects, live on the web. Tap any card to visit the site, filter by type, or watch the case study and client reviews below.', 'WORK', ctas=f'<a class="btn btn-gold mag" href="{CAL}" target="_blank" rel="noopener">Book a free call <span class="arr">→</span></a><a class="btn btn-ghost mag" href="#reviews">Client reviews</a>') + work_full + reviews_sec(WR_ALL) + CASE + '\n' + cta('Want yours <em>next</em>?', 'Book a free 30-minute call and we’ll plan your build together.')
pages['work'] = page('Work', 'work', work_body, [ORG])

# ---------------- ABOUT ----------------
about_sec = sec('about').replace('<section id="about" style="padding-top:0">', '<section id="about">').replace('<div class="label rv">About FelixeWeb</div>', '<div class="label rv">The founder</div>')
about_body = phero(['About'], 'A small studio with <em>big</em> standards.', 'FelixeWeb started as Felix building WordPress and WooCommerce stores for brands that were tired of waiting months to launch. Today it’s a small team covering web, apps, video, books and automation.', 'STUDIO', ctas=f'<a class="btn btn-gold mag" href="{CAL}" target="_blank" rel="noopener">Book a free call <span class="arr">→</span></a><a class="btn btn-ghost mag" href="#team">Meet the team</a>') + about_sec + stats.replace('padding-bottom:0;padding-top:clamp(50px,6vw,80px)', 'padding:0') + f'''
<section id="team">
 <div class="wrap">
  {head('The team', 'The people behind <em>FelixeWeb</em>.', 'Felix leads every project, with a small team of 2D and 3D AI video creators, a book formatter and a WordPress &amp; AI automation developer.')}
  {team_grid()}
 </div>
</section>
<section style="padding-top:0">
 <div class="wrap">
  {head('How we work', 'What you can <em>count</em> on.')}
  <div class="vals">
   <div class="val rv"><div class="k">01</div><h4>Fast, with a plan</h4><p>Clear timelines agreed on the first call, and updates as we go.</p></div>
   <div class="val rv d1"><div class="k">02</div><h4>One point of contact</h4><p>Felix stays your contact from first call to delivery, whoever is on the work.</p></div>
   <div class="val rv d2"><div class="k">03</div><h4>Fixed quotes</h4><p>You know the price before we start. No surprise invoices.</p></div>
   <div class="val rv d3"><div class="k">04</div><h4>Built to hand over</h4><p>Walkthroughs and guides so you can run what we build.</p></div>
  </div>
 </div>
</section>
''' + REVIEWS.replace('Real clients talking about working with me, unedited.', 'Real clients talking about working with Felix, unedited.') + '\n' + cta('Let’s work <em>together</em>.', 'Book a free 30-minute call. Tell us what you’re building and we’ll show you how we’d do it.', 'HELLO')
pages['about'] = page('About & team', 'about', about_body, [ORG])

# ---------------- CONTACT ----------------
contact_faq = [(re.sub('<[^>]+>','',re.search(r'<button[^>]*>(.*?)<i>', q).group(1)), re.search(r'<p>(.*?)</p></div></div></div>', q, re.S).group(1)) for q in FAQ_ALL]
contact_body = phero(['Contact'], 'Let’s talk about your <em>project</em>.', 'Send a message and Felix will reply within one working day, or book a free 30-minute call straight away.', 'HELLO', ctas='') .replace('<div class="hero-cta rv d3"></div>', '') + f'''
<section style="padding-top:clamp(60px,7vw,100px)">
 <div class="wrap contact-grid">
  <form class="form rv" id="enq" novalidate>
   <label>Your name<input name="name" required autocomplete="name"></label>
   <label>Email<input type="email" name="email" required autocomplete="email"></label>
   <label>Business or brand<input name="company" autocomplete="organization"></label>
   <label>Website (if you have one)<input name="website" inputmode="url" placeholder="yourbrand.com"></label>
   <label>What do you need?<select name="service"><option value="web">Website or store</option><option value="app">App</option><option value="2d">2D explainer video</option><option value="3d">3D animation</option><option value="edit">AI video editing</option><option value="book">Book formatting</option><option value="automation">AI automation</option><option value="other">Something else</option></select></label>
   <label>Budget<select name="budget"><option value="">Not sure yet</option><option>Under $300</option><option>$300–$600</option><option>$600–$1,500</option><option>$1,500+</option></select></label>
   <label class="full">Tell us about your project<textarea name="message" required placeholder="What you’re building, what you need, and any deadline."></textarea></label>
   <input class="hp" name="company_url" tabindex="-1" autocomplete="off" aria-hidden="true">
   <div class="msg" role="status"></div>
   <button class="btn btn-gold" type="submit">Send message <span class="arr">→</span></button>
   <span class="note">We reply within one working day.</span>
  </form>
  <div class="ways">
   <a class="way gold rv" href="{CAL}" target="_blank" rel="noopener"><span class="ni">{ICONS['cal']}</span><span><b>Book a free 30-min call</b><small>Google Meet, Monday to Friday</small></span></a>
   <a class="way rv d1" href="mailto:hello@felixeweb.com"><span class="ni">{ICONS['mail']}</span><span><b>hello@felixeweb.com</b><small>Email us any time</small></span></a>
   <a class="way rv d2" href="{IG}" target="_blank" rel="noopener"><span class="ni">{ICONS['ig']}</span><span><b>@felixeweb</b><small>DM on Instagram</small></span></a>
   <a class="way rv d3" href="{FIVERR}" target="_blank" rel="noopener"><span class="ni">{ICONS['star']}</span><span><b>Hire us on Fiverr</b><small>65+ client reviews</small></span></a>
  </div>
 </div>
</section>
''' + faqs(contact_faq, 'Questions, <em>answered</em>.')
pages['contact'] = page('Contact', 'contact', contact_body, [ORG, faq_schema(contact_faq)])

os.makedirs('out', exist_ok=True)
for k, v in pages.items():
    open(f'out/{k}.html', 'w').write(v)
    print(k, len(v))

# ---------- chrome for the Hub blog templates ----------
PLUG = os.environ.get('FW_PLUGIN', '/home/claude/fwcrm/felixeweb-crm/assets/site')
os.makedirs(PLUG, exist_ok=True)
open(os.path.join(PLUG, 'site.css'), 'w').write(CSS + EXTRA_CSS)
open(os.path.join(PLUG, 'header.html'), 'w').write(header('blog'))
open(os.path.join(PLUG, 'footer.html'), 'w').write(FOOTER)
open(os.path.join(PLUG, 'site.js'), 'w').write(JS)
print('chrome written to', PLUG)
