from pathlib import Path
import re

p = Path('index.html')
text = p.read_text(encoding='utf-8')

# Quitar una versión anterior de este bloque si existe.
text = re.sub(r'\n?<style id="copafem-portada-profesional">.*?</style>\n?', '\n', text, flags=re.S)

css = r'''
<style id="copafem-portada-profesional">
:root{
  --cp-navy:#0f376b;
  --cp-blue:#1e5a98;
  --cp-light:#eaf4ff;
  --cp-gold:#c99a30;
  --cp-ink:#17365f;
}
.pro-cover{
  min-height:100vh;
  background:linear-gradient(180deg,#fff 0%,#f8fbff 65%,#eef5fc 100%);
  color:var(--cp-ink);
  overflow:hidden;
  position:relative;
  padding:26px 26px 30px;
  display:flex;
  align-items:center;
  justify-content:center;
}
.pro-cover:before,.pro-cover:after{
  content:"";position:absolute;pointer-events:none;opacity:.5;filter:blur(.2px)
}
.pro-cover:before{
  width:520px;height:230px;left:-170px;top:90px;transform:rotate(-18deg);
  background:linear-gradient(120deg,transparent 5%,rgba(125,179,231,.18) 18%,rgba(85,157,221,.38) 48%,rgba(201,154,48,.14) 62%,transparent 83%);
  border-radius:55% 30% 60% 35%;
}
.pro-cover:after{
  width:420px;height:420px;right:-110px;top:55px;border-radius:50%;
  border:10px solid rgba(79,139,199,.08);box-shadow:inset 0 0 0 2px rgba(79,139,199,.09);
}
.pro-wrap{width:min(1180px,100%);position:relative;z-index:2;margin:auto}
.pro-brand{display:flex;justify-content:center;align-items:center;margin:0 auto 22px}
.pro-logo{
  width:250px;height:145px;display:flex;align-items:center;justify-content:center;position:relative;
}
.pro-logo-ring{
  width:138px;height:138px;border-radius:50%;border:2px solid #234d82;position:absolute;left:0;top:2px;
  box-shadow:inset 0 0 0 6px #fff, inset 0 0 0 8px rgba(115,168,220,.45);
  background:#fff;
}
.pro-logo-racket{position:absolute;left:41px;top:27px;width:55px;height:85px}
.pro-logo-racket:before{
  content:"";position:absolute;width:48px;height:58px;border:4px solid #173f78;border-radius:48% 48% 42% 42%;left:0;top:0;
  background:radial-gradient(circle,#173f78 1.4px,transparent 1.8px) 0 0/9px 9px,#f7fbff;
}
.pro-logo-racket:after{
  content:"";position:absolute;width:8px;height:28px;background:#173f78;left:23px;top:57px;border-radius:0 0 4px 4px;
}
.pro-logo-text{position:absolute;left:116px;top:28px;font-family:Georgia,serif;font-size:39px;letter-spacing:3px;color:#123b73;line-height:.92;white-space:nowrap}
.pro-logo-text b{display:block;margin-left:38px;font-weight:500;letter-spacing:5px}
.pro-brand-sub{position:absolute;left:119px;top:108px;font-size:13px;letter-spacing:3px;font-weight:800;white-space:nowrap;color:#173e73}
.pro-card{
  border-radius:34px;overflow:hidden;min-height:430px;display:grid;grid-template-columns:1.08fr .92fr;
  box-shadow:0 20px 55px rgba(21,61,107,.18);border:1px solid rgba(27,70,116,.12);
  background:#0e376d;
}
.pro-card-copy{
  padding:42px 44px 38px;color:white;position:relative;display:flex;flex-direction:column;justify-content:center;
  background:linear-gradient(130deg,#082e5f 0%,#12477d 67%,#1b5a91 100%);
}
.pro-ball{
  width:72px;height:72px;border-radius:50%;background:#fff;display:grid;place-items:center;margin-bottom:22px;
  color:var(--cp-gold);box-shadow:0 8px 24px rgba(0,0,0,.14);font-size:38px;
}
.pro-title{font:500 clamp(52px,6vw,82px)/.95 Georgia,'Times New Roman',serif;letter-spacing:1px;margin:0}
.pro-gold-line{height:2px;width:285px;max-width:75%;background:linear-gradient(90deg,var(--cp-gold),var(--cp-gold) 72%,transparent);margin:20px 0 18px;position:relative}
.pro-gold-line:after{content:'♡';position:absolute;right:15%;top:-12px;background:#12477d;color:var(--cp-gold);padding:0 10px;font-size:18px}
.pro-copy{font-size:21px;line-height:1.45;margin:0 0 26px;max-width:460px;color:#f3f8ff}
.pro-player-btn{
  width:min(365px,100%);min-height:76px;border:0;border-radius:22px;background:#fff;color:#113a70;font-size:25px;font-weight:900;
  display:flex;align-items:center;justify-content:center;gap:18px;cursor:pointer;box-shadow:0 10px 28px rgba(1,20,48,.24);transition:.18s ease;
}
.pro-player-btn:hover{transform:translateY(-2px);box-shadow:0 14px 32px rgba(1,20,48,.28)}
.pro-player-btn .arr{color:var(--cp-gold);font-size:34px;font-weight:400}
.pro-visual{
  position:relative;overflow:hidden;background:linear-gradient(145deg,#5b9ad0 0%,#23679f 48%,#0b3c72 100%);
}
.pro-visual:before{
  content:"";position:absolute;inset:0;background:
  linear-gradient(90deg,transparent 49%,rgba(255,255,255,.16) 50%,transparent 51%),
  linear-gradient(0deg,transparent 48%,rgba(255,255,255,.1) 49%,transparent 50%);
  background-size:145px 100%,100% 105px;opacity:.8;
}
.pro-visual:after{
  content:"";position:absolute;left:12%;right:8%;bottom:13%;height:28%;border:3px solid rgba(255,255,255,.5);transform:perspective(420px) rotateX(55deg);transform-origin:bottom;
}
.pro-racket{
  position:absolute;width:180px;height:235px;right:14%;top:22%;transform:rotate(18deg);filter:drop-shadow(0 15px 20px rgba(0,0,0,.28));
}
.pro-racket-head{
  position:absolute;width:145px;height:180px;border-radius:46% 46% 43% 43%;background:#122f52;border:8px solid #d6e4f0;right:0;top:0;
  box-shadow:inset 0 0 0 4px #091f3a;
}
.pro-racket-head:after{content:"";position:absolute;inset:20px;border-radius:42%;background:radial-gradient(circle,#d9e4ee 3px,transparent 4px) 0 0/19px 19px;opacity:.7}
.pro-racket-handle{position:absolute;width:27px;height:90px;background:linear-gradient(90deg,#dedede,#5d6d7c,#eee);left:45px;top:163px;border-radius:8px;transform:rotate(10deg)}
.pro-player-silhouette{
  position:absolute;left:17%;bottom:-10px;width:150px;height:330px;opacity:.75;transform:rotate(-5deg);
}
.pro-player-silhouette:before{content:"";position:absolute;width:78px;height:78px;border-radius:50%;background:#d5e4ef;left:35px;top:0}
.pro-player-silhouette:after{content:"";position:absolute;width:135px;height:250px;border-radius:60px 60px 20px 20px;background:linear-gradient(180deg,#e7f0f6,#b7d1e2);left:5px;top:68px;clip-path:polygon(22% 0,78% 0,100% 100%,0 100%)}
.pro-admin-row{display:flex;justify-content:flex-end;margin-top:-66px;position:relative;z-index:5;padding-right:26px}
.pro-admin-btn{
  border:0;background:transparent;color:#123b72;font-weight:900;font-size:17px;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:7px;
}
.pro-admin-icon{width:78px;height:78px;border-radius:21px;background:#fff;display:grid;place-items:center;font-size:39px;box-shadow:0 12px 28px rgba(24,59,98,.16);border:1px solid #dce8f3}
.pro-admin-deco{width:84px;height:2px;background:linear-gradient(90deg,var(--cp-gold) 0 38%,transparent 38% 62%,var(--cp-gold) 62%);position:relative}
.pro-admin-deco:after{content:'♡';position:absolute;left:35px;top:-11px;color:var(--cp-gold);font-size:13px}
.pro-features{
  margin-top:36px;background:rgba(255,255,255,.88);border:1px solid #e0eaf4;border-radius:18px;padding:18px 22px;
  display:grid;grid-template-columns:repeat(4,1fr);gap:0;box-shadow:0 8px 25px rgba(22,59,98,.08)
}
.pro-feature{display:flex;align-items:center;gap:12px;padding:4px 18px;border-left:1px solid #dfe8f1}
.pro-feature:first-child{border-left:0}.pro-fi{font-size:28px}.pro-feature strong{font-size:14px;color:#113a70;display:block}.pro-feature small{font-size:11px;color:#5c718a;display:block;margin-top:2px}
.pro-login{position:fixed!important;z-index:200!important;left:50%;top:50%;transform:translate(-50%,-50%);width:min(460px,calc(100vw - 28px));margin:0!important;box-shadow:0 24px 70px rgba(13,43,78,.32)!important;background:#fff!important}
@media(max-width:820px){
  .pro-cover{padding:16px 12px 26px;align-items:flex-start}.pro-wrap{width:100%}.pro-brand{margin-bottom:12px}.pro-logo{transform:scale(.82);transform-origin:center;width:230px;height:122px}.pro-card{grid-template-columns:1fr;min-height:0;border-radius:26px}.pro-card-copy{padding:28px 24px 26px}.pro-title{font-size:52px}.pro-copy{font-size:17px;margin-bottom:20px}.pro-player-btn{font-size:21px;min-height:64px}.pro-visual{min-height:260px}.pro-racket{transform:scale(.75) rotate(18deg);right:7%;top:10%}.pro-player-silhouette{transform:scale(.8);transform-origin:bottom left}.pro-admin-row{margin-top:18px;justify-content:center;padding:0}.pro-admin-icon{width:65px;height:65px;font-size:32px}.pro-features{grid-template-columns:1fr 1fr;margin-top:20px;padding:10px}.pro-feature{border-left:0;border-top:1px solid #e4ecf4;padding:12px}.pro-feature:nth-child(-n+2){border-top:0}}
@media(max-width:480px){.pro-visual{min-height:210px}.pro-features{grid-template-columns:1fr}.pro-feature{border-top:1px solid #e4ecf4!important}.pro-feature:first-child{border-top:0!important}.pro-ball{width:58px;height:58px;font-size:30px}.pro-card-copy{padding:24px 20px}.pro-title{font-size:46px}}
</style>
'''
text = text.replace('</head>', css + '\n</head>', 1)

gateway = r'''  <section id="roleGateway" class="pro-cover">
    <div class="pro-wrap">
      <div class="pro-brand" aria-label="COPAFEM Torneos Argentina">
        <div class="pro-logo">
          <div class="pro-logo-ring"></div>
          <div class="pro-logo-racket"></div>
          <div class="pro-logo-text">COPA<b>FEM</b></div>
          <div class="pro-brand-sub">TORNEOS · ARGENTINA</div>
        </div>
      </div>

      <div class="pro-card">
        <div class="pro-card-copy">
          <div class="pro-ball">◯</div>
          <h1 class="pro-title">INGRESO</h1>
          <div class="pro-gold-line"></div>
          <p class="pro-copy">Consultá tus partidos, horarios, resultados y el Drop completo.</p>
          <button id="choosePlayer" class="pro-player-btn" type="button"><span class="arr">→</span> SOY JUGADOR</button>
        </div>
        <div class="pro-visual" aria-hidden="true">
          <div class="pro-player-silhouette"></div>
          <div class="pro-racket"><div class="pro-racket-head"></div><div class="pro-racket-handle"></div></div>
        </div>
      </div>

      <div class="pro-admin-row">
        <button id="chooseAdmin" class="pro-admin-btn" type="button">
          <span class="pro-admin-icon">⚙</span><span class="pro-admin-deco"></span><span>Administrador</span>
        </button>
      </div>

      <div class="pro-features">
        <div class="pro-feature"><span class="pro-fi">▣</span><div><strong>TUS PARTIDOS</strong><small>Seguí todos tus encuentros</small></div></div>
        <div class="pro-feature"><span class="pro-fi">◷</span><div><strong>TUS HORARIOS</strong><small>Día, hora y cancha</small></div></div>
        <div class="pro-feature"><span class="pro-fi">♕</span><div><strong>RESULTADOS</strong><small>Actualizados al instante</small></div></div>
        <div class="pro-feature"><span class="pro-fi">⇩</span><div><strong>DROP COMPLETO</strong><small>Consultá el fixture</small></div></div>
      </div>
    </div>

    <div id="adminLogin" class="login-card pro-login" hidden>
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

text = re.sub(r'name="copafem-app-version" content="[^"]+"', 'name="copafem-app-version" content="2.1.6"', text, count=1)
p.write_text(text, encoding='utf-8')
print('Portada profesional COPAFEM aplicada sin imágenes externas')
