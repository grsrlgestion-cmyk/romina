from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

replacement = '<img class="premium-logo" src="logo-copafem-real.png?v=20260903-real" alt="COPAFEM Argentina">'

s, n = re.subn(r'<svg class="premium-logo".*?</svg>', replacement, s, count=1, flags=re.S)
if n != 1:
    raise SystemExit('No se pudo localizar el logo generado en la portada')

p.write_text(s, encoding='utf-8')
print('Logo real de COPAFEM aplicado')
