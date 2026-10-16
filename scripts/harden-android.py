"""Disable profile backups in the generated Android host. No secrets or user files involved."""
from pathlib import Path
import xml.etree.ElementTree as ET
root = Path('src-tauri/gen/android/app/src/main')
manifest = root / 'AndroidManifest.xml'
ns = 'http://schemas.android.com/apk/res/android'
ET.register_namespace('android', ns)
tree = ET.parse(manifest)
app = tree.getroot().find('application')
if app is None:
    raise SystemExit('Missing Android application manifest')
for key, value in {'allowBackup':'false', 'fullBackupContent':'false', 'dataExtractionRules':'@xml/data_extraction_rules'}.items():
    app.set('{'+ns+'}'+key,value)
tree.write(manifest,encoding='utf-8',xml_declaration=True)
resources = root / 'res/xml'
resources.mkdir(parents=True,exist_ok=True)
rules=ET.Element('data-extraction-rules')
for kind in ['cloud-backup','device-transfer']:
    branch=ET.SubElement(rules,kind)
    for domain in ['root','file','database','sharedpref','external']:
        ET.SubElement(branch,'exclude',{'domain':domain,'path':'.'})
ET.ElementTree(rules).write(resources/'data_extraction_rules.xml',encoding='utf-8',xml_declaration=True)
assert app.get('{'+ns+'}allowBackup')=='false'
print('Android private profile backup/transfer exclusions applied')
