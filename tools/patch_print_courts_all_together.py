from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_PRINT_COURTS_ALL_TOGETHER_V1'
if MARK in s:
    print('courts all-together print already applied')
    raise SystemExit

patch=r'''
<style id="COPAFEM_PRINT_COURTS_ALL_TOGETHER_V1">
@media print{
  body.copafem-print-canchas-by-category .copafem-schedule-category-page{
    break-after:auto!important;
    page-break-after:auto!important;
  }
  body.copafem-print-canchas-by-category .copafem-schedule-category-title{
    border-left-color:#7b78bd!important;
    background:#f1f0fb!important;
    color:#334066!important;
  }
  body.copafem-print-canchas-by-category .copafem-schedule-category-page thead{
    display:table-header-group!important;
  }
}
</style>
<script>
(() => {
  function buildAllCourtsTogether(){
    const view=document.getElementById('view-canchas');
    if(!view || !view.classList.contains('active')) return;
    const body=document.getElementById('scheduleBody');
    if(!body) return;
    const rows=[...body.querySelectorAll('tr')].filter(r=>r.cells && r.cells.length>=7);
    if(!rows.length) return;

    let holder=document.getElementById('copafemSchedulePrintPages');
    if(!holder){
      holder=document.createElement('div');
      holder.id='copafemSchedulePrintPages';
      view.appendChild(holder);
    }
    holder.innerHTML='';

    const page=document.createElement('section');
    page.className='copafem-schedule-category-page';
    page.style.setProperty('--pcat','#7b78bd');
    page.style.setProperty('--psoft','#f1f0fb');
    page.style.setProperty('--pink','#334066');

    const date=(window.state?.tournament?.date||'').split('-').reverse().join('/');
    const title=document.createElement('div');
    title.className='copafem-schedule-category-title';
    title.innerHTML='<span>COPAFEM · RESUMEN DE CANCHAS</span><small>'+date+'</small>';
    page.appendChild(title);

    const table=document.createElement('table');
    table.className='schedule-table';
    table.innerHTML='<thead><tr><th>Hora</th><th>Cancha</th><th>Categoría</th><th>Etapa</th><th>Pareja 1</th><th>Pareja 2</th><th>Resultado</th></tr></thead><tbody></tbody>';
    const tb=table.querySelector('tbody');

    // Conserva exactamente el orden que ya se ve en el Resumen de Canchas.
    rows.forEach(r=>tb.appendChild(r.cloneNode(true)));

    page.appendChild(table);
    holder.appendChild(page);
    document.body.classList.add('copafem-print-canchas-by-category');
  }

  // Se registra al final para reemplazar la impresión anterior separada por categoría.
  window.addEventListener('beforeprint',buildAllCourtsTogether);
})();
</script>
'''

if '</body>' not in s:
    raise SystemExit('No se encontró </body>')
head,tail=s.rsplit('</body>',1)
s=head+patch+'\n<!-- '+MARK+' -->\n</body>'+tail
p.write_text(s,encoding='utf-8')
print('COPAFEM: impresión de canchas unificada y en el mismo orden de pantalla')
