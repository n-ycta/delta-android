"""Release APK acceptance on a disposable rooted AOSP emulator, not a physical-device claim."""
import subprocess,time,re,xml.etree.ElementTree as ET
from pathlib import Path
out=Path('acceptance');out.mkdir(exist_ok=True)
def adb(*a,check=True):return subprocess.run(['adb',*a],check=check,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout
def dump():
 adb('shell','uiautomator','dump','/sdcard/delta-ui.xml');data=adb('shell','cat','/sdcard/delta-ui.xml');(out/'ui.xml').write_bytes(data);return ET.fromstring(data)
def screen(name): (out/(name+'.png')).write_bytes(adb('exec-out','screencap','-p'))
def start():adb('shell','am','start','-W','-n','dev.delta.android/.MainActivity');time.sleep(12)
adb('root');time.sleep(3);adb('wait-for-device');adb('shell','pm','grant','dev.delta.android','android.permission.POST_NOTIFICATIONS',check=False);adb('logcat','-c');start();screen('home')
profile='/data/data/dev.delta.android/files/node/config.json'
before=adb('exec-out','cat',profile)
assert before.startswith(b'DLC1'),'Profile must be Keystore-encrypted'
assert b'node_id' not in before and b'root_token' not in before,'No plaintext identity/credentials'
# A complete invitation deep link only prefills fields, never auto-joins.
adb('shell','am','start','-W','-a','android.intent.action.VIEW','-d',"'delta://pair?url=https%3A%2F%2Fexample.invalid&code=smoke'",'dev.delta.android');time.sleep(5)
root=dump();texts=' '.join(n.get('text','')+' '+n.get('content-desc','') for n in root.iter())
assert 'Native connection' in texts or 'Нативное подключение' in texts,'Native settings must render after a pairing link'
boxes=[n for n in root.iter() if n.get('checkable')=='true' or n.get('text') in ['Background service','Фоновая служба'] or n.get('content-desc') in ['Background service','Фоновая служба']]
assert boxes,'Background service switch must be accessible'
b=boxes[0];coords=list(map(int,re.findall(r'\d+',b.get('bounds',''))));assert len(coords)==4
if b.get('checked')!='true':adb('shell','input','tap',str((coords[0]+coords[2])//2),str((coords[1]+coords[3])//2))
time.sleep(5);services=adb('shell','dumpsys','activity','services','dev.delta.android').decode();assert 'DeltaNodeService' in services,'Foreground service must start from explicit UI opt-in'
adb('shell','input','keyevent','KEYCODE_HOME');time.sleep(5);assert 'DeltaNodeService' in adb('shell','dumpsys','activity','services','dev.delta.android').decode(),'Service must survive hiding Activity'
start();screen('restored');adb('shell','am','startservice','-n','dev.delta.android/.platform.DeltaNodeService','-a','stop');time.sleep(5);adb('shell','input','keyevent','KEYCODE_HOME');start();assert adb('exec-out','cat',profile)==before,'Stopping the service must release its profile lease for restart';adb('shell','am','force-stop','dev.delta.android');start();after=adb('exec-out','cat',profile);assert before==after,'A user restart must preserve the encrypted node identity/profile'
logs=adb('logcat','-d').decode(errors='replace');(out/'logcat.txt').write_text(logs)
assert 'FATAL EXCEPTION' not in logs and 'Fatal signal' not in logs,'Native process must not crash'
(out/'result.txt').write_text('PASS: release startup, Keystore ciphertext, explicit background service, Activity background and user restart with persistent profile. Emulator only; no battery/physical-device guarantee.\n')
print((out/'result.txt').read_text())
