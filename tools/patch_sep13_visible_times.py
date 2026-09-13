from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_SEP13_VISIBLE_TIMES_V1'
if MARK in s:
    print('visible sep13 times already applied')
    raise SystemExit

old_admin='''  function activeDateScheduledRows(){
    const date=state.tournament.date;
    return eventsOnDate(date).flatMap(([id,e])=>scheduledRowsForEvent(e,id)).sort((a,b)=>(a.time||"99:99").localeCompare(b.time||"99:99") || Number(a.court||999)-Number(b.court||999) || CATEGORIES.indexOf(a.category)-CATEGORIES.indexOf(b.category) || a.stage.localeCompare(b.stage));
  }'''
new_admin='''  // COPAFEM_SEP13_VISIBLE_TIMES_V1
  function activeDateScheduledRows(){
    const date=state.tournament.date;
    let rows=eventsOnDate(date).flatMap(([id,e])=>scheduledRowsForEvent(e,id));
    const target=date==='2026-09-13'||date==='13/09/2026';
    const needs=target && rows.some(m=>String(m.time||'')==='12:30');
    if(needs){
      rows=rows.map(m=>{
        const t=parseTime(m.time||'');
        return Number.isFinite(t)&&t>=parseTime('12:30') ? {...m,time:fmtTime(t+30)} : m;
      });
    }
    return rows.sort((a,b)=>(a.time||"99:99").localeCompare(b.time||"99:99") || Number(a.court||999)-Number(b.court||999) || CATEGORIES.indexOf(a.category)-CATEGORIES.indexOf(b.category) || a.stage.localeCompare(b.stage));
  }'''
if old_admin not in s:
    raise SystemExit('No se encontró activeDateScheduledRows')
s=s.replace(old_admin,new_admin,1)

old_player='''  function allMatches(ev){
    const rows=(ev.zoneMatches||[]).map(m=>({...m,stage:`Zona ${m.zone}`,cup:"Zona"}));
    (ev.brackets?.gold||[]).forEach(m=>rows.push({...m,stage:`Oro · ${m.round}`,cup:"Oro"}));
    (ev.brackets?.silver||[]).forEach(m=>rows.push({...m,stage:`Plata · ${m.round}`,cup:"Plata"}));
    return rows.sort((a,b)=>(a.time||"99:99").localeCompare(b.time||"99:99")||Number(a.court||999)-Number(b.court||999)||a.stage.localeCompare(b.stage));
  }'''
new_player='''  function allMatches(ev){
    let rows=(ev.zoneMatches||[]).map(m=>({...m,stage:`Zona ${m.zone}`,cup:"Zona"}));
    (ev.brackets?.gold||[]).forEach(m=>rows.push({...m,stage:`Oro · ${m.round}`,cup:"Oro"}));
    (ev.brackets?.silver||[]).forEach(m=>rows.push({...m,stage:`Plata · ${m.round}`,cup:"Plata"}));
    const d=String(ev?.tournament?.date||'');
    const target=d==='2026-09-13'||d==='13/09/2026';
    const needs=target && rows.some(m=>String(m.time||'')==='12:30');
    if(needs){
      rows=rows.map(m=>{
        const mm=String(m.time||'').match(/^(\\d{1,2}):(\\d{2})$/);
        if(!mm) return m;
        const t=Number(mm[1])*60+Number(mm[2]);
        if(t<750) return m;
        const n=t+30;
        return {...m,time:String(Math.floor(n/60)).padStart(2,'0')+':'+String(n%60).padStart(2,'0')};
      });
    }
    return rows.sort((a,b)=>(a.time||"99:99").localeCompare(b.time||"99:99")||Number(a.court||999)-Number(b.court||999)||a.stage.localeCompare(b.stage));
  }'''
if old_player not in s:
    raise SystemExit('No se encontró allMatches del jugador')
s=s.replace(old_player,new_player,1)

p.write_text(s,encoding='utf-8')
print('COPAFEM: horarios visibles del 13/09 corregidos 12:30 -> 13:00 y posteriores +30 min')
