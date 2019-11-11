'''

jsPoseDriver

'''

# Select driver followed by object to orient pose reader to

import maya.cmds as mc

def jsPoseDriver():
    
    # Declare variables
    
    sysName = '_PD'
    nurName = '_Nrb'
    locName = '_Loc'
    grpName = '_Grp'
    
    downAxis = mc.optionMenu (jsPD_downAxis_OP, q = True, v = True)
    
    # Run command
    
    sel = mc.ls (sl = True)
    selLen = len(sel)
    
    if selLen != 2:
        
        mc.warning ('Please select 2 objects: The driver, then the object to orient the pose reader to.')
        
    else:
        
        drv = sel[0]
        par = sel[1]
        
        # Build sphere and locator
        
        sph = mc.sphere (ch = 0, n = '%s_hor%s%s' %(drv, sysName, nurName))
        
        anno = mc.annotate (sph, tx = 'H+')
        mc.setAttr ('%s.displayArrow' %anno, 0)
        mc.setAttr ('%s.template' %anno, 1)
        mc.parent (anno, sph)
        aTrans = mc.listRelatives (anno, p = 1)[0]
        aTrans = mc.rename (aTrans, '%s_hPos_Anno' %sph)
        mc.setAttr ('%s.tx' %aTrans, 1.25)
        
        anno = mc.annotate (sph, tx = 'H-')
        mc.setAttr ('%s.displayArrow' %anno, 0)
        mc.setAttr ('%s.template' %anno, 1)
        mc.parent (anno, sph)
        aTrans = mc.listRelatives (anno, p = 1)[0]
        aTrans = mc.rename (aTrans, '%s_hNeg_Anno' %sph)
        mc.setAttr ('%s.tx' %aTrans, -1.25)
        
        mc.setAttr ('%s.sx' %sph[0], .5)
        mc.setAttr ('%s.sy' %sph[0], .5)
        mc.setAttr ('%s.sz' %sph[0], .5)
        mc.makeIdentity (sph, a = True, s = 1)
        loc = mc.spaceLocator (n = '%s%s_hor%s' %(drv, sysName, locName))[0]
        loc2 = mc.spaceLocator (n = '%s%s_vert%s' %(drv, sysName, locName))[0]
        mc.setAttr ('%s.tz' %loc, -1.5)
        grp = mc.group (em = True, w = True, n = '%s%s' %(loc, grpName))
        grpOff = mc.group (em = True, w = True, n = '%s_offset%s' %(loc, grpName))
        grpSph = mc.group (em = True, w = True, n = '%s%s' %(sph[0], grpName))
        mc.parent (loc, grpOff)
        mc.parent (grpOff, grp)
        mc.parent (sph, grpSph)
        mc.makeIdentity (loc, a = True, t = 1)
        cnst = mc.parentConstraint (loc, loc2)
        mc.delete (cnst)
        mc.parent (loc2, loc)
        mc.makeIdentity (loc2, a = True, t = 1)
        mc.setAttr ('%s.v' %loc, 0)
        mc.setAttr ('%s.v' %loc2, 0)
        
        sph2 = mc.sphere (ch = 0, n = '%s_vert%s%s' %(drv, sysName, nurName))
        
        anno = mc.annotate (sph, tx = 'V+')
        mc.setAttr ('%s.displayArrow' %anno, 0)
        mc.setAttr ('%s.template' %anno, 1)
        mc.parent (anno, sph2)
        aTrans = mc.listRelatives (anno, p = 1)[0]
        aTrans = mc.rename (aTrans, '%s_vPos_Anno' %sph)
        mc.setAttr ('%s.tx' %aTrans, 1.25)
        
        anno = mc.annotate (sph, tx = 'V-')
        mc.setAttr ('%s.displayArrow' %anno, 0)
        mc.setAttr ('%s.template' %anno, 1)
        mc.parent (anno, sph2)
        aTrans = mc.listRelatives (anno, p = 1)[0]
        aTrans = mc.rename (aTrans, '%s_vNeg_Anno' %sph)
        mc.setAttr ('%s.tx' %aTrans, -1.25)        
        
        mc.setAttr ('%s.sx' %sph2[0], .5)
        mc.setAttr ('%s.sy' %sph2[0], .5)
        mc.setAttr ('%s.sz' %sph2[0], .5)
        mc.setAttr ('%s.rz' %sph2[0], 90)
        mc.makeIdentity (sph2, a = True, s = 1, r = 1)
        mc.parent (sph2, grpSph)
        
        # Build group
        
        grpMas = mc.group (em = True, w = True, n = '%s%s%s' %(drv, sysName, grpName))
        mc.parent (grp, grpSph, grpMas)
        cnst = mc.parentConstraint (drv, grpMas, mo = 0)
        mc.delete (cnst)
        
        if mc.objExists ('poseDriver%s' %grpName):
            mc.parent (grpMas, 'poseDriver%s' %grpName)
        else:
            mc.group (em = True, w = True, n = 'poseDriver%s' %grpName)
            mc.parent (grpMas, 'poseDriver%s' %grpName)
        
        # Orient system according to driver
        
        aimLoc = mc.spaceLocator (n = 'jsPD_tempAimLoc_LOC')
        mc.parent (aimLoc, drv)
        mc.setAttr ('jsPD_tempAimLoc_LOC.tx', 0)
        mc.setAttr ('jsPD_tempAimLoc_LOC.ty', 0)
        mc.setAttr ('jsPD_tempAimLoc_LOC.tz', 0)
        mc.setAttr ('jsPD_tempAimLoc_LOC.rx', 0)
        mc.setAttr ('jsPD_tempAimLoc_LOC.ry', 0)
        mc.setAttr ('jsPD_tempAimLoc_LOC.rz', 0)
        mc.makeIdentity (aimLoc, a = True, t = 1, r = 1)
        
        if downAxis == 'x+':
            mc.setAttr ('jsPD_tempAimLoc_LOC.tx', 5)
            cnst = mc.aimConstraint (aimLoc, grp, o = (0,0,0), w = 1, aim = (0,0,-1), u = (0,1,0), wut = 'objectrotation', wu = (0,1,0), wuo = drv)
            cnst2 = mc.aimConstraint (aimLoc, grpSph, o = (0,0,0), w = 1, aim = (0,0,-1), u = (0,1,0), wut = 'objectrotation', wu = (0,1,0), wuo = drv)
            mc.delete (cnst, cnst2, aimLoc)
        elif downAxis == 'x-':
            mc.setAttr ('jsPD_tempAimLoc_LOC.tx', -5)
            cnst = mc.aimConstraint (aimLoc, grp, o = (0,0,0), w = 1, aim = (0,0,-1), u = (0,0,1), wut = 'objectrotation', wu = (0,0,1), wuo = drv)
            cnst2 = mc.aimConstraint (aimLoc, grpSph, o = (0,0,0), w = 1, aim = (0,0,-1), u = (0,0,1), wut = 'objectrotation', wu = (0,0,1), wuo = drv)
            mc.delete (cnst, cnst2, aimLoc)
            mc.setAttr ('%s.rz' %sph[0], 180)
            mc.makeIdentity (sph, a = True, r = 1)
        elif downAxis == 'y+':
            mc.setAttr ('jsPD_tempAimLoc_LOC.ty', 5)
            cnst = mc.aimConstraint (aimLoc, grp, o = (0,0,0), w = 1, aim = (0,0,-1), u = (1,0,0), wut = 'objectrotation', wu = (1,0,0), wuo = drv)
            cnst2 = mc.aimConstraint (aimLoc, grpSph, o = (0,0,0), w = 1, aim = (0,0,-1), u = (1,0,0), wut = 'objectrotation', wu = (1,0,0), wuo = drv)
            mc.delete (cnst, cnst2, aimLoc)
        elif downAxis == 'y-':
            mc.setAttr ('jsPD_tempAimLoc_LOC.ty', -5)
            cnst = mc.aimConstraint (aimLoc, grp, o = (0,0,0), w = 1, aim = (0,0,-1), u = (1,0,0), wut = 'objectrotation', wu = (1,0,0), wuo = drv)
            cnst2 = mc.aimConstraint (aimLoc, grpSph, o = (0,0,0), w = 1, aim = (0,0,-1), u = (1,0,0), wut = 'objectrotation', wu = (1,0,0), wuo = drv)
            mc.delete (cnst, cnst2, aimLoc)
            mc.setAttr ('%s.rz' %sph2[0], 180)
            mc.makeIdentity (sph2, a = True, r = 1)
        elif downAxis == 'z+':
            mc.setAttr ('jsPD_tempAimLoc_LOC.tz', 5)
            cnst = mc.aimConstraint (aimLoc, grp, o = (0,0,0), w = 1, aim = (0,0,-1), u = (1,0,0), wut = 'objectrotation', wu = (1,0,0), wuo = drv)
            cnst2 = mc.aimConstraint (aimLoc, grpSph, o = (0,0,0), w = 1, aim = (0,0,-1), u = (1,0,0), wut = 'objectrotation', wu = (1,0,0), wuo = drv)
            mc.delete (cnst, cnst2, aimLoc)
            mc.setAttr ('%s.rz' %sph2[0], 180)
            mc.makeIdentity (sph2, a = True, r = 1)
        elif downAxis == 'z-':
            mc.setAttr ('jsPD_tempAimLoc_LOC.tz', -5)
            cnst = mc.aimConstraint (aimLoc, grp, o = (0,0,0), w = 1, aim = (0,0,-1), u = (1,0,0), wut = 'objectrotation', wu = (1,0,0), wuo = drv)
            cnst2 = mc.aimConstraint (aimLoc, grpSph, o = (0,0,0), w = 1, aim = (0,0,-1), u = (1,0,0), wut = 'objectrotation', wu = (1,0,0), wuo = drv)
            mc.delete (cnst, cnst2, aimLoc)
            
        # Connect some stuff and tidy
        
        mc.parentConstraint (sph[0], sph2[0])
        mc.scaleConstraint (sph[0], sph2[0])
        
        mc.setAttr ('%s.visibility' %sph[0], k = False)
        #mc.setAttr ('%s.visibility' %loc, 0)
        sph2S = mc.listRelatives (sph2, s = 1)[0]
        mc.setAttr ('%s.visibility' %sph2S, 0)
    
        mc.pointConstraint (drv, grpSph, mo = 0)
        mc.orientConstraint (par, grpSph, mo = 1)
        mc.parentConstraint (drv, grp, mo = 1)
                
        # Create nodes to connect for sphere horizontal
            
        close = mc.createNode ('closestPointOnSurface', n = '%s_hor_CLOSE' %drv)
        ucn = mc.createNode ('unitConversion', n = '%s_hor_UCN' %drv)
        ramp = mc.createNode ('ramp', n = '%s_hor_RAMP' %drv)
        remapPos = mc.createNode ('remapValue', n = '%s_hor_pos_REMAP' %drv)
        remapNeg = mc.createNode ('remapValue', n = '%s_hor_neg_REMAP' %drv)
    
        shader = mc.shadingNode ('surfaceShader', asShader = True, n = '%s%s_vert_MAT' %(drv, sysName))
        
        mc.select ('%s.sf[2][6]' %sph[0], '%s.sf[3][6]' %sph[0], '%s.sf[1][6]' %sph[0], '%s.sf[0][6]' %sph[0], '%s.sf[0][7]' %sph[0], '%s.sf[1][7]' %sph[0], '%s.sf[2][7]' %sph[0], '%s.sf[3][0]' %sph[0], '%s.sf[2][0]' %sph[0], '%s.sf[1][0]' %sph[0], '%s.sf[3][7]' %sph[0], '%s.sf[0][0]' %sph[0], '%s.sf[3][1]' %sph[0], '%s.sf[2][1]' %sph[0], '%s.sf[1][1]' %sph[0], '%s.sf[0][1]' %sph[0])
        mc.hyperShade (assign = shader)
        mc.select (cl = True)
        mc.setAttr ('%s.conversionFactor' %ucn, .25)
        mc.setAttr ('%s.type' %ramp, 1)
        
        mc.setAttr ('%s.colorEntryList[0].color' %ramp, 1, 0, 0, type = 'double3')
        mc.setAttr ('%s.colorEntryList[1].color' %ramp, 0, 0, 0, type = 'double3')
        mc.setAttr ('%s.colorEntryList[2].color' %ramp, 0, 0, 1, type = 'double3')
        
        mc.setAttr ('%s.colorEntryList[0].position' %ramp, 0)
        mc.setAttr ('%s.colorEntryList[1].position' %ramp, .5)
        mc.setAttr ('%s.colorEntryList[2].position' %ramp, 1)
        
        # Connect node network
        
        shp = mc.listRelatives (sph[0], s = True)
        locShp = mc.listRelatives (loc, s = True)
        mc.connectAttr ('%s.worldPosition[0]' %locShp[0], '%s.inPosition' %close)
        mc.connectAttr ('%s.worldSpace[0]' %shp[0], '%s.inputSurface' %close)
        mc.connectAttr ('%s.parameterU' %close, '%s.input' %ucn)
        mc.connectAttr ('%s.output' %ucn, '%s.uCoord' %ramp)
        mc.connectAttr ('%s.outColor' %ramp, '%s.outColor' %shader)
        
        mc.addAttr (sph, k = True, at = 'float', ln = 'horizontalPos')
        mc.addAttr (sph, k = True, at = 'float', ln = 'horizontalNeg')
        
        mc.connectAttr ('%s.outColorR' %ramp, '%s.inputValue' %remapNeg)
        mc.connectAttr ('%s.outColorB' %ramp, '%s.inputValue' %remapPos)
        
        mc.connectAttr ('%s.outValue' %remapPos, '%s.horizontalPos' %sph[0])
        mc.connectAttr ('%s.outValue' %remapNeg, '%s.horizontalNeg' %sph[0])
        
        # Create nodes to connect for sphere vertical
            
        close2 = mc.createNode ('closestPointOnSurface', n = '%s_vert_CLOSE' %drv)
        ucn2 = mc.createNode ('unitConversion', n = '%s_vert_UCN' %drv)
        ramp2 = mc.createNode ('ramp', n = '%s_vert_RAMP' %drv)
        remapPos2 = mc.createNode ('remapValue', n = '%s_vert_pos_REMAP' %drv)
        remapNeg2 = mc.createNode ('remapValue', n = '%s_vert_neg_REMAP' %drv)
    
        shader2 = mc.shadingNode ('surfaceShader', asShader = True, n = '%s%s_hor_MAT' %(drv, sysName))
        
        mc.select ('%s.sf[2][6]' %sph2[0], '%s.sf[3][6]' %sph2[0], '%s.sf[1][6]' %sph2[0], '%s.sf[0][6]' %sph2[0], '%s.sf[0][7]' %sph2[0], '%s.sf[1][7]' %sph2[0], '%s.sf[2][7]' %sph2[0], '%s.sf[3][0]' %sph2[0], '%s.sf[2][0]' %sph2[0], '%s.sf[1][0]' %sph2[0], '%s.sf[3][7]' %sph2[0], '%s.sf[0][0]' %sph2[0], '%s.sf[3][1]' %sph2[0], '%s.sf[2][1]' %sph2[0], '%s.sf[1][1]' %sph2[0], '%s.sf[0][1]' %sph2[0])
        mc.hyperShade (assign = shader2)
        mc.select (cl = True)
        mc.setAttr ('%s.conversionFactor' %ucn2, .25)
        mc.setAttr ('%s.type' %ramp2, 1)
        
        mc.setAttr ('%s.colorEntryList[0].color' %ramp2, 1, 0, 0, type = 'double3')
        mc.setAttr ('%s.colorEntryList[1].color' %ramp2, 0, 0, 0, type = 'double3')
        mc.setAttr ('%s.colorEntryList[2].color' %ramp2, 0, 0, 1, type = 'double3')
        
        mc.setAttr ('%s.colorEntryList[0].position' %ramp2, 0)
        mc.setAttr ('%s.colorEntryList[1].position' %ramp2, .5)
        mc.setAttr ('%s.colorEntryList[2].position' %ramp2, 1)
        
        # Connect node network
        
        shp2 = mc.listRelatives (sph2[0], s = True)
        mc.connectAttr ('%s.worldPosition[0]' %locShp[0], '%s.inPosition' %close2)
        mc.connectAttr ('%s.worldSpace[0]' %shp2[0], '%s.inputSurface' %close2)
        mc.connectAttr ('%s.parameterU' %close2, '%s.input' %ucn2)
        mc.connectAttr ('%s.output' %ucn2, '%s.uCoord' %ramp2)
        mc.connectAttr ('%s.outColor' %ramp2, '%s.outColor' %shader2)
        
        mc.addAttr (sph, k = True, at = 'float', ln = 'verticalPos')
        mc.addAttr (sph, k = True, at = 'float', ln = 'verticalNeg')
        
        mc.connectAttr ('%s.outColorR' %ramp2, '%s.inputValue' %remapNeg2)
        mc.connectAttr ('%s.outColorB' %ramp2, '%s.inputValue' %remapPos2)

        mc.connectAttr ('%s.outValue' %remapPos2, '%s.verticalPos' %sph[0])
        mc.connectAttr ('%s.outValue' %remapNeg2, '%s.verticalNeg' %sph[0])
        
        # Fix naming
        
        toRen = mc.ls ('%s%s_hor_offset_Loc*' %(sel[0],sysName), tr = 1)
        for i in toRen:
            new = i.replace ('hor_', '')
            mc.rename (i, new)
            
        toRen = mc.ls ('%s*_Loc_Loc*' %sel[0], tr = 1)
        for i in toRen:
            new = i.replace ('Loc_Loc', 'surf_Loc')
            mc.rename (i, new)
            
        toRen = mc.ls ('*%s%s%s|%s%s%s' %(sel[0],sysName,locName,sel[0],sysName,locName), tr = 1)
        print toRen
        for i in toRen:
            spl = i.split ('|')
            endInd = len(spl)-1
            new = spl[endInd].replace ('%s' %locName, '_surf%s' %locName)
            mc.rename (i, new)
    
        toRen = mc.ls ('%s_hor%s%s%s*' %(sel[0],sysName,nurName,grpName), tr = 1)
        for i in toRen:
            new = i.replace ('_hor', '')
            mc.rename (i, new)
        
        toRen = mc.ls ('*%s*___*_Anno' %sel[0], tr = 1)
        for i in toRen:
            new = i.replace ('___', '_')
            mc.rename (i, new)
        
        
# Create UI

jsPD_winHide = 'jsPD_createWin'
jsPD_winTitleHide = 'Pose Driver'
mc.windowPref (jsPD_winHide, width = 100, height = 10)

if (mc.window (jsPD_winHide, exists = True)):
    mc.deleteUI (jsPD_winHide)

mc.window (jsPD_winHide, rtf = True, width = 200, height = 100, title = jsPD_winTitleHide, s = True)
mc.columnLayout (adjustableColumn = True, rowSpacing = 2)

mc.text (' ', h = 8)
mc.text ('Select the driver, then the object to orient the pose reader to.')
mc.text (' ', h = 8)

mc.rowColumnLayout (rowSpacing = [2,2], nc = 3)
mc.text ('                                   ')
jsPD_downAxis_OP = mc.optionMenu (l = 'Down Axis:')
mc.menuItem (l = 'x+')
mc.menuItem (l = 'x-')
mc.menuItem (l = 'y+')
mc.menuItem (l = 'y-')
mc.menuItem (l = 'z+')
mc.menuItem (l = 'z-')
mc.text ('                                      ')

mc.setParent ('..')

mc.text (' ', h = 8)
mc.button (l = 'Create', c = lambda x:jsPoseDriver())

mc.showWindow (jsPD_winHide)