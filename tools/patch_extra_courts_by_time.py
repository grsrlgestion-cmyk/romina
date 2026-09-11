from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
MARKER = 'COPAFEM_COURT_OVERRIDES_BY_TIME_V2'
if MARKER in s:
    print('court overrides by time already applied')
    raise SystemExit

# -----------------------------------------------------------------------------
# 1) Persistencia: canchas extra y canchas bloqueadas por turno para cada categoría.
# -----------------------------------------------------------------------------
old_default = '''        courts: Array.isArray(t.courts) && t.courts.length ? [...t.courts] : [1,3,5,7]\n'''
new_default = '''        courts: Array.isArray(t.courts) && t.courts.length ? [...t.courts] : [1,3,5,7],\n        extraCourts: Array.isArray(t.extraCourts) ? t.extraCourts.map(x=>({time:String(x?.time||""),court:Number(x?.court)})).filter(x=>/^\\d{2}:\\d{2}$/.test(x.time)&&Number.isFinite(x.court)&&x.court>=1&&x.court<=8) : [],\n        blockedCourts: Array.isArray(t.blockedCourts) ? t.blockedCourts.map(x=>({time:String(x?.time||""),court:Number(x?.court)})).filter(x=>/^\\d{2}:\\d{2}$/.test(x.time)&&Number.isFinite(x.court)&&x.court>=1&&x.court<=8) : []\n'''
if old_default not in s:
    raise SystemExit('No se encontró defaultEvent.courts')
s = s.replace(old_default, new_default, 1)

old_read = '''      courts: courts.length ? [...new Set(courts)] : suggestedCourtsFor(category)\n'''
new_read = '''      courts: courts.length ? [...new Set(courts)] : suggestedCourtsFor(category),\n      extraCourts: Array.isArray(state.tournament.extraCourts) ? state.tournament.extraCourts : [],\n      blockedCourts: Array.isArray(state.tournament.blockedCourts) ? state.tournament.blockedCourts : []\n'''
if old_read not in s:
    raise SystemExit('No se encontró readSettings.courts')
s = s.replace(old_read, new_read, 1)

# -----------------------------------------------------------------------------
# 2) UI en la pestaña Canchas.
# -----------------------------------------------------------------------------
needle_html = '''      </div>\n      <article class="panel">\n        <div id="scheduleConflictNotice" class="schedule-conflict-notice" hidden></div>\n'''
panel_html = '''      </div>\n      <article class="panel extra-courts-panel" id="extraCourtsPanel">\n        <div class="panel-head extra-courts-head">\n          <div>\n            <h3>Canchas por horario</h3>\n            <p>Podés <b>agregar</b> una cancha puntual o <b>bloquear</b> una cancha base de esta categoría en el horario que necesites.</p>\n          </div>\n          <span id="extraCourtCategoryBadge" class="category-badge">7ma</span>\n        </div>\n        <div class="extra-court-form">\n          <label>Horario\n            <input id="extraCourtTime" type="time" value="10:00" step="900" />\n          </label>\n          <label>Cancha\n            <select id="extraCourtNumber">\n              <option value="1">Cancha 1</option><option value="2">Cancha 2</option>\n              <option value="3">Cancha 3</option><option value="4">Cancha 4</option>\n              <option value="5">Cancha 5</option><option value="6">Cancha 6</option>\n              <option value="7">Cancha 7</option><option value="8">Cancha 8</option>\n            </select>\n          </label>\n          <div class="court-override-actions">\n            <button id="addExtraCourtBtn" class="btn primary" type="button">Agregar cancha</button>\n            <button id="blockCourtBtn" class="btn danger-soft" type="button">Bloquear cancha</button>\n          </div>\n        </div>\n        <div class="court-override-group">\n          <div class="court-override-label">Canchas adicionales</div>\n          <div id="extraCourtsList" class="extra-courts-list"></div>\n        </div>\n        <div class="court-override-group">\n          <div class="court-override-label blocked">Canchas bloqueadas para esta categoría</div>\n          <div id="blockedCourtsList" class="extra-courts-list"></div>\n        </div>\n        <p class="hint extra-court-hint">Ejemplo: si 7ma usa normalmente 1, 3, 5 y 7, podés bloquear <b>10:00 · Cancha 1</b> para dejarla libre para otra categoría. A las 10:30 vuelve a estar disponible salvo que también la bloquees.</p>\n      </article>\n      <article class="panel">\n        <div id="scheduleConflictNotice" class="schedule-conflict-notice" hidden></div>\n'''
if needle_html not in s:
    raise SystemExit('No se encontró el panel de Canchas')
s = s.replace(needle_html, panel_html, 1)

# -----------------------------------------------------------------------------
# 3) Lógica de UI dentro del IIFE principal.
# -----------------------------------------------------------------------------
marker_render = '''  function renderAll(){applyCategoryTheme();renderSettings();renderEvents();renderPairs();renderZones();renderResults();rebuildBrackets(true);renderCups();renderSchedule();renderHeader();renderDrop();}\n'''
helpers = r'''
  // COPAFEM_COURT_OVERRIDES_BY_TIME_V2
  function copafemTimedCourtList(event=state,key='extraCourts'){
    if(!event?.tournament) return [];
    if(!Array.isArray(event.tournament[key])) event.tournament[key]=[];
    event.tournament[key]=event.tournament[key]
      .map(x=>({time:String(x?.time||""),court:Number(x?.court)}))
      .filter(x=>/^\d{2}:\d{2}$/.test(x.time)&&Number.isFinite(x.court)&&x.court>=1&&x.court<=8)
      .filter((x,i,a)=>a.findIndex(y=>y.time===x.time&&y.court===x.court)===i)
      .sort((a,b)=>parseTime(a.time)-parseTime(b.time)||a.court-b.court);
    return event.tournament[key];
  }

  function copafemExtraList(event=state){ return copafemTimedCourtList(event,'extraCourts'); }
  function copafemBlockedList(event=state){ return copafemTimedCourtList(event,'blockedCourts'); }

  function renderCourtOverrideList(list,key,emptyText,blocked=false){
    if(!list) return;
    const rows=key==='extraCourts'?copafemExtraList():copafemBlockedList();
    list.innerHTML=rows.length ? rows.map((x,i)=>`<div class="extra-court-chip ${blocked?'blocked':''}"><div><strong>${esc(x.time)}</strong><span>Cancha ${x.court}</span></div><button type="button" class="icon-btn extra-court-remove" data-court-override-key="${key}" data-court-override-index="${i}" title="Quitar">✕</button></div>`).join("") : `<div class="extra-courts-empty">${esc(emptyText)}</div>`;
  }

  function renderExtraCourts(){
    const extraList=$("extraCourtsList"), blockedList=$("blockedCourtsList");
    if(!extraList && !blockedList) return;
    const cat=state.tournament.category||"—";
    const badge=$("extraCourtCategoryBadge"); if(badge) badge.textContent=cat;
    renderCourtOverrideList(extraList,'extraCourts',`No hay canchas adicionales cargadas para ${cat}.`,false);
    renderCourtOverrideList(blockedList,'blockedCourts',`No hay canchas bloqueadas para ${cat}.`,true);
    document.querySelectorAll("[data-court-override-key]").forEach(b=>b.addEventListener("click",()=>removeCourtOverride(b.dataset.courtOverrideKey,Number(b.dataset.courtOverrideIndex))));
    const time=$("extraCourtTime");
    if(time && !time.dataset.userEdited) time.value=state.tournament.startTime||"10:00";
  }

  function copafemExtraAligned(time){
    const start=parseTime(state.tournament.startTime||"10:00"), t=parseTime(time), dur=Math.max(1,Number(state.tournament.duration||30));
    return t>=start && ((t-start)%dur===0);
  }

  function copafemReadCourtOverrideForm(){
    const time=String($("extraCourtTime")?.value||"");
    const court=Number($("extraCourtNumber")?.value||0);
    if(!/^\d{2}:\d{2}$/.test(time)){toast("Elegí el horario");return null;}
    if(!Number.isFinite(court)||court<1||court>8){toast("Elegí una cancha válida");return null;}
    if(!copafemExtraAligned(time)){toast(`El horario debe coincidir con turnos de ${state.tournament.duration||30} minutos desde ${state.tournament.startTime||"10:00"}`);return null;}
    return {time,court};
  }

  function copafemRescheduleAfterCourtChange(){
    if(state.zoneMatches.length) generateSchedule(false); else saveState();
    renderAll();
  }

  function addExtraCourt(){
    const v=copafemReadCourtOverrideForm(); if(!v) return;
    const {time,court}=v;
    if((state.tournament.courts||[]).map(Number).includes(court)) return toast(`La cancha ${court} ya está disponible normalmente para ${state.tournament.category}`);
    if(copafemBlockedList().some(x=>x.time===time&&x.court===court)) return toast(`La cancha ${court} está bloqueada a las ${time}. Quitá primero el bloqueo.`);
    const extras=copafemExtraList();
    if(extras.some(x=>x.time===time&&x.court===court)) return toast(`La cancha ${court} ya está agregada a las ${time}`);
    extras.push({time,court}); state.tournament.extraCourts=extras;
    copafemRescheduleAfterCourtChange();
    toast(`Cancha ${court} agregada a ${state.tournament.category} a las ${time}`);
  }

  function blockCourt(){
    const v=copafemReadCourtOverrideForm(); if(!v) return;
    const {time,court}=v;
    const base=(state.tournament.courts||[]).map(Number);
    if(!base.includes(court)){
      const extraIndex=copafemExtraList().findIndex(x=>x.time===time&&x.court===court);
      if(extraIndex>=0){
        state.tournament.extraCourts.splice(extraIndex,1);
        copafemRescheduleAfterCourtChange();
        return toast(`Cancha ${court} extra quitada de las ${time}`);
      }
      return toast(`La cancha ${court} no es una cancha base de ${state.tournament.category}`);
    }
    const blocked=copafemBlockedList();
    if(blocked.some(x=>x.time===time&&x.court===court)) return toast(`La cancha ${court} ya está bloqueada a las ${time}`);
    blocked.push({time,court}); state.tournament.blockedCourts=blocked;
    copafemRescheduleAfterCourtChange();
    toast(`Cancha ${court} bloqueada para ${state.tournament.category} a las ${time}`);
  }

  function removeCourtOverride(key,index){
    if(!['extraCourts','blockedCourts'].includes(key)) return;
    const rows=copafemTimedCourtList(state,key), removed=rows[index];
    if(!removed) return;
    rows.splice(index,1); state.tournament[key]=rows;
    copafemRescheduleAfterCourtChange();
    toast(key==='blockedCourts' ? `Cancha ${removed.court} habilitada nuevamente a las ${removed.time}` : `Cancha ${removed.court} extra quitada de las ${removed.time}`);
  }

'''
if marker_render not in s:
    raise SystemExit('No se encontró renderAll')
s = s.replace(marker_render, helpers + '''  function renderAll(){applyCategoryTheme();renderSettings();renderEvents();renderPairs();renderZones();renderResults();rebuildBrackets(true);renderCups();renderSchedule();renderHeader();renderDrop();renderExtraCourts();}\n''', 1)

old_listener = '''    $("exportCsvBtn").addEventListener("click", exportCSV);\n'''
new_listener = '''    $("exportCsvBtn").addEventListener("click", exportCSV);\n    $("addExtraCourtBtn")?.addEventListener("click", addExtraCourt);\n    $("blockCourtBtn")?.addEventListener("click", blockCourt);\n    $("extraCourtTime")?.addEventListener("change",e=>e.target.dataset.userEdited="1");\n'''
if old_listener not in s:
    raise SystemExit('No se encontró listener exportCsvBtn')
s = s.replace(old_listener, new_listener, 1)

# -----------------------------------------------------------------------------
# 4) El asignador usa: canchas base + extras del turno - bloqueos del turno.
# -----------------------------------------------------------------------------
old_free = '''  function copafemFreeCourts(event,occupied,start){\n    const dur=copafemDuration(event);\n    return copafemUniqueCourts(event).filter(c=>copafemCourtFree(occupied,c,start,dur));\n  }\n'''
new_free = '''  function copafemExtraCourtsAt(event,start){\n    const time=fmtTime(start);\n    return [...new Set((event?.tournament?.extraCourts||[])\n      .filter(x=>String(x?.time||"")===time)\n      .map(x=>Number(x?.court))\n      .filter(n=>Number.isFinite(n)&&n>=1&&n<=8))];\n  }\n\n  function copafemBlockedCourtsAt(event,start){\n    const time=fmtTime(start);\n    return new Set((event?.tournament?.blockedCourts||[])\n      .filter(x=>String(x?.time||"")===time)\n      .map(x=>Number(x?.court))\n      .filter(n=>Number.isFinite(n)&&n>=1&&n<=8));\n  }\n\n  function copafemAvailableCourtsAt(event,start){\n    const blocked=copafemBlockedCourtsAt(event,start);\n    return [...new Set([...copafemUniqueCourts(event),...copafemExtraCourtsAt(event,start)])].filter(c=>!blocked.has(c));\n  }\n\n  function copafemFreeCourts(event,occupied,start){\n    const dur=copafemDuration(event);\n    return copafemAvailableCourtsAt(event,start).filter(c=>copafemCourtFree(occupied,c,start,dur));\n  }\n'''
if old_free not in s:
    raise SystemExit('No se encontró copafemFreeCourts del asignador')
s = s.replace(old_free, new_free, 1)

old_min = '''    const absoluteMin=Math.max(minRounds,Math.ceil(total/courts.length));\n'''
new_min = '''    const adjustedTimes=[...new Set([\n      ...(event?.tournament?.extraCourts||[]).map(x=>String(x?.time||"")),\n      ...(event?.tournament?.blockedCourts||[]).map(x=>String(x?.time||""))\n    ].filter(Boolean))];\n    const maxCourtCount=Math.max(courts.length,...adjustedTimes.map(t=>copafemAvailableCourtsAt(event,parseTime(t)).length),1);\n    const absoluteMin=Math.max(minRounds,Math.ceil(total/maxCourtCount));\n'''
if old_min not in s:
    raise SystemExit('No se encontró absoluteMin del asignador')
s = s.replace(old_min, new_min, 1)

old_order = '''    const zoneOrder=[...entries].sort((a,b)=>\n      parseTime(a[1].tournament.startTime||'10:00')-parseTime(b[1].tournament.startTime||'10:00') ||\n      CATEGORIES.indexOf(a[1].tournament.category)-CATEGORIES.indexOf(b[1].tournament.category)\n    );\n'''
new_order = '''    const zoneOrder=[...entries].sort((a,b)=>\n      parseTime(a[1].tournament.startTime||'10:00')-parseTime(b[1].tournament.startTime||'10:00') ||\n      ((a[1].tournament.extraCourts||[]).length-(b[1].tournament.extraCourts||[]).length) ||\n      CATEGORIES.indexOf(a[1].tournament.category)-CATEGORIES.indexOf(b[1].tournament.category)\n    );\n'''
if old_order not in s:
    raise SystemExit('No se encontró zoneOrder del asignador')
s = s.replace(old_order, new_order, 1)

# -----------------------------------------------------------------------------
# 5) Estilos.
# -----------------------------------------------------------------------------
css = r'''
<style id="COPAFEM_COURT_OVERRIDES_BY_TIME_V2">
.extra-courts-panel{border-top:4px solid var(--cat)}
.extra-courts-head{align-items:center}
.extra-court-form{display:grid;grid-template-columns:170px 180px minmax(280px,1fr);gap:10px;align-items:end;margin:4px 0 14px}
.extra-court-form label{font-size:12px;color:#5b6067;font-weight:800}
.extra-court-form input,.extra-court-form select{width:100%;margin-top:6px;border:1px solid #d5e0eb;border-radius:11px;padding:10px 11px;background:#fff;min-height:43px;color:var(--ink)}
.court-override-actions{display:flex;gap:8px}.court-override-actions .btn{min-height:43px;flex:1}
.court-override-group{margin-top:12px;padding-top:11px;border-top:1px solid var(--line)}
.court-override-label{font-size:11px;font-weight:950;text-transform:uppercase;letter-spacing:.05em;color:var(--cat-ink);margin-bottom:6px}
.court-override-label.blocked{color:#9b2c20}
.extra-courts-list{display:flex;gap:8px;flex-wrap:wrap;min-height:42px;align-items:center}
.extra-court-chip{display:flex;align-items:center;gap:10px;border:1px solid color-mix(in srgb,var(--cat) 35%,#d5e0eb);background:var(--cat-soft);border-radius:12px;padding:7px 8px 7px 11px;color:var(--cat-ink)}
.extra-court-chip.blocked{border-color:#efb7ae;background:#fff2ef;color:#8d2f25}
.extra-court-chip>div{display:flex;align-items:center;gap:7px}.extra-court-chip strong{font-size:14px}.extra-court-chip span{font-size:12px;font-weight:850}
.extra-court-chip .icon-btn{background:#fff;color:#8d2f25}.extra-courts-empty{font-size:12px;color:var(--muted);padding:9px 0}.extra-court-hint{margin-top:12px}
@media(max-width:760px){.extra-court-form{grid-template-columns:1fr 1fr}.court-override-actions{grid-column:1/-1}.extra-courts-head{align-items:flex-start;flex-direction:column}}
@media(max-width:520px){.extra-court-form{grid-template-columns:1fr}.court-override-actions{grid-column:auto;flex-direction:column}}
@media print{.extra-courts-panel{display:none!important}}
</style>
'''
if '</head>' not in s:
    raise SystemExit('No se encontró </head>')
s = s.replace('</head>', css + '\n</head>', 1)

p.write_text(s, encoding='utf-8')
print('COPAFEM add/block courts by time patch OK')
