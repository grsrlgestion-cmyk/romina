from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_PRINT_CUPS_FIVE_PAGES_V1'
if MARK in s:
    print('cups five-page print already applied')
    raise SystemExit

patch=r'''
<style id="COPAFEM_PRINT_CUPS_FIVE_PAGES_V1">
#copafemCupsPrintPages{display:none}
@media print{
  body.copafem-print-cups-five #view-copas.active > *:not(#copafemCupsPrintPages){display:none!important}
  body.copafem-print-cups-five #view-copas.active #copafemCupsPrintPages{
    display:block!important;
    margin:0!important;
    padding:0!important;
    width:100%!important;
  }
  body.copafem-print-cups-five .copafem-print-context{display:none!important}

  .copafem-cups-print-page{
    box-sizing:border-box!important;
    width:100%!important;
    margin:0!important;
    padding:0!important;
    break-after:page!important;
    page-break-after:always!important;
    break-before:auto!important;
    page-break-before:auto!important;
  }
  .copafem-cups-print-page:last-child{
    break-after:auto!important;
    page-break-after:auto!important;
  }
  .copafem-cups-print-head{
    display:flex!important;
    justify-content:space-between!important;
    align-items:center!important;
    gap:4mm!important;
    margin:0 0 3mm!important;
    padding:2.5mm 3.5mm!important;
    border-left:2mm solid var(--pcat,#7787c7)!important;
    background:var(--psoft,#f0f2fc)!important;
    color:var(--pink,#334066)!important;
    font-size:13pt!important;
    font-weight:950!important;
    line-height:1.1!important;
  }
  .copafem-cups-print-head small{
    font-size:8.5pt!important;
    font-weight:800!important;
    white-space:nowrap!important;
  }
  .copafem-cups-print-subtitle{
    margin:0 0 2.5mm!important;
    font-size:12pt!important;
    font-weight:900!important;
    color:#223a5e!important;
  }
  .copafem-cups-print-rounds{
    display:grid!important;
    grid-template-columns:1fr!important;
    gap:2mm!important;
    margin:0!important;
    padding:0!important;
  }
  .copafem-cups-print-page.combo .copafem-cups-print-rounds{
    grid-template-columns:1fr 1fr!important;
    gap:5mm!important;
    align-items:start!important;
  }
  .copafem-cups-print-page .round{
    margin:0!important;
    padding:0!important;
    break-inside:avoid!important;
    page-break-inside:avoid!important;
  }
  .copafem-cups-print-page .round-title{
    margin:0 0 1.5mm!important;
    padding:1.5mm 2mm!important;
    background:#f4f7fb!important;
    border-left:1.4mm solid var(--pcat,#7787c7)!important;
    font-size:9pt!important;
    font-weight:950!important;
    color:#344b68!important;
  }
  .copafem-cups-print-page .bracket-match{
    margin:1.15mm 0!important;
    padding:1.35mm 1.7mm!important;
    border:1px solid #d6e2ed!important;
    border-radius:2mm!important;
    background:#fff!important;
    break-inside:avoid!important;
    page-break-inside:avoid!important;
  }
  .copafem-cups-print-page .bracket-meta{
    margin:0 0 .5mm!important;
    font-size:6.8pt!important;
    color:#5d6e84!important;
  }
  .copafem-cups-print-page .bracket-team{
    display:grid!important;
    grid-template-columns:minmax(0,1fr) 8mm!important;
    gap:1.2mm!important;
    padding:.65mm 0!important;
  }
  .copafem-cups-print-page .bracket-team span{
    font-size:7.8pt!important;
    line-height:1.12!important;
    white-space:normal!important;
    overflow:visible!important;
    text-overflow:clip!important;
  }
  .copafem-cups-print-page .bracket-team input{
    width:8mm!important;
    min-width:8mm!important;
    height:6.6mm!important;
    padding:.4mm!important;
    font-size:7.5pt!important;
    border-radius:1.4mm!important;
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
  function activeViewIsCups(){return document.getElementById('view-copas')?.classList.contains('active');}
  function val(id){return (document.getElementById(id)?.value||'').trim();}
  function category(){return val('category')||document.getElementById('dropCategoryBadge')?.textContent?.trim()||'Categoría';}
  function dateText(){
    const raw=val('tournamentDate')||val('newEventDate')||'';
    if(/^\d{4}-\d{2}-\d{2}$/.test(raw)) return raw.split('-').reverse().join('/');
    return raw;
  }
  function findRound(root,name){
    return [...(root?.querySelectorAll('.round')||[])].find(r=>(r.querySelector('.round-title')?.textContent||'').trim().toLowerCase().includes(name.toLowerCase()))||null;
  }
  function head(cat,date,label,color){
    const h=document.createElement('div');
    h.className='copafem-cups-print-head';
    h.style.setProperty('--pcat',color.main);h.style.setProperty('--psoft',color.soft);h.style.setProperty('--pink',color.ink);
    h.innerHTML='<span>COPAFEM · '+cat+' · '+label+'</span><small>'+date+'</small>';
    return h;
  }
  function page(cat,date,label,color,rounds,combo=false){
    const p=document.createElement('section');
    p.className='copafem-cups-print-page'+(combo?' combo':'');
    p.style.setProperty('--pcat',color.main);p.style.setProperty('--psoft',color.soft);p.style.setProperty('--pink',color.ink);
    p.appendChild(head(cat,date,label,color));
    const sub=document.createElement('div');sub.className='copafem-cups-print-subtitle';sub.textContent=label;p.appendChild(sub);
    const wrap=document.createElement('div');wrap.className='copafem-cups-print-rounds';
    rounds.filter(Boolean).forEach(r=>wrap.appendChild(r.cloneNode(true)));
    p.appendChild(wrap);
    return p;
  }
  function build(){
    const view=document.getElementById('view-copas');
    if(!view || !activeViewIsCups()) return;
    let holder=document.getElementById('copafemCupsPrintPages');
    if(!holder){holder=document.createElement('div');holder.id='copafemCupsPrintPages';view.appendChild(holder);}
    holder.innerHTML='';
    const cat=category(),date=dateText(),c=COLORS[cat]||COLORS['7ma'];
    const gold=document.getElementById('goldBracket');
    const silver=document.getElementById('silverBracket');

    holder.appendChild(page(cat,date,'COPA DE ORO · OCTAVOS',c,[findRound(gold,'octavos')]));
    holder.appendChild(page(cat,date,'COPA DE ORO · CUARTOS',c,[findRound(gold,'cuartos')]));
    holder.appendChild(page(cat,date,'COPA DE ORO · SEMIFINAL Y FINAL',c,[findRound(gold,'semifinal'),findRound(gold,'final')],true));
    holder.appendChild(page(cat,date,'COPA DE PLATA · CUARTOS',c,[findRound(silver,'cuartos')]));
    holder.appendChild(page(cat,date,'COPA DE PLATA · SEMIFINAL Y FINAL',c,[findRound(silver,'semifinal'),findRound(silver,'final')],true));
    document.body.classList.add('copafem-print-cups-five');
  }
  function cleanup(){document.body.classList.remove('copafem-print-cups-five');}
  window.addEventListener('beforeprint',build);
  window.addEventListener('afterprint',cleanup);
  document.addEventListener('click',e=>{if(e.target?.id==='printBtn' && activeViewIsCups()) build();},true);
})();
</script>
'''

if '</body>' not in s:
    raise SystemExit('No se encontró </body>')
head,tail=s.rsplit('</body>',1)
s=head+patch+'\n<!-- '+MARK+' -->\n</body>'+tail
p.write_text(s,encoding='utf-8')
print('COPAFEM: impresión Oro/Plata separada en cinco hojas')
