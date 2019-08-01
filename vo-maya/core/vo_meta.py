
"""
    Some basic meta utilities so other scripts can more easily navigate and track 
    the complex graphs of scenes and characters.
"""

import pymel.core as pm

#def meta_find(attr = ''):
    #pm.select(pm.ls(attr, objectsOnly = True), replace = True)


#       ==== CORE FUNCTIONS ====        #

def meta_tag(target, tag=''):

    if target.hasAttr(attr):
        tag = target.getAttr(attr)
        return tag
        #print('%s tag exists'), %(tag)
    else:
        #using 'string' over 'message' type so that we can write in data when we need to
        tag = pm.addAttr(target, longName = attr, attributeType = 'string')
        return tag


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
def set_character_node(target, meshes):
    meta_tag(target, tag='pCharacter')
    meta_tag(target, tag='metaParent')
    for mesh in meshes:
        #TODO implement discrimination check and tagging
        #discriminate geo with blendShapes, skinClusters, and no deformation
        #no deformer == .noExport tag for deletion on export
        #skinCluster only == skinMesh tag for combine on skeletalMesh export, deletion on anim export
        #blendShape == exclusion from skinMesh combine proc and baking of animated parameters
        pass
    



class MetaNode():
    """
    class to make network nodes that help find rig and character stuff
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
        
        meta_tag(target, tag='metaParent')



#this def needs to be a class, sinc there are many types of rig parts with different 
# kinds of data and components.

#PURPOSE            network node to assist other scripts in finding rig components
#PRESUMPTIONS       corresponding character part and rig components already exist
class RigPart():#TODO   make this subclass of a generic metaNode type
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
# TODO    subclass for character props
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


class characterProp(characterPart):
    def __init__(self, character_node, name):
        pass
