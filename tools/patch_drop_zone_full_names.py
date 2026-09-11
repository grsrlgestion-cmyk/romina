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

# 3) En cada partido: A1 · NOMBRE APELLIDO, A2 · NOMBRE APELLIDO.
old_m1='''<span class="dm-team">${esc(pairName(m.p1))}</span>'''
new_m1='''<span class="dm-team" title="${esc(`${zn(m.p1)} · ${pairName(m.p1)}`)}">${esc(`${zn(m.p1)} · ${pairName(m.p1)}`)}</span>'''
old_m2='''<span class="dm-team">${esc(pairName(m.p2))}</span>'''
new_m2='''<span class="dm-team" title="${esc(`${zn(m.p2)} · ${pairName(m.p2)}`)}">${esc(`${zn(m.p2)} · ${pairName(m.p2)}`)}</span>'''
if old_m1 not in s or old_m2 not in s:
    raise SystemExit('No se encontraron los nombres de los partidos del Drop')
s=s.replace(old_m1,new_m1,1).replace(old_m2,new_m2,1)

# 4) En posiciones también conserva la referencia original de zona+número.
old_pos='''<span>${esc(r.name)}</span><span>PG ${r.pg}</span>'''
new_pos='''<span title="${esc(`${zn(r.id)} · ${r.name}`)}">${esc(`${zn(r.id)} · ${r.name}`)}</span><span>PG ${r.pg}</span>'''
if old_pos not in s:
    raise SystemExit('No se encontró el nombre de posiciones del Drop')
s=s.replace(old_pos,new_pos,1)

# 5) Nombres SIEMPRE en una sola línea. Si no entran, se recortan con puntos suspensivos.
#    El usuario puede usar el zoom + para ampliar la visualización.
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
  .drop-zone-pair span,
  .drop-match-row .dm-team,
  .drop-stand-row span:nth-child(2){
    display:block!important;
    min-width:0!important;
    white-space:nowrap!important;
    overflow:hidden!important;
    text-overflow:ellipsis!important;
    word-break:normal!important;
    overflow-wrap:normal!important;
    line-height:1.25!important;
  }
  .drop-match-row{
    align-items:center!important;
    height:auto!important;
    min-height:25px!important;
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
    .copafem-print-zones .drop-zone-pair span,
    .copafem-print-zones .drop-match-row .dm-team,
    .copafem-print-zones .drop-stand-row span:nth-child(2){
      display:block!important;
      min-width:0!important;
      white-space:nowrap!important;
      overflow:hidden!important;
      text-overflow:ellipsis!important;
      word-break:normal!important;
      overflow-wrap:normal!important;
      line-height:1.2!important;
    }
    .copafem-print-zones .drop-match-row{
      height:auto!important;
      min-height:6mm!important;
      align-items:center!important;
    }
    .copafem-print-zones .drop-match-row .dm-team{font-size:7.1pt!important}
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
print('COPAFEM zone labels + one-line names patch OK')
