from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_FINAL_WEB_AUDIT_V1'
if MARK in s:
    print('final web audit already applied')
    raise SystemExit

# Puente seguro entre la lógica principal (IIFE) y los helpers de formatos de Drop
# agregados por los últimos parches. Se usan accessors para que siempre apunten al
# state activo, incluso al cambiar de fecha/categoría.
bridge=r'''
  /* COPAFEM_FINAL_WEB_AUDIT_V1 — puente de funciones internas */
  try{
    Object.defineProperty(window,'state',{configurable:true,get:()=>state,set:v=>{state=v;}});
    Object.defineProperty(window,'store',{configurable:true,get:()=>store,set:v=>{store=v;}});
  }catch(_){ window.state=state; window.store=store; }
  window.ZONES=ZONES;
  window.CATEGORIES=CATEGORIES;
  window.zoneStandings=zoneStandings;
  window.hasScore=hasScore;
  window.winnerId=winnerId;
  window.loserId=loserId;
  window.scheduleBrackets=scheduleBrackets;
  window.saveState=saveState;
  window.renderAll=renderAll;
  window.renderCups=renderCups;
  window.renderSchedule=renderSchedule;
  window.renderHeader=renderHeader;
  window.renderDrop=renderDrop;
  window.setZoneScore=setZoneScore;
  window.setBracketScore=setBracketScore;
  window.toast=toast;
  if(typeof copafemRealMatch==='function') window.copafemRealMatch=copafemRealMatch;
'''
needle='  init();\n})();'
if needle not in s:
    raise SystemExit('No se encontró cierre del módulo administrador')
s=s.replace(needle,bridge+'\n'+needle,1)

# Ajustes finales de amplitud del Drop y comportamiento de inputs.
injection=r'''
<style id="COPAFEM_FINAL_WEB_AUDIT_V1">
@media screen and (min-width:1000px){
  /* Drop realmente amplio: A-B / C-D con espacio suficiente para nombres completos. */
  #view-drop .drop-canvas{width:3400px!important;min-width:3400px!important}
  #view-drop .drop-category-sheet{
    width:3370px!important;
    grid-template-columns:250px 1820px 1260px!important;
    column-gap:14px!important;
  }
  #view-drop .drop-zones-area{
    grid-template-columns:repeat(2,minmax(0,1fr))!important;
    gap:16px!important;
  }
  #view-drop .drop-zone-pair{grid-template-columns:52px minmax(0,1fr)!important;font-size:10.5px!important}
  #view-drop .drop-zone-pair span{font-size:10.5px!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important}
  #view-drop .drop-match-row{
    grid-template-columns:minmax(0,1.35fr) 58px 54px minmax(0,1.35fr) 48px!important;
    gap:5px!important;font-size:9.3px!important
  }
  #view-drop .drop-match-row .dm-team{grid-template-columns:34px minmax(0,1fr)!important;gap:5px!important}
  #view-drop .drop-match-row .dm-code{min-width:34px!important;font-size:9.5px!important}
  #view-drop .drop-match-row .dm-name,
  #view-drop .drop-stand-team .dm-name{font-size:9.3px!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important}
  #view-drop .drop-stand-row{grid-template-columns:24px minmax(0,1fr) 34px 38px!important;font-size:9px!important}
}

@media print{
  /* Nunca mezclar dos categorías en la misma hoja del Drop. Cada sección de la
     categoría (Zonas/Oro/Plata) queda en su propia A4, conservando el pedido previo. */
  #view-drop.active .copafem-print-page{break-before:auto!important;page-break-before:auto!important;break-after:page!important;page-break-after:always!important}
  #view-drop.active .copafem-print-page:last-child{break-after:auto!important;page-break-after:auto!important}
}
</style>
<script>
(() => {
  // Enter confirma un resultado y dispara el mismo guardado que al salir del campo.
  document.addEventListener('keydown',e=>{
    const t=e.target;
    if(e.key==='Enter' && t && t.matches && (t.matches('[data-zscore]')||t.matches('[data-bscore]'))){
      e.preventDefault();
      t.blur();
    }
  },true);

  // Auditoría liviana en ejecución: si falta un control crítico queda registrado
  // claramente en consola, sin interrumpir el torneo.
  const required=[
    'saveSettingsBtn','generateScheduleBtn','addBulkBtn','clearPairsBtn',
    'generateZonesBtn','regenerateZonesBtn','clearResultsBtn','rebuildBracketsBtn',
    'exportCsvBtn','exportJsonBtn','resetAllBtn','printBtn','dropExcelBtn',
    'dropPrintBtn','dropFitBtn','dropZoomOut','dropZoomIn'
  ];
  const audit=()=>{
    const missing=required.filter(id=>!document.getElementById(id));
    if(missing.length) console.error('COPAFEM · controles faltantes:',missing);
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',audit);else audit();
})();
</script>
'''

if '</body>' not in s:
    raise SystemExit('No se encontró </body>')
head,tail=s.rsplit('</body>',1)
s=head+injection+'\n</body>'+tail
p.write_text(s,encoding='utf-8')
print('COPAFEM final web audit patch OK')
