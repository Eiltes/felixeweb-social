import json, sys, os
from playwright.sync_api import sync_playwright
src, out = sys.argv[1], sys.argv[2]
JS = """() => { const main=document.body; const stop=document.body; const res={};
 function key(el){const parts=[];while(el&&el!==stop){const sib=[...el.parentElement.children].filter(x=>x.tagName===el.tagName);parts.unshift(el.tagName.toLowerCase()+sib.indexOf(el));el=el.parentElement;}return parts.join('/');}
 for(const el of main.querySelectorAll('*')){const cs=getComputedStyle(el);res[key(el)]={display:cs.display,fd:cs.flexDirection,fw:cs.flexWrap};}
 return res;}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1440,'height':900})
    pg.set_content('<meta charset="utf-8">'+open(src).read(), wait_until='load'); pg.wait_for_timeout(500)
    json.dump(pg.evaluate(JS), open(out,'w')); b.close()
print('ok')
