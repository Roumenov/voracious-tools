import pymel.core as pm
import maya.cmds as cmds
import vo_maya.core.vo_animation as voa

path_components = pm.sceneName().split('/')[0:-1]
path_components.append( 'config' )
config_path = '/'.join(path_components)

anim_layers = voa.get_anim_layers()
type(anim_layers)

start_frame = 1
end_frame = 121
#set timeline preroll
#set timeline postroll

for item in anim_layers:
    print item
    item.setLock()

sim_layer = voa.create_anim_layer("SimulationAnimLayer")

#add target chain to sim layer
#TODO: add considerations for namespace changes....
sim_archetype = {
    "targets" : [u'r:Luna_L_antenna_01_CTL', u'r:Luna_L_antenna_02_CTL', u'r:Luna_L_antenna_03_CTL', u'r:Luna_L_antenna_04_CTL', u'r:Luna_L_antenna_05_CTL', u'r:Luna_L_antenna_06_CTL', u'r:Luna_L_antenna_07_CTL'],
    "config" : '/antenna_stiff_simple.cfg',
    "sim_type" : "chain"#chain, point, or chain_simple to indicate which key and SimulatorModule to use
}

#get config for target chain
config_file = config_path + '/antenna_stiff_simple.cfg'

testty = BroTools.core.config_parser.BroConfig(config_file)
sim_dict = testty.__dict__
values = testty.__dict__['chain_simple'].__dict__

sim_parameters = {#TODO: fill these values from config dict
    "preserveAnimation" : True,
    "simulationProperties" : testty.__dict__['chain_simple'].__dict__,
    "collisionMode" : False,
    "dontRefresh" : False,
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
#TODO: conditions from archetype for 
simulator = BroTools.BroDynamics.modules.chain_simple.SimulatorModule()
objects = cmds.ls(sl=1)
simulator.run(objects, **sim_parameters)



#Z:\0_p4v\PotionomicsSourceAssets\Art_sourcefiles\Characters\scenes\Animation\Luna\config

sim_layer.setKeyframe(weight)
pm.setKeyframe(sim_layer.weight)