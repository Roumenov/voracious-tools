
"""
    function wrappers for shelf buttons
    typically this means a version that feeds the selection into the arguments
    largely this is to simplify shelf editing for artists and allow them to 
    more easily batch operations with saved selections.

    TODO: add procs for building shelves, not sure how to copy shelves while maya is running, though
"""

import pymel.core as pm
import vo_meta as meta
import vo_general as general
import vo_shadow as shadow
import vo_controls as controls
import vo_ribbons as ribbons


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
    def method_1(self,args):
        self.function(args)


def meta_tag_wrapper():
    for target in pm.ls(sl=1):
        meta.meta_tag(target)


def object_at_selection(name = '', objType = '', radius = 1.0):
    output = []
    if len(pm.ls(sl=1)):
        for target in pm.ls(sl=1):
            new_object = general.create_object(name = name, objType = objType, radius = 1.0)
            output.append(new_object)
            pm.matchTransform(new_object, target, pos = True, rot = True, scale = False)
    else:
        output = general.create_object(name = objType+'_00', objType = objType, radius = 1.0)
    pm.select(output, r=1)
    return output

#TODO: deprecate
def nest_transform(name, action = 'child', transformObj = 'locator', transformRadius = 1.0):
    for item in pm.ls(sl=1):
        general.nest_transform(name = name, action = action, target = item, transformObj = 'locator', transformRadius = 1.0)

#TODO: deprecate
def object_under_selection(name = '', objType = '', radius = 1.0):
    output = []
    if len(pm.ls(sl=1)):
        for target in pm.ls(sl=1):
            new_object = general.create_object(name = name, objType = objType, radius = 1.0)
            output.append(new_object)
            pm.matchTransform(new_object, target, pos = True, rot = True, scale = False)
            target | new_object
    else:
        output = general.create_object(name = name, objType = objType, radius = 1.0)
    pm.select(output, r=1)
    return output


def object_at_select_verts(name='', objType='', radius = 1.0):
    selection = pm.ls(sl=1, flatten = True)
    #vertices = pm.ls(pm.polyListComponentConversion(selection, toVertex=True), flatten=True, orderedSelection=True)
    new_object = general.object_on_vertices(selection, name = name, objType = objType, radius = 1.0)
    pm.select(new_object, r=1)
    return new_object


def object_at_vert_subset(vertices, name = '', objType = '', radius = 1.0, subset_len = 1):
    #TODO:      make this function more than just zombie code idea
    #make lists of verts by slicing with increments of subset_len
    output = []
    for subset in pm.ls(sl=1):
        new_object = general.object_on_vertices(vertices, name = '', objType = '', radius = 1.0)
        output.append(new_object)
    pm.select(output, r=1)
    return output


def primitive_at_selection(axis='y', primitive='cube'):
    """
    create primitive at location of each selected item
    @param primitive: takes 'cube', 'cylinder', 'capsule', 'sphere', 'plane', or 'torus'
    @param axis: takes 'x', 'y', 'z', '-x', '-y', '-z'
    """
    output = []
    for item in pm.ls(sl=1):
        name = item.name() + primitive
        primitive_mesh = general.create_primitive(name=name, primitive=primitive, axis=axis)
        pm.matchTransform(primitive_mesh, item, pos = True, rot = True, scale = False)
        output.append(primitive_mesh)
    pm.select(output, r=1)
    return output


def primitive_at_select_verts(name='cube', primitive='cube', axis='y', radius = 1.0):
    selection = pm.ls(sl=1, flatten = True)
    new_object = general.primitive_on_vertices(selection, name = name, primitive = primitive, radius = 1.0)
    pm.select(new_object, r=1)
    return new_object


def make_follicle():
    ribbons.create_follicle(target = pm.ls(sl=1)[0], uPos = 0.5, vPos = 0.5)


def make_follicle_row():
    segment_input = general.prompt_string(promptTitle = 'Segments', promptMessage = 'Enter number of segments')
    ribbons.create_follicle_row(target = pm.ls(sl=1)[0], segments = int(segment_input))


def make_follicle_column():
    segment_input = general.prompt_string(promptTitle = 'Segments', promptMessage = 'Enter number of segments')
    ribbons.create_follicle_row(target = pm.ls(sl=1)[0], segments = int(segment_input), uvDirection = 'v')


def make_follicle_grid():
    segment_input = general.prompt_string(promptTitle = 'Segments', promptMessage = 'Enter number of segments')
    row_input = general.prompt_string(promptTitle = 'Rows', promptMessage = 'Enter number of rows')
    ribbons.create_follicle_grid(target = pm.ls(sl=1)[0], segments = int(segment_input), rows = int(row_input), offset = 0.5, uvDirection = 'u', uvDefault = 0.5)


def make_super_ribbon():
    #build_auto_ribbon(ribbon_name, drivers, segments=5, rows=3, offset=0.5, uvDirection='u', uvDefault=0.5)
    ribbon_name = general.prompt_string(promptTitle = 'Ribbon Name', promptMessage = 'Enter ribbon name')
    ribbon_GRP, driver_GRP, follicles = ribbons.build_auto_ribbon(ribbon_name = ribbon_name, drivers = pm.ls(sl=1))
    return ribbon_GRP, driver_GRP, follicles
    #build_ribbon(ribbon_name, drivers, segments=5, rows=3, offset=0.5, uvDirection='u', uvDefault=0.5)

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




"""
===============        RIG OPERATIONS      ===============

"""

def create_control(offset = False):
    control_list = []

    for item in pm.ls(sl = True):
        current_control = controls.Control(target=item, name = item.stripNamespace())
        control_object = current_control.control_object

        #insert offset
        control_list.append(control_object)
    pm.select(control_list)
    return control_list


def create_chain(offset = False):

    object_list= pm.ls(sl = True)
    control_list = create_control()

    controls.chain_controls(control_list)

    pm.select(control_list)

