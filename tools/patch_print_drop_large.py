from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

MARKER = 'COPAFEM_PRINT_3_PAGES_V2'
if MARKER in s:
    print('three-page print already applied')
    raise SystemExit

injection = r'''
<style id="COPAFEM_PRINT_3_PAGES_V2">
.copafem-print-pages{display:none}
@page{size:A4 landscape;margin:5mm}
@media print{
  html,body{background:#fff!important;margin:0!important;padding:0!important}

  #view-drop.active .drop-title-row,
  #view-drop.active .drop-meta,
  #view-drop.active .drop-scroll,
  #view-drop.active .drop-mobile-hint{display:none!important}

  #view-drop.active .copafem-print-pages{
    display:block!important;
    width:100%!important;
    margin:0!important;
    padding:0!important;
  }

  .copafem-print-page{
    box-sizing:border-box!important;
    width:287mm!important;
    height:200mm!important;
    overflow:hidden!important;
    margin:0!important;
    padding:3mm 4mm!important;
    background:#fff!important;
    color:#233a59!important;
    break-after:page!important;
    page-break-after:always!important;
  }
  .copafem-print-page:last-child{
    break-after:auto!important;
    page-break-after:auto!important;
  }

  .copafem-print-title{
    display:flex!important;
    justify-content:space-between!important;
    align-items:center!important;
    min-height:11mm!important;
    margin:0 0 3mm!important;
    padding:2mm 4mm!important;
    border-left:2.2mm solid var(--print-cat,#7787c7)!important;
    background:var(--print-soft,#f0f2fc)!important;
    color:var(--print-ink,#334066)!important;
    font-size:15pt!important;
    font-weight:950!important;
    text-transform:uppercase!important;
    letter-spacing:.03em!important;
  }
  .copafem-print-title small{
    font-size:9pt!important;
    font-weight:800!important;
    text-transform:none!important;
    letter-spacing:0!important;
  }

  /* HOJA 1 — ZONAS */
  .copafem-print-zones .drop-zones-area{
    display:grid!important;
    grid-template-columns:repeat(4,minmax(0,1fr))!important;
    gap:3mm!important;
    width:100%!important;
    align-content:start!important;
  }
  .copafem-print-zones .drop-zone{
    border:1.2px solid #9fb4c8!important;
    break-inside:avoid!important;
    page-break-inside:avoid!important;
    min-width:0!important;
  }
  .copafem-print-zones .drop-zone-head{
    padding:2.1mm 2.3mm!important;
    font-size:10pt!important;
  }
  .copafem-print-zones .drop-zone-pair{
    min-height:6.1mm!important;
    grid-template-columns:7mm 1fr!important;
    font-size:8.6pt!important;
  }
  .copafem-print-zones .drop-zone-pair span{
    padding:1.2mm 1.5mm!important;
  }
  .copafem-print-zones .drop-mini-label{
    padding:1.2mm 1.6mm!important;
    font-size:7.4pt!important;
  }
  .copafem-print-zones .drop-match-row{
    grid-template-columns:1fr 13mm 12mm 1fr 11mm!important;
    gap:.8mm!important;
    padding:1.1mm 1.3mm!important;
    font-size:7.2pt!important;
    min-height:5.5mm!important;
  }
  .copafem-print-zones .drop-stand-row{
    grid-template-columns:6mm 1fr 9mm 10mm!important;
    gap:.8mm!important;
    padding:1.05mm 1.3mm!important;
    font-size:7.2pt!important;
    min-height:5.3mm!important;
  }

  /* HOJA 2 — COPA DE ORO */
  .copafem-print-gold .drop-elims{
    display:grid!important;
    grid-template-columns:2.15fr 1.4fr 1fr .9fr!important;
    gap:5mm!important;
    width:100%!important;
    align-content:start!important;
  }
  .copafem-print-gold .drop-round-title{
    padding:2.3mm 2mm!important;
    margin-bottom:2.5mm!important;
    font-size:10.5pt!important;
  }
  .copafem-print-gold .drop-match{
    margin:2.4mm 0!important;
    min-height:13mm!important;
    border:1.2px solid #c7d2dd!important;
    break-inside:avoid!important;
  }
  .copafem-print-gold .drop-match-head{
    min-height:5.2mm!important;
    padding:1.3mm 1.8mm!important;
    font-size:8.3pt!important;
  }
  .copafem-print-gold .drop-match-team{
    grid-template-columns:1fr 8mm!important;
    padding:1.6mm 1.8mm!important;
    font-size:8.8pt!important;
    min-height:6mm!important;
  }

  /* HOJA 3 — COPA DE PLATA */
  .copafem-print-silver .drop-silver-area{
    display:grid!important;
    border-top:0!important;
    padding-top:0!important;
    gap:5mm!important;
    width:100%!important;
    align-content:start!important;
  }
  .copafem-print-silver .drop-silver-heading{display:none!important}
  .copafem-print-silver .drop-round-title{
    padding:2.5mm 2mm!important;
    margin-bottom:3mm!important;
    font-size:11pt!important;
  }
  .copafem-print-silver .drop-match{
    margin:3mm 0!important;
    min-height:15mm!important;
    border:1.2px solid #c5ced7!important;
    break-inside:avoid!important;
  }
  .copafem-print-silver .drop-match-head{
    min-height:5.6mm!important;
    padding:1.4mm 2mm!important;
    font-size:9pt!important;
  }
  .copafem-print-silver .drop-match-team{
    grid-template-columns:1fr 9mm!important;
    padding:1.9mm 2mm!important;
    font-size:9.5pt!important;
    min-height:6.5mm!important;
  }
}
</style>
<script>
(() => {
  const COLORS={
    '4ta':{main:'#234f7d',soft:'#e8f0f8',ink:'#173554'},
    '5ta':{main:'#4d86c6',soft:'#edf5fd',ink:'#315b89'},
    '6ta':{main:'#3f9f9a',soft:'#eaf8f6',ink:'#246b67'},
    '7ma':{main:'#7b78bd',soft:'#f1f0fb',ink:'#514e88'},
    '8va':{main:'#d2a33a',soft:'#fff7df',ink:'#7d5e17'}
  };

  function info(sheet){
    const text=sheet.querySelector('.drop-block-title')?.textContent||'';
    const cat=(text.match(/·\s*(4ta|5ta|6ta|7ma|8va)\s*·/i)||[])[1]||'';
    const date=(text.match(/·\s*(\d{2}\/\d{2}\/\d{4})\s*·/i)||[])[1]||'';
    const courts=(text.match(/Canchas\s+(.+)$/i)||[])[1]||'';
    return {cat,date,courts,color:COLORS[cat.toLowerCase()]||COLORS['7ma']};
  }

  function title(meta,section){
    const el=document.createElement('div');
    el.className='copafem-print-title';
    el.innerHTML='<span>COPAFEM · '+(meta.cat||'')+' · '+section+'</span><small>'+[meta.date,meta.courts?'Canchas '+meta.courts:''].filter(Boolean).join(' · ')+'</small>';
    return el;
  }

  function page(meta,kind,label,node){
    const p=document.createElement('section');
    p.className='copafem-print-page copafem-print-'+kind;
    p.style.setProperty('--print-cat',meta.color.main);
    p.style.setProperty('--print-soft',meta.color.soft);
    p.style.setProperty('--print-ink',meta.color.ink);
    p.appendChild(title(meta,label));
    if(node)p.appendChild(node.cloneNode(true));
    return p;
  }

  function cleanSilver(clone){
    const cols=[...clone.querySelectorAll(':scope > .drop-round-col')].filter(c=>getComputedStyle(c).display!=='none' && c.style.display!=='none');
    [...clone.querySelectorAll(':scope > .drop-round-col')].forEach(c=>{if(!cols.includes(c))c.remove();});
    const n=Math.max(1,cols.length);
    clone.style.gridTemplateColumns='repeat('+n+',minmax(0,1fr))';
    return clone;
  }

  function buildPrintPages(){
    const view=document.getElementById('view-drop');
    if(!view)return;
    let holder=view.querySelector('.copafem-print-pages');
    if(!holder){holder=document.createElement('div');holder.className='copafem-print-pages';view.appendChild(holder);}
    holder.innerHTML='';

    const sheets=[...view.querySelectorAll('.drop-category-sheet')];
    sheets.forEach(sheet=>{
      const meta=info(sheet);
      const zones=sheet.querySelector('.drop-zones-area');
      const gold=sheet.querySelector('.drop-elims');
      const silver=sheet.querySelector('.drop-silver-area');
      if(zones)holder.appendChild(page(meta,'zones','ZONAS',zones));
      if(gold)holder.appendChild(page(meta,'gold','COPA DE ORO',gold));
      if(silver){
        const silverClone=silver.cloneNode(true);
        cleanSilver(silverClone);
        holder.appendChild(page(meta,'silver','COPA DE PLATA',silverClone));
      }
    });
  }

  window.addEventListener('beforeprint',buildPrintPages);
  document.addEventListener('click',e=>{
    if(e.target && (e.target.id==='dropPrintBtn' || e.target.id==='printBtn')) buildPrintPages();
  },true);
})();
</script>
'''

if '</body>' not in s:
    raise SystemExit('No se encontró </body> en index.html')
head, tail = s.rsplit('</body>', 1)
s = head + injection + '\n</body>' + tail
p.write_text(s, encoding='utf-8')
print('COPAFEM three-page A4 print patch OK')
