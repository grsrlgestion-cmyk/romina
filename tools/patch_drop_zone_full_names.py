from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARKER='COPAFEM_ZONE_LABELS_FULL_NAMES_V1'
if MARKER in s:
    print('zone labels/full names already applied')
    raise SystemExit

# 1) Cada pareja de la zona se identifica como A1, A2, B1, etc. y se muestran
#    todas las parejas reales (3 o 4), no una cantidad fija de tres.
old_pairs='''<div class="drop-zone-pairs">${[0,1,2].map(i=>`<div class="drop-zone-pair"><b>${i+1}</b><span>${esc(pairName(ids[i]))}</span></div>`).join("")}</div>'''
new_pairs='''<div class="drop-zone-pairs">${ids.map((id,i)=>`<div class="drop-zone-pair"><b>${z}${i+1}</b><span title="${esc(pairName(id))}">${esc(pairName(id))}</span></div>`).join("")}</div>'''
if old_pairs not in s:
    raise SystemExit('No se encontró el listado de parejas del Drop')
s=s.replace(old_pairs,new_pairs,1)

# 2) Helper de etiqueta de zona+número dentro de cada tarjeta de zona.
old_decl='''const ids=state.zones[z]||[],ms=state.zoneMatches.filter(m=>m.zone===z),st=zoneStandings(z).rows;return'''
new_decl='''const ids=state.zones[z]||[],ms=state.zoneMatches.filter(m=>m.zone===z),st=zoneStandings(z).rows,zn=id=>{const k=ids.indexOf(id);return k>=0?`${z}${k+1}`:`${z}?`};return'''
if old_decl not in s:
    raise SystemExit('No se encontró la declaración interna de zona del Drop')
s=s.replace(old_decl,new_decl,1)

# 3) En cada partido el código queda en una columna propia: A1 | Nombre Apellido.
#    El código no se recorta jamás; la elipsis se aplica solo al nombre.
old_m1='''<span class="dm-team">${esc(pairName(m.p1))}</span>'''
new_m1='''<span class="dm-team" title="${esc(`${zn(m.p1)} · ${pairName(m.p1)}`)}"><b class="dm-code">${esc(zn(m.p1))}</b><span class="dm-name">${esc(pairName(m.p1))}</span></span>'''
old_m2='''<span class="dm-team">${esc(pairName(m.p2))}</span>'''
new_m2='''<span class="dm-team" title="${esc(`${zn(m.p2)} · ${pairName(m.p2)}`)}"><b class="dm-code">${esc(zn(m.p2))}</b><span class="dm-name">${esc(pairName(m.p2))}</span></span>'''
if old_m1 not in s or old_m2 not in s:
    raise SystemExit('No se encontraron los nombres de los partidos del Drop')
s=s.replace(old_m1,new_m1,1).replace(old_m2,new_m2,1)

# 4) En posiciones también conserva la referencia original de zona+número en una columna fija.
old_pos='''<span>${esc(r.name)}</span><span>PG ${r.pg}</span>'''
new_pos='''<span class="drop-stand-team" title="${esc(`${zn(r.id)} · ${r.name}`)}"><b class="dm-code">${esc(zn(r.id))}</b><span class="dm-name">${esc(r.name)}</span></span><span>PG ${r.pg}</span>'''
if old_pos not in s:
    raise SystemExit('No se encontró el nombre de posiciones del Drop')
s=s.replace(old_pos,new_pos,1)

# 5) Una sola línea. El código A1/B2/etc. queda siempre visible y solo el nombre usa ...
style=r'''
<style id="COPAFEM_ZONE_LABELS_FULL_NAMES_V1">
  .drop-zone-pair{
    grid-template-columns:42px minmax(0,1fr)!important;
    align-items:center!important;
    height:auto!important;
    min-height:25px!important;
  }
  .drop-zone-pair b{
    padding:4px 2px!important;
    text-align:center!important;
    font-weight:950!important;
    color:var(--cat-ink)!important;
    white-space:nowrap!important;
  }
  .drop-zone-pair span{
    display:block!important;
    min-width:0!important;
    white-space:nowrap!important;
    overflow:hidden!important;
    text-overflow:ellipsis!important;
    word-break:normal!important;
    overflow-wrap:normal!important;
  }

  .drop-match-row{
    align-items:center!important;
    height:auto!important;
    min-height:25px!important;
  }
  .drop-match-row .dm-team,
  .drop-stand-team{
    display:grid!important;
    grid-template-columns:27px minmax(0,1fr)!important;
    align-items:center!important;
    gap:3px!important;
    min-width:0!important;
    overflow:visible!important;
    white-space:normal!important;
    text-overflow:clip!important;
  }
  .dm-code{
    display:block!important;
    min-width:27px!important;
    white-space:nowrap!important;
    overflow:visible!important;
    text-overflow:clip!important;
    font-weight:950!important;
    color:var(--cat-ink)!important;
  }
  .dm-name{
    display:block!important;
    min-width:0!important;
    white-space:nowrap!important;
    overflow:hidden!important;
    text-overflow:ellipsis!important;
    word-break:normal!important;
    overflow-wrap:normal!important;
    line-height:1.25!important;
  }
  .drop-match-row .dm-team{font-weight:700!important}
  .drop-stand-row{align-items:center!important;height:auto!important;min-width:0!important}

  @media print{
    .copafem-print-zones .drop-zone-pair{
      grid-template-columns:11mm minmax(0,1fr)!important;
      min-height:6mm!important;
      height:auto!important;
      align-items:center!important;
    }
    .copafem-print-zones .drop-zone-pair span{
      display:block!important;
      min-width:0!important;
      white-space:nowrap!important;
      overflow:hidden!important;
      text-overflow:ellipsis!important;
      word-break:normal!important;
      overflow-wrap:normal!important;
    }
    .copafem-print-zones .drop-match-row{
      height:auto!important;
      min-height:6mm!important;
      align-items:center!important;
    }
    .copafem-print-zones .drop-match-row .dm-team,
    .copafem-print-zones .drop-stand-team{
      display:grid!important;
      grid-template-columns:8mm minmax(0,1fr)!important;
      gap:1mm!important;
      min-width:0!important;
      overflow:visible!important;
    }
    .copafem-print-zones .dm-code{
      min-width:8mm!important;
      white-space:nowrap!important;
      overflow:visible!important;
      font-size:7.3pt!important;
    }
    .copafem-print-zones .dm-name{
      min-width:0!important;
      white-space:nowrap!important;
      overflow:hidden!important;
      text-overflow:ellipsis!important;
      font-size:7.1pt!important;
    }
    .copafem-print-zones .drop-stand-row{
      height:auto!important;
      min-height:5.5mm!important;
      align-items:center!important;
    }
  }
</style>
'''
head,tail=s.rsplit('</body>',1)
s=head+style+'\n</body>'+tail

p.write_text(s,encoding='utf-8')
print('COPAFEM zone code always visible + one-line names patch OK')
