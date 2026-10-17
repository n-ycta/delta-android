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
 def test_catalog_is_selected_before_install_and_installed_before_open(self):
  self.assertLess(source.index("tap_label('Catalogue'"),source.index("tap_label('Install'"))
  self.assertLess(source.index("tap_label('Install'"),source.index("tap_label('Established'"))
  self.assertLess(source.index("tap_label('Established'"),source.index("tap_label('Open'"))

if __name__=='__main__':unittest.main()
