from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_RUNTIME_PRINT_RELIABILITY_V1'
if MARK in s:
    print('runtime/print reliability already applied')
    raise SystemExit

# 1) El módulo principal se ejecuta antes que los helpers de formatos de Drop.
#    Nunca debe llamar una función global que todavía no fue cargada.
s=s.replace(
    '    return copafemRebuildDropByMode(preserveScores);\n    if(dynMode()) return rebuildDynamicBrackets(preserveScores);',
    "    if(typeof window.copafemRebuildDropByMode==='function') return window.copafemRebuildDropByMode(preserveScores);\n    if(dynMode()) return rebuildDynamicBrackets(preserveScores);",
    1
)
s=s.replace(
    '); copafemRefreshDropModeUI();\n  }',
    "); if(typeof window.copafemRefreshDropModeUI==='function') window.copafemRefreshDropModeUI();\n  }",
    1
)
s=s.replace(
    "if(typeof copafemModeBracketBatches==='function') return copafemModeBracketBatches(event);",
    "if(typeof window.copafemModeBracketBatches==='function') return window.copafemModeBracketBatches(event);",
    1
)

# 2) Imprimir Drop debe conservar el gesto directo del usuario. Un setTimeout puede
#    ser bloqueado por el navegador como impresión no iniciada por un clic.
s=s.replace(
    '$("dropPrintBtn").addEventListener("click", ()=>{setView("drop"); setTimeout(()=>window.print(),120);});',
    '$("dropPrintBtn").addEventListener("click", ()=>{setView("drop"); window.print();});',
    1
)
s=s.replace('<button id="printBtn" class="btn ghost">Imprimir</button>',
            '<button id="printBtn" class="btn ghost" type="button">Imprimir</button>',1)

# 3) Refuerzo final de impresión y del ancho del Drop.
injection=r'''
<style id="COPAFEM_RUNTIME_PRINT_RELIABILITY_V1">
#copafemSchedulePrintPages{display:none}
@media screen and (min-width:1000px){
  #view-drop .drop-canvas{width:4000px!important;min-width:4000px!important}
  #view-drop .drop-category-sheet{
    width:3970px!important;
    grid-template-columns:300px 2300px 1330px!important;
    column-gap:16px!important;
  }
  #view-drop .drop-zones-area{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:18px!important}
  #view-drop .drop-zone-pair span,
  #view-drop .drop-match-row .dm-name,
  #view-drop .drop-stand-team .dm-name{white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important}
}
@media print{
  body.copafem-print-canchas-by-category #view-canchas > *:not(#copafemSchedulePrintPages){display:none!important}
  body.copafem-print-canchas-by-category #copafemSchedulePrintPages{display:block!important}
  body.copafem-print-canchas-by-category #view-canchas{display:block!important}
  .copafem-schedule-category-page{
    width:100%!important;
    box-sizing:border-box!important;
    break-after:page!important;
    page-break-after:always!important;
    padding:2mm 0!important;
  }
  .copafem-schedule-category-page:last-child{break-after:auto!important;page-break-after:auto!important}
  .copafem-schedule-category-title{
    display:flex!important;justify-content:space-between!important;align-items:center!important;
    padding:3mm 4mm!important;margin:0 0 3mm!important;border-left:2mm solid var(--pcat,#7787c7)!important;
    background:var(--psoft,#f0f2fc)!important;color:var(--pink,#334066)!important;font-weight:900!important;font-size:15pt!important;
  }
  .copafem-schedule-category-page table{width:100%!important;border-collapse:collapse!important;table-layout:fixed!important}
  .copafem-schedule-category-page th,.copafem-schedule-category-page td{font-size:8.3pt!important;padding:1.7mm 1.5mm!important;vertical-align:middle!important;border-bottom:1px solid #dbe7f2!important}
  .copafem-schedule-category-page th:nth-child(1){width:12mm!important}
  .copafem-schedule-category-page th:nth-child(2){width:18mm!important}
  .copafem-schedule-category-page th:nth-child(3){width:16mm!important}
  .copafem-schedule-category-page th:nth-child(4){width:26mm!important}
  .copafem-schedule-category-page th:nth-child(7){width:18mm!important}
  .copafem-schedule-category-page td:nth-child(5),.copafem-schedule-category-page td:nth-child(6){white-space:normal!important;overflow:visible!important;text-overflow:clip!important}
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

  function buildSchedulePrintPages(){
    const view=document.getElementById('view-canchas');
    if(!view || !view.classList.contains('active')) return;
    const body=document.getElementById('scheduleBody');
    if(!body) return;
    const rows=[...body.querySelectorAll('tr')].filter(r=>r.cells && r.cells.length>=7);
    if(!rows.length) return;
    let holder=document.getElementById('copafemSchedulePrintPages');
    if(!holder){holder=document.createElement('div');holder.id='copafemSchedulePrintPages';view.appendChild(holder);}
    holder.innerHTML='';
    const groups=new Map();
    rows.forEach(r=>{
      const cat=(r.cells[2]?.textContent||'').trim()||'Categoría';
      if(!groups.has(cat))groups.set(cat,[]);
      groups.get(cat).push(r);
    });
    const date=(window.state?.tournament?.date||'').split('-').reverse().join('/');
    groups.forEach((catRows,cat)=>{
      const c=COLORS[cat]||COLORS['7ma'];
      const page=document.createElement('section');
      page.className='copafem-schedule-category-page';
      page.style.setProperty('--pcat',c.main);page.style.setProperty('--psoft',c.soft);page.style.setProperty('--pink',c.ink);
      const title=document.createElement('div');title.className='copafem-schedule-category-title';
      title.innerHTML='<span>COPAFEM · '+cat+'</span><small>'+date+'</small>';
      page.appendChild(title);
      const table=document.createElement('table');table.className='schedule-table';
      table.innerHTML='<thead><tr><th>Hora</th><th>Cancha</th><th>Categoría</th><th>Etapa</th><th>Pareja 1</th><th>Pareja 2</th><th>Resultado</th></tr></thead><tbody></tbody>';
      const tb=table.querySelector('tbody');catRows.forEach(r=>tb.appendChild(r.cloneNode(true)));
      page.appendChild(table);holder.appendChild(page);
    });
    document.body.classList.add('copafem-print-canchas-by-category');
  }
  function cleanupSchedulePrint(){document.body.classList.remove('copafem-print-canchas-by-category');}
  window.addEventListener('beforeprint',buildSchedulePrintPages);
  window.addEventListener('afterprint',cleanupSchedulePrint);

  // Si los helpers del selector se cargaron después del módulo principal,
  // refrescar una sola vez cuando toda la página ya está disponible.
  window.addEventListener('load',()=>setTimeout(()=>{
    try{
      if(typeof window.copafemRefreshDropModeUI==='function') window.copafemRefreshDropModeUI();
      if(typeof window.renderAll==='function') window.renderAll();
    }catch(err){console.error('COPAFEM post-load:',err);}
  },0));
})();
</script>
'''

if '</body>' not in s:
    raise SystemExit('No se encontró </body>')
head,tail=s.rsplit('</body>',1)
s=head+injection+'\n</body>'+tail
p.write_text(s,encoding='utf-8')
print('COPAFEM runtime, botones e impresión reforzados')
