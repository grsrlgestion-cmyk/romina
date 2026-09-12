from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# El parche anterior (patch_placeholder_source_labels.py) ya deja cada lugar como:
# 1° ZONA A · A definir
# y, cuando se resuelve, como:
# 1° ZONA A · Nombre de la pareja
# Este paso se mantiene solo por compatibilidad con el workflow.
if 'COPAFEM_PLACEHOLDER_SOURCE_LABELS_V1' not in s:
    raise SystemExit('No se aplicó el parche de origen de los cruces')

print('COPAFEM: zona y posición en Oro/Plata ya aplicadas por el paso anterior')
