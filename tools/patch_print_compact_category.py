from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_PRINT_COMPACT_CATEGORY_V1'
if MARK in s:
    print('print compact/category already applied')
    raise SystemExit

patch=r'''
<style id="COPAFEM_PRINT_COMPACT_CATEGORY_V1">
.copafem-print-context{display:none}
@media print{
  /* Encabezado de categoría para las vistas que imprimen directamente. */
  .copafem-print-context{
    display:flex!important;
    align-items:center!important;
    justify-content:space-between!important;
    gap:4mm!important;
    margin:0 0 3mm!important;
    padding:2.5mm 3.5mm!important;
    border-left:2mm solid var(--cat,#7787c7)!important;
    background:var(--cat-soft,#f0f2fc)!important;
    color:var(--cat-ink,#334066)!important;
    font-size:13pt!important;
    font-weight:950!important;
    line-height:1.1!important;
  }
  .copafem-print-context small{
    font-size:8.5pt!important;
    font-weight:800!important;
    white-space:nowrap!important;
  }

  /* Oro / Plata: evitar que el panel entero salte a la hoja siguiente.
     Ese break-inside heredado era el que podía dejar la primera hoja vacía. */
  #view-copas.active .brackets-wrap{
    display:block!important;
    margin:0!important;
    padding:0!important;
  }
  #view-copas.active .panel,
  #view-copas.active .gold-panel,
  #view-copas.active .silver-panel{
    break-inside:auto!important;
    page-break-inside:auto!important;
    break-before:auto!important;
    page-break-before:auto!important;
    margin:0 0 3mm!important;
    padding:3mm 3.5mm!important;
    box-shadow:none!important;
  }
  #view-copas.active .section-title{
    margin:0 0 2.5mm!important;
    padding:0!important;
  }
  #view-copas.active .section-title h2{font-size:15pt!important;line-height:1.1!important}
  #view-copas.active .section-title p{font-size:8pt!important;margin-top:1mm!important}
  #view-copas.active .cup-title{margin:0 0 2mm!important;gap:2mm!important}
  #view-copas.active .cup-title .cup{font-size:17pt!important}
  #view-copas.active .cup-title h3{font-size:13pt!important;line-height:1.1!important}
  #view-copas.active .cup-title p{font-size:7.5pt!important;margin-top:.7mm!important}
  #view-copas.active .round{margin:2mm 0 3mm!important}
  #view-copas.active .round-title{font-size:8pt!important;margin:0 0 1.2mm!important}
  #view-copas.active .bracket-match{
    break-inside:avoid!important;
    page-break-inside:avoid!important;
    margin:1.2mm 0!important;
    padding:1.4mm 1.8mm!important;
    border-radius:2mm!important;
  }
  #view-copas.active .bracket-meta{font-size:7pt!important;margin-bottom:.5mm!important}
  #view-copas.active .bracket-team{
    grid-template-columns:minmax(0,1fr) 8.5mm!important;
    gap:1.2mm!important;
    padding:.8mm 0!important;
  }
  #view-copas.active .bracket-team span{
    font-size:8pt!important;
    line-height:1.15!important;
    white-space:normal!important;
    overflow:visible!important;
    text-overflow:clip!important;
  }
  #view-copas.active .bracket-team input{
    width:8.5mm!important;
    min-width:8.5mm!important;
    height:7mm!important;
    padding:.5mm!important;
    font-size:8pt!important;
    border-radius:1.5mm!important;
  }

  /* Evitar hojas fantasma antes del contenido activo. */
  #view-copas.active{margin:0!important;padding:0!important;break-before:auto!important;page-break-before:auto!important}
  #view-copas.active > :first-child{break-before:auto!important;page-break-before:auto!important}

  /* Drop y Canchas ya generan sus propios encabezados por categoría. */
  #view-drop .copafem-print-context,
  #view-canchas .copafem-print-context{display:none!important}
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
  const LABELS={
    'view-inicio':'Inicio','view-parejas':'Parejas','view-zonas':'Zonas',
    'view-resultados':'Resultados','view-copas':'Oro / Plata','view-datos':'Datos'
  };

  function value(id){return (document.getElementById(id)?.value||'').trim();}
  function formatDate(raw){
    if(/^\\d{4}-\\d{2}-\\d{2}$/.test(raw)) return raw.split('-').reverse().join('/');
    return raw||'';
  }
  function preparePrintContext(){
    document.querySelectorAll('.copafem-print-context').forEach(x=>x.remove());
    const view=document.querySelector('.view.active');
    if(!view || view.id==='view-drop' || view.id==='view-canchas') return;
    const cat=value('category') || value('newEventCategory') || document.getElementById('dropCategoryBadge')?.textContent?.trim() || 'Categoría';
    const date=formatDate(value('tournamentDate') || value('newEventDate'));
    const c=COLORS[cat]||COLORS['7ma'];
    const label=LABELS[view.id]||'';
    const head=document.createElement('div');
    head.className='copafem-print-context';
    head.style.setProperty('--cat',c.main);
    head.style.setProperty('--cat-soft',c.soft);
    head.style.setProperty('--cat-ink',c.ink);
    head.innerHTML='<span>COPAFEM · '+cat+(label?' · '+label:'')+'</span><small>'+date+'</small>';
    view.insertBefore(head,view.firstChild);
  }
  function cleanup(){document.querySelectorAll('.copafem-print-context').forEach(x=>x.remove());}
  window.addEventListener('beforeprint',preparePrintContext);
  window.addEventListener('afterprint',cleanup);
  document.addEventListener('click',e=>{
    if(e.target?.id==='printBtn' || e.target?.id==='dropPrintBtn') preparePrintContext();
  },true);
})();
</script>
'''

if '</body>' not in s:
    raise SystemExit('No se encontró </body>')
head,tail=s.rsplit('</body>',1)
s=head+patch+'\n<!-- '+MARK+' -->\n</body>'+tail
p.write_text(s,encoding='utf-8')
print('COPAFEM: impresión compacta, con categoría y sin salto inicial')
