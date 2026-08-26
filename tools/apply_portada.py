from pathlib import Path
import re

p = Path('index.html')
text = p.read_text(encoding='utf-8')

logo_match = re.search(r'<img class="role-logo" src="([^"]+)"', text)
if not logo_match:
    logo_match = re.search(r'<div class="player-brand"><img src="([^"]+)"', text)
logo_src = logo_match.group(1) if logo_match else 'logo.jpg'

start_marker = '/* ===== PORTADA COPAFEM NUEVA ===== */'
end_marker = '/* ===== FIN PORTADA COPAFEM NUEVA ===== */'
text = re.sub(re.escape(start_marker) + r'.*?' + re.escape(end_marker), '', text, flags=re.S)

css = r'''
/* ===== PORTADA COPAFEM NUEVA ===== */
#roleGateway.role-shell{
  min-height:100vh;padding:24px 34px 38px;
  background:radial-gradient(circle at 50% -10%,#fff 0 42%,#f7f9fc 70%,#edf4fb 100%);
  position:relative;overflow:hidden;display:flex;align-items:flex-start;justify-content:center
}
#roleGateway.role-shell:before{
  content:"";position:absolute;left:-8%;top:9%;width:42%;height:45%;
  background:linear-gradient(135deg,rgba(116,174,227,.38),rgba(116,174,227,.03));
  filter:blur(1px);transform:rotate(-13deg);border-radius:45% 55% 50% 30%;opacity:.9
}
#roleGateway.role-shell:after{
  content:"";position:absolute;right:-7%;top:5%;width:32vw;height:32vw;max-width:520px;max-height:520px;
  border:8px solid rgba(115,151,197,.12);border-radius:50%;
  background:radial-gradient(circle at 50% 50%,rgba(58,96,144,.12) 0 4px,transparent 5px) 0 0/38px 38px;
  opacity:.62;transform:rotate(-10deg)
}
#roleGateway .role-wrap{width:min(1500px,100%);max-width:none;margin:0 auto;position:relative;z-index:2}
.copa-entry-logo{display:flex;justify-content:center;margin:0 auto 18px;position:relative;z-index:2}
.copa-entry-logo img{width:min(330px,34vw);height:auto;max-height:270px;object-fit:contain;filter:drop-shadow(0 8px 22px rgba(31,65,111,.08))}
.copa-entry-layout{display:grid;grid-template-columns:minmax(0,1fr) 170px;gap:34px;align-items:end;max-width:1240px;margin:0 auto}
.copa-entry-card{min-height:470px;border-radius:38px;overflow:hidden;display:grid;grid-template-columns:46% 54%;background:#123d72;box-shadow:0 22px 55px rgba(19,55,94,.20);border:1px solid rgba(22,63,111,.16)}
.copa-entry-copy{position:relative;padding:38px 44px;display:flex;flex-direction:column;justify-content:center;background:radial-gradient(circle at 90% 55%,rgba(43,104,164,.25),transparent 47%),linear-gradient(135deg,#113765,#0e427c 64%,#154f8d);color:#fff;overflow:hidden}
.copa-entry-copy:after{content:"";position:absolute;right:-80px;top:-60px;width:310px;height:680px;background:linear-gradient(105deg,transparent 10%,rgba(72,137,196,.32),transparent 70%);transform:rotate(9deg)}
.copa-ball-icon{width:80px;height:80px;border-radius:50%;display:grid;place-items:center;background:#fff;color:#c9922b;font-size:44px;line-height:1;box-shadow:0 8px 24px rgba(0,0,0,.12);margin-bottom:24px;position:relative;z-index:2}
.copa-ball-icon:before{content:"◔";transform:rotate(-35deg)}
.copa-entry-copy h1{font-family:Georgia,'Times New Roman',serif;font-size:clamp(52px,5.2vw,84px);font-weight:500;letter-spacing:.025em;margin:0;line-height:.95;position:relative;z-index:2;text-shadow:0 2px 4px rgba(0,0,0,.12)}
.copa-gold-line{display:flex;align-items:center;gap:9px;margin:16px 0 17px;position:relative;z-index:2}
.copa-gold-line span{display:block;width:145px;height:2px;background:#d29b31}
.copa-gold-line b{font-size:18px;color:#d29b31;font-weight:400}
.copa-entry-copy p{font-size:clamp(18px,1.7vw,24px);line-height:1.4;max-width:470px;margin:0 0 24px;color:#f4f8ff;position:relative;z-index:2}
#choosePlayer.copa-player-btn{width:min(360px,100%);min-height:82px;border:1px solid #d7e1ec;border-radius:24px;background:#fff;color:#143f78;display:flex;align-items:center;justify-content:center;gap:18px;font-size:clamp(21px,1.8vw,29px);font-weight:950;cursor:pointer;box-shadow:0 11px 25px rgba(3,23,49,.16);position:relative;z-index:3;transition:.18s ease}
#choosePlayer.copa-player-btn:hover{transform:translateY(-2px);box-shadow:0 15px 30px rgba(3,23,49,.22)}
#choosePlayer .copa-arrow{font-size:42px;line-height:1;color:#c9922b;font-weight:400}
.copa-entry-photo{min-height:470px;background:linear-gradient(90deg,rgba(9,50,94,.38),rgba(10,48,89,.03) 32%,rgba(7,34,69,.08)),url('https://contents.mediadecathlon.com/m22633185/k%243bb1f8882a594de6c33c81124cfe23b1/padel-racket-one-ultralight-white-head-f16a4840-c2bb-428d-872c-f252135e65c3.jpg?f=1920x0&format=auto') center 42%/cover no-repeat;position:relative}
.copa-entry-photo:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(12,55,99,.32),transparent 28%)}
#chooseAdmin.copa-admin-btn{border:0;background:transparent;color:#143f78;display:flex;flex-direction:column;align-items:center;gap:7px;cursor:pointer;padding:0 6px 6px;font-weight:900;font-size:18px;transition:.18s ease}
#chooseAdmin.copa-admin-btn:hover{transform:translateY(-2px)}
.copa-admin-icon{width:94px;height:94px;border-radius:24px;background:#fff;display:grid;place-items:center;font-size:48px;box-shadow:0 13px 30px rgba(22,57,96,.16);border:1px solid #dce6f0}
.copa-admin-sep{display:flex;align-items:center;gap:7px;color:#c9922b}
.copa-admin-sep:before,.copa-admin-sep:after{content:"";width:40px;height:2px;background:#c9922b}
.copa-admin-sep b{font-size:13px;font-weight:400}
#roleGateway #adminLogin.login-card{position:fixed;z-index:120;left:50%;top:50%;transform:translate(-50%,-50%);width:min(460px,calc(100vw - 30px));margin:0;box-shadow:0 0 0 100vmax rgba(8,30,61,.55),0 28px 70px rgba(6,28,58,.32)}
@media(max-width:900px){
  #roleGateway.role-shell{padding:18px 14px 26px}.copa-entry-logo img{width:min(260px,54vw)}
  .copa-entry-layout{grid-template-columns:1fr;gap:18px}.copa-entry-card{grid-template-columns:1fr;min-height:0}
  .copa-entry-photo{order:1;min-height:300px}.copa-entry-copy{order:2;padding:30px 28px}
  #chooseAdmin.copa-admin-btn{justify-self:center}.copa-entry-copy h1{font-size:58px}
}
@media(max-width:560px){
  #roleGateway.role-shell{padding:14px 10px 24px}.copa-entry-logo{margin-bottom:10px}.copa-entry-logo img{width:min(220px,62vw)}
  .copa-entry-layout{gap:14px;max-width:460px}.copa-entry-card{border-radius:26px}.copa-entry-photo{min-height:235px;background-position:center 35%}
  .copa-entry-copy{padding:24px 20px 26px}.copa-ball-icon{width:62px;height:62px;font-size:34px;margin-bottom:16px}
  .copa-entry-copy h1{font-size:49px}.copa-gold-line span{width:90px}.copa-entry-copy p{font-size:17px;margin-bottom:18px}
  #choosePlayer.copa-player-btn{min-height:66px;border-radius:19px;font-size:20px}
  #chooseAdmin.copa-admin-btn{font-size:16px}.copa-admin-icon{width:76px;height:76px;font-size:40px}
}
/* ===== FIN PORTADA COPAFEM NUEVA ===== */
'''

style_end = text.find('</style>')
if style_end < 0:
    raise SystemExit('No se encontró </style>')
text = text[:style_end] + css + '\n' + text[style_end:]

new_gateway = f'''  <section id="roleGateway" class="role-shell">
    <div class="role-wrap">
      <div class="copa-entry-logo"><img src="{logo_src}" alt="COPAFEM San Juan Argentina"></div>
      <div class="copa-entry-layout">
        <div class="copa-entry-card">
          <div class="copa-entry-copy">
            <div class="copa-ball-icon" aria-hidden="true"></div>
            <h1>INGRESO</h1>
            <div class="copa-gold-line" aria-hidden="true"><span></span><b>♡</b><span></span></div>
            <p>Consultá tus partidos, horarios, resultados y el Drop completo.</p>
            <button id="choosePlayer" class="copa-player-btn" type="button"><span class="copa-arrow">→</span><span>SOY JUGADOR</span></button>
          </div>
          <div class="copa-entry-photo" role="img" aria-label="Jugadora de pádel en cancha azul"></div>
        </div>
        <button id="chooseAdmin" class="copa-admin-btn" type="button"><span class="copa-admin-icon">⚙</span><span class="copa-admin-sep"><b>♡</b></span><span>Administrador</span></button>
      </div>
      <div id="adminLogin" class="login-card" hidden>
        <h2>Acceso administrador</h2><p>Ingresá la contraseña para abrir el panel de organización.</p>
        <form id="adminLoginForm"><label>Contraseña<input id="adminPassword" type="password" autocomplete="current-password" required placeholder="Contraseña de administrador"></label><div class="login-actions"><button class="btn primary" type="submit">Ingresar</button><button id="cancelAdminLogin" class="btn" type="button">Volver</button></div><div id="adminLoginError" class="login-error" aria-live="polite"></div></form>
      </div>
    </div>
  </section>'''

pattern = re.compile(r'  <section id="roleGateway" class="role-shell">.*?</section>\s*\n\s*<section id="playerApp" hidden>', re.S)
if not pattern.search(text):
    raise SystemExit('No se encontró la portada actual')
text = pattern.sub(new_gateway + '\n\n  <section id="playerApp" hidden>', text, count=1)
p.write_text(text, encoding='utf-8')
print('Portada COPAFEM aplicada')
