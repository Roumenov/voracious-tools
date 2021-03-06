"""
    procs for managing deformers, mostly skinCluster and blendShape
"""


import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import Red9.core.Red9_Meta as r9Meta


def get_blendShape(target):
    """Get blendshape of target."""
    if (pm.nodeType(target.getShape()) in ["mesh", "nurbsSurface", "nurbsCurve"]):
        blendShape = pm.listHistory(target, type="blendShape")[0]
    else:
        pm.warning("target doesn't appear to be a mesh, nurbsSurface, or nurbsCurve")
        return False
    return blendShape

def add_blendShape(new_shape, blend_mesh):
    """
    Add blendshape target to mesh with existing blendShape deformer
    Parameters
    ----------
    new_shape : mesh, nurbsSurface, nurbsCurve
    blend_mesh : mesh, nurbsSurface, nurbsCurve
    """
    blendShape_node = get_blendShape(blend_mesh)
    new_index = blendShape_node.numWeights()
    #print(new_index)
    try:
        pm.blendShape(blendShape_node, edit=True, target=(blend_mesh, new_index, new_shape, 1.0))
    except:
        pm.warning('not working')
    return


####====    USAGE   ====####

#first selected is the new shape, second is the target mesh with a blendshape to add to
#new_shape, blend_mesh = pm.ls(sl=1)[0:2]
#add_blendShape(new_shape, blend_mesh)


def copy_blendshape_params(blendshape, target):
    """proc for making connection attrs for blendShape's weight params"""
    target_node = r9Meta.MetaClass(target.name())
    
    shape_params = pm.listAttr(blendshape.weight, multi = True)
    for param in shape_params:
        target_node.addAttr(param,0.0)
        target_param = '.'.join((target.name(), param))
        blendshape.connectAttr(param, target_param)
    return
#copy_blendshape_params(blendshape,target)


def check_skincluster(target):
    if target.connections(type = 'skinCluster'):
        return True
    else:
        return False


#PURPOSE            check if given joint is skinned
#PROCEDURE            cycle through connections and find skinCluster nodes
#PRESUMPTIONS        arg is a single object of type joint
def check_skincluster2(jointObject):
    for node in jointObject.connections():
        if node.nodeType() == 'skinCluster':
            return True
        else:
            return False


def list_influences(mesh):
	#test_thing.listHistory(type = 'skinCluster')
    return pm.skinCluster(mesh.history(type = 'skinCluster'),query=True,inf=True)


def auto_copy_weights(source_mesh,target_mesh, surface_association = 'closestComponent'):
    """
    @param surface_association: 'closestPoint', 'rayCast', or 'closestComponent'
    
    auto_copy_weights(source_mesh = pm.ls(sl=1)[0],target_mesh = pm.ls(sl=1)[1], surface_association = 'closestComponent')
    auto_copy_weights(source_mesh = pm.ls(sl=1)[0],target_mesh = pm.ls(sl=1)[1], surface_association = 'closestPoint')
    auto_copy_weights(source_mesh = pm.ls(sl=1)[0],target_mesh = pm.ls(sl=1)[1], surface_association = 'rayCast')
    """
    #joints = pm.skinCluster(source_mesh.history(type = 'skinCluster'),query=True,inf=True)
    pm.select(cl=1) 
    source_cluster = source_mesh.history(type = 'skinCluster')[0]
    joints = pm.skinCluster(source_cluster,query=True,inf=True)
    max_influences = pm.skinCluster(source_mesh.history(type = 'skinCluster'), query = True, maximumInfluences = True)
    try:
        target_cluster = target_mesh.history(type = 'skinCluster')[0]
    except:
        target_cluster = pm.skinCluster(joints, target_mesh, toSelectedBones = True, bindMethod = 0, normalizeWeights = 1, weightDistribution = 1, maximumInfluences = max_influences, obeyMaxInfluences = True, skinMethod = 0, smoothWeights = 0.8, dropoffRate = 2, removeUnusedInfluence = False)
    pm.copySkinWeights(sourceSkin = source_cluster, destinationSkin = target_cluster, noMirror = True, surfaceAssociation = surface_association, influenceAssociation = ('label'), normalize = True)
    
    #pm.skinCluster(target_cluster, removeUnusedInfluence = True, edit = True)
    pm.select(source_mesh,target_mesh)    
    return target_cluster
    #pm.copySkinWeights(sourceSkin = source_cluster,destinationSkin = target_cluster, noMirror = True, surfaceAssociation = 'rayCast', influenceAssociation = ('label'), normalize = True)
    #,'oneToOne','name'
    #copySkinWeights  -noMirror -surfaceAssociation rayCast -influenceAssociation label -influenceAssociation oneToOne -influenceAssociation name -normalize;

    #pm.mel.removeUnusedInfluences(mesh)
    #cmds.file(export_path, exportSelected=True, type="FBX export")




#TODO:     look into using OpenMaya and pymel to see if these operations can be sped up
#TODO:     return new mesh
#PURPOSE:       Combine a bunch of skinned meshes to one shape with one skinCluster attached to all the bones of the source meshes
#PROCEDURE:     Make a list of skin joints, duplicate and group meshes, combine the duplicates, copySkinWeights to combo mesh, delete sources
def combine_skin_mesh(meshName, targets):
    joint_list = []

    if(len(meshName) == 0) or (" " in meshName) or cmds.objExists(meshName):
    	raise TypeError("Invalid name")
    
    for item in targets:       
        item_cluster = mel.eval('findRelatedSkinCluster ' + item)
        if cmds.objExists (item_cluster):
            print item_cluster
        else:
            raise TypeError(item +" Clusters not found")
            
        matrix_array = cmds.getAttr(item_cluster + ".matrix", mi = True)
    
        for item in matrix_array:
            list = cmds.connectionInfo(item_cluster + ".matrix[" + str(item) + "]", sourceFromDestination = True)
            joint = list.split(".")
            joint_list.append(joint[0])
            
    if(len(targets) < 2):
        raise TypeError ('Please Select at least two skinned Meshes')

    elif(len(targets) > 2):
        duplicate = cmds.duplicate (targets)
        #duplicate_offset = cmds.group (duplicate)#....  this looks mega redundant
        combine = cmds.polyUnite (duplicate_offset, name = meshName)
        cmds.delete (combine, ch=True)
        #deleteGrp = cmds.select (cmds.delete (duplicate_offset))
        new_cluster = cmds.skinCluster(joint_list,meshName, n="skinCluster"+meshName, maximumInfluences = 4)
        cmds.select (joint_list, targets, meshName, add= True )
        cmds.copySkinWeights (nm=True, sa ="closestPoint", ia ="closestJoint")
        cmds.delete (targets)
        cmds.select (meshName)
        #mel.eval('removeUnusedInfluences ')
        return 
        
    else:
        raise TypeError ('Somehow len(targets) is between 2 and 2!!')

#selection = cmds.ls(sl=1)
#combine_skin_mesh('skin_mesh', selection)


def CombineSkinnedMeshProc(*args):
    
    selection = cmds.ls(sl=True)
    joint_list = []
    if(len(selection) == 0):
        raise TypeError ('Please Select at least two skinned Meshes')
		
    elif(len(selection) == 1):
        raise TypeError ('Please Select at least two skinned Meshes')	

    textField_obj = cmds.textField( textFieldName, query=True, text=True )
    
    if(len(textField_obj) == 0):
        raise TypeError ('Please Assign a Name')
    if " " in textField_obj:
        raise TypeError("Warning: you are using illegal characters for the name")
    if cmds.objExists(textField_obj):
           raise TypeError("Warning: this name is already in use")
             
    for item in selection:       
        findSkinStart = mel.eval('findRelatedSkinCluster ' + item)
        
        if cmds.objExists (findSkinStart):
            print findSkinStart
                 
        else:
            raise TypeError("Please Select at least two skinned Meshes ") 
            
        matrix_array = cmds.getAttr(findSkinStart + ".matrix", mi = True)
    
        for i in matrix_array:
            list = cmds.connectionInfo(findSkinStart + ".matrix[" + str(i) + "]", sourceFromDestination = True)
            joint = list.split(".")
            joint_list.append(joint[0])         
                    
    if (len(selection) > 0):
            print selection
            for i in range(1):
                duplicateObj = cmds.duplicate (selection)
                createGrp = cmds.group (duplicateObj)        
                combine = cmds.polyUnite (createGrp, name = textField_obj)
                deleteHistory = cmds.delete (combine, ch=True)
                deleteGrp = cmds.select (cmds.delete (createGrp))
                cmds.textField( textFieldName, e=True, text='')   
                newskin = cmds.skinCluster(joint_list,textField_obj, n=textField_obj + "_SKC")
                newSelect = cmds.select (joint_list, selection, textField_obj, add= True )
                transfer = cmds.copySkinWeights (nm=True, sa ="closestPoint", ia ="closestJoint")
                delete = cmds.delete (selection)
                selectnewobj = cmds.select (textField_obj)
                cleanSkinEnd = mel.eval('removeUnusedInfluences ')
                deselect = cmds.select (cl=True)


def SeparateSkinnedMeshProc( *args):
    
    selection = cmds.ls(sl=True)
    
    if(len(selection) == 0):
        raise TypeError ('Please Select a Skinned Mesh')
		
    elif(len(selection) > 1):
        raise TypeError ('Please Select only one Skinned Mesh to separate')	

    textField_obj = cmds.textField( textFieldName, query=True, text=True )
    
    if(len(textField_obj) == 0):
        raise TypeError ('Please Assign a Name')
    
    if " " in textField_obj:
        raise TypeError("Warning: you are using illegal characters for the name")
        
    if cmds.objExists(textField_obj):
           raise TypeError("Warning: this name is already in use")  
    
    
    for item in selection:       
        findSkinStart = mel.eval('findRelatedSkinCluster ' + item)
        
        if cmds.objExists (findSkinStart):
            print findSkinStart
                 
        else:
            raise TypeError("Please Select a Skinned Mesh ")         
    
    if len (selection) > 0:
            print selection
            for i in range(1):
                duplicateObj = cmds.duplicate (selection, name = textField_obj)
                     
                separate = cmds.polySeparate (duplicateObj, name = textField_obj + "NewSkin*", ch=True)
                deleteHistory = cmds.delete (separate, ch=True)

                
                deselect01 = cmds.select (cl=True)
                selectnewmeshes = cmds.select( textField_obj, hi=True)
                deselGrp = cmds.select(textField_obj, d=True)
                givenlist = cmds.ls (sl=True)
                mesh = givenlist
                
                for index in range(len(mesh)):
                    print mesh[index]
                    joints = cmds.skinCluster (item , q=True , inf=True)
                    cmds.textField( textFieldName, e=True, text='')
                    for obj in mesh:
                        findSkinEnd = mel.eval('findRelatedSkinCluster ' + obj)
        
                        if cmds.objExists (findSkinEnd):
                            print findSkinEnd
                        else:
                            newskin = cmds.skinCluster(obj, joints, n=textField_obj + "_SKC")
                            break
                            
                    newSelect = cmds.select (joints, selection, obj , add= True)
                    transfer = cmds.copySkinWeights (nm=True, sa ="closestPoint", ia ="closestJoint")
                    cleanSkinEnd = mel.eval('removeUnusedInfluences ')
                       
                cmds.select (cl=True)
                cmds.delete (selection)
               

class CombineSeparateSkinnedMesh():
    def __init__(self):
        
        global textFieldName
        
        if cmds.window('CombSepSkinMeshWin', exists=True):
           cmds.deleteUI('CombSepSkinMeshWin')
		
        CombSepSkinMeshWin = cmds.window ("CombSepSkinMeshWin", title="Combine Separate Skinned Mesh", widthHeight=(300, 120), s=0)
        cmds.columnLayout(adjustableColumn=True )
        cmds.text( label='Assign Name to New Mesh' )
        textFieldName = cmds.textField()
        spacenoedit = cmds.textField( ed = False)
        cmds.button( label='Combine Skinned Mesh', c=combine_skin_mesh)
        cmds.button( label='Separate Skinned Mesh', c=SeparateSkinnedMeshProc)
        cmds.setParent( '..' )
        cmds.showWindow(CombSepSkinMeshWin)   
        
#CombineSeparateSkinnedMesh()

"""
import maya.cmds as cmds
from skinningTool.skinningTools import SkinningTools as skinTool
#cmds.select(self.skinTool.combineSkinnedMeshes(selection), r=1)
selection = cmds.ls(sl=True)
skin_tool_instance = skinTool()
cmds.select(skin_tool_instance.combineSkinnedMeshes(selection), r=1)
#this call works in that it finds the functions and supplies args
#but the cmds.SkinWeights call seems to be wrong and I don't know how to correct that....
type(skin_tool_instance)
"""