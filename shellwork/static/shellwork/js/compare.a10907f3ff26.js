(()=>{const K='shellwork-compare',tray=document.getElementById('tray'),items=document.getElementById('trayItems'),go=document.getElementById('trayGo');
const get=()=>{try{return JSON.parse(localStorage.getItem(K))||[]}catch(e){return[]}},put=v=>{localStorage.setItem(K,JSON.stringify(v));render()};
function render(){const v=get();tray.hidden=!v.length;items.replaceChildren(...v.map(x=>{const b=document.createElement('button');b.type='button';b.textContent=x.name+' ✕';b.title='Remove';b.onclick=()=>put(get().filter(y=>y.slug!=x.slug));return b}));
 const base=go.getAttribute('href').split('?')[0];go.href=base+'?b='+v.map(x=>x.slug).join(',');go.classList.toggle('btn--mint',v.length>=2);go.textContent=v.length>=2?'Compare '+v.length:'Add one more breed';
 document.querySelectorAll('.js-compare').forEach(b=>{const on=v.some(x=>x.slug==b.dataset.slug);b.textContent=on?'✓ Added':'+ Compare'})}
document.addEventListener('click',e=>{const b=e.target.closest('.js-compare');if(!b)return;e.stopPropagation();let v=get();
 if(v.some(x=>x.slug==b.dataset.slug))v=v.filter(x=>x.slug!=b.dataset.slug);else{v.push({slug:b.dataset.slug,name:b.dataset.name});if(v.length>3)v.shift()}put(v)},true);
document.getElementById('trayClear').onclick=()=>put([]);render();})();
