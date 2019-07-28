#			 only for maya 2011/2012/2013/2014
#
#
#			 connectionSwitcher.py 
#			 version 1.0, last modified 10-16-2013
#			 Copyright (C) 2013 Perry Leijten
#			 Email: perryleijten@gmail.com
#			 Website: www.perryleijten.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# See http://www.gnu.org/licenses/gpl.html for a copy of the GNU General 
# Public License.
#--------------------------------------------------------------------------------#
#					I N S T A L L A T I O N:
#
# Copy the "connectionSwitcher.py" together with "connectionSwitcher.ui" and the Icon folder to your Maya scriptsdirectory:
#	 MyDocuments\Maya\scripts\
#		 use this text as a python script within Maya:
'''
import connectionSwitcher
connectionSwitcher.StartUI()
'''
# this text can be entered from the script editor and can be made into a button
#
# note: PyQt and sip or pyside libraries are necessary to run this file!!!
from maya import cmds, OpenMayaUI

default = "none"
try:
	import os, sip, PyQt4, sys, stat, re
	from PyQt4 						import uic, QtGui, QtCore
	default = "pyqt4"
except:
	print "pyqt4 not found, trying pySide!"
try:
	import pysideuic, os, shiboken, sys, stat, re
	import xml.etree.ElementTree	as xml
	from cStringIO					import StringIO
	from PySide						import QtGui, QtCore
	default = "pyside"
except:
	print "pyside not found, trying PyQt4!"

if default == "none":
	cmds.error("no Library found, please install PyQt4 or PySide!")
import connectionSwitcher
def loadUiType(uiFile):
	if default ==  "pyqt4":
		form_class, base_class =  PyQt4.uic.loadUiType( uiFile )
	else:
		parsed = xml.parse(uiFile)
		widget_class = parsed.find('widget').get('class')
		form_class = parsed.find('class').text

		with open(uiFile, 'r') as f:
			o = StringIO()
			frame = {}

			pysideuic.compileUi(f, o, indent=0)
			pyc = compile(o.getvalue(), '<string>', 'exec')
			exec pyc in frame

			form_class = frame['Ui_%s'%form_class]
			base_class = eval('QtGui.%s'%widget_class)
	return form_class, base_class

FilePath = connectionSwitcher.__file__.replace('\\','/').rsplit('/',1)[0] + '/'
# Import the UI file for the interface
qDir	 = QtCore.QDir()
uiFile	 = FilePath + 'connectionSwitcher.ui'
ui_path = os.path.dirname(uiFile)
qDir.setCurrent(ui_path)
Ui_MainWindow, Ui_BaseClass = loadUiType( uiFile )	

class connectionSwitcher(Ui_MainWindow, Ui_BaseClass):
	ConnectionSwitcherSavedList = []
	def __init__(self, parent=None):
			# Parent UI to Dock
		super(connectionSwitcher, self).__init__(parent)
		self.setupUi( self )
			#variables that determine what to change
		self.__useKeys				 = True
		self.__useConstraints		 = True
		self.__useDirectConnections	 = True
		self.__useExpressions		 = True
		self.__maintainOffset		 = False
			#variables that are used for storing the used values
		self.__usedConnections 		= []
		self.selectedAmount 		= 0
		self.__unableToConnect 		= []
			#checkboxes
		self.all_checkBox.toggled.connect(self.__allCheckBoxFunction) 
		self.keyFrame_checkBox.toggled.connect(self.__connectionsSettings) 
		self.constraint_checkBox.toggled.connect(self.__connectionsSettings) 
		self.expression_checkBox.toggled.connect(self.__connectionsSettings) 
		self.directConnection_checkBox.toggled.connect(self.__connectionsSettings) 
		self.maintainOffset_checkBox.toggled.connect(self.__maintainOffsetFunction) 
			#buttons
		self.switch_pushButton.clicked.connect(self.switchConnection)
		self.move_pushButton.clicked.connect(self.moveConnection)
		self.break_pushButton.clicked.connect(self.breakConnection)
			
		self.cut_pushButton.clicked.connect(self.cutConnection)
		self.copy_pushButton.clicked.connect(self.copyConnection)
		self.paste_pushButton.clicked.connect(self.pasteConnection)
		
		self.point_pushButton.clicked.connect(self.createConstraintFunction)
		self.orient_pushButton.clicked.connect(self.createConstraintFunction)
		self.parent_pushButton.clicked.connect(self.createConstraintFunction)
		self.poleVector_pushButton.clicked.connect(self.createConstraintFunction)
	def __maintainOffsetFunction(self, *args):
		checked = self.maintainOffset_checkBox.isChecked()
		if checked == True:
			self.__maintainOffset = True
		else:
			self.__maintainOffset = False
	
	def createConstraintFunction(self, *args):
			#fast creation of most used constraints
		CurrentPos 		= QtGui.QCursor().pos()
		ButtonWidget 	= QtGui.qApp.widgetAt(CurrentPos)
		selection = cmds.ls(sl=True)
		selectionLength = len(selection)
		if selectionLength < 2:
			cmds.error('not enough objects selected')
		else:
			if ButtonWidget.objectName().split("_")[0] == "point":
				cmds.pointConstraint(mo=self.__maintainOffset)
			elif ButtonWidget.objectName().split("_")[0] == "orient":
				cmds.orientConstraint(mo=self.__maintainOffset)
			elif ButtonWidget.objectName().split("_")[0] == "parent":
				cmds.parentConstraint(mo=self.__maintainOffset)
			else:
				cmds.poleVectorConstraint()

	def __allCheckBoxFunction(self,*args):
			#multiple functionality works together with individual boxes
		checked = self.all_checkBox.isChecked()
		if checked == True:
			self.keyFrame_checkBox.setChecked(True)
			self.constraint_checkBox.setChecked(True)
			self.expression_checkBox.setChecked(True)
			self.directConnection_checkBox.setChecked(True)
		else:
			self.keyFrame_checkBox.setChecked(False)
			self.constraint_checkBox.setChecked(False)
			self.expression_checkBox.setChecked(False)
			self.directConnection_checkBox.setChecked(False)

	def __connectionsSettings(self, *args):
			#multiple functionality works together with all_checkBox
		keyFrameChecked = self.keyFrame_checkBox.isChecked()
		constraintChecked = self.constraint_checkBox.isChecked()
		expressionChecked = self.expression_checkBox.isChecked()
		directChecked = self.directConnection_checkBox.isChecked()
		if keyFrameChecked and constraintChecked and expressionChecked and directChecked:
			self.all_checkBox.setChecked(True)
		elif not keyFrameChecked and not constraintChecked and not expressionChecked and not directChecked:
			self.all_checkBox.setChecked(False)
			#individual workable
		if keyFrameChecked:
			self.__useKeys				 = True
		else:
			self.__useKeys				 = False
		if constraintChecked:
			self.__useConstraints		 = True
		else:
			self.__useConstraints		 = False
		if expressionChecked:
			self.__useExpressions		 = True
		else:
			self.__useExpressions		 = False
		if directChecked:
			self.__useDirectConnections	 = True
		else:
			self.__useDirectConnections	 = False

	def __saveAllConnection(self,objects, typeToFilterList,lastSelected = None, *args):
			# this will only list all possible connections (from selection)
		temporaryConnectionList = []
		connectionList 			= []
		if type(objects) == unicode or type(objects) == str:
			objects = [objects]
		for typeToFilter in typeToFilterList:
			for object in range(len(objects)):
				allConnections = cmds.listConnections(objects[object], c=True, p=True, t=typeToFilter)
				if allConnections != None:
						#ugly identification if searching for direct connection or constraint connection
					if typeToFilter == "constraint" and not any("Constraint" in s for s in allConnections): 
						pass
					elif typeToFilter == "transform" and any("Constraint" in s for s in allConnections): 
						pass
					else:
							#cleaning connections for easy re=connection
						if not allConnections == None:
							for i in range(len(allConnections)):
								if i % 2 == False:
									temporaryConnectionList.append(allConnections[i])
								elif i % 2 == True:
									temporaryConnectionList.append(allConnections[i])
									connectionList.append(temporaryConnectionList)
									temporaryConnectionList = []
								# reversing list so it visualises the direction of the connection
							for connection in connectionList:
								for attr in connection:
									if cmds.connectionInfo(attr, isDestination = True):
										pass
									else:
										connection.reverse()
							newList = [objects[object],objects[object-1], connectionList]
							if lastSelected in newList:
								newList.remove(lastSelected)
							self.__usedConnections.append(newList)
							connectionList = []

	def __useSettings(self,*args):
		self.toConnect = []
			# check for which nodetypes it needs to search in connections
		if self.__useKeys:
			self.toConnect.append('animCurve')
		if self.__useConstraints:
			self.toConnect.append('constraint')
		if self.__useExpressions:
			self.toConnect.append('expression')
		if self.__useDirectConnections:
			self.toConnect.append('transform')
			
	def __disConnect(self,*args):		
			#try to break connections before connecting again
		for usedconnectionList in self.__usedConnections:
			for connection in usedconnectionList[-1]:
				try:
					cmds.disconnectAttr(connection[0], connection[1])
				except:
					cmds.disconnectAttr(connection[1], connection[0])
				else:
					print 'not able to disconnect: ' + connection[0] + " from " + connection[1] 
	
	def __reConnect(self,switch = True, input = None, *args):		
			#reconnect using stored values
		for usedconnectionList in self.__usedConnections:
			for connection in usedconnectionList[-1]:
				if switch == True:
					base = usedconnectionList[0]
					end = usedconnectionList[1]
						# determine which operation is necessary 
					if connection[0].split('.')[0] == base:
						newDriver = end + '.' + connection[0].split('.')[1]
						try:
							cmds.connectAttr(newDriver, connection[1],f=True)
						except:
							self.__unableToConnect.append([newDriver, connection[1]])
						self.__usedConnections =[]
					elif connection[0].split('.')[0] == end:
							# make sure this works on objects that have a bigger connection hierarchy then 1
						newDriver = base+ '.' + connection[1].split('.')[1]
						newDriven = end+ '.' + connection[0].split('.')[1]
						try:
							cmds.connectAttr(newDriver, connection[0],f=True)
						except:
							cmds.connectAttr(connection[1],newDriven ,f=True)
						else:
							self.__unableToConnect.append([newDriver, connection[0]])
						self.__usedConnections =[]
					else:
						newDriven = end+'.'+connection[1].split(".")[1]
						try:
							cmds.connectAttr(connection[0], newDriven,f=True)
						except:
							self.__unableToConnect.append([connection[0], newDriven])
						self.__usedConnections =[]
				else:
						# this needs an input!!
					if input == None:
						cmds.error("input needs to be given to know which object is last selected")
					else:
						if type(connection) == list:
							if connection[0].split('.')[0] == usedconnectionList[0]:
								newDriven = input+'.'+connection[0].split(".")[1]
								try:
									cmds.connectAttr(newDriven, connection[1],f=True)
								except:
									self.__unableToConnect.append([connection[0], newDriven])
								self.__usedConnections =[]
							
							else:
								newDriver = input+'.'+connection[1].split(".")[1]
								try:
									cmds.connectAttr(connection[0],newDriver, f=True)
								except:
									self.__unableToConnect.append([newDriver,connection[1] ])
								self.__usedConnections =[]

		if len(self.__unableToConnect) > 0:
			print "these connections could not be made: "
			for misConnection in self.__unableToConnect:
				print ">> " + misConnection[0] + "<->" + misConnection[1]
		self.__unableToConnect = []
	
	def switchConnection(self, *args):
			# this function switches 2 objects connections
		selection = cmds.ls(sl=True)
		self.selectedAmount = len(selection)
		if self.selectedAmount != 2:
			cmds.error("this option needs exact 2 objects of the same type!")
		else:
			self.__useSettings()
			self.__saveAllConnection(selection,self.toConnect)			
			self.__disConnect()
			self.__reConnect()
	
	def moveConnection(self, *args):
			# this function moves all the connections from all selected objects to the last selected object
		selection = cmds.ls(sl=True)
		self.selectedAmount = len(selection)
		if self.selectedAmount < 2:
			cmds.error("this option needs at least 2 objects selected")
		else:
			self.__useSettings()
			self.__saveAllConnection(selection,self.toConnect, selection[-1])			
			self.__disConnect()
			self.__reConnect(switch = False, input = selection[-1])

	def breakConnection(self, *args):
			# this function will break only the selected connections
		selection = cmds.ls(sl=True)
		self.selectedAmount = len(selection)
		self.__useSettings()
		self.__saveAllConnection(selection, self.toConnect)
		self.__disConnect()
		self.__usedConnections =[]
	
	def cutConnection(self, *args):
			# get all connections and break them in sequence
		selection = cmds.ls(sl=True)
		for selected in selection:
			self.__useSettings()
			self.__saveAllConnection(selected,self.toConnect)
			if not self.__usedConnections == []:
				connectionSwitcher.ConnectionSwitcherSavedList.append(self.__usedConnections)
			self.__disConnect()
			self.__usedConnections = []
	
	def copyConnection(self, *args):
			# get all connections in sequence
		selection = cmds.ls(sl=True)
		for selected in selection:
			self.__useSettings()
			self.__saveAllConnection(selected,self.toConnect)
			if not self.__usedConnections == []:
				connectionSwitcher.ConnectionSwitcherSavedList.append(self.__usedConnections)
			self.__usedConnections = []	

	def pasteConnection(self, *args):
			# paste all connections in sequence
		selection = cmds.ls(sl=True)
		totalSelection = len(selection)
		if totalSelection > connectionSwitcher.ConnectionSwitcherSavedList:
			print "not all selected objects will be connected"
		for selected in range(totalSelection):
			base = connectionSwitcher.ConnectionSwitcherSavedList[0][0]
			end = selection[selected]
			connectionList = connectionSwitcher.ConnectionSwitcherSavedList[0][-1]
			self.__usedConnections = [base, end, connectionList]
			self.__reConnect(switch = False, input = selection[selected])
			self.usedConnections=[]
			connectionSwitcher.ConnectionSwitcherSavedList.pop(0)
			
def StartUI():	
	'''starts UI and makes it dockable within Maya'''
	if default == "pyqt4":
		MayaWindowPtr = sip.wrapinstance(long( OpenMayaUI.MQtUtil.mainWindow() ), QtCore.QObject)
	else:
		MayaWindowPtr = shiboken.wrapInstance(long(OpenMayaUI.MQtUtil.mainWindow()), QtGui.QMainWindow)
	
	window_name	 = 'connection_switcher_Window'
	dock_control	 = 'connection_switcher_Dock'
	
	if cmds.window( window_name, exists=True ):
		cmds.deleteUI( window_name )
		
	Window = connectionSwitcher(MayaWindowPtr)
	Window.setObjectName(window_name)
	if (cmds.dockControl(dock_control, q=True, ex=True)):
		cmds.deleteUI(dock_control)
		
	AllowedAreas = ['right', 'left']
	cmds.dockControl(dock_control,aa=AllowedAreas, a='right', floating=True, content=window_name, label='Connection Switcher')