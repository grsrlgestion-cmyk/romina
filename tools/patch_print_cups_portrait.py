from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_PRINT_CUPS_PORTRAIT_V1'
if MARK in s:
    print('cups portrait print already applied')
    raise SystemExit

patch=r'''
<style id="COPAFEM_PRINT_CUPS_PORTRAIT_V1">
@page copafemCupsPortrait{
  size:A4 portrait;
  margin:7mm;
}
@media print{
  body.copafem-print-cups-five .copafem-cups-print-page{
    page:copafemCupsPortrait!important;
    box-sizing:border-box!important;
    width:100%!important;
    max-width:190mm!important;
    min-height:270mm!important;
    margin:0 auto!important;
    padding:3mm 0!important;
    display:flex!important;
    flex-direction:column!important;
    justify-content:center!important;
  }
  body.copafem-print-cups-five .copafem-cups-print-head{
    position:relative!important;
    display:flex!important;
    justify-content:center!important;
    align-items:center!important;
    min-height:14mm!important;
    margin:0 0 5mm!important;
    padding:3.5mm 18mm!important;
    font-size:18pt!important;
    line-height:1.15!important;
    text-align:center!important;
  }
  body.copafem-print-cups-five .copafem-cups-print-head small{
    position:absolute!important;
    right:4mm!important;
    top:50%!important;
    transform:translateY(-50%)!important;
    font-size:10.5pt!important;
  }
  body.copafem-print-cups-five .copafem-cups-print-subtitle{
    font-size:17pt!important;
    line-height:1.15!important;
    text-align:center!important;
    margin:0 0 5mm!important;
  }
  body.copafem-print-cups-five .copafem-cups-print-rounds,
  body.copafem-print-cups-five .copafem-cups-print-page.combo .copafem-cups-print-rounds{
    flex:1 1 auto!important;
    display:flex!important;
    flex-direction:column!important;
    justify-content:space-evenly!important;
    gap:5mm!important;
    width:100%!important;
    margin:0 auto!important;
  }
  body.copafem-print-cups-five .copafem-cups-print-page .round{
    flex:1 1 0!important;
    display:flex!important;
    flex-direction:column!important;
    justify-content:center!important;
    gap:3mm!important;
    width:100%!important;
    margin:0!important;
  }
  body.copafem-print-cups-five .copafem-cups-print-page .round-title{
    font-size:13.5pt!important;
    line-height:1.15!important;
    padding:2.4mm 3mm!important;
    margin:0 0 1mm!important;
    text-align:center!important;
  }
  body.copafem-print-cups-five .copafem-cups-print-page .bracket-match{
    width:100%!important;
    box-sizing:border-box!important;
    margin:0!important;
    padding:3mm 4mm!important;
    min-height:24mm!important;
    display:flex!important;
    flex-direction:column!important;
    justify-content:center!important;
    border-width:1.2px!important;
    border-radius:3mm!important;
  }
  body.copafem-print-cups-five .copafem-cups-print-page .bracket-meta{
    font-size:10.5pt!important;
    line-height:1.2!important;
    margin:0 0 1.5mm!important;
    text-align:center!important;
  }
  body.copafem-print-cups-five .copafem-cups-print-page .bracket-team{
    grid-template-columns:minmax(0,1fr) 12mm!important;
    gap:2mm!important;
    align-items:center!important;
    padding:1.5mm 0!important;
  }
  body.copafem-print-cups-five .copafem-cups-print-page .bracket-team span{
    font-size:13pt!important;
    line-height:1.25!important;
    font-weight:900!important;
    text-align:center!important;
    white-space:normal!important;
    overflow:visible!important;
    text-overflow:clip!important;
  }
  body.copafem-print-cups-five .copafem-cups-print-page .bracket-team input{
    width:12mm!important;
    min-width:12mm!important;
    height:10mm!important;
    padding:1mm!important;
    font-size:11.5pt!important;
    font-weight:800!important;
  }
}
</style>
<script>
(() => {
  const STYLE_ID='copafem-cups-runtime-portrait-page';
  function isCups(){return document.getElementById('view-copas')?.classList.contains('active');}
  function addPortraitPage(){
    if(!isCups()) return;
    let st=document.getElementById(STYLE_ID);
    if(!st){
      st=document.createElement('style');
      st.id=STYLE_ID;
      st.textContent='@page{size:A4 portrait;margin:7mm;}';
      document.head.appendChild(st);
    }
  }
  function removePortraitPage(){document.getElementById(STYLE_ID)?.remove();}
  window.addEventListener('beforeprint',addPortraitPage);
  window.addEventListener('afterprint',removePortraitPage);
  document.addEventListener('click',e=>{
    if(e.target?.id==='printBtn' && isCups()) addPortraitPage();
  },true);
})();
</script>
'''

if '</body>' not in s:
    raise SystemExit('No se encontró </body>')
head,tail=s.rsplit('</body>',1)
s=head+patch+'\n<!-- '+MARK+' -->\n</body>'+tail
p.write_text(s,encoding='utf-8')
print('COPAFEM: Oro/Plata A4 vertical grande, centrado y aprovechando la hoja')
