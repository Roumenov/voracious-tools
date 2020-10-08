"""
    animation stuff, mostly layer management 
"""


import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import Red9.core.Red9_PoseSaver as r9Pose
import Red9.core.Red9_CoreUtils as r9Core
import Red9.startup.setup as r9Setup



def create_anim_layer(anim_layer_name):
    base_anim_layer = pm.animLayer(query=True, root=True)

    if (base_anim_layer != None):
        child_layers = pm.animLayer(base_anim_layer, query=True, children=True)

        if (len(child_layers) > 0) :
            if anim_layer_name in child_layers:
                pm.warning('Layer ' + anim_layer_name + ' already exists')
            else:
                new_anim_layer = pm.animLayer(anim_layer_name)
                return new_anim_layer
        else:
            new_anim_layer = pm.animLayer(anim_layer_name)
            return new_anim_layer
    else:
        new_anim_layer = pm.animLayer(anim_layer_name)
        return new_anim_layer

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
        return anim_layers
    

#create_anim_layer("SimulationAnimLayer")


def select_layer_objects():
    anim_layer_editor = 'AnimLayerTabanimLayerEditor'
    current_anim_layers = pm.treeView(anim_layer_editor, q=True, si=True)
    pm.mel.layerEditorSelectObjectAnimLayer(current_anim_layers)


def flatten_anim_layers():
    return


def getPoseFolder():
    return os.path.abspath("Z:/0_p4v/PotionomicsSourceAssets/Maya_sourcefiles/PoseLibrary/Roxanne/emot_doubtful.pose")
    #return os.path.join(r9Setup.red9ModulePath(), 'tests', 'testFiles', 'MetaRig_Poses')

class PoseData_Loader():
    '''
    same set of tests as the meta but going through the nodeType filters and 
    matchMethods stripPrefix/mirrorIndex/index etc
    '''
    def __init__(self, root):
        #cmds.file(os.path.join(r9Setup.red9ModulePath(), 'tests', 'testFiles', 'MetaRig_anim_jump.mb'), open=True, f=True)
        self.rootNode = root##TODO:    see if this what gets set from setRoot button, test with one arg
        self.poseFolder = getPoseFolder()

        # make our PoseData object with the unitTest config loaded
        filterNode = r9Core.FilterNode_Settings()
        filterNode.nodeTypes = 'nurbsCurve'
        filterNode.incRoots = False
        filterNode.filterPriority = ['Roxanne_ROOTC', 'Roxanne_MainHipC', 'Roxanne_HeadC']#TODO:    test with no args
        self.poseData = r9Pose.PoseData(filterNode)
    
    def test_poseLoad_relativeProjected_stripPrefix(self):
        '''
        load the pose with relative and check against the store 'projected' posefile
        copied from Test_PoseData_loaders.test_poseLoad_relativeProjected_stripPrefix(self)
        '''
        # stripPrefix Match -------------------------------------------------
        self.poseData.matchMethod = 'stripPrefix'
        #TODO:  join path? look at other test functions to decipher what _projected is for
        requiredPose = required_Pose#os.path.join(self.poseFolder, 'jump_f218_projected.pose')
        filepath = file_path#os.path.join(self.poseFolder, 'jump_f218.pose')
        #cmds.select('L_Foot_Ctrl')
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

