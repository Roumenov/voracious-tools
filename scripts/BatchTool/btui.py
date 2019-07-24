# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:/GIT/creativecrashtools/BatchToolDev/btui.ui'
#
# Created: Fri Nov 30 16:02:33 2018
#      by: pyside2-uic 2.0.0 running on PySide2 5.6.0~a1
#
# WARNING! All changes made in this file will be lost!

from Qt import QtCompat, QtCore, QtGui, QtWidgets

class Ui_wBatchTools(object):
    def setupUi(self, wBatchTools):
        wBatchTools.setObjectName("wBatchTools")
        wBatchTools.resize(594, 878)
        wBatchTools.setStyleSheet("QToolTip\n"
"{\n"
"     border: 1px solid black;\n"
"     background-color: #b5b5b5;\n"
"     border-radius: 3px;\n"
"}\n"
"\n"
"QWidget\n"
"{\n"
"    color: #b1b1b1;\n"
"    background-color: #323232;\n"
"}\n"
"\n"
"QWidget:item:hover\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #ca0619);\n"
"    color: #000000;\n"
"}\n"
"\n"
"QWidget:item:selected\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"QMenuBar::item\n"
"{\n"
"    background: transparent;\n"
"}\n"
"\n"
"QMenuBar::item:selected\n"
"{\n"
"    background: transparent;\n"
"    border: 1px solid #ffaa00;\n"
"}\n"
"\n"
"QMenuBar::item:pressed\n"
"{\n"
"    background: #444;\n"
"    border: 1px solid #000;\n"
"    background-color: QLinearGradient(\n"
"        x1:0, y1:0,\n"
"        x2:0, y2:1,\n"
"        stop:1 #212121,\n"
"        stop:0.4 #343434/*,\n"
"        stop:0.2 #343434,\n"
"        stop:0.1 #ffaa00*/\n"
"    );\n"
"    margin-bottom:-1px;\n"
"    padding-bottom:1px;\n"
"}\n"
"\n"
"QMenu\n"
"{\n"
"    border: 1px solid #000;\n"
"}\n"
"\n"
"QMenu::item\n"
"{\n"
"    padding: 2px 20px 2px 20px;\n"
"}\n"
"\n"
"QMenu::item:selected\n"
"{\n"
"    color: #000000;\n"
"}\n"
"\n"
"QWidget:disabled\n"
"{\n"
"    color: #404040;\n"
"    background-color: #323232;\n"
"}\n"
"\n"
"QAbstractItemView\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0.1 #646464, stop: 1 #5d5d5d);\n"
"}\n"
"\n"
"QWidget:focus\n"
"{\n"
"    /*border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);*/\n"
"}\n"
"\n"
"QLineEdit\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);\n"
"    padding: 1px;\n"
"    border-style: solid;\n"
"    border: 1px solid #1e1e1e;\n"
"    border-radius: 2;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"    color: #b1b1b1;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
"    border-width: 1px;\n"
"    border-color: #1e1e1e;\n"
"    border-style: solid;\n"
"    border-radius: 2;\n"
"    padding: 3px;\n"
"    font-size: 12px;\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
"}\n"
"\n"
"QComboBox\n"
"{\n"
"    selection-background-color: #ffaa00;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
"    border-style: solid;\n"
"    border: 1px solid #1e1e1e;\n"
"    border-radius: 2;\n"
"}\n"
"\n"
"QComboBox:hover,QPushButton:hover\n"
"{\n"
"    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"\n"
"QComboBox:on\n"
"{\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
"    selection-background-color: #ffaa00;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView\n"
"{\n"
"    border: 2px solid darkgray;\n"
"    selection-background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"QComboBox::drop-down\n"
"{\n"
"     subcontrol-origin: padding;\n"
"     subcontrol-position: top right;\n"
"     width: 15px;\n"
"\n"
"     border-left-width: 0px;\n"
"     border-left-color: darkgray;\n"
"     border-left-style: solid; /* just a single line */\n"
"     border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"     border-bottom-right-radius: 3px;\n"
" }\n"
"\n"
"QComboBox::down-arrow\n"
"{\n"
"     image: url(:/down_arrow.png);\n"
"}\n"
"\n"
"QGroupBox:focus\n"
"{\n"
"border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"QTextEdit:focus\n"
"{\n"
"    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"QScrollBar:horizontal {\n"
"     border: 1px solid #222222;\n"
"     background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);\n"
"     height: 7px;\n"
"     margin: 0px 16px 0 16px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal\n"
"{\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);\n"
"      min-height: 20px;\n"
"      border-radius: 2px;\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal {\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"      width: 14px;\n"
"      subcontrol-position: right;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal {\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"      width: 14px;\n"
"     subcontrol-position: left;\n"
"     subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal\n"
"{\n"
"      border: 1px solid black;\n"
"      width: 1px;\n"
"      height: 1px;\n"
"      background: white;\n"
"}\n"
"\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"      background: none;\n"
"}\n"
"\n"
"QScrollBar:vertical\n"
"{\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);\n"
"      width: 7px;\n"
"      margin: 16px 0 16px 0;\n"
"      border: 1px solid #222222;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical\n"
"{\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);\n"
"      min-height: 20px;\n"
"      border-radius: 2px;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical\n"
"{\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"      height: 14px;\n"
"      subcontrol-position: bottom;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical\n"
"{\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #d7801a, stop: 1 #ffa02f);\n"
"      height: 14px;\n"
"      subcontrol-position: top;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical\n"
"{\n"
"      border: 1px solid black;\n"
"      width: 1px;\n"
"      height: 1px;\n"
"      background: white;\n"
"}\n"
"\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical\n"
"{\n"
"      background: none;\n"
"}\n"
"\n"
"QTextEdit\n"
"{\n"
"    background-color: #242424;\n"
"}\n"
"\n"
"QPlainTextEdit\n"
"{\n"
"    background-color: #242424;\n"
"}\n"
"\n"
"QHeaderView::section\n"
"{\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop: 0.5 #505050, stop: 0.6 #434343, stop:1 #656565);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #6c6c6c;\n"
"}\n"
"\n"
"QDockWidget::title\n"
"{\n"
"    text-align: center;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);\n"
"}\n"
"\n"
"QDockWidget::close-button, QDockWidget::float-button\n"
"{\n"
"    text-align: center;\n"
"    spacing: 1px; /* spacing between items in the tool bar */\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);\n"
"}\n"
"\n"
"QDockWidget::close-button:hover, QDockWidget::float-button:hover\n"
"{\n"
"    background: #242424;\n"
"}\n"
"\n"
"QDockWidget::close-button:pressed, QDockWidget::float-button:pressed\n"
"{\n"
"    padding: 1px -1px -1px 1px;\n"
"}\n"
"\n"
"QMainWindow::separator\n"
"{\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #4c4c4c;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"}\n"
"\n"
"QMainWindow::separator:hover\n"
"{\n"
"\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d7801a, stop:0.5 #b56c17 stop:1 #ffa02f);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #6c6c6c;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"}\n"
"\n"
"QToolBar::handle\n"
"{\n"
"     spacing: 3px; /* spacing between items in the tool bar */\n"
"     background: url(:/images/handle.png);\n"
"}\n"
"\n"
"QMenu::separator\n"
"{\n"
"    height: 2px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    margin-left: 10px;\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"QProgressBar\n"
"{\n"
"    border: 2px solid grey;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    background-color: #d7801a;\n"
"    width: 2.15px;\n"
"    margin: 0.5px;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    color: #b1b1b1;\n"
"    border: 1px solid #444;\n"
"    border-bottom-style: none;\n"
"    background-color: #323232;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    padding-top: 3px;\n"
"    padding-bottom: 2px;\n"
"    margin-right: -1px;\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"    border: 1px solid #444;\n"
"    top: 1px;\n"
"}\n"
"\n"
"QTabBar::tab:last\n"
"{\n"
"    margin-right: 0; /* the last selected tab has nothing to overlap with on the right */\n"
"    border-top-right-radius: 3px;\n"
"}\n"
"\n"
"QTabBar::tab:first:!selected\n"
"{\n"
" margin-left: 0px; /* the last selected tab has nothing to overlap with on the right */\n"
"\n"
"\n"
"    border-top-left-radius: 3px;\n"
"}\n"
"\n"
"QTabBar::tab:!selected\n"
"{\n"
"    color: #b1b1b1;\n"
"    border-bottom-style: solid;\n"
"    margin-top: 3px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:.4 #343434);\n"
"}\n"
"\n"
"QTabBar::tab:selected\n"
"{\n"
"    border-top-left-radius: 3px;\n"
"    border-top-right-radius: 3px;\n"
"    margin-bottom: 0px;\n"
"}\n"
"\n"
"QTabBar::tab:!selected:hover\n"
"{\n"
"    /*border-top: 2px solid #ffaa00;\n"
"    padding-bottom: 3px;*/\n"
"    border-top-left-radius: 3px;\n"
"    border-top-right-radius: 3px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:0.4 #343434, stop:0.2 #343434, stop:0.1 #ffaa00);\n"
"}\n"
"\n"
"QRadioButton::indicator:checked, QRadioButton::indicator:unchecked{\n"
"    color: #b1b1b1;\n"
"    background-color: #323232;\n"
"    border: 1px solid #b1b1b1;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked\n"
"{\n"
"    background-color: qradialgradient(\n"
"        cx: 0.5, cy: 0.5,\n"
"        fx: 0.5, fy: 0.5,\n"
"        radius: 1.0,\n"
"        stop: 0.25 #ffaa00,\n"
"        stop: 0.3 #323232\n"
"    );\n"
"}\n"
"\n"
"QRadioButton::indicator\n"
"{\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QRadioButton::indicator:hover\n"
"{\n"
"    border: 1px solid #ffaa00;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(wBatchTools)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.toolBox = QtWidgets.QToolBox(self.splitter)
        self.toolBox.setObjectName("toolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 576, 344))
        self.page.setObjectName("page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.le_SceneList = QtWidgets.QLineEdit(self.page)
        self.le_SceneList.setEnabled(True)
        self.le_SceneList.setReadOnly(True)
        self.le_SceneList.setObjectName("le_SceneList")
        self.horizontalLayout.addWidget(self.le_SceneList)
        self.lcdNumberOfScenes = QtWidgets.QLCDNumber(self.page)
        self.lcdNumberOfScenes.setObjectName("lcdNumberOfScenes")
        self.horizontalLayout.addWidget(self.lcdNumberOfScenes)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.cbSaveoperation = QtWidgets.QComboBox(self.page)
        self.cbSaveoperation.setObjectName("cbSaveoperation")
        self.cbSaveoperation.addItem("")
        self.cbSaveoperation.addItem("")
        self.cbSaveoperation.addItem("")
        self.verticalLayout.addWidget(self.cbSaveoperation)
        self.tabWidget = QtWidgets.QTabWidget(self.page)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.teMel = QtWidgets.QPlainTextEdit(self.tab)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.teMel.setFont(font)
        self.teMel.setPlainText("")
        self.teMel.setObjectName("teMel")
        self.gridLayout.addWidget(self.teMel, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tePython = QtWidgets.QPlainTextEdit(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.tePython.setFont(font)
        self.tePython.setInputMethodHints(QtCore.Qt.ImhNone)
        self.tePython.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.tePython.setPlainText("")
        self.tePython.setOverwriteMode(False)
        self.tePython.setBackgroundVisible(False)
        self.tePython.setCenterOnScroll(False)
        self.tePython.setObjectName("tePython")
        self.gridLayout_2.addWidget(self.tePython, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.toolBox.addItem(self.page, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 576, 344))
        self.page_2.setObjectName("page_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.page_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.outputFilePathLabel = QtWidgets.QLabel(self.page_2)
        self.outputFilePathLabel.setObjectName("outputFilePathLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.outputFilePathLabel)
        self.rootFolderLabel = QtWidgets.QLabel(self.page_2)
        self.rootFolderLabel.setObjectName("rootFolderLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.rootFolderLabel)
        self.pbGenSceneList = QtWidgets.QPushButton(self.page_2)
        self.pbGenSceneList.setObjectName("pbGenSceneList")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.pbGenSceneList)
        self.extensionsLabel = QtWidgets.QLabel(self.page_2)
        self.extensionsLabel.setObjectName("extensionsLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.extensionsLabel)
        self.extensionsWidget = QtWidgets.QWidget(self.page_2)
        self.extensionsWidget.setObjectName("extensionsWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.extensionsWidget)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.cbMa = QtWidgets.QCheckBox(self.extensionsWidget)
        self.cbMa.setChecked(True)
        self.cbMa.setObjectName("cbMa")
        self.horizontalLayout_3.addWidget(self.cbMa)
        self.cbMb = QtWidgets.QCheckBox(self.extensionsWidget)
        self.cbMb.setChecked(True)
        self.cbMb.setObjectName("cbMb")
        self.horizontalLayout_3.addWidget(self.cbMb)
        self.cbFbx = QtWidgets.QCheckBox(self.extensionsWidget)
        self.cbFbx.setChecked(True)
        self.cbFbx.setObjectName("cbFbx")
        self.horizontalLayout_3.addWidget(self.cbFbx)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.extensionsWidget)
        self.useGeneratedListLabel = QtWidgets.QLabel(self.page_2)
        self.useGeneratedListLabel.setObjectName("useGeneratedListLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.useGeneratedListLabel)
        self.useGeneratedListCheckBox = QtWidgets.QCheckBox(self.page_2)
        self.useGeneratedListCheckBox.setChecked(True)
        self.useGeneratedListCheckBox.setObjectName("useGeneratedListCheckBox")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.useGeneratedListCheckBox)
        self.widget_2 = QtWidgets.QWidget(self.page_2)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.outputFilePathLineEdit = QtWidgets.QLineEdit(self.widget_2)
        self.outputFilePathLineEdit.setObjectName("outputFilePathLineEdit")
        self.horizontalLayout_4.addWidget(self.outputFilePathLineEdit)
        self.pbGrabFilePath = QtWidgets.QPushButton(self.widget_2)
        self.pbGrabFilePath.setObjectName("pbGrabFilePath")
        self.horizontalLayout_4.addWidget(self.pbGrabFilePath)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.widget_2)
        self.widget_3 = QtWidgets.QWidget(self.page_2)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.rootFolderLineEdit = QtWidgets.QLineEdit(self.widget_3)
        self.rootFolderLineEdit.setObjectName("rootFolderLineEdit")
        self.horizontalLayout_5.addWidget(self.rootFolderLineEdit)
        self.pbGetRootDir = QtWidgets.QPushButton(self.widget_3)
        self.pbGetRootDir.setObjectName("pbGetRootDir")
        self.horizontalLayout_5.addWidget(self.pbGetRootDir)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.widget_3)
        self.gridLayout_3.addLayout(self.formLayout, 0, 0, 1, 1)
        self.toolBox.addItem(self.page_2, "")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 569, 380))
        self.page_3.setObjectName("page_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.page_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.versionLabel = QtWidgets.QLabel(self.page_3)
        self.versionLabel.setObjectName("versionLabel")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.versionLabel)
        self.versionComboBox = QtWidgets.QComboBox(self.page_3)
        self.versionComboBox.setMinimumSize(QtCore.QSize(100, 0))
        self.versionComboBox.setObjectName("versionComboBox")
        self.versionComboBox.addItem("")
        self.versionComboBox.addItem("")
        self.versionComboBox.addItem("")
        self.versionComboBox.addItem("")
        self.versionComboBox.addItem("")
        self.versionComboBox.addItem("")
        self.versionComboBox.addItem("")
        self.versionComboBox.addItem("")
        self.versionComboBox.addItem("")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.versionComboBox)
        self.generateLogLabel = QtWidgets.QLabel(self.page_3)
        self.generateLogLabel.setObjectName("generateLogLabel")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.generateLogLabel)
        self.generateLogCheckBox = QtWidgets.QCheckBox(self.page_3)
        self.generateLogCheckBox.setObjectName("generateLogCheckBox")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.generateLogCheckBox)
        self.exportInAsciiLabel = QtWidgets.QLabel(self.page_3)
        self.exportInAsciiLabel.setObjectName("exportInAsciiLabel")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.exportInAsciiLabel)
        self.exportInAsciiCheckBox = QtWidgets.QCheckBox(self.page_3)
        self.exportInAsciiCheckBox.setChecked(True)
        self.exportInAsciiCheckBox.setObjectName("exportInAsciiCheckBox")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.exportInAsciiCheckBox)
        self.bakeResampleAnimationLabel = QtWidgets.QLabel(self.page_3)
        self.bakeResampleAnimationLabel.setObjectName("bakeResampleAnimationLabel")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.bakeResampleAnimationLabel)
        self.bakeResampleAnimationCheckBox = QtWidgets.QCheckBox(self.page_3)
        self.bakeResampleAnimationCheckBox.setChecked(False)
        self.bakeResampleAnimationCheckBox.setObjectName("bakeResampleAnimationCheckBox")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.bakeResampleAnimationCheckBox)
        self.smoothingGroupsLabel = QtWidgets.QLabel(self.page_3)
        self.smoothingGroupsLabel.setObjectName("smoothingGroupsLabel")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.smoothingGroupsLabel)
        self.smoothingGroupsCheckBox = QtWidgets.QCheckBox(self.page_3)
        self.smoothingGroupsCheckBox.setChecked(True)
        self.smoothingGroupsCheckBox.setObjectName("smoothingGroupsCheckBox")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.smoothingGroupsCheckBox)
        self.triangulateLabel = QtWidgets.QLabel(self.page_3)
        self.triangulateLabel.setObjectName("triangulateLabel")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.triangulateLabel)
        self.triangulateCheckBox = QtWidgets.QCheckBox(self.page_3)
        self.triangulateCheckBox.setChecked(False)
        self.triangulateCheckBox.setObjectName("triangulateCheckBox")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.triangulateCheckBox)
        self.smoothMeshLabel = QtWidgets.QLabel(self.page_3)
        self.smoothMeshLabel.setObjectName("smoothMeshLabel")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.smoothMeshLabel)
        self.smoothMeshCheckBox = QtWidgets.QCheckBox(self.page_3)
        self.smoothMeshCheckBox.setChecked(True)
        self.smoothMeshCheckBox.setObjectName("smoothMeshCheckBox")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.smoothMeshCheckBox)
        self.inputConnectionsLabel = QtWidgets.QLabel(self.page_3)
        self.inputConnectionsLabel.setObjectName("inputConnectionsLabel")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.inputConnectionsLabel)
        self.inputConnectionsCheckBox = QtWidgets.QCheckBox(self.page_3)
        self.inputConnectionsCheckBox.setObjectName("inputConnectionsCheckBox")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.inputConnectionsCheckBox)
        self.constraintsLabel = QtWidgets.QLabel(self.page_3)
        self.constraintsLabel.setObjectName("constraintsLabel")
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.constraintsLabel)
        self.constraintsCheckBox = QtWidgets.QCheckBox(self.page_3)
        self.constraintsCheckBox.setObjectName("constraintsCheckBox")
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.constraintsCheckBox)
        self.skinsLabel = QtWidgets.QLabel(self.page_3)
        self.skinsLabel.setObjectName("skinsLabel")
        self.formLayout_2.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.skinsLabel)
        self.skinsCheckBox = QtWidgets.QCheckBox(self.page_3)
        self.skinsCheckBox.setObjectName("skinsCheckBox")
        self.formLayout_2.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.skinsCheckBox)
        self.axisConversionMethodLabel = QtWidgets.QLabel(self.page_3)
        self.axisConversionMethodLabel.setObjectName("axisConversionMethodLabel")
        self.formLayout_2.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.axisConversionMethodLabel)
        self.axisConversionMethodComboBox = QtWidgets.QComboBox(self.page_3)
        self.axisConversionMethodComboBox.setMinimumSize(QtCore.QSize(100, 0))
        self.axisConversionMethodComboBox.setObjectName("axisConversionMethodComboBox")
        self.axisConversionMethodComboBox.addItem("")
        self.axisConversionMethodComboBox.addItem("")
        self.axisConversionMethodComboBox.addItem("")
        self.formLayout_2.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.axisConversionMethodComboBox)
        self.bakeComplexAnimationLabel = QtWidgets.QLabel(self.page_3)
        self.bakeComplexAnimationLabel.setObjectName("bakeComplexAnimationLabel")
        self.formLayout_2.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.bakeComplexAnimationLabel)
        self.bakeComplexAnimationCheckBox = QtWidgets.QCheckBox(self.page_3)
        self.bakeComplexAnimationCheckBox.setObjectName("bakeComplexAnimationCheckBox")
        self.formLayout_2.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.bakeComplexAnimationCheckBox)
        self.bakeComplexStartLabel = QtWidgets.QLabel(self.page_3)
        self.bakeComplexStartLabel.setObjectName("bakeComplexStartLabel")
        self.formLayout_2.setWidget(12, QtWidgets.QFormLayout.LabelRole, self.bakeComplexStartLabel)
        self.bakeComplexStartSpinBox = QtWidgets.QSpinBox(self.page_3)
        self.bakeComplexStartSpinBox.setObjectName("bakeComplexStartSpinBox")
        self.formLayout_2.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.bakeComplexStartSpinBox)
        self.bakeComplexStepLabel = QtWidgets.QLabel(self.page_3)
        self.bakeComplexStepLabel.setObjectName("bakeComplexStepLabel")
        self.formLayout_2.setWidget(13, QtWidgets.QFormLayout.LabelRole, self.bakeComplexStepLabel)
        self.bakeComplexStepSpinBox = QtWidgets.QSpinBox(self.page_3)
        self.bakeComplexStepSpinBox.setObjectName("bakeComplexStepSpinBox")
        self.formLayout_2.setWidget(13, QtWidgets.QFormLayout.FieldRole, self.bakeComplexStepSpinBox)
        self.bakeComplexEndLabel = QtWidgets.QLabel(self.page_3)
        self.bakeComplexEndLabel.setObjectName("bakeComplexEndLabel")
        self.formLayout_2.setWidget(14, QtWidgets.QFormLayout.LabelRole, self.bakeComplexEndLabel)
        self.bakeComplexEndSpinBox = QtWidgets.QSpinBox(self.page_3)
        self.bakeComplexEndSpinBox.setObjectName("bakeComplexEndSpinBox")
        self.formLayout_2.setWidget(14, QtWidgets.QFormLayout.FieldRole, self.bakeComplexEndSpinBox)
        self.pbResetFbxOptions = QtWidgets.QPushButton(self.page_3)
        self.pbResetFbxOptions.setMinimumSize(QtCore.QSize(150, 0))
        self.pbResetFbxOptions.setObjectName("pbResetFbxOptions")
        self.formLayout_2.setWidget(15, QtWidgets.QFormLayout.FieldRole, self.pbResetFbxOptions)
        self.pbUePreset = QtWidgets.QPushButton(self.page_3)
        self.pbUePreset.setMinimumSize(QtCore.QSize(150, 0))
        self.pbUePreset.setObjectName("pbUePreset")
        self.formLayout_2.setWidget(16, QtWidgets.QFormLayout.FieldRole, self.pbUePreset)
        self.horizontalLayout_2.addLayout(self.formLayout_2)
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setObjectName("formLayout_4")
        self.exportInstancesLabel = QtWidgets.QLabel(self.page_3)
        self.exportInstancesLabel.setObjectName("exportInstancesLabel")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.exportInstancesLabel)
        self.exportInstancesCheckBox = QtWidgets.QCheckBox(self.page_3)
        self.exportInstancesCheckBox.setObjectName("exportInstancesCheckBox")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.exportInstancesCheckBox)
        self.exportLightsLabel = QtWidgets.QLabel(self.page_3)
        self.exportLightsLabel.setObjectName("exportLightsLabel")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.exportLightsLabel)
        self.exportLightsCheckBox = QtWidgets.QCheckBox(self.page_3)
        self.exportLightsCheckBox.setObjectName("exportLightsCheckBox")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.exportLightsCheckBox)
        self.exportQuaternionLabel = QtWidgets.QLabel(self.page_3)
        self.exportQuaternionLabel.setObjectName("exportQuaternionLabel")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.exportQuaternionLabel)
        self.exportQuaternionComboBox = QtWidgets.QComboBox(self.page_3)
        self.exportQuaternionComboBox.setMinimumSize(QtCore.QSize(100, 0))
        self.exportQuaternionComboBox.setObjectName("exportQuaternionComboBox")
        self.exportQuaternionComboBox.addItem("")
        self.exportQuaternionComboBox.addItem("")
        self.exportQuaternionComboBox.addItem("")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.exportQuaternionComboBox)
        self.exportReferencedAssetsContentLabel = QtWidgets.QLabel(self.page_3)
        self.exportReferencedAssetsContentLabel.setObjectName("exportReferencedAssetsContentLabel")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.exportReferencedAssetsContentLabel)
        self.exportReferencedAssetsContentCheckBox = QtWidgets.QCheckBox(self.page_3)
        self.exportReferencedAssetsContentCheckBox.setObjectName("exportReferencedAssetsContentCheckBox")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.exportReferencedAssetsContentCheckBox)
        self.exportShapesLabel = QtWidgets.QLabel(self.page_3)
        self.exportShapesLabel.setObjectName("exportShapesLabel")
        self.formLayout_4.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.exportShapesLabel)
        self.exportShapesCheckBox = QtWidgets.QCheckBox(self.page_3)
        self.exportShapesCheckBox.setObjectName("exportShapesCheckBox")
        self.formLayout_4.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.exportShapesCheckBox)
        self.exportTangentsLabel = QtWidgets.QLabel(self.page_3)
        self.exportTangentsLabel.setObjectName("exportTangentsLabel")
        self.formLayout_4.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.exportTangentsLabel)
        self.exportTangentsCheckBox = QtWidgets.QCheckBox(self.page_3)
        self.exportTangentsCheckBox.setObjectName("exportTangentsCheckBox")
        self.formLayout_4.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.exportTangentsCheckBox)
        self.exportUpAxisLabel = QtWidgets.QLabel(self.page_3)
        self.exportUpAxisLabel.setObjectName("exportUpAxisLabel")
        self.formLayout_4.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.exportUpAxisLabel)
        self.exportUpAxisComboBox = QtWidgets.QComboBox(self.page_3)
        self.exportUpAxisComboBox.setMinimumSize(QtCore.QSize(50, 0))
        self.exportUpAxisComboBox.setObjectName("exportUpAxisComboBox")
        self.exportUpAxisComboBox.addItem("")
        self.exportUpAxisComboBox.addItem("")
        self.formLayout_4.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.exportUpAxisComboBox)
        self.hardEdgesLabel_2 = QtWidgets.QLabel(self.page_3)
        self.hardEdgesLabel_2.setObjectName("hardEdgesLabel_2")
        self.formLayout_4.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.hardEdgesLabel_2)
        self.hardEdgesCheckBox = QtWidgets.QCheckBox(self.page_3)
        self.hardEdgesCheckBox.setObjectName("hardEdgesCheckBox")
        self.formLayout_4.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.hardEdgesCheckBox)
        self.embeddedTexturesLabel_2 = QtWidgets.QLabel(self.page_3)
        self.embeddedTexturesLabel_2.setObjectName("embeddedTexturesLabel_2")
        self.formLayout_4.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.embeddedTexturesLabel_2)
        self.embeddedTexturesCheckBox = QtWidgets.QCheckBox(self.page_3)
        self.embeddedTexturesCheckBox.setObjectName("embeddedTexturesCheckBox")
        self.formLayout_4.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.embeddedTexturesCheckBox)
        self.exportCamerasLabel_2 = QtWidgets.QLabel(self.page_3)
        self.exportCamerasLabel_2.setObjectName("exportCamerasLabel_2")
        self.formLayout_4.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.exportCamerasLabel_2)
        self.exportCamerasCheckBox = QtWidgets.QCheckBox(self.page_3)
        self.exportCamerasCheckBox.setObjectName("exportCamerasCheckBox")
        self.formLayout_4.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.exportCamerasCheckBox)
        self.cacheFileLabel_2 = QtWidgets.QLabel(self.page_3)
        self.cacheFileLabel_2.setObjectName("cacheFileLabel_2")
        self.formLayout_4.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.cacheFileLabel_2)
        self.cacheFileCheckBox = QtWidgets.QCheckBox(self.page_3)
        self.cacheFileCheckBox.setObjectName("cacheFileCheckBox")
        self.formLayout_4.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.cacheFileCheckBox)
        self.applyConstantKeyReducerLabel_2 = QtWidgets.QLabel(self.page_3)
        self.applyConstantKeyReducerLabel_2.setObjectName("applyConstantKeyReducerLabel_2")
        self.formLayout_4.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.applyConstantKeyReducerLabel_2)
        self.applyConstantKeyReducerCheckBox = QtWidgets.QCheckBox(self.page_3)
        self.applyConstantKeyReducerCheckBox.setObjectName("applyConstantKeyReducerCheckBox")
        self.formLayout_4.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.applyConstantKeyReducerCheckBox)
        self.exportAnimationOnlyLabel_2 = QtWidgets.QLabel(self.page_3)
        self.exportAnimationOnlyLabel_2.setObjectName("exportAnimationOnlyLabel_2")
        self.formLayout_4.setWidget(12, QtWidgets.QFormLayout.LabelRole, self.exportAnimationOnlyLabel_2)
        self.exportAnimationOnlyCheckBox = QtWidgets.QCheckBox(self.page_3)
        self.exportAnimationOnlyCheckBox.setObjectName("exportAnimationOnlyCheckBox")
        self.formLayout_4.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.exportAnimationOnlyCheckBox)
        self.resetOptionsWidget = QtWidgets.QWidget(self.page_3)
        self.resetOptionsWidget.setObjectName("resetOptionsWidget")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.resetOptionsWidget)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.formLayout_4.setWidget(13, QtWidgets.QFormLayout.FieldRole, self.resetOptionsWidget)
        self.unrealWidget = QtWidgets.QWidget(self.page_3)
        self.unrealWidget.setObjectName("unrealWidget")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.unrealWidget)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.formLayout_4.setWidget(14, QtWidgets.QFormLayout.FieldRole, self.unrealWidget)
        self.horizontalLayout_2.addLayout(self.formLayout_4)
        self.toolBox.addItem(self.page_3, "")
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 576, 344))
        self.page_4.setObjectName("page_4")
        self.formLayoutWidget_3 = QtWidgets.QWidget(self.page_4)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 196, 68))
        self.formLayoutWidget_3.setObjectName("formLayoutWidget_3")
        self.formLayout_3 = QtWidgets.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setObjectName("formLayout_3")
        self.fontSizeLabel = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.fontSizeLabel.setObjectName("fontSizeLabel")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.fontSizeLabel)
        self.fontSizeSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget_3)
        self.fontSizeSpinBox.setProperty("value", 8)
        self.fontSizeSpinBox.setObjectName("fontSizeSpinBox")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.fontSizeSpinBox)
        self.fontWidget = QtWidgets.QWidget(self.formLayoutWidget_3)
        self.fontWidget.setObjectName("fontWidget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.fontWidget)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.fontWidget)
        self.toolBox.addItem(self.page_4, "")
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.teOutput = QtWidgets.QPlainTextEdit(self.widget)
        self.teOutput.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.teOutput.setFont(font)
        self.teOutput.setInputMethodHints(QtCore.Qt.ImhNone)
        self.teOutput.setReadOnly(True)
        self.teOutput.setPlainText("")
        self.teOutput.setObjectName("teOutput")
        self.gridLayout_4.addWidget(self.teOutput, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.splitter)
        wBatchTools.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(wBatchTools)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 594, 21))
        self.menubar.setObjectName("menubar")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        wBatchTools.setMenuBar(self.menubar)
        self.actionSet_scene_list = QtWidgets.QAction(wBatchTools)
        self.actionSet_scene_list.setObjectName("actionSet_scene_list")
        self.actionStart = QtWidgets.QAction(wBatchTools)
        self.actionStart.setObjectName("actionStart")
        self.menuEdit.addAction(self.actionSet_scene_list)
        self.menuEdit.addAction(self.actionStart)
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(wBatchTools)
        self.toolBox.setCurrentIndex(2)
        self.tabWidget.setCurrentIndex(1)
        self.versionComboBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(wBatchTools)

    def retranslateUi(self, wBatchTools):
        wBatchTools.setWindowTitle(QtCompat.translate("wBatchTools", "BatchTool", None, -1))
        self.le_SceneList.setToolTip(QtCompat.translate("wBatchTools", "used scenelist", None, -1))
        self.cbSaveoperation.setItemText(0, QtCompat.translate("wBatchTools", "SaveCurrent", None, -1))
        self.cbSaveoperation.setItemText(1, QtCompat.translate("wBatchTools", "Skip", None, -1))
        self.cbSaveoperation.setItemText(2, QtCompat.translate("wBatchTools", "SaveAsNew", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtCompat.translate("wBatchTools", "mel", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtCompat.translate("wBatchTools", "python", None, -1))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), QtCompat.translate("wBatchTools", "Batch", None, -1))
        self.outputFilePathLabel.setText(QtCompat.translate("wBatchTools", "Output file path", None, -1))
        self.rootFolderLabel.setText(QtCompat.translate("wBatchTools", "Root folder", None, -1))
        self.pbGenSceneList.setText(QtCompat.translate("wBatchTools", "generate", None, -1))
        self.extensionsLabel.setText(QtCompat.translate("wBatchTools", "Extensions", None, -1))
        self.cbMa.setText(QtCompat.translate("wBatchTools", "ma", None, -1))
        self.cbMb.setText(QtCompat.translate("wBatchTools", "mb", None, -1))
        self.cbFbx.setText(QtCompat.translate("wBatchTools", "fbx", None, -1))
        self.useGeneratedListLabel.setText(QtCompat.translate("wBatchTools", "Use generated list", None, -1))
        self.outputFilePathLineEdit.setToolTip(QtCompat.translate("wBatchTools", "<html><head/><body><p>c:/scene_list.txt</p></body></html>", None, -1))
        self.outputFilePathLineEdit.setText(QtCompat.translate("wBatchTools", "d:/ls.txt", None, -1))
        self.pbGrabFilePath.setText(QtCompat.translate("wBatchTools", "<<", None, -1))
        self.rootFolderLineEdit.setToolTip(QtCompat.translate("wBatchTools", "<html><head/><body><p>s:/Props/+folderName</p></body></html>", None, -1))
        self.rootFolderLineEdit.setText(QtCompat.translate("wBatchTools", "d:/", None, -1))
        self.pbGetRootDir.setText(QtCompat.translate("wBatchTools", "<<", None, -1))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QtCompat.translate("wBatchTools", "Scene list generator", None, -1))
        self.versionLabel.setText(QtCompat.translate("wBatchTools", "Version", None, -1))
        self.versionComboBox.setItemText(0, QtCompat.translate("wBatchTools", "FBX200611", None, -1))
        self.versionComboBox.setItemText(1, QtCompat.translate("wBatchTools", "FBX200900", None, -1))
        self.versionComboBox.setItemText(2, QtCompat.translate("wBatchTools", "FBX201000", None, -1))
        self.versionComboBox.setItemText(3, QtCompat.translate("wBatchTools", "FBX201100", None, -1))
        self.versionComboBox.setItemText(4, QtCompat.translate("wBatchTools", "FBX201200", None, -1))
        self.versionComboBox.setItemText(5, QtCompat.translate("wBatchTools", "FBX201300", None, -1))
        self.versionComboBox.setItemText(6, QtCompat.translate("wBatchTools", "FBX201400", None, -1))
        self.versionComboBox.setItemText(7, QtCompat.translate("wBatchTools", "FBX201600", None, -1))
        self.versionComboBox.setItemText(8, QtCompat.translate("wBatchTools", "FBX201800", None, -1))
        self.generateLogLabel.setText(QtCompat.translate("wBatchTools", "GenerateLog ", None, -1))
        self.exportInAsciiLabel.setText(QtCompat.translate("wBatchTools", "ExportInAscii", None, -1))
        self.bakeResampleAnimationLabel.setText(QtCompat.translate("wBatchTools", "BakeResampleAnimation", None, -1))
        self.smoothingGroupsLabel.setText(QtCompat.translate("wBatchTools", "ExportSmoothingGroups", None, -1))
        self.triangulateLabel.setText(QtCompat.translate("wBatchTools", "ExportTriangulate", None, -1))
        self.smoothMeshLabel.setText(QtCompat.translate("wBatchTools", "ExportSmoothMesh", None, -1))
        self.inputConnectionsLabel.setText(QtCompat.translate("wBatchTools", "InputConnections", None, -1))
        self.constraintsLabel.setText(QtCompat.translate("wBatchTools", "Constraints", None, -1))
        self.skinsLabel.setText(QtCompat.translate("wBatchTools", "ExportSkins", None, -1))
        self.axisConversionMethodLabel.setText(QtCompat.translate("wBatchTools", "AxisConversionMethod", None, -1))
        self.axisConversionMethodComboBox.setItemText(0, QtCompat.translate("wBatchTools", "none", None, -1))
        self.axisConversionMethodComboBox.setItemText(1, QtCompat.translate("wBatchTools", "convertAnimation", None, -1))
        self.axisConversionMethodComboBox.setItemText(2, QtCompat.translate("wBatchTools", "addFbxRoot", None, -1))
        self.bakeComplexAnimationLabel.setText(QtCompat.translate("wBatchTools", "BakeComplexAnimation", None, -1))
        self.bakeComplexStartLabel.setText(QtCompat.translate("wBatchTools", "BakeComplexStart", None, -1))
        self.bakeComplexStepLabel.setText(QtCompat.translate("wBatchTools", "BakeComplexStep", None, -1))
        self.bakeComplexEndLabel.setText(QtCompat.translate("wBatchTools", "BakeComplexEnd", None, -1))
        self.pbResetFbxOptions.setText(QtCompat.translate("wBatchTools", "maya defaults", None, -1))
        self.pbUePreset.setText(QtCompat.translate("wBatchTools", "unreal preset", None, -1))
        self.exportInstancesLabel.setText(QtCompat.translate("wBatchTools", "ExportInstances", None, -1))
        self.exportLightsLabel.setText(QtCompat.translate("wBatchTools", "ExportLights", None, -1))
        self.exportQuaternionLabel.setText(QtCompat.translate("wBatchTools", "ExportQuaternion", None, -1))
        self.exportQuaternionComboBox.setItemText(0, QtCompat.translate("wBatchTools", "quaternion", None, -1))
        self.exportQuaternionComboBox.setItemText(1, QtCompat.translate("wBatchTools", "euler", None, -1))
        self.exportQuaternionComboBox.setItemText(2, QtCompat.translate("wBatchTools", "resample", None, -1))
        self.exportReferencedAssetsContentLabel.setText(QtCompat.translate("wBatchTools", "ExportReferencedAssetsContent", None, -1))
        self.exportShapesLabel.setText(QtCompat.translate("wBatchTools", "ExportShapes", None, -1))
        self.exportTangentsLabel.setText(QtCompat.translate("wBatchTools", "ExportTangents", None, -1))
        self.exportUpAxisLabel.setText(QtCompat.translate("wBatchTools", "ExportUpAxis", None, -1))
        self.exportUpAxisComboBox.setItemText(0, QtCompat.translate("wBatchTools", "y", None, -1))
        self.exportUpAxisComboBox.setItemText(1, QtCompat.translate("wBatchTools", "z", None, -1))
        self.hardEdgesLabel_2.setText(QtCompat.translate("wBatchTools", "HardEdges", None, -1))
        self.embeddedTexturesLabel_2.setText(QtCompat.translate("wBatchTools", "EmbeddedTextures", None, -1))
        self.exportCamerasLabel_2.setText(QtCompat.translate("wBatchTools", "ExportCameras", None, -1))
        self.cacheFileLabel_2.setText(QtCompat.translate("wBatchTools", "CacheFile", None, -1))
        self.applyConstantKeyReducerLabel_2.setText(QtCompat.translate("wBatchTools", "ApplyConstantKeyReducer", None, -1))
        self.exportAnimationOnlyLabel_2.setText(QtCompat.translate("wBatchTools", "ExportAnimationOnly", None, -1))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), QtCompat.translate("wBatchTools", "Fbx export options", None, -1))
        self.fontSizeLabel.setText(QtCompat.translate("wBatchTools", "Font size", None, -1))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_4), QtCompat.translate("wBatchTools", "Tool settings", None, -1))
        self.menuEdit.setTitle(QtCompat.translate("wBatchTools", "Edit", None, -1))
        self.actionSet_scene_list.setText(QtCompat.translate("wBatchTools", "SetSceneList", None, -1))
        self.actionSet_scene_list.setShortcut(QtCompat.translate("wBatchTools", "Ctrl+Alt+Shift+N", None, -1))
        self.actionStart.setText(QtCompat.translate("wBatchTools", "Batch", None, -1))
        self.actionStart.setShortcut(QtCompat.translate("wBatchTools", "Ctrl+Alt+Shift+B", None, -1))

