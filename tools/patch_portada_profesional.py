from pathlib import Path
import re

p = Path('index.html')
text = p.read_text(encoding='utf-8')

# Elimina versiones anteriores de esta portada inyectada.
text = re.sub(r'\n?<style id="copafem-portada-profesional">.*?</style>\n?', '\n', text, flags=re.S)

css = r'''
<style id="copafem-portada-profesional">
:root{
  --home-navy:#123b72;
  --home-blue:#1f5f9f;
  --home-gold:#c99b36;
  --home-ink:#183d6b;
}
html,body{margin:0;padding:0}
.home-gateway{
  min-height:100svh;
  height:100svh;
  overflow:hidden;
  background:
    radial-gradient(circle at 8% 22%,rgba(139,188,230,.23),transparent 25%),
    radial-gradient(circle at 93% 24%,rgba(174,205,233,.20),transparent 27%),
    linear-gradient(180deg,#ffffff 0%,#f8fbff 68%,#eef5fc 100%);
  display:flex;
  align-items:center;
  justify-content:center;
  padding:18px 24px;
  position:relative;
  box-sizing:border-box;
}
.home-gateway:before{
  content:"";
  position:absolute;
  left:-80px;
  top:110px;
  width:420px;
  height:170px;
  border-radius:50%;
  background:linear-gradient(120deg,transparent,rgba(103,165,220,.17),rgba(201,155,54,.08),transparent);
  transform:rotate(-15deg);
}
.home-shell{
  width:min(1180px,96vw);
  max-height:calc(100svh - 36px);
  position:relative;
  z-index:2;
  display:flex;
  flex-direction:column;
  align-items:center;
}
.home-logo-wrap{
  height:150px;
  display:flex;
  align-items:center;
  justify-content:center;
  margin-bottom:10px;
}
.home-logo{
  display:block;
  width:150px;
  height:146px;
  object-fit:contain;
  border-radius:50%;
  background:#fff;
  filter:drop-shadow(0 8px 20px rgba(20,57,101,.10));
}
.home-card{
  width:100%;
  height:min(460px,57svh);
  min-height:390px;
  display:grid;
  grid-template-columns:54% 46%;
  overflow:hidden;
  border-radius:30px;
  border:1px solid rgba(24,61,107,.12);
  box-shadow:0 20px 50px rgba(23,59,104,.18);
  background:#123b72;
}
.home-copy{
  position:relative;
  z-index:2;
  color:#fff;
  padding:38px 42px;
  display:flex;
  flex-direction:column;
  justify-content:center;
  background:
    linear-gradient(125deg,rgba(7,40,82,.98) 0%,rgba(16,64,112,.97) 72%,rgba(22,83,137,.94) 100%);
}
.home-ball{
  width:64px;
  height:64px;
  border-radius:50%;
  display:grid;
  place-items:center;
  background:#fff;
  color:var(--home-gold);
  font-size:31px;
  margin-bottom:20px;
  box-shadow:0 8px 22px rgba(0,0,0,.14);
}
.home-copy h1{
  margin:0;
  font:500 clamp(48px,5.1vw,76px)/.95 Georgia,'Times New Roman',serif;
  letter-spacing:.01em;
}
.home-line{
  width:265px;
  max-width:72%;
  height:2px;
  margin:17px 0 17px;
  background:linear-gradient(90deg,var(--home-gold) 0 72%,transparent 72%);
  position:relative;
}
.home-line:after{
  content:'♡';
  position:absolute;
  right:18%;
  top:-12px;
  padding:0 8px;
  color:var(--home-gold);
  background:#124579;
  font-size:17px;
}
.home-copy p{
  margin:0 0 24px;
  max-width:470px;
  font-size:clamp(17px,1.55vw,21px);
  line-height:1.42;
  color:#f4f8fd;
}
.home-player-btn{
  width:min(350px,100%);
  min-height:68px;
  border:0;
  border-radius:20px;
  background:#fff;
  color:#123b72;
  font-size:23px;
  font-weight:900;
  display:flex;
  align-items:center;
  justify-content:center;
  gap:15px;
  box-shadow:0 10px 26px rgba(0,0,0,.20);
  cursor:pointer;
  transition:.18s ease;
}
.home-player-btn:hover{transform:translateY(-2px);box-shadow:0 14px 30px rgba(0,0,0,.23)}
.home-player-btn .arr{font-size:31px;color:var(--home-gold);font-weight:400}
.home-photo{
  position:relative;
  background-image:
    linear-gradient(90deg,rgba(16,64,112,.18),rgba(7,32,65,.05)),
    url('https://afpcourts.com/wp-content/uploads/Marita_Bendinat_adidas_Panoramic_AFP-scaled.jpg');
  background-size:cover;
  background-position:center 38%;
  overflow:hidden;
}
.home-photo:before{
  content:"";
  position:absolute;
  inset:0;
  box-shadow:inset 28px 0 42px rgba(9,49,92,.20);
  pointer-events:none;
}
.home-admin-row{
  width:100%;
  display:flex;
  justify-content:flex-end;
  margin-top:12px;
  padding-right:16px;
  box-sizing:border-box;
}
.home-admin-btn{
  border:0;
  background:transparent;
  color:#153f74;
  display:flex;
  align-items:center;
  gap:10px;
  font-weight:850;
  font-size:15px;
  cursor:pointer;
  padding:5px 8px;
}
.home-admin-icon{
  width:46px;
  height:46px;
  border-radius:14px;
  display:grid;
  place-items:center;
  background:#fff;
  font-size:24px;
  border:1px solid #d9e6f2;
  box-shadow:0 7px 18px rgba(25,59,98,.12);
}
.home-login{
  position:fixed!important;
  z-index:300!important;
  left:50%;
  top:50%;
  transform:translate(-50%,-50%);
  width:min(460px,calc(100vw - 28px));
  margin:0!important;
  background:#fff!important;
  box-shadow:0 24px 70px rgba(13,43,78,.32)!important;
}
@media(max-height:790px) and (min-width:821px){
  .home-gateway{padding:10px 20px}
  .home-shell{max-height:calc(100svh - 20px)}
  .home-logo-wrap{height:112px;margin-bottom:6px}
  .home-logo{width:112px;height:109px}
  .home-card{height:min(420px,61svh);min-height:340px}
  .home-copy{padding:28px 36px}
  .home-ball{width:54px;height:54px;font-size:27px;margin-bottom:14px}
  .home-copy h1{font-size:56px}
  .home-copy p{font-size:17px;margin-bottom:18px}
  .home-player-btn{min-height:60px;font-size:21px}
  .home-admin-row{margin-top:6px}
}
@media(max-width:820px){
  .home-gateway{height:auto;min-height:100svh;overflow:auto;padding:14px 12px 26px;align-items:flex-start}
  .home-shell{width:100%;max-height:none}
  .home-logo-wrap{height:124px;margin-bottom:10px}
  .home-logo{width:120px;height:116px}
  .home-card{height:auto;min-height:0;grid-template-columns:1fr;border-radius:24px}
  .home-copy{padding:26px 22px 24px}
  .home-ball{width:55px;height:55px;font-size:28px;margin-bottom:15px}
  .home-copy h1{font-size:50px}
  .home-copy p{font-size:17px;margin-bottom:20px}
  .home-player-btn{min-height:62px;font-size:21px}
  .home-photo{min-height:245px;background-position:center 34%}
  .home-admin-row{justify-content:center;padding:0;margin-top:12px}
}
@media(max-width:480px){
  .home-logo-wrap{height:110px}.home-logo{width:106px;height:103px}
  .home-copy h1{font-size:44px}.home-copy{padding:22px 18px}.home-photo{min-height:210px}
}
</style>
'''
text = text.replace('</head>', css + '\n</head>', 1)

gateway = r'''  <section id="roleGateway" class="home-gateway">
    <div class="home-shell">
      <div class="home-logo-wrap">
        <img class="home-logo" src="logo.jpg?v=20260901c" alt="COPAFEM Argentina">
      </div>

      <div class="home-card">
        <div class="home-copy">
          <div class="home-ball">◯</div>
          <h1>INGRESO</h1>
          <div class="home-line"></div>
          <p>Consultá tus partidos, horarios, resultados y el Drop completo.</p>
          <button id="choosePlayer" class="home-player-btn" type="button"><span class="arr">→</span> SOY JUGADOR</button>
        </div>
        <div class="home-photo" aria-hidden="true"></div>
      </div>

      <div class="home-admin-row">
        <button id="chooseAdmin" class="home-admin-btn" type="button"><span class="home-admin-icon">⚙</span><span>Administrador</span></button>
      </div>
    </div>

    <div id="adminLogin" class="login-card home-login" hidden>
      <h2>Acceso administrador</h2>
      <p>Ingresá la contraseña para abrir el panel de organización.</p>
      <form id="adminLoginForm">
        <label>Contraseña<input id="adminPassword" type="password" autocomplete="current-password" required placeholder="Contraseña de administrador"></label>
        <div class="login-actions"><button class="btn primary" type="submit">Ingresar</button><button id="cancelAdminLogin" class="btn" type="button">Volver</button></div>
        <div id="adminLoginError" class="login-error" aria-live="polite"></div>
      </form>
    </div>
  </section>
'''

pattern = r'\s*<section id="roleGateway"[^>]*>.*?</section>\s*(?=<section id="playerApp" hidden>)'
text, n = re.subn(pattern, '\n' + gateway + '\n', text, count=1, flags=re.S)
if n != 1:
    raise SystemExit(f'No se encontró la portada para reemplazar: {n}')

text = re.sub(r'name="copafem-app-version" content="[^"]+"', 'name="copafem-app-version" content="2.1.7"', text, count=1)
p.write_text(text, encoding='utf-8')
print('Portada COPAFEM compacta y profesional aplicada')
