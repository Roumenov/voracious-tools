

import maya.cmds as cmds
import pymel.core as pm
import vo_general as general
import vo_meta as meta
import Red9.core.Red9_Meta as r9Meta


class Control():#TODO   search/replace references to pControl with Control
    """
    class for building controls for potionomics rigs
    """
    def __init__(
                self,
                target,
                name = '',
                orient = 'x',
                scale = 1.0,
                parent = '',
                lock_channels = [],
                line_width = 1.0,
                control_type = 'controller'
                ):
        """
        @param target: Required. Object to constrain to control.
        @param name: Name for control, defaults to target if empty.
        @param parent: Transform to parent root_offset to.
        @param control_type: what tag to put on controller. Current options are controller or microController.
        """
        target_object = pm.ls(target)[0]
        if len(name):
            base_name = name
        #elif pm.objExists(target_object):
        else:
            base_name = str(target_object)
        if orient == 'y':
            self.control_object = pm.circle (ch = 1, name = base_name + '_CTL', radius = scale, nrx = 0, nry = 1, nrz = 0)[0]
        elif orient == 'z':
            self.control_object = pm.circle (ch = 1, name = base_name + '_CTL', radius = scale, nrx = 0, nry = 0, nrz = 1)[0]
        else:
            self.control_object = pm.circle (ch = 1, name = base_name + '_CTL', radius = scale, nrx = 1, nry = 0, nrz = 0)[0]

        self.root_offset = general.nest_transform(name = base_name + '_GRP', action = 'parent', target = self.control_object, transformObj = 'group')
        #pm.group(name = base_name + '_GRP', world = True)
        
        if pm.objExists(parent):
            pm.parent(self.root_offset,parent)
        else:
            pass
        
        #tagging
        pm.addAttr(self.control_object, longName = 'metaParent', attributeType = 'message')
        if control_type == 'microController':
            pm.addAttr(self.control_object, longName = 'microController', attributeType = 'message')
        else:
            pm.addAttr(self.control_object, longName = 'controller', attributeType = 'message')
        if target_object.hasAttr('metaParent'):
            print('metaParent exists')
        else:
            pm.addAttr(target_object, longName = 'metaParent', attributeType = 'message')

        self.control_object.metaParent >> target_object.metaParent
        pm.matchTransform(self.root_offset, target_object, pos = True, rot = True, scale = False)
        tr_constraint = pm.parentConstraint (self.control_object,target_object, mo = 1, weight = 1)
        tr_constraint.setAttr('interpType', 2)
        #s_constraint =
        pm.scaleConstraint(self.control_object,target_object, mo = True)
        
        self.control_object.setAttr('lineWidth', line_width)
        general.attr_lock(self.control_object, attr = 'visibility', lock = True)
        if len(lock_channels):
            for attribute_val in lock_channels:
                if type(attribute_val) == 'string':
                    general.attr_lock(self.control_object, attr = attribute_val, lock = True)
            
        #public members
        #self.control = control_object
        #self.root = root_offset

    def offset(self, offsets = 1):
        for index in range(offsets):
            #create name
            if index <= 1:
                current_offset_name = base_name + '_OST'
            else:
                current_offset_name = base_name + '_OS' + str(index + 1)
            #create group
            last_offset = general.nest_transform(name = current_offset_name, action = 'parent', target = last_offset, transformObj = 'group')
            #parent offset under previous offset
            #save ref to this offset
    def link(self, target, position = 'parent', offset = '_GRP', link = 'constrain'):
        if position == 'parent':
            link_controls(parent = self,child = target, offset = offset, link = 'constrain')
            pass
        elif position == 'child':
            link_controls(parent = target,child = self, offset = offset, link = 'constrain')
        else:
            pm.error("Argument not recognized, position accepts 'child' or 'parent'")


def get_constraints1():
    constraint = set(pm.listConnections(target, source = True, type = 'constraint')).pop()
    #print(constraint)
    sources = list(set(constraint.listConnections(source = True, type = 'transform')))
    sources.remove(target)
    return
def get_constraints(target):
    constraints = set(pm.listConnections(target, source = True, type = 'constraint')).pop()
    #print(constraint)
    return constraints

def get_constraint_sources(constraint):
    sources = list(set(constraint.listConnections(source = True, type = 'transform')))
    destinations = list(set(constraint.listConnections(destination = True, type = 'transform')))
    sources.remove(constraint)
    return sources#first item is the constraint target


def rebuild_constraint(target,constraint):
    constraint_type = pm.nodeType()
    store_constraint(target,constraint)
    if constraint_type == 'parentConstraint':
        restore_constraint(target, attr = 'parentConstraintStore')
    elif constraint_type == 'scaleConstraint':
        restore_constraint(target, attr = 'scaleConstraintStore')
    elif constraint_type == 'orientConstraint':
        restore_constraint(target, attr = 'orientConstraintStore')
    elif constraint_type == 'aimConstraint':
        pass
    else:
        return


def multi_constrain(satellites = [], target = None, constraintType = 'parent', normalize = True):
    '''
    Constrains target object to n satellites and normalizes the influence to add up to 1.0
    @param satellites: 
    @param constraintType: parent, orient, or point
    @param target: object getting constrained to the satellites
    @return constraint:  the multi influence constraint affecting target
    '''
    influences = general.distance_influence_calc(satellites, target)
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


def store_constraint(target,constraint):
    '''
    @param target:  object to write constraint data to
    @param constraint:  constraint who's data to store
    '''
    node = r9Meta.MetaClass(target.name())
    print(constraint)
    sources = list(set(constraint.listConnections(source = True, type = 'transform')))
    sources.remove(target)#TODO: this is teling, update get_constraint_sources while keeping in mind what object is target here, vas there
    constraint_sources = {}
    for item in sources:
        if type(item) == pm.nodetypes.Constraint:
            pass
        else:
            constraint_sources[item.name()] = constraint.getWeight(item)
    
    if type(constraint) == pm.nodetypes.ParentConstraint:
        node.addAttr('parentConstraintStore', constraint_sources)
        #print item
    elif type(constraint) == pm.nodetypes.ScaleConstraint:
        node.addAttr('scaleConstraintStore', constraint_sources)
        #print item
    elif type(constraint) == pm.nodetypes.OrientConstraint:
        node.addAttr('orientConstraintStore', constraint_sources)
        #print item
    else:
        pm.warning('constraint type not supported')
    pm.delete(constraint)


def store_all_constraints(target):
    target_constraints = set(pm.listConnections(target, source = True, type = 'constraint'))#.pop()
    for constraint in target_constraints:
        print constraint
        print type(constraint)
        store_constraint(target,constraint)


def restore_constraint(target, attr = 'parentConstraintStore'):
    node = r9Meta.MetaClass(target.name())
    if attr == 'parentConstraintStore':
        constraint_sources = node.parentConstraintStore
        sources = pm.ls(constraint_sources.keys())
        constraint = pm.parentConstraint(sources, target, maintainOffset = True)
        constraint.setAttr('interpType', 2)
        for index in range(len(sources)):
            name = sources[index].name()#.stripNamespace()
            constraint.setAttr(name+'W'+str(index), constraint_sources[name])
        node.delAttr('parentConstraintStore')
        return
    elif attr == 'orientConstraintStore':#TODO:     test this function
        constraint_sources = node.orientConstraintStore
        sources = pm.ls(constraint_sources.keys())
        constraint = pm.orientConstraint(sources, target, maintainOffset = True)
        constraint.setAttr('interpType', 2)
        for index in range(len(sources)):
            name = sources[index].name()#.stripNamespace()
            constraint.setAttr(name+'W'+str(index), constraint_sources[name])
        node.delAttr('orientConstraintStore')
        return
    elif attr == 'scaleConstraintStore':
        constraint_sources = node.scaleConstraintStore
        sources = pm.ls(constraint_sources.keys())
        constraint = pm.scaleConstraint(sources, target, maintainOffset = True)
        for index in range(len(sources)):
            name = sources[index].name()#.stripNamespace()
            constraint.setAttr(name+'W'+str(index), constraint_sources[name])
        node.delAttr('scaleConstraintStore')
        return
    else:
        pm.warning('valid constraintStore not found')



def link_controls(parent,child, offset = '_GRP', link = 'constrain'):
    """
    Constrains child control's root group to parent control and connects metaParent attr.
    @param link: type of link to make, "constraint" to makes parent constraint, "connect" to connect attribute values
    """
    parent.metaParent >> child.metaParent
    #child.root_offset
    child_offset = str(child).replace('_CTL',offset)        ##not reliable, need to upgrade to use class features
    #if general.check_connections(target = child_offset):
    #    constraint = pm.parentConstraint (parent,child_offset, mo = 1, weight = 1)
    #else:
    #    child_offset = general.nest_transform(name = str(child).replace('_CTL','_OST'), action = 'parent', target = child, transformObj = 'group')
    #    constraint = pm.parentConstraint (parent,child_offset, mo = 1, weight = 1)
    constraint = pm.parentConstraint (parent,child_offset, mo = 1, weight = 1)
    constraint.setAttr('interpType', 2)
    pm.scaleConstraint(parent,child_offset, mo = True)


def chain_controls(controls, offset = '_GRP'):
    """
    Link a list of controls
    """
    control_count = len(controls)-1
    print control_count
    for control_index in range(0,control_count):
        link = controls[control_index]
        print link
        next_control = controls[control_index + 1]
        print next_control
        link_controls(link, next_control, offset)
        #link.metaParent >> next_control.metaParent



def match_micro(source, flip = 'none'):
    if source.hasAttr('microController'):
        try:
            joint_target = general.meta_traverse(source = source, relation = 'child', tag = 'jointSkin')[0]
            control_grp = pm.ls(str(source).replace('_CTL','_GRP'))[0]
        except:
            pm.warning('problem finding joint_target or control_grp')
        try:
            pm.delete(control_grp, constraints = 1)
            pm.matchTransform(control_grp, joint_target, pos = True, rot = True, scale = False)
        except:
            pm.warning('failed to matchTransform')
        try:
            tr_constraint = pm.parentConstraint (source,joint_target, mo = 1, weight = 1)
            tr_constraint.setAttr('interpType', 2)
            sc_constraint = pm.scaleConstraint(source,joint_target, mo = 1, weight = 1)
        except:
            pm.warning('failed to constrain')
        if 'x' in flip:
            pm.xform(source, euler = True, rotation = [180,0,0])
        elif 'y' in flip:
            pm.xform(source, euler = True, rotation = [0,180,0])
        elif 'z' in flip:
            pm.xform(source, euler = True, rotation = [0,0,180])
        else:
            pm.warning('controller attr present ')
            pass
    elif source.hasAttr('controller'):
        pm.warning("make sure this doesn't fuck anything!")
        try:
            joint_target = general.meta_traverse(source = source, relation = 'child', tag = 'jointSkin')[0]
            control_grp = pm.ls(str(source).replace('_CTL','_GRP'))[0]
        except:
            pm.warning('problem finding joint_target or control_grp')
        try:
            pm.delete(control_grp, constraints = 1)
            pm.matchTransform(control_grp, joint_target, pos = True, rot = True, scale = False)
        except:
            pm.warning('failed to matchTransform')
        try:
            tr_constraint = pm.parentConstraint (source,joint_target, mo = 1, weight = 1)
            tr_constraint.setAttr('interpType', 2)
            sc_constraint = pm.scaleConstraint(source,joint_target, mo = 1, weight = 1)
        except:
            pm.warning('failed to constrain')
        if 'x' in flip:
            pm.xform(source, euler = True, rotation = [180,0,0])
        elif 'y' in flip:
            pm.xform(source, euler = True, rotation = [0,180,0])
        elif 'z' in flip:
            pm.xform(source, euler = True, rotation = [0,0,180])
        else:
            pm.warning('controller attr present ')
            pass
        pass
    else:
        pm.warning('no controller or microController attr')
        pass
    pass

def match_macro(source):
    if source.hasAttr('controller'):
        try:
            #joint_target = general.meta_traverse(source = source, relation = 'child', tag = 'jointSkin')[0]
            control_grp = pm.ls(str(source).replace('_CTL','_GRP'))[0]
            child_controls = general.meta_traverse(source = source, relation = 'child', tag = 'jointSkin')[0]
            target_locator = general.nest_transform(name = str(source)+ '_target_position', action = 'child', target = source, transformObj = 'locator', transformRadius = 1.0)
            pm.parent(target_locator, world = True)
            brow_position = general.average_position(*brow_controls)
            offset_joint = pm.joint(name = str(brow_main_control)+ '_offset_thing', relative = False, radius = 2, position = brow_position)
            pm.parent(offset_joint, world = True)
            offset_joint | target_locator
        except:
            pm.warning('problem finding target location')
        try:
            for micro_controller in brow_controls:
                joint_target_list = joint_target_list+ [general.meta_traverse(source = control_object, relation = 'child', tag = 'jointSkin')[0]]
            final_position = general.average_position(*joint_target_list)
            pm.xform(offset_joint, translation = final_position, worldSpace = True)
            pm.matchTransform(brow_main_grp, target_position, pos = True, rot = False, scale = False)
            pm.delete(offset_joint)
            pass
        except:
            pm.warning('problem finding target location')
        try:
            pm.delete(source, constraints = 1)
            pm.matchTransform(control_grp, joint_target, pos = True, rot = True, scale = False)
        except:
            pm.warning('failed to matchTransform')

        if '_R_' in str(control_object):
            pm.xform(control_object, euler = True, rotation = [0,0,180])
        else:
            pass
    elif source.hasAttr('controller'):
        pass
    else:
        pm.warning('no controller or microController attr')
        pass
    pass



def constrain_list(listA,listB):
    #iterate through listA by index, then match it to listB?
    source_list = targets[::2]
    target_list = targets[1::2]
    for index, object in enumerate(source_list):
        print(str(object))
        object_target = target_list[index]

    #================== ----------- 
    for index, source_object in enumerate(source_list):
        print(str(source_object))
        target_name = str(source_object).replace('fat_male', target_string)
        target_object = pm.ls(target_name)[0]
        pm.matchTransform(source_object, target_object, pos = True, rot = True, scale = False)

    objectList = pm.ls (sl = 1)
    sourceObj = objectList[0]
    targetList = objectList[1:]
    for target in targetList:
        transformName = str(sourceObj)
        currentReplacement = pm.duplicate(sourceObj)
        pm.matchTransform(currentReplacement, target)
        #rename?
        if useTargetName == True:
            #transformName = str(item)
            pm.rename(currentReplacement,str(target))
        else:
            print('using source name')
        #delete target
        targetParent = str(pm.listRelatives(target, parent = True)[0])
        print(targetParent)


def break_trs_connections(target):
    for character in 'XYZ':
            target_attr = 'translate' + character
            target.disconnectAttr(target_attr)
            target_attr = 'rotate' + character
            target.disconnectAttr(target_attr)
            target_attr = 'scale' + character
            target.disconnectAttr(target_attr)
    return

