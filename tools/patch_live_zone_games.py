from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARKER='COPAFEM_LIVE_ZONE_GAMES_V1'
if MARKER in s:
    print('live zone games already applied')
    raise SystemExit

# Agrega identificadores de zona y un contenedor para refrescar solo la tabla de posiciones.
old='''$("resultsContainer").innerHTML=ZONES.map(z=>{const ms=state.zoneMatches.filter(m=>m.zone===z),st=zoneStandings(z);return `<article class="zone-block"><div class="zone-block-head"><h3>Zona ${z}</h3><span class="counter">${ms.filter(m=>hasScore(m)&&m.s1!==m.s2).length}/3</span></div>${ms.map(m=>`<div class="match-grid"><div class="team-name">${esc(pairName(m.p1))}</div><div class="score-box"><input inputmode="numeric" min="0" type="number" value="${m.s1??""}" data-zscore="${m.id}" data-side="s1"><b>–</b><input inputmode="numeric" min="0" type="number" value="${m.s2??""}" data-zscore="${m.id}" data-side="s2"></div><div class="team-name">${esc(pairName(m.p2))}</div><div class="schedule-meta">${m.time||"--:--"} · Cancha ${m.court??"—"}</div></div>`).join("")}${standingsHTML(st)}</article>`;}).join("");
    document.querySelectorAll("[data-zscore]").forEach(el=>el.addEventListener("change",e=>setZoneScore(e.target.dataset.zscore,e.target.dataset.side,e.target.value)));'''
new='''$("resultsContainer").innerHTML=ZONES.map(z=>{const ms=state.zoneMatches.filter(m=>m.zone===z),st=zoneStandings(z);return `<article class="zone-block" data-zone-block="${z}"><div class="zone-block-head"><h3>Zona ${z}</h3><span class="counter">${ms.filter(m=>hasScore(m)&&m.s1!==m.s2).length}/3</span></div>${ms.map(m=>`<div class="match-grid"><div class="team-name">${esc(pairName(m.p1))}</div><div class="score-box"><input inputmode="numeric" min="0" type="number" value="${m.s1??""}" data-zscore="${m.id}" data-side="s1"><b>–</b><input inputmode="numeric" min="0" type="number" value="${m.s2??""}" data-zscore="${m.id}" data-side="s2"></div><div class="team-name">${esc(pairName(m.p2))}</div><div class="schedule-meta">${m.time||"--:--"} · Cancha ${m.court??"—"}</div></div>`).join("")}<div data-zone-standings="${z}">${standingsHTML(st)}</div></article>`;}).join("");
    document.querySelectorAll("[data-zscore]").forEach(el=>{
      el.addEventListener("input",e=>previewZoneScore(e.target.dataset.zscore,e.target.dataset.side,e.target.value));
      el.addEventListener("change",e=>setZoneScore(e.target.dataset.zscore,e.target.dataset.side,e.target.value));
    });'''
if old not in s:
    raise SystemExit('No se encontró renderResults esperado; verificar orden del parche')
s=s.replace(old,new,1)

# Vista previa inmediata: actualiza el modelo y la tabla GF/GC/DG sin reconstruir inputs.
anchor='''  function setZoneScore(id, side, value){
'''
if anchor not in s:
    raise SystemExit('No se encontró setZoneScore')
helper='''  /* COPAFEM_LIVE_ZONE_GAMES_V1 */
  function previewZoneScore(id,side,value){
    const m=state.zoneMatches.find(x=>x.id===id); if(!m)return;
    const n=value===""?null:parseInt(value,10);
    m[side]=Number.isFinite(n)?Math.max(0,n):null;
    const zone=m.zone;
    const wrap=document.querySelector(`[data-zone-standings="${zone}"]`);
    if(wrap) wrap.innerHTML=standingsHTML(zoneStandings(zone));
    const block=document.querySelector(`[data-zone-block="${zone}"] .counter`);
    if(block){const ms=state.zoneMatches.filter(x=>x.zone===zone);block.textContent=`${ms.filter(x=>hasScore(x)&&x.s1!==x.s2).length}/${ms.length}`;}
  }

'''
s=s.replace(anchor,helper+anchor,1)

# Aclara visualmente la fórmula en el encabezado de la tabla.
s=s.replace('<span>GF</span><span>GC</span><span>DG</span>', '<span>GF</span><span>GC</span><span title="DG = GF - GC">DG</span>', 1)

p.write_text(s,encoding='utf-8')
print('COPAFEM: GF/GC/DG en vivo aplicado a todas las zonas y categorías')
