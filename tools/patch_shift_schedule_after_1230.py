from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_SHIFT_2026_09_13_AFTER_1230_V3'
if MARK in s:
    print('shift after 12:30 v3 already applied')
    raise SystemExit

patch=r'''
<script id="COPAFEM_SHIFT_2026_09_13_AFTER_1230_V3">
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

  function hasExact1230(ev){
    return eventMatches(ev) && allMatches(ev).some(m=>String(m?.time||'')==='12:30');
  }

  function shiftAllFrom1230(ev){
    if(!hasExact1230(ev)) return false;
    let changed=false;
    allMatches(ev).forEach(m=>{
      if(!m?.time) return;
      const t=parseTime(m.time);
      if(Number.isFinite(t) && t>=FROM){
        m.time=fmtTime(t+SHIFT);
        changed=true;
      }
    });
    if(ev?.tournament) ev.tournament.copafemShiftAfter1230V3=true;
    return changed;
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

  function applyShift(){
    let changed=false;
    entriesForTargetDate().forEach(([,ev])=>{ if(shiftAllFrom1230(ev)) changed=true; });
    return changed;
  }

  // Si el cronograma se regenera y vuelve a aparecer 12:30, corregirlo nuevamente.
  // La condición "existe 12:30" hace que sea idempotente: una vez movido a 13:00
  // no vuelve a sumar otros 30 minutos.
  if(typeof window.copafemScheduleDateNoConflicts==='function'){
    const original=window.copafemScheduleDateNoConflicts;
    window.copafemScheduleDateNoConflicts=function(){
      const ok=original.apply(this,arguments);
      if(!ok) return ok;
      applyShift();
      return ok;
    };
    try{ copafemScheduleDateNoConflicts=window.copafemScheduleDateNoConflicts; }catch(_e){}
  }

  function tryApply(){
    try{
      if(applyShift()){
        if(typeof saveState==='function') saveState();
        if(typeof renderAll==='function') renderAll();
      }
    }catch(err){ console.error('COPAFEM shift 12:30 v3:',err); }
  }

  // Reintentos para cubrir el caso en que el estado guardado todavía no terminó
  // de cargarse cuando dispara el evento load.
  window.addEventListener('load',()=>{
    [50,250,750,1500,3000].forEach(ms=>setTimeout(tryApply,ms));
  });
})();
</script>
'''

if '</body>' not in s:
    raise SystemExit('No se encontró </body>')
head,tail=s.rsplit('</body>',1)
s=head+patch+'\n</body>'+tail
p.write_text(s,encoding='utf-8')
print('COPAFEM: corrimiento reforzado 12:30 -> 13:00 y posteriores +30 min')
