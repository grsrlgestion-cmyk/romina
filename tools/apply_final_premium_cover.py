from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

start = '/* COPAFEM PREMIUM FINAL */'
end = '/* END COPAFEM PREMIUM FINAL */'
s = re.sub(re.escape(start) + r'.*?' + re.escape(end), '', s, flags=re.S)

css = r'''
/* COPAFEM PREMIUM FINAL */
.premium-gateway{
  position:relative;
  min-height:100vh;
  overflow:hidden;
  display:flex;
  align-items:center;
  justify-content:center;
  padding:28px 18px 42px;
  background:
    radial-gradient(circle at 50% 15%,rgba(255,255,255,.98) 0 24%,rgba(255,252,246,.96) 46%,rgba(246,240,224,.94) 72%,rgba(225,210,171,.82) 100%),
    linear-gradient(135deg,#fffdf8 0%,#f6ead0 44%,#d5b56a 72%,#173e72 100%);
  color:#163d70;
}
.premium-gateway[hidden]{display:none!important}
.premium-gateway::before{
  content:"";position:absolute;inset:auto -8% -155px -8%;height:310px;
  background:linear-gradient(145deg,#7ca9d9 0 18%,#426d9e 18% 34%,#173f75 34% 73%,#092c58 73% 100%);
  border-top:2px solid rgba(214,166,69,.95);transform:rotate(-2deg);transform-origin:center;z-index:0;
}
.premium-gateway::after{
  content:"";position:absolute;width:520px;height:520px;right:-245px;top:-245px;border-radius:50%;
  border:1px solid rgba(194,145,49,.36);box-shadow:0 0 0 34px rgba(255,255,255,.2),0 0 0 70px rgba(194,145,49,.08);z-index:0;
}
.premium-shell{
  position:relative;z-index:1;width:min(930px,96vw);min-height:min(900px,94vh);
  border:1.5px solid rgba(197,148,52,.72);border-radius:34px;
  background:linear-gradient(160deg,rgba(255,255,255,.97),rgba(255,253,248,.94) 62%,rgba(247,239,219,.93));
  box-shadow:0 28px 80px rgba(13,43,78,.20),inset 0 1px 0 #fff;
  padding:42px 54px 62px;text-align:center;display:flex;flex-direction:column;align-items:center;
}
.premium-dots{position:absolute;width:220px;height:220px;left:-25px;top:-18px;opacity:.24;background-image:radial-gradient(#c79536 1.2px,transparent 1.2px);background-size:10px 10px;mask-image:linear-gradient(135deg,#000,transparent 74%)}
.premium-logo-wrap{width:min(330px,54vw);aspect-ratio:1;border-radius:50%;padding:7px;background:linear-gradient(145deg,#f4d58a,#b9862d,#f9e4aa);box-shadow:0 14px 30px rgba(83,61,23,.16);margin:0 auto 26px}
.premium-logo{width:100%;height:100%;display:block;border-radius:50%;background:#fff}
.premium-title{font-family:Georgia,'Times New Roman',serif;font-size:clamp(36px,5.5vw,62px);font-weight:700;letter-spacing:.025em;line-height:1.05;margin:0;color:#123b70;text-shadow:0 1px 0 #fff}
.premium-divider{width:min(620px,82%);height:28px;display:flex;align-items:center;gap:14px;margin:7px 0 6px;color:#c59434;font-size:25px}
.premium-divider::before,.premium-divider::after{content:"";height:1.5px;flex:1;background:linear-gradient(90deg,transparent,#c59434)}
.premium-divider::after{background:linear-gradient(90deg,#c59434,transparent)}
.premium-subtitle{max-width:690px;margin:0 auto 31px;color:#56708c;font-size:clamp(18px,2.3vw,25px);line-height:1.45;font-weight:450}
.premium-player-btn{width:min(720px,92%);min-height:92px;border:2px solid #d7aa51;border-radius:23px;background:linear-gradient(105deg,#082d59 0%,#123f75 48%,#245b91 100%);box-shadow:0 15px 30px rgba(13,43,78,.20),inset 0 1px 0 rgba(255,255,255,.18);color:#fff;font-size:clamp(24px,3.4vw,37px);font-weight:900;letter-spacing:.02em;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:20px;transition:.2s ease}
.premium-player-btn:hover{transform:translateY(-2px);box-shadow:0 19px 36px rgba(13,43,78,.25)}
.premium-player-btn .arrow{position:absolute;margin-left:min(570px,70%);color:#e4bd65;font-size:49px;font-weight:300;line-height:1}
.premium-admin-btn{margin-top:24px;border:0;background:transparent;color:#496b91;font-size:clamp(18px,2.2vw,24px);font-weight:850;letter-spacing:.02em;cursor:pointer;padding:12px 24px;display:flex;align-items:center;gap:12px}
.premium-admin-btn .gear{width:35px;height:35px;border-radius:50%;display:grid;place-items:center;color:#1b4d83;font-size:26px}
.premium-admin-line{display:flex;align-items:center;width:min(480px,76%);gap:14px;justify-content:center}
.premium-admin-line::before,.premium-admin-line::after{content:"";height:1.5px;flex:1;background:linear-gradient(90deg,transparent,#d0a14c)}
.premium-admin-line::after{background:linear-gradient(90deg,#d0a14c,transparent)}
.premium-gateway .login-card{position:absolute;z-index:20;left:50%;top:50%;transform:translate(-50%,-50%);width:min(470px,calc(100vw - 34px));background:#fff;border:1px solid #d7b46a;border-radius:24px;box-shadow:0 28px 80px rgba(9,34,67,.30);padding:28px;text-align:left}
.premium-gateway .login-card h2{margin:0 0 7px;color:#173f75}.premium-gateway .login-card p{margin:0 0 18px;color:#68788c}
.premium-gateway .login-card label{font-weight:800;font-size:13px;color:#40546d}.premium-gateway .login-card input{width:100%;margin-top:7px;border:1px solid #d8dee8;border-radius:12px;padding:12px}.premium-gateway .login-actions{display:flex;gap:9px;margin-top:16px}.premium-gateway .login-error{margin-top:12px;color:#a8342a;font-size:13px}
@media(max-width:700px){
  .premium-gateway{padding:12px 8px 34px;align-items:flex-start}.premium-shell{width:100%;min-height:calc(100vh - 24px);padding:28px 16px 50px;border-radius:25px}.premium-logo-wrap{width:min(260px,64vw);margin-bottom:22px}.premium-title{font-size:clamp(31px,9vw,43px)}.premium-subtitle{font-size:18px;margin-bottom:26px}.premium-player-btn{width:100%;min-height:72px;border-radius:18px;font-size:25px}.premium-player-btn .arrow{position:static;margin:0;font-size:38px}.premium-admin-btn{font-size:18px;margin-top:18px}.premium-gateway::before{height:200px;bottom:-125px}.premium-dots{width:145px;height:145px}
}
/* END COPAFEM PREMIUM FINAL */
'''
s = s.replace('</style>', css + '\n</style>', 1)

logo_svg = '''
<svg class="premium-logo" viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="COPAFEM Argentina">
  <defs><linearGradient id="brush" x1="0" x2="1"><stop stop-color="#dbe9f7"/><stop offset=".52" stop-color="#9ebddd"/><stop offset="1" stop-color="#f0d69b"/></linearGradient></defs>
  <circle cx="250" cy="250" r="244" fill="#fff" stroke="#1b4679" stroke-width="2"/>
  <path d="M72 312 C145 268 202 297 269 274 C333 252 367 263 430 233" fill="none" stroke="url(#brush)" stroke-width="24" opacity=".72"/>
  <text x="67" y="190" font-family="Arial,Helvetica,sans-serif" font-size="88" font-weight="300" fill="#173f75">C</text>
  <text x="287" y="190" font-family="Arial,Helvetica,sans-serif" font-size="88" font-weight="300" fill="#173f75">PA</text>
  <text x="242" y="285" font-family="Arial,Helvetica,sans-serif" font-size="82" font-weight="300" fill="#617da1">FEM</text>
  <g transform="translate(142,71)">
    <ellipse cx="85" cy="77" rx="63" ry="75" fill="url(#brush)" stroke="#173f75" stroke-width="6"/>
    <path d="M48 128 L82 174 L118 128" fill="#173f75" stroke="#173f75" stroke-width="5"/>
    <rect x="72" y="167" width="27" height="82" rx="7" fill="#efe6d3" stroke="#173f75" stroke-width="4"/>
    <g fill="#173f75">''' + ''.join(f'<circle cx="{x}" cy="{y}" r="4.4"/>' for y in [40,57,74,91,108] for x in [57,75,93,111]) + '''</g>
  </g>
  <circle cx="423" cy="177" r="17" fill="#8aa8c8" stroke="#315c8d" stroke-width="2"/><path d="M410 169 Q423 161 436 171" fill="none" stroke="#fff" stroke-width="2" opacity=".8"/>
  <line x1="145" x2="218" y1="333" y2="333" stroke="#c99735" stroke-width="2"/><text x="250" y="342" text-anchor="middle" font-family="Arial" font-size="22" fill="#c99735">♡</text><line x1="282" x2="355" y1="333" y2="333" stroke="#c99735" stroke-width="2"/>
  <text x="250" y="365" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="15" fill="#173f75" letter-spacing="3">NO PUEDO,</text><text x="318" y="365" font-family="Georgia,serif" font-size="21" font-style="italic" fill="#6382a6">tengo pádel</text>
  <g transform="translate(250 403)"><circle r="15" fill="#d5a33e"/><g stroke="#d5a33e" stroke-width="2">''' + ''.join(f'<line x1="0" y1="-22" x2="0" y2="-31" transform="rotate({a})"/>' for a in range(0,360,20)) + '''</g></g>
  <path d="M185 401 H230 M270 401 H315" stroke="#adc6df" stroke-width="7" opacity=".8"/>
  <text x="250" y="455" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="17" fill="#173f75" letter-spacing="7">ARGENTINA</text>
</svg>'''

gateway = f'''
<section id="roleGateway" class="premium-gateway">
  <div class="premium-shell">
    <div class="premium-dots" aria-hidden="true"></div>
    <div class="premium-logo-wrap">{logo_svg}</div>
    <h1 class="premium-title">COPAFEM AMERICANOS</h1>
    <div class="premium-divider" aria-hidden="true">♡</div>
    <p class="premium-subtitle">Ingresá a tu torneo y consultá tus partidos,<br>horarios, resultados y el Drop completo.</p>
    <button id="choosePlayer" class="premium-player-btn" type="button"><span>SOY JUGADOR</span><span class="arrow">›</span></button>
    <div class="premium-admin-line"><button id="chooseAdmin" class="premium-admin-btn" type="button"><span class="gear">⚙</span><span>ADMINISTRADOR</span></button></div>
    <div id="adminLogin" class="login-card" hidden>
      <h2>Acceso administrador</h2><p>Ingresá la contraseña para abrir el panel de organización.</p>
      <form id="adminLoginForm"><label>Contraseña<input id="adminPassword" type="password" autocomplete="current-password" required placeholder="Contraseña de administrador"></label><div class="login-actions"><button class="btn primary" type="submit">Ingresar</button><button id="cancelAdminLogin" class="btn" type="button">Volver</button></div><div id="adminLoginError" class="login-error" aria-live="polite"></div></form>
    </div>
  </div>
</section>
'''

pattern = r'<section id="roleGateway"[^>]*>.*?</section>\s*(?=<section id="playerApp")'
s, n = re.subn(pattern, gateway + '\n', s, count=1, flags=re.S)
if n != 1:
    raise SystemExit('No se pudo localizar roleGateway')

p.write_text(s, encoding='utf-8')
print('Portada premium final aplicada')
