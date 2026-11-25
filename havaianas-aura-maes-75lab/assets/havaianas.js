/* HAV009: abas em todas as telas (o deck base só liga a primeira de cada tipo) e vídeo só no painel aberto */
document.querySelectorAll('section.tela').forEach(function(t){
  var b=[].slice.call(t.querySelectorAll('[data-aba]')),p=[].slice.call(t.querySelectorAll('[data-painel]'));
  if(!b.length)return;
  b.forEach(function(x,k){x.addEventListener('click',function(e){e.stopPropagation();
    b.forEach(function(y,j){y.classList.toggle('on',j===k)});p.forEach(function(y,j){y.classList.toggle('on',j===k);
      y.querySelectorAll('video').forEach(function(v){j===k?v.play():v.pause()})})})});
});
