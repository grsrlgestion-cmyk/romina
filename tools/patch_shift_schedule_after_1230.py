from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_SHIFT_2026_09_13_CORE_SCOPE_V4'
if MARK in s:
    print('core shift 12:30 already applied')
    raise SystemExit

start=s.find('  function renderAll(){')
if start<0:
    raise SystemExit('No se encontró renderAll')
end=s.find('\n\n  function renderSettings', start)
if end<0:
    raise SystemExit('No se encontró fin de renderAll')

helper=r'''
  // COPAFEM_SHIFT_2026_09_13_CORE_SCOPE_V4
  function copafemShiftSep13After1230Core(){
    const from=parseTime('12:30');
    let changed=false;
    Object.values(store?.events||{}).forEach(ev=>{
      const d=String(ev?.tournament?.date||'').trim();
      if(d!=='2026-09-13' && d!=='13/09/2026') return;
      const matches=[...(ev?.zoneMatches||[]),...(ev?.brackets?.gold||[]),...(ev?.brackets?.silver||[])];
      // Se aplica solo mientras todavía exista algún partido a las 12:30.
      // Una vez corregido a 13:00 no vuelve a sumar otros 30 minutos.
      if(!matches.some(m=>m?.time && parseTime(m.time)===from)) return;
      matches.forEach(m=>{
        if(!m?.time) return;
        const t=parseTime(m.time);
        if(Number.isFinite(t) && t>=from){
          m.time=fmtTime(t+30);
          changed=true;
        }
      });
    });
    if(changed){
      state=store.events[store.activeEventId]||state;
      const now=new Date().toISOString();
      state.updatedAt=now;
      store.updatedAt=now;
      try{ localStorage.setItem(STORAGE_KEY,JSON.stringify(store)); }catch(_e){}
      if(window.COPAFEM_ADMIN_PASSWORD) window.COPAFEM_REMOTE_PUSH?.(store);
    }
    return changed;
  }
'''

block=s[start:end]
if 'rebuildBrackets(true);' in block:
    block=block.replace('rebuildBrackets(true);','rebuildBrackets(true);copafemShiftSep13After1230Core();',1)
else:
    block=block.replace('function renderAll(){','function renderAll(){copafemShiftSep13After1230Core();',1)

s=s[:start]+helper+block+s[end:]
p.write_text(s,encoding='utf-8')
print('COPAFEM: corrimiento 12:30 -> 13:00 aplicado dentro del núcleo, después de reconstruir cruces')
