'''Connect Combo Tool by Josh Sobel'''

# UI to connect combo shapes together. Only works on attributes with a min of 0 and max of 1.
# End result is "correctiveAttr = attr1 * attr2"

import maya.cmds as mc
    
# Define button commands

def getShape1():
    global getShape1_VAR_CCT
    global getObj1_VAR_CCT
    getObj1_VAR_CCT = mc.ls (sl = True)
    getShape1_VAR_CCT = mc.channelBox ('mainChannelBox', q=True, sma=True)[0]
    mc.textField (getShape1_TF, e = True, text = getObj1_VAR_CCT[0] + '.' + getShape1_VAR_CCT)
    
def getShape2():
    global getShape2_VAR_CCT
    global getObj2_VAR_CCT
    getObj2_VAR_CCT = mc.ls (sl = True)
    getShape2_VAR_CCT = mc.channelBox ('mainChannelBox', q=True, sma=True)[0]
    mc.textField (getShape2_TF, e = True, text = getObj2_VAR_CCT[0] + '.' + getShape2_VAR_CCT)

def getCombo():
    global getCombo_VAR_CCT
    global getObj3_VAR_CCT
    getObj3_VAR_CCT = mc.ls (sl = True)
    getCombo_VAR_CCT = mc.channelBox ('mainChannelBox', q=True, sma=True)[0]
    mc.textField (getCombo_TF, e = True, text = getObj3_VAR_CCT[0] + '.' + getCombo_VAR_CCT)

def createCombo():
    global createCombo_VAR_CCT
    createCombo_VAR_CCT = mc.createNode ('multiplyDivide', n = getCombo_VAR_CCT + '_MULT')
    mc.setAttr (createCombo_VAR_CCT + ".operation", 1)
    mc.connectAttr ((getObj1_VAR_CCT[0] + "." + getShape1_VAR_CCT), (createCombo_VAR_CCT + ".input1X"))
    mc.connectAttr ((getObj2_VAR_CCT[0] + "." + getShape2_VAR_CCT), (createCombo_VAR_CCT + ".input2X"))
    mc.connectAttr ((createCombo_VAR_CCT + ".outputX"), (getObj3_VAR_CCT[0] + "." + getCombo_VAR_CCT))
    mc.select (cl = True)

    if mc.objExists (("comboMults_" + getObj3_VAR_CCT[0] + "_SET")):
        mc.sets ((getCombo_VAR_CCT + "_MULT"), add = ("comboMults_" + getObj3_VAR_CCT[0] + "_SET"))
    else:
        mc.sets (n = ("comboMults_" + getObj3_VAR_CCT[0] + "_SET"))
        mc.sets ((getCombo_VAR_CCT + "_MULT"), add = ("comboMults_" + getObj3_VAR_CCT[0] + "_SET"))

# Create UI

win = 'createWin'
winTitle = 'Connect Combo Tool'
mc.windowPref (win, width = 280, height = 106)

if (mc.window (win, exists = True)):
    mc.deleteUI (win)

mc.window (win, rtf = True, width = 280, height = 280, title = winTitle, s = False)
mc.columnLayout (adjustableColumn = True, rowSpacing = 2)

mc.text (l = ' ')
mc.text (l = '"Pick" buttons fill fields with selected attributes from the channel box.')
mc.text (l = '"Select" buttons quickly select the node that houses the picked attributes of each row.')
mc.text (l = "Getting an error? Ensure the selected attribute's parent node is the node selected.")
mc.text (l = ' ')

mc.rowLayout (cw3 = (50, 280, 40), nc = 4)
mc.text (l = 'Driver 1')
getShape1_TF = mc.textField (bgc = (.15,.15,.15), w=340, ed = 0)
mc.button (l = 'Pick', c = 'getShape1()')
mc.button (l = 'Select', c = 'mc.select (getObj1_VAR_CCT)')
mc.setParent( '..' )

mc.text (l = '      x', al = 'left')

mc.rowLayout (cw3 = (50, 280, 40), nc = 4)
mc.text (l = 'Driver 2')
getShape2_TF = mc.textField (bgc = (.15,.15,.15), w=340, ed = 0)
mc.button (l = 'Pick', c = 'getShape2()')
mc.button (l = 'Select', c = 'mc.select (getObj2_VAR_CCT)')
mc.setParent( '..' )

mc.text (l = '      =', al = 'left')
    
mc.rowLayout (cw3 = (50, 280, 40), nc = 4)
mc.text (l = 'Driven')
getCombo_TF = mc.textField (bgc = (.15,.15,.15), w=347, ed = 0)
mc.button (l = 'Pick', c = 'getCombo()')
mc.button (l = 'Select', c = 'mc.select (getObj3_VAR_CCT)')
mc.setParent( '..' )

mc.text (l = ' ')
mc.text (l = 'Click to create a multiply node that connects the values according to selection.')
mc.text (l = 'You can find the node under a set titled "comboMults_[your BS node here]_SET"')
mc.text (l = ' ')
mc.button (l = 'Create Combo', c = 'createCombo()')

mc.showWindow (win)