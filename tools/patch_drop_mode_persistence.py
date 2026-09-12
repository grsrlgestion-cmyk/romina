from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_DROP_MODE_PERSISTENCE_V1'
if MARK in s:
    print('drop mode persistence already applied')
    raise SystemExit

old='''        duration: Number(t.duration) || 30,
        courts: Array.isArray(t.courts) && t.courts.length ? [...t.courts] : [1,3,5,7]
'''
new='''        duration: Number(t.duration) || 30,
        courts: Array.isArray(t.courts) && t.courts.length ? [...t.courts] : [1,3,5,7],
        dropMode: ['op1','op2','op3'].includes(t.dropMode) ? t.dropMode : 'op1'
'''
if old not in s:
    raise SystemExit('No se encontró tournament de defaultEvent')
s=s.replace(old,new,1)

s=s.replace('</body>', '<!-- '+MARK+' -->\n</body>', 1)
p.write_text(s,encoding='utf-8')
print('COPAFEM: formato del Drop persistente por categoría/fecha')
