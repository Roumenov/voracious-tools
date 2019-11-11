#jbEngineTools   ||   Josh Buck, 2019   ||   CGARTISTRY


"""
import jbEngineTools
reload (jbEngineTools)
jbEngineTools.jbEngineToolsGo()
"""

import maya.cmds as cmds
import json
import os
import sys


jbEngineToolsOptionsJson = []

def jbEngineToolsGo():

    jbEngineToolsUI()
    loadOptionsJson()
    fillUiFieldsFromOptionsFile()


def jbEngineToolsUI():
    versionNumber = "v1.00"
    sys.stdout.write("jb Engine Tools " + versionNumber + "  ||  Josh Buck, 2019  ||  CGARTISTRY" + '\n')

    if cmds.window("jbEngineTools_WIN", exists=True):
        cmds.deleteUI("jbEngineTools_WIN", window=True)

    if cmds.windowPref("jbEngineTools_WIN", exists=True):
        cmds.windowPref('jbEngineTools_WIN', remove=True)

    cmds.window("jbEngineTools_WIN", t="jb Engine Tools  " + versionNumber, mnb=False, mxb=False, s=True)

    cmds.columnLayout("mainUI_C", p="jbEngineTools_WIN")

    # Grid Settings
    cmds.rowColumnLayout(nc=1, cw=[(1, 238)], p="mainUI_C")
    cmds.separator(height=10, style="none")
    cmds.text(label='--- G r i d ---', font="boldLabelFont")
    cmds.separator(height=5, style="none")

    cmds.rowColumnLayout(nc=2, cw=[(1, 80),(2,116)], cs=[(1,20),(2,4)], p="mainUI_C")
    cmds.text(l="Layout Presets", align="right")
    cmds.optionMenu("gridLayoutPresets_OM", cc=lambda args: setGridSize())
    cmds.separator(height=5, style="none")

    cmds.rowColumnLayout(nc=3, cw=[(1,110),(2,80),(3,16)], cs=[(1,1),(2,6),(3,2)], p="mainUI_C")
    cmds.text(l="Length and width", al="right")
    cmds.floatField('gridLengthWidth_FF', h=26, min=1.0, max=1000000.0, pre=2, step=.01, v=1000.00,
                    ec=lambda args: updateGridSize("lengthAndWidth"))
    cmds.textField("gridColorDisplayOne_TF", h=26, ed=False)

    cmds.text(l="Grid lines every", al="right")
    cmds.floatField('gridLinesEvery_FF', h=26, min=1.0, max=1000.0, pre=2, step=.01, v=100.00,
                    ec=lambda args: updateGridSize("gridLinesEvery"))
    cmds.textField("gridColorDisplayTwo_TF", h=26, ed=False)

    cmds.text(l="Subdivisions", al="right")
    cmds.intField('gridSubdivisions_IF', h=26, min=1, max=1000, v=10, ec=lambda args: updateGridSize("subdivisions"))
    cmds.textField("gridColorDisplayThree_TF", h=26, ed=False)

    cmds.rowColumnLayout(nc=1, cw=[(1, 200)], cs=[(1,20)], p="mainUI_C")
    cmds.separator(height=5, style="none")

    cmds.rowColumnLayout(nc=2, cw=[(1, 80),(2,116)], cs=[(1,20),(2,4)], p="mainUI_C")
    cmds.text(l="Colors", align="right")
    cmds.optionMenu("gridColorPresets_OM", cc=lambda args: setGridColor())

    cmds.rowColumnLayout(nc=1, cw=[(1, 238)], p="mainUI_C")
    cmds.separator(height=3, style="none")

    cmds.rowColumnLayout(nc=2, cw=[(1, 80), (2, 116)], cs=[(1, 20), (2, 4)], p="mainUI_C")
    cmds.text(l="BG Colors", align="right")
    cmds.optionMenu("backgroundColorPresets_OM", cc=lambda args: setBackgroundColor())

    # Pivot
    cmds.rowColumnLayout(nc=1, cw=[(1, 238)], p="mainUI_C")
    cmds.separator(height=10, style="in")
    cmds.text(label='--- P i v o t ---', font="boldLabelFont")
    cmds.separator(height=5, style="none")

    cmds.rowColumnLayout(nc=3, cw=[(1, 60),(2,60),(3,60)], cs=[(1,52)], p="mainUI_C")
    cmds.radioCollection('positionPivot_RC')
    pivotRbHeight = 22
    cmds.radioButton('rearLeft_RB', h=pivotRbHeight, l="")
    cmds.radioButton('rearMid_RB', h=pivotRbHeight, l="")
    cmds.radioButton('rearRight_RB', h=pivotRbHeight, l="")
    cmds.radioButton('centerLeft_RB', h=pivotRbHeight, l="")
    cmds.radioButton('centerMid_RB', h=pivotRbHeight, l="", select=True)
    cmds.radioButton('centerRight_RB', h=pivotRbHeight, l="")
    cmds.radioButton('frontLeft_RB', h=pivotRbHeight, l="")
    cmds.radioButton('frontMid_RB', h=pivotRbHeight, l="")
    cmds.radioButton('frontRight_RB', h=pivotRbHeight, l="")

    cmds.rowColumnLayout(nc=1, cw=[(1, 196)], cs=[(1,20)], p="mainUI_C")
    cmds.button(l="Set", c=lambda args: setPivot('moveToPoint'))

    cmds.rowColumnLayout(nc=1, cw=[(1, 238)], p="mainUI_C")
    cmds.separator(height=2, style="none")

    cmds.rowColumnLayout(nc=2, cw=[(1, 96), (2, 96)], cs=[(1, 20), (2, 4)], p="mainUI_C")
    cmds.button(l="Zero", c=lambda args: setPivot('zero'))
    cmds.button(l="Center", c=lambda args: setPivot("center"))

    # Object
    cmds.rowColumnLayout(nc=1, cw=[(1, 238)], p="mainUI_C")
    cmds.separator(height=10, style="in")
    cmds.text(label='--- O b j e c t ---', font="boldLabelFont")
    cmds.separator(height=5, style="none")

    cmds.radioCollection('objectTransformOptions_RC')
    cmds.rowColumnLayout(nc=1, cw=[(1, 140)], cs=[(1,60)], p="mainUI_C")
    cmds.radioButton('objectOptionTranslate_RB', l="Translate", select=True)
    cmds.rowColumnLayout(nc=2, cw=[(1, 70), (2,60)], cs=[(1, 60)], p="mainUI_C")
    cmds.radioButton('objectOptionRotate_RB', l="Rotate")
    cmds.floatField('objectRotate_FF', min=0, v=90.0, pre=2)

    cmds.rowColumnLayout(nc=1, cw=[(1, 238)], p="mainUI_C")
    cmds.separator(height=5, style="none")

    cmds.rowColumnLayout(nc=3, cw=[(1, 50), (2, 50), (3, 50)], cs=[(1, 40),(2,5),(3,5)], p="mainUI_C")
    cmds.button(l="X-", h=30, c=lambda args: transformObjects('transform', (-1.0, 0.0, 0.0 )))
    cmds.button(l="Y-", h=30, c=lambda args: transformObjects('transform', (0.0, -1.0, 0.0)))
    cmds.button(l="Z-", h=30, c=lambda args: transformObjects('transform', (0.0, 0.0, -1.0)))

    cmds.rowColumnLayout(nc=1, cw=[(1, 238)], p="mainUI_C")
    cmds.separator(height=2, style="none")

    cmds.rowColumnLayout(nc=3, cw=[(1, 50), (2, 50), (3, 50)], cs=[(1, 40), (2, 5), (3, 5)], p="mainUI_C")
    cmds.button(l="X+", h=30, c=lambda args: transformObjects('transform', (1.0, 0.0, 0.0)))
    cmds.button(l="Y+", h=30, c=lambda args: transformObjects('transform', (0.0, 1.0, 0.0)))
    cmds.button(l="Z+", h=30, c=lambda args: transformObjects('transform', (0.0, 0.0, 1.0)))

    cmds.rowColumnLayout(nc=1, cw=[(1, 238)], p="mainUI_C")
    cmds.separator(height=5, style="none")

    cmds.rowColumnLayout(nc=2, cw=[(1, 96),(2,96)],cs=[(1,20),(2,4)], p="mainUI_C")
    cmds.button(l="Center", c=lambda args: transformObjects('center', None))
    cmds.button(l="Sit", c=lambda args: transformObjects('sit', None))

    # Stack
    cmds.rowColumnLayout(nc=1, cw=[(1, 238)], p="mainUI_C")
    cmds.separator(height=10, style="in")
    cmds.text(label='--- S t a c k ---', font="boldLabelFont")
    cmds.separator(height=5, style="none")

    cmds.rowColumnLayout(nc=3, cw=[(1, 60),(2,60),(3,60)], cs=[(1,40)], p="mainUI_C")
    cmds.radioCollection('stackDirection_RC')
    cmds.radioButton('stackXpos', l="X+")
    cmds.radioButton('stackYpos', l="Y+", select=True)
    cmds.radioButton('stackZpos', l="Z+")
    cmds.radioButton('stackXneg', l="X-")
    cmds.radioButton('stackYneg', l="Y-")
    cmds.radioButton('stackZneg', l="Z-")

    cmds.rowColumnLayout(nc=1, cw=[(1, 196)], cs=[(1,20)], p="mainUI_C")
    cmds.separator(height=5, style="none")
    cmds.button(l="Stack", c=lambda args: stackObjects())

    # Align
    cmds.rowColumnLayout(nc=1, cw=[(1, 238)], p="mainUI_C")
    cmds.separator(height=10, style="in")
    cmds.text(label='--- A l i g n ---', font="boldLabelFont")
    cmds.separator(height=5, style="none")

    cmds.rowColumnLayout(nc=2, cw=[(1, 96),(2,96)],cs=[(1,20),(2,4)], p="mainUI_C")
    cmds.button(l="Position", c=lambda args: doAlign("position"))
    cmds.button(l="Orientation", c=lambda args: doAlign("orientation"))

    # Calculator
    cmds.rowColumnLayout(nc=1, cw=[(1, 238)], p="mainUI_C")
    cmds.separator(height=10, style="in")
    cmds.text(label='--- C a l c u l a t o r ---', font="boldLabelFont")
    cmds.separator(height=5, style="none")

    calcFieldHeight = 26
    cmds.rowColumnLayout( nc=4, cw=[(1, 30), (2, 65), (3, 30), (4, 65)], cs=[(1, 14), (2, 4), (3,1), (4,4)], p="mainUI_C")
    cmds.text( al="right", label="mm")
    cmds.floatField( 'cMillimeters_FF', h=calcFieldHeight, min=0, v=1*1000.0, pre=1, cc=lambda z:doCalculatorAction('mm') )
    cmds.text( al="right", label="in")
    cmds.floatField( 'cInches_FF', h=calcFieldHeight, min=0, v=1*39.3700787, pre=1, cc=lambda z:doCalculatorAction('in') )
    cmds.text( al="right", label="cm")
    cmds.floatField( 'cCentimeters_FF', h=calcFieldHeight, min=0, v=1*100.0, pre=1, cc=lambda z:doCalculatorAction('cm') )
    cmds.text( al="right", label="ft" )
    cmds.floatField( 'cFeet_FF', h=calcFieldHeight, min=0, v=1.0/3.2808399, pre=2, cc=lambda z:doCalculatorAction('ft') )
    cmds.text( al="right", label="m")
    cmds.floatField( 'cMeters_FF', h=calcFieldHeight, min=0, v=1.0, pre=3, cc=lambda z:doCalculatorAction('m') )
    cmds.text( al="right", label="yd")
    cmds.floatField( 'cYards_FF', h=calcFieldHeight, min=0, v=1*1.0936133, pre=3,  cc=lambda z:doCalculatorAction('yd') )
    cmds.text( al="right", label="km")
    cmds.floatField( 'cKilometers_FF', h=calcFieldHeight, min=0, v=1/100.0, pre=4, cc=lambda z:doCalculatorAction('km') )
    cmds.text( al="right", label="mi")
    cmds.floatField( 'cMiles_FF',h=calcFieldHeight,  min=0, v=1/1000.0, pre=4, cc=lambda z:doCalculatorAction('mi') )

    # Footer
    cmds.rowColumnLayout(nc=1, cw=[(1, 238)],  p="mainUI_C")
    cmds.separator(height=10, style="none")

    # WRITE JSON FILE
    # cmds.rowColumnLayout(nc=1, cw=[(1, 238)], p="mainUI_C")
    # cmds.separator(height=10, style="none")
    # cmds.text(label='--- WRITE JSON FILE ---', font="boldLabelFont")
    # cmds.separator(height=5, style="none")
    # cmds.button(l="Write JSON", c=lambda args: writeDataJSON())

    cmds.showWindow("jbEngineTools_WIN")


def loadOptionsJson():

    global jbEngineToolsOptionsJson

    loadSessionPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "jbEngineToolsSettings.json")

    if os.path.exists(loadSessionPath):
        sessionFile = open(loadSessionPath)
    else:
        cmds.warning("jbEngineToolsSettings.json file not found")
        fileFilter = "JSON Files (*.json)"
        loadSessionPath = cmds.fileDialog2(dialogStyle=1, fileMode=1, cap="Load jbEngineTools Settings File", ff=fileFilter)
        if loadSessionPath is None:
            return None
        sessionFile = open(loadSessionPath[0])

    jbEngineToolsOptionsJson = json.load(sessionFile)


def fillUiFieldsFromOptionsFile():
    gridLayoutPresets = jbEngineToolsOptionsJson['gridLayoutPresets']
    gridColorThemes = jbEngineToolsOptionsJson['gridColorThemes']
    backgroundColorThemes = jbEngineToolsOptionsJson['backgroundColorThemes']

    for each in gridLayoutPresets:
        cmds.menuItem(label=each[0], p="gridLayoutPresets_OM")

    for each in gridColorThemes:
        cmds.menuItem(label=each[0], p="gridColorPresets_OM")

    for each in backgroundColorThemes:
        cmds.menuItem(label=each[0], p="backgroundColorPresets_OM")


def setGridSize():
    typ = cmds.optionMenu('gridLayoutPresets_OM', q=True, v=True)

    gridLayoutPresets = jbEngineToolsOptionsJson['gridLayoutPresets']
    for each in gridLayoutPresets:
        if typ == each[0]:
            lengthAndWidth = each[1]["lengthAndWidth"]
            gridLines = each[1]["gridLines"]
            subdivisions = each[1]["subdivisions"]
            farClipPlane = each[1]["farClipPlane"]
            nearClipPlane = each[1]["nearClipPlane"]
            viewSetOption = each[1]["viewSet"]

    # set grid
    cmds.floatField('gridLengthWidth_FF', e=True, v=lengthAndWidth)
    cmds.floatField('gridLinesEvery_FF', e=True, v=gridLines)
    cmds.intField('gridSubdivisions_IF', e=True, v=subdivisions)
    cmds.grid(size=lengthAndWidth, spacing=gridLines, divisions=subdivisions)

    # set camera clipping planes
    cmds.setAttr ( 'perspShape.farClipPlane', farClipPlane )
    cmds.setAttr ( 'perspShape.nearClipPlane', nearClipPlane)
    cmds.setAttr ( 'topShape.farClipPlane', farClipPlane )
    cmds.setAttr ( 'topShape.nearClipPlane', nearClipPlane )
    cmds.setAttr ( 'sideShape.farClipPlane', farClipPlane )
    cmds.setAttr ( 'sideShape.nearClipPlane', nearClipPlane )
    cmds.setAttr ( 'frontShape.farClipPlane', farClipPlane )
    cmds.setAttr ( 'frontShape.nearClipPlane', nearClipPlane )

    if viewSetOption is True:
        cmds.viewSet(home=True, animate=True)


def updateGridSize(which):
    if which == "lengthAndWidth":
        lengthAndWidth = cmds.floatField('gridLengthWidth_FF', q=True, v=True)
        cmds.grid(size=lengthAndWidth)
        cmds.viewSet(home=True, animate=True)
    elif which == "gridLinesEvery":
        gridLines = cmds.floatField('gridLinesEvery_FF', q=True, v=True)
        cmds.grid(spacing=gridLines)
    elif which == "subdivisions":
        subdivisions = cmds.intField('gridSubdivisions_IF', q=True, v=True)
        cmds.grid(divisions=subdivisions)


def setGridColor():
    color = cmds.optionMenu('gridColorPresets_OM', q=True, v=True)
    gridColorThemes = jbEngineToolsOptionsJson['gridColorThemes']
    for each in gridColorThemes:
        if color == each[0]:
            gridAxisColor = each[1]["gridAxisColor"]
            gridHighlightColor = each[1]["gridHighlightColor"]
            gridLineColor = each[1]["gridLineColor"]

    cmds.displayColor('gridAxis', gridAxisColor, c=True, dormant=True)
    cmds.displayColor('gridHighlight', gridHighlightColor, c=True, dormant=True)
    cmds.displayColor('grid', gridLineColor, c=True, dormant=True)

    cmds.textField("gridColorDisplayOne_TF", edit=True, bgc=cmds.colorIndex(gridAxisColor, q=True))
    cmds.textField("gridColorDisplayTwo_TF", edit=True, bgc=cmds.colorIndex(gridHighlightColor, q=True))
    cmds.textField("gridColorDisplayThree_TF", edit=True, bgc=cmds.colorIndex(gridLineColor, q=True))


def setBackgroundColor():
    bgTheme = cmds.optionMenu('backgroundColorPresets_OM', q=True, v=True)
    backgroundColorThemes = jbEngineToolsOptionsJson['backgroundColorThemes']
    for each in backgroundColorThemes:
        if bgTheme == each[0]:
            background = normalizeRgbColor(each[1]["background"][0], each[1]["background"][1], each[1]["background"][2])
            backgroundTop = normalizeRgbColor(each[1]["backgroundTop"][0], each[1]["backgroundTop"][1], each[1]["backgroundTop"][2])
            backgroundBottom = normalizeRgbColor(each[1]["backgroundBottom"][0], each[1]["backgroundBottom"][1], each[1]["backgroundBottom"][2])
            displayGradient = each[1]["displayGradient"]

    cmds.displayRGBColor('background', background[0], background[1], background[2])
    cmds.displayRGBColor('backgroundTop', backgroundTop[0], backgroundTop[1], backgroundTop[2])
    cmds.displayRGBColor('backgroundBottom', backgroundBottom[0], backgroundBottom[1], backgroundBottom[2])
    cmds.displayPref (displayGradient = displayGradient)


def setPivot(doThis):
    sel = cmds.ls(sl=True)
    if not sel:
        cmds.warning("No object(s) selected")
        return None

    for each in sel:
        xmin, ymin, zmin, xmax, ymax, zmax = cmds.xform(each, query=True, ws=True, bb=True)
        if doThis == "moveToPoint":
            optn = cmds.radioCollection('positionPivot_RC', query=True, select=True)
            if optn == 'rearLeft_RB':
                cmds.xform(each, ws=True, piv=(xmin, ymin, zmin))
            elif optn == 'rearMid_RB':
                cmds.xform(each, ws=True, piv=((xmax + xmin) / 2, ymin, zmin))
            elif optn == 'rearRight_RB':
                cmds.xform(each, ws=True, piv=(xmax, ymin, zmin))
            elif optn == 'centerLeft_RB':
                cmds.xform(each, ws=True, piv=(xmin, ymin, (zmax + zmin) / 2))
            elif optn == 'centerMid_RB':
                cmds.xform(each, ws=True, piv=((xmax + xmin) / 2, ymin, (zmax + zmin) / 2))
            elif optn == 'centerRight_RB':
                cmds.xform(each, ws=True, piv=(xmax, ymin, (zmax + zmin) / 2))
            elif optn == 'frontLeft_RB':
                cmds.xform(each, ws=True, piv=(xmin, ymin, zmax))
            elif optn == 'frontMid_RB':
                cmds.xform(each, ws=True, piv=((xmax + xmin) / 2, ymin, zmax))
            elif optn == 'frontRight_RB':
                cmds.xform(each, ws=True, piv=(xmax, ymin, zmax))
        elif doThis == "zero":
            cmds.xform(each, ws=True, piv=(0, 0, 0))
        elif doThis == "center":
            cmds.xform(each, cpc=True)


def transformObjects(op, val):
    sel = cmds.ls(sl=True)
    if not sel:
        cmds.warning("No object(s) selected")
        return None

    for each in sel:
        print each
        xmin, ymin, zmin, xmax, ymax, zmax = cmds.xform(each, query=True, ws=True, bb=True)
        if op == "center":
            cmds.move(-((xmax + xmin) / 2), -((ymax + ymin) / 2), -((zmax + zmin) / 2), each, relative=True)
        elif op == "sit":
            cmds.move(-ymin, each, moveY=True, relative=True)
        elif op == "transform":
            typ = cmds.radioCollection('objectTransformOptions_RC', q=True, sl=True)
            if typ == 'objectOptionTranslate_RB':
                gridLines = cmds.floatField('gridLinesEvery_FF', q=True, v=True)
                gridSubDiv = cmds.intField('gridSubdivisions_IF', q=True, v=True)
                cmds.move(val[0] * (gridLines / gridSubDiv), val[1] * (gridLines / gridSubDiv),
                          val[2] * (gridLines / gridSubDiv), each, relative=True)
            elif typ == 'objectOptionRotate_RB':
                rotAmount = cmds.floatField('objectRotate_FF', q=True, v=True)
                cmds.rotate(val[0] * rotAmount, val[1] * rotAmount, val[2] * rotAmount, each, relative=True)


def stackObjects():
    sel = cmds.ls(sl=True)
    if not len(sel) >= 2:
        cmds.warning("Please select 2 or more objects to stack")
        return None

    stackDirection = cmds.radioCollection('stackDirection_RC', q=True, sl=True)
    for x in range(1, len(sel)):
        stackMe = sel[x]
        stackTo = sel[x-1]
        stackMeSize, stackMePos = bbCalcs(stackMe)
        stackToSize, stackToPos = bbCalcs(stackTo)
        cmds.move(-stackMePos[0], -stackMePos[1], -stackMePos[2], stackMe, relative=True)
        cmds.move(stackToPos[0], stackToPos[1], stackToPos[2], stackMe, relative=True)
        if stackDirection == "stackXpos":
            cmds.move((stackToSize[0] / 2) + (stackMeSize[0] / 2), stackMe, moveX=True, relative=True)
        elif stackDirection == "stackXneg":
            cmds.move(-(stackToSize[0] / 2) - (stackMeSize[0] / 2), stackMe, moveX=True, relative=True)
        elif stackDirection == "stackYpos":
            cmds.move((stackToSize[1] / 2) + (stackMeSize[1] / 2), stackMe, moveY=True, relative=True)
        elif stackDirection == "stackYneg":
            cmds.move(-(stackToSize[1] / 2) - (stackMeSize[1] / 2), stackMe, moveY=True, relative=True)
        elif stackDirection == "stackZpos":
            cmds.move((stackToSize[2] / 2) + (stackMeSize[2] / 2), stackMe, moveZ=True, relative=True)
        elif stackDirection == "stackZneg":
            cmds.move(-(stackToSize[2] / 2) - (stackMeSize[2] / 2), stackMe, moveZ=True, relative=True)


def doAlign(op):
    sel = cmds.ls(sl=True)
    if not len(sel) >= 2:
        cmds.warning("Please select 2 or more objects to stack")
        return None
    if op == 'position':
        for each in sel[1:]:
            alignMeSize, alignMePos = bbCalcs(each)
            alignToSize, alignToPos = bbCalcs(sel[0])
            cmds.move(-alignMePos[0], -alignMePos[1], -alignMePos[2], each, relative=True)
            cmds.move(alignToPos[0], alignToPos[1], alignToPos[2], each, relative=True)
    elif op == 'orientation':
        for each in sel[1:]:
            tempOrientConstraint = cmds.orientConstraint(sel[0], each, mo=False)
            cmds.delete(tempOrientConstraint)


def doCalculatorAction(type):
    # inches
    if type == 'in':
        cInches = cmds.floatField('cInches_FF', query=True, value=True)
        cmds.floatField('cFeet_FF', edit=True, value=cInches / 12.0)
        cmds.floatField('cYards_FF', edit=True, value=cInches / 36.0)
        cmds.floatField('cMiles_FF', edit=True, value=cInches / 63360.0)
        cmds.floatField('cMillimeters_FF', edit=True, value=cInches * 25.4)
        cmds.floatField('cCentimeters_FF', edit=True, value=cInches * 2.54)
        cmds.floatField('cMeters_FF', edit=True, value=cInches / 39.3700787)
        cmds.floatField('cKilometers_FF', edit=True, value=cInches / 39370.0787)
    # feet
    elif type == 'ft':
        cFeet = cmds.floatField('cFeet_FF', query=True, value=True)
        cmds.floatField('cInches_FF', edit=True, value=cFeet * 12.0)
        cmds.floatField('cYards_FF', edit=True, value=cFeet / 3.0)
        cmds.floatField('cMiles_FF', edit=True, value=cFeet / 5280.0)
        cmds.floatField('cMillimeters_FF', edit=True, value=cFeet * 304.8)
        cmds.floatField('cCentimeters_FF', edit=True, value=cFeet * 30.48)
        cmds.floatField('cMeters_FF', edit=True, value=cFeet / 3.2808399)
        cmds.floatField('cKilometers_FF', edit=True, value=cFeet / 3280.8399)
        # yards
    elif type == 'yd':
        cYards = cmds.floatField('cYards_FF', query=True, value=True)
        cmds.floatField('cInches_FF', edit=True, value=cYards * 36.0)
        cmds.floatField('cFeet_FF', edit=True, value=cYards * 3.0)
        cmds.floatField('cMiles_FF', edit=True, value=cYards / 1760.0)
        cmds.floatField('cMillimeters_FF', edit=True, value=cYards * 914.4)
        cmds.floatField('cCentimeters_FF', edit=True, value=cYards * 91.44)
        cmds.floatField('cMeters_FF', edit=True, value=cYards * 0.9144)
        cmds.floatField('cKilometers_FF', edit=True, value=cYards / 1093.6133)
    # miles
    elif type == 'mi':
        cMiles = cmds.floatField('cMiles_FF', query=True, value=True)
        cmds.floatField('cInches_FF', edit=True, value=cMiles * 63360.0)
        cmds.floatField('cFeet_FF', edit=True, value=cMiles * 5280.0)
        cmds.floatField('cYards_FF', edit=True, value=cMiles * 1760.0)
        cmds.floatField('cMillimeters_FF', edit=True, value=cMiles * 1609344.0)
        cmds.floatField('cCentimeters_FF', edit=True, value=cMiles * 160934.4)
        cmds.floatField('cMeters_FF', edit=True, value=cMiles * 1609.344)
        cmds.floatField('cKilometers_FF', edit=True, value=cMiles * 1.609344)
        # millimeters
    elif type == 'mm':
        cMillimeters = cmds.floatField('cMillimeters_FF', query=True, value=True)
        cmds.floatField('cInches_FF', edit=True, value=cMillimeters / 25.4)
        cmds.floatField('cFeet_FF', edit=True, value=cMillimeters / 304.8)
        cmds.floatField('cYards_FF', edit=True, value=cMillimeters / 914.4)
        cmds.floatField('cMiles_FF', edit=True, value=cMillimeters / 1609344.0)
        cmds.floatField('cCentimeters_FF', edit=True, value=cMillimeters / 10.0)
        cmds.floatField('cMeters_FF', edit=True, value=cMillimeters / 1000.0)
        cmds.floatField('cKilometers_FF', edit=True, value=cMillimeters / 1000000.0)
        # centimeters
    elif type == 'cm':
        cCentimeters = cmds.floatField('cCentimeters_FF', query=True, value=True)
        cmds.floatField('cInches_FF', edit=True, value=cCentimeters / 2.54)
        cmds.floatField('cFeet_FF', edit=True, value=cCentimeters / 30.48)
        cmds.floatField('cYards_FF', edit=True, value=cCentimeters / 91.44)
        cmds.floatField('cMiles_FF', edit=True, value=cCentimeters / 160934.4)
        cmds.floatField('cMillimeters_FF', edit=True, value=cCentimeters * 10)
        cmds.floatField('cMeters_FF', edit=True, value=cCentimeters / 100)
        cmds.floatField('cKilometers_FF', edit=True, value=cCentimeters / 1000000)
        # meters
    elif type == 'm':
        cMeters = cmds.floatField('cMeters_FF', query=True, value=True)
        cmds.floatField('cInches_FF', edit=True, value=cMeters * 39.3700787)
        cmds.floatField('cFeet_FF', edit=True, value=cMeters * 3.2808399)
        cmds.floatField('cYards_FF', edit=True, value=cMeters * 1.0936133)
        cmds.floatField('cMiles_FF', edit=True, value=cMeters / 1609.344)
        cmds.floatField('cMillimeters_FF', edit=True, value=cMeters * 1000.0)
        cmds.floatField('cCentimeters_FF', edit=True, value=cMeters * 100.0)
        cmds.floatField('cKilometers_FF', edit=True, value=cMeters / 1000.0)
        # kilometers
    elif type == 'km':
        cKilometers = cmds.floatField('cKilometers_FF', query=True, value=True)
        cmds.floatField('cInches_FF', edit=True, value=cKilometers * 39370.0787)
        cmds.floatField('cFeet_FF', edit=True, value=cKilometers * 3280.8399)
        cmds.floatField('cYards_FF', edit=True, value=cKilometers * 1093.6133)
        cmds.floatField('cMiles_FF', edit=True, value=cKilometers / 1.609344)
        cmds.floatField('cMillimeters_FF', edit=True, value=cKilometers * 1000000.0)
        cmds.floatField('cCentimeters_FF', edit=True, value=cKilometers * 100000.0)
        cmds.floatField('cMeters_FF', edit=True, value=cKilometers * 1000)


def bbCalcs(obj):
    xmin, ymin, zmin, xmax, ymax, zmax = cmds.xform(obj, query=True, ws=True, bb=True)
    xSize = abs(xmax - xmin)
    ySize = abs(ymax - ymin)
    zSize = abs(zmax - zmin)
    objectCenter = ((xmax + xmin) / 2, (ymax + ymin) / 2, (zmax + zmin) / 2)
    return (xSize, ySize, zSize), objectCenter


def normalizeRgbColor(colorR, colorG, colorB):
    red = round(colorR / 255.0, 5)
    green = round(colorG / 255.0, 5)
    blue = round(colorB / 255.0, 5)
    return red, green, blue


def writeDataJSON():
    gridLayout1 = ["Default", {"lengthAndWidth" : 12.00, "gridLines" : 5.00, "subdivisions" : 5,
                              "farClipPlane" : 10000.000, "nearClipPlane" : 0.10, "viewSet" : True}]
    gridLayout2 = ["Unreal", {"lengthAndWidth" : 1000.00, "gridLines" : 100.00, "subdivisions" : 2,
                              "farClipPlane" : 100000.000, "nearClipPlane" : 10.00, "viewSet" : True}]
    gridLayout3 = ["Unreal Detail", {"lengthAndWidth" : 500.00, "gridLines" : 100.00, "subdivisions" : 10,
                              "farClipPlane" : 10000.000, "nearClipPlane" : 0.1, "viewSet" : True}]
    gridLayout4 = ["Unity", {"lengthAndWidth" : 10.00, "gridLines" : 1.00, "subdivisions" : 2,
                              "farClipPlane" : 1000.000, "nearClipPlane" : 0.01, "viewSet" : True}]
    gridLayout5 = ["Unity Detail", {"lengthAndWidth" : 5.00, "gridLines" : 1.00, "subdivisions" : 10,
                              "farClipPlane" : 1000.000, "nearClipPlane" : 0.001, "viewSet" : True}]


    gridColorTheme1 = ["Default", {"gridAxisColor" : 2, "gridHighlightColor" : 2, "gridLineColor" : 2}]
    gridColorTheme2 = ["Highlite", {"gridAxisColor": 1, "gridHighlightColor": 3, "gridLineColor": 2}]
    gridColorTheme3 = ["Forest", {"gridAxisColor": 10, "gridHighlightColor": 23, "gridLineColor": 2}]
    gridColorTheme4 = ["Modern", {"gridAxisColor": 1, "gridHighlightColor": 4, "gridLineColor": 15}]
    gridColorTheme5 = ["Rave", {"gridAxisColor": 9, "gridHighlightColor": 14, "gridLineColor": 18}]

    backgroundColorTheme1 = ["Default", {"background" : (92, 92, 92), "backgroundTop" : (136, 157, 179),
                                      "backgroundBottom" : (13, 13, 13), "displayGradient" : True}]
    backgroundColorTheme2 = ["Surf", {"background" : (96, 90, 78), "backgroundTop" : (164, 148, 80),
                                      "backgroundBottom" : (41, 108, 138), "displayGradient" : True}]
    backgroundColorTheme3 = ["Dusk", {"background" : (85, 92, 89), "backgroundTop" : (92, 48, 123),
                                      "backgroundBottom" : (39, 103, 131), "displayGradient" : True}]
    backgroundColorTheme4 = ["Mono Dark", {"background" : (31, 31, 31), "backgroundTop" : (49, 49, 49),
                                      "backgroundBottom" : (5, 5, 5), "displayGradient" : True}]
    backgroundColorTheme5 = ["Mono Light", {"background" : (115, 115, 115), "backgroundTop" : (199, 199, 199),
                                      "backgroundBottom" : (87, 87, 87), "displayGradient" : True}]

    fileFilter = "JSON File (*.json)"
    saveSessionPath = cmds.fileDialog2(dialogStyle=1, fileMode=0, cap="Write Palette JSON",
                                       ff=fileFilter)
    if saveSessionPath is not None:
        saveFile = open(saveSessionPath[0], 'w')

        saveData = {"gridColorThemes" : [gridColorTheme1, gridColorTheme2, gridColorTheme3, gridColorTheme4,
                                         gridColorTheme5],
                    "gridLayoutPresets" : [gridLayout1, gridLayout2, gridLayout3, gridLayout4, gridLayout5],
                    "backgroundColorThemes" : [backgroundColorTheme1, backgroundColorTheme2, backgroundColorTheme3,
                                               backgroundColorTheme4, backgroundColorTheme5]}

        json.dump(saveData, saveFile, indent=4)
        saveFile.close