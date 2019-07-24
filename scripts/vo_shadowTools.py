
import pymel.core as pm
import vo_usefulFunctions as uf


#basic methods ::

def select_by_material(materialName):
    
    #materialName = "lambert1"
    shading_group = pm.listConnections(materialName, type="shadingEngine")
    mesh_components = pm.sets(shading_group, q=True)
    pm.select(mesh_components)

def shadow_primitive():
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
        shadow_height_ratio = get_distance(shadow_start_location,shadow_end_location)
        shadow_cylinder[0].rotatePivot.set([-0.5*shadow_height_ratio,0,0])
        shadow_cylinder[0].scalePivot.set([-0.5*shadow_height_ratio,0,0])
        shadow_cylinder[1].heightRatio.set(shadow_height_ratio)
    else:
        pass
    pm.matchTransform(shadow_cylinder, shadow_start, scale = False)




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
    shadow_height_ratio = get_distance(shadow_start_location,shadow_end_location)
    print shadow_height_ratio
    shadow_cylinder[0].rotatePivot.set([-0.5*shadow_height_ratio,0,0])
    shadow_cylinder[0].scalePivot.set([-0.5*shadow_height_ratio,0,0])
    shadow_cylinder[1].heightRatio.set(shadow_height_ratio/shadow_radius)
else:
    pass
pm.matchTransform(shadow_cylinder, shadow_start, scale = False)
aim_object(aimer, target, axis = '+x')


#pm.move(shadow_cylinder, [-1.15381, 1.627506, 0.141238], relative = True, rotatePivotRelative = 1, scalePivotRelative = 1)

print(pm.distanceDimension(startPoint = shadow_start_location, endPoint = shadow_end_location))

#set shadow_length
import math
def get_distance(startPoint, endPoint):
    
    dx = startPoint[0] - endPoint[0]
    dy = startPoint[1] - endPoint[1]
    dz = startPoint[2] - endPoint[2]
    return math.sqrt( dx*dx + dy*dy + dz*dz )