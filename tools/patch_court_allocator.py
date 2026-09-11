from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

MARKER = 'COPAFEM_COURT_ALLOCATOR_V4'
if MARKER in s:
    print('court allocator v4 already applied')
    raise SystemExit

helpers = r'''
  // COPAFEM_COURT_ALLOCATOR_V4
  // Reglas obligatorias:
  // 1) una cancha nunca recibe dos partidos superpuestos;
  // 2) una pareja nunca juega dos partidos en el mismo horario;
  // 3) se usan todas las canchas posibles antes de extender el cronograma;
  // 4) funciona aunque la fecha esté vacía ("Sin fecha").

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

  function copafemZoneRound(m){
    const direct=Number(m?.zoneRound);
    if(Number.isFinite(direct)&&direct>0) return direct;
    const hit=String(m?.id||'').match(/-(\d+)(?:-\d+)?$/);
    return hit ? Number(hit[1]) : 1;
  }

  function copafemOverlaps(a0,a1,b0,b1){
    return a0 < b1 && b0 < a1;
  }

  function copafemCourtFree(occupied,court,start,dur){
    const end=start+dur;
    return !(occupied.get(court)||[]).some(x=>copafemOverlaps(start,end,x.start,x.end));
  }

  function copafemFreeCourts(event,occupied,start){
    const dur=copafemDuration(event);
    return copafemUniqueCourts(event).filter(c=>copafemCourtFree(occupied,c,start,dur));
  }

  function copafemReserve(occupied,court,start,dur,eventId,match){
    if(!occupied.has(court)) occupied.set(court,[]);
    occupied.get(court).push({start,end:start+dur,eventId,match});
    occupied.get(court).sort((a,b)=>a.start-b.start);
  }

  function copafemZoneGroups(event){
    const map=new Map();
    (event.zoneMatches||[]).filter(copafemRealMatch).forEach(m=>{
      const zone=String(m.zone||'');
      const round=copafemZoneRound(m);
      const key=zone+'|'+round;
      if(!map.has(key)) map.set(key,{key,zone,round,matches:[]});
      map.get(key).matches.push(m);
    });
    return [...map.values()].map(g=>({...g,size:g.matches.length})).sort((a,b)=>
      a.round-b.round || b.size-a.size || ZONES.indexOf(a.zone)-ZONES.indexOf(b.zone) || a.key.localeCompare(b.key)
    );
  }

  function copafemGroupPlayers(group){
    const ids=[];
    group.matches.forEach(m=>{
      if(m.p1) ids.push(String(m.p1));
      if(m.p2) ids.push(String(m.p2));
    });
    return ids;
  }

  function copafemGroupInternallyValid(group){
    const ids=copafemGroupPlayers(group);
    return new Set(ids).size===ids.length;
  }

  function copafemTryPackGroups(groups,capacities){
    const H=capacities.length;
    const used=Array(H).fill(0);
    const zones=Array.from({length:H},()=>new Set());
    const slotGroups=Array.from({length:H},()=>[]);
    const assigned=new Map();
    const ordered=[...groups].sort((a,b)=>
      a.round-b.round || b.size-a.size || ZONES.indexOf(a.zone)-ZONES.indexOf(b.zone) || a.key.localeCompare(b.key)
    );

    const prevAssignedSlot=(g)=>{
      let p=-1;
      for(const other of ordered){
        if(other.zone!==g.zone || other.round>=g.round) continue;
        const s=assigned.get(other.key);
        if(Number.isInteger(s)) p=Math.max(p,s);
      }
      return p;
    };

    function dfs(i){
      if(i>=ordered.length) return true;
      const g=ordered[i];
      const minSlot=prevAssignedSlot(g)+1;
      const candidates=[];
      for(let s=minSlot;s<H;s++){
        if(zones[s].has(g.zone)) continue;
        if(used[s]+g.size>capacities[s]) continue;
        candidates.push(s);
      }
      // Prefiere el horario más temprano; dentro del mismo horizonte esto compacta el torneo.
      candidates.sort((a,b)=>a-b || used[b]-used[a]);

      for(const s of candidates){
        used[s]+=g.size;
        zones[s].add(g.zone);
        slotGroups[s].push(g);
        assigned.set(g.key,s);
        if(dfs(i+1)) return true;
        assigned.delete(g.key);
        slotGroups[s].pop();
        zones[s].delete(g.zone);
        used[s]-=g.size;
      }
      return false;
    }

    return dfs(0) ? {slotGroups,used} : null;
  }

  function copafemPackZoneGroups(event,occupied){
    const groups=copafemZoneGroups(event);
    if(!groups.length) return null;
    if(groups.some(g=>!copafemGroupInternallyValid(g))) return null;

    const courts=copafemUniqueCourts(event);
    if(!courts.length) return null;
    const dur=copafemDuration(event);
    const base=parseTime(event?.tournament?.startTime||'10:00');
    const total=groups.reduce((a,g)=>a+g.size,0);
    const roundsByZone=new Map();
    groups.forEach(g=>roundsByZone.set(g.zone,(roundsByZone.get(g.zone)||0)+1));
    const minRounds=Math.max(...roundsByZone.values(),1);
    const absoluteMin=Math.max(minRounds,Math.ceil(total/courts.length));
    const maxH=Math.max(absoluteMin,groups.length+8);

    for(let H=absoluteMin;H<=maxH;H++){
      const capacities=[];
      for(let k=0;k<H;k++) capacities.push(copafemFreeCourts(event,occupied,base+k*dur).length);
      if(capacities.reduce((a,b)=>a+b,0)<total) continue;
      const packed=copafemTryPackGroups(groups,capacities);
      if(packed) return {base,dur,groups,capacities,...packed};
    }
    return null;
  }

  function copafemScheduleZonesEvent(event,eventId,occupied){
    const packed=copafemPackZoneGroups(event,occupied);
    const base=parseTime(event?.tournament?.startTime||'10:00');
    const dur=copafemDuration(event);
    if(!packed){
      // Respaldo seguro: programa grupo por grupo, nunca dos partidos de la misma pareja simultáneamente.
      let cursor=base;
      for(const group of copafemZoneGroups(event)){
        let placed=false,guard=0;
        while(!placed && guard++<1000){
          const free=copafemFreeCourts(event,occupied,cursor);
          if(free.length>=group.size){
            group.matches.forEach((m,i)=>{
              m.time=fmtTime(cursor); m.court=free[i];
              copafemReserve(occupied,free[i],cursor,dur,eventId,m);
            });
            placed=true;
          }else cursor+=dur;
        }
        cursor+=dur;
      }
      return cursor;
    }

    let latestEnd=base;
    packed.slotGroups.forEach((groups,slot)=>{
      if(!groups.length) return;
      const t=packed.base+slot*packed.dur;
      const free=copafemFreeCourts(event,occupied,t);
      let ci=0;
      for(const group of groups){
        for(const m of group.matches){
          const court=free[ci++];
          if(court==null) continue;
          m.time=fmtTime(t);
          m.court=court;
          copafemReserve(occupied,court,t,packed.dur,eventId,m);
          latestEnd=Math.max(latestEnd,t+packed.dur);
        }
      }
    });
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

  function copafemMatchPlayers(m){
    return [m?.p1,m?.p2].filter(Boolean).map(String);
  }

  function copafemPickBracketMatches(pending,limit){
    const selected=[];
    const usedPlayers=new Set();
    for(const m of pending){
      if(selected.length>=limit) break;
      const ps=copafemMatchPlayers(m);
      if(ps.some(p=>usedPlayers.has(p))) continue;
      selected.push(m);
      ps.forEach(p=>usedPlayers.add(p));
    }
    return selected;
  }

  function copafemScheduleBracketBatch(batch,event,eventId,readyAt,occupied){
    const dur=copafemDuration(event);
    const pending=[...batch.matches].filter(copafemRealMatch);
    if(!pending.length) return readyAt;
    let cursor=readyAt,latestEnd=readyAt,guard=0;

    while(pending.length && guard++<2000){
      const free=copafemFreeCourts(event,occupied,cursor);
      if(!free.length){ cursor+=dur; continue; }
      const playable=copafemPickBracketMatches(pending,free.length);
      if(!playable.length){ cursor+=dur; continue; }
      playable.forEach((m,i)=>{
        const court=free[i];
        m.time=fmtTime(cursor); m.court=court;
        copafemReserve(occupied,court,cursor,dur,eventId,m);
        const pos=pending.indexOf(m);
        if(pos>=0) pending.splice(pos,1);
        latestEnd=Math.max(latestEnd,cursor+dur);
      });
      cursor+=dur;
    }
    return latestEnd;
  }

  function copafemValidateSchedule(entries){
    const errors=[];
    const courtSeen=new Map();
    for(const [eventId,event] of entries){
      const all=[...(event.zoneMatches||[]),...(event.brackets?.gold||[]),...(event.brackets?.silver||[])].filter(copafemRealMatch);
      const pairSeen=new Map();
      for(const m of all){
        if(!m.time || m.court==null) continue;
        const ck=String(m.time)+'|'+String(m.court);
        if(courtSeen.has(ck)) errors.push('Cancha '+m.court+' repetida a las '+m.time);
        courtSeen.set(ck,eventId+'|'+String(m.id));
        for(const p of copafemMatchPlayers(m)){
          const pk=String(m.time)+'|'+p;
          if(pairSeen.has(pk)) errors.push('Pareja repetida a las '+m.time);
          pairSeen.set(pk,String(m.id));
        }
      }
    }
    return errors;
  }

  function copafemScheduleDateNoConflicts(){
    const date=String(state?.tournament?.date||'');
    let entries=eventsOnDate(date).filter(([,e])=>e && (e.zoneMatches||[]).length);
    if(!entries.length && state && (state.zoneMatches||[]).length){
      entries=[[store.activeEventId||'active',state]];
    }
    if(!entries.length) return false;

    entries.forEach(([,e])=>{
      (e.zoneMatches||[]).forEach(m=>{m.time=null;m.court=null;});
      (e.brackets?.gold||[]).forEach(m=>{m.time=null;m.court=null;});
      (e.brackets?.silver||[]).forEach(m=>{m.time=null;m.court=null;});
    });

    const occupied=new Map();
    const zoneEnds=new Map();
    const zoneOrder=[...entries].sort((a,b)=>
      parseTime(a[1].tournament.startTime||'10:00')-parseTime(b[1].tournament.startTime||'10:00') ||
      CATEGORIES.indexOf(a[1].tournament.category)-CATEGORIES.indexOf(b[1].tournament.category)
    );

    zoneOrder.forEach(([id,e])=>{
      zoneEnds.set(id,copafemScheduleZonesEvent(e,id,occupied));
    });

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

    const errors=copafemValidateSchedule(entries);
    if(errors.length){
      console.error('COPAFEM schedule validation',errors);
      toast('No se guardaron horarios: se detectó una superposición');
      return false;
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
    '  function generateSchedule(requireZones=true){\n    if(requireZones && !state.zoneMatches.length) return toast("Primero generá las zonas");\n    const ok=copafemScheduleDateNoConflicts();\n    if(ok){ saveState(); renderAll(); }\n    return ok;\n    if(dynMode()) return generateScheduleDynamic();',
    1
)

s = s.replace(
    '  function generateScheduleDynamic(){\n    if(!state.zoneMatches.length)return;',
    '  function generateScheduleDynamic(){\n    if(!state.zoneMatches.length)return;\n    const ok=copafemScheduleDateNoConflicts();\n    if(ok){ saveState(); renderAll(); }\n    return ok;',
    1
)

s = s.replace(
    '  function scheduleBrackets(){\n    const gold=state.brackets.gold||[], silver=state.brackets.silver||[];',
    '  function scheduleBrackets(){\n    return copafemScheduleDateNoConflicts();\n    const gold=state.brackets.gold||[], silver=state.brackets.silver||[];',
    1
)

p.write_text(s,encoding='utf-8')
print('COPAFEM court allocator v4 patch OK')
