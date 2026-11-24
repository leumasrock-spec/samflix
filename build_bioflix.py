#!/usr/bin/env python3
"""Extrai o catálogo do BioFlix (https://bioflix.vercel.app/) -> data/bioflix.json + capas em assets/bioflix/.
Requer node e Pillow. Uso: python3 build_bioflix.py"""
import json,base64,io,re,subprocess,urllib.request,pathlib
from PIL import Image
D=pathlib.Path(__file__).resolve().parent; A=D/'assets/bioflix'; A.mkdir(parents=True,exist_ok=True)
html=urllib.request.urlopen(urllib.request.Request('https://bioflix.vercel.app/',headers={'User-Agent':'Mozilla/5.0'})).read().decode('utf8')
a=html.find('const V = {'); b=html.find('CATALOGO.forEach(i => { if(!i.imagem && CAPAS[i.id])')
f=html.find('const FUNDOS',b); g=html.find('};',f)+2
js=html[a:b]+html[f:g]+"\nprocess.stdout.write(JSON.stringify({CATALOGO,CAPAS,FUNDOS}));"
d=json.loads(subprocess.run(['node','-'],input=js,capture_output=True,text=True,check=True).stdout)
def save(uri,path,w):
    im=Image.open(io.BytesIO(base64.b64decode(uri.split(',',1)[1]))).convert('RGB')
    im.thumbnail((w,10000)); im.save(path,'JPEG',quality=78,optimize=True,progressive=True)
def yid(src):
    s=base64.b64decode(src[4:]).decode() if src.startswith('b64:') else src
    m=re.search(r'(?:v=|youtu\.be/|embed/|shorts/)([\w-]{11})',s); return m.group(1) if m else s
def oembed(v):
    try:
        j=json.load(urllib.request.urlopen(f'https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={v}&format=json',timeout=15)); return j['title'],j['author_name']
    except Exception: return None,None
areas={}; skipped=[]
for c in d['CATALOGO']:
    poster=f"assets/bioflix/{c['id']}.jpg" if c['id'] in d['CAPAS'] else None
    if poster: save(d['CAPAS'][c['id']],D/poster,240)
    fundo=f"assets/bioflix/{c['id']}-banner.jpg" if c['id'] in d['FUNDOS'] else None
    if fundo: save(d['FUNDOS'][c['id']],D/fundo,960)
    eps=c.get('episodios') or [{'titulo':c['titulo'],'video':c.get('video') or {}}]
    for e in eps:
        src=(e.get('video') or {}).get('src','')
        if not src: skipped.append(c['titulo']+' (sem vídeo)'); continue
        v=yid(src); yt,ch=oembed(v)
        if not yt: skipped.append(f"{c['titulo']} – {e['titulo']} ({v}) indisponível"); continue
        t=c['titulo'] if len(eps)==1 else f"{c['titulo']} · {e['titulo']}"
        areas.setdefault(c['area'],[]).append({'id':v,'t':t,'c':ch,'yt':yt,'sin':c.get('sinopse',''),'poster':poster,'banner':fundo,'dest':c.get('destaque')})
ICON={'Corpo Humano':'🫀','Genética e Evolução':'🧬','Ecologia':'🌎','Célula':'🔬','Botânica':'🌿','Microbiologia':'🦠'}
cats=[{'slug':'bf-'+re.sub(r'[^a-z]+','-',k.lower().encode('ascii','ignore').decode()).strip('-'),'label':k,'icon':ICON.get(k,'🎬'),'videos':v} for k,v in sorted(areas.items(),key=lambda x:-len(x[1]))]
# links do PDF "Bioflix" (Drive, arquivo cmiejvodc...pdf): bioflix.vercel.app + pasta do Drive (já presente em Material de apoio)
out={'site':'https://bioflix.vercel.app/','pdf_links':['https://bioflix.vercel.app/','https://drive.google.com/drive/folders/1-ftb5iARJTQP5Y9_-Ob9g28iiO4E7L3J?usp=sharing'],'cats':cats,'skipped':skipped}
json.dump(out,open(D/'data/bioflix.json','w'),ensure_ascii=False,indent=1)
for c in cats: print(c['label'],len(c['videos']))
print('total',sum(len(c['videos']) for c in cats),'titulos',len(d['CATALOGO']),'pulados',skipped)
