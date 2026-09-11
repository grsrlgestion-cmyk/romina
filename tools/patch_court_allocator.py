from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

MARKER = 'COPAFEM_COURT_ALLOCATOR_V2'
if MARKER in s:
    print('court allocator v2 already applied')
    raise SystemExit

helpers = r'''
  // COPAFEM_COURT_ALLOCATOR_V2
  // Compacta los partidos para no dejar canchas libres mientras exista un partido compatible por jugar.
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

  function copafemOverlaps(a0,a1,b0,b1){
    return a0 < b1 && b0 < a1;
  }

  function copafemCourtFree(occupied,court,start,dur){
    const end=start+dur;
    return !(occupied.get(court)||[]).some(x=>copafemOverlaps(start,end,x.start,x.end));
  }

  function copafemReserve(occupied,court,start,dur,eventId,match){
    if(!occupied.has(court)) occupied.set(court,[]);
    occupied.get(court).push({start,end:start+dur,eventId,match});
    occupied.get(court).sort((a,b)=>a.start-b.start);
  }

  function copafemNextCourtTime(occupied,court,start,dur){
    let t=start;
    const xs=occupied.get(court)||[];
    let guard=0;
    while(guard++<500){
      const conflict=xs.find(x=>copafemOverlaps(t,t+dur,x.start,x.end));
      if(!conflict) return t;
      t=conflict.end;
    }
    return t;
  }

  function copafemZoneSort(a,b){
    const za=ZONES.indexOf(a.zone), zb=ZONES.indexOf(b.zone);
    const ra=Number(a.zoneRound||1), rb=Number(b.zoneRound||1);
    return ra-rb || za-zb || String(a.id).localeCompare(String(b.id));
  }

  function copafemPickPlayableZoneMatches(pending,limit){
    if(limit<=0 || !pending.length) return [];
    const selected=[];
    const usedPlayers=new Set();

    // Primera pasada: reparte entre zonas para que todas avancen y llena canchas.
    const ordered=[...pending].sort(copafemZoneSort);
    const usedZones=new Set();
    for(const m of ordered){
      if(selected.length>=limit) break;
      if(usedZones.has(m.zone)) continue;
      const p1=String(m.p1||''), p2=String(m.p2||'');
      if((p1&&usedPlayers.has(p1)) || (p2&&usedPlayers.has(p2))) continue;
      selected.push(m); usedZones.add(m.zone);
      if(p1) usedPlayers.add(p1); if(p2) usedPlayers.add(p2);
    }

    // Segunda pasada: si quedan canchas libres, permite un segundo partido de una zona
    // solo cuando las parejas no se repiten (útil en zonas de 4).
    if(selected.length<limit){
      for(const m of ordered){
        if(selected.length>=limit) break;
        if(selected.includes(m)) continue;
        const p1=String(m.p1||''), p2=String(m.p2||'');
        if((p1&&usedPlayers.has(p1)) || (p2&&usedPlayers.has(p2))) continue;
        selected.push(m);
        if(p1) usedPlayers.add(p1); if(p2) usedPlayers.add(p2);
      }
    }
    return selected;
  }

  function copafemScheduleZonesEvent(event,eventId,occupied){
    const courts=copafemUniqueCourts(event);
    const dur=copafemDuration(event);
    const pending=(event.zoneMatches||[]).filter(copafemRealMatch).sort(copafemZoneSort);
    if(!courts.length || !pending.length) return parseTime(event?.tournament?.startTime||'10:00');

    let cursor=parseTime(event?.tournament?.startTime||'10:00');
    let latestEnd=cursor;
    let guard=0;

    while(pending.length && guard++<2000){
      const nextTimes=courts.map(c=>copafemNextCourtTime(occupied,c,cursor,dur));
      const t=Math.min(...nextTimes);
      const freeCourts=courts.filter(c=>copafemCourtFree(occupied,c,t,dur));
      if(!freeCourts.length){ cursor=t+1; continue; }

      const playable=copafemPickPlayableZoneMatches(pending,freeCourts.length);
      if(!playable.length){ cursor=t+dur; continue; }

      playable.forEach((m,i)=>{
        const court=freeCourts[i];
        m.time=fmtTime(t);
        m.court=court;
        copafemReserve(occupied,court,t,dur,eventId,m);
        const pos=pending.indexOf(m);
        if(pos>=0) pending.splice(pos,1);
        latestEnd=Math.max(latestEnd,t+dur);
      });

      // No pasa de horario hasta haber agotado todas las canchas utilizables de este turno.
      cursor=t;
    }
    return latestEnd;
  }

  function copafemBracketBatches(event){
    const batches=[];
    const gold=(event.brackets?.gold||[]).filter(copafemRealMatch);
    const silver=(event.brackets?.silver||[]).filter(copafemRealMatch);
    const rounds=[...new Set([...gold,...silver].map(m=>m.round))].sort((a,b)=>copafemRoundOrder(a)-copafemRoundOrder(b));
    rounds.forEach(round=>{
      const g=gold.filter(m=>m.round===round);
      const pl=silver.filter(m=>m.round===round);
      if(round==='Semifinal' || round==='Final'){
        const ms=[...g,...pl];
        if(ms.length) batches.push({stage:round,matches:ms});
      }else{
        if(g.length) batches.push({stage:'Oro '+round,matches:g});
        if(pl.length) batches.push({stage:'Plata '+round,matches:pl});
      }
    });
    return batches;
  }

  function copafemScheduleBracketBatch(batch,event,eventId,readyAt,occupied){
    const courts=copafemUniqueCourts(event);
    const dur=copafemDuration(event);
    const pending=[...batch.matches].filter(copafemRealMatch);
    if(!courts.length || !pending.length) return readyAt;
    let cursor=readyAt, latestEnd=readyAt, guard=0;

    while(pending.length && guard++<1000){
      const nextTimes=courts.map(c=>copafemNextCourtTime(occupied,c,cursor,dur));
      const t=Math.min(...nextTimes);
      const freeCourts=courts.filter(c=>copafemCourtFree(occupied,c,t,dur));
      if(!freeCourts.length){ cursor=t+1; continue; }
      for(const court of freeCourts){
        if(!pending.length) break;
        const m=pending.shift();
        m.time=fmtTime(t); m.court=court;
        copafemReserve(occupied,court,t,dur,eventId,m);
        latestEnd=Math.max(latestEnd,t+dur);
      }
      cursor=t;
    }
    return latestEnd;
  }

  function copafemScheduleDateNoConflicts(){
    const date=state?.tournament?.date;
    if(!date) return false;
    const entries=eventsOnDate(date).filter(([,e])=>e && (e.zoneMatches||[]).length);
    if(!entries.length) return false;

    // Recalcula completa la fecha para que ningún horario viejo reserve una cancha innecesariamente.
    entries.forEach(([,e])=>{
      (e.zoneMatches||[]).forEach(m=>{m.time=null;m.court=null;});
      (e.brackets?.gold||[]).forEach(m=>{m.time=null;m.court=null;});
      (e.brackets?.silver||[]).forEach(m=>{m.time=null;m.court=null;});
    });

    const occupied=new Map();
    const zoneEnds=new Map();

    // Primero compacta todas las zonas. Cada categoría usa todas sus canchas posibles.
    const zoneOrder=[...entries].sort((a,b)=>
      parseTime(a[1].tournament.startTime||'10:00')-parseTime(b[1].tournament.startTime||'10:00') ||
      CATEGORIES.indexOf(a[1].tournament.category)-CATEGORIES.indexOf(b[1].tournament.category)
    );
    zoneOrder.forEach(([id,e])=>{
      zoneEnds.set(id,copafemScheduleZonesEvent(e,id,occupied));
    });

    // Después programa las copas, respetando que cada categoría termine primero sus zonas.
    const queues=entries.map(([id,e])=>({
      id,event:e,batches:copafemBracketBatches(e),index:0,
      readyAt:zoneEnds.get(id)??parseTime(e.tournament.startTime||'10:00'),
      categoryIndex:CATEGORIES.indexOf(e.tournament.category)
    })).filter(q=>q.batches.length && copafemUniqueCourts(q.event).length);

    while(queues.some(q=>q.index<q.batches.length)){
      const ready=queues.filter(q=>q.index<q.batches.length)
        .sort((a,b)=>a.readyAt-b.readyAt || a.categoryIndex-b.categoryIndex || a.id.localeCompare(b.id));
      const q=ready[0];
      q.readyAt=copafemScheduleBracketBatch(q.batches[q.index++],q.event,q.id,q.readyAt,occupied);
    }
    return true;
  }
'''

marker = '  function generateSchedule(requireZones=true){'
if marker not in s:
    raise SystemExit('No se encontró generateSchedule')
s = s.replace(marker, helpers + '\n' + marker, 1)

s = s.replace(
    '  function generateSchedule(requireZones=true){\n    if(dynMode()) return generateScheduleDynamic();',
    '  function generateSchedule(requireZones=true){\n    if(requireZones && !state.zoneMatches.length) return toast("Primero generá las zonas");\n    return copafemScheduleDateNoConflicts();\n    if(dynMode()) return generateScheduleDynamic();',
    1
)

s = s.replace(
    '  function generateScheduleDynamic(){\n    if(!state.zoneMatches.length)return;',
    '  function generateScheduleDynamic(){\n    if(!state.zoneMatches.length)return;\n    return copafemScheduleDateNoConflicts();',
    1
)

s = s.replace(
    '  function scheduleBrackets(){\n    const gold=state.brackets.gold||[], silver=state.brackets.silver||[];',
    '  function scheduleBrackets(){\n    return copafemScheduleDateNoConflicts();\n    const gold=state.brackets.gold||[], silver=state.brackets.silver||[];',
    1
)

p.write_text(s,encoding='utf-8')
print('COPAFEM court allocator v2 patch OK')
