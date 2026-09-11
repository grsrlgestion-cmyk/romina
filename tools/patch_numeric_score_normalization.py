from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
MARKER = 'COPAFEM_NUMERIC_SCORE_NORMALIZATION_V1'
if MARKER in s:
    print('numeric score normalization already applied')
    raise SystemExit

old = '''  const pairName = (id) => state.pairs.find(p => p.id === id)?.name || "—";
  const hasScore = (m) => Number.isFinite(m?.s1) && Number.isFinite(m?.s2);
  const winnerId = (m) => hasScore(m) && m.s1 !== m.s2 ? (m.s1 > m.s2 ? m.p1 : m.p2) : null;
  const loserId = (m) => hasScore(m) && m.s1 !== m.s2 ? (m.s1 > m.s2 ? m.p2 : m.p1) : null;'''
new = '''  const pairName = (id) => state.pairs.find(p => p.id === id)?.name || "—";
  /* COPAFEM_NUMERIC_SCORE_NORMALIZATION_V1
     Supabase/localStorage pueden devolver scores como texto (ej. "4").
     Los normalizamos en el momento de leerlos para que PJ/PG/GF/GC/DG siempre calculen. */
  const hasScore = (m) => {
    if(!m || m.s1 === null || m.s1 === undefined || m.s1 === "" || m.s2 === null || m.s2 === undefined || m.s2 === "") return false;
    const a=Number(m.s1), b=Number(m.s2);
    if(!Number.isFinite(a) || !Number.isFinite(b)) return false;
    m.s1=a; m.s2=b;
    return true;
  };
  const winnerId = (m) => hasScore(m) && m.s1 !== m.s2 ? (m.s1 > m.s2 ? m.p1 : m.p2) : null;
  const loserId = (m) => hasScore(m) && m.s1 !== m.s2 ? (m.s1 > m.s2 ? m.p2 : m.p1) : null;'''
if old not in s:
    raise SystemExit('No se encontró bloque hasScore/winnerId esperado')
s = s.replace(old, new, 1)

old_player = '''  const scored=m=>Number.isFinite(m?.s1)&&Number.isFinite(m?.s2)&&m.s1!==m.s2;'''
new_player = '''  const scored=m=>{
    if(!m || m.s1===null || m.s1===undefined || m.s1==="" || m.s2===null || m.s2===undefined || m.s2==="") return false;
    const a=Number(m.s1),b=Number(m.s2);
    if(!Number.isFinite(a)||!Number.isFinite(b)) return false;
    m.s1=a;m.s2=b;
    return a!==b;
  };'''
if old_player not in s:
    raise SystemExit('No se encontró scored de vista jugador')
s = s.replace(old_player, new_player, 1)

# Al guardar desde los inputs, siempre persiste números, nunca strings.
old_set = '''    const n=value===""?null:parseInt(value,10); m[side]=Number.isFinite(n)?Math.max(0,n):null;'''
new_set = '''    const n=value===""?null:Number(value); m[side]=Number.isFinite(n)?Math.max(0,n):null;'''
# Aparece en zonas y brackets; reemplazamos todas las ocurrencias para uniformidad.
s = s.replace(old_set, new_set)

p.write_text(s, encoding='utf-8')
print('COPAFEM: scores normalizados a número; PJ PG GF GC DG corregidos')
