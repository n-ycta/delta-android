"""Regenerate legacy launcher PNGs and safe-zone vectors. Requires Pillow.

The mark is 2/3 of the previous size (0.66 -> 0.44 in a 108 viewport).
Canvas/background size and the installed package identity are unchanged.
"""
from pathlib import Path
from PIL import Image, ImageDraw
root = Path(__file__).resolve().parents[1]
for name in ['delta_launcher_foreground', 'delta_launcher_monochrome']:
 p=root/f'android-res/drawable/{name}.xml'
 s=p.read_text().replace('translateX="21"','translateX="32"').replace('translateY="21"','translateY="32"').replace('scaleX="0.66"','scaleX="0.44"').replace('scaleY="0.66"','scaleY="0.44"')
 p.write_text(s)
for density,size in [('mdpi',48),('hdpi',72),('xhdpi',96),('xxhdpi',144),('xxxhdpi',192)]:
 k=size*4/108
 im=Image.new('RGB',(size*4,size*4),'#171824');d=ImageDraw.Draw(im)
 points=[((32+x*.44)*k,(32+y*.44)*k) for x,y in [(66.8,80.25),(8,80.25),(50,7.5),(79.4,58.42)]]
 w=13*.44*k
 d.line(points,fill='#6D5DFC',width=round(w),joint='curve')
 for x,y in points:d.ellipse((x-w/2,y-w/2,x+w/2,y+w/2),fill='#6D5DFC')
 x,y=(32+89*.44)*k,(32+78.25*.44)*k;r=8.06*.44*k
 d.ellipse((x-r,y-r,x+r,y+r),fill='#FF6A3D')
 im=im.resize((size,size),Image.Resampling.LANCZOS)
 im.save(root/f'android-res/mipmap-{density}/ic_launcher.png')
 mask=Image.new('L',(size*4,size*4));ImageDraw.Draw(mask).ellipse((0,0,size*4-1,size*4-1),fill=255)
 rounded=im.convert('RGBA');rounded.putalpha(mask.resize((size,size),Image.Resampling.LANCZOS));rounded.save(root/f'android-res/mipmap-{density}/ic_launcher_round.png')
print('Generated all legacy icons; adaptive and monochrome marks use scale 0.44, centred at 54.')
