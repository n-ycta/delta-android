"""Release APK acceptance on a disposable rooted AOSP emulator, not a physical-device claim."""
import subprocess,time,re,atexit,xml.etree.ElementTree as ET
from pathlib import Path
out=Path('acceptance');out.mkdir(exist_ok=True)
def adb(*a,check=True):
 result=subprocess.run(['adb',*a],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
 if check and result.returncode:
  (out/'adb-error.txt').write_bytes(result.stderr);result.check_returncode()
 return result.stdout
@atexit.register
def diagnostics():
 try:(out/'logcat-final.txt').write_bytes(adb('logcat','-d',check=False))
 except Exception:pass
def dump():
 adb('shell','uiautomator','dump','/sdcard/delta-ui.xml');data=adb('shell','cat','/sdcard/delta-ui.xml');(out/'ui.xml').write_bytes(data);return ET.fromstring(data)
def screen(name): (out/(name+'.png')).write_bytes(adb('exec-out','screencap','-p'))
def start():adb('shell','am','start','-W','-n','dev.delta.android/.MainActivity');time.sleep(12)
assert b'uid=0' in adb('shell','su','0','id'),'Disposable userdebug emulator must permit local root inspection';adb('shell','pm','grant','dev.delta.android','android.permission.POST_NOTIFICATIONS',check=False);adb('logcat','-c');start();screen('home')
# Exercise explicit first-run identity setup through real accessibility clicks.
size=list(map(int,re.findall(r'\d+',adb('shell','wm','size').decode())[-2:]));width,height=size

def tap_node(node):
 coords=list(map(int,re.findall(r'-?\d+',node.get('bounds',''))))
 if len(coords)!=4:return False
 left,top,right,bottom=max(0,coords[0]),max(0,coords[1]),min(width,coords[2]),min(height,coords[3])
 if right<=left or bottom<=top:return False
 adb('shell','input','tap',str((left+right)//2),str((top+bottom)//2));time.sleep(1);return True

def inside_scrollport(node,parents):
 bounds=list(map(int,re.findall(r'-?\d+',node.get('bounds',''))))
 if len(bounds)!=4:return False
 parent=parents.get(node)
 while parent is not None:
  if parent.get('scrollable')=='true':
   clip=list(map(int,re.findall(r'-?\d+',parent.get('bounds',''))))
   if len(clip)==4 and (bounds[0]<clip[0] or bounds[2]>clip[2] or bounds[1]<clip[1]+4 or bounds[3]>clip[3]-12):return False
  parent=parents.get(parent)
 return True

def tap_label(*labels,scroll=False,counted=False,buttons=False):
 for attempt in range(7 if scroll else 3):
  root=dump();parents={child:parent for parent in root.iter() for child in parent}
  for node in root.iter():
   names=[node.get('text',''),node.get('content-desc','')]
   if counted:names=[re.sub(r'\s+\d+$','',name).strip() for name in names]
   if buttons and not node.get('class','').endswith('Button'):continue
   if scroll and not inside_scrollport(node,parents):continue
   if any(name in labels for name in names) and node.get('enabled')!='false' and tap_node(node):return
  if scroll:adb('shell','input','swipe',str(width//2),str(height*3//4),str(width//2),str(height//3),'400')
  time.sleep(1)
 raise AssertionError('Accessible action not found: '+str(labels))

# WebView publishes its virtual accessibility tree asynchronously after UiAutomation connects.
for attempt in range(20):
 root=dump();texts=' '.join(n.get('text','')+' '+n.get('content-desc','') for n in root.iter())
 if 'Set up Delta' in texts or 'Настройка Delta' in texts:break
 adb('shell','input','tap',str(width//2),'150');time.sleep(2)
assert 'Set up Delta' in texts or 'Настройка Delta' in texts,'Fresh install must show explicit onboarding'
name=next((n for n in root.iter() if n.get('class')=='android.widget.EditText'),None)
assert name is not None and tap_node(name),'Identity name input must be accessible'
adb('shell','input','text','Emulator-owner');adb('shell','input','keyevent','KEYCODE_BACK')
tap_label('Generate','Сгенерировать')
tap_label('I saved the recovery phrase','Я сохранил seed-фразу',scroll=True)
tap_label('Create','Создать',scroll=True);time.sleep(6)
# No recovery phrase is included in captured acceptance screenshots/log output.
screen('onboarded')
for label in ['Plugins','Nodes','Settings']:
 tap_label('menu','меню');tap_label(label,{'Plugins':'Плагины','Nodes':'Узлы','Settings':'Настройки'}[label],scroll=True);time.sleep(2)
 activity=adb('shell','dumpsys','activity','activities').decode(errors='replace')
 resumed=' '.join(line for line in activity.splitlines() if 'mResumedActivity' in line or 'topResumedActivity' in line)
 assert 'dev.delta.android' in resumed,'Internal menu click escaped to an external application: '+label
screen('internal-navigation')
# The reviewed static Media package installs offline on Android with no Node process.
tap_label('menu','меню');tap_label('Plugins','Плагины',scroll=True)
tap_label('Catalogue','Catalog','Каталог',counted=True)
tap_label('Install','Установить',scroll=True)
# Observe the real installer instead of mistaking an off-screen click for success.
for attempt in range(30):
 installed=adb('shell','su','0','ls','/data/data/dev.delta.android/apps/dev.delta.media/index.html',check=False)
 if b'index.html' in installed:break
 time.sleep(2)
else:
 screen('media-install-failed');root=dump()
 raise AssertionError('Media installation did not produce the reviewed app assets: '+' '.join(n.get('text','') for n in root.iter()))
screen('media-install-complete')
tap_label('Established','Installed','Установленные',counted=True)
for attempt in range(20):
 root=dump();texts=' '.join(n.get('text','')+' '+n.get('content-desc','') for n in root.iter())
 if 'Interface' in texts or 'Интерфейс' in texts or 'Open' in texts or 'Открыть' in texts:break
 time.sleep(2)
tap_label('Interface','Интерфейс','Open','Открыть',scroll=True,buttons=True)
for attempt in range(20):
 root=dump();texts=' '.join(n.get('text','')+' '+n.get('content-desc','') for n in root.iter())
 if ('Library' in texts or 'Медиатека' in texts) and ('Import' in texts or 'Импорт' in texts):break
 time.sleep(2)
screen('media-installed')
assert ('Library' in texts or 'Медиатека' in texts) and ('Import' in texts or 'Импорт' in texts),'Installed Media must render in its isolated app-origin inside APK'
assets=adb('shell','su','0','ls','/data/data/dev.delta.android/apps/dev.delta.media').split()
assert b'index.html' in assets and b'node' not in assets,'Portable app must contain browser assets, not a Node runtime'
tap_label('Library','Медиатека');screen('media-library')
tap_label('Console','Консоль');time.sleep(3)


profile='/data/data/dev.delta.android/files/node/config.json'
before=adb('exec-out','su','0','cat',profile)
assert before.startswith(b'DLC1'),'Profile must be Keystore-encrypted'
assert b'node_id' not in before and b'root_token' not in before,'No plaintext identity/credentials'
# A complete invitation deep link only prefills fields, never auto-joins.
adb('shell','am','start','-W','-a','android.intent.action.VIEW','-d',"'delta://pair?url=https%3A%2F%2Fexample.invalid&code=smoke'",'dev.delta.android');time.sleep(5)
screen('pairing')
for attempt in range(10):
 root=dump();texts=' '.join(n.get('text','')+' '+n.get('content-desc','') for n in root.iter())
 if 'Native connection' in texts or 'Нативное подключение' in texts:break
 time.sleep(2)
assert 'Native connection' in texts or 'Нативное подключение' in texts,'Native settings must render after a pairing link'
boxes=[n for n in root.iter() if n.get('checkable')=='true' or n.get('text') in ['Background service','Фоновая служба'] or n.get('content-desc') in ['Background service','Фоновая служба']]
assert boxes,'Background service switch must be accessible'
b=boxes[0];coords=list(map(int,re.findall(r'\d+',b.get('bounds',''))));assert len(coords)==4
if b.get('checked')!='true':adb('shell','input','tap',str((coords[0]+coords[2])//2),str((coords[1]+coords[3])//2))
time.sleep(5);services=adb('shell','dumpsys','activity','services','dev.delta.android').decode();assert 'DeltaNodeService' in services,'Foreground service must start from explicit UI opt-in'
adb('shell','input','keyevent','KEYCODE_HOME');time.sleep(5);assert 'DeltaNodeService' in adb('shell','dumpsys','activity','services','dev.delta.android').decode(),'Service must survive hiding Activity'
start();screen('restored');adb('shell','su','0','am','startservice','-n','dev.delta.android/.platform.DeltaNodeService','-a','stop');time.sleep(5);adb('shell','input','keyevent','KEYCODE_HOME');start();assert adb('exec-out','su','0','cat',profile)==before,'Stopping the service must release its profile lease for restart';adb('shell','am','force-stop','dev.delta.android');start();after=adb('exec-out','su','0','cat',profile);assert before==after,'A user restart must preserve the encrypted node identity/profile'
logs=adb('logcat','-d').decode(errors='replace');(out/'logcat.txt').write_text(logs)
assert 'FATAL EXCEPTION' not in logs and 'Fatal signal' not in logs,'Native process must not crash'
(out/'result.txt').write_text('PASS: explicit key onboarding, internal menu clicks stay in APK, offline portable Media installation and embedded navigation, release startup, Keystore ciphertext, explicit background service, Activity background and user restart with persistent profile. Emulator only; no battery/physical-device guarantee.\n')
print((out/'result.txt').read_text())
