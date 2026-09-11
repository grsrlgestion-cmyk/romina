from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

MARKER = 'COPAFEM_DROP_SCHEDULE_V1'
if MARKER in s:
    print('drop schedule already applied')
    raise SystemExit

injection = r'''
<style id="COPAFEM_DROP_SCHEDULE_V1">
  .drop-match-head.copafem-drop-schedule{
    justify-content:center;
    align-items:center;
    text-align:center;
    font-size:8px;
    font-weight:950;
    letter-spacing:.02em;
    white-space:nowrap;
    min-height:18px;
  }
  .drop-match-head.copafem-drop-schedule span{width:100%;text-align:center}
</style>
<script>
(() => {
  const norm=s=>String(s||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');

  function sheetCourts(sheet){
    const t=sheet.querySelector('.drop-block-title')?.textContent||'';
    const m=t.match(/Canchas\s+([0-9, ]+)/i);
    const parsed=m?m[1].split(',').map(x=>Number(x.trim())).filter(Number.isFinite):[];
    if(parsed.length)return parsed;
    const cat=(t.match(/·\s*(7ma|8va)\s*·/i)||[])[1]?.toLowerCase();
    return cat==='8va'?[2,4,6,8]:[1,3,5,7];
  }

  function plan(cup,round,courts){
    const c=(i)=>courts[i%Math.max(courts.length,1)] ?? '—';
    const mk=(time,court)=>({time,court});
    if(cup==='gold'){
      if(round==='octavos') return Array.from({length:8},(_,i)=>mk(i<4?'13:00':'13:30',c(i)));
      if(round==='cuartos') return Array.from({length:4},(_,i)=>mk('14:00',c(i)));
      if(round==='semifinal') return Array.from({length:2},(_,i)=>mk('15:00',c(i)));
      if(round==='final') return [mk('15:30',c(0))];
    }
    if(cup==='silver'){
      if(round==='cuartos') return Array.from({length:4},(_,i)=>mk('14:30',c(i)));
      if(round==='semifinal') return Array.from({length:2},(_,i)=>mk('15:00',c(i+2)));
      if(round==='final') return [mk('15:30',c(1))];
      if(round==='octavos') return [];
    }
    return [];
  }

  function roundName(text){
    const t=norm(text);
    if(t.includes('octavos'))return'octavos';
    if(t.includes('cuartos'))return'cuartos';
    if(t.includes('semi'))return'semifinal';
    if(t.includes('final'))return'final';
    return'';
  }

  function slotText(slot){return slot.time+' · Cancha '+slot.court;}

  function placeholder(slot){
    const el=document.createElement('div');
    el.className='drop-match';
    el.dataset.copafemPlanned='1';
    el.innerHTML='<div class="drop-match-head copafem-drop-schedule"><span>'+slotText(slot)+'</span></div>'+
      '<div class="drop-match-team"><span>A definir</span><b>—</b></div>'+
      '<div class="drop-match-team"><span>A definir</span><b>—</b></div>';
    return el;
  }

  function normalizeExistingHeader(match,slot){
    let head=match.querySelector('.drop-match-head');
    if(!head && slot){
      head=document.createElement('div');
      head.className='drop-match-head copafem-drop-schedule';
      match.insertBefore(head,match.firstChild);
    }
    if(!head)return;
    const spans=[...head.querySelectorAll('span')];
    let raw=spans.length>1?spans[spans.length-1].textContent.trim():head.textContent.trim();
    raw=raw.replace(/\s*·\s*C(?:ancha\s*)?/i,' · Cancha ');
    const hasTime=/\b\d{1,2}:\d{2}\b/.test(raw);
    const hasCourt=/Cancha\s*\d+/i.test(raw);
    const value=(hasTime&&hasCourt)?raw:(slot?slotText(slot):raw||'Horario a definir · Cancha —');
    head.classList.add('copafem-drop-schedule');
    if(head.children.length!==1 || head.firstElementChild?.tagName!=='SPAN' || head.textContent.trim()!==value){
      head.innerHTML='<span>'+value+'</span>';
    }
  }

  function plannedMatchesOK(matches,slots){
    if(matches.length!==slots.length)return false;
    return matches.every((m,i)=>m.dataset.copafemPlanned==='1' && m.querySelector('.copafem-drop-schedule')?.textContent.trim()===slotText(slots[i]));
  }

  function decorate(){
    document.querySelectorAll('.drop-category-sheet').forEach(sheet=>{
      const courts=sheetCourts(sheet);
      sheet.querySelectorAll('.drop-round-col').forEach(col=>{
        const title=col.querySelector('.drop-round-title');
        if(!title)return;
        const t=norm(title.textContent);
        const cup=t.includes('plata')||title.classList.contains('silver')?'silver':'gold';
        const round=roundName(t);
        const slots=plan(cup,round,courts);
        let matches=[...col.querySelectorAll(':scope > .drop-match')];
        const real=matches.filter(m=>!m.dataset.copafemPlanned && m.querySelector('.drop-match-head'));

        if(real.length){
          matches.filter(m=>m.dataset.copafemPlanned).forEach(m=>m.remove());
          real.forEach((m,i)=>normalizeExistingHeader(m,slots[i]));
          if(col.style.display==='none')col.style.display='';
          return;
        }

        const generic=matches.length===1 && !matches[0].querySelector('.drop-match-head');
        const allPlanned=matches.length>0 && matches.every(m=>m.dataset.copafemPlanned==='1');
        if(generic || allPlanned || !matches.length){
          if(slots.length){
            if(!plannedMatchesOK(matches,slots)){
              matches.forEach(m=>m.remove());
              slots.forEach(slot=>col.appendChild(placeholder(slot)));
            }
            if(col.style.display==='none')col.style.display='';
          }else if(cup==='silver'&&round==='octavos'){
            if(col.style.display!=='none')col.style.display='none';
          }
          return;
        }

        matches.forEach((m,i)=>normalizeExistingHeader(m,slots[i]));
      });

      const silver=sheet.querySelector('.drop-silver-area');
      if(silver){
        const visible=[...silver.querySelectorAll(':scope > .drop-round-col')].filter(x=>x.style.display!=='none').length;
        const wanted=visible>0?'repeat('+visible+',minmax(0,1fr))':'';
        if(wanted && silver.style.gridTemplateColumns!==wanted)silver.style.gridTemplateColumns=wanted;
      }
    });
  }

  let queued=false;
  const queue=()=>{
    if(queued)return;
    queued=true;
    requestAnimationFrame(()=>{queued=false;decorate();});
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',queue);else queue();
  new MutationObserver(queue).observe(document.documentElement,{subtree:true,childList:true});
  document.addEventListener('click',()=>setTimeout(queue,0),true);
})();
</script>
'''

if '</body>' not in s:
    raise SystemExit('No se encontró </body> en index.html')

head, tail = s.rsplit('</body>', 1)
s = head + injection + '\n</body>' + tail
p.write_text(s, encoding='utf-8')
print('COPAFEM drop schedule patch OK')
