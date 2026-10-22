"""Stage checksum-pinned app packages from this repo catalog."""
from pathlib import Path
import urllib.request,hashlib,json
here=Path(__file__).resolve().parent
catalog=json.loads(next(x for x in (here/'app-catalog.json', here.parent/'app-catalog.json') if x.exists()).read_text(encoding='utf-8'))
target=Path('app-packages');target.mkdir(exist_ok=True)
for app in catalog:
 url=app['asset'];assert url.startswith('https://github.com/n-ycta/') and '/releases/download/' in url
 with urllib.request.urlopen(url,timeout=120) as response:
  data=response.read(16*1024*1024+1)
 assert len(data)<=16*1024*1024 and hashlib.sha256(data).hexdigest()==app['sha256'],'App package checksum mismatch'
 (target/(app['id']+'.delta-app')).write_bytes(data)
print('Verified portable app packages:',len(catalog))
