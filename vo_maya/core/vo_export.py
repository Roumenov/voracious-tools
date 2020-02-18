"""
    functions for character export
    TODO    add proc for exporting animated props
    TODO    replace cmds.file usage with whatever the pymel equivalent is

"""

import pymel.core as pm
import maya.cmds as cmds
import vo_deformers, vo_general as deformers, general
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
    character_paths = {
        'Anubia' : None,
        'Baptiste' : 'scenes/Animation/Baptist/export',
        'BossFinn' : None,
        'Corsac' : 'scenes/Animation/Corsac/export',
        'GenChar' : 'scenes/Animation/GenChar/export',
        'Luna' : 'scenes/Animation/Luna/export',
        'Maven' : 'scenes/Animation/Maven1/export',
        'Mint' : 'scenes/Animation/Mint/export',
        'Muktuk' : 'scenes/Animation/MukTuk/export',
        'Owl' : 'scenes/Animation/Owl/Export',#no RRARigConnection attr
        'Pepper' : None,
        'Quinn' : 'scenes/Animation/Quinn/Export',
        'Robin' : 'scenes/Animation/Robin/export',
        'Roxanne' : 'scenes/Animation/Roxanne/Export',
        'Saffron' : 'scenes/Animation/Saffron/export',
        'Salt' : None,
        'SoulWitch' : 'scenes/Animation/SoulWitch/export',
        'sylv_ROOT' : 'scenes/Animation/Sylvia/export',#no RRARigConnection attr
        'Xidriel' : 'scenes/Animation/Xidriel/export'
    }
    
    #initial_path = pm.workspace.getcwd()
    path = ['','']
    path[0] = pm.sceneName().split('/scenes')[0]
    path[1] = pm.sceneName().split('/')[-1].replace('.ma','.fbx')
    output_path = character_paths[character_name].join(path)

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
        return False

    elif os.path.isfile(pathA) and os.path.isfile(pathB):
        if os.path.getmtime(pathA) > os.path.getmtime(pathB):
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
        reference = pm.referenceQuery(target, referenceNode = True)
    else:
        pm.warning('target is not referenced')
    return reference

#PURPOSE            
#PROCEDURE          loop over list of all references in scene and import if it's loaded
#PRESUMPTION        references are only one reference deep, and right now we really only have one(?)
def import_references():
    """
        import all referenced scenes
        returns True if scenes were imported, False if no references
    """

    done = False
    print ("looking for references ....")
    refs = pm.listReferences()
    totalRefs = len(refs)
    if len(refs) == 0:#TODO:    this shit is a mess
        print "no references to import"
        return False
    else:
        while (done == False and (len(refs) != 0)): #----   why not just do everything in the for loop?
            refs = pm.listReferences()
            print ("importing ", len(refs), " references....")
            for ref in refs:
                if ref.isLoaded():
                    done = False
                    print ("remaining refs = ")
                    ref.importContents(removeNamespace = True) #---- remove namespace doesn't seem to work
                else:
                    print ("All references imported")
                    done = True
        print ("Imported " + str(totalRefs) + " references")
        return True


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
        namespace = reference.namespace
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
        print (itemString)
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
    #pm.select(pm.ls('*.export', objectsOnly = True), replace = True)#TODO:  this should select root
    pm.select(root, replace = True)
    cmds.file(path, exportSelected=True, type="FBX export")


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
        pm.select(pm.ls('*.export', objectsOnly = True), replace = True)
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
        pm.select(pm.ls('*.export', objectsOnly = True), replace = True)
        cmds.file(export_path, exportSelected=True, type="FBX export")
        return
    else:

        return



def potionomics_export(param):
    #
    #TODO:  mke dict for rigs and iterate over the keys?
    characters = []
    rigs = pm.ls('*.export', objectsOnly = True)
    for root in rigs:
        if need_export(pm.sceneName(), get_export_path(root.name())):
            ref = get_reference(root)
            
            character_data = {
                'name' : root.name(),
                'root' : root,
                'path' : get_export_path(root.name()),
                'namespace_data' : eval_namespace(ref)
            }
            
            characters.append(character_data)
    #refs = pm.listReferences()
    import_references()

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








