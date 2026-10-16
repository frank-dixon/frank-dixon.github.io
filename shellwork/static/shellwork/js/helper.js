// Breeding-for-color filter, client-side so it also works on the static (GitHub Pages) freeze.
(()=>{const chips=[...document.querySelectorAll('#helperChips .chip')],cards=[...document.querySelectorAll('.paircard')],
layers=[...document.querySelectorAll('.js-layers')],none=document.getElementById('noPairs');
function apply(cat){let n=0;cards.forEach(c=>{const on=!cat||c.dataset.cat===cat;c.hidden=!on;if(on)n++});
 layers.forEach(l=>l.hidden=l.dataset.cat!==cat);chips.forEach(c=>c.classList.toggle('on',!!cat&&c.dataset.cat===cat));none.hidden=n>0}
chips.forEach(c=>c.addEventListener('click',e=>{e.preventDefault();const cat=c.dataset.cat;
 history.pushState({cat},'',cat?'?colour='+encodeURIComponent(cat):location.pathname);apply(cat)}));
addEventListener('popstate',()=>apply(new URLSearchParams(location.search).get('colour')||''));
apply(new URLSearchParams(location.search).get('colour')||'');})();
