from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_PLACEHOLDER_SOURCE_LABELS_V1'
if MARK in s:
    print('placeholder source labels already applied')
    raise SystemExit

# 1) Guardar el origen lógico de cada lugar del cuadro (1A, 3B, W:G-QF-1, L:G-SF-2, etc.).
old='''function copafemMakeMatch(id,round,a,b,old){
  const p1=a?.value||null,p2=b?.value||null,prev=old[id],same=prev&&prev.p1===p1&&prev.p2===p2;
  return {id,round,p1,p2,s1:same?(prev.s1??null):null,s2:same?(prev.s2??null):null,time:null,court:null,dropFormat:true};
}'''
new='''function copafemMakeMatch(id,round,a,b,old){
  const p1=a?.value||null,p2=b?.value||null,prev=old[id],same=prev&&prev.p1===p1&&prev.p2===p2;
  return {id,round,p1,p2,source1:a?.key||'',source2:b?.key||'',s1:same?(prev.s1??null):null,s2:same?(prev.s2??null):null,time:null,court:null,dropFormat:true};
}'''
if old not in s:
    raise SystemExit('No se encontró copafemMakeMatch')
s=s.replace(old,new,1)

# 2) Mostrar al lado de "A definir" de dónde sale esa pareja.
needle='''  function bracketTeam(kind,m,pSide,sSide){
    const id=m[pSide],real=!!id&&!String(id).startsWith("__TBD__"),name=real?pairName(id):"A definir";return `<div class="bracket-team"><span class="${real?"":"placeholder"}">${esc(name)}</span><input type="number" min="0" inputmode="numeric" ${real?"":"disabled"} value="${real?(m[sSide]??""):""}" data-kind="${kind}" data-bscore="${m.id}" data-side="${sSide}"></div>`;
  }'''
replacement='''  function copafemDescribeSourceMatch(id){
    const raw=String(id||"");
    const cup=raw.startsWith("S")?"Plata":"Oro";
    const round=raw.includes("-R32-")?"Dieciseisavos":raw.includes("-R16-")?"Octavos":raw.includes("-QF-")?"Cuartos":raw.includes("-SF-")?"Semifinal":raw.includes("-F-")?"Final":"cruce";
    const zone=raw.match(/-Z([A-Z])$/);
    const num=raw.match(/-(\\d+)$/);
    if(round==="Final") return `Final de ${cup}`;
    if(zone) return `${round} de ${cup} · Zona ${zone[1]}`;
    if(num) return `${round} de ${cup} ${num[1]}`;
    return `${round} de ${cup}`;
  }

  function copafemSourceLabel(key){
    const raw=String(key||"");
    const seed=raw.match(/^([1-9])([A-Z])$/);
    if(seed) return `${seed[1]}.º Zona ${seed[2]}`;
    const flow=raw.match(/^([WL]):(.+)$/);
    if(flow) return `${flow[1]==="W"?"Ganador":"Perdedor"} de ${copafemDescribeSourceMatch(flow[2])}`;
    return "";
  }

  function copafemPlaceholderLabel(m,pSide){
    const key=pSide==="p1"?m.source1:m.source2;
    const fromSource=copafemSourceLabel(key);
    if(fromSource) return fromSource;
    const id=String(m[pSide]||"");
    let legacy=id.match(/^__TBD__[GS]-(\\d+)-([A-Z])$/);
    if(legacy) return `${legacy[1]}.º Zona ${legacy[2]}`;
    legacy=id.match(/^__TBD__S-GL-(\\d+)$/);
    if(legacy) return `Perdedor de Oro ${legacy[1]}`;
    return "";
  }

  function bracketTeam(kind,m,pSide,sSide){
    const id=m[pSide],real=!!id&&!String(id).startsWith("__TBD__");
    const source=real?"":copafemPlaceholderLabel(m,pSide);
    const name=real?pairName(id):`A definir${source?` · ${source}`:""}`;
    return `<div class="bracket-team"><span class="${real?"":"placeholder"}">${esc(name)}</span><input type="number" min="0" inputmode="numeric" ${real?"":"disabled"} value="${real?(m[sSide]??""):""}" data-kind="${kind}" data-bscore="${m.id}" data-side="${sSide}"></div>`;
  }'''
if needle not in s:
    raise SystemExit('No se encontró bracketTeam')
s=s.replace(needle,replacement,1)

s=s.replace('</body>',f'\n<!-- {MARK} -->\n</body>',1)
p.write_text(s,encoding='utf-8')
print('COPAFEM: A definir ahora muestra posición/zona o cruce de origen')
