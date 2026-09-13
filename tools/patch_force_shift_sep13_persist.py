from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_FORCE_SHIFT_SEP13_PERSIST_V1'
if MARK in s:
    print('force shift sep13 persist already applied')
    raise SystemExit

helper=r'''
<script id="COPAFEM_FORCE_SHIFT_SEP13_PERSIST_V1">
(() => {
  const KEY='copafem_torneos_v4_multicategoria';
  const TARGETS=new Set(['2026-09-13','13/09/2026']);
  function mins(t){
    const m=String(t||'').match(/^(\d{1,2}):(\d{2})$/);
    return m ? Number(m[1])*60+Number(m[2]) : NaN;
  }
  function fmt(n){
    const h=Math.floor(n/60),m=n%60;
    return String(h).padStart(2,'0')+':'+String(m).padStart(2,'0');
  }
  window.COPAFEM_SHIFT_SEP13_STORE=function(st){
    if(!st || typeof st!=='object' || !st.events) return st;
    const events=Object.values(st.events).filter(ev=>ev?.tournament && TARGETS.has(String(ev.tournament.date||'').trim()));
    if(!events.length) return st;
    const all=ev=>[...(ev.zoneMatches||[]),...(ev.brackets?.gold||[]),...(ev.brackets?.silver||[])];
    const needs=events.some(ev=>all(ev).some(m=>String(m?.time||'')==='12:30'));
    if(!needs) return st;
    events.forEach(ev=>{
      all(ev).forEach(m=>{
        const t=mins(m?.time);
        if(Number.isFinite(t) && t>=750) m.time=fmt(t+30);
      });
      ev.tournament.copafemShiftSep13PersistV1=true;
    });
    st.copafemShiftSep13PersistV1=true;
    try{ localStorage.setItem(KEY,JSON.stringify(st)); }catch(_e){}
    return st;
  };
})();
</script>
'''

anchor='''  <script>\n(() => {\n  const STORAGE_KEY = "copafem_torneos_v4_multicategoria";'''
if anchor not in s:
    raise SystemExit('No se encontró inicio del script principal')
s=s.replace(anchor,helper+'\n'+anchor,1)

old='''  function loadStore(){\n    try{\n      const raw=localStorage.getItem(STORAGE_KEY);\n      if(raw) return normalizeStore(JSON.parse(raw));\n      for(const key of LEGACY_KEYS){\n        const legacy=localStorage.getItem(key);\n        if(legacy) return normalizeStore(JSON.parse(legacy));\n      }\n    }catch(e){}\n    return newStore();\n  }\n\n  let store = loadStore();\n  let state = store.events[store.activeEventId];'''
new='''  function loadStore(){\n    try{\n      const raw=localStorage.getItem(STORAGE_KEY);\n      if(raw){\n        const loaded=window.COPAFEM_SHIFT_SEP13_STORE(normalizeStore(JSON.parse(raw)));\n        localStorage.setItem(STORAGE_KEY,JSON.stringify(loaded));\n        return loaded;\n      }\n      for(const key of LEGACY_KEYS){\n        const legacy=localStorage.getItem(key);\n        if(legacy){\n          const loaded=window.COPAFEM_SHIFT_SEP13_STORE(normalizeStore(JSON.parse(legacy)));\n          localStorage.setItem(STORAGE_KEY,JSON.stringify(loaded));\n          return loaded;\n        }\n      }\n    }catch(e){}\n    return newStore();\n  }\n\n  let store = loadStore();\n  let state = store.events[store.activeEventId];\n  window.COPAFEM_APPLY_SHIFTED_STORE=function(nextStore){\n    try{\n      store=window.COPAFEM_SHIFT_SEP13_STORE(normalizeStore(nextStore));\n      localStorage.setItem(STORAGE_KEY,JSON.stringify(store));\n      setActiveState();\n      renderAll();\n      return store;\n    }catch(_e){ return null; }\n  };'''
if old not in s:
    raise SystemExit('No se encontró loadStore principal')
s=s.replace(old,new,1)

old_remote='''    if(!window.COPAFEM_ADMIN_PASSWORD){\n      try{ store=normalizeStore(e.detail.store); setActiveState(); renderAll(); }catch(_){}\n    }'''
new_remote='''    if(!window.COPAFEM_ADMIN_PASSWORD){\n      try{\n        store=window.COPAFEM_SHIFT_SEP13_STORE(normalizeStore(e.detail.store));\n        localStorage.setItem(STORAGE_KEY,JSON.stringify(store));\n        setActiveState(); renderAll();\n      }catch(_){}\n    }'''
if old_remote not in s:
    raise SystemExit('No se encontró listener remoto principal')
s=s.replace(old_remote,new_remote,1)

needle='''await window.COPAFEM_REMOTE_PULL?.(true);enterAdmin();'''
replacement='''await window.COPAFEM_REMOTE_PULL?.(true);try{const raw=localStorage.getItem("copafem_torneos_v4_multicategoria");if(raw){const shifted=window.COPAFEM_APPLY_SHIFTED_STORE?.(JSON.parse(raw));if(shifted) await window.COPAFEM_REMOTE_PUSH?.(shifted);}}catch(_e){}enterAdmin();'''
if needle not in s:
    raise SystemExit('No se encontró flujo de ingreso administrador')
s=s.replace(needle,replacement,1)

p.write_text(s,encoding='utf-8')
print('COPAFEM: corrimiento 12:30 -> 13:00 aplicado también a datos online y persistido')
