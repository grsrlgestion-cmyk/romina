from pathlib import Path
import re, subprocess, tempfile, sys

p=Path('index.html')
s=p.read_text(encoding='utf-8')

required_ids=[
  'newEventForm','saveSettingsBtn','generateScheduleBtn','addBulkBtn','clearPairsBtn',
  'generateZonesBtn','regenerateZonesBtn','clearResultsBtn','rebuildBracketsBtn',
  'exportCsvBtn','exportJsonBtn','resetAllBtn','printBtn','dropExcelBtn',
  'dropPrintBtn','dropFitBtn','dropZoomOut','dropZoomIn','resultsContainer',
  'goldBracket','silverBracket','dropScroll'
]
missing=[x for x in required_ids if f'id="{x}"' not in s]
if missing:
    raise SystemExit('Faltan controles/áreas críticas: '+', '.join(missing))

required_functions=[
  'function init()','function saveState(','function setZoneScore(','function setBracketScore(',
  'function clearResults()','function renderResults()','function renderCups()',
  'function renderDrop()','function generateSchedule('
]
missing_fn=[x for x in required_functions if x not in s]
if missing_fn:
    raise SystemExit('Faltan funciones críticas: '+', '.join(missing_fn))

# Confirmar que los controles principales tengan conexión de evento en el HTML final.
listener_tokens=[
  'clearResultsBtn','generateScheduleBtn','generateZonesBtn','rebuildBracketsBtn',
  'dropPrintBtn','dropZoomOut','dropZoomIn','printBtn'
]
for token in listener_tokens:
    if s.count(token)<2:
        raise SystemExit(f'Control sin conexión aparente: {token}')

# Validar sintaxis de cada script inline con Node. Los scripts remotos/src se omiten.
scripts=re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>',s,re.S|re.I)
for i,code in enumerate(scripts,1):
    # Evitar falsos positivos por bloques no-JS vacíos.
    if not code.strip():
        continue
    with tempfile.NamedTemporaryFile('w',suffix='.js',delete=False,encoding='utf-8') as f:
        f.write(code)
        name=f.name
    r=subprocess.run(['node','--check',name],capture_output=True,text=True)
    Path(name).unlink(missing_ok=True)
    if r.returncode!=0:
        print(r.stderr)
        raise SystemExit(f'Error de sintaxis JavaScript en script inline #{i}')

# Marcadores de las correcciones recientes que deben existir en el artefacto final.
markers=[
  'COPAFEM_CLEAR_RESULTS_FIX_V1','COPAFEM_LIVE_ZONE_GAMES_V1',
  'COPAFEM_DROP_FORMAT_SELECTOR_V1','COPAFEM_DROP_FORMAT_OP3_V1',
  'COPAFEM_FINAL_WEB_AUDIT_V1','COPAFEM_PRINT_3_PAGES_V2'
]
miss_mark=[m for m in markers if m not in s]
if miss_mark:
    raise SystemExit('Faltan parches finales: '+', '.join(miss_mark))

print(f'COPAFEM VALIDACIÓN OK · {len(required_ids)} controles · {len(scripts)} scripts JS revisados')
