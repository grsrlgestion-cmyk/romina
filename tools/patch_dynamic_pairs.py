from pathlib import Path
p=Path('index.html'); s=p.read_text(encoding='utf-8')
if 'COPAFEM_DYNAMIC_PAIRS_V1' in s:
    print('dynamic pairs already applied'); raise SystemExit

helpers=r'''
  // COPAFEM_DYNAMIC_PAIRS_V1 — soporte 6 a 23 parejas (24 conserva formato original)
  const dynMode=()=>state.pairs.length>=6&&state.pairs.length<24;
  const dynZones=()=>ZONES.filter(z=>(state.zones[z]||[]).length);
  const dynExpected=(z)=>{const n=(state.zones[z]||[]).length;return n*(n-1)/2;};
  function dynRoundRobin(ids){const a=[...ids];if(a.length%2)a.push(null);const out=[];for(let r=0;r<a.length-1;r++){const ps=[];for(let i=0;i<a.length/2;i++){const x=a[i],y=a[a.length-1-i];if(x&&y)ps.push([x,y]);}out.push(ps);a.splice(1,0,a.pop());}return out;}
  function generateZonesDynamic(){
    const n=state.pairs.length;if(n<6||n>=24)return false;
    const fours=n%3===1?1:(n%3===2?2:0),threes=(n-4*fours)/3,sizes=[...Array(threes).fill(3),...Array(fours).fill(4)],zn=ZONES.slice(0,sizes.length),ids=state.pairs.map(p=>p.id),az=Object.fromEntries(ZONES.map(z=>[z,[]]));
    let c=0,r=0;while(c<ids.length){const o=[...zn.keys()];if(r++%2)o.reverse();for(const i of o){if(c>=ids.length)break;if(az[zn[i]].length<sizes[i])az[zn[i]].push(ids[c++]);}}
    state.zones=az;state.zoneMatches=[];zn.forEach(z=>dynRoundRobin(az[z]).forEach((ps,rr)=>ps.forEach((ab,k)=>state.zoneMatches.push({id:`Z${z}-${rr+1}-${k+1}`,zone:z,zoneRound:rr+1,p1:ab[0],p2:ab[1],s1:null,s2:null,court:null,time:null}))));
    generateScheduleDynamic();rebuildDynamicBrackets(false);saveState();renderAll();setView('zonas');toast(`${zn.length} zonas generadas · ${threes} de 3${fours?` · ${fours} de 4`:''}`);return true;
  }
  function generateScheduleDynamic(){
    if(!state.zoneMatches.length)return;const courts=state.tournament.courts;if(!courts.length)return toast('Configurá al menos una cancha');const base=parseTime(state.tournament.startTime),dur=state.tournament.duration,rs=[...new Set(state.zoneMatches.map(m=>m.zoneRound||1))].sort((a,b)=>a-b);let slot=0;
    rs.forEach(r=>{const ms=state.zoneMatches.filter(m=>(m.zoneRound||1)===r).sort((a,b)=>ZONES.indexOf(a.zone)-ZONES.indexOf(b.zone)||a.id.localeCompare(b.id));ms.forEach((m,i)=>{const q=Math.floor(i/courts.length);m.court=courts[i%courts.length];m.time=fmtTime(base+(slot+q)*dur)});slot+=Math.ceil(ms.length/courts.length)});scheduleBrackets();saveState();
  }
  function dynQualifiers(){const gold=[],silver=[];dynZones().forEach(z=>{const ms=state.zoneMatches.filter(m=>m.zone===z),st=zoneStandings(z);if(ms.length===dynExpected(z)&&ms.every(m=>hasScore(m)&&m.s1!==m.s2)&&st.rows.length>=3){gold.push({zone:z,pos:1,id:st.rows[0].id},{zone:z,pos:2,id:st.rows[1].id});st.rows.slice(2).forEach((x,i)=>silver.push({zone:z,pos:i+3,id:x.id}))}});return{gold,silver};}
  function rebuildDynamicBrackets(preserveScores=true){
    const zones=dynZones();if(!zones.length){state.brackets={gold:[],silver:[]};return}if(!zones.every(z=>state.zoneMatches.filter(m=>m.zone===z).length===dynExpected(z)&&state.zoneMatches.filter(m=>m.zone===z).every(m=>hasScore(m)&&m.s1!==m.s2))){state.brackets={gold:[],silver:[]};return}
    const q=dynQualifiers(),oldG=Object.fromEntries((state.brackets.gold||[]).map(m=>[m.id,m])),oldS=Object.fromEntries((state.brackets.silver||[]).map(m=>[m.id,m]));
    const pow=n=>{let x=2;while(x<n)x*=2;return Math.min(16,x)},ord=n=>{let a=[1,2];while(a.length<n){const t=a.length*2+1;a=a.flatMap(x=>[x,t-x])}return a},rn=n=>n>=16?'Octavos':n===8?'Cuartos':n===4?'Semifinal':'Final',rc=n=>n==='Octavos'?'R16':n==='Cuartos'?'QF':n==='Semifinal'?'SF':'F';
    const win=m=>!m?null:m.bye?(m.p1||m.p2):winnerId(m),mk=(id,round,p1,p2,old,bye=false)=>{const x=old[id],same=x&&x.p1===p1&&x.p2===p2;return{id,round,p1,p2,bye,dynamic:true,s1:preserveScores&&same&&!bye?(x.s1??null):null,s2:preserveScores&&same&&!bye?(x.s2??null):null,time:null,court:null}},build=(pre,ids,old)=>{if(ids.length<2)return[];const size=pow(ids.length),slots=ord(size).map(k=>ids[k-1]||null),out=[];let n=size,prev=[];while(n>=2){const round=rn(n),cur=[];for(let i=0;i<n/2;i++){const p1=prev.length?win(prev[2*i]):slots[2*i],p2=prev.length?win(prev[2*i+1]):slots[2*i+1],bye=!prev.length&&!!((p1&&!p2)||(p2&&!p1)),m=mk(`${pre}-${rc(round)}-${i+1}`,round,p1,p2,old,bye);out.push(m);cur.push(m)}prev=cur;n/=2}return out};
    const first=q.gold.filter(x=>x.pos===1).sort((a,b)=>ZONES.indexOf(a.zone)-ZONES.indexOf(b.zone)),second=q.gold.filter(x=>x.pos===2).sort((a,b)=>ZONES.indexOf(a.zone)-ZONES.indexOf(b.zone));state.brackets.gold=build('G',[...first,...second].map(x=>x.id),oldG);
    const fr=state.brackets.gold[0]?.round,real=state.brackets.gold.filter(m=>m.round===fr&&m.p1&&m.p2);if(real.every(m=>hasScore(m)&&m.s1!==m.s2)){state.brackets.silver=build('S',[...q.silver.map(x=>x.id),...real.map(loserId).filter(Boolean)],oldS)}else state.brackets.silver=[];scheduleBrackets();
  }
  function renderZonesDynamic(){const zs=dynZones();$('zonesGrid').innerHTML=zs.map(z=>{const ids=state.zones[z]||[];return `<article class="zone-card"><div class="zone-head"><span>ZONA ${z}</span><span>${ids.length} parejas</span></div>${ids.map((id,i)=>`<div class="zone-pair"><b>${i+1}.</b> ${esc(pairName(id))}</div>`).join('')}</article>`}).join('')||`<article class="panel"><p class="muted">Cargá entre 6 y 24 parejas y generá las zonas.</p></article>`;}
  function renderResultsDynamic(){if(!state.zoneMatches.length){$('resultsContainer').innerHTML=`<article class="panel"><p class="muted">Primero generá las zonas.</p></article>`;return}const zs=dynZones();$('resultsContainer').innerHTML=zs.map(z=>{const ms=state.zoneMatches.filter(m=>m.zone===z),st=zoneStandings(z);return `<article class="zone-block"><div class="zone-block-head"><h3>Zona ${z}</h3><span class="counter">${ms.filter(m=>hasScore(m)&&m.s1!==m.s2).length}/${ms.length}</span></div>${ms.map(m=>`<div class="match-grid"><div class="team-name">${esc(pairName(m.p1))}</div><div class="score-box"><input inputmode="numeric" min="0" type="number" value="${m.s1??''}" data-zscore="${m.id}" data-side="s1"><b>–</b><input inputmode="numeric" min="0" type="number" value="${m.s2??''}" data-zscore="${m.id}" data-side="s2"></div><div class="team-name">${esc(pairName(m.p2))}</div><div class="schedule-meta">${m.time||'--:--'} · Cancha ${m.court??'—'}</div></div>`).join('')}${standingsHTML(st)}</article>`}).join('');document.querySelectorAll('[data-zscore]').forEach(el=>el.addEventListener('change',e=>setZoneScore(e.target.dataset.zscore,e.target.dataset.side,e.target.value)))}
'''
marker='  function generateZones(){'
s=s.replace(marker,helpers+'\n'+marker,1)
s=s.replace('  function generateZones(){\n    if(state.pairs.length!==24) return toast("Necesitás exactamente 24 parejas");','  function generateZones(){\n    if(dynMode()) return generateZonesDynamic();\n    if(state.pairs.length!==24) return toast("Cargá entre 6 y 24 parejas");',1)
s=s.replace('  function generateSchedule(requireZones=true){\n    if(requireZones && state.zoneMatches.length!==24) return toast("Primero generá las zonas");','  function generateSchedule(requireZones=true){\n    if(dynMode()) return generateScheduleDynamic();\n    if(requireZones && state.zoneMatches.length!==24) return toast("Primero generá las zonas");',1)
s=s.replace('  function qualifiers(){\n    const gold=[], silver=[];','  function qualifiers(){\n    if(dynMode()) return dynQualifiers();\n    const gold=[], silver=[];',1)
s=s.replace('  function rebuildBrackets(preserveScores=true){\n    const s=seedMap();','  function rebuildBrackets(preserveScores=true){\n    if(dynMode()) return rebuildDynamicBrackets(preserveScores);\n    const s=seedMap();',1)
s=s.replace('  function renderZones(){\n    $("zonesGrid")','  function renderZones(){\n    if(dynMode()) return renderZonesDynamic();\n    $("zonesGrid")',1)
s=s.replace('  function renderResults(){\n    if(!state.zoneMatches.length)','  function renderResults(){\n    if(dynMode()) return renderResultsDynamic();\n    if(!state.zoneMatches.length)',1)
s=s.replace('  function renderHeader(){\n    $("heroCategory")','  function renderHeader(){\n    if(dynMode()){const q=dynQualifiers(),done=state.zoneMatches.filter(m=>hasScore(m)&&m.s1!==m.s2).length;$("statPairs").textContent=String(state.pairs.length);$("statZoneMatches").textContent=state.zoneMatches.length?`${done}/${state.zoneMatches.length}`:"0";$("statGold").textContent=`${q.gold.length}/${dynZones().length*2}`;$("statSilver").textContent=String(q.silver.length);}\n    $("heroCategory")',1)
s=s.replace('    $("statPairs").textContent=`${state.pairs.length}/24`; const done=state.zoneMatches.filter', '    if(!dynMode()) $("statPairs").textContent=`${state.pairs.length}/24`; const done=state.zoneMatches.filter',1)
s=s.replace('$("statZoneMatches").textContent=`${done}/24`;', 'if(!dynMode()) $("statZoneMatches").textContent=`${done}/24`;',1)
s=s.replace('    $("pairCounter").textContent=$("statPairs").textContent=`${state.pairs.length}/24`;', '    $("pairCounter").textContent=dynMode()?`${state.pairs.length} parejas`:`${state.pairs.length}/24`; if(!dynMode()) $("statPairs").textContent=`${state.pairs.length}/24`;',1)
s=s.replace('${isMine?"TU ZONA":"3 PAREJAS"}','${isMine?"TU ZONA":`${(ev.zones?.[zone]||[]).length} PAREJAS`}')
s=s.replace('<span>8 zonas · 3 parejas</span>','<span>${zones.length} zonas</span>')
s=s.replace('Cargá 24 parejas, generá 8 zonas de 3, registrá resultados y la app arma automáticamente posiciones, Copa de Oro y Copa de Plata.','Cargá entre 6 y 24 parejas. La app arma zonas automáticamente y luego calcula posiciones, Copa de Oro y Copa de Plata.')
s=s.replace('Automatizado para 24 parejas.','Automatizado para 6 a 24 parejas.')
s=s.replace('Generar 8 zonas de 3','Generar zonas automáticamente')
s=s.replace('Para cada categoría, elegí sus canchas, cargá las 24 parejas y generá las zonas.','Para cada categoría, elegí sus canchas, cargá entre 6 y 24 parejas y generá las zonas.')
p.write_text(s,encoding='utf-8');print('COPAFEM dynamic pairs patch OK')
