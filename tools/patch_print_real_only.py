from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARKER='COPAFEM_PRINT_REAL_ONLY_V1'
if MARKER in s:
    print('print real-only already applied'); raise SystemExit

injection=r'''
<script id="COPAFEM_PRINT_REAL_ONLY_V1">
(() => {
  const realName=v=>{const t=String(v||'').trim();return !!t&&t!=='—'&&t!=='A definir';};

  function cleanPrintPages(){
    const holder=document.querySelector('#view-drop .copafem-print-pages');
    if(!holder)return;

    [...holder.querySelectorAll('.copafem-print-zones')].forEach(page=>{
      const area=page.querySelector('.drop-zones-area');
      if(!area){page.remove();return;}
      const zones=[...area.querySelectorAll(':scope > .drop-zone')];
      zones.forEach(z=>{
        const has=[...z.querySelectorAll('.drop-zone-pair span')].some(x=>realName(x.textContent));
        if(!has)z.remove();
      });
      const n=area.querySelectorAll(':scope > .drop-zone').length;
      if(!n){page.remove();return;}
      area.style.setProperty('grid-template-columns',`repeat(${Math.min(4,n)},minmax(0,1fr))`,'important');
    });

    [...holder.querySelectorAll('.copafem-print-gold')].forEach(page=>{
      const area=page.querySelector('.drop-elims');
      if(!area){page.remove();return;}
      [...area.querySelectorAll(':scope > .drop-round-col')].forEach(c=>{
        if(!c.querySelector('.drop-match'))c.remove();
      });
      const n=area.querySelectorAll(':scope > .drop-round-col').length;
      if(!n){page.remove();return;}
      area.style.setProperty('grid-template-columns',`repeat(${n},minmax(0,1fr))`,'important');
    });

    [...holder.querySelectorAll('.copafem-print-silver')].forEach(page=>{
      const area=page.querySelector('.drop-silver-area');
      if(!area){page.remove();return;}
      [...area.querySelectorAll(':scope > .drop-round-col')].forEach(c=>{
        if(!c.querySelector('.drop-match'))c.remove();
      });
      const n=area.querySelectorAll(':scope > .drop-round-col').length;
      if(!n){page.remove();return;}
      area.style.setProperty('grid-template-columns',`repeat(${n},minmax(0,1fr))`,'important');
    });
  }

  window.addEventListener('beforeprint',cleanPrintPages);
  document.addEventListener('click',e=>{
    if(e.target && (e.target.id==='dropPrintBtn'||e.target.id==='printBtn')) setTimeout(cleanPrintPages,0);
  },true);
})();
</script>
'''

head,tail=s.rsplit('</body>',1)
s=head+injection+'\n</body>'+tail
p.write_text(s,encoding='utf-8')
print('COPAFEM print real-only patch OK')
