'''

jsDriverModifier

'''

# Creates a series of conections that allows a driver attribute to drive another attribute according to a multiplier.

import maya.cmds as mc

def jsDM_driver():
    
    # Load driver attr
    
    getDriverTrans = mc.ls (sl = True)
    getDriverChan = mc.channelBox ('mainChannelBox', q=True, sma=True)[0]
    mc.textField (jsDM_getDriver_TF, e = True, text = '%s.%s' %(getDriverTrans[0], getDriverChan))

def jsDM_driven():

    # Load driven attr
    
    getDrivenTrans = mc.ls (sl = True)
    getDrivenChan = mc.channelBox ('mainChannelBox', q=True, sma=True)[0]
    mc.textField (jsDM_getDriven_TF, e = True, text = '%s.%s' %(getDrivenTrans[0], getDrivenChan))
    
def jsDM_execute():
    
    # Reload and clean up drivers and drivens
    
    getDriver = mc.textField (jsDM_getDriver_TF, q = True, text = True)
    getDriven = mc.textField (jsDM_getDriven_TF, q = True, text = True)
    getName = mc.textField (jsDM_name_TF, q = True, text = True)
    getLongName = getName.replace(' ', '')
    getFixedDriven = getDriven.replace('.', '_')
    getFixedDriver = getDriver.split('.')
    getFixedDriven2 = getDriven.split('.')
    
    # Some cheat variables
    
    pos_cheatLn = ('%s_pos' %getLongName)
    pos_cheatNn = ('%s +' %getName)
    
    neg_cheatLn = ('%s_neg' %getLongName)
    neg_cheatNn = ('%s -' %getName)
    
    # Add multiplier attrs
    
    mc.addAttr (getFixedDriver[0], at = 'float', ln = pos_cheatLn, nn = pos_cheatNn, k = True, dv = 1)
    mc.addAttr (getFixedDriver[0], at = 'float', ln = neg_cheatLn, nn = neg_cheatNn, k = True, dv = 1)
    
    # Create two multiply nodes and one condition node (set to 'greater or equal')
    
    cond = mc.createNode ('condition', n = '%s_%s_pos_COND' %(getFixedDriven, getLongName))
    mc.setAttr ('%s.operation' %cond, 3)
    pos_mult = mc.createNode ('multiplyDivide', n = '%s_%s_pos_MULT' %(getFixedDriven, getLongName))
    neg_mult = mc.createNode ('multiplyDivide', n = '%s_%s_neg_MULT' %(getFixedDriven, getLongName))
    
    # pos_mult = driver attr * pos multiplier attr
    
    mc.connectAttr (getDriver, '%s.input1X' %pos_mult)
    mc.connectAttr ('%s.%s_pos' %(getFixedDriver[0], getLongName), '%s.input2X' %pos_mult)
    
    # neg_mult = driver attr * neg multiplier attr
    
    mc.connectAttr (getDriver, '%s.input1X' %neg_mult)
    mc.connectAttr ('%s.%s_neg' %(getFixedDriver[0], getLongName), '%s.input2X' %neg_mult)
    
    # cond colorIfTrueR = pos_mult
    # cond colorIfFalseR = neg_mult
    
    mc.connectAttr ('%s.outputX' %pos_mult, '%s.colorIfTrueR' %cond)
    mc.connectAttr ('%s.outputX' %neg_mult, '%s.colorIfFalseR' %cond)
    
    # cond firstTerm = driver attr
    
    mc.connectAttr (getDriver, '%s.firstTerm' %cond)
    mc.connectAttr ('%s.outColorR' %cond, getDriven)
    
    # Select driver object
    
    mc.select (getFixedDriver[0])

# Create UI

jsDM_winHide = 'jsDM_createWin'
jsDM_winTitleHide = 'Driver Multiplier'
mc.windowPref (jsDM_winHide, width = 200, height = 100)

if (mc.window (jsDM_winHide, exists = True)):
    mc.deleteUI (jsDM_winHide)

mc.window (jsDM_winHide, rtf = True, width = 200, height = 100, title = jsDM_winTitleHide, s = False)
mc.columnLayout (adjustableColumn = True, rowSpacing = 2)
mc.rowColumnLayout (rowSpacing = [2,2], nc = 2)

jsDM_getDriver_TF = mc.textField (bgc = (.15,.15,.15), w=300, ed = 1, text = 'Driver Attribute')
mc.button (l = 'Pick', c = 'jsDM_driver()')

jsDM_getDriven_TF = mc.textField (bgc = (.15,.15,.15), w=300, ed = 1, text = 'Driven Attribute')
mc.button (l = 'Pick', c = 'jsDM_driven()')

mc.setParent ('..')

jsDM_name_TF = mc.textField (bgc = (.15,.15,.15), w=200, ed = 1, text = 'Attribute Name')

mc.button (l = 'Create', c = 'jsDM_execute()')

mc.showWindow (jsDM_winHide)