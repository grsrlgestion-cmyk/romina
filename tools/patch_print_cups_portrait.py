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
  margin:8mm;
}
@media print{
  body.copafem-print-cups-five .copafem-cups-print-page{
    page:copafemCupsPortrait!important;
    width:100%!important;
    max-width:none!important;
  }
  body.copafem-print-cups-five .copafem-cups-print-page.combo .copafem-cups-print-rounds{
    grid-template-columns:1fr!important;
    gap:3mm!important;
  }
  body.copafem-print-cups-five .copafem-cups-print-head{
    font-size:14pt!important;
    padding:3mm 4mm!important;
  }
  body.copafem-print-cups-five .copafem-cups-print-head small{
    font-size:9pt!important;
  }
  body.copafem-print-cups-five .copafem-cups-print-subtitle{
    font-size:13pt!important;
    margin-bottom:3mm!important;
  }
  body.copafem-print-cups-five .copafem-cups-print-page .round-title{
    font-size:10pt!important;
    padding:1.8mm 2.3mm!important;
  }
  body.copafem-print-cups-five .copafem-cups-print-page .bracket-match{
    margin:1.6mm 0!important;
    padding:1.8mm 2.2mm!important;
  }
  body.copafem-print-cups-five .copafem-cups-print-page .bracket-meta{
    font-size:8pt!important;
    margin-bottom:.8mm!important;
  }
  body.copafem-print-cups-five .copafem-cups-print-page .bracket-team{
    grid-template-columns:minmax(0,1fr) 9mm!important;
    gap:1.5mm!important;
    padding:1mm 0!important;
  }
  body.copafem-print-cups-five .copafem-cups-print-page .bracket-team span{
    font-size:10pt!important;
    line-height:1.2!important;
    font-weight:850!important;
  }
  body.copafem-print-cups-five .copafem-cups-print-page .bracket-team input{
    width:9mm!important;
    min-width:9mm!important;
    height:7.8mm!important;
    font-size:9pt!important;
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
      st.textContent='@page{size:A4 portrait;margin:8mm;}';
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
print('COPAFEM: Oro/Plata en A4 vertical con nombres más grandes')
