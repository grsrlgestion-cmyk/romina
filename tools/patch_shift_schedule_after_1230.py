from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_SHIFT_2026_09_13_AFTER_1230_V2'
if MARK in s:
    print('shift after 12:30 v2 already applied')
    raise SystemExit

patch=r'''
<script id="COPAFEM_SHIFT_2026_09_13_AFTER_1230_V2">
(() => {
  const FROM=parseTime('12:30');
  const SHIFT=30;

  function targetDate(value){
    const d=String(value||'').trim();
    return d==='2026-09-13' || d==='13/09/2026';
  }

  function eventMatches(ev){
    return !!ev && targetDate(ev?.tournament?.date);
  }

  function allMatches(ev){
    return [...(ev?.zoneMatches||[]),...(ev?.brackets?.gold||[]),...(ev?.brackets?.silver||[])];
  }

  function shiftAllFrom1230(ev){
    if(!eventMatches(ev)) return false;
    let changed=false;
    allMatches(ev).forEach(m=>{
      if(!m?.time) return;
      const t=parseTime(m.time);
      if(Number.isFinite(t) && t>=FROM){
        m.time=fmtTime(t+SHIFT);
        changed=true;
      }
    });
    return changed;
  }

  function hasExact1230(ev){
    return allMatches(ev).some(m=>String(m?.time||'')==='12:30');
  }

  function entriesForTargetDate(){
    const out=[];
    const seen=new Set();
    const add=(id,ev)=>{
      if(!eventMatches(ev) || seen.has(ev)) return;
      seen.add(ev); out.push([id,ev]);
    };
    if(typeof eventsOnDate==='function'){
      try{ (eventsOnDate('2026-09-13')||[]).forEach(([id,ev])=>add(id,ev)); }catch(_e){}
      try{ (eventsOnDate('13/09/2026')||[]).forEach(([id,ev])=>add(id,ev)); }catch(_e){}
    }
    if(eventMatches(state)) add((typeof store!=='undefined'&&store?.activeEventId)||'active',state);
    return out;
  }

  function correctSavedScheduleOnce(){
    let changed=false;
    for(const [,ev] of entriesForTargetDate()){
      if(ev?.tournament?.copafemShiftAfter1230V2) continue;

      // Si todavía existe al menos un partido a las 12:30, el corrimiento
      // anterior no quedó reflejado en el cronograma guardado: aplicarlo ahora.
      // Si la versión anterior nunca se ejecutó, aplicarlo también.
      const oldMarked=!!ev?.tournament?.copafemShiftAfter1230V1;
      if(hasExact1230(ev) || !oldMarked){
        if(shiftAllFrom1230(ev)) changed=true;
      }
      if(ev?.tournament) ev.tournament.copafemShiftAfter1230V2=true;
    }
    return changed;
  }

  // Cada vez que se recomponga el cronograma del 13/09, volver a aplicar
  // exactamente +30 min desde 12:30 sobre el cronograma recién generado.
  if(typeof window.copafemScheduleDateNoConflicts==='function'){
    const original=window.copafemScheduleDateNoConflicts;
    window.copafemScheduleDateNoConflicts=function(){
      const ok=original.apply(this,arguments);
      if(!ok) return ok;
      entriesForTargetDate().forEach(([,ev])=>shiftAllFrom1230(ev));
      return ok;
    };
    try{ copafemScheduleDateNoConflicts=window.copafemScheduleDateNoConflicts; }catch(_e){}
  }

  window.addEventListener('load',()=>setTimeout(()=>{
    try{
      const changed=correctSavedScheduleOnce();
      if(typeof saveState==='function') saveState();
      if(changed && typeof renderAll==='function') renderAll();
    }catch(err){ console.error('COPAFEM shift 12:30 v2:',err); }
  },0));
})();
</script>
'''

if '</body>' not in s:
    raise SystemExit('No se encontró </body>')
head,tail=s.rsplit('</body>',1)
s=head+patch+'\n</body>'+tail
p.write_text(s,encoding='utf-8')
print('COPAFEM: 12:30 pasa a 13:00 y todos los horarios posteriores avanzan 30 minutos')
