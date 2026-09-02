from pathlib import Path
import re

p = Path('index.html')
text = p.read_text(encoding='utf-8')

# La portada agrega un script propio. En versiones anteriores quedó insertado
# dentro del HTML que arma el Excel, y el navegador cerraba el <script> principal.
# Lo extraemos de donde haya quedado y lo movemos antes del </body> REAL.
pattern = re.compile(r'\n?<script id="copafem-portada-ingreso-js">.*?</script>\n?', re.S)
m = pattern.search(text)
if m:
    block = m.group(0).strip()
    text = text[:m.start()] + '\n' + text[m.end():]
    pos = text.rfind('</body>')
    if pos == -1:
        raise SystemExit('No se encontró </body> real')
    text = text[:pos] + '\n' + block + '\n' + text[pos:]

# Fuerza apertura desde arriba y elimina registros viejos del service worker.
cleanup = '''<script id="copafem-arranque-limpio">
window.addEventListener('load',()=>{
  try{window.scrollTo(0,0);}catch(e){}
  if('serviceWorker' in navigator){navigator.serviceWorker.getRegistrations().then(rs=>rs.forEach(r=>r.unregister())).catch(()=>{});}
});
</script>'''
text = re.sub(r'\n?<script id="copafem-arranque-limpio">.*?</script>\n?', '\n', text, flags=re.S)
pos = text.rfind('</body>')
text = text[:pos] + '\n' + cleanup + '\n' + text[pos:]

# Validación básica: no debe quedar el código posterior al exportador fuera del script.
opens = len(re.findall(r'<script(?:\s|>)', text, flags=re.I))
closes = len(re.findall(r'</script>', text, flags=re.I))
if opens != closes:
    raise SystemExit(f'HTML inválido: {opens} aperturas de script y {closes} cierres')

p.write_text(text, encoding='utf-8')
print(f'HTML corregido. Scripts balanceados: {opens}/{closes}')
