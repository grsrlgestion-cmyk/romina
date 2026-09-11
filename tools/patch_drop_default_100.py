from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Escala visual inicial del Drop completo.
s = s.replace('let dropZoom = .85;', 'let dropZoom = 1;', 1)
s = s.replace('id="dropZoomLabel" class="drop-zoom-label">85%</span>', 'id="dropZoomLabel" class="drop-zoom-label">100%</span>', 1)

# Hay dos declaraciones CSS equivalentes en la base; ambas deben arrancar en 100%.
s = s.replace('--drop-scale:.85', '--drop-scale:1')

# No ejecutar "Ver completo" automáticamente al entrar al Drop.
# El usuario puede seguir usando ese botón manualmente.
s = s.replace('if(name==="drop") setTimeout(fitDrop,60);', 'if(name==="drop") setTimeout(()=>setDropZoom(1),60);', 1)

p.write_text(s, encoding='utf-8')
print('COPAFEM Drop abre al 100% sin auto-fit')
