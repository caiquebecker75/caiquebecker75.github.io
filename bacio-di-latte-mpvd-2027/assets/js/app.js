/* Bacio di Latte · MPVD 2027 · 75LAB — navegação, animação e interação */
(function(){
  var slides=[].slice.call(document.querySelectorAll('.slide'));
  var n=slides.length, cur=-1, busy=false;
  var stage=document.getElementById('stage');
  var mobile=function(){return window.matchMedia('(max-width:900px)').matches};
  var reduce=window.matchMedia('(prefers-reduced-motion:reduce)').matches;

  /* palavras animadas: [data-words] vira spans */
  document.querySelectorAll('[data-words]').forEach(function(el){
    var words=el.innerHTML.trim().split(/\s+(?![^<]*>)/);
    el.classList.add('words');
    el.innerHTML=words.map(function(w,i){return '<span class="w"><span style="--i:'+i+'">'+w+'</span></span>'}).join(' ');
  });
  /* comprimento real dos traços SVG */
  document.querySelectorAll('svg .draw').forEach(function(p){try{p.style.setProperty('--len',Math.ceil(p.getTotalLength()+2))}catch(e){}});

  /* capítulos */
  var chapters=[];
  slides.forEach(function(s,i){var c=s.dataset.chapter;if(c&&(!chapters.length||chapters[chapters.length-1].name!==c))chapters.push({name:c,start:i});});
  var list=document.querySelector('#chaps ol');
  chapters.forEach(function(c){var li=document.createElement('li');var b=document.createElement('button');b.textContent=c.name;b.onclick=function(){closeChaps();go(c.start)};li.appendChild(b);list.appendChild(li);});
  function chapterOf(i){var r=chapters[0];chapters.forEach(function(c){if(c.start<=i)r=c});return r}

  function fit(){
    if(mobile()){stage.style.transform='';return}
    var k=Math.min(innerWidth/1920,innerHeight/1080);
    stage.style.transform='translate(-50%,-50%) scale('+k+')';
  }

  function countUp(root){
    root.querySelectorAll('[data-count]').forEach(function(el){
      var to=parseFloat(el.dataset.count), dec=(el.dataset.count.split('.')[1]||'').length;
      var pre=el.dataset.pre||'', suf=el.dataset.suf||'', t0=null, dur=reduce?1:1800, delay=parseInt(el.dataset.delay||'400',10);
      function fmt(v){return pre+v.toLocaleString('pt-BR',{minimumFractionDigits:dec,maximumFractionDigits:dec})+suf}
      el.textContent=fmt(0);
      setTimeout(function(){requestAnimationFrame(function step(t){if(!t0)t0=t;var p=Math.min(1,(t-t0)/dur);var e=1-Math.pow(1-p,4);el.textContent=fmt(to*e);if(p<1)requestAnimationFrame(step)})},reduce?0:delay);
    });
  }

  function go(i,force){
    if(mobile()){slides[Math.max(0,Math.min(n-1,i))].scrollIntoView({behavior:'smooth'});return}
    i=Math.max(0,Math.min(n-1,i));
    if(i===cur&&!force)return;
    var prev=cur, chPrev=prev>=0?chapterOf(prev).name:null, chNow=chapterOf(i).name;
    if(prev>=0){var o=slides[prev];o.classList.remove('on');o.classList.add('out');setTimeout(function(){o.classList.remove('out')},900);}
    var show=function(){
      cur=i;var s=slides[i];
      s.classList.add('on');countUp(s);
      document.body.dataset.theme=s.dataset.theme||'light';
      document.getElementById('pos').innerHTML='<b>'+String(i+1).padStart(2,'0')+'</b> / '+String(n).padStart(2,'0');
      document.getElementById('prog').style.width=((i+1)/n*100)+'%';
      document.getElementById('hdr-chap').textContent=chNow;
      document.querySelectorAll('#chaps button').forEach(function(b){b.classList.toggle('cur',b.textContent===chNow)});
      history.replaceState(null,'','#s'+(i+1));
    };
    if(prev>=0&&chPrev!==chNow&&!reduce){var c=document.getElementById('curtain');c.classList.remove('go');void c.offsetWidth;c.classList.add('go');setTimeout(show,480);}
    else show();
  }
  function next(){go(cur+1)} function prev(){go(cur-1)}

  /* teclado */
  addEventListener('keydown',function(e){
    if(lb.classList.contains('on')){if(e.key==='Escape')closeLb();else if(e.key==='ArrowRight')lbStep(1);else if(e.key==='ArrowLeft')lbStep(-1);return}
    if(chaps.classList.contains('on')){if(e.key==='Escape')closeChaps();return}
    var k=e.key;
    if(['ArrowRight','ArrowDown','PageDown',' ','Enter'].indexOf(k)>-1){e.preventDefault();next()}
    else if(['ArrowLeft','ArrowUp','PageUp','Backspace'].indexOf(k)>-1){e.preventDefault();prev()}
    else if(k==='Home')go(0);else if(k==='End')go(n-1);
    else if(k==='m'||k==='M')openChaps();
  });
  /* clique: metade direita avança, metade esquerda volta */
  document.addEventListener('click',function(e){
    if(mobile()||e.target.closest('a,button,[data-zoom],#lb,#chaps'))return;
    if(String(window.getSelection&&getSelection()))return;
    if(e.clientX>=innerWidth/2)next();else prev();
  });
  /* roda do mouse / trackpad */
  var wheelLock=0;
  addEventListener('wheel',function(e){
    if(mobile()||lb.classList.contains('on')||chaps.classList.contains('on'))return;
    var now=Date.now();if(now<wheelLock||Math.abs(e.deltaY)<25)return;
    wheelLock=now+900;if(e.deltaY>0)next();else prev();
  },{passive:true});
  /* toque */
  var x0=null,y0=null;
  addEventListener('touchstart',function(e){x0=e.touches[0].clientX;y0=e.touches[0].clientY},{passive:true});
  addEventListener('touchend',function(e){if(x0===null||mobile())return;var dx=e.changedTouches[0].clientX-x0,dy=e.changedTouches[0].clientY-y0;if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy))dx<0?next():prev();x0=null},{passive:true});
  document.getElementById('nb-next').onclick=next;
  document.getElementById('nb-prev').onclick=prev;

  /* menu de capítulos */
  var chaps=document.getElementById('chaps');
  function openChaps(){chaps.classList.add('on');var b=chaps.querySelector('button.cur')||chaps.querySelector('li button');b&&b.focus()}
  function closeChaps(){chaps.classList.remove('on')}
  document.getElementById('chap-btn').onclick=openChaps;
  chaps.querySelector('.x').onclick=closeChaps;
  chaps.addEventListener('click',function(e){if(e.target===chaps)closeChaps()});

  /* lightbox */
  var lb=document.getElementById('lb'),lbImg=lb.querySelector('img'),lbCap=lb.querySelector('figcaption'),gal=[],gi=0,lastFocus=null;
  function openLb(el){
    var scope=el.closest('.slide');gal=[].slice.call(scope.querySelectorAll('[data-zoom]'));gi=gal.indexOf(el);lastFocus=el;
    showLb();lb.classList.add('on');lb.querySelector('.lbx').focus();
  }
  function showLb(){var el=gal[gi],img=el.querySelector('img');lbImg.src=img.dataset.full||img.src;lbImg.alt=img.alt;lbCap.textContent=(el.dataset.zoom||img.alt)+(gal.length>1?'  ·  '+(gi+1)+' / '+gal.length:'');
    lb.querySelector('.lbp').style.display=lb.querySelector('.lbn').style.display=gal.length>1?'grid':'none'}
  function lbStep(d){gi=(gi+d+gal.length)%gal.length;showLb()}
  function closeLb(){lb.classList.remove('on');lastFocus&&lastFocus.focus()}
  document.querySelectorAll('[data-zoom]').forEach(function(el){
    el.setAttribute('tabindex','0');el.setAttribute('role','button');el.setAttribute('aria-label','Ampliar imagem: '+(el.dataset.zoom||''));
    el.addEventListener('click',function(e){e.stopPropagation();openLb(el)});
    el.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();e.stopPropagation();openLb(el)}});
  });
  lb.addEventListener('click',function(e){if(e.target===lb||e.target.tagName==='FIGURE')closeLb()});
  lb.querySelector('.lbx').onclick=closeLb;
  lb.querySelector('.lbp').onclick=function(e){e.stopPropagation();lbStep(-1)};
  lb.querySelector('.lbn').onclick=function(e){e.stopPropagation();lbStep(1)};

  /* cursor personalizado (só mouse) */
  if(window.matchMedia('(pointer:fine)').matches&&!reduce){
    var c1=document.getElementById('cur'),c2=document.getElementById('cur-r'),mx=-100,my=-100,rx=-100,ry=-100;
    document.body.classList.add('has-cur');
    addEventListener('mousemove',function(e){mx=e.clientX;my=e.clientY;c1.style.transform='translate('+(mx-4)+'px,'+(my-4)+'px)';
      var t=e.target;document.body.classList.toggle('c-zoom',!!t.closest('[data-zoom]'));document.body.classList.toggle('c-link',!t.closest('[data-zoom]')&&!!t.closest('a,button'));});
    (function loop(){rx+=(mx-rx)*.18;ry+=(my-ry)*.18;var w=c2.offsetWidth;c2.style.transform='translate('+(rx-w/2)+'px,'+(ry-w/2)+'px)';requestAnimationFrame(loop)})();
    c1.style.left=c2.style.left='0';c1.style.top=c2.style.top='0';
  }

  /* celular: revela ao rolar e conta números */
  if(mobile()&&'IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting&&!en.target.dataset.seen){en.target.dataset.seen=1;en.target.classList.add('on');countUp(en.target)}})},{threshold:.05});
    slides.forEach(function(s){io.observe(s)});
  }

  addEventListener('resize',fit);fit();
  var m=/^#s(\d+)$/.exec(location.hash);
  go(m?+m[1]-1:0,true);
  addEventListener('hashchange',function(){var m=/^#s(\d+)$/.exec(location.hash);if(m&&+m[1]-1!==cur)go(+m[1]-1)});
  document.querySelector('.skip')&&document.querySelector('.skip').addEventListener('click',function(e){e.stopPropagation();next()});
})();
