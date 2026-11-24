import json,pathlib
D=pathlib.Path(__file__).resolve().parent
data=json.load(open(D/'data/samflix.json'))
bf=D/'data/bioflix.json'
if bf.exists(): data['bioflix']=json.load(open(bf))
s=json.dumps(data,ensure_ascii=False).replace('</','<\\/')
(D/'index.html').write_text((D/'template.html').read_text().replace('__DATA__',s),encoding='utf-8')
import base64,glob
imgs={'assets/bioflix/'+pathlib.Path(f).name:'data:image/jpeg;base64,'+base64.b64encode(open(f,'rb').read()).decode() for f in sorted(glob.glob(str(D/'assets/bioflix/*.jpg')))}
(D/'assets/bioflix-covers.js').write_text('window.BFIMG='+json.dumps(imgs)+';')
print('ok',len(s),'covers.js',len(imgs))
