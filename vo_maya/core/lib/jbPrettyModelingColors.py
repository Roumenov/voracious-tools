# Pretty Modeling Colors
# Joshua Buck, 2019

# import prettyModelingColors
# reload(prettyModelingColors)
# prettyModelingColors.PMCgo()

import maya.cmds as cmds
import json
import os
import sys

pmcVersionNumber = " v1.00"

def PMCgo():
    sys.stdout.write("Pretty Modeling Colors" + pmcVersionNumber + "  ||  Josh Buck, 2018  ||  cgartistry.com" + '\n')
    PMCui()
    PMCinit()



def PMCui():
    if cmds.window("PMCwin", exists=True):
        cmds.deleteUI("PMCwin", window=True)

    # if cmds.windowPref("PMCwin", exists=True):
    #     cmds.windowPref("PMCwin", remove=True)

    cmds.window("PMCwin", title="PMC" + pmcVersionNumber, minimizeButton=False, maximizeButton=False, sizeable=True)

    cmds.columnLayout("mainUI_C", p="PMCwin")

    cmds.rowColumnLayout(nc=1, cw=[(1, 150)], p="mainUI_C")
    cmds.separator(h=5, style="none")
    cmds.text(l="Pretty Modeling Colors", font="boldLabelFont", align="center")

    cmds.rowColumnLayout("paletteButtons_RCL", nc=1, cw=[(1, 150)], p="mainUI_C")

    cmds.rowColumnLayout("utilityButton_RCL", nc=3, cw=[(1, 40),(2, 85),(3, 15)], cs=[(1, 2),(2, 2),(3, 3)],
                         p="mainUI_C")

    cmds.rowColumnLayout(nc=1, cw=[(1, 141)], cs=[(1, 5)], p="mainUI_C")
    cmds.separator(h=5, style="none")

    # cmds.button(l="Write JSON", h=30, c=lambda args: writePaletteJSON())

    cmds.showWindow("PMCwin")



def PMCinit():
    loadSessionPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "PMC_palette.json")

    if os.path.exists(loadSessionPath):
        sessionFile = open(loadSessionPath)
    else:
        cmds.warning("PMC_palette.json file not found")
        fileFilter = "JSON Files (*.json)"
        loadSessionPath = cmds.fileDialog2(dialogStyle=1, fileMode=1, cap="Load Palette JSON", ff=fileFilter)
        if loadSessionPath is None:
            return None
        sessionFile = open(loadSessionPath[0])

    paletteData = json.load(sessionFile)

    # populate utility buttons layout
    cmds.optionMenu("whichPalette_OM", p="utilityButton_RCL")
    cmds.button(l="Assign Palette", c=lambda args: assignPaletteToSelected(), p="utilityButton_RCL")
    cmds.button(l="R", c=lambda args: resetDefaultColors(), p="utilityButton_RCL")

    # populate palette buttons layout
    buttonNum = 1
    for x in range(len(paletteData)):
        cmds.menuItem(label=str(x + 1), p="whichPalette_OM")
        cmds.rowColumnLayout(nc=1, cw=[(1, 150)], p="paletteButtons_RCL")
        cmds.separator(h=2, style="none")
        cmds.rowColumnLayout("pb_RCL#", nc=5, cw=[(1, 30), (2, 30), (3, 30), (4, 30), (5, 30)], p="paletteButtons_RCL")
        for palette in paletteData[x]:
            colorButton = cmds.button("pmcColor_" + str(buttonNum),  l="", h=30,
                                      bgc=normalizeRgbColor(palette[0], palette[1], palette[2]))
            cmds.button(colorButton, edit=True, c=Callback(doColorButtonPush, colorButton))
            buttonNum += 1

    cmds.menuItem(label="All", p="whichPalette_OM")
    cmds.rowColumnLayout(nc=1, cw=[(1, 150)], p="paletteButtons_RCL")
    cmds.separator(h=2, style="none")



def doColorButtonPush(colorButton):
    sel = cmds.ls(sl=True, type="transform")
    if sel == []:
        return None

    color = cmds.button(colorButton, q=True, bgc=True)
    matName = colorButton.split("|")[-1]
    matSG = createMaterialAndShadingGroup(matName, color)

    colorSelectedShape(matSG)
    shadingGroupCleanup()



def createMaterialAndShadingGroup(matName, color):
    sel = cmds.ls(sl=True, type="transform")
    if sel == []:
        return None

    if cmds.objExists(matName):
        matSG = matName + "SG"
    else:
        mat = cmds.shadingNode("lambert", asShader=True, name=matName)
        cmds.setAttr(mat + ".color", color[0], color[1], color[2])
        matSG = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=mat + "SG")
        cmds.connectAttr(mat + ".outColor", matSG + ".surfaceShader", f=True)

    cmds.select(sel, r=True)
    return(matSG)



def colorSelectedShape(matSG):
    sel = cmds.ls(sl=True, type="transform")
    if sel == []:
        return None

    for each in sel:
        shapeNode = cmds.listRelatives(each, shapes=True)
        shapeNode = shapeNode[0]
        if cmds.sets(shapeNode, isMember=matSG) is False:
            cmds.sets(shapeNode, e=True, forceElement=matSG)



def assignPaletteToSelected():
    sel = cmds.ls(sl=True, type="transform")
    if sel == []:
        return None

    buttonColumnLayouts = cmds.rowColumnLayout("paletteButtons_RCL", q=True, childArray=True)
    for each in list(buttonColumnLayouts):
        if "pb_RCL" not in each:
            buttonColumnLayouts.remove(each)

    paletteOption = cmds.optionMenu("whichPalette_OM", q=True, value=True)

    if paletteOption == "All":
        butList = []
        for each in buttonColumnLayouts:
            butList.extend(cmds.rowColumnLayout(each, q=True, childArray=True))
    else:
        paletteOption = int(paletteOption) - 1
        butList = cmds.rowColumnLayout(buttonColumnLayouts[paletteOption], q=True, childArray=True)

    x = 0
    for tform in sel:
        if x == len(butList):
            x = 0
        cmds.select(tform, r=True)
        # randButtonSelection = butList[random.randint(0, 4)]
        doColorButtonPush(butList[x])
        x += 1

    cmds.select(clear=True)
    for each in sel:
        cmds.select(each, add=True)




def resetDefaultColors():
    sel = cmds.ls(sl=True, type="transform")
    for each in sel:
        shapeNode = cmds.listRelatives(each, shapes=True)
        if cmds.sets(shapeNode, isMember="initialShadingGroup") is False:
            cmds.sets(shapeNode, e=True, forceElement="initialShadingGroup")
    shadingGroupCleanup()



def shadingGroupCleanup():
    existingShadingGroups = cmds.ls(type="shadingEngine")
    for each in list(existingShadingGroups):
        if "pmcColor_" not in each:
            existingShadingGroups.remove(each)

    for each in existingShadingGroups:
        l = cmds.listConnections(each)[-1]
        if cmds.nodeType(l) == "lambert":
            cmds.delete(each, l)


def normalizeRgbColor(colorR, colorG, colorB):
    red = round(colorR / 255.0, 5)
    green = round(colorG / 255.0, 5)
    blue = round(colorB / 255.0, 5)

    return (red, green, blue)


class Callback(object):
    def __init__( self, func, *args, **kwargs ):
        self.args = args
        self.func = func
        self.kwargs = kwargs
    def __call__(self, *args, **kwargs):
        return self.func( *self.args, **self.kwargs )



# def writePaletteJSON():
#     palette1 = [(95, 75, 81), (140, 190, 178), (242, 235, 191), (243, 181, 98), (240, 96, 96)]
#     palette2 = [(148, 59, 97), (97, 52, 140), (4, 135, 165), (235, 182, 68), (209, 71, 52)]
#     palette3 = [(138, 59, 62), (73, 121, 100), (203, 199, 123), (214, 129, 68), (182, 62, 45)]
#     palette4 = [(145, 224, 242), (162, 217, 137), (191, 188, 136), (242, 223, 126), (242, 153, 133)]
#     palette5 = [(140, 48, 55), (101, 136, 166), (2, 115, 94), (166, 148, 96), (140, 117, 104)]
#
#     fileFilter = "JSON File (*.json)"
#     saveSessionPath = cmds.fileDialog2(dialogStyle=1, fileMode=0, cap="Write Palette JSON",
#                                        ff=fileFilter)
#     if saveSessionPath is not None:
#         saveFile = open(saveSessionPath[0], 'w')
#
#         saveData = [palette1, palette2, palette3, palette4, palette5]
#
#         json.dump(saveData, saveFile, indent=4)
#
#         saveFile.close
#
#         print "File Saved: ", saveSessionPath[0]




