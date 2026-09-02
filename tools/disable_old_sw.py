from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')
old = 'if("serviceWorker" in navigator && location.protocol.startsWith("http")) navigator.serviceWorker.register("sw.js").catch(()=>{});'
new = '''if ("serviceWorker" in navigator) {
  navigator.serviceWorker.getRegistrations().then(regs => regs.forEach(reg => reg.unregister())).catch(()=>{});
}
if (window.caches) {
  caches.keys().then(keys => Promise.all(keys.map(key => caches.delete(key)))).catch(()=>{});
}'''
if old in text:
    text = text.replace(old, new, 1)
elif 'navigator.serviceWorker.register("sw.js")' in text:
    text = text.replace('navigator.serviceWorker.register("sw.js").catch(()=>{});', new, 1)
# Agrega cabeceras meta para evitar reutilizar una portada antigua del navegador.
marker = '<meta name="viewport"'
meta = '<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">\n  <meta http-equiv="Pragma" content="no-cache">\n  <meta http-equiv="Expires" content="0">\n  '
if 'http-equiv="Cache-Control"' not in text and marker in text:
    text = text.replace(marker, meta + marker, 1)
p.write_text(text, encoding='utf-8')
print('Service Worker antiguo desactivado y caches limpiadas')
