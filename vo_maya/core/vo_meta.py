
"""
    Some basic meta utilities so other scripts can more easily navigate and track 
    the complex graphs of scenes and characters.
"""

import pymel.core as pm
import Red9.core.Red9_Meta as r9Meta
import vo_export as export

#def meta_find(attr = ''):
    #pm.select(pm.ls(attr, objectsOnly = True), replace = True)

#       ==== ATTR TYPE USAGE ====       #
"""         because i constantly forget what does what      
attrType = 'messageSimple'#attr with no value only a name, used for tagging. Returns connected object.
attrType = 'message'#red9 makes this a multiMessage attr that will return an ordered list
red9 can assume attr types from the data type being passed(int, bool, float)
JSON dicts can be passed right in, as well. written in as string attrType(red9 has json serializer)
"""


#       ==== CORE FUNCTIONS ====        #

def meta_tag(target, tag='', type = 'string'):#TODO:    deprecate this and replace its usage with r9 commands
    """
    tag target with a custom attr of given type
    @param: target = pyNodeObject
    """
    node = r9Meta.MetaClass(target.name())
    node.addAttr(tag)

#====          ZOMBIE CODE            ====#
"""    if target.hasAttr(attr):
        tag = target.getAttr(attr)
        return tag
        #print('%s tag exists'), %(tag)
    else:
        #using 'string' over 'message' type so that we can write in data when we need to
        tag = pm.addAttr(target, longName = attr, attributeType = 'string')
        return tag"""



def meta_make_child(source, *target_list):
    #TODO:      replace with r9 method
    """Make all objects in target_list the meta children of source object."""
    print source
    for target in target_list:
        if target.hasAttr('metaParent'):
            source.metaParent >> target.metaParent
        else:
            print('adding metaParent attr')
            pm.addAttr(target, longName = 'metaParent', attributeType = 'message')
            source.metaParent >> target.metaParent


#PURPOSE            Navigating parent/child relationship through .metaParent attr connections
#PRESUMPTIONS       source has metaParent attribute
def meta_traverse(source, relation, tag = ''):
    """Return metaParent or children of source.
    relation: 'parent', or "children"
    tag: return only relation with attr of given name
    """
    meta_attr = str(source) + '.metaParent'
    meta_children = []
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
                        meta_children = meta_children + [child]
                    else:
                        pass
                return meta_children
            else:
                return source_children
    else:
        pm.warning('no metaParent tag on :: ' + str(source))
#uf.meta_traverse(source, relation = 'parent', tag = '')



#PURPOSE            Navigating parent/child relationship through .metaParent attr connections
#PRESUMPTIONS       target is root transform of character hierarchy
def set_character_node(target, meshes):#FIXME   this is unused, replace with func for making rig meta node
    node = r9Meta.MetaClass(target.name())
    node.addAttr('pCharacter')
    node.addAttr('metaParent')
    for mesh in meshes:
        #TODO implement discrimination check and tagging
        #discriminate geo with blendShapes, skinClusters, and no deformation
        #no deformer == .noExport tag for deletion on export
        #skinCluster only == skinMesh tag for combine on skeletalMesh export, deletion on anim export
        #blendShape == exclusion from skinMesh combine proc and baking of animated parameters
        pass
    


#PURPOSE            finding all the bits of a genchar costume, lol
#PRESUMPTIONS       need to import 'vo_export' same way it's used for in-ine execution
#                   select network node first
class meta_navigator:
    def __init__(self):
        if pm.window('MetaNavigator', exists=True):
            pm.deleteUI('MetaNavigator', window=True)
        pm.window('MetaNavigator', sizeable=1 )
        pm.rowColumnLayout( numberOfColumns=3 )
        self.character_targets = export.r9Meta.getMetaNodes()
        self.char_names = []
        for target in self.character_targets:
            target_name = "{}{}".format(target.personality,target.jobClass)
            self.char_names.append(target_name)
            pm.button(bgc = (0.2,0.1,0.5), label = "    {}    ".format(target_name), command = "pm.select('{}')".format(target_name) )
            pm.button(bgc = (0.2,0.6,0.2),label = '    meshes    ', command = 'pm.select(export.character_asset(node = pm.ls(sl=1)[0]).node.meshes)' )
            pm.button(bgc = (0.4,0.2,0.5),label = '    skel    ', command = 'pm.select(export.character_asset(node = pm.ls(sl=1)[0]).node.skeleton)')
        
        pm.setParent( '..' )
        pm.showWindow('MetaNavigator')
    def get_meshes(self,target_name):#CBB   superfluous
        target = r9Meta.MetaClass(target_name)
        pm.select(target.meshes)
        print(target)
    def get_skel(self,target):#CBB   superfluous
        #target = r9Meta.MetaClass(target_name)
        pm.select(target.skeleton)
        print(target)



#this def needs to be a class, sinc there are many types of rig parts with different 
# kinds of data and components.

#PURPOSE            network node to assist other scripts in finding rig components
#PRESUMPTIONS       corresponding character part and rig components already exist
class RigPart():#TODO   identify difference between RigPart and CharacterPart
    """
    class to make network nodes that help find rig sub components
    these should always connected to one of: character part or prop
    """
    def __init__(
                self,
                character_part,

                start,
                end,
                name = ''
                ):
        """
        @param :
        """
        
        meta_tag(target, tag='rigPart')
        meta_tag(target, tag='metaParent')

#PURPOSE            network node to assist other scripts in finding character parts
#PRESUMPTIONS       corresponding character root is already tagged for
class CharacterPart():
    """
    class to make network nodes that help find rig sub components
    these should always connected to one of: character part or prop
    """
    def __init__(
                self,
                character_node,
                meta_type,
                name = '',

                ):
        """
        @param character_node: the character that this part belongs to
        """
        
        #not sure how to handle this and sub-classing yet
        meta_tag(target, tag='pCharPart')
        meta_tag(target, tag='metaParent')


class characterProp(CharacterPart):
    def __init__(self, character_node, name):
        pass



"""
Joint Rename
"""



#if string[-2] == 'J':
#    new_string = string.replace(string['J','_0'])
#elif string[-1] === 'J':
#    new_string = string.replace(string['J','_0'])



"""
Saffron metaRig test setup


import Red9.core.Red9_Meta as core.r9Meta
import maya.cmds as cmds

#make a new blank mClass MayaNode
character_name = pm.ls('*.potionomicsCharacterRoot', objectsOnly = True)[0].name()
root = core.r9Meta.MetaClass(character_name)
root.delAttr('potionomicsCharacterRoot')


mRig=core.r9Meta.MetaRig(name='SaffronRig')
mRig.rigType = 'character'
#mRig.rename('Rig')
mRig.mNodeID = 'mSystem'#mNodeID is put what gets slapped onto the next objects' attrs

node = core.r9Meta.MetaClass('Saffron_MainHipC')
node.addAttr(attr = 'metaParent', attrType = 'message' )

spine_name = character_name.join('Spine')
spine= mRig.addMetaSubSystem('Spine', 'Centre', nodeName='SpineSystem', attr='SpineSystem')
spine.addAttr('controls', attrType = 'messageSimple')
#spine.addRigCtrl()
spine.addRigCtrl('Saffron_MainHipC','Hips', mirrorData={'side':'Centre','slot':3})  
#print(spine)

#mRig.delAttr('Facial')
facial=mRig.addChildMetaNode('MetaFacialRig',attr='Facial',nodeName='FACIAL') #NEW generic method in BaseClass
#addChildMetaNode seems to be more generic system

pyObject = pm.ls(sl=1)[0]
print(pyObject.name())

"""

