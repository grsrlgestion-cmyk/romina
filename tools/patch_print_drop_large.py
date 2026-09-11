from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

MARKER = 'COPAFEM_PRINT_DROP_LARGE_V1'
if MARKER in s:
    print('large print drop already applied')
    raise SystemExit

css = r'''
<style id="COPAFEM_PRINT_DROP_LARGE_V1">
@page{size:A4 landscape;margin:4mm}
@media print{
  #view-drop.active .drop-scroll{
    width:100%!important;
    border:0!important;
    padding:0!important;
    margin:0!important;
    overflow:visible!important;
  }
  #view-drop.active .drop-canvas{
    transform:scale(.49)!important;
    transform-origin:top left!important;
    width:2220px!important;
    margin:0!important;
  }
  #view-drop.active .drop-category-sheet{
    break-after:page;
    page-break-after:always;
    box-shadow:none!important;
  }
  #view-drop.active .drop-category-sheet:last-child{
    break-after:auto;
    page-break-after:auto;
  }
}
</style>
'''

head, tail = s.rsplit('</body>', 1)
s = head + css + '\n</body>' + tail
p.write_text(s, encoding='utf-8')
print('COPAFEM large print drop patch OK')
