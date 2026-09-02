from pathlib import Path
import re

p = Path('index.html')
text = p.read_text(encoding='utf-8')

text = re.sub(r'\n?<style id="copafem-portada-profesional">.*?</style>\n?', '\n', text, flags=re.S)
text = re.sub(r'\n?<script id="copafem-portada-ingreso-js">.*?</script>\n?', '\n', text, flags=re.S)

css = r'''
<style id="copafem-portada-profesional">
:root{--cp-navy:#0b3468;--cp-blue:#8eb9e8;--cp-gold:#d8a533;--cp-ink:#153b70;--cp-soft:#f5f9fe}
html,body{margin:0;padding:0}
.cp-cover{min-height:100svh;box-sizing:border-box;position:relative;overflow:hidden;background:linear-gradient(180deg,#fff 0%,#f8fbff 70%,#eef5fc 100%);display:flex;align-items:center;justify-content:center;color:var(--cp-ink);padding:16px 20px}
.cp-cover:before{content:"";position:absolute;left:-150px;top:70px;width:590px;height:520px;background:linear-gradient(135deg,rgba(148,194,235,.48),rgba(255,255,255,0));clip-path:polygon(0 20%,90% 0,62% 22%,100% 38%,58% 51%,88% 70%,36% 80%,70% 100%,0 92%);opacity:.55;transform:rotate(-9deg)}
.cp-cover:after{content:"";position:absolute;right:-135px;top:30px;width:460px;height:460px;border-radius:50%;border:12px solid rgba(113,166,216,.08);box-shadow:inset 0 0 0 2px rgba(113,166,216,.08);opacity:.8}
.cp-shell{position:relative;z-index:2;width:min(1280px,96vw);height:min(900px,calc(100svh - 24px));display:flex;flex-direction:column;align-items:center;justify-content:center}
.cp-brand{height:190px;display:flex;align-items:center;justify-content:center;margin-bottom:10px;position:relative}
.cp-logo-img{width:210px;height:210px;object-fit:contain;display:block;filter:drop-shadow(0 10px 25px rgba(23,58,101,.10))}
.cp-logo-fallback{display:none;width:210px;height:210px;border:2px solid #173f75;border-radius:50%;background:#fff;position:relative;align-items:center;justify-content:center;flex-direction:column;box-shadow:0 10px 25px rgba(23,58,101,.08)}
.cp-logo-fallback b{font:500 45px/1 Georgia,serif;letter-spacing:4px;color:#163e74}.cp-logo-fallback small{font-size:11px;letter-spacing:4px;font-weight:800;color:#173f75;margin-top:10px}.cp-logo-fallback i{font-style:normal;color:#a37820;font-size:12px;margin-top:7px}
.cp-layout{width:100%;display:grid;grid-template-columns:minmax(0,1fr) 150px;gap:28px;align-items:center}
.cp-card{height:min(405px,48svh);min-height:360px;border-radius:32px;background:rgba(255,255,255,.90);border:1px solid rgba(215,228,241,.92);box-shadow:0 22px 55px rgba(19,56,98,.16);display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;padding:30px 38px;box-sizing:border-box;backdrop-filter:blur(8px)}
.cp-card:before{content:"";position:absolute;left:-40px;bottom:-15px;width:390px;height:190px;background:linear-gradient(135deg,rgba(139,186,231,.35),rgba(255,255,255,0));clip-path:polygon(0 0,100% 45%,68% 55%,92% 72%,46% 76%,78% 100%,0 92%);opacity:.6}
.cp-card:after{content:"";position:absolute;right:-45px;bottom:-20px;width:350px;height:170px;background:linear-gradient(315deg,rgba(145,191,234,.30),rgba(255,255,255,0));clip-path:polygon(0 45%,100% 0,100% 100%,22% 88%,48% 70%);opacity:.55}
.cp-form{position:relative;z-index:2;width:min(470px,100%);display:flex;flex-direction:column;align-items:center;text-align:center}
.cp-title{margin:0;color:#10386e;font:500 clamp(52px,5vw,75px)/.95 Georgia,'Times New Roman',serif;letter-spacing:.01em}
.cp-gold-line{height:2px;width:345px;max-width:82%;margin:15px 0 14px;background:linear-gradient(90deg,var(--cp-gold) 0 43%,transparent 43% 57%,var(--cp-gold) 57% 100%);position:relative}.cp-gold-line:after{content:'♡';position:absolute;left:50%;top:-12px;transform:translateX(-50%);background:#fff;color:var(--cp-gold);padding:0 9px;font-size:17px}
.cp-intro{margin:0 0 16px;color:#173d70;font-size:16px;line-height:1.45;max-width:430px}
.cp-entry-form{width:min(400px,100%);display:grid;gap:10px}
.cp-input-wrap{height:55px;border-radius:13px;background:#fff;border:1px solid #bcd3ea;box-shadow:0 6px 17px rgba(25,65,108,.06);display:flex;align-items:center;padding:0 16px;box-sizing:border-box}.cp-input-wrap span{font-size:21px;color:#7395bd;margin-right:12px}.cp-input-wrap input{width:100%;border:0;outline:0;background:transparent;color:#173e70;font-size:18px}.cp-input-wrap input::placeholder{color:#8195ae}
.cp-enter-btn{height:58px;border:0;border-radius:13px;background:linear-gradient(90deg,#d99f2d,#f0bd58);color:#0e376b;font-size:20px;font-weight:950;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:16px;box-shadow:0 10px 22px rgba(187,135,31,.20);transition:.18s}.cp-enter-btn:hover{transform:translateY(-2px);box-shadow:0 14px 27px rgba(187,135,31,.25)}.cp-enter-btn b{font-size:29px;font-weight:400}.cp-entry-error{min-height:15px;color:#a45b00;font-size:12px;font-weight:800;text-align:left}
.cp-admin{border:0;background:transparent;color:#153e74;font-size:16px;font-weight:900;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:8px}.cp-admin-icon{width:98px;height:98px;border-radius:24px;background:#fff;display:grid;place-items:center;font-size:45px;box-shadow:0 14px 34px rgba(24,62,103,.15);border:1px solid #dce8f3}.cp-admin-line{width:82px;height:2px;background:linear-gradient(90deg,var(--cp-gold) 0 39%,transparent 39% 61%,var(--cp-gold) 61%);position:relative}.cp-admin-line:after{content:'♡';position:absolute;left:35px;top:-11px;color:var(--cp-gold);font-size:13px}
.cp-features{width:calc(100% - 180px);align-self:flex-start;margin-top:22px;display:grid;grid-template-columns:repeat(4,1fr);gap:0}.cp-feature{display:flex;align-items:center;gap:13px;padding:7px 24px;border-left:1px solid #d8e4ef;min-height:70px}.cp-feature:first-child{border-left:0}.cp-fi{width:58px;height:58px;min-width:58px;border-radius:50%;background:linear-gradient(180deg,#f9fcff,#e9f3fd);border:1px solid #d4e4f2;box-shadow:0 8px 20px rgba(20,57,100,.09);display:grid;place-items:center;font-size:29px;color:#113d74}.cp-feature strong{display:block;color:#0e376c;font-size:14px}.cp-feature small{display:block;color:#637b96;font-size:11px;line-height:1.25;margin-top:3px}
.cp-login{position:fixed!important;z-index:500!important;left:50%;top:50%;transform:translate(-50%,-50%);width:min(460px,calc(100vw - 28px));margin:0!important;background:#fff!important;box-shadow:0 25px 75px rgba(12,43,78,.32)!important}
@media(max-height:780px) and (min-width:821px){.cp-cover{padding:8px 18px}.cp-shell{height:calc(100svh - 16px)}.cp-brand{height:125px;margin-bottom:4px}.cp-logo-img,.cp-logo-fallback{width:138px;height:138px}.cp-logo-fallback b{font-size:30px}.cp-card{height:365px;min-height:330px}.cp-title{font-size:56px}.cp-intro{font-size:14px;margin-bottom:11px}.cp-input-wrap{height:47px}.cp-enter-btn{height:49px;font-size:18px}.cp-admin-icon{width:72px;height:72px;font-size:34px}.cp-features{margin-top:10px}.cp-feature{min-height:54px;padding:4px 15px}.cp-fi{width:42px;height:42px;min-width:42px;font-size:21px}}
@media(max-width:820px){.cp-cover{height:auto;min-height:100svh;overflow:auto;padding:12px 12px 25px}.cp-shell{height:auto;width:100%;justify-content:flex-start}.cp-brand{height:135px;margin-bottom:5px}.cp-logo-img,.cp-logo-fallback{width:140px;height:140px}.cp-layout{grid-template-columns:1fr;gap:12px}.cp-card{height:auto;min-height:390px;border-radius:26px;padding:24px 18px}.cp-admin{justify-self:center}.cp-admin-icon{width:70px;height:70px;font-size:32px}.cp-features{width:100%;grid-template-columns:1fr 1fr;margin-top:12px}.cp-feature{border-left:0;border-top:1px solid #dce6ef;padding:10px 13px}.cp-feature:nth-child(-n+2){border-top:0}}
@media(max-width:480px){.cp-brand{height:115px}.cp-logo-img,.cp-logo-fallback{width:120px;height:120px}.cp-card{min-height:370px}.cp-title{font-size:48px}.cp-intro{font-size:14px}.cp-entry-form{width:100%}.cp-features{grid-template-columns:1fr}.cp-feature{border-top:1px solid #dce6ef!important}.cp-feature:first-child{border-top:0!important}}
</style>
'''

text = text.replace('</head>', css + '\n</head>', 1)

gateway = r'''  <section id="roleGateway" class="cp-cover">
    <div class="cp-shell">
      <div class="cp-brand">
        <img class="cp-logo-img" src="logo.jpg?v=20260902-final" alt="COPAFEM" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
        <div class="cp-logo-fallback"><b>COPA<br>FEM</b><i>NO PUEDO, tengo pádel</i><small>ARGENTINA</small></div>
      </div>
      <div class="cp-layout">
        <div class="cp-card">
          <div class="cp-form">
            <h1 class="cp-title">INGRESO</h1>
            <div class="cp-gold-line"></div>
            <p class="cp-intro">Ingresá tus datos para ver tus partidos, horarios, resultados y el Drop completo.</p>
            <div class="cp-entry-form" role="form" aria-label="Ingreso jugador">
              <label class="cp-input-wrap"><span>♙</span><input id="coverFirstName" type="text" autocomplete="given-name" placeholder="Nombre" aria-label="Nombre"></label>
              <label class="cp-input-wrap"><span>♙</span><input id="coverLastName" type="text" autocomplete="family-name" placeholder="Apellido" aria-label="Apellido"></label>
              <button id="choosePlayer" class="cp-enter-btn" type="button"><b>→</b> INGRESAR</button>
              <div id="coverEntryError" class="cp-entry-error"></div>
            </div>
          </div>
        </div>
        <button id="chooseAdmin" class="cp-admin" type="button"><span class="cp-admin-icon">⚙</span><span class="cp-admin-line"></span><span>Administrador</span></button>
      </div>
      <div class="cp-features">
        <div class="cp-feature"><span class="cp-fi">▣</span><div><strong>TUS PARTIDOS</strong><small>Consultá tus próximos partidos</small></div></div>
        <div class="cp-feature"><span class="cp-fi">◷</span><div><strong>TUS HORARIOS</strong><small>Día, hora y cancha</small></div></div>
        <div class="cp-feature"><span class="cp-fi">♕</span><div><strong>RESULTADOS</strong><small>Actualizados al instante</small></div></div>
        <div class="cp-feature"><span class="cp-fi">⌘</span><div><strong>DROP COMPLETO</strong><small>Explorá el cuadro completo</small></div></div>
      </div>
    </div>
    <div id="adminLogin" class="login-card cp-login" hidden>
      <h2>Acceso administrador</h2><p>Ingresá la contraseña para abrir el panel de organización.</p>
      <form id="adminLoginForm"><label>Contraseña<input id="adminPassword" type="password" autocomplete="current-password" required placeholder="Contraseña de administrador"></label><div class="login-actions"><button class="btn primary" type="submit">Ingresar</button><button id="cancelAdminLogin" class="btn" type="button">Volver</button></div><div id="adminLoginError" class="login-error" aria-live="polite"></div></form>
    </div>
  </section>
'''

pattern = r'\s*<section id="roleGateway"[^>]*>.*?</section>\s*(?=<section id="playerApp" hidden>)'
text, n = re.subn(pattern, '\n' + gateway + '\n', text, count=1, flags=re.S)
if n != 1:
    raise SystemExit(f'No se encontró roleGateway: {n}')

extra_js = r'''
<script id="copafem-portada-ingreso-js">
(function(){
  const norm=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
  const btn=document.getElementById('choosePlayer');
  if(btn){btn.addEventListener('click',function(ev){
    const first=(document.getElementById('coverFirstName')?.value||'').trim();
    const last=(document.getElementById('coverLastName')?.value||'').trim();
    const err=document.getElementById('coverEntryError');
    if(!first||!last){if(err)err.textContent='Ingresá nombre y apellido.';ev.preventDefault();ev.stopImmediatePropagation();return;}
    if(err)err.textContent='';
    const target=norm(first+' '+last);
    setTimeout(()=>{
      try{
        const ps=document.getElementById('playerName') || [...document.querySelectorAll('select')].find(s=>[...s.options].some(o=>norm(o.textContent).includes(norm(first))&&norm(o.textContent).includes(norm(last))));
        if(!ps)return;
        const op=[...ps.options].find(o=>{const t=norm(o.textContent);return t.includes(norm(first))&&t.includes(norm(last));});
        if(op){ps.value=op.value;ps.dispatchEvent(new Event('change',{bubbles:true}));}
      }catch(e){}
    },500);
  },true);}
})();
</script>
'''
text = text.replace('</body>', extra_js + '\n</body>', 1)
text = re.sub(r'name="copafem-app-version" content="[^"]+"','name="copafem-app-version" content="2.1.8"',text)
p.write_text(text,encoding='utf-8')
print('Portada COPAFEM aprobada aplicada')
