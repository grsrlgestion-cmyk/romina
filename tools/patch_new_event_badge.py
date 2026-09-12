from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='COPAFEM_NEW_EVENT_BADGE_SYNC_V1'
if MARK in s:
    print('new-event badge already synced')
    raise SystemExit

old='''  function syncNewEventCategoryTheme(){
    const form=$("newEventForm"); if(!form)return;
    const cat=$("newEventCategory")?.value||'7ma';
    const c=CATEGORY_COLORS[cat]||CATEGORY_COLORS['7ma'];
    form.style.setProperty('--new-event-cat',c.main);
    form.style.setProperty('--new-event-cat-soft',c.soft);
    form.style.setProperty('--new-event-cat-ink',c.ink);
  }'''
new='''  function syncNewEventCategoryTheme(){
    const form=$("newEventForm"); if(!form)return;
    const cat=$("newEventCategory")?.value||'7ma';
    const c=CATEGORY_COLORS[cat]||CATEGORY_COLORS['7ma'];
    form.style.setProperty('--new-event-cat',c.main);
    form.style.setProperty('--new-event-cat-soft',c.soft);
    form.style.setProperty('--new-event-cat-ink',c.ink);
    const badge=$("activeEventBadge");
    if(badge){
      badge.textContent=cat;
      badge.style.background=c.main;
      badge.style.color='#fff';
      badge.style.boxShadow=`0 6px 18px ${c.main}33`;
    }
  }'''
if old not in s:
    raise SystemExit('No se encontró syncNewEventCategoryTheme')
s=s.replace(old,new,1)

old_header='''    $("heroCategory").textContent=state.tournament.category||"—"; $("dropCategoryBadge").textContent=state.tournament.category||"—"; $("activeEventBadge").textContent=state.tournament.category||"—";'''
new_header='''    $("heroCategory").textContent=state.tournament.category||"—"; $("dropCategoryBadge").textContent=state.tournament.category||"—"; $("activeEventBadge").textContent=state.tournament.category||"—"; syncNewEventCategoryTheme();'''
if old_header not in s:
    raise SystemExit('No se encontró renderHeader esperado')
s=s.replace(old_header,new_header,1)

marker='''\n<script id="COPAFEM_NEW_EVENT_BADGE_SYNC_V1">window.COPAFEM_NEW_EVENT_BADGE_SYNC=true;</script>\n'''
head,tail=s.rsplit('</body>',1)
s=head+marker+'\n</body>'+tail
p.write_text(s,encoding='utf-8')
print('COPAFEM: badge de alta sincronizado con categoría elegida')
