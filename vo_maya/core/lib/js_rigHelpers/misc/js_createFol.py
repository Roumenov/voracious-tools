'''


jsObjFol


'''


# Select objects to create follicles based on the locations of, followed by the object
# to create follicles on. Then Run.


import maya.cmds as mc
import maya.mel as mel


def jsObjFol():
    
    sel = mc.ls (sl=True)
    length = len(sel)
    shape = mc.listRelatives (sel[length-1], s = True)
    type = mc.objectType (shape[0])
    
    if type == 'mesh':
    
        for obj in sel:
            
            if obj == sel[-1]:
                pass
            else:
                
                loc = mc.spaceLocator ()[0]
                cnst = mc.parentConstraint (obj, loc)
                mc.delete (cnst)
                
                closest = cmds.createNode ('closestPointOnMesh')
                mc.connectAttr (sel[-1] + '.outMesh', closest + '.inMesh')
                pos = mc.xform (loc, t = True, q = True)
                mc.setAttr (closest + '.inPositionX', pos[0])
                mc.setAttr (closest + '.inPositionY', pos[1])
                mc.setAttr (closest + '.inPositionZ', pos[2])
                
                face = mc.getAttr (closest + '.closestFaceIndex')
                clus = mc.cluster ('%s.f[%s]' %(sel[-1], face))[1]
                loc2 = mc.spaceLocator ()[0]
                cnst = mc.parentConstraint (clus, loc2)
                mc.delete (cnst)
                
                closest2 = cmds.createNode ('closestPointOnMesh')
                mc.connectAttr (sel[-1] + '.outMesh', closest2 + '.inMesh')
                pos2 = mc.xform (loc2, t = True, q = True)
                mc.setAttr (closest2 + '.inPositionX', pos2[0])
                mc.setAttr (closest2 + '.inPositionY', pos2[1])
                mc.setAttr (closest2 + '.inPositionZ', pos2[2])
                
                fol = mc.createNode ("follicle")
                folTrans = mc.listRelatives (fol, type = 'transform', p = True)
                mc.connectAttr (fol + ".outRotate", folTrans[0] + ".rotate")
                mc.connectAttr (fol + ".outTranslate", folTrans[0] + ".translate")
                mc.connectAttr (sel[-1] + '.worldMatrix', fol + '.inputWorldMatrix')
                mc.connectAttr (sel[-1] + '.outMesh', fol + '.inputMesh')
                mc.setAttr(fol + ".simulationMethod", 0)
                
                u = mc.getAttr (closest2 + '.result.parameterU')
                v = mc.getAttr (closest2 + '.result.parameterV')
                mc.setAttr (fol + '.parameterU', u)
                mc.setAttr (fol + '.parameterV', v)
                
                mc.delete (closest, closest2, loc2, loc, clus)


                mc.select (folTrans)
                    
    elif type == 'nurbsSurface':
        
        for obj in sel:
            
            if obj == sel[-1]:
                pass
            else:
                closest = cmds.createNode ('closestPointOnSurface')
                print shape[0], closest
                mc.connectAttr (shape[0] + '.worldSpace', closest + '.inputSurface')
                pos = mc.xform (obj, t = True, q = True)
                mc.setAttr (closest + '.inPositionX', pos[0])
                mc.setAttr (closest + '.inPositionY', pos[1])
                mc.setAttr (closest + '.inPositionZ', pos[2])
                
                fol = mc.createNode ("follicle")
                folTrans = mc.listRelatives (fol, type = 'transform', p = True)
                mc.connectAttr (fol + ".outRotate", folTrans[0] + ".rotate")
                mc.connectAttr (fol + ".outTranslate", folTrans[0] + ".translate")
                mc.connectAttr (shape[0] + '.worldSpace', fol + '.inputSurface')
                mc.setAttr(fol + ".simulationMethod", 0)
                
                u = mc.getAttr (closest + '.result.parameterU')
                v = mc.getAttr (closest + '.result.parameterV')
                mc.setAttr (fol + '.parameterU', u)
                mc.setAttr (fol + '.parameterV', v)
                
                mc.delete (closest)
                
                if obj not in sel[length - 1]:
                    mc.delete (obj)        


jsObjFol()