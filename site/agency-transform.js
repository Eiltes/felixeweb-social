function T(h){
 const miss=[];
 const rep=(a,b)=>{ if(h.includes(a)) h=h.replace(a,b); else miss.push(a.slice(0,50)); };
 if(h.includes('id="team"')) return {h, miss:['already has team']};
 // nav
 rep('<a href="#apps">Apps</a>','<a href="#team">Team</a>');
 rep('<a class="m" href="#apps"><em>03</em>Apps</a>','<a class="m" href="#team"><em>03</em>Team</a>');
 // hero
 rep('WooCommerce web designer · WordPress &amp; app developer</div>','Web &amp; video studio · WooCommerce stores · 2D/3D AI video</div>');
 rep('Most store builds drag on for months. I design and launch WordPress &amp; WooCommerce stores in 7–10 days, built to sell from day one.','Most store builds drag on for months. FelixeWeb designs and launches WordPress &amp; WooCommerce stores in 7–10 days, and our video team makes 2D explainers, 3D animations and AI-edited videos that help them sell.');
 rep('<span class="chip">Mobile &amp; web apps</span></div>','<span class="chip">Mobile &amp; web apps</span><span class="chip">2D &amp; 3D AI video</span></div>');
 rep('<a class="btn btn-ghost mag" href="#work">See my work</a>','<a class="btn btn-ghost mag" href="#work">See our work</a>');
 // marquee
 rep('<span>Digital Products</span>','<span>2D Explainer Videos</span><span>3D Animation</span><span>AI Video Editing</span><span>Digital Products</span>');
 // summary
 rep('is the web design studio of <strong>Felix</strong>,','is a web and video studio founded by <strong>Felix</strong>,');
 rep('Felix has launched <strong>50+ websites</strong>','A small team of 2D and 3D AI video creators makes <strong>explainer videos, 3D animations and video edits</strong>. Felix has launched <strong>50+ websites</strong>');
 // services
 rep('Stores, sites &amp; <em>apps</em>.</h2>','Stores, sites, apps &amp; <em>video</em>.</h2>');
 rep('Websites, online stores and mobile apps, all mobile-first,','Websites, online stores, apps and videos, all mobile-first,');
 const svcStart=h.indexOf('<div class="svc-grid">');
 const n06=h.indexOf('<div class="num">06</div>',svcStart);
 if(svcStart<0||n06<0) miss.push('svc 06'); else {
  const end=h.indexOf('</section>',n06);
  const close=h.lastIndexOf('</div>',h.lastIndexOf('</div>',end)-1); // closes .svc-grid
  const cards=`
   <div class="svc svc-new rv"><span class="badge badge-new">NEW</span><div class="num">07</div><h3>2D explainer video</h3><ul><li>Script &amp; storyboard help</li><li>Clean 2D animation</li><li>Voiceover &amp; music</li><li>Delivered in about a week</li></ul><div class="price"><small>Starting from</small><b>$200</b></div></div>
   <div class="svc rv d1"><div class="num">08</div><h3>3D animation</h3><ul><li>3D product &amp; character animation</li><li>AI-assisted 3D scenes</li><li>Cuts for ads &amp; social</li><li>Delivered in about a week</li></ul><div class="price"><small>Starting from</small><b>$300</b></div></div>
   <div class="svc rv d2"><div class="num">09</div><h3>AI video editing</h3><ul><li>Ads, reels &amp; YouTube edits</li><li>Captions, music &amp; colour</li><li>Your footage, polished</li><li>Fast turnaround</li></ul><div class="price"><small>Starting from</small><b>$100</b></div></div>
  `;
  h=h.slice(0,close)+cards+h.slice(close);
 }
 // about
 rep('Hello, I’m Felix. I build stores that <em>sell</em>.','Hello, I’m Felix. I founded FelixeWeb to build stores that <em>sell</em>.');
 rep('You work directly with me, from the first call to launch day.','You work directly with me from the first call to launch day, and on video projects with our 2D and 3D AI video creators.');
 // faq
 rep('<div class="q"><button aria-expanded="false">WooCommerce or Shopify','<div class="q"><button aria-expanded="false">Do you make videos?<i></i></button><div class="a"><div><p>Yes. Our video team makes 2D explainer videos from $200, 3D animations from $300 and AI video editing from $100, usually delivered in about a week. Explainers work well for clinics, apps and stores that need to show how something works.</p></div></div></div>\n   <div class="q"><button aria-expanded="false">WooCommerce or Shopify');
 // team section before faq
 const team=`<section id="team" style="padding-top:0" aria-label="The FelixeWeb team">
 <div class="wrap">
  <div class="sec-head"><div><div class="label rv">The team</div><h2 class="rv d1">The people behind <em>FelixeWeb</em>.</h2></div><p class="rv d2">Felix leads every project. Our 2D and 3D AI video creators make the explainers, product animations and edits.</p></div>
  <div class="tm-grid" id="tmGrid"><div class="tm"><div class="tm-ph"><img src="/wp-content/uploads/2026/11/felix.webp" alt="Felix, founder of FelixeWeb" loading="lazy"></div><div class="tm-b"><h3>Felix</h3><span>Founder</span><p>Founder of FelixeWeb. Felix designs and launches WordPress and WooCommerce stores and leads every project, from the first call to launch day.</p></div></div></div>
 </div>
 <style>
 .tm-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px}
 .tm{background:var(--char);border:1px solid var(--line);border-radius:22px;overflow:hidden;display:flex;flex-direction:column;transition:transform .4s,border-color .4s}
 .tm:hover{transform:translateY(-4px);border-color:#7A5C1C}
 .tm-ph{aspect-ratio:4/4.4;background:#141210;display:flex;align-items:flex-end;justify-content:center;overflow:hidden}
 .tm-ph img{width:100%;height:100%;object-fit:cover;object-position:top center;filter:grayscale(.15)}
 .tm-ph .ini{width:96px;height:96px;margin:auto;border-radius:50%;border:2px solid #B08A2E;display:flex;align-items:center;justify-content:center;font-size:38px;font-weight:800;color:#B08A2E}
 .tm-b{padding:20px 22px 24px}
 .tm-b h3{font-size:20px;margin:0}
 .tm-b span{display:block;color:#B08A2E;font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;margin:6px 0 10px}
 .tm-b p{color:var(--soft);font-size:14px;line-height:1.6;margin:0}
 </style>
 <script>
 (function(){var g=document.getElementById('tmGrid');if(!g||!window.fetch)return;
 fetch('/wp-json/fwcrm/v1/team').then(function(r){return r.json()}).then(function(list){
  if(!Array.isArray(list)||!list.length)return;g.innerHTML='';
  list.forEach(function(m){var c=document.createElement('div');c.className='tm';
   var ph=document.createElement('div');ph.className='tm-ph';
   if(m.photo){var i=document.createElement('img');i.src=m.photo;i.alt=m.name+', '+m.title+' at FelixeWeb';i.loading='lazy';ph.appendChild(i);}else{var n=document.createElement('div');n.className='ini';n.textContent=(m.name||'?').charAt(0);ph.appendChild(n);}
   var b=document.createElement('div');b.className='tm-b';var h=document.createElement('h3');h.textContent=m.name;var s=document.createElement('span');s.textContent=m.title;b.appendChild(h);b.appendChild(s);
   if(m.bio){var p=document.createElement('p');p.textContent=m.bio;b.appendChild(p);}
   c.appendChild(ph);c.appendChild(b);g.appendChild(c);});
 }).catch(function(){});})();
 </script>
</section>

`;
 rep('<section id="faq"', team+'<section id="faq"');
 return {h, miss};
}
