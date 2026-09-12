from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_OP2_CROSS_ZONE_BRACKET_V1'
if MARK in s:
    print('op2 cross-zone bracket already applied')
    raise SystemExit

patch=r'''
<script id="COPAFEM_OP2_CROSS_ZONE_BRACKET_V1">
// Opción 2: los 2.º y 3.º de una misma zona nunca se enfrentan entre sí en Octavos.
// El 1.º de cada zona entra en un Cuarto de una rama distinta a la de sus compañeros de zona.
function copafemMode2(oldG,oldS){
  const zones=copafemActiveZones();
  if(!zones.length)return {gold:[],silver:[]};
  const n=zones.length;
  const gold=[],silver=[],goldQFWinners=[],silverQFWinners=[];
  const r16=[];

  // OCTAVOS DE ORO: 2.º de una zona vs 3.º de la zona siguiente.
  // Ejemplo: 2.º A vs 3.º B; 2.º B vs 3.º C; etc.
  for(let i=0;i<n;i++){
    const za=zones[i];
    const zb=zones[(i+1)%n];
    const m=copafemMakeMatch(
      `G-R16-X${i+1}`,
      'Octavos',
      copafemSeedSource(za,2),
      copafemSeedSource(zb,3),
      oldG
    );
    gold.push(m);
    r16.push(m);
  }

  // CUARTOS DE ORO: cada 1.º espera al ganador de un Octavo de la rama opuesta.
  // De esta forma no puede cruzarse en Cuartos con el 2.º ni el 3.º de su propia zona.
  const offset=Math.max(1,Math.floor(n/2));
  zones.forEach((z,i)=>{
    const feed=r16[(i+offset)%n];
    const qf=copafemMakeMatch(
      `G-QF-Z${z}`,
      'Cuartos',
      copafemSeedSource(z,1),
      copafemSource(`W:${feed.id}`,winnerId(feed)),
      oldG
    );
    gold.push(qf);
    goldQFWinners.push(copafemSource(`W:${qf.id}`,winnerId(qf)));

    // Plata conserva la regla del formato: perdedor del Octavo vs perdedor del Cuarto
    // correspondiente a esa llave de Oro.
    const sqf=copafemMakeMatch(
      `S-QF-Z${z}`,
      'Cuartos',
      copafemSource(`L:${feed.id}`,loserId(feed)),
      copafemSource(`L:${qf.id}`,loserId(qf)),
      oldS
    );
    silver.push(sqf);
    silverQFWinners.push(copafemSource(`W:${sqf.id}`,winnerId(sqf)));
  });

  const gt=copafemBuildBracket('G2',goldQFWinners,oldG,goldQFWinners.length>4?'Ronda Oro':'');
  const st=copafemBuildBracket('S2',silverQFWinners,oldS,silverQFWinners.length>4?'Ronda Plata':'');
  gold.push(...gt.matches);
  silver.push(...st.matches);
  return {gold,silver};
}

// Ajustar únicamente el texto explicativo de Opción 2.
const _copafemRefreshDropModeUICrossZone=window.copafemRefreshDropModeUI;
window.copafemRefreshDropModeUI=function(){
  if(typeof _copafemRefreshDropModeUICrossZone==='function') _copafemRefreshDropModeUICrossZone();
  if(copafemDropMode()==='op2'){
    const g=document.getElementById('goldRuleText');
    const help=document.getElementById('dropFormatHelp');
    if(g)g.textContent='Los 3 clasifican a Oro · 2.º vs 3.º de otra zona · 1.º espera en Cuartos';
    if(help)help.innerHTML='<b>Opción 2:</b> los 3 clasifican a Oro. En Octavos, el 2.º juega contra el 3.º de otra zona. El 1.º espera en Cuartos en una llave distinta para evitar cruces entre parejas de la misma zona.';
  }
};
</script>
'''

head,tail=s.rsplit('</body>',1)
s=head+patch+'\n</body>'+tail
p.write_text(s,encoding='utf-8')
print('COPAFEM: Opción 2 sembrada por zonas cruzadas y llaves distintas')
