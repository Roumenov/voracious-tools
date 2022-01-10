"""
    functions for character export
    TODO    add proc for exporting animated props
    CBB    replace cmds.file usage with whatever the pymel equivalent is

"""

import pymel.core as pm
import maya.cmds as cmds
import vo_deformers as deformers
import vo_general as general
import Red9.core.Red9_Meta as r9Meta
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


def generate_scene_list(raw, path= None, name = None):
    output = str([path+item+'.ma' for item in raw.split('\n')])
    return output
#generate_scene_list(raw, path = voe.get_export_path('Roxanne').split('Export')[0])
#
def get_export_path(character_name):#CBB:    character_name conflicts with local variable
    """
        Get 
    """
    #CBB:  store these values into the .export attr
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


#CBB:      reevaluate whether this is still necessary, seems like you could just do object._setNamespace('root') or smth
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


def get_timeline():#CBB:   move to animation or general?
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



class character_asset():
    #character and skl export status
    def __init__(self, personality = '', jobClass = '', skeleton = None, simJoints=None, meshes = None, node = None):
        """
        @param personality : animation class indicating animation set
        @param jobClass : gameplay class indicating costume type
        @param skeleton : root of skeleton
        @param meshes : unicode name of geometry objects to be combined to skinned_mesh

        @param node : passed in as pyObject reference....
        """
        
        if node:
            self.node = r9Meta.MetaClass(node.name())
            self.name = node.personality.capitalize() + node.jobClass.capitalize()
            self.skeleton, self.meshes, self.filepath = node.skeleton, node.meshes, node.filepath#set values from node
        else:
            self.node = r9Meta.MetaClass(name = self.name)
            self.name = personality.capitalize() + jobClass.capitalize()
            self.node.addAttr('personality',attrType = 'string', value = personality)
            self.node.addAttr('jobClass',attrType = 'string', value = jobClass)#
            #node.addAttr('meshes',attrType = 'message')
            #self.skeleton = skeleton
            self.node.connectChild(skeleton.name(), 'skeleton')#
            #self.meshes = meshes
            self.node.connectChildren(meshes, 'meshes')#FIXME   need to account for skinMesh tag
            
            #CBB set these by checking pm.ls('*.jointSim', objectsOnly = True) against all skinned joints
            if simJoints:
                #self.simJoints = simJoints
                self.node.connectChildren(cmds.ls(simJoints), 'jointSim')
            #node.connectChildren(skeleton, 'simJoints')#
            self.set_export_path()
        self.garbage = {}#maybe better to store on node for consistency???
        
    def set_export_path(self):
        """
            Write filepath to node for current costume
        """
        output_path = None
        filename = self.name + '.fbx'
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
                isSkinned = deformers.check_skincluster(item)#TODO: write check for skin function
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
        skinned_meshes = self.node.meshes
        unskinned_meshes = self.node.meshes
        for mesh in self.node.meshes:#may need to explicitly cast to pynode?
            if not deformers.check_skincluster(mesh):
                unskinned_meshes.append(mesh)
                skinned_meshes.pop(mesh)
                #prop : 
                ##mesh_node = r9Meta.MetaClass(mesh.name())
                #node.addAttr('coverage', 'body')
                ##mesh_node.coverage
                #match coverage with source
                #TODO!      need some way to get the male or female mesh to copy skinweights from
                #deformers.auto_copy_weights(source_mesh = source, target_mesh=mesh)
                #add skinluster? delete mesh connection?
                #TODO!      tag source meshes with string attr that ids what they're for?
                #later we could come back and add rules for further discrimination
                
            else:#[body, hands, legs, arms, head, face] indicate influence joint set
                skinned_meshes.append(mesh)
                unskinned_meshes.pop(mesh)
                #CBB
                #if mesh.skinCluster.influences() > 4:
                    #print(mesh.name() + ' exceeds max influences of 4')
        return skinned_meshes, unskinned_meshes
    ##      SPECIAL SKIN PROCS
    def auto_skin_body_parts(self, mesh):
        #need to 
        if mesh.coverage == 'body':
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
    def import_costume_cluster(self,mesh):
        
        return
    def prepare_export(self):
        import_references()
        skinned_meshes, unskinned_meshes = self.validate_meshes()
        skinned_mesh = pm.polyUniteSkinned(skinned_meshes, ch = 0, muv = 1)
        skinned_mesh.rename('skinned_mesh')
        root = pm.group(self.node.skeleton, skinned_mesh, name = 'GenChar')
        garbage = pm.group(unskinned_meshes, name = '{}_unskinned_meshes'.format(self.name))
        #Remove extraneous joints
        self.process_joints(self.node.skeleton.getChildren())
        self.garbage_collect()
        #process child components, clean garbage
        return root, garbage
    def export(self, root):
        """
        @param root : root of hierarchy to export
        """
        pm.select(root, replace = True)
        #TODO!    need to get/provide path
        pm.exportSelected(self.filepath, force=True, type="FBX export")



class genchar_asset():#FIXME    subclass from character asset, add personality+job class params
    #character and skl export status
    def __init__(self,name):
        self.node = r9Meta.MetaClass(name=name)
        node.addAttr('meshes',attrType = 'message')
        node.addAttr('joints',attrType = 'message')#root, simulation
        node.addAttr('personality',attrType = 'message')
        node.addAttr('class',attrType = 'message')
        self.reference = get_reference()
        self.export = need_export()
        
        #node.addAttr(tag)
        self.reference = get_reference(root)#TODO
        if need_export():
            self.export = True
        name = root.name().split(ns_data[1])[1]#TODO
        
        self.filepath = get_export_path(name)
        if self.reference.isUsingNamespaces():
            self.namespace = self.reference.reference.namespace+':'
        else:
            self.prefix = self.reference.reference.namespace+'_'
            
        return
    def add_component(self,component):
        node.connectChild(component.name())
        return
    def add_mesh(self,mesh):
        node.connectChild(mesh.name(),'meshes')
        return



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


def export_animation(data):
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
        bake_animation(pm.ls('*.jointSkin', objectsOnly = True, recursive = True), start = play_start_time, end = play_end_time)
        #export_animation1(data['root'], data['path'])#
    except:
        pm.warning('bake failed')
    pm.delete(pm.ls('*.noExport', objectsOnly = True, recursive = True))
    pm.select(data['root'], replace = True)
    pm.exportSelected(data['path'], force=True, type="FBX export")
    return True


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
            play_start_time = int(pm.playbackOptions(query = True, minTime = True))
            play_end_time = int(pm.playbackOptions(query = True, maxTime = True))
            bake_animation(pm.ls('*.jointSkin', objectsOnly = True, recursive = True), start = play_start_time, end = play_end_time)
        except:
            pm.warning('bake failed')
        pm.delete(pm.ls('*.noExport', objectsOnly = True, recursive = True))
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






