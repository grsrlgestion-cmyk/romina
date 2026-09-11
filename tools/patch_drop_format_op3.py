from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_DROP_FORMAT_OP3_V1'
if MARK in s:
    print('drop format op3 already applied')
    raise SystemExit

# 1) Agregar la opción al selector generado por patch_drop_format_selector.py
needle='''            <option value="op2">Opción 2 · Los 3 a Oro / 2.º vs 3.º y 1.º espera en Cuartos</option>'''
replacement=needle+'''\n            <option value="op3">Opción 3 · Máximo cupo · 1.º y 2.º a Octavos de Oro / 3.º a Octavos de Plata</option>'''
if needle not in s:
    raise SystemExit('No se encontró la opción 2 del selector')
s=s.replace(needle,replacement,1)

# 2) Permitir guardar op3 en lugar de convertirlo a op1.
s=s.replace(
    "state.tournament.dropMode=e.target.value==='op2'?'op2':'op1';",
    "state.tournament.dropMode=['op1','op2','op3'].includes(e.target.value)?e.target.value:'op1';",
    1
)
s=s.replace(
    "toast(state.tournament.dropMode==='op2'?'Formato 2 aplicado':'Formato 1 aplicado');",
    "toast(state.tournament.dropMode==='op3'?'Formato 3 · Máximo cupo aplicado':state.tournament.dropMode==='op2'?'Formato 2 aplicado':'Formato 1 aplicado');",
    1
)

# 3) Insertar la lógica de Opción 3 y sobreescribir las funciones generales del selector.
injection=r'''
<script id="COPAFEM_DROP_FORMAT_OP3_V1">
// Opción 3 · Máximo cupo
// 1.º y 2.º de cada zona -> Octavos de Oro.
// 3.º de cada zona + perdedores de Octavos de Oro -> Octavos de Plata.
// Desde Cuartos de Oro, el perdedor queda eliminado. En Plata, toda derrota elimina.
function copafemMode3(oldG,oldS){
  const zones=copafemActiveZones();
  if(!zones.length)return {gold:[],silver:[]};
  const gold=[];
  const silver=[];
  const goldR16Winners=[];
  const silverR16Winners=[];
  const n=zones.length;

  // ORO: 1.º vs 2.º de una zona opuesta/invertida para evitar cruces de la misma zona.
  for(let i=0;i<n;i++){
    const za=zones[i];
    const zb=zones[n-1-i];
    const m=copafemMakeMatch(`G3-R16-${i+1}`,'Octavos',copafemSeedSource(za,1),copafemSeedSource(zb,2),oldG);
    gold.push(m);
    goldR16Winners.push(copafemSource(`W:${m.id}`,winnerId(m)));
  }

  // PLATA: cada 3.º de zona enfrenta un perdedor de Octavos de Oro desplazado.
  // Con 8 zonas: A3 enfrenta al perdedor del 3.er Octavo, B3 al del 4.º, etc.
  for(let i=0;i<n;i++){
    const z=zones[i];
    const goldLossMatch=gold[(i+2)%n];
    const m=copafemMakeMatch(
      `S3-R16-${i+1}`,
      'Octavos',
      copafemSeedSource(z,3),
      copafemSource(`L:${goldLossMatch.id}`,loserId(goldLossMatch)),
      oldS
    );
    silver.push(m);
    silverR16Winners.push(copafemSource(`W:${m.id}`,winnerId(m)));
  }

  // Desde Cuartos, ambas copas son eliminación directa independiente.
  const goldTail=copafemBuildBracket('G3T',goldR16Winners,oldG);
  const silverTail=copafemBuildBracket('S3T',silverR16Winners,oldS);
  gold.push(...goldTail.matches);
  silver.push(...silverTail.matches);
  return {gold,silver};
}

// Reemplaza la reconstrucción general para incluir op3.
function copafemRebuildDropByMode(preserveScores=true){
  const oldG=preserveScores?Object.fromEntries((state.brackets?.gold||[]).map(m=>[m.id,m])):{};
  const oldS=preserveScores?Object.fromEntries((state.brackets?.silver||[]).map(m=>[m.id,m])):{};
  const mode=copafemDropMode();
  const built=mode==='op3'?copafemMode3(oldG,oldS):mode==='op2'?copafemMode2(oldG,oldS):copafemMode1(oldG,oldS);
  state.brackets={gold:built.gold,silver:built.silver};
  scheduleBrackets();
  return state.brackets;
}

// Orden de horarios/canchas de la Opción 3.
function copafemModeBracketBatches(event){
  const g=(event.brackets?.gold||[]).filter(copafemRealMatch);
  const s=(event.brackets?.silver||[]).filter(copafemRealMatch);
  const out=[];
  const add=(stage,matches)=>{if(matches.length)out.push({stage,matches});};
  const mode=event.tournament?.dropMode||'op1';

  if(mode==='op3'){
    add('Oro Octavos',g.filter(m=>m.round==='Octavos'));
    add('Plata Octavos',s.filter(m=>m.round==='Octavos'));
    add('Oro Cuartos',g.filter(m=>m.round==='Cuartos'));
    add('Plata Cuartos',s.filter(m=>m.round==='Cuartos'));
    add('Semifinal',[...g.filter(m=>m.round==='Semifinal'),...s.filter(m=>m.round==='Semifinal')]);
    add('Final',[...s.filter(m=>m.round==='Final'),...g.filter(m=>m.round==='Final')]);
    return out;
  }

  if(mode==='op1'){
    [...new Set(g.filter(m=>m.round!=='Final').map(m=>m.round))]
      .sort((a,b)=>copafemModeRoundRank(a)-copafemModeRoundRank(b))
      .forEach(r=>add('Oro '+r,g.filter(m=>m.round===r)));
    [...new Set(s.map(m=>m.round))]
      .sort((a,b)=>copafemModeRoundRank(a)-copafemModeRoundRank(b))
      .forEach(r=>add('Plata '+r,s.filter(m=>m.round===r)));
    add('Oro Final',g.filter(m=>m.round==='Final'));
  }else{
    add('Oro Octavos',g.filter(m=>m.round==='Octavos'));
    add('Oro Cuartos',g.filter(m=>m.round==='Cuartos'));
    [...new Set(g.filter(m=>String(m.round).startsWith('Ronda Oro')).map(m=>m.round))]
      .forEach(r=>add('Oro '+r,g.filter(m=>m.round===r)));
    add('Plata Cuartos',s.filter(m=>m.round==='Cuartos'));
    [...new Set(s.filter(m=>String(m.round).startsWith('Ronda Plata')).map(m=>m.round))]
      .forEach(r=>add('Plata '+r,s.filter(m=>m.round===r)));
    add('Semifinal',[...g.filter(m=>m.round==='Semifinal'),...s.filter(m=>m.round==='Semifinal')]);
    add('Final',[...s.filter(m=>m.round==='Final'),...g.filter(m=>m.round==='Final')]);
  }
  return out;
}

// Textos visibles de la nueva opción.
function copafemRefreshDropModeUI(){
  const mode=copafemDropMode(),sel=document.getElementById('dropFormatMode'),help=document.getElementById('dropFormatHelp');
  if(sel)sel.value=mode;
  const g=document.getElementById('goldRuleText'),p=document.getElementById('silverRuleText');
  if(mode==='op3'){
    if(g)g.textContent='Máximo cupo · 1.º y 2.º de cada zona juegan Octavos de Oro';
    if(p)p.textContent='3.º de cada zona + perdedores de Octavos de Oro juegan Octavos de Plata';
    if(help)help.innerHTML='<b>Opción 3 · Máximo cupo:</b> 1.º y 2.º pasan a Octavos de Oro. El 3.º pasa a Octavos de Plata. El que pierde en Octavos de Oro baja a Octavos de Plata. Desde Cuartos de Oro en adelante, el que pierde queda eliminado. En Plata, cualquier derrota elimina.';
  }else if(mode==='op2'){
    if(g)g.textContent='Los 3 clasifican a Oro · 2.º vs 3.º en Octavos · 1.º espera en Cuartos';
    if(p)p.textContent='Perdedor de Octavos de Oro vs perdedor de Cuartos de Oro';
    if(help)help.innerHTML='<b>Opción 2:</b> 2.º y 3.º juegan Octavos de Oro. El 1.º entra directo a Cuartos contra ese ganador. El perdedor del Octavo y el perdedor del Cuarto de Oro se enfrentan en Cuartos de Plata.';
  }else{
    if(g)g.textContent='1.º y 2.º de cada zona clasifican a Copa de Oro';
    if(p)p.textContent='3.º de cada zona + perdedores de Oro hasta Semifinal';
    if(help)help.innerHTML='<b>Opción 1:</b> 1.º y 2.º van a Oro; 3.º va a Plata. Todo el que pierde en Oro, desde la primera ronda y hasta Semifinal inclusive, entra al cuadro de Plata.';
  }
}
</script>
'''

if '</body>' not in s:
    raise SystemExit('No se encontró </body>')
head,tail=s.rsplit('</body>',1)
s=head+injection+'\n</body>'+tail
p.write_text(s,encoding='utf-8')
print('COPAFEM Opción 3 máximo cupo aplicada')
