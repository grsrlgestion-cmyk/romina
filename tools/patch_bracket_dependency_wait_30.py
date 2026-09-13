from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_BRACKET_DEPENDENCY_WAIT_30_V2'
if MARK in s:
    print('dependency wait v2 already applied')
    raise SystemExit

patch=r'''
<script id="COPAFEM_BRACKET_DEPENDENCY_WAIT_30_V2">
(() => {
  const WAIT=30;

  function targetDate(value){
    const d=String(value||'').trim();
    return d==='2026-09-13' || d==='13/09/2026';
  }

  function dateEntries(){
    const out=[];
    const seen=new Set();
    const add=(id,ev)=>{
      if(!ev || !targetDate(ev?.tournament?.date) || seen.has(ev)) return;
      seen.add(ev); out.push([id,ev]);
    };
    if(typeof eventsOnDate==='function'){
      try{ (eventsOnDate('2026-09-13')||[]).forEach(([id,ev])=>add(id,ev)); }catch(_e){}
      try{ (eventsOnDate('13/09/2026')||[]).forEach(([id,ev])=>add(id,ev)); }catch(_e){}
    }
    if(targetDate(state?.tournament?.date)) add((typeof store!=='undefined'&&store?.activeEventId)||'active',state);
    return out;
  }

  function bracketMatches(ev){
    return [...(ev?.brackets?.gold||[]),...(ev?.brackets?.silver||[])];
  }

  function allMatches(entries){
    const out=[];
    entries.forEach(([eventId,ev])=>{
      [...(ev?.zoneMatches||[]),...bracketMatches(ev)].forEach(m=>out.push({eventId,ev,m}));
    });
    return out;
  }

  function dependencyIds(m){
    const ids=[];
    [m?.source1,m?.source2].forEach(src=>{
      const hit=String(src||'').match(/^[WL]:(.+)$/);
      if(hit) ids.push(hit[1]);
    });
    return ids;
  }

  function overlaps(a0,a1,b0,b1){ return a0<b1 && b0<a1; }

  function durationOf(ev){
    const d=Number(ev?.tournament?.duration||30);
    return Number.isFinite(d)&&d>0?d:30;
  }

  function courtBusy(entries,childEv,child,candidate){
    if(child?.court==null) return false;
    const childDur=durationOf(childEv);
    const end=candidate+childDur;
    for(const rec of allMatches(entries)){
      const other=rec.m;
      if(other===child || other?.court==null || !other?.time) continue;
      if(Number(other.court)!==Number(child.court)) continue;
      const start=parseTime(other.time);
      if(!Number.isFinite(start)) continue;
      const otherEnd=start+durationOf(rec.ev);
      if(overlaps(candidate,end,start,otherEnd)) return true;
    }
    return false;
  }

  function enforceEvent(ev,entries){
    if(!ev || !targetDate(ev?.tournament?.date)) return false;
    const ms=bracketMatches(ev);
    const byId=new Map(ms.map(m=>[String(m.id),m]));
    let changed=false;

    // Si un partido espera ganador/perdedor de otro, debe comenzar al menos
    // 30 minutos después del horario de ese partido anterior.
    for(let pass=0;pass<20;pass++){
      let passChanged=false;
      for(const m of ms){
        if(!m?.time) continue;
        const parents=dependencyIds(m).map(id=>byId.get(String(id))).filter(Boolean);
        if(!parents.length) continue;
        const parentTimes=parents.map(x=>x?.time?parseTime(x.time):NaN).filter(Number.isFinite);
        if(!parentTimes.length) continue;

        const required=Math.max(...parentTimes)+WAIT;
        const current=parseTime(m.time);
        if(!Number.isFinite(current) || current>=required) continue;

        // No cambiar cancha. Si esa misma cancha está ocupada, avanzar de a
        // 30 minutos hasta que quede disponible.
        let candidate=required;
        let guard=0;
        while(courtBusy(entries,ev,m,candidate) && guard++<40) candidate+=WAIT;
        m.time=fmtTime(candidate);
        passChanged=true;
        changed=true;
      }
      if(!passChanged) break;
    }
    return changed;
  }

  function enforceAll(){
    const entries=dateEntries();
    let changed=false;
    entries.forEach(([,ev])=>{ if(enforceEvent(ev,entries)) changed=true; });
    return changed;
  }

  // Este parche se carga después del corrimiento 12:30 -> 13:00.
  if(typeof window.copafemScheduleDateNoConflicts==='function'){
    const original=window.copafemScheduleDateNoConflicts;
    window.copafemScheduleDateNoConflicts=function(){
      const ok=original.apply(this,arguments);
      if(!ok) return ok;
      enforceAll();
      return ok;
    };
    try{ copafemScheduleDateNoConflicts=window.copafemScheduleDateNoConflicts; }catch(_e){}
  }

  window.addEventListener('load',()=>setTimeout(()=>{
    try{
      if(enforceAll()){
        if(typeof saveState==='function') saveState();
        if(typeof renderAll==='function') renderAll();
      }
    }catch(err){console.error('COPAFEM dependency wait v2:',err);}
  },20));
})();
</script>
'''

if '</body>' not in s:
    raise SystemExit('No se encontró </body>')
head,tail=s.rsplit('</body>',1)
s=head+patch+'\n</body>'+tail
p.write_text(s,encoding='utf-8')
print('COPAFEM: cada cruce dependiente espera al menos 30 minutos sin cambiar cancha')
