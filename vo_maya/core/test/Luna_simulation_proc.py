import pymel.core as pm
import maya.cmds as cmds
import os as os
import vo_maya.core.vo_animation as voa
import vo_maya.core.vo_general as vog

#NOTE:  01  set character name and path for config files
target_character = "Luna"#name of rig root without namespace
#NOTE:  02  config_path MUST prefix with r if it contains backslashes
config_path = r"Z:\0_p4v\PotionomicsSourceAssets\Art_sourcefiles\Characters\scenes\Animation\Luna\config"#Z:\0_p4v\PotionomicsSourceAssets\Art_sourcefiles\Characters\scenes\Animation\Luna\config
Asset_Data = vog.AnimAsset(root = pm.ls(target_character,recursive = 1)[0], pose_path = "Z:/0_p4v/PotionomicsSourceAssets/Maya_sourcefiles/PoseLibrary/Luna")


sim_group_01 = {#NOTE:  03  make one of these for each chain that needs to be simulated
    "targets" : [u'r:Luna_L_antenna_01_CTL', u'r:Luna_L_antenna_02_CTL', u'r:Luna_L_antenna_03_CTL', u'r:Luna_L_antenna_04_CTL', u'r:Luna_L_antenna_05_CTL', u'r:Luna_L_antenna_06_CTL', u'r:Luna_L_antenna_07_CTL'],
    "config" : 'antenna_stiff_simple.cfg',#name of config file with simulation settings
    "sim_type" : "chain"#chain, point, or chain_simple to indicate which key and SimulatorModule to use
}

sim_group_02 = {#make one of these for each chain that needs to be simulated
    "targets" : [u'r:Luna_L_antenna_01_CTL', u'r:Luna_L_antenna_02_CTL', u'r:Luna_L_antenna_03_CTL', u'r:Luna_L_antenna_04_CTL', u'r:Luna_L_antenna_05_CTL', u'r:Luna_L_antenna_06_CTL', u'r:Luna_L_antenna_07_CTL'],
    "config" : 'antenna_stiff_simple.cfg',#name of config file with simulation settings
    "sim_type" : "chain"#chain, point, or chain_simple to indicate which key and SimulatorModule to use
}

#NOTE:  04  list all sim objects in sim_list
sim_list = [sim_group_01, sim_group_02]
target_chains = [item['targets'] for item in sim_list]
priority_list = [item['targets'][0] for item in sim_list]

#sets anim timeline buffer
pm.playbackOptions(min = Asset_Data.start_frame - 10, max = Asset_Data.end_frame + 10)

anim_layers = voa.get_anim_layers()
if anim_layers:
    voa.do_bake(True, False)
else:
    pass

sim_layer = voa.create_anim_layer(anim_layer_name = "SimulationAnimLayer", objects = target_chains)
pm.animLayer(query=True, root=True).setLock()
voa.select_anim_layer(anim_layer = None)


for item in sim_list:
    #TODO: loop to read values from config
    config_file = os.path.normpath(os.path.join(config_path, item["config"])).replace('\\', '/')#replace with data from sim_dict
    testty = BroTools.core.config_parser.BroConfig(config_file)
    sim_dict = testty.__dict__
    values = testty.__dict__['chain_simple'].__dict__#TODO:     take key from sim_dict['sim_type']
    sim_parameters = {
                    "preserveAnimation" : True,
                    "simulationProperties" : testty.__dict__['chain_simple'].__dict__,
                    "collisionMode" : False,
                    "dontRefresh" : True,
                    "skipControls" : 0,
                    "skipFrames" : 0,
                    "aimRotation" : False,
                    "matchPositions" : True,
                    "debugMode" : False,
                    "deleteNucleus" : False,
                    "up" : ['x','y','z'],
                    "axis" : ['x','y','z']
                    }
    #running simulation

    simulator = BroTools.BroDynamics.modules.chain_simple.SimulatorModule()
    #objects = cmds.ls(sl=1)#replace with sim target
    simulator.run(objects, **sim_parameters)

#TODO:  poseCorrectLayer.setKeyframe(weight), add controls, key pose corrections
voa.pose_correct_layer(root, targets, AnimAsset)

pm.playbackOptions(min = Asset_Data.start_frame, max = Asset_Data.end_frame)


