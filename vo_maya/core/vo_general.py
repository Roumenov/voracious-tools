import pymel.core as pm
import maya.cmds as cmds
import math
import os as os
import pprint

#general utilities, no dependencies on the rest of vo-maya
p4_path = r'Z:\0_p4v'#NOTE:     can't end with \
pose_path = r"\Maya_sourcefiles\PoseLibrary"
project_path = r"0_p4v\PotionomicsSourceAssets\Art_sourcefiles\Characters"


def strip_string(operation = '', string = ''):
    if operation == 'prefix':
        return
    pass


def strip_suffix(inputString='', suffix=''):
    """
    Return string without suffix.
    """

    if inputString.endswith(suffix):
        remove = len(suffix)
        #print "removing prefix"
        output_string = inputString[:-remove]
        #print (output_string)
        return output_string
    else:
        #print "suffix not found"
        return False

def strip_prefix(inputString='', prefix=''):
    """
    Return string without prefix.
    """

    if inputString.startswith(prefix):
        remove = len(prefix)
        #print "removing prefix"
        output_string = inputString[remove:]
        # NOT SURE HOW TO SLICE NOTATE THIS CORRECTLY
        return output_string
    else:
        #print "prefix not found"
        return False


class NameString():
    def __init__(
            self,
            target):
                self.components = target.name().split('_')
                self.name = self.components[0]
                self.side = self.components[1]
                self.suffix = self.components[-1]  # ....    this isn't reliable
                # because of how many items end in numbers.. which is primarily
                # a symptom of maya's simplistic renaming when duplicating
                self.warble = '_'.join(self.components[2:-1])
                return

    def get_number(self):
        warble_components = self.warble.split('_')
        return warble_components[-1]



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
#USAGE          average_position(object1, object2, object3)
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
    loc_object = create_object(name = loc_name, objType = 'locator', radius = 5.0)
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


def freeze_worldspace(*targets):
    '''
    recomputes S/R/T values to use world zero as the zero'd out location
    '''
    #transform_list = pm.ls(sl=1)

    for transform in targets:
        original_location = pm.xform(transform, q=True, worldSpace = True, relative=True, rotatePivot=True)
        original_rotation = pm.xform(transform, query = True, rotation = True, worldSpace = True)
        transform_parent = transform.getParent()
        pm.parent(transform, world = True)
        pm.move (rotatePivotRelative = True, x=0, y=0, z=0)
        pm.makeIdentity(transform, apply = True, translate = True, rotate = False, scale = True)
        pm.xform(transform, ws=True, translation= original_location)


def euler_flip(target, axis = '+z'):
    """
    Rotate object 180 in object space
    @param target:      Object being rotated
    @param axis:        '+x', '+y', '+z', '-x', '-y', '-z'
    example usage: euler_flip(pm.ls(sl=1)[0], axis = '+y')
    """
    magnitude = int(axis[0] + str(180))
    
    if axis[1].lower() == 'x':
        euler = (magnitude,0,0)
    elif axis[1].lower() == 'y':
        euler = (0,magnitude,0)
    elif axis[1].lower() == 'z':
        euler = (0,0,magnitude)
    else:
        pm.warning('axis not recognized')
    try:
        pm.rotate(target, euler, relative = True, objectSpace = True, forceOrderXYZ = True)
        return axis
    except:
        pm.warning('rotation operation failed')


def match_pivot(source = None, target = None):
    #TODO:      use as basis for rewrite of object_on_pivot?
    """
    Match one object's pivot to another object's pivot without moving either object.
    @param source:      Object whose pivot is going to be matched.
    @param target:      Object whose pivot is going to be changed.
    """
    pivot_value = [(pm.xform (source, q=1, ws=1, piv=1))[0], (pm.xform (source, q=1, ws=1, piv=1))[1], (pm.xform (source, q=1, ws=1, piv=1))[2]]
    pm.xform (target, worldSpace = True, piv=(pivot_value))


def create_primitive(name='', primitive='cube', axis='y'):
    """
    create primitive, just as exciting as it sounds!
    @param primitive:       takes 'cube', 'cylinder', 'capsule', 'sphere', 'plane', or 'torus'
    @param axis:        takes 'x', 'y', 'z', '-x', '-y', '-z'
    """
    axis_coordinates = {'x' : [1, 0, 0], 'y' : [0, 1, 0], 'z' : [0, 0, 1], '-x' : [-1, 0, 0], '-y' : [0, -1, 0], '-z' : [0, 0, -1]}
    if primitive == 'cube':
        primitive_mesh = pm.polyCube()
    elif primitive == 'cylinder':
        primitive_mesh = pm.polyCylinder(axis=axis_coordinates[axis], radius=1, height=2,
            roundCap=False, subdivisionsX=12, subdivisionsY=1, subdivisionsZ=0)
    elif primitive == 'capsule':
        primitive_mesh = pm.polyCylinder(axis=axis_coordinates[axis], radius=1, height=2,
            roundCap = True, subdivisionsX=12, subdivisionsY=4, subdivisionsZ=4)
    elif primitive == 'sphere':
        primitive_mesh = pm.polySphere(axis=axis_coordinates['-x'], radius = 1, subdivisionsX=12, subdivisionsY=8)
    elif primitive == 'plane':
        primitive_mesh = pm.polyPlane(axis=axis_coordinates[axis], height = 2.0, width = 2.0, subdivisionsX=1, subdivisionsY=1)
    elif primitive == 'torus':
        primitive_mesh = pm.polyTorus(axis=axis_coordinates[axis],
            radius=1, sectionRadius=0.5, subdivisionsX=12, subdivisionsY=8)
    elif primitive == 'cone':
        primitive_mesh = pm.polyCone(axis=axis_coordinates[axis], radius=1, height=2,
            roundCap=False, subdivisionsX=12, subdivisionsY=1, subdivisionsZ=0)
    else:
        primitive_mesh = pm.polyCube(height = 1, width=1, subdivisionsX=0, subdivisionsY=0, subdivisionsZ=0)
    return primitive_mesh


def create_object(name = '', objType = '', radius = 1.0):
    """
    Create various basic objects. Default is group.
    @param objType: String input accepts, locator, group, sphereShape, cubeShape, coneShape, joint, circleCTL, squareCTL, boxCTL, sphereCTL, arrowX, arrowY, or arrowZ.
    """
    pm.select(clear = True)
    if objType == 'locator':
        output = pm.spaceLocator(name = name, relative = True)
        output.setAttr('localScaleX', radius) 
        output.setAttr('localScaleY', radius) 
        output.setAttr('localScaleZ', radius)
    elif objType == 'group':
        output = pm.group(name = name, world=True)
    elif objType == 'sphereShape':
        #shape_name = name + 'Shape'
        output = pm.createNode('renderSphere') # name = name
        output.setAttr('radius', radius)
        output = output.listRelatives(parent = True)[0]
        pm.rename(output, name)
    elif objType == 'cubeShape':
        #shape_name = name + 'Shape'
        output = pm.createNode('renderBox')
        output.setAttr('sizeX', radius)
        output.setAttr('sizeY', radius)
        output.setAttr('sizeZ', radius)
        output = output.listRelatives(parent = True)[0] # can also use output.getParent()
        pm.rename(output, name)
    elif objType == 'coneShape':
        #shape_name = name + 'Shape'
        output = pm.createNode('renderCone')
        output.setAttr('coneAngle', radius*10)
        output = output.listRelatives(parent = True)[0]
        pm.rename(output, name)
    elif objType == 'joint':
        output = pm.joint(name = name, radius = radius)
    elif objType == 'circleCTL': ##----tries to parent shape instead of transform
        output = pm.circle (ch = 1, name = name, radius = radius, nrx = 1, nry = 0, nrz = 0)[0]
    elif objType == 'squareCTL':
        output = pm.curve(name = name, degree = 1, point = [(1,0,1), (-1,0,1), (-1,0,-1), (1,0,-1), (1,0,1)], knot =[0,1,2,3,4])[0]
    elif objType == 'boxCTL':
        cornerPos = radius * 0.5
        output = pm.curve(name = name, degree = 1, point = [(-cornerPos, cornerPos, cornerPos),(cornerPos,cornerPos,cornerPos), (cornerPos,-cornerPos,cornerPos), (-cornerPos, -cornerPos,cornerPos), (-cornerPos,cornerPos,cornerPos), (-cornerPos, cornerPos, -cornerPos), (-cornerPos,-cornerPos,-cornerPos), (cornerPos,-cornerPos,-cornerPos), (cornerPos,-cornerPos,cornerPos),(cornerPos,cornerPos,cornerPos), (cornerPos,cornerPos,-cornerPos), (cornerPos, -cornerPos,-cornerPos), (cornerPos,cornerPos,-cornerPos), (-cornerPos,cornerPos,-cornerPos), (-cornerPos,-cornerPos,-cornerPos), (-cornerPos,-cornerPos,cornerPos)], knot =[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])[0]
    elif objType == 'sphereCTL':
        output = pm.circle (ch = 1, name = name, radius = radius, nrx = 1, nry = 0, nrz = 0)[0]
        pm.circle (ch = 1, name = name + 'subRingY', radius = radius, nrx = 0, nry = 1, nrz = 0)
        pm.circle (ch = 1, name = name + 'subRingZ', radius = radius, nrx = 0, nry = 0, nrz = 1)
        pm.select(clear = True)
        pm.select(name + 'subRingYShape', name + 'subRingZShape', output)
        pm.parent(relative=True,shape=True)
    elif objType == 'arrowX':
        output = pm.curve(name = name + '_arrow', degree = 1, point = [(0,0,0), (0,0,13), (0,1,11), (0,-1,11), (0,0,13), (1,0,11), (-1,0,11), (0,0,13)], knot =[0,1,2,3,4,5,6,7])
        pm.xform(output, relative = True, scale = (radius,radius,radius))
        pm.xform(output, relative = True, rotation = (0,90,0))
        pm.makeIdentity(output, apply = True)
    elif objType == 'arrowY':
        output = pm.curve(name = name + '_arrow', degree = 1, point = [(0,0,0), (0,0,13), (0,1,11), (0,-1,11), (0,0,13), (1,0,11), (-1,0,11), (0,0,13)], knot =[0,1,2,3,4,5,6,7])
        pm.xform(output, relative = True, scale = (radius,radius,radius))
        pm.xform(output, relative = True, rotation = (-90,0,0))
        pm.makeIdentity(output, apply = True)
    elif objType == 'arrowZ':
        output = pm.curve(name = name + '_arrow', degree = 1, point = [(0,0,0), (0,0,13), (0,1,11), (0,-1,11), (0,0,13), (1,0,11), (-1,0,11), (0,0,13)], knot =[0,1,2,3,4,5,6,7])
        pm.xform(output, relative = True, scale = (radius,radius,radius))
        pm.makeIdentity(output, apply = True)
    elif objType == 'segment':#TODO create line segment, add rounded square
        #output = pm.curve( d = 1,p = [[0.0, 0.0, -0.5], [0.0, 0.0, 0.5]],k = (0.0, 1.0))
        output = pm.curve( d = 1,p = [[0.0, 0.5, 0], [0.0, -0.5, 0]],k = (0.0, 1.0))
        #curve -d 1 -p 0 0 -1 -p 0 0 1 -k 0 -k 1 ;
        #output = pm.curve(name = name + '_arrow', degree = 1, point = [(0,0,0), (0,0,13), (0,1,11), (0,-1,11), (0,0,13), (1,0,11), (-1,0,11), (0,0,13)], knot =[0,1,2,3,4,5,6,7])
        pm.xform(output, relative = True, scale = (radius,radius,radius))
        pm.makeIdentity(output, apply = True)
    elif objType == 'squareRound':#TODO create line segment, add rounded square
        output = pm.curve( d = 3,p = [[-0.5, 0.38888888888888884, 0.0], [-0.5, 0.41666666666666663, 0.0], [-0.47222222222222227, 0.47222222222222227, 0.0], [-0.41666666666666663, 0.5, 0.0], [-0.38888888888888884, 0.5, 0.0], [0.0, 0.5, 0.0], [0.38888888888888884, 0.5, 0.0], [0.41666666666666663, 0.5, 0.0], [0.47222222222222227, 0.47222222222222227, 0.0], [0.5, 0.41666666666666663, 0.0], [0.5, 0.38888888888888884, 0.0], [0.5, -0.38888888888888884, 0.0], [0.5, -0.41666666666666663, 0.0], [0.47222222222222227, -0.47222222222222227, 0.0], [0.41666666666666663, -0.5, 0.0], [0.38888888888888884, -0.5, 0.0], [0.0, -0.5, 0.0], [-0.38888888888888884, -0.5, 0.0], [-0.41666666666666663, -0.5, 0.0], [-0.47222222222222227, -0.47222222222222227, 0.0], [-0.5, -0.41666666666666663, 0.0], [-0.5, -0.38888888888888884, 0.0], [-0.5, 0.0, 0.0], [-0.5, 0.38888888888888884, 0.0]],k = (0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 21.0, 21.0))
        #output = pm.curve(name = name + '_arrow', degree = 1, point = [(0,0,0), (0,0,13), (0,1,11), (0,-1,11), (0,0,13), (1,0,11), (-1,0,11), (0,0,13)], knot =[0,1,2,3,4,5,6,7])
        pm.xform(output, relative = True, scale = (radius,radius,radius))
        pm.makeIdentity(output, apply = True)
    else:
        output = pm.group(name = name, world=True)
        #need to expound on this later....
    pm.addAttr(output, longName = 'metaParent', attributeType = 'message')
    return output

#create_object(name = 'test_LOC', objType = 'locator', radius = 1.0)

# nest_transform()
#PURPOSE
#PROCEDURE          check suffix and set name, object based on arg
#PRESUMPTIONS       user inputs corremt name, takes only one explicit target at a time

def nest_transform(name, action, target = None, transformObj = 'locator', transformRadius = 1.0):
    """
    Creates a transform inside a hierarchy.
    @param action: 'parent' makes new transform parent of target.
                    'child' makes it child.
                    'adopt' makes child and adopts all child transforms.
                    #TODO:  add 'sibling' to parent xform to target's parent
    """
    nested_transform = None
    if not target:
        pm.warning('no target provided')
        return None
    target_name = str(target)
    if len(name): #set transform name to arg value
        transform_name = name
    else:
        transform_name = target_name + '_nest'
    nested_transform = create_object(name = transform_name, objType = transformObj, radius = transformRadius)
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
def replace(source_object, target, useTargetName = True, clearSource = False):
    #object_list = pm.ls (sl = 1)
    #source_object = object_list[0]
    transform_name = str(source_object)
    current_replacement = pm.duplicate(source_object)[0]
    pm.matchTransform(current_replacement, target, scale = False)
    target_parent = pm.listRelatives(target, parent = True, type = 'transform')[0]
    target_children = pm.listRelatives(target, children = True, type = 'transform')
    if target_parent:
        #print( 'parenting to :: ' + str(target_parent))
        target_parent | current_replacement
    else:
        #print( 'parent is world')
        pass
    for child in target_children:
        current_replacement | child
    pm.delete(target)
    if useTargetName:
        pm.rename(current_replacement,str(target))
    else:
        pm.rename(current_replacement, source_object.shortName())
        #print('using source name')
    if clearSource:
        pm.delete(source_object)
    else:
        pass
        #print('preserved source object')

def multi_replace(source_object, *target_objects):
    #target_list = object_list[1:]
    for target in target_objects:
        replace(source_object, target, useTargetName = True, clearSource = False)
    return

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

def object_on_vertices(vertices, name = '', objType = '', radius = 1.0):
    """Make cluster on vertex list and replace with given object type.
    @param vertices: flat list of vertices
    """
    center_cluster = pm.cluster(vertices)
    new_object = create_object(name = name, objType = objType, radius = radius)
    pm.matchTransform(new_object, center_cluster, scale = False)
    pm.delete(center_cluster)
    return new_object
#object_on_vertex(name = 'test_joint', objType = 'joint', radius = 1.0)


def primitive_on_vertices(vertices, name = '', primitive = 'cube', axis='y', radius = 1.0):
    """Make cluster on vertex list and replace with given primitive type.
    @param vertices: flat list of vertices
    """
    center_cluster = pm.cluster(vertices)
    new_primitive = create_primitive(name=name, axis=axis, primitive=primitive)
    pm.matchTransform(new_primitive, center_cluster, scale = False)
    pm.delete(center_cluster)
    return new_primitive


def object_on_pivot(objType = 'joint'):
    #TODO:      check functionality and udpate to support object function
	"""
	Create a bone from the customPivot context
	In component mode of a mesh:
	Press "D" or "Insert" to go into custom pivot context
	  If you click on edges verts or faces the pivot will auto align
	  If you want to aim an axis click on the axis and Ctrl+Shift on another vert/edge/face to aim it
	  When you have the pivot you want run this to create the joint with that pivot
	*Arguments:*
		* objType currently does nothing
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

#output_curve_name = prompt_string(promptTitle = 'Offset String', promptMessage = 'Enter string to use for curve name')
#selection = pm.ls(sl=1, flatten = True)
#curve_on_vertices(name = output_curve_name, vertices = selection)




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

#output_curve_name = prompt_string(promptTitle = 'Curve Name', promptMessage = 'Enter curve name')
#selection = pm.ls(sl=1)
#curve_on_transforms(name = output_curve_name, transforms = selection)


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
        current_object = create_object(name = current_name, objType = obj_type, radius = 1.0)
        motion_path = pm.pathAnimation(curve,current_object, fractionMode = True, follow = True, followAxis = 'z', upAxis = 'y', worldUpType = 'vector', worldUpVector = (0,1,0), inverseUp = False, inverseFront = False, bank = False, startTimeU = u_value)
    return motion_path
#transform_count = int(prompt_string())
#transform_on_curve(count = transform_count, start_transform = True,end_transform = True)


def curve_chain():
    pass
    #output_curve_name = prompt_string(promptTitle = 'Offset String', promptMessage = 'Enter string to use for offset')
    #transform_list = pm.ls(sl=True)
    
    #curve_on_transforms(name = output_curve_name, transforms = transform_list)

    #transform_count = int(prompt_string())
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
        vector = (1,0,0)
    elif axis == '+y':
        vector = (0,1,0)
    elif axis == '+z':
        vector = (0,0,1)
    elif axis == '-x':
        vector = (-1,0,0)
    elif axis == '-y':
        vector = (0,-1,0)
    elif axis == '-z':
        vector = (0,0,-1)
    else:
        pass
    skip_val = 'x' # used to read letter value "axis[1]"
    proxy_name = str(aimer)+'_aimer'
    aim_proxy = create_object(name = proxy_name, objType = 'locator')
    pm.matchTransform(aim_proxy, aimer)
    aim_constraint = pm.aimConstraint(target,aim_proxy, aimVector = vector, worldUpType = 'scene', skip = skip_val)
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


def load_csv(sourcename = '', targetname = '', filename = 'JointMapping.csv', directory = 'Z:/0_p4v/PotionomicsSourceAssets/Art_sourcefiles/Characters/'):
    """
    Load a csv file and return columns as lists
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
#src_list, dest_list = load_csv(sourcename = '', targetname = '', filename = 'JointMapping.csv', directory = 'Z:/0_p4v/PotionomicsSourceAssets/Art_sourcefiles/Characters/')

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
                    pm.matchTransform(source_object, pm.ls(dest_string)[0], pos = True, rot = True, scale = False)
                except:
                    pm.warning('failed match')
            else:
                pass
        else:
            pm.warning('no length')
            pass
    print('fin')

#list_match(source_list = src_list,destination_list = dest_list, operation = 'match', sourceName = ['skel_', 'Skel_'], destName = ['character_','Luna_'])


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

#list_rename(source_list=genchar_table[0],destination_list=genchar_table[1], sourceName = ['character_','GenChar_'], destName = ['skel_', 'skel:Skel_'])

