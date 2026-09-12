from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_DELETE_LAST_CATEGORY_V1'
if MARK in s:
    print('delete last category already applied')
    raise SystemExit

old='''    const groups=new Map();\n    Object.entries(store.events).sort((a,b)=>(a[1].tournament.date||"9999").localeCompare(b[1].tournament.date||"9999") || CATEGORIES.indexOf(a[1].tournament.category)-CATEGORIES.indexOf(b[1].tournament.category)).forEach(([id,e])=>{'''
new='''    const groups=new Map();\n    /* COPAFEM_DELETE_LAST_CATEGORY_V1: no mostrar el borrador vacío que la app mantiene internamente cuando se elimina la última categoría. */\n    Object.entries(store.events)\n      .filter(([,e])=>Boolean(e?.tournament?.date) || (e?.pairs||[]).length>0 || (e?.zoneMatches||[]).length>0)\n      .sort((a,b)=>(a[1].tournament.date||"9999").localeCompare(b[1].tournament.date||"9999") || CATEGORIES.indexOf(a[1].tournament.category)-CATEGORIES.indexOf(b[1].tournament.category)).forEach(([id,e])=>{'''
if old not in s:
    raise SystemExit('No se encontró renderEvents esperado')
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
print('COPAFEM: la última categoría eliminada ya no reaparece como borrador Sin fecha')
