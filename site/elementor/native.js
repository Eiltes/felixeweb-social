(function(){
 // data-* attributes travel as classes (fwd-<name>--<value>) so the elements stay editable in Elementor
 document.querySelectorAll('[class*="fwd-"]').forEach(function(el){[].slice.call(el.classList).forEach(function(c){var m=/^fwd-([a-z0-9]+)--(.*)$/.exec(c);if(m){el.setAttribute('data-'+m[1],m[2]==='_'?'':m[2]);}})});
 // highlight the menu link for this page
 var p=location.pathname.replace(/\/+$/,'/')||'/';
 document.querySelectorAll('header a[href], #mobile-menu a[href]').forEach(function(a){a.classList.remove('on');var h=a.getAttribute('href');if(h===p)a.classList.add('on')});
})();

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
