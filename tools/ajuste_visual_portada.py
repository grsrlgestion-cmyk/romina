from pathlib import Path

p=Path('index.html')
text=p.read_text(encoding='utf-8')

old="https://afpcourts.com/wp-content/uploads/Marita_Bendinat_adidas_Panoramic_AFP-scaled.jpg"
new="https://tennis.scene7.com/is/image/dtbtennis/_justus.fotos-20250627-DSC01296?dpr=off&qlt=90&ts=1761989488450"
text=text.replace(old,new)

# Ajustes para que la portada entre mejor en una pantalla de escritorio.
text=text.replace('.cp-logo-wrap{height:150px;', '.cp-logo-wrap{height:132px;')
text=text.replace('.cp-logo{width:190px;height:190px;', '.cp-logo{width:165px;height:165px;')
text=text.replace('height:min(510px,57svh);min-height:410px;', 'height:min(470px,55svh);min-height:380px;')
text=text.replace('background-position:center 39%;', 'background-position:center 45%;')

p.write_text(text,encoding='utf-8')
print('Ajuste visual final aplicado')
