from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_SWAP_GOLD_OCTAVOS_1_3_V1'
if MARK in s:
    print('swap octavos 1/3 already applied')
    raise SystemExit

old="""  const r16W=r16.map(m=>copafemSource(`W:${m.id}`,winnerId(m)));
  const firsts=zones.map(z=>copafemSeedSource(z,1));
  const qf=copafemMakeSafeStage('G2-QF','Cuartos',firsts,r16W,oldG,r16);
  const qfW=qf.map(m=>copafemSource(`W:${m.id}`,winnerId(m)));"""

new="""  const r16W=r16.map(m=>copafemSource(`W:${m.id}`,winnerId(m)));
  const firsts=zones.map(z=>copafemSeedSource(z,1));

  // Mantener el criterio de cruce ya armado, pero intercambiar exclusivamente
  // el Ganador del Octavo de Oro 1 con el Ganador del Octavo de Oro 3.
  // Se ordenan las fuentes antes de crear los Cuartos para que los resultados
  // de Cuartos sigan siendo persistentes en reconstrucciones posteriores.
  const qfRight=copafemBestRightOrder(firsts.slice(),r16W.slice(),r16);
  if(r16.length>=3){
    const key1=`W:${r16[0].id}`;
    const key3=`W:${r16[2].id}`;
    const i1=qfRight.findIndex(x=>x?.key===key1);
    const i3=qfRight.findIndex(x=>x?.key===key3);
    if(i1>=0 && i3>=0){
      const tmp=qfRight[i1]; qfRight[i1]=qfRight[i3]; qfRight[i3]=tmp;
    }
  }
  const qf=firsts.slice(0,qfRight.length).map((src,i)=>
    copafemMakeMatch(`G2-QF-${i+1}`,'Cuartos',src,qfRight[i],oldG)
  );
  const qfW=qf.map(m=>copafemSource(`W:${m.id}`,winnerId(m)));"""

if old not in s:
    raise SystemExit('No se encontró el armado de Cuartos de Oro de Opción 2')

s=s.replace(old,new,1)
s=s.replace('</body>',f'\n<!-- {MARK} -->\n</body>',1)
p.write_text(s,encoding='utf-8')
print('COPAFEM: Ganadores de Octavos de Oro 1 y 3 intercambiados en Cuartos')
