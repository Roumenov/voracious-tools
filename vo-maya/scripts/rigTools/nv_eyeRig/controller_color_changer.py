import pymel.core as pm

result = pm.confirmDialog(title='Pick color for shape node', message='Pick color for shape node',
                          button=['Red', 'Blue', 'Yellow', 'Green', 'Cancel'], defaultButton='Cancel',
                          cancelButton='Cancel', dismissString='Cancel')

if not result == "Cancel":
    for obj in pm.selected():
        shape_node = pm.listRelatives(obj, shapes=True)[0]
        shape_node.overrideEnabled.set(1)
        shape_node.overrideRGBColors.set(1)

        if result == "Red":
            shape_node.overrideColorRGB.set(1, 0, 0)
        elif result == "Blue":
            shape_node.overrideColorRGB.set(0, 0, 1)
        elif result == "Yellow":
            shape_node.overrideColorRGB.set(1, 1, 0)
        elif result == "Green":
            shape_node.overrideColorRGB.set(0, 1, 0)
        else:
            pass