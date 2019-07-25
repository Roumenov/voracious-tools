import pymel.core as pm
import maya.cmds as cmds
import math
#a few functions that are actually usable


def strip_suffix(inputString='', suffix=''):
    """
    Return string without suffix.
    """

    if inputString.endswith(suffix):
        remove = len(suffix)
        print "removing prefix"
        output_string = inputString[:-remove]
        #print (output_string)
        return output_string
    else:
        print "suffix not found"
        return inputString

def strip_prefix(inputString='', prefix=''):
    """
    Return string without prefix.
    """

    if inputString.endswith(prefix):
        remove = len(prefix)
        print "removing prefix"
        output_string = inputString[remove:]
        # NOT SURE HOW TO SLICE NOTATE THIS CORRECTLY
        return output_string
    else:
        print "prefix not found"
        return inputString

#PURPOSE/PROCEDURE      create prompt that requests name input, then returns input
#PRESUMPTIONS   user knows the name they want and doesn't have a reason to click elsewhere, user only needs one name
def prompt_string(promptTitle = '', promptMessage = ''):
    """
    Prints and returns user provided string from a prompt dialogue.
    """
    name_prompt = pm.promptDialog(
            text = True,
            title=promptTitle,
            message= promptMessage,
            button=['Confirm', 'Cancel'],
            dismissString= 'Cancel'
            )
    if name_prompt == 'Confirm':
        prompt_string = pm.promptDialog(query=True, text=True)
        print( 'name :: ' + prompt_string)
        return prompt_string
    else:
        pm.warning('no name given')


def attr_lock(target, attr = '', lock = False):
    """
    'all' will lock/unlock TRS and Visibility
    translation will lock/hide translates
    """
    if attr == 'all':
        for character in 'XYZ':
            target_attr = 'translate' + character
            if lock:
                target.setAttr(target_attr, lock = True, keyable = False, channelBox = False)
            else:
                target.setAttr(target_attr, channelBox = True, lock = False)
                target.setAttr(target_attr, keyable = True)
            target_attr = 'rotate' + character
            if lock:
                target.setAttr(target_attr, lock = True, keyable = False, channelBox = False)
            else:
                target.setAttr(target_attr, channelBox = True, lock = False)
                target.setAttr(target_attr, keyable = True)
            target_attr = 'scale' + character
            if lock:
                target.setAttr(target_attr, lock = True, keyable = False, channelBox = False)
            else:
                target.setAttr(target_attr, channelBox = True, lock = False)
                target.setAttr(target_attr, keyable = True)
    elif attr == 'translate':
        for character in 'XYZ':
            target_attr = 'translate' + character
            print target_attr
            if lock:
                target.setAttr(target_attr, lock = True, keyable = False, channelBox = False)
            else:
                target.setAttr(target_attr, channelBox = True, lock = False)
                target.setAttr(target_attr, keyable = True)
    elif attr == 'rotate':
        for character in 'XYZ':
            print character
            target_attr = 'rotate' + character
            if lock:
                target.setAttr(target_attr, lock = True, keyable = False, channelBox = False)
            else:
                target.setAttr(target_attr, channelBox = True, lock = False)
                target.setAttr(target_attr, keyable = True)
    elif attr == 'scale':
        for character in 'XYZ':
            target_attr = 'scale' + character
            if lock:
                target.setAttr(target_attr, lock = True, keyable = False, channelBox = False)
            else:
                target.setAttr(target_attr, channelBox = True, lock = False)
                target.setAttr(target_attr, keyable = True)
    elif attr == 'visibility':
        target_attr = 'visibility'
        if lock:
            target.setAttr(target_attr, lock = True, keyable = False, channelBox = False)
        else:
            target.setAttr(target_attr, channelBox = True, lock = False)
            target.setAttr(target_attr, keyable = True)
    else:
        try:
            target_attr = attr
            if lock:
                target.setAttr(target_attr, lock = True, keyable = False, channelBox = False)
            else:
                target.setAttr(target_attr, channelBox = True, lock = False)
                target.setAttr(target_attr, keyable = True)
        except:
            pass
        #pm.error('unrecognized attr argument')
        #pass

#should later simplify to only link two objects, then encapsulate in another function or tool that decides which objects to pair how
def link_attrs(Translate = None, Rotate = None, Scale = None, source = None, target = None):
    """
    Links Translate, Rotate, and Scale attributes between source and target
    @param Translate: takes string 'x', 'y', and 'z' in any order
    @param Rotate: takes string 'x', 'y', and 'z' in any order
    @param Scale: takes string 'x', 'y', and 'z' in any order
    @param targets: takes list of things to parse and link
    """
    #source = targets[0]
    #target = targets[1]
    
    if Translate:
        if 'x' in Translate:
            source.translateX >> target.translateX
        else:
            pass
        if 'y' in Translate:
            source.translateY >> target.translateY
        else:
            pass
        if 'z' in Translate:
            source.translateZ >> target.translateZ
        else:
            pass
    else:
        print('no translate values')
    if Rotate:
        if 'x' in Rotate:
            source.rotateX >> target.rotateX
        else:
            pass
        if 'y' in Rotate:
            source.rotateY >> target.rotateY
        else:
            pass
        if 'z' in Rotate:
            source.rotateZ >> target.rotateZ
        else:
            pass
    else:
        print('no rotate values')
    if Scale:
        if 'x' in Scale:
            source.scaleX >> target.scaleX
        else:
            pass
        if 'y' in Scale:
            source.scaleY >> target.scaleY
        else:
            pass
        if 'z' in Scale:
            source.scaleZ >> target.scaleZ
        else:
            pass
    else:
        print('no scale values')



def list_link_attrs(Translate = None, Rotate = None, Scale = None, targets = None):
    """
    Links Translate, Rotate, and Scale attributes between every other selection in a list.
    @param Translate: boolean option
    @param Rotate: boolean option
    @param Scale: boolean option
    @param targets: takes list of things to parse and link
    """
    source_list = targets[::2]
    target_list = targets[1::2]
    for index, current_object in enumerate(source_list):
        print(str(current_object))
        object_target = target_list[index]
        link_attrs(Translate, Rotate, Scale, source = current_object, target = object_target)

#PURPOSE        Find center point in worldspace between a number of transforms
#USAGE          uf.average_position(object1, object2, object3)
#PRESUMPTIONS   only works with transforms as arguments

def average_position(*target_list):
    """
    Returns average position in space between all target_list items.
    """
    if len(target_list):
        #target_list = arglist
        count = len(target_list)
        sums = [0,0,0]
        pos = [0.0,0.0,0.0]
        for item in target_list:
            print(item)
            pos = pm.xform(item, q=True, ws=True, rotatePivot=True)
            sums[0] += pos[0]
            sums[1] += pos[1]
            sums[2] += pos[2]
        center = [sums[0]/count, sums[1]/count, sums[2]/count]
        return center
    else:
        target_list = pm.ls(sl=True, fl=True)
        count = len(target_list)
        sums = [0,0,0]
        for item in target_list:  
            pos = pm.xform(item, q=True, ws=True, rotatePivot=True)
            sums[0] += pos[0]
            sums[1] += pos[1]
            sums[2] += pos[2]
        center = [sums[0]/count, sums[1]/count, sums[2]/count]
        return center

def loc_average(objType = None, *target_list):
    loc_name = 'location_average_00'
    loc_position = average_position(*target_list)
    loc_object = create_object(objName = loc_name, objType = 'locator', radius = 5.0)
    pm.xform(loc_object, translation = loc_position)
    
    return

def get_distance(startPoint, endPoint):
    """
    Returns distance between two points in space
    Use pm.xform(object, q=True, ws=True, rp=True) to get and object's location in worldSpace.
    @param startPoint:      (floatX,floatY,floatZ)
    Specifies point to measure distance from.
    @param endPoint:        (floatX,floatY,floatZ)
    Specifies point to measure distance to, from startPoint.
    """
    dx = startPoint[0] - endPoint[0]
    dy = startPoint[1] - endPoint[1]
    dz = startPoint[2] - endPoint[2]
    return math.sqrt( dx*dx + dy*dy + dz*dz )


def distance_influence_calc(satellites = [], target = None):
    '''
    Calculates relative influence of satellites influencing movement of target (inversly proportional to distance to target)
    sum of satellite influence is equal to 1.0
    @param satelites: list of transforms influencing target
    @param target: object being trasformed
    @return influence: list of transform influence to target
    '''
    influence = range(len(satellites))
    inverse_distances = range(len(satellites))
    target_point = pm.xform(target, ws=True, rp = True, q = True)
    sum = 0
    
    #calculate inverse distances and their sum
    for i in range(0, len(satellites)):
        sat_point = pm.xform(satellites[i], ws=True, rp = True, q = True)
        inverse_distances[i] = 1 / get_distance(sat_point, target_point)
        sum += inverse_distances[i]
    
    # calculate relative influence
    for i in range(0, len(satellites)):
        influence[i] = inverse_distances[i] / sum
    print(influence)
    return influence

#influences = distance_influence_calc(satellites, target)

def multi_constrain(satellites = [], target = None, constraintType = 'parent', normalize = True):
    '''
    Constrains target object to n satellites and normalizes the influence to add up to 1.0
    @param satellites: 
    @param constraintType: parent, orient, or point
    @param target: object getting constrained to the satellites
    @return constraint:  the multi influence constraint affecting target
    '''
    influences = distance_influence_calc(satellites, target)
    for index in range(len(satellites)):
        if constraintType == 'parent':
            print (satellites[index])
            print(target)
            constraint = pm.parentConstraint(satellites[index],target, mo = 1, weight = 1)
            constraint.setAttr('interpType', 2)
        elif constraintType == 'orient':
            constraint = pm.orientConstraint(satellites[index],target, mo = 1, weight = 1)
            constraint.setAttr('interpType', 2)
        elif constraintType == 'point':
            constraint = pm.pointConstraint(satellites[index],target, mo = 1, weight = 1)
        elif constraintType == 'scale':
            constraint = pm.scaleConstraint(satellites[index],target, mo = 1, weight = 1)
        else:
            pm.error('unknown argument')
    
    #set constraint weight
    for index in range(len(satellites)):
        name = str(satellites[index].stripNamespace())
        #print(str(satellites[index])+'W'+str(index))
        #str(satellites[index])
        constraint.setAttr(name+'W'+str(index), influences[index])
    return constraint
#multi_constrain(satellites, target)


#match pivot to target


def match_pivot(source = None, target = None):
    """
    Match one object's pivot to another object's pivot without moving either object.
    @param source:      Object whose pivot is going to be matched.
    @param target:      Object whose pivot is going to be changed.
    """
    pivot_value = [(pm.xform (source, q=1, ws=1, piv=1))[0], (pm.xform (source, q=1, ws=1, piv=1))[1], (pm.xform (source, q=1, ws=1, piv=1))[2]]
    print ('source = '+ str(source))
    print ('target = ' + str(target))
    print(pivot_value)
    pm.xform (target, worldSpace = True, piv=(pivot_value))




def create_object(objName = '', objType = '', radius = 1.0):
    """
    Create various basic objects. Default is group.
    @param objType: String input accepts, locator, group, sphereShape, cubeShape, coneShape, joint, circleCTL, squareCTL, boxCTL, sphereCTL, arrowX, arrowY, or arrowZ.
    """
    pm.select(clear = True)
    if objType == 'locator':
        output = pm.spaceLocator(name = objName, relative = True)
        output.setAttr('localScaleX', radius) 
        output.setAttr('localScaleY', radius) 
        output.setAttr('localScaleZ', radius)
    elif objType == 'group':
        output = pm.group(name = objName, world=True)
    elif objType == 'sphereShape':
        #shape_name = objName + 'Shape'
        output = pm.createNode('renderSphere') # name = objName
        output.setAttr('radius', radius)
        output = output.listRelatives(parent = True)[0]
        pm.rename(output, objName)
    elif objType == 'cubeShape':
        #shape_name = objName + 'Shape'
        output = pm.createNode('renderBox')
        output.setAttr('sizeX', radius)
        output.setAttr('sizeY', radius)
        output.setAttr('sizeZ', radius)
        output = output.listRelatives(parent = True)[0] # can also use output.getParent()
        pm.rename(output, objName)
    elif objType == 'coneShape':
        #shape_name = objName + 'Shape'
        output = pm.createNode('renderCone')
        output.setAttr('coneAngle', radius*10)
        output = output.listRelatives(parent = True)[0]
        pm.rename(output, objName)
    elif objType == 'joint':
        output = pm.joint(name = objName, radius = radius)
    elif objType == 'circleCTL': ##----tries to parent shape instead of transform
        output = pm.circle (ch = 1, name = objName, radius = radius, nrx = 1, nry = 0, nrz = 0)[0]
    elif objType == 'squareCTL':
        output = pm.curve(name = objName, degree = 1, point = [(1,0,1), (-1,0,1), (-1,0,-1), (1,0,-1), (1,0,1)], knot =[0,1,2,3,4])[0]
    elif objType == 'boxCTL':
        cornerPos = radius * 0.5
        output = pm.curve(name = objName, degree = 1, point = [(-cornerPos, cornerPos, cornerPos),(cornerPos,cornerPos,cornerPos), (cornerPos,-cornerPos,cornerPos), (-cornerPos, -cornerPos,cornerPos), (-cornerPos,cornerPos,cornerPos), (-cornerPos, cornerPos, -cornerPos), (-cornerPos,-cornerPos,-cornerPos), (cornerPos,-cornerPos,-cornerPos), (cornerPos,-cornerPos,cornerPos),(cornerPos,cornerPos,cornerPos), (cornerPos,cornerPos,-cornerPos), (cornerPos, -cornerPos,-cornerPos), (cornerPos,cornerPos,-cornerPos), (-cornerPos,cornerPos,-cornerPos), (-cornerPos,-cornerPos,-cornerPos), (-cornerPos,-cornerPos,cornerPos)], knot =[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])[0]
    elif objType == 'sphereCTL':
        output = pm.circle (ch = 1, name = objName, radius = radius, nrx = 1, nry = 0, nrz = 0)[0]
        pm.circle (ch = 1, name = objName + 'subRingY', radius = radius, nrx = 0, nry = 1, nrz = 0)
        pm.circle (ch = 1, name = objName + 'subRingZ', radius = radius, nrx = 0, nry = 0, nrz = 1)
        pm.select(clear = True)
        pm.select(objName + 'subRingYShape', objName + 'subRingZShape', output)
        pm.parent(relative=True,shape=True)
    elif objType == 'arrowX':
        output = pm.curve(name = objName + '_arrow', degree = 1, point = [(0,0,0), (0,0,13), (0,1,11), (0,-1,11), (0,0,13), (1,0,11), (-1,0,11), (0,0,13)], knot =[0,1,2,3,4,5,6,7])
        pm.xform(output, relative = True, scale = (radius,radius,radius))
        pm.xform(output, relative = True, rotation = (0,90,0))
        pm.makeIdentity(output, apply = True)
    elif objType == 'arrowY':
        output = pm.curve(name = objName + '_arrow', degree = 1, point = [(0,0,0), (0,0,13), (0,1,11), (0,-1,11), (0,0,13), (1,0,11), (-1,0,11), (0,0,13)], knot =[0,1,2,3,4,5,6,7])
        pm.xform(output, relative = True, scale = (radius,radius,radius))
        pm.xform(output, relative = True, rotation = (-90,0,0))
        pm.makeIdentity(output, apply = True)
    elif objType == 'arrowZ':
        output = pm.curve(name = objName + '_arrow', degree = 1, point = [(0,0,0), (0,0,13), (0,1,11), (0,-1,11), (0,0,13), (1,0,11), (-1,0,11), (0,0,13)], knot =[0,1,2,3,4,5,6,7])
        pm.xform(output, relative = True, scale = (radius,radius,radius))
        pm.makeIdentity(output, apply = True)
    else:
        output = pm.group(name = objName, world=True)
        #need to expound on this later....
    pm.addAttr(output, longName = 'metaParent', attributeType = 'message')
    return output

#uf.create_object(objName = 'test_LOC', objType = 'locator', radius = 1.0)

# nest_transform()
#PURPOSE
#PROCEDURE          check suffix and set name, object based on arg
#PRESUMPTIONS       user inputs corremt name, takes only one explicit target at a time

def nest_transform(name, action, target = None, transformObj = 'locator', transformRadius = 1.0):
    """
    Creates a transform inside a hierarchy.
    @param action: 'parent' makes new transform parent of target. 'child' makes it child. 'adopt' makes child and adopts all child transforms.
    """
    nested_transform = None
    if not target:
        target = pm.ls(sl = 1)[0]
        if target.exists():
            print( 'using selection :: ' + str(target) + ' as target')
        else:
            print( 'no available target')
            pm.error(showLineNumber = True)
            return None
    else:
        print('target = ' + str(target))
    target_name = str(target)
    if len(name): #set transform name to arg value
        transformName = name
    else:
        transformName = target_name + '_nest'
    nested_transform = create_object(objName = transformName, objType = transformObj, radius = transformRadius)
    pm.matchTransform(nested_transform, target)
    if action == 'parent':
        transform_parent = target.getParent()
        pm.parent(target, nested_transform)
        pm.parent(nested_transform, transform_parent)
    elif action == 'child':
        pm.parent(nested_transform, target)
    elif action == 'adopt':
        transform_children = target.getChildren(children = True, type = 'transform')
        pm.parent(transform_children, nested_transform)
        pm.parent(nested_transform, target)
    else:
        print('unknown arg')
    return nested_transform


#gets weird if things are scaled
def replace_target(useTargetName = True, clearSource = False):
    object_list = pm.ls (sl = 1)
    source_object = object_list[0]
    target_list = object_list[1:]
    for target in target_list:
        print( 'replacing :: ' +str(target))
        transformName = str(source_object)
        current_replacement = pm.duplicate(source_object)[0]
        pm.matchTransform(current_replacement, target, scale = False)
        target_parent = pm.listRelatives(target, parent = True, type = 'transform')[0]
        target_children = pm.listRelatives(target, children = True, type = 'transform')
        if target_parent:
            print( 'parenting to :: ' + str(target_parent))
            target_parent | current_replacement
        else:
            print( 'parent is world')
            pass
        for child in target_children:
            current_replacement | child
        pm.delete(target)
        if useTargetName:
            pm.rename(current_replacement,str(target))
        else:
            pm.rename(current_replacement, source_object.shortName())
            print('using source name')
        
        
    if clearSource:
        pm.delete(source_object)
    else:
        print('preserved source object')


def joint_on_vertex():
    """Make cluster on selected vertices and replace with a joint."""
    #target_verts = pm.ls(sl=1)
    center_cluster = pm.cluster()
    print( 'center cluster :: ' + str(center_cluster))
    center_point = center_cluster[1].getRotatePivot()
    print( 'center point :: ' + str(center_point))
    pm.select(clear=True)
    vertex_joint = pm.joint(position = center_point)
    pm.delete(center_cluster)
    return vertex_joint

def object_on_vertex(objName = '', objType = '', radius = 1.0):
    """Make cluster on selected vertices and replace with a joint."""
    #target_verts = pm.ls(sl=1)
    center_cluster = pm.cluster()
    print( 'center cluster :: ' + str(center_cluster))
    cluster_position = center_cluster[1].getRotatePivot()
    print( 'center point :: ' + str(cluster_position))
    pm.select(clear=True)
    pm.delete(center_cluster)
    vertex_joint = create_object(objName = objName, objType = objType, radius = radius)
    pm.xform(vertex_joint, translation = cluster_position)
    return vertex_joint
#uf.object_on_vertex(objName = 'test_joint', objType = 'joint', radius = 1.0)

def object_on_pivot(objType = 'joint'):
	"""
	Create a bone from the customPivot context
	In component mode of a mesh:
	Press "D" or "Insert" to go into custom pivot context
	  If you click on edges verts or faces the pivot will auto align
	  If you want to aim an axis click on the axis and Ctrl+Shift on another vert/edge/face to aim it
	  When you have the pivot you want run this to create the joint with that pivot
	*Arguments:*
		* objType currently does nothing
	*Keyword Arguments:*
		* ``None`` 
	*Returns:*
		* ``None`` 
	*Author:*
	* randall.hess, randall.hess@gmail.com, 9/3/2017 5:17:19 PM
	"""

	# get these values	
	loc_xform = None
	loc_rp    = None
	
	# Get manipulator pos and orient	
	manip_pin = cmds.manipPivot(pinPivot=True)
	manip_pos = cmds.manipPivot(q=True, p=True)[0]
	manip_rot = cmds.manipPivot(q=True, o=True)[0]
	
	# delete existing temp objs
	temp_joint = None
	temp_loc   = None
	temp_cluster= None
	temp_joint_name = 'temp_joint'
	temp_loc_name = 'temp_loc'
	temp_cluster_name = 'temp_cluster'
	temp_objs = [temp_joint_name, temp_loc_name]	
			
	# get the selectMode
	sel_mode_obj       = cmds.selectMode(q=True, o=True)
	sel_mode_component = cmds.selectMode(q=True, co=True)

	# store and clear selection
	selection = cmds.ls(sl=True)
	py_selection = pm.ls(sl=True)
	if len(selection) == 0:
		cmds.warning('You must have a selection!')
		return
	
	
	if len(selection) > 0:
		
		sel = selection[0]
		py_sel = py_selection[0]
	
		# create temp joint and set pos/rot
		cmds.select(cl=True)
		temp_joint= pm.joint(n=temp_joint_name)
		temp_loc = pm.spaceLocator(n=temp_loc_name)
		
		# get transform from the selected object
		if type(py_sel) == pm.nodetypes.Transform:
			# snap loc to position			
			const = pm.pointConstraint(sel, temp_loc, mo=False, w=1.0)
			pm.delete(const)
			const = pm.orientConstraint(sel, temp_loc, mo=False, w=1.0)
			pm.delete(const)
		else:
			# get transform from parent object
			if type(py_sel.node()) == pm.nodetypes.Mesh:
				parent = py_sel.node().getParent()
				if parent:
					const = pm.pointConstraint(parent, temp_loc, mo=False, w=1.0)
					pm.delete(const)
					const = pm.orientConstraint(parent, temp_loc, mo=False, w=1.0)
					pm.delete(const)
					
					# get the transforms
					loc_xform = pm.xform(temp_loc, q=True, m=True, ws=True)
					loc_rp = pm.xform(temp_loc, q=True, ws=True, rp=True)					

		# rotate the temp_loc if manip rot has been modified
		if not manip_rot == (0.0,0.0,0.0):				
			pm.rotate(temp_loc, manip_rot)
			
		# move position to the cluster position
		if not manip_pos == (0.0,0.0,0.0):		
			pm.xform(temp_loc, ws=True, t=manip_pos)
			
		# get the transforms
		loc_xform = pm.xform(temp_loc, q=True, m=True, ws=True)
		loc_rp = pm.xform(temp_loc, q=True, ws=True, rp=True)		
			
		# get the position from the component selection			
		if not type(py_sel) == pm.nodetypes.Transform:
			cmds.select(selection, r=True)
			cmds.ConvertSelectionToVertices()
			try:
				cluster = cmds.cluster(n=temp_cluster_name)[1]
			except:
				cmds.warning('You must select a mesh object!')
				pm.delete(temp_joint)
				pm.delete(temp_loc)
				return
			
			# get the cluster position
			cmds.select(cl=True)		
			pos = cmds.xform(cluster, q=True, ws=True, rp=True)				
			
			# snap to the cluster
			const = pm.pointConstraint(cluster, temp_loc, mo=False, w=1.0)
			pm.delete(const)
			
			cmds.delete(cluster)
			
			# rotate the temp_loc if manip rot has been modified
			if not manip_rot == (0.0,0.0,0.0):				
				pm.rotate(temp_loc, manip_rot)
				
			# move position to the cluster position
			if not manip_pos == (0.0,0.0,0.0):		
				pm.xform(temp_loc, ws=True, t=manip_pos)				
					
			# get the transforms
			loc_xform = pm.xform(temp_loc, q=True, m=True, ws=True)
			loc_rp = pm.xform(temp_loc, q=True, ws=True, rp=True)	
		
		# remove temp loc
		pm.delete(temp_loc)

	# modify the joint and stu
	if temp_joint:		
		if loc_xform and loc_rp:
			pm.xform(temp_joint, m=loc_xform, ws=True)
			pm.xform(temp_joint, piv=loc_rp, ws=True)			
		
		# freeze orient	
		pm.select(temp_joint)	
		pm.makeIdentity( apply=True, translate=True, rotate=True, scale=True, n=False )

	# unpin pivot
	cmds.manipPivot(pinPivot=False)


def curve_on_vertices(name, vertices):
    """
    make a curve with CVs along the given list of vertices
    @param name: string to use as curve name
    @param vertices: flat list of vertices to build curve along
    """
    vertices = pm.ls(pm.polyListComponentConversion(vertices, toVertex=True), flatten=True, orderedSelection=True)
    #format list of transforms
    positions = range(len(vertices))
    for index in range(len(vertices)):
        #item = vertices[index]
        positions[index] = pm.xform(vertices[index], query=True, worldSpace=True, translation=True)
        #current_position = pm.xform(vertices[index], query=True, worldSpace=True, translation=True) #pm.pointPosition(vertex, world = True)
        #position_list.append(current_position)
    
    output_curve = pm.curve(name = name, degree = 3, point = positions)
    
    return output_curve

#output_curve_name = uf.prompt_string(promptTitle = 'Offset String', promptMessage = 'Enter string to use for curve name')
#selection = pm.ls(sl=1, flatten = True)
#uf.curve_on_vertices(name = output_curve_name, vertices = selection)




def curve_on_transforms(name, transforms):
    """
    make a curve with CVs along the given list 
    @param name: 
    """
    if len(transforms) <= 3:
        curve_degree = 1
    else:
        curve_degree = len(transforms)-1
    #format list of transforms
    positions = range(len(transforms))
    for index in range(len(transforms)):
        positions[index] = pm.xform(transforms[index], q=True, ws=True, rotatePivot=True)
    print(positions)
    output_curve = pm.curve(name = name, degree = curve_degree, editPoint = positions)
    
    return output_curve

#output_curve_name = uf.prompt_string(promptTitle = 'Curve Name', promptMessage = 'Enter curve name')
#selection = pm.ls(sl=1)
#uf.curve_on_transforms(name = output_curve_name, transforms = selection)


#PURPOSE        MAKE A BUNCH OF OBJECTS ON A MOTION PATH

def obj_on_curve(curve, count, obj_type, start_transform = True,end_transform = True):
    
    iterations = count
    if start_transform == True:
        #iterations += 1
        start_int = 0
    else:
        start_int = 1
    if end_transform == True:
        iterations += 1
    else:
        pass
        
    for index in range(start_int,iterations):
        u_value = index*(1.0/count)
        print u_value
        #create object
        current_name = 'curvejoint_' + str(index)
        current_object = create_object(objName = current_name, objType = obj_type, radius = 1.0)
        motion_path = pm.pathAnimation(curve,current_object, fractionMode = True, follow = True, followAxis = 'z', upAxis = 'y', worldUpType = 'vector', worldUpVector = (0,1,0), inverseUp = False, inverseFront = False, bank = False, startTimeU = u_value)
    return motion_path
#transform_count = int(uf.prompt_string())
#transform_on_curve(count = transform_count, start_transform = True,end_transform = True)


def curve_chain():
    pass
    #output_curve_name = uf.prompt_string(promptTitle = 'Offset String', promptMessage = 'Enter string to use for offset')
    #transform_list = pm.ls(sl=True)
    
    #curve_on_transforms(name = output_curve_name, transforms = transform_list)

    #transform_count = int(uf.prompt_string())
    #transform_on_curve(count = transform_count, start_transform = True,end_transform = True)



def aim_object(aimer, target, axis = '+x'): ##---- update to make locator, use that to get aim value, and set value .
    """
    Aim first thing at second thing, then delete history.
    aimer: Object being rotated
    target: Object aimer is aiming at.
    axis: '+x', '+y', '+z', '-x', '-y', '-z'
    example usage: aim_object(aimer = pm.ls(sl=1)[0], target = pm.ls(sl=1)[1], axis = '+x')
    """
    if axis == '+x':
        aimer_vector = (1,0,0)
    elif axis == '+y':
        aimer_vector = (0,1,0)
    elif axis == '+z':
        aimer_vector = (0,0,1)
    elif axis == '-x':
        aimer_vector = (-1,0,0)
    elif axis == '-y':
        aimer_vector = (0,-1,0)
    elif axis == '-z':
        aimer_vector = (0,0,-1)
    else:
        pass
    skip_val = 'x' # used to read letter value "axis[1]"
    proxy_name = str(aimer)+'_aimer'
    aim_proxy = create_object(objName = proxy_name, objType = 'locator')
    pm.matchTransform(aim_proxy, aimer)
    aim_constraint = pm.aimConstraint(target,aim_proxy, aimVector = aimer_vector, worldUpType = 'scene', skip = skip_val)
    pm.delete(aim_constraint)
    pm.matchTransform(aimer,aim_proxy)
    pm.delete(aim_proxy)
    if aimer.type() == 'joint':
        pm.makeIdentity(aimer, translate = 1, rotate = 1, scale = 1, apply = True)
    else:
        pass


def check_connections(target, tranlation = 1, rotation = 1):
    """
    use to see if a transform is connectable
    returns False if attributes already have connections
    returns True if no connections are present
    will later expand to check any given attr
    """
    if tranlation:
        for character in 'XYZ':
            #print character
            target_attr = str(target)+'.translate' + character
            #print target_attr
            trans_check = pm.listConnections(target_attr)
            if len(trans_check):
                #print 'translate ' +character + ' connected'
                return False
            else:
                pass
                #print 'translate ' +character + ' clear'
    else:
        pass
    if rotation:
        for character in 'XYZ':
            print character
            target_attr = str(target)+'.rotate' + character
            print target_attr
            rot_check = pm.listConnections(target_attr)
            if len(rot_check):
                #print 'rotate ' +character + ' connected'
                return False
            else:
                #return True
                #print 'rotate ' +character + ' clear'
                pass
    else:
        pass
    return True


def list_influences(mesh):
	#test_thing.listHistory(type = 'skinCluster')
	target_cluster = mesh.history(type = 'skinCluster')
	
	influence_list = pm.skinCluster(target_cluster,query=True,inf=True)
	influence_return_list = []
	for item in influence_list:
		influence_return_list.append(str(item))
		#print(item)
	return influence_return_list



##      META TOOLS  ===================================



def meta_make_child(source, *target_list):
    """Make all objects in target_list the meta children of source object."""
    print source
    for target in target_list:
        if target.hasAttr('metaParent'):
            source.metaParent >> target.metaParent
        else:
            print('adding metaParent attr')
            pm.addAttr(target, longName = 'metaParent', attributeType = 'message')
            source.metaParent >> target.metaParent

def meta_traverse_old(source, relation = 'parent', tag = ''):
    """Return metaParent or children of source.
    relation: 'parent', or "children"
    tag: return only relation with attr of given name
    """
    meta_attr = str(source) + '.metaParent'
    if source.hasAttr('metaParent'):
        target_attr = str(source)+'.metaParent'
        trans_check = pm.listConnections(target_attr)
        if relation == 'parent':
            source_parent = pm.listConnections(meta_attr, source = True, destination = False)[0]
            return source_parent
        else:
            source_children = pm.listConnections(meta_attr, source = False, destination = True)
            if len(tag):
                meta_childrens = []
                for child in source_children:
                    if child.hasAttr(tag):
                        #print child
                        meta_childrens = meta_childrens + [child]
                    else:
                        pass
            return meta_childrens
    else:
        pm.warning('no metaParent tag on :: ' + str(source))

def meta_traverse(source, relation, tag = ''):
    """Return metaParent or children of source.
    relation: 'parent', or "children"
    tag: return only relation with attr of given name
    """
    meta_attr = str(source) + '.metaParent'
    meta_childrens = []
    if source.hasAttr('metaParent'):
        target_attr = str(source)+'.metaParent'
        trans_check = pm.listConnections(target_attr)
        if relation == 'parent':
            try:
                source_parent = pm.listConnections(meta_attr, source = True, destination = False)[0]
                return source_parent
            except:
                return False
        else:
            source_children = pm.listConnections(meta_attr, source = False, destination = True)
            if len(tag):
                for child in source_children:
                    if child.hasAttr(tag):
                        #print child
                        meta_childrens = meta_childrens + [child]
                    else:
                        pass
                return meta_childrens
            else:
                return source_children
    else:
        pm.warning('no metaParent tag on :: ' + str(source))
#uf.meta_traverse(source, relation = 'parent', tag = '')


def load_csv(sourcename = '', targetname = '', filename = 'JointMapping.csv', directory = 'Z:/0_p4v/PotionomicsSourceAssets/Art_sourcefiles/Characters/'):
    """
    Load a csv file and return a list of 
    """
    filepath = directory + filename
    csv_table = open(filepath, "r")
    table_content = csv_table.readlines()
    column_a = []
    column_b = []
    csv_table.close()
    #read lines
    for line in table_content:
        #print('current line:')
        column_a.append(line.split(",")[0])
        item_b = line.split(",")[1]
        column_b.append(item_b.split("\r\n")[0])
    return column_a, column_b
#src_list, dest_list = uf.load_csv(sourcename = '', targetname = '', filename = 'JointMapping.csv', directory = 'Z:/0_p4v/PotionomicsSourceAssets/Art_sourcefiles/Characters/')

def list_match(source_list=None,destination_list=None, operation = 'match', sourceName = ['skel_', 'Skel_'], destName = ['character_','Corsac_']):
    #iterate through source_list by index, then match it to destination_list?
    for index, current_source_string in enumerate(source_list):
        if len(current_source_string):
            source_string = str(current_source_string).replace(sourceName[0], sourceName[1])
            dest_string = str(destination_list[index]).replace(destName[0], destName[1])
            #new_dest_string = dest_string + '_location'
            print(source_string)
            print(dest_string)
            if pm.objExists(source_string) and pm.objExists(dest_string):
                source_object = pm.ls(source_string)[0]
                #print(source_object)
                #destination_object = pm.ls(dest_string)[0]
                #print(destination_object)
                try:
                    print('matching')
                    pm.matchTransform(source_object, pm.ls(dest_string)[0], pos = True, rot = True, scale = False)
                except:
                    print('failed match')
            else:
                pass
        else:
            print('no length')
            pass
    print('fin')

#uf.list_match(source_list = src_list,destination_list = dest_list, operation = 'match', sourceName = ['skel_', 'Skel_'], destName = ['character_','Luna_'])


#================== ----------- 
#for index, source_object in enumerate(listA):
#    print(str(source_object))
#    target_name = str(source_object).replace('fat_male', target_string)
#    target_object = pm.ls(target_name)[0]
#    pm.matchTransform(source_object, target_object, pos = True, rot = True, scale = False)



#need to be super conscious of which list is source and which is destination
#probably need to do string replace and matching on import or as a separate pass
#need special exceptions or separate mapping tables for generic character
#
#
def list_constrain(source_list=None,destination_list=None, sourceName = ['skel_', 'Skel_'], destName = ['character_','Corsac_']):
    #iterate through source_list by index, then match it to destination_list?
    for index, current_source_string in enumerate(source_list):
        #print(current_source_string)
        #print(type(current_source_string))
        #print(len(current_source_string))
        if len(current_source_string):
            new_source_string = current_source_string.replace(sourceName[0], sourceName[1])
            new_dest_string = destination_list[index].replace(destName[0], destName[1])
            #new_dest_string = dest_string + '_location'
            print(new_source_string)
            print(new_dest_string)
            if pm.objExists(new_source_string) and pm.objExists(new_dest_string):
                source_object = pm.ls(new_source_string)[0]
                print(source_object)
                destination_object = pm.ls(new_dest_string)[0]
                print(destination_object)
                try:
                    print('matching')
                    constraint = pm.parentConstraint(source_object, destination_object, mo = 1, weight = 1)
                    constraint.setAttr('interpType', 2)
                    pm.scaleConstraint(source_object, destination_object, mo = True)
                except:
                    print('failed match')
            else:
                pass
        else:
            print('no length')
            pass
    print('fin')

#list_constrain_list(source_list=genchar_table[0],destination_list=genchar_table[1], sourceName = ['character_','GenChar_'], destName = ['skel_', 'skel:Skel_'])


def list_rename(source_list=None,destination_list=None, sourceName = ['skel_', 'Skel_'], destName = ['character_','Corsac_']):
    #iterate through source_list by index, then rename to 
    for index, current_source_string in enumerate(source_list):
        #print(current_source_string)
        #print(type(current_source_string))
        #print(len(current_source_string))
        if len(current_source_string):
            target_name = current_source_string.replace(sourceName[0], sourceName[1])
            new_dest_string = destination_list[index].replace(destName[0], destName[1])
            #new_dest_string = dest_string + '_location'
            print(target_name)
            print(new_dest_string)
            if pm.objExists(target_name):
                source_object = pm.ls(target_name)[0]
                try:
                    source_object.rename(new_dest_string)
                except:
                    print('failed match')
            else:
                pass
        else:
            print('no length')
            pass
    print('fin')

#uf.list_rename(source_list=genchar_table[0],destination_list=genchar_table[1], sourceName = ['character_','GenChar_'], destName = ['skel_', 'skel:Skel_'])


####
#
#       GEOMETRY MANIPULATION
#
####

import maya.cmds as cmds
import maya.mel as mel


def CombineSkinnedMeshProc( *args):
    
    selection = cmds.ls(sl=True)
    joint_list = []
    if(len(selection) == 0):
        raise TypeError ('Please Select at least two skinned Meshes')
		
    elif(len(selection) == 1):
        raise TypeError ('Please Select at least two skinned Meshes')	

    textField_obj = cmds.textField( textFieldName, query=True, text=True )
    
    if(len(textField_obj) == 0):
        raise TypeError ('Please Assign a Name')
           
    if " " in textField_obj:
        raise TypeError("Warning: you are using illegal characters for the name")
          
    if cmds.objExists(textField_obj):
           raise TypeError("Warning: this name is already in use")
    
             
    for item in selection:       
        findSkinStart = mel.eval('findRelatedSkinCluster ' + item)
        
        if cmds.objExists (findSkinStart):
            print findSkinStart
                 
        else:
            raise TypeError("Please Select at least two skinned Meshes ") 
            
        matrix_array = cmds.getAttr(findSkinStart + ".matrix", mi = True)
    
        for i in matrix_array:
            list = cmds.connectionInfo(findSkinStart + ".matrix[" + str(i) + "]", sourceFromDestination = True)
            joint = list.split(".")
            joint_list.append(joint[0])         
                    
    if (len(selection) > 0):
            print selection
            for i in range(1):
                duplicateObj = cmds.duplicate (selection)
                createGrp = cmds.group (duplicateObj)        
                combine = cmds.polyUnite (createGrp, name = textField_obj)
                deleteHistory = cmds.delete (combine, ch=True)
                deleteGrp = cmds.select (cmds.delete (createGrp))
                cmds.textField( textFieldName, e=True, text='')   
                newskin = cmds.skinCluster(joint_list,textField_obj, n=textField_obj + "_SKC")
                newSelect = cmds.select (joint_list, selection, textField_obj, add= True )
                transfer = cmds.copySkinWeights (nm=True, sa ="closestPoint", ia ="closestJoint")
                delete = cmds.delete (selection)
                selectnewobj = cmds.select (textField_obj)
                cleanSkinEnd = mel.eval('removeUnusedInfluences ')
             
                
                deselect = cmds.select (cl=True)
                
              
def SeparateSkinnedMeshProc( *args):
    
    selection = cmds.ls(sl=True)
    
    if(len(selection) == 0):
        raise TypeError ('Please Select a Skinned Mesh')
		
    elif(len(selection) > 1):
        raise TypeError ('Please Select only one Skinned Mesh to separate')	

    textField_obj = cmds.textField( textFieldName, query=True, text=True )
    
    if(len(textField_obj) == 0):
        raise TypeError ('Please Assign a Name')
    
    if " " in textField_obj:
        raise TypeError("Warning: you are using illegal characters for the name")
        
    if cmds.objExists(textField_obj):
           raise TypeError("Warning: this name is already in use")  
    
    
    for item in selection:       
        findSkinStart = mel.eval('findRelatedSkinCluster ' + item)
        
        if cmds.objExists (findSkinStart):
            print findSkinStart
                 
        else:
            raise TypeError("Please Select a Skinned Mesh ")         
    
    if len (selection) > 0:
            print selection
            for i in range(1):
                duplicateObj = cmds.duplicate (selection, name = textField_obj)
                     
                separate = cmds.polySeparate (duplicateObj, name = textField_obj + "NewSkin*", ch=True)
                deleteHistory = cmds.delete (separate, ch=True)

                
                deselect01 = cmds.select (cl=True)
                selectnewmeshes = cmds.select( textField_obj, hi=True)
                deselGrp = cmds.select(textField_obj, d=True)
                givenlist = cmds.ls (sl=True)
                mesh = givenlist
                
                for index in range(len(mesh)):
                    print mesh[index]
                    joints = cmds.skinCluster (item , q=True , inf=True)
                    cmds.textField( textFieldName, e=True, text='')
                    for obj in mesh:
                        findSkinEnd = mel.eval('findRelatedSkinCluster ' + obj)
        
                        if cmds.objExists (findSkinEnd):
                            print findSkinEnd
                        else:
                            newskin = cmds.skinCluster(obj, joints, n=textField_obj + "_SKC")
                            break
                            
                    newSelect = cmds.select (joints, selection, obj , add= True)
                    transfer = cmds.copySkinWeights (nm=True, sa ="closestPoint", ia ="closestJoint")
                    cleanSkinEnd = mel.eval('removeUnusedInfluences ')
                       
                cmds.select (cl=True)
                cmds.delete (selection)
               


class CombineSeparateSkinnedMesh():
    def __init__(self):
        
        global textFieldName
        
        if cmds.window('CombSepSkinMeshWin', exists=True):
           cmds.deleteUI('CombSepSkinMeshWin')
		
        CombSepSkinMeshWin = cmds.window ("CombSepSkinMeshWin", title="Combine Separate Skinned Mesh", widthHeight=(300, 120), s=0)
        cmds.columnLayout(adjustableColumn=True )
        cmds.text( label='Assign Name to New Mesh' )
        textFieldName = cmds.textField()
        spacenoedit = cmds.textField( ed = False)
        cmds.button( label='Combine Skinned Mesh', c=CombineSkinnedMeshProc)
        cmds.button( label='Separate Skinned Mesh', c=SeparateSkinnedMeshProc)
        cmds.setParent( '..' )
        cmds.showWindow(CombSepSkinMeshWin)   
        
#CombineSeparateSkinnedMesh()                         
