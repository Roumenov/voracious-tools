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
def get_export_path(path = None, character_name = ''):#TODO:    character_name conflicts with local variable
    """
        Get 
    """
    #TODO:  create dict of character name/path ? or just pull name from stored value on root?
    name_path = {
        'Anubia' : 
        'BossFinn' : 
        'Corsac' : 
        'GenChar' : 
        'Luna' : 
        'Maven' : 
        'Mint' : 'Animation\Mint/export'
        'MukTuk' : 
        'Owl' : 
        'Pepper' : 
        'Quinn' : 
        'Robin' : 
        'Saffron' : 
        'Salt' : 
        'Sylvia' : 
        'Xid' : 
    }

    if path:
        initial_path = path
    else:
        initial_path = cmds.file(query=True, l=True)[0].replace('.ma','.fbx')
    
    if '/latest' in initial_path:
        current_path = initial_path.split('/latest')[0]
        file_name = initial_path.split('/latest')[1]
        output_path = current_path + '/export' + file_name
    else:
        file_name = initial_path.split('/')[-1]
        character_name = initial_path.split('/')[-2]
        output_path = initial_path.replace(character_name,character_name +'/export')
    return output_path
#print(get_export_path())


#https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


#PURPOSE            check if there is a fresh fbx export of the current file
#PROCEDURE          
#PRESUMPTION        pathA is current scene, pathB is fbx scene
def need_export(pathA, pathB):
    #files = pm.getFileList(path, filespec = '*.fbx')
    #scene_path = cmds.file(query=True, l=True)[0]
    
    scene_time = os.path.getmtime(pathA)
    fbx_path = get_export_path()

    fbx_time = creation_date(fbx_path)
    
    if os.path.isfile(pathA) and os.path.isfile(pathB):
        if scene_time > fbx_time:
            return True
        else:
            return False
    else:
        return True# no file is the same as not having exported
    


def check_export_date():
    
    if os.path.isfile(fbx_path):#if 
        pass
    else:
        pass


#PURPOSE            get reference of a maya object
#PROCEDURE          if object is referenced, return reference node
#PRESUMPTION        ???     target is a dag object      ???
def get_reference(target):#TODO:    test in maya
    if cmds.referenceQuery(target, isNodeReferenced = True):
        reference = cmds.referenceQuery(target, referenceNode = True)
    else:
        pm.warning('target is not referenced')
    return reference

#PURPOSE            import all referenced scenes
#PROCEDURE          loop over list of all references in scene and import if it's loaded
#PRESUMPTION        references are only one reference deep, and right now we really only have one
def import_references():
    done = False
    print ("looking for references ....")
    refs = pm.listReferences()
    totalRefs = len(refs)
    if len(refs) == 0:
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



#TODO:      integrate this into import function so we don't have to do this manually
def remove_object_namespace(object):
    target_namespace = object.namespace()
    print 'removing namespace :: ' + target_namespace
    pm.namespace(removeNamespace = target_namespace, mergeNamespaceWithRoot = True)


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
    
    

#TODO:  make this look only within a given namespace
#TODO:  use general.strip_prefix() or integrate the string class?
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
    """
    @param root: root node of character to export
    """
    if root:
        
        muffins = pm.ls('*.jointSkin', objectsOnly = True)
        bake_animation(muffins)
        pm.delete(pm.ls('*.noExport', objectsOnly = True))
        pm.select(pm.ls('*.export', objectsOnly = True), replace = True)
        cmds.file(export_path, exportSelected=True, type="FBX export")
    else:
        pm.warning('no rig selected')

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
    #get references
    rigs = pm.ls('*.export', objectsOnly = True)
    for item in rigs:
        get_reference(item)
    #refs = pm.listReferences()
    import_references()
    export_path = get_export_path()
    pass








