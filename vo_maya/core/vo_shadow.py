"""
    Functions for making proxy geometry across rig transforms. Mostly used for guiding modelers
    to avoid stupid bullshit that's structurally unsound for rigging.
"""

import pymel.core as pm
import vo_general as general


class ShadowMaterial():
    def __init__(self,
            color,
            target
            ):
        self.material_reference = pm.createNode("phongE")
        material_reference.setAttr(color = color)
    
class CharacterMakeup():#....   class to create a bunch of materials on a character
    def __init__(self,
            targets
            ):
        self.base_material = pm.createNode("phongE")
        self.start_color = self.base_material.color#TODO    check if this works
    def generate_colors(start_color):#.... make the color palette based on starting color
        return
    def rank_surfaces():#....   rank surfaces by a rank of volume + poly count
        #higher density gives a lighter color
        #largest combined volume and poly count decides order of hue from start_color
        return ordered_surfaces
    def make_materials():
        return
    def get_materials():
        return

#TODO....   alter this to actually work with an rgb input instead of single float number
def hue_shift(rgb, type = ''):
    """
    @param rgb: rgb param is deceptive, it's actually just a single float instead of a tuple
    """
    if type == 'cool':
        #bring it closer to 180
        return
    elif type == 'warm':
        #bring it closer to 0 or 360
        return
    elif type == 'ambient':#dark complementary color
        if rgb > 180:
            ambient = 360-rgb
        else:
            ambient = 360-rgb
        #set ambient 
        return ambient
    else:#.... return complement
        if rgb > 180:
            complement = 360-rgb
        else:
            complement = 360-rgb
        return complement

"""
color_value = (1, 1, 0.0)
base_material.setColor(col = color_value)

base_material.setAmbientColor(ambient_color = color_value)
#https://stackoverflow.com/questions/24852345/hsv-to-rgb-color-conversion

"""
#hue_shift(rgb=41.539)

#TODO....   once hue shift works, make a version that creates color nodes so it all changes dynamically


def select_by_material(materialName):
    
    #materialName = "lambert1"
    shading_group = pm.listConnections(materialName, type="shadingEngine")
    mesh_components = pm.sets(shading_group, q=True)
    pm.select(mesh_components)

#TODO   update to utilize select_by_material()
def get_meshes_using_materials(material_list):
    meshes = list()

    for material in material_list:
        shading_engine = pm.listConnections(material, type='shadingEngine')[0]
        meshes.extend(shading_engine.listConnections(type='mesh'))

    # Swap to a set to force a single instance, then back to a list
    meshes = list(set(meshes))
    return meshes

#TODO   make image path optional
#TODO   change material to phongE and set parameters
def create_material(image_path):
    """
    Function to create a new material using the supplied image

    Args:
        image_path: path on disk to the image to use
    """

    # Create a file node and assign the texture
    file_node = pm.createNode("file")
    file_node.fileTextureName.set(image_path)

    # Create a blank blinn material
    material = pm.createNode("blinn")

    # Create a blank shading group
    sg = pm.sets(renderable=True, noSurfaceShader=True, empty=True)

    # Connect the output from the file node to the input on the material
    pm.connectAttr( (file_node + ".outColor"), (material + ".color"), force=True)

    # Connect the output of the material to the input on the shading group
    pm.connectAttr( (material + ".outColor"), (sg + ".surfaceShader"), force=True)

    # Return our new material instance
    return material

#TODO   turn this into a class
def shadow_primitive(primitive='cylinder'):
    """
    Creates a primitive at selected transforms with .shadow tag
    """

    if primitive == 'cylinder':

        shadow_targets = pm.ls(sl=1)
        shadow_start = shadow_targets[0]
        shadow_start_location = pm.xform(shadow_start, q=True, ws=True, rotatePivot=True)

        if shadow_start.hasAttr('radius'):
            start_radius_attr = str(shadow_start) + '.radius'
            shadow_radius = shadow_start.radius.get()
        else:
            shadow_radius = 5
        #shadow_sphere = pm.sphere(radius = shadow_start_radius)
        shadow_cylinder = pm.cylinder(radius = shadow_radius, heightRatio = 2, axis = [1,0,0], sections = 12, constructionHistory = 1)

        if len(shadow_targets) > 1:
            shadow_end = shadow_targets[-1]
            shadow_end_location = pm.xform(shadow_end, q=True, ws=True, rotatePivot=True)
            shadow_height_ratio = general.meta_children(shadow_start_location,shadow_end_location)
            shadow_cylinder[0].rotatePivot.set([-0.5*shadow_height_ratio,0,0])
            shadow_cylinder[0].scalePivot.set([-0.5*shadow_height_ratio,0,0])
            shadow_cylinder[1].heightRatio.set(shadow_height_ratio)
        else:
            pass
        pm.matchTransform(shadow_cylinder, shadow_start, scale = False)
    elif primitive == 'sphere':
        shadow_targets = pm.ls(sl=1)
        shadow_start = shadow_targets[0]
        if len(shadow_targets) > 1:
            shadow_end = shadow_targets[-1]
        else:
            pass
        shadow_start_location = pm.xform(shadow_start, q=True, ws=True, rotatePivot=True)

        if shadow_start.hasAttr('radius'):
            start_radius_attr = str(shadow_start) + '.radius'
            shadow_start_radius = shadow_start.radius.get()
        else:
            shadow_start_radius = 5
        shadow_sphere = pm.sphere(radius = shadow_start_radius)
        pm.matchTransform(shadow_sphere, shadow_start, scale = False)
    else:
        pm.warning("invalid primitive value, accepted values are 'sphere' and 'cylinder'")
        return False

def extrude_band(name, targets, profile = 'segment'):
    path_curve = general.curve_on_transforms(name = name, transforms = targets)[0]
    profile_curve = general.create_object(name = (name+'_CRV'), objType = profile, radius = 1.0)
    output = pm.extrude(profile_curve, path_curve, et = 2, fixedPath = True,useComponentPivot = 1, name = name)[0]
    #pm.extrude(pm.ls(sl=1)[0], pm.ls(sl=1)[1], et = 2, fixedPath = True,useComponentPivot = 1)

    return output

def loft_band(name, targets, profile = 'segment', parent = False):
    #path_curve = general.curve_on_transforms(name = name, transforms = targets)
    loft_targets = range(len(targets))
    profile_curve = general.create_object(name = (name+'_CRV'), objType = profile, radius = 1.0)
    for index in range(len(targets)):
        loft_targets[index] = profile_curve.duplicate()[0]
        pm.matchTransform(loft_targets[index],targets[index])
        if parent:
            loft_targets[index] | targets[index]
    output = pm.loft(loft_targets, sectionSpans = 2, name = 'extrude_band')
    #pm.extrude(pm.ls(sl=1)[0], pm.ls(sl=1)[1], et = 2, fixedPath = True,useComponentPivot = 1)

    return output



