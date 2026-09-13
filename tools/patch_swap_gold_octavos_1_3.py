from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_SWAP_GOLD_OCTAVOS_1_3_V1'
if MARK in s:
    print('swap octavos 1/3 y 2/4 already applied')
    raise SystemExit

old="""  const r16W=r16.map(m=>copafemSource(`W:${m.id}`,winnerId(m)));
  const firsts=zones.map(z=>copafemSeedSource(z,1));
  const qf=copafemMakeSafeStage('G2-QF','Cuartos',firsts,r16W,oldG,r16);
  const qfW=qf.map(m=>copafemSource(`W:${m.id}`,winnerId(m)));"""

new="""  const r16W=r16.map(m=>copafemSource(`W:${m.id}`,winnerId(m)));
  const firsts=zones.map(z=>copafemSeedSource(z,1));

  // Mantener el criterio de cruce ya armado, pero intercambiar exclusivamente
  // los ganadores de Octavos 1 con 3 y 2 con 4 en los Cuartos de Oro.
  // Se ordenan las fuentes antes de crear los Cuartos para que los resultados
  // de Cuartos sigan siendo persistentes en reconstrucciones posteriores.
  const qfRight=copafemBestRightOrder(firsts.slice(),r16W.slice(),r16);
  const swapSources=(a,b)=>{
    if(r16.length<Math.max(a,b)) return;
    const keyA=`W:${r16[a-1].id}`;
    const keyB=`W:${r16[b-1].id}`;
    const iA=qfRight.findIndex(x=>x?.key===keyA);
    const iB=qfRight.findIndex(x=>x?.key===keyB);
    if(iA>=0 && iB>=0){
      const tmp=qfRight[iA]; qfRight[iA]=qfRight[iB]; qfRight[iB]=tmp;
    }
  };
  swapSources(1,3);
  swapSources(2,4);

  const qf=firsts.slice(0,qfRight.length).map((src,i)=>
    copafemMakeMatch(`G2-QF-${i+1}`,'Cuartos',src,qfRight[i],oldG)
  );
  const qfW=qf.map(m=>copafemSource(`W:${m.id}`,winnerId(m)));"""

if old not in s:
    raise SystemExit('No se encontró el armado de Cuartos de Oro de Opción 2')

s=s.replace(old,new,1)
s=s.replace('</body>',f'\n<!-- {MARK} -->\n</body>',1)
p.write_text(s,encoding='utf-8')
print('COPAFEM: Ganadores de Octavos de Oro 1/3 y 2/4 intercambiados en Cuartos')
