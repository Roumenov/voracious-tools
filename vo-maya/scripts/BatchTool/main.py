import os
import pymel.core as pm
import json
from maya import OpenMayaUI as omui
from Qt import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance
import sys
import pythonSyntax
import btui
reload(btui)

mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QtWidgets.QWidget)


class logLevels:

    lDisplay = 'Display'
    lWarning = 'Warning'
    lError = 'Error'


class BatchTools(QtWidgets.QMainWindow, btui.Ui_wBatchTools):
    def __init__(self, parent):
        super(BatchTools, self).__init__(parent)
        self._currentSceneList = []
        self.setupUi(self)
        self.preLoad()
        self.connectUI()

    def isSceneListValid(self):

        if len(self.getCurrentSceneList()) == 0:
            return False
        else:
            return True

    def export_data_to_file(self, data, path):

        with open(path, 'wb') as fp:
            json.dump(data, fp)

    def import_data_from_file(self, path):

        with open(path, 'r') as fp:
            return json.load(fp)

    def getCurrentSceneList(self):

        return self._currentSceneList

    def onGrabFilePath(self):

        filePath = QtWidgets.QFileDialog.getSaveFileName(caption="Select scene list file")
        if not filePath[0] == '':
            self.outputFilePathLineEdit.setText(filePath[0])

    def onGrabrootDir(self):

        filePath = QtWidgets.QFileDialog.getExistingDirectory(caption="Select root folder for search")
        if not filePath[0] == '':
            self.rootFolderLineEdit.setText(filePath.replace("\\", "/"))

    def UE4FbxPreset(self):

        self.FBXExportReset()

        pm.mel.eval('FBXExportSmoothingGroups -v 1;')
        self.smoothingGroupsCheckBox.setChecked(pm.mel.eval('FBXExportSmoothingGroups -q;'))
        pm.mel.eval('FBXExportSmoothMesh -v 1;')
        self.smoothMeshCheckBox.setChecked(pm.mel.eval('FBXExportSmoothMesh -q;'))
        pm.mel.eval('FBXExportTriangulate -v 1;')
        self.triangulateCheckBox.setChecked(pm.mel.eval('FBXExportTriangulate -q;'))
        pm.mel.eval('FBXExportFileVersion -v FBX201300;')
        self.versionComboBox.setCurrentIndex(self.versionComboBox.findText(pm.mel.eval('FBXExportFileVersion -q;')))

    def FBXExportReset(self):

        pm.mel.eval('FBXResetExport;')
        self.versionComboBox.setCurrentIndex(self.versionComboBox.findText(pm.mel.eval('FBXExportFileVersion -q;')))
        self.generateLogCheckBox.setChecked(bool(pm.mel.eval('FBXExportGenerateLog -q;')))
        self.exportInAsciiCheckBox.setChecked(bool(pm.mel.eval('FBXExportInAscii -q;')))
        self.bakeResampleAnimationCheckBox.setChecked(pm.mel.eval('FBXExportBakeResampleAnimation -q;'))
        self.smoothingGroupsCheckBox.setChecked(pm.mel.eval('FBXExportSmoothingGroups -q;'))
        self.triangulateCheckBox.setChecked(pm.mel.eval('FBXExportTriangulate -q;'))
        self.smoothMeshCheckBox.setChecked(pm.mel.eval('FBXExportSmoothMesh -q;'))
        self.inputConnectionsCheckBox.setChecked(pm.mel.eval('FBXExportInputConnections -q;'))
        self.constraintsCheckBox.setChecked(pm.mel.eval('FBXExportConstraints -q;'))
        self.skinsCheckBox.setChecked(pm.mel.eval('FBXExportSkins -q;'))
        self.axisConversionMethodComboBox.setCurrentIndex(self.axisConversionMethodComboBox.findText('none'))
        self.bakeComplexAnimationCheckBox.setChecked(bool(pm.mel.eval('FBXExportBakeComplexAnimation -q;')))
        self.bakeComplexStartSpinBox.setValue(pm.mel.eval('FBXExportBakeComplexStart -q;'))
        self.bakeComplexStepSpinBox.setValue(pm.mel.eval('FBXExportBakeComplexStep -q;'))
        self.bakeComplexEndSpinBox.setValue(pm.mel.eval('FBXExportBakeComplexEnd -q;'))
        self.exportInstancesCheckBox.setChecked(pm.mel.eval('FBXExportInstances -q;'))
        self.exportLightsCheckBox.setChecked(pm.mel.eval('FBXExportLights -q;'))
        self.exportQuaternionComboBox.setCurrentIndex(self.exportQuaternionComboBox.findText(pm.mel.eval('FBXExportQuaternion -q;')))
        self.exportReferencedAssetsContentCheckBox.setChecked(pm.mel.eval('FBXExportReferencedAssetsContent -q;'))
        self.exportShapesCheckBox.setChecked(pm.mel.eval('FBXExportShapes -q;'))
        self.exportTangentsCheckBox.setChecked(pm.mel.eval('FBXExportTangents -q;'))
        self.exportUpAxisComboBox.setCurrentIndex(self.exportUpAxisComboBox.findText(pm.mel.eval('FBXExportUpAxis -q;')))
        self.hardEdgesCheckBox.setChecked(pm.mel.eval('FBXExportHardEdges -q;'))
        self.embeddedTexturesCheckBox.setChecked(pm.mel.eval('FBXExportEmbeddedTextures -q;'))
        self.exportCamerasCheckBox.setChecked(pm.mel.eval('FBXExportCameras -q;'))
        self.cacheFileCheckBox.setChecked(pm.mel.eval('FBXExportCacheFile -q;'))
        self.applyConstantKeyReducerCheckBox.setChecked(pm.mel.eval('FBXExportApplyConstantKeyReducer -q;'))
        self.exportAnimationOnlyCheckBox.setChecked(pm.mel.eval('FBXExportAnimationOnly -q;'))

    def connectUI(self):

        self.actionSet_scene_list.triggered.connect(self.setSceneListUi)
        self.actionStart.triggered.connect(self.startBatch)
        self.action.triggered.connect(lambda: self.teOutput.clear())
        self.pbResetFbxOptions.clicked.connect(self.FBXExportReset)
        self.pbUePreset.clicked.connect(self.UE4FbxPreset)
        self.fontSizeSpinBox.valueChanged.connect(lambda: self.setFontSize(self.fontSizeSpinBox.value()))
        self.pbGenSceneList.clicked.connect(self.generateSceneList)
        self.pbGrabFilePath.clicked.connect(self.onGrabFilePath)
        self.pbGetRootDir.clicked.connect(self.onGrabrootDir)
        # fbx options
        self.versionComboBox.currentIndexChanged.connect(lambda: pm.mel.eval('FBXExportFileVersion -v %s' % self.versionComboBox.currentText()))
        self.generateLogCheckBox.stateChanged.connect(lambda: pm.mel.eval('FBXExportGenerateLog -v %d;' % self.generateLogCheckBox.isChecked()))
        self.exportInAsciiCheckBox.stateChanged.connect(lambda: pm.mel.eval('FBXExportInAscii -v %d;' % self.exportInAsciiCheckBox.isChecked()))
        self.bakeResampleAnimationCheckBox.stateChanged.connect(lambda: pm.mel.eval('FBXExportBakeComplexAnimation -v %d;' % self.bakeResampleAnimationCheckBox.isChecked()))
        self.smoothingGroupsCheckBox.stateChanged.connect(lambda: pm.mel.eval('FBXExportSmoothingGroups -v %d;' % self.smoothingGroupsCheckBox.isChecked()))
        self.triangulateCheckBox.stateChanged.connect(lambda: pm.mel.eval('FBXExportTriangulate -v %d;' % self.triangulateCheckBox.isChecked()))
        self.smoothMeshCheckBox.stateChanged.connect(lambda: pm.mel.eval('FBXExportSmoothMesh -v %d;' % self.smoothMeshCheckBox.isChecked()))
        self.inputConnectionsCheckBox.stateChanged.connect(lambda: pm.mel.eval('FBXExportInputConnections -v %d;' % self.inputConnectionsCheckBox.isChecked()))
        self.constraintsCheckBox.stateChanged.connect(lambda: pm.mel.eval('FBXExportConstraints -v %d;' % self.constraintsCheckBox.isChecked()))
        self.skinsCheckBox.stateChanged.connect(lambda: pm.mel.eval('FBXExportSkins -v %d;' % self.skinsCheckBox.isChecked()))
        self.axisConversionMethodComboBox.currentIndexChanged.connect(lambda: pm.mel.eval('FBXExportAxisConversionMethod %s' % self.axisConversionMethodComboBox.currentText()))
        self.bakeComplexAnimationCheckBox.stateChanged.connect(lambda: pm.mel.eval('FBXExportBakeComplexAnimation -v %d;' % self.bakeComplexAnimationCheckBox.isChecked()))
        self.bakeComplexStartSpinBox.valueChanged.connect(lambda: pm.mel.eval('FBXExportBakeComplexStart -v %d;' % self.bakeComplexStartSpinBox.value()))
        self.bakeComplexStepSpinBox.valueChanged.connect(lambda: pm.mel.eval('FBXExportBakeComplexStep -v %d;' % self.bakeComplexStepSpinBox.value()))
        self.bakeComplexEndSpinBox.valueChanged.connect(lambda: pm.mel.eval('FBXExportBakeComplexEnd -v %d;' % self.bakeComplexEndSpinBox.value()))
        self.exportInstancesCheckBox.stateChanged.connect(lambda: pm.mel.eval('FBXExportInstances -v %d;' % self.exportInstancesCheckBox.isChecked()))
        self.exportLightsCheckBox.stateChanged.connect(lambda: pm.mel.eval('FBXExportLights -v %d;' % self.exportLightsCheckBox.isChecked()))
        self.exportQuaternionComboBox.currentIndexChanged.connect(lambda: pm.mel.eval('FBXExportQuaternion -v %s' % self.exportQuaternionComboBox.currentText()))
        self.exportReferencedAssetsContentCheckBox.stateChanged.connect(lambda: pm.mel.eval('FBXExportReferencedAssetsContent -v %d;' % self.exportReferencedAssetsContentCheckBox.isChecked()))
        self.exportShapesCheckBox.stateChanged.connect(lambda: pm.mel.eval('FBXExportShapes -v %d;' % self.exportShapesCheckBox.isChecked()))
        self.exportTangentsCheckBox.stateChanged.connect(lambda: pm.mel.eval('FBXExportTangents -v %d;' % self.exportTangentsCheckBox.isChecked()))
        self.exportUpAxisComboBox.currentIndexChanged.connect(lambda: pm.mel.eval('FBXExportUpAxis %s' % self.exportUpAxisComboBox.currentText()))
        self.hardEdgesCheckBox.stateChanged.connect(lambda: pm.mel.eval('FBXExportHardEdges -v %d;' % self.hardEdgesCheckBox.isChecked()))
        self.embeddedTexturesCheckBox.stateChanged.connect(lambda: pm.mel.eval('FBXExportEmbeddedTextures -v %d;' % self.embeddedTexturesCheckBox.isChecked()))
        self.exportCamerasCheckBox.stateChanged.connect(lambda: pm.mel.eval('FBXExportCameras -v %d;' % self.exportCamerasCheckBox.isChecked()))
        self.cacheFileCheckBox.stateChanged.connect(lambda: pm.mel.eval('FBXExportCacheFile -v %d;' % self.cacheFileCheckBox.isChecked()))
        self.applyConstantKeyReducerCheckBox.stateChanged.connect(lambda: pm.mel.eval('FBXExportApplyConstantKeyReducer -v %d;' % self.applyConstantKeyReducerCheckBox.isChecked()))
        self.exportAnimationOnlyCheckBox.stateChanged.connect(lambda: pm.mel.eval('FBXExportAnimationOnly -v %d;' % self.exportAnimationOnlyCheckBox.isChecked()))

    def log(self, msg, level=logLevels.lDisplay):

        if level == logLevels.lDisplay:
            self.teOutput.appendHtml('<FONT COLOR="white">[*] {0}</FONT>'.format(msg))
        elif level == logLevels.lWarning:
            self.teOutput.appendHtml('<FONT COLOR="yellow">[**] {0}</FONT>'.format(msg))
        else:
            self.teOutput.appendHtml('<FONT COLOR="red">[***] {0}</FONT>'.format(msg))

    def getCommandFromTab(self, idx):

        if idx == 0:
            return self.teMel.toPlainText()
        if idx == 1:
            return self.tePython.toPlainText()
        return None

    def onSave(self, path):

        operation = self.cbSaveoperation.currentText()
        extension = self.sceneListExtension()
        self.log('Current scenes extension: {0}'.format(extension))

        if operation == 'Skip':
            self.log('saving skipped')
        elif operation == 'SaveCurrent':
            if extension == 'fbx':
                self.log('Saving {0}'.format(path))
                self.saveFbx(path)
                pm.newFile(f=1)
            else:
                self.log('Saving {0}'.format(path))
                pm.saveAs(path, f=1)
        else:
            name = self.getFileName(path)
            extension = self.sceneListExtension()
            newName = os.path.dirname(path)+'/'+name+'_new.'+extension
            self.log('Saving {0}'.format(newName))
            pm.saveAs(newName)

    def getFileName(self, path):

        return os.path.basename(path).split('.')[0]

    def executeActiveTab(self):

        activeIndex = self.tabWidget.currentIndex()
        if activeIndex == 0:
            cmd = self.getCommandFromTab(activeIndex)
            if not cmd == '':
                pm.mel.eval(cmd)
            else:
                self.log('Current tab is empty', logLevels.lWarning)
        else:
            cmd = self.getCommandFromTab(activeIndex)
            if not cmd == '':
                exec(cmd)
            else:
                self.log('Current tab is empty', logLevels.lWarning)

    def openFbx(self, path):

        if os.path.isfile(path):
            pm.newFile(f=1)
            pm.importFile(path.replace('\\', '/'), f=1)
            self.log('Open {0}'.format(path))
        else:
            self.log('Invalid file name {0}'.format(path), logLevels.lWarning)

    def saveFbx(self, path):

        pm.mel.eval('FBXExport -f "{0}" -ea'.format(path))

    def openScene(self, path):

        if os.path.isfile(path):
            pm.openFile(path.replace('\\', '/'), f=1)
            self.log('Open {0}'.format(path))
        else:
            self.log('Invalid file name {0}'.format(path), logLevels.lWarning)

    def setFontSize(self, size):

        f = self.teOutput.font()
        f.setPointSize(abs(size))
        self.teOutput.setFont(f)
        self.tePython.setFont(f)
        self.teMel.setFont(f)

    def sceneListExtension(self):

        if self.isSceneListValid():
            return os.path.basename(self.getCurrentSceneList()[0]).split('.')[1]

    def startBatch(self):

        if self.isSceneListValid():
            for s in self.getCurrentSceneList():
                # open/import
                if self.sceneListExtension() == 'ma':
                    self.openScene(s)
                else:
                    self.openFbx(s)
                # do job
                self.log('Processing...')
                self.executeActiveTab()

                # save/export
                self.onSave(s)

    def preLoad(self):

        self.teOutput.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.action = QtWidgets.QAction('clear', self.teOutput)
        self.teOutput.addAction(self.action)
        pythonSyntax.PythonHighlighter(self.tePython.document())

    def postLoad(self):

        self.log('BatchTools loaded', logLevels.lDisplay)
        self.splitter.setSizes([self.splitter.sizes()[0], self.height()/10])
        self.UE4FbxPreset()

    def generateSceneList(self):

        root = self.rootFolderLineEdit.text()
        outFile = self.outputFilePathLineEdit.text()
        exts = []
        if self.cbMa.isChecked():
            exts.append(".ma")
        if self.cbMb.isChecked():
            exts.append(".mb")
        if self.cbFbx.isChecked():
            exts.append(".fbx")

        if len(exts) == 0:
            self.log("Select extension to grab", logLevels.lError)
            return

        if not os.path.isdir(root):
            self.log('Invalid root folder', logLevels.lError)
            return

        if not os.path.isdir(os.path.dirname(outFile)):
            self.log('No directory exists for file %s' % outFile, logLevels.lError)
            return

        SceneList = []
        for root, d, files in os.walk(root):
            for f in files:
                fPath = str()
                fPath = "%s/%s" % (root, f)
                if os.path.splitext(fPath)[1] in exts:
                    SceneList.append(fPath.replace("//", "/"))

        self.export_data_to_file(SceneList, outFile)
        self.log('Scene list generated! %s' % outFile)

        if self.useGeneratedListCheckBox.isChecked():
            self.setSceneListFromPath(outFile)

    def setSceneListFromPath(self, path):

        if os.path.isfile(path):
            self.le_SceneList.setText(path)
            data = self.import_data_from_file(path)
            self.lcdNumberOfScenes.display(len(data))
            self._currentSceneList = data
            self.log('{0} used'.format(os.path.basename(path)), logLevels.lDisplay)
        else:
            self.le_SceneList.clear()
            self.lcdNumberOfScenes.display(0)
            self.log('Invalid file path', logLevels.lWarning)

    def setSceneListUi(self):

        filePath = QtWidgets.QFileDialog.getOpenFileName(filter='*.txt')
        self.setSceneListFromPath(filePath[0])


def start():

    if pm.window('wBatchTools', ex=1):
        pm.deleteUI('wBatchTools')

    DOCK_NAME = 'BT_DOCK'
    LYT_NAME = 'BT_LYT_NAME'
    WIN_NAME = 'wBatchTools'
    AREA = 'left'

    app = BatchTools(mayaMainWindow)
    app.show()
    app.postLoad()

    # dock window
    if pm.dockControl(DOCK_NAME, ex=1):
        pm.deleteUI(DOCK_NAME)
    dockLayout = pm.paneLayout(LYT_NAME, configuration='single', parent=WIN_NAME, width = 500, height = 500 )
    pm.dockControl(DOCK_NAME, aa=['left','right'], a=AREA , floating=0, content=dockLayout, l='Batch tools')
    pm.control(WIN_NAME, e=True, parent=dockLayout)
    if pm.dockControl( DOCK_NAME, ex = 1 ):
        pm.control( WIN_NAME, e = 1, p = dockLayout )
        pm.dockControl( DOCK_NAME, e = 1, a = AREA, fl = 0 )
        pm.dockControl( DOCK_NAME, e = 1, vis = 1 )
        pm.dockControl( DOCK_NAME, e = 1, w = 500 )
