"""Prepare generated Tauri Android project from reviewed native platform sources."""
from pathlib import Path
import shutil,xml.etree.ElementTree as ET
exec(Path('scripts/harden-android.py').read_text())
root=Path('src-tauri/gen/android/app/src/main');dest=root/'java/dev/delta/android';dest.mkdir(parents=True,exist_ok=True)
shutil.copytree('android-res', root/'res', dirs_exist_ok=True)
shutil.copytree('app-packages',root/'assets/delta-apps',dirs_exist_ok=True)
for source in Path('android').rglob('*.kt'):
 target=dest/source.relative_to('android');target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
ns='http://schemas.android.com/apk/res/android';a=lambda k:'{'+ns+'}'+k
p=root/'AndroidManifest.xml';tree=ET.parse(p);manifest=tree.getroot();app=manifest.find('application')
app.set(a('label'),'Delta')
app.set(a('icon'),'@mipmap/ic_launcher');app.set(a('roundIcon'),'@mipmap/ic_launcher_round')
for permission in ['INTERNET','FOREGROUND_SERVICE','FOREGROUND_SERVICE_CONNECTED_DEVICE','CHANGE_NETWORK_STATE','POST_NOTIFICATIONS','RECEIVE_BOOT_COMPLETED','REQUEST_INSTALL_PACKAGES']:
 if not any(v.get(a('name'))=='android.permission.'+permission for v in manifest.findall('uses-permission')):ET.SubElement(manifest,'uses-permission',{a('name'):'android.permission.'+permission})
ET.SubElement(app,'service',{a('name'):'.platform.DeltaNodeService',a('exported'):'false',a('foregroundServiceType'):'connectedDevice',a('stopWithTask'):'false'})
r=ET.SubElement(app,'receiver',{a('name'):'.platform.BootReceiver',a('exported'):'false'});f=ET.SubElement(r,'intent-filter');ET.SubElement(f,'action',{a('name'):'android.intent.action.BOOT_COMPLETED'});ET.SubElement(f,'action',{a('name'):'android.intent.action.MY_PACKAGE_REPLACED'})
r=ET.SubElement(app,'receiver',{a('name'):'.platform.UpdateStatusReceiver',a('exported'):'false'});f=ET.SubElement(r,'intent-filter');ET.SubElement(f,'action',{a('name'):'dev.delta.android.UPDATE_STATUS'})
# Android 11+ package visibility: without this resolveActivity() for the installer's confirmation intent returns null.
q=ET.SubElement(manifest,'queries');qi=ET.SubElement(q,'intent');ET.SubElement(qi,'action',{a('name'):'android.content.pm.action.CONFIRM_INSTALL'})
activity=app.find('activity');f=ET.SubElement(activity,'intent-filter');ET.SubElement(f,'action',{a('name'):'android.intent.action.VIEW'})
for c in ['DEFAULT','BROWSABLE']:ET.SubElement(f,'category',{a('name'):'android.intent.category.'+c})
ET.SubElement(f,'data',{a('scheme'):'delta',a('host'):'pair'})
tree.write(p,encoding='utf-8',xml_declaration=True)
p=Path('src-tauri/gen/android/app/build.gradle.kts');s=p.read_text();s+='''
android {
    signingConfigs {
        create("production") {
            storeFile = file(System.getenv("DELTA_KEYSTORE") ?: "missing-release-key")
            storePassword = System.getenv("DELTA_STORE_PASSWORD")
            keyAlias = "delta"
            keyPassword = System.getenv("DELTA_KEY_PASSWORD")
        }
    }
    buildTypes.getByName("release") { signingConfig = signingConfigs.getByName("production") }
}
''';p.write_text(s)
# JNI entrypoints and Keystore classes are accessed by name from native threads.
p=Path('src-tauri/gen/android/app/proguard-rules.pro');p.write_text(p.read_text()+'\n-keep class dev.delta.android.platform.** { *; }\n')
print('Android lifecycle, private storage, deep links and production signing configured')
