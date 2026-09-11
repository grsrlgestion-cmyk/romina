from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")

new_css = r'''/* ===== PORTADA COPAFEM SIMPLE ===== */
.cover-gateway{
  --cover-navy:#103a6d;
  --cover-gold:#c89c3f;
  min-height:100svh;
  position:relative;
  display:flex;
  align-items:center;
  justify-content:center;
  padding:clamp(22px,4vw,54px);
  overflow:auto;
  background:
    radial-gradient(circle at 15% 10%,rgba(190,216,242,.52),transparent 30%),
    radial-gradient(circle at 86% 18%,rgba(220,233,247,.75),transparent 28%),
    linear-gradient(180deg,#fafdff 0%,#eef5fc 100%);
}
.cover-gateway::before{
  content:"";
  position:fixed;
  width:64vw;
  height:64vw;
  right:-26vw;
  bottom:-38vw;
  border:1px solid rgba(16,58,109,.07);
  border-radius:50%;
  box-shadow:0 0 0 60px rgba(255,255,255,.26),0 0 0 120px rgba(16,58,109,.025);
  pointer-events:none;
}
.cover-stage{
  width:min(560px,100%);
  position:relative;
  z-index:2;
}
.cover-shell{
  width:100%;
  border:1px solid rgba(16,58,109,.10);
  border-radius:32px;
  background:rgba(255,255,255,.94);
  box-shadow:0 28px 75px rgba(24,61,103,.14);
  backdrop-filter:blur(14px);
  overflow:hidden;
}
.cover-main{
  padding:clamp(34px,6vw,58px);
  display:flex;
  flex-direction:column;
  align-items:center;
  text-align:center;
}
.cover-logo-wrap{
  display:flex;
  justify-content:center;
  width:100%;
  margin-bottom:18px;
}
.cover-logo{
  width:min(300px,78vw);
  max-height:300px;
  height:auto;
  object-fit:contain;
  display:block;
  filter:drop-shadow(0 9px 22px rgba(16,58,109,.08));
}
.cover-kicker{
  color:var(--cover-gold);
  font-size:11px;
  font-weight:900;
  letter-spacing:.24em;
  text-transform:uppercase;
  margin-bottom:9px;
}
.cover-title{
  margin:0;
  color:var(--cover-navy);
  font-family:Georgia,"Times New Roman",serif;
  font-size:clamp(48px,8vw,72px);
  line-height:1;
  letter-spacing:.07em;
}
.cover-rule{
  display:flex;
  align-items:center;
  gap:10px;
  margin:18px auto 16px;
  width:min(280px,72%);
}
.cover-rule::before,.cover-rule::after{
  content:"";
  height:1px;
  flex:1;
  background:linear-gradient(90deg,transparent,var(--cover-gold));
}
.cover-rule::after{background:linear-gradient(90deg,var(--cover-gold),transparent)}
.cover-rule span{color:var(--cover-gold);font-size:18px}
.cover-subtitle{
  margin:0 auto 24px;
  max-width:410px;
  color:#62758c;
  font-size:14px;
  line-height:1.55;
}
.cover-actions{
  width:100%;
  max-width:410px;
  display:grid;
  gap:10px;
}
.cover-player-btn{
  width:100%;
  border:0;
  border-radius:16px;
  min-height:58px;
  padding:14px 18px;
  background:linear-gradient(135deg,#103a6d,#1b548f);
  color:#fff;
  font-weight:900;
  font-size:16px;
  letter-spacing:.03em;
  cursor:pointer;
  box-shadow:0 12px 26px rgba(16,58,109,.20);
  display:flex;
  align-items:center;
  justify-content:center;
  gap:10px;
  transition:.18s ease;
}
.cover-player-btn:hover{transform:translateY(-1px);box-shadow:0 16px 30px rgba(16,58,109,.24)}
.cover-player-btn .arrow{font-size:22px;color:#f0cf80;line-height:1}
.cover-player-note{color:#8190a1;font-size:11px;margin:0 0 2px}
.cover-admin-btn{
  min-height:49px;
  border:1px solid #d8e3ee;
  border-radius:15px;
  background:#fff;
  color:var(--cover-navy);
  font-weight:850;
  cursor:pointer;
  display:flex;
  align-items:center;
  justify-content:center;
  gap:8px;
  transition:.18s ease;
}
.cover-admin-btn:hover{background:#f6f9fc;border-color:#c9d8e7}
.cover-footnote{
  margin-top:22px;
  display:flex;
  justify-content:center;
  gap:9px;
  align-items:center;
  color:#8b98a7;
  font-size:10px;
  font-weight:800;
  letter-spacing:.14em;
  text-transform:uppercase;
}
.cover-footnote i{width:4px;height:4px;border-radius:50%;background:var(--cover-gold)}
.cover-login{
  position:fixed!important;
  z-index:120!important;
  left:50%;top:50%;transform:translate(-50%,-50%);
  width:min(460px,calc(100vw - 28px));
  margin:0!important;
  box-shadow:0 28px 80px rgba(13,43,78,.30)!important;
  border:1px solid #d9e5f0!important;
}
@media(max-width:560px){
  .cover-gateway{padding:14px}
  .cover-shell{border-radius:24px}
  .cover-main{padding:28px 20px}
  .cover-logo{width:min(240px,72vw);max-height:240px}
  .cover-title{font-size:46px}
  .cover-subtitle{font-size:13px;margin-bottom:20px}
  .cover-player-btn{min-height:55px;font-size:15px}
  .cover-footnote{margin-top:18px;font-size:9px}
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
          <p class="cover-subtitle">Consultá tus horarios, resultados, zonas y el Drop completo del torneo.</p>
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
      </div>
    </div>
    <div id="adminLogin" class="login-card cover-login" hidden>
      <h2>Acceso administrador</h2><p>Ingresá la contraseña para abrir el panel de organización.</p>
      <form id="adminLoginForm"><label>Contraseña<input id="adminPassword" type="password" autocomplete="current-password" required placeholder="Contraseña de administrador"></label><div class="login-actions"><button class="btn primary" type="submit">Ingresar</button><button id="cancelAdminLogin" class="btn" type="button">Volver</button></div><div id="adminLoginError" class="login-error" aria-live="polite"></div></form>
    </div>
  </section>
'''

css_markers = ["/* ===== PORTADA COPAFEM ===== */","/* ===== PORTADA COPAFEM PROFESIONAL ===== */","/* ===== PORTADA COPAFEM SIMPLE ===== */"]
css_start = next((text.find(m) for m in css_markers if text.find(m) >= 0), -1)
if css_start < 0:
    raise SystemExit("No se encontró el CSS de portada")
style_close = text.index("</style>", css_start)
text = text[:css_start] + new_css + "\n\n  " + text[style_close:]

html_start = text.index('  <section id="roleGateway" class="cover-gateway">')
player_start = text.index('  <section id="playerApp" hidden>', html_start)
text = text[:html_start] + new_html + "\n" + text[player_start:]

path.write_text(text, encoding="utf-8")
print("Portada COPAFEM simple y centrada aplicada")
