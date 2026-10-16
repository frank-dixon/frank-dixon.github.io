(()=>{const drum=document.getElementById('drum');if(!drum)return;
const cards=[...drum.querySelectorAll('.rc')],N=cards.length,step=360/N,wheel=document.getElementById('wheel'),
pulled=document.getElementById('pulled'),pin=document.getElementById('pin'),cnt=document.getElementById('cnt');
let ang=0,cur=0,f={c:null,s:null,h:null};
const match=i=>{const d=cards[i].dataset;return(!f.c||d.c==f.c)&&(!f.s||d.s==f.s)&&(!f.h||d.h==f.h)};
function set(){const pos=ang/step;cur=((Math.round(pos)%N)+N)%N;cards.forEach((c,i)=>{const d=((i-pos)%N+N+N/2)%N-N/2;c.style.transform='rotateX('+(-d*36)+'deg) translateZ(330px)';const v=Math.abs(d)<1.6;c.style.opacity=v?'':0;c.style.pointerEvents=Math.abs(d)<.5?'':'none';c.setAttribute('aria-hidden',Math.abs(d)<.5?'false':'true')})}
function go(i){const t=i*step;ang=ang+((t-ang)%360+540)%360-180;set()}
function stepTo(dir){for(let k=1;k<=N;k++){const j=((cur+dir*k)%N+N)%N;if(match(j)){go(j);return}}}
function apply(){cards.forEach((c,i)=>c.classList.toggle('dim',!match(i)));const m=cards.map((_,i)=>i).filter(match);cnt.textContent=m.length+' of '+N+' breeds match';if(m.length&&!match(cur))go(m[0]);
 document.querySelectorAll('#filters .chip').forEach(b=>b.classList.toggle('on',b.dataset.k!='x'&&f[b.dataset.k]==b.dataset.v))}
document.querySelectorAll('#filters .chip').forEach(b=>b.onclick=()=>{if(b.dataset.k=='x')f={c:null,s:null,h:null};else f[b.dataset.k]=f[b.dataset.k]==b.dataset.v?null:b.dataset.v;apply()});
let lockY=0;function lock(){if(document.body.classList.contains('sw-lock'))return;lockY=window.scrollY;document.body.style.top=-lockY+'px';document.body.classList.add('sw-lock')}
function unlock(){if(!document.body.classList.contains('sw-lock'))return;document.body.classList.remove('sw-lock');document.body.style.top='';window.scrollTo(0,lockY)}
function open(){if(!match(cur))return;lock();const t=document.getElementById('t-'+cards[cur].dataset.slug);pin.replaceChildren(t.content.cloneNode(true));pulled.className='pulled';pulled.hidden=false;pin.style.animation='none';pin.offsetHeight;pin.style.animation='';pin.focus?.()}
function close(){pulled.hidden=true;pulled.className='pulled';unlock()}
pin.addEventListener('click',e=>{const t=e.target.closest('.pc__ctog');if(!t)return;const on=t.getAttribute('aria-expanded')!='true';t.setAttribute('aria-expanded',on);document.getElementById(t.getAttribute('aria-controls')).hidden=!on});
pulled.addEventListener('click',e=>{if(e.target===pulled)close()});
document.getElementById('pull').onclick=open;
document.getElementById('up').onclick=document.getElementById('kl').onclick=()=>stepTo(-1);
document.getElementById('down').onclick=document.getElementById('kr').onclick=()=>stepTo(1);
wheel.addEventListener('selectstart',e=>e.preventDefault());wheel.addEventListener('dragstart',e=>e.preventDefault());
wheel.addEventListener('wheel',e=>{e.preventDefault();stepTo(Math.sign(e.deltaY))},{passive:false});
wheel.onpointerdown=e=>{if(e.button>0||!pulled.hidden||e.target.closest('#pulled'))return;e.preventDefault();window.getSelection()?.removeAllRanges();wheel.setPointerCapture(e.pointerId);drum.classList.add('drag');const sy=e.clientY,a0=ang;let mv=0;
 wheel.onpointermove=ev=>{mv=Math.max(mv,Math.abs(ev.clientY-sy));ang=a0-(ev.clientY-sy)*.5;/* minus: cards follow the finger (next card sits below) */set()};
 wheel.onpointerup=()=>{wheel.onpointermove=null;drum.classList.remove('drag');ang=Math.round(ang/step)*step;set();if(!match(cur))stepTo(1);if(mv<5)open()}};
addEventListener('keydown',e=>{if(!pulled.hidden){if(e.key=='Escape')close();if(e.key=='Enter'&&!e.target.closest('a,button'))pin.click();return}
 if(e.target.closest('input,textarea'))return;if(e.key=='ArrowUp'){e.preventDefault();stepTo(-1)}if(e.key=='ArrowDown'){e.preventDefault();stepTo(1)}if(e.key=='Enter'&&e.target===wheel)open()});
set();apply();window.shellwork={stepTo,open,close,go,get cur(){return cards[cur].dataset.slug}};})();
