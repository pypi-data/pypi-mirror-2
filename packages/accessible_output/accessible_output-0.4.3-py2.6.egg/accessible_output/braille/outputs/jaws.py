import win32com.client
import win32gui

from main import OutputError, BrailleOutput

class Jaws (BrailleOutput):
 """Braille output supporting the Jaws for Windows screen reader."""

 def __init__(self, *args, **kwargs):
  try:
   self.dll = windll.LoadLibrary(paths.root('lib\\jfwapi.dll'))
  except:
   raise OutputError

 def braille(self, text, interrupt=False):
  # HACK: replace " with ', Jaws doesn't seem to understand escaping them with \
  text = text.replace('"', "'")
  self.dll.JFWRunFunction("BrailleString(\"%s\")" % text.encode('windows-1252'))

 def canBraille(self):
  try:
   return win32gui.FindWindow("JFWUI2", "JAWS") != 0 and super(Jaws, self).canBraille()
  except:
   return False
