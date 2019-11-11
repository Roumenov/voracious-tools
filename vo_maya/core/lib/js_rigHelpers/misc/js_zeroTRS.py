import maya.cmds as mc
import re

objs = mc.ls (sl=True, transforms=True)
for list in objs:
    attrs = mc.listAttr (list, u=True, k=True)
    
    for t in attrs:
        if re.match ('translate*', t):
            mc.setAttr (list+'.'+t, 0)
            
    for r in attrs:
        if re.match ('rotate*', r):
            mc.setAttr (list+'.'+r, 0)

    for s in attrs:
        if re.match ('scale*', s):
            mc.setAttr (list+'.'+s, 1)