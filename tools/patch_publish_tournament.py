from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_PUBLISH_TOURNAMENT_V1'
if MARK in s:
    print('publish tournament already applied')
    raise SystemExit

# 1) Persistir el estado de publicación por fecha/categoría.
needle="        dropMode: ['op1','op2','op3'].includes(t.dropMode) ? t.dropMode : 'op1'\n"
replacement="        dropMode: ['op1','op2','op3'].includes(t.dropMode) ? t.dropMode : 'op1',\n        published: t.published === true\n"
if needle not in s:
    raise SystemExit('No se encontró dropMode en defaultEvent')
s=s.replace(needle,replacement,1)

# 2) Botón Publicar en el administrador.
needle='''      <button id="adminChangeMode" class="mode-switch-btn" type="button">Cambiar perfil</button>\n      <span id="saveStatus" class="save-status">Guardado local</span>'''
replacement='''      <button id="adminChangeMode" class="mode-switch-btn" type="button">Cambiar perfil</button>\n      <button id="publishTournamentBtn" class="btn publish-tournament-btn" type="button">Publicar</button>\n      <span id="saveStatus" class="save-status">Guardado local</span>'''
if needle not in s:
    raise SystemExit('No se encontró top-actions del administrador')
s=s.replace(needle,replacement,1)

# 3) Cartel del jugador mientras no haya torneos publicados.
needle='''      <section class="player-select-panel"><div class="player-select-grid"><label>Fecha<select id="playerDate"></select></label><label>Categoría<select id="playerCategory"></select></label><label>Jugador<select id="playerName"></select></label></div></section>'''
replacement='''      <section id="playerBuilding" class="player-building" hidden>\n        <div class="player-building-icon">🎾</div>\n        <h2>TORNEO EN PROCESO DE ARMADO</h2>\n        <p>Estamos organizando los cuadros, horarios y cruces del torneo.</p>\n        <p>En breve vas a poder consultar toda la información desde aquí.</p>\n        <strong>¡Gracias por participar y ser parte de COPAFEM! 🏆</strong>\n      </section>\n      <section id="playerSelectPanel" class="player-select-panel"><div class="player-select-grid"><label>Fecha<select id="playerDate"></select></label><label>Categoría<select id="playerCategory"></select></label><label>Jugador<select id="playerName"></select></label></div></section>'''
if needle not in s:
    raise SystemExit('No se encontró selector del jugador')
s=s.replace(needle,replacement,1)

# 4) Estilos limitados a esta nueva función.
css=r'''
<style id="COPAFEM_PUBLISH_TOURNAMENT_V1">
.publish-tournament-btn{background:#2f7d62!important;border-color:#2f7d62!important;color:#fff!important;font-weight:900!important;min-width:110px}
.publish-tournament-btn.is-published{background:#fff3f0!important;border-color:#efc9c2!important;color:#a33b2d!important}
.player-building{margin:14px 0;background:#fff;border:1px solid #dbe7f2;border-top:5px solid #7b78bd;border-radius:20px;padding:30px 24px;text-align:center;box-shadow:0 8px 26px rgba(35,58,94,.06)}
.player-building-icon{font-size:38px;line-height:1;margin-bottom:12px}.player-building h2{margin:0 0 14px;color:#223a5e;font-size:clamp(21px,4vw,29px);letter-spacing:.02em}.player-building p{margin:7px auto;color:#5d6e84;max-width:650px;line-height:1.55;font-size:14px}.player-building strong{display:block;margin-top:17px;color:#334066;font-size:15px}
@media(max-width:580px){.publish-tournament-btn{min-width:0;padding:8px 10px!important}.player-building{padding:24px 17px}}
@media print{.publish-tournament-btn,.player-building{display:none!important}}
</style>
'''
if '</head>' not in s:
    raise SystemExit('No se encontró </head>')
s=s.replace('</head>',css+'\n</head>',1)

# 5) Lógica del administrador: publicar o quitar publicación de la fecha/categoría activa.
needle='''  function renderHeader(){'''
helpers=r'''  function renderPublishButton(){
    const b=$("publishTournamentBtn"); if(!b)return;
    const hasDate=!!state?.tournament?.date;
    const published=state?.tournament?.published===true;
    b.textContent=published?'Quitar publicación':'Publicar';
    b.classList.toggle('is-published',published);
    b.disabled=!hasDate;
    b.title=!hasDate?'Primero creá una fecha':published?'Ocultar esta fecha y categoría del perfil del jugador':'Publicar esta fecha y categoría para los jugadores';
  }

  function togglePublishActiveTournament(){
    if(!state?.tournament?.date) return toast('Primero creá una fecha');
    const next=state.tournament.published!==true;
    state.tournament.published=next;
    saveState();
    renderPublishButton();
    toast(next?'Torneo publicado para los jugadores':'Publicación retirada del perfil del jugador');
  }

  function renderHeader(){
    renderPublishButton();'''
if needle not in s:
    raise SystemExit('No se encontró renderHeader')
s=s.replace(needle,helpers,1)

needle='''    $("printBtn").addEventListener("click", ()=>window.print());'''
replacement='''    $("publishTournamentBtn")?.addEventListener("click", togglePublishActiveTournament);\n    $("printBtn").addEventListener("click", ()=>window.print());'''
if needle not in s:
    raise SystemExit('No se encontró listener printBtn')
s=s.replace(needle,replacement,1)

# 6) En modo jugador, solo las fechas publicadas son visibles.
needle='''  function allEvents(){return Object.entries(loadStore().events||{}).filter(([,e])=>e?.tournament).sort((a,b)=>(a[1].tournament.date||"9999").localeCompare(b[1].tournament.date||"9999")||CATS.indexOf(a[1].tournament.category)-CATS.indexOf(b[1].tournament.category));}'''
replacement='''  function allStoredEvents(){return Object.entries(loadStore().events||{}).filter(([,e])=>e?.tournament).sort((a,b)=>(a[1].tournament.date||"9999").localeCompare(b[1].tournament.date||"9999")||CATS.indexOf(a[1].tournament.category)-CATS.indexOf(b[1].tournament.category));}\n  function allEvents(){return allStoredEvents().filter(([,e])=>e.tournament.published===true);}'''
if needle not in s:
    raise SystemExit('No se encontró allEvents del jugador')
s=s.replace(needle,replacement,1)

needle='''  function populateDates(){\n    const dates=[...new Set(allEvents().map(([,e])=>e.tournament.date).filter(Boolean))];\n    const s=el("playerDate");s.innerHTML=dates.length?dates.map(d=>`<option value="${ehtml(d)}">${ehtml(formatDate(d))}</option>`).join(""):`<option value="">Sin fechas cargadas</option>`;\n    populateCategories();\n  }'''
replacement='''  function setPlayerBuildingState(show){\n    const building=el("playerBuilding"),selector=el("playerSelectPanel");\n    if(building)building.hidden=!show;\n    if(selector)selector.hidden=show;\n    if(show){el("playerEmpty").hidden=true;el("playerContent").hidden=true;selectedPairId="";}\n  }\n  function populateDates(){\n    const dates=[...new Set(allEvents().map(([,e])=>e.tournament.date).filter(Boolean))];\n    const s=el("playerDate");\n    if(!dates.length){\n      setPlayerBuildingState(true);\n      s.innerHTML='<option value="">Próximamente</option>';\n      el("playerCategory").innerHTML='<option value="">Próximamente</option>';\n      el("playerName").innerHTML='<option value="">Próximamente</option>';\n      return;\n    }\n    setPlayerBuildingState(false);\n    s.innerHTML=dates.map(d=>`<option value="${ehtml(d)}">${ehtml(formatDate(d))}</option>`).join("");\n    populateCategories();\n  }'''
if needle not in s:
    raise SystemExit('No se encontró populateDates del jugador')
s=s.replace(needle,replacement,1)

s=s.replace('</body>', '<!-- '+MARK+' -->\n</body>',1)
p.write_text(s,encoding='utf-8')
print('COPAFEM: publicación manual reversible del torneo aplicada')
