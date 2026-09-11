from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
MARKER = 'COPAFEM_ZONE_TIEBREAK_GAMES_V2'
if MARKER in s:
    print('zone tiebreak games already applied')
    raise SystemExit

# ---- ADMIN: clasificación de zona ----
old = '''    rows.forEach(r=>r.dg=r.gf-r.gc);
    rows.sort((a,b)=>b.pg-a.pg || b.dg-a.dg || b.gf-a.gf || a.name.localeCompare(b.name,"es"));
    let tied=false;
    for(let i=0;i<rows.length-1;i++) if(rows[i].pg===rows[i+1].pg && rows[i].dg===rows[i+1].dg && rows[i].gf===rows[i+1].gf && rows[i].pj===2 && rows[i+1].pj===2) tied=true;
    return {rows,tied};'''
new = '''    rows.forEach(r=>r.dg=r.gf-r.gc);
    const baseCmp=(a,b)=>b.pg-a.pg || b.dg-a.dg || b.gf-a.gf || a.gc-b.gc;
    rows.sort((a,b)=>baseCmp(a,b) || a.name.localeCompare(b.name,"es"));

    // Si exactamente dos parejas siguen iguales en PG, DG, GF y GC,
    // define el enfrentamiento directo entre ellas.
    let tied=false;
    for(let start=0;start<rows.length;){
      let end=start+1;
      while(end<rows.length && baseCmp(rows[start],rows[end])===0) end++;
      const group=rows.slice(start,end);
      if(group.length===2){
        const [x,y]=group;
        const direct=state.zoneMatches.find(m=>m.zone===zone && hasScore(m) && m.s1!==m.s2 && ((m.p1===x.id&&m.p2===y.id)||(m.p1===y.id&&m.p2===x.id)));
        if(direct){
          const winner=direct.s1>direct.s2?direct.p1:direct.p2;
          if(rows[start].id!==winner){ const tmp=rows[start]; rows[start]=rows[start+1]; rows[start+1]=tmp; }
        }else if(x.pj>0 && y.pj>0){
          tied=true;
        }
      }else if(group.length>2){
        tied=true;
      }
      start=end;
    }
    return {rows,tied};'''
if old not in s:
    raise SystemExit('No se encontró zoneStandings del administrador')
s = s.replace(old, new, 1)

# ---- JUGADOR: misma clasificación para que ambas vistas coincidan ----
old_player = '''    rows.forEach(r=>r.dg=r.gf-r.gc);rows.sort((a,b)=>b.pg-a.pg||b.dg-a.dg||b.gf-a.gf||a.name.localeCompare(b.name,"es"));return rows;'''
new_player = '''    rows.forEach(r=>r.dg=r.gf-r.gc);
    const baseCmp=(a,b)=>b.pg-a.pg||b.dg-a.dg||b.gf-a.gf||a.gc-b.gc;
    rows.sort((a,b)=>baseCmp(a,b)||a.name.localeCompare(b.name,"es"));
    for(let start=0;start<rows.length;){let end=start+1;while(end<rows.length&&baseCmp(rows[start],rows[end])===0)end++;if(end-start===2){const x=rows[start],y=rows[start+1],direct=(ev.zoneMatches||[]).find(m=>m.zone===zone&&scored(m)&&m.s1!==m.s2&&((m.p1===x.id&&m.p2===y.id)||(m.p1===y.id&&m.p2===x.id)));if(direct){const winner=direct.s1>direct.s2?direct.p1:direct.p2;if(rows[start].id!==winner){const tmp=rows[start];rows[start]=rows[start+1];rows[start+1]=tmp;}}}start=end;}return rows;'''
if old_player not in s:
    raise SystemExit('No se encontró zoneStandings del jugador')
s = s.replace(old_player, new_player, 1)

# ---- Mostrar explícitamente GF y GC en Resultados ----
old_html = '''return `<div class="standings"><div class="stand-row head"><span>#</span><span>Pareja</span><span>PJ</span><span>PG</span><span>DG</span><span>GF</span></div>${st.rows.map((r,i)=>`<div class="stand-row ${i<2?"qual-gold":"qual-silver"}"><span class="rank-pill">${i+1}</span><span>${esc(r.name)}</span><span>${r.pj}</span><span>${r.pg}</span><span>${r.dg}</span><span>${r.gf}</span></div>`).join("")}</div>${st.tied?`<div class="tie-warning">⚠ Igualdad total en criterios: revisá el desempate manualmente antes de usar la clasificación.</div>`:""}`;'''
new_html = '''return `<div class="standings"><div class="stand-row head"><span>#</span><span>Pareja</span><span>PJ</span><span>PG</span><span>GF</span><span>GC</span><span>DG</span></div>${st.rows.map((r,i)=>`<div class="stand-row ${i<2?"qual-gold":"qual-silver"}"><span class="rank-pill">${i+1}</span><span>${esc(r.name)}</span><span>${r.pj}</span><span>${r.pg}</span><span>${r.gf}</span><span>${r.gc}</span><span>${r.dg}</span></div>`).join("")}</div>${st.tied?`<div class="tie-warning">⚠ Persisten empatadas después de PG, diferencia de games, GF, GC y enfrentamiento directo. Revisá manualmente.</div>`:""}`;'''
if old_html not in s:
    raise SystemExit('No se encontró standingsHTML')
s = s.replace(old_html, new_html, 1)

# ---- CSS 7 columnas ----
style = r'''
<style id="COPAFEM_ZONE_TIEBREAK_GAMES_V2">
  .stand-row{
    grid-template-columns:34px minmax(220px,1fr) 42px 42px 42px 42px 48px!important;
  }
  @media(max-width:580px){
    .stand-row{grid-template-columns:28px minmax(150px,1fr) 34px 34px 34px 34px 42px!important;overflow-x:auto}
  }
  @media print{
    #view-results .stand-row{grid-template-columns:10mm 1fr 12mm 12mm 12mm 12mm 12mm!important}
  }
</style>
'''
head, tail = s.rsplit('</body>', 1)
s = head + style + '\n</body>' + tail

p.write_text(s, encoding='utf-8')
print('COPAFEM: desempate PG > DG > GF > GC > enfrentamiento directo aplicado')
