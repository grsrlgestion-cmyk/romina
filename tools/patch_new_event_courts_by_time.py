from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_NEW_EVENT_COURTS_BY_TIME_V1'
if MARK in s:
    print('new-event courts by time already applied')
    raise SystemExit

# -----------------------------------------------------------------------------
# 1) UI: solo dentro de Inicio > Fechas y categorías.
# -----------------------------------------------------------------------------
needle='''          </fieldset>\n          <button id="createEventBtn" class="btn primary date-create-btn" type="submit">Agregar categoría</button>'''
block=r'''          </fieldset>

          <section class="new-event-time-courts" id="COPAFEM_NEW_EVENT_COURTS_BY_TIME_V1">
            <div class="new-event-time-head">
              <div>
                <strong>Canchas según horario <span>(opcional)</span></strong>
                <small>Modificá solamente los turnos que usan canchas distintas a las seleccionadas arriba.</small>
              </div>
            </div>
            <div class="new-event-time-row">
              <label>Horario
                <input id="newEventOverrideTime" type="time" value="10:00" step="1800" />
              </label>
              <fieldset class="court-picker new-event-override-picker">
                <legend>Canchas disponibles en ese horario</legend>
                <div class="court-options">
                  <label><input type="checkbox" name="newEventOverrideCourt" value="1"><span>1</span></label>
                  <label><input type="checkbox" name="newEventOverrideCourt" value="2"><span>2</span></label>
                  <label><input type="checkbox" name="newEventOverrideCourt" value="3"><span>3</span></label>
                  <label><input type="checkbox" name="newEventOverrideCourt" value="4"><span>4</span></label>
                  <label><input type="checkbox" name="newEventOverrideCourt" value="5"><span>5</span></label>
                  <label><input type="checkbox" name="newEventOverrideCourt" value="6"><span>6</span></label>
                  <label><input type="checkbox" name="newEventOverrideCourt" value="7"><span>7</span></label>
                  <label><input type="checkbox" name="newEventOverrideCourt" value="8"><span>8</span></label>
                </div>
              </fieldset>
              <button id="saveNewEventOverrideBtn" class="btn" type="button">Guardar horario</button>
            </div>
            <div id="newEventOverridesList" class="new-event-overrides-list"></div>
          </section>

          <button id="createEventBtn" class="btn primary date-create-btn" type="submit">Agregar categoría</button>'''
if needle not in s:
    raise SystemExit('No se encontró el selector de canchas del formulario Inicio')
s=s.replace(needle,block,1)

# -----------------------------------------------------------------------------
# 2) CSS limitado al nuevo bloque.
# -----------------------------------------------------------------------------
css=r'''
<style id="COPAFEM_NEW_EVENT_COURTS_BY_TIME_STYLE">
.new-event-time-courts{
  grid-column:1/-1;
  border:1px solid #d5e0eb;
  border-radius:14px;
  background:#f9fbfd;
  padding:12px;
  margin-top:2px;
}
.new-event-time-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;margin-bottom:9px}
.new-event-time-head strong{display:block;color:var(--ink);font-size:13px}
.new-event-time-head strong span{color:var(--muted);font-weight:700}
.new-event-time-head small{display:block;color:var(--muted);font-size:11px;margin-top:3px}
.new-event-time-row{display:grid;grid-template-columns:150px minmax(350px,1fr) auto;gap:10px;align-items:end}
.new-event-time-row>label{font-size:12px;color:#5b6573;font-weight:800}
.new-event-time-row input[type="time"]{width:100%;margin-top:6px;border:1px solid #d5e0eb;border-radius:11px;padding:10px 11px;background:#fff;min-height:44px}
.new-event-override-picker{background:#fff}
#saveNewEventOverrideBtn{min-height:44px}
.new-event-overrides-list{display:flex;flex-wrap:wrap;gap:7px;margin-top:10px}
.new-event-override-chip{display:flex;align-items:center;gap:8px;border:1px solid #d8e3ed;background:#fff;border-radius:10px;padding:7px 8px 7px 10px;font-size:11px;color:#516174}
.new-event-override-chip strong{color:var(--ink)}
.new-event-override-chip button{border:0;background:#f1f5f9;color:#7a8796;width:25px;height:25px;border-radius:7px;cursor:pointer;font-weight:900}
.new-event-override-empty{font-size:11px;color:var(--muted);padding:2px 0}
@media(max-width:900px){.new-event-time-row{grid-template-columns:150px 1fr}.new-event-override-picker{grid-column:1/-1}#saveNewEventOverrideBtn{grid-column:1/-1}}
@media(max-width:580px){.new-event-time-row{grid-template-columns:1fr}.new-event-override-picker,#saveNewEventOverrideBtn{grid-column:auto}}
@media print{.new-event-time-courts{display:none!important}}
</style>
'''
if '</head>' not in s:
    raise SystemExit('No se encontró </head>')
s=s.replace('</head>',css+'\n</head>',1)

# -----------------------------------------------------------------------------
# 3) Estado y helpers dentro del IIFE administrador.
# -----------------------------------------------------------------------------
helpers=r'''
  /* COPAFEM_NEW_EVENT_COURTS_BY_TIME_V1 */
  let newEventTimeOverrides=[];

  function newEventBaseCourts(){
    return [...document.querySelectorAll('input[name="newEventCourt"]:checked')]
      .map(x=>Number(x.value)).filter(Number.isFinite).sort((a,b)=>a-b);
  }

  function newEventOverrideCourts(){
    return [...document.querySelectorAll('input[name="newEventOverrideCourt"]:checked')]
      .map(x=>Number(x.value)).filter(Number.isFinite).sort((a,b)=>a-b);
  }

  function setNewEventOverrideCourts(courts){
    const wanted=new Set((courts||[]).map(Number));
    document.querySelectorAll('input[name="newEventOverrideCourt"]').forEach(x=>x.checked=wanted.has(Number(x.value)));
  }

  function selectedNewEventOverride(){
    const time=$("newEventOverrideTime")?.value||"";
    return newEventTimeOverrides.find(x=>x.time===time)||null;
  }

  function syncNewEventOverridePicker(){
    const saved=selectedNewEventOverride();
    setNewEventOverrideCourts(saved?saved.courts:newEventBaseCourts());
  }

  function renderNewEventOverrides(){
    const list=$("newEventOverridesList"); if(!list)return;
    newEventTimeOverrides.sort((a,b)=>parseTime(a.time)-parseTime(b.time));
    list.innerHTML=newEventTimeOverrides.length
      ? newEventTimeOverrides.map(x=>`<div class="new-event-override-chip"><strong>${esc(x.time)}</strong><span>Canchas ${esc(x.courts.join(', ')||'ninguna')}</span><button type="button" data-new-event-override-remove="${esc(x.time)}" title="Quitar horario">✕</button></div>`).join('')
      : '<div class="new-event-override-empty">Sin modificaciones por horario. Se usarán las canchas seleccionadas arriba en todos los turnos.</div>';
    document.querySelectorAll('[data-new-event-override-remove]').forEach(b=>b.addEventListener('click',()=>{
      const time=b.dataset.newEventOverrideRemove;
      newEventTimeOverrides=newEventTimeOverrides.filter(x=>x.time!==time);
      renderNewEventOverrides();
      if($("newEventOverrideTime")?.value===time) syncNewEventOverridePicker();
    }));
  }

  function saveNewEventTimeOverride(){
    const time=$("newEventOverrideTime")?.value||"";
    if(!/^\\d{2}:\\d{2}$/.test(time)) return toast('Elegí el horario');
    const courts=newEventOverrideCourts();
    if(!courts.length) return toast('Elegí al menos una cancha para ese horario');
    const base=newEventBaseCourts();
    if(courts.join(',')===base.join(',')){
      newEventTimeOverrides=newEventTimeOverrides.filter(x=>x.time!==time);
      renderNewEventOverrides();
      return toast(`${time}: se usarán las canchas base`);
    }
    const row={time,courts:[...new Set(courts)]};
    const i=newEventTimeOverrides.findIndex(x=>x.time===time);
    if(i>=0)newEventTimeOverrides[i]=row;else newEventTimeOverrides.push(row);
    renderNewEventOverrides();
    toast(`${time}: canchas ${row.courts.join(', ')}`);
  }

  function resetNewEventTimeOverrides(){
    newEventTimeOverrides=[];
    const time=$("newEventOverrideTime"); if(time)time.value='10:00';
    syncNewEventOverridePicker();
    renderNewEventOverrides();
  }

  function newEventOverridePayload(baseCourts){
    const base=new Set((baseCourts||[]).map(Number));
    const extraCourts=[],blockedCourts=[];
    newEventTimeOverrides.forEach(row=>{
      const chosen=new Set(row.courts.map(Number));
      chosen.forEach(c=>{if(!base.has(c))extraCourts.push({time:row.time,court:c});});
      base.forEach(c=>{if(!chosen.has(c))blockedCourts.push({time:row.time,court:c});});
    });
    return {extraCourts,blockedCourts};
  }

'''
needle_init='  function init(){\n'
if needle_init not in s:
    raise SystemExit('No se encontró function init')
s=s.replace(needle_init,helpers+needle_init,1)

# -----------------------------------------------------------------------------
# 4) Conectar únicamente los nuevos controles y sincronizar al cambiar categoría.
# -----------------------------------------------------------------------------
old_cat='''    $("newEventCategory").addEventListener("change",e=>setNewEventCourts(suggestedCourtsFor(e.target.value)));'''
new_cat='''    $("newEventCategory").addEventListener("change",e=>{setNewEventCourts(suggestedCourtsFor(e.target.value));resetNewEventTimeOverrides();});'''
if old_cat not in s:
    raise SystemExit('No se encontró listener newEventCategory')
s=s.replace(old_cat,new_cat,1)

listener_anchor='''    $("saveSettingsBtn").addEventListener("click", readSettings);'''
listener_add='''    $("saveNewEventOverrideBtn")?.addEventListener("click", saveNewEventTimeOverride);
    $("newEventOverrideTime")?.addEventListener("change", syncNewEventOverridePicker);
    document.querySelectorAll('input[name="newEventCourt"]').forEach(x=>x.addEventListener('change',()=>{if(!selectedNewEventOverride())syncNewEventOverridePicker();}));
    renderNewEventOverrides();
    syncNewEventOverridePicker();
    $("saveSettingsBtn").addEventListener("click", readSettings);'''
if listener_anchor not in s:
    raise SystemExit('No se encontró ancla saveSettingsBtn')
s=s.replace(listener_anchor,listener_add,1)

# -----------------------------------------------------------------------------
# 5) Al crear la categoría, convertir la selección horaria en extras/bloqueos.
#    No se toca ninguna otra lógica de createEvent.
# -----------------------------------------------------------------------------
old_event='''    const event=defaultEvent({date,category,name:"Americano COPAFEM",startTime:"10:00",duration:30,courts});'''
new_event='''    const {extraCourts,blockedCourts}=newEventOverridePayload(courts);
    const event=defaultEvent({date,category,name:"Americano COPAFEM",startTime:"10:00",duration:30,courts,extraCourts,blockedCourts});'''
if old_event not in s:
    raise SystemExit('No se encontró creación de event esperada')
s=s.replace(old_event,new_event,1)

# Resetear solamente el mini-editor horario después de crear la categoría.
create_tail='''    toast(`${category} agregada al ${formatDate(date)} · Canchas ${courts.join(", ")}`);'''
create_tail_new='''    resetNewEventTimeOverrides();
    toast(`${category} agregada al ${formatDate(date)} · Canchas ${courts.join(", ")}`);'''
if create_tail not in s:
    raise SystemExit('No se encontró toast final createEvent')
s=s.replace(create_tail,create_tail_new,1)

p.write_text(s,encoding='utf-8')
print('COPAFEM: canchas por horario agregadas al formulario de nueva categoría')
