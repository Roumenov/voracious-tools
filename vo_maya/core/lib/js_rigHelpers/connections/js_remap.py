import maya.cmds as mc

def js_remap():
    
    pos = 1
    neg = 1
    
    sel = mc.ls (sl = 1)
    
    for obj in sel:
        
        selAttrs = mc.channelBox ('mainChannelBox', q = 1, sma = 1)
        
        for a in selAttrs:
            
            if pos == 1:
                name = 'remap_%sPos' %a
                nice = 'remap_%s+' %a
                attr = mc.addAttr (obj, ln = name, nn = nice, k = 1)
                rem = mc.createNode ('remapValue', n = '%s_%sPos_REMAP' %(obj,a))
                mc.connectAttr ('%s.%s' %(obj,a), '%s.inputValue' %rem)
                #mc.setAttr ('%s.inputMax' %rem, 2.5)
                mc.connectAttr ('%s.outValue' %rem, '%s.%s' %(obj,name))
            
            if neg == 1:
                name = 'remap_%sNeg' %a
                nice = 'remap_%s-' %a
                attr = mc.addAttr (obj, ln = name, nn = nice, k = 1)
                rem = mc.createNode ('remapValue', n = '%s_%sNeg_REMAP' %(obj,a))
                mc.connectAttr ('%s.%s' %(obj,a), '%s.inputValue' %rem)
                #mc.setAttr ('%s.inputMax' %rem, -2.5)
                mc.connectAttr ('%s.outValue' %rem, '%s.%s' %(obj,name))
        
    mc.select (sel)
    
js_remap()