from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
MARKER = 'COPAFEM_EXTRA_COURTS_BY_TIME_V1'
if MARKER in s:
    print('extra courts by time already applied')
    raise SystemExit

# -----------------------------------------------------------------------------
# 1) Persistencia: cada categoría puede guardar canchas extra para turnos puntuales.
# -----------------------------------------------------------------------------
old_default = '''        courts: Array.isArray(t.courts) && t.courts.length ? [...t.courts] : [1,3,5,7]\n'''
new_default = '''        courts: Array.isArray(t.courts) && t.courts.length ? [...t.courts] : [1,3,5,7],\n        extraCourts: Array.isArray(t.extraCourts) ? t.extraCourts.map(x=>({time:String(x?.time||""),court:Number(x?.court)})).filter(x=>/^\\d{2}:\\d{2}$/.test(x.time)&&Number.isFinite(x.court)&&x.court>=1&&x.court<=8) : []\n'''
if old_default not in s:
    raise SystemExit('No se encontró defaultEvent.courts')
s = s.replace(old_default, new_default, 1)

old_read = '''      courts: courts.length ? [...new Set(courts)] : suggestedCourtsFor(category)\n'''
new_read = '''      courts: courts.length ? [...new Set(courts)] : suggestedCourtsFor(category),\n      extraCourts: Array.isArray(state.tournament.extraCourts) ? state.tournament.extraCourts : []\n'''
if old_read not in s:
    raise SystemExit('No se encontró readSettings.courts')
s = s.replace(old_read, new_read, 1)

# -----------------------------------------------------------------------------
# 2) UI en la pestaña Canchas.
# -----------------------------------------------------------------------------
needle_html = '''      </div>\n      <article class="panel">\n        <div id="scheduleConflictNotice" class="schedule-conflict-notice" hidden></div>\n'''
panel_html = '''      </div>\n      <article class="panel extra-courts-panel" id="extraCourtsPanel">\n        <div class="panel-head extra-courts-head">\n          <div>\n            <h3>Canchas extra por horario</h3>\n            <p>Habilitá una cancha adicional para esta categoría solamente en un turno puntual. Ejemplo: <b>10:00 · Cancha 2</b>.</p>\n          </div>\n          <span id="extraCourtCategoryBadge" class="category-badge">7ma</span>\n        </div>\n        <div class="extra-court-form">\n          <label>Horario\n            <input id="extraCourtTime" type="time" value="10:00" step="900" />\n          </label>\n          <label>Cancha\n            <select id="extraCourtNumber">\n              <option value="1">Cancha 1</option><option value="2">Cancha 2</option>\n              <option value="3">Cancha 3</option><option value="4">Cancha 4</option>\n              <option value="5">Cancha 5</option><option value="6">Cancha 6</option>\n              <option value="7">Cancha 7</option><option value="8">Cancha 8</option>\n            </select>\n          </label>\n          <button id="addExtraCourtBtn" class="btn primary" type="button">Agregar cancha</button>\n        </div>\n        <div id="extraCourtsList" class="extra-courts-list"></div>\n        <p class="hint extra-court-hint">La cancha extra se habilita solo para ese turno. Si otra categoría ya la está usando a esa hora, el sistema no la superpone. Al agregar o quitar una cancha se rehacen los horarios automáticamente.</p>\n      </article>\n      <article class="panel">\n        <div id="scheduleConflictNotice" class="schedule-conflict-notice" hidden></div>\n'''
if needle_html not in s:
    raise SystemExit('No se encontró el panel de Canchas')
s = s.replace(needle_html, panel_html, 1)

# -----------------------------------------------------------------------------
# 3) Lógica de UI dentro del IIFE principal.
# -----------------------------------------------------------------------------
marker_render = '''  function renderAll(){applyCategoryTheme();renderSettings();renderEvents();renderPairs();renderZones();renderResults();rebuildBrackets(true);renderCups();renderSchedule();renderHeader();renderDrop();}\n'''
helpers = r'''
  // COPAFEM_EXTRA_COURTS_BY_TIME_V1
  function copafemExtraList(event=state){
    if(!event?.tournament) return [];
    if(!Array.isArray(event.tournament.extraCourts)) event.tournament.extraCourts=[];
    event.tournament.extraCourts=event.tournament.extraCourts
      .map(x=>({time:String(x?.time||""),court:Number(x?.court)}))
      .filter(x=>/^\d{2}:\d{2}$/.test(x.time)&&Number.isFinite(x.court)&&x.court>=1&&x.court<=8)
      .filter((x,i,a)=>a.findIndex(y=>y.time===x.time&&y.court===x.court)===i)
      .sort((a,b)=>parseTime(a.time)-parseTime(b.time)||a.court-b.court);
    return event.tournament.extraCourts;
  }

  function renderExtraCourts(){
    const list=$("extraCourtsList");
    if(!list) return;
    const cat=state.tournament.category||"—";
    const badge=$("extraCourtCategoryBadge"); if(badge) badge.textContent=cat;
    const extras=copafemExtraList();
    list.innerHTML=extras.length ? extras.map((x,i)=>`<div class="extra-court-chip"><div><strong>${esc(x.time)}</strong><span>Cancha ${x.court}</span></div><button type="button" class="icon-btn extra-court-remove" data-extra-court-index="${i}" title="Quitar cancha extra">✕</button></div>`).join("") : `<div class="extra-courts-empty">No hay canchas extra cargadas para ${esc(cat)}.</div>`;
    list.querySelectorAll("[data-extra-court-index]").forEach(b=>b.addEventListener("click",()=>removeExtraCourt(Number(b.dataset.extraCourtIndex))));
    const time=$("extraCourtTime");
    if(time && !time.dataset.userEdited){
      time.value=state.tournament.startTime||"10:00";
    }
  }

  function copafemExtraAligned(time){
    const start=parseTime(state.tournament.startTime||"10:00"), t=parseTime(time), dur=Math.max(1,Number(state.tournament.duration||30));
    return t>=start && ((t-start)%dur===0);
  }

  function addExtraCourt(){
    const time=String($("extraCourtTime")?.value||"");
    const court=Number($("extraCourtNumber")?.value||0);
    if(!/^\d{2}:\d{2}$/.test(time)) return toast("Elegí el horario de la cancha extra");
    if(!Number.isFinite(court)||court<1||court>8) return toast("Elegí una cancha válida");
    if((state.tournament.courts||[]).map(Number).includes(court)) return toast(`La cancha ${court} ya está disponible en todos los horarios de ${state.tournament.category}`);
    if(!copafemExtraAligned(time)) return toast(`El horario debe coincidir con turnos de ${state.tournament.duration||30} minutos desde ${state.tournament.startTime||"10:00"}`);
    const extras=copafemExtraList();
    if(extras.some(x=>x.time===time&&x.court===court)) return toast(`La cancha ${court} ya está agregada a las ${time}`);
    extras.push({time,court});
    state.tournament.extraCourts=extras;
    if(state.zoneMatches.length) generateSchedule(false); else saveState();
    renderAll();
    toast(`Cancha ${court} agregada a las ${time}`);
  }

  function removeExtraCourt(index){
    const extras=copafemExtraList();
    const removed=extras[index];
    if(!removed) return;
    extras.splice(index,1);
    state.tournament.extraCourts=extras;
    if(state.zoneMatches.length) generateSchedule(false); else saveState();
    renderAll();
    toast(`Cancha ${removed.court} quitada de las ${removed.time}`);
  }

'''
if marker_render not in s:
    raise SystemExit('No se encontró renderAll')
s = s.replace(marker_render, helpers + '''  function renderAll(){applyCategoryTheme();renderSettings();renderEvents();renderPairs();renderZones();renderResults();rebuildBrackets(true);renderCups();renderSchedule();renderHeader();renderDrop();renderExtraCourts();}\n''', 1)

# Listener de alta + recordar que el usuario tocó el horario.
old_listener = '''    $("exportCsvBtn").addEventListener("click", exportCSV);\n'''
new_listener = '''    $("exportCsvBtn").addEventListener("click", exportCSV);\n    $("addExtraCourtBtn")?.addEventListener("click", addExtraCourt);\n    $("extraCourtTime")?.addEventListener("change",e=>e.target.dataset.userEdited="1");\n'''
if old_listener not in s:
    raise SystemExit('No se encontró listener exportCsvBtn')
s = s.replace(old_listener, new_listener, 1)

# -----------------------------------------------------------------------------
# 4) El asignador usa canchas base + extras SOLO en el horario indicado.
# -----------------------------------------------------------------------------
old_free = '''  function copafemFreeCourts(event,occupied,start){\n    const dur=copafemDuration(event);\n    return copafemUniqueCourts(event).filter(c=>copafemCourtFree(occupied,c,start,dur));\n  }\n'''
new_free = '''  function copafemExtraCourtsAt(event,start){\n    const time=fmtTime(start);\n    return [...new Set((event?.tournament?.extraCourts||[])\n      .filter(x=>String(x?.time||"")===time)\n      .map(x=>Number(x?.court))\n      .filter(n=>Number.isFinite(n)&&n>=1&&n<=8))];\n  }\n\n  function copafemAvailableCourtsAt(event,start){\n    return [...new Set([...copafemUniqueCourts(event),...copafemExtraCourtsAt(event,start)])];\n  }\n\n  function copafemFreeCourts(event,occupied,start){\n    const dur=copafemDuration(event);\n    return copafemAvailableCourtsAt(event,start).filter(c=>copafemCourtFree(occupied,c,start,dur));\n  }\n'''
if old_free not in s:
    raise SystemExit('No se encontró copafemFreeCourts del asignador')
s = s.replace(old_free, new_free, 1)

# La estimación de turnos debe contemplar que en algún horario puede haber más canchas.
old_min = '''    const absoluteMin=Math.max(minRounds,Math.ceil(total/courts.length));\n'''
new_min = '''    const extraTimes=[...new Set((event?.tournament?.extraCourts||[]).map(x=>String(x?.time||"")).filter(Boolean))];\n    const maxCourtCount=Math.max(courts.length,...extraTimes.map(t=>copafemAvailableCourtsAt(event,parseTime(t)).length),1);\n    const absoluteMin=Math.max(minRounds,Math.ceil(total/maxCourtCount));\n'''
if old_min not in s:
    raise SystemExit('No se encontró absoluteMin del asignador')
s = s.replace(old_min, new_min, 1)

# Primero se programan las categorías sin canchas prestadas; luego las que tienen extras
# aprovechan únicamente los huecos que quedaron realmente libres.
old_order = '''    const zoneOrder=[...entries].sort((a,b)=>\n      parseTime(a[1].tournament.startTime||'10:00')-parseTime(b[1].tournament.startTime||'10:00') ||\n      CATEGORIES.indexOf(a[1].tournament.category)-CATEGORIES.indexOf(b[1].tournament.category)\n    );\n'''
new_order = '''    const zoneOrder=[...entries].sort((a,b)=>\n      parseTime(a[1].tournament.startTime||'10:00')-parseTime(b[1].tournament.startTime||'10:00') ||\n      ((a[1].tournament.extraCourts||[]).length-(b[1].tournament.extraCourts||[]).length) ||\n      CATEGORIES.indexOf(a[1].tournament.category)-CATEGORIES.indexOf(b[1].tournament.category)\n    );\n'''
if old_order not in s:
    raise SystemExit('No se encontró zoneOrder del asignador')
s = s.replace(old_order, new_order, 1)

# -----------------------------------------------------------------------------
# 5) Estilos.
# -----------------------------------------------------------------------------
css = r'''
<style id="COPAFEM_EXTRA_COURTS_BY_TIME_V1">
.extra-courts-panel{border-top:4px solid var(--cat)}
.extra-courts-head{align-items:center}
.extra-court-form{display:grid;grid-template-columns:170px 180px auto;gap:10px;align-items:end;margin:4px 0 14px}
.extra-court-form label{font-size:12px;color:#5b6067;font-weight:800}
.extra-court-form input,.extra-court-form select{width:100%;margin-top:6px;border:1px solid #d5e0eb;border-radius:11px;padding:10px 11px;background:#fff;min-height:43px;color:var(--ink)}
.extra-court-form .btn{min-height:43px}
.extra-courts-list{display:flex;gap:8px;flex-wrap:wrap;min-height:42px;align-items:center}
.extra-court-chip{display:flex;align-items:center;gap:10px;border:1px solid color-mix(in srgb,var(--cat) 35%,#d5e0eb);background:var(--cat-soft);border-radius:12px;padding:7px 8px 7px 11px;color:var(--cat-ink)}
.extra-court-chip>div{display:flex;align-items:center;gap:7px}
.extra-court-chip strong{font-size:14px}.extra-court-chip span{font-size:12px;font-weight:850}
.extra-court-chip .icon-btn{background:#fff;color:#8d2f25}
.extra-courts-empty{font-size:12px;color:var(--muted);padding:10px 0}
.extra-court-hint{margin-top:10px}
@media(max-width:650px){.extra-court-form{grid-template-columns:1fr 1fr}.extra-court-form .btn{grid-column:1/-1}.extra-courts-head{align-items:flex-start;flex-direction:column}}
@media print{.extra-courts-panel{display:none!important}}
</style>
'''
if '</head>' not in s:
    raise SystemExit('No se encontró </head>')
s = s.replace('</head>', css + '\n</head>', 1)

p.write_text(s, encoding='utf-8')
print('COPAFEM extra courts by time patch OK')
