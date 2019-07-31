
"""

        META TOOLS  ===================================
        Some basic meta utilities so other scripts can identify 

"""

#def meta_find(attr = ''):
    #pm.select(pm.ls(attr, objectsOnly = True), replace = True)

import pymel.core as pm

def set_character_node(target, meshes):
    meta_tag(target, tag='pCharacter')
    meta_tag(target, tag='metaParent')
    for mesh in meshes:

        pass


#this may need to be a class
def rig_part_node(start, end):

    meta_tag(target, tag='rigPart')
    meta_tag(target, tag='metaParent')

class rigPart():
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
        @param target: Required. Object to constrain to control.
        @param name: Name for control, defaults to target if empty.
        @param parent: Transform to parent root_offset to.
        @param control_type: what tag to put on controller. Current options are controller or microController.
        """
        meta_tag(target, tag='rigPart')
        meta_tag(target, tag='metaParent')

    def 

def meta_tag(target, tag=''):

    if target.hasAttr(attr):
        tag = target.getAttr(attr)
        return tag
        #print('%s tag exists'), %(tag)
    else:
        tag = pm.addAttr(target, longName = attr, attributeType = 'message')
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

