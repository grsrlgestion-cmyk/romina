from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")

new_css = """/* ===== PORTADA COPAFEM ===== */
.cover-gateway{
  min-height:100vh;
  background:
    radial-gradient(circle at top right, rgba(210,226,242,.72) 0 19%, transparent 19% 100%),
    linear-gradient(180deg,#fbfdff 0%,#f4f8fd 100%);
  display:flex;
  justify-content:center;
  align-items:center;
  padding:24px;
  overflow:hidden;
  position:relative;
}
.cover-gateway::before{
  content:"";
  position:absolute;
  left:-120px;
  top:120px;
  width:540px;
  height:220px;
  background:linear-gradient(135deg,rgba(198,220,242,.65),rgba(198,220,242,0));
  transform:rotate(-16deg);
  border-radius:48px;
  pointer-events:none;
}
.cover-gateway::after{
  content:"";
  position:absolute;
  right:-120px;
  top:80px;
  width:420px;
  height:420px;
  border-radius:50%;
  border:16px solid rgba(214,226,239,.62);
  opacity:.58;
  pointer-events:none;
}
.cover-stage{
  width:min(100%,1380px);
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  gap:22px;
  position:relative;
  z-index:1;
}
.cover-brand{
  display:flex;
  flex-direction:column;
  align-items:center;
  gap:7px;
  text-align:center;
}
.cover-logo{
  width:min(300px,60vw);
  max-width:100%;
  height:auto;
  display:block;
  filter:drop-shadow(0 8px 18px rgba(23,63,117,.08));
}
.cover-brand-text{
  font-size:clamp(17px,1.8vw,24px);
  font-weight:800;
  letter-spacing:.19em;
  color:#173f75;
}
.cover-card{
  width:min(100%,1320px);
  min-height:520px;
  border-radius:34px;
  background:#fff;
  box-shadow:0 22px 58px rgba(23,63,117,.14);
  border:1px solid #dce8f3;
  display:grid;
  grid-template-columns:minmax(390px,535px) 1fr;
  overflow:hidden;
  position:relative;
}
.cover-copy{
  background:linear-gradient(180deg,#0a3569 0%,#0e477f 100%);
  color:#fff;
  padding:46px 52px;
  display:flex;
  flex-direction:column;
  justify-content:center;
  position:relative;
  z-index:2;
}
.cover-ball{
  width:82px;
  height:82px;
  border-radius:50%;
  background:#fff;
  display:grid;
  place-items:center;
  margin-bottom:24px;
  box-shadow:0 8px 18px rgba(3,24,48,.12),inset 0 0 0 1px rgba(212,167,56,.2);
}
.cover-ball::before{
  content:"◔";
  color:#d4a738;
  font-size:38px;
  line-height:1;
  transform:rotate(-14deg);
}
.cover-copy h1{
  margin:0;
  font-family:Georgia,"Times New Roman",serif;
  font-size:clamp(68px,6.4vw,102px);
  line-height:.96;
  letter-spacing:.01em;
  text-shadow:0 2px 2px rgba(0,0,0,.04);
}
.cover-sep{
  display:flex;
  align-items:center;
  gap:16px;
  margin:26px 0 22px;
}
.cover-sep::before,.cover-sep::after{
  content:"";
  flex:1;
  height:3px;
  background:#d4a738;
  border-radius:999px;
}
.cover-sep span{
  color:#d4a738;
  font-size:28px;
  line-height:1;
}
.cover-copy p{
  margin:0 0 30px;
  font-size:clamp(20px,1.75vw,26px);
  line-height:1.42;
  max-width:420px;
}
.cover-primary{
  align-self:flex-start;
  border:0;
  background:#fff;
  color:#173f75;
  border-radius:22px;
  padding:20px 34px;
  font-size:clamp(23px,2.1vw,30px);
  font-weight:900;
  display:inline-flex;
  align-items:center;
  gap:14px;
  box-shadow:0 10px 24px rgba(7,28,58,.2);
  cursor:pointer;
  transition:.18s ease;
}
.cover-primary:hover{transform:translateY(-2px);box-shadow:0 14px 30px rgba(7,28,58,.24)}
.cover-primary::before{
  content:"→";
  color:#d4a738;
  font-size:1.35em;
  line-height:1;
}
.cover-visual{
  position:relative;
  min-height:520px;
  background-image:
    linear-gradient(90deg,rgba(9,53,101,.7) 0%,rgba(9,53,101,.24) 26%,rgba(9,53,101,.06) 48%,rgba(9,53,101,0) 70%),
    url('portada-copafem.webp');
  background-size:auto 100%;
  background-repeat:no-repeat;
  background-position:86% center;
  background-color:#0b3d70;
  filter:saturate(1.04) contrast(1.02);
}
.cover-visual::after{
  content:"";
  position:absolute;
  inset:0;
  background:linear-gradient(180deg,rgba(255,255,255,.02),rgba(0,20,44,.08));
  pointer-events:none;
}
.cover-admin{
  position:absolute;
  right:24px;
  bottom:24px;
  width:132px;
  min-height:142px;
  border:0;
  border-radius:22px;
  background:rgba(255,255,255,.96);
  color:#173f75;
  box-shadow:0 14px 34px rgba(23,63,117,.18);
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  gap:7px;
  font-weight:900;
  cursor:pointer;
  z-index:3;
  backdrop-filter:blur(8px);
  transition:.18s ease;
}
.cover-admin:hover{transform:translateY(-2px)}
.cover-admin .gear{font-size:40px;line-height:1}
.cover-admin span{display:block}
.cover-admin .cover-admin-txt{font-size:16px;letter-spacing:.02em}
.cover-login{
  position:fixed!important;
  z-index:100!important;
  left:50%;
  top:50%;
  transform:translate(-50%,-50%);
  width:min(460px,calc(100vw - 28px));
  margin:0!important;
  box-shadow:0 22px 70px rgba(13,43,78,.28)!important;
}
@media(max-width:1050px){
  .cover-gateway{align-items:flex-start;padding-top:18px;overflow:auto}
  .cover-card{grid-template-columns:1fr;max-width:780px;min-height:auto}
  .cover-copy{padding:36px 30px 30px}
  .cover-copy p{max-width:none}
  .cover-visual{min-height:360px;background-size:cover;background-position:center center}
  .cover-admin{right:20px;bottom:20px;width:122px;min-height:130px}
}
@media(max-width:700px){
  .cover-gateway{padding:12px 10px 20px;min-height:auto}
  .cover-stage{gap:16px}
  .cover-logo{width:min(235px,66vw)}
  .cover-brand-text{font-size:14px;letter-spacing:.15em}
  .cover-card{border-radius:24px}
  .cover-copy{padding:26px 20px 24px}
  .cover-ball{width:62px;height:62px;margin-bottom:18px}
  .cover-ball::before{font-size:30px}
  .cover-copy h1{font-size:62px}
  .cover-sep{margin:18px 0}
  .cover-copy p{font-size:18px;margin-bottom:22px}
  .cover-primary{width:100%;justify-content:center;padding:17px 18px;font-size:20px;border-radius:17px}
  .cover-visual{min-height:245px;background-size:cover;background-position:72% center}
  .cover-admin{position:static;width:calc(100% - 24px);min-height:auto;padding:14px 12px;border-radius:17px;flex-direction:row;gap:10px;margin:12px;justify-content:center}
  .cover-admin .gear{font-size:28px}
  .cover-admin .cover-admin-txt{font-size:15px}
}
"""

new_html = """  <section id=\"roleGateway\" class=\"cover-gateway\">
    <div class=\"cover-stage\">
      <div class=\"cover-brand\">
        <img class=\"cover-logo\" src=\"logo-copafem-aprobado.svg?v=20260908\" alt=\"COPAFEM\">
        <div class=\"cover-brand-text\">TORNEOS • ARGENTINA</div>
      </div>
      <div class=\"cover-card\">
        <div class=\"cover-copy\">
          <div class=\"cover-ball\" aria-hidden=\"true\"></div>
          <h1>INGRESO</h1>
          <div class=\"cover-sep\" aria-hidden=\"true\"><span>♡</span></div>
          <p>Consultá tus partidos, horarios, resultados y el Drop completo.</p>
          <button id=\"choosePlayer\" class=\"cover-primary\" type=\"button\" aria-label=\"Soy jugador\">SOY JUGADOR</button>
        </div>
        <div class=\"cover-visual\" aria-hidden=\"true\"></div>
        <button id=\"chooseAdmin\" class=\"cover-admin\" type=\"button\" aria-label=\"Administrador\">
          <span class=\"gear\">⚙</span>
          <span class=\"cover-admin-txt\">ACCESO<br>ADMIN</span>
        </button>
      </div>
    </div>
    <div id=\"adminLogin\" class=\"login-card cover-login\" hidden>
      <h2>Acceso administrador</h2><p>Ingresá la contraseña para abrir el panel de organización.</p>
      <form id=\"adminLoginForm\"><label>Contraseña<input id=\"adminPassword\" type=\"password\" autocomplete=\"current-password\" required placeholder=\"Contraseña de administrador\"></label><div class=\"login-actions\"><button class=\"btn primary\" type=\"submit\">Ingresar</button><button id=\"cancelAdminLogin\" class=\"btn\" type=\"button\">Volver</button></div><div id=\"adminLoginError\" class=\"login-error\" aria-live=\"polite\"></div></form>
    </div>
  </section>
"""

css_start = text.index("/* ===== PORTADA COPAFEM ===== */")
style_close = text.index("</style>", css_start)
text = text[:css_start] + new_css + "\n\n  " + text[style_close:]

html_start = text.index('  <section id="roleGateway" class="cover-gateway">')
player_start = text.index('  <section id="playerApp" hidden>', html_start)
text = text[:html_start] + new_html + "\n" + text[player_start:]

path.write_text(text, encoding="utf-8")
print("Portada COPAFEM completa aplicada")
