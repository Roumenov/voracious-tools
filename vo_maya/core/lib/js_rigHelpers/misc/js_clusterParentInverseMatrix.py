import maya.cmds as mc

objs = mc.ls (sl = True)

for obj in objs:
    out = mc.listConnections (obj, d = True)
    mc.connectAttr (obj + ".pim", out[0] + ".pm", f = True)
    mc.setAttr (out[0] + ".relative", 0)