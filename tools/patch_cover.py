from pathlib import Path
import re

p = Path('index.html')
text = p.read_text(encoding='utf-8')

cover_css = r'''
/* ===== PORTADA COPAFEM ===== */
.cover-gateway{
  min-height:100vh;
  background:#f7f9fc;
  display:flex;
  justify-content:center;
  align-items:flex-start;
  padding:0;
  overflow-x:hidden;
}
.cover-stage{
  position:relative;
  width:min(100vw,1672px);
  aspect-ratio:1672/941;
  margin:0 auto;
  background:#fff;
}
.cover-image{
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
  object-fit:contain;
  display:block;
  user-select:none;
  -webkit-user-drag:none;
}
.cover-hit{
  position:absolute;
  z-index:5;
  border:0;
  background:transparent;
  cursor:pointer;
  padding:0;
  border-radius:26px;
  -webkit-tap-highlight-color:transparent;
}
.cover-hit:focus-visible{
  outline:4px solid rgba(31,78,130,.45);
  outline-offset:3px;
}
.cover-player{left:15.8%;top:71.2%;width:23.1%;height:10.8%;}
.cover-admin{left:83.7%;top:68.1%;width:10.5%;height:16.5%;}
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
@media(max-width:700px){
  .cover-gateway{min-height:auto;background:#fff;}
  .cover-stage{width:100vw;}
  .cover-player{left:14.5%;top:69.5%;width:27%;height:14%;}
  .cover-admin{left:81.5%;top:64.5%;width:17%;height:24%;}
}
'''

if '/* ===== PORTADA COPAFEM ===== */' not in text:
    text = text.replace('  </style>', cover_css + '\n  </style>', 1)

new_gateway = '''  <section id="roleGateway" class="cover-gateway">
    <div class="cover-stage">
      <img class="cover-image" src="portada-copafem.webp" alt="COPAFEM · Ingreso">
      <button id="choosePlayer" class="cover-hit cover-player" type="button" aria-label="Soy jugador"></button>
      <button id="chooseAdmin" class="cover-hit cover-admin" type="button" aria-label="Administrador"></button>
    </div>
    <div id="adminLogin" class="login-card cover-login" hidden>
      <h2>Acceso administrador</h2><p>Ingresá la contraseña para abrir el panel de organización.</p>
      <form id="adminLoginForm"><label>Contraseña<input id="adminPassword" type="password" autocomplete="current-password" required placeholder="Contraseña de administrador"></label><div class="login-actions"><button class="btn primary" type="submit">Ingresar</button><button id="cancelAdminLogin" class="btn" type="button">Volver</button></div><div id="adminLoginError" class="login-error" aria-live="polite"></div></form>
    </div>
  </section>
'''

pattern = r'  <section id="roleGateway" class="role-shell">.*?</section>\s*\n\s*<section id="playerApp" hidden>'
replacement = new_gateway + '\n  <section id="playerApp" hidden>'
text, n = re.subn(pattern, replacement, text, count=1, flags=re.S)
if n != 1:
    raise SystemExit(f'No se pudo reemplazar la portada: {n}')

text = re.sub(r'name="copafem-app-version" content="[^"]+"', 'name="copafem-app-version" content="2.1.4"', text, count=1)
p.write_text(text, encoding='utf-8')
print('Portada COPAFEM aplicada')
