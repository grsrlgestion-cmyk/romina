from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_SHIFT_2026_09_13_AFTER_1230_V1'
if MARK in s:
    print('shift after 12:30 already applied')
    raise SystemExit

patch=r'''
<script id="COPAFEM_SHIFT_2026_09_13_AFTER_1230_V1">
(() => {
  const TARGET_DATE='2026-09-13';
  const FROM=parseTime('12:30');
  const SHIFT=30;

  function shiftEventTimes(ev){
    if(!ev || String(ev?.tournament?.date||'')!==TARGET_DATE) return false;
    let changed=false;
    const all=[...(ev.zoneMatches||[]),...(ev.brackets?.gold||[]),...(ev.brackets?.silver||[])];
    all.forEach(m=>{
      if(!m?.time) return;
      const t=parseTime(m.time);
      if(Number.isFinite(t) && t>=FROM){
        m.time=fmtTime(t+SHIFT);
        changed=true;
      }
    });
    return changed;
  }

  function shiftCurrentDateOnce(){
    let changed=false;
    const entries=(typeof eventsOnDate==='function')?eventsOnDate(TARGET_DATE):[];
    entries.forEach(([,ev])=>{
      if(ev?.tournament?.copafemShiftAfter1230V1) return;
      if(shiftEventTimes(ev)) changed=true;
      if(ev?.tournament) ev.tournament.copafemShiftAfter1230V1=true;
    });
    if(String(state?.tournament?.date||'')===TARGET_DATE && !state.tournament?.copafemShiftAfter1230V1){
      if(shiftEventTimes(state)) changed=true;
      state.tournament.copafemShiftAfter1230V1=true;
    }
    return changed;
  }

  // Cada vez que el sistema recompone el cronograma, aplicar el corrimiento
  // una sola vez sobre el cronograma recién generado. No cambia canchas ni cruces.
  if(typeof window.copafemScheduleDateNoConflicts==='function'){
    const original=window.copafemScheduleDateNoConflicts;
    window.copafemScheduleDateNoConflicts=function(){
      const ok=original.apply(this,arguments);
      if(!ok) return ok;
      const entries=(typeof eventsOnDate==='function')?eventsOnDate(TARGET_DATE):[];
      entries.forEach(([,ev])=>shiftEventTimes(ev));
      if(String(state?.tournament?.date||'')===TARGET_DATE && !entries.some(([,ev])=>ev===state)) shiftEventTimes(state);
      return ok;
    };
    // Las funciones existentes llaman al identificador global; actualizarlo también.
    try{ copafemScheduleDateNoConflicts=window.copafemScheduleDateNoConflicts; }catch(_e){}
  }

  // Corregir también los horarios ya guardados en el navegador al abrir esta versión.
  window.addEventListener('load',()=>setTimeout(()=>{
    try{
      if(shiftCurrentDateOnce()){
        if(typeof saveState==='function') saveState();
        if(typeof renderAll==='function') renderAll();
      }else if(typeof saveState==='function'){
        // Guarda la marca para no volver a desplazar horarios ya corregidos.
        saveState();
      }
    }catch(err){console.error('COPAFEM shift 12:30:',err);}
  },0));
})();
</script>
'''

if '</body>' not in s:
    raise SystemExit('No se encontró </body>')
head,tail=s.rsplit('</body>',1)
s=head+patch+'\n</body>'+tail
p.write_text(s,encoding='utf-8')
print('COPAFEM: partidos del 13/09/2026 desde 12:30 desplazados 30 minutos sin cambiar canchas')
