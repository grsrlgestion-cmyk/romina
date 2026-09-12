from pathlib import Path
import re, subprocess, tempfile

p=Path('index.html')
s=p.read_text(encoding='utf-8')

required_ids=[
  'newEventForm','saveSettingsBtn','generateScheduleBtn','addBulkBtn','clearPairsBtn',
  'generateZonesBtn','regenerateZonesBtn','clearResultsBtn','rebuildBracketsBtn',
  'exportCsvBtn','exportJsonBtn','resetAllBtn','printBtn','dropExcelBtn',
  'dropPrintBtn','dropFitBtn','dropZoomOut','dropZoomIn','resultsContainer',
  'goldBracket','silverBracket','dropScroll','addExtraCourtBtn','blockCourtBtn'
]
missing=[x for x in required_ids if f'id="{x}"' not in s]
if missing:
    raise SystemExit('Faltan controles/áreas críticas: '+', '.join(missing))

required_functions=[
  'function init()','function saveState(','function setZoneScore(','function setBracketScore(',
  'function clearResults()','function renderResults()','function renderCups()',
  'function renderDrop()','function generateSchedule(','function addExtraCourt()',
  'function blockCourt()','function renderExtraCourts()'
]
missing_fn=[x for x in required_functions if x not in s]
if missing_fn:
    raise SystemExit('Faltan funciones críticas: '+', '.join(missing_fn))

# Confirmar conexiones de los botones principales.
listener_tokens=[
  'clearResultsBtn','generateScheduleBtn','generateZonesBtn','rebuildBracketsBtn',
  'dropPrintBtn','dropZoomOut','dropZoomIn','printBtn','addExtraCourtBtn','blockCourtBtn'
]
for token in listener_tokens:
    if s.count(token)<2:
        raise SystemExit(f'Control sin conexión aparente: {token}')

# Errores de orden de carga que anteriormente dejaban todos los botones posteriores sin funcionar.
if 'return copafemRebuildDropByMode(preserveScores);' in s:
    raise SystemExit('Referencia insegura: copafemRebuildDropByMode se llama antes de cargar sus helpers')
if '); copafemRefreshDropModeUI();\n  }' in s:
    raise SystemExit('Referencia insegura: copafemRefreshDropModeUI sin protección de carga')
if 'setTimeout(()=>window.print(),120)' in s:
    raise SystemExit('Impresión del Drop todavía usa setTimeout y puede ser bloqueada por el navegador')

# Validar sintaxis de cada script inline con Node.
scripts=re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>',s,re.S|re.I)
for i,code in enumerate(scripts,1):
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

markers=[
  'COPAFEM_CLEAR_RESULTS_FIX_V1','COPAFEM_LIVE_ZONE_GAMES_V1',
  'COPAFEM_DROP_FORMAT_SELECTOR_V1','COPAFEM_DROP_FORMAT_OP3_V1',
  'COPAFEM_FINAL_WEB_AUDIT_V1','COPAFEM_PRINT_3_PAGES_V2',
  'COPAFEM_RUNTIME_PRINT_RELIABILITY_V1'
]
miss_mark=[m for m in markers if m not in s]
if miss_mark:
    raise SystemExit('Faltan parches finales: '+', '.join(miss_mark))

print(f'COPAFEM VALIDACIÓN OK · {len(required_ids)} controles · {len(scripts)} scripts JS revisados · impresión directa habilitada')
