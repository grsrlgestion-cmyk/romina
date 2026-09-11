from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_DROP_FORMAT_SELECTOR_V1'
if MARK in s:
    print('drop format selector already applied')
    raise SystemExit

# Selector visible en Oro / Plata.
needle='''      <div class="brackets-wrap">'''
selector=r'''
      <section class="drop-format-box" id="COPAFEM_DROP_FORMAT_SELECTOR_V1">
        <div class="drop-format-title">
          <div>
            <strong>Formato del Drop</strong>
            <span>Elegí cómo se clasifican las parejas de esta categoría.</span>
          </div>
          <select id="dropFormatMode" aria-label="Formato del Drop">
            <option value="op1">Opción 1 · 1.º y 2.º a Oro / 3.º a Plata + perdedores de Oro</option>
            <option value="op2">Opción 2 · Los 3 a Oro / 2.º vs 3.º y 1.º espera en Cuartos</option>
          </select>
        </div>
        <div class="drop-format-help" id="dropFormatHelp"></div>
      </section>
'''
if needle not in s:
    raise SystemExit('No se encontró brackets-wrap')
s=s.replace(needle,selector+needle,1)

# Textos de cabecera dinámicos.
s=s.replace('<div class="cup-title"><span class="cup">🏆</span><div><h3>Copa de Oro</h3><p>1.º y 2.º de cada zona · 16 parejas</p></div></div>',
            '<div class="cup-title"><span class="cup">🏆</span><div><h3>Copa de Oro</h3><p id="goldRuleText">1.º y 2.º de cada zona</p></div></div>',1)
s=s.replace('<div class="cup-title"><span class="cup">🥈</span><div><h3>Copa de Plata</h3><p>3.º de cada zona + perdedores de Octavos de Oro · 16 parejas</p></div></div>',
            '<div class="cup-title"><span class="cup">🥈</span><div><h3>Copa de Plata</h3><p id="silverRuleText">3.º de cada zona + perdedores de Oro</p></div></div>',1)

css=r'''
<style>
.drop-format-box{background:#fff;border:1px solid var(--line);border-radius:16px;padding:14px 16px;margin:0 0 14px;box-shadow:0 3px 14px rgba(20,25,35,.04)}
.drop-format-title{display:flex;align-items:center;justify-content:space-between;gap:16px}.drop-format-title strong{display:block;font-size:15px;color:var(--ink)}.drop-format-title span{display:block;margin-top:3px;font-size:12px;color:var(--muted)}
#dropFormatMode{min-width:460px;max-width:100%;border:1px solid #cad9e8;border-radius:12px;padding:10px 12px;background:#fff;color:var(--ink);font-weight:800}
.drop-format-help{margin-top:10px;padding:10px 12px;border-radius:12px;background:var(--cat-soft);color:var(--cat-ink);font-size:12px;line-height:1.45;font-weight:650}
@media(max-width:800px){.drop-format-title{align-items:flex-start;flex-direction:column}#dropFormatMode{min-width:0;width:100%}}
@media print{.drop-format-box{display:none!important}}
</style>
'''

helpers=r'''
<script>
// COPAFEM_DROP_FORMAT_SELECTOR_V1
function copafemDropMode(ev=state){return ev?.tournament?.dropMode||'op1';}
function copafemActiveZones(ev=state){return ZONES.filter(z=>(ev.zones?.[z]||[]).length>=3);}
function copafemZoneComplete(z){
  const ids=state.zones?.[z]||[];
  const ms=(state.zoneMatches||[]).filter(m=>m.zone===z);
  const expected=ids.length*(ids.length-1)/2;
  return ids.length>=3 && ms.length===expected && ms.every(m=>hasScore(m)&&m.s1!==m.s2);
}
function copafemSeedSource(z,pos){
  let value=null;
  if(copafemZoneComplete(z)) value=zoneStandings(z).rows[pos-1]?.id||null;
  return {key:`${pos}${z}`,value};
}
function copafemSource(key,value){return {key,value:value||null};}
function copafemNextPow2(n){let p=2;while(p<n)p*=2;return p;}
function copafemSeedOrder(n){let a=[1,2];while(a.length<n){const t=a.length*2+1;a=a.flatMap(x=>[x,t-x]);}return a;}
function copafemRoundName(size){return size>=32?'Dieciseisavos':size===16?'Octavos':size===8?'Cuartos':size===4?'Semifinal':'Final';}
function copafemRoundCode(name){return name==='Dieciseisavos'?'R32':name==='Octavos'?'R16':name==='Cuartos'?'QF':name==='Semifinal'?'SF':name==='Final'?'F':'R';}
function copafemMakeMatch(id,round,a,b,old){
  const p1=a?.value||null,p2=b?.value||null,prev=old[id],same=prev&&prev.p1===p1&&prev.p2===p2;
  return {id,round,p1,p2,s1:same?(prev.s1??null):null,s2:same?(prev.s2??null):null,time:null,court:null,dropFormat:true};
}
function copafemBuildBracket(prefix,sources,old,renameFirst=''){
  if(sources.length<2)return {matches:[],champion:sources[0]||null};
  const size=copafemNextPow2(sources.length),order=copafemSeedOrder(size),slots=order.map(k=>sources[k-1]||null),matches=[];
  let current=slots,n=size,first=true;
  while(n>=2){
    let round=copafemRoundName(n);
    if(first&&renameFirst) round=renameFirst;
    const next=[];
    for(let i=0;i<current.length;i+=2){
      const a=current[i],b=current[i+1];
      if(a&&b){
        const id=`${prefix}-${copafemRoundCode(copafemRoundName(n))}-${i/2+1}`;
        const m=copafemMakeMatch(id,round,a,b,old);matches.push(m);next.push(copafemSource(`W:${id}`,winnerId(m)));
      }else next.push(a||b||null);
    }
    current=next;n/=2;first=false;
  }
  return {matches,champion:current[0]||null};
}
function copafemMode1(oldG,oldS){
  const zones=copafemActiveZones();
  if(!zones.length)return {gold:[],silver:[]};
  const first=zones.map(z=>copafemSeedSource(z,1));
  const second=[...zones].reverse().map(z=>copafemSeedSource(z,2));
  const goldSources=[];
  for(let i=0;i<Math.max(first.length,second.length);i++){if(first[i])goldSources.push(first[i]);if(second[i])goldSources.push(second[i]);}
  const gb=copafemBuildBracket('G',goldSources,oldG);
  const silverSources=zones.map(z=>copafemSeedSource(z,3));
  // Todo perdedor de Oro entra a Plata, salvo el perdedor de la Final de Oro.
  gb.matches.filter(m=>m.round!=='Final').forEach(m=>silverSources.push(copafemSource(`L:${m.id}`,loserId(m))));
  const sb=copafemBuildBracket('S',silverSources,oldS);
  return {gold:gb.matches,silver:sb.matches};
}
function copafemMode2(oldG,oldS){
  const zones=copafemActiveZones();
  if(!zones.length)return {gold:[],silver:[]};
  const gold=[],silver=[],goldQFWinners=[],silverQFWinners=[];
  zones.forEach((z,i)=>{
    const r16=copafemMakeMatch(`G-R16-Z${z}`,'Octavos',copafemSeedSource(z,2),copafemSeedSource(z,3),oldG);gold.push(r16);
    const qf=copafemMakeMatch(`G-QF-Z${z}`,'Cuartos',copafemSeedSource(z,1),copafemSource(`W:${r16.id}`,winnerId(r16)),oldG);gold.push(qf);
    goldQFWinners.push(copafemSource(`W:${qf.id}`,winnerId(qf)));
    const sqf=copafemMakeMatch(`S-QF-Z${z}`,'Cuartos',copafemSource(`L:${r16.id}`,loserId(r16)),copafemSource(`L:${qf.id}`,loserId(qf)),oldS);silver.push(sqf);
    silverQFWinners.push(copafemSource(`W:${sqf.id}`,winnerId(sqf)));
  });
  const gt=copafemBuildBracket('G2',goldQFWinners,oldG,goldQFWinners.length>4?'Ronda Oro':'');
  const st=copafemBuildBracket('S2',silverQFWinners,oldS,silverQFWinners.length>4?'Ronda Plata':'');
  gold.push(...gt.matches);silver.push(...st.matches);
  return {gold,silver};
}
function copafemRebuildDropByMode(preserveScores=true){
  const oldG=preserveScores?Object.fromEntries((state.brackets?.gold||[]).map(m=>[m.id,m])):{};
  const oldS=preserveScores?Object.fromEntries((state.brackets?.silver||[]).map(m=>[m.id,m])):{};
  const built=copafemDropMode()==='op2'?copafemMode2(oldG,oldS):copafemMode1(oldG,oldS);
  state.brackets={gold:built.gold,silver:built.silver};
  scheduleBrackets();
  return state.brackets;
}
function copafemModeRoundRank(r){
  if(r==='Dieciseisavos')return 0;if(r==='Octavos')return 1;if(r==='Cuartos')return 2;
  if(String(r).startsWith('Ronda Oro')||String(r).startsWith('Ronda Plata'))return 2.5;
  if(r==='Semifinal')return 3;if(r==='Final')return 4;return 99;
}
function copafemModeBracketBatches(event){
  const g=(event.brackets?.gold||[]).filter(copafemRealMatch),s=(event.brackets?.silver||[]).filter(copafemRealMatch),out=[];
  const add=(stage,matches)=>{if(matches.length)out.push({stage,matches});};
  if((event.tournament?.dropMode||'op1')==='op1'){
    [...new Set(g.filter(m=>m.round!=='Final').map(m=>m.round))].sort((a,b)=>copafemModeRoundRank(a)-copafemModeRoundRank(b)).forEach(r=>add('Oro '+r,g.filter(m=>m.round===r)));
    [...new Set(s.map(m=>m.round))].sort((a,b)=>copafemModeRoundRank(a)-copafemModeRoundRank(b)).forEach(r=>add('Plata '+r,s.filter(m=>m.round===r)));
    add('Oro Final',g.filter(m=>m.round==='Final'));
  }else{
    add('Oro Octavos',g.filter(m=>m.round==='Octavos'));
    add('Oro Cuartos',g.filter(m=>m.round==='Cuartos'));
    [...new Set(g.filter(m=>String(m.round).startsWith('Ronda Oro')).map(m=>m.round))].forEach(r=>add('Oro '+r,g.filter(m=>m.round===r)));
    add('Plata Cuartos',s.filter(m=>m.round==='Cuartos'));
    [...new Set(s.filter(m=>String(m.round).startsWith('Ronda Plata')).map(m=>m.round))].forEach(r=>add('Plata '+r,s.filter(m=>m.round===r)));
    add('Semifinal',[...g.filter(m=>m.round==='Semifinal'),...s.filter(m=>m.round==='Semifinal')]);
    add('Final',[...s.filter(m=>m.round==='Final'),...g.filter(m=>m.round==='Final')]);
  }
  return out;
}
function copafemRefreshDropModeUI(){
  const mode=copafemDropMode(),sel=document.getElementById('dropFormatMode'),help=document.getElementById('dropFormatHelp');
  if(sel)sel.value=mode;
  const g=document.getElementById('goldRuleText'),p=document.getElementById('silverRuleText');
  if(mode==='op2'){
    if(g)g.textContent='Los 3 clasifican a Oro · 2.º vs 3.º en Octavos · 1.º espera en Cuartos';
    if(p)p.textContent='Perdedor de Octavos de Oro vs perdedor de Cuartos de Oro';
    if(help)help.innerHTML='<b>Opción 2:</b> 2.º y 3.º juegan Octavos de Oro. El 1.º entra directo a Cuartos contra ese ganador. El perdedor del Octavo y el perdedor del Cuarto de Oro se enfrentan en Cuartos de Plata.';
  }else{
    if(g)g.textContent='1.º y 2.º de cada zona clasifican a Copa de Oro';
    if(p)p.textContent='3.º de cada zona + perdedores de Oro hasta Semifinal';
    if(help)help.innerHTML='<b>Opción 1:</b> 1.º y 2.º van a Oro; 3.º va a Plata. Todo el que pierde en Oro, desde la primera ronda y hasta Semifinal inclusive, entra al cuadro de Plata.';
  }
}
document.addEventListener('change',e=>{
  if(e.target?.id!=='dropFormatMode')return;
  state.tournament.dropMode=e.target.value==='op2'?'op2':'op1';
  state.brackets={gold:[],silver:[]};
  copafemRebuildDropByMode(false);saveState();renderAll();copafemRefreshDropModeUI();
  toast(state.tournament.dropMode==='op2'?'Formato 2 aplicado':'Formato 1 aplicado');
});
</script>
'''

# Insertar helpers antes del cierre para que las funciones estén disponibles en tiempo de ejecución.
head,tail=s.rsplit('</body>',1)
s=head+css+helpers+'\n</body>'+tail

# Toda reconstrucción usa el formato seleccionado, incluso en torneos dinámicos.
old='''  function rebuildBrackets(preserveScores=true){\n    if(dynMode()) return rebuildDynamicBrackets(preserveScores);'''
new='''  function rebuildBrackets(preserveScores=true){\n    return copafemRebuildDropByMode(preserveScores);\n    if(dynMode()) return rebuildDynamicBrackets(preserveScores);'''
if old not in s:
    raise SystemExit('No se encontró rebuildBrackets post dynamic patch')
s=s.replace(old,new,1)

# Renderizar textos del selector cada vez que se muestran las copas.
old_render='''  function renderCups(){\n    if(!state.brackets.gold.length) rebuildBrackets(true); $("goldBracket").innerHTML=bracketHTML("gold",state.brackets.gold||[]); $("silverBracket").innerHTML=bracketHTML("silver",state.brackets.silver||[]); document.querySelectorAll("[data-bscore]").forEach(el=>el.addEventListener("change",e=>setBracketScore(e.target.dataset.kind,e.target.dataset.bscore,e.target.dataset.side,e.target.value)));\n  }'''
new_render='''  function renderCups(){\n    if(!state.brackets.gold.length) rebuildBrackets(true); $("goldBracket").innerHTML=bracketHTML("gold",state.brackets.gold||[]); $("silverBracket").innerHTML=bracketHTML("silver",state.brackets.silver||[]); document.querySelectorAll("[data-bscore]").forEach(el=>el.addEventListener("change",e=>setBracketScore(e.target.dataset.kind,e.target.dataset.bscore,e.target.dataset.side,e.target.value))); copafemRefreshDropModeUI();\n  }'''
if old_render not in s:
    raise SystemExit('No se encontró renderCups')
s=s.replace(old_render,new_render,1)

# El planificador debe respetar el orden especial de alimentación Oro -> Plata.
old_batches='''  function copafemBracketBatches(event){\n    const batches=[];'''
new_batches='''  function copafemBracketBatches(event){\n    if(typeof copafemModeBracketBatches==='function') return copafemModeBracketBatches(event);\n    const batches=[];'''
if old_batches not in s:
    raise SystemExit('No se encontró copafemBracketBatches')
s=s.replace(old_batches,new_batches,1)

# Reconocer todas las rondas nuevas en el orden general.
s=s.replace("return ({'Octavos':1,'Cuartos':2,'Semifinal':3,'Final':4})[name]||99;",
            "return ({'Dieciseisavos':0,'Octavos':1,'Cuartos':2,'Ronda Oro':2.5,'Ronda Plata':2.5,'Semifinal':3,'Final':4})[name]||99;",1)

p.write_text(s,encoding='utf-8')
print('COPAFEM: selector de formato de Drop aplicado')
