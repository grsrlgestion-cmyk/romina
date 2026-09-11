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
new_pairs='''<div class="drop-zone-pairs">${ids.map((id,i)=>`<div class="drop-zone-pair"><b>${z}${i+1}</b><span>${esc(pairName(id))}</span></div>`).join("")}</div>'''
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
new_m1='''<span class="dm-team">${esc(`${zn(m.p1)} · ${pairName(m.p1)}`)}</span>'''
old_m2='''<span class="dm-team">${esc(pairName(m.p2))}</span>'''
new_m2='''<span class="dm-team">${esc(`${zn(m.p2)} · ${pairName(m.p2)}`)}</span>'''
if old_m1 not in s or old_m2 not in s:
    raise SystemExit('No se encontraron los nombres de los partidos del Drop')
s=s.replace(old_m1,new_m1,1).replace(old_m2,new_m2,1)

# 4) En posiciones también conserva la referencia original de zona+número.
old_pos='''<span>${esc(r.name)}</span><span>PG ${r.pg}</span>'''
new_pos='''<span>${esc(`${zn(r.id)} · ${r.name}`)}</span><span>PG ${r.pg}</span>'''
if old_pos not in s:
    raise SystemExit('No se encontró el nombre de posiciones del Drop')
s=s.replace(old_pos,new_pos,1)

# 5) Permitir nombres completos en pantalla e impresión, sin elipsis.
style=r'''
<style id="COPAFEM_ZONE_LABELS_FULL_NAMES_V1">
  .drop-zone-pair{grid-template-columns:34px 1fr!important;align-items:start!important;height:auto!important;min-height:25px!important}
  .drop-zone-pair b{padding:4px 2px!important;text-align:center!important;font-weight:950!important;color:var(--cat-ink)!important}
  .drop-zone-pair span{white-space:normal!important;overflow:visible!important;text-overflow:clip!important;line-height:1.28!important;overflow-wrap:anywhere!important}
  .drop-match-row{align-items:start!important;height:auto!important;min-height:25px!important}
  .drop-match-row .dm-team{white-space:normal!important;overflow:visible!important;text-overflow:clip!important;line-height:1.25!important;overflow-wrap:anywhere!important;font-weight:700!important}
  .drop-stand-row{align-items:start!important;height:auto!important}
  .drop-stand-row span:nth-child(2){white-space:normal!important;line-height:1.25!important;overflow-wrap:anywhere!important}

  @media print{
    .copafem-print-zones .drop-zone-pair{grid-template-columns:9mm 1fr!important;min-height:6mm!important;height:auto!important}
    .copafem-print-zones .drop-zone-pair span{white-space:normal!important;overflow:visible!important;text-overflow:clip!important;line-height:1.25!important}
    .copafem-print-zones .drop-match-row{height:auto!important;min-height:6mm!important;align-items:start!important}
    .copafem-print-zones .drop-match-row .dm-team{white-space:normal!important;overflow:visible!important;text-overflow:clip!important;line-height:1.22!important;font-size:7.1pt!important}
    .copafem-print-zones .drop-stand-row{height:auto!important;min-height:5.5mm!important;align-items:start!important}
    .copafem-print-zones .drop-stand-row span:nth-child(2){white-space:normal!important;line-height:1.2!important}
  }
</style>
'''
head,tail=s.rsplit('</body>',1)
s=head+style+'\n</body>'+tail

p.write_text(s,encoding='utf-8')
print('COPAFEM zone labels + full names patch OK')
