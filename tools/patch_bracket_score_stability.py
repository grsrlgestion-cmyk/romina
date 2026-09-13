from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_BRACKET_SCORE_STABILITY_V1'
if MARK in s:
    print('bracket score stability already applied')
    raise SystemExit

patch=r'''
<script id="COPAFEM_BRACKET_SCORE_STABILITY_V1">
// Mantener estables los cruces una vez generados.
// La regla de "no revancha" debe evitar principalmente cruces ya jugados en ZONA.
// No debe considerar el mismo partido del cuadro recién cargado como antecedente,
// porque al reconstruir cambiaba el rival, borraba el score y no propagaba ganador.
function copafemAlreadyPlayed(a,b){
  if(!a||!b||a===b) return a===b;
  const za=copafemPairZone(a),zb=copafemPairZone(b);
  if(za&&za===zb) return true;
  return (state.zoneMatches||[]).some(m=>
    ((m.p1===a&&m.p2===b)||(m.p1===b&&m.p2===a)) &&
    hasScore(m) && m.s1!==m.s2
  );
}
</script>
'''

if '</body>' not in s:
    raise SystemExit('No se encontró </body>')
head,tail=s.rsplit('</body>',1)
s=head+patch+'\n</body>'+tail
p.write_text(s,encoding='utf-8')
print('COPAFEM: resultados de cuadro estables y ganador propagado')
