from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_FIX_NEW_EVENT_RANGE_VALIDATION_V1'
if MARK in s:
    print('range validation fix already applied')
    raise SystemExit

bad = r"const m=/^(\\d{2}):(\\d{2})$/.exec(String(v||''));"
good = r"const m=/^(\d{2}):(\d{2})$/.exec(String(v||''));"

if bad not in s:
    raise SystemExit('No se encontró la validación horaria defectuosa')

s=s.replace(bad, good, 1)
s=s.replace('/* COPAFEM_NEW_EVENT_COURTS_BY_RANGE_V2 */','/* COPAFEM_NEW_EVENT_COURTS_BY_RANGE_V2 */\n  /* COPAFEM_FIX_NEW_EVENT_RANGE_VALIDATION_V1 */',1)

p.write_text(s,encoding='utf-8')
print('COPAFEM: validación de rangos horarios corregida')
