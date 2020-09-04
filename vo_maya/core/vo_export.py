"""
    functions for character export
    TODO    add proc for exporting animated props
    TODO    replace cmds.file usage with whatever the pymel equivalent is

"""

import pymel.core as pm
import maya.cmds as cmds
import vo_deformers as deformers
import vo_general as general
import sys, inspect, os, platform


def publish_rig(rig):
    """"Update rig binary file in rigs folder
    """
    # step 0:   save rig binary
    # step 1:   delete animation
    # step 2:   zero rig
    # step 3:   check children of root nodes for tags
    # step 4:   check for metaRig
    # step 5:   update json
    # step 6:   export SKL
    return


#
def get_export_path(character_name):#TODO:    character_name conflicts with local variable
    """
        Get 
    """
    #TODO:  store these values into the .export attr
    output_path = None
    character_paths = {
        'Anubia' : '/scenes/Animation/Anubia/export/',
        'Baptiste' : '/scenes/Animation/Baptist/export/',
        'BossFinn' : '/scenes/Animation/BossFinn/export',
        'Corsac' : '/scenes/Animation/Corsac/export/',
        'GenChar' : '/scenes/Animation/GenChar/export/',
        'Luna' : '/scenes/Animation/Luna/export/',
        'Maven' : '/scenes/Animation/Maven1/export/',
        'Mint' : '/scenes/Animation/Mint/export/',
        'Muktuk' : '/scenes/Animation/MukTuk/export/',
        'Owl' : '/scenes/Animation/Owl/Export/',#no RRARigConnection attr
        'Pepper' : '/scenes/Animation/SaltPepper/export/',
        'Quinn' : '/scenes/Animation/Quinn/Export/',
        'Robin' : '/scenes/Animation/Robin/export/',
        'Roxanne' : '/scenes/Animation/Roxanne/Export/',
        'Saffron' : '/scenes/Animation/Saffron/export/',
        'Salt' : '/scenes/Animation/SaltPepper/export/',
        'SoulWitch' : '/scenes/Animation/SoulWitch/export/',
        'sylv_ROOT' : '/scenes/Animation/Sylvia/export/',#no RRARigConnection attr
        'Xidriel' : '/scenes/Animation/Xidriel/export/'
    }
    if character_paths[character_name] == None:
        pm.warning('no path set for %s ' % character_name)
    else:
        #initial_path = pm.workspace.getcwd()
        path = ['','']
        path[0] = pm.sceneName().split('/scenes')[0]
        path[1] = pm.sceneName().split('/')[-1].replace('.ma','.fbx')
        if character_name in character_paths:
            output_path = character_paths[character_name].join(path)
        else:
            pm.warning('%s not found in path dict' % character_name)
        
        return output_path
#print(get_export_path())


#PURPOSE            check if there is a fresh fbx export of the current file
#PROCEDURE          
#PRESUMPTION        pathA is current scene, pathB is fbx scene
def need_export(pathA, pathB):
    """
        return True if pathA indicates a newer file
        pathA is current scene, pathB is fbx scene
    """
    #files = pm.getFileList(path, filespec = '*.fbx')
    #scene_path = cmds.file(query=True, l=True)[0]
    
    if os.path.exists(pathA) and not os.path.exists(pathB):
        return True
    elif os.path.isfile(pathA) and os.path.isfile(pathB):
        if os.path.getmtime(pathA) > os.path.getmtime(pathB):
            print(pathA)
            return True
        else:
            return False
    else:
        pm.error('invalid pathA provided')#pathA must exist


#PURPOSE            get reference of a maya object
#PROCEDURE          if object is referenced, return reference node
#PRESUMPTION        target is a dag object
def get_reference(target):
    if pm.referenceQuery(target, isNodeReferenced = True):
        name = pm.referenceQuery(target, referenceNode = True)
        reference = pm.FileReference(refnode = name)
        return reference
    else:
        pm.warning('target is not referenced')
        return None
   

#PURPOSE            import all references recursively
#PROCEDURE          loop over list of all references in scene and import if it's loaded, remove if it isn't loaded
#PRESUMPTION        user is trying to import full depth of all references
def import_references():
    """
        import all referenced scenes
        returns True if scenes were imported, False if no references
    """
    for ref in pm.listReferences(recursive = True):
        try:
            if ref.isLoaded():
                ref.importContents(removeNamespace = True)
            else:
                ref.remove(force = True)
        except:
            print ("Skipped import of unloaded refs")
    return# True


#PURPOSE            to obliterate extraneous Owl references that litter Sylvia's files
#PROCEDURE          loop over list of all references in scene and unload anything that matches target file
#PRESUMPTION        
def remove_target_reference(filepath, reference):
    """
    """
    if reference == filepath:
        try:
            reference.remove(force = True)
            return True
        except:
            print("removal failed")
    else:
        return False

def obliterate_references(filepath = None):
    """
    """
    for reference in pm.listReferences(recursive = True):
        if filepath:
            try:
                remove_target_reference(filepath, reference)
            except:
                pm.warning('attempted and failed to execute remove_target_reference() on %s' %(reference))
        else:
            try:
                if reference.isLoaded():
                    pass
                else:
                    reference.remove(force = True)
            except:
                pm.warning('strange result with %s' %(reference))
    return# True


#if scene uses namespace, return True and the namespace
#otherwise return false and the prefix
#refs = pm.listReferences()
def eval_namespace(reference):
    """
    @param reference: pymel object 
    """
    namespace = None
    prefix = None
    if reference.isUsingNamespaces():
        namespace = reference.namespace+':'
        return True, namespace
    else:
        prefix = reference.namespace+'_'
        return False, prefix


#TODO:      integrate this into import function so we don't have to do this manually
#TODO:  reevaluate whether this is still necessary
def remove_object_namespace(object):
    target_namespace = object.namespace()
    print 'removing namespace :: ' + target_namespace
    pm.namespace(removeNamespace = target_namespace, mergeNamespaceWithRoot = True)


#PROCEDURE          get 
#PRESUMPTIONS       only one prefix
def remove_scene_prefix(prefix, namespace = None):
    scene = pm.ls()

    for item in scene:
        itemString = item.shortName()
        #print(itemString)
        if itemString.startswith(prefix):
            #breaks off first string 
            itemName = itemString.split("_", 1)[1]
            #print (itemName)
            pm.rename(item, itemName)
        else:
            pass
            #print "no prefix"



def set_timeline():
    playStartTime = pm.playbackOptions(query = True, minTime = True)
    playEndTime = pm.playbackOptions(query = True, maxTime = True)
    playStartTime = int(playStartTime)
    playEndTime = int(playEndTime)
    return playStartTime, playEndTime


def bake_animation(targets, sampling = 1):#changed to list input
    #pm.select(bakeTarget)
    #set timeline
    playStartTime = int(pm.playbackOptions(query = True, minTime = True))
    playEndTime = int(pm.playbackOptions(query = True, maxTime = True))
    #Bake Animation
    #for target in targets:
    pm.bakeResults(targets, simulation = 1, sampleBy = sampling, pok = 1, sac = 0, time = (playStartTime, playEndTime))


#def fileExport(arg):
#    pm.select(arg)
#    cmds.file(outputFile, exportSelected=True, type="FBX export")

    


####====                    ========                    ====####
#
#                       ACTION ZONE!!!!
#
####====                    ========                    ====####

def export_skeletal_mesh(rig):
    """
    @param rig:  rig is mClass MetaRig object or network node
    """
    
    if rig.type == 'mClass':
        return
    elif rig.type == 'network':
        return
    else:
        pm.warning('reference is neither mClass or network node')


    #delete rig controls and setup structure

    #get skin meshes

    #combine skinned meshes
    #skinned_mesh = combine_skinMeshes(rig.skinMeshes)
    #reparent skinned_mesh


def export_animation(root, path):
    #TODO:  make this function handle namespace and prefix shit
    """
    @param root: root node of character to export
    """
    
    bake_animation(pm.ls('*.jointSkin', objectsOnly = True))
    pm.delete(pm.ls('*.noExport', objectsOnly = True))
    #pm.select(pm.ls('*.export', objectsOnly = True, recursive = True), replace = True)#TODO:  this should select root
    pm.select(root, replace = True)
    pm.exportSelected(path, force=True, type="FBX export")
    #cmds.file(path, exportSelected=True, type="FBX export", force = True)


#pm.delete(pm.ls('*.skinMesh', objectsOnly = True))
#pm.delete(pm.ls('*.blendMesh', objectsOnly = True))


#export prop, hat, broom, wand
def export_prop(param):
    """
    @param auto: Boolean to automatically export from current scene. False will provide prompts for filepath and output name.
    """
    if param == 'auto':
        import_references()
        print('refs imported')
        export_path = get_export_path()
        print(export_path)
        #muffins = pm.ls('*.jointSkin', objectsOnly = True)
        muffins = pm.ls('*.jointSkin', objectsOnly = True)
        bake_animation(muffins)
        pm.delete(pm.ls('*.noExport', objectsOnly = True))
        print('deleted crap')
        pm.select(pm.ls('*.export', objectsOnly = True, recursive = True), replace = True)
        cmds.file(export_path, exportSelected=True, type="FBX export")
        return
    elif param == 'skel':
        import_references()
        print('refs imported')
        export_path = get_export_path()
        print(export_path)
        muffins = pm.ls('*.jointSkin', objectsOnly = True)
        bake_animation(muffins)
        pm.delete(pm.ls('*.noExport', objectsOnly = True))
        print('deleted crap')
        pm.select(pm.ls('*.export', objectsOnly = True, recursive = True), replace = True)
        cmds.file(export_path, exportSelected=True, type="FBX export")
        return
    else:

        return



def potionomics_export():
    #
    #TODO:  mke dict for rigs and iterate over the keys?
    characters = []
    rigs = pm.ls('*.export', objectsOnly = True, recursive = True)
    for root in rigs:
        #print(root.name())
        #print(root)
        ref = get_reference(root)
        ns_data = eval_namespace(ref)
        name = root.name().split(ns_data[1])[1]
        path = get_export_path(name)

        if need_export(pm.sceneName(), path):
            
            character_data = {
                'name' : name,
                'root' : root,
                'path' : path,
                'namespace_data' : ns_data
            }
            
            characters.append(character_data)
            #print(character_data)
        else:
            print('scene file is older than export')
    #refs = pm.listReferences()
    import_references()
    print(characters)
    for this_dict in characters:
        if this_dict['namespace_data'][0]:
            try:
                target_namespace = this_dict['namespace_data'][1]
                pm.namespace(removeNamespace = target_namespace, mergeNamespaceWithRoot = True)
                #remove_object_namespace(key)
            except:
                pass
        else:
            remove_scene_prefix(this_dict['namespace_data'][1])
            export_animation(this_dict['root'], this_dict['path'])#
    return



def character_prep1(overwrite = False):
    #
    characters = []
    rigs = pm.ls('*.export', objectsOnly = True, recursive = True)
    for root in rigs:
        #print(root.name())
        #print(root)
        ref = get_reference(root)
        ns_data = eval_namespace(ref)
        name = root.name().split(ns_data[1])[1]
        path = get_export_path(name)

        if overwrite or need_export(pm.sceneName(), path):
            character_data = {
                'name' : name,
                'root' : root,
                'path' : path,
                'namespace_data' : ns_data
            }
            characters.append(character_data)
            #print(character_data)
        else:
            print('scene file is older than export')
    return characters

def export_animation1(root, path):
    #TODO:  make this function handle namespace and prefix shit
    """
    @param root: root node of character to export
    """
    
    bake_animation(pm.ls('*.jointSkin', objectsOnly = True))
    pm.delete(pm.ls('*.noExport', objectsOnly = True, recursive = True))
    #pm.select(pm.ls('*.export', objectsOnly = True, recursive = True), replace = True)#TODO:  this should select root
    pm.select(root, replace = True)
    #pm.exportSelected(path, force=True, type="FBX export")
    cmds.file(path, exportSelected=True, type="FBX export", force = True)

def export_skeleton(characters):
    print(characters)
    for this_dict in characters:
        if this_dict['namespace_data'][0]:
            try:
                target_namespace = this_dict['namespace_data'][1]
                pm.namespace(removeNamespace = target_namespace, mergeNamespaceWithRoot = True)
                #voe.export_animation(this_dict['root'], this_dict['path'])#
            except:
                pass
        else:
            remove_scene_prefix(this_dict['namespace_data'][1])
        #TODO:  combine skinMeshes using function in vo_deformers
        pm.delete(pm.ls('*.noExport', objectsOnly = True, recursive = True))
        pm.select(this_dict['root'], replace = True)
        pm.exportSelected(this_dict['path'], force=True, type="FBX export")
    return True
    #else:
    #    return False

def potionomics_export1(characters):
    print(characters)
    for this_dict in characters:
        if this_dict['namespace_data'][0]:
            try:
                target_namespace = this_dict['namespace_data'][1]
                pm.namespace(removeNamespace = target_namespace, mergeNamespaceWithRoot = True)
                #voe.export_animation(this_dict['root'], this_dict['path'])#
            except:
                pass
        else:
            remove_scene_prefix(this_dict['namespace_data'][1])
        try:
            bake_animation(pm.ls('*.jointSkin', objectsOnly = True, recursive = True))
            #export_animation1(this_dict['root'], this_dict['path'])#
        except:
            pm.warning('export failed')
        pm.delete(pm.ls('*.noExport', objectsOnly = True, recursive = True))
        pm.select(this_dict['root'], replace = True)
        pm.exportSelected(this_dict['path'], force=True, type="FBX export")
    return True
    #else:
    #    return False

"""


import vo_maya.core.vo_export as voe
reload(voe)

characters = voe.character_prep1(overwrite = True)
if len(characters) > 0:
    voe.import_references()
    voe.potionomics_export1(characters)
else:
    print('nothing ot export')

"""


#characters = character_prep()

#potionomics_export(characters)






