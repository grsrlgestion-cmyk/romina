from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_NO_REMATCH_ALL_MODES_V1'
if MARK in s:
    print('no-rematch all modes already applied')
    raise SystemExit

patch=r'''
<script id="COPAFEM_NO_REMATCH_ALL_MODES_V1">
// Regla general COPAFEM: en cualquier formato, priorizar cruces entre parejas
// que no se hayan enfrentado antes. Las parejas de una misma zona se mantienen
// en ramas diferentes siempre que exista una combinación posible.

function copafemPairZone(id){
  const pid=String(id||'');
  if(!pid || pid.startsWith('__TBD__')) return '';
  for(const z of ZONES){
    if((state.zones?.[z]||[]).includes(pid)) return z;
  }
  return '';
}

function copafemAlreadyPlayed(a,b){
  if(!a||!b||a===b) return a===b;
  const same=(m)=>((m.p1===a&&m.p2===b)||(m.p1===b&&m.p2===a));
  // En zona, pertenecer a la misma zona ya implica que se enfrentaron entre sí.
  const za=copafemPairZone(a),zb=copafemPairZone(b);
  if(za&&za===zb) return true;
  // También evitar revanchas de partidos ya disputados en Oro/Plata.
  return [...(state.zoneMatches||[]),...(state.brackets?.gold||[]),...(state.brackets?.silver||[])]
    .some(m=>same(m)&&hasScore(m)&&m.s1!==m.s2);
}

function copafemFindMatchForSource(id,pool=[]){
  return pool.find(m=>m.id===id)
    || (state.brackets?.gold||[]).find(m=>m.id===id)
    || (state.brackets?.silver||[]).find(m=>m.id===id)
    || null;
}

function copafemSourceZones(src,pool=[],seen=new Set()){
  if(!src) return new Set();
  if(src.value){
    const z=copafemPairZone(src.value);
    return z?new Set([z]):new Set();
  }
  const key=String(src.key||'');
  const direct=key.match(/^[1-9]([A-Z])$/);
  if(direct) return new Set([direct[1]]);
  const flow=key.match(/^[WL]:(.+)$/);
  if(!flow||seen.has(flow[1])) return new Set();
  seen.add(flow[1]);
  const m=copafemFindMatchForSource(flow[1],pool);
  if(!m) return new Set();
  const out=new Set();
  const s1={key:m.source1||'',value:m.p1||null};
  const s2={key:m.source2||'',value:m.p2||null};
  for(const z of copafemSourceZones(s1,pool,new Set(seen))) out.add(z);
  for(const z of copafemSourceZones(s2,pool,new Set(seen))) out.add(z);
  return out;
}

function copafemSourceConflict(a,b,pool=[]){
  if(!a||!b) return 0;
  if(a.value&&b.value){
    if(a.value===b.value) return 100000;
    if(copafemAlreadyPlayed(a.value,b.value)) return 10000;
  }
  const za=copafemSourceZones(a,pool),zb=copafemSourceZones(b,pool);
  let overlap=0;
  za.forEach(z=>{if(zb.has(z)) overlap++;});
  return overlap?1000+overlap:0;
}

function copafemBestRightOrder(left,right,pool=[]){
  const n=Math.min(left.length,right.length);
  if(n<=1) return right.slice();
  if(n>12){
    const remaining=right.slice(),out=[];
    left.forEach(a=>{
      let bi=0,best=Infinity;
      remaining.forEach((b,i)=>{const c=copafemSourceConflict(a,b,pool);if(c<best){best=c;bi=i;}});
      out.push(remaining.splice(bi,1)[0]);
    });
    return out;
  }
  const memo=new Map();
  function dp(i,mask){
    if(i===n) return {cost:0,order:[]};
    const k=i+'|'+mask;
    if(memo.has(k)) return memo.get(k);
    let best={cost:Infinity,order:[]};
    for(let j=0;j<n;j++){
      if(mask&(1<<j)) continue;
      const tail=dp(i+1,mask|(1<<j));
      const cost=copafemSourceConflict(left[i],right[j],pool)+tail.cost;
      if(cost<best.cost) best={cost,order:[right[j],...tail.order]};
    }
    memo.set(k,best);return best;
  }
  return dp(0,0).order;
}

function copafemMakeSafeStage(prefix,round,left,right,old,pool=[]){
  const n=Math.min(left.length,right.length);
  const ordered=copafemBestRightOrder(left.slice(0,n),right.slice(0,n),pool);
  const matches=[];
  for(let i=0;i<n;i++){
    matches.push(copafemMakeMatch(`${prefix}-${i+1}`,round,left[i],ordered[i],old));
  }
  return matches;
}

function copafemSafeElimination(prefix,sources,old,pool=[],forcedFirstRound=''){
  let current=sources.filter(Boolean).slice();
  const matches=[];
  let first=true,roundNo=0;
  while(current.length>1){
    roundNo++;
    const count=current.length;
    const round=first&&forcedFirstRound?forcedFirstRound:copafemRoundName(copafemNextPow2(count));
    let bye=null;
    if(current.length%2===1) bye=current.shift();
    const half=current.length/2;
    const left=current.slice(0,half),right=current.slice(half);
    const stage=copafemMakeSafeStage(`${prefix}-${copafemRoundCode(round)}${roundNo}`,round,left,right,old,[...pool,...matches]);
    const next=[];
    if(bye) next.push(bye);
    stage.forEach(m=>next.push(copafemSource(`W:${m.id}`,winnerId(m))));
    matches.push(...stage);
    current=next;
    first=false;
  }
  return {matches,champion:current[0]||null};
}

// OPCIÓN 1: 1.º y 2.º a Oro; 3.º + perdedores de Oro a Plata.
function copafemMode1(oldG,oldS){
  const zones=copafemActiveZones();
  if(!zones.length) return {gold:[],silver:[]};
  const goldSources=[...zones.map(z=>copafemSeedSource(z,1)),...zones.map(z=>copafemSeedSource(z,2))];
  const gb=copafemSafeElimination('G1',goldSources,oldG,[]);
  const silverSources=[...zones.map(z=>copafemSeedSource(z,3))];
  gb.matches.filter(m=>m.round!=='Final').forEach(m=>silverSources.push(copafemSource(`L:${m.id}`,loserId(m))));
  const sb=copafemSafeElimination('S1',silverSources,oldS,gb.matches);
  return {gold:gb.matches,silver:sb.matches};
}

// OPCIÓN 2: 2.º vs 3.º de otra zona; 1.º espera en Cuartos.
// La Plata se vuelve a cruzar entre ramas para evitar revancha del Octavo de Oro.
function copafemMode2(oldG,oldS){
  const zones=copafemActiveZones();
  if(!zones.length) return {gold:[],silver:[]};
  const seconds=zones.map(z=>copafemSeedSource(z,2));
  const thirds=zones.map(z=>copafemSeedSource(z,3));
  const r16=copafemMakeSafeStage('G2-R16','Octavos',seconds,thirds,oldG,[]);
  const r16W=r16.map(m=>copafemSource(`W:${m.id}`,winnerId(m)));
  const firsts=zones.map(z=>copafemSeedSource(z,1));
  const qf=copafemMakeSafeStage('G2-QF','Cuartos',firsts,r16W,oldG,r16);
  const qfW=qf.map(m=>copafemSource(`W:${m.id}`,winnerId(m)));
  const tail=copafemSafeElimination('G2T',qfW,oldG,[...r16,...qf]);
  const gold=[...r16,...qf,...tail.matches];

  const silverSources=[
    ...r16.map(m=>copafemSource(`L:${m.id}`,loserId(m))),
    ...qf.map(m=>copafemSource(`L:${m.id}`,loserId(m)))
  ];
  const sb=copafemSafeElimination('S2',silverSources,oldS,gold);
  return {gold,silver:sb.matches};
}

// OPCIÓN 3: 1.º y 2.º a Oro; 3.º + perdedores del primer cruce de Oro a Plata.
function copafemMode3(oldG,oldS){
  const zones=copafemActiveZones();
  if(!zones.length) return {gold:[],silver:[]};
  const goldSources=[...zones.map(z=>copafemSeedSource(z,1)),...zones.map(z=>copafemSeedSource(z,2))];
  const gb=copafemSafeElimination('G3',goldSources,oldG,[]);
  const firstRound=gb.matches[0]?.round;
  const goldFirst=gb.matches.filter(m=>m.round===firstRound);
  const silverSources=[
    ...zones.map(z=>copafemSeedSource(z,3)),
    ...goldFirst.map(m=>copafemSource(`L:${m.id}`,loserId(m)))
  ];
  const sb=copafemSafeElimination('S3',silverSources,oldS,gb.matches);
  return {gold:gb.matches,silver:sb.matches};
}

function copafemRebuildDropByMode(preserveScores=true){
  const oldG=preserveScores?Object.fromEntries((state.brackets?.gold||[]).map(m=>[m.id,m])):{};
  const oldS=preserveScores?Object.fromEntries((state.brackets?.silver||[]).map(m=>[m.id,m])):{};
  const mode=copafemDropMode();
  const built=mode==='op3'?copafemMode3(oldG,oldS):mode==='op2'?copafemMode2(oldG,oldS):copafemMode1(oldG,oldS);
  state.brackets={gold:built.gold,silver:built.silver};
  scheduleBrackets();
  return state.brackets;
}
</script>
'''

head,tail=s.rsplit('</body>',1)
s=head+patch+'\n</body>'+tail
p.write_text(s,encoding='utf-8')
print('COPAFEM: regla sin revanchas aplicada a las 3 opciones del Drop')
