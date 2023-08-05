from ctypes import windll
from accessible_output import paths
import win32gui

from main import OutputError, ScreenreaderSpeechOutput

class Jaws (ScreenreaderSpeechOutput):
 """Speech output supporting the Jaws for Windows screen reader."""
 def __init__(self, *args, **kwargs):
  super (Jaws, self).__init__(*args, **kwargs)
  try:
   self.dll = windll.LoadLibrary(paths.root('lib\\jfwapi.dll'))
  except:
   raise OutputError

 def speak(self, text, interrupt=False):
  self.dll.JFWSayString(text.encode('windows-1252'), interrupt)

 def canSpeak(self):
  try:
   return win32gui.FindWindow("JFWUI2", "JAWS") != 0 and super(Jaws, self).canSpeak()
  except:
   return False

