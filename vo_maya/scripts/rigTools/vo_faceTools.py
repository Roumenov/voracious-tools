import pymel.core as pm
import vo_usefulFunctions as uf
reload(uf)

#gets weird if things are scaled
def make_proxy_pivot(name, target):
    target_position = pm.xform(target, worldSpace = True)
    #target_parent
    pm.select(target, replace = True)
    pivot_root = pm.ls(sl=1)[0]
    pm.select(clear = True)
    
    #pm.addAttr(pivot_root, longName = 'proxy', attributeType = 'message')
    pivot_target = pm.spaceLocator(name = name + '_pivotTarget')
    pm.addAttr(pivot_target, longName = 'metaParent', attributeType = 'message')
    pm.addAttr(pivot_target, longName = 'rigPivot', shortName = 'rpv', attributeType = 'message')
    pm.addAttr(longName = 'radiusFactor', shortName = 'radf', attributeType = 'double', dv = 1.0)
    pivot_target.setAttr('radiusFactor', keyable = True, channelBox = True)
    pivot_target.setAttr('radiusFactor', keyable = True, channelBox = True)
    joint_target = pm.spaceLocator(name = name + '_jointTarget')
    pm.addAttr(joint_target, longName = 'metaParent', attributeType = 'message')
    pm.addAttr(joint_target, longName = 'jointSkinTarget', shortName = 'sjt', attributeType = 'message')
    #make visualizations
    axial_ring = pm.circle(name = name + '_axialRing', constructionHistory = True, normalY = 1.0, normalZ = 0)
    #pm.addAttr(axial_ring, longName = 'metaParent', attributeType = 'message')
    #axial_ring[0].setAttr('axialPlane', keyable = True, channelBox = True)
    ring_construction = axial_ring[0].listHistory()[1]
    arrow_viz = uf.create_object(objName = name + '_arrow', objType = 'arrowX')
    #pm.curve(name = , degree = 1, point = [(0,0,0), (0,0,13), (0,1,11), (0,-1,11), (0,0,13), (1,0,11), (-1,0,11), (0,0,13)], knot =[0,1,2,3,4,5,6,7])
    sphere_viz = pm.sphere(name = name + '_sphereViz', axis = [0,1,0])
    sphere_construction = sphere_viz[0].listHistory()[1]
    proxy_distance_measure = pm.shadingNode('distanceBetween', name = name+'_distanceBetween', asUtility = True)
    #proxy_distance_factor = pm.shadingNode('plusMinusAverage', name = name+'_plusMinAvg', asUtility = True)
    proxy_distance_factor = pm.shadingNode('floatMath', name = name+'_sphereFactor', asUtility = True)
    proxy_distance_factor.setAttr('operation', 2)
    proxy_ring_mult = pm.shadingNode('floatMath', name = name+'_floatMult', asUtility = True)
    proxy_ring_mult.setAttr('operation', 2)
    proxy_ring_mult.setAttr('floatB', 1.1)
    pivot_target.worldPosition >> proxy_distance_measure.point1
    joint_target.worldPosition >> proxy_distance_measure.point2
    proxy_distance_measure.distance >> proxy_distance_factor.floatA
    pivot_target.radiusFactor >> proxy_distance_factor.floatB
    proxy_distance_factor.outFloat >> sphere_construction.radius
    proxy_distance_factor.outFloat >> proxy_ring_mult.floatA
    print('ring construction node ::')
    print(ring_construction)
    proxy_ring_mult.outFloat >> ring_construction.radius
    #wrap everything in structure under root
    pivot_target.addChild(arrow_viz.getShape(), relative = True, shape = True)
    pivot_target.addChild(axial_ring[0].getShape(), relative = True, shape = True)
    pivot_target.addChild(sphere_viz[0].getShape(), relative = True, shape = True)
    pivot_target.setAttr('rotateOrder', 2)
    pm.matchTransform(pivot_target, pivot_root, scale = False)
    pm.matchTransform(joint_target, pivot_root, scale = False)
    pm.select(joint_target, pivot_target, replace = True)
    pm.move(pivot_target, [-7,0,0])
    pm.aimConstraint(maintainOffset = True, weight = 1, aimVector = [1,0,0], upVector = [0,1,0], worldUpType = "vector", worldUpVector = [0,1,0], skip = 'x')
    #place
    pm.delete(arrow_viz, axial_ring[0], sphere_viz[0])
    pivot_root | pivot_target
    pivot_root | joint_target
    if pivot_root.hasAttr('metaParent'):
        #pivot_root.metaParent >> pivot_target.rigPivot
        print('metaParent attr exists')
    else:
        print('adding metaParent attr')
        pm.addAttr(pivot_root, longName = 'metaParent', attributeType = 'message')
    pivot_root.metaParent >> pivot_target.metaParent
    pivot_root.metaParent >> joint_target.metaParent
    pm.select(pivot_root, replace = True)
    return pivot_root






#from http://chrislesage.com/character-rigging/manually-create-maya-follicle-in-python/
#create single folllicle:
#oFoll = create_follicle(pm.selected()[0], 0.5, 0.5)

#loop across surface:
#follicleCount = 8
#for i in range(0,follicleCount):
#    oFoll = create_follicle(myObject, i/(follicleCount-1.00), 0.5)
def create_follicle(oNurbs, uPos=0.0, vPos=0.0):
    """manually place and connect a follicle onto a nurbs surface."""
    if oNurbs.type() == 'transform':
        oNurbs = oNurbs.getShape()
    elif oNurbs.type() == 'nurbsSurface':
        pass
    else:
        'Warning: Input must be a nurbs surface.'
        return False

    # create a name with frame padding
    pName = '_'.join((oNurbs.name(),'follicle','#'.zfill(2)))
    oFoll = pm.createNode('follicle', name=pName)
    oNurbs.local.connect(oFoll.inputSurface)
    # if using a polygon mesh, use this line instead.
    # (The polygons will need to have UVs in order to work.)
    #oMesh.outMesh.connect(oFoll.inMesh)

    oNurbs.worldMatrix[0].connect(oFoll.inputWorldMatrix)
    oFoll.outRotate.connect(oFoll.getParent().rotate)
    oFoll.outTranslate.connect(oFoll.getParent().translate)
    oFoll.parameterU.set(uPos)
    oFoll.parameterV.set(vPos)
    oFoll.getParent().t.lock()
    oFoll.getParent().r.lock()

    return oFoll



#example:
#ab_build_ribbon(start='locator1', end='locator2', match = 'all', segments = 8, ribbonName = 'upperLip')
#changed attribute connection to connect ribbon_rootGRP.metaParent to all children instead of .ribbon

def build_ribbon(start = '', end = '', match = 'all', segments = 6, ribbonName = 'ribbon'):
    ribbon_rootName = ribbonName #+'_RBN'
    ribbon_distance_measure = pm.shadingNode('distanceBetween', name = ribbon_rootName+'_distance', asUtility = True)
    start_matrix = pm.shadingNode('decomposeMatrix', name = ribbon_rootName+'_start_matrix', asUtility = True)
    end_matrix = pm.shadingNode('decomposeMatrix', name = ribbon_rootName+'_end_matrix', asUtility = True)
    pm.connectAttr(start+'.worldMatrix', start_matrix+'.inputMatrix')
    pm.connectAttr(start_matrix+'.outputTranslate', ribbon_distance_measure+'.point1')
    pm.connectAttr(end+'.worldMatrix', end_matrix+'.inputMatrix')
    pm.connectAttr(end_matrix+'.outputTranslate', ribbon_distance_measure+'.point2')
    ribbon_length = pm.getAttr(ribbon_distance_measure+'.distance')
    ribbon_length_ratio = ribbon_length/(ribbon_length * segments)
    ribbonGEO = pm.nurbsPlane(name = ribbon_rootName+'_GEO', axis = [0,1,0], width = ribbon_length, lengthRatio = ribbon_length_ratio, degree = 3, patchesU = segments, patchesV = 1, constructionHistory = 0)
    ribbonGEO = ribbonGEO[0]
    pm.addAttr(ribbonGEO, longName = 'metaParent', attributeType = 'message')
    pm.addAttr(ribbonGEO, shortName = 'rbn', longName = 'ribbon', attributeType = 'message')
    ribbon_rootGRP = pm.group(name = ribbon_rootName+'_GRP')
    pm.addAttr(ribbon_rootGRP, longName = 'metaParent', attributeType = 'message')
    pm.addAttr(ribbon_rootGRP, shortName = 'rbn', longName = 'ribbon', attributeType = 'message') ##---- connect with tagger
    pm.addAttr(ribbon_rootGRP, longName = 'ribbonSegments', attributeType = 'long', defaultValue = segments)
    pm.addAttr(ribbon_rootGRP, longName = 'rigPart', attributeType = 'message')
    ribbon_rootGRP.metaParent >> ribbonGEO.metaParent
    print 'making ribbon drive joints'
    #connect to face rig or lower face, whatever is the closest rig part
    startJointTrans = pm.xform(start, q=True, ws=True, translation=True)
    endJointTrans = pm.xform(end, q=True, ws=True, translation=True)
    midJointTrans = uf.average_position(start,end)
    
    drive_joint_list = []
    ##pm.setAttr(jointName + '.drawStyle' = 2) hide joints
    pm.select(clear = True)
    startJoint = pm.joint(name = ribbonName+ '_RBN_start_J', relative = True, radius = 2, position = startJointTrans)
    pm.addAttr(startJoint, longName = 'metaParent', attributeType = 'message')
    pm.addAttr(startJoint, shortName = 'rbn', longName = 'ribbon', attributeType = 'message')
    pm.makeIdentity(startJoint, apply = True, rotate = True)
    drive_joint_list = drive_joint_list + [startJoint]
    ribbon_rootGRP.metaParent >> startJoint.metaParent
    pm.select(clear = True)
    endJoint = pm.joint(name = ribbonName+ '_RBN_end_J', relative = True, radius = 2, position = endJointTrans)
    pm.addAttr(endJoint, longName = 'metaParent', attributeType = 'message')
    pm.addAttr(endJoint, longName = 'ribbon', attributeType = 'message')
    pm.makeIdentity(endJoint, apply = True, rotate = True)
    drive_joint_list = drive_joint_list + [endJoint]
    ribbon_rootGRP.metaParent >> endJoint.metaParent
    pm.select(clear = True)
    midJoint = pm.joint(name = ribbonName+ '_RBN_mid_J', relative = True, radius = 2, position = midJointTrans)
    pm.addAttr(midJoint, longName = 'metaParent', attributeType = 'message')
    pm.addAttr(midJoint, shortName = 'rbn', longName = 'ribbon', attributeType = 'message')
    drive_joint_list = drive_joint_list + [midJoint]
    ribbon_rootGRP.metaParent >> midJoint.metaParent
    driver_group = uf.nest_transform(name = ribbon_rootName + '_drivers_GRP', action = 'parent', target = midJoint, transformObj = 'group')
    driver_group | startJoint
    driver_group | endJoint
    pm.select(clear = True)
    
    midEndTrans = uf.average_position(midJoint,end)
    midEndJoint = pm.joint(name = ribbonName+ '_RBN_mid_end_J', relative = True, radius = 2, position = midEndTrans)
    pm.addAttr(midEndJoint, longName = 'metaParent', attributeType = 'message')
    pm.addAttr(midEndJoint, longName = 'ribbon', attributeType = 'message')
    pm.makeIdentity(endJoint, apply = True, rotate = True)
    drive_joint_list = drive_joint_list + [midEndJoint]
    ribbon_rootGRP.metaParent >> midEndJoint.metaParent
    driver_group | midEndJoint
    pm.select(clear = True)
    
    midStartTrans = uf.average_position(midJoint,start)
    midStartJoint = pm.joint(name = ribbonName+ '_RBN_mid_start_J', relative = True, radius = 2, position = midStartTrans)
    pm.addAttr(midStartJoint, longName = 'metaParent', attributeType = 'message')
    pm.addAttr(midStartJoint, longName = 'ribbon', attributeType = 'message')
    pm.makeIdentity(startJoint, apply = True, rotate = True)
    drive_joint_list = drive_joint_list + [midStartJoint]
    ribbon_rootGRP.metaParent >> midStartJoint.metaParent
    driver_group | midStartJoint
    
    pm.select(clear = True)
    for driver in drive_joint_list:
        current_group_name = str(driver).replace('_J', '_GRP')
        current_group = uf.nest_transform(name = current_group_name, action = 'parent', target = driver, transformObj = 'group')
    pm.select(clear = True)
    #move everything into position
    pm.xform(ribbon_rootGRP, translation = midJointTrans, worldSpace = True)
    ##---- skin to nurbs curve
    pm.select(drive_joint_list, ribbonGEO)
    pm.skinCluster(toSelectedBones = True, bindMethod = 0, normalizeWeights = 1, weightDistribution = 0, maximumInfluences = 2, obeyMaxInfluences = True, skinMethod = 1, dropoffRate = 2, removeUnusedInfluence = False)
    ##----
    
    # Propagate follicles
    print('making follicles and skin joints')
    follicle_list = []
    ribbon_locator_list = []
    current_name = ''
    for i in range(segments):
        uPosition_factor = 1/float(segments)
        currentUposition = uPosition_factor * (float(i)+0.5)
        print 'follicle'
        last_follicle = create_follicle(oNurbs = ribbonGEO, uPos=currentUposition, vPos = 0.5)
        print('last follicle = ' + last_follicle.getParent())
        pm.addAttr(last_follicle, longName = 'metaParent', attributeType = 'message')
        pm.addAttr(last_follicle, shortName = 'rbn', longName = 'ribbon', attributeType = 'message')
        ribbon_rootGRP.metaParent >> last_follicle.metaParent
        follicle_list.append(last_follicle)
        if i == (segments/2):
            currentSide = 'C_'
        elif i < (segments/2):
            currentSide = 'R_'
        else:
            currentSide = 'L_'
        current_name = currentSide + ribbon_rootName
        #currentJointName = currentSide + current_name
        print( current_name)
        current_locator = uf.nest_transform(name = current_name+'_LOC', action = 'child', target = last_follicle.getParent(), transformObj = 'locator')
        current_group = uf.nest_transform(name = current_name + '_GRP', action = 'parent', target = current_locator, transformObj = 'group')
        pm.addAttr(current_locator, shortName = 'rbn', longName = 'ribbon', attributeType = 'message')
        ribbon_locator_list = ribbon_locator_list + [current_locator]
        ribbon_rootGRP.metaParent >> current_locator.metaParent
    
    if match == 'all': ##---- expand matching options later
        pass
        #print('creating clusters')
        #match cluster to each proxy ----------- ASSUMES 8 SEGMENTS ON LIPS!!!!!!!!!!
        #pm.select(ribbonGeo+'.cv[0:2][0:3]', replace = True)
        #rbnCluster01 = pm.cluster(name = 'rbnCluster01', relative = True, envelope = 1)
        # and all the sets in between
        #pm.select(ribbonGeo+'.cv[8:10][0:3]', replace = True)
        #rbnCluster08 = pm.cluster(name = 'rbnCluster08', relative = True, envelope = 1)
        #pm.select(clear = 1)
        #print('making joints per follicle')
        #rotate created skin joints -90 on ry
        #place skin joint on each follicle
    elif match == 'bounds':
        pass
        #print('match start/end bounds only')
    elif match == 'start':
        pass
        #print('match start only')
    elif match == 'end':
        pass
        #print('match end only')
    ribbonRef = ribbon_rootGRP

    return ribbonRef




def super_ribbon(start = '', end = '', segments = 5, ribbonName = 'ribbon'):
    ribbon_rootName = ribbonName #+'_RBN'
    ribbon_distance_measure = pm.shadingNode('distanceBetween', name = ribbon_rootName+'_distance', asUtility = True)
    start_matrix = pm.shadingNode('decomposeMatrix', name = ribbon_rootName+'_start_matrix', asUtility = True)
    end_matrix = pm.shadingNode('decomposeMatrix', name = ribbon_rootName+'_end_matrix', asUtility = True)
    pm.connectAttr(start+'.worldMatrix', start_matrix+'.inputMatrix')
    pm.connectAttr(start_matrix+'.outputTranslate', ribbon_distance_measure+'.point1')
    pm.connectAttr(end+'.worldMatrix', end_matrix+'.inputMatrix')
    pm.connectAttr(end_matrix+'.outputTranslate', ribbon_distance_measure+'.point2')
    ribbon_length = pm.getAttr(ribbon_distance_measure+'.distance')
    ribbon_length_ratio = ribbon_length/(ribbon_length * segments)
    ribbonGEO = pm.nurbsPlane(name = ribbon_rootName+'_GEO', axis = [0,1,0], width = ribbon_length, lengthRatio = ribbon_length_ratio, degree = 3, patchesU = segments, patchesV = 1, constructionHistory = 0)
    ribbonGEO = ribbonGEO[0]
    pm.addAttr(ribbonGEO, longName = 'metaParent', attributeType = 'message')
    pm.addAttr(ribbonGEO, shortName = 'rbn', longName = 'ribbon', attributeType = 'message')
    ribbon_rootGRP = pm.group(name = ribbon_rootName+'_GRP')
    pm.addAttr(ribbon_rootGRP, longName = 'metaParent', attributeType = 'message')
    pm.addAttr(ribbon_rootGRP, shortName = 'rbn', longName = 'ribbon', attributeType = 'message') ##---- connect with tagger
    pm.addAttr(ribbon_rootGRP, longName = 'ribbonSegments', attributeType = 'long', defaultValue = segments)
    pm.addAttr(ribbon_rootGRP, longName = 'rigPart', attributeType = 'message')
    ribbon_rootGRP.metaParent >> ribbonGEO.metaParent
    print 'making ribbon drive joints'
    #connect to face rig or lower face, whatever is the closest rig part
    startJointTrans = pm.xform(start, q=True, ws=True, translation=True)
    endJointTrans = pm.xform(end, q=True, ws=True, translation=True)
    midJointTrans = uf.average_position(start,end)
    
    drive_joint_list = []
    ##pm.setAttr(jointName + '.drawStyle' = 2) hide joints
    pm.select(clear = True)
    startJoint = pm.joint(name = ribbonName+ '_RBN_start_DRV', relative = True, radius = 2, position = startJointTrans)
    pm.addAttr(startJoint, longName = 'metaParent', attributeType = 'message')
    pm.addAttr(startJoint, shortName = 'rbn', longName = 'ribbon', attributeType = 'message')
    pm.makeIdentity(startJoint, apply = True, rotate = True)
    drive_joint_list = drive_joint_list + [startJoint]
    ribbon_rootGRP.metaParent >> startJoint.metaParent
    pm.select(clear = True)
    endJoint = pm.joint(name = ribbonName+ '_RBN_end_DRV', relative = True, radius = 2, position = endJointTrans)
    pm.addAttr(endJoint, longName = 'metaParent', attributeType = 'message')
    pm.addAttr(endJoint, longName = 'ribbon', attributeType = 'message')
    pm.makeIdentity(endJoint, apply = True, rotate = True)
    drive_joint_list = drive_joint_list + [endJoint]
    ribbon_rootGRP.metaParent >> endJoint.metaParent
    pm.select(clear = True)
    midJoint = pm.joint(name = ribbonName+ '_RBN_mid_DRV', relative = True, radius = 2, position = midJointTrans)
    pm.addAttr(midJoint, longName = 'metaParent', attributeType = 'message')
    pm.addAttr(midJoint, shortName = 'rbn', longName = 'ribbon', attributeType = 'message')
    drive_joint_list = drive_joint_list + [midJoint]
    ribbon_rootGRP.metaParent >> midJoint.metaParent
    driver_group = uf.nest_transform(name = ribbon_rootName + '_drivers_GRP', action = 'parent', target = midJoint, transformObj = 'group')
    driver_group | startJoint
    driver_group | endJoint
    pm.select(clear = True)

    for driver in drive_joint_list:
        current_group_name = str(driver).replace('_DRV', '_GRP')
        current_group = uf.nest_transform(name = current_group_name, action = 'parent', target = driver, transformObj = 'group')
        current_offset = uf.nest_transform(name = current_group_name.replace('GRP', 'OST'), action = 'parent', target = driver, transformObj = 'group')
    pm.select(clear = True)
    #move everything into position
    pm.xform(ribbon_rootGRP, translation = midJointTrans, worldSpace = True)
    ##---- skin to nurbs curve
    pm.select(drive_joint_list, ribbonGEO)
    pm.skinCluster(toSelectedBones = True, bindMethod = 0, normalizeWeights = 1, weightDistribution = 0, maximumInfluences = 2, obeyMaxInfluences = True, skinMethod = 1, dropoffRate = 2, removeUnusedInfluence = False)
    ##----
    # Propagate follicles
    print('making follicles and skin joints')
    follicle_list = []
    ribbon_locator_list = []
    current_name = ''
    for i in range(segments):
        uPosition_factor = 1/float(segments)
        currentUposition = uPosition_factor * (float(i)+0.5)
        print 'follicle'
        last_follicle = create_follicle(oNurbs = ribbonGEO, uPos=currentUposition, vPos = 0.5)
        print('last follicle = ' + last_follicle.getParent())
        pm.addAttr(last_follicle, longName = 'metaParent', attributeType = 'message')
        pm.addAttr(last_follicle, shortName = 'rbn', longName = 'ribbon', attributeType = 'message')
        ribbon_rootGRP.metaParent >> last_follicle.metaParent
        follicle_list.append(last_follicle)
        if i == (segments/2):
            currentSide = 'C_'
        elif i < (segments/2):
            currentSide = 'R_'
        else:
            currentSide = 'L_'
        current_name = currentSide + ribbon_rootName
        #currentJointName = currentSide + current_name
        print( current_name)
        current_locator = uf.nest_transform(name = current_name+'_LOC', action = 'child', target = last_follicle.getParent(), transformObj = 'locator')
        current_group = uf.nest_transform(name = current_name + '_GRP', action = 'parent', target = current_locator, transformObj = 'group')
        pm.addAttr(current_locator, shortName = 'rbn', longName = 'ribbon', attributeType = 'message')
        ribbon_locator_list = ribbon_locator_list + [current_locator]
        ribbon_rootGRP.metaParent >> current_locator.metaParent
    
    ribbonRef = ribbon_rootGRP
    
    return ribbonRef



