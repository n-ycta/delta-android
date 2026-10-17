"""Exercise counted Android accessibility tabs without starting an emulator."""
import ast,re,unittest,xml.etree.ElementTree as ET
from pathlib import Path

source=(Path(__file__).parent/'emulator-smoke.py').read_text()
function=next(node for node in ast.parse(source).body if isinstance(node,ast.FunctionDef) and node.name=='tap_label')

class CountedTabs(unittest.TestCase):
 def test_catalog_and_installed_tabs_with_counts(self):
  for name,labels in [('Catalogue 1',('Catalogue','Каталог')),('Каталог 1',('Catalogue','Каталог')),('Established 0',('Established','Installed','Установленные')),('Установленные 12',('Established','Installed','Установленные'))]:
   node=ET.Element('node',{'text':name,'enabled':'true'});root=ET.Element('root');root.append(node);tapped=[]
   context={'dump':lambda:root,'tap_node':lambda n:tapped.append(n) or True,'re':re}
   exec(compile(ast.Module(body=[function],type_ignores=[]),'<tap_label>','exec'),context)
   context['tap_label'](*labels,counted=True)
   self.assertEqual(tapped,[node])
 def test_taps_reject_offscreen_nodes_and_clip_partial_bounds(self):
  node_function=next(node for node in ast.parse(source).body if isinstance(node,ast.FunctionDef) and node.name=='tap_node')
  taps=[]
  context={'re':re,'width':320,'height':640,'adb':lambda *args:taps.append(args),'time':type('Clock',(),{'sleep':staticmethod(lambda _:None)})}
  exec(compile(ast.Module(body=[node_function],type_ignores=[]),'<tap_node>','exec'),context)
  for bounds in ['[0][700][100][800]','[-100][0][-1][30]','[400][0][500][30]']:
   self.assertFalse(context['tap_node'](ET.Element('node',{'bounds':bounds})))
  self.assertEqual(taps,[])
  self.assertTrue(context['tap_node'](ET.Element('node',{'bounds':'[-20][620][100][700]'})))
  self.assertEqual(taps[-1],('shell','input','tap','50','630'))
 def test_clipped_button_scrolls_instead_of_tapping_scrollbar(self):
  helper=next(node for node in ast.parse(source).body if isinstance(node,ast.FunctionDef) and node.name=='inside_scrollport')
  context={'re':re}
  exec(compile(ast.Module(body=[helper],type_ignores=[]),'<inside_scrollport>','exec'),context)
  viewport=ET.Element('node',{'scrollable':'true','bounds':'[0,187][320,558]'})
  button=ET.SubElement(viewport,'node',{'bounds':'[29,538][319,570]'})
  self.assertFalse(context['inside_scrollport'](button,{button:viewport}))
  button.set('bounds','[29,400][319,432]')
  self.assertTrue(context['inside_scrollport'](button,{button:viewport}))
 def test_catalog_is_selected_before_install_and_installed_before_open(self):
  self.assertLess(source.index("tap_label('Catalogue'"),source.index("tap_label('Install'"))
  self.assertLess(source.index("tap_label('Install'"),source.index("tap_label('Established'"))
  self.assertLess(source.index("tap_label('Established'"),source.index("tap_label('Interface'"))

if __name__=='__main__':unittest.main()
