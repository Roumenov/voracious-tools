
"""
    function wrappers for shelf buttons
    typically this means a version that feeds the selection into the arguments
    largely this is to simplify shelf editing for artists and allow them to 
    more easily batch operations with saved selections.

    TODO: add procs for building shelves, not sure how to copy shelves while maya is running, though
"""



import pymel.core as pm
import vo_meta
import vo_general
#import vo-maya.core.vo_general as uf
#reload(uf)


#maybe use class to define parameters needed in button
#then use methods to create usages with that function
#when building shelves, takes methods after 1st and makes them into popup commands

class shelf_wrapper():
    def __init__(self,
                function,
                name,
                icon):
        self.name = name
        self.function = function
        self.icon = icon#TODO make default icon path that goes here
    def method_1(args):
        self.function(args)


def meta_tag_wrapper():
    for target in pm.ls(sl=1):
        vo_meta.meta_tag(target)


def object_at_selection(objName = '', objType = '', radius = 1.0):
    output = []
    for target in pm.ls(sl=1):
        new_object = create_object(objName = objName, objType = objType, radius = 1.0)
        output.append(new_object)
        pm.matchTransform(new_object, target, pos = True, rot = True, scale = False)
    pm.select(output, r=1)
    return output

def object_at_select_verts(object_name='', object_type='', radius = 1.0):
    output = []
    for target in pm.ls(sl=1):
        new_object = create_on_vertex(vertices, objName = '', objType = '', radius = 1.0)
        output.append(new_object)
    pm.select(output, r=1)
    return output

def create_at_vert_subset(vertices, objName = '', objType = '', radius = 1.0, subset_len = 1):
    #make lists of verts by slicing with increments of subset_len
    output = []
    for subset in pm.ls(sl=1):
        new_object = create_on_vertex(vertices, objName = '', objType = '', radius = 1.0)
        output.append(new_object)
    pm.select(output, r=1)
    return output

def primitive_at_selection(axis='y', primitive='cube', ):
    """
    @param primitive: takes 'cube', 'cylinder', 'capsule', 'sphere', 'plane', or 'torus'
    """
    axis_coordinates = {'x' : [1, 0, 0], 'y' : [0, 1, 0], 'z' : [0, 0, 1], '-x' : [-1, 0, 0], '-y' : [0, -1, 0], '-z' : [0, 0, -1]}
    output = []
    for item in pm.ls(sl=1):
        if primitive == 'cube':
            primitive_mesh = pm.polyCube()
        elif primitive == 'cylinder':
            primitive_mesh = pm.polyCylinder(axis=axis_coordinates[axis], radius=1, height=2,
                roundCap=False, subdivisionsX=12, subdivisionsY=1, subdivisionsZ=0)
        elif primitive == 'capsule':
            primitive_mesh = pm.polyCylinder(axis=axis_coordinates[axis], radius=1, height=2,
                roundCap = True, subdivisionsX=12, subdivisionsY=4, subdivisionsZ=4)
        elif primitive == 'sphere':
            primitive_mesh = pm.polySphere(axis=axis_coordinates['-x'], radius = 1, subdivisionsX=12, subdivisionsY=8)
        elif primitive == 'plane':
            primitive_mesh = pm.polyPlane(axis=axis_coordinates[axis], height = 2.0, width = 2.0, subdivisionsX=1, subdivisionsY=1)
        elif primitive == 'torus':
            primitive_mesh = pm.polyTorus(axis=axis_coordinates[axis],
                radius=1, sectionRadius=0.5, subdivisionsX=12, subdivisionsY=8)
        elif primitive == 'cone':
            primitive_mesh = pm.polyCone(axis=axis_coordinates[axis], radius=1, height=2,
                roundCap=False, subdivisionsX=12, subdivisionsY=1, subdivisionsZ=0)
        else:
            primitive_mesh = pm.polyCube(height = 1, width=1, subdivisionsX=0, subdivisionsY=0, subdivisionsZ=0)
        pm.matchTransform(primitive_mesh, target, pos = True, rot = True, scale = False)
        output.append(primitive_mesh)
    pm.select(output, r=1)
    return output

def showPrimitiveWindow():
    name = 'primitiveWindow'
    if pm.window(name, query=True, exists=True):
        pm.deleteUI(name)
    pm.window(name)
    pm.showWindow()

    row = pm.rowLayout(numberOfColumns=2)
    column = pm.columnLayout(parent = row)
    primitive_frame = pm.frameLayout(label="choose primitive")

    pm.columnLayout(parent = primitive_frame)
    pm.radioCollection("primitiveTypes")
    pm.radioButton(label='cube', select = True)
    pm.radioButton(label='cylinder')
    pm.radioButton(label='capsule')
    pm.radioButton(label='sphere')
    pm.radioButton(label='plane')
    pm.radioButton(label='torus')
    pm.radioButton(label='cone')

    axis_frame = pm.frameLayout(label="choose axis")
    pm.columnLayout()
    pm.radioCollection("axis")
    pm.radioButton(label='x')
    pm.radioButton(label='y', select = True)
    pm.radioButton(label='z')

    pm.setParent(column)
    pm.rowLayout(numberOfColumns=1)
    pm.button(label='create')

