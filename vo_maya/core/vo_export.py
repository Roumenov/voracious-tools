"""
    functions for character export
    TODO    add proc for exporting animated props
    TODO    replace cmds.file usage with whatever the pymel equivalent is

"""

import pymel.core as pm
import maya.cmds as cmds
import vo_deformers as deformers
import vo_general as general
import vo_controls as controls
import Red9.core.Red9_Meta as r9Meta
import sys, inspect, os, platform


def publish_rig():
    """"Update rig binary file in rigs folder
    """
    #this is basically how we find rigs in lieu of a more sophisticated data structure
    #TODO:  why do we use both export and rig ?
    root = pm.ls('*.export', objectsOnly = True, recursive = True)[0]
    #sometimes keys are left on during testing/skinning
    [pm.cutKey(control) for control in pm.ls('*.controller', objectsOnly = True, recursive = True)]
    #references slow down file loading, so we bring everything in for this binary
    import_references()
    #check all the deformation objects for garbage or wip structures
    joints = pm.ls('*.jointSkin', objectsOnly = True, recursive = True)
    if len(joints) > 0:
        [pm.delete(item) for item in joints if item.hasAttr('noExport')]
    #we want to remove scene objects that aren't considered rigs, like cameras
    cameras = [shape.root() for shape in pm.ls(ca = 1, dag = 1)]
    assemblies = pm.ls(set(pm.ls(assemblies = 1, o = 1, r = 0, rn = 0)) - set(pm.ls(assemblies = 1, o = 1, r = 0, rn = 1)) - set(cameras) - set(pm.ls('*.rig', o = 1)))
    [pm.delete(object) for object in assemblies]
    #minimal mesh objects
    meshes = pm.ls('*.skinMesh', objectsOnly = True, recursive = True)
    if len(meshes) > 0:
        [pm.delete(item) for item in meshes if not item.listHistory(type = 'skinCluster')]
        skinned_meshes = [item for item in pm.ls('*.skinMesh', objectsOnly = True, recursive = True) if item.listHistory(type = 'skinCluster')]
        skinned_mesh = pm.PyNode(pm.polyUniteSkinned(skinned_meshes, ch = 0, muv = 1)[0])
        skinned_mesh.rename('skinned_mesh')
        skinned_mesh.addAttr('skinMesh', attributeType = 'message')
        root | skinned_mesh
    else:
        pass
    #TODO   handle blend meshes
    #       in most files we want to rename, but for sylv we skip
    #CBB    delete unused layers?
    #       write path into export attr?
    #CBB    create proc to get proper filename automatically
    #       requires fixing a bunch of file name inconsistentcies and refs
    pm.select(pm.ls('*.rig', objectsOnly = True),replace = True)
    pm.exportSelected(pm.fileDialog2(), type = 'mayaBinary')

    return


def generate_scene_list(raw, path= None, name = None):
    output = str([path+item+'.ma' for item in raw.split('\n')])
    return output
#generate_scene_list(raw, path = voe.get_export_path('Roxanne').split('Export')[0])

#PURPOSE        get the export path of a character by name
#PRESUMPTION    paths don't change, any character that needs export will be in this dict
def get_export_path(character_name):#TODO:    character_name conflicts with local variable
    """
        Return correct filepath for given character name and extension
    """
    #TODO:  store these values into the .export attr
    output_path = None
    character_paths = {#dict matching rig root name to filepath
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
    else:#CBB this doesn't work for rigs, would need new func to discriminate better
        #initial_path = pm.workspace.getcwd()
        #file_namer()
        path = ['','']
        path[0] = pm.sceneName().split('/scenes')[0]
        path[1] = pm.sceneName().split('/')[-1].replace('.ma','.fbx')
        if character_name in character_paths:
            output_path = character_paths[character_name].join(path)
        else:
            pm.warning('%s not found in path dict' % character_name)
        
        return output_path
#print(get_export_path())


#PURPOSE     get a final, correctly named version of target character
#CBB expanding the file name operation from get_export_path
def file_namer(name, extension):
    #name
    #short name
    #_SKL
    #_rig
    path[1] = pm.sceneName().split('/')[-1].replace('.ma','.fbx')
    if character_name in character_paths:
        output_path = character_paths[character_name].join(path)
    else:
        pm.warning('%s not found in path dict' % character_name)
    return


#PURPOSE            check if there is a fresh fbx export of the current file
#PROCEDURE          
#PRESUMPTION        pathA is current scene, pathB is fbx scene
def need_export(pathA, pathB):
    """
        return True if pathA indicates a newer file or pathB doesn't exist yet
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


#PURPOSE            replace existing reference to target file with another file
#PROCEDURE          compare absolute filepaths of references, then replace if they don't match
#PRESUMPTION        
def replace_target_reference(reference, filepath):
    """
    @param filename:    string of filename to search for
    @param filepath:    string of replacement path

    returns number of refs replaced
    """
    if reference.path.abspath() == os.path.abspath(filepath):
        pm.warning('reference and filepath appear to be identical')
    else:
        reference.replaceWith(filepath)
        print('replaced %s with %s' %(reference,filepath))
    """
    try:
        reference.replaceWith(filepath)
        output += 1
    except:
        pm.warning('attempted and failed to replace %s with %s' %(reference,filepath))
    """

#replace_target_reference(filename = 'Roxanne_Rig.ma', filepath = '//scenes/Rigs/roxanne_rig.mb')


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


#if reference uses namespace, return True and the namespace
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





class namespace_machine():
    def __init__(self):
        namespace = str
        filepath = str
        debug = False


#TODO:      integrate this into import function so we don't have to do this manually
#TODO:      reevaluate whether this is still necessary, seems like you could just do object._setNamespace('root') or smth
#PURPOSE:       removing namespaces from imported references
#PRESUMPTION:   imported refs will keep namespaces
def remove_object_namespace(object):
    target_namespace = object.namespace()
    print ('removing namespace :: ' + target_namespace)
    pm.namespace(removeNamespace = target_namespace, mergeNamespaceWithRoot = True)


#PURPOSE        this basically exists so that namespaces won't get changed recursively the way references do
def replace_target_namespace(namespace, string):
    for reference in pm.listReferences(recursive = False):
        if reference._getNamespace() == namespace:
            reference._setNamespace(string)
    return
#replace_target_namespace('mesh', 'rig')


def claim_namespace(filepath, namespace, debug = False):
    """
    claim_namespace(filepath = "Z:/0_p4v/PotionomicsSourceAssets/Art_sourcefiles/Characters/scenes/Rigs/ShopCameraScene.ma", namespace = 'cam')

    """
    data = {ref._getNamespace():ref for ref in pm.listReferences(recursive = False)}
    for key in data:
        if debug:
            print(key, data[key])
        if os.path.abspath(filepath) == data[key].path.abspath() and key == namespace:
            print('namespace already belongs to reference with target filepath')
            #return
        elif os.path.abspath(filepath) == data[key].path.abspath():
            print('assigning namespace %s to reference in filepath %s' %(namespace,filepath))
            data[key]._setNamespace(namespace)
        elif key == namespace and os.path.abspath(filepath) != data[key].path.abspath():
            print('reference %s pushed from target namespace %s' %(data[key],namespace))
            data[key]._setNamespace(key + str(1))
        else:
            pass
    return



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



#PURPOSE        load available file references and unload unavailable ones
def load_unload_reference(reference):
    
    if os.path.isfile(reference.path.abspath()):
        if not reference.isLoaded():
            try:
                reference.load(loadReferenceDepth = 'all')
                print('loaded %s' %(reference))
            except:
                pm.warning('unknown exception when loading reference %s' %(reference))
    else:
        pm.warning('file not found')


#PURPOSE        to clean up the poorly set up references in our animation files
def clean_references(filename, filepath):
    """
    @param filename:    string of filename to search for
    @param filepath:    string of replacement path

    returns number of refs replaced

    clean_references(filename = 'Roxanne_Rig.ma', filepath = '//scenes/Rigs/roxanne_rig.mb', namespace = 'mesh', string = 'rig')
    """
    ##ZOMBIE CODE##
    #if replace:
    #    replace_target_namespace(namespace, string)
    #else:
    #    claim_namespace(filepath, namespace, debug = False)
    output = 00
    for item in pm.listReferences(recursive = True):
        load_unload_reference(item)
        if item.path.__contains__(filename):
            replace_target_reference(reference = item, filepath = filepath)
            output += 1
        else:
            continue
    return output


def get_timeline():#TODO:   move to animation or general?
    return pm.playbackOptions(query = True, minTime = True), pm.playbackOptions(query = True, maxTime = True)


def bake_animation(targets, sampling = 1, start = 0, end = 0):#TODO:   move to animation or general?
    #pm.select(bakeTarget)
    #set timeline
    playStartTime = int(pm.playbackOptions(query = True, minTime = True))
    playEndTime = int(pm.playbackOptions(query = True, maxTime = True))
    #Bake Animation
    #for target in targets:
    pm.bakeResults(targets, simulation = 1, sampleBy = sampling, pok = 1, sac = 0, time = (playStartTime, playEndTime))

    return playStartTime, playEndTime


#def fileExport(arg):
#    pm.select(arg)
#    cmds.file(outputFile, exportSelected=True, type="FBX export")


####====                    ========                    ====####
#
#                       ACTION ZONE!!!!
#
####====                    ========                    ====####

def export_skeletal_mesh():#TODO param to run prop export would be cool, not too hard....
    #print()
    import_references()
    rigs = pm.ls('*.export', objectsOnly = True, recursive = True)
    for root in rigs:
        name = root.name()
        #CBB  get_export returns _rig suffix, should have a proc to get _SKL
        #path = get_export_path(name)
        #DONE  removing display layers makes life a lot easier, non-blocker, but VERY annoying
        layers = pm.ls(type = 'displayLayer')
        for target in layers:
            pm.delete(target)
        #CBB    would be nice to clear material connections, do some cleanup
        #DONE:  combine skinMeshes
        #CBB    shouldn't need to do this mesh stuff after new publish_rig()
        '''
        meshes = [geo for geo in pm.ls() if geo.hasAttr('skinMesh')]
        #CBB an intelligent way to go to bindpose would be really great
        #pm.dagPose( restore=True, global=True, bindPose=True )
        #would need to remove extraneous bind poses, as well...
        #geo.goToBindPose()
        skinned_mesh = pm.PyNode(pm.polyUniteSkinned(meshes, ch = 0, muv = 1)[0])
        skinned_mesh.rename('skinned_mesh')
        root | skinned_mesh
        '''
        #DONE  handle joints, break connections, etc
        joints = pm.ls('*.jointSkin', objectsOnly = True, recursive = True, type = 'joint')
        #[pm.delete(item, constraints = 1), controls.break_trs_connections(item) for item in joints]
        for item in joints:
            try:
                pm.delete(item, constraints = 1)
                controls.break_trs_connections(item)
            finally:#DONE    pynode objects don't have a delete() method
                if item.hasAttr('noExport'):# or not deformers.check_skincluster2(item)
                    pm.delete(item)
        pm.delete(pm.ls('*.noExport', objectsOnly = True, recursive = True))
        #URGENT handle blend meshes
        #   ideally rename, but that may break sylv....
        pm.select(root, replace = True)
        
        pm.exportSelected(pm.fileDialog2(), force=True, type="FBX export")
    return rigs
    #else:
    #    return False


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


class character_asset():#FIXME  this is just zombie code, ,rn
    #character and skl export status
    def __init__(self, personality = '', jobClass = '', skeleton = None, simJoints=None, meshes = None, node = None):
        """
        @param personality : animation class indicating animation set
        @param jobClass : gameplay class indicating costume type
        @param skeleton : root of skeleton
        @param meshes : unicode name of geometry objects to be combined to skinned_mesh
        """
        self.name = personality.capitalize() + jobClass.capitalize()
        if node:
            self.node = r9Meta.MetaClass(node.name())
            self.skeleton, self.meshes, self.filepath = node.skeleton, node.meshes, node.filepath#set values from node
        else:
            self.node = r9Meta.MetaClass(name = self.name)
            
            self.node.addAttr('personality',attrType = 'string', value = personality)
            self.node.addAttr('jobClass',attrType = 'string', value = jobClass)#
            #node.addAttr('meshes',attrType = 'message')
            self.skeleton = skeleton
            self.node.connectChild(self.skeleton.name(), 'skeleton')#
            self.meshes = meshes
            self.node.connectChildren(self.meshes, 'meshes')
            
            #TODO CBB set these by checking pm.ls('*.jointSim', objectsOnly = True) against all skinned joints
            
            if simJoints:
                self.simJoints = simJoints
                self.node.connectChildren(cmds.ls(self.simJoints), 'jointSim')
            #node.connectChildren(skeleton, 'simJoints')#
            #testnode2.connectChild(node = newnode.shortName(), attr = 'skeleton')
            
            self.filepath = self.set_export_path()
        self.garbage = {}#TODO maybe better to store on node for consistency???
        
    def set_export_path(self):#CBB this is redundant to get_export_path()
        """
            Write filepath to node for current costume
        """
        #get_export_path(self.name, '.fbx')
        filename = self.name + '.fbx'
        #FIXME  genchar skeletal meshes should be on the same path as others
            #   putting it in models makes no sense unless all skel go to same place on model path
        filepath = os.path.abspath(pm.sceneName().split('/scenes')[0] + '/scenes/Models/GenChar/export/' +filename)
        self.node.addAttr('filepath',attrType = 'string', value = filepath)
        return filepath
    
    
    #PRESUMPTION: all files are using namespaces and we always import w/out ns
    def set_namespace_data(self):#TODO: remove this, seems extraneous
        if self.reference.isUsingNamespaces():
            self.namespace = self.reference.reference.namespace+':'
        else:
            self.prefix = self.reference.reference.namespace+'_'
        return
    #this function is redundant and superfluous
    def add_component(self,component,tag = ''):#
        self.node.connectChild(component.name(), tag)#
        return#
    def check_for_skin(mesh):
        return deformers.check_skincluster(mesh)
        
    def garbage_store(self, target):#store so we can investigate erroneous elements in the set
        self.garbage.add(target.name())
    def garbage_collect(self):
        #pm.hyperShade(o="blinn1") FIXME    need to delete everything with delete material, clear non-deform hist
        pm.delete(self.garbage)
    def process_joints(self, joints):
        processed_joints = []
        	#process child components, clean garbage
        for item in joints:
            if item.type() == 'joint':#make sure it's a joint
                #self.node.connectChild(child.name(), tag)
                item.rename(item.name().replace('Fkel', 'Skel'))
                pm.delete(item, constraints = 1)
                isSkinned = self.check_for_skin(item)#TODO: write check for skin function
                if not isSkinned:
                    self.garbage_store(item)
                else:
                    processed_joints.push(item)
            else:
                self.garbage.push(item.name())
                #pm.delete(child)    garbage collect will clean this later
        return processed_joints
    #PURPOSE    check that meshes are ready to be combined
    def validate_meshes(self):
        for mesh in self.node.meshes:#may need to explicitly cast to pynode?
            if deformers.check_skincluster(mesh):
                #TODO CBB
                #unskinned_meshes.append(mesh)
                #if mesh.skinCluster.influences() > 4:
                    #print(mesh.name() + ' exceeds max influences of 4')
                return
            else:
                #skinned_meshes.append(mesh)
                #TODO!      need some way to get the male or female mesh to copy skinweights from
                #deformers.auto_copy_weights(source_mesh = source, target_mesh=mesh)
                #add skinluster? delete mesh connection?
                #TODO!      tag source meshes with string attr that ids what they're for?
                #later we could come back and add rules for further discrimination
                return
    def auto_skin_body_parts(self, mesh):
        #TODO
            #1. need some way to get the male or female mesh to copy skinweights from
            #deformers.auto_copy_weights(source_mesh = source, target_mesh=mesh)
            #add skinluster? delete mesh connection?
            #2. tag source meshes with string attr that ids what they're for?
            #later we could come back and add rules for further discrimination
        if mesh.coverage == 'body':
            #TODO
            #find body source mesh
            #?  male/female?
            #?  namespace
            pass
        elif mesh.coverage == 'head':
            pass
        elif mesh.coverage == 'hands':
            pass
        elif mesh.coverage == 'faceParts':
            pass
        return
    def prepare_export(self):
        import_references()
        skinned_mesh = pm.polyUniteSkinned(self.meshes, ch = 0, muv = 1)
        skinned_mesh.rename('skinned_mesh')
        root = pm.group(self.skeleton, skinned_mesh, name = 'GenChar')
        #Remove extraneous joints
        self.process_joints(self.node.skeleton.getChildren())
        self.garbage_collect()
        #process child components, clean garbage
        return
    def export(self, root):
        """
        @param root : root of hierarchy to export
        """
        pm.select(root, replace = True)
        #TODO!    need to get/provide path
        pm.exportSelected(self.filepath, force=True, type="FBX export")



class genchar_asset():
    #character and skl export status
    def __init__(self, personality = '', jobClass = '', skeleton = None, simJoints=None, meshes = None, node = None):
        """
        @param personality : animation class indicating animation set
        @param jobClass : gameplay class indicating costume type
        @param skeleton : root of skeleton
        @param meshes : unicode name of geometry objects to be combined to skinned_mesh
        """
        self.name = personality.capitalize() + jobClass.capitalize()
        if node:
            self.node = r9Meta.MetaClass(node.name())
            self.skeleton, self.meshes, self.filepath = node.skeleton, node.meshes, node.filepath#set values from node
        else:
            self.node = r9Meta.MetaClass(name = self.name)
            
            self.node.addAttr('personality',attrType = 'string', value = personality)
            self.node.addAttr('jobClass',attrType = 'string', value = jobClass)#
            #node.addAttr('meshes',attrType = 'message')
            self.skeleton = skeleton
            self.node.connectChild(self.skeleton.name(), 'skeleton')#
            self.meshes = meshes
            self.node.connectChildren(self.meshes, 'meshes')
            
            #TODO   set these by checking pm.ls('*.jointSim', objectsOnly = True) against all skinned joints
            #CBB    do we really need this for anything? seems superfluous
            if simJoints:
                self.simJoints = simJoints
                self.node.connectChildren(cmds.ls(self.simJoints), 'jointSim')
            #node.connectChildren(skeleton, 'simJoints')#
            #testnode2.connectChild(node = newnode.shortName(), attr = 'skeleton')
            
            self.filepath = self.set_export_path()
        self.garbage = {}#TODO maybe better to store on node for consistency???
        
    def set_export_path(self):#CBB this is redundant to get_export_path()
        """
            Write filepath to node for current costume
        """
        #get_export_path(self.name, '.fbx')
        filename = self.name + '.fbx'
        #FIXME  genchar skeletal meshes should be on the same path as others
            #   putting it in models makes no sense unless all skel go to same place on model path
        filepath = os.path.abspath(pm.sceneName().split('/scenes')[0] + '/scenes/Models/GenChar/export/' +filename)
        self.node.addAttr('filepath',attrType = 'string', value = filepath)
        return filepath
    
    
    #PRESUMPTION: all files are using namespaces and we always import w/out ns
    def set_namespace_data(self):#TODO: remove this, seems extraneous
        if self.reference.isUsingNamespaces():
            self.namespace = self.reference.reference.namespace+':'
        else:
            self.prefix = self.reference.reference.namespace+'_'
        return
    #this function is redundant and superfluous
    def add_component(self,component,tag = ''):#
        self.node.connectChild(component.name(), tag)#
        return#
    def check_for_skin(mesh):
        return deformers.check_skincluster(mesh)
        
    def garbage_store(self, target):#store so we can investigate erroneous elements in the set
        self.garbage.add(target.name())
    def garbage_collect(self):
        #pm.hyperShade(o="blinn1") FIXME    need to delete everything with delete material, clear non-deform hist
        pm.delete(self.garbage)
    def process_joints(self, joints):
        processed_joints = []
        	#process child components, clean garbage
        for item in joints:
            if item.type() == 'joint':#make sure it's a joint
                #self.node.connectChild(child.name(), tag)
                item.rename(item.name().replace('Fkel', 'Skel'))
                pm.delete(item, constraints = 1)
                isSkinned = self.check_for_skin(item)#TODO: write check for skin function
                if not isSkinned:
                    self.garbage_store(item)
                else:
                    processed_joints.push(item)
            else:
                self.garbage.push(item.name())
                #pm.delete(child)    garbage collect will clean this later
        return processed_joints
    #PURPOSE    check that meshes are ready to be combined
    def validate_meshes(self):
        for mesh in self.node.meshes:#may need to explicitly cast to pynode?
            if deformers.check_skincluster(mesh):
                #TODO CBB
                #if mesh.skinCluster.influences() > 4:
                    #print(mesh.name() + ' exceeds max influences of 4')
                return
            else:
                #TODO!      need some way to get the male or female mesh to copy skinweights from
                #deformers.auto_copy_weights(source_mesh = source, target_mesh=mesh)
                #add skinluster? delete mesh connection?
                #TODO!      tag source meshes with string attr that ids what they're for?
                #later we could come back and add rules for further discrimination
                return
    def prepare_export(self):
        import_references()
        skinned_mesh = pm.polyUniteSkinned(self.meshes, ch = 0, muv = 1)
        skinned_mesh.rename('skinned_mesh')
        #TODO   maybe GenChar rig gets its own character node?
        root = pm.group(self.skeleton, skinned_mesh, name = 'GenChar')
        #Remove extraneous joints
        self.process_joints(self.node.skeleton.getChildren())
        self.garbage_collect()
        #process child components, clean garbage
        return
    def export(self, root):
        """
        @param root : root of hierarchy to export
        """
        pm.select(root, replace = True)
        #TODO!    need to get/provide path
        pm.exportSelected(self.filepath, force=True, type="FBX export")



class anim_asset(character_asset):
    assets = []#to track all asset class instances

    def __init__(self, root):
        self.reference = get_reference(root)
        if need_export(root):
            self.export = True
        name = root.name().split(ns_data[1])[1]
        
        self.filepath = get_export_path(name)
        if self.reference.isUsingNamespaces():
            self.namespace = self.reference.reference.namespace+':'
        else:
            self.prefix = self.reference.reference.namespace+'_'
            
        self.debug = False
    
    def prep_for_export(self):
        pass


#PURPOSE        get dictionaries of export data for all chars in current scene
#PRESUMPTION    rigs are tagged correctly, conform to standard
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


def prep_character(root, overwrite = False):
    """
    prep single character, arg is character root
    """
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
        #characters.append(character_data)
        #print(character_data)
    else:
        print('scene file is older than export')
    return character_data


def export_animation(data):#TODO    this should go inside ptionomics_export1()
    """
    arg data is character dictionary as output by prep_character()
    """
    print(data)
    if data['namespace_data'][0]:
        try:
            target_namespace = data['namespace_data'][1]
            pm.namespace(removeNamespace = target_namespace, mergeNamespaceWithRoot = True)
            #voe.export_animation(data['root'], data['path'])#
        except:
            pass
    else:
        remove_scene_prefix(data['namespace_data'][1])
    try:
        play_start_time = int(pm.playbackOptions(query = True, minTime = True))
        play_end_time = int(pm.playbackOptions(query = True, maxTime = True))
<<<<<<< HEAD
        #URGENT     this seems to be failing
        joint_targets = pm.ls('*.jointSkin', objectsOnly = True, recursive = True)
        blendshape_targets = pm.ls(type='blendShape', objectsOnly = True, recursive = True)#CBB using this operator is probably bad practice
        bake_targets = joint_targets + blendshape_targets
        #failure happened here, wasn't passing targets for baking
=======
        bake_targets = pm.ls('*.jointSkin', objectsOnly = True, recursive = True)
        bake_targets += pm.ls(type = 'blendShape', objectsOnly = True, recursive = True)
>>>>>>> 2ad61e725cd35801c700f7dc36c3b741f2189eaa
        bake_animation(bake_targets, start = play_start_time, end = play_end_time)
        #export_animation1(data['root'], data['path'])#
    except:
        pm.warning('bake failed')
    pm.delete(pm.ls('*.noExport', objectsOnly = True, recursive = True))
<<<<<<< HEAD
    #we'll be tagging blendshape meshes with noExport to take them out of anim files
    #for sylvia, keeping the blendmesh has become necessary, described in [[Sylv Blendshape Bugs]]
=======
>>>>>>> 2ad61e725cd35801c700f7dc36c3b741f2189eaa
    #pm.delete(pm.ls('*.blendMesh', objectsOnly = True, recursive = True))
    pm.delete(pm.ls('*.skinMesh', objectsOnly = True, recursive = True))
    pm.select(data['root'], replace = True)
    pm.exportSelected(data['path'], force=True, type="FBX export")
    return True


def potionomics_export1(characters):
    """
    exprt animation
    """
    #FIXME  should use prep_character() and export_animation()
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
            play_start_time = int(pm.playbackOptions(query = True, minTime = True))
            play_end_time = int(pm.playbackOptions(query = True, maxTime = True))
            bake_animation(pm.ls('*.jointSkin', objectsOnly = True, recursive = True), start = play_start_time, end = play_end_time)
        except:
            pm.warning('bake failed')
        pm.delete(pm.ls('*.noExport', objectsOnly = True, recursive = True))
        pm.delete(pm.ls('*.skinMesh', objectsOnly = True, recursive = True))
        pm.select(this_dict['root'], replace = True)
        pm.exportSelected(this_dict['path'], force=True, type="FBX export")
    return True
    #else:
    #    return False



class export_system():
    assets = []#to track all asset class instances

    def __init__(self, name_space, file_path, debug):
        self.namespace = str
        self.filepath = str
        self.debug = False

    def process(self, args):#export skel or anim? time range? 
        for char_dict in args:
            if char_dict['namespace_data'][0]:
                try:
                    target_namespace = char_dict['namespace_data'][1]
                    pm.namespace(removeNamespace = target_namespace, mergeNamespaceWithRoot = True)
                    #voe.export_animation(this_dict['root'], this_dict['path'])#
                except:
                    pass
            else:
                remove_scene_prefix(char_dict['namespace_data'][1])
            try:
                play_start_time = int(pm.playbackOptions(query = True, minTime = True))
                play_end_time = int(pm.playbackOptions(query = True, maxTime = True))
                bake_animation(pm.ls('*.jointSkin', objectsOnly = True, recursive = True), start = play_start_time, end = play_end_time)
            except:
                pm.warning('bake failed')
            self.clean()
            self.export(char_dict['root'])
        return True

    def export(self, root):
        """
        @param root : root of hierarchy to export
        """
        pm.select(root, replace = True)
        pm.exportSelected(root, force=True, type="FBX export")

    def clean(self, profile = ''):#TODO:    make profiles to delete specific subsets of stuff
        targets = pm.ls('*.noExport', objectsOnly = True, recursive = True)
        pm.delete(targets)


    def run(self, args):
        return self.process(args)



"""


import vo_maya.core.vo_export as voe
reload(voe)

characters = voe.character_prep1(overwrite = True)
if len(characters) > 0:
    voe.import_references()
    voe.potionomics_export1(characters)
else:
    print('nothing to export')

"""


#characters = character_prep()

#potionomics_export(characters)






