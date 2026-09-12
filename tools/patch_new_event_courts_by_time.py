from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_NEW_EVENT_COURTS_BY_RANGE_V2'
if MARK in s:
    print('new-event court ranges already applied')
    raise SystemExit

# -----------------------------------------------------------------------------
# 1) UI: solo Inicio > Fechas y categorías.
# -----------------------------------------------------------------------------
needle='''          </fieldset>\n          <button id="createEventBtn" class="btn primary date-create-btn" type="submit">Agregar categoría</button>'''
block=r'''          </fieldset>

          <section class="new-event-time-courts" id="COPAFEM_NEW_EVENT_COURTS_BY_RANGE_V2">
            <div class="new-event-time-head">
              <div>
                <strong>Canchas según horario <span>(opcional)</span></strong>
                <small>Indicá desde qué hora hasta qué hora están disponibles determinadas canchas para esta categoría.</small>
              </div>
            </div>
            <div class="new-event-time-row">
              <label>Desde
                <input id="newEventOverrideFrom" type="time" value="10:00" step="1800" />
              </label>
              <label>Hasta
                <input id="newEventOverrideTo" type="time" value="12:00" step="1800" />
              </label>
              <fieldset class="court-picker new-event-override-picker">
                <legend>Canchas disponibles en ese rango</legend>
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
              <button id="saveNewEventOverrideBtn" class="btn" type="button">Agregar rango</button>
            </div>
            <div id="newEventOverridesList" class="new-event-overrides-list"></div>
          </section>

          <button id="createEventBtn" class="btn primary date-create-btn" type="submit">Agregar categoría</button>'''
if needle not in s:
    raise SystemExit('No se encontró el selector de canchas del formulario Inicio')
s=s.replace(needle,block,1)

# -----------------------------------------------------------------------------
# 2) CSS limitado al formulario de alta de categoría.
# -----------------------------------------------------------------------------
css=r'''
<style id="COPAFEM_NEW_EVENT_COURTS_BY_RANGE_STYLE">
#newEventForm{
  --new-event-cat:var(--cat);
  --new-event-cat-soft:var(--cat-soft);
  --new-event-cat-ink:var(--cat-ink);
}
#newEventForm #newEventCategory{
  border:2px solid color-mix(in srgb,var(--new-event-cat) 58%,#d5e0eb)!important;
  background:linear-gradient(180deg,#fff,var(--new-event-cat-soft))!important;
  color:var(--new-event-cat-ink)!important;
  font-weight:900;
}
#newEventForm .court-options input:checked+span{
  background:var(--new-event-cat)!important;
  border-color:var(--new-event-cat)!important;
  color:#fff!important;
}
#newEventForm .date-create-btn{
  background:var(--new-event-cat)!important;
  border-color:var(--new-event-cat)!important;
}
.new-event-time-courts{
  grid-column:1/-1;
  border:1px solid color-mix(in srgb,var(--new-event-cat) 24%,#d5e0eb);
  border-radius:14px;
  background:color-mix(in srgb,var(--new-event-cat-soft) 55%,#fff);
  padding:12px;
  margin-top:2px;
}
.new-event-time-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;margin-bottom:9px}
.new-event-time-head strong{display:block;color:var(--new-event-cat-ink);font-size:13px}
.new-event-time-head strong span{color:var(--muted);font-weight:700}
.new-event-time-head small{display:block;color:var(--muted);font-size:11px;margin-top:3px}
.new-event-time-row{display:grid;grid-template-columns:135px 135px minmax(350px,1fr) auto;gap:10px;align-items:end}
.new-event-time-row>label{font-size:12px;color:#5b6573;font-weight:800}
.new-event-time-row input[type="time"]{width:100%;margin-top:6px;border:1px solid #d5e0eb;border-radius:11px;padding:10px 11px;background:#fff;min-height:44px}
.new-event-override-picker{background:#fff}
#saveNewEventOverrideBtn{min-height:44px;border-color:color-mix(in srgb,var(--new-event-cat) 42%,#d7d9de);color:var(--new-event-cat-ink)}
.new-event-overrides-list{display:flex;flex-wrap:wrap;gap:7px;margin-top:10px}
.new-event-override-chip{display:flex;align-items:center;gap:8px;border:1px solid color-mix(in srgb,var(--new-event-cat) 26%,#d8e3ed);background:#fff;border-radius:10px;padding:7px 8px 7px 10px;font-size:11px;color:#516174}
.new-event-override-chip strong{color:var(--new-event-cat-ink)}
.new-event-override-chip button{border:0;background:#f1f5f9;color:#7a8796;width:25px;height:25px;border-radius:7px;cursor:pointer;font-weight:900}
.new-event-override-empty{font-size:11px;color:var(--muted);padding:2px 0}
@media(max-width:1000px){.new-event-time-row{grid-template-columns:135px 135px 1fr}.new-event-override-picker{grid-column:1/-1}#saveNewEventOverrideBtn{grid-column:1/-1}}
@media(max-width:580px){.new-event-time-row{grid-template-columns:1fr 1fr}.new-event-override-picker,#saveNewEventOverrideBtn{grid-column:1/-1}}
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
  /* COPAFEM_NEW_EVENT_COURTS_BY_RANGE_V2 */
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

  function copafemTimeMinutes(v){
    const m=/^(\\d{2}):(\\d{2})$/.exec(String(v||''));
    return m ? Number(m[1])*60+Number(m[2]) : NaN;
  }

  function copafemMinutesTime(n){
    n=((Number(n)||0)%1440+1440)%1440;
    return String(Math.floor(n/60)).padStart(2,'0')+':'+String(n%60).padStart(2,'0');
  }

  function syncNewEventCategoryTheme(){
    const form=$("newEventForm"); if(!form)return;
    const cat=$("newEventCategory")?.value||'7ma';
    const c=CATEGORY_COLORS[cat]||CATEGORY_COLORS['7ma'];
    form.style.setProperty('--new-event-cat',c.main);
    form.style.setProperty('--new-event-cat-soft',c.soft);
    form.style.setProperty('--new-event-cat-ink',c.ink);
  }

  function syncNewEventOverridePicker(){
    setNewEventOverrideCourts(newEventBaseCourts());
  }

  function renderNewEventOverrides(){
    const list=$("newEventOverridesList"); if(!list)return;
    newEventTimeOverrides.sort((a,b)=>copafemTimeMinutes(a.from)-copafemTimeMinutes(b.from)||copafemTimeMinutes(a.to)-copafemTimeMinutes(b.to));
    list.innerHTML=newEventTimeOverrides.length
      ? newEventTimeOverrides.map((x,i)=>`<div class="new-event-override-chip"><strong>${esc(x.from)}–${esc(x.to)}</strong><span>Canchas ${esc(x.courts.join(', '))}</span><button type="button" data-new-event-override-remove="${i}" title="Quitar rango">✕</button></div>`).join('')
      : '<div class="new-event-override-empty">Sin rangos especiales. Se usarán las canchas seleccionadas arriba en todos los horarios.</div>';
    document.querySelectorAll('[data-new-event-override-remove]').forEach(b=>b.addEventListener('click',()=>{
      newEventTimeOverrides.splice(Number(b.dataset.newEventOverrideRemove),1);
      renderNewEventOverrides();
    }));
  }

  function saveNewEventTimeOverride(){
    const from=$("newEventOverrideFrom")?.value||'';
    const to=$("newEventOverrideTo")?.value||'';
    const a=copafemTimeMinutes(from),b=copafemTimeMinutes(to);
    if(!Number.isFinite(a)||!Number.isFinite(b)) return toast('Elegí hora desde y hasta');
    if(b<=a) return toast('La hora Hasta debe ser posterior a Desde');
    const courts=newEventOverrideCourts();
    if(!courts.length) return toast('Elegí al menos una cancha para ese rango');
    const row={from,to,courts:[...new Set(courts)]};
    const same=newEventTimeOverrides.findIndex(x=>x.from===from&&x.to===to);
    if(same>=0)newEventTimeOverrides[same]=row;else newEventTimeOverrides.push(row);
    renderNewEventOverrides();
    toast(`${from} a ${to}: canchas ${row.courts.join(', ')}`);
  }

  function resetNewEventTimeOverrides(){
    newEventTimeOverrides=[];
    const from=$("newEventOverrideFrom"),to=$("newEventOverrideTo");
    if(from)from.value='10:00';
    if(to)to.value='12:00';
    syncNewEventOverridePicker();
    renderNewEventOverrides();
  }

  function newEventOverridePayload(baseCourts){
    const base=new Set((baseCourts||[]).map(Number));
    const byTime=new Map();
    // Cada rango se convierte en turnos de 30 minutos. El límite "Hasta" es el fin del rango.
    newEventTimeOverrides.forEach(row=>{
      const start=copafemTimeMinutes(row.from),end=copafemTimeMinutes(row.to);
      for(let t=start;t<end;t+=30) byTime.set(copafemMinutesTime(t),new Set(row.courts.map(Number)));
    });
    const extraCourts=[],blockedCourts=[];
    [...byTime.entries()].forEach(([time,chosen])=>{
      chosen.forEach(c=>{if(!base.has(c))extraCourts.push({time,court:c});});
      base.forEach(c=>{if(!chosen.has(c))blockedCourts.push({time,court:c});});
    });
    return {extraCourts,blockedCourts};
  }

'''
needle_init='  function init(){\n'
if needle_init not in s:
    raise SystemExit('No se encontró function init')
s=s.replace(needle_init,helpers+needle_init,1)

# -----------------------------------------------------------------------------
# 4) Conectar controles; cambiar color inmediatamente al elegir categoría.
# -----------------------------------------------------------------------------
old_cat='''    $("newEventCategory").addEventListener("change",e=>setNewEventCourts(suggestedCourtsFor(e.target.value)));'''
new_cat='''    $("newEventCategory").addEventListener("change",e=>{setNewEventCourts(suggestedCourtsFor(e.target.value));syncNewEventCategoryTheme();resetNewEventTimeOverrides();});'''
if old_cat not in s:
    raise SystemExit('No se encontró listener newEventCategory')
s=s.replace(old_cat,new_cat,1)

listener_anchor='''    $("saveSettingsBtn").addEventListener("click", readSettings);'''
listener_add='''    $("saveNewEventOverrideBtn")?.addEventListener("click", saveNewEventTimeOverride);
    document.querySelectorAll('input[name="newEventCourt"]').forEach(x=>x.addEventListener('change',syncNewEventOverridePicker));
    syncNewEventCategoryTheme();
    renderNewEventOverrides();
    syncNewEventOverridePicker();
    $("saveSettingsBtn").addEventListener("click", readSettings);'''
if listener_anchor not in s:
    raise SystemExit('No se encontró ancla saveSettingsBtn')
s=s.replace(listener_anchor,listener_add,1)

# -----------------------------------------------------------------------------
# 5) Al crear la categoría, expandir los rangos a extras/bloqueos por turno.
# -----------------------------------------------------------------------------
old_event='''    const event=defaultEvent({date,category,name:"Americano COPAFEM",startTime:"10:00",duration:30,courts});'''
new_event='''    const {extraCourts,blockedCourts}=newEventOverridePayload(courts);
    const event=defaultEvent({date,category,name:"Americano COPAFEM",startTime:"10:00",duration:30,courts,extraCourts,blockedCourts});'''
if old_event not in s:
    raise SystemExit('No se encontró creación de event esperada')
s=s.replace(old_event,new_event,1)

create_tail='''    toast(`${category} agregada al ${formatDate(date)} · Canchas ${courts.join(", ")}`);'''
create_tail_new='''    resetNewEventTimeOverrides();
    toast(`${category} agregada al ${formatDate(date)} · Canchas ${courts.join(", ")}`);'''
if create_tail not in s:
    raise SystemExit('No se encontró toast final createEvent')
s=s.replace(create_tail,create_tail_new,1)

p.write_text(s,encoding='utf-8')
print('COPAFEM: rangos de canchas y color de categoría aplicados al alta')
