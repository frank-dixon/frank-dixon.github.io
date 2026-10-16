// Compare page: shows the ?b=slug,slug(,slug) columns in that order. Client-side so it works statically.
(()=>{const grid=document.getElementById('cmp'),cols=[...grid.querySelectorAll('.cmp__col')],empty=document.getElementById('cmpEmpty');
const slugs=(new URLSearchParams(location.search).get('b')||'').split(',').filter(Boolean).slice(0,3);
let n=0;cols.forEach(c=>{const i=slugs.indexOf(c.dataset.slug);c.hidden=i<0;c.style.order=i;if(i>=0)n++});
grid.style.setProperty('--n',Math.max(n,1));empty.hidden=n>=2;})();
