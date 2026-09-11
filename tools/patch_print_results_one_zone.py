from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
MARKER = 'COPAFEM_PRINT_RESULTS_ONE_ZONE_V1'
if MARKER in s:
    print('print results one-zone already applied')
    raise SystemExit

css = r'''
<style id="COPAFEM_PRINT_RESULTS_ONE_ZONE_V1">
@media print {
  /* En Resultados, cada zona completa ocupa su propia hoja. */
  #view-resultados.active #resultsContainer > .zone-block {
    break-inside: avoid !important;
    page-break-inside: avoid !important;
    break-after: page !important;
    page-break-after: always !important;
    margin: 0 0 8mm 0 !important;
  }

  #view-resultados.active #resultsContainer > .zone-block:last-child {
    break-after: auto !important;
    page-break-after: auto !important;
  }

  /* Mantener cada partido y la tabla de posiciones unidos. */
  #view-resultados.active .match-grid,
  #view-resultados.active .standings,
  #view-resultados.active .stand-row {
    break-inside: avoid !important;
    page-break-inside: avoid !important;
  }

  /* Mejor aprovechamiento del ancho al imprimir Resultados. */
  #view-resultados.active .match-grid {
    grid-template-columns: minmax(0,1.35fr) 30mm minmax(0,1.35fr) 38mm !important;
    gap: 2.5mm !important;
    padding: 3mm !important;
    margin: 2mm 0 !important;
    border-radius: 3mm !important;
  }
  #view-resultados.active .team-name {
    font-size: 10pt !important;
    line-height: 1.25 !important;
  }
  #view-resultados.active .schedule-meta {
    font-size: 9pt !important;
    white-space: nowrap !important;
    text-align: right !important;
  }
  #view-resultados.active .score-box input {
    width: 11mm !important;
    height: 9mm !important;
    padding: 1mm !important;
    font-size: 10pt !important;
  }
  #view-resultados.active .zone-block-head {
    margin: 0 0 3mm 0 !important;
  }
  #view-resultados.active .zone-block-head h3 {
    font-size: 17pt !important;
  }
  #view-resultados.active .standings {
    margin-top: 3mm !important;
  }
  #view-resultados.active .stand-row {
    padding: 2.2mm 2.5mm !important;
    font-size: 9pt !important;
  }
}
</style>
'''

if '</head>' not in s:
    raise SystemExit('No se encontró </head>')
s = s.replace('</head>', css + '\n</head>', 1)
p.write_text(s, encoding='utf-8')
print('COPAFEM print Results one zone per page OK')
