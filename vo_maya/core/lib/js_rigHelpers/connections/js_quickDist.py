'''Quick Distance Tool by Josh Sobel'''

# Creates two locators parented under selected objects, and places distance node under a group.
# Select two objects and run.

import maya.cmds as mc
import sys

if mc.objExists ('locator1' or 'locator2' or 'distanceDimension1'):
    mc.error ('Cannot create. "locator1" or "locator2" or "distanceDimension1" already exist')
    sys.exit()

distObjs_LIST_QDT = mc.ls (sl = True)

mc.distanceDimension (sp = (1, 1, 1), ep = (2, 2, 2))

constrain1_VAR_QDT = mc.pointConstraint (distObjs_LIST_QDT[0], 'locator1', mo = 0)
mc.delete (constrain1_VAR_QDT)

constrain1_VAR_QDT = mc.pointConstraint (distObjs_LIST_QDT[1], 'locator2', mo = 0)
mc.delete (constrain1_VAR_QDT)

mc.parent ('locator1', distObjs_LIST_QDT[0])
mc.parent ('locator2', distObjs_LIST_QDT[1])

mc.makeIdentity ('locator1', apply=True, t=1, r=1, s=1)
mc.makeIdentity ('locator2', apply=True, t=1, r=1, s=1)

loc1R_VAR_QDT = mc.rename ('locator1', (distObjs_LIST_QDT[0] + '_DLOC'))
loc2R_VAR_QDT = mc.rename ('locator2', (distObjs_LIST_QDT[1] + '_DLOC'))

if mc.objExists ('dist_GRP'):
    mc.parent ('distanceDimension1', 'dist_GRP')
else:
    mc.select (cl = True)
    mc.group (n = 'dist_GRP', w = True, em = True)
    mc.parent ('distanceDimension1', 'dist_GRP')
    
mc.rename ('distanceDimension1', distObjs_LIST_QDT[0] + '_' + distObjs_LIST_QDT[1] + '_DIST')