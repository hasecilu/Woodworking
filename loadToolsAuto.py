# This tool gets "Tools" array from file loadToolsSettings.py and 
# generate loadTools.py file. 
# This should be run only once if you added new macro.
# There is no need to run it ad each workbench startup.

import loadToolsSettings

arr = loadToolsSettings.Tools
output = '''# This file has been automatically generated by the loadToolsAuto.py script. Don't change it here.

import FreeCADGui

import os, sys
import fakemodule
path = os.path.dirname(fakemodule.__file__)
iconPath = os.path.join(path, "Icons")

'''

# ######################################################################################################################
# Create Classes
# ######################################################################################################################

i = 0
while i < len(arr):

	output += '''

# ######################################################################################################################
class '''+arr[i+2]+'''():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "'''+arr[i]+'''.xpm"),
				"Accel"   : "",
				"MenuText": "'''+arr[i+3]+'''",
				"ToolTip" : "'''+arr[i+4]+'''"}

	def Activated(self):

		import os, sys
		import fakemodule

		modulePath = sys.path
		
		module = "'''+arr[i]+'''"
		
		path = os.path.dirname(fakemodule.__file__)
		path = os.path.join(path, "Tools")
		'''

	if arr[i+1] != "":
		output += '''path = os.path.join(path, "'''+arr[i+1]+'''")'''

	output += '''
		sys.path.append(path)

		if module in sys.modules:
			del sys.modules[module]

		__import__(module, globals(), locals(), [], 0)
		
		sys.path = modulePath

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("'''+arr[i+2]+'''", '''+arr[i+2]+'''())

	'''
	
	i += 5


# ######################################################################################################################
# Overwrite the file loadTools.py
# ######################################################################################################################

with open("loadTools.py", 'w') as file:
	file.write("%s" % output)
