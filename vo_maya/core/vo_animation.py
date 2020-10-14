"""
    animation stuff, mostly layer management 
"""

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import os as os
import Red9.core.Red9_PoseSaver as r9Pose
import Red9.core.Red9_CoreUtils as r9Core
import Red9.startup.setup as r9Setup



def create_anim_layer(anim_layer_name = None, objects = None):
    """
    #create_anim_layer("SimulationAnimLayer")
    """
    base_anim_layer = pm.animLayer(query=True, root=True)

    if (base_anim_layer != None):
        child_layers = pm.animLayer(base_anim_layer, query=True, children=True)

        if (len(child_layers) > 0) :
            if anim_layer_name in child_layers:
                pm.warning('Layer ' + anim_layer_name + ' already exists')
            else:
                new_anim_layer = pm.animLayer(anim_layer_name)
                #return new_anim_layer
        else:
            new_anim_layer = pm.animLayer(anim_layer_name)
            #return new_anim_layer
    else:
        new_anim_layer = pm.animLayer(anim_layer_name)
    if objects:
        print(objects)
        pm.select(objects, replace = True)
        add_objects_to_anim_layer(objects, new_anim_layer)
    return new_anim_layer


def add_objects_to_anim_layer(objects, anim_layer):
    """
    Add the specified objects to the specified animation layer.
    addObjectsToAnimLayer(objects = pm.ls(sl=1), anim_layer = sim_layer)
    """
    if not hasattr(objects, '__iter__'):#TODO:      apparently this is bad practice, replace with getattr() as shown here https://hynek.me/articles/hasattr/
        objects = [objects]
    
    for item in objects:
        attributes = pm.listAttr(item, keyable=True, unlocked=True)
        if not attributes:
            pm.warning('Object "{0}" had no keyable attributes to add to animation layer.')
            continue
        
        object_attrs = ['{0}.{1}'.format(item.name(), attr) for attr in attributes]
        pm.animLayer(anim_layer, e=True, attribute=object_attrs)


def get_anim_layers():
    anim_layers = []
    try:
        base_anim_layer = pm.animLayer(query=True, root=True)
        anim_layers.append(base_anim_layer)
        child_layers = pm.animLayer(base_anim_layer, query=True, children=True)
        for item in child_layers:
            anim_layers.append(item)
        #if (len(child_layers) > 0 ):
        #    anim_layers.append(child_layers)
        return anim_layers
    except:
        pm.warning('no base layer found in scene')
        return None
    

def select_anim_layer(anim_layer = None):
    '''
    Deselect anim layers and select the specified animation layer
    '''
    #deselect all layers
    for layer in pm.ls(type='animLayer'):
        pm.animLayer(layer, edit=True, selected=False, preferred=False)
    if anim_layer:
        pm.animLayer(anim_layer, edit=True, selected=True, preferred=True)
    else:
        pm.warning('no anim_layer provided')


def select_active_layer_objects():
    anim_layer_editor = 'AnimLayerTabanimLayerEditor'
    current_anim_layers = pm.treeView(anim_layer_editor, q=True, si=True)
    pm.mel.layerEditorSelectObjectAnimLayer(current_anim_layers)

#
def get_layer_objects(anim_layer = None):
    """
    get_layer_objects(anim_layer = pm.PyNode('AnimLayer1'))
    """
    layer_objects = []
    if type(anim_layer) == pm.nodetypes.AnimLayer:
        layer_objects = anim_layer.__getattr__('dagSetMembers').listConnections()
    else:#no valid animation layer, select objects in active layer
        all_layers = get_anim_layers()
        for layer in all_layers:
            layer_objects.extend(layer.__getattr__('dagSetMembers').listConnections())
    return set(layer_objects)

def select_layer_objects(anim_layer = None):
    pm.select(clear = True)
    layer_objects = []
    if type(anim_layer) == pm.nodetypes.AnimLayer:
        pm.mel.layerEditorSelectObjectAnimLayer(anim_layer.name())
        layer_objects = pm.ls(sl=1)
        return layer_objects
    else:#no valid animation layer, select objects in active layer
        all_layers = get_anim_layers()
        
        for layer in all_layers:
            pm.mel.layerEditorSelectObjectAnimLayer(layer)
            layer_objects.append(pm.ls(sl=1))
        #used to select from active layer
        #anim_layer_editor = 'AnimLayerTabanimLayerEditor'
        #current_anim_layer = pm.treeView(anim_layer_editor, q=True, si=True)
        #pm.mel.layerEditorSelectObjectAnimLayer(current_anim_layer)
    return set(layer_objects)


def flatten_anim_layers():
    return


def pose_correct_layer(targets, priority, AnimAsset):
    """

    """
    pose_layer = create_anim_layer(anim_layer_name = 'PoseCorrectLayer', objects = targets)
    select_anim_layer(anim_layer = pose_layer)
    #select_layer_objects(anim_layer = pose_layer)
    loader = PoseData_Loader(AnimAsset.root, priority)
    start_pose, end_pose = AnimAsset.get_pose_path()
    #GOTO:  anim start
    pm.currentTime(AnimAsset.start_frame, edit = True)
    pm.select(targets, clear = True)
    loader.poseLoad_relativeProjected_stripPrefix(start_pose)
    pm.setKeyframe(targets, animLayer = pose_layer, time=AnimAsset.start_frame)#key controls
    #GOTO:  anim end
    pm.currentTime(AnimAsset.end_frame, edit = True)
    pm.select(targets, clear = True)
    loader.poseLoad_relativeProjected_stripPrefix(end_pose)
    pm.setKeyframe(targets, animLayer = pose_layer, time=AnimAsset.end_frame)#key controls
    return pose_layer


def getPoseFolder():
    return os.path.abspath("Z:/0_p4v/PotionomicsSourceAssets/Maya_sourcefiles/PoseLibrary/Roxanne/emot_doubtful.pose")
    #return os.path.join(r9Setup.red9ModulePath(), 'tests', 'testFiles', 'MetaRig_Poses')

class PoseData_Loader():
    '''
    same set of tests as the meta but going through the nodeType filters and 
    matchMethods stripPrefix/mirrorIndex/index etc

    test = Test_PoseData_loaders()
    test.setup()
    test.poseLoad_relativeProjected_stripPrefix()
    '''
    def __init__(self, root, priority):
        #cmds.file(os.path.join(r9Setup.red9ModulePath(), 'tests', 'testFiles', 'MetaRig_anim_jump.mb'), open=True, f=True)
        self.rootNode = root##TODO:    see if this what gets set from setRoot button, test with one arg
        #self.poseFolder = getPoseFolder()#TODO:     get from args, will pass from AnimAsset

        # make PoseData object with the unitTest config loaded
        filterNode = r9Core.FilterNode_Settings()
        filterNode.nodeTypes = 'nurbsCurve'
        filterNode.incRoots = False
        filterNode.filterPriority = priority#['Roxanne_ROOTC', 'Roxanne_MainHipC', 'Roxanne_HeadC']#TODO:    test with no args or load every first list target ??
        self.poseData = r9Pose.PoseData(filterNode)
    
    def poseLoad_relativeProjected_stripPrefix(self, file_path):
        '''
        load the pose with relative and check against the store 'projected' posefile
        copied from Test_PoseData_loaders.poseLoad_relativeProjected_stripPrefix(self)
        '''
        # stripPrefix Match -------------------------------------------------
        self.poseData.matchMethod = 'stripPrefix'
        #TODO:  join path? look at other test functions to decipher what _projected is for
        requiredPose = file_path#os.path.join(self.poseFolder, 'jump_f218_projected.pose')
        #filepath = file_path#os.path.join(self.poseFolder, 'jump_f218.pose')
        #cmds.select('L_Foot_Ctrl')
        #TODO:  select target controls
        self.poseData.poseLoad(self.rootNode, filepath=file_path, useFilter=True,
                               relativePose=True,
                               relativeRots='projected',
                               relativeTrans='projected')#TODO:     test with 'absolute'
        print '\n\n\n##########   MAYA UP AXIS : ###################', r9Setup.mayaUpAxis()#prints up axis, seems unnecessary

        # the pose is no longer in the same space due to the relative code,
        # we need up update the internal pose before comparing
        nodes = self.poseData.buildDataMap(self.rootNode)
        self.poseData.buildBlocks_fill(nodes)
        assert r9Pose.PoseCompare(self.poseData, requiredPose).compare()



"""
Anim Bake is to simplify making global changes to cycle animations that have been built with infinity curves offset
from each other. Standard Maya baking and copying of curves does not preserve tangent information, so this script
ensures that the start/end key tangents are identical before baking, keeping the curves identical. 
In addition, the tool has settings to automatically bake all animation layers, as well as trim the animation to the
time range without altering the curve shapes at all.
Author: Eric Luhta, ericluhta@gmail.com
to use:
  import vo_maya.core.vo_animation as voa
  reload(voa)
  voa.window_ui()
commands for executing without UI (for hotkeys or right click shelf button):
all layers and trim:
  import vo_maya.core.vo_animation as voa
  reload(voa)
  voa.do_bake(True, True)
  
all layers no trim:
  import vo_maya.core.vo_animation as voa
  reload(voa)
  voa.do_bake(True, False)
current layer and trim:
  import vo_maya.core.vo_animation as voa
  reload(voa)
  voa.do_bake(False, True)
current layer no trim:
  import vo_maya.core.vo_animation as voa
  reload(voa)
  voa.do_bake(False, False)
"""


class AnimBake:
    """
    Class for holding data and functions to do the bake and track desired options.
    Attributes:
        time_range : tuple of first and last frames taken from the Maya timeline
        anim_length : the length of the animation in frames
        curves : a list of all the animation curve names
        child_layers : a list of anim layers if present
        bake_all_layers : option to bake anim layers instead of just current layer
        has_anim_layers : stores if anim layers are present
        BUFFER : anim_length * 2 that's used to overshoot time range before/after to make sure all keys are captured
        SET_KEYS_AT : a list used to keep the first and last keys, -/+ 1 respectively. Used for setting keys that
                        preserve Maya's tangent information
    """

    def __init__(self, bake_all_layers=False, buffer_multiplier=2):
        self.time_range = (pm.playbackOptions(q=True, min=True), pm.playbackOptions(q=True, max=True))
        self.anim_length = abs(self.time_range[1] - self.time_range[0])
        self.curves = pm.findKeyframe(curve=True)
        self.child_layers = None
        self.bake_all_layers = bake_all_layers
        self.has_anim_layers = self.check_anim_layers()

        self.BUFFER = self.anim_length * buffer_multiplier
        self.SET_KEYS_AT = [self.time_range[0] - 1, self.time_range[1] + 1, self.time_range[0], self.time_range[1]]

    def get_first_last_keys(self, curve):
        """
        :param curve: the anim curve to get the first and last keys from
        :return: tuple of first and last frames of the curve
        """
        first_key = pm.findKeyframe(curve, which='first')
        last_key = pm.findKeyframe(curve, which='last')
        return first_key, last_key

    def check_anim_layers(self):
        """
        checks if anim layers exist and if so, puts the names of them in the attribute
        :return: if anim layers are present or not
        """
        self.base_anim_layer = cmds.animLayer(q=True, root=True)
        found_layer = False

        # if the BaseAnimation layer exists check if there are other child layers
        if self.base_anim_layer is not None:
            self.child_layers = cmds.animLayer(self.base_anim_layer, q=True, children=True)

            if (self.child_layers is not None) and (len(self.child_layers) > 0):
                found_layer = True

        return found_layer

    def add_all_layer_curves(self):
        """
        Goes through all layers and adds their anim curves to the master list to be baked
        :return: None
        """
        if self.has_anim_layers:
            self.curves = [curve for curve in cmds.listHistory(pdo=True,
                                                               lf=False) if
                           cmds.nodeType(curve, i=True)[0] == 'animCurve']

    def curves_exist(self):
        """
        Makes sure list of curves isn't empty, otherwise stop and display a warning
        :return: self.curves is not empty
        """
        if self.curves is not None:
            return True
        else:
            pm.warning('[anim_bake.py] No curves to bake')
            return False

    def bake_curves(self):
        """
        Checks all the keyframe tangent information of the first and last keys, then makes sure its identical
        between them
        :return: None
        """
        if self.curves_exist():
            for curve in self.curves:
                keys = self.get_first_last_keys(curve)

                # get the correct tangent weights/angles on the first and last keys of the curve
                first_tangent = pm.keyTangent(curve, q=True, outWeight=True, time=(keys[0],))[0]
                first_angle = pm.keyTangent(curve, q=True, outAngle=True, time=(keys[0],))[0]
                last_tangent = pm.keyTangent(curve, q=True, inWeight=True, time=(keys[1],))[0]
                last_angle = pm.keyTangent(curve, q=True, inAngle=True, time=(keys[1],))[0]

                # check all the tangents and make sure they are the same on the first/last keys
                tangent_opts = {'inWeight': last_tangent,
                                'inAngle': last_angle,
                                'outWeight': first_tangent,
                                'outAngle': first_angle}

                for key in keys:
                    pm.keyTangent(curve, edit=True, time=(key,), lock=False, **tangent_opts)

                # bake the curve
                pm.bakeResults(curve, time=(self.time_range[0] - self.BUFFER, self.time_range[1] + self.BUFFER),
                               sac=True)

    def trim_bake_to_timerange(self):
        """
        Cuts down the curves to the range of the timeline while keeping tangents intact
        :return: None
        """
        # set keys at the start/end of the range and one frame outside to create a BUFFER
        if self.curves_exist():
            for curve in self.curves:
                for key in self.SET_KEYS_AT:
                    pm.setKeyframe(curve, insert=True, time=key)

                # delete the extraneous keys
                pm.cutKey(curve, clear=True, time=(self.time_range[0] - self.BUFFER, self.time_range[0] - 1))
                pm.cutKey(curve, clear=True, time=(self.time_range[1] + 1, self.time_range[1] + self.BUFFER))


def do_bake(bake_layers, trim_curves):
    """
    Create a class to do the operations, check the options, and DO IT
    :param bake_layers: should we bake all the layers or not
    :param trim_curves: should we trim curves to the time range or not
    :return: None
    """
    if len(pm.ls(selection=True)):
        bake = AnimBake(bake_layers)

        if bake_layers:
            bake.add_all_layer_curves()

        bake.bake_curves()

        if trim_curves:
            bake.trim_bake_to_timerange()
    else:
        pm.warning('[anim_bake.py] Nothing selected.')


# Interface

def window_ui():
    """ Tool window and UI """
    windowID = "anim_bake"

    if pm.window(windowID, exists=True):
        pm.deleteUI(windowID)

    tool_window = pm.window(windowID, title="Anim Bake", width=200, height=50, mnb=False, mxb=False, sizeable=True)
    main_layout = pm.rowColumnLayout(width=200, height=50)

    # Main tool tab
    top_layout = pm.rowColumnLayout(nc=2, w=200, h=20, cw=[(1, 90), (2, 110)])
    bake_layers = pm.checkBox(label='use all layers', v=False)
    trim_curves = pm.checkBox(label='trim curves?', v=True)
    pm.setParent('..')
    # setup to convert options from ui.
    setup_bake = lambda x=bake_layers, y=trim_curves: do_bake(x.getValue(), y.getValue())
    pm.button(label="DO IT", bgc=(.969, .922, .145), c=pm.Callback(setup_bake), w=50)
    pm.showWindow(tool_window)