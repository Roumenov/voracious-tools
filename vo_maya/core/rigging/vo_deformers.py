"""
    procs for managing deformers, mostly skinCluster and blendShape

"""


import maya.cmds as cmds
import maya.mel as mel


#TODO:     look into using OpenMaya and pymel to see if these operations can be sped up
#TODO:      add args to return skincluster or mesh, as well as preserving source objects
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
        duplicate_offset = cmds.group (duplicate)#....  this looks mega redundant
        combine = cmds.polyUnite (duplicate_offset, name = meshName)
        cmds.delete (combine, ch=True)
        deleteGrp = cmds.select (cmds.delete (duplicate_offset))
        new_cluster = cmds.skinCluster(joint_list,meshName, n="skinCluster"+meshName)
        cmds.select (joint_list, targets, meshName, add= True )
        cmds.copySkinWeights (nm=True, sa ="closestPoint", ia ="closestJoint")
        cmds.delete (targets)
        cmds.select (meshName)
        mel.eval('removeUnusedInfluences ')
        return 
        
    else:
        raise TypeError ('Somehow len(targets) is between 2 and 2!!')

#selection = cmds.ls(sl=1)
#combine_skin_mesh('skin_mesh', selection)



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
