from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
MARK = 'COPAFEM_FINAL_POSITIONS_ONLY_WHEN_ZONE_COMPLETE_V1'
if MARK in s:
    print('final positions visibility already applied')
    raise SystemExit

# 1) La tabla principal de posiciones conoce si la zona está realmente completa.
old = '''    return {rows,tied};
  }

  /* COPAFEM_LIVE_ZONE_GAMES_V1 */'''
new = '''    const zoneGames=state.zoneMatches.filter(m=>m.zone===zone);
    const expected=ids.length>1 ? (ids.length*(ids.length-1))/2 : 0;
    const complete=expected>0 && zoneGames.length===expected && zoneGames.every(m=>hasScore(m)&&m.s1!==m.s2);
    return {rows,tied,complete};
  }

  /* COPAFEM_LIVE_ZONE_GAMES_V1 */'''
if old not in s:
    raise SystemExit('No se encontró el retorno principal de zoneStandings')
s = s.replace(old, new, 1)

# 2) En Resultados: mientras falte un partido se muestran estadísticas, pero no puesto 1/2/3 ni color de clasificación.
start = s.find('  function standingsHTML(st){')
end = s.find('\n\n  function renderCups(){', start)
if start < 0 or end < 0:
    raise SystemExit('No se encontró standingsHTML')
new_standings = '''  function standingsHTML(st){
    const complete=!!st.complete;
    return `<div class="standings"><div class="stand-row head"><span>#</span><span>Pareja</span><span>PJ</span><span>PG</span><span>GF</span><span>GC</span><span title="DG = GF - GC">DG</span></div>${st.rows.map((r,i)=>`<div class="stand-row ${complete?(i<2?"qual-gold":"qual-silver"):""}"><span class="rank-pill">${complete?i+1:""}</span><span>${esc(r.name)}</span><span>${r.pj}</span><span>${r.pg}</span><span>${r.gf}</span><span>${r.gc}</span><span>${r.dg}</span></div>`).join("")}</div>${complete&&st.tied?`<div class="tie-warning">⚠ Persisten empatadas después de PG, diferencia de games, GF, GC y enfrentamiento directo. Revisá manualmente.</div>`:""}`;
  }'''
s = s[:start] + new_standings + s[end:]

# 3) Drop completo: tampoco mostrar número de posición hasta que la zona esté terminada.
old = 'st=zoneStandings(z).rows,zn=id=>'
new = 'stand=zoneStandings(z),st=stand.rows,zoneDone=!!stand.complete,zn=id=>'
if old not in s:
    raise SystemExit('No se encontró standings del Drop')
s = s.replace(old, new, 1)
old = '<div class="drop-stand-row"><b>${i+1}</b>'
new = '<div class="drop-stand-row"><b>${zoneDone?i+1:""}</b>'
if old not in s:
    raise SystemExit('No se encontró numeración de posiciones del Drop')
s = s.replace(old, new, 1)

# 4) Vista jugador - tarjeta visual de zona: sin puesto provisorio antes de completar todos los partidos.
old = '''    const rows=zoneStandings(ev,zone);const games=(ev.zoneMatches||[]).filter(m=>m.zone===zone);const isMine=(ev.zones?.[zone]||[]).includes(selectedPairId);'''
new = '''    const rows=zoneStandings(ev,zone);const games=(ev.zoneMatches||[]).filter(m=>m.zone===zone);const ids=(ev.zones?.[zone]||[]);const expected=ids.length>1?(ids.length*(ids.length-1))/2:0;const complete=expected>0&&games.length===expected&&games.every(scored);const isMine=ids.includes(selectedPairId);'''
if old not in s:
    raise SystemExit('No se encontró playerZoneCard')
s = s.replace(old, new, 1)
old = '<span class="player-zone-pos">${i+1}</span>'
new = '<span class="player-zone-pos">${complete?i+1:""}</span>'
if old not in s:
    raise SystemExit('No se encontró posición en playerZoneCard')
s = s.replace(old, new, 1)

# 5) Vista jugador - clasificación personal: quitar "Posición provisional" y numeración hasta finalizar la zona.
old = '''if(zoneEntry){const [zone]=zoneEntry,rows=zoneStandings(ev,zone),idx=rows.findIndex(r=>r.id===selectedPairId),zoneMatches=(ev.zoneMatches||[]).filter(m=>m.zone===zone),complete=zoneMatches.length===3&&zoneMatches.every(scored);let classif="Zona en juego";if(complete&&idx>=0){const inSilver=(ev.brackets?.silver||[]).some(m=>m.p1===selectedPairId||m.p2===selectedPairId);classif=idx<2?(inSilver?"Pasa a Copa de Plata":"Clasificado a Copa de Oro"):"Clasificado directo a Copa de Plata";}else if(idx>=0)classif=`Posición provisional: ${idx+1}.º`;'''
new = '''if(zoneEntry){const [zone]=zoneEntry,rows=zoneStandings(ev,zone),idx=rows.findIndex(r=>r.id===selectedPairId),zoneMatches=(ev.zoneMatches||[]).filter(m=>m.zone===zone),zoneIds=(ev.zones?.[zone]||[]),expected=zoneIds.length>1?(zoneIds.length*(zoneIds.length-1))/2:0,complete=expected>0&&zoneMatches.length===expected&&zoneMatches.every(scored);let classif="Zona en juego";if(complete&&idx>=0){const inSilver=(ev.brackets?.silver||[]).some(m=>m.p1===selectedPairId||m.p2===selectedPairId);classif=idx<2?(inSilver?"Pasa a Copa de Plata":"Clasificado a Copa de Oro"):"Clasificado directo a Copa de Plata";}'''
if old not in s:
    raise SystemExit('No se encontró clasificación provisional del jugador')
s = s.replace(old, new, 1)
old = '<span class="player-rank">${i+1}</span>'
new = '<span class="player-rank">${complete?i+1:""}</span>'
if old not in s:
    raise SystemExit('No se encontró ranking de jugador')
s = s.replace(old, new, 1)

# Marcador para idempotencia y trazabilidad.
s = s.replace('</body>', f'\n<!-- {MARK} -->\n</body>', 1)
p.write_text(s, encoding='utf-8')
print('COPAFEM: posiciones definitivas visibles solo al completar cada zona')
