from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARKER='COPAFEM_VISIBLE_FUTURE_CUP_MATCHES_V1'
if MARKER in s:
    print('future cup matches already applied')
    raise SystemExit

start=s.find('  function rebuildDynamicBrackets(preserveScores=true){')
end=s.find('  function renderZonesDynamic(){', start)
if start<0 or end<0:
    raise SystemExit('No se encontró rebuildDynamicBrackets')

new_func=r'''  function rebuildDynamicBrackets(preserveScores=true){
    const zones=dynZones();
    if(!zones.length){state.brackets={gold:[],silver:[]};return}

    const q=dynQualifiers(),oldG=Object.fromEntries((state.brackets.gold||[]).map(m=>[m.id,m])),oldS=Object.fromEntries((state.brackets.silver||[]).map(m=>[m.id,m]));
    const pow=n=>{let x=2;while(x<n)x*=2;return Math.min(16,x)},ord=n=>{let a=[1,2];while(a.length<n){const t=a.length*2+1;a=a.flatMap(x=>[x,t-x])}return a},rn=n=>n>=16?'Octavos':n===8?'Cuartos':n===4?'Semifinal':'Final',rc=n=>n==='Octavos'?'R16':n==='Cuartos'?'QF':n==='Semifinal'?'SF':'F';
    const tbd=label=>`__TBD__${label}`;
    const win=m=>!m?null:m.bye?(m.p1||m.p2):winnerId(m);
    const mk=(id,round,p1,p2,old,bye=false)=>{const x=old[id],same=x&&x.p1===p1&&x.p2===p2;return{id,round,p1,p2,bye,dynamic:true,s1:preserveScores&&same&&!bye?(x.s1??null):null,s2:preserveScores&&same&&!bye?(x.s2??null):null,time:null,court:null}};
    const build=(pre,ids,old)=>{if(ids.length<2)return[];const size=pow(ids.length),slots=ord(size).map(k=>ids[k-1]||null),out=[];let n=size,prev=[];while(n>=2){const round=rn(n),cur=[];for(let i=0;i<n/2;i++){const p1=prev.length?win(prev[2*i]):slots[2*i],p2=prev.length?win(prev[2*i+1]):slots[2*i+1],bye=!prev.length&&!!((p1&&!p2)||(p2&&!p1)),m=mk(`${pre}-${rc(round)}-${i+1}`,round,p1,p2,old,bye);out.push(m);cur.push(m)}prev=cur;n/=2}return out};

    // ORO: dos lugares por cada zona. Si la zona todavía no terminó,
    // reservamos el lugar con A definir para que horario y cancha ya sean visibles.
    const goldByKey=new Map(q.gold.map(x=>[`${x.pos}${x.zone}`,x.id]));
    const goldIds=[
      ...zones.map(z=>goldByKey.get(`1${z}`)||tbd(`G-1-${z}`)),
      ...zones.map(z=>goldByKey.get(`2${z}`)||tbd(`G-2-${z}`))
    ];
    state.brackets.gold=build('G',goldIds,oldG);

    // PLATA: todos los puestos desde 3.º en adelante + perdedores de la primera
    // ronda real de Oro. Esos lugares también se reservan aunque aún no tengan nombre.
    const silverByKey=new Map(q.silver.map(x=>[`${x.pos}${x.zone}`,x.id]));
    const silverIds=[];
    zones.forEach(z=>{
      const count=(state.zones[z]||[]).length;
      for(let pos=3;pos<=count;pos++) silverIds.push(silverByKey.get(`${pos}${z}`)||tbd(`S-${pos}-${z}`));
    });
    const firstRound=state.brackets.gold[0]?.round;
    const goldFirst=(state.brackets.gold||[]).filter(m=>m.round===firstRound&&!m.bye);
    goldFirst.forEach((m,i)=>silverIds.push(loserId(m)||tbd(`S-GL-${i+1}`)));
    state.brackets.silver=build('S',silverIds,oldS);

    scheduleBrackets();
  }

'''
s=s[:start]+new_func+s[end:]

# Los IDs internos __TBD__ se muestran siempre como "A definir".
s=s.replace(
    'const pairName = (id) => state.pairs.find(p => p.id === id)?.name || "—";',
    'const pairName = (id) => String(id||"").startsWith("__TBD__") ? "A definir" : (state.pairs.find(p => p.id === id)?.name || "—");',
    1
)
s=s.replace(
    'function pairName(ev,id){return ev?.pairs?.find(p=>p.id===id)?.name||"A definir";}',
    'function pairName(ev,id){return String(id||"").startsWith("__TBD__")?"A definir":(ev?.pairs?.find(p=>p.id===id)?.name||"A definir");}',
    1
)

# En la Copa, A definir no habilita carga de resultado.
old='''  function bracketTeam(kind,m,pSide,sSide){\n    const id=m[pSide],name=id?pairName(id):"A definir";return `<div class="bracket-team"><span class="${id?"":"placeholder"}">${esc(name)}</span><input type="number" min="0" inputmode="numeric" ${id?"":"disabled"} value="${m[sSide]??""}" data-kind="${kind}" data-bscore="${m.id}" data-side="${sSide}"></div>`;\n  }'''
new='''  function bracketTeam(kind,m,pSide,sSide){\n    const id=m[pSide],real=!!id&&!String(id).startsWith("__TBD__"),name=real?pairName(id):"A definir";return `<div class="bracket-team"><span class="${real?"":"placeholder"}">${esc(name)}</span><input type="number" min="0" inputmode="numeric" ${real?"":"disabled"} value="${real?(m[sSide]??""):""}" data-kind="${kind}" data-bscore="${m.id}" data-side="${sSide}"></div>`;\n  }'''
if old not in s:
    raise SystemExit('No se encontró bracketTeam')
s=s.replace(old,new,1)

# No dibujar BYE como partido en Oro/Plata; sí mantener las rondas futuras reales.
s=s.replace(
    'matches.filter(m=>m.round===r).map(m=>`<div class="bracket-match">',
    'matches.filter(m=>m.round===r && !m.bye).map(m=>`<div class="bracket-match">',
    1
)

# En el Drop completo, los placeholders internos también dicen A definir.
s=s.replace(
    '${esc(m.p1?pairName(m.p1):"A definir")}',
    '${esc(m.p1&&!String(m.p1).startsWith("__TBD__")?pairName(m.p1):"A definir")}',
    1
)
s=s.replace(
    '${esc(m.p2?pairName(m.p2):"A definir")}',
    '${esc(m.p2&&!String(m.p2).startsWith("__TBD__")?pairName(m.p2):"A definir")}',
    1
)

# Marcador para futuras publicaciones.
style='''\n<style id="COPAFEM_VISIBLE_FUTURE_CUP_MATCHES_V1">\n  .bracket-team .placeholder{font-style:italic;color:#8b96a6!important}\n</style>\n'''
head,tail=s.rsplit('</body>',1)
s=head+style+'\n</body>'+tail
p.write_text(s,encoding='utf-8')
print('COPAFEM future Oro/Plata matches visible with schedule')
