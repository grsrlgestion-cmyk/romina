from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_DROP_MODE_PERSISTENCE_V1'
if MARK in s:
    print('drop mode persistence already applied')
    raise SystemExit

needle='''        blockedCourts: Array.isArray(t.blockedCourts) ? t.blockedCourts.map(x=>({time:String(x?.time||""),court:Number(x?.court)})).filter(x=>/^\\d{2}:\\d{2}$/.test(x.time)&&Number.isFinite(x.court)&&x.court>=1&&x.court<=8) : []
'''
replacement='''        blockedCourts: Array.isArray(t.blockedCourts) ? t.blockedCourts.map(x=>({time:String(x?.time||""),court:Number(x?.court)})).filter(x=>/^\\d{2}:\\d{2}$/.test(x.time)&&Number.isFinite(x.court)&&x.court>=1&&x.court<=8) : [],
        dropMode: ['op1','op2','op3'].includes(t.dropMode) ? t.dropMode : 'op1'
'''
if needle not in s:
    raise SystemExit('No se encontró blockedCourts de defaultEvent')
s=s.replace(needle,replacement,1)

s=s.replace('</body>', '<!-- '+MARK+' -->\n</body>', 1)
p.write_text(s,encoding='utf-8')
print('COPAFEM: formato del Drop persistente por categoría/fecha')
