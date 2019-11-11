import maya.cmds as mc

sel = mc.ls (sl = 1)

for i in sel:
    mc.setAttr ('%s.tx' %i, l = 0, k = 1)
    mc.setAttr ('%s.ty' %i, l = 0, k = 1)
    mc.setAttr ('%s.tz' %i, l = 0, k = 1)
    mc.setAttr ('%s.rx' %i, l = 0, k = 1)
    mc.setAttr ('%s.ry' %i, l = 0, k = 1)
    mc.setAttr ('%s.rz' %i, l = 0, k = 1)
    mc.setAttr ('%s.sx' %i, l = 0, k = 1)
    mc.setAttr ('%s.sy' %i, l = 0, k = 1)
    mc.setAttr ('%s.sz' %i, l = 0, k = 1)