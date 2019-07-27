import pymel.core as pm
import vo_usefulFunctions as uf
reload(uf)

class metaDeformer():
    """
    
    """
    def __init__(
                self,
                target,
                cluster,
                influences,
                mesh,
                name = ''
                ):
        cluster = mesh.history(type = 'skinCluster')[0]
        name = cluster.name()
        """
        target = mesh
        cluster 
        """
    def export_cluster(self,cluster):
        export_name = self.name + '.xml'
        pm.deformerWeights(export_name, ex=True, deformer=cluster.name)
    
    def import_cluster(self):
        pm.deformerWeights(im = True, )
        pass
    def create_cluster(self,influences,mesh):
        
        pass



#http://help.autodesk.com/cloudhelp/2018/CHS/Maya-Tech-Docs/PyMel/generated/functions/pymel.core.animation/pymel.core.animation.deformerWeights.html?highlight=deformerweights
test = pm.ls(sl=1)[0].history(type = 'skinCluster')[0]
print test
print(pm.skinCluster(test,query=True,inf=True))

influences = []
cluster_names = []
source_meshes = pm.ls(sl=1)
file_path = 'Z:/0_p4v/PotionomicsSourceAssets/Art_sourcefiles/Characters/scenes/Rigs/Muktuk/clusters/'

for mesh in source_meshes:
    cluster = mesh.history(type = 'skinCluster')
    export_name = cluster[0].name()
    cluster_names.append(export_name)
    export_name = export_name+'.xml'
    
    #export deformer weights
    pm.deformerWeights(export_name, ex=True, path = file_path, method = 'index', deformer=cluster)
    
    
    #skin_joints = pm.skinCluster(cluster,query=True,inf=True)
    
    influences.append(uf.list_influences(mesh))
    pass

print influences[1]
pm.select(influences[1])
pm.select(influences[1],source_meshes[1])

#rename old joints, name new joints to old name
#delete old skinClusters!!

for index in range(len(source_meshes)):
    destination_mesh = pm.ls(('mesh:'+source_meshes[index].name()))
    
    pm.select(influences[index],destination_mesh, replace = True)
    #name cluster after the old one
    
    new_cluster = pm.skinCluster(name = cluster_names[index], toSelectedBones = True, bindMethod = 0, normalizeWeights = 1, weightDistribution = 1, maximumInfluences = 4, obeyMaxInfluences = True, skinMethod = 0, smoothWeights = 0.8, dropoffRate = 2, removeUnusedInfluence = False)
    
    pass

#delete 

for index in range(len(source_meshes)):
    destination_mesh = pm.ls(('mesh:'+source_meshes[index].name()))[0]
    #pm.select(destination_mesh, replace = True)
    cluster = destination_mesh.history(type = 'skinCluster')[0]
    import_name = cluster.name()+'.xml'
    pm.deformerWeights(import_name, im=True, path = file_path, deformer=cluster)
    

