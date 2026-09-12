from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_CUP_ZONE_POSITION_LABELS_V1'
if MARK in s:
    print('cup zone/position labels already applied')
    raise SystemExit

old='''  function bracketTeam(kind,m,pSide,sSide){
    const id=m[pSide],real=!!id&&!String(id).startsWith("__TBD__");
    const source=real?"":copafemPlaceholderLabel(m,pSide);
    const name=real?pairName(id):`A definir${source?` · ${source}`:""}`;
    return `<div class="bracket-team"><span class="${real?"":"placeholder"}">${esc(name)}</span><input type="number" min="0" inputmode="numeric" ${real?"":"disabled"} value="${real?(m[sSide]??""):""}" data-kind="${kind}" data-bscore="${m.id}" data-side="${sSide}"></div>`;
  }'''

new='''  function copafemDirectZonePosition(key){
    const seed=String(key||"").match(/^([1-9])([A-Z])$/);
    return seed ? `Zona ${seed[2]} · ${seed[1]}.º` : "";
  }

  function copafemResolvedZonePosition(id){
    const pid=String(id||"");
    if(!pid || pid.startsWith("__TBD__")) return "";
    try{
      for(const z of ZONES){
        const st=zoneStandings(z);
        const rows=Array.isArray(st)?st:(st?.rows||[]);
        const idx=rows.findIndex(r=>r.id===pid);
        if(idx>=0) return `Zona ${z} · ${idx+1}.º`;
      }
    }catch(_){ }
    return "";
  }

  function bracketTeam(kind,m,pSide,sSide){
    const id=m[pSide],real=!!id&&!String(id).startsWith("__TBD__");
    const key=pSide==="p1"?m.source1:m.source2;
    let source="";
    if(real){
      source=copafemResolvedZonePosition(id)||copafemDirectZonePosition(key);
    }else{
      source=copafemDirectZonePosition(key)||copafemSourceLabel(key)||copafemPlaceholderLabel(m,pSide);
    }
    const name=real?pairName(id):"A definir";
    const display=source?`${source} — ${name}`:name;
    return `<div class="bracket-team"><span class="${real?"":"placeholder"}">${esc(display)}</span><input type="number" min="0" inputmode="numeric" ${real?"":"disabled"} value="${real?(m[sSide]??""):""}" data-kind="${kind}" data-bscore="${m.id}" data-side="${sSide}"></div>`;
  }'''

if old not in s:
    raise SystemExit('No se encontró bracketTeam generado por placeholder source labels')
s=s.replace(old,new,1)
s=s.replace('</body>',f'\n<!-- {MARK} -->\n</body>',1)
p.write_text(s,encoding='utf-8')
print('COPAFEM: Copa muestra Zona + posición junto al nombre/A definir')
