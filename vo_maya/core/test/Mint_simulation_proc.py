
import pymel.core as pm
import maya.cmds as cmds
import os as os
import vo_maya.core.vo_animation as voa
import vo_maya.core.vo_general as vog
reload(voa)

#NOTE:  01  set character name and path for config files
target_character = "Mint"#name of rig root without namespace
#NOTE:  02  config_path MUST prefix with r if it contains backslashes
config_path = r"Z:\0_p4v\PotionomicsSourceAssets\Art_sourcefiles\Characters\scenes\Animation\Luna\config"#Z:\0_p4v\PotionomicsSourceAssets\Art_sourcefiles\Characters\scenes\Animation\Luna\config
Asset_Data = vog.AnimAsset(root = pm.ls(target_character,recursive = 1)[0], pose_path = "Z:/0_p4v/PotionomicsSourceAssets/Maya_sourcefiles/PoseLibrary/Mint")

 
sim_group_01 = {#NOTE:  03  make one of these for each chain that needs to be simulated
    "targets" : [u'Mint_braid_04_CTL', u'Mint_braid_06_CTL', u'Mint_braid_08_CTL', u'Mint_braid_10_CTL'],
    "config" : 'antenna_fluid_simple.cfg',#name of config file with simulation settings
    "sim_type" : "chain_simple"#chain, point, or chain_simple to indicate which key and SimulatorModule to use
}
sim_group_02 = {#NOTE:  03  make one of these for each chain that needs to be simulated
    "targets" : [u'Mint_MainHipC', u'Mint_satchel_01_CTL', u'Mint_satchel_02_CTL', u'Mint_satchel_03_CTL'],
    "config" : 'antenna_stiff_simple.cfg',#name of config file with simulation settings
    "sim_type" : "chain_simple"#chain, point, or chain_simple to indicate which key and SimulatorModule to use
}

#NOTE:  04  list all sim objects in sim_list
sim_list = [sim_group_02, sim_group_02]#, sim_group_03]#, sim_group_04, sim_group_05, sim_group_06, sim_group_07, sim_group_08, sim_group_09]

priority_list = []
all_sim_targets = []
for group in sim_list:
    all_sim_targets.extend(pm.ls(group['targets'], recursive = True))
    priority_list.append(group['targets'][0])
    
print priority_list
print all_sim_targets


#sets anim timeline buffer
pm.playbackOptions(min = Asset_Data.start_frame - 10, max = Asset_Data.end_frame + 10)

anim_layers = voa.get_anim_layers()
if len(anim_layers) > 1:
    #pm.select(all_sim_targets)
    layer_targets = voa.get_layer_objects(anim_layer = None)
    pm.bakeResults(layer_targets, removeBakedAttributeFromLayer = True, time=(0,65), sac=True, resolveWithoutLayer = anim_layers)
    pm.delete(anim_layers)
sim_layer = voa.create_anim_layer(anim_layer_name = "SimulationAnimLayer", objects = all_sim_targets)
#voa.add_objects_to_anim_layer(objects = all_sim_targets, anim_layer = sim_layer)
#pm.animLayer(query=True, root=True).setLock()


for entry in sim_list:
    voa.select_anim_layer(anim_layer = sim_layer)
    #pm.select(voa.get_layer_objects(anim_layer = sim_layer))
    sim_targets = [target.name() for target in pm.ls(entry['targets'], recursive = True)]
    pm.select(sim_targets, replace = True)
    print('simulation targets %s' %(sim_targets))
    config_file = os.path.normpath(os.path.join(config_path, entry["config"])).replace('\\', '/')#replace with data from sim_dict
    #testty = BroTools.core.config_parser.BroConfig(config_file)
    #sim_dict = testty.__dict__
    print('entry sim type %s' %(entry['sim_type']))
    #values = testty.__dict__[entry['sim_type']].__dict__
    broConfig_parser = BroTools.core.config_parser.BroConfig(config_file)
    sim_properties = broConfig_parser.__dict__[entry['sim_type']].__dict__
    sim_parameters = {#must be here to hold sim properties
                        "preserveAnimation" : True,
                        "simulationProperties" : sim_properties,
                        "autoShiftDistance" : True,
                        "collisionMode" : False,
                        "dontRefresh" : True,
                        "skipControls" : 0,
                        "skipFrames" : 0,
                        "aimRotation" : False,
                        "matchPositions" : True,
                        "debugMode" : True,
                        "deleteNucleus" : True,
                        "up" : [0, 1, 0],
                        "axis" : [1, 0, 0]
                        }
    #running simulation
    if entry['sim_type'] == 'chain_simple':
        #print(entry['sim_type'])
        import BroTools.BroDynamics.modules.chain_simple
        simulator = BroTools.BroDynamics.modules.chain_simple.SimulatorModule()
    elif entry['sim_type'] == 'chain':
        print(entry['sim_type'])
        import BroTools.BroDynamics.modules.chain
        simulator = BroTools.BroDynamics.modules.chain.SimulatorModule()
    elif entry['sim_type'] == 'point':
        #print(entry['sim_type'])
        import BroTools.BroDynamics.modules.point
        simulator = BroTools.BroDynamics.modules.point.SimulatorModule()
    else:
        pm.warning('sim type not found')
    #objects = cmds.ls(sl=1)#replace with sim target
    simulator.run(sim_targets, **sim_parameters)

#TODO:  poseCorrectLayer.setKeyframe(weight), add controls, key pose corrections
stuff = voa.get_layer_objects(anim_layer = None)
voa.pose_correct_layer(all_sim_targets, priority_list, Asset_Data)
pm.playbackOptions(min = Asset_Data.start_frame, max = Asset_Data.end_frame)


