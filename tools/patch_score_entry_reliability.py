from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_SCORE_ENTRY_RELIABILITY_V1'
if MARK in s:
    print('score entry reliability already applied')
    raise SystemExit

old_zone='''  function setZoneScore(id, side, value){\n    const m=state.zoneMatches.find(x=>x.id===id); if(!m)return;\n    const n=value===""?null:parseInt(value,10); m[side]=Number.isFinite(n)?Math.max(0,n):null;\n    if(hasScore(m)&&m.s1===m.s2) toast("No se permiten empates: definí un ganador");\n    rebuildBrackets(false); saveState(); renderResults(); renderCups(); renderSchedule(); renderHeader(); renderDrop();\n  }'''
new_zone='''  function setZoneScore(id, side, value){\n    const m=state.zoneMatches.find(x=>x.id===id); if(!m)return;\n    const wasComplete=hasScore(m)&&m.s1!==m.s2;\n    const n=value===""?null:parseInt(value,10); m[side]=Number.isFinite(n)?Math.max(0,n):null;\n    if(hasScore(m)&&m.s1===m.s2) toast("No se permiten empates: definí un ganador");\n\n    // No reconstruir Resultados al salir de la primera casilla: eso destruía\n    // la segunda casilla antes de poder escribirla. En el formato clásico\n    // actualizamos únicamente posiciones y contador.\n    const zone=m.zone;\n    const wrap=document.querySelector(`[data-zone-standings="${zone}"]`);\n    if(wrap) wrap.innerHTML=standingsHTML(zoneStandings(zone));\n    const counter=document.querySelector(`[data-zone-block="${zone}"] .counter`);\n    if(counter){\n      const ms=state.zoneMatches.filter(x=>x.zone===zone);\n      counter.textContent=`${ms.filter(x=>hasScore(x)&&x.s1!==x.s2).length}/${ms.length}`;\n    }\n\n    const complete=hasScore(m)&&m.s1!==m.s2;\n    rebuildBrackets(false); saveState();\n\n    // En torneos dinámicos (menos de 24 parejas) el HTML de posiciones es\n    // diferente y no tiene data-zone-standings. Recién cuando el resultado\n    // queda completo (o se borra uno ya completo) redibujamos Resultados.\n    if(!wrap && (complete||wasComplete)) renderResults();\n    renderCups(); renderSchedule(); renderHeader(); renderDrop();\n  }'''
if old_zone not in s:
    raise SystemExit('No se encontró setZoneScore esperado')
s=s.replace(old_zone,new_zone,1)

old_bracket='''  function setBracketScore(kind,id,side,value){\n    const m=state.brackets[kind].find(x=>x.id===id); if(!m)return;\n    const n=value===""?null:parseInt(value,10); m[side]=Number.isFinite(n)?Math.max(0,n):null;\n    if(hasScore(m)&&m.s1===m.s2) toast("No se permiten empates");\n    rebuildBrackets(true); saveState(); renderCups(); renderSchedule(); renderHeader(); renderDrop();\n  }'''
new_bracket='''  function setBracketScore(kind,id,side,value){\n    const m=state.brackets[kind].find(x=>x.id===id); if(!m)return;\n    const wasComplete=hasScore(m)&&m.s1!==m.s2;\n    const n=value===""?null:parseInt(value,10); m[side]=Number.isFinite(n)?Math.max(0,n):null;\n    if(hasScore(m)&&m.s1===m.s2) toast("No se permiten empates");\n\n    // En un resultado nuevo, el primer score se guarda sin redibujar el cuadro.\n    // Al completar ambos scores sí se reconstruye para pasar ganador/perdedor.\n    const complete=hasScore(m)&&m.s1!==m.s2;\n    saveState();\n    if(complete || wasComplete){\n      rebuildBrackets(true); saveState(); renderCups(); renderSchedule(); renderHeader(); renderDrop();\n    }else{\n      renderSchedule(); renderHeader(); renderDrop();\n    }\n  }'''
if old_bracket not in s:
    raise SystemExit('No se encontró setBracketScore esperado')
s=s.replace(old_bracket,new_bracket,1)

marker='''\n<script id="COPAFEM_SCORE_ENTRY_RELIABILITY_V1">window.COPAFEM_SCORE_ENTRY_RELIABILITY=true;</script>\n'''
head,tail=s.rsplit('</body>',1)
s=head+marker+'\n</body>'+tail
p.write_text(s,encoding='utf-8')
print('COPAFEM carga de resultados y posiciones corregida')
