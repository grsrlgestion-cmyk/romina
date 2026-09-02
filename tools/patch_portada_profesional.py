from pathlib import Path
import re

p = Path('index.html')
text = p.read_text(encoding='utf-8')

# Quitar portada inyectada anterior.
text = re.sub(r'\n?<style id="copafem-portada-profesional">.*?</style>\n?', '\n', text, flags=re.S)
text = re.sub(r'\n?<script id="copafem-portada-ingreso-js">.*?</script>\n?', '\n', text, flags=re.S)

css = r'''
<style id="copafem-portada-profesional">
:root{--cp-navy:#082f63;--cp-blue:#0d477f;--cp-gold:#e6ad37;--cp-ink:#0d3970}
html,body{margin:0;padding:0}
.cp-cover{height:100svh;min-height:650px;overflow:hidden;box-sizing:border-box;position:relative;background:linear-gradient(180deg,#fff 0%,#f7fbff 72%,#eef5fc 100%);display:flex;align-items:center;justify-content:center;padding:14px 26px 20px;color:var(--cp-ink)}
.cp-cover:before{content:"";position:absolute;left:-120px;top:80px;width:520px;height:520px;background:linear-gradient(135deg,rgba(137,190,235,.38),rgba(222,237,249,.08));clip-path:polygon(0 20%,95% 0,70% 18%,100% 32%,62% 42%,91% 58%,44% 67%,80% 84%,0 100%);opacity:.48;transform:rotate(-8deg)}
.cp-cover:after{content:"";position:absolute;right:-100px;top:58px;width:400px;height:400px;border:14px solid rgba(103,160,211,.09);border-radius:50%;box-shadow:inset 0 0 0 2px rgba(103,160,211,.08);opacity:.8}
.cp-shell{position:relative;z-index:2;width:min(1320px,96vw);height:min(900px,calc(100svh - 28px));display:flex;flex-direction:column;align-items:center;justify-content:center}
.cp-logo-wrap{height:150px;display:flex;align-items:center;justify-content:center;margin-bottom:7px}
.cp-logo{width:190px;height:190px;object-fit:contain;display:block;filter:drop-shadow(0 9px 24px rgba(19,59,105,.10));border-radius:0;background:transparent}
.cp-main-row{width:100%;display:grid;grid-template-columns:minmax(0,1fr) 122px;gap:34px;align-items:end}
.cp-card{height:min(510px,57svh);min-height:410px;border-radius:30px;overflow:hidden;display:grid;grid-template-columns:48% 52%;background:#082f63;box-shadow:0 22px 58px rgba(16,54,99,.20);border:1px solid rgba(14,59,108,.12)}
.cp-form-side{position:relative;padding:34px 42px 30px;color:#fff;display:flex;flex-direction:column;justify-content:center;background:linear-gradient(135deg,#052a58 0%,#07396f 66%,#0b4a82 100%);box-sizing:border-box;overflow:hidden}
.cp-form-side:after{content:"";position:absolute;right:-74px;top:-25%;width:170px;height:150%;border-radius:50%;border:6px solid var(--cp-gold);opacity:.95;box-shadow:0 0 0 8px rgba(8,47,99,.35)}
.cp-mini-ball{width:58px;height:58px;border-radius:50%;background:#fff;color:var(--cp-gold);display:grid;place-items:center;font-size:28px;margin-bottom:16px;box-shadow:0 8px 20px rgba(0,0,0,.13);position:relative;z-index:2}
.cp-title{font:500 clamp(50px,5.4vw,78px)/.92 Georgia,'Times New Roman',serif;letter-spacing:.015em;margin:0;position:relative;z-index:2}
.cp-gold-line{height:2px;width:270px;max-width:75%;margin:16px 0 15px;background:linear-gradient(90deg,var(--cp-gold) 0 43%,transparent 43% 57%,var(--cp-gold) 57% 100%);position:relative;z-index:2}.cp-gold-line:after{content:'♡';position:absolute;left:48%;top:-11px;color:var(--cp-gold);font-size:16px;transform:translateX(-50%)}
.cp-intro{font-size:17px;line-height:1.4;margin:0 0 17px;max-width:430px;color:#f4f8fd;position:relative;z-index:2}
.cp-entry-form{display:grid;gap:10px;width:min(365px,100%);position:relative;z-index:3}
.cp-input-wrap{height:55px;border-radius:12px;background:#fff;display:flex;align-items:center;padding:0 16px;border:1px solid rgba(223,232,242,.8);box-shadow:0 5px 14px rgba(0,0,0,.09);box-sizing:border-box}.cp-input-wrap span{font-size:22px;color:#346aa2;margin-right:12px}.cp-input-wrap input{width:100%;border:0;outline:0;background:transparent;font-size:18px;color:#1a426e;font-family:inherit}.cp-input-wrap input::placeholder{color:#8296ae}
.cp-enter-btn{height:58px;border:0;border-radius:12px;background:linear-gradient(90deg,#e6ac36,#f0bd56);color:#0a376e;font-weight:950;font-size:20px;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:16px;box-shadow:0 9px 20px rgba(0,0,0,.16);transition:.18s}.cp-enter-btn:hover{transform:translateY(-2px);box-shadow:0 12px 25px rgba(0,0,0,.20)}.cp-enter-btn b{font-size:28px;font-weight:400}.cp-entry-error{min-height:16px;color:#ffe0a0;font-size:12px;font-weight:750;padding-left:3px}
.cp-photo{position:relative;background-image:linear-gradient(90deg,rgba(8,47,99,.13),rgba(4,31,65,.02)),url('https://afpcourts.com/wp-content/uploads/Marita_Bendinat_adidas_Panoramic_AFP-scaled.jpg');background-size:cover;background-position:center 39%;overflow:hidden}.cp-photo:after{content:"";position:absolute;inset:0;box-shadow:inset 32px 0 46px rgba(8,47,99,.22)}
.cp-admin{align-self:end;margin-bottom:22px;border:0;background:transparent;color:#133f75;font-size:15px;font-weight:900;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:7px;width:122px}.cp-admin-icon{width:78px;height:78px;border-radius:19px;background:#fff;display:grid;place-items:center;font-size:37px;box-shadow:0 12px 28px rgba(16,58,103,.14);border:1px solid #dce8f3}.cp-admin-line{width:70px;height:2px;background:linear-gradient(90deg,var(--cp-gold) 0 40%,transparent 40% 60%,var(--cp-gold) 60%);position:relative}.cp-admin-line:after{content:'♡';position:absolute;left:30px;top:-10px;color:var(--cp-gold);font-size:12px}
.cp-features{width:calc(100% - 155px);align-self:flex-start;margin-top:18px;margin-left:0;display:grid;grid-template-columns:repeat(4,1fr);background:rgba(255,255,255,.93);border-radius:18px;border:1px solid #e1eaf4;box-shadow:0 9px 26px rgba(15,55,99,.08);overflow:hidden}.cp-feature{min-height:76px;display:flex;align-items:center;gap:12px;padding:10px 18px;box-sizing:border-box;border-left:1px solid #dce6ef}.cp-feature:first-child{border-left:0}.cp-fi{width:46px;height:46px;min-width:46px;border-radius:50%;background:#f7fbff;display:grid;place-items:center;font-size:25px;color:#123d74;box-shadow:0 5px 14px rgba(17,57,102,.10)}.cp-feature strong{display:block;font-size:13px;color:#0c376c}.cp-feature small{display:block;font-size:10px;line-height:1.25;color:#657c96;margin-top:3px}
.cp-footer-wave{position:absolute;left:-5%;bottom:-165px;width:110%;height:220px;border-radius:50% 50% 0 0;background:#072f63;border-top:5px solid var(--cp-gold);z-index:1}
.cp-login{position:fixed!important;z-index:400!important;left:50%;top:50%;transform:translate(-50%,-50%);width:min(460px,calc(100vw - 28px));margin:0!important;background:#fff!important;box-shadow:0 24px 70px rgba(13,43,78,.32)!important}
@media(max-height:790px) and (min-width:821px){.cp-cover{min-height:600px;padding-top:8px}.cp-shell{height:calc(100svh - 18px)}.cp-logo-wrap{height:104px;margin-bottom:3px}.cp-logo{width:132px;height:132px}.cp-card{height:min(430px,58svh);min-height:360px}.cp-form-side{padding:25px 36px 22px}.cp-mini-ball{width:48px;height:48px;font-size:23px;margin-bottom:10px}.cp-title{font-size:56px}.cp-intro{font-size:15px;margin-bottom:12px}.cp-input-wrap{height:48px}.cp-enter-btn{height:50px;font-size:18px}.cp-admin{margin-bottom:12px}.cp-admin-icon{width:64px;height:64px;font-size:30px}.cp-features{margin-top:10px}.cp-feature{min-height:62px;padding:7px 14px}.cp-fi{width:38px;height:38px;min-width:38px;font-size:20px}.cp-footer-wave{bottom:-190px}}
@media(max-width:820px){.cp-cover{height:auto;min-height:100svh;overflow:auto;padding:12px 11px 25px}.cp-shell{height:auto;width:100%;justify-content:flex-start}.cp-logo-wrap{height:120px;margin-bottom:5px}.cp-logo{width:130px;height:130px}.cp-main-row{grid-template-columns:1fr;gap:10px}.cp-card{height:auto;min-height:0;grid-template-columns:1fr;border-radius:24px}.cp-form-side{padding:25px 20px 22px}.cp-form-side:after{display:none}.cp-mini-ball{width:50px;height:50px;margin-bottom:12px}.cp-title{font-size:49px}.cp-intro{font-size:16px}.cp-entry-form{width:100%}.cp-photo{min-height:245px;background-position:center 33%}.cp-admin{justify-self:center;align-self:center;margin:4px 0 0}.cp-admin-icon{width:62px;height:62px;font-size:30px}.cp-features{width:100%;grid-template-columns:1fr 1fr;margin-top:10px}.cp-feature{border-left:0;border-top:1px solid #dce6ef;min-height:65px}.cp-feature:nth-child(-n+2){border-top:0}.cp-footer-wave{display:none}}
@media(max-width:480px){.cp-logo-wrap{height:105px}.cp-logo{width:112px;height:112px}.cp-photo{min-height:210px}.cp-features{grid-template-columns:1fr}.cp-feature{border-top:1px solid #dce6ef!important}.cp-feature:first-child{border-top:0!important}}
</style>
'''
text = text.replace('</head>', css + '\n</head>', 1)

gateway = r'''  <section id="roleGateway" class="cp-cover">
    <div class="cp-footer-wave" aria-hidden="true"></div>
    <div class="cp-shell">
      <div class="cp-logo-wrap"><img class="cp-logo" src="logo.jpg?v=20260902d" alt="COPAFEM Argentina"></div>
      <div class="cp-main-row">
        <div class="cp-card">
          <div class="cp-form-side">
            <div class="cp-mini-ball">◯</div>
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
          <div class="cp-photo" aria-hidden="true"></div>
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
  function buscarJugador(){
    const first=document.getElementById('coverFirstName')?.value||'';
    const last=document.getElementById('coverLastName')?.value||'';
    const target=norm(first+' '+last);
    if(!target) return;
    setTimeout(()=>{
      try{
        const ds=document.getElementById('playerDate'),cs=document.getElementById('playerCategory'),ps=document.getElementById('playerName');
        if(!ds||!cs||!ps) return;
        for(const d of [...ds.options]){
          ds.value=d.value; if(typeof populateCategories==='function') populateCategories();
          for(const c of [...cs.options]){
            cs.value=c.value; if(typeof populatePlayers==='function') populatePlayers();
            const found=[...ps.options].find(o=>{const n=norm(o.textContent);return n===target||n.includes(target)||target.includes(n)});
            if(found){ps.value=found.value;if(typeof renderPlayer==='function')renderPlayer();return;}
          }
        }
        const err=document.getElementById('coverEntryError'); if(err)err.textContent='No encontramos ese nombre. Podés seleccionarte manualmente en la pantalla siguiente.';
      }catch(e){}
    },0);
  }
  window.addEventListener('DOMContentLoaded',()=>{
    const btn=document.getElementById('choosePlayer');
    if(btn) btn.addEventListener('click',buscarJugador);
    ['coverFirstName','coverLastName'].forEach(id=>document.getElementById(id)?.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();btn?.click();}}));
  });
})();
</script>
'''
text = text.replace('</body>', extra_js + '\n</body>', 1)
text = re.sub(r'name="copafem-app-version" content="[^"]+"', 'name="copafem-app-version" content="2.1.8"', text, count=1)
p.write_text(text, encoding='utf-8')
print('Portada COPAFEM aprobada aplicada')
