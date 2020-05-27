"""
    procs for managing deformers, mostly skinCluster and blendShape
"""


import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm



def create_anim_layer(anim_layer_name):
    base_anim_layer = pm.animLayer(query=True, root=True)

    if (base_anim_layer != None):
        child_layers = pm.animLayer(base_anim_layer, query=True, children=True)

        if (len(child_layers) > 0) :
            if anim_layer_name in child_layers:
                pm.warning('Layer ' + anim_layer_name + ' already exists')
            else:
                new_anim_layer = pm.animLayer(anim_layer_name)
        else:
            pm.warning('weird shit happened')
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