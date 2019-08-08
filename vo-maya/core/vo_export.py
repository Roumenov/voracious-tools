"""
    functions for character export
    TODO    add proc for exporting animated props
    TODO    replace cmds.file usage with whatever the pymel equivalent is

"""

import pymel.core as pm
import maya.cmds as cmds
import sys
import inspect



#PURPOSE            check if given joint is skinned
#PROCEDURE            cycle through connections and find skinCluster nodes
#PRESUMPTIONS        arg is a single object of type joint
#TODO       looks like something that belongs in rigging.vo_deformers
def check_skincluster(jointObject):
    for node in jointObject.connections():
        if node.nodeType() == 'skinCluster':
            return True
        else:
            return False




#declaring initial variables
#global playStartTime
#global playEndTime
#TODO     this really seems like it should be a more generic function in vo_general with a standard set of paths
def get_export_path():
    #global outputFile
    initial_path = cmds.file(query=True, l=True)[0].replace('.ma','.fbx')
    print "current file:"
    print initial_path
    if '/latest' in initial_path:
        print "Sylvia"
        current_path = output_path.split('/latest')[0]
        file_name = output_path.split('/latest')[1]
        output_path = testFileA + '/export' + file_name
        print output_path
    else:
        file_name = initial_path.split('/')[-1]
        character_name = initial_path.split('/')[-2]
        output_path = initial_path.replace(character_name,character_name +'/export')
    return output_path
#print(get_export_path())


#PURPOSE            import all referenced scenes
#PROCEDURE          list pymel references, looop 
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



def set_timeline():
    playStartTime = pm.playbackOptions(query = True, minTime = True)
    playEndTime = pm.playbackOptions(query = True, maxTime = True)
    playStartTime = int(playStartTime)
    playEndTime = int(playEndTime)
    return playStartTime, playEndTime



# Should change this later to take the prefix as an argument.
#PRESUMPTIONS       prefix takes the form of a single character followed by '_' x_ Any other order will break shit.
#PRESUMPTIONS       prefix will be one character followed by an underscore and nothing has happened to the name since import
def remove_prefix(prefix):
    print "removing prefix :"
    print prefix

    sceneList = pm.ls()

    for item in sceneList:
        itemString = item.shortName()
        print (itemString)
        if itemString.startswith(prefix):
            print "removing prefix"
            itemName = itemString.split("_", 1)[1]
            print (itemName)
            pm.rename(item, itemName)
        else:
            print "no prefix"


def bake_animation(bakeList):#changed to list input
    #pm.select(bakeTarget)
    #set timeline
    playStartTime = int(pm.playbackOptions(query = True, minTime = True))
    playEndTime = int(pm.playbackOptions(query = True, maxTime = True))
    #Bake Animation
    #for target in bakeList:
    pm.bakeResults(bakeList, simulation = 1, sampleBy = 1, pok = 1, sac = 0, time = (playStartTime, playEndTime))


#def fileExport(arg):
#    pm.select(arg)
#    cmds.file(outputFile, exportSelected=True, type="FBX export")

    


####====                    ========                    ====####
#
#                       ACTION ZONE!!!!
#
####====                    ========                    ====####

def export_skeletal_mesh(target):
    """
    @param target:  target is mClass MetaRig
    """
    #skinned_mesh = combine_skinMeshes(target.skinMeshes)
    #reparent skinned_mesh


def export_character(param):
    """
    @param auto: Boolean to automatically export from current scene. False will provide prompts for filepath and output name.
    """
    if param == 'auto':
        import_references()
        export_path = get_export_path()
        muffins = pm.ls('*.jointSkin', objectsOnly = True)
        bake_animation(muffins)
        pm.delete(pm.ls('*.noExport', objectsOnly = True))
        pm.select(pm.ls('*.export', objectsOnly = True), replace = True)
        cmds.file(export_path, exportSelected=True, type="FBX export")
    elif param == 'nonsense':
    #if len(pm.ls(sl=1)):
        #root = tag_root(tag = True, target = pm.ls(selection = True)[0])
        import_references()
        print('refs imported')
        export_path = get_export_path()
        #set_timeline()
        #pm.select("bakeSet", replace = True)
        muffins = pm.ls('*.jointSkin', objectsOnly = True)
        bake_animation(muffins)
        pm.delete(pm.ls('*.noExport', objectsOnly = True))
        print('deleted crap')
        pm.select(pm.ls('*.export', objectsOnly = True), replace = True)
        cmds.file(export_path, exportSelected=True, type="FBX export")
        #try mixing this up
    elif param == 'manual':
        pass
    else:
        pm.warning('no rig selected')

#export_character('auto')


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
        muffins = pm.ls('*.jointSkin', objectsOnly = True)
        bake_animation(muffins)
        pm.delete(pm.ls('*.noExport', objectsOnly = True))
        print('deleted crap')
        pm.select(pm.ls('*.export', objectsOnly = True), replace = True)
        cmds.file(export_path, exportSelected=True, type="FBX export")



def potionomics_export(param):
    #
    pass








