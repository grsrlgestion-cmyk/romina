from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
MARKER = 'COPAFEM_CLEAR_RESULTS_FIX_V1'
if MARKER in s:
    print('clear results fix already applied')
    raise SystemExit

pattern = re.compile(r'''  function clearResults\(\)\{\n.*?\n  \}\n\n  function renderAll\(\)''', re.S)
replacement = r'''  /* COPAFEM_CLEAR_RESULTS_FIX_V1 */
  function clearResults(){
    if(!confirm("¿Borrar todos los resultados de zona y copas de esta fecha?")) return;

    // 1) Borrar TODOS los resultados de zona sin modificar horarios ni canchas.
    (state.zoneMatches||[]).forEach(m=>{
      m.s1=null;
      m.s2=null;
    });

    // 2) Borrar resultados de Oro/Plata y dejar los participantes como "A definir".
    // Se conserva la estructura, horario y cancha de cada cruce.
    for(const kind of ["gold","silver"]){
      (state.brackets?.[kind]||[]).forEach(m=>{
        m.s1=null;
        m.s2=null;
        m.p1=null;
        m.p2=null;
      });
    }

    // 3) Guardar ANTES de renderizar, para que ningún reconstruido recupere scores viejos.
    saveState();

    // 4) Refrescar únicamente las vistas afectadas. No reconstruir el Drop durante el borrado.
    renderResults();
    renderCups();
    renderSchedule();
    renderHeader();
    renderDrop();

    // 5) Persistencia final (local y online si corresponde).
    saveState();
    toast("Resultados borrados correctamente");
  }

  function renderAll()'''

s2, n = pattern.subn(replacement, s, count=1)
if n != 1:
    raise SystemExit(f'No se pudo reemplazar clearResults; coincidencias: {n}')

p.write_text(s2, encoding='utf-8')
print('COPAFEM: botón Borrar resultados corregido')
