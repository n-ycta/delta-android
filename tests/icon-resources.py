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
