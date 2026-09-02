from pathlib import Path
import re

p = Path('index.html')
text = p.read_text(encoding='utf-8')

START = '/* ===== PORTADA V16 COPAFEM ===== */'
END = '/* ===== FIN PORTADA V16 COPAFEM ===== */'
text = re.sub(re.escape(START) + r'.*?' + re.escape(END), '', text, flags=re.S)

css = r'''
/* ===== PORTADA V16 COPAFEM ===== */
.v16-gateway{min-height:100vh;background:radial-gradient(circle at top,#f1e4c5 0%,rgba(241,228,197,0) 28%),linear-gradient(145deg,#091b2f 0%,#163b61 52%,#365573 72%,#e8eef3 100%);padding:22px;display:flex;align-items:center;justify-content:center;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
.v16-shell{width:min(620px,100%);background:linear-gradient(180deg,#ffffff 0%,#fbf8f1 100%);border:1px solid rgba(198,154,84,.28);border-radius:28px;padding:38px 44px 34px;box-shadow:0 26px 78px rgba(8,29,50,.26),inset 0 1px 0 rgba(255,255,255,.7);text-align:center;position:relative;overflow:hidden}
.v16-shell:before{content:'';position:absolute;inset:-120px auto auto -80px;width:280px;height:280px;background:radial-gradient(circle,rgba(198,154,84,.18) 0%,rgba(198,154,84,0) 70%);pointer-events:none}
.v16-shell:after{content:'';position:absolute;inset:auto -90px -120px auto;width:260px;height:260px;background:radial-gradient(circle,rgba(35,75,114,.10) 0%,rgba(35,75,114,0) 72%);pointer-events:none}
.v16-brand{display:flex;justify-content:center;align-items:center;position:relative;z-index:1}
.v16-logo{width:190px;height:190px;object-fit:contain;border-radius:50%;border:0;box-shadow:0 14px 36px rgba(20,48,79,.14);filter:drop-shadow(0 2px 0 rgba(198,154,84,.18));background:#fff}
.v16-panel{padding:0;margin-top:22px;position:relative;z-index:1}
.v16-title{font-size:29px;line-height:1.08;font-weight:950;color:#0f2742;margin:0;text-align:center;letter-spacing:.01em}
.v16-copy{margin:8px auto 0;color:#667586;font-size:14px;line-height:1.45;max-width:430px}
.v16-actions{display:grid;grid-template-columns:1fr;gap:9px;margin-top:20px}
.v16-player-btn{min-height:54px;width:100%;border:1px solid #183757;border-radius:12px;background:linear-gradient(135deg,#102844 0%,#21496f 70%,#9d7639 140%);color:#fff;font-weight:900;font-size:16px;box-shadow:0 10px 22px rgba(16,40,68,.14);cursor:pointer}
.v16-player-btn:hover{transform:translateY(-1px)}
.v16-admin-btn{min-height:42px;width:100%;border:0;border-radius:11px;background:transparent;color:#66788a;font-weight:800;font-size:14px;cursor:pointer}
.v16-admin-btn:hover{color:#0f2742;background:linear-gradient(180deg,#f9f7f1 0%,#f1ece2 100%)}
.v16-goldline{height:1px;background:linear-gradient(90deg,transparent,#c69a54,transparent);margin:18px auto 0;width:72%}
.v16-admin-login{margin-top:14px;padding:14px;border:1px solid #ddd3be;border-radius:14px;background:linear-gradient(180deg,#f9fafb 0%,#f4efe5 100%);text-align:left;box-shadow:inset 0 1px 0 rgba(255,255,255,.9);position:relative;z-index:2}
.v16-admin-login h2{margin:0 0 5px;color:#0f2742;font-size:16px}.v16-admin-login p{margin:0 0 10px;color:#667586;font-size:12px;line-height:1.4}
.v16-admin-login label{display:block;color:#536171;font-size:12px;font-weight:800}.v16-admin-login input{width:100%;min-height:48px;margin-top:6px;border:1px solid #c9b789;border-radius:12px;padding:10px 13px;font-size:16px;background:linear-gradient(180deg,#fff 0%,#fffdfa 100%)}
.v16-admin-login .login-actions{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:9px}.v16-admin-login .login-error{font-size:12px;margin-top:7px;color:#a45050}
@media(max-width:760px){.v16-gateway{padding:12px;align-items:flex-start}.v16-shell{padding:28px 20px 24px;margin-top:14px;border-radius:22px}.v16-logo{width:165px;height:165px}.v16-title{font-size:25px}.v16-panel{margin-top:18px}}
/* ===== FIN PORTADA V16 COPAFEM ===== */
'''
text = text.replace('</style>', css + '\n</style>', 1)

gateway = r'''
  <section id="roleGateway" class="v16-gateway">
    <div class="v16-shell">
      <div class="v16-brand">
        <img class="v16-logo" src="logo-copafem-aprobado.svg?v=16" alt="Logo COPAFEM">
      </div>
      <div class="v16-panel">
        <h1 class="v16-title">COPAFEM</h1>
        <p class="v16-copy">Ingresá a tu torneo y consultá tus partidos, horarios, resultados y el Drop completo.</p>
        <div class="v16-goldline"></div>
        <div class="v16-actions">
          <button id="choosePlayer" class="v16-player-btn" type="button">SOY JUGADOR</button>
          <button id="chooseAdmin" class="v16-admin-btn" type="button">⚙ ADMINISTRADOR</button>
        </div>
      </div>
      <div id="adminLogin" class="login-card v16-admin-login" hidden>
        <h2>Acceso administrador</h2>
        <p>Ingresá la contraseña para abrir el panel de organización.</p>
        <form id="adminLoginForm">
          <label>Contraseña<input id="adminPassword" type="password" autocomplete="current-password" required placeholder="Contraseña de administrador"></label>
          <div class="login-actions"><button class="btn primary" type="submit">Ingresar</button><button id="cancelAdminLogin" class="btn" type="button">Volver</button></div>
          <div id="adminLoginError" class="login-error" aria-live="polite"></div>
        </form>
      </div>
    </div>
  </section>
'''

pattern = r'\s*<section id="roleGateway"[^>]*>.*?</section>\s*(?=<section id="playerApp" hidden>)'
text, n = re.subn(pattern, '\n' + gateway + '\n', text, count=1, flags=re.S)
if n != 1:
    raise SystemExit(f'No se pudo reemplazar roleGateway: {n}')

p.write_text(text, encoding='utf-8')
print('Portada V16 aplicada correctamente')
