from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
MARK = 'COPAFEM_HIDE_POSITIONS_UNTIL_ZONE_COMPLETE_V1'
if MARK in s:
    print('positions-until-complete already applied')
    raise SystemExit

# 1) La tabla de posiciones del administrador conoce si la zona terminó.
old = '''    return {rows,tied};\n  }\n\n  /* COPAFEM_LIVE_ZONE_GAMES_V1 */'''
new = '''    const zoneGames=state.zoneMatches.filter(m=>m.zone===zone);\n    const expected=ids.length>1 ? (ids.length*(ids.length-1))/2 : 0;\n    const complete=expected>0 && zoneGames.length===expected && zoneGames.every(m=>hasScore(m)&&m.s1!==m.s2);\n    return {rows,tied,complete};\n  }\n\n  /* COPAFEM_HIDE_POSITIONS_UNTIL_ZONE_COMPLETE_V1 */\n\n  /* COPAFEM_LIVE_ZONE_GAMES_V1 */'''
if old not in s:
    raise SystemExit('No se encontró retorno de zoneStandings administrador')
s = s.replace(old, new, 1)

# 2) Mientras falte un partido, mostrar estadísticas pero NO 1/2/3 ni colores de clasificación.
old = '''  function standingsHTML(st){\n    return `<div class="standings"><div class="stand-row head"><span>#</span><span>Pareja</span><span>PJ</span><span>PG</span><span>GF</span><span>GC</span><span title="DG = GF - GC">DG</span></div>${st.rows.map((r,i)=>`<div class="stand-row ${i<2?"qual-gold":"qual-silver"}"><span class="rank-pill">${i+1}</span><span>${esc(r.name)}</span><span>${r.pj}</span><span>${r.pg}</span><span>${r.gf}</span><span>${r.gc}</span><span>${r.dg}</span></div>`).join("")}</div>${st.tied?`<div class="tie-warning">⚠ Persisten empatadas después de PG, diferencia de games, GF, GC y enfrentamiento directo. Revisá manualmente.</div>`:""}`;\n  }'''
new = '''  function standingsHTML(st){\n    const final=!!st.complete;\n    return `<div class="standings"><div class="stand-row head"><span>#</span><span>Pareja</span><span>PJ</span><span>PG</span><span>GF</span><span>GC</span><span title="DG = GF - GC">DG</span></div>${st.rows.map((r,i)=>`<div class="stand-row ${final?(i<2?"qual-gold":"qual-silver"):""}"><span class="rank-pill">${final?i+1:"—"}</span><span>${esc(r.name)}</span><span>${r.pj}</span><span>${r.pg}</span><span>${r.gf}</span><span>${r.gc}</span><span>${r.dg}</span></div>`).join("")}</div>${final&&st.tied?`<div class="tie-warning">⚠ Persisten empatadas después de PG, diferencia de games, GF, GC y enfrentamiento directo. Revisá manualmente.</div>`:""}`;\n  }'''
if old not in s:
    raise SystemExit('No se encontró standingsHTML')
s = s.replace(old, new, 1)

# 3) Drop completo: tampoco mostrar números de posición hasta finalizar la zona.
old = 'st=zoneStandings(z).rows,zn=id=>'
new = 'stData=zoneStandings(z),st=stData.rows,zn=id=>'
if old not in s:
    raise SystemExit('No se encontró standings del Drop')
s = s.replace(old, new, 1)
old = '<div class="drop-stand-row"><b>${i+1}</b><span class="drop-stand-team"'
new = '<div class="drop-stand-row"><b>${stData.complete?i+1:"—"}</b><span class="drop-stand-team"'
if old not in s:
    raise SystemExit('No se encontró posición del Drop')
s = s.replace(old, new, 1)

# 4) Vista jugador: no mostrar posición provisional ni números antes de cerrar la zona.
old = '''  function playerZoneCard(ev,zone,selectedPairId){\n    const rows=zoneStandings(ev,zone);const games=(ev.zoneMatches||[]).filter(m=>m.zone===zone);const isMine=(ev.zones?.[zone]||[]).includes(selectedPairId);\n    return `<div class="player-zone-card ${isMine?"my-zone":""}"><div class="player-zone-card-title"><span>ZONA ${ehtml(zone)}</span><small>${isMine?"TU ZONA":`${(ev.zones?.[zone]||[]).length} PAREJAS`}</small></div><div class="player-zone-pairs">${rows.map((r,i)=>`<div class="player-zone-pair ${r.id===selectedPairId?"me":""}"><span class="player-zone-pos">${i+1}</span><span>${ehtml(r.name)}</span><span class="player-zone-record">${r.pg} PG · DG ${r.dg}</span></div>`).join("")}</div><div class="player-zone-games">${games.map(m=>`<div class="player-zone-game"><span>${ehtml(pairName(ev,m.p1))} <b>vs</b> ${ehtml(pairName(ev,m.p2))}</span><b>${scored(m)?`${m.s1}–${m.s2}`:`${ehtml(m.time||"—")} · C${ehtml(m.court??"—")}`}</b></div>`).join("")}</div></div>`;\n  }'''
new = '''  function playerZoneCard(ev,zone,selectedPairId){\n    const rows=zoneStandings(ev,zone);const games=(ev.zoneMatches||[]).filter(m=>m.zone===zone);const isMine=(ev.zones?.[zone]||[]).includes(selectedPairId);const n=(ev.zones?.[zone]||[]).length;const expected=n>1?(n*(n-1))/2:0;const complete=expected>0&&games.length===expected&&games.every(m=>scored(m)&&m.s1!==m.s2);\n    return `<div class="player-zone-card ${isMine?"my-zone":""}"><div class="player-zone-card-title"><span>ZONA ${ehtml(zone)}</span><small>${isMine?"TU ZONA":`${(ev.zones?.[zone]||[]).length} PAREJAS`}</small></div><div class="player-zone-pairs">${rows.map((r,i)=>`<div class="player-zone-pair ${r.id===selectedPairId?"me":""}"><span class="player-zone-pos">${complete?i+1:"—"}</span><span>${ehtml(r.name)}</span><span class="player-zone-record">${r.pg} PG · DG ${r.dg}</span></div>`).join("")}</div><div class="player-zone-games">${games.map(m=>`<div class="player-zone-game"><span>${ehtml(pairName(ev,m.p1))} <b>vs</b> ${ehtml(pairName(ev,m.p2))}</span><b>${scored(m)?`${m.s1}–${m.s2}`:`${ehtml(m.time||"—")} · C${ehtml(m.court??"—")}`}</b></div>`).join("")}</div></div>`;\n  }'''
if old not in s:
    raise SystemExit('No se encontró playerZoneCard')
s = s.replace(old, new, 1)

# En estado del jugador, eliminar “posición provisional”.
old = '''}else if(idx>=0)classif=`Posición provisional: ${idx+1}.º`;'''
new = '''}else classif="Zona en juego";'''
if old not in s:
    raise SystemExit('No se encontró posición provisional del jugador')
s = s.replace(old, new, 1)

# En tabla detallada del jugador, posición en guion hasta completar.
old = '''<span class="player-rank">${i+1}</span><span>${ehtml(r.name)}</span>'''
new = '''<span class="player-rank">${complete?i+1:"—"}</span><span>${ehtml(r.name)}</span>'''
if old not in s:
    raise SystemExit('No se encontró rank detallado del jugador')
s = s.replace(old, new, 1)

p.write_text(s, encoding='utf-8')
print('COPAFEM: posiciones ocultas hasta completar cada zona')
