from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Escala visual inicial del Drop completo.
s = s.replace('let dropZoom = .85;', 'let dropZoom = 1;', 1)
s = s.replace('id="dropZoomLabel" class="drop-zoom-label">85%</span>', 'id="dropZoomLabel" class="drop-zoom-label">100%</span>', 1)

# Hay dos declaraciones CSS equivalentes en la base; ambas deben arrancar en 100%.
s = s.replace('--drop-scale:.85', '--drop-scale:1')

p.write_text(s, encoding='utf-8')
print('COPAFEM Drop default zoom = 100%')
