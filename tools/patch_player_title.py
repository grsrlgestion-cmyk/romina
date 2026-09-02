from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')
old = '<h2>Tu torneo, sin complicaciones</h2>'
new = '<h2>TUS PARTIDOS, TUS HORARIOS 🎾</h2>'
if old not in text:
    raise SystemExit('No se encontró el título original')
text = text.replace(old, new, 1)
text = text.replace('name="copafem-app-version" content="2.1.2"','name="copafem-app-version" content="2.1.3"',1)
p.write_text(text, encoding='utf-8')
print('Título del jugador actualizado')
