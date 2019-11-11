import maya.cmds as mc

def js_rev():
    
    sel = mc.ls (sl = 1)
    
    for obj in sel:
        
        selAttrs = mc.channelBox ('mainChannelBox', q = 1, sma = 1)
        
        for a in selAttrs:
            name = 'rev_%s' %a
            nice = 'rev_%s' %a
            attr = mc.addAttr (obj, ln = name, nn = nice, k = 1)
            rev = mc.createNode ('reverse', n = '%s_%s_inv_REV' %(obj,a))
            mc.connectAttr ('%s.%s' %(obj,a), '%s.inputX' %rev)
            mc.connectAttr ('%s.outputX' %rev, '%s.%s' %(obj,name))
        
    mc.select (sel)
    
js_rev()