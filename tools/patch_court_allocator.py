from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

MARKER = 'COPAFEM_COURT_ALLOCATOR_V1'
if MARKER in s:
    print('court allocator already applied')
    raise SystemExit

helpers = r'''
  // COPAFEM_COURT_ALLOCATOR_V1
  // Programa toda la fecha usando todas las canchas configuradas y evitando superposiciones.
  function copafemUniqueCourts(event){
    return [...new Set((event?.tournament?.courts||[]).map(Number).filter(n=>Number.isFinite(n)&&n>0))];
  }

  function copafemDuration(event){
    return Math.max(1,Number(event?.tournament?.duration||30));
  }

  function copafemRealMatch(m){
    return !!m && !m.bye;
  }

  function copafemRoundOrder(name){
    return ({'Octavos':1,'Cuartos':2,'Semifinal':3,'Final':4})[name]||99;
  }

  function copafemEventBatches(event){
    const batches=[];
    const zoneMatches=(event.zoneMatches||[]).filter(copafemRealMatch);
    if(zoneMatches.length){
      const zoneRounds=[...new Set(zoneMatches.map(m=>Number(m.zoneRound||((String(m.id).match(/-(\d+)(?:-\d+)?$/)||[])[1])||1)))].sort((a,b)=>a-b);
      zoneRounds.forEach(r=>{
        const ms=zoneMatches.filter(m=>Number(m.zoneRound||((String(m.id).match(/-(\d+)(?:-\d+)?$/)||[])[1])||1)===r)
          .sort((a,b)=>ZONES.indexOf(a.zone)-ZONES.indexOf(b.zone)||String(a.id).localeCompare(String(b.id)));
        if(ms.length)batches.push({stage:'Zona '+r,matches:ms});
      });
    }

    const gold=(event.brackets?.gold||[]).filter(copafemRealMatch);
    const silver=(event.brackets?.silver||[]).filter(copafemRealMatch);
    const rounds=[...new Set([...gold,...silver].map(m=>m.round))].sort((a,b)=>copafemRoundOrder(a)-copafemRoundOrder(b));
    rounds.forEach(round=>{
      const g=gold.filter(m=>m.round===round);
      const pl=silver.filter(m=>m.round===round);
      // Octavos/Cuartos se respetan por copa; semis y finales pueden compartir turno/canchas libres.
      if(round==='Semifinal' || round==='Final'){
        const ms=[...g,...pl];
        if(ms.length)batches.push({stage:round,matches:ms});
      }else{
        if(g.length)batches.push({stage:'Oro '+round,matches:g});
        if(pl.length)batches.push({stage:'Plata '+round,matches:pl});
      }
    });
    return batches;
  }

  function copafemOverlaps(a0,a1,b0,b1){ return a0 < b1 && b0 < a1; }

  function copafemCourtFree(occupied,court,start,dur){
    const end=start+dur;
    return !(occupied.get(court)||[]).some(x=>copafemOverlaps(start,end,x.start,x.end));
  }

  function copafemReserve(occupied,court,start,dur,eventId,match){
    if(!occupied.has(court))occupied.set(court,[]);
    occupied.get(court).push({start,end:start+dur,eventId,match});
    occupied.get(court).sort((a,b)=>a.start-b.start);
  }

  function copafemNextCourtTime(occupied,court,start,dur){
    let t=start;
    const xs=occupied.get(court)||[];
    let changed=true;
    while(changed){
      changed=false;
      for(const x of xs){
        if(copafemOverlaps(t,t+dur,x.start,x.end)){
          t=x.end;
          changed=true;
          break;
        }
      }
    }
    return t;
  }

  function copafemScheduleBatch(batch,event,eventId,readyAt,occupied){
    const courts=copafemUniqueCourts(event);
    if(!courts.length)return readyAt;
    const dur=copafemDuration(event);
    const pending=[...batch.matches];
    let cursor=readyAt;
    let latestEnd=readyAt;

    while(pending.length){
      const nextTimes=courts.map(c=>copafemNextCourtTime(occupied,c,cursor,dur));
      const t=Math.min(...nextTimes);
      const free=courts.filter(c=>copafemCourtFree(occupied,c,t,dur));
      if(!free.length){ cursor=t+1; continue; }

      // En cada turno ocupa todas las canchas libres antes de avanzar de horario.
      for(const court of free){
        if(!pending.length)break;
        const m=pending.shift();
        m.time=fmtTime(t);
        m.court=court;
        copafemReserve(occupied,court,t,dur,eventId,m);
        latestEnd=Math.max(latestEnd,t+dur);
      }
      cursor=t;
    }
    return latestEnd;
  }

  function copafemScheduleDateNoConflicts(){
    const date=state?.tournament?.date;
    if(!date)return false;
    const entries=eventsOnDate(date).filter(([,e])=>e && (e.zoneMatches||[]).length);
    if(!entries.length)return false;

    // Limpiamos horarios para recalcular la fecha completa de forma coherente.
    entries.forEach(([,e])=>{
      (e.zoneMatches||[]).forEach(m=>{m.time=null;m.court=null;});
      (e.brackets?.gold||[]).forEach(m=>{m.time=null;m.court=null;});
      (e.brackets?.silver||[]).forEach(m=>{m.time=null;m.court=null;});
    });

    const occupied=new Map();
    const queues=entries.map(([id,e])=>({
      id,event:e,batches:copafemEventBatches(e),index:0,
      readyAt:parseTime(e.tournament.startTime||'10:00'),
      categoryIndex:CATEGORIES.indexOf(e.tournament.category)
    })).filter(x=>x.batches.length && copafemUniqueCourts(x.event).length);

    // List scheduling: siempre toma primero la próxima etapa que esté lista.
    while(queues.some(q=>q.index<q.batches.length)){
      const ready=queues.filter(q=>q.index<q.batches.length)
        .sort((a,b)=>a.readyAt-b.readyAt || a.categoryIndex-b.categoryIndex || a.id.localeCompare(b.id));
      const q=ready[0];
      const batch=q.batches[q.index++];
      q.readyAt=copafemScheduleBatch(batch,q.event,q.id,q.readyAt,occupied);
    }
    return true;
  }
'''

marker = '  function generateSchedule(requireZones=true){'
if marker not in s:
    raise SystemExit('No se encontró generateSchedule')
s = s.replace(marker, helpers + '\n' + marker, 1)

# El generador normal pasa a usar el planificador global de la fecha.
s = s.replace(
    '  function generateSchedule(requireZones=true){\n    if(dynMode()) return generateScheduleDynamic();',
    '  function generateSchedule(requireZones=true){\n    if(requireZones && !state.zoneMatches.length) return toast("Primero generá las zonas");\n    return copafemScheduleDateNoConflicts();\n    if(dynMode()) return generateScheduleDynamic();',
    1
)

# El generador dinámico (6 a 23 parejas) usa exactamente la misma lógica.
s = s.replace(
    '  function generateScheduleDynamic(){\n    if(!state.zoneMatches.length)return;',
    '  function generateScheduleDynamic(){\n    if(!state.zoneMatches.length)return;\n    return copafemScheduleDateNoConflicts();',
    1
)

# Cada vez que cambian los clasificados/reconstruyen copas, se vuelve a equilibrar toda la fecha.
s = s.replace(
    '  function scheduleBrackets(){\n    const gold=state.brackets.gold||[], silver=state.brackets.silver||[];',
    '  function scheduleBrackets(){\n    return copafemScheduleDateNoConflicts();\n    const gold=state.brackets.gold||[], silver=state.brackets.silver||[];',
    1
)

p.write_text(s,encoding='utf-8')
print('COPAFEM court allocator patch OK')
