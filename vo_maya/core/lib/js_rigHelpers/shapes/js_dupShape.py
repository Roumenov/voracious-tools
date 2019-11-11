'''Duplicate Shape Tool by Josh Sobel'''

# Replaces shapes with other shapes. Mostly used for nurbs curve controls.
# Select the transform containing the shape to copy, followed by the transform containing the shape to replace.

import maya.cmds as mc

# Get selection

selObjs_LIST_DST = mc.ls (sl = True)

# Duplicate source and move to target location

sourceTrans_VAR_DST = mc.duplicate (selObjs_LIST_DST[0], rc = True)
moveToTgt_VAR_DST = mc.parentConstraint (selObjs_LIST_DST[1], sourceTrans_VAR_DST[0], mo = False)
mc.delete (moveToTgt_VAR_DST)

# Parent source to target's parent

mc.select (selObjs_LIST_DST[1])
srcParent_VAR_DST = mc.pickWalk (d = 'up')
mc.parent (sourceTrans_VAR_DST[0], srcParent_VAR_DST[0])
mc.select (cl = True)
mc.makeIdentity (sourceTrans_VAR_DST[0], apply=True, t=1, r=1, s=1)

# Get transforms and shapes of source and target

getShapes_src_LIST_DST = mc.listRelatives (sourceTrans_VAR_DST[0], s = True)
getShapes_tgt_LIST_DST = mc.listRelatives (selObjs_LIST_DST[1], s = True)

# Parent shapes of source to target

for srcShapes in getShapes_src_LIST_DST:
    mc.parent (srcShapes, selObjs_LIST_DST[1], add = True, s = True)

# Clean up

mc.delete (sourceTrans_VAR_DST)
mc.delete (getShapes_tgt_LIST_DST)
mc.select (selObjs_LIST_DST[0])