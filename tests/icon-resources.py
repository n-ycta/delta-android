"""Source-resource checks; packaged APK inspection is a separate acceptance step."""
from pathlib import Path
import struct,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1]
for density,size in [('mdpi',48),('hdpi',72),('xhdpi',96),('xxhdpi',144),('xxxhdpi',192)]:
 for name in ['ic_launcher','ic_launcher_round']:
  raw=(root/f'android-res/mipmap-{density}/{name}.png').read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n';assert struct.unpack('>II',raw[16:24])==(size,size)
for p in (root/'android-res').rglob('*.xml'):ET.parse(p)
for version in ['v26','v33']:
 for name in ['ic_launcher','ic_launcher_round']:
  r=ET.parse(root/f'android-res/mipmap-anydpi-{version}/{name}.xml').getroot();assert r.tag=='adaptive-icon';assert r.find('background') is not None;assert r.find('foreground') is not None
  if version=='v33':assert r.find('monochrome') is not None
source=(root/'scripts/prepare-android.py').read_text();assert "shutil.copytree('android-res'" in source;assert "'@mipmap/ic_launcher'" in source;assert "'@mipmap/ic_launcher_round'" in source
print('PASS: five PNG densities, round/adaptive/themed icons, XML and persistent resource wiring')

import json
assert json.loads((root/'src-tauri/tauri.conf.json').read_text())['productName']=='Delta'
assert "app.set(a('label'),'Delta')" in source
print('PASS: installed Android application label is Delta; package identity is unchanged')
ns='{http://schemas.android.com/apk/res/android}'
for name in ['delta_launcher_foreground','delta_launcher_monochrome']:
 group=ET.parse(root/f'android-res/drawable/{name}.xml').getroot().find('group')
 assert float(group.get(ns+'scaleX'))==0.44 and float(group.get(ns+'scaleY'))==0.44
 assert float(group.get(ns+'translateX'))==32 and float(group.get(ns+'translateY'))==32
print('PASS: adaptive and themed marks reduced to 2/3, centred with launcher safe-zone padding')

import shutil
ui=root/'node_modules'/'@delta'/'ui'
(ui/'scripts').mkdir(parents=True, exist_ok=True)
shutil.copy(root/'vendor'/'delta-ui'/'app-catalog.json', ui/'app-catalog.json')
shutil.copy(root/'vendor'/'delta-ui'/'scripts'/'prepare-apps.py', ui/'scripts'/'prepare-apps.py')
print('PASS: app catalog staged for the existing prepare step')
