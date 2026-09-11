from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

MARKER = 'COPAFEM_DROP_SCHEDULE_V2'
if MARKER in s:
    print('real drop already applied')
    raise SystemExit

# Los BYE no son partidos: no deben ocupar horario/cancha ni mostrarse como cruces.
s = s.replace(
    'const by=(arr,r)=>arr.filter(m=>m.round===r);',
    'const by=(arr,r)=>arr.filter(m=>m.round===r && !m.bye);',
    1
)
# En el Drop, un BYE tampoco se dibuja como partido.
s = s.replace(
    '  function compactMatchHTML(m){\n',
    '  function compactMatchHTML(m){\n    if(m?.bye) return ``;\n',
    1
)

injection = r'''
<style id="COPAFEM_DROP_SCHEDULE_V2">
  .drop-match-head.copafem-drop-schedule{
    justify-content:center;
    align-items:center;
    text-align:center;
    font-size:8px;
    font-weight:950;
    letter-spacing:.02em;
    white-space:nowrap;
    min-height:18px;
  }
  .drop-match-head.copafem-drop-schedule span{width:100%;text-align:center}
  .drop-category-sheet.copafem-empty-event{display:none!important}
</style>
<script>
(() => {
  const norm=s=>String(s||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');

  function sheetCourts(sheet){
    const t=sheet.querySelector('.drop-block-title')?.textContent||'';
    const m=t.match(/Canchas\s+([0-9, ]+)/i);
    const parsed=m?m[1].split(',').map(x=>Number(x.trim())).filter(Number.isFinite):[];
    if(parsed.length)return parsed;
    const cat=(t.match(/·\s*(7ma|8va)\s*·/i)||[])[1]?.toLowerCase();
    return cat==='8va'?[2,4,6,8]:[1,3,5,7];
  }

  function roundName(text){
    const t=norm(text);
    if(t.includes('octavos'))return'octavos';
    if(t.includes('cuartos'))return'cuartos';
    if(t.includes('semi'))return'semifinal';
    if(t.includes('final'))return'final';
    return'';
  }

  function plan(cup,round,courts){
    const c=i=>courts[i%Math.max(courts.length,1)]??'—';
    if(cup==='gold'){
      if(round==='octavos')return Array.from({length:8},(_,i)=>({time:i<4?'13:00':'13:30',court:c(i)}));
      if(round==='cuartos')return Array.from({length:4},(_,i)=>({time:'14:00',court:c(i)}));
      if(round==='semifinal')return Array.from({length:2},(_,i)=>({time:'15:00',court:c(i)}));
      if(round==='final')return [{time:'15:30',court:c(0)}];
    }
    if(cup==='silver'){
      if(round==='cuartos')return Array.from({length:4},(_,i)=>({time:'14:30',court:c(i)}));
      if(round==='semifinal')return Array.from({length:2},(_,i)=>({time:'15:00',court:c(i+2)}));
      if(round==='final')return [{time:'15:30',court:c(1)}];
    }
    return [];
  }

  function normalizeHeader(match,slot){
    const head=match.querySelector('.drop-match-head');
    if(!head)return;
    const spans=[...head.querySelectorAll('span')];
    let raw=spans.length>1?spans[spans.length-1].textContent.trim():head.textContent.trim();
    raw=raw.replace(/\s*·\s*C(?:ancha\s*)?/i,' · Cancha ');
    const good=/\b\d{1,2}:\d{2}\b/.test(raw)&&/Cancha\s*\d+/i.test(raw);
    const value=good?raw:(slot?`${slot.time} · Cancha ${slot.court}`:(raw||'Horario a definir · Cancha —'));
    head.classList.add('copafem-drop-schedule');
    if(head.textContent.trim()!==value || head.children.length!==1){
      head.innerHTML='<span>'+value+'</span>';
    }
  }

  function isRealName(v){
    const t=String(v||'').trim();
    return !!t && t!=='—' && t!=='A definir';
  }

  function decorate(){
    document.querySelectorAll('.drop-category-sheet').forEach(sheet=>{
      // Listado: mostrar únicamente las parejas cargadas para esa fecha/categoría.
      let rosterCount=0;
      sheet.querySelectorAll('.drop-roster-row').forEach(row=>{
        const show=isRealName(row.querySelector('span')?.textContent);
        if(show)rosterCount++;
        if(row.style.display !== (show?'':'none')) row.style.display=show?'':'none';
      });
      sheet.classList.toggle('copafem-empty-event',rosterCount===0);
      if(!rosterCount)return;

      // Zonas: ocultar las que no tienen ninguna pareja inscripta.
      const zones=[...sheet.querySelectorAll('.drop-zone')];
      zones.forEach(zone=>{
        const real=[...zone.querySelectorAll('.drop-zone-pair span')].some(x=>isRealName(x.textContent));
        if(zone.style.display !== (real?'':'none')) zone.style.display=real?'':'none';
      });
      const visibleZones=zones.filter(z=>z.style.display!=='none').length;
      const zoneArea=sheet.querySelector('.drop-zones-area');
      if(zoneArea && visibleZones){
        const cols=Math.min(4,Math.max(1,visibleZones));
        zoneArea.style.gridTemplateColumns=`repeat(${cols},minmax(0,1fr))`;
      }

      const courts=sheetCourts(sheet);
      // Cruces: eliminar el cuadro genérico de relleno y dejar sólo partidos realmente creados.
      sheet.querySelectorAll('.drop-round-col').forEach(col=>{
        [...col.querySelectorAll(':scope > .drop-match')].forEach(m=>{
          if(!m.querySelector('.drop-match-head')) m.remove();
        });
        const matches=[...col.querySelectorAll(':scope > .drop-match')];
        const title=col.querySelector('.drop-round-title');
        if(matches.length===0){
          if(col.style.display!=='none')col.style.display='none';
          return;
        }
        if(col.style.display==='none')col.style.display='';
        const t=norm(title?.textContent||'');
        const cup=t.includes('plata')||title?.classList.contains('silver')?'silver':'gold';
        const slots=plan(cup,roundName(t),courts);
        matches.forEach((m,i)=>normalizeHeader(m,slots[i]));
      });

      // Ajustar ancho de Oro y Plata a la cantidad de rondas reales.
      const gold=sheet.querySelector('.drop-elims');
      if(gold){
        const cols=[...gold.querySelectorAll(':scope > .drop-round-col')].filter(c=>c.style.display!=='none').length;
        gold.style.display=cols?'grid':'none';
        if(cols)gold.style.gridTemplateColumns=`repeat(${cols},minmax(0,1fr))`;
      }
      const silver=sheet.querySelector('.drop-silver-area');
      if(silver){
        const cols=[...silver.querySelectorAll(':scope > .drop-round-col')].filter(c=>c.style.display!=='none').length;
        silver.style.display=cols?'grid':'none';
        if(cols)silver.style.gridTemplateColumns=`repeat(${cols},minmax(0,1fr))`;
      }
    });
  }

  let queued=false;
  const queue=()=>{
    if(queued)return;
    queued=true;
    requestAnimationFrame(()=>{queued=false;decorate();});
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',queue);else queue();
  new MutationObserver(queue).observe(document.documentElement,{subtree:true,childList:true});
  document.addEventListener('click',()=>setTimeout(queue,0),true);
})();
</script>
'''

if '</body>' not in s:
    raise SystemExit('No se encontró </body> en index.html')
head, tail = s.rsplit('</body>', 1)
s = head + injection + '\n</body>' + tail
p.write_text(s, encoding='utf-8')
print('COPAFEM real-only drop patch OK')
