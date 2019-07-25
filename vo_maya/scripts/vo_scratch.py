import pymel.core as pm
import vo_usefulFunctions as uf
reload(uf)

target_list = pm.ls(sl=1)
metaparents = range(len(target_list))
for index in range(0, len(target_list)):
    metaparents[index] = uf.meta_traverse(source = target_list[index], relation = 'parent', tag = '')
pm.select(metaparents)

target_list = pm.ls(sl=1)
metachildren = range(len(target_list))
for index in range(0, len(target_list)):
    metachildren[index] = uf.meta_traverse(source = target_list[index], relation = 'child', tag = '')
pm.select(metachildren)

import xml.etree.ElementTree as ET
xml_root = ET.parse('Z:/0_p4v/PotionomicsSourceAssets/Art_sourcefiles/Characters/scenes/Rigs/GenChar/clusters/MaleAverageNew.xml').getroot()
joints = []
for type_tag in xml_root.findall('weights'):
    value = type_tag.get('source')
    joints.append(value)
    #print(value)
print joints

for entry in joints:
    try:
        pm.select(entry, add=True)
    except:
        print(entry)



src_list, dest_list = uf.load_csv(sourcename = '', targetname = '', filename = 'JointMapping.csv', directory = 'Z:/0_p4v/PotionomicsSourceAssets/Art_sourcefiles/Characters/')
print dest_list
uf.list_match(source_list = src_list,destination_list = dest_list, operation = 'match', sourceName = ['skel_', 'Skel_'], destName = ['character_','mesh:GenChar_'])
uf.list_constrain(source_list=dest_list,destination_list=src_list, sourceName = ['character_','Xidriel_'], destName = ['skel_', 'Skel_'])

uf.list_rename(source_list=dest_list,destination_list=src_list, sourceName = ['character_','Skel_'], destName = ['skel_', 'Skel_'])


pm.select(pm.ls('*:pipe_ctrl', objectsOnly = True), replace = True)
pm.ls('*.jointSkin', objectsOnly = True)

pm.select(pm.ls('*stache*', objectsOnly = True), replace = True)


pm.addAttr(longName = 'costume', type = 'string')
pm.addAttr(longName = 'RRARigName', type = 'string')
pm.addAttr(longName = 'jointSkin', attributeType = 'message')

eye_ramp = pm.ls('geo:R_eye_ramp')[0]
eye_joints = pm.ls(sl=1)
eye_control = pm.ls(sl=1)[0]
#checked items fill list of attrs
#'blink'
eye_parts = ('pupil', 'iris') #'offset'
eye_attrs = ('radius', 'shape', 'angle', 'stretch')
#pm.addAttr(longName = 'iris', type = 'float')

for joint in eye_joints:
    if '_L_' in joint.name():
        side = 'L'
    elif '_R_' in joint.name():
        side = 'R'
    else:
        side = None
    setup_eye_attrs(joint=joint, control = eye_control, ramp = eye_ramp)

def setup_eye_attrs(joint, control, ramp, pupil = False, side = None):
    if joint.hasAttr('blink'):
        pass
    else:
        pm.addAttr(joint,longName = 'blink', attributeType = 'double', defaultValue = 0.0, minValue = -1.0, maxValue = 1.0)
        joint.setAttr('blink', keyable = True)
    
        
    
    eye_control.new_control_attr >> joint.attr



def setup_iris_attrs(joint, control, ramp, side = None):
    if joint.hasAttr('radius'):
        pass
    else:
        radius_attr = pm.addAttr(joint,longName = 'radius', attributeType = 'double', defaultValue = 1.0, minValue = 0.0, maxValue = 1.0)
        joint.setAttr('radius', keyable = True)
    
    if side:
        control_radius = side+'Radius'#+attr[0].upper()+attr[1:]
    else:
        control_radius = 'radius'
    
    if control.hasAttr(control_radius):
        pass
    else:
        pm.addAttr(joint,longName = control_radius, attributeType = 'double', defaultValue = 1.0, minValue = 0.0, maxValue = 1.0)
        joint.setAttr(control_radius, keyable = True)
    
    pm.addAttr(item,longName = 'RIrisShape', attributeType = 'double', defaultValue = 0.0)
    item.setAttr('RIrisShape', keyable = True)
    pm.addAttr(item,longName = 'RIrisAngle', attributeType = 'double', defaultValue = 0.0)
    item.setAttr('RIrisAngle', keyable = True)
    
    radius_default = float(eye_ramp.getAttr('colorEntryList[1]')[0])#pm.getAttr(eye_ramp.colorEntryList[1].position)
    #pm.shadingNode('floatMath', asUtility = True, name = 'test')
    radius_math = pm.createNode('floatMath', name = str(side+'irisRadius_FM')) #float math to add
    radius_math.setAttr('floatA', radius_default)
    radius_math.setAttr('operation', 2)
    radius_attr >> radius_math.floatB
    radius_math.outFloat >> eye_ramp.colorEntryList[1].position
    pass

def setup_pupil(joint, control, eye_ramp):
    #make pupil
    #setAttr geo:R_eye_ramp.colorEntryList[2].color -type double3 0.404 0 0;
    #setAttr geo:R_eye_ramp.colorEntryList[2].position 0.0299401;
    
    pass

if joint.hasAttr(attr):
    pass
else:
    pm.addAttr(joint,longName = attr, attributeType = 'double', defaultValue = 0.0, minValue = -1.0, maxValue = 1.0)
    joint.setAttr(attr, keyable = True)
pass


for item in eye_targets:
    if item.hasAttr('RBlink'):
        pass
    else:
        pm.addAttr(item,longName = 'R_blink', attributeType = 'double', defaultValue = 0.0, minValue = -1.0, maxValue = 1.0)
        item.setAttr('RBlink', keyable = True)
    if item.hasAttr('LBlink'):
        pass
    else:
        pm.addAttr(item,longName = 'R_blink', attributeType = 'double', defaultValue = 0.0, minValue = -1.0, maxValue = 1.0)
        item.setAttr('LBlink', keyable = True)
    if item.hasAttr('pupilRadius'):
        pass
    else:
        pm.addAttr(item, longName = 'RPupilRadius', attributeType = 'double', defaultValue = 1.0)
        item.setAttr('RPupilRadius', keyable = True)
    if item.hasAttr('RIrisRadius'):
        pass
    else:
        pm.addAttr(item,longName = 'RIrisRadius', attributeType = 'double', defaultValue = 1.0)
        item.setAttr('RIrisRadius', keyable = True)
    if item.hasAttr('LIrisRadius'):
        pass
    else:
        pm.addAttr(item,longName = 'LIrisRadius', attributeType = 'double', defaultValue = 1.0)
        item.setAttr('LIrisRadius', keyable = True)
    
    pm.addAttr(item,longName = 'LStretchX', attributeType = 'double', defaultValue = 1.0)
    item.setAttr('LStretchX', keyable = True)
    pm.addAttr(item,longName = 'RStretchY', attributeType = 'double', defaultValue = 1.0)
    item.setAttr('RStretchY', keyable = True)
    pm.addAttr(item,longName = 'RIrisShape', attributeType = 'double', defaultValue = 0.0)
    item.setAttr('RIrisShape', keyable = True)
    pm.addAttr(item,longName = 'RIrisShape', attributeType = 'double', defaultValue = 0.0)
    item.setAttr('RIrisShape', keyable = True)
    pm.addAttr(item,longName = 'RIrisAngle', attributeType = 'double', defaultValue = 0.0)
    item.setAttr('RIrisAngle', keyable = True)

for item in eye_targets:
    pm.addAttr(item,longName = 'irisShape', attributeType = 'double', defaultValue = 0.0)
    item.setAttr('irisShape', keyable = True)
    pm.addAttr(item,longName = 'irisX', attributeType = 'double', defaultValue = 1.0)
    item.setAttr('irisX', keyable = True)
    pm.addAttr(item,longName = 'irisY', attributeType = 'double', defaultValue = 1.0)
    item.setAttr('irisY', keyable = True)
    pm.addAttr(item,longName = 'irisShape', attributeType = 'double', defaultValue = 0.0)
    item.setAttr('irisShape', keyable = True)
    pm.addAttr(item,longName = 'irisX', attributeType = 'double', defaultValue = 1.0)
    item.setAttr('irisX', keyable = True)
    pm.addAttr(item,longName = 'irisY', attributeType = 'double', defaultValue = 1.0)
    item.setAttr('irisY', keyable = True)



#update constraint offsets?
#parentConstraint -e -maintainOffset GenChar_lShoulderJ  Skel_L_Shoulder_parentConstraint1;



######################
######################


#space switch


import pymel.core as pm
import rigTools
reload(rigTools.vo_controls)
import vo_usefulFunctions as uf
reload(uf)


#addAttr -ln "Parent"  -at "enum" -en "Obj1:Obj2:"  |Hammer_controls|Hammer_GRP|Hammer_OST|Hammer_CTL;

astring = 'blah_two'
print(astring.split('_')[1])

#button 1 sets constraint sources that
#button 2 feeds as params to spacify function
#button 0 adds a default parentSpace attr       ##==== NOTE THAT PARENT IS A RESERVED PYTHON WORD, BAD ATTR NAME ====##




def make_space_switch(parents, target, control, offset=0):
    enum_strings = range(len(parents)+1)
    #print len(enum_strings)
    all_parents = [parents[0].root()]+parents
    #print len(all_parents)

    pm.select(all_parents,target)
    space_constraint = pm.parentConstraint (mo = offset, weight = 0)
    space_constraint.setAttr('interpType', 2)
    #world_target = target.root()
    
    #pm.select(clear=True)
    
    for index in range(len(all_parents)):
        name_parts = ''
        #print(all_parents[index].name())
        if index == 0:
            enum_strings[index] = 'World'
        elif index > 0 and len(all_parents[index].name().split('_')) <= 2:## length of string after a split is 2 or fewer members
            #enum_strings[index] = all_parents[index].name().split('_')[-1:]
            enum_strings[index] = str(all_parents[index]).split('_')[-1:][0]
        elif index > 0 and len(all_parents[index].name().split('_')) > 2:## length of string after a split is more than 2 members
            name_parts = all_parents[index].name().split('_')[1:]
            enum_strings[index] = str(name_parts[0]) + '_' + str(name_parts[1])
        else:
            #print all_parents[index].name()
            enum_strings[index] = all_parents[index].name()
        #print enum_strings[index]
    #print enum_strings
    #print all_parents
    pm.addAttr(control, longName = 'parentSpace', attributeType = 'enum', enumName = enum_strings)
    uf.attr_lock(control, attr = 'parentSpace', lock = False)
    
    pm.select(control, replace = 1)

    #uf.multi_constrain(parents, target)
    
    for index in range(len(enum_strings)):
        constraint_weight_target = ''
        node_name = enum_strings[index]+'_space_CD'
        condition = pm.createNode('condition', name = node_name)
        
        condition.setAttr('colorIfTrueR', 1.0)
        condition.setAttr('colorIfFalseR', 0.0)
        condition.setAttr('colorIfFalseG', 0.0)
        condition.setAttr('colorIfFalseB', 0.0)
        control.parentSpace >> condition.firstTerm
        condition.setAttr('secondTerm', float(index))
        constraint_weight_target = str(space_constraint) + '.' + str(all_parents[index])+'W'+str(index)
        print(constraint_weight_target)
        condition.outColorR >> constraint_weight_target
        #pm.connectAttr(condition.colorIfTrueR, constraint_weight_target)
    pass

target_parents = pm.ls(sl=1)
target_offset = pm.ls(sl=1)[0]
control_curve = pm.ls(sl=1)[0]
make_space_switch(target_parents, target_offset, control_curve, offset = 1)

this,that = pm.ls(sl=1)[0],pm.ls(sl=1)[1]
this.parentSpace >> that.firstTerm
that.setAttr('colorIfTrueR', 1.0)
that.setAttr('colorIfFalseR', 0.0)
that.setAttr('colorIfFalseG', 0.0)
that.setAttr('colorIfFalseB', 0.0)


target_list = pm.ls(sl=1)

for target in target_list:
    
    pm.addAttr(target, longName = 'parentSpace', attributeType = 'enum', enumName = "World:COG:LHand:RHand")
    uf.attr_lock(target, attr = 'parentSpace', lock = False)
    #target.setAttr('parent', keyable = True)
    #target.setAttr(target_attr, channelBox = True, lock = False)
    #target.setAttr(target_attr, keyable = True)
#addAttr -ln "Parent"  -at "enum" -en "World:COG:LHand:RHand:"  |Muktuk|Muktuk_custom_controls|Hammer_controls|Hammer_GRP|Hammer_OST|Hammer_CTL;
#setAttr -e-keyable true |Muktuk|Muktuk_custom_controls|Hammer_controls|Hammer_GRP|Hammer_OST|Hammer_CTL.Parent;








#####################################
#####################################



#tagging stuff



import pymel.core as pm
#remove microController tag

tag_list = pm.ls(sl=1)
for target in tag_list:
    if target.hasAttr('export'):
        pass
    else:
        custom_attr = pm.addAttr(target, longName = 'export', type = 'string')
        target.setAttr('export', 'potionomicsCharacter')
        pm.
        #roots = pm.ls('*.potionomicsCharacterRoot', objectsOnly = True)


pm.select(pm.ls('*.noExport', objectsOnly = True), replace = True)

import pymel.core as pm
import vo_usefulFunctions as uf
reload(uf)

target_list = pm.ls(sl=1)

for target in target_list:
    uf.attr_lock(target, attr = 'export', lock = True)


#skinMesh
import pymel.core as pm

tag_list = pm.ls(sl=1)
for target in tag_list:
    if target.hasAttr('skinMesh'):
        print('skinMesh tag exists')
    else:
        pm.addAttr(target, longName = 'skinMesh', attributeType = 'message')

#blendMesh

import pymel.core as pm

tag_list = pm.ls(sl=1)
for target in tag_list:
    if target.hasAttr('blendMesh'):
        print('blendMesh tag exists')
    else:
        pm.addAttr(target, longName = 'blendMesh', attributeType = 'message')

