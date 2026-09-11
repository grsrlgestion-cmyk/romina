from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARKER='COPAFEM_DROP_ZONES_TWO_COLUMNS_V1'
if MARKER in s:
    print('drop zones two columns already applied')
    raise SystemExit

style=r'''
<style id="COPAFEM_DROP_ZONES_TWO_COLUMNS_V1">
@media screen{
  /* Más ancho para las zonas: A-B / C-D / E-F / G-H */
  #view-drop .drop-canvas{
    width:2500px!important;
  }
  #view-drop .drop-category-sheet{
    width:2484px!important;
    grid-template-columns:220px 1120px 1080px!important;
  }
  #view-drop .drop-zones-area{
    display:grid!important;
    grid-template-columns:repeat(2,minmax(0,1fr))!important;
    grid-auto-flow:row!important;
    gap:14px!important;
    align-content:start!important;
  }
  #view-drop .drop-zone{
    min-width:0!important;
    width:100%!important;
  }
  #view-drop .drop-zone-pair{
    grid-template-columns:48px minmax(0,1fr)!important;
    font-size:10px!important;
  }
  #view-drop .drop-zone-pair span{
    font-size:10px!important;
    white-space:nowrap!important;
    overflow:hidden!important;
    text-overflow:ellipsis!important;
  }
  #view-drop .drop-match-row{
    grid-template-columns:minmax(0,1fr) 54px 50px minmax(0,1fr) 44px!important;
    font-size:8.5px!important;
  }
  #view-drop .drop-match-row .dm-team{
    grid-template-columns:30px minmax(0,1fr)!important;
  }
  #view-drop .drop-match-row .dm-name,
  #view-drop .drop-stand-team .dm-name{
    font-size:8.5px!important;
  }
  #view-drop .drop-stand-row{
    grid-template-columns:20px minmax(0,1fr) 30px 34px!important;
    font-size:8.5px!important;
  }
}
</style>
'''

head,tail=s.rsplit('</body>',1)
s=head+style+'\n</body>'+tail
p.write_text(s,encoding='utf-8')
print('COPAFEM Drop zones two-column wide layout OK')
