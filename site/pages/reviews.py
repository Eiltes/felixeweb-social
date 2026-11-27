"""Written client reviews, copied word for word from Felix's public Fiverr profile (27 Nov 2026).
Only 5-star reviews. Never edit the text. 'what' is a short label of the service, taken from the review itself."""
R = {
 'betterwaydan': ('United States', 'Peptide website', 'very efficient.....went above and beyond....probably the most knowledgeable at building peptide sites on Fiverr. Will be using him again in the future'),
 'strosinw-web': ('Canada', 'Peptide website', 'I had a great experience working with Felix on my peptide website. He demonstrated a deep understanding of the project, paid close attention to every detail, and made sure everything worked perfectly. The website was bug free, and he went above and beyond to ensure the final result met my expectations. I especially appreciated his professionalism, patience, and dedication to getting everything right. I truly love working with him and would happily recommend Felix to anyone looking for a skilled, reliable, and detail-oriented freelancer. I look forward to working with him again!'),
 'myrtfred-coa': ('United States', 'COA page setup', 'Another excellent experience working with Felix! He helped me set up the COA page and integrate the COA button on individual product pages. He understood exactly what I wanted, paid attention to every detail, and made sure everything worked smoothly. His technical knowledge, communication, and commitment to delivering quality work really stood out. He didn\'t just complete the task; he made sure everything was properly implemented and looked great. I\'m very happy with his work and highly recommend him to anyone looking for a reliable and professional developer. Definitely looking forward to working with him again!'),
 'drop211cpk': ('Australia', 'Website build', 'Felix genuinely exceeded every expectation. His attention to detail, patience and willingness to refine every tiny request until it was absolutely perfect was nothing short of incredible. He didn’t just build a website—he brought my vision to life. Communication was flawless, and nothing ever felt like too much trouble. If you’re looking for someone who truly cares about the end result and takes immense pride in their work, you’ve found the right person.'),
 'redboy_23': ('United States', 'Ongoing web projects', 'Already been working with Felix for last 3 months. Love his work ethic, fast respose and top quality service. He will be the one doing all my big projects moving forward!! From a Developer i consider him a great friend!!! Recomended!! AA++++++++++'),
 'jameshuffman84': ('United States', 'Custom website feature', 'A great job as always. He coded me a special action on my website, which was better than a plug-in. Fantastic work!'),
 'myrtfred-kids': ('United States', '3D kids animation', 'Felix did an incredible job creating our 3D Pixar-style kids video. He was creative, patient, and paid close attention to every detail. The characters looked amazing, the animation was smooth, and the story came to life beautifully. Communication was great throughout, and he was always open to feedback. I’m extremely happy with the final result and would highly recommend Felix for kids’ animation projects!'),
 'strosinw-bday': ('Canada', '3D birthday video', 'Felix did an amazing job creating a beautiful 3D Pixar-style birthday video for my child. He captured the fun, personality, and special moments perfectly. The animation was creative, colorful, and full of life, and the final video was even better than I expected. Felix was professional, responsive, and easy to work with throughout the project. I’m very happy with the result and would definitely recommend him!'),
 'kenmorz': ('United States', 'AI video', 'Really impressed with the final AI video! The quality was excellent, the visuals were engaging, and the seller did a great job bringing the concept to life. They were easy to communicate with, understood the requirements, and delivered a professional result. I’m very happy with the work and will definitely come back for more projects!'),
 'oliver_ja001': ('Germany', 'Animated story', 'I really loved the job he did for me. He was calm, professional, and very easy to work with throughout the project. His storytelling and creativity were outstanding, and he truly went above and beyond my expectations. The level of cooperation was excellent, and he made the whole process smooth and stress-free. I highly recommend working with him!'),
}
WEB = ['betterwaydan', 'drop211cpk', 'myrtfred-coa', 'strosinw-web', 'redboy_23', 'jameshuffman84']
VIDEO = ['myrtfred-kids', 'kenmorz', 'strosinw-bday', 'oliver_ja001']
HOME = ['betterwaydan', 'drop211cpk', 'myrtfred-kids', 'strosinw-web', 'kenmorz', 'jameshuffman84']
ALL = WEB + VIDEO

STAR = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 1.6l2.6 5.3 5.8.8-4.2 4.1 1 5.8L10 14.9l-5.2 2.7 1-5.8L1.6 7.7l5.8-.8z"/></svg>'

def wr_cards(keys):
    import html
    out = ''
    for n, k in enumerate(keys):
        country, what, text = R[k]
        user = k.split('-')[0]
        long = len(text) > 330
        out += (f'<figure class="wr rv d{n % 3}"><div class="wr-top"><span class="wr-stars" aria-label="5 out of 5 stars">{STAR*5}</span><span class="wr-what">{what}</span></div>'
                f'<blockquote class="{"wr-clip" if long else ""}">{html.escape(text, quote=False)}</blockquote>'
                + ('<button class="wr-more" type="button" onclick="var q=this.previousElementSibling;q.classList.toggle(\'open\');this.textContent=q.classList.contains(\'open\')?\'Show less\':\'Read full review\'">Read full review</button>' if long else '')
                + f'<figcaption><span class="wr-av">{user[0].upper()}</span><span><b>{user}</b><small>{country} · via Fiverr</small></span></figcaption></figure>')
    return out

def carousel(track, label):
    arrow = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>'
    return (f'<div class="car" data-car role="region" aria-label="{label}">{track}'
            f'<div class="car-nav"><button type="button" class="car-btn prev" aria-label="Previous">{arrow}</button>'
            f'<div class="car-dots"></div><button type="button" class="car-btn next" aria-label="Next">{arrow}</button></div></div>')

def wr_block(keys, fiverr, title='What clients <em>write</em>.', label='Written reviews', intro=True):
    head = (f'<div class="sec-head"><div><div class="label rv">{label}</div><h2 class="rv d1">{title}</h2></div>'
            f'<p class="rv d2">Word for word from Fiverr, unedited.</p></div>') if intro else ''
    badge = (f'<div class="wr-badge rv"><div class="wr-score"><b>4.9</b><span>{STAR*5}</span></div>'
             f'<p><b>65+ five-star reviews</b> on Fiverr</p>'
             f'<a class="btn btn-ghost mag" href="{fiverr}" target="_blank" rel="noopener">Read all reviews on Fiverr <span class="arr">→</span></a></div>')
    return head + carousel(f'<div class="wr-grid car-track">{wr_cards(keys)}</div>', 'Client reviews') + badge

CSS = '''
.wr-wrap{margin-top:clamp(50px,6vw,80px)}
.wr{margin:0;background:#141414;border:1px solid #26231e;border-radius:20px;padding:24px 24px 20px;display:flex;flex-direction:column;gap:14px;transition:border-color .3s,transform .3s}
.wr:hover{border-color:#5a4720;transform:translateY(-3px)}
.wr-top{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap}
.wr-stars svg,.wr-score svg{width:15px;height:15px;fill:#B08A2E;margin-right:2px}
.wr-what{font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#B08A2E;background:rgba(176,138,46,.1);border-radius:999px;padding:5px 10px}
.wr blockquote{margin:0;font-size:15.5px;line-height:1.65;color:#e6e0d4;position:relative}
.wr blockquote::before{content:"“";font:800 52px/0 Montserrat,sans-serif;color:#B08A2E;opacity:.35;position:absolute;left:-4px;top:14px;pointer-events:none}
.wr blockquote{padding-top:18px}
.wr-clip{display:-webkit-box;-webkit-line-clamp:7;-webkit-box-orient:vertical;overflow:hidden}
.wr-clip.open{display:block;-webkit-line-clamp:unset}
.wr-more{align-self:flex-start;background:none;border:0;padding:0;color:#B08A2E;font:600 13px Montserrat,sans-serif;cursor:pointer}
.wr-more:hover{color:#d9b45a}
.wr figcaption{display:flex;align-items:center;gap:12px;border-top:1px solid #221f1a;padding-top:14px}
.wr-av{width:38px;height:38px;border-radius:50%;background:#1f1b14;border:1px solid #5a4720;color:#d9b45a;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:15px;flex:none}
.wr figcaption b{display:block;color:#F3EEE4;font-size:14px}
.wr figcaption small{color:#8f887c;font-size:12.5px}
.wr-badge{margin-top:12px;display:flex;align-items:center;gap:22px;flex-wrap:wrap;border:1px solid #26231e;border-radius:20px;padding:18px 22px;background:linear-gradient(90deg,rgba(176,138,46,.08),transparent)}
.wr-score{display:flex;align-items:center;gap:10px}
.wr-score b{font-size:34px;font-weight:800;color:#F3EEE4;letter-spacing:-.02em}
.wr-badge p{margin:0;color:#cfc8bb;flex:1;min-width:180px}
.wr-badge p b{color:#F3EEE4}
@media (max-width:700px){.wr-badge{flex-direction:column;align-items:flex-start;gap:12px}.wr-badge .btn{width:100%;justify-content:center}}
/* carousel */
.car{position:relative}
.car-track{display:flex;gap:20px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;-ms-overflow-style:none;padding:4px 2px 6px;cursor:grab;overscroll-behavior-x:contain}
.car-track::-webkit-scrollbar{display:none}
.car-track.drag{cursor:grabbing;scroll-snap-type:none;user-select:none}
.car-track.drag *{pointer-events:none}
.car-track>*{flex:0 0 calc((100% - 40px)/3);scroll-snap-align:start;min-width:0}
.wr-grid.car-track>.wr{align-self:stretch}
.tm-grid.car-track{display:flex}
.tm-grid.car-track>.tm{flex-basis:calc((100% - 54px)/4)}
.car-nav{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-top:18px}
.car-btn{width:46px;height:46px;border-radius:50%;border:1px solid #3a3226;background:#141414;color:#F3EEE4;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:background .25s,border-color .25s,color .25s,opacity .25s;flex:none}
.car-btn svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.car-btn.prev svg{transform:rotate(180deg)}
.car-btn:hover{background:#B08A2E;border-color:#B08A2E;color:#0A0A0A}
.car-btn[disabled]{opacity:.3;cursor:default;background:#141414;border-color:#3a3226;color:#F3EEE4}
.car-dots{display:flex;gap:8px;flex-wrap:wrap;justify-content:center}
.car-dots button{width:8px;height:8px;border-radius:99px;border:0;padding:0;background:#3a3226;cursor:pointer;transition:width .3s,background .3s}
.car-dots button.on{width:26px;background:#B08A2E}
@media (max-width:1000px){.car-track>*{flex-basis:calc((100% - 20px)/2)}.tm-grid.car-track>.tm{flex-basis:calc((100% - 36px)/2.6)}}
@media (max-width:700px){.car-track{gap:14px;margin:0 -20px;padding:4px 20px 6px;scroll-padding:0 20px}.car-track>*{flex-basis:86%}.tm-grid.car-track>.tm{flex-basis:72%}.car-btn{width:42px;height:42px}}
}
'''
