from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")

new_css = r'''/* ===== PORTADA COPAFEM PROFESIONAL ===== */
.cover-gateway{
  --cover-navy:#123d72;
  --cover-navy-2:#0b2f5c;
  --cover-blue:#dceafb;
  --cover-gold:#c89c3f;
  min-height:100svh;
  position:relative;
  display:grid;
  place-items:center;
  padding:clamp(18px,3vw,42px);
  overflow:auto;
  background:
    radial-gradient(circle at 13% 8%,rgba(182,211,242,.55),transparent 30%),
    radial-gradient(circle at 88% 14%,rgba(218,232,247,.9),transparent 27%),
    linear-gradient(145deg,#fdfefe 0%,#f2f7fd 55%,#e9f2fb 100%);
}
.cover-gateway::before{
  content:"";
  position:fixed;
  inset:auto -10vw -30vh auto;
  width:58vw;
  height:58vw;
  border:2px solid rgba(18,61,114,.08);
  border-radius:50%;
  box-shadow:0 0 0 58px rgba(255,255,255,.22),0 0 0 120px rgba(18,61,114,.025);
  pointer-events:none;
}
.cover-gateway::after{
  content:"";
  position:fixed;
  left:-8vw;
  top:17vh;
  width:40vw;
  height:17vw;
  background:linear-gradient(135deg,rgba(157,195,234,.28),rgba(255,255,255,0));
  border-radius:44px;
  transform:rotate(-14deg);
  pointer-events:none;
}
.cover-stage{
  width:min(1180px,100%);
  position:relative;
  z-index:2;
}
.cover-shell{
  display:grid;
  grid-template-columns:minmax(390px,.9fr) minmax(420px,1.1fr);
  min-height:min(720px,calc(100svh - 70px));
  border:1px solid rgba(18,61,114,.10);
  border-radius:36px;
  overflow:hidden;
  background:rgba(255,255,255,.93);
  box-shadow:0 34px 90px rgba(22,58,99,.16);
  backdrop-filter:blur(18px);
}
.cover-main{
  padding:clamp(34px,5vw,64px);
  display:flex;
  flex-direction:column;
  justify-content:center;
  background:linear-gradient(180deg,rgba(255,255,255,.98),rgba(248,251,255,.98));
}
.cover-logo-wrap{
  display:flex;
  justify-content:center;
  margin-bottom:22px;
}
.cover-logo{
  width:min(300px,76%);
  height:auto;
  object-fit:contain;
  display:block;
  filter:drop-shadow(0 12px 24px rgba(18,61,114,.10));
}
.cover-kicker{
  text-align:center;
  color:var(--cover-gold);
  font-size:11px;
  font-weight:900;
  letter-spacing:.28em;
  text-transform:uppercase;
  margin-bottom:11px;
}
.cover-title{
  margin:0;
  color:var(--cover-navy-2);
  text-align:center;
  font-family:Georgia,"Times New Roman",serif;
  font-size:clamp(44px,5vw,70px);
  line-height:1;
  letter-spacing:.08em;
}
.cover-rule{
  display:flex;
  align-items:center;
  gap:12px;
  margin:19px auto 18px;
  width:min(330px,82%);
}
.cover-rule::before,.cover-rule::after{content:"";height:1px;flex:1;background:linear-gradient(90deg,transparent,var(--cover-gold))}
.cover-rule::after{background:linear-gradient(90deg,var(--cover-gold),transparent)}
.cover-rule span{color:var(--cover-gold);font-size:20px}
.cover-subtitle{
  margin:0 auto 28px;
  max-width:430px;
  text-align:center;
  color:#60738b;
  font-size:15px;
  line-height:1.65;
}
.cover-actions{display:grid;gap:12px}
.cover-player-btn{
  width:100%;
  border:0;
  border-radius:18px;
  min-height:62px;
  padding:16px 20px;
  background:linear-gradient(135deg,var(--cover-navy),#1d558f);
  color:#fff;
  font-weight:900;
  font-size:18px;
  letter-spacing:.03em;
  cursor:pointer;
  box-shadow:0 14px 30px rgba(18,61,114,.22);
  display:flex;
  align-items:center;
  justify-content:center;
  gap:12px;
  transition:.2s ease;
}
.cover-player-btn:hover{transform:translateY(-2px);box-shadow:0 18px 36px rgba(18,61,114,.27)}
.cover-player-btn .arrow{font-size:25px;color:#f4d98f;line-height:1}
.cover-player-note{text-align:center;color:#718196;font-size:12px;margin-top:2px}
.cover-admin-btn{
  margin-top:8px;
  min-height:52px;
  border:1px solid #d7e3ef;
  border-radius:16px;
  background:#fff;
  color:var(--cover-navy);
  font-weight:850;
  cursor:pointer;
  display:flex;
  align-items:center;
  justify-content:center;
  gap:9px;
  transition:.18s ease;
}
.cover-admin-btn:hover{background:#f5f9fd;border-color:#c4d7ea}
.cover-footnote{
  margin-top:24px;
  display:flex;
  justify-content:center;
  gap:10px;
  align-items:center;
  color:#7c8b9d;
  font-size:11px;
  font-weight:800;
  letter-spacing:.16em;
  text-transform:uppercase;
}
.cover-footnote i{width:4px;height:4px;border-radius:50%;background:var(--cover-gold)}
.cover-visual{
  position:relative;
  overflow:hidden;
  background:
    radial-gradient(circle at 66% 26%,rgba(255,255,255,.36),transparent 18%),
    linear-gradient(145deg,#0c386a 0%,#164f87 48%,#8bb6dc 100%);
  display:flex;
  flex-direction:column;
  justify-content:space-between;
  padding:clamp(34px,4vw,54px);
  color:#fff;
}
.cover-visual::before{
  content:"";
  position:absolute;
  inset:0;
  opacity:.50;
  background-image:
    linear-gradient(rgba(255,255,255,.12) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.12) 1px,transparent 1px);
  background-size:86px 86px;
  transform:perspective(720px) rotateX(59deg) scale(1.45) translateY(12%);
  transform-origin:center bottom;
}
.cover-visual::after{
  content:"";
  position:absolute;
  width:390px;
  height:390px;
  right:-120px;
  bottom:-100px;
  border:2px solid rgba(255,255,255,.18);
  border-radius:50%;
  box-shadow:0 0 0 55px rgba(255,255,255,.035),0 0 0 110px rgba(255,255,255,.025);
}
.cover-visual-top,.cover-visual-center,.cover-visual-bottom{position:relative;z-index:2}
.cover-visual-top{display:flex;justify-content:flex-end;gap:12px;font-size:11px;font-weight:850;letter-spacing:.18em;text-transform:uppercase;color:#eaf4ff}
.cover-visual-top span+span::before{content:"•";color:#e9bf60;margin-right:12px}
.cover-visual-center{max-width:480px}
.cover-visual-center .small{font-size:12px;font-weight:900;letter-spacing:.24em;text-transform:uppercase;color:#c9ddf2}
.cover-visual-center h2{margin:12px 0 14px;font-family:Georgia,"Times New Roman",serif;font-size:clamp(42px,5vw,72px);line-height:1.02;letter-spacing:-.02em}
.cover-visual-center p{margin:0;max-width:420px;color:#e3eef9;font-size:16px;line-height:1.7}
.cover-court-card{
  margin-top:30px;
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:1px;
  border:1px solid rgba(255,255,255,.20);
  border-radius:18px;
  overflow:hidden;
  background:rgba(255,255,255,.16);
  backdrop-filter:blur(8px);
}
.cover-court-card div{padding:17px 13px;background:rgba(5,35,67,.18);text-align:center}
.cover-court-card strong{display:block;font-size:19px;color:#fff}.cover-court-card span{display:block;margin-top:4px;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#cfe1f2}
.cover-visual-bottom{font-size:12px;letter-spacing:.22em;text-transform:uppercase;font-weight:850;color:#dceaf7}
.cover-visual-bottom b{color:#efc96f;font-weight:900}
.cover-login{
  position:fixed!important;
  z-index:120!important;
  left:50%;top:50%;transform:translate(-50%,-50%);
  width:min(460px,calc(100vw - 28px));
  margin:0!important;
  box-shadow:0 28px 80px rgba(13,43,78,.32)!important;
  border:1px solid #d9e5f0!important;
}
@media(max-width:900px){
  .cover-gateway{place-items:start center;padding:14px}
  .cover-shell{grid-template-columns:1fr;min-height:auto;max-width:690px}
  .cover-main{padding:34px 26px}
  .cover-logo{width:min(250px,66vw)}
  .cover-visual{min-height:350px;padding:30px}
  .cover-visual-center h2{font-size:44px}
}
@media(max-width:560px){
  .cover-gateway{padding:0;background:#f5f9fd}
  .cover-shell{border-radius:0;border:0;box-shadow:none;min-height:100svh;width:100%}
  .cover-main{padding:28px 20px 24px}
  .cover-logo{width:min(220px,72vw)}
  .cover-title{font-size:42px}
  .cover-subtitle{font-size:14px;margin-bottom:22px}
  .cover-player-btn{min-height:58px;font-size:17px}
  .cover-visual{min-height:290px;padding:26px 22px}
  .cover-visual-top{justify-content:flex-start}
  .cover-visual-center h2{font-size:38px;margin-top:8px}
  .cover-visual-center p{font-size:14px}
  .cover-court-card div{padding:13px 7px}.cover-court-card strong{font-size:16px}.cover-court-card span{font-size:8px}
}
'''

new_html = r'''  <section id="roleGateway" class="cover-gateway">
    <div class="cover-stage">
      <div class="cover-shell">
        <div class="cover-main">
          <div class="cover-logo-wrap">
            <img class="cover-logo" src="logo-copafem-real.png?v=20260911" alt="COPAFEM · Argentina">
          </div>
          <div class="cover-kicker">San Juan · Argentina</div>
          <h1 class="cover-title">INGRESO</h1>
          <div class="cover-rule" aria-hidden="true"><span>♡</span></div>
          <p class="cover-subtitle">Ingresá a COPAFEM para consultar tus horarios, resultados, zonas y el Drop completo del torneo.</p>
          <div class="cover-actions">
            <button id="choosePlayer" class="cover-player-btn" type="button" aria-label="Ingresar como jugador">
              <span>INGRESAR COMO JUGADOR</span><span class="arrow">→</span>
            </button>
            <div class="cover-player-note">Acceso directo · no requiere registro previo</div>
            <button id="chooseAdmin" class="cover-admin-btn" type="button" aria-label="Acceso administrador">
              <span aria-hidden="true">⚙</span><span>Acceso administrador</span>
            </button>
          </div>
          <div class="cover-footnote"><span>Torneos</span><i></i><span>Comunidad</span><i></i><span>Pádel</span></div>
        </div>
        <aside class="cover-visual" aria-hidden="true">
          <div class="cover-visual-top"><span>COPAFEM</span><span>2026</span></div>
          <div class="cover-visual-center">
            <div class="small">Más que un torneo</div>
            <h2>El pádel<br>también nos une.</h2>
            <p>Una experiencia simple y clara para seguir cada fecha, cada partido y cada cruce.</p>
            <div class="cover-court-card">
              <div><strong>ZONAS</strong><span>Clasificación</span></div>
              <div><strong>ORO</strong><span>Competencia</span></div>
              <div><strong>PLATA</strong><span>Comunidad</span></div>
            </div>
          </div>
          <div class="cover-visual-bottom"><b>NO PUEDO, TENGO PÁDEL</b> · ARGENTINA</div>
        </aside>
      </div>
    </div>
    <div id="adminLogin" class="login-card cover-login" hidden>
      <h2>Acceso administrador</h2><p>Ingresá la contraseña para abrir el panel de organización.</p>
      <form id="adminLoginForm"><label>Contraseña<input id="adminPassword" type="password" autocomplete="current-password" required placeholder="Contraseña de administrador"></label><div class="login-actions"><button class="btn primary" type="submit">Ingresar</button><button id="cancelAdminLogin" class="btn" type="button">Volver</button></div><div id="adminLoginError" class="login-error" aria-live="polite"></div></form>
    </div>
  </section>
'''

css_marker = "/* ===== PORTADA COPAFEM ===== */"
if css_marker not in text:
    css_marker = "/* ===== PORTADA COPAFEM PROFESIONAL ===== */"
css_start = text.index(css_marker)
style_close = text.index("</style>", css_start)
text = text[:css_start] + new_css + "\n\n  " + text[style_close:]

html_start = text.index('  <section id="roleGateway" class="cover-gateway">')
player_start = text.index('  <section id="playerApp" hidden>', html_start)
text = text[:html_start] + new_html + "\n" + text[player_start:]

path.write_text(text, encoding="utf-8")
print("Portada profesional COPAFEM con logo real aplicada")
