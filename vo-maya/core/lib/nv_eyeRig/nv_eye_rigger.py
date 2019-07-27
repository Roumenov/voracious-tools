##
## NV Eye Rigger
## www.nielsvaes.be
## nielsvaes+nv_eye_rigger@gmail.com
##
## Make sure you select the points on the upper and lower eye lid in the same order
## e.g.: if the first vertex you select on the upper eye lid is on the corner nearest to the nose,
##       make sure that the first vertex you select for the lower eye lid is also the vertex on the corner
##       nearest to the nose
##

import os

import pymel.core as pm
from maya import OpenMayaUI as omui
# from maya import OpenMaya
import math

try:
    # Maya 2017 and up
    from PySide2.QtCore import *
    from PySide2.QtUiTools import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance
except ImportError:
    # Older versions of Maya
    from PySide.QtUiTools import *
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
    from shiboken import wrapInstance


class EyeRiggerWindow(QMainWindow):
    def __init__(self):
        # The script will try to find itself in your home/maya/Scripts folder
        # It needs to be in a folder called EyeRig
        self.SCRIPT_LOCATION = os.path.join(os.environ['HOME'], "maya", "Scripts", "EyeRig")

        # If you want to use it script from another location, comment out the line above and uncomment the line below
        # Change the path to the location where you put the EyeRig folder

        #self.SCRIPT_LOCATION = r"T:/Tools/Maya/PythonScript/EyeRig"


        self.ui = None

        self.lid_vertices = []
        self.lower_lid_vertices = []

        self.head_joint = None
        self.head_skin = None
        self.head_controller = None

        self.eyelid_high_res_curve = None
        self.eyelid_low_res_curve = None
        self.joint_radius = 0.03

        self.center_eye_position = None
        self.side_prefix = None
        self.up_down_prefix = None

        self.do_not_touch_group = None

        # make sure selection order is tracked, why this is not on by default is beyond me...
        pm.selectPref(trackSelectionOrder=True)

        self.build_ui()

    def build_ui(self):
        QMainWindow.__init__(self)

        mayaMainWindowPtr = omui.MQtUtil.mainWindow()
        mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)

        for each in mayaMainWindow.findChildren(QMainWindow):
            if each.objectName() == "window_nv_eye_rigger":
                each.deleteLater()

        loader = QUiLoader()
        self.ui = loader.load(os.path.join(self.SCRIPT_LOCATION, 'nv_eye_rigger.ui'), parentWidget=mayaMainWindow)

        self.ui.btn_set_lid_points.clicked.connect(self.set_lid_points)
        self.ui.btn_set_center_eye.clicked.connect(self.set_center_eye)
        self.ui.btn_set_head_joint.clicked.connect(self.set_head_joint)
        self.ui.btn_set_head_mesh.clicked.connect(self.set_head_mesh)
        self.ui.btn_set_head_controller.clicked.connect(self.set_head_controller)

        self.ui.btn_build_phase_1.clicked.connect(self.trigger_phase_1)

        self.ui.btn_build_phase_2.clicked.connect(self.build_phase_2)

        self.ui.show()

    def set_lid_points(self):
        selection = pm.ls(selection=True, flatten=True)
        self.lid_vertices = pm.ls(pm.polyListComponentConversion(selection, toVertex=True), flatten=True,
                                  orderedSelection=True)

        if len(self.lid_vertices) > 0:
            self.ui.lbl_lid_points_set.setText("Points set: %s" % len(self.lid_vertices))

    def set_center_eye(self):
        if len(pm.selected()) > 0:
            self.center_eye_position = pm.selected()[0].getTranslation(worldSpace=True)
            self.ui.lbl_center_eye.setText("Center eye: %s" % pm.selected()[0].name())

            print self.center_eye_position

    def set_head_joint(self):
        if len(pm.selected()) > 0:
            self.head_joint = pm.selected()[0]
            self.ui.lbl_head_joint.setText("Head joint: %s" % pm.selected()[0].name())

    def set_head_mesh(self):
        #don't really care about the mesh, just need the skin cluster attached to it
        if len(pm.selected()) > 0:
            self.head_skin = pm.mel.eval('findRelatedSkinCluster %s' % pm.selected()[0].name())
            self.ui.lbl_head_mesh.setText("Head mesh: %s" % pm.selected()[0].name())

    def set_head_controller(self):
        if len(pm.selected()) > 0:
            self.head_controller = pm.selected()[0]
            self.ui.lbl_head_controller.setText("Head controller: %s" % pm.selected()[0].name())

    def trigger_phase_1(self):
        if self.build_phase_1() == "success":
            self.reset()

    def build_phase_1(self):
        self.side_prefix = str(self.ui.cb_side_prefix.currentText())
        self.up_down_prefix = str(self.ui.cb_up_down_prefix.currentText())

        self.joint_radius = float(self.ui.spin_joint_size.value())

        if self.center_eye_position is None:
            self.show_warning("Make sure you've set an object that's the center of the eye!")
            return

        if len(self.lid_vertices) == 0:
            self.show_warning("Make sure you've set the points for the eyelid!")
            return

        if self.head_joint is None:
            self.show_warning("Make sure you've set the head joint!")
            return

        if self.head_skin is None:
            self.show_warning("Make sure you've set the head mesh!")
            return

        if pm.objExists("%s_%s_lid_aim_locator_group" % (self.side_prefix, self.up_down_prefix)):
            self.show_warning("Check your side and up/down prefix, this already exists in the scene!")
            return


        # create the joint and locator groups
        pm.select(None)
        lid_aim_locator_group = pm.PyNode(
            pm.group(name="%s_%s_lid_aim_locator_group" % (self.side_prefix, self.up_down_prefix)))
        pm.select(None)

        lid_aim_locator_group.setTranslation(self.center_eye_position, worldSpace=True)
        pm.makeIdentity(lid_aim_locator_group, translate=True)

        # make a list we can append the positions of every vertex to, this list is used to build the high res curve
        vertex_position_list = []

        # make a list to add the aim locators to, so we can iterate over this list when we need to connect the locators to the high res curve
        aim_locator_list = []

        # build the locators and joints at the position of every vertex
        index = 1
        for vertex in self.lid_vertices:
            vertex_position = pm.xform(vertex, query=True, worldSpace=True, translation=True)
            vertex_position_list.append(vertex_position)

            skin_joint = pm.joint(name="%s_%s_eyelid_skin_joint_%02d" % (self.side_prefix, self.up_down_prefix, index),
                                  position=vertex_position, radius=self.joint_radius)
            pm.select(None)
            center_joint = pm.joint(
                name="%s_%s_eyelid_center_joint_%02d" % (self.side_prefix, self.up_down_prefix, index),
                position=self.center_eye_position, radius=self.joint_radius)

            pm.parent(skin_joint, center_joint)
            self.add_joint_to_skin(skin_joint, self.head_skin)
            pm.joint(center_joint, edit=True, orientJoint="xyz", secondaryAxisOrient="yup", children=True,
                     zeroScaleOrient=True)

            pm.parent(center_joint, self.head_joint)
            pm.select(None)

            aim_locator = pm.spaceLocator(absolute=True, name="%s_%s_eyelid_aim_locator_%02d" % (self.side_prefix, self.up_down_prefix, index))
            aim_locator.translate.set(vertex_position)
            aim_locator.centerPivots()
            aim_locator_shape = pm.listRelatives(shapes=True)[0]
            aim_locator_shape.localScaleX.set(self.joint_radius)
            aim_locator_shape.localScaleY.set(self.joint_radius)
            aim_locator_shape.localScaleZ.set(self.joint_radius)

            aim_locator_list.append(aim_locator)
            pm.parent(aim_locator, lid_aim_locator_group)

            pm.aimConstraint(aim_locator, center_joint, maintainOffset=True, weight=1, aimVector=(1, 0, 0),
                             upVector=(0, 1, 0), worldUpType="scene")

            index += 1

        # build the high res curve
        eyelid_high_res_curve = pm.curve(name="%s_%s_eyelid_high_res_curve" % (self.side_prefix, self.up_down_prefix),
                                         point=vertex_position_list, degree=1)
        self.add_attribute(eyelid_high_res_curve, "eyelidCurve", "%s_%s_high" % (self.side_prefix, self.up_down_prefix))
        eyelid_high_res_curve_shape = pm.listRelatives(eyelid_high_res_curve, shapes=True)[0]
        self.set_shape_node_color(eyelid_high_res_curve_shape, (1, 1, 0))
        eyelid_high_res_curve.centerPivots()

        # build the low res curve
        eyelid_low_res_curve = pm.duplicate(eyelid_high_res_curve, name="%s_%s_eyelid_low_res_curve" % (self.side_prefix, self.up_down_prefix))[0]
        pm.displaySmoothness(eyelid_low_res_curve, divisionsU = 3, divisionsV = 3, pointsWire = 16)
        pm.rebuildCurve(eyelid_low_res_curve, degree = 3, endKnots = True, spans = 2, keepRange = 1, replaceOriginal = True, rebuildType = 0)
        eyelid_low_res_curve.eyelidCurve.set("%s_%s_low" % (self.side_prefix, self.up_down_prefix))

        eyelid_low_res_curve_shape = pm.listRelatives(eyelid_low_res_curve, shapes=True)[0]
        self.set_shape_node_color(eyelid_low_res_curve_shape, (0, 0, 1))
        eyelid_low_res_curve.centerPivots()

        # parent the curves in their group
        if not pm.objExists("%s_eyelid_deformer_curve_group" % self.side_prefix):
            eyelid_deformer_curve_group = pm.group(eyelid_high_res_curve, eyelid_low_res_curve,
                     name="%s_eyelid_deformer_curve_group" % self.side_prefix)
        else:
            eyelid_deformer_curve_group = pm.PyNode("%s_eyelid_deformer_curve_group" % self.side_prefix)
            pm.parent(eyelid_high_res_curve, eyelid_deformer_curve_group)
            pm.parent(eyelid_low_res_curve, eyelid_deformer_curve_group)

        # connect the locators to the high res curve
        for locator in aim_locator_list:
            npoc = pm.createNode("nearestPointOnCurve", name="npoc")
            position = locator.getTranslation(space="world")
            eyelid_high_res_curve_shape.worldSpace >> npoc.inputCurve
            npoc.inPosition.set(position)

            u = npoc.parameter.get()

            pci_node = pm.createNode("pointOnCurveInfo", name=locator.name().replace("locator", "PCI"))
            eyelid_high_res_curve_shape.worldSpace >> pci_node.inputCurve
            pci_node.parameter.set(u)
            pci_node.position >> locator.translate

            pm.delete(npoc)

        if not pm.objExists("DO_NOT_TOUCH"):
            pm.select(None)
            self.do_not_touch_group = pm.PyNode(pm.group(name="DO_NOT_TOUCH"))
        else:
            self.do_not_touch_group = pm.PyNode("DO_NOT_TOUCH")

        pm.parent(eyelid_deformer_curve_group, self.do_not_touch_group)
        pm.parent(lid_aim_locator_group, self.do_not_touch_group)

        self.do_not_touch_group.visibility.set(False)
        #eyelid_deformer_curve_group.visibility.set(False)

        self.show_success_message("Phase 1 built successfully!")
        return "success"


    def build_phase_2(self):
        if self.head_controller is None:
            self.show_warning("Make sure you've set a head controller!")
            return

        # there's a chance that the user doesn't run the entire script at once
        # so for phase 2 we're just find the curves again by the special attribute they received when they were made
        # It's not the prettiest way, but it works
        self.do_not_touch_group = pm.PyNode("DO_NOT_TOUCH")
        self.side_prefix = str(self.ui.cb_side_prefix.currentText())
        eyelid_deformer_curve_group = pm.PyNode("%s_eyelid_deformer_curve_group" % self.side_prefix)

        high_res_curve_up = None
        high_res_curve_down = None

        low_res_curve_up = None
        low_res_curve_down = None

        for node in pm.ls(type = "transform"):
            if node.hasAttr("eyelidCurve"):
                if "high" in node.eyelidCurve.get() and self.side_prefix in node.eyelidCurve.get():
                    if "up" in node.eyelidCurve.get():
                        high_res_curve_up = node
                    else:
                        high_res_curve_down = node
                if "low" in node.eyelidCurve.get() and self.side_prefix in node.eyelidCurve.get():
                    if "up" in node.eyelidCurve.get():
                        low_res_curve_up = node
                    else:
                        low_res_curve_down = node

        # apply wire deformer to high res curves
        pm.wire(high_res_curve_up, groupWithBase=False, envelope=1, crossingEffect=0, localInfluence=0,
                wire=low_res_curve_up.name())
        pm.wire(high_res_curve_down, groupWithBase=False, envelope=1, crossingEffect=0, localInfluence=0,
                wire=low_res_curve_down.name())


        # make a list of the main lid controllers
        # these are the two controllers in the middle of the upper and lower eyelid that will hold the blink attribute
        main_lid_controllers = []

        # make a list for the constrain controllers
        # these are the controllers on the edge of the eye, and on top and bottom, that are needed to constrain the helper controllers
        # that sit between them
        # 0 = corner at nose, 1 = main controller on top of eye, 2 = corner at outer edge of eye, 3 = main controller at the bottom of eye
        constrain_controllers = []

        # make a list for the constrained groups on the helper controllers
        # these controllers sit between the corners and the main controllers
        # they each have a group called constrained in their hierarchy that we're going to constrain
        # that way we still have a driven group that we can use for automation (like moving the lids when the eye look up, down, left or right)
        # and we can still grab the controller itself to make adjustments
        # 0 = between corner at nose and top main, 1 = between top main and corner at edge
        # 2 = between corner at nose and bottom main, 3 = between bottom main and corner at edge
        helper_constrained_groups = []


        # get the position for the controls joints of the low res curve, skin the low res curves to these joints
        # also create the controllers and have them constrain the joints for the low res curve
        pm.select(None)
        eye_controller_group = pm.group(name = "%s_eye_controller_group" % self.side_prefix)
        pm.select(None)
        eye_controller_joint_group = pm.group(name = "%s_eye_controller_joint_group" % self.side_prefix)
        #eye_controller_joint_group.visibility.set(False)
        control_joints_1 = []

        for index, cv_location in enumerate(low_res_curve_up.getCVs()):
            pm.select(None)
            jnt = pm.joint(name="%s_eyelid_control_joint_%02d" % (self.side_prefix, index), position=cv_location,
                           radius=self.ui.spin_joint_size.value())
            control_joints_1.append(jnt)
            controller = pm.circle(normal = [0, 0, 1], name="%s_eyelid_%02d_controller" % (self.side_prefix, index))[0]
            driven = pm.group(controller, name = controller.name().replace("controller", "driven"))
            constrained = pm.group(driven, name = driven.name().replace("driven", "constrained"))
            offset = pm.group(constrained, name = constrained.replace("constrained", "offset"))
            offset.setTranslation(cv_location)
            offset.setScale((self.joint_radius * 10, self.joint_radius * 10, self.joint_radius * 10))

            if self.ui.chk_flip_controller_orientation.isChecked():
                print "Flipping offset group 180 degrees."
                offset.setRotation([0, 180, 0])

            pm.parentConstraint(controller, jnt, maintainOffset = True)
            pm.parent(offset, eye_controller_group)

            if index == 2:
                main_lid_controllers.append(controller)
                self.lock_and_hide_attributes(controller, ["sx", "sy", "sz"])

            if index == 0 or index == 2 or index == 4:
                constrain_controllers.append(controller)
                self.lock_and_hide_attributes(controller, ["sx", "sy", "sz"])

            if index == 1 or index == 3:
                helper_constrained_groups.append(constrained)
                self.lock_and_hide_attributes(controller, ["sx", "sy", "sz", "rx", "ry", "rz"])

            pm.parent(jnt, eye_controller_joint_group)

        pm.skinCluster(control_joints_1, low_res_curve_up, toSelectedBones=True)


        control_joints_2 = []
        for index, cv_location in enumerate(low_res_curve_down.getCVs()):
            if index == 1 or index == 2 or index == 3:
                pm.select(None)
                jnt = pm.joint(name="%s_eyelid_control_joint_%02d" % (self.side_prefix, index + 5),
                               position=cv_location,
                               radius=self.ui.spin_joint_size.value())
                control_joints_2.append(jnt)
                controller = pm.circle(normal = [0, 0, 1], name="%s_eyelid_%02d_controller" % (self.side_prefix, index + 5))[0]
                driven = pm.group(controller, name = controller.name().replace("controller", "driven"))
                constrained = pm.group(driven, name=driven.name().replace("driven", "constrained"))
                offset = pm.group(constrained, name=constrained.replace("constrained", "offset"))
                offset.setTranslation(cv_location)
                offset.setScale((self.joint_radius * 10, self.joint_radius * 10, self.joint_radius * 10))
                pm.parentConstraint(controller, jnt, maintainOffset=True)
                pm.parent(offset, eye_controller_group)

                if index == 2:
                    main_lid_controllers.append(controller)
                    constrain_controllers.append(controller)
                    self.lock_and_hide_attributes(controller, ["sx", "sy", "sz"])

                if index == 1 or index == 3:
                    helper_constrained_groups.append(constrained)
                    self.lock_and_hide_attributes(controller, ["sx", "sy", "sz", "rx", "ry", "rz"])

                pm.parent(jnt, eye_controller_joint_group)

        pm.skinCluster(control_joints_2, control_joints_1[0], control_joints_1[-1], low_res_curve_down,
                       toSelectedBones=True)

        #constrain the inbetween helper constrain groups to the 4 main controllers on the edges and top and top bottom of the eye
        pm.parentConstraint(constrain_controllers[0], constrain_controllers[1], helper_constrained_groups[0], maintainOffset = True)
        pm.parentConstraint(constrain_controllers[1], constrain_controllers[2], helper_constrained_groups[1], maintainOffset = True)
        pm.parentConstraint(constrain_controllers[0], constrain_controllers[3], helper_constrained_groups[2], maintainOffset = True)
        pm.parentConstraint(constrain_controllers[3], constrain_controllers[2], helper_constrained_groups[3], maintainOffset = True)



        # Blinking
        #

        # set up the blink height
        blink_height_curve = pm.duplicate(low_res_curve_up, name = "%s_blink_height_curve" % self.side_prefix)[0]
        blink_height_blend_shape = pm.blendShape(low_res_curve_down, low_res_curve_up, blink_height_curve, name = "%s_blink_height_shapes" % self.side_prefix)

        for index, controller in enumerate(main_lid_controllers):
            if index == 0:
                self.add_attribute(controller, "blink_height", 0, type="float")
            self.add_attribute(controller, "blink", 0, type="float" )

        pm.connectAttr("%s.blink_height" % main_lid_controllers[0].name(), "%s_blink_height_shapes.%s" % (self.side_prefix, low_res_curve_down.name()))

        reverse_node = pm.createNode("reverse", name = "%s_eye_blink_reverse" % self.side_prefix)
        pm.connectAttr("%s.blink_height" % main_lid_controllers[0].name(), "%s.inputX" % reverse_node.name())
        pm.connectAttr("%s.outputX" % reverse_node.name(), "%s_blink_height_shapes.%s" % (self.side_prefix, low_res_curve_up.name()))


        #set up the blink
        high_res_blink_curve_up = pm.duplicate(high_res_curve_up, name = "%s_up_eyelid_high_blink_curve" % self.side_prefix)[0]
        high_res_blink_curve_down = pm.duplicate(high_res_curve_down, name = "%s_down_eye_high_blink_curve" %self.side_prefix)[0]

        main_lid_controllers[0].blink_height.set(0)
        up_blink_wire_deformer = pm.wire(high_res_blink_curve_up, groupWithBase=False, envelope=1, crossingEffect=0, localInfluence=0,  wire=blink_height_curve.name())[0]
        main_lid_controllers[0].blink_height.set(1)
        low_blink_wire_deformer = pm.wire(high_res_blink_curve_down, groupWithBase=False, envelope=1, crossingEffect=0, localInfluence=0, wire=blink_height_curve.name())[0]
        main_lid_controllers[0].blink_height.set(0)

        up_blink_wire_deformer.setWireScale(0, 0)
        low_blink_wire_deformer.setWireScale(0, 0)

        blink_up_blend_shape = pm.blendShape(high_res_blink_curve_up, high_res_curve_up, name = "%s_up_blink_shapes" % self.side_prefix)
        blink_down_blend_shape = pm.blendShape(high_res_blink_curve_down, high_res_curve_down, name="%s_down_blink_shapes" % self.side_prefix)

        pm.connectAttr("%s.blink" % main_lid_controllers[0], "%s_up_blink_shapes.%s" % (self.side_prefix, high_res_blink_curve_up.name()))
        pm.connectAttr("%s.blink" % main_lid_controllers[1], "%s_down_blink_shapes.%s" % (self.side_prefix, high_res_blink_curve_down.name()))


        pm.parent(eye_controller_group, self.head_controller)

        pm.parent(eye_controller_joint_group, self.do_not_touch_group)

        self.show_success_message("Phase 2 built successfully!")
        return "success"

    def reset(self):
        self.ui.lbl_lid_points_set.setText("Points set: 0")
        self.ui.lbl_center_eye.setText("Center eye:")
        self.ui.lbl_head_joint.setText("Head joint:")
        self.ui.lbl_head_mesh.setText("Head mesh:")
        self.ui.lbl_head_controller.setText("Head controller:")

        self.lid_vertices = []
        self.lower_lid_vertices = []

        self.head_joint = None
        self.head_skin = None
        self.head_controller = None

        self.eyelid_high_res_curve = None
        self.eyelid_low_res_curve = None
        self.joint_radius = 0.03

        self.center_eye_position = None
        self.side_prefix = None
        self.up_down_prefix = None


    def add_joint_to_skin(self, joint, skin):
        pm.skinCluster(skin, edit=True, addInfluence=joint, weight=0, lockWeights=True)
        pm.setAttr("%s.liw" % joint, False)

    def add_attribute(self, node, attribute_name, value, type = "string", min=0, max=1):
        if type == "string":
            node.addAttr(attribute_name, dataType="string")
            node.setAttr(attribute_name, value)
        if type == "float":
            node.addAttr(attribute_name, attributeType="float", minValue=min, maxValue=max, defaultValue=value, keyable=True)

    def lock_and_hide_attributes(self, node, attributes=[]):
        node = pm.PyNode(node)
        for attribute in attributes:
            pm.setAttr("%s.%s" % (node, attribute), lock = True, keyable = False)

    def set_shape_node_color(self, shape_node, color=(0, 0, 0)):
        shape_node.overrideEnabled.set(True)
        shape_node.overrideRGBColors.set(True)
        shape_node.overrideColorRGB.set(color)

    def show_warning(self, warning_message, icon="warning"):
        result = pm.confirmDialog(title='nv Eye Rigger', message=warning_message,
                                  button=["OK"], defaultButton='OK',
                                  cancelButton='OK', dismissString='OK', icon=icon)

    def show_success_message(self, text):
        print "SUCCESS: %s" % text

        pm.inViewMessage(assistMessage=text, backColor=0x0021610B, fadeStayTime=6000, f=True,
                         position="topCenter")


rigger = EyeRiggerWindow()

