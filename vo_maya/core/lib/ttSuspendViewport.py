__author__ = 'Tyler Thornock'

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaMPx as OpenMayaMPx

kPluginCmdName="suspendViewport"

class suspendViewport (OpenMayaMPx.MPxCommand):
	'''
	Simple plugin to turn off the main modeling panes and any torn off panels.  Ideal for baking and scrubbing
	operations since it bypasses the rendering even in simple use, can provide 10x faster results.  This was made
	into a plugin in order to support undo.

	# Example use, notice the try and except... errors MUST be caught or the viewport will remain be off
	import maya.cmds as cmds
	cmds.loadPlugin('suspendViewport.py')
	cmds.suspendViewport(True)
	try:
		sphere = cmds.polySphere()[0]
		for x in range(0,300):
			cmds.currentTime(x)
			cmds.setKeyframe(sphere, at='tx', v=float(x) * .1)
	except:
		raise
	finally:
		cmds.suspendViewport(False)
	'''
	def __init__(self):
		OpenMayaMPx.MPxCommand.__init__(self)
		self.state = True
		self.layouts = None
		self.batch = cmds.about(batch=True)

	def isUndoable (self):
		return True

	def doIt(self, args):
		argCount = args.length()
		if not argCount:
			raise Exception ('viewportSuspend requires a True or False argument.')

		self.state = args.asBool(0)

		self.batch = cmds.about(b=True)
		if self.batch:
			print 'Batch mode detected, skipping viewportSuspend.'
			return
		viewPane = mel.eval('$fastBakeTmp = $gMainPane;')
		windows = cmds.lsUI(windows=True)
		self.layouts = [viewPane]
		for window in windows:
			if 'modelPanel' in window:
				self.layouts.append(window.replace('Window', ''))

		self.redoIt()

	def redoIt(self):
		if self.batch:
			print 'Batch mode detected, skipping viewportSuspend.'
			return
		for layout in self.layouts:
			if cmds.layout(layout, q=True, ex=True):
				cmds.layout(layout, e=True, m=not self.state)
		cmds.setFocus(self.layouts[0])

	def undoIt(self):
		if self.batch:
			print 'Batch mode detected, skipping viewportSuspend.'
			return
		for layout in self.layouts:
			if cmds.layout(layout, q=True, ex=True):
				cmds.layout(layout, e=True, m=self.state)
		cmds.setFocus(self.layouts[0])

def cmdCreator():
	return OpenMayaMPx.asMPxPtr(suspendViewport())


def initializePlugin (mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.registerCommand(kPluginCmdName, cmdCreator)
	except:
		raise("Failed to register command: " + kPluginCmdName)

def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterCommand(kPluginCmdName)
	except:
		raise("Failed to unregister command: " + kPluginCmdName)
