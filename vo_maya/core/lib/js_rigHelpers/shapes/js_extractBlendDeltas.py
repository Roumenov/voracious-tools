# jsExtractBlendDeltas

# Extracts deltas between two shapes. Will not accurately take skinning into consideration.
# Select corrective mesh first and posed mesh second.


import maya.cmds as mc


def jsBlendDeltas():
    
    bs = mc.textField (jsBD_bs_TF, q = 1, tx = True)
    offset = 10
    addToBs = mc.checkBox (addToBs_CB, q = True, v = True)
    name = mc.textField (jsBD_name_TF, q = 1, tx = True)
    name = name.replace (' ', '_')
    name = name.replace ('.', '_')
    
    # List meshes
    selMeshes = mc.ls (sl = True)
    
    # Duplicate corrective mesh and posed mesh
    corr = mc.duplicate (selMeshes[0], n = "jsEBD_corrective")
    posed = mc.duplicate (selMeshes[1], n = "jsEBD_posed")
    mc.setAttr ("jsEBD_posed.tx", l = False)
    mc.setAttr ("jsEBD_posed.ty", l = False)
    mc.setAttr ("jsEBD_posed.tz", l = False)
    
    # Set envelopes to 0
    
    hist = mc.listHistory (selMeshes[1], pdo = True)
    skin = mc.ls (hist, type = 'skinCluster')
    skinLen = len(skin)
    
    blends = mc.ls (hist, type = 'blendShape')
    print blends
    blendsLen = len(blends)
    
    if blendsLen != 0:
        for node in blends:
            mc.setAttr (node + ".envelope", 0)
    
    if skinLen == 1:
        mc.setAttr (skin[0] + ".envelope", 0)
    
    # Duplicate default mesh
    default = mc.duplicate (selMeshes[1], n = "jsEBD_default")
    mc.setAttr ("jsEBD_default.tx", l = False)
    mc.setAttr ("jsEBD_default.ty", l = False)
    mc.setAttr ("jsEBD_default.tz", l = False)
    
    # Extract deltas
    bsn = mc.blendShape (corr, posed, default, n = "jsBD_BS")
    mc.setAttr (bsn[0] + '.' + corr[0], 1)
    mc.setAttr (bsn[0] + '.' + posed[0], -1)
    newMesh = mc.duplicate (default, n = name)
    mc.delete (corr, posed, default)
    
    # Move result
    getTX = mc.getAttr (selMeshes[0] + ".tx")
    mc.setAttr (newMesh[0] + ".tx", getTX - offset)
    getTY = mc.getAttr (selMeshes[0] + ".ty")
    mc.setAttr (newMesh[0] + ".ty", getTY)
    
    # Set envelopes to 1    
    if blendsLen != 0:
        for node in blends:
            mc.setAttr (node + ".envelope", 1)
    
    if skinLen == 1:
        mc.setAttr (skin[0] + ".envelope", 1)
    
    if addToBs == 1:        
        # Create blend shape
        targetIndex = mc.aliasAttr (bs, q = True)
        indexLen = len(targetIndex)
        mc.blendShape (bs, e = True, t = (selMeshes[1], indexLen/2, newMesh[0], 1.0))




def jsBD_loadBs():
    
    sel = mc.ls (sl = True)
    mc.textField (jsBD_bs_TF, e = True, tx = sel[0])


def jsBD_selBs():
    
    toSel = mc.textField (jsBD_bs_TF, q = True, tx = True)
    mc.select (toSel)


# Create UI


jsBD_winHide = 'jsBD_createWin'
jsBD_winTitleHide = 'Extract Blend Deltas'
mc.windowPref (jsBD_winHide, width = 10, height = 10)


if (mc.window (jsBD_winHide, exists = True)):
    mc.deleteUI (jsBD_winHide)


mc.window (jsBD_winHide, rtf = True, width = 280, height = 150, title = jsBD_winTitleHide, s = True)
mc.columnLayout (adjustableColumn = True, rowSpacing = 2)


jsBD_name_TF = mc.textField (bgc = (.15,.15,.15), w=210, ed = 1, cc = 'jsBD_loadBs', text = 'Combo Shape Name')


mc.rowColumnLayout (rowSpacing = [2,2], nc = 2)
mc.text ('                      ')
addToBs_CB = mc.checkBox (l = 'Auto add to blend shape:', v = 1)
mc.setParent ('..')


mc.rowColumnLayout (rowSpacing = [2,2], nc = 4)
jsBD_bs_TF = mc.textField (bgc = (.15,.15,.15), w=200, ed = 1, text = 'Blend Shape Node')
mc.button (l = 'Load', c = 'jsBD_loadBs()')
mc.text (' ')
mc.button (l = 'Select', c = 'jsBD_selBs()')
mc.setParent ('..')


mc.button (l = 'Extract', c = 'jsBlendDeltas()')


mc.showWindow (jsBD_winHide)