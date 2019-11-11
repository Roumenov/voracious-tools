import maya.cmds as mc

def js_inv():
    
    sel = mc.ls (sl = 1)
    
    for obj in sel:
        
        selAttrs = mc.channelBox ('mainChannelBox', q = 1, sma = 1)
        
        for a in selAttrs:
            name = 'inv_%s' %a
            nice = 'inv_%s' %a
            attr = mc.addAttr (obj, ln = name, nn = nice, k = 1)
            mult = mc.createNode ('multiplyDivide', n = '%s_%s_inv_MULT' %(obj,a))
            mc.connectAttr ('%s.%s' %(obj,a), '%s.input1X' %mult)
            mc.setAttr ('%s.input2X' %mult, -1)
            mc.connectAttr ('%s.outputX' %mult, '%s.%s' %(obj,name))
        
    mc.select (sel)
    
js_inv()